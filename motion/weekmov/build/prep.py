"""Build gain.json / loss.json + TTS lines from the weekly CSVs.  usage: python3 prep.py"""
import csv, json, os, re
H = os.path.dirname(os.path.abspath(__file__))
W = '/home/claude/reels/studio/weekmov/'
IDX = json.load(open(W + 'indices.json'))
SAY = json.load(open(H + '/say.json')) if os.path.exists(H + '/say.json') else {}   # pronunciation fixes: display -> spoken

def short(n):
    n = re.sub(r'\b(Ltd\.?|Limited|Corporation|Company|Co\.?|Industries Ltd)\s*$', '', n.strip(), flags=re.I).strip(' .,')
    n = re.sub(r'\s+(Ltd\.?|Limited)$', '', n, flags=re.I)
    n = n.replace(' (India)', '').replace(' India Ltd', '').replace(' & ', ' & ')
    return n if len(n) <= 22 else n[:21].rstrip() + '…'

def load(f):
    rows = [r for r in csv.DictReader(open(W + f)) if r.get('week_pct') not in (None, '', 'nan')]
    for r in rows: r['pct'] = float(r['week_pct']); r['short'] = short(r['name'])
    return rows

ONES = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split()
TENS = 'zero ten twenty thirty forty fifty sixty seventy eighty ninety'.split()
def words(n):
    n = int(n)
    if n < 20: return ONES[n]
    if n < 100: return TENS[n // 10] + ('' if n % 10 == 0 else ' ' + ONES[n % 10])
    return ONES[n // 100] + ' hundred' + ('' if n % 100 == 0 else ' and ' + words(n % 100))
def pct_words(p):
    p = abs(round(p, 1)); a = int(p); b = int(round((p - a) * 10))
    return words(a) + (f' point {ONES[b]}' if b else '') + ' percent'
def say(n): return SAY.get(n, n)

G = [('LARGE CAP', 'Nifty 100', 'large.csv', 'Large caps'), ('MIDCAP', 'Nifty Midcap 150', 'mid.csv', 'Midcaps'), ('SMALLCAP', 'Nifty Smallcap 250', 'small.csv', 'Smallcaps')]
data = {g[2]: load(g[2]) for g in G}
n50 = IDX['nifty50']['pct']; m150 = IDX['midcap150']['pct']

for mode in ('gain', 'loss'):
    gain = mode == 'gain'
    groups = []; tts = []; spoken = []
    for lab, sub, f, word in G:
        rows = sorted(data[f], key=lambda r: -r['pct'] if gain else r['pct'])[:10]
        groups.append(dict(label=lab, sub=sub, rows=[dict(name=r['short'], pct=r['pct'], full=r['name'], prev=float(r['prev_week_close']), close=float(r['close'])) for r in rows]))
    allr = [(r, g) for g in groups for r in g['rows']]
    top, tg = max(allr, key=lambda x: x[0]['pct'] if gain else -x[0]['pct'])
    verb = 'jumped' if gain else 'fell'
    spoken.append(f"Top {'gainers' if gain else 'losers'} this week: {top['name']} {verb} {abs(top['pct']):.1f}% in just five days.")
    tts.append(f"Top {'gainers' if gain else 'losers'} this week: {say(top['name'])} {verb} {pct_words(top['pct'])} in just five days.")
    for (lab, sub, f, word), g in zip(G, groups):
        n3 = [r['name'] for r in g['rows'][:3]]
        lead = 'led the gains' if gain else 'fell the most'
        spoken.append(f"{word}, {sub}: {n3[0]}, {n3[1]} and {n3[2]} {lead}.")
        tts.append(f"{word}, {sub.replace('Nifty', 'Nifty')}: {say(n3[0])}, {say(n3[1])} and {say(n3[2])} {lead}.")
    up = n50 >= 0
    if gain:
        line = f"Meanwhile, the Nifty 50 moved just {abs(n50):.1f}% this week."
        tline = f"Meanwhile, the Nifty fifty moved just {pct_words(n50)} this week."
        ctxl = f"Nifty 50: just <b style='color:#1E8E4E'>{'+' if up else '−'}{abs(n50):.1f}%</b>.<br>These stocks did far more."
    else:
        line = f"And this was a week when the Nifty 50 {'rose' if up else 'fell'} {abs(n50):.1f}%."
        tline = f"And this was a week when the Nifty fifty {'rose' if up else 'fell'} {pct_words(n50)}."
        ctxl = f"Index {'up' if up else 'down'}, these stocks <b style='color:#D93A2B'>down</b>.<br>That's stock risk."
    spoken.append(line); tts.append(tline)
    kw = 'GAIN' if gain else 'LOSS'
    q = 'Which one do you hold?' if gain else 'Did you hold any of these?'
    spoken.append(f"{q} Comment {kw}, and follow for next week's list.")
    tts.append(f"{q} Comment {kw}, and follow for next week's list.")
    D = dict(mode=mode, title=f"Top 10 weekly {'gainers' if gain else 'losers'} by market cap",
             kw=f"TOP {'GAINERS' if gain else 'LOSERS'} THIS WEEK · 9–13 NOV",
             hook_ttl=f"biggest {'jump' if gain else 'fall'} this week", hook2=f"+ top 10 {'gainers' if gain else 'losers'} in<br><b>large · mid · small</b> caps 👇",
             top=dict(name=top['name'], pct=top['pct'], sub=f"{tg['sub']} · ₹{top['prev']:,.2f} → ₹{top['close']:,.2f}"),
             groups=groups, spoken=spoken,
             context=dict(rows=[('Nifty 50', n50), ('Nifty 100', IDX['nifty100']['pct']), ('Nifty Midcap 150', m150)], line=ctxl),
             cta_ttl=q.replace('?', '') + '?', cta_kw=kw,
             disc='Week change: 6 Nov close → 13 Nov close · Data: INDmoney · Not a buy/sell call · Education only')
    json.dump(D, open(f'{H}/{mode}.json', 'w'), indent=1, ensure_ascii=False)
    d = f'/home/claude/reels/studio/weekmov_{mode}'; os.makedirs(d, exist_ok=True)
    json.dump([dict(who='narrator', text=t) for t in tts], open(d + '/lines.json', 'w'), indent=1, ensure_ascii=False)
    json.dump({'narrator': ['am_michael', 1.08]} if gain else {'narrator': ['af_heart', 1.08]}, open(d + '/voices.json', 'w'))
    print(mode, '| top:', top['name'], top['pct']); [print('  ', s) for s in spoken]
