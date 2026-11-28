import json
W=json.load(open('studio/penny15_1128/week.json'))
RISK="Low price ≠ cheap. Check market cap, debt and NSE ASM/GSM surveillance lists. Penny stocks are volatile and can hit lower circuits."
def p(v): return ('+' if v>0 else '−')+f'{abs(v):.2f}%'
rows='\n'.join(f"{i+1}. {d['name']} ₹{d['close']:.2f} ({p(d['week_pct'])}, {d['below_hi']:.1f}% vs 1-yr high ₹{d['hi52']:g})" for i,d in enumerate(W))
src="Source: NSE via INDmoney, week ending 27 Nov 2026 (Friday close 27 Nov vs 20 Nov; 4 sessions, 24 Nov market holiday). 52-week highs and market caps: INDmoney, 27 Nov 2026 close."
cap=f"""15 penny stocks this week: last week's 4 winners were all banks. This week all 4 fell 👇

Nifty 500 stocks under ₹50, week of 23–27 Nov 2026, best to worst:
{rows}

Only 4 of 15 rose: Bharat Coking Coal, Vedanta Iron & Steel (last week's worst), Trident and Vedanta Oil & Gas. No bank made the list of risers.
All 15 are below their 1-year high. Reliance Power is the furthest, 58.1% under ₹40.8.

⚠️ {RISK}

Send this to the friend who buys anything under ₹50. New list every Saturday.

Which one surprised you? 👇

{src}
Not a buy/sell call. Education only. I may hold some of the stocks named.

#pennystocks #stockmarketindia #nifty500 #moneyincloud"""
ytd=f"""15 penny stocks (Nifty 500, under ₹50) and how they moved in the week of 23–27 Nov 2026. Only 4 rose: Bharat Coking Coal +2.17%, Vedanta Iron & Steel +1.72% (last week's worst), Trident +1.24%, Vedanta Oil & Gas +0.82%. Last week's 4 risers were all banks; this week all 4 fell (Yes Bank −0.61%, Indian Overseas Bank −3.75%, Central Bank −4.02%, UCO Bank −4.56%). Worst: Tata Teleservices −6.14%. All 15 are below their 1-year high (Reliance Power −58.1%).

{rows}

{RISK}

{src}
Not a buy/sell call. Education only, not investment advice. I may hold some of the stocks named.
#pennystocks #stockmarketindia #shorts"""
e={'id':'penny15-weekly-2026-11-28','publish_at':'2026-11-28 12:00',
'video':'15-penny-stocks-this-week-india-23-27-nov-2026.mp4','yt_video':'15-penny-stocks-this-week-india-23-27-nov-2026-yt.mp4',
'cover':'15-penny-stocks-this-week-india-23-27-nov-2026-cover.jpg','story':'15-penny-stocks-this-week-india-23-27-nov-2026-story.jpg',
'story_delay_min':60,'ig_caption':cap,'first_comment':"Which of these 15 surprised you most this week? 👇",
'yt_title':"15 Penny Stocks This Week (23–27 Nov 2026): Last Week's 4 Winners All Fell #shorts",'yt_description':ytd,
'yt_tags':["penny stocks","penny stocks india","penny stocks under 50","nifty 500","stock market this week","bharat coking coal share","tata teleservices share","vedanta iron and steel share","vodafone idea share","reliance power share","moneyincloud"]}
assert len(e['yt_title'])<=100
J=json.dumps
s=f"""
- id: {e['id']}
  approved: true   # standing order: owner chat 19 Nov 2026 – weekly penny stocks (queued by the Sat 15 Penny Stocks scheduled task)
  publish_at: {e['publish_at']}
  platforms: [youtube, instagram, instagram_trial, instagram_story]
  video: {e['video']}
  yt_video: {e['yt_video']}
  cover: {e['cover']}
  story: {e['story']}
  story_delay_min: 60
  ig_caption: {J(cap,ensure_ascii=False)}
  first_comment: {J(e['first_comment'],ensure_ascii=False)}
  yt_title: {J(e['yt_title'],ensure_ascii=False)}
  yt_description: {J(ytd,ensure_ascii=False)}
  yt_tags: {J(e['yt_tags'],ensure_ascii=False)}
"""
open('studio/penny15_1128/entry.yaml','w').write(s); open('studio/penny15_1128/caption.txt','w').write(cap); print(cap)
