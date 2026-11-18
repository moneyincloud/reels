"""Scenes for the 18 Nov 2026 IPO listing report: subscription vs listing day vs today. Assembled by build.py.
Data: NSE daily candles via INDmoney (retrieved 18 Nov 2026 06:47 IST, last close 17 Nov 2026);
subscription = final-day figures from chittorgarh.com (NSE/BSE consolidated bids)."""
CAPTXT = []   # owner's rule: NO subtitles

BG = ['#EFE7FF', '#FFF1B8', '#FFE2D1', '#E6E0FF', '#D7F5E9', '#DDF0FF', '#FFD6DE', '#FFF7E0', '#EFE7FF']
INK = '#1B1B1F'; GRN = '#1E8E4E'; RED = '#D93A2B'; PUR = '#6B3FD4'; YEL = '#FFE45C'


def bars(p, vals, labs, cols, top=520, h=520):
    """3-bar race: issue -> day-1 close -> latest close. Heights share one scale."""
    mx = max(vals)
    out = [f'<div class="bchart" style="top:{top}px;height:{h}px">']
    for k, (v, l, c) in enumerate(zip(vals, labs, cols)):
        hh = int((h - 90) * v / mx)
        x = 40 + k * 300
        out.append(f'<div class="bar" id="{p}b{k}" style="left:{x}px;width:220px;height:{hh}px;background:{c}"></div>')
        out.append(f'<div class="bval" id="{p}v{k}" style="left:{x - 40}px;bottom:{hh + 14}px">₹<span id="{p}n{k}">{v:,.2f}</span></div>')
        out.append(f'<div class="blab2" style="left:{x - 40}px;top:{h + 14}px">{l}</div>')
    out.append('</div>')
    return '\n'.join(out)


def spark(p, closes, issue, w=900, h=330, lo=None, hi=None):
    lo = lo if lo is not None else min(closes + [issue]) * 0.97
    hi = hi if hi is not None else max(closes + [issue]) * 1.02
    X = lambda i: 20 + i * (w - 40) / (len(closes) - 1)
    Y = lambda v: h - (v - lo) / (hi - lo) * h
    pts = ' '.join(f'{X(i):.1f},{Y(v):.1f}' for i, v in enumerate(closes))
    yi = Y(issue)
    return (f'<svg class="spark" id="{p}sp" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<line x1="0" x2="{w}" y1="{yi:.1f}" y2="{yi:.1f}" stroke="{INK}" stroke-width="4" stroke-dasharray="14 12"/>'
            f'<text x="10" y="{yi - 12:.1f}" text-anchor="start" font-family="Oswald" font-size="30" fill="{INK}">issue ₹{issue:g}</text>'
            f'<polyline id="{p}pl" pathLength="1" points="{pts}" fill="none" stroke="{PUR}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round" style="stroke-dasharray:1 1.2;stroke-dashoffset:1.1"/>'
            f'<circle id="{p}dot" cx="{X(len(closes) - 1):.1f}" cy="{Y(closes[-1]):.1f}" r="16" fill="{PUR}" stroke="{INK}" stroke-width="5"/></svg>')


# real NSE daily closes (INDmoney): listing day .. 17 Nov 2026
BC_CLOSES = [94.81, 90.07, 85.57, 81.30, 83.92, 81.72, 81.08, 80.10, 83.41]
MK_CLOSES = [162.20, 160.54, 158.08, 157.92, 154.56, 161.90, 170.96, 176.87, 183.12, 187.66]

SCN = {}
SCN[0] = f'''<div class="ttl hand" style="top:190px;font-size:76px">One November IPO was</div>
<div class="big" id="h64" style="left:0;right:0;text-align:center;top:300px;font-size:430px;color:{PUR}">64x</div>
<div class="stk" id="hsub" style="left:250px;top:770px;background:{YEL};transform:rotate(-3deg);font-size:76px">SUBSCRIBED</div>
<div class="pill" id="hd1" style="left:80px;top:1000px;background:{GRN};font-size:66px">DAY 1 ▲ 15.6%</div>
<div class="arr" id="harr" style="left:540px;top:1180px;width:150px;background:{RED};transform:rotate(90deg)"></div>
<div class="pill" id="hnow" style="left:330px;top:1290px;background:{RED};font-size:76px;transform:rotate(2deg)">NOW ▲ 1.7%</div>'''

CARDS = [('🧪', 'BLS Polymers', 'listed 3 Nov', '#DDF0FF'), ('💧', 'SFC Environmental', 'listed 3 Nov', '#D7F5E9'),
         ('💍', 'M.K. Sons Fine Jewels', 'listed 4 Nov', '#FFF1B8'), ('🔩', 'Bombay Coated & Special Steels', 'listed 5 Nov', '#FFD6DE')]
SCN[1] = '<div class="ttl hand" style="top:190px">4 mainboard IPOs</div>\n<div class="ttl" style="top:300px;font-family:Oswald;font-size:44px;color:#55556A">listed on NSE &amp; BSE, 3–5 Nov 2026</div>\n' + '\n'.join(
    f'<div class="card ipo" id="c{k}" style="left:{70 + (k % 2) * 480}px;top:{420 + (k // 2) * 520}px;background:{bg}"><div class="e">{e}</div><b>{n}</b><span>{d}</span></div>'
    for k, (e, n, d, bg) in enumerate(CARDS))

SCN[2] = f'''<div class="card" id="myth" style="left:80px;right:80px;top:220px;padding:30px;text-align:center;background:#fff">
<div style="font-family:Anton;font-size:56px;color:{RED}">THE MYTH</div>
<div style="font-family:Poppins;font-weight:700;font-size:54px;line-height:1.2">More subscription<br>= bigger gains?</div></div>
<div class="stk" id="mq" style="left:780px;top:180px;background:{YEL};font-size:90px;transform:rotate(8deg)">?</div>
<div class="ttl hand" id="sbt" style="top:690px;font-size:90px">The scoreboard</div>
<div class="col" id="k0" style="left:60px;top:860px;background:#fff">ISSUE<br><small>price</small></div>
<div class="arr" id="ka0" style="left:370px;top:960px;width:70px"></div>
<div class="col" id="k1" style="left:400px;top:860px;background:{YEL}">DAY 1<br><small>listing close</small></div>
<div class="arr" id="ka1" style="left:710px;top:960px;width:70px"></div>
<div class="col" id="k2" style="left:740px;top:860px;background:#D7F5E9">TODAY<br><small>17 Nov close</small></div>'''

SCN[3] = f'''<div class="ttl hand" style="top:200px;font-size:96px">But wait…</div>
<div class="fight" id="f5" style="left:90px;top:470px;background:#FFF1B8">💍<b>5x</b><span>least wanted</span></div>
<div class="big" id="vs" style="left:0;right:0;text-align:center;top:620px;font-size:120px">VS</div>
<div class="fight" id="f64" style="left:590px;top:470px;background:#FFD6DE">🔩<b>64x</b><span>most hyped?</span></div>
<div class="stk" id="beat" style="left:150px;top:1080px;background:{PUR};color:#fff;transform:rotate(-3deg);font-size:64px">WHO'S AHEAD NOW?</div>
<div class="ring" id="ring"><span id="cd">3</span></div>'''

SCN[4] = f'''<div class="tag" style="top:190px">1/4</div><div class="ttl hand" style="top:200px">🧪 BLS Polymers</div>
<div class="chipx" id="bsub" style="left:120px;top:330px">Subscribed <b>241x</b></div>
{bars('p', [150, 268.80, 275.50], ['ISSUE', 'DAY 1', '17 NOV'], ['#B9B9C6', YEL, '#2BB673'], top=480)}
<div class="pill" id="p79" style="left:330px;top:1150px;background:{GRN};font-size:64px">DAY 1 ▲ 79.2%</div>
<div class="pill" id="p84" style="left:310px;top:1300px;background:{PUR};font-size:64px;transform:rotate(-2deg)">NOW ▲ 83.7%</div>'''

SCN[5] = f'''<div class="tag" style="top:190px">2/4</div><div class="ttl hand" style="top:200px">💧 SFC Environmental</div>
<div class="chipx" id="ssub" style="left:120px;top:330px">Subscribed <b>9.5x</b></div>
{bars('q', [330, 426.10, 432.50], ['ISSUE', 'DAY 1', '17 NOV'], ['#B9B9C6', YEL, '#2BB673'], top=480)}
<div class="stk" id="suc" style="left:540px;top:405px;background:{RED};color:#fff;transform:rotate(-4deg);font-size:44px">UPPER CIRCUIT DAY 1</div>
<div class="pill" id="q29" style="left:330px;top:1150px;background:{GRN};font-size:64px">DAY 1 ▲ 29.1%</div>
<div class="pill" id="q31" style="left:310px;top:1300px;background:{PUR};font-size:64px;transform:rotate(-2deg)">NOW ▲ 31.1%</div>'''

SCN[6] = f'''<div class="panel" style="left:0">
<div class="tag" style="top:190px">3/4</div><div class="ttl hand" style="top:200px">🔩 Bombay Coated</div>
<div class="chipx" id="csub" style="left:120px;top:330px">Subscribed <b>63.9x</b></div>
<div class="pill" id="c16" style="left:90px;top:470px;background:{GRN};font-size:58px">DAY 1 ▲ 15.6%</div>
<div style="position:absolute;left:90px;top:620px">{spark('c', BC_CLOSES, 82)}</div>
<div class="stk" id="clc" style="left:200px;top:990px;background:{RED};color:#fff;transform:rotate(4deg);font-size:50px">3 LOWER CIRCUITS IN A ROW</div>
<div class="pill" id="c17" style="left:290px;top:1140px;background:{RED};font-size:70px;transform:rotate(-2deg)">NOW ▲ 1.7%</div>
<div class="note" style="left:90px;top:1290px">NSE daily closes, 5–17 Nov 2026</div></div>
<div class="panel" style="left:1080px">
<div class="tag" style="top:190px">4/4</div><div class="ttl hand" style="top:200px">💍 M.K. Sons</div>
<div class="chipx" id="msub" style="left:120px;top:330px">Subscribed <b>5.1x</b></div>
<div class="pill" id="mflat" style="left:90px;top:470px;background:#8A8A99;font-size:58px">DAY 1 ▲ 0.1% (flat)</div>
<div style="position:absolute;left:90px;top:620px">{spark('m', MK_CLOSES, 162)}</div>
<div class="pill" id="m16" style="left:290px;top:1060px;background:{GRN};font-size:70px;transform:rotate(-2deg)">NOW ▲ 15.8%</div>
<div class="note" style="left:90px;top:1210px">NSE daily closes, 4–17 Nov 2026</div></div>'''

ROWS = [('BLS Polymers', '241x', '+79.2%', '+83.7%'), ('SFC Environ.', '9.5x', '+29.1%', '+31.1%'),
        ('M.K. Sons', '5.1x', '+0.1%', '+15.8%'), ('Bombay Coated', '63.9x', '+15.6%', '+1.7%')]
SCN[7] = f'''<div class="ttl hand" style="top:190px;font-size:84px">The answer</div>
<div class="card" id="sheet" style="left:50px;right:50px;top:310px;padding:20px 26px;background:#fff">
<div class="row hd"><span>IPO</span><span>Subs</span><span>Day 1</span><span>17 Nov</span></div>
''' + '\n'.join(f'<div class="row" id="r{k}"><span>{a}</span><span>{b}</span><span>{c}</span><span class="{"hi" if k in (2, 3) else ""}">{d}</span></div>' for k, (a, b, c, d) in enumerate(ROWS)) + f'''
<div class="src">% vs issue price · NSE closes via INDmoney · subscription: chittorgarh (final day)</div></div>
<div class="card" id="ans" style="left:70px;right:70px;top:1010px;padding:22px 26px;text-align:center;background:#FFF7E0">
<div style="font-family:Anton;font-size:52px;line-height:1.15">Subscription = demand on bidding day</div>
<div style="font-family:Poppins;font-weight:700;font-size:38px;margin-top:6px">not where the price goes next</div></div>
<div class="stk" id="chap" style="left:150px;top:1290px;background:{PUR};color:#fff;transform:rotate(-2deg);font-size:50px">LISTING DAY = ONE CHAPTER</div>
<div class="stk" id="bm" style="left:760px;top:170px;background:{YEL};transform:rotate(6deg);font-size:46px">🔖 SAVE THIS</div>'''

SCN[8] = f'''<div class="ttl hand" style="top:330px;font-size:84px">64x subscribed ≠<br>64x safe</div>
<img id="host" src="assets/img/s0_008.png" style="position:absolute;left:40px;top:620px;width:360px"/>
<div class="card" id="send" style="left:420px;top:620px;width:600px;padding:20px 24px;background:#fff">
<div style="font-family:Anton;font-size:46px">✈️ SEND THIS TO</div>
<div style="font-family:Poppins;font-weight:700;font-size:36px;line-height:1.2">the friend who applies for every IPO</div></div>
<div class="emo" id="plane" style="left:430px;top:900px;font-size:110px">✈️</div>
<div class="pill" id="sv" style="left:430px;top:960px;background:{YEL};color:{INK};font-size:58px">🔖 SAVE THIS</div>
<div class="pill" id="fl" style="left:430px;top:1120px;background:{PUR};font-size:52px">FOLLOW · every Wed</div>
<div class="stk" id="edu" style="left:110px;top:1320px;background:#fff;font-size:42px;transform:rotate(-1deg)">Education only · Not investment advice</div>'''

EXTRA_CSS = '''
#prog { position:absolute; left:0; top:0; height:12px; width:1080px; background:#6B3FD4; transform-origin:0 50%; z-index:60; }
.tag { position:absolute; left:40px; font-family:"Anton",sans-serif; font-size:44px; background:#1B1B1F; color:#fff; padding:2px 16px; border-radius:10px; }
.ipo { width:460px; height:470px; text-align:center; padding:24px 20px; }
.ipo .e { font-size:150px; line-height:1.2; } .ipo b { display:block; font-family:"Anton",sans-serif; font-weight:400; font-size:54px; line-height:1.1; }
.ipo span { display:block; font-family:"Poppins",sans-serif; font-weight:700; font-size:34px; margin-top:10px; color:#55556A; }
.col { position:absolute; width:300px; height:220px; border:6px solid #1B1B1F; border-radius:22px; box-shadow:8px 8px 0 #1B1B1F; text-align:center; padding-top:34px;
  font-family:"Anton",sans-serif; font-size:64px; line-height:1.05; } .col small { font-family:"Poppins",sans-serif; font-weight:700; font-size:30px; }
.fight { position:absolute; width:400px; height:470px; border:6px solid #1B1B1F; border-radius:26px; box-shadow:10px 10px 0 #1B1B1F; text-align:center; font-size:130px; padding-top:30px; line-height:1.1; }
.fight b { display:block; font-family:"Anton",sans-serif; font-weight:400; font-size:120px; } .fight span { display:block; font-family:"Caveat",cursive; font-size:54px; }
.ring { position:absolute; left:440px; top:1240px; width:200px; height:200px; border-radius:50%; border:12px solid #6B3FD4; background:#fff; text-align:center; font-family:"Anton",sans-serif; font-size:120px; line-height:176px; }
.chipx { position:absolute; padding:10px 28px; background:#fff; border:5px solid #1B1B1F; border-radius:18px; box-shadow:6px 6px 0 #1B1B1F; font-family:"Poppins",sans-serif; font-weight:700; font-size:44px; }
.chipx b { font-family:"Anton",sans-serif; font-weight:400; color:#6B3FD4; font-size:58px; }
.bchart { position:absolute; left:90px; width:900px; border-bottom:8px solid #1B1B1F; }
.bval { position:absolute; width:300px; text-align:center; font-family:"Anton",sans-serif; font-size:56px; }
.blab2 { position:absolute; width:300px; text-align:center; font-family:"Oswald",sans-serif; font-size:40px; }
.panel { position:absolute; top:0; width:1080px; height:1920px; }
.spark { overflow:visible; }
.note { position:absolute; font-family:"Oswald",sans-serif; font-size:30px; color:#55556A; }
.row { display:grid; grid-template-columns: 1.7fr 0.9fr 1fr 1fr; padding:16px 6px; border-bottom:3px solid #ddd; font-family:"Poppins",sans-serif; font-weight:700; font-size:40px; }
.row span:not(:first-child) { text-align:right; font-family:"Anton",sans-serif; font-weight:400; font-size:48px; }
.row.hd { font-family:"Oswald",sans-serif; font-size:34px; color:#55556A; } .row.hd span { font-family:"Oswald",sans-serif !important; font-size:34px !important; }
.row .hi { color:#6B3FD4; }
.src { font-family:"Oswald",sans-serif; font-size:26px; color:#55556A; margin-top:12px; text-align:center; }
'''

JS_SCENES = '''
const cam = CAM(tl);
tl.fromTo("#prog", {scaleX:0}, {scaleX:1, duration:T.DUR, ease:"none"}, 0);
const count = (id, a, b, at, d, dec) => { const o = {v:a}; tl.to(o, {v:b, duration:d||1.2, ease:"power2.out", onUpdate:() => { const e = document.getElementById(id); if (e) e.textContent = o.v.toLocaleString("en-IN", {minimumFractionDigits:dec===undefined?2:dec, maximumFractionDigits:dec===undefined?2:dec}); }}, at); };
// 0 HOOK: 64x already on screen and moving at frame 0
tl.fromTo("#h64", {scale:1.6, rotation:-6}, {scale:1, rotation:0, duration:0.9, ease:"back.out(1.6)"}, 0);
tl.fromTo("#hsub", {scale:0.3, opacity:0}, {scale:1, opacity:1, duration:0.4, ease:"back.out(2.2)"}, 0.5);
tl.set(["#hd1", "#harr", "#hnow"], {opacity:0}, 0);
pop("#hd1", T.lost - 0.1); tl.fromTo("#harr", {opacity:1, scaleX:0}, {scaleX:1, duration:0.4, ease:"power2.out"}, T.lost + 0.5);
pop("#hnow", T.lost + 0.9, 2); shake("#sc0", T.lost + 0.95, 16);
cam.crashZoom("#cam0", T.lost + 0.9, {to:1.3, ox:"50%", oy:"70%", hold:0.5});
tl.to("#h64", {scale:1.04, duration:0.6, yoyo:true, repeat:5, ease:"sine.inOut"}, 1.2);
// 1 four IPO cards drop in, camera tracks down
tl.set(["#c0", "#c1", "#c2", "#c3"], {opacity:0}, SC[1][0]);
["#c0", "#c1", "#c2", "#c3"].forEach((c, k) => pop(c, T.four + 0.3 + k * 0.45, k % 2 ? 2 : -2));
cam.pushIn("#cam1", SC[1][0], {from:1.15, to:1, dur:SC[1][1] - SC[1][0], oy:"40%", ease:"power1.out"});
// 2 myth + scoreboard columns
tl.set(["#myth", "#mq", "#sbt", "#k0", "#k1", "#k2", "#ka0", "#ka1"], {opacity:0}, SC[2][0]);
up("#myth", T.myth - 0.2); pop("#mq", T.myth + 1.2, 8); tl.to("#mq", {rotation:-8, duration:0.3, yoyo:true, repeat:5}, T.myth + 1.7);
up("#sbt", T.board - 0.1); pop("#k0", T.iss); pop("#ka0", T.lday - 0.2); pop("#k1", T.lday); pop("#ka1", T.tday - 0.2); pop("#k2", T.tday);
cam.dutch("#cam2", T.myth, {deg:-5, dur:0.5, hold:1.6});
cam.track("#cam2", T.board - 0.3, {y0:0, y:-50, x0:0, x:0, dur:1.6});
// 3 REHOOK: colour flash + vs + countdown
tl.fromTo("#sc3", {backgroundColor:"#6B3FD4"}, {backgroundColor:"#E6E0FF", duration:0.6, ease:"power2.out"}, SC[3][0] + 0.05);
tl.set(["#f5", "#f64", "#vs", "#beat", "#ring"], {opacity:0}, SC[3][0]);
tl.fromTo("#f5", {x:-600, opacity:1}, {x:0, duration:0.5, ease:"back.out(1.6)"}, T.least);
tl.fromTo("#f64", {x:600, opacity:1}, {x:0, duration:0.5, ease:"back.out(1.6)"}, T.sixty - 0.3);
pop("#vs", T.sixty + 0.3); shake("#sc3", T.sixty + 0.35, 12); pop("#beat", T.sixty + 1.2, -3);
pop("#ring", SC[3][0] + 1.0);
tl.set("#cd", {textContent:"2"}, SC[3][0] + 2.4); tl.set("#cd", {textContent:"1"}, SC[3][0] + 3.6);
cam.orbit("#cam3", SC[3][0] + 0.4, {from:-16, to:10, dur:SC[3][1] - SC[3][0] - 0.6});
// 4/5 bar races
tl.set(["#bsub", "#p79", "#p84", "#sc4 .bchart"], {opacity:0}, SC[4][0]);
pop("#bsub", T.b241 - 0.1);
tl.to("#sc4 .bchart", {opacity:1, duration:0.3}, SC[4][0] + 0.5);
[["#pb0", "#pv0", "pn0", 150, SC[4][0] + 0.6], ["#pb1", "#pv1", "pn1", 268.80, T.b79 - 0.3], ["#pb2", "#pv2", "pn2", 275.50, T.b84 - 0.3]].forEach(([b, v, n, val, at]) => {
  tl.fromTo(b, {scaleY:0}, {scaleY:1, duration:0.9, ease:"power3.out"}, at); tl.fromTo(v, {opacity:0}, {opacity:1, duration:0.2}, at); count(n, 0, val, at, 0.9); });
pop("#p79", T.b79 + 0.4); pop("#p84", T.b84 + 0.4, -2);
cam.pushIn("#cam4", SC[4][0], {from:1, to:1.12, dur:3, oy:"30%"}); cam.pullOut("#cam4", T.b79 - 0.4, {from:1.12, to:1, dur:1.2});
tl.set(["#ssub", "#q29", "#q31", "#suc", "#sc5 .bchart"], {opacity:0}, SC[5][0]);
pop("#ssub", T.s9);
tl.to("#sc5 .bchart", {opacity:1, duration:0.3}, SC[5][0] + 0.4);
[["#qb0", "#qv0", "qn0", 330, SC[5][0] + 0.5], ["#qb1", "#qv1", "qn1", 426.10, T.suc - 0.5], ["#qb2", "#qv2", "qn2", 432.50, T.s31 - 0.2]].forEach(([b, v, n, val, at]) => {
  tl.fromTo(b, {scaleY:0}, {scaleY:1, duration:0.9, ease:"power3.out"}, at); tl.fromTo(v, {opacity:0}, {opacity:1, duration:0.2}, at); count(n, 0, val, at, 0.9); });
pop("#suc", T.suc + 0.2, -6); shake("#sc5", T.suc + 0.25, 12); pop("#q29", T.suc + 0.9); pop("#q31", T.s31 + 0.4, -2);
cam.tilt("#cam5", SC[5][0], {from:22, to:0, dur:1.4});
cam.crashZoom("#cam5", T.suc + 0.2, {to:1.25, oy:"35%", hold:0.6});
// 6 Bombay Coated chart, then track to M.K. Sons
tl.set(["#csub", "#c16", "#clc", "#c17", "#cdot", "#msub", "#mflat", "#m16", "#mdot"], {opacity:0}, SC[6][0]);
pop("#csub", T.bc64 - 0.1); pop("#c16", T.bc16);
tl.fromTo("#cpl", {strokeDashoffset:1.1}, {strokeDashoffset:0, duration:T.bc17 - T.lc + 0.3, ease:"power1.inOut"}, T.lc - 0.3);
pop("#clc", T.lc + 0.6, 4); shake("#sc6", T.lc + 0.65, 14);
tl.to("#cdot", {opacity:1, duration:0.2}, T.bc17); pop("#c17", T.bc17 + 0.2, -2);
cam.track("#cam6", T.mk - 0.5, {x0:0, x:-1080, dur:0.7, ease:"power3.inOut"});
tl.fromTo("#cam6", {filter:"blur(0px)"}, {filter:"blur(10px)", duration:0.35, yoyo:true, repeat:1}, T.mk - 0.5);
pop("#msub", T.mk5); pop("#mflat", T.mkflat);
tl.fromTo("#mpl", {strokeDashoffset:1.1}, {strokeDashoffset:0, duration:SC[6][1] - T.mk16 + 0.4, ease:"power1.inOut"}, T.mkflat + 0.4);
tl.to("#mdot", {opacity:1, duration:0.2}, SC[6][1] - 0.3); pop("#m16", T.mk16 + 0.2, -2);
// 7 ANSWER: cheat sheet stamps in row by row
tl.set(["#sheet", "#r0", "#r1", "#r2", "#r3", "#ans", "#chap", "#bm"], {opacity:0}, SC[7][0]);
up("#sheet", SC[7][0] + 0.2); ["#r0", "#r1", "#r2", "#r3"].forEach((r, k) => up(r, SC[7][0] + 0.5 + k * 0.3));
up("#ans", T.subs); pop("#chap", T.chap, -2); shake("#sc7", T.chap + 0.05, 10);
pop("#bm", SC[7][0] + 1.6, 6); tl.to("#bm", {y:-16, duration:0.35, yoyo:true, repeat:9, ease:"sine.inOut"}, SC[7][0] + 2.2);
cam.pullOut("#cam7", SC[7][0], {from:1.2, to:1, dur:1.6, oy:"30%"});
cam.rack("#sheet", T.subs - 0.3, {blur:6, dur:0.5, out:true}); cam.rack("#sheet", T.chap + 1.2, {blur:6, dur:0.6});
// 8 CTA: send / save / follow, plane flies
tl.set(["#host", "#send", "#plane", "#sv", "#fl", "#edu"], {opacity:0}, SC[8][0]);
tl.fromTo("#host", {y:120, opacity:0}, {y:0, opacity:1, duration:0.5, ease:EIN}, SC[8][0] + 0.2);
up("#send", T.send); tl.fromTo("#plane", {x:0, y:0, opacity:1, rotation:0}, {x:620, y:-520, rotation:-20, opacity:0, duration:1.4, ease:"power2.in"}, T.send + 1.2);
pop("#sv", T.save, -3); tl.to("#sv", {scale:1.12, duration:0.2, yoyo:true, repeat:3}, T.save + 0.5);
pop("#fl", T.follow, 2); up("#edu", T.edu);
cam.pushIn("#cam8", SC[8][0], {from:1.1, to:1, dur:1.4, ease:"power2.out"});
cam.dollyZoom("#host", "#sc8 .ttl", T.loop - 0.2, {amt:0.12, dur:1.6});
'''
