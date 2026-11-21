import json
W=json.load(open('studio/penny15_1121/week.json'))
RISK="Low price ≠ cheap. Check market cap, debt and NSE ASM/GSM surveillance lists. Penny stocks are volatile and can hit lower circuits."
def p(v): return ('+' if v>0 else '−')+f'{abs(v):.2f}%'
rows='\n'.join(f"{i+1}. {d['name']} ₹{d['close']:.2f} ({p(d['week_pct'])}, {d['below_hi']:.1f}% vs 1-yr high ₹{d['hi52']:g})" for i,d in enumerate(W))
src="Source: NSE via INDmoney, week ending 20 Nov 2026 (Friday close 20 Nov vs 13 Nov). 52-week highs and market caps: INDmoney, 20 Nov 2026 close."
cap=f"""15 penny stocks this week: only 4 rose, and all 4 are banks 👇

Nifty 500 stocks under ₹50, week of 16–20 Nov 2026, best to worst:
{rows}

All 15 are below their 1-year high. Reliance Power is the furthest, 57.7% under ₹41.75.

⚠️ {RISK}

Send this to the friend who buys anything under ₹50. New list every Saturday.

{src}
Not a buy/sell call. Education only. I may hold some of the stocks named.

#pennystocks #stockmarketindia #nifty500 #moneyincloud"""
ytd=f"""15 penny stocks (Nifty 500, under ₹50) and how they moved in the week of 16–20 Nov 2026. Only 4 rose, all banks: Central Bank +6.67%, Yes Bank +2.81%, UCO Bank +2.33%, Indian Overseas Bank +1.14%. Worst: Vedanta Iron & Steel −9.34%. All 15 are below their 1-year high (Reliance Power −57.7%).

{rows}

{RISK}

{src}
Not a buy/sell call. Education only, not investment advice. I may hold some of the stocks named.
#pennystocks #stockmarketindia #shorts"""
e={'id':'penny15-weekly-2026-11-21','publish_at':'2026-11-21 12:00',
'video':'15-penny-stocks-this-week-india-16-20-nov-2026.mp4','yt_video':'15-penny-stocks-this-week-india-16-20-nov-2026-yt.mp4',
'cover':'15-penny-stocks-this-week-india-16-20-nov-2026-cover.jpg','story':'15-penny-stocks-this-week-india-16-20-nov-2026-story.jpg',
'story_delay_min':60,'ig_caption':cap,'first_comment':"Which of these 15 surprised you most this week? 👇",
'yt_title':"15 Penny Stocks This Week (16–20 Nov 2026): Only 4 Rose, All Banks #shorts",'yt_description':ytd,
'yt_tags':["penny stocks","penny stocks india","penny stocks under 50","nifty 500","stock market this week","central bank of india share","vodafone idea share","yes bank share","reliance power share","moneyincloud"]}
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
open('studio/penny15_1121/entry.yaml','w').write(s); open('studio/penny15_1121/caption.txt','w').write(cap); print(cap)
