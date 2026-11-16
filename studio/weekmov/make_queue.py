"""Name the rendered files, copy them to autopost/media and append the two posts to autopost/queue.yaml.

usage: python3 make_queue.py "<gain publish_at>" "<loss publish_at>" "<approval note>"
  e.g. python3 make_queue.py "2026-11-21 07:00" "2026-11-21 09:00" "standing order: owner chat 16 Nov 2026 09:46 IST"
Needs: motion/weekmov/build/{gain,loss}.json (from prep.py), motion/weekmov/renders/{gain,loss}.mp4,
       studio/weekmov/cover/{gain,loss}_{cover,story}.jpg.  Prints the slugs.
"""
import json, shutil, sys

R = '/home/claude/reels/'
gain_at, loss_at, note = sys.argv[1], sys.argv[2], sys.argv[3]
P = json.load(open(R + 'studio/weekmov/period.json'))
WK = P['kind'] == 'week'
MON = P['month_name'].split()[0]
q = lambda s: json.dumps(s, ensure_ascii=False)          # a JSON string is a valid YAML double-quoted scalar
f1 = lambda p: f"{'+' if p > 0 else '−'}{abs(p):.1f}%"
EMO = {'gain': ['🏦', '🚀', '🔥'], 'loss': ['🏦', '⚠️', '🔻']}
CAPN = ['Large cap (Nifty 100)', 'Mid cap (Nifty Midcap 150)', 'Small cap (Nifty Smallcap 250)']
SHORT = ['Large cap', 'Mid cap', 'Small cap']
entries = []
for mode, at in (('gain', gain_at), ('loss', loss_at)):
    D = json.load(open(R + f'motion/weekmov/build/{mode}.json'))
    g = mode == 'gain'; W = 'gainers' if g else 'losers'; WT = W.title()
    when = 'this week' if WK else f'in {MON}'
    slug = (f'top-{W}-this-week-nifty-large-mid-smallcap-{P["end"]}' if WK
            else f'top-{W}-{MON.lower()}-{P["end"][:4]}-nifty-large-mid-smallcap')
    for src, suf in ((f'motion/weekmov/renders/{mode}.mp4', '.mp4'), (f'studio/weekmov/cover/{mode}_cover.jpg', '-cover.jpg'),
                     (f'studio/weekmov/cover/{mode}_story.jpg', '-story.jpg')):
        shutil.copy(R + src, R + f'studio/out/{slug}{suf}'); shutil.copy(R + src, R + f'autopost/media/{slug}{suf}')
    import subprocess
    subprocess.run(['python3', R + 'studio/yt_endcard.py', R + f'autopost/media/{slug}.mp4'], check=True)
    top = D['top']; verb = 'jumped' if g else 'fell'
    span = f"in just {P['sessions']} trading days" if WK else 'in one month'
    lines = []
    for i, gr in enumerate(D['groups']):
        r3 = ', '.join(f"{r['spk']} {f1(r['pct'])}" for r in gr['rows'][:3])
        lines.append((EMO[mode][i], CAPN[i], SHORT[i], r3))
    n50 = D['context']['rows'][0][1]
    ctx = (f"Meanwhile the Nifty 50 moved just {f1(n50)}." if g else
           f"The Nifty 50 {'rose' if n50 >= 0 else 'fell'} {f1(n50)} over the same period." + (" Index up, these stocks down: that's single-stock risk." if n50 >= 0 else ''))
    chg = f"{'Week' if WK else 'Month'} change = {P['prev_label']} close → {P['end_label']} close. Data: INDmoney."
    disc = f"A big {'weekly' if WK else 'monthly'} {'jump' if g else 'fall'} is not a reason to {'buy' if g else 'buy or sell'}. Not a buy/sell call. Education only. I may hold some of the stocks named."
    period_txt = f"({P['range_label'].title() if WK else P['month_name']})"
    cap = [f"Top {W} {when} in the Indian stock market {period_txt} {'📈' if g else '📉'}",
           f"{top['name']} {verb} {abs(top['pct']):.1f}% {span}.", '',
           'Top 3 in each index:' if g else 'Bottom 3 in each index:']
    cap += [f'{e} {c}: {r}' for e, c, _, r in lines]
    cap += ['', ctx + ' Full top 10 lists in the reel.', '',
            f"{D['cta_ttl']} Comment {D['cta_kw']} 👇", f"💾 Save this and follow for next {'week' if WK else 'month'}'s list.", '',
            chg, disc, '',
            f"#StockMarketIndia #Top{WT} #Nifty #{'SmallCap' if g else 'MidCap'} #moneyincloud"]
    title = (f"Top {WT} {'This Week' if WK else 'of ' + P['month_name']}: {top['name']} {f1(top['pct'])} | Nifty 100, Midcap, Smallcap Top 10 #shorts")
    desc = [f"Top 10 {'weekly' if WK else 'monthly'} {W} in the Nifty 100, Nifty Midcap 150 and Nifty Smallcap 250 {period_txt}.",
            f"Biggest {'jump' if g else 'fall'}: {top['name']} {f1(top['pct'])} ({top['sub'].split(' · ')[-1]})."]
    desc += [f'{s}: {r}.' for _, _, s, r in lines]
    desc += [f"Nifty 50 {'this week' if WK else 'this month'}: {f1(n50)}.", chg, 'Not a buy/sell call. Education only. I may hold some of the stocks named.']
    tags = [f"top {W} {'this week' if WK else MON.lower() + ' ' + P['end'][:4]}", 'stock market india', 'nifty 100', 'nifty midcap 150',
            'nifty smallcap 250', f"{'weekly' if WK else 'monthly'} {W}"] + [gr['rows'][0]['spk'].lower() + ' share' for gr in D['groups']] + ['moneyincloud']
    fc = ('Large, mid or small cap: which list surprised you most? 👇' if g else 'Do you average down after a fall like this, or wait? 👇')
    ind = lambda txt: '\n'.join('    ' + l if l else '' for l in txt)
    entries.append(f"""- id: {slug}
  approved: true   # {note}
  publish_at: {at}
  story: {slug}-story.jpg
  story_delay_min: 60
  platforms: [youtube, instagram, instagram_story, instagram_trial]
  video: {slug}.mp4
  yt_video: {slug}-yt.mp4
  cover: {slug}-cover.jpg
  ig_caption: |
{ind(cap)}
  first_comment: {q(fc)}
  yt_title: {q(title[:100])}
  yt_description: |
{ind(desc)}
  yt_tags: {q(tags)}
""")
    print(slug)
qy = R + 'autopost/queue.yaml'
open(qy, 'w').write(open(qy).read().rstrip('\n') + '\n\n' + '\n'.join(entries))
