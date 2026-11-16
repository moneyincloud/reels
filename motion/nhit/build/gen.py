"""₹1 lakh in National Highways Infra Trust: colourful Vox reel with camera moves. usage: python3 gen.py"""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(H + '/t.json'))
DUR = T['DUR']; S = T['STARTS']; V = T['VO']; DU = T['DURS']

CAPTXT = [
    "Put ₹1 lakh into India's highway trust and toll roads pay you every quarter. But there's a catch.",
    "National Highways Infra Trust (NHIT) owns toll roads monetised by NHAI. Every toll a truck pays, part flows to unitholders.",
    "At ₹169 a unit, ₹1 lakh buys about 591 units.",
    "June quarter: ₹3.187 per unit. That's about ₹1,880 on your ₹1 lakh.",
    "September quarter: ₹2.529 declared. About ₹1,495. The payout changes every quarter.",
    "Most of it is interest, so it's taxed at your income-tax slab.",
    "Now the catch. NHIT is privately placed. On NSE it trades in lots of 25,000 units. At today's price, that's about ₹42 lakh.",
    "So with ₹1 lakh you can't buy it on the exchange. Public InvITs, like NHAI's newer Raajmarg trust, trade 1 unit at a time.",
    "Would you buy highway income? Comment ROAD, and save this.",
]
caps = []
for i, line in enumerate(CAPTXT):
    gs, cur = [], []
    for w in line.split():
        cur.append(w)
        if len(cur) >= 5 or re.search(r'[.,?!:]$', w): gs.append(cur); cur = []
    if cur: gs.append(cur)
    tot = sum(len(' '.join(g)) for g in gs); acc = 0
    for g in gs:
        txt = ' '.join(g); st = V[i] + DU[i] * acc / tot; acc += len(txt); en = V[i] + DU[i] * acc / tot
        caps.append([round(st, 2), round(en, 2), txt])
for k in range(len(caps) - 1):
    caps[k][1] = round(min(max(caps[k][1], caps[k + 1][0] - 0.02), caps[k][1] + 0.6), 2)

# scenes: 0 hook | 1 how it works | 2 units | 3 payouts (VO3-4) | 4 tax | 5 catch | 6 route | 7 CTA
SC = [(0, S[1]), (S[1], S[2]), (S[2], S[3]), (S[3], S[5]), (S[5], S[6]), (S[6], S[7]), (S[7], S[8]), (S[8], DUR)]
BG = ['#FFF1B8', '#D7F5E9', '#E6E0FF', '#DDF0FF', '#FFE2D1', '#FFD6DE', '#D9F7D0', '#FFF1B8']

toks = '\n'.join(f'<div class="tok" id="tk{k}" style="left:{150 + (k % 14) * 56}px;top:{720 + (k // 14) * 56}px"></div>' for k in range(84))

SCN = {}
SCN[0] = '''<div class="ttl hand" style="top:240px">₹1 lakh in India's<br>highway trust?</div>
<div id="road"><div id="lane"></div></div>
<div class="emo" id="booth" style="left:760px;top:470px;font-size:190px">🛂</div>
<div class="emo" id="truck" style="color:#fff;left:-260px;top:660px;font-size:210px;transform:scaleX(-1)">🚚</div>
<div class="emo" id="coin0" style="left:820px;top:520px;font-size:90px">🪙</div>
<div class="emo" id="coin1" style="left:860px;top:520px;font-size:90px">🪙</div>
<div class="stk" id="wal" style="left:90px;top:1000px;background:#1E8E4E;color:#fff;transform:rotate(-3deg)">₹1,00,000</div>
<div class="stk" id="ctch" style="left:560px;top:990px;background:#D93A2B;color:#fff;transform:rotate(4deg)">THE CATCH?</div>'''
SCN[1] = '''<div class="ttl hand" style="top:220px;font-size:84px">How NHIT pays you</div>
<div class="node" id="n0" style="left:60px;top:430px"><div class="e">🛣️</div><b>NHAI toll roads</b></div>
<div class="node" id="n1" style="left:700px;top:430px"><div class="e">🚚</div><b>trucks pay toll</b></div>
<div class="node" id="n2" style="left:700px;top:820px"><div class="e">🏦</div><b>NHIT trust</b></div>
<div class="node" id="n3" style="left:60px;top:820px"><div class="e">🙋</div><b>unitholders</b></div>
<div class="arr" id="a0" style="left:370px;top:540px;width:300px"></div>
<div class="arr" id="a1" style="left:850px;top:700px;width:100px;transform:rotate(90deg)"></div>
<div class="arr" id="a2" style="left:670px;top:930px;width:300px;transform:rotate(180deg)"></div>'''
SCN[2] = f'''<div class="card" style="left:70px;right:70px;top:330px;height:300px;display:flex;align-items:center;justify-content:center;gap:24px;font-family:Anton;font-size:96px">
<span style="color:#1E8E4E">₹1,00,000</span><span>÷</span><span>₹169</span></div>
<div class="big" id="u591" style="left:0;right:0;text-align:center;top:1010px;font-size:120px;color:#6C4BD8">= 591 units</div>
{toks}'''
SCN[3] = '''<div class="ttl hand" id="t3" style="top:250px;font-size:84px">What ₹1 lakh earned</div>
<div id="chart" style="position:absolute;left:120px;right:120px;top:400px;height:620px;border-bottom:8px solid #1B1B1F">
<div class="bar" id="b0" style="left:60px;height:560px;background:#2BB673"></div>
<div class="bar" id="b1" style="right:60px;height:444px;background:#3B82F6"></div>
<div class="blab" id="v0" style="left:40px;top:-10px;color:#1E8E4E">₹1,883</div>
<div class="blab" id="v1" style="right:40px;top:106px;color:#1D4ED8">₹1,495</div></div>
<div class="blab" style="left:150px;top:1035px;font-size:40px">JUN QTR · ₹3.187/unit</div>
<div class="blab" style="right:150px;top:1035px;font-size:40px">SEP QTR · ₹2.529/unit</div>
<div class="stk" id="chg" style="left:250px;top:250px;background:#FFE45C;transform:rotate(-4deg);font-size:50px">changes every quarter ↕</div>'''
SCN[4] = '''<div class="emo" id="rcpt" style="left:0;right:0;text-align:center;top:330px;font-size:260px">🧾</div>
<div class="card" id="taxc" style="left:90px;right:90px;top:690px;padding:34px 40px;text-align:center">
<div style="font-family:Anton;font-size:76px">MOSTLY <span style="color:#D93A2B">INTEREST</span></div>
<div style="font-family:Poppins;font-size:44px;margin-top:10px">→ taxed at your income-tax slab</div></div>'''
SCN[5] = '''<div class="stk" id="ctch2" style="left:300px;top:230px;background:#D93A2B;color:#fff;transform:rotate(-3deg);font-size:80px">THE CATCH</div>
<div class="card" id="lotc" style="left:70px;right:70px;top:420px;padding:26px 36px">
<div style="font-family:Poppins;font-size:38px;color:#5B5B66">NSE trading lot (privately placed InvIT)</div>
<div style="display:flex;justify-content:space-between;font-family:Anton;font-size:64px;margin-top:8px"><span>25,000 units</span><span>× ₹169</span></div>
<div style="display:flex;justify-content:space-between;border-top:5px solid #1B1B1F;margin-top:10px;padding-top:8px;font-family:Anton;font-size:84px"><span>=</span><span style="color:#D93A2B" id="l42">₹42.25 lakh</span></div></div>
<div id="cmp" style="position:absolute;left:110px;top:840px;width:860px;height:300px">
<div style="position:absolute;left:0;top:0;font-family:Anton;font-size:40px">your ₹1 lakh</div>
<div id="cb0" style="position:absolute;left:0;top:56px;width:20px;height:70px;background:#2BB673;border:5px solid #1B1B1F;border-radius:8px"></div>
<div style="position:absolute;left:0;top:150px;font-family:Anton;font-size:40px">1 lot = 42× more</div>
<div id="cb1" style="position:absolute;left:0;top:206px;width:845px;height:70px;background:#D93A2B;border:5px solid #1B1B1F;border-radius:8px;transform-origin:0 50%"></div></div>'''
SCN[6] = '''<div class="card" id="r0" style="left:80px;right:80px;top:290px;padding:28px 36px;display:flex;align-items:center;gap:28px">
<span style="font-size:110px">🔒</span><div><div style="font-family:Anton;font-size:62px">NHIT units</div><div style="font-family:Poppins;font-size:38px">₹42 lakh lots · not for ₹1 lakh</div></div></div>
<div class="card" id="r1" style="left:80px;right:80px;top:640px;padding:28px 36px;display:flex;align-items:center;gap:28px;background:#ECFFF1">
<span style="font-size:110px">✅</span><div><div style="font-family:Anton;font-size:62px;color:#1E8E4E">Public InvITs</div><div style="font-family:Poppins;font-size:38px">1 unit at a time · e.g. Raajmarg (RIIT)</div></div></div>'''
SCN[7] = '''<div class="ttl hand" style="top:240px">Would you buy<br>highway income?</div>
<img id="host" src="assets/img/s0_008.png" style="position:absolute;left:40px;top:600px;width:360px"/>
<div class="emo" style="left:470px;top:560px;font-size:150px">🛣️</div>
<div class="pill" id="kw" style="left:430px;top:780px;background:#1E8E4E;font-size:76px">COMMENT ROAD</div>
<div class="pill" id="sv" style="left:430px;top:960px;background:#FFE45C;color:#1B1B1F;font-size:56px">💾 SAVE THIS</div>'''

def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;')
body = '\n'.join(f'<section class="scene clip" id="sc{i}" style="--bg:{BG[i]}" data-start="{a:.2f}" data-duration="{min(b + 0.35, DUR) - a:.2f}" data-track-index="{i + 1}"><div class="cam" id="cam{i}">{SCN[i]}</div></section>'
                 for i, (a, b) in enumerate(SC))
caps_html = '\n'.join(f'<div class="cap" id="cap{k}"><span>{esc(t)}</span></div>' for k, (_, _, t) in enumerate(caps))

JS = '''const T = %s, CAPS = %s, SC = %s;
const tl = gsap.timeline({ paused: true });
const EIN = "expo.out";
const pop = (sel, at, r) => tl.fromTo(sel, {scale:0.3, opacity:0, rotation:(r||0)-8}, {scale:1, opacity:1, rotation:r||0, duration:0.5, ease:"back.out(2.2)"}, at);
const up = (sel, at) => tl.fromTo(sel, {opacity:0, y:30}, {opacity:1, y:0, duration:0.45, ease:EIN}, at);
const shake = (sel, at, a) => { const kf = []; for (let k = 0; k < 8; k++) kf.push({y:(k%%2?-1:1)*(a||14)*(1-k/8), duration:0.04, ease:"none"}); kf.push({y:0, duration:0.04}); tl.to(sel, {keyframes:kf}, at); };
tl.to("#world", {rotation:0.35, x:5, y:-4, duration:3, ease:"sine.inOut", repeat:Math.max(0, Math.floor(T.DUR/3)-1), yoyo:true}, 0);
SC.forEach(([a, b], i) => { const s = "#sc" + i;
  if (i > 0) tl.fromTo(s, {x:(i%%2? 1150 : -1150), filter:"blur(14px)"}, {x:0, filter:"blur(0px)", duration:0.5, ease:"power3.out"}, a - 0.05);
  if (i < SC.length - 1) tl.to(s, {x:(i%%2? 1150 : -1150), filter:"blur(14px)", duration:0.42, ease:"power3.in"}, b - 0.37); });
// 0 hook: truck drives to the toll booth, coins fly to the ₹1 lakh wallet, camera pushes in
tl.fromTo("#cam0", {scale:1.25, x:-140, y:-120}, {scale:1, x:0, y:0, duration:3.0, ease:"power2.inOut"}, 0);
tl.fromTo("#lane", {x:0}, {x:-680, duration:SC[0][1], ease:"none"}, 0);
tl.to("#truck", {x:820, duration:T.toll - 0.2, ease:"power2.out"}, 0.1);
tl.set(["#coin0", "#coin1", "#wal", "#ctch"], {opacity:0}, 0);
[0, 1].forEach(k => tl.fromTo("#coin" + k, {opacity:1, x:0, y:0, scale:0.6}, {x:-640 - k*40, y:470, scale:1, duration:0.8, ease:"power2.in"}, T.toll + k*0.2));
tl.set(["#coin0", "#coin1"], {opacity:0}, T.toll + 1.2);
pop("#wal", T.toll + 0.9, -3); pop("#ctch", T.catch0, 4); shake("#sc0", T.catch0 + 0.05, 12);
// 1 how it works: camera follows the money around the loop
tl.set("#cam1", {scale:1.12, x:-30, y:-110}, SC[1][0]);
["#n0", "#n1", "#n2", "#n3"].forEach((s, k) => pop(s, SC[1][0] + 0.4 + k*0.55));
tl.set([".arr"], {scaleX:0}, SC[1][0]);
tl.to("#a0", {scaleX:1, duration:0.5}, T.truck - 0.3);
tl.to("#cam1", {x:-100, y:-110, duration:0.9, ease:"power2.inOut"}, T.truck - 0.4);
tl.to("#a1", {scaleX:1, duration:0.4}, T.truck + 0.6);
tl.to("#cam1", {x:-100, y:-230, duration:0.9, ease:"power2.inOut"}, T.truck + 0.5);
tl.to("#a2", {scaleX:1, duration:0.5}, T.flows - 0.3);
tl.to("#cam1", {scale:1, x:0, y:0, duration:1.0, ease:"power3.inOut"}, T.flows);
// 2 units: tokens rain in, counter
tl.fromTo("#cam2", {scale:1.12, x:-60, y:-60}, {scale:1, x:0, y:0, duration:SC[2][1]-SC[2][0], ease:"none"}, SC[2][0]);
document.querySelectorAll(".tok").forEach((el, k) => tl.fromTo(el, {opacity:0, y:-260}, {opacity:1, y:0, duration:0.3, ease:"bounce.out"}, T.units - 0.8 + k*0.022));
const c591 = {v:0}; tl.set("#u591", {opacity:0}, SC[2][0]);
tl.to("#u591", {opacity:1, duration:0.2}, T.units);
tl.to(c591, {v:591, duration:0.9, ease:"power2.out", onUpdate:() => { document.getElementById("u591").textContent = "= " + Math.round(c591.v) + " units"; }}, T.units);
// 3 payouts: bars grow, camera pans from June to September
tl.set(["#b0", "#b1"], {scaleY:0}, SC[3][0]); tl.set(["#v0", "#v1", "#chg"], {opacity:0}, SC[3][0]);
tl.set("#cam3", {scale:1.3, x:-30, y:-340}, SC[3][0]);
tl.to("#b0", {scaleY:1, duration:0.8, ease:"back.out(1.6)"}, T.jun); pop("#v0", T.r1880);
tl.to("#cam3", {x:-300, duration:1.0, ease:"power2.inOut"}, T.sep - 0.8);
tl.to("#b1", {scaleY:1, duration:0.8, ease:"back.out(1.6)"}, T.sep); pop("#v1", T.r1495);
tl.to("#cam3", {scale:1, x:0, y:0, duration:1.0, ease:"power3.inOut"}, T.changes - 0.4);
tl.set("#t3", {opacity:0}, SC[3][0]);
pop("#chg", T.changes + 0.2, -4);
tl.to("#b1", {scaleY:0.9, duration:0.5, yoyo:true, repeat:1, ease:"sine.inOut"}, T.changes + 0.4);
// 4 tax: stamp
tl.fromTo("#rcpt", {y:-300, rotation:-20}, {y:0, rotation:0, duration:0.6, ease:"bounce.out"}, SC[4][0] + 0.1);
tl.fromTo("#taxc", {scale:2, opacity:0, rotation:-6}, {scale:1, opacity:1, rotation:-2, duration:0.35, ease:"power4.in"}, T.tax - 0.3);
shake("#sc4", T.tax + 0.05, 10);
// 5 catch: the lot card, then the camera pulls back to compare ₹1 lakh with one lot
tl.set("#cam5", {scale:1.2, x:-108, y:-90}, SC[5][0]);
pop("#ctch2", T.catch, -3); shake("#sc5", T.catch + 0.1, 12);
up("#lotc", T.priv);
tl.fromTo("#l42", {scale:0.4, opacity:0}, {scale:1, opacity:1, duration:0.5, ease:"back.out(2.5)"}, T.lot + 0.9);
tl.to("#cam5", {scale:1, x:0, y:0, duration:1.1, ease:"power3.inOut"}, T.lot + 0.3);
tl.set("#cmp", {opacity:0}, SC[5][0]); tl.to("#cmp", {opacity:1, duration:0.3}, T.lot + 1.2);
tl.fromTo("#cb1", {scaleX:0.02}, {scaleX:1, duration:1.3, ease:"power2.inOut"}, T.lot + 1.4);
// 6 route: lock vs tick
tl.fromTo("#cam6", {scale:1.1, x:-54, y:-40}, {scale:1, x:0, y:0, duration:SC[6][1]-SC[6][0], ease:"none"}, SC[6][0]);
pop("#r0", T.cant - 0.4, -1); shake("#sc6", T.cant, 8); pop("#r1", T.pub + 0.2, 1);
// 7 CTA
tl.fromTo("#cam7", {scale:1.1, x:-54, y:-60}, {scale:1, x:0, y:0, duration:1.4, ease:"power2.out"}, SC[7][0]);
tl.fromTo("#host", {y:120, opacity:0}, {y:0, opacity:1, duration:0.5, ease:EIN}, SC[7][0] + 0.2);
pop("#kw", T.comment, -3); pop("#sv", T.save, 2);
CAPS.forEach(([s, e], k) => { const g = "#cap" + k;
  tl.fromTo(g, {opacity:0, y:14}, {opacity:1, y:0, duration:0.14, ease:"power2.out"}, Math.max(0.15, s - 0.05));
  tl.to(g, {opacity:0, duration:0.1}, e - 0.1); tl.set(g, {opacity:0, visibility:"hidden"}, e); });
window.__timelines = window.__timelines || {};
window.__timelines["main"] = tl;''' % (json.dumps(T), json.dumps(caps), json.dumps(SC))

html = open(H + '/template.html').read()
for k, v in dict(DUR=f'{DUR:.2f}', BODY=body, CAPS_HTML=caps_html, JS=JS).items():
    html = html.replace('__' + k + '__', v)
open(H + '/../index.html', 'w').write(html)
print('caps', len(caps), 'dur', round(DUR, 1))
