"""Scenes for the 17 Nov 2026 market reel: green Nifty, but more stocks fell. Assembled by build.py."""
CAPTXT = [
    "Nifty closed green today. But more stocks fell than rose. So who pushed the market up?",
    "Tuesday, 17 November. Nifty closed at 25,387, up 0.38%. Sensex added 427 points.",
    "Yet on the BSE, 2,148 stocks fell, and only 2,012 rose. Smallcaps ended in the red.",
    "And here's the twist. One index closed at a level it has never closed at before.",
    "Bank Nifty. Up 1.13%, to a record close of 62,273. PSU banks jumped almost 2%. Axis Bank and SBI led the charge.",
    "Why? Crude oil slipped to about $91 a barrel during the day, easing India's import bill. And foreign investors kept buying India, even after a sharp sell-off on Wall Street.",
    "Not everyone joined the party. IT stocks fell. HCL Tech dropped 2%, and Infosys 1.3%.",
    "So here's the answer. A few heavyweight banks can lift the whole Nifty, even when most stocks fall. The index alone never tells the full story.",
    "Save this, and follow @moneyincloud for the market in a minute. Education only, not investment advice.",
]
BG = ['#D7F5E9', '#FFF1B8', '#FFD6DE', '#1F2433', '#DDF0FF', '#FFE2D1', '#FFD6DE', '#E6E0FF', '#D7F5E9']

dots = '\n'.join(
    f'<div class="dot {"dn" if k % 2 == 0 else "upd"}" id="d{k}" style="left:{90 + (k % 9) * 100}px;top:{870 + (k // 9) * 90}px"></div>'
    for k in range(18))

SCN = {}
SCN[0] = '''<div class="ttl hand" style="top:200px;font-size:92px">17 Nov 2026</div>
<div class="pill" id="h_up" style="left:110px;top:430px;background:#1E8E4E;font-size:84px;transform:rotate(-3deg)">NIFTY ▲ 0.38%</div>
<div class="pill" id="h_dn" style="left:150px;top:640px;background:#D93A2B;font-size:62px;transform:rotate(2deg)">BUT MORE STOCKS FELL ▼</div>
<div class="big" id="qm" style="left:0;right:0;text-align:center;top:820px;font-size:300px;color:#1B1B1F">?</div>'''
SCN[1] = '''<div class="ttl hand" style="top:220px">Closing bell</div>
<div class="card" id="board" style="left:70px;right:70px;top:400px;padding:16px 40px;background:#1B1B1F;color:#fff">
<div class="tr" id="r0"><span>NIFTY 50</span><b id="v0">25,387.40</b></div>
<div class="tr sub" id="r0b"><span></span><i class="g">▲ 96.30 · 0.38%</i></div>
<div class="tr" id="r1"><span>SENSEX</span><b id="v1">82,532.19</b></div>
<div class="tr sub" id="r1b"><span></span><i class="g">▲ 427.40 · 0.52%</i></div></div>
<div class="stk" id="grn" style="left:250px;top:1000px;background:#1E8E4E;color:#fff;transform:rotate(-2deg)">ALL GREEN? 🤔</div>'''
SCN[2] = f'''<div class="ttl hand" style="top:200px;font-size:84px">BSE · stocks today</div>
<div id="chart" style="position:absolute;left:150px;right:150px;top:410px;height:380px;border-bottom:8px solid #1B1B1F">
<div class="bar" id="bf" style="left:40px;height:360px;background:#D93A2B"></div>
<div class="bar" id="br" style="right:40px;height:338px;background:#2BB673"></div>
<div class="blab" id="lf" style="left:20px;top:-64px;color:#B42318">2,148</div>
<div class="blab" id="lr" style="right:20px;top:-42px;color:#1E8E4E">2,012</div></div>
<div class="blab" style="left:170px;top:805px;font-size:46px">FELL ▼</div>
<div class="blab" style="right:170px;top:805px;font-size:46px">ROSE ▲</div>
{dots}
<div class="stk" id="smc" style="left:200px;top:1045px;background:#D93A2B;color:#fff;transform:rotate(-3deg);font-size:54px">Smallcap 100 ▼ 0.22%</div>'''
SCN[3] = '''<div class="ttl hand" style="top:260px;color:#FFE45C">The twist…</div>
<div class="emo" id="vault" style="left:0;right:0;text-align:center;top:470px;font-size:300px">🏦</div>
<div class="stk" id="nev" style="left:110px;top:930px;background:#FFE45C;transform:rotate(-4deg);font-size:58px">NEVER CLOSED HERE BEFORE</div>'''
SCN[4] = '''<div class="ttl hand" style="top:200px">Bank Nifty</div>
<div class="big" id="bn" style="left:0;right:0;text-align:center;top:330px;font-size:190px;color:#1B1B1F">62,273</div>
<div class="pill" id="bnp" style="left:330px;top:560px;background:#1E8E4E;font-size:64px">▲ 1.13%</div>
<div class="stk" id="rec" style="left:190px;top:700px;background:#FFE45C;transform:rotate(-5deg);font-size:72px">🏆 RECORD CLOSE</div>
<div class="chip" id="c0" style="left:70px;top:900px">PSU Bank <b>▲ 1.95%</b></div>
<div class="chip" id="c1" style="left:560px;top:900px">Axis Bank <b>▲ 1.98%</b></div>
<div class="chip" id="c2" style="left:315px;top:1040px">SBI <b>▲ 1.6%</b></div>'''
SCN[5] = '''<div class="ttl hand" style="top:200px">Why up?</div>
<div class="card why" id="w0" style="left:60px;top:360px"><div class="e">🛢️</div><b>Crude slipped</b><span>to ≈ $91/barrel intraday</span><i>lower import bill</i></div>
<div class="card why" id="w1" style="left:560px;top:360px"><div class="e">🌍</div><b>Foreign investors</b><span>kept buying India</span><i>even as Wall St fell</i></div>
<div class="arr" id="aw" style="left:400px;top:1000px;width:260px;transform:rotate(-90deg)"></div>
<div class="stk" id="ind" style="left:330px;top:1040px;background:#1E8E4E;color:#fff;font-size:60px">🇮🇳 INDIA ▲</div>'''
SCN[6] = '''<div class="ttl hand" style="top:200px">Not everyone partied</div>
<div class="pill" id="itp" style="left:300px;top:380px;background:#D93A2B;font-size:70px">IT ▼ 0.90%</div>
<div class="card lose" id="l0" style="left:110px;top:590px"><b>HCL Tech</b><span>▼ 2.09%</span></div>
<div class="card lose" id="l1" style="left:570px;top:590px"><b>Infosys</b><span>▼ 1.3%</span></div>
<div class="emo" id="ball" style="left:470px;top:880px;font-size:140px">🎈</div>'''
SCN[7] = '''<div class="ttl hand" style="top:200px">The answer</div>
<div id="seesaw" style="position:absolute;left:90px;width:900px;top:640px;height:24px;background:#1B1B1F;border-radius:12px;transform-origin:50% 50%"></div>
<div id="pivot" style="position:absolute;left:490px;top:664px;width:0;height:0;border-left:50px solid transparent;border-right:50px solid transparent;border-bottom:110px solid #1B1B1F"></div>
<div class="blk" id="b0" style="left:110px;top:440px">🏦</div>
<div class="blk" id="b1" style="left:300px;top:440px">🏦</div>
<div class="small" id="sm" style="left:600px;top:560px">● ● ● ● ●<br>● ● ● ● ●</div>
<div class="card" id="ans" style="left:70px;right:70px;top:860px;padding:26px 30px;text-align:center;background:#FFF7E0">
<div style="font-family:Anton;font-size:64px;line-height:1.1">A few heavyweights<br>can lift the Nifty</div>
<div style="font-family:Poppins;font-weight:700;font-size:38px;margin-top:10px">even when most stocks fall</div></div>
<div class="stk" id="idx" style="left:170px;top:1120px;background:#D93A2B;color:#fff;transform:rotate(-3deg);font-size:54px">INDEX ≠ WHOLE MARKET</div>'''
SCN[8] = '''<div class="ttl hand" style="top:220px">Green Nifty ≠<br>green market</div>
<img id="host" src="assets/img/s0_008.png" style="position:absolute;left:40px;top:600px;width:360px"/>
<div class="pill" id="sv" style="left:430px;top:640px;background:#FFE45C;color:#1B1B1F;font-size:60px">💾 SAVE THIS</div>
<div class="pill" id="fl" style="left:430px;top:820px;background:#1E8E4E;font-size:56px">FOLLOW for daily</div>
<div class="pill" id="fl2" style="left:430px;top:980px;background:#1B1B1F;font-size:50px">market in a minute</div>'''

EXTRA_CSS = '''#sc3 .ttl { color:#FFE45C; }
.tr { display:flex; justify-content:space-between; align-items:baseline; padding:24px 0 6px; font-family:"Poppins",sans-serif; font-size:50px; }
.tr b { font-family:"Anton",sans-serif; font-weight:400; font-size:84px; color:#FFE45C; }
.tr.sub { padding:0 0 22px; border-bottom:2px solid #444; } .tr.sub:last-child { border:0; }
.tr i { font-style:normal; font-family:"Anton",sans-serif; font-size:50px; } .g { color:#5BE39A; }
.dot { position:absolute; width:56px; height:56px; border-radius:50%; border:4px solid #1B1B1F; }
.dot.dn { background:#D93A2B; } .dot.upd { background:#2BB673; }
.chip { position:absolute; width:450px; padding:18px 24px; background:#fff; border:5px solid #1B1B1F; border-radius:20px; box-shadow:6px 6px 0 #1B1B1F;
  font-family:"Poppins",sans-serif; font-weight:700; font-size:40px; }
.chip b { font-family:"Anton",sans-serif; font-weight:400; color:#1E8E4E; float:right; }
.why { width:460px; height:560px; text-align:center; padding:26px 22px; }
.why .e { font-size:140px; line-height:1.15; } .why b { display:block; font-family:"Anton",sans-serif; font-weight:400; font-size:58px; }
.why span { display:block; font-family:"Poppins",sans-serif; font-weight:700; font-size:36px; margin-top:8px; }
.why i { display:block; font-style:normal; font-family:"Caveat",cursive; font-weight:700; font-size:50px; color:#1E8E4E; margin-top:14px; }
.lose { width:400px; height:240px; text-align:center; padding-top:30px; background:#fff; }
.lose b { display:block; font-family:"Anton",sans-serif; font-weight:400; font-size:66px; } .lose span { font-family:"Anton",sans-serif; font-size:76px; color:#D93A2B; }
.blk { position:absolute; width:150px; height:190px; font-size:130px; text-align:center; background:#DDF0FF; border:6px solid #1B1B1F; border-radius:18px; box-shadow:6px 6px 0 #1B1B1F; }
.small { position:absolute; font-size:44px; line-height:1.1; color:#D93A2B; letter-spacing:4px; }
'''

JS_SCENES = '''
const cam = CAM(tl);
// 0 hook: green pill slams, red pill counters, big "?" crash-zooms
tl.set(["#h_up", "#h_dn", "#qm"], {opacity:0}, 0);
pop("#h_up", 0.25, -3); pop("#h_dn", T.fell0, 2); shake("#sc0", T.fell0 + 0.05, 12);
pop("#qm", T.who - 0.2); tl.to("#qm", {rotation:12, duration:0.35, yoyo:true, repeat:5, ease:"sine.inOut"}, T.who + 0.3);
cam.pushIn("#cam0", 0, {from:1.12, to:1, dur:1.2, ease:"power2.out"});
cam.crashZoom("#cam0", T.who, {to:1.35, oy:"62%", hold:0.4});
// 1 closing board: rows rise with the voice, numbers count up
tl.set(["#board", "#r0", "#r0b", "#r1", "#r1b", "#grn"], {opacity:0}, SC[1][0]);
up("#board", SC[1][0] + 0.2); up("#r0", T.nifty - 0.2); up("#r0b", T.nifty + 1.6); up("#r1", T.sensex - 0.2); up("#r1b", T.sensex + 0.5);
const n0 = {v:25291.10}, n1 = {v:82104.79};
tl.to(n0, {v:25387.40, duration:1.4, ease:"power2.out", onUpdate:() => { document.getElementById("v0").textContent = n0.v.toLocaleString("en-IN", {minimumFractionDigits:2, maximumFractionDigits:2}); }}, T.nifty);
tl.to(n1, {v:82532.19, duration:1.4, ease:"power2.out", onUpdate:() => { document.getElementById("v1").textContent = n1.v.toLocaleString("en-IN", {minimumFractionDigits:2, maximumFractionDigits:2}); }}, T.sensex);
pop("#grn", SC[2][0] - 1.6, -2);
cam.track("#cam1", SC[1][0], {x0:0, y0:-60, x:0, y:0, dur:SC[1][1]-SC[1][0], ease:"none"});
// 2 breadth: red bar outgrows green, dots flip, smallcap sticker
tl.set(["#bf", "#br"], {scaleY:0}, SC[2][0]); tl.set(["#lf", "#lr", "#smc"], {opacity:0}, SC[2][0]);
tl.set(".dot", {opacity:0, scale:0}, SC[2][0]);
tl.to("#bf", {scaleY:1, duration:0.9, ease:"power2.out"}, T.fell); pop("#lf", T.fell + 0.6);
tl.to("#br", {scaleY:1, duration:0.9, ease:"power2.out"}, T.rose); pop("#lr", T.rose + 0.6);
document.querySelectorAll("#sc2 .dot").forEach((el, k) => tl.to(el, {opacity:1, scale:1, duration:0.18, ease:"back.out(2)"}, T.fell + 0.2 + k * 0.07));
pop("#smc", T.small, -3);
cam.pushIn("#cam2", SC[2][0], {from:1, to:1.08, dur:SC[2][1]-SC[2][0], ease:"none", oy:"30%"});
// 3 rehook: dark scene, dutch angle, vault drops, stamp
tl.set(["#vault", "#nev"], {opacity:0}, SC[3][0]);
tl.fromTo("#vault", {y:-500, opacity:1}, {y:0, opacity:1, duration:0.7, ease:"bounce.out"}, T.twist);
pop("#nev", T.never, -4); shake("#sc3", T.never + 0.05, 14);
cam.dutch("#cam3", SC[3][0] + 0.1, {deg:-6, dur:0.5, hold:SC[3][1]-SC[3][0]-1.2});
// 4 Bank Nifty: counter to the record, trophy stamp, chips
const b = {v:61575.90}; tl.set(["#bn", "#bnp", "#rec", ".chip"], {opacity:0}, SC[4][0]);
tl.to("#bn", {opacity:1, duration:0.2}, T.bank);
tl.to(b, {v:62273.25, duration:1.6, ease:"power2.out", onUpdate:() => { document.getElementById("bn").textContent = Math.round(b.v).toLocaleString("en-IN"); }}, T.bank);
pop("#bnp", T.bank + 1.0); pop("#rec", T.record, -5); shake("#sc4", T.record + 0.05, 10);
pop("#c0", T.psu); pop("#c1", T.axis); pop("#c2", T.axis + 0.6);
cam.pullOut("#cam4", SC[4][0], {from:1.25, to:1, dur:1.4, oy:"25%"});
cam.crashZoom("#cam4", T.record - 0.1, {to:1.25, oy:"40%", hold:0.6});
// 5 why: two cause cards, arrow up to India
tl.set(["#w0", "#w1", "#ind"], {opacity:0}, SC[5][0]); tl.set("#aw", {scaleX:0}, SC[5][0]);
pop("#w0", T.crude - 0.2, -2); pop("#w1", T.fii - 0.2, 2);
tl.to("#aw", {scaleX:1, duration:0.4}, T.wall); pop("#ind", T.wall + 0.3);
cam.track("#cam5", SC[5][0], {x0:60, y0:0, x:-60, y:0, dur:SC[5][1]-SC[5][0], ease:"sine.inOut"});
// 6 IT losers: cards drop, balloon deflates
tl.set(["#itp", "#l0", "#l1"], {opacity:0}, SC[6][0]);
pop("#itp", T.it - 0.1); tl.fromTo("#l0", {y:-300, opacity:0}, {y:0, opacity:1, duration:0.5, ease:"bounce.out"}, T.hcl);
tl.fromTo("#l1", {y:-300, opacity:0}, {y:0, opacity:1, duration:0.5, ease:"bounce.out"}, T.infy);
tl.fromTo("#ball", {scale:1, y:0}, {scale:0.45, y:160, duration:1.6, ease:"power2.in"}, T.it);
cam.pushIn("#cam6", SC[6][0], {from:1.06, to:1, dur:SC[6][1]-SC[6][0], ease:"none"});
// 7 answer: two bank blocks tip the seesaw, cheat-sheet card stamps in
tl.set(["#b0", "#b1", "#sm", "#ans", "#idx"], {opacity:0}, SC[7][0]); tl.set("#seesaw", {rotation:0}, SC[7][0]);
pop("#sm", SC[7][0] + 0.4);
tl.fromTo("#b0", {y:-500, opacity:1}, {y:0, opacity:1, duration:0.45, ease:"power3.in"}, T.ans);
tl.fromTo("#b1", {y:-500, opacity:1}, {y:0, opacity:1, duration:0.45, ease:"power3.in"}, T.ans + 0.25);
tl.to("#seesaw", {rotation:-9, duration:0.5, ease:"back.out(2)"}, T.ans + 0.7);
tl.to(["#b0", "#b1"], {y:40, duration:0.5, ease:"back.out(2)"}, T.ans + 0.7);
tl.to("#sm", {y:-90, duration:0.5, ease:"back.out(2)"}, T.ans + 0.7);
up("#ans", T.ans + 1.2); pop("#idx", T.index, -3); shake("#sc7", T.index + 0.05, 10);
cam.pullOut("#cam7", SC[7][0], {from:1.18, to:1, dur:1.6, oy:"35%"});
// 8 CTA
tl.fromTo("#host", {y:120, opacity:0}, {y:0, opacity:1, duration:0.5, ease:EIN}, SC[8][0] + 0.2);
tl.set(["#sv", "#fl", "#fl2"], {opacity:0}, SC[8][0]);
pop("#sv", T.save, -3); pop("#fl", T.follow, 2); pop("#fl2", T.follow + 0.5, -1);
cam.pushIn("#cam8", SC[8][0], {from:1.1, to:1, dur:1.4, ease:"power2.out"});
'''
