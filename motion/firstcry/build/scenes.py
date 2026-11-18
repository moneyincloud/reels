"""Scenes for the FirstCry business reel (Soft Nursery light template). Assembled by build.py."""
CAPTXT = [
    "This baby shop stock jumped 13% in one day, on about 75x its usual volume. Yet it still trades at less than half its IPO price. Why?",
    "Meet FirstCry, run by Brainbees Solutions from Pune. Founded in 2010, listed in 2024.",
    "It sells almost everything for babies and kids. Diapers, clothes, toys and strollers. About 2 million products from 7,800+ brands, online and in nearly 1,200 stores.",
    "But the smartest part of the business is hiding on the label.",
    "Its own brands, like BabyHug, CuteWalk and Pine Kids. When FirstCry sells its own brand, it doesn't share the margin with an outside company.",
    "It runs four businesses. The India business, the biggest one. Online shopping in the UAE and Saudi Arabia. GlobalBees, a group of online brands. And Intellitots preschools.",
    "Now, the profit. In the September quarter, revenue grew 14% to ₹2,396 crore. And the loss shrank 75%, to just ₹12.6 crore.",
    "That's what excited the market. The India business already made a profit last year. But the company as a whole is still in a small loss, and the share is far below its IPO price of ₹465.",
    "Would you buy the baby products, or the company that sells them? Tell me in the comments, and follow @moneyincloud. Education only, not a buy or sell call.",
]
BG = ['rgba(255,216,194,.35)', 'rgba(205,232,255,.35)', 'rgba(189,240,221,.35)', 'rgba(227,217,255,.45)',
      'rgba(255,216,194,.35)', 'rgba(205,232,255,.35)', 'rgba(189,240,221,.35)', 'rgba(227,217,255,.40)', 'rgba(255,216,194,.35)']

SCN = {}
SCN[0] = '''<div class="kick" style="top:180px">17 Nov 2026</div>
<div class="card" id="tick" style="left:90px;right:90px;top:270px;height:300px;padding:34px 44px">
<div style="font-size:40px;color:var(--mut)">🍼 FIRSTCRY · NSE</div>
<div class="num" id="px" style="left:44px;top:100px;font-size:140px">₹158.59</div>
<div class="pill g-mint" id="chg" style="right:30px;top:24px;font-size:44px;padding:8px 26px">▲ 12.85%</div></div>
<div class="card" id="volc" style="left:90px;right:90px;top:620px;height:200px;padding:28px 44px">
<div style="font-size:38px;color:var(--mut)">Shares traded vs usual day</div>
<div style="position:absolute;left:44px;right:44px;top:100px;height:56px;border-radius:28px;background:#F1EDFA;overflow:hidden">
<div id="volf" style="position:absolute;left:0;top:0;bottom:0;width:100%;border-radius:28px;background:linear-gradient(90deg,#FFC94D,#FF5C7A);transform-origin:0 50%"></div></div>
<div class="num" id="volx" style="right:56px;top:94px;font-size:60px;color:var(--ink)">~75x</div></div>
<div class="card" id="ipoc" style="left:90px;right:90px;top:870px;height:250px;padding:28px 44px">
<div style="font-size:38px;color:var(--mut)">IPO price (2024) vs now</div>
<div class="num" style="left:44px;top:96px;font-size:96px;color:var(--mut)">₹465</div>
<div class="num" style="left:330px;top:100px;font-size:90px">→</div>
<div class="num" id="now" style="left:470px;top:96px;font-size:96px;color:var(--coral)">₹179</div>
<div class="emo" id="qq" style="right:40px;top:80px;font-size:120px">🤔</div></div>'''
SCN[1] = '''<div class="kick" style="top:200px">meet</div>
<div class="ttl" id="fc" style="top:280px;font-size:150px">First<em>Cry</em></div>
<div class="pill g-lav" id="bb" style="left:200px;top:470px;font-size:46px">by Brainbees Solutions</div>
<div class="emo" id="pin" style="left:150px;top:640px;font-size:150px">📍</div>
<div class="num" id="pune" style="left:330px;top:680px;font-size:96px">Pune</div>
<div id="tline" style="position:absolute;left:160px;right:160px;top:1000px;height:12px;border-radius:6px;background:linear-gradient(90deg,#34D1A6,#A68BFF);transform-origin:0 50%"></div>
<div class="card" id="y10" style="left:80px;top:900px;width:300px;height:210px;text-align:center;padding-top:26px"><div style="font-size:84px;line-height:1">2010</div><div style="font-size:36px;color:var(--mut)">founded</div></div>
<div class="card" id="y24" style="right:80px;top:900px;width:300px;height:210px;text-align:center;padding-top:26px"><div style="font-size:84px;line-height:1;color:var(--lav)">2024</div><div style="font-size:36px;color:var(--mut)">listed 🔔</div></div>'''
items = ['👶', '🧸', '👕', '🛒', '🍼', '👟', '🧴', '🚼']
grid = '\n'.join(f'<div class="card it" id="it{k}" style="left:{90 + (k % 4) * 230}px;top:{290 + (k // 4) * 230}px;width:200px;height:200px;text-align:center;font-size:120px;line-height:200px">{e}</div>' for k, e in enumerate(items))
SCN[2] = grid + '''
<div class="card st" id="s0" style="left:70px;top:790px;width:300px;height:250px"><div class="n" id="n0">0</div><div class="l">products</div></div>
<div class="card st" id="s1" style="left:390px;top:790px;width:300px;height:250px"><div class="n" id="n1">0</div><div class="l">brands</div></div>
<div class="card st" id="s2" style="left:710px;top:790px;width:300px;height:250px"><div class="n" id="n2">0</div><div class="l">stores</div></div>'''
SCN[3] = '''<div class="kick" style="top:260px">the secret is on the…</div>
<div id="tagw" style="position:absolute;left:290px;top:420px;width:500px;height:560px;transform-origin:50% 0%">
<div style="position:absolute;left:246px;top:0;width:8px;height:120px;background:var(--ink);border-radius:4px"></div>
<div class="card" style="left:0;top:110px;width:500px;height:440px;text-align:center;padding-top:60px;background:linear-gradient(160deg,#fff,#FFF1EA)">
<div style="width:60px;height:60px;border-radius:50%;margin:0 auto;border:8px solid #EBDDF2"></div>
<div style="font-size:120px;line-height:1.15;margin:10px 0;color:var(--coral)">LABEL</div><div style="font-size:44px;color:var(--mut)">🏷️ look closer</div></div></div>'''
SCN[4] = '''<div class="ttl" style="top:200px">Its <em>own</em> brands</div>
<div class="pill g-coral" id="br0" style="left:110px;top:360px">BabyHug</div>
<div class="pill g-sky" id="br1" style="left:520px;top:360px">CuteWalk</div>
<div class="pill g-mint" id="br2" style="left:300px;top:490px">Pine Kids</div>
<div class="card" id="mg" style="left:70px;right:70px;top:650px;height:480px;padding:30px 40px">
<div style="font-size:38px;color:var(--mut)">Where the margin goes on ₹100 of sales*</div>
<div class="ml" style="top:110px">Outside brand</div>
<div class="mb" style="top:170px"><div id="m0a" class="seg" style="width:50%;background:#C9C2DE">brand's cut</div><div id="m0b" class="seg" style="width:50%;background:#FFC94D">shop</div></div>
<div class="ml" style="top:290px">Own brand</div>
<div class="mb" style="top:350px"><div id="m1" class="seg" style="width:100%;background:linear-gradient(90deg,#34D1A6,#1FAE8C);color:#fff">FirstCry keeps it all 💚</div></div></div>
<div style="position:absolute;left:70px;right:70px;top:1140px;text-align:center;font-size:26px;color:var(--mut)">*illustration of how private labels work, not FirstCry's actual split</div>'''
biz = [('🇮🇳', 'India business', 'stores + app · biggest', '₹5,753 cr', 'g-coral'),
       ('🌍', 'UAE + Saudi', 'online shopping', '₹947 cr', 'g-sky'),
       ('🐝', 'GlobalBees', 'online brands', '₹1,894 cr', 'g-sun'),
       ('🎒', 'Intellitots', 'preschools', 'smallest', 'g-lav')]
SCN[5] = '<div class="ttl" style="top:190px"><em>4</em> businesses</div>\n' + '\n'.join(
    f'<div class="card bz" id="bz{k}" style="left:{70 + (k % 2) * 480}px;top:{340 + (k // 2) * 410}px;width:460px;height:380px">'
    f'<div class="e">{e}</div><b>{n}</b><span>{d}</span><div class="pill {g}" style="left:30px;bottom:24px;font-size:36px;padding:8px 26px">FY26 rev {r}</div></div>'
    for k, (e, n, d, r, g) in enumerate(biz))
SCN[5] = SCN[5].replace('FY26 rev smallest', 'smallest')
SCN[6] = '''<div class="ttl" style="top:190px">The <em>profit</em> check</div>
<div class="kick" style="top:300px;font-size:56px;color:var(--mut)">September quarter, year on year</div>
<div class="card" id="rv" style="left:70px;top:400px;width:460px;height:660px;padding:26px 30px">
<div style="font-size:40px">Revenue</div>
<div style="position:absolute;left:40px;right:40px;top:120px;height:380px">
<div class="bar" id="r0" style="left:10px;width:160px;height:333px;background:#D8D2EA"></div>
<div class="bar" id="r1" style="right:10px;width:160px;height:380px;background:linear-gradient(180deg,#34D1A6,#1FAE8C)"></div></div>
<div style="position:absolute;left:40px;top:515px;width:190px;text-align:center;font-size:30px;color:var(--mut)">₹2,099 cr<br>Q2 FY26</div>
<div style="position:absolute;right:40px;top:515px;width:190px;text-align:center;font-size:30px">₹2,396 cr<br>Q2 FY27</div>
<div class="pill g-mint" id="rp" style="right:24px;top:20px;font-size:38px;padding:6px 22px">▲ 14.1%</div></div>
<div class="card" id="ls" style="left:550px;top:400px;width:460px;height:660px;padding:26px 30px">
<div style="font-size:40px">Net loss</div>
<div style="position:absolute;left:40px;right:40px;top:120px;height:380px">
<div class="bar" id="l0" style="left:10px;width:160px;height:380px;background:linear-gradient(180deg,#FF8A65,#FF5C7A)"></div>
<div class="bar" id="l1" style="right:10px;width:160px;height:95px;background:linear-gradient(180deg,#FF8A65,#FF5C7A)"></div></div>
<div style="position:absolute;left:40px;top:515px;width:190px;text-align:center;font-size:30px;color:var(--mut)">₹50.5 cr<br>Q2 FY26</div>
<div style="position:absolute;right:40px;top:515px;width:190px;text-align:center;font-size:30px">₹12.6 cr<br>Q2 FY27</div>
<div class="pill g-coral" id="lp" style="right:20px;top:66px;font-size:38px;padding:6px 22px">▼ 75% smaller</div></div>'''
SCN[7] = '''<div class="ttl" style="top:190px">So… <em>good</em> or not?</div>
<div class="card chk" id="k0" style="left:70px;right:70px;top:360px"><span class="e">✅</span><b>India business</b><i>profitable in FY26</i></div>
<div class="card chk" id="k1" style="left:70px;right:70px;top:560px"><span class="e">⚠️</span><b>Whole company</b><i>still a small loss</i></div>
<div class="card" id="gauge" style="left:70px;right:70px;top:760px;height:330px;padding:28px 40px">
<div style="font-size:38px;color:var(--mut)">Share price vs IPO price</div>
<div style="position:absolute;left:40px;right:40px;top:120px;height:56px;border-radius:28px;background:#F1EDFA"></div>
<div id="gf" style="position:absolute;left:40px;top:120px;width:357px;height:56px;border-radius:28px;background:linear-gradient(90deg,#FF8A65,#FF5C7A);transform-origin:0 50%"></div>
<div style="position:absolute;right:40px;top:196px;font-size:40px">IPO ₹465</div>
<div style="position:absolute;left:40px;top:196px;font-size:40px;color:var(--coral)">Now ₹179</div>
<div class="pill g-coral" id="gp" style="left:330px;top:250px;font-size:36px;padding:6px 24px">about 62% below</div></div>'''
SCN[8] = '''<div class="ttl" style="top:190px">Would you buy…</div>
<div class="card pick" id="p0" style="left:80px;top:370px"><div class="e">🍼</div><b>the products</b></div>
<div class="kick" id="or" style="top:520px;left:0;right:0;font-size:90px">or</div>
<div class="card pick" id="p1" style="right:80px;top:370px"><div class="e">📈</div><b>the company</b></div>
<img id="host" src="assets/img/s0_008.png" style="position:absolute;left:60px;top:780px;width:330px"/>
<div class="pill g-sun" id="cm" style="left:420px;top:820px;font-size:50px">💬 Comment below</div>
<div class="pill g-lav" id="fl" style="left:420px;top:960px;font-size:50px">➕ Follow for more</div>'''

EXTRA_CSS = '''
.st { text-align:center; padding-top:40px; } .st .n { font-size:78px; line-height:1.1; letter-spacing:-2px; } .st .l { font-size:36px; color:var(--mut); }
.ml { position:absolute; left:40px; font-size:38px; }
.mb { position:absolute; left:40px; right:40px; height:84px; border-radius:42px; overflow:hidden; display:flex; background:#F1EDFA; }
.seg { height:100%; display:flex; align-items:center; justify-content:center; font-size:32px; transform-origin:0 50%; white-space:nowrap; }
.bz { padding:26px 30px; } .bz .e { font-size:96px; line-height:1.1; } .bz b { display:block; font-size:46px; } .bz span { display:block; font-size:32px; color:var(--mut); }
.chk { height:170px; padding:28px 36px 0 160px; } .chk .e { position:absolute; left:36px; top:34px; font-size:96px; line-height:1; }
.chk b { display:block; font-size:52px; line-height:1.1; } .chk i { font-style:normal; font-size:38px; color:var(--mut); }
.pick { width:400px; height:330px; text-align:center; padding-top:30px; } .pick .e { font-size:150px; line-height:1.2; } .pick b { font-size:46px; }
'''

JS_SCENES = '''
const cam = CAM(tl);
const cnt = (id, from, to, at, dur, fmt) => { const o = {v:from}; tl.to(o, {v:to, duration:dur, ease:"power2.out", onUpdate:() => { document.getElementById(id).textContent = fmt(o.v); }}, at); };
const inr = (v, d) => v.toLocaleString("en-IN", {minimumFractionDigits:d, maximumFractionDigits:d});
// 0 hook
tl.set(["#tick", "#chg", "#volc", "#ipoc", "#qq"], {opacity:0}, 0); tl.set("#volf", {scaleX:0}, 0);
up("#tick", 0.15); cnt("px", 158.59, 178.97, T.jump - 0.2, 1.2, v => "₹" + inr(v, 2)); pop("#chg", T.jump + 0.6, -3);
up("#volc", T.vol - 0.1); tl.to("#volf", {scaleX:1, duration:1.2, ease:"power2.inOut"}, T.vol + 0.1);
up("#ipoc", T.ipo0 - 0.1); pop("#qq", T.why - 0.1, 8); tl.to("#qq", {rotation:-10, duration:0.3, yoyo:true, repeat:3, ease:"sine.inOut"}, T.why + 0.4);
cam.pushIn("#cam0", 0, {from:1.08, to:1, dur:1.4, ease:"power2.out"});
cam.crashZoom("#cam0", T.ipo0 + 0.6, {to:1.22, oy:"55%", hold:0.8});
// 1 meet
tl.set(["#fc", "#bb", "#pin", "#pune", "#y10", "#y24"], {opacity:0}, SC[1][0]); tl.set("#tline", {scaleX:0}, SC[1][0]);
pop("#fc", T.meet); pop("#bb", T.meet + 1.0, -2);
tl.fromTo("#pin", {y:-300, opacity:0}, {y:0, opacity:1, duration:0.6, ease:"bounce.out"}, T.pune - 0.2); up("#pune", T.pune);
pop("#y10", T.y10); tl.to("#tline", {scaleX:1, duration:0.9, ease:"power2.inOut"}, T.y10 + 0.3); pop("#y24", T.y24, 2);
cam.track("#cam1", SC[1][0], {x0:0, y0:40, x:0, y:-20, dur:SC[1][1]-SC[1][0], ease:"sine.inOut"});
// 2 products
tl.set([".it", ".st"], {opacity:0}, SC[2][0]);
document.querySelectorAll("#sc2 .it").forEach((el, k) => pop(el, T.items - 0.2 + k * 0.22, (k % 2 ? 6 : -6)));
pop("#s0", T.skus); cnt("n0", 0, 2, T.skus, 1.0, v => inr(v, 1) + " mn");
pop("#s1", T.brands); cnt("n1", 0, 7800, T.brands, 1.0, v => inr(Math.round(v / 100) * 100, 0) + "+");
pop("#s2", T.stores); cnt("n2", 0, 1189, T.stores, 1.0, v => inr(Math.round(v), 0));
cam.orbit("#cam2", SC[2][0], {from:-10, to:8, dur:SC[2][1]-SC[2][0]});
// 3 rehook: swinging tag
tl.fromTo("#tagw", {rotation:-28, y:-700}, {rotation:-28, y:0, duration:0.5, ease:"power3.out"}, SC[3][0] + 0.15);
tl.to("#tagw", {keyframes:[{rotation:18, duration:0.6, ease:"sine.inOut"}, {rotation:-10, duration:0.55, ease:"sine.inOut"}, {rotation:5, duration:0.5, ease:"sine.inOut"}, {rotation:0, duration:0.45, ease:"sine.out"}]}, SC[3][0] + 0.65);
cam.crashZoom("#cam3", T.label, {to:1.3, oy:"45%", hold:0.7});
// 4 own brands + margin bars
tl.set(["#br0", "#br1", "#br2", "#mg"], {opacity:0}, SC[4][0]); tl.set(["#m0a", "#m0b", "#m1"], {scaleX:0}, SC[4][0]);
pop("#br0", T.own + 1.0, -4); pop("#br1", T.own + 1.6, 3); pop("#br2", T.own + 2.3, -2);
up("#mg", T.marg - 0.2); tl.to("#m0a", {scaleX:1, duration:0.5}, T.marg + 0.3); tl.to("#m0b", {scaleX:1, duration:0.5}, T.marg + 0.7);
tl.to("#m1", {scaleX:1, duration:0.9, ease:"power2.out"}, T.marg + 1.6);
cam.pushIn("#cam4", SC[4][0], {from:1, to:1.06, dur:SC[4][1]-SC[4][0]-0.4, ease:"none", oy:"70%"});
// 5 four businesses
tl.set(".bz", {opacity:0}, SC[5][0]);
[["#bz0", T.b1], ["#bz1", T.b2], ["#bz2", T.b3], ["#bz3", T.b4]].forEach(([s, t], k) => tl.fromTo(s, {opacity:0, y:120, rotation:(k%2?6:-6)}, {opacity:1, y:0, rotation:0, duration:0.55, ease:"back.out(1.8)"}, t - 0.15));
cam.tilt("#cam5", SC[5][0], {from:18, to:0, dur:1.6});
// 6 profit bars
tl.set(["#rv", "#ls", "#rp", "#lp"], {opacity:0}, SC[6][0]); tl.set(["#r0", "#r1", "#l0", "#l1"], {scaleY:0}, SC[6][0]);
up("#rv", T.prof); up("#ls", T.prof + 0.3);
tl.to("#r0", {scaleY:1, duration:0.6}, T.rev); tl.to("#r1", {scaleY:1, duration:0.8, ease:"back.out(1.6)"}, T.rev + 0.5); pop("#rp", T.rev + 1.4);
tl.to("#l0", {scaleY:1, duration:0.6}, T.loss - 0.2); tl.to("#l1", {scaleY:1, duration:0.6, ease:"back.out(1.6)"}, T.loss + 0.6); pop("#lp", T.loss + 1.3, -3);
cam.crashZoom("#cam6", T.loss + 1.3, {to:1.1, ox:"75%", oy:"45%", hold:0.5});
// 7 verdict
tl.set(["#k0", "#k1", "#gauge", "#gp"], {opacity:0}, SC[7][0]); tl.set("#gf", {scaleX:0}, SC[7][0]);
pop("#k0", T.indp - 0.2); pop("#k1", T.still - 0.1); up("#gauge", T.ipo - 0.2);
tl.to("#gf", {scaleX:1, duration:1.0, ease:"power2.out"}, T.ipo + 0.2); pop("#gp", T.ipo + 1.2, -2);
cam.dutch("#cam7", T.still, {deg:-4, dur:0.5, hold:1.6});
// 8 CTA
tl.set(["#p0", "#p1", "#or", "#host", "#cm", "#fl"], {opacity:0}, SC[8][0]);
pop("#p0", T.q + 0.6, -4); pop("#or", T.q + 1.4); pop("#p1", T.q + 2.0, 4);
tl.fromTo("#host", {y:120, opacity:0}, {y:0, opacity:1, duration:0.5, ease:EIN}, T.cmt - 0.4);
pop("#cm", T.cmt, -2); pop("#fl", T.fol, 2);
cam.pullOut("#cam8", SC[8][0], {from:1.12, to:1, dur:1.4});
'''
