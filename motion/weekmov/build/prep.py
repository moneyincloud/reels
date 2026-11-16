"""Build gain.json / loss.json + TTS lines from the weekly CSVs.  usage: python3 prep.py"""
import csv, json, os, re
H = os.path.dirname(os.path.abspath(__file__))
W = '/home/claude/reels/studio/weekmov/'
IDX = json.load(open(W + 'indices.json'))
SAY = json.load(open(H + '/say.json')) if os.path.exists(H + '/say.json') else {}   # pronunciation fixes: display -> spoken

NAMES = {'Kalyan Jewellers India': 'Kalyan Jewellers', 'Canara HSBC Life Insurance': 'Canara HSBC Life',
         'Tata Teleservices (Maharashtra)': 'Tata Teleservices', 'Schneider Electric Infrastructure': 'Schneider Electric Infra',
         'Deepak Fertilisers & Petrochem': 'Deepak Fertilisers', 'Navin Fluorine International': 'Navin Fluorine',
         'Hitachi Energy India': 'Hitachi Energy', 'Aditya Birla Real Estate': 'Aditya Birla Real Estate',
         'CG Power & Industrial Solutions': 'CG Power', 'Oil & Natural Gas Corpn': 'ONGC', 'Tata Consultancy Services': 'TCS',
         'Fertilizers & Chemicals Travancore': 'FACT', 'Deepak Fertilisers and Petrochemicals Corporation': 'Deepak Fertilisers',
         'Deepak Fertilisers and Petrochemicals Corpn': 'Deepak Fertilisers', 'One 97 Communications': 'Paytm (One 97)',
         'Siemens Energy India': 'Siemens Energy', 'Cummins India': 'Cummins', 'Deepak Fertilisers and Petrochemicals Corp': 'Deepak Fertilisers'}
def clean(n):
    n = re.sub(r'\s+(Ltd\.?|Limited)$', '', n.strip(), flags=re.I).strip(' .,')
    n = re.sub(r'\s+(Corporation|Company|Co\.?)$', '', n, flags=re.I)
    n = n.replace(' (India)', '')
    return NAMES.get(n, n)
def short(n):
    n = clean(n)
    return n if len(n) <= 24 else n[:23].rstrip() + '…'

def load(f):
    rows = [r for r in csv.DictReader(open(W + f)) if r.get('week_pct') not in (None, '', 'nan')]
    for r in rows: r['pct'] = float(r['week_pct']); r['short'] = short(r['name']); r['spk'] = clean(r['name'])
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

P = json.load(open(W + 'period.json'))
WK = P['kind'] == 'week'
THIS = 'this week' if WK else 'in ' + P['month_name'].split()[0]
NEXT = "next week's" if WK else "next month's"
SPAN = f"in just {words(P['sessions'])} trading days" if WK else "in just one month"


G = [('LARGE CAP', 'Nifty 100', 'large.csv', 'Large caps'), ('MIDCAP', 'Nifty Midcap 150', 'mid.csv', 'Midcaps'), ('SMALLCAP', 'Nifty Smallcap 250', 'small.csv', 'Smallcaps')]
data = {g[2]: load(g[2]) for g in G}
n50 = IDX['nifty50']['pct']; m150 = IDX['midcap150']['pct']

for mode in ('gain', 'loss'):
    gain = mode == 'gain'
    groups = []; tts = []; spoken = []
    for lab, sub, f, word in G:
        rows = sorted(data[f], key=lambda r: -r['pct'] if gain else r['pct'])[:10]
        groups.append(dict(label=lab, sub=sub, rows=[dict(name=r['short'], spk=r['spk'], pct=r['pct'], full=r['name'], prev=float(r['prev_week_close']), close=float(r['close'])) for r in rows]))
    allr = [(r, g) for g in groups for r in g['rows']]
    top, tg = max(allr, key=lambda x: x[0]['pct'] if gain else -x[0]['pct'])
    verb = 'jumped' if gain else 'fell'
    spoken.append(f"Top {'gainers' if gain else 'losers'} {THIS}: {top['spk']} {verb} {abs(top['pct']):.1f}% {SPAN}.")
    tts.append(f"Top {'gainers' if gain else 'losers'} {THIS}: {say(top['spk'])} {verb} {pct_words(top['pct'])} {SPAN}.")
    for (lab, sub, f, word), g in zip(G, groups):
        n3 = [r['spk'] for r in g['rows'][:3]]
        lead = 'led the gains' if gain else 'fell the most'
        spoken.append(f"{word}, {sub}: {n3[0]}, {n3[1]} and {n3[2]} {lead}.")
        tts.append(f"{word}, {sub.replace('Nifty', 'Nifty')}: {say(n3[0])}, {say(n3[1])} and {say(n3[2])} {lead}.")
    up = n50 >= 0
    if gain:
        line = f"Meanwhile, the Nifty 50 moved just {abs(n50):.1f}% {THIS}."
        tline = f"Meanwhile, the Nifty fifty moved just {pct_words(n50)} {THIS}."
        ctxl = f"Nifty 50: just <b style='color:#1E8E4E'>{'+' if up else '−'}{abs(n50):.1f}%</b>.<br>These stocks did far more."
    else:
        line = f"And this was a {'week' if WK else 'month'} when the Nifty 50 {'rose' if up else 'fell'} {abs(n50):.1f}%."
        tline = f"And this was a {'week' if WK else 'month'} when the Nifty fifty {'rose' if up else 'fell'} {pct_words(n50)}."
        ctxl = f"Index {'up' if up else 'down'}, these stocks <b style='color:#D93A2B'>down</b>.<br>That's stock risk."
    spoken.append(line); tts.append(tline)
    kw = 'GAIN' if gain else 'LOSS'
    q = 'Which one do you hold?' if gain else 'Did you hold any of these?'
    spoken.append(f"{q} Comment {kw}, and follow for {NEXT} list.")
    tts.append(f"{q} Comment {kw}, and follow for {NEXT} list.")
    D = dict(mode=mode, title=f"Top 10 {'weekly' if WK else 'monthly'} {'gainers' if gain else 'losers'} by market cap",
             kw=f"TOP {'GAINERS' if gain else 'LOSERS'} " + ('THIS WEEK · ' if WK else '· ') + P['range_label'],
             hook_ttl=f"biggest {'jump' if gain else 'fall'} {THIS}", hook2=f"+ top 10 {'gainers' if gain else 'losers'} in<br><b>large · mid · small</b> caps 👇",
             top=dict(name=top['name'], pct=top['pct'], sub=f"{tg['sub']} · ₹{top['prev']:,.2f} → ₹{top['close']:,.2f}"),
             groups=groups, spoken=spoken,
             context=dict(rows=[('Nifty 50', n50), ('Nifty 100', IDX['nifty100']['pct']), ('Nifty Midcap 150', m150)], line=ctxl),
             cta_ttl=q.replace('?', '') + '?', cta_kw=kw,
             disc=f"{'Week' if WK else 'Month'} change: {P['prev_label']} close → {P['end_label']} close · Data: INDmoney · Not a buy/sell call · Education only",
             follow_pill='FOLLOW FOR NEXT ' + ('WEEK' if WK else 'MONTH'), period=P)
    json.dump(D, open(f'{H}/{mode}.json', 'w'), indent=1, ensure_ascii=False)
    d = f'/home/claude/reels/studio/weekmov_{mode}'; os.makedirs(d, exist_ok=True)
    json.dump([dict(who='narrator', text=t) for t in tts], open(d + '/lines.json', 'w'), indent=1, ensure_ascii=False)
    json.dump({'narrator': ['am_michael', 1.08]} if gain else {'narrator': ['af_heart', 1.08]}, open(d + '/voices.json', 'w'))
    print(mode, '| top:', top['name'], top['pct']); [print('  ', s) for s in spoken]
