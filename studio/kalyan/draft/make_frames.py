"""Draft storyboard frames for the Kalyan Jewellers reel ("Royal Gold" template). Writes f1..f8.html."""
import json, re, os
D = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(D, '..', 'maps')
F = '/home/claude/reels/motion/firstcry/assets/fonts'
india = open(os.path.join(M, 'node_modules/@svg-maps/india/india.svg')).read()
india_paths = ''.join(re.findall(r'<path[\s\S]*?/>', india))
world = open(os.path.join(M, 'world.svg')).read()
world_paths = re.search(r'<svg[^>]*>([\s\S]*)</svg>', world).group(1).replace('id="win"', 'id="win" style="display:none"')
P = json.load(open(os.path.join(M, 'world_pts.json')))

HEAD = f'''<html><head><meta charset="utf-8"><style>
@font-face{{font-family:A;src:url({F}/anton-latin-400-normal.woff)}}
@font-face{{font-family:P;src:url({F}/Poppins-Bold.ttf)}}
@font-face{{font-family:PF;src:url({F}/playfair-display-latin-700-italic.woff)}}
@font-face{{font-family:O;src:url({F}/oswald-latin-500-normal.woff)}}
body{{margin:0;width:1080px;height:1920px;overflow:hidden;position:relative;font-family:P;color:#FFF4DC;
 background:radial-gradient(120% 80% at 50% 30%,#6B1328 0%,#3A0816 55%,#22040C 100%)}}
body:before{{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(246,210,122,.10) 2px,transparent 2.5px);background-size:52px 52px}}
.gold{{background:linear-gradient(180deg,#FFE7A3,#E8B64C 55%,#B07A22);-webkit-background-clip:text;color:transparent}}
.t{{position:absolute;left:0;right:0;text-align:center}}
.h{{position:absolute;left:40px;top:56px;padding:8px 22px;border:2px solid rgba(246,210,122,.5);border-radius:999px;font-family:O;font-size:30px;color:#F6D27A}}
.card{{position:absolute;border-radius:30px;background:linear-gradient(160deg,rgba(255,244,220,.10),rgba(255,244,220,.04));border:2px solid rgba(246,210,122,.45);box-shadow:0 20px 50px rgba(0,0,0,.35)}}
.pill{{position:absolute;border-radius:999px;padding:12px 36px;font-family:P;white-space:nowrap;color:#3A0816;background:linear-gradient(135deg,#FFE7A3,#E8B64C);box-shadow:0 10px 26px rgba(0,0,0,.35)}}
.cap{{position:absolute;left:0;right:0;top:1170px;text-align:center}}
.cap span{{display:inline-block;max-width:930px;padding:12px 36px;border-radius:999px;background:rgba(20,2,8,.75);border:2px solid #E8B64C;font-size:40px;line-height:1.2;font-size:36px}}
.disc{{position:absolute;left:40px;right:40px;top:1322px;text-align:center;font-family:O;font-size:28px;color:#D9C29A}}
.tag{{position:absolute;left:40px;top:120px;font-family:O;font-size:30px;color:#3A0816;background:#F6D27A;padding:4px 16px;border-radius:8px}}
</style></head><body><div class="h">@moneyincloud</div>'''
DISC = '<div class="disc">Data: Kalyan Jewellers Q2 FY27 results &amp; investor presentation (10 Nov 2026) · Education only, not a buy/sell call · I may hold some stocks named</div>'
def page(n, body, cap):
    return HEAD + f'<div class="tag">DRAFT · FRAME {n}</div>' + body + f'<div class="cap"><span>{cap}</span></div>' + DISC + '</body></html>'

frames = {}
frames[1] = page(1, '''
<div class="t" style="top:230px;font-family:PF;font-size:70px;color:#F6D27A">3 months. 1 jeweller.</div>
<div class="t gold" style="top:330px;font-family:A;font-size:230px;line-height:1">₹427 cr</div>
<div class="t" style="top:580px;font-size:50px">profit · ▲ 64%</div>
<div class="t" style="top:700px;font-size:300px;line-height:1">💍</div>
<div class="pill" style="left:250px;top:1050px;font-size:56px">546 showrooms 🌍</div>''',
    'This jeweller made ₹427 crore profit in just 3 months.')
frames[2] = page(2, f'''
<div class="t" style="top:200px;font-family:PF;font-size:76px" ><span class="gold">Where it began</span></div>
<svg style="position:absolute;left:250px;top:330px;width:580px;height:660px" viewBox="0 0 612 696">
<g fill="rgba(255,244,220,.10)" stroke="#E8B64C" stroke-width="1.2">{india_paths}</g>
<style>#kl{{fill:#E8B64C}}</style></svg>
<div style="position:absolute;left:418px;top:900px;font-size:90px">📍</div>
<div class="card" style="left:560px;top:880px;width:440px;height:200px;padding:22px 30px"><div class="gold" style="font-family:A;font-size:84px;line-height:1">THRISSUR</div><div style="font-size:36px">Kerala · since 1993</div></div>''',
    'It started with one showroom in Thrissur, Kerala, in 1993.')
frames[3] = page(3, f'''
<div class="t" style="top:190px;font-family:A;font-size:96px"><span class="gold">India: 504 stores</span></div>
<svg style="position:absolute;left:20px;top:320px;width:620px;height:700px" viewBox="0 0 612 696">
<g fill="rgba(255,244,220,.12)" stroke="#E8B64C" stroke-width="1.2">{india_paths}</g></svg>
<div class="card" style="left:640px;top:380px;width:400px;height:190px;padding:20px 26px"><div class="gold" style="font-family:A;font-size:96px;line-height:1">365</div><div style="font-size:32px">Kalyan showrooms</div></div>
<div class="card" style="left:640px;top:600px;width:400px;height:190px;padding:20px 26px"><div class="gold" style="font-family:A;font-size:96px;line-height:1">138</div><div style="font-size:32px">Candere stores</div></div>
<div class="card" style="left:640px;top:820px;width:400px;height:190px;padding:20px 26px"><div class="gold" style="font-family:A;font-size:96px;line-height:1">1</div><div style="font-size:30px">Akshaya Thanga Maligai</div></div>
<div class="t" style="top:1060px;font-size:30px;color:#D9C29A">✨ animated: gold dots light up across the states</div>''',
    'Today: 365 Kalyan showrooms and 138 Candere stores across India.')
x0, y0 = 680, 249
pins = ''.join(f'<circle cx="{P[k][0]}" cy="{P[k][1]}" r="5" fill="#FFE7A3" stroke="#3A0816" stroke-width="1.5"/>' for k in ['ae', 'qa', 'kw', 'om', 'us', 'gb'])
arcs = ''.join(f'<path d="M{P["in"][0]},{P["in"][1]} Q{(P["in"][0]+P[k][0])/2},{min(P["in"][1],P[k][1])-90} {P[k][0]},{P[k][1]}" fill="none" stroke="#FFE7A3" stroke-width="2" stroke-dasharray="6 5"/>' for k in ['ae', 'us', 'gb'])
frames[4] = page(4, f'''
<div class="t" style="top:200px;font-family:A;font-size:96px"><span class="gold">Abroad: 42 stores</span></div>
<svg style="position:absolute;left:-60px;top:330px;width:1200px;height:672px" viewBox="0 0 1000 560">
<g fill="rgba(255,244,220,.10)" stroke="rgba(246,210,122,.35)" stroke-width=".5">{world_paths}</g>
<style>.h{{fill:rgba(232,182,76,.85)}}</style>
<svg x="{x0}" y="{y0}" width="84" height="99" viewBox="0 0 612 696" preserveAspectRatio="none"><g fill="#E8B64C">{india_paths}</g></svg>
{arcs}{pins}</svg>
<div class="pill" style="left:240px;top:930px;font-size:38px;text-align:center">Middle East · 38<br><span style="font-size:28px">🇦🇪 UAE · 🇶🇦 Qatar · 🇰🇼 Kuwait · 🇴🇲 Oman</span></div>
<div class="pill" style="left:90px;top:470px;font-size:38px">🇺🇸 USA · 2</div>
<div class="pill" style="left:380px;top:390px;font-size:38px">🇬🇧 UK · 2</div>''',
    'Abroad: 38 in the UAE, Qatar, Kuwait and Oman, plus 2 in the USA and 2 in the UK.')
frames[5] = page(5, '''
<div class="t" style="top:200px;font-family:PF;font-size:76px"><span class="gold">The profit check</span></div>
<div class="t" style="top:300px;font-size:38px;color:#D9C29A">July–September 2026 vs a year ago</div>
<div class="card" style="left:70px;top:390px;width:460px;height:620px;padding:24px 30px"><div style="font-size:42px">Revenue</div>
<div style="position:absolute;left:50px;bottom:120px;width:150px;height:300px;border-radius:20px 20px 6px 6px;background:rgba(255,244,220,.25)"></div>
<div style="position:absolute;right:50px;bottom:120px;width:150px;height:394px;border-radius:20px 20px 6px 6px;background:linear-gradient(180deg,#FFE7A3,#B07A22)"></div>
<div style="position:absolute;left:30px;bottom:30px;width:190px;text-align:center;font-size:30px">₹7,856 cr</div><div style="position:absolute;right:30px;bottom:30px;width:190px;text-align:center;font-size:30px">₹10,323 cr</div>
<div class="pill" style="right:24px;top:20px;font-size:36px;padding:6px 20px">▲ 31%</div></div>
<div class="card" style="left:550px;top:390px;width:460px;height:620px;padding:24px 30px"><div style="font-size:42px">Profit</div>
<div style="position:absolute;left:50px;bottom:120px;width:150px;height:240px;border-radius:20px 20px 6px 6px;background:rgba(255,244,220,.25)"></div>
<div style="position:absolute;right:50px;bottom:120px;width:150px;height:394px;border-radius:20px 20px 6px 6px;background:linear-gradient(180deg,#FFE7A3,#B07A22)"></div>
<div style="position:absolute;left:30px;bottom:30px;width:190px;text-align:center;font-size:30px">₹261 cr</div><div style="position:absolute;right:30px;bottom:30px;width:190px;text-align:center;font-size:30px">₹427 cr</div>
<div class="pill" style="right:24px;top:20px;font-size:36px;padding:6px 20px">▲ 64%</div></div>
<div class="t" style="top:1050px;font-size:32px;color:#F6D27A">⚠️ includes a one-time ₹73.5 cr land-sale gain</div>''',
    'Revenue up 31% to ₹10,323 crore. Profit up 64% to ₹427 crore.')
frames[6] = page(6, '''
<div class="t" style="top:200px;font-family:PF;font-size:76px"><span class="gold">Where the money comes from</span></div>
<div class="card" style="left:70px;right:70px;top:360px;height:300px;padding:26px 36px"><div style="font-size:46px">🇮🇳 India</div>
<div style="position:absolute;left:36px;top:110px;font-size:34px;color:#D9C29A">Revenue</div><div class="gold" style="position:absolute;left:36px;top:150px;font-family:A;font-size:100px">₹9,007 cr</div>
<div style="position:absolute;right:36px;top:110px;font-size:34px;color:#D9C29A">Profit</div><div class="gold" style="position:absolute;right:36px;top:150px;font-family:A;font-size:100px">₹424 cr</div></div>
<div class="card" style="left:70px;right:70px;top:700px;height:300px;padding:26px 36px"><div style="font-size:46px">🌍 Middle East</div>
<div style="position:absolute;left:36px;top:110px;font-size:34px;color:#D9C29A">Revenue</div><div style="position:absolute;left:36px;top:150px;font-family:A;font-size:100px">₹960 cr</div>
<div style="position:absolute;right:36px;top:110px;font-size:34px;color:#D9C29A">Profit</div><div style="position:absolute;right:36px;top:150px;font-family:A;font-size:100px;color:#FF9C8A">₹12 cr</div></div>
<div class="t" style="top:1040px;font-size:36px">India brings in almost all of the profit</div>''',
    'India: ₹9,007 crore revenue, ₹424 crore profit. Middle East: ₹960 crore, but just ₹12 crore profit.')
frames[7] = page(7, '''
<div class="t" style="top:200px;font-family:PF;font-size:76px"><span class="gold">The growth trick</span></div>
<div class="card" style="left:70px;right:70px;top:340px;height:330px;padding:28px 36px;text-align:center"><div style="font-size:120px;line-height:1.1">🤝🏪</div>
<div style="font-size:48px">Franchise showrooms</div><div style="font-size:34px;color:#D9C29A">partners fund the store and its gold stock, Kalyan runs it</div></div>
<div class="card" style="left:70px;top:710px;width:460px;height:300px;padding:28px;text-align:center"><div class="gold" style="font-family:A;font-size:120px;line-height:1">~59%</div><div style="font-size:32px">of revenue from franchise stores</div></div>
<div class="card" style="left:550px;top:710px;width:460px;height:300px;padding:28px;text-align:center"><div class="gold" style="font-family:A;font-size:120px;line-height:1">+134</div><div style="font-size:32px">planned: 84 Kalyan + 50 Candere (H2)</div></div>''',
    'Its trick: franchise showrooms. Partners fund the store and its stock, so Kalyan grows faster with less of its own money.')
frames[8] = page(8, '''
<div class="t" style="top:220px;font-family:PF;font-size:80px"><span class="gold">Would you buy…</span></div>
<div class="card" style="left:80px;top:400px;width:400px;height:330px;text-align:center;padding-top:30px"><div style="font-size:150px;line-height:1.2">💍</div><div style="font-size:44px">the gold</div></div>
<div class="t" style="top:520px;font-family:PF;font-size:80px;color:#F6D27A">or</div>
<div class="card" style="right:80px;top:400px;width:400px;height:330px;text-align:center;padding-top:30px"><div style="font-size:150px;line-height:1.2">📈</div><div style="font-size:44px">the jeweller</div></div>
<div class="pill" style="left:240px;top:850px;font-size:52px">💬 Comment below</div>
<div class="pill" style="left:280px;top:980px;font-size:50px">➕ Follow for more</div>''',
    'Would you buy the gold, or the jeweller? Comment below, and follow for more.')
for n, h in frames.items():
    open(os.path.join(D, f'f{n}.html'), 'w').write(h)
print('ok', len(frames))
