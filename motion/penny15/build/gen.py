"""15 Penny Stocks of the Week (doodle HyperFrames). Data-driven, NO subtitles.
Usage: python3 build/gen.py <studio data dir with week.json + times.json + meta.json>
week.json: 15 rows sorted by week_pct desc (name, close, week_pct, hi52, below_hi, mcap_cr).
times.json: VO segment starts {seg: [start, dur]}, DUR. meta.json: labels (week, source, hook...)."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__))
D = sys.argv[1]
W = json.load(open(os.path.join(D, 'week.json')))
T = json.load(open(os.path.join(D, 'times.json')))
M = json.load(open(os.path.join(D, 'meta.json')))
DUR = T['DUR']
st = lambda k: T[k][0]
en = lambda k: T[k][0] + T[k][1]
CARD_T = [st('g0') + 1.0, st('g1'), st('g2'), st('g3')] + [st(f'f{k}') for k in range(4, 14)] + [st('f14') + 1.1]
NUP = sum(1 for d in W if d['week_pct'] > 0)
SC = [(0, st('l1') - 0.1), (st('l1') - 0.1, st('g0') - 0.1), (st('g0') - 0.1, st('r0') - 0.15),
      (st('r0') - 0.15, st('cta') - 0.1), (st('cta') - 0.1, DUR)]
json.dump({'SC': SC, 'CARD_T': CARD_T, 'T': T}, open(os.path.join(H, 't.json'), 'w'))

def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;')
def pct(v): return ('+' if v > 0 else '−') + f'{abs(v):.2f}%'
def nfs(n): return 44 if len(n) <= 12 else 38 if len(n) <= 15 else 33 if len(n) <= 18 else 30
cards = []
for k, d in enumerate(W):
    col, row = k % 3, k // 3
    x = 54 + col * 330; y = 380 + row * 166
    up = d['week_pct'] > 0
    cards.append(f'''<div class="cw" id="cw{k}" style="left:{x}px;top:{y}px"><div class="card boil">
<svg class="cbox" viewBox="0 0 312 156"><path id="cb{k}" d="" /></svg>
<div class="rk">{k + 1}</div><div class="cn" style="font-size:{nfs(d['name'])}px">{esc(d['name'])}</div>
<div class="hi" id="hi{k}">{d['below_hi']:.1f}% vs ₹{d['hi52']:g} high</div>
<div class="cp">₹{d['close']:.2f}</div>
<div class="wk {'up' if up else 'dn'}">{pct(d['week_pct'])}</div></div></div>''')
cards = '\n'.join(cards)
RP = max(range(len(W)), key=lambda k: -W[k]['below_hi'])  # deepest below 1-yr high
rp = W[RP]
# two market-cap examples for the risk scene: cheapest price vs smallest market cap
cheap = min(W, key=lambda d: d['close']); small = min(W, key=lambda d: d['mcap_cr'])
def cr(v): return f"₹{v/100000:.2f} lakh cr" if v >= 100000 else f"₹{v:,.0f} cr"

html = f'''<!doctype html>
<html lang="en" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<title>15 penny stocks of the week ({esc(M['week'])})</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<script src="assets/camera.js"></script>
<style>
@font-face {{ font-family:"Caveat"; src:url("assets/fonts/Caveat-700-latin.woff2") format("woff2"); font-weight:700; }}
@font-face {{ font-family:"Anton"; src:url("assets/fonts/anton-latin-400-normal.woff") format("woff"); }}
@font-face {{ font-family:"Poppins"; src:url("assets/fonts/Poppins-Bold.ttf") format("truetype"); font-weight:700; }}
@font-face {{ font-family:"Oswald"; src:url("assets/fonts/oswald-latin-500-normal.woff") format("woff"); font-weight:500; }}
:root {{ --paper:#FBF8F0; --ink:#1B1B1F; --blue:#2F5BEA; --red:#D93A2B; --grn:#1E9E5A; --hl:#FFE45C; --mut:#5B5B66; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:var(--paper); }}
#root {{ position:relative; width:100%; height:100%; overflow:hidden; color:var(--ink); font-family:"Caveat","Poppins",cursive; }}
#paper {{ position:absolute; inset:0; background-color:var(--paper);
  background-image: linear-gradient(rgba(70,120,220,.13) 2px, transparent 2px), linear-gradient(90deg, rgba(70,120,220,.13) 2px, transparent 2px);
  background-size: 54px 54px; }}
.scene {{ position:absolute; inset:0; }}
.inner, .cam {{ position:absolute; inset:0; }}
.handle {{ position:absolute; left:40px; top:120px; font-family:"Oswald",sans-serif; font-size:30px; color:#55556A; z-index:50; }}
.hand {{ font-family:"Caveat",cursive; font-weight:700; }}
.ttl {{ position:absolute; left:0; right:0; text-align:center; font-size:92px; line-height:1; }}
#kw, .kwc {{ position:absolute; left:0; right:0; top:200px; text-align:center; z-index:45; }}
#kw span, .kwc span {{ display:inline-block; background:var(--ink); color:#fff; font-family:"Oswald",sans-serif; font-size:40px; letter-spacing:2px; padding:10px 32px; border-radius:999px; }}
svg {{ overflow:visible; }}
path {{ fill:none; stroke:var(--ink); stroke-width:6; stroke-linecap:round; stroke-linejoin:round; }}
#big4 {{ position:absolute; left:190px; top:400px; width:700px; height:440px; }}
#big4 svg, #big15 svg, .cbox {{ position:absolute; inset:0; width:100%; height:100%; }}
#big4 .num {{ position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font-family:"Anton",sans-serif; font-size:270px; line-height:1; }}
#big4 .num b {{ color:var(--grn); font-weight:400; }} #big4 .num i {{ font-style:normal; font-size:150px; color:var(--mut); padding-left:14px; }}
#uplab {{ position:absolute; left:0; right:0; top:880px; text-align:center; font-size:84px; }}
#qm {{ position:absolute; left:0; right:0; top:1000px; text-align:center; font-size:72px; color:var(--blue); }}
#qbig {{ position:absolute; left:860px; top:330px; font-family:"Anton",sans-serif; font-size:200px; color:var(--red); }}
#big15 {{ position:absolute; left:340px; top:470px; width:400px; height:400px; }}
#big15 .num {{ position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font-family:"Anton",sans-serif; font-size:250px; color:var(--blue); }}
#sub15 {{ position:absolute; left:0; right:0; top:920px; text-align:center; font-size:80px; line-height:1.15; }}
#src15 {{ position:absolute; left:0; right:0; top:1120px; text-align:center; font-family:"Oswald",sans-serif; font-size:36px; color:var(--mut); }}
.cw {{ position:absolute; width:312px; height:156px; }}
.card {{ position:absolute; inset:0; }}
.card path {{ stroke-width:5; fill:#fff; }}
.rk {{ position:absolute; left:-12px; top:-14px; width:44px; height:44px; border-radius:50%; background:var(--ink); color:#fff; font-family:"Oswald",sans-serif; font-size:28px; display:flex; align-items:center; justify-content:center; }}
.cn {{ position:absolute; left:34px; top:8px; right:10px; line-height:1.05; white-space:nowrap; }}
.hi {{ position:absolute; left:18px; right:10px; top:58px; font-family:"Oswald",sans-serif; font-size:28px; line-height:1; color:var(--red); white-space:nowrap; opacity:0; }}
.cp {{ position:absolute; right:16px; bottom:10px; font-family:"Anton",sans-serif; font-size:42px; color:var(--blue); }}
.wk {{ position:absolute; left:14px; bottom:12px; color:#fff; font-family:"Anton",sans-serif; font-size:34px; padding:2px 12px; border-radius:10px; }}
.wk.up {{ background:var(--grn); }} .wk.dn {{ background:var(--red); }}
.hlc {{ position:absolute; inset:-10px; border:8px solid var(--hl); border-radius:20px; opacity:0; }}
#stampB {{ position:absolute; left:380px; top:610px; font-family:"Anton",sans-serif; font-size:76px; color:var(--grn); border:8px solid var(--grn); border-radius:16px; padding:4px 26px; background:rgba(255,255,255,.92); transform:rotate(-8deg); opacity:0; white-space:nowrap; }}
#twist {{ position:absolute; left:40px; right:40px; top:1216px; text-align:center; font-size:50px; background:#fff; border:5px solid var(--ink); border-radius:18px; padding:6px 10px; white-space:nowrap; line-height:1.05; opacity:0; }}
#twist b {{ color:var(--red); font-weight:700; }}
#twist2 {{ position:absolute; left:40px; right:40px; top:1216px; text-align:center; font-size:50px; background:var(--hl); border:5px solid var(--ink); border-radius:18px; padding:6px 10px; white-space:nowrap; line-height:1.05; opacity:0; }}
#t2 {{ top:290px; font-size:72px; }}
#chk {{ position:absolute; left:110px; right:60px; top:470px; }}
.ck {{ position:relative; height:140px; font-size:72px; padding-left:130px; line-height:120px; white-space:nowrap; }}
.ck svg {{ position:absolute; left:0; top:10px; width:100px; height:100px; }}
.ck .tick {{ stroke:var(--red); stroke-width:10; }}
#circ {{ position:absolute; left:60px; right:60px; top:1040px; text-align:center; font-size:62px; color:var(--red); }}
#cmp {{ position:absolute; left:60px; right:60px; top:1140px; font-family:"Oswald",sans-serif; font-size:34px; color:var(--mut); text-align:center; line-height:1.35; }}
#cmp b {{ color:var(--ink); }}
.host {{ position:absolute; }}
.pill {{ position:absolute; display:inline-block; border-radius:22px; padding:12px 34px; font-family:"Anton",sans-serif; font-size:58px; color:#fff; border:5px solid var(--ink); box-shadow:8px 8px 0 var(--ink); white-space:nowrap; }}
#sendto {{ position:absolute; left:60px; right:60px; top:300px; text-align:center; font-size:76px; line-height:1.1; }}
#cta-save {{ left:400px; top:700px; background:var(--blue); }}
#cta-follow {{ left:380px; top:830px; background:var(--hl); color:var(--ink); }}
#edu {{ position:absolute; left:80px; right:80px; top:1110px; text-align:center; font-family:"Oswald",sans-serif; font-size:36px; line-height:1.3; }}
#risk {{ position:absolute; left:50px; right:50px; top:1305px; text-align:center; font-family:"Oswald",sans-serif; font-size:28px; line-height:1.3; color:var(--ink); background:rgba(255,228,92,.55); border-radius:14px; padding:8px 16px; z-index:30; }}
#disc {{ position:absolute; left:0; right:0; top:1412px; text-align:center; font-family:"Oswald",sans-serif; font-size:28px; color:rgb(84,84,96); z-index:30; }}
#vignette {{ position:absolute; inset:0; pointer-events:none; z-index:99; background:radial-gradient(ellipse at center, transparent 60%, rgba(27,27,31,.10) 100%); }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{DUR}" data-fps="30">
  <div id="paper"></div>
  <div class="handle">@moneyincloud</div>
  <audio id="vo" src="assets/vo_mix.wav" data-start="0" data-duration="{DUR}" data-track-index="9" data-volume="1"></audio>

  <section class="scene clip" id="sc0" data-start="0" data-duration="{SC[0][1] + 0.3:.2f}" data-track-index="1"><div class="inner" id="in0"><div id="kw"><span>15 PENNY STOCKS · {esc(M['week_pill'])}</span></div><div class="cam" id="cam0">
    <div id="big4"><div class="boil" style="position:absolute;inset:0"><svg viewBox="0 0 700 440"><path id="circ4" d="" /></svg><div class="num"><b>{M.get("big_num",NUP)}</b><i>{M.get("big_den","/ "+str(len(W)))}</i></div></div></div>
    <div id="qbig" class="boil">?</div>
    <div id="uplab" class="hand">{M.get("uplab",'went <span style="color:var(--grn)">UP</span> this week')}</div>
    <div id="qm" class="hand">{M.get("qm","what do they have in common?")}</div>
  </div></div></section>

  <section class="scene clip" id="sc1" data-start="{SC[1][0]:.2f}" data-duration="{SC[1][1] - SC[1][0] + 0.3:.2f}" data-track-index="2"><div class="inner" id="in1"><div id="kw1" class="kwc"><span>15 PENNY STOCKS · {esc(M['week_pill'])}</span></div><div class="cam" id="cam1">
    <div id="big15"><div class="boil" style="position:absolute;inset:0"><svg viewBox="0 0 400 400"><path id="circ15" d="" /></svg><div class="num">15</div></div></div>
    <div id="sub15" class="hand">Nifty 500 stocks<br/>under <span style="color:var(--blue)">₹{M['cap']}</span></div>
    <div id="src15">{esc(M.get("src15","Friday close "+M["end_label"]+" vs "+M["prev_label"]+" · NSE via INDmoney"))}</div>
  </div></div></section>

  <section class="scene clip" id="sc2" data-start="{SC[2][0]:.2f}" data-duration="{SC[2][1] - SC[2][0] + 0.3:.2f}" data-track-index="3"><div class="inner" id="in2"><div class="cam" id="cam2">
    <div class="ttl hand" id="t2">this week, best <span style="color:var(--grn)">→</span> worst</div>
    {cards}
    <div id="stampB" style="{M.get("stamp_style","")}">{M.get("stamp","ALL "+str(NUP)+" = BANKS")}</div>
  </div>
    <div id="twist" class="hand">ALL {len(W)}: <b>below their 1-year high</b></div>
    <div id="twist2" class="hand">{esc(rp['name'])}: <b style="color:var(--red)">{rp['below_hi']:.1f}%</b> from ₹{rp['hi52']:g} high</div>
  </div></section>

  <section class="scene clip" id="sc4" data-start="{SC[3][0]:.2f}" data-duration="{SC[3][1] - SC[3][0] + 0.3:.2f}" data-track-index="4" style="perspective:1600px"><div class="inner" id="in4"><div class="cam" id="cam4">
    <div class="ttl hand" style="top:300px">low price <span style="color:var(--red)">≠</span> cheap</div>
    <div id="chk">
      <div class="ck hand"><svg viewBox="0 0 100 100"><path id="bx0" d="M8 10 L92 6 L95 92 L6 95 Z" /><path class="tick" id="tk0" d="M18 52 L42 78 L90 8" /></svg>market cap</div>
      <div class="ck hand"><svg viewBox="0 0 100 100"><path id="bx1" d="M6 8 L93 9 L92 94 L9 92 Z" /><path class="tick" id="tk1" d="M18 52 L42 78 L90 8" /></svg>debt</div>
      <div class="ck hand"><svg viewBox="0 0 100 100"><path id="bx2" d="M9 7 L94 10 L91 93 L7 94 Z" /><path class="tick" id="tk2" d="M18 52 L42 78 L90 8" /></svg>NSE ASM / GSM lists</div>
    </div>
    <div id="circ" class="hand">volatile · can hit lower circuits</div>
    <div id="cmp">₹{cheap['close']:.2f} {esc(cheap['name'])} = <b>{cr(cheap['mcap_cr'])}</b> market cap<br/>₹{small['close']:.2f} {esc(small['name'])} = <b>{cr(small['mcap_cr'])}</b> market cap</div>
  </div></div></section>

  <section class="scene clip" id="sc5" data-start="{SC[4][0]:.2f}" data-duration="{DUR - SC[4][0]:.2f}" data-track-index="5"><div class="inner" id="in5"><div class="cam" id="cam5">
    <div id="sendto" class="hand">send this to the friend who buys<br/>anything under <span style="color:var(--red)">₹50</span></div>
    <img class="host" id="host-wave" src="assets/img/p31.png" style="left:50px;top:560px;width:360px" />
    <div class="pill" id="cta-save">SAVE THIS</div>
    <div class="pill" id="cta-follow">FOLLOW @moneyincloud</div>
    <div id="edu">Every Saturday: 15 penny stocks of the week · Education only, not investment advice</div>
  </div></div></section>

  <div id="risk">Low price ≠ cheap. Check market cap, debt and NSE ASM/GSM surveillance lists.<br/>Penny stocks are volatile and can hit lower circuits.</div>
  <div id="disc">NSE via INDmoney, week ending {esc(M['end_label'])} · Not a buy/sell call · Education only</div>
  <div id="vignette"></div>
</div>
<script>
const SC = {json.dumps(SC)}, CT = {json.dumps(CARD_T)}, TS = {json.dumps(T)}, RP = {RP};
const EIN = "expo.out", EOUT = "expo.in";
const tl = gsap.timeline({{ paused: true }});
const cam = CAM(tl);
window.hwOnUpdate = function (tl, fn) {{ if (!tl.__hwRenders) {{ tl.__hwRenders = []; tl.eventCallback("onUpdate", function () {{ for (var i = 0; i < tl.__hwRenders.length; i++) tl.__hwRenders[i](); }}); }} tl.__hwRenders.push(fn); fn(); }};
window.hwHash = function (n, seed) {{ var x = Math.sin(n * 127.1 + (seed || 1) * 311.7) * 43758.5453; return (x - Math.floor(x)) * 2 - 1; }};
window.hwBoil = function (tl, target, opts) {{ opts = opts || {{}}; var amp = opts.amp ?? 1.6, rot = opts.rot ?? 0.5, fps = 30, drop = opts.frameDrop || 3, seed = opts.seed || 1; var els = gsap.utils.toArray(target);
  window.hwOnUpdate(tl, function () {{ var step = Math.floor((tl.time() * fps) / drop); for (var i = 0; i < els.length; i++) gsap.set(els[i], {{ x: hwHash(step*3+i*97, seed)*amp, y: hwHash(step*3+1+i*97, seed)*amp, rotation: hwHash(step*3+2+i*97, seed)*rot }}); }}); }};
window.hwWobble = function (cx, cy, rx, ry, seed, pct) {{ var N = 14, pts = []; for (var i = 0; i < N; i++) {{ var a = i / N * Math.PI * 2, wr = 1 + hwHash(i*13+5, seed) * pct / 100; pts.push([cx + Math.cos(a)*rx*wr, cy + Math.sin(a)*ry*wr]); }}
  var d = "M" + ((pts[0][0]+pts[N-1][0])/2).toFixed(1) + " " + ((pts[0][1]+pts[N-1][1])/2).toFixed(1);
  for (var j = 0; j < N; j++) {{ var p = pts[j], q = pts[(j+1)%N]; d += " Q" + p[0].toFixed(1) + " " + p[1].toFixed(1) + " " + ((p[0]+q[0])/2).toFixed(1) + " " + ((p[1]+q[1])/2).toFixed(1); }} return d; }};
window.hwRect = function (w, h, seed) {{ const j = k => hwHash(k, seed) * 5; return `M${{6+j(1)}} ${{6+j(2)}} L${{w-6+j(3)}} ${{5+j(4)}} L${{w-5+j(5)}} ${{h-6+j(6)}} L${{5+j(7)}} ${{h-5+j(8)}} Z`; }};
const draw = (sel, at, dur) => {{ const p = document.querySelector(sel); const L = p.getTotalLength(); tl.set(p, {{opacity:0}}, 0); tl.set(p, {{opacity:1}}, at); tl.fromTo(p, {{strokeDasharray:L, strokeDashoffset:L}}, {{strokeDashoffset:0, duration:dur||0.6, ease:"power2.inOut"}}, at); }};
document.getElementById("circ4").setAttribute("d", hwWobble(350, 220, 330, 200, 3, 5));
document.getElementById("circ15").setAttribute("d", hwWobble(200, 200, 185, 185, 7, 5));
for (let k = 0; k < CT.length; k++) document.getElementById("cb"+k).setAttribute("d", hwRect(312, 156, 20+k));
hwBoil(tl, ".boil", {{amp:1.4, rot:0.45}});

// scene enter/exit
const INN = ["#in0","#in1","#in2","#in4","#in5"];
SC.forEach(([a,b],i) => {{
  if (i > 0) tl.fromTo(INN[i], {{xPercent:8, opacity:0}}, {{xPercent:0, opacity:1, duration:0.4, ease:EIN}}, a);
  if (i < SC.length-1) tl.to(INN[i], {{xPercent:-8, opacity:0, duration:0.3, ease:EOUT}}, b - 0.05); }});

// HOOK: number already on screen at frame 0 and moving
tl.fromTo("#big4 .num", {{scale:1.25}}, {{scale:1, duration:0.6, ease:"back.out(2)"}}, 0);
draw("#circ4", 0.0, 0.8);
cam.pushIn("#cam0", 0.2, {{from:1, to:1.12, dur:SC[0][1]-0.3, ease:"sine.inOut"}});
tl.fromTo("#uplab", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.35, ease:EIN}}, 0.5);
tl.fromTo("#qm", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.35, ease:EIN}}, 2.2);
tl.fromTo("#qbig", {{scale:0, rotation:-30}}, {{scale:1, rotation:12, duration:0.5, ease:"back.out(2)"}}, 1.2);
tl.to("#qbig", {{rotation:-8, duration:0.6, ease:"sine.inOut", yoyo:true, repeat:3}}, 1.7);

// 15 under 50
draw("#circ15", SC[1][0] + 0.2, 0.7);
tl.fromTo("#big15 .num", {{scale:0.4, opacity:0}}, {{scale:1, opacity:1, duration:0.5, ease:"back.out(2)"}}, SC[1][0] + 0.15);
tl.fromTo("#sub15", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.4, ease:EIN}}, SC[1][0] + 1.0);
tl.fromTo("#src15", {{opacity:0}}, {{opacity:1, duration:0.4}}, TS.l1[0] + 1.2);
cam.pullOut("#cam1", SC[1][0], {{from:1.2, to:1, dur:SC[1][1]-SC[1][0]}});

// CARDS pop as each name is spoken
CT.forEach((ts, k) => {{
  tl.fromTo("#cw"+k, {{scale:0.5, opacity:0, rotation:(k%2?4:-4)}}, {{scale:1, opacity:1, rotation:0, duration:0.4, ease:"back.out(1.8)"}}, ts - 0.1);
  draw("#cb"+k, ts - 0.1, 0.45); }});
// banks stamp
tl.fromTo("#stampB", {{opacity:0, scale:2.4}}, {{opacity:1, scale:1, duration:0.3, ease:"back.out(1.5)"}}, TS.banks[0] + 0.1);
tl.to("#stampB", {{opacity:0, duration:0.25}}, TS.f4[0] - 0.25);
// worst: crash zoom on the last card
const lc = document.getElementById("cw14"); const ox = (parseFloat(lc.style.left)+156)+"px", oy = (parseFloat(lc.style.top)+78)+"px";
cam.crashZoom("#cam2", TS.f14[0] + 1.2, {{to:1.15, hold:1.4, ox:ox, oy:oy}});
// twist: below-1-yr-high line on every card
cam.dutch("#cam2", TS.twist[0], {{deg:-5, dur:0.5, hold:1.6}});
tl.fromTo("#twist", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.4, ease:EIN}}, TS.twist[0] + 1.9);
for (let k = 0; k < CT.length; k++) tl.fromTo("#hi"+k, {{opacity:0, x:-10}}, {{opacity:1, x:0, duration:0.25}}, TS.twist[0] + 2.0 + k*0.07);
tl.to("#twist", {{opacity:0, duration:0.2}}, TS.rp[0] - 0.1);
tl.fromTo("#twist2", {{opacity:0, scale:0.8}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, TS.rp[0]);
const rc = document.getElementById("cw"+RP);
cam.pushIn("#cam2", TS.rp[0] + 0.1, {{from:1, to:1.08, dur:1.6, ox:(parseFloat(rc.style.left)+156)+"px", oy:(parseFloat(rc.style.top)+78)+"px"}});
tl.fromTo("#cw"+RP, {{boxShadow:"0 0 0 0 rgba(255,228,92,0)"}}, {{boxShadow:"0 0 0 14px rgba(255,228,92,1)", duration:0.3, borderRadius:20}}, TS.rp[0] + 0.1);

// CHECKLIST
cam.tilt("#cam4", SC[3][0], {{from:22, to:0, dur:1.2}});
["bx0","bx1","bx2"].forEach((b,k) => draw("#"+b, SC[3][0] + 0.2 + k*0.15, 0.4));
draw("#tk0", TS.r1[0] + 0.2, 0.35); draw("#tk1", TS.r2[0] + 0.1, 0.35); draw("#tk2", TS.r3[0] + 0.3, 0.35);
tl.fromTo("#circ", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.4, ease:EIN}}, TS.r4[0]);
tl.fromTo("#cmp", {{opacity:0}}, {{opacity:1, duration:0.4}}, TS.r1[0]);
cam.shake("#cam4", TS.r4[0] + 1.6, {{}});

// CTA
cam.pushIn("#cam5", SC[4][0] + 0.3, {{from:1, to:1.03, dur:DURATION_CTA, ease:"sine.inOut", ox:"40%", oy:"35%"}});
tl.fromTo("#sendto", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.4, ease:EIN}}, SC[4][0] + 0.15);
tl.fromTo("#host-wave", {{y:100, opacity:0}}, {{y:0, opacity:1, duration:0.5, ease:EIN}}, SC[4][0] + 0.3);
tl.fromTo("#cta-save", {{scale:0.4, opacity:0}}, {{scale:1, opacity:1, duration:0.45, ease:"back.out(2)"}}, TS.cta[0] + 3.4);
tl.fromTo("#cta-follow", {{scale:0.4, opacity:0}}, {{scale:1, opacity:1, duration:0.45, ease:"back.out(2)"}}, TS.cta[0] + 4.4);
tl.fromTo("#edu", {{opacity:0}}, {{opacity:1, duration:0.4}}, TS.cta[0] + 6.6);
tl.fromTo("#risk", {{opacity:0}}, {{opacity:1, duration:0.4}}, 1.0);
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''.replace('DURATION_CTA', f'{DUR - SC[4][0] - 0.5:.2f}')
open(os.path.join(H, '..', 'index.html'), 'w').write(html)
print('ok', DUR, 'up', NUP, 'deepest', rp['name'])
