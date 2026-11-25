"""Comment-to-DM: when someone comments a keyword on a reel, send them ONE private DM (and an optional public reply).

Owner's instruction, 25 Nov 2026: "create the setup how to do comment section of any one comment need to send that set ups".
Rules live in comment_rules.yaml. What has been answered is kept in comment_dm_state.json, so nobody gets two DMs.

Instagram API used (Instagram Login, graph.instagram.com):
  read comments   GET  /{media-id}/comments?fields=id,text,username,timestamp,from   (instagram_business_manage_comments)
  private reply   POST /{ig-user-id}/messages  recipient={"comment_id": ...}        (instagram_business_manage_messages)
  public reply    POST /{comment-id}/replies   message=...                          (instagram_business_manage_comments)
Instagram only allows one private reply per comment, within 7 days of the comment.

Flags: --dry-run (print only, send nothing), --check (read-only: list matching comments, send nothing)
"""
import argparse, datetime as dt, json, os, re, sys, time

import requests
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "comment_dm_state.json")
MAX_PER_RUN = 40            # stay far below Instagram's messaging limits
WINDOW = dt.timedelta(days=7)


def graph():
    tok = os.environ.get("IG_ACCESS_TOKEN", "")
    return "https://graph.facebook.com/v23.0" if tok.startswith("EAA") else "https://graph.instagram.com/v23.0"


def log(*a):
    print(dt.datetime.now(dt.timezone.utc).strftime("%H:%M:%SZ"), *a, flush=True)


def load(p, default):
    return json.load(open(p)) if os.path.exists(p) else default


def media_ids(rule, posted):
    """Which reels a rule watches: queue ids (looked up in posted.json) or raw media ids."""
    out = []
    for ref in rule.get("reels", []):
        ref = str(ref)
        if ref.isdigit():
            out.append(ref); continue
        p = posted.get(ref, {})
        for k in ("instagram", "instagram_trial"):
            if p.get(k, {}).get("media_id"):
                out.append(p[k]["media_id"])
    return out


def matches(text, keywords):
    t = (text or "").upper()
    return any(re.search(r"(?<![A-Z0-9])" + re.escape(k.upper()) + r"(?![A-Z0-9])", t) for k in keywords)


def comments(G, mid, tok):
    url, params = f"{G}/{mid}/comments", {"fields": "id,text,username,timestamp,from", "limit": 50, "access_token": tok}
    while url:
        r = requests.get(url, params=params, timeout=30)
        if not r.ok:
            log("read comments failed", mid, r.text[:200]); return
        j = r.json()
        yield from j.get("data", [])
        url, params = j.get("paging", {}).get("next"), None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    send = not (a.dry_run or a.check)
    G, uid, tok = graph(), os.environ["IG_USER_ID"], os.environ["IG_ACCESS_TOKEN"]
    rules = (yaml.safe_load(open(os.path.join(HERE, "comment_rules.yaml"))) or {}).get("rules", [])
    posted = load(os.path.join(HERE, "posted.json"), {})
    state = load(STATE, {})
    me = requests.get(f"{G}/{uid}", params={"fields": "username", "access_token": tok}, timeout=30).json().get("username", "")
    if not me:
        log("STOP: could not read our own username; refusing to run so we never reply to ourselves"); return 1
    own_texts = {str(e.get("first_comment", "")).strip() for e in (yaml.safe_load(open(os.path.join(HERE, "queue.yaml"))) or [])}
    now, sent = dt.datetime.now(dt.timezone.utc), 0
    for rule in rules:
        if not rule.get("enabled"):
            continue
        done = state.setdefault(rule["id"], {})
        for mid in media_ids(rule, posted):
            for c in comments(G, mid, tok):
                cid, who = c["id"], c.get("username") or c.get("from", {}).get("username", "")
                own = who.lower() == me.lower() or str(c.get("from", {}).get("id", "")) == str(uid) or (c.get("text") or "").strip() in own_texts
                if cid in done or own or not matches(c.get("text"), rule["keywords"]):
                    continue
                ts = dt.datetime.strptime(c["timestamp"], "%Y-%m-%dT%H:%M:%S%z")
                if now - ts > WINDOW:
                    done[cid] = {"skipped": "older than 7 days"}; continue
                if sent >= MAX_PER_RUN:
                    log("per-run cap reached; the rest go next run"); break
                log(("SEND" if send else "WOULD SEND"), rule["id"], "->", "@" + who, repr((c.get("text") or "")[:60]))
                if not send:
                    continue
                r = requests.post(f"{G}/{uid}/messages", timeout=30, json={
                    "recipient": {"comment_id": cid}, "message": {"text": rule["dm"].strip()}}, params={"access_token": tok})
                rec = {"user": who, "at": now.isoformat(), "dm": r.ok}
                if not r.ok:
                    log("DM failed:", r.text[:300])
                    if any(s in r.text.lower() for s in ("permission", '"code":10', '"code":3,', '"code":200')):
                        log("STOP: the token lacks instagram_business_manage_messages; nothing recorded, will retry after the token is fixed")
                        json.dump(state, open(STATE, "w"), indent=1, ensure_ascii=False); return 1
                    rec["error"] = r.text[:200]
                if r.ok and rule.get("public_reply"):
                    pr = requests.post(f"{G}/{cid}/replies", data={"message": rule["public_reply"], "access_token": tok}, timeout=30)
                    rec["public_reply"] = pr.ok
                done[cid] = rec; sent += 1
                time.sleep(2)
    if send:
        json.dump(state, open(STATE, "w"), indent=1, ensure_ascii=False)
    log("done, DMs sent:", sent)


if __name__ == "__main__":
    sys.exit(main())
