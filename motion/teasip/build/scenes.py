"""Scene content + animation for the tea money -> SIP reel. Assembled by build.py."""
CAPTXT = [
    "Your daily tea or coffee isn't even our tradition. But it quietly takes ₹25 from you every day.",
    "Tea became an Indian habit only after British-era campaigns in the 1930s, with free cups at railway stations.",
    "In Tamil Nadu, coffee replaced our morning neeragaram and kanji only in the early 1900s.",
    "So here's a swap: put that ₹25 into a daily SIP, only on working days.",
    "That's ₹125 a week, about ₹510 a month, around ₹6,100 a year.",
    "In 20 years you'd invest about ₹1.22 lakh.",
    "If it grew the way the Nifty 50 did over the last 20 years (about 12% a year), it could be around ₹4.9 lakh.",
    "But past returns are not a promise. Markets fall too, so this needs patience, not luck.",
    "Would you swap one tea for this? Comment SIP, and save this.",
]
BG = ['#FFF1B8', '#DDF0FF', '#D7F5E9', '#E6E0FF', '#FFE2D1', '#FFF1B8', '#D9F7D0', '#FFD6DE', '#FFF1B8']

days = ''.join(f'<div class="day" id="dy{k}" style="left:{80 + k * 186}px">{d}<b>{"✓" if k < 5 else "✕"}</b></div>' for k, d in enumerate(['MON', 'TUE', 'WED', 'THU', 'FRI']))
coins = '\n'.join(f'<div class="tok" id="cn{k}" style="left:{300 + (k % 3) * 160 + (k // 3 % 2) * 40}px;top:{1000 - (k // 3) * 46}px"></div>' for k in range(18))
zig = 'M40 300 L140 250 L220 290 L300 180 L380 230 L450 120 L520 330 L600 260 L700 160 L780 210 L880 60'

SCN = {}
SCN[0] = '''<div class="emo" id="cup" style="left:0;right:0;text-align:center;top:400px;font-size:330px">☕</div>
<div class="steam" id="st0" style="left:470px"></div><div class="steam" id="st1" style="left:540px"></div><div class="steam" id="st2" style="left:610px"></div>
<div class="stk" id="tag25" style="left:640px;top:760px;background:#1E8E4E;color:#fff;transform:rotate(8deg)">₹25/day</div>
<div class="stk" id="trad" style="left:120px;top:250px;background:#D93A2B;color:#fff;transform:rotate(-4deg);font-size:58px">NOT OUR TRADITION?</div>'''
SCN[1] = '''<div class="card" id="poster" style="left:90px;right:90px;top:260px;padding:30px;text-align:center;background:#FFF7E0">
<div style="font-family:Anton;font-size:44px;color:#B45309">1930s · INDIAN TEA MARKET EXPANSION BOARD</div>
<div style="font-family:Caveat;font-weight:700;font-size:96px;line-height:1">“Drink tea!”</div></div>
<div id="track" style="position:absolute;left:-100px;right:-100px;top:930px;height:16px;background:repeating-linear-gradient(90deg,#1B1B1F 0 40px,transparent 40px 70px)"></div>
<div class="emo" id="train" style="left:-420px;top:740px;font-size:200px">🚂</div>
<div class="emo cupf" id="cf0" style="left:320px;top:620px;font-size:90px">🍵</div>
<div class="emo cupf" id="cf1" style="left:470px;top:580px;font-size:90px">🍵</div>
<div class="emo cupf" id="cf2" style="left:620px;top:620px;font-size:90px">🍵</div>
<div class="stk" id="free" style="left:330px;top:1010px;background:#FFE45C;transform:rotate(-3deg);font-size:54px">FREE CUPS AT STATIONS</div>'''
SCN[2] = '''<div class="ttl hand" style="top:230px;font-size:84px">Tamil Nadu mornings</div>
<div class="card" id="old" style="left:70px;width:420px;top:420px;height:430px;text-align:center;padding-top:30px">
<div style="font-size:150px">🥣</div><div style="font-family:Anton;font-size:52px">neeragaram<br>&amp; kanji</div><div style="font-family:Poppins;font-size:30px;color:#5B5B66">before</div></div>
<div class="arr" id="ar2" style="left:500px;top:620px;width:80px"></div>
<div class="card" id="new" style="right:70px;width:420px;top:420px;height:430px;text-align:center;padding-top:30px;background:#FFF7E0">
<div style="font-size:150px">☕</div><div style="font-family:Anton;font-size:52px">filter<br>coffee</div><div style="font-family:Poppins;font-size:30px;color:#5B5B66">early 1900s</div></div>'''
SCN[3] = f'''<div class="emo" id="cup3" style="left:420px;top:300px;font-size:200px">☕</div>
<div class="emo" id="coin3" style="left:440px;top:320px;font-size:170px">🪙</div>
<div class="card" id="jar" style="left:330px;top:540px;width:420px;height:230px;text-align:center;padding-top:40px;background:#ECFFF1">
<div style="font-family:Anton;font-size:80px;color:#1E8E4E">DAILY SIP</div><div style="font-family:Poppins;font-size:34px">₹25 a day</div></div>
<div id="days" style="position:absolute;left:0;right:0;top:880px;height:180px">{days}</div>'''
SCN[4] = '''<div class="card" id="tbl" style="left:70px;right:70px;top:260px;padding:16px 40px;background:#1B1B1F;color:#fff">
<div class="tr" id="t0"><span>Per working day</span><b>₹25</b></div>
<div class="tr" id="t1"><span>Per week (5 days)</span><b>₹125</b></div>
<div class="tr" id="t2"><span>Per month</span><b>≈ ₹510</b></div>
<div class="tr" id="t3"><span>Per year (~245 days)</span><b>≈ ₹6,125</b></div></div>'''
SCN[5] = f'''<div class="ttl hand" style="top:240px">20 years later</div>
<div class="big" id="inv" style="left:0;right:0;text-align:center;top:420px;font-size:150px;color:#B45309">₹1,22,500</div>
<div style="position:absolute;left:0;right:0;text-align:center;top:600px;font-family:Poppins;font-size:40px">invested · just ₹25 a working day</div>
{coins}'''
SCN[6] = '''<div class="ttl hand" style="top:230px;font-size:80px">If it grew like Nifty 50's<br>last 20 years (12.44%/yr)</div>
<div id="chart" style="position:absolute;left:140px;right:140px;top:470px;height:560px;border-bottom:8px solid #1B1B1F">
<div class="bar" id="g0" style="left:60px;height:132px;background:#F59E0B"></div>
<div class="bar" id="g1" style="right:60px;height:534px;background:#2BB673"></div>
<div class="blab" id="gv0" style="left:40px;top:340px">₹1.22 L</div>
<div class="blab" id="gv1" style="right:40px;top:-62px;color:#1E8E4E">≈ ₹4.95 L</div></div>
<div class="blab" style="left:160px;top:1045px;font-size:38px">you put in</div>
<div class="blab" style="right:160px;top:1045px;font-size:38px">illustration*</div>'''
SCN[7] = f'''<div class="ttl hand" style="top:240px">Past ≠ promise</div>
<svg id="zz" viewBox="0 0 920 360" style="position:absolute;left:80px;top:440px;width:920px;height:360px;overflow:visible">
<path id="zp" d="{zig}" style="stroke:#1B1B1F;stroke-width:12"/></svg>
<div class="stk" id="dn" style="left:330px;top:840px;background:#D93A2B;color:#fff;transform:rotate(-3deg)">markets fall too 📉</div>
<div class="stk" id="pat" style="left:240px;top:990px;background:#FFE45C;transform:rotate(2deg);font-size:54px">needs patience, not luck</div>'''
SCN[8] = '''<div class="ttl hand" style="top:240px">Swap one tea<br>for this?</div>
<img id="host" src="assets/img/s0_008.png" style="position:absolute;left:40px;top:600px;width:360px"/>
<div class="emo" style="left:480px;top:560px;font-size:150px">☕➜🪙</div>
<div class="pill" id="kw" style="left:430px;top:790px;background:#1E8E4E;font-size:76px">COMMENT SIP</div>
<div class="pill" id="sv" style="left:430px;top:970px;background:#FFE45C;color:#1B1B1F;font-size:56px">💾 SAVE THIS</div>'''

EXTRA_CSS = '''#zp { fill:none; stroke-linecap:round; stroke-linejoin:round; }
.steam { position:absolute; top:330px; width:26px; height:120px; border-radius:13px; background:rgba(120,120,130,.35); }
.day { position:absolute; top:0; width:160px; height:160px; background:#fff; border:5px solid #1B1B1F; border-radius:20px; box-shadow:6px 6px 0 #1B1B1F;
  text-align:center; font-family:"Anton",sans-serif; font-size:44px; padding-top:12px; }
.day b { display:block; font-weight:400; font-size:64px; color:#1E8E4E; }
.tr { display:flex; justify-content:space-between; align-items:baseline; padding:30px 0; border-bottom:2px solid #444; font-family:"Poppins",sans-serif; font-size:44px; }
.tr:last-child { border:0; } .tr b { font-family:"Anton",sans-serif; font-weight:400; font-size:66px; color:#FFE45C; }
'''

JS_SCENES = '''
// 0 hook: steaming cup, price tag swings, "not our tradition" stamp
tl.fromTo("#cam0", {scale:1.3, x:-162, y:-200}, {scale:1, x:0, y:0, duration:3.0, ease:"power2.inOut"}, 0);
["#st0", "#st1", "#st2"].forEach((s, k) => tl.fromTo(s, {y:40, opacity:0, scaleY:0.5}, {y:-80, opacity:0.9, scaleY:1.2, duration:1.6, repeat:3, ease:"sine.out"}, 0.1 + k*0.3));
tl.set(["#tag25", "#trad"], {opacity:0}, 0);
pop("#trad", T.trad, -4); shake("#sc0", T.trad + 0.05, 10);
pop("#tag25", T.rs25, 8); tl.to("#tag25", {rotation:-6, duration:0.5, yoyo:true, repeat:3, ease:"sine.inOut"}, T.rs25 + 0.5);
// 1 tea history: poster drops, train rolls in handing out cups, camera tracks the train
tl.set("#cam1", {scale:1.15, x:-40, y:-80}, SC[1][0]);
tl.fromTo("#poster", {y:-400, rotation:-6}, {y:0, rotation:-1, duration:0.7, ease:"bounce.out"}, SC[1][0] + 0.2);
tl.to("#train", {x:900, duration:2.2, ease:"power2.out"}, T.tea30 - 0.4);
tl.to("#cam1", {x:-120, duration:2.2, ease:"power2.out"}, T.tea30 - 0.4);
tl.set([".cupf", "#free"], {opacity:0}, SC[1][0]);
[0, 1, 2].forEach(k => pop("#cf" + k, T.cups + k*0.18));
pop("#free", T.cups + 0.7, -3); tl.to("#cam1", {scale:1, x:0, y:0, duration:0.9, ease:"power3.inOut"}, T.cups + 0.3);
// 2 Tamil Nadu: old drink card, arrow, coffee card
tl.fromTo("#cam2", {scale:1.08, x:-43, y:-40}, {scale:1, x:0, y:0, duration:SC[2][1]-SC[2][0], ease:"none"}, SC[2][0]);
tl.set(["#old", "#new"], {opacity:0}, SC[2][0]); tl.set("#ar2", {scaleX:0}, SC[2][0]);
pop("#old", T.kanji - 0.3, -2); tl.to("#ar2", {scaleX:1, duration:0.4}, T.early - 0.5); pop("#new", T.early, 2);
// 3 swap: cup spins into a coin and drops into the SIP jar; Mon-Fri ticks
tl.set(["#coin3", "#jar"], {opacity:0}, SC[3][0]); tl.set(".day", {opacity:0}, SC[3][0]);
tl.to("#cup3", {rotationY:90, duration:0.25, ease:"power2.in"}, T.swap);
tl.set("#cup3", {opacity:0}, T.swap + 0.25); tl.set("#coin3", {opacity:1, rotationY:-90}, T.swap + 0.25);
tl.to("#coin3", {rotationY:0, duration:0.25}, T.swap + 0.25);
pop("#jar", T.swap + 0.2); tl.to("#coin3", {y:250, scale:0.4, opacity:0, duration:0.5, ease:"power2.in"}, T.swap + 0.6);
document.querySelectorAll(".day").forEach((el, k) => pop(el, T.work + k*0.15));
tl.fromTo("#cam3", {scale:1.1, x:-54, y:-60}, {scale:1, x:0, y:0, duration:SC[3][1]-SC[3][0], ease:"none"}, SC[3][0]);
// 4 table: rows slide in with the voice
tl.set("#tbl", {opacity:0}, SC[4][0]); up("#tbl", SC[4][0] + 0.2);
tl.set([".tr"], {opacity:0}, SC[4][0]);
up("#t0", SC[4][0] + 0.4); up("#t1", T.wk); up("#t2", T.mo); up("#t3", T.yr);
tl.fromTo("#cam4", {scale:1.15, x:-81, y:-40}, {scale:1, x:0, y:0, duration:SC[4][1]-SC[4][0], ease:"power1.out"}, SC[4][0]);
// 5 20 years: counter + coin stack
const ci = {v:0}; tl.set("#inv", {opacity:0}, SC[5][0]); tl.to("#inv", {opacity:1, duration:0.2}, T.inv - 0.3);
tl.to(ci, {v:122500, duration:1.2, ease:"power2.out", onUpdate:() => { document.getElementById("inv").textContent = "₹" + Math.round(ci.v).toLocaleString("en-IN"); }}, T.inv - 0.3);
document.querySelectorAll("#sc5 .tok").forEach((el, k) => tl.fromTo(el, {opacity:0, y:-300}, {opacity:1, y:0, duration:0.3, ease:"bounce.out"}, SC[5][0] + 0.3 + k*0.12));
tl.fromTo("#cam5", {scale:1.2, x:-108, y:-120}, {scale:1, x:0, y:0, duration:1.4, ease:"power2.inOut"}, SC[5][0]);
// 6 growth illustration: bars, camera tilts up the tall bar
tl.set(["#g0", "#g1"], {scaleY:0}, SC[6][0]); tl.set(["#gv0", "#gv1"], {opacity:0}, SC[6][0]);
tl.set("#cam6", {scale:1, x:0, y:0}, SC[6][0]);
tl.to("#g0", {scaleY:1, duration:0.6, ease:"back.out(1.6)"}, T.nifty - 0.3); pop("#gv0", T.nifty);
tl.to("#g1", {scaleY:1, duration:1.2, ease:"power2.out"}, T.twelve);
tl.to("#cam6", {scale:1.12, x:-90, y:-30, duration:1.0, ease:"power2.inOut"}, T.twelve);
pop("#gv1", T.l49); tl.to("#cam6", {scale:1, x:0, y:0, duration:0.8, ease:"power2.inOut"}, T.l49 + 0.6);
// 7 risk: zigzag line draws, drops, shake
const zp = document.getElementById("zp"), ZL = zp.getTotalLength();
tl.set(zp, {strokeDasharray:ZL, strokeDashoffset:ZL}, SC[7][0]);
tl.to(zp, {strokeDashoffset:0, duration:2.4, ease:"none"}, SC[7][0] + 0.3);
tl.set(["#dn", "#pat"], {opacity:0}, SC[7][0]);
pop("#dn", T.fall, -3); shake("#sc7", T.fall + 0.1, 12); pop("#pat", T.fall + 1.2, 2);
tl.fromTo("#cam7", {scale:1.1, x:-54, y:-50}, {scale:1, x:0, y:0, duration:SC[7][1]-SC[7][0], ease:"none"}, SC[7][0]);
// 8 CTA
tl.fromTo("#cam8", {scale:1.1, x:-54, y:-60}, {scale:1, x:0, y:0, duration:1.4, ease:"power2.out"}, SC[8][0]);
tl.fromTo("#host", {y:120, opacity:0}, {y:0, opacity:1, duration:0.5, ease:EIN}, SC[8][0] + 0.2);
pop("#kw", T.comment, -3); pop("#sv", T.save, 2);
'''
