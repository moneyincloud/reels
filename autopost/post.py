"""moneyincloud auto-post agent: posts approved reels from queue.yaml to Instagram and YouTube.

Runs on GitHub Actions (cron) or anywhere with Python. No third-party scheduler.

  Instagram : Instagram API with Instagram Login (graph.instagram.com). Instagram has no API scheduling,
              so a reel is published by the run that happens at or just after its time.
  YouTube   : YouTube Data API v3. Uploaded as soon as the entry is approved, set to private with
              publishAt = its time, so YouTube itself releases it on time.

Only entries with `approved: true` are ever posted. What has been posted is recorded in posted.json.

Environment (GitHub secrets):
  IG_USER_ID, IG_ACCESS_TOKEN                     Instagram professional account + long-lived token
  YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN  OAuth client + refresh token (get_youtube_token.py)
  RAW_BASE   public base URL of this folder, e.g. https://raw.githubusercontent.com/moneyincloud/reels/main/autopost
Flags: --dry-run (print what would happen), --only instagram|youtube
"""
import argparse, datetime as dt, json, os, sys, time
from zoneinfo import ZoneInfo

import requests
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
IST = ZoneInfo("Asia/Kolkata")
GRAPH = "https://graph.instagram.com/v23.0"
LATE_LIMIT = dt.timedelta(hours=6)  # never post an Instagram reel more than 6 h after its slot


def log(*a):
    print(dt.datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S IST"), *a, flush=True)


def load_state():
    p = os.path.join(HERE, "posted.json")
    return json.load(open(p)) if os.path.exists(p) else {}


def save_state(st):
    json.dump(st, open(os.path.join(HERE, "posted.json"), "w"), indent=1, ensure_ascii=False)


def when(entry):
    return dt.datetime.strptime(entry["publish_at"], "%Y-%m-%d %H:%M").replace(tzinfo=IST)


# ---------------- Instagram ----------------
def ig_post(entry, dry):
    uid, tok, base = os.environ["IG_USER_ID"], os.environ["IG_ACCESS_TOKEN"], os.environ["RAW_BASE"].rstrip("/")
    params = {"media_type": "REELS", "video_url": f"{base}/media/{entry['video']}", "caption": entry["ig_caption"].strip(),
              "share_to_feed": "true", "access_token": tok}
    if entry.get("cover"):
        params["cover_url"] = f"{base}/media/{entry['cover']}"
    if dry:
        log("DRY instagram container", {k: v for k, v in params.items() if k != "access_token"}); return {"dry": True}
    r = requests.post(f"{GRAPH}/{uid}/media", data=params, timeout=60); r.raise_for_status()
    cid = r.json()["id"]; log("instagram container", cid)
    for _ in range(40):  # up to ~10 min of processing
        time.sleep(15)
        s = requests.get(f"{GRAPH}/{cid}", params={"fields": "status_code,status", "access_token": tok}, timeout=30).json()
        code = s.get("status_code")
        if code == "FINISHED": break
        if code in ("ERROR", "EXPIRED"): raise RuntimeError(f"instagram processing {code}: {s.get('status')}")
    else:
        raise RuntimeError("instagram processing timed out")
    r = requests.post(f"{GRAPH}/{uid}/media_publish", data={"creation_id": cid, "access_token": tok}, timeout=60); r.raise_for_status()
    mid = r.json()["id"]
    info = requests.get(f"{GRAPH}/{mid}", params={"fields": "permalink", "access_token": tok}, timeout=30).json()
    if entry.get("first_comment"):
        c = requests.post(f"{GRAPH}/{mid}/comments", data={"message": entry["first_comment"], "access_token": tok}, timeout=30)
        if not c.ok: log("first comment failed (needs instagram_business_manage_comments):", c.text[:200])
    log("instagram published", info.get("permalink", mid))
    return {"media_id": mid, "permalink": info.get("permalink"), "at": dt.datetime.now(IST).isoformat()}


# ---------------- YouTube ----------------
def yt_service():
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    creds = Credentials(None, refresh_token=os.environ["YT_REFRESH_TOKEN"], token_uri="https://oauth2.googleapis.com/token",
                        client_id=os.environ["YT_CLIENT_ID"], client_secret=os.environ["YT_CLIENT_SECRET"],
                        scopes=["https://www.googleapis.com/auth/youtube.upload"])
    return build("youtube", "v3", credentials=creds, cache_discovery=False)


def yt_post(entry, dry):
    t = when(entry)
    status = {"privacyStatus": "public", "selfDeclaredMadeForKids": False}
    if t > dt.datetime.now(IST) + dt.timedelta(minutes=15):  # let YouTube release it at the slot
        status = {"privacyStatus": "private", "publishAt": t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                  "selfDeclaredMadeForKids": False}
    body = {"snippet": {"title": entry["yt_title"][:100], "description": entry.get("yt_description", "").strip(),
                        "tags": entry.get("yt_tags", []), "categoryId": "27"},  # 27 = Education
            "status": status}
    if dry:
        log("DRY youtube upload", body["snippet"]["title"], status); return {"dry": True}
    from googleapiclient.http import MediaFileUpload
    yt = yt_service()
    req = yt.videos().insert(part="snippet,status", body=body,
                             media_body=MediaFileUpload(os.path.join(HERE, "media", entry["video"]), chunksize=8 * 1024 * 1024, resumable=True))
    resp = None
    while resp is None:
        _, resp = req.next_chunk()
    vid = resp["id"]
    if entry.get("cover"):
        try:
            yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(os.path.join(HERE, "media", entry["cover"]))).execute()
        except Exception as e:  # custom thumbnails need a verified channel
            log("thumbnail skipped:", str(e)[:160])
    log("youtube uploaded", vid, status.get("publishAt", "public now"))
    return {"video_id": vid, "url": f"https://youtube.com/shorts/{vid}", "publish_at": status.get("publishAt"), "at": dt.datetime.now(IST).isoformat()}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--only", choices=["instagram", "youtube"])
    a = ap.parse_args()
    queue = yaml.safe_load(open(os.path.join(HERE, "queue.yaml"))) or []
    st = load_state(); now = dt.datetime.now(IST); failed = False
    for e in queue:
        if not e.get("approved"):
            continue
        key = e["id"]; done = st.setdefault(key, {})
        for plat in e.get("platforms", ["instagram", "youtube"]):
            if a.only and plat != a.only or plat in done:
                continue
            t = when(e)
            if plat == "instagram":
                if now < t: continue
                if now - t > LATE_LIMIT:
                    log(f"{key}: instagram slot missed by more than 6 h, skipped (re-date it in queue.yaml)"); continue
            try:
                res = ig_post(e, a.dry_run) if plat == "instagram" else yt_post(e, a.dry_run)
                if not a.dry_run: done[plat] = res; save_state(st)
            except Exception as ex:
                failed = True; log(f"{key}: {plat} FAILED:", str(ex)[:400])
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
