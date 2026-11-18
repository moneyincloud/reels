"""Scenes for the Kalyan Jewellers reel (Royal Gold template). Assembled by build.py."""
import json, re
MAPS = '/home/claude/reels/studio/kalyan/maps/'
india = ''.join(re.findall(r'<path[\s\S]*?/>', open(MAPS + 'node_modules/@svg-maps/india/india.svg').read()))
india = re.sub(r'\s+', ' ', india)
india_n = re.sub(r'\bid="', 'data-s="', india)
world = re.search(r'<svg[^>]*>([\s\S]*)</svg>', open(MAPS + 'world.svg').read()).group(1).replace('id="win"', 'id="win" style="display:none"')
P = json.load(open(MAPS + 'world_pts.json'))

CAPTXT = [
    "This jeweller made ₹427 crore profit in just 3 months. And it all started with one shop in Kerala.",
    "Kalyan Jewellers opened its first showroom in Thrissur, Kerala, in 1993.",
    "Today it runs over 500 stores across India. 365 Kalyan showrooms, and 138 Candere stores.",
    "But here's what most people don't know. Kalyan isn't just an Indian jeweller.",
    "It has 38 showrooms in the UAE, Qatar, Kuwait and Oman. Plus 2 in America, and 2 in the UK. That's 546 stores in total.",
    "Now, the money. From July to September, revenue jumped 31%, to ₹10,323 crore. Profit rose 64%, though a one-time land sale helped.",
    "And almost all of that profit comes from India. ₹424 crore from India, and just ₹12 crore from the Middle East.",
    "The growth trick? Franchise showrooms. Partners put in the money for the store, and Kalyan runs it. About 59% of revenue already comes from them, and 84 more are planned.",
    "So, would you buy the gold, or the jeweller? Tell me in the comments, and follow @moneyincloud. Education only, not a buy or sell call.",
]
BG = [''] * 9

def jw(i, k, x, y, w, h, r=0):
    return f'<div class="jw" id="{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({r}deg)"><img src="assets/img/{k}.jpg"/><div class="shine"></div></div>'

SCN = {}
SCN[0] = '<div class="ser" style="top:190px">3 months. 1 jeweller.</div>' \
    '<div class="big gold" id="p427" style="top:290px;font-size:240px">₹0 cr</div>' \
    '<div class="big" id="pl" style="top:560px;font-family:Poppins;font-size:52px">profit · July–Sept 2026</div>' \
    + jw('h1', 'j1', 70, 680, 300, 300, -6) + jw('h2', 'j3', 390, 660, 300, 330, 2) + jw('h3', 'j7', 710, 690, 300, 300, 7) + \
    '<div class="pill" id="ker" style="left:200px;top:1060px;font-size:52px">🏪 It began with 1 shop</div>'
SCN[1] = f'''<div class="ser" style="top:190px">Where it began</div>
<div class="card" id="logo" style="left:60px;top:320px;width:300px;height:300px;background:#FFF8EA;border-radius:40px"><img src="assets/img/kalyan-logo.png" style="width:100%;height:100%"/></div>
<svg id="imap1" style="position:absolute;left:420px;top:320px;width:560px;height:637px" viewBox="0 0 612 696">
<g fill="rgba(255,244,220,.08)" stroke="#E8B64C" stroke-width="1.2">{india}</g></svg>
<div class="emo" id="pin" style="left:549px;top:800px;font-size:90px">📍</div>
<div class="card" id="thr" style="left:60px;top:660px;width:340px;height:220px;padding:24px 30px"><div class="gold" style="font-family:Anton;font-size:72px;line-height:1">THRISSUR</div><div style="font-size:36px">Kerala</div></div>
<div class="card" id="y93" style="left:60px;top:920px;width:340px;height:190px;padding:20px 30px"><div class="gold" style="font-family:Anton;font-size:96px;line-height:1" id="yr">1993</div><div style="font-size:32px">first showroom</div></div>'''
SCN[2] = f'''<div class="big gold" id="t504" style="top:180px;font-size:110px">India: 500+ stores</div>
<svg id="imap2" style="position:absolute;left:20px;top:320px;width:620px;height:700px" viewBox="0 0 612 696">
<defs><linearGradient id="sw" x1="0" x2="1"><stop offset="0" stop-color="#E8B64C" stop-opacity="0"/><stop offset=".5" stop-color="#FFE7A3" stop-opacity=".9"/><stop offset="1" stop-color="#E8B64C" stop-opacity="0"/></linearGradient>
<clipPath id="ic">{india_n}</clipPath></defs>
<g fill="rgba(255,244,220,.12)" stroke="#E8B64C" stroke-width="1.2">{india_n}</g>
<g clip-path="url(#ic)"><rect id="swp" x="-300" y="0" width="300" height="696" fill="url(#sw)"/></g></svg>
<div class="card" id="k1" style="left:640px;top:360px;width:400px;height:200px;padding:20px 26px"><div class="gold" style="font-family:Anton;font-size:100px;line-height:1" id="n365">0</div><div style="font-size:32px">Kalyan showrooms</div></div>
<div class="card" id="k2" style="left:640px;top:590px;width:400px;height:200px;padding:20px 26px"><div class="gold" style="font-family:Anton;font-size:100px;line-height:1" id="n138">0</div><div style="font-size:32px">Candere stores</div></div>
<div class="card" id="k3" style="left:640px;top:820px;width:400px;height:170px;padding:20px 26px"><div class="gold" style="font-family:Anton;font-size:80px;line-height:1">+1</div><div style="font-size:30px">Akshaya Thanga Maligai</div></div>'''
SCN[3] = '<div class="ser" style="top:230px">But here\'s the twist…</div>' \
    '<div class="emo" id="globe" style="left:0;right:0;text-align:center;top:420px;font-size:330px">🌍</div>' \
    + jw('t1', 'j2', 60, 380, 230, 230, -8) + jw('t2', 'j8', 790, 420, 230, 230, 8) + jw('t3', 'j5', 80, 840, 260, 180, 6) + jw('t4', 'j9', 760, 840, 230, 200, -6) + \
    '<div class="pill" id="nj" style="left:150px;top:1060px;font-size:50px">not just an Indian jeweller</div>'
x0, y0 = 680, 249
pins = ''.join(f'<circle class="wp" id="wp{k}" cx="{P[k][0]}" cy="{P[k][1]}" r="5" fill="#FFE7A3" stroke="#3A0816" stroke-width="1.5"/>' for k in ['ae', 'qa', 'kw', 'om', 'us', 'gb'])
arcs = ''.join(f'<path class="arc" id="arc{k}" d="M{P["in"][0]},{P["in"][1]} Q{(P["in"][0]+P[k][0])/2},{min(P["in"][1],P[k][1])-90} {P[k][0]},{P[k][1]}" fill="none" stroke="#FFE7A3" stroke-width="2.5" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>' for k in ['ae', 'us', 'gb'])
SCN[4] = f'''<div class="big gold" style="top:180px;font-size:110px">Abroad: 42 stores</div>
<svg id="wmap" style="position:absolute;left:-60px;top:330px;width:1200px;height:672px" viewBox="0 0 1000 560">
<g fill="rgba(255,244,220,.10)" stroke="rgba(246,210,122,.35)" stroke-width=".5">{world}</g>
<style>.h{{fill:rgba(232,182,76,.85)}}</style>
<svg x="{x0}" y="{y0}" width="84" height="99" viewBox="0 0 612 696" preserveAspectRatio="none"><g fill="#E8B64C">{india_n}</g></svg>
{arcs}{pins}</svg>
<div class="pill" id="pus" style="left:90px;top:470px;font-size:40px">🇺🇸 USA · 2</div>
<div class="pill" id="puk" style="left:380px;top:390px;font-size:40px">🇬🇧 UK · 2</div>
<div class="pill" id="pme" style="left:420px;top:930px;font-size:42px;text-align:center">Middle East · 38<br><span style="font-size:28px">🇦🇪 UAE · 🇶🇦 Qatar · 🇰🇼 Kuwait · 🇴🇲 Oman</span></div>
<div class="card" id="tot" style="left:40px;top:720px;width:360px;height:210px;text-align:center;padding-top:20px;background:rgba(34,4,12,.92)"><div class="gold" style="font-family:Anton;font-size:116px;line-height:1">546</div><div style="font-size:36px">stores in total</div></div>'''
SCN[5] = '''<div class="ser" style="top:190px">The profit check</div>
<div class="big" style="top:290px;font-family:Poppins;font-size:38px;color:#D9C29A">July–September 2026 vs a year ago</div>
<div class="card" id="cr" style="left:70px;top:380px;width:460px;height:640px;padding:24px 30px"><div style="font-size:42px">Revenue</div>
<div class="bar" id="r0" style="left:50px;bottom:120px;width:150px;height:300px;background:rgba(255,244,220,.25)"></div>
<div class="bar" id="r1" style="right:50px;bottom:120px;width:150px;height:394px;background:linear-gradient(180deg,#FFE7A3,#B07A22)"></div>
<div style="position:absolute;left:30px;bottom:30px;width:190px;text-align:center;font-size:30px;color:#D9C29A">₹7,856 cr</div><div style="position:absolute;right:30px;bottom:30px;width:190px;text-align:center;font-size:30px" id="rv">₹10,323 cr</div>
<div class="pill" id="rp" style="right:24px;top:20px;font-size:36px;padding:6px 20px">▲ 31%</div></div>
<div class="card" id="cp" style="left:550px;top:380px;width:460px;height:640px;padding:24px 30px"><div style="font-size:42px">Profit</div>
<div class="bar" id="q0" style="left:50px;bottom:120px;width:150px;height:240px;background:rgba(255,244,220,.25)"></div>
<div class="bar" id="q1" style="right:50px;bottom:120px;width:150px;height:394px;background:linear-gradient(180deg,#FFE7A3,#B07A22)"></div>
<div style="position:absolute;left:30px;bottom:30px;width:190px;text-align:center;font-size:30px;color:#D9C29A">₹261 cr</div><div style="position:absolute;right:30px;bottom:30px;width:190px;text-align:center;font-size:30px">₹427 cr</div>
<div class="pill" id="qp" style="right:24px;top:20px;font-size:36px;padding:6px 20px">▲ 64%</div></div>
<div class="pill" id="land" style="left:130px;top:1060px;font-size:34px;background:linear-gradient(135deg,#FFC6B8,#FF9C8A)">⚠️ includes one-time ₹73.5 cr land-sale gain</div>'''
SCN[6] = '''<div class="ser" style="top:200px;font-size:66px">Where the profit comes from</div>
<div class="card" id="ci" style="left:70px;right:70px;top:330px;height:330px;padding:26px 36px"><div style="font-size:46px">🇮🇳 India</div>
<div style="position:absolute;left:36px;top:100px;font-size:32px;color:#D9C29A">Revenue ₹9,007 cr</div>
<div class="gold" style="position:absolute;right:36px;top:30px;font-family:Anton;font-size:110px" id="pin424">₹0 cr</div>
<div style="position:absolute;left:36px;right:36px;top:200px;height:60px;border-radius:30px;background:rgba(255,244,220,.12)"></div>
<div id="bi" style="position:absolute;left:36px;right:36px;top:200px;height:60px;border-radius:30px;background:linear-gradient(90deg,#B07A22,#FFE7A3);transform-origin:0 50%"></div></div>
<div class="card" id="cm" style="left:70px;right:70px;top:700px;height:330px;padding:26px 36px"><div style="font-size:46px">🌍 Middle East</div>
<div style="position:absolute;left:36px;top:100px;font-size:32px;color:#D9C29A">Revenue ₹960 cr</div>
<div style="position:absolute;right:36px;top:30px;font-family:Anton;font-size:110px;color:#FF9C8A">₹12 cr</div>
<div style="position:absolute;left:36px;right:36px;top:200px;height:60px;border-radius:30px;background:rgba(255,244,220,.12)"></div>
<div id="bm" style="position:absolute;left:36px;top:200px;width:24px;height:60px;border-radius:30px;background:#FF9C8A;transform-origin:0 50%"></div>
<div style="position:absolute;left:80px;top:208px;font-size:30px;color:#D9C29A">profit bar, same scale</div></div>'''
SCN[7] = '''<div class="ser" style="top:190px">The growth trick</div>
<div class="card" id="fr" style="left:70px;right:70px;top:310px;height:330px;padding:24px 36px;text-align:center"><div style="font-size:120px;line-height:1.1">🤝🏪</div>
<div style="font-size:50px">Franchise showrooms</div><div style="font-size:34px;color:#D9C29A">partner puts in the money · Kalyan runs the store</div></div>
<div class="card" id="c59" style="left:70px;top:680px;width:460px;height:360px;text-align:center;padding-top:20px">
<svg width="230" height="230" viewBox="0 0 100 100" style="display:block;margin:0 auto"><circle cx="50" cy="50" r="40" fill="none" stroke="rgba(255,244,220,.15)" stroke-width="12"/>
<circle id="ring" cx="50" cy="50" r="40" fill="none" stroke="#E8B64C" stroke-width="12" stroke-linecap="round" pathLength="100" stroke-dasharray="59 100" stroke-dashoffset="59" transform="rotate(-90 50 50)"/>
<text x="50" y="58" text-anchor="middle" font-family="Anton" font-size="24" fill="#FFE7A3">~59%</text></svg>
<div style="font-size:30px">of revenue from franchise stores</div></div>
<div class="card" id="c84" style="left:550px;top:680px;width:460px;height:360px;text-align:center;padding-top:40px">
<div class="gold" style="font-family:Anton;font-size:170px;line-height:1" id="n84">+0</div><div style="font-size:32px">more Kalyan franchise<br>showrooms planned (H2)</div></div>'''
SCN[8] = '''<div class="ser" style="top:200px;font-size:84px">Would you buy…</div>
<div class="jw" id="g0" style="left:80px;top:360px;width:400px;height:330px"><img src="assets/img/j4.jpg"/><div class="shine"></div></div>
<div class="pill" id="g0t" style="left:150px;top:650px;font-size:44px">the gold 💍</div>
<div class="ser" id="or" style="top:470px;font-size:80px">or</div>
<div class="card" id="g1" style="right:80px;top:360px;width:400px;height:330px;background:#FFF8EA"><img src="assets/img/kalyan-logo.png" style="position:absolute;left:65px;top:30px;width:270px;height:270px"/></div>
<div class="pill" id="g1t" style="left:640px;top:650px;font-size:44px">the jeweller 📈</div>
<img id="host" src="assets/img/s0_008.png" style="position:absolute;left:60px;top:790px;width:320px"/>
<div class="pill" id="cmt" style="left:420px;top:830px;font-size:50px">💬 Comment below</div>
<div class="pill" id="fol" style="left:420px;top:970px;font-size:50px">➕ Follow for more</div>'''

EXTRA_CSS = '''.bar { position:absolute; border-radius:20px 20px 6px 6px; transform-origin:50% 100%; }'''

JS_SCENES = '''
const cam = CAM(tl);
const cnt = (id, from, to, at, dur, fmt) => { const o = {v:from}; tl.to(o, {v:to, duration:dur, ease:"power2.out", onUpdate:() => { document.getElementById(id).textContent = fmt(o.v); }}, at); };
const inr = v => Math.round(v).toLocaleString("en-IN");
const shine = (sel, at) => tl.fromTo(sel + " .shine", {x:"-120%"}, {x:"120%", duration:0.9, ease:"power2.inOut"}, at);
// 0 hook: profit counter, jewels fly in, shine
tl.set(["#pl", "#h1", "#h2", "#h3", "#ker"], {opacity:0}, 0);
cnt("p427", 0, 427, T.profit - 0.1, 1.4, v => "₹" + inr(v) + " cr"); up("#pl", T.months);
[["#h1",-6,-400],["#h2",2,0],["#h3",7,400]].forEach(([s,r,x],k) => { tl.fromTo(s, {opacity:0, x:x, y:300, rotation:r*3}, {opacity:1, x:0, y:0, rotation:r, duration:0.7, ease:"back.out(1.6)"}, T.months + 0.2 + k*0.18); shine(s, T.months + 1.2 + k*0.2); });
pop("#ker", T.kerala, -2);
cam.pushIn("#cam0", 0, {from:1.12, to:1, dur:1.6, ease:"power2.out"});
// 1 origin: logo, map draws, pin drops, 1993
tl.set(["#logo", "#thr", "#y93"], {opacity:0}, SC[1][0]);
tl.fromTo("#imap1 path", {strokeDasharray:"0 3000"}, {strokeDasharray:"3000 0", duration:1.6, ease:"power1.inOut"}, SC[1][0] + 0.1);
tl.fromTo("#imap1 #kl", {fill:"rgba(255,244,220,.08)"}, {fill:"#E8B64C", duration:0.6}, T.thr - 0.2);
pop("#logo", T.first - 0.3, -3);
tl.fromTo("#pin", {y:-400, opacity:0}, {y:0, opacity:1, duration:0.6, ease:"bounce.out"}, T.thr); up("#thr", T.thr + 0.3);
pop("#y93", T.y93); cnt("yr", 2026, 1993, T.y93, 1.0, v => String(Math.round(v)));
cam.pushIn("#cam1", SC[1][0], {from:1, to:1.06, dur:SC[1][1]-SC[1][0]-0.4, ease:"none", ox:"70%", oy:"50%"});
// 2 India: shimmer sweep, counters
tl.set(["#t504", "#k1", "#k2", "#k3"], {opacity:0}, SC[2][0]);
pop("#t504", T.five - 0.2);
tl.fromTo("#swp", {attr:{x:-300}}, {attr:{x:700}, duration:1.8, ease:"power1.inOut", repeat:1}, T.five);
pop("#k1", T.k365 - 0.2); cnt("n365", 0, 365, T.k365, 1.2, inr);
pop("#k2", T.c138 - 0.2); cnt("n138", 0, 138, T.c138, 1.0, inr); pop("#k3", T.c138 + 1.2);
cam.track("#cam2", SC[2][0], {x0:30, y0:0, x:-30, y:0, dur:SC[2][1]-SC[2][0], ease:"sine.inOut"});
// 3 twist: globe spins in, jewels orbit
tl.set(["#globe", "#nj", "#t1", "#t2", "#t3", "#t4"], {opacity:0}, SC[3][0]);
tl.fromTo("#globe", {scale:0.2, rotation:-180, opacity:0}, {scale:1, rotation:0, opacity:1, duration:0.9, ease:"back.out(1.5)"}, SC[3][0] + 0.3);
["#t1","#t2","#t3","#t4"].forEach((s,k) => pop(s, SC[3][0] + 0.6 + k*0.15, [-8,8,6,-6][k]));
pop("#nj", T.notjust, -2);
cam.orbit("#cam3", SC[3][0], {from:-12, to:6, dur:SC[3][1]-SC[3][0]});
// 4 world: arcs draw, pins, zoom to Gulf, total
tl.set(["#pus", "#puk", "#pme", "#tot", ".wp"], {opacity:0}, SC[4][0]);
tl.to("#arcae", {strokeDashoffset:0, duration:0.8, ease:"power2.out"}, T.me);
["#wpae","#wpqa","#wpkw","#wpom"].forEach((s,k) => tl.fromTo(s, {opacity:0, attr:{r:0}}, {opacity:1, attr:{r:5}, duration:0.3, ease:"back.out(3)"}, T.me + 0.6 + k*0.25));
pop("#pme", T.us + 0.4, -1);
cam.pushIn("#cam4", T.me, {from:1, to:1.9, dur:1.2, ease:"power2.inOut", ox:"60%", oy:"40%"});
tl.to("#cam4", {scale:1, duration:0.9, ease:"power2.inOut"}, T.us - 0.6);
tl.to("#arcus", {strokeDashoffset:0, duration:0.9, ease:"power2.out"}, T.us); tl.fromTo("#wpus", {opacity:0}, {opacity:1, duration:0.2}, T.us + 0.8); pop("#pus", T.us + 0.8);
tl.to("#arcgb", {strokeDashoffset:0, duration:0.8, ease:"power2.out"}, T.uk); tl.fromTo("#wpgb", {opacity:0}, {opacity:1, duration:0.2}, T.uk + 0.7); pop("#puk", T.uk + 0.7);
pop("#tot", T.total); shake("#sc4", T.total + 0.1, 10);
// 5 profit bars
tl.set(["#cr", "#cp", "#rp", "#qp", "#land"], {opacity:0}, SC[5][0]); tl.set(["#r0", "#r1", "#q0", "#q1"], {scaleY:0}, SC[5][0]);
up("#cr", T.money); up("#cp", T.money + 0.3);
tl.to("#r0", {scaleY:1, duration:0.6}, T.rev); tl.to("#r1", {scaleY:1, duration:0.8, ease:"back.out(1.5)"}, T.rev + 0.5); pop("#rp", T.rev + 1.3);
tl.to("#q0", {scaleY:1, duration:0.6}, T.prof - 0.2); tl.to("#q1", {scaleY:1, duration:0.8, ease:"back.out(1.5)"}, T.prof + 0.3); pop("#qp", T.prof + 1.1);
pop("#land", T.land, -1);
cam.crashZoom("#cam5", T.prof + 1.1, {to:1.1, ox:"75%", oy:"40%", hold:0.5});
// 6 India vs Middle East
tl.set(["#ci", "#cm"], {opacity:0}, SC[6][0]); tl.set(["#bi", "#bm"], {scaleX:0}, SC[6][0]);
up("#ci", SC[6][0] + 0.4); cnt("pin424", 0, 424, T.india, 1.2, v => "₹" + inr(v) + " cr"); tl.to("#bi", {scaleX:1, duration:1.2, ease:"power2.out"}, T.india);
up("#cm", SC[6][0] + 0.8); tl.to("#bm", {scaleX:1, duration:0.4, ease:"power2.out"}, T.mideast + 0.4);
cam.dutch("#cam6", T.mideast + 0.3, {deg:-3, dur:0.5, hold:1.2});
// 7 franchise
tl.set(["#fr", "#c59", "#c84"], {opacity:0}, SC[7][0]);
pop("#fr", T.fr - 0.2); pop("#c59", T.p59 - 0.3, -2); tl.to("#ring", {strokeDashoffset:0, duration:1.2, ease:"power2.out"}, T.p59);
pop("#c84", T.p84 - 0.3, 2); cnt("n84", 0, 84, T.p84, 1.0, v => "+" + Math.round(v));
cam.tilt("#cam7", SC[7][0], {from:14, to:0, dur:1.4});
// 8 CTA
tl.set(["#g0", "#g0t", "#or", "#g1", "#g1t", "#host", "#cmt", "#fol"], {opacity:0}, SC[8][0]);
pop("#g0", T.q + 0.5, -3); pop("#g0t", T.q + 0.9); shine("#g0", T.q + 1.1); pop("#or", T.q + 1.4); pop("#g1", T.q + 1.8, 3); pop("#g1t", T.q + 2.2);
tl.fromTo("#host", {y:120, opacity:0}, {y:0, opacity:1, duration:0.5, ease:EIN}, T.cmt - 0.4);
pop("#cmt", T.cmt, -2); pop("#fol", T.fol, 2);
cam.pullOut("#cam8", SC[8][0], {from:1.12, to:1, dur:1.4});
'''
