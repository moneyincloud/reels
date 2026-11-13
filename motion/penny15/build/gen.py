"""Doodle-style 15 penny stocks reel (HyperFrames + hand-drawn kit helpers)."""
import json, re, os
H = os.path.dirname(__file__)
T = json.load(open(os.path.join(H, 't.json')))
DUR = T['DUR']; S = T['STARTS']
STOCKS = [("Vodafone Idea", "Telecom", 12.56, -20.5), ("Yes Bank", "Private bank", 17.57, -31.8), ("Suzlon", "Wind energy", 38.16, -36.9),
          ("UCO Bank", "PSU bank", 24.85, -23.3), ("Punjab & Sind", "PSU bank", 21.75, -30.8), ("Central Bank", "PSU bank", 32.18, -21.4),
          ("Indian Overseas", "PSU bank", 31.63, -22.4), ("IRB Infra", "Toll roads", 18.79, -21.5), ("Reliance Power", "Power plants", 18.54, -56.8),
          ("JP Power", "Power", 14.08, -42.5), ("Alok Ind.", "Textiles", 8.13, -54.0), ("Trident", "Home textiles", 23.51, -24.0),
          ("HCC", "Construction", 18.44, -35.3), ("RattanIndia Pwr", "Thermal power", 7.00, -35.1), ("GTL Infra", "Telecom towers", 1.08, -35.3)]
SPOKEN = ["Nobody tells you this ₹12 stock is worth ₹1.4 lakh crore.", "Here are 15 popular penny stocks, all under ₹40.",
          "Vodafone Idea, Yes Bank, Suzlon, and 4 PSU banks: UCO, Punjab & Sind, Central Bank, and Indian Overseas Bank.",
          "Then IRB, Reliance Power, JP Power, Alok, Trident, HCC, RattanIndia Power, and GTL Infra, at just ₹1.",
          "The twist? Every single one is down 20% to 57% from its 1-year high.",
          "A low price is not cheap. Check the market value, the debt, and the exchange's surveillance list first.",
          "Which one do you own? Comment PENNY, and follow for more."]
SC = [(0, S[1]), (S[1], S[2]), (S[2], S[4]), (S[4], S[5]), (S[5], S[6]), (S[6], DUR)]

groups = []
for i, line in enumerate(SPOKEN):
    words = line.split(); cur = []; gs = []
    for w in words:
        cur.append(w)
        if len(cur) >= 4 or re.search(r'[.,?!:]$', w): gs.append(cur); cur = []
    if cur: gs.append(cur)
    tot = sum(len(' '.join(g)) for g in gs); t0 = T['VO'][i]; d = T['DURS'][i]; acc = 0
    for g in gs:
        txt = ' '.join(g); st = t0 + d * acc / tot; acc += len(txt); en = t0 + d * acc / tot
        groups.append((round(st, 2), round(en, 2), txt))
line4 = (T['VO'][4] - 0.1, T['VO'][4] + T['DURS'][4] + 0.3)
groups = [g for g in groups if not (line4[0] <= g[0] <= line4[1])]
caps = []
for k, (st, en, txt) in enumerate(groups):
    nxt = groups[k + 1][0] if k + 1 < len(groups) else DUR - 0.2
    caps.append((st, round(min(max(en, nxt - 0.02), en + 0.6), 2), txt))

def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;')
cards = []
for k, (nm, biz, p, dd) in enumerate(STOCKS):
    col, row = k % 3, k // 3
    x = 54 + col * 330; y = 400 + row * 160
    cards.append(f'''<div class="cw" id="cw{k}" style="left:{x}px;top:{y}px"><div class="card boil" id="cd{k}">
<svg class="cbox" viewBox="0 0 312 146"><path id="cb{k}" d="" /></svg>
<div class="cn">{esc(nm)}</div><div class="cb">{esc(biz)}</div><div class="cp">₹{p:.2f}</div>
<div class="dd" id="dd{k}">{dd:.0f}%</div></div></div>''')
cards = '\n'.join(cards)
caps_html = '\n'.join(f'<div class="cap" id="cap{k}"><span>{esc(t)}</span></div>' for k, (_, _, t) in enumerate(caps))

html = f'''<!doctype html>
<html lang="en" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<title>15 penny stocks under ₹40 (doodle)</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
@font-face {{ font-family:"Caveat"; src:url("assets/fonts/Caveat-700-latin.woff2") format("woff2"); font-weight:700; }}
@font-face {{ font-family:"Anton"; src:url("assets/fonts/anton-latin-400-normal.woff") format("woff"); }}
@font-face {{ font-family:"Poppins"; src:url("assets/fonts/Poppins-Bold.ttf") format("truetype"); font-weight:700; }}
@font-face {{ font-family:"Oswald"; src:url("assets/fonts/oswald-latin-500-normal.woff") format("woff"); font-weight:500; }}
:root {{ --paper:#FBF8F0; --ink:#1B1B1F; --blue:#2F5BEA; --red:#D93A2B; --hl:#FFE45C; --mut:#5B5B66; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:var(--paper); }}
#root {{ position:relative; width:100%; height:100%; overflow:hidden; color:var(--ink); font-family:"Caveat","Poppins",cursive; }}
#paper {{ position:absolute; inset:0; background-color:var(--paper);
  background-image: linear-gradient(rgba(70,120,220,.13) 2px, transparent 2px), linear-gradient(90deg, rgba(70,120,220,.13) 2px, transparent 2px);
  background-size: 54px 54px; }}
.scene {{ position:absolute; inset:0; }}
.inner {{ position:absolute; inset:0; }}
.handle {{ position:absolute; left:40px; top:120px; font-family:"Oswald",sans-serif; font-size:30px; color:#55556A; z-index:50; }}
.hand {{ font-family:"Caveat",cursive; font-weight:700; }}
.ttl {{ position:absolute; left:0; right:0; text-align:center; font-size:96px; line-height:1; }}
.wm {{ display:inline-block; overflow:hidden; vertical-align:top; padding:0 6px 14px; margin-bottom:-14px; }}
.w {{ display:inline-block; }}
#kw {{ position:absolute; left:0; right:0; top:205px; text-align:center; }}
#kw span {{ display:inline-block; background:var(--ink); color:#fff; font-family:"Oswald",sans-serif; font-size:42px; letter-spacing:2px; padding:10px 32px; border-radius:999px; }}
#price12 {{ position:absolute; left:120px; top:420px; width:400px; height:300px; }}
#price12 svg, #worth svg, .cbox, #big15 svg {{ position:absolute; inset:0; width:100%; height:100%; overflow:visible; }}
path {{ fill:none; stroke:var(--ink); stroke-width:6; stroke-linecap:round; stroke-linejoin:round; }}
#price12 .num {{ position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font-family:"Anton",sans-serif; font-size:150px; }}
#vi-lab {{ position:absolute; left:130px; top:730px; width:380px; text-align:center; font-size:60px; }}
#arrow1 {{ position:absolute; left:470px; top:480px; width:220px; height:200px; }}
#arrow1 svg {{ width:100%; height:100%; overflow:visible; }}
#worth {{ position:absolute; left:560px; top:600px; width:480px; height:250px; }}
#worth .num {{ position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; }}
#worth .num b {{ font-family:"Anton",sans-serif; font-weight:400; font-size:74px; white-space:nowrap; color:var(--blue); line-height:1; }}
#worth .num i {{ font-style:normal; font-size:56px; }}
#hl-worth {{ position:absolute; left:575px; top:672px; width:450px; height:96px; background:var(--hl); transform-origin:left center; border-radius:12px; opacity:.75; }}
#big15 {{ position:absolute; left:340px; top:560px; width:400px; height:400px; }}
#big15 .num {{ position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font-family:"Anton",sans-serif; font-size:260px; color:var(--blue); }}
#under40 {{ position:absolute; left:0; right:0; top:1000px; text-align:center; font-size:84px; }}
.cw {{ position:absolute; width:312px; height:146px; }}
.card {{ position:absolute; inset:0; }}
.card path {{ stroke-width:5; fill:#fff; }}
.cn {{ position:absolute; left:18px; top:10px; right:12px; font-size:46px; line-height:1; white-space:nowrap; }}
.cb {{ position:absolute; left:20px; top:62px; max-width:150px; font-family:"Oswald",sans-serif; font-size:26px; color:var(--mut); }}
.cp {{ position:absolute; right:18px; bottom:10px; font-family:"Anton",sans-serif; font-size:44px; color:var(--blue); }}
.dd {{ position:absolute; left:14px; bottom:12px; background:var(--red); color:#fff; font-family:"Anton",sans-serif; font-size:40px; padding:2px 14px; border-radius:10px; opacity:0; }}
#twist {{ position:absolute; left:40px; right:40px; top:1200px; text-align:center; font-size:50px; background:#fff; border:5px solid var(--ink); border-radius:18px; padding:6px 10px; white-space:nowrap; line-height:1.05; opacity:0; }}
#twist b {{ color:var(--red); font-weight:700; }}
#chk {{ position:absolute; left:110px; right:80px; top:560px; }}
.ck {{ position:relative; height:150px; font-size:76px; padding-left:130px; line-height:120px; }}
.ck svg {{ position:absolute; left:0; top:10px; width:100px; height:100px; overflow:visible; }}
.ck .tick {{ stroke:var(--red); stroke-width:10; }}
#cmp {{ position:absolute; left:80px; right:80px; top:1050px; font-family:"Oswald",sans-serif; font-size:36px; color:var(--mut); text-align:center; }}
#cmp b {{ color:var(--ink); }}
.host {{ position:absolute; }}
.pill {{ position:absolute; display:inline-block; border-radius:22px; padding:12px 34px; font-family:"Anton",sans-serif; font-size:60px; color:#fff; border:5px solid var(--ink); box-shadow:8px 8px 0 var(--ink); white-space:nowrap; }}
#cta-comment {{ left:430px; top:820px; background:var(--blue); }}
#cta-follow {{ left:430px; top:950px; background:var(--hl); color:var(--ink); }}
.cap {{ position:absolute; left:0; right:0; top:1215px; text-align:center; opacity:0; }}
.cap span {{ display:inline-block; max-width:920px; background:#fff; border:5px solid var(--ink); border-radius:18px; box-shadow:6px 8px 0 var(--ink); padding:10px 34px; font-family:"Poppins",sans-serif; font-weight:700; font-size:44px; line-height:1.25; }}
#disc {{ position:absolute; left:0; right:0; top:1305px; text-align:center; font-family:"Oswald",sans-serif; font-size:28px; color:rgb(84,84,96); z-index:30; }}
#vignette {{ position:absolute; inset:0; pointer-events:none; z-index:99; background:radial-gradient(ellipse at center, transparent 60%, rgba(27,27,31,.10) 100%); }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{DUR}" data-fps="30">
  <div id="paper"></div>
  <div class="handle">@moneyincloud</div>
  <audio id="vo" src="assets/vo_mix.wav" data-start="0" data-duration="{DUR}" data-track-index="9" data-volume="1"></audio>

  <section class="scene clip" id="sc0" data-start="0" data-duration="{SC[0][1] + 0.3:.2f}" data-track-index="1"><div class="inner" id="in0">
    <div id="kw"><span>PENNY STOCKS UNDER ₹40 · INDIA 2026</span></div>
    <div id="price12"><div class="boil" id="b-p12" style="position:absolute;inset:0"><svg viewBox="0 0 400 300"><path id="circ12" d="" /></svg><div class="num">₹12</div></div></div>
    <div id="vi-lab" class="hand">Vodafone Idea</div>
    <div id="arrow1"><svg viewBox="0 0 220 200"><path id="arr1" d="M10 30 C 90 10, 150 60, 190 150" /><path id="arr1h" d="M160 140 L192 156 L196 118" /></svg></div>
    <div id="hl-worth"></div>
    <div id="worth"><div class="boil" id="b-worth" style="position:absolute;inset:0"><svg viewBox="0 0 480 250"><path id="box-worth" d="" /></svg>
      <div class="num"><b>₹1.4 LAKH CR</b><i class="hand">company value</i></div></div></div>
  </div></section>

  <section class="scene clip" id="sc1" data-start="{SC[1][0]}" data-duration="{SC[1][1] - SC[1][0] + 0.3:.2f}" data-track-index="2"><div class="inner" id="in1">
    <div class="ttl hand" style="top:300px">popular <span style="color:var(--red)">penny</span> stocks</div>
    <div id="big15"><div class="boil" id="b-15" style="position:absolute;inset:0"><svg viewBox="0 0 400 400"><path id="circ15" d="" /></svg><div class="num">15</div></div></div>
    <div id="under40" class="hand">all under <span style="color:var(--blue)">₹40</span></div>
  </div></section>

  <section class="scene clip" id="sc2" data-start="{SC[2][0]}" data-duration="{SC[3][1] - SC[2][0] + 0.3:.2f}" data-track-index="3"><div class="inner" id="in2">
    <div class="ttl hand" style="top:225px;font-size:84px" id="t2">15 under <span style="color:var(--blue)">₹40</span> · live price</div>
    {cards}
    <div id="twist" class="hand">ALL 15: <b>down 20% to 57%</b> from 1-year high</div>
  </div></section>

  <section class="scene clip" id="sc4" data-start="{SC[4][0]}" data-duration="{SC[4][1] - SC[4][0] + 0.3:.2f}" data-track-index="4"><div class="inner" id="in4">
    <div class="ttl hand" style="top:300px">low price <span style="color:var(--red)">≠</span> cheap</div>
    <div id="chk">
      <div class="ck hand" id="ck0"><svg viewBox="0 0 100 100"><path id="bx0" d="M8 10 L92 6 L95 92 L6 95 Z" /><path class="tick" id="tk0" d="M18 52 L42 78 L90 8" /></svg>market value</div>
      <div class="ck hand" id="ck1"><svg viewBox="0 0 100 100"><path id="bx1" d="M6 8 L93 9 L92 94 L9 92 Z" /><path class="tick" id="tk1" d="M18 52 L42 78 L90 8" /></svg>debt</div>
      <div class="ck hand" id="ck2"><svg viewBox="0 0 100 100"><path id="bx2" d="M9 7 L94 10 L91 93 L7 94 Z" /><path class="tick" id="tk2" d="M18 52 L42 78 L90 8" /></svg>surveillance list</div>
    </div>
    <div id="cmp">₹12.56 Vodafone Idea = <b>₹1.4 lakh cr</b> · ₹8.13 Alok = <b>₹4,072 cr</b></div>
  </div></section>

  <section class="scene clip" id="sc5" data-start="{SC[5][0]}" data-duration="{DUR - SC[5][0]:.2f}" data-track-index="5"><div class="inner" id="in5">
    <div class="ttl hand" style="top:300px">which one do <span style="color:var(--blue)">you</span> own?</div>
    <img class="host" id="host-wave" src="assets/img/p31.png" style="left:50px;top:620px;width:360px" />
    <div class="pill" id="cta-comment">COMMENT "PENNY"</div>
    <div class="pill" id="cta-follow">FOLLOW @moneyincloud</div>
  </div></section>

  <section class="clip" id="caps" data-start="0" data-duration="{DUR}" data-track-index="6" data-track-kind="captions" style="position:absolute;inset:0;z-index:40">
    {caps_html}
  </section>
  <div id="disc">Prices: INDmoney, 13 Nov 2026, 3:13 PM · Not a buy/sell call · Education only</div>
  <div id="vignette"></div>
</div>
<script>
const T = {json.dumps(T)};
const CAPS = {json.dumps(caps)};
const SC = {json.dumps(SC)};
const EIN = "expo.out", EOUT = "expo.in";
const tl = gsap.timeline({{ paused: true }});
// ---- hand-drawn kit helpers (from registry hw-boil) ----
window.hwOnUpdate = function (tl, fn) {{ if (!tl.__hwRenders) {{ tl.__hwRenders = []; tl.eventCallback("onUpdate", function () {{ for (var i = 0; i < tl.__hwRenders.length; i++) tl.__hwRenders[i](); }}); }} tl.__hwRenders.push(fn); fn(); }};
window.hwHash = function (n, seed) {{ var x = Math.sin(n * 127.1 + (seed || 1) * 311.7) * 43758.5453; return (x - Math.floor(x)) * 2 - 1; }};
window.hwBoil = function (tl, target, opts) {{ opts = opts || {{}}; var amp = opts.amp ?? 1.6, rot = opts.rot ?? 0.5, fps = 30, drop = opts.frameDrop || 3, seed = opts.seed || 1; var els = gsap.utils.toArray(target);
  window.hwOnUpdate(tl, function () {{ var step = Math.floor((tl.time() * fps) / drop); for (var i = 0; i < els.length; i++) gsap.set(els[i], {{ x: hwHash(step*3+i*97, seed)*amp, y: hwHash(step*3+1+i*97, seed)*amp, rotation: hwHash(step*3+2+i*97, seed)*rot }}); }}); }};
window.hwWobble = function (cx, cy, rx, ry, seed, pct) {{ var N = 14, pts = []; for (var i = 0; i < N; i++) {{ var a = i / N * Math.PI * 2, wr = 1 + hwHash(i*13+5, seed) * pct / 100; pts.push([cx + Math.cos(a)*rx*wr, cy + Math.sin(a)*ry*wr]); }}
  var d = "M" + ((pts[0][0]+pts[N-1][0])/2).toFixed(1) + " " + ((pts[0][1]+pts[N-1][1])/2).toFixed(1);
  for (var j = 0; j < N; j++) {{ var p = pts[j], q = pts[(j+1)%N]; d += " Q" + p[0].toFixed(1) + " " + p[1].toFixed(1) + " " + ((p[0]+q[0])/2).toFixed(1) + " " + ((p[1]+q[1])/2).toFixed(1); }} return d; }};
window.hwRect = function (w, h, seed) {{ const j = k => hwHash(k, seed) * 5; return `M${{6+j(1)}} ${{6+j(2)}} L${{w-6+j(3)}} ${{5+j(4)}} L${{w-5+j(5)}} ${{h-6+j(6)}} L${{5+j(7)}} ${{h-5+j(8)}} Z`; }};
const draw = (sel, at, dur) => {{ const p = document.querySelector(sel); const L = p.getTotalLength(); tl.set(p, {{opacity:0}}, 0); tl.set(p, {{opacity:1}}, at); tl.fromTo(p, {{strokeDasharray:L, strokeDashoffset:L}}, {{strokeDashoffset:0, duration:dur||0.6, ease:"power2.inOut"}}, at); }};
document.getElementById("circ12").setAttribute("d", hwWobble(200, 150, 185, 130, 3, 5));
document.getElementById("circ15").setAttribute("d", hwWobble(200, 200, 185, 185, 7, 5));
document.getElementById("box-worth").setAttribute("d", hwRect(480, 250, 11));
for (let k = 0; k < 15; k++) document.getElementById("cb"+k).setAttribute("d", hwRect(312, 146, 20+k));
hwBoil(tl, ".boil", {{amp:1.4, rot:0.45}});

// scene enter/exit
SC.forEach(([a,b],i) => {{ const id = ["#in0","#in1","#in2","#in2","#in4","#in5"][i]; if (i===3) return;
  if (i > 0) tl.fromTo(id, {{yPercent:6, opacity:0}}, {{yPercent:0, opacity:1, duration:0.4, ease:EIN}}, a);
  const end = i === 2 ? SC[3][1] : b; if (i < SC.length-1) tl.to(id, {{yPercent:-5, opacity:0, duration:0.3, ease:EOUT}}, end - 0.05); }});

// HOOK (frame 0 already shows ₹12 + keyword pill)
tl.fromTo("#circ12", {{strokeDasharray:1200, strokeDashoffset:1200}}, {{strokeDashoffset:0, duration:0.7, ease:"power2.inOut"}}, 0.0);
tl.fromTo("#vi-lab", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.4, ease:EIN}}, 0.6);
draw("#arr1", 1.6, 0.5); draw("#arr1h", 2.05, 0.2);
tl.fromTo("#worth", {{scale:0.6, opacity:0}}, {{scale:1, opacity:1, duration:0.5, ease:"back.out(2)"}}, T.lakh - 0.3);
draw("#box-worth", T.lakh - 0.3, 0.6);
tl.fromTo("#hl-worth", {{scaleX:0}}, {{scaleX:1, duration:0.45, ease:"power2.out"}}, T.lakh + 0.4);

// 15 / under ₹40
draw("#circ15", T.fifteen - 0.2, 0.7);
tl.fromTo("#big15 .num", {{scale:0.4, opacity:0}}, {{scale:1, opacity:1, duration:0.5, ease:"back.out(2)"}}, T.fifteen - 0.2);
tl.fromTo("#under40", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.4, ease:EIN}}, T.fifteen + 0.8);

// CARDS pop as each name is spoken; box draws on
T.stocks.forEach((ts, k) => {{
  tl.fromTo("#cw"+k, {{scale:0.5, opacity:0, rotation:(k%2?4:-4)}}, {{scale:1, opacity:1, rotation:0, duration:0.4, ease:"back.out(1.8)"}}, ts - 0.1);
  draw("#cb"+k, ts - 0.1, 0.45);
}});
// TWIST: red % stamps ripple across all 15
tl.to(".cb", {{opacity:0, duration:0.2}}, T.twist);
for (let k = 0; k < 15; k++) tl.fromTo("#dd"+k, {{opacity:0, scale:2.2, rotation:-12}}, {{opacity:1, scale:1, rotation:-6, duration:0.3, ease:"back.out(1.6)"}}, T.twist + 0.15 + k*0.07);
tl.fromTo("#twist", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.4, ease:EIN}}, T.twist - 0.1);

// CHECKLIST
["bx0","bx1","bx2"].forEach((b,k) => draw("#"+b, SC[4][0] + 0.2 + k*0.15, 0.4));
draw("#tk0", T.mv - 0.2, 0.35); draw("#tk1", T.debt - 0.2, 0.35); draw("#tk2", T.surv - 0.2, 0.35);
tl.fromTo("#cmp", {{opacity:0}}, {{opacity:1, duration:0.4}}, T.mv - 0.3);

// CTA
tl.fromTo("#host-wave", {{y:100, opacity:0}}, {{y:0, opacity:1, duration:0.5, ease:EIN}}, SC[5][0] + 0.2);
tl.fromTo("#cta-comment", {{scale:0.4, opacity:0}}, {{scale:1, opacity:1, duration:0.45, ease:"back.out(2)"}}, T.comment - 0.2);
tl.fromTo("#cta-follow", {{scale:0.4, opacity:0}}, {{scale:1, opacity:1, duration:0.45, ease:"back.out(2)"}}, T.follow - 0.1);

// CAPTIONS (hidden while the twist line shares the slot)
CAPS.forEach(([st, en, txt], k) => {{ const g = "#cap"+k;
  tl.fromTo(g, {{opacity:0, y:14}}, {{opacity:1, y:0, duration:0.14, ease:"power2.out"}}, Math.max(0.15, st - 0.05));
  tl.to(g, {{opacity:0, duration:0.1}}, en - 0.1); tl.set(g, {{opacity:0, visibility:"hidden"}}, en); }});
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''
open(os.path.join(H, '..', 'index.html'), 'w').write(html)
print('caps', len(caps))
