"""Scenes for 'Semiconductor penny stocks: multibagger or trap?' (Silicon Noir). Assembled by build.py."""
import os, re
H = os.path.dirname(os.path.abspath(__file__))
IMG = H + '/../assets/img/'
MAPS = '/home/claude/reels/studio/kalyan/maps/'
india = ''.join(re.findall(r'<path[\s\S]*?/>', open(MAPS + 'node_modules/@svg-maps/india/india.svg').read()))
india = re.sub(r'\s+', ' ', india)


def has(n):
    return os.path.exists(IMG + n + '.jpg')


def photo(n, id_, x, y, w, h, r=0, fallback=''):
    if has(n):
        return f'<div class="photo" id="{id_}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({r}deg)"><img src="assets/img/{n}.jpg"/><div style="position:absolute;right:12px;bottom:10px;padding:2px 12px;border-radius:8px;background:rgba(5,11,20,.7);font-family:Oswald;font-size:28px;color:#B9C6CC">illustration</div></div>'
    return fallback


def chip(id_, x, y, s, glow='#2EE6C5', label='', cracked=False):
    """SVG microchip, s = body size in px"""
    pins = ''
    n = 8
    for k in range(n):
        p = 30 + k * (140 / (n - 1))
        pins += f'<rect x="{p-5}" y="2" width="10" height="26" rx="2" fill="#B9C6CC"/><rect x="{p-5}" y="172" width="10" height="26" rx="2" fill="#B9C6CC"/>'
        pins += f'<rect x="2" y="{p-5}" width="26" height="10" rx="2" fill="#B9C6CC"/><rect x="172" y="{p-5}" width="26" height="10" rx="2" fill="#B9C6CC"/>'
    crack = '<path d="M62 40 L92 88 L78 104 L118 160" stroke="#FF4D5E" stroke-width="5" fill="none" stroke-linecap="round"/>' if cracked else ''
    lab = f'<text data-layout-ignore x="100" y="152" text-anchor="middle" font-family="Oswald" font-size="13" fill="#6F8794" letter-spacing="2">{label}</text>' if label else ''
    return f'''<svg id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s}px;overflow:visible;filter:drop-shadow(0 0 40px {glow}66) drop-shadow(0 30px 40px rgba(0,0,0,.7))" viewBox="0 0 200 200">
{pins}<rect x="26" y="26" width="148" height="148" rx="14" fill="#0B1218" stroke="{glow}" stroke-width="3"/>
<rect x="56" y="56" width="88" height="88" rx="6" fill="#111C24" stroke="{glow}" stroke-opacity=".6" stroke-width="2"/>
<g stroke="{glow}" stroke-opacity=".55" stroke-width="2">{''.join(f'<line x1="64" y1="{70+i*14}" x2="136" y2="{70+i*14}"/>' for i in range(6))}</g>
<circle cx="44" cy="44" r="5" fill="{glow}"/>{lab}{crack}</svg>'''


def traces():
    """deterministic circuit traces for the background"""
    out = []
    pts = [(80, 300, 380, 300, 380, 620, 700, 620), (1240, 200, 980, 200, 980, 520, 760, 520), (120, 1300, 420, 1300, 420, 1000, 640, 1000),
           (1200, 1700, 900, 1700, 900, 1420, 620, 1420), (60, 1900, 300, 1900, 300, 1640, 520, 1640), (1260, 960, 1060, 960, 1060, 1180, 840, 1180),
           (200, 80, 200, 220, 560, 220, 560, 420), (700, 2100, 700, 1900, 1000, 1900, 1000, 1760)]
    for k, p in enumerate(pts):
        d = 'M' + ' L'.join(f'{p[i]},{p[i+1]}' for i in range(0, len(p), 2))
        out.append(f'<path d="{d}" stroke="rgba(46,230,197,.14)" stroke-width="4" fill="none"/>')
        out.append(f'<path class="tr" id="tr{k}" d="{d}" stroke="{"#2EE6C5" if k % 3 else "#FFB547"}" stroke-width="5" fill="none" pathLength="1" stroke-dasharray=".12 .88" stroke-dashoffset="1" opacity=".9" style="filter:drop-shadow(0 0 8px #2EE6C5)"/>')
        out.append(f'<circle cx="{p[-2]}" cy="{p[-1]}" r="9" fill="#0B1218" stroke="rgba(46,230,197,.5)" stroke-width="3"/>')
    return ''.join(out)


BGIMG = '<img src="assets/img/u6.jpg"/>' if has('u6') else ''
SRC = lambda id_, t: f'<div class="src" id="{id_}">{t}</div>'

SCN = {}
# 0 hook
SCN[0] = ('<div class="photo" id="h_img" style="left:0;top:0;width:1080px;height:1920px;border:none;border-radius:0"><img src="assets/img/u1.jpg"/></div><div style="position:absolute;right:40px;top:1380px;font-family:Oswald;font-size:28px;color:#8FA6B2">illustration</div>'
          '<div data-layout-ignore style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(5,11,20,.75) 0%,rgba(5,11,20,.15) 30%,rgba(5,11,20,.35) 50%,rgba(5,11,20,.92) 75%)"></div>'
          if has('u1') else chip('h_chip', 290, 470, 500, '#2EE6C5', 'NSE · BSE')) + \
    '<div class="kick" id="h_k" style="top:240px">CHIP STOCKS UNDER ₹100</div>' \
    '<div class="big teal" id="h_m" style="top:1040px;font-size:170px">MULTIBAGGER</div>' \
    '<div class="big red" id="h_t" style="top:1230px;font-size:190px">OR TRAP?</div>'
# 1 SPEL intro
SCN[1] = '<div class="kick" style="top:220px">STOCK #1</div><div class="big" id="s_n" style="top:280px;font-size:118px">SPEL SEMICONDUCTOR</div>' + \
    photo('u3', 's_img', 230, 430, 620, 580, -1.5, chip('s_chip', 380, 480, 320, '#FFB547', 'IC ASSEMBLY')) + \
    '<div class="pill a" id="s_c" style="left:90px;top:1040px;font-size:44px">📍 Chennai, Tamil Nadu</div>' \
    '<div class="pill" id="s_o" style="left:90px;top:1140px;font-size:40px">Packs &amp; tests chips (OSAT)</div>' \
    '<div class="pill" id="s_f" style="left:90px;top:1240px;font-size:40px">"India\'s first OSAT"</div>' \
    '<div class="card" id="s_p" style="left:690px;top:1060px;width:320px;height:250px;text-align:center;padding-top:30px"><div class="lab">PRICE</div><div class="val amb" style="font-size:110px">₹77.55</div></div>' + \
    SRC('s_src', 'SPEL filings (BSE) · price: INDmoney, 20 Nov 2026')
# 2 the catch
SCN[2] = '<div class="big red" id="c_h" style="top:220px;font-size:140px">THE CATCH</div>' \
    '<svg id="c_fac" style="position:absolute;left:290px;top:400px;width:500px;height:330px" viewBox="0 0 500 330">' \
    '<path d="M20 320 V150 L140 90 V150 L260 90 V150 L380 90 V320 Z" fill="#101C26" stroke="#8FA6B2" stroke-width="5"/>' \
    '<rect x="390" y="30" width="60" height="290" fill="#101C26" stroke="#8FA6B2" stroke-width="5"/>' \
    '<g fill="#1B2C38">' + ''.join(f'<rect x="{50+k*80}" y="200" width="50" height="50" rx="4"/>' for k in range(4)) + '</g>' \
    '<g id="c_smoke" fill="rgba(143,166,178,.25)"><circle cx="420" cy="20" r="0"/></g></svg>' \
    '<div class="stamp" id="c_st" style="left:150px;top:600px;font-size:86px;transform:rotate(-8deg)">SHUT SINCE 14 JAN</div>' \
    '<div class="card" id="c_s" style="left:70px;top:840px;width:450px;height:440px;padding:30px"><div class="lab">FY26 SALES</div>' \
    '<div class="val teal" style="font-size:96px;margin-top:10px" id="c_sv">₹6.28 cr</div><div style="position:absolute;left:30px;right:30px;bottom:40px;height:40px;border-radius:20px;background:rgba(46,230,197,.12)">' \
    '<div id="c_sb" style="width:26%;height:100%;border-radius:20px;background:#2EE6C5;transform-origin:0 50%"></div></div></div>' \
    '<div class="card r" id="c_l" style="left:560px;top:840px;width:450px;height:440px;padding:30px"><div class="lab">FY26 LOSS</div>' \
    '<div class="val red" style="font-size:96px;margin-top:10px" id="c_lv">₹23.84 cr</div><div style="position:absolute;left:30px;right:30px;bottom:40px;height:40px;border-radius:20px;background:rgba(255,77,94,.12)">' \
    '<div id="c_lb" style="width:100%;height:100%;border-radius:20px;background:#FF4D5E;transform-origin:0 50%"></div></div></div>' + \
    SRC('c_src', 'FY26 results (19 May 2026) · plant shut since 14 Jan 2026')
# 3 valuation
SCN[3] = '<div class="kick" style="top:230px">THE MARKET STILL VALUES IT AT</div>' \
    '<div class="big amb" id="v_mc" style="top:300px;font-size:200px">₹0 cr</div>' \
    '<div class="big" style="top:520px;font-family:Oswald;font-size:44px;color:#8FA6B2">market cap · vs ₹6.28 cr yearly sales</div>' \
    '<svg id="v_ch" style="position:absolute;left:90px;top:640px;width:900px;height:520px" viewBox="0 0 900 520">' \
    '<line x1="40" y1="480" x2="880" y2="480" stroke="#3A4E5A" stroke-width="3"/>' \
    '<line x1="40" y1="70" x2="880" y2="70" stroke="#FFB547" stroke-dasharray="10 10" stroke-width="3" opacity=".7"/>' \
    '<text x="50" y="55" font-family="Oswald" font-size="32" fill="#FFB547">52-week high ₹157</text>' \
    '<path id="v_line" d="M40 300 L140 180 L230 70 L330 160 L430 230 L520 200 L620 290 L720 330 L800 380 L870 330" stroke="#FF4D5E" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1" style="filter:drop-shadow(0 0 12px #FF4D5E)"/>' \
    '<circle id="v_dot" cx="870" cy="330" r="16" fill="#FF4D5E"/><text x="760" y="430" font-family="Anton" font-size="48" fill="#E9F4F7">₹77.55</text></svg>' \
    '<div class="stamp" id="v_st" style="left:250px;top:1190px;font-size:110px;transform:rotate(-5deg)">-51% FROM HIGH</div>' + \
    SRC('v_src', 'Market cap & 52-wk high: INDmoney 20 Nov 2026 · chart illustrative')
# 4 MIC
SCN[4] = '<div class="kick" style="top:220px">STOCK #2</div><div class="big" id="m_n" style="top:280px;font-size:130px">MIC ELECTRONICS</div>' \
    '<div class="card" id="m_c" style="left:140px;top:470px;width:800px;height:330px;text-align:center;padding-top:40px"><div class="lab">PRICE</div>' \
    '<div class="val teal" style="font-size:150px">₹35.32</div><div class="lab" style="margin-top:6px">52-week high ₹57.60 · <span style="color:#FF4D5E">-39%</span></div></div>' \
    '<div class="lab" style="position:absolute;left:0;right:0;top:860px;text-align:center;font-size:40px">WHAT IT ACTUALLY SELLS</div>' \
    '<div class="pill a" id="m_t0" style="left:110px;top:940px;font-size:48px">💡 LED displays</div>' \
    '<div class="pill a" id="m_t1" style="left:520px;top:940px;font-size:48px">🚆 Railway systems</div>' \
    '<div class="pill a" id="m_t2" style="left:330px;top:1050px;font-size:48px">⚡ EV charging</div>' \
    '<div class="stamp" id="m_st" style="left:210px;top:1190px;font-size:78px;transform:rotate(-4deg)">CHIP LINK: WEAK</div>' + \
    SRC('m_src', 'Business: company profile · price: INDmoney 20 Nov 2026')
# 5 Artificial Electronics
SCN[5] = '<div class="kick" style="top:200px">STOCK #3</div><div class="big" id="a_n" style="top:290px;font-size:90px">ARTIFICIAL ELECTRONICS</div>' + \
    photo('u5', 'a_img', 200, 420, 680, 480, 2, chip('a_chip', 390, 430, 300, '#FF4D5E', 'BSE 526443', True)) + \
    '<div class="card r" id="a_c" style="left:90px;top:960px;width:430px;height:230px;text-align:center;padding-top:26px"><div class="lab">PRICE</div><div class="val" style="font-size:96px">₹37.42</div></div>' \
    '<div class="card r" id="a_d" style="left:560px;top:960px;width:430px;height:230px;text-align:center;padding-top:26px"><div class="lab">FROM ₹175.50 HIGH</div><div class="val red" style="font-size:96px">-79%</div></div>' \
    '<div class="stamp" id="a_st" style="left:140px;top:1240px;font-size:76px;transform:rotate(3deg)">⚠ UNDER SURVEILLANCE</div>' + \
    SRC('a_src', 'Surveillance flag & prices: INDmoney, 20 Nov 2026')
# 6 RIR
SCN[6] = '<div class="kick" style="top:220px">THE REAL CHIP BUSINESS</div><div class="big teal" id="r_n" style="top:280px;font-size:92px">RIR POWER ELECTRONICS</div>' \
    f'<svg id="r_map" style="position:absolute;left:60px;top:430px;width:620px;height:705px" viewBox="0 0 612 696"><g fill="rgba(46,230,197,.07)" stroke="rgba(46,230,197,.55)" stroke-width="1.4">{india}</g></svg>' \
    '<div id="r_pin" style="position:absolute;left:366px;top:836px;width:60px;height:60px;border-radius:50%;background:#FFB547;box-shadow:0 0 0 14px rgba(255,181,71,.25),0 0 60px #FFB547"></div>' \
    '<div class="pill a" id="r_od" style="left:450px;top:858px;font-size:42px">Odisha</div>' \
    '<div class="card" id="r_c" style="left:640px;top:880px;width:390px;height:300px;text-align:center;padding-top:26px"><div class="lab">SiC CHIP PLANT</div>' \
    '<div class="val amb" style="font-size:110px" id="r_v">₹0 cr</div><div class="lab" style="font-size:28px">planned investment</div></div>' \
    '<div class="pill" id="r_p" style="left:90px;top:1210px;font-size:36px">₹140.77 · <span style="color:#FF4D5E">-34% from high</span> · just above ₹100</div>' + \
    SRC('r_src', '₹618 cr SiC plant: company release, Sep 2026 · INDmoney')
# 7 MosChip + both
SCN[7] = '<div class="big" style="top:220px;font-size:110px">REAL, BUT NOT RISK-FREE</div>' + \
    photo('u2', 'b_w', 190, 360, 700, 760, 0).replace('class="photo"', 'class="photo" data-layout-ignore', 1).replace('transform:rotate(0deg)', 'transform:rotate(0deg);opacity:.4;border:none') + \
    '<div class="card" id="b_r" style="left:70px;top:420px;width:450px;height:620px;text-align:center;padding-top:40px">' + chip('b_c1', 145, 60, 160, '#2EE6C5').replace('position:absolute;left:145px;top:60px', 'position:relative;margin:0 auto;display:block') + \
    '<div class="val" style="font-size:66px;margin-top:20px">RIR POWER</div><div class="lab">makes power chips</div><div class="val teal" style="font-size:80px;margin-top:20px">₹140.77</div><div class="val red" style="font-size:72px" id="b_r2">-34%</div></div>' \
    '<div class="card" id="b_m" style="left:560px;top:420px;width:450px;height:620px;text-align:center;padding-top:40px">' + chip('b_c2', 145, 60, 160, '#FFB547').replace('position:absolute;left:145px;top:60px', 'position:relative;margin:0 auto;display:block') + \
    '<div class="val" style="font-size:66px;margin-top:20px">MOSCHIP</div><div class="lab">designs chips</div><div class="val amb" style="font-size:80px;margin-top:20px">₹161.32</div><div class="val red" style="font-size:72px" id="b_m2">-37%</div></div>' \
    '<div class="pill r" id="b_p" style="left:150px;top:1110px;font-size:44px">both still down 30%+ from their highs</div>' + \
    SRC('b_src', '52-wk highs: RIR ₹213.94, MosChip ₹255.78 · INDmoney')
# 8 checklist
chk = lambda k, txt, y: f'<div class="card" id="k{k}" style="left:90px;top:{y}px;width:900px;height:200px;padding:0 40px;display:flex;align-items:center;gap:40px">' \
    f'<div style="width:110px;height:110px;border-radius:24px;border:5px solid #2EE6C5;position:relative;flex:none"><svg id="kt{k}" viewBox="0 0 100 100" style="position:absolute;inset:6px"><path d="M18 52 L42 76 L84 26" stroke="#2EE6C5" stroke-width="13" fill="none" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1"/></svg></div>' \
    f'<div class="val" style="font-size:72px">{txt}</div></div>'
SCN[8] = '<div class="kick" style="top:230px">BEFORE YOU BUY ANY CHIP PENNY STOCK</div><div class="big amb" style="top:300px;font-size:130px">CHECK 3 THINGS</div>' + \
    chk(0, 'Is the factory running?', 520) + chk(1, 'Is it making a profit?', 760) + chk(2, 'On the surveillance list?', 1000)
# 9 CTA
SCN[9] = '<div class="big" id="e_l" style="top:330px;font-size:150px">LOW PRICE</div><div class="big red" id="e_n" style="top:500px;font-size:150px">≠ CHEAP</div>' + \
    photo('u4', 'e_chip', 300, 690, 480, 340, -2, chip('e_chip', 400, 700, 280, '#2EE6C5')) + \
    '<div class="pill" id="e_s" style="left:200px;top:1060px;font-size:56px">🔖 SAVE THIS CHECKLIST</div>' \
    '<div class="pill a" id="e_f" style="left:150px;top:1190px;font-size:56px">➕ FOLLOW @moneyincloud</div>'
BG = [''] * 10
TRACES = traces()

JS_SCENES = '''
const cam = CAM(tl);
const cnt = (id, from, to, at, dur, fmt) => { const o = {v:from}; tl.to(o, {v:to, duration:dur, ease:"power2.out", onUpdate:() => { document.getElementById(id).textContent = fmt(o.v); }}, at); };
const inr = v => Math.round(v).toLocaleString("en-IN");
const slam = (sel, at, r) => tl.fromTo(sel, {scale:2.6, opacity:0, rotation:(r||0)}, {scale:1, opacity:1, duration:0.32, ease:"power4.in"}, at);
const flash = (at) => tl.fromTo("#flash", {opacity:0.28}, {opacity:0, duration:0.5, ease:"power2.out", immediateRender:false}, at);
const sweep = (at) => tl.fromTo("#sweep", {x:0}, {x:2300, duration:1.1, ease:"power2.inOut", immediateRender:false}, at);
// ambient
tl.fromTo("#progf", {scaleX:0}, {scaleX:1, duration:T.DUR, ease:"none"}, 0);
document.querySelectorAll(".tr").forEach((el, k) => tl.fromTo(el, {strokeDashoffset:1}, {strokeDashoffset:-1, duration:3.2 + (k % 3), ease:"none", repeat:Math.floor(T.DUR / 3.2), }, k * 0.4));
tl.fromTo("#hz0", {x:0, y:0}, {x:120, y:80, duration:T.DUR / 2, ease:"sine.inOut", yoyo:true, repeat:1}, 0);
tl.fromTo("#hz1", {x:0, y:0}, {x:-100, y:-90, duration:T.DUR / 2, ease:"sine.inOut", yoyo:true, repeat:1}, 0);
tl.fromTo("#bgw", {x:0, y:0}, {x:-60, y:-80, duration:T.DUR, ease:"none"}, 0);
cam.handheld("#world", T.DUR, {rot:0.25, x:4, y:-3, period:3.2});
// whip pans between all scenes
SC.forEach(([a, b], i) => { if (i > 0) cam.whip("#sc" + (i - 1), "#sc" + i, a, {dir: i % 2 ? 1 : -1, dur:0.4}); sweep(a + 0.1); });

// 0 hook: chip push-in, MULTIBAGGER, crash zoom on TRAP
tl.set(["#h_k", "#h_m", "#h_t"], {opacity:0}, 0);
cam.pullOut("#cam0", 0, {from:1.45, to:1.0, dur:2.4, ease:"power3.out", oy:"38%"}); cam.kenBurns("#h_img", 2.4, {dur:SC[0][1] - 2.4, from:1.0, to:1.1, x:-20, y:-30});
up("#h_k", 0.4);
pop("#h_m", T.multi - 0.1); slam("#h_t", T.traps - 0.25, -3); flash(T.traps); cam.shake("#sc0", T.traps + 0.05, {amp:18});
cam.crashZoom("#cam0", T.traps + 0.1, {to:1.18, ox:"50%", oy:"68%", hold:0.9});

// 1 SPEL: track across the card, chip rotates in
tl.set(["#s_n", "#s_c", "#s_o", "#s_f", "#s_p", "#s_src"], {opacity:0}, SC[1][0]);
up("#s_n", T.spel - 0.2);
tl.fromTo("#s_img, #s_chip", {opacity:0, rotationY:-60, scale:0.7}, {opacity:1, rotationY:0, scale:1, duration:0.9, ease:"power3.out"}, T.spel);
pop("#s_c", T.chennai - 0.1, -1); pop("#s_o", T.packs, 1); pop("#s_f", T.first, -1); pop("#s_p", T.perfect - 0.3, 2); up("#s_src", SC[1][0] + 1.0);
cam.track("#cam1", SC[1][0], {x0:60, y0:0, x:-40, y:0, dur:SC[1][1] - SC[1][0], ease:"sine.inOut"});
cam.orbit("#s_img, #s_chip", T.packs, {from:0, to:14, dur:3});

// 2 catch: dutch angle + stamp shake, bars
tl.set(["#c_h", "#c_st", "#c_s", "#c_l", "#c_src"], {opacity:0}, SC[2][0]); tl.set(["#c_sb", "#c_lb"], {scaleX:0}, SC[2][0]);
slam("#c_h", T.catch - 0.2); cam.dutch("#cam2", T.catch, {deg:-6, dur:0.5, hold:1.6});
slam("#c_st", T.shut, -8); flash(T.shut + 0.25); cam.shake("#sc2", T.shut + 0.3, {amp:16});
up("#c_s", T.sales - 0.3); cnt("c_sv", 0, 6.28, T.sales, 1.0, v => "₹" + v.toFixed(2) + " cr"); tl.to("#c_sb", {scaleX:1, duration:0.9, ease:"power2.out"}, T.sales);
up("#c_l", T.loss - 0.3); cnt("c_lv", 0, 23.84, T.loss, 1.2, v => "₹" + v.toFixed(2) + " cr"); tl.to("#c_lb", {scaleX:1, duration:1.2, ease:"power2.out"}, T.loss);
up("#c_src", SC[2][0] + 1.0);
cam.pushIn("#cam2", T.sales, {from:1, to:1.08, dur:SC[2][1] - T.sales, ease:"none", oy:"60%"});

// 3 valuation: counter, line draws, crash zoom on -51%
tl.set(["#v_st", "#v_src"], {opacity:0}, SC[3][0]);
cnt("v_mc", 0, 358, T.values, 1.3, v => "₹" + inr(v) + " cr");
tl.to("#v_line", {strokeDashoffset:0, duration:2.0, ease:"power2.inOut"}, T.values + 0.6);
tl.fromTo("#v_dot", {scale:0, transformOrigin:"50% 50%"}, {scale:1, duration:0.3, ease:"back.out(3)"}, T.values + 2.5);
slam("#v_st", T.f51 - 0.2, -5); cam.crashZoom("#cam3", T.f51, {to:1.22, ox:"50%", oy:"66%", hold:1.0}); flash(T.f51 + 0.1);
cam.tilt("#v_ch", SC[3][0] + 0.2, {from:40, to:0, dur:1.4}); up("#v_src", SC[3][0] + 1.0);

// 4 MIC: orbit the price card, tags, stamp
tl.set(["#m_n", "#m_c", "#m_t0", "#m_t1", "#m_t2", "#m_st", "#m_src"], {opacity:0}, SC[4][0]);
up("#m_n", T.mic - 0.3); pop("#m_c", T.mic + 0.4);
cam.orbit("#m_c", T.mic + 0.4, {from:-24, to:10, dur:2.4});
pop("#m_t0", T.led - 0.1, -2); pop("#m_t1", T.led + 0.5, 2); pop("#m_t2", T.led + 1.0, -1);
slam("#m_st", T.led + 1.8, -4); cam.shake("#sc4", T.weak + 0.1, {amp:12});
cam.pushIn("#cam4", SC[4][0], {from:1.06, to:1, dur:SC[4][1] - SC[4][0], ease:"none"}); up("#m_src", SC[4][0] + 1.0);

// 5 Artificial Electronics: dolly zoom, red flash, dutch
tl.set(["#a_n", "#a_c", "#a_d", "#a_st", "#a_src"], {opacity:0}, SC[5][0]);
up("#a_n", T.ae - 0.3); tl.fromTo("#a_img, #a_chip", {opacity:0, scale:0.8}, {opacity:1, scale:1, duration:0.6, ease:"power3.out"}, T.ae);
cam.dollyZoom("#bgw", "#cam5", T.ae, {amt:0.25, dur:2.0});
pop("#a_c", T.ae + 0.8, -1); pop("#a_d", T.f79 - 0.2, 1);
slam("#a_st", T.surv - 0.2, 3); flash(T.surv); flash(T.flag); cam.dutch("#cam5", T.flag - 0.2, {deg:5, dur:0.4, hold:1.0}); cam.shake("#sc5", T.surv + 0.1, {amp:16});
up("#a_src", SC[5][0] + 1.0);

// 6 RIR: map draw, push in to Odisha, counter
tl.set(["#r_n", "#r_pin", "#r_od", "#r_c", "#r_p", "#r_src"], {opacity:0}, SC[6][0]);
up("#r_n", T.rir - 0.3);
tl.fromTo("#r_map path", {strokeDasharray:"0 3000"}, {strokeDasharray:"3000 0", duration:1.8, ease:"power1.inOut"}, SC[6][0] + 0.3);
tl.fromTo("#r_map #or", {fill:"rgba(46,230,197,.07)"}, {fill:"#FFB547", duration:0.6}, T.odisha - 0.2);
tl.fromTo("#r_pin", {opacity:0, y:-300}, {opacity:1, y:0, duration:0.6, ease:"bounce.out"}, T.odisha); pop("#r_od", T.odisha + 0.4, -2);
cam.pushIn("#cam6", T.odisha - 0.2, {from:1, to:1.35, dur:1.4, ox:"38%", oy:"47%", ease:"power2.inOut"});
tl.to("#cam6", {scale:1, duration:0.8, ease:"power2.inOut"}, T.odisha + 1.3);
pop("#r_c", T.p618 - 0.2); cnt("r_v", 0, 618, T.p618, 1.2, v => "₹" + inr(v) + " cr"); pop("#r_p", T.p618 + 0.2);
up("#r_src", SC[6][0] + 1.0);

// 7 both: parallax cards, tilt
tl.set(["#b_r", "#b_m", "#b_p", "#b_src", "#b_r2", "#b_m2"], {opacity:0}, SC[7][0]);
pop("#b_r", T.mos - 0.6, -2); pop("#b_m", T.mos, 2);
cam.parallax(["#b_r", "#b_m"], SC[7][0] + 0.2, {dist:-40, dur:SC[7][1] - SC[7][0]});
cam.tilt("#cam7", SC[7][0], {from:18, to:0, dur:1.4});
slam("#b_r2", T.f30 - 0.3, -3); slam("#b_m2", T.f30, 3); pop("#b_p", T.both - 0.3); up("#b_src", SC[7][0] + 1.0);

// 8 checklist: track down, ticks draw
tl.set(["#k0", "#k1", "#k2"], {opacity:0}, SC[8][0]);
[["c1", 0], ["c2", 1], ["c3", 2]].forEach(([k, i]) => { tl.fromTo("#k" + i, {opacity:0, x:-300}, {opacity:1, x:0, duration:0.5, ease:"power3.out"}, T[k] - 0.4);
  tl.to("#kt" + i + " path", {strokeDashoffset:0, duration:0.4, ease:"power2.out"}, T[k] + 0.4); });
cam.track("#cam8", SC[8][0], {x0:0, y0:60, x:0, y:-60, dur:SC[8][1] - SC[8][0], ease:"sine.inOut"});

// 9 CTA: rack focus + pull out
tl.set(["#e_l", "#e_n", "#e_s", "#e_f"], {opacity:0}, SC[9][0]);
up("#e_l", SC[9][0] + 0.2); slam("#e_n", T.cheap - 0.2); flash(T.cheap);
cam.rack("#e_chip", SC[9][0] + 0.2, {blur:14, dur:1.0});
tl.fromTo("#e_chip", {scale:1}, {scale:1.08, duration:SC[9][1] - SC[9][0], ease:"none"}, SC[9][0]);
pop("#e_s", T.save - 0.1, -2); pop("#e_f", T.follow - 0.1, 2);
cam.pullOut("#cam9", SC[9][0], {from:1.25, to:1, dur:1.6});
'''
