"""Scenes for the 23 Nov 2026 Monday IPO reel: Foodlink F&B Holdings + Integris Medtech (open 26/27 Nov).
Facts: Foodlink RHP & Integris DRHP summaries via chittorgarh.com (updated 20 Nov 2026), multibagg.ai RHP note (20 Nov),
newboard.in DRHP study (15 Nov); dates also goodreturns.in (22 Nov 2026). No GMP. NO subtitles (owner's rule)."""
from mapgen import svg as mapsvg, P
CAPTXT = []
BG = ['#EFE7FF', '#FFF1B8', '#FFE2D1', '#E6E0FF', '#FFF7E0', '#D7F5E9', '#DDF0FF', '#FFF7E0', '#EFE7FF']
INK = '#1B1B1F'; GRN = '#1E8E4E'; RED = '#D93A2B'; PUR = '#6B3FD4'; YEL = '#FFE45C'; ORG = '#F08A24'; TEAL = '#11A3A3'

def pin(cls, lon, lat, sc, ox, oy, emo, pid, lab=''):
    x, y = P(lon, lat); x = ox + x * sc; y = oy + y * sc
    l = f'<b>{lab}</b>' if lab else ''
    return f'<div class="pin" id="{pid}" style="left:{x - 30:.0f}px;top:{y - 62:.0f}px">{emo}{l}</div>'

EVENTS = ['CHE', 'TUR', 'ITA', 'ESP', 'FRA', 'OMN', 'QAT', 'EGY', 'JOR', 'THA', 'NGA', 'GBR', 'MYS', 'ARE']
SCN = {}
SCN[0] = f'''<div class="big" id="h2" style="left:150px;top:230px;font-size:560px;color:{PUR}">2</div>
<div class="big" id="hipo" style="left:470px;top:330px;font-size:230px">IPOs</div>
<div class="stk" id="hwk" style="left:470px;top:600px;background:{YEL};transform:rotate(-3deg);font-size:64px">OPEN THIS WEEK</div>
<div class="pill" id="hmis" style="left:120px;top:860px;background:{RED};font-size:78px;transform:rotate(-2deg)">YOUR MISTAKE?</div>
<div class="card qc" id="hq0" style="left:90px;top:1080px;background:#FFF1B8"><div class="e">🍽️</div><b>what do they sell?</b></div>
<div class="card qc" id="hq1" style="left:560px;top:1080px;background:#DDF0FF"><div class="e">🫀</div><b>what do they sell?</b></div>'''

DAYS = [('MON', 23), ('TUE', 24), ('WED', 25), ('THU', 26), ('FRI', 27)]
SCN[1] = '<div class="ttl hand" style="top:200px">This week</div>\n' + '\n'.join(
    f'<div class="day" id="d{k}" style="left:{40 + k * 202}px;top:360px"><span>{d}</span><b>{n}</b><i>NOV</i></div>' for k, (d, n) in enumerate(DAYS)) + f'''
<div class="card ipo" id="pf" style="left:330px;top:720px;background:#FFF1B8"><div class="e">🍽️</div><b>Foodlink F&amp;B</b><span>opens Thu 26 Nov<br>closes Mon 30 Nov</span></div>
<div class="card ipo" id="pi" style="left:600px;top:1090px;background:#DDF0FF"><div class="e">🫀</div><b>Integris Medtech</b><span>opens Fri 27 Nov<br>closes Tue 1 Dec</span></div>
<div class="chipx" id="nse" style="left:40px;top:1150px">NSE + BSE<br><small>mainboard</small></div>
<div class="note" style="left:40px;right:40px;top:1470px;text-align:center">Dates: chittorgarh.com (updated 20 Nov) · goodreturns (22 Nov 2026) · Integris dates as reported</div>'''

SCN[2] = f'''<div class="card" id="pbc" style="left:90px;right:90px;top:300px;padding:40px 30px;text-align:center">
<div style="font-family:Oswald;font-size:54px;color:#55556A">PRICE BAND</div>
<div class="big" style="position:relative;font-size:170px">₹ ??? – ???</div></div>
<div class="stk" id="nout" style="left:230px;top:700px;background:{RED};color:#fff;transform:rotate(-6deg);font-size:80px">NOT OUT YET</div>
<div class="note" id="asof" style="left:0;right:0;top:900px;text-align:center;font-size:36px">as of 23 Nov 2026, 7 am IST · lot size also not announced</div>
<div class="ring" id="ring" style="top:1010px"><span id="qq">?</span></div>
<div class="pill" id="bfirst" style="left:180px;top:1260px;background:{PUR};font-size:80px;transform:rotate(-2deg)">🔍 BUSINESS FIRST</div>'''

wa_fill = {a: ORG for a in EVENTS}
SCN[3] = f'''<div class="ttl hand" style="top:200px;font-size:100px">But here's the twist</div>
<div id="mapA" style="position:absolute;left:40px;top:380px;width:1000px;height:478px">{mapsvg({}, 'wa')}</div>
<div class="cnt" id="k15" style="left:60px;top:930px;background:#FFE2C2"><b><span id="n15">0</span></b><span>countries where Foodlink<br>catered events</span></div>
<div class="cnt" id="k65" style="left:560px;top:930px;background:#CFF3F1"><b><span id="n65">0</span>+</b><span>markets Integris<br>supplies to</span></div>
<div class="note" style="left:40px;right:40px;top:1290px;text-align:center">Orange = event countries named in Foodlink's RHP · Integris: "65+ international markets" (DRHP)</div>'''

wb_fill = {'IND': PUR, 'ARE': PUR, 'GBR': PUR, 'MYS': PUR}
SB = 0.94; OBX = 30; OBY = 330
PRODS_F = [('🥡', 'China Bistro'), ('🍛', 'India Bistro'), ('🍲', 'Art of Dum'), ('💍', 'Weddings &amp; events')]
SCN[4] = f'''<div class="tag" style="top:190px">1/2</div><div class="ttl hand" style="top:195px">🍽️ Foodlink F&amp;B</div>
<div id="mapB" style="position:absolute;left:{OBX}px;top:{OBY}px;width:1000px;height:478px;transform:scale({SB});transform-origin:0 0">{mapsvg({}, 'wb')}</div>
{pin('wb', 72.8, 19.1, SB, OBX, OBY, '📍', 'pbm', 'Mumbai HQ')}
{pin('wb', 55.3, 25.2, SB, OBX - 90, OBY - 10, '📍', 'pbu', 'UAE')}
<div class="chipx" id="f4c" style="left:560px;top:330px;font-size:34px">operates in <b>4</b> countries</div>
''' + '\n'.join(f'<div class="card prod" id="fp{k}" style="left:{40 + k * 252}px;top:830px"><div class="e">{e}</div><b>{n}</b></div>' for k, (e, n) in enumerate(PRODS_F)) + f'''
<div class="card" id="f28" style="left:60px;right:60px;top:1120px;height:330px;padding:20px 30px">
<div style="font-family:Anton;font-size:130px;line-height:1;color:{PUR};display:inline-block"><span id="n28">0</span></div>
<div style="display:inline-block;vertical-align:top;margin:14px 0 0 20px;font-family:Poppins;font-weight:700;font-size:38px;line-height:1.15">restaurants &amp;<br>cloud kitchens</div>
<div class="split"><div id="sIN" style="width:{15/28*100:.1f}%;background:#B9A6F2">India 15</div><div id="sAE" style="width:{13/28*100:.1f}%;background:{ORG}">UAE 13</div></div></div>
<div class="note" style="left:40px;right:40px;top:1470px;text-align:center">RHP data as of 30 Sep 2026 · 4 countries: India, UAE, UK, Malaysia · brands are the company's own</div>'''

PROF = [('FY24', -15.35), ('FY25', 14.26), ('FY26', 29.11), ('Apr–Sep 26', -16.15)]
BASE = 820; SCL = 9.0
def pbars():
    o = []
    for k, (l, v) in enumerate(PROF):
        h = abs(v) * SCL; x = 90 + k * 235
        top = BASE - h if v > 0 else BASE
        c = GRN if v > 0 else RED
        o.append(f'<div class="pb" id="pb{k}" style="left:{x}px;top:{top:.0f}px;height:{h:.0f}px;background:{c};transform-origin:50% {"100%" if v > 0 else "0%"}"></div>')
        vy = top - 70 if v > 0 else top + h + 8
        o.append(f'<div class="pv" id="pv{k}" style="left:{x - 30}px;top:{vy:.0f}px;color:{c}">{"+" if v > 0 else "−"}₹{abs(v):.1f} cr</div>')
        ly = BASE + 14 if v > 0 else BASE - 60
        o.append(f'<div class="pl" style="left:{x - 30}px;top:{ly}px">{l}</div>')
    return '\n'.join(o)
SCN[5] = f'''<div class="tag" style="top:190px">1/2</div><div class="ttl hand" style="top:195px">Foodlink: the numbers</div>
<div class="chipx" id="frev" style="left:120px;top:320px">FY26 revenue <b>₹<span id="nrev">0</span> cr</b></div>
<div class="note" style="left:90px;top:440px;font-size:34px;color:{INK}">Profit / loss (₹ crore)</div>
<div id="base" style="position:absolute;left:60px;right:60px;top:{BASE - 3}px;height:6px;background:{INK}"></div>
{pbars()}
<div class="stk" id="lossst" style="left:90px;top:500px;background:{RED};color:#fff;transform:rotate(-5deg);font-size:50px">APR–SEP: LOSS</div>
<div class="card" id="fipo" style="left:70px;right:70px;top:1110px;padding:24px 30px;background:#fff">
<div style="font-family:Oswald;font-size:40px;color:#55556A">THE IPO</div>
<div style="font-family:Anton;font-size:76px;line-height:1.1">₹192 cr <span style="font-size:48px">fresh issue</span></div>
<div id="fofs" style="font-family:Poppins;font-weight:700;font-size:42px">+ offer for sale: 88.35 lakh shares</div></div>
<div class="note" style="left:40px;right:40px;top:1470px;text-align:center">Foodlink RHP via chittorgarh.com &amp; multibagg.ai (20 Nov 2026) · FY ends March · Apr–Sep 2026 not annualised</div>'''

wc_fill = {'IND': TEAL, 'DEU': TEAL, 'NLD': TEAL}
SC6 = 0.94; OCX = 30; OCY = 620
PRODS_I = [('🫀', 'Heart stents'), ('🎈', 'Coronary balloons'), ('🧪', 'Lab diagnostics'), ('🔬', 'Lab equipment')]
SCN[6] = f'''<div class="panel" style="left:0">
<div class="tag" style="top:190px">2/2</div><div class="ttl hand" style="top:195px">🫀 Integris Medtech</div>
''' + '\n'.join(f'<div class="card prod" id="ip{k}" style="left:{40 + k * 252}px;top:330px"><div class="e">{e}</div><b>{n}</b></div>' for k, (e, n) in enumerate(PRODS_I)) + f'''
<div id="mapC" style="position:absolute;left:{OCX}px;top:{OCY}px;width:1000px;height:478px;transform:scale({SC6});transform-origin:0 0">{mapsvg({}, 'wc')}</div>
{pin('wc', 77, 21, SC6, OCX, OCY, '🏭', 'fin', 'India')}
{pin('wc', 10.5, 50.5, SC6, OCX, OCY, '🏭', 'fde', 'Germany')}
{pin('wc', 4.9, 52.3, SC6, OCX - 70, OCY - 60, '🏭', 'fnl', 'Netherlands')}
<div class="chipx" id="imade" style="left:150px;top:1120px">factories in <b>3</b> countries</div>
<div class="note" style="left:40px;right:40px;top:1470px;text-align:center">DRHP via chittorgarh.com (updated 20 Nov 2026) · symbols are illustrations</div></div>
<div class="panel" style="left:1080px">
<div class="tag" style="top:190px">2/2</div><div class="ttl hand" style="top:195px">Integris: the numbers</div>
<div class="chipx" id="irev" style="left:120px;top:320px">FY25 revenue <b>₹<span id="nirev">0</span> cr</b></div>
<svg id="donut" style="position:absolute;left:140px;top:450px" width="440" height="440" viewBox="0 0 440 440">
<circle cx="220" cy="220" r="170" fill="none" stroke="#B9B9C6" stroke-width="70"/>
<circle id="darc" cx="220" cy="220" r="170" fill="none" stroke="{TEAL}" stroke-width="70" pathLength="100" stroke-dasharray="100 100" stroke-dashoffset="100" transform="rotate(-90 220 220)"/>
<text x="220" y="245" text-anchor="middle" font-family="Anton" font-size="110" fill="{INK}"><tspan id="n65b">0</tspan>%</text></svg>
<div class="note" style="left:620px;top:560px;width:420px;font-size:42px;color:{INK};font-family:Poppins;font-weight:700;line-height:1.2">of revenue from <span style="color:{TEAL}">outside India</span></div>
<div class="note" style="left:620px;top:760px;width:400px;font-size:30px">FY25, from the DRHP's regional split (about 65%)</div>
<div class="chipx" id="ipat" style="left:120px;top:940px">FY25 profit <b>₹70.7 cr</b></div>
<div class="card" id="iipo" style="left:70px;right:70px;top:1110px;padding:24px 30px;background:#fff">
<div style="font-family:Oswald;font-size:40px;color:#55556A">THE IPO</div>
<div style="font-family:Anton;font-size:76px;line-height:1.1">₹600 cr <span style="font-size:48px">fresh issue</span></div>
<div id="iofs" style="font-family:Poppins;font-weight:700;font-size:42px">+ offer for sale: 1.08 crore shares</div></div>
<div class="note" style="left:40px;right:40px;top:1470px;text-align:center">DRHP (filed Oct 2025) via newboard.in &amp; chittorgarh.com · issue terms per chittorgarh, 20 Nov 2026</div></div>'''

ROWS = [('', 'Foodlink', 'Integris'), ('Sells', 'food &amp; catering', 'stents &amp; lab kits'),
        ('Opens', '26 Nov', '27 Nov'), ('Lists', '3 Dec', '4 Dec'), ('Fresh issue', '₹192 cr', '₹600 cr'),
        ('Revenue', '₹567.5 cr', '₹1,902 cr'), ('Price band', 'TBA', 'TBA')]
SCN[7] = f'''<div class="ttl hand" style="top:190px;font-size:90px">The cheat sheet</div>
<div class="card" id="sheet" style="left:40px;right:40px;top:320px;padding:18px 24px;background:#fff">
''' + '\n'.join(f'<div class="row{" hd" if k == 0 else ""}" id="r{k}"><span>{a}</span><span>{b}</span><span>{c}</span></div>' for k, (a, b, c) in enumerate(ROWS)) + f'''
<div class="src">Revenue: Foodlink FY26 (RHP), Integris FY25 (DRHP) · dates: chittorgarh / goodreturns · Integris dates as reported</div></div>
<div class="stk" id="rhp" style="left:170px;top:1190px;background:{PUR};color:#fff;transform:rotate(-2deg);font-size:64px">📄 READ THE RHP FIRST</div>
<div class="stk" id="bm" style="left:340px;top:1360px;background:{YEL};transform:rotate(4deg);font-size:46px">🔖 SAVE THIS</div>'''

SCN[8] = f'''<div class="ttl hand" style="top:300px;font-size:88px">Business first.<br>Price later.</div>
<img id="host" src="assets/img/s0_008.png" style="position:absolute;left:40px;top:620px;width:360px"/>
<div class="card" id="send" style="left:420px;top:620px;width:600px;padding:20px 24px;background:#fff">
<div style="font-family:Anton;font-size:46px">✈️ SEND THIS TO</div>
<div style="font-family:Poppins;font-weight:700;font-size:36px;line-height:1.2">the friend who applies for every IPO</div></div>
<div class="emo" id="plane" style="left:430px;top:900px;font-size:110px">✈️</div>
<div class="pill" id="sv" style="left:430px;top:960px;background:{YEL};color:{INK};font-size:58px">🔖 SAVE THIS</div>
<div class="pill" id="fl" style="left:430px;top:1120px;background:{PUR};font-size:52px">FOLLOW · every Monday</div>
<div class="stk" id="edu" style="left:110px;top:1320px;background:#fff;font-size:42px;transform:rotate(-1deg)">Education only · Not investment advice</div>'''

EXTRA_CSS = '''
#prog { position:absolute; left:0; top:0; height:12px; width:1080px; background:#6B3FD4; transform-origin:0 50%; z-index:60; }
.tag { position:absolute; left:40px; font-family:"Anton",sans-serif; font-size:44px; background:#1B1B1F; color:#fff; padding:2px 16px; border-radius:10px; z-index:5; }
.qc { width:430px; height:330px; text-align:center; padding-top:20px; } .qc .e { font-size:150px; line-height:1.2; }
.qc b { display:block; font-family:"Caveat",cursive; font-size:62px; }
.day { position:absolute; width:190px; height:250px; background:#fff; border:5px solid #1B1B1F; border-radius:20px; box-shadow:6px 6px 0 #1B1B1F; text-align:center; padding-top:14px; }
.day span { display:block; font-family:"Oswald",sans-serif; font-size:40px; color:#55556A; } .day b { display:block; font-family:"Anton",sans-serif; font-weight:400; font-size:110px; line-height:1.05; } .day i { font-style:normal; font-family:"Oswald",sans-serif; font-size:32px; }
.ipo { width:440px; height:340px; text-align:center; padding:16px 18px; }
.ipo .e { font-size:110px; line-height:1.15; } .ipo b { display:block; font-family:"Anton",sans-serif; font-weight:400; font-size:54px; line-height:1.1; }
.ipo span { display:block; font-family:"Poppins",sans-serif; font-weight:700; font-size:32px; margin-top:6px; color:#55556A; line-height:1.25; }
.chipx { position:absolute; padding:10px 28px; background:#fff; border:5px solid #1B1B1F; border-radius:18px; box-shadow:6px 6px 0 #1B1B1F; font-family:"Poppins",sans-serif; font-weight:700; font-size:44px; line-height:1.15; z-index:5; }
.chipx b { font-family:"Anton",sans-serif; font-weight:400; color:#6B3FD4; font-size:58px; } .chipx small { font-size:30px; color:#55556A; }
.ring { position:absolute; left:440px; width:200px; height:200px; border-radius:50%; border:12px solid #6B3FD4; background:#fff; text-align:center; font-family:"Anton",sans-serif; font-size:120px; line-height:176px; }
.note { position:absolute; font-family:"Oswald",sans-serif; font-size:28px; color:#55556A; line-height:1.3; }
.wa, .wb, .wc { overflow:hidden; } .wa path, .wb path, .wc path { stroke:#8C8676; stroke-width:0.9; }
.cnt { position:absolute; width:460px; height:300px; border:6px solid #1B1B1F; border-radius:26px; box-shadow:10px 10px 0 #1B1B1F; text-align:center; padding-top:14px; }
.cnt b { display:block; font-family:"Anton",sans-serif; font-weight:400; font-size:150px; line-height:1.05; } .cnt > span { display:block; font-family:"Poppins",sans-serif; font-weight:700; font-size:34px; line-height:1.2; }
.pin { position:absolute; font-size:60px; line-height:1; z-index:6; white-space:nowrap; }
.pin b { font-family:"Oswald",sans-serif; font-weight:500; font-size:32px; background:#1B1B1F; color:#fff; padding:2px 10px; border-radius:8px; margin-left:4px; vertical-align:middle; }
.prod { width:236px; height:250px; text-align:center; padding-top:14px; } .prod .e { font-size:100px; line-height:1.2; }
.prod b { display:block; font-family:"Poppins",sans-serif; font-size:30px; line-height:1.15; padding:0 8px; }
.split { position:absolute; left:30px; right:30px; top:190px; height:100px; display:flex; border:5px solid #1B1B1F; border-radius:16px; overflow:hidden; }
.split div { font-family:"Anton",sans-serif; font-size:50px; line-height:90px; text-align:center; color:#1B1B1F; transform-origin:0 50%; }
.split div + div { border-left:5px solid #1B1B1F; }
.pb { position:absolute; width:170px; border:6px solid #1B1B1F; }
.pv { position:absolute; width:230px; text-align:center; font-family:"Anton",sans-serif; font-size:50px; }
.pl { position:absolute; width:230px; text-align:center; font-family:"Oswald",sans-serif; font-size:34px; }
.panel { position:absolute; top:0; width:1080px; height:1920px; }
.row { display:grid; grid-template-columns: 1.05fr 1fr 1fr; padding:20px 6px; border-bottom:3px solid #ddd; font-family:"Poppins",sans-serif; font-weight:700; font-size:38px; align-items:center; }
.row span:not(:first-child) { text-align:right; font-family:"Anton",sans-serif; font-weight:400; font-size:48px; line-height:1.05; }
.row.hd span { font-family:"Anton",sans-serif !important; font-size:52px !important; color:#6B3FD4; }
.src { font-family:"Oswald",sans-serif; font-size:28px; color:#55556A; margin-top:12px; text-align:center; }
'''

def fills(cls, d, at, stag=0.06):
    return '\n'.join(f'tl.to("#{cls}-{a}", {{fill:"{c}", duration:0.3}}, {at} + {k * stag:.2f});' for k, (a, c) in enumerate(d.items()))

JS_SCENES = '''
const cam = CAM(tl);
tl.fromTo("#prog", {scaleX:0}, {scaleX:1, duration:T.DUR, ease:"none"}, 0);
const count = (id, a, b, at, d, dec) => { const o = {v:a}; tl.to(o, {v:b, duration:d||1.2, ease:"power2.out", onUpdate:() => { const e = document.getElementById(id); if (e) e.textContent = o.v.toLocaleString("en-IN", {minimumFractionDigits:dec||0, maximumFractionDigits:dec||0}); }}, at); };
// 0 HOOK: giant 2 already moving at frame 0
tl.fromTo("#h2", {scale:1.7, rotation:-10}, {scale:1, rotation:0, duration:0.9, ease:"back.out(1.6)"}, 0);
tl.fromTo("#hipo", {x:300, opacity:0}, {x:0, opacity:1, duration:0.45, ease:"expo.out"}, 0.35);
tl.fromTo("#hwk", {scale:0.3, opacity:0}, {scale:1, opacity:1, duration:0.4, ease:"back.out(2.2)"}, 0.8);
tl.set(["#hmis", "#hq0", "#hq1"], {opacity:0}, 0);
pop("#hmis", T.mist - 0.05, -2); shake("#sc0", T.mist, 16);
cam.crashZoom("#cam0", T.mist, {to:1.25, ox:"30%", oy:"50%", hold:0.5});
pop("#hq0", T.sell0, -3); pop("#hq1", T.sell0 + 0.25, 3);
tl.to(["#hq0 .e", "#hq1 .e"], {rotation:8, duration:0.3, yoyo:true, repeat:5, ease:"sine.inOut"}, T.sell0 + 0.6);
tl.to("#h2", {scale:1.04, duration:0.5, yoyo:true, repeat:5, ease:"sine.inOut"}, 1.2);
// 1 calendar
tl.set(["#d0","#d1","#d2","#d3","#d4","#pf","#pi","#nse"], {opacity:0}, SC[1][0]);
["#d0","#d1","#d2","#d3","#d4"].forEach((d,k) => pop(d, SC[1][0] + 0.15 + k*0.1));
tl.to("#d3", {backgroundColor:"#FFE45C", duration:0.2}, T.thu - 0.1); pop("#pf", T.thu + 0.1, -2);
tl.to("#d4", {backgroundColor:"#B9E3FF", duration:0.2}, T.fri - 0.1); pop("#pi", T.fri + 0.1, 2);
pop("#nse", T.nse);
cam.track("#cam1", SC[1][0], {x0:0, y0:60, x:0, y:-40, dur:SC[1][1]-SC[1][0], ease:"power1.inOut"});
// 2 price band: dutch tension + stamp
tl.set(["#pbc","#nout","#asof","#ring","#bfirst"], {opacity:0}, SC[2][0]);
up("#pbc", T.pb - 0.1); pop("#nout", T.notout, -6); shake("#sc2", T.notout + 0.05, 14); up("#asof", T.notout + 0.6);
pop("#ring", T.notout + 0.8); tl.to("#ring", {rotation:360, duration:1.2, ease:"power2.inOut"}, T.notout + 1.2);
pop("#bfirst", T.biz, -2);
cam.dutch("#cam2", T.pb, {deg:-6, dur:0.5, hold:1.4});
cam.pushIn("#cam2", T.biz - 0.2, {from:1, to:1.12, dur:1.2, oy:"70%"});
// 3 REHOOK: purple flash, whip-in map, counters
tl.fromTo("#sc3", {backgroundColor:"#6B3FD4"}, {backgroundColor:"#E6E0FF", duration:0.6, ease:"power2.out"}, SC[3][0] + 0.05);
tl.set(["#k15","#k65"], {opacity:0}, SC[3][0]);
''' + fills('wa', {a: ORG for a in EVENTS}, 'T.c15 - 0.2', 0.07) + '''
pop("#k15", T.c15 - 0.1, -2); count("n15", 0, 15, T.c15, 1.0);
pop("#k65", T.c65, 2); count("n65", 0, 65, T.c65 + 0.1, 1.4);
cam.pullOut("#cam3", SC[3][0] + 0.2, {from:1.35, to:1, dur:1.8, oy:"30%"});
cam.rack("#mapA", T.c65 - 0.1, {blur:5, dur:0.5, out:true});
// 4 Foodlink business: map, pins, product icons, 28 counter
tl.set(["#pbm","#pbu","#f4c","#fp0","#fp1","#fp2","#fp3","#f28"], {opacity:0}, SC[4][0]);
''' + fills('wb', wb_fill, 'T.f1 + 0.4', 0.15) + '''
pop("#pbm", T.fmum); pop("#f4c", T.f1 + 0.9);
pop("#fp0", T.fcb); pop("#fp1", T.fib); pop("#fp2", T.fad); pop("#fp3", T.fwed);
up("#f28", T.f28 - 0.1); count("n28", 0, 28, T.f28, 0.9);
tl.fromTo(["#sIN","#sAE"], {scaleX:0}, {scaleX:1, duration:0.6, stagger:0.3, ease:"power3.out"}, T.f28 + 0.3);
pop("#pbu", T.fuae); tl.to("#sAE", {scale:1.06, duration:0.2, yoyo:true, repeat:3}, T.fuae);
cam.tilt("#cam4", SC[4][0], {from:22, to:0, dur:1.4});
cam.pushIn("#cam4", T.fcb - 0.2, {from:1, to:1.06, dur:2.0, oy:"60%"});
cam.pullOut("#cam4", T.f28 - 0.3, {from:1.06, to:1, dur:1.0, oy:"60%"});
// 5 Foodlink numbers: revenue counter, profit bars, loss stamp, IPO card
tl.set(["#frev","#pb0","#pb1","#pb2","#pb3","#pv0","#pv1","#pv2","#pv3","#lossst","#fipo"], {opacity:0}, SC[5][0]);
pop("#frev", T.frev); count("nrev", 0, 567.5, T.frev + 0.1, 1.2, 1);
[["#pb0","#pv0",SC[5][0]+0.6],["#pb1","#pv1",SC[5][0]+0.9],["#pb2","#pv2",T.fpat]].forEach(([b,v,at]) => { tl.fromTo(b, {opacity:1, scaleY:0}, {scaleY:1, duration:0.7, ease:"power3.out"}, at); tl.to(v, {opacity:1, duration:0.2}, at + 0.4); });
tl.fromTo("#pb3", {opacity:1, scaleY:0}, {scaleY:1, duration:0.8, ease:"power3.out"}, T.floss - 0.1); tl.to("#pv3", {opacity:1, duration:0.2}, T.floss + 0.3);
pop("#lossst", T.floss + 0.4, -5); shake("#sc5", T.floss + 0.45, 14);
cam.dutch("#cam5", T.floss + 0.4, {deg:-4, dur:0.4, hold:1.0});
up("#fipo", T.fipo); tl.fromTo("#fofs", {opacity:0}, {opacity:1, duration:0.3}, T.fofs);
cam.pushIn("#cam5", T.fipo, {from:1, to:1.08, dur:2.5, oy:"75%"});
// 6 Integris: products, factories, then track to numbers panel
tl.set(["#ip0","#ip1","#ip2","#ip3","#fin","#fde","#fnl","#imade","#irev","#ipat","#iipo","#iofs"], {opacity:0}, SC[6][0]);
pop("#ip0", T.istent - 0.1); pop("#ip1", T.istent + 0.6); pop("#ip2", T.istent + 1.2); pop("#ip3", T.istent + 1.7);
tl.to("#wc-IND", {fill:"#11A3A3", duration:0.3}, T.imade); pop("#fin", T.imade + 0.1);
tl.to("#wc-DEU", {fill:"#11A3A3", duration:0.3}, T.ideu); pop("#fde", T.ideu + 0.1);
tl.to("#wc-NLD", {fill:"#11A3A3", duration:0.3}, T.inld); pop("#fnl", T.inld + 0.1); pop("#imade", T.imade + 0.4);
cam.parallax(["#mapC"], SC[6][0], {dist:-40, dur:T.irev - SC[6][0]});
cam.track("#cam6", T.irev - 0.5, {x0:0, x:-1080, dur:0.7, ease:"power3.inOut"});
tl.fromTo("#cam6", {filter:"blur(0px)"}, {filter:"blur(10px)", duration:0.35, yoyo:true, repeat:1}, T.irev - 0.5);
pop("#irev", T.irev + 0.2); count("nirev", 0, 1902, T.irev + 0.3, 1.0);
tl.to("#darc", {strokeDashoffset:35, duration:1.2, ease:"power2.out"}, T.i65 - 0.1); count("n65b", 0, 65, T.i65 - 0.1, 1.2);
pop("#ipat", T.i65 + 1.4);
up("#iipo", T.i600 - 0.1); tl.fromTo("#iofs", {opacity:0}, {opacity:1, duration:0.3}, T.iofs);
// 7 ANSWER: cheat sheet
tl.set(["#sheet","#r0","#r1","#r2","#r3","#r4","#r5","#r6","#rhp","#bm"], {opacity:0}, SC[7][0]);
up("#sheet", SC[7][0] + 0.1); ["#r0","#r1","#r2","#r3","#r4","#r5","#r6"].forEach((r,k) => up(r, SC[7][0] + 0.3 + k*0.25));
tl.to("#r3", {backgroundColor:"#FFF1B8", duration:0.3}, T.lf); tl.to("#r6", {backgroundColor:"#FFE2D1", duration:0.3}, T.plot);
pop("#rhp", T.rhp, -2); shake("#sc7", T.rhp + 0.05, 10);
pop("#bm", SC[7][0] + 2.4, 4); tl.to("#bm", {y:-16, duration:0.35, yoyo:true, repeat:9, ease:"sine.inOut"}, SC[7][0] + 2.2);
cam.pullOut("#cam7", SC[7][0], {from:1.2, to:1, dur:1.6, oy:"30%"});
cam.orbit("#sheet", T.lf, {from:-8, to:4, dur:2.4});
// 8 CTA
tl.set(["#host","#send","#plane","#sv","#fl","#edu"], {opacity:0}, SC[8][0]);
tl.fromTo("#host", {y:120, opacity:0}, {y:0, opacity:1, duration:0.5, ease:EIN}, SC[8][0] + 0.2);
up("#send", T.send); tl.fromTo("#plane", {x:0, y:0, opacity:1, rotation:0}, {x:620, y:-520, rotation:-20, opacity:0, duration:1.4, ease:"power2.in"}, T.send + 1.2);
pop("#sv", T.save, -3); tl.to("#sv", {scale:1.12, duration:0.2, yoyo:true, repeat:3}, T.save + 0.5);
pop("#fl", T.follow, 2); up("#edu", T.edu);
cam.pushIn("#cam8", SC[8][0], {from:1.1, to:1, dur:1.4, ease:"power2.out"});
cam.dollyZoom("#host", "#sc8 .ttl", T.loop - 0.2, {amt:0.12, dur:1.6});
'''
