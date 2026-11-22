"""Scenes for '₹1 lakh in 2021: which stock made crores?' (Wealth Noir). Assembled by build.py."""
import os
H = os.path.dirname(os.path.abspath(__file__))
from importlib import util as _u
_s = _u.spec_from_file_location('sp', H + '/../../semipenny/build/scenes.py'); _sp = _u.module_from_spec(_s); _s.loader.exec_module(_sp)
TRACES = _sp.traces()
BGIMG = ''
SRC = lambda id_, t: f'<div class="src" id="{id_}">{t}</div>'
MAXV = 149.24

# rank, name, bought, today, value (lakh), label, key
ROWS = [(10, 'Hitachi Energy', '₹1,925.60', '₹30,150', 15.66, '₹15.7 L', 'hit'),
        (9, 'Servotech', '₹2.52', '₹63.86', 25.34, '₹25.3 L', 'servo'),
        (8, 'GE Vernova T&amp;D', '₹143.25', '₹4,235', 29.56, '₹29.6 L', 'gev'),
        (7, 'AXISCADES', '₹60.30', '₹1,873', 31.07, '₹31.1 L', 'axis'),
        (6, 'Kesar India', '₹24.63', '₹1,210', 49.13, '₹49.1 L', 'kesar'),
        (5, 'BSE', '₹65.64', '₹3,781', 57.60, '₹57.6 L', 'bse'),
        (4, 'Spectrum Electrical', '₹50.25', '₹4,468', 88.92, '₹88.9 L', 'spec')]


def row(r, y):
    rk, name, b, t, v, lab, key = r
    w = int(860 * v / MAXV)
    return f'''<div class="card" id="r_{key}" style="left:60px;top:{y}px;width:960px;height:190px;padding:18px 28px">
<div style="position:absolute;left:24px;top:22px;width:84px;height:84px;border-radius:50%;background:rgba(59,227,138,.15);border:3px solid var(--teal);text-align:center;font-family:Anton;font-size:50px;line-height:78px">{rk}</div>
<div style="position:absolute;left:130px;top:14px;font-family:Anton;font-size:56px">{name}</div>
<div style="position:absolute;left:132px;top:84px" class="lab">{b} → {t}</div>
<div class="val amb" id="v_{key}" style="position:absolute;right:28px;top:22px;font-size:76px">{lab}</div>
<div style="position:absolute;left:24px;right:24px;bottom:20px;height:22px;border-radius:11px;background:rgba(59,227,138,.10)">
<div class="bar" id="b_{key}" style="width:{w}px;height:100%;border-radius:11px;background:linear-gradient(90deg,#1E8F57,#3BE38A,#FFC94D);transform-origin:0 50%"></div></div></div>'''


def notes(id_, x, y, s):
    out = ''
    for k in range(6):
        out += f'<div class="note" style="left:{x + k * 14}px;top:{y - k * 18}px;width:{s}px;height:{int(s * .46)}px;transform:rotate({-4 + k * 1.6}deg)"><span>₹</span></div>'
    return f'<div id="{id_}" data-layout-ignore style="position:absolute;inset:0">{out}</div>'


def confetti():
    cols = ['#FFC94D', '#3BE38A', '#FFFFFF', '#FF9F43']
    out = ''
    for k in range(40):
        x = (k * 137) % 1040 + 20; c = cols[k % 4]; w = 14 + (k * 7) % 12; r = (k * 53) % 180
        out += f'<div class="cf" style="left:{x}px;top:-60px;width:{w}px;height:{w * 2}px;background:{c};transform:rotate({r}deg)"></div>'
    return out


SCN = {}
SCN[0] = '<div class="kick" id="h_y" style="top:230px">THE YEAR IS 2021</div>' + notes('h_notes', 300, 600, 460) + \
    '<div class="big amb" id="h_v" style="top:740px;font-size:180px">₹0</div>' \
    '<div class="pill" id="h_one" style="left:230px;top:960px;font-size:52px">☝ ONE STOCK. ONE CHOICE.</div>' \
    '<div class="big teal" id="h_c" style="top:1100px;font-size:96px">→ CRORES?</div>' \
    '<div class="big red" id="h_l" style="top:1220px;font-size:96px">→ A LOSS?</div>'
SCN[1] = '<div class="big" style="top:200px;font-size:96px">2021 → 2026</div><div class="kick" style="top:310px">WHAT ₹1 LAKH BECAME · #10 TO #7</div>' + \
    ''.join(row(r, 400 + k * 230) for k, r in enumerate(ROWS[:4])) + SRC('s1', '2021 prices: Trade Brains · today: INDmoney, 20 Nov 2026')
SCN[2] = '<div class="kick" style="top:260px">#6 TO #4</div>' + ''.join(row(r, 360 + k * 230) for k, r in enumerate(ROWS[4:])) + \
    '<div class="stamp" id="s2_st" style="left:120px;top:1110px;font-size:76px;transform:rotate(-4deg);color:#FFC94D;border-color:#FFC94D;text-shadow:0 0 24px rgba(255,201,77,.6)">SO CLOSE TO ₹1 CRORE</div>' + \
    SRC('s2', '2021 prices: Trade Brains · today: INDmoney, 20 Nov 2026')
SCN[3] = '<div class="kick" style="top:220px">#2</div><div class="big" id="n_n" style="top:270px;font-size:130px">NURTURE WELL</div>' \
    '<div class="pill a" id="n_b" style="left:250px;top:450px;font-size:44px">🍪 small biscuit maker</div>' \
    '<div class="card" id="n_c" style="left:90px;top:580px;width:900px;height:300px;text-align:center;padding-top:30px"><div class="lab">BOUGHT 19 MAY 2021 → TODAY</div>' \
    '<div class="val" style="font-size:130px;margin-top:10px"><span class="teal">₹0.14</span> → <span class="amb">₹17.86</span></div></div>' \
    '<div class="lab" style="position:absolute;left:0;right:0;top:940px;text-align:center;font-size:40px">₹1 LAKH IS NOW</div>' \
    '<div class="big amb" id="n_v" style="top:1000px;font-size:170px">₹0</div>' \
    '<div class="stamp" id="n_st" style="left:260px;top:1210px;font-size:80px;transform:rotate(-5deg);color:#3BE38A;border-color:#3BE38A;text-shadow:0 0 24px rgba(59,227,138,.6)">CRORE CLUB</div>' + \
    SRC('s3', '19 May 2021 price: Trade Brains · today: BSE close 20 Nov 2026 (INDmoney)')
SCN[4] = '<div class="big red" id="w_h" style="top:220px;font-size:140px">BUT WAIT…</div>' \
    '<svg id="w_ch" style="position:absolute;left:90px;top:420px;width:900px;height:600px" viewBox="0 0 900 600">' \
    '<line x1="40" y1="560" x2="880" y2="560" stroke="#3A4E5A" stroke-width="3"/>' \
    '<path id="w_line" d="M40 520 L200 440 L330 300 L430 90 L520 160 L620 250 L720 300 L860 330" stroke="#FF4D5E" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1" style="filter:drop-shadow(0 0 12px #FF4D5E)"/>' \
    '<circle id="w_pk" cx="430" cy="90" r="16" fill="#FFC94D"/><text x="300" y="60" font-family="Anton" font-size="52" fill="#FFC94D">APRIL: ₹2.51 CR</text>' \
    '<circle id="w_now" cx="860" cy="330" r="16" fill="#FF4D5E"/><text x="560" y="400" font-family="Anton" font-size="52" fill="#E9F4F7">NOW: ₹1.28 CR</text></svg>' \
    '<div class="stamp" id="w_st" style="left:180px;top:1100px;font-size:96px;transform:rotate(-5deg)">HALF IS GONE</div>' + \
    SRC('s4', 'April value: ₹35.10 on 24 Apr 2026 (Trade Brains) · chart illustrative')
SCN[5] = '<div id="cf">' + confetti() + '</div><div class="kick" style="top:220px">#1</div><div class="big amb" id="c_n" style="top:270px;font-size:170px">CUPID</div>' \
    '<div class="card" id="c_c" style="left:90px;top:520px;width:900px;height:300px;text-align:center;padding-top:30px"><div class="lab">JULY 2021 → TODAY</div>' \
    '<div class="val" style="font-size:104px;margin-top:16px"><span class="teal">₹2.45</span> → <span class="amb">₹365.65</span></div></div>' \
    '<div class="lab" style="position:absolute;left:0;right:0;top:880px;text-align:center;font-size:40px">₹1 LAKH BECAME</div>' \
    '<div class="big amb" id="c_v" style="top:940px;font-size:190px">₹0</div>' \
    '<div class="pill a" id="c_x" style="left:330px;top:1200px;font-size:56px">149× in ~5 years</div>' + \
    SRC('s5', 'July 2021 price: Sahi (14 Jul 2026 article) · today: NSE close 20 Nov 2026 (INDmoney)')
SCN[6] = '<div class="big red" id="p_h" style="top:210px;font-size:120px">THE TWIST</div>' \
    '<div class="kick" style="top:350px">BIGGEST IPO OF 2021</div><div class="big" id="p_n" style="top:410px;font-size:150px">PAYTM</div>' \
    '<div class="card r" id="p_c" style="left:90px;top:620px;width:900px;height:280px;text-align:center;padding-top:28px"><div class="lab">IPO PRICE NOV 2021 → TODAY</div>' \
    '<div class="val" style="font-size:120px;margin-top:10px"><span>₹2,150</span> → <span class="red">₹1,740</span></div></div>' \
    '<div class="lab" style="position:absolute;left:0;right:0;top:960px;text-align:center;font-size:40px">₹1 LAKH IS NOW</div>' \
    '<div class="big red" id="p_v" style="top:1020px;font-size:170px">₹1,00,000</div>' \
    '<div class="stamp" id="p_st" style="left:330px;top:1230px;font-size:90px;transform:rotate(-6deg)">LOSS</div>' + \
    SRC('s6', 'IPO price ₹2,150: PTI / Chittorgarh · today: NSE close 20 Nov 2026 (INDmoney)')
tiles = ''
TL = [('CUPID', '₹1.49 CR', 'g'), ('NURTURE', '₹1.28 CR', 'g'), ('SPECTRUM', '₹89 L', 'l'), ('BSE', '₹58 L', 'l'), ('KESAR', '₹49 L', 'l'),
      ('AXISCADES', '₹31 L', 'l'), ('GE VERNOVA', '₹30 L', 'l'), ('SERVOTECH', '₹25 L', 'l'), ('HITACHI', '₹16 L', 'l'), ('PAYTM', '₹81 K', 'r')]
for k, (n, v, kind) in enumerate(TL):
    x = 70 + (k % 2) * 480; y = 380 + (k // 2) * 150
    col = {'g': '#FFC94D', 'l': '#3BE38A', 'r': '#FF4D5E'}[kind]
    tiles += f'<div class="card t" id="t{k}" style="left:{x}px;top:{y}px;width:460px;height:130px;border-color:{col};padding:16px 24px"><div style="font-family:Anton;font-size:44px">{n}</div><div class="val" style="position:absolute;right:24px;top:30px;font-size:62px;color:{col}">{v}</div></div>'
SCN[7] = '<div class="big" style="top:200px;font-size:110px"><span class="amb">2</span> OUT OF <span>10</span></div>' + tiles + \
    '<div class="pill r" id="g_p" style="left:110px;top:1170px;font-size:42px">the stocks that crashed are never in these lists</div>' \
    '<div class="big" id="g_w" style="top:1270px;font-size:70px;color:#8FA6B2">you only hear about the winners</div>'
SCN[8] = '<div class="kick" style="top:220px">RAVI\'S LESSON</div><div class="big amb" style="top:280px;font-size:120px">3 RULES</div>' + \
    ''.join(f'<div class="card" id="k{k}" style="left:90px;top:{470 + k * 200}px;width:900px;height:170px;padding:0 40px;display:flex;align-items:center;gap:36px"><div class="val teal" style="font-size:90px">{k + 1}</div><div class="val" style="font-size:66px">{t}</div></div>'
            for k, t in enumerate(["Don't bet it all on one stock", 'Check the business', 'Be patient'])) + \
    '<div class="pill" id="e_s" style="left:190px;top:1110px;font-size:52px">🔖 SAVE THIS STORY</div>' \
    '<div class="pill a" id="e_f" style="left:150px;top:1230px;font-size:52px">➕ FOLLOW @moneyincloud</div>'
BG = [''] * 9

EXTRA_CSS = '''.note { position:absolute; border-radius:14px; background:linear-gradient(135deg,#2F6B48,#1C4A30); border:3px solid #6FD39B;
  box-shadow:0 14px 30px rgba(0,0,0,.5); display:flex; align-items:center; justify-content:center; }
.note span { font-family:Anton; font-size:110px; color:rgba(255,255,255,.35); }
.cf { position:absolute; border-radius:3px; opacity:.9; }
.card.t { box-shadow:0 18px 40px rgba(0,0,0,.5); }'''

JS_SCENES = '''
const cam = CAM(tl);
const cnt = (id, from, to, at, dur, fmt) => { const o = {v:from}; tl.to(o, {v:to, duration:dur, ease:"power2.out", onUpdate:() => { document.getElementById(id).textContent = fmt(o.v); }}, at); };
const inr = v => Math.round(v).toLocaleString("en-IN");
const lakh = v => v >= 100 ? "₹" + (v / 100).toFixed(2) + " CR" : "₹" + v.toFixed(1) + " L";
const slam = (sel, at, r) => tl.fromTo(sel, {scale:2.6, opacity:0, rotation:(r||0)}, {scale:1, opacity:1, duration:0.32, ease:"power4.in"}, at);
const flash = (at) => tl.fromTo("#flash", {opacity:0.28}, {opacity:0, duration:0.5, ease:"power2.out", immediateRender:false}, at);
const sweep = (at) => tl.fromTo("#sweep", {x:0}, {x:2300, duration:1.1, ease:"power2.inOut", immediateRender:false}, at);
tl.fromTo("#progf", {scaleX:0}, {scaleX:1, duration:T.DUR, ease:"none"}, 0);
document.querySelectorAll(".tr").forEach((el, k) => tl.fromTo(el, {strokeDashoffset:1}, {strokeDashoffset:-1, duration:3.2 + (k % 3), ease:"none", repeat:Math.floor(T.DUR / 3.2)}, k * 0.4));
tl.fromTo("#hz0", {x:0, y:0}, {x:120, y:80, duration:T.DUR / 2, ease:"sine.inOut", yoyo:true, repeat:1}, 0);
tl.fromTo("#hz1", {x:0, y:0}, {x:-100, y:-90, duration:T.DUR / 2, ease:"sine.inOut", yoyo:true, repeat:1}, 0);
tl.fromTo("#bgw", {x:0, y:0}, {x:-60, y:-80, duration:T.DUR, ease:"none"}, 0);
cam.handheld("#world", T.DUR, {rot:0.25, x:4, y:-3, period:3.2});
SC.forEach(([a, b], i) => { if (i > 0) cam.whip("#sc" + (i - 1), "#sc" + i, a, {dir: i % 2 ? 1 : -1, dur:0.4}); sweep(a + 0.1); });

// 0 hook
tl.set(["#h_y", "#h_one", "#h_c", "#h_l"], {opacity:0}, 0);
up("#h_y", 0.2);
tl.fromTo("#h_notes .note", {y:-500, opacity:0}, {y:0, opacity:1, duration:0.5, ease:"back.out(1.6)", stagger:0.08}, 0.3);
cnt("h_v", 0, 100000, T.one_lakh - 0.2, 1.2, v => "₹" + inr(v));
cam.pullOut("#cam0", 0, {from:1.35, to:1, dur:2.2, oy:"45%"});
pop("#h_one", T.pick - 0.2, -2);
slam("#h_c", T.crores - 0.2); cam.crashZoom("#cam0", T.crores, {to:1.15, oy:"62%", hold:0.6});
slam("#h_l", T.lost - 0.2, 2); flash(T.lost); cam.shake("#sc0", T.lost + 0.1, {amp:14});

// 1 + 2 leaderboard rows: slide in, bar grows, value counts
const ROWK = [["hit",15.66],["servo",25.34],["gev",29.56],["axis",31.07],["kesar",49.13],["bse",57.60],["spec",88.92]];
ROWK.forEach(([k, v]) => { tl.set("#r_" + k, {opacity:0}, SC[k === "kesar" || k === "bse" || k === "spec" ? 2 : 1][0]);
  tl.fromTo("#r_" + k, {opacity:0, x:-400}, {opacity:1, x:0, duration:0.5, ease:"power3.out"}, T[k] - 0.4);
  tl.fromTo("#b_" + k, {scaleX:0}, {scaleX:1, duration:1.0, ease:"power2.out"}, T[k] - 0.1);
  cnt("v_" + k, 1, v, T[k] - 0.1, 1.0, lakh); });
cam.track("#cam1", SC[1][0], {x0:0, y0:0, x:0, y:-70, dur:SC[1][1] - SC[1][0], ease:"sine.inOut"});
cam.tilt("#cam2", SC[2][0], {from:16, to:0, dur:1.2});
tl.set("#s2_st", {opacity:0}, SC[2][0]); slam("#s2_st", T.close - 0.2, -4); cam.shake("#sc2", T.close + 0.1, {amp:10});

// 3 Nurture Well
tl.set(["#n_n", "#n_b", "#n_c", "#n_st"], {opacity:0}, SC[3][0]);
up("#n_n", T.n2 - 0.2); pop("#n_b", T.biscuit - 0.2, -2); pop("#n_c", T.paise - 0.3);
cam.orbit("#n_c", T.paise - 0.3, {from:-20, to:8, dur:2});
cnt("n_v", 1, 127.57, T.today2, 1.4, lakh); slam("#n_st", T.today2 + 1.5, -5); flash(T.today2 + 1.6);
cam.crashZoom("#cam3", T.today2 + 1.45, {to:1.15, oy:"60%", hold:0.6});

// 4 but wait
tl.set(["#w_h", "#w_st", "#w_pk", "#w_now"], {opacity:0}, SC[4][0]);
slam("#w_h", T.wait - 0.2); cam.dutch("#cam4", T.wait, {deg:-6, dur:0.4, hold:2.2});
tl.to("#w_line", {strokeDashoffset:0, duration:1.8, ease:"power2.inOut"}, T.april - 0.3);
pop("#w_pk", T.april + 0.4); pop("#w_now", T.gone - 0.2);
slam("#w_st", T.gone, -5); flash(T.gone + 0.2); cam.shake("#sc4", T.gone + 0.2, {amp:16});

// 5 Cupid #1
tl.set(["#c_n", "#c_c", "#c_x"], {opacity:0}, SC[5][0]);
slam("#c_n", T.n1 - 0.2); pop("#c_c", T.p245 - 0.3);
cnt("c_v", 1, 149.24, T.became - 0.2, 1.6, lakh); pop("#c_x", T.became + 1.6, -2);
cam.crashZoom("#cam5", T.became + 1.3, {to:1.18, oy:"58%", hold:0.8}); flash(T.became + 1.4);
tl.fromTo("#cf .cf", {y:0, rotation:0}, {y:2100, rotation:540, duration:3.2, ease:"power1.in", stagger:{each:0.04}}, T.became + 1.2);
cam.pushIn("#cam5", SC[5][0], {from:1.08, to:1, dur:1.6});

// 6 Paytm twist
tl.set(["#p_h", "#p_n", "#p_c", "#p_st"], {opacity:0}, SC[6][0]);
slam("#p_h", T.twist - 0.2); up("#p_n", T.paytm - 0.3); pop("#p_c", T.paytm + 0.6);
cnt("p_v", 100000, 80930, T.worth, 1.4, v => "₹" + inr(v)); slam("#p_st", T.worth + 1.5, -6); flash(T.worth + 1.6);
cam.dutch("#cam6", T.worth + 1.4, {deg:5, dur:0.4, hold:1.0}); cam.shake("#sc6", T.worth + 1.6, {amp:16});

// 7 2 out of 10
tl.set(["#g_p", "#g_w"], {opacity:0}, SC[7][0]);
tl.fromTo("#cam7 .card.t", {opacity:0, scale:0.6}, {opacity:1, scale:1, duration:0.35, ease:"back.out(2)", stagger:0.12}, SC[7][0] + 0.2);
tl.to(["#t2","#t3","#t4","#t5","#t6","#t7","#t8","#t9"], {opacity:0.35, duration:0.4}, Math.max(T.two + 0.4, SC[7][0] + 1.6));
pop("#g_p", T.crashed - 0.2); up("#g_w", T.winners - 0.3);
cam.rack("#cam7", SC[7][0], {blur:10, dur:0.8}); cam.pushIn("#cam7", T.two, {from:1, to:1.06, dur:2.5, oy:"35%"});

// 8 rules + CTA
tl.set(["#k0", "#k1", "#k2", "#e_s", "#e_f"], {opacity:0}, SC[8][0]);
[["bet",0],["check",1],["patient",2]].forEach(([k, i]) => tl.fromTo("#k" + i, {opacity:0, x:-300}, {opacity:1, x:0, duration:0.45, ease:"power3.out"}, T[k] - 0.3));
pop("#e_s", T.save - 0.1, -2); pop("#e_f", T.follow - 0.1, 2);
cam.pullOut("#cam8", SC[8][0], {from:1.2, to:1, dur:1.4});
'''
