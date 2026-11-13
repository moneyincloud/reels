"""Doodle reel: Earn -> income tax, Spend -> GST again (HyperFrames + hand-drawn kit + owner's doodle stickers)."""
import json, re, os
H = os.path.dirname(__file__)
T = json.load(open(os.path.join(H, 't.json')))
DUR = T['DUR']; S = T['STARTS']
SPOKEN = ["You pay income tax when you earn. And you pay GST again when you spend.",
          "Say your salary is ₹15 lakh a year.",
          "Under the new tax regime, after the ₹75,000 standard deduction, your income tax with cess is ₹97,500.",
          "That leaves about ₹1,16,875 a month.",
          "Now you buy a 43-inch TV for ₹30,000.",
          "18% GST is already inside that price. That's ₹4,576.",
          "Spend ₹1 lakh a year on 18% items, and about ₹15,000 of it is GST.",
          "Some relief: since September 2025, milk, paneer and health insurance carry zero GST.",
          "Earn, tax. Spend, tax again. Is it fair? Comment TAX and tell me."]
# scenes: 0 hook | 1 salary->tax->take-home (lines 1-3) | 2 TV (4-5) | 3 lakh (6) | 4 relief (7) | 5 CTA (8)
SC = [(0, S[1]), (S[1], S[4]), (S[4], S[6]), (S[6], S[7]), (S[7], S[8]), (S[8], DUR)]

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
caps = []
for k, (st, en, txt) in enumerate(groups):
    nxt = groups[k + 1][0] if k + 1 < len(groups) else DUR - 0.2
    caps.append((st, round(min(max(en, nxt - 0.02), en + 0.6), 2), txt))

def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;')
def img(id_, f, x, y, w, extra=''): return f'<img class="stk" id="{id_}" src="assets/img/{f}.png" style="left:{x}px;top:{y}px;width:{w}px;{extra}" />'
caps_html = '\n'.join(f'<div class="cap" id="cap{k}"><span>{esc(t)}</span></div>' for k, (_, _, t) in enumerate(caps))

html = f'''<!doctype html>
<html lang="en" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<title>Earn tax, spend tax again (doodle)</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
@font-face {{ font-family:"Caveat"; src:url("assets/fonts/Caveat-700-latin.woff2") format("woff2"); font-weight:700; }}
@font-face {{ font-family:"Anton"; src:url("assets/fonts/anton-latin-400-normal.woff") format("woff"); }}
@font-face {{ font-family:"Poppins"; src:url("assets/fonts/Poppins-Bold.ttf") format("truetype"); font-weight:700; }}
@font-face {{ font-family:"Oswald"; src:url("assets/fonts/oswald-latin-500-normal.woff") format("woff"); font-weight:500; }}
:root {{ --paper:#FBF8F0; --ink:#1B1B1F; --blue:#2F5BEA; --red:#D93A2B; --green:#1E8E4E; --hl:#FFE45C; --mut:#5B5B66; }}
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
#kw {{ position:absolute; left:0; right:0; top:205px; text-align:center; }}
#kw span {{ display:inline-block; background:var(--ink); color:#fff; font-family:"Oswald",sans-serif; font-size:40px; letter-spacing:2px; padding:10px 32px; border-radius:999px; }}
.stk {{ position:absolute; height:auto; filter:drop-shadow(4px 6px 0 rgba(27,27,31,.18)); }}
svg.ov {{ position:absolute; overflow:visible; }}
path {{ fill:none; stroke:var(--ink); stroke-width:7; stroke-linecap:round; stroke-linejoin:round; }}
.big {{ position:absolute; left:0; right:0; text-align:center; font-family:"Anton",sans-serif; line-height:1; }}
.row {{ position:absolute; left:80px; font-size:108px; line-height:1; }}
.row b {{ font-weight:700; }}
.note {{ position:absolute; left:70px; right:70px; text-align:center; font-family:"Oswald",sans-serif; font-size:32px; color:var(--mut); }}
.hl {{ position:absolute; background:var(--hl); opacity:.8; border-radius:10px; transform-origin:left center; }}
.formula {{ position:absolute; left:0; right:0; text-align:center; font-size:66px; }}
.ck {{ position:relative; height:128px; font-size:84px; padding-left:130px; line-height:110px; }}
.ck svg {{ position:absolute; left:0; top:8px; width:96px; height:96px; overflow:visible; }}
.ck .tick {{ stroke:var(--green); stroke-width:11; }}
.pill {{ position:absolute; display:inline-block; border-radius:22px; padding:12px 34px; font-family:"Anton",sans-serif; font-size:62px; color:#fff; border:5px solid var(--ink); box-shadow:8px 8px 0 var(--ink); white-space:nowrap; }}
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
    <div id="kw"><span>INCOME TAX + GST · INDIA 2026</span></div>
    <div class="row hand" id="r1" style="top:330px">EARN <span style="color:var(--mut)">→</span> <b style="color:var(--red)">TAX</b></div>
    <div class="row hand" id="r2" style="top:480px">SPEND <span style="color:var(--mut)">→</span> <b style="color:var(--red)">TAX</b></div>
    <div class="hand" id="again" style="position:absolute;left:330px;top:610px;font-size:130px;color:var(--red);transform:rotate(-6deg)">AGAIN!</div>
    <svg class="ov" style="left:330px;top:740px;width:330px;height:40px" viewBox="0 0 330 40"><path id="ul0" d="M5 25 C 90 10, 200 38, 325 14" style="stroke:var(--red)" /></svg>
    {img("st-think", "s0_001", 760, 290, 290)}
    {img("st-why", "s4_002", 120, 830, 330)}
    {img("st-q", "s0_002", 760, 760, 150) if os.path.exists(os.path.join(H,'..','assets/img/s0_002.png')) else ''}
  </div></section>

  <section class="scene clip" id="sc1" data-start="{SC[1][0]}" data-duration="{SC[1][1] - SC[1][0] + 0.3:.2f}" data-track-index="2"><div class="inner" id="in1">
    {img("st-lpa", "s2_004", 70, 250, 230)}
    {img("st-salary", "s0_003", 60, 420, 420)}
    <svg class="ov" style="left:470px;top:470px;width:160px;height:140px" viewBox="0 0 160 140"><path id="a1" d="M10 30 C 70 10, 120 40, 145 110" /><path id="a1h" d="M118 98 L146 114 L150 80" /></svg>
    {img("st-tax", "s0_000", 640, 300, 340)}
    <div class="note" id="n-regime" style="top:760px;left:560px;right:40px;text-align:center;font-size:30px">new regime · after ₹75,000<br>standard deduction · incl. 4% cess</div>
    <svg class="ov" style="left:560px;top:850px;width:160px;height:140px" viewBox="0 0 160 140"><path id="a2" d="M140 10 C 100 40, 60 60, 30 120" /><path id="a2h" d="M22 88 L28 124 L62 112" /></svg>
    {img("st-take", "s0_004", 140, 760, 420)}
    <div class="hl" id="hl-take" style="left:165px;top:1150px;width:370px;height:16px"></div>
    <div class="note" id="n-take" style="top:1110px;left:560px;right:40px;font-size:28px">₹15,00,000 − ₹97,500 = ₹14,02,500 ÷ 12<br>(before EPF &amp; professional tax)</div>
  </div></section>

  <section class="scene clip" id="sc2" data-start="{SC[2][0]}" data-duration="{SC[2][1] - SC[2][0] + 0.3:.2f}" data-track-index="3"><div class="inner" id="in2">
    <div class="ttl hand" style="top:240px" id="t2">now you <span style="color:var(--blue)">spend</span> it…</div>
    {img("st-cart", "s4_015", 60, 380, 220)}
    {img("st-tv", "s4_016", 300, 360, 460)}
    {img("st-price", "s4_020", 720, 380, 300)}
    {img("st-gst18", "s3_011", 70, 720, 300)}
    {img("st-4576", "s4_029", 400, 740, 360)}
    {img("st-shock", "s3_018", 770, 700, 270)}
    <div class="formula hand" id="f1" style="top:1040px">₹30,000 × 18 ÷ 118 = <span style="color:var(--red)">₹4,576</span></div>
  </div></section>

  <section class="scene clip" id="sc3" data-start="{SC[3][0]}" data-duration="{SC[3][1] - SC[3][0] + 0.3:.2f}" data-track-index="4"><div class="inner" id="in3">
    <div class="ttl hand" style="top:250px">spend <span style="color:var(--blue)">₹1 lakh</span> a year</div>
    <div class="ttl hand" style="top:360px;font-size:70px;color:var(--mut)">on 18% GST items</div>
    {img("st-wallet", "s3_027", 110, 520, 280)}
    {img("st-fly", "s4_024", 420, 540, 360)}
    <div class="big" id="b15" style="top:840px;font-size:190px;color:var(--red)">≈ ₹15,254</div>
    <div class="ttl hand" id="b15l" style="top:1060px;font-size:76px">goes to GST</div>
  </div></section>

  <section class="scene clip" id="sc4" data-start="{SC[4][0]}" data-duration="{SC[4][1] - SC[4][0] + 0.3:.2f}" data-track-index="5"><div class="inner" id="in4">
    <div class="ttl hand" style="top:250px">some <span style="color:var(--green)">relief</span> ✨</div>
    <div class="note" style="top:365px;font-size:34px">GST 2.0 · since 22 Sep 2025</div>
    <div style="position:absolute;left:110px;right:60px;top:470px">
      <div class="ck hand" id="ck0"><svg viewBox="0 0 100 100"><path id="bx0" d="M8 10 L92 6 L95 92 L6 95 Z" /><path class="tick" id="tk0" d="M18 52 L42 78 L90 8" /></svg>milk</div>
      <div class="ck hand" id="ck1"><svg viewBox="0 0 100 100"><path id="bx1" d="M6 8 L93 9 L92 94 L9 92 Z" /><path class="tick" id="tk1" d="M18 52 L42 78 L90 8" /></svg>paneer</div>
      <div class="ck hand" id="ck2"><svg viewBox="0 0 100 100"><path id="bx2" d="M9 7 L94 10 L91 93 L7 94 Z" /><path class="tick" id="tk2" d="M18 52 L42 78 L90 8" /></svg>health insurance</div>
    </div>
    <div class="pill" id="zero" style="left:600px;top:500px;background:var(--green);font-size:110px;transform:rotate(-8deg)">0% GST</div>
    <div class="note" style="top:1110px">Soap, shampoo, toothpaste: now 5%</div>
  </div></section>

  <section class="scene clip" id="sc5" data-start="{SC[5][0]}" data-duration="{DUR - SC[5][0]:.2f}" data-track-index="6"><div class="inner" id="in5">
    {img("st-cloud", "s0_007", 200, 230, 680)}
    {img("st-idea", "s0_008", 40, 760, 330)}
    <div class="ttl hand" id="fair" style="top:770px;left:360px;right:260px;font-size:90px">is it <span style="color:var(--red)">fair?</span></div>
    <div class="pill" id="cta" style="left:380px;top:930px;background:var(--blue)">COMMENT "TAX"</div>
  </div></section>

  <section class="clip" id="caps" data-start="0" data-duration="{DUR}" data-track-index="7" data-track-kind="captions" style="position:absolute;inset:0;z-index:40">
    {caps_html}
  </section>
  <div id="disc">New regime FY 2026-27 · GST incl. in price · Education only, not tax advice</div>
  <div id="vignette"></div>
</div>
<script>
const T = {json.dumps(T)};
const CAPS = {json.dumps(caps)};
const SC = {json.dumps(SC)};
const EIN = "expo.out", EOUT = "expo.in";
const tl = gsap.timeline({{ paused: true }});
window.hwOnUpdate = function (tl, fn) {{ if (!tl.__hwRenders) {{ tl.__hwRenders = []; tl.eventCallback("onUpdate", function () {{ for (var i = 0; i < tl.__hwRenders.length; i++) tl.__hwRenders[i](); }}); }} tl.__hwRenders.push(fn); fn(); }};
window.hwHash = function (n, seed) {{ var x = Math.sin(n * 127.1 + (seed || 1) * 311.7) * 43758.5453; return (x - Math.floor(x)) * 2 - 1; }};
window.hwBoil = function (tl, target, opts) {{ opts = opts || {{}}; var amp = opts.amp ?? 1.6, rot = opts.rot ?? 0.5, fps = 30, drop = opts.frameDrop || 3, seed = opts.seed || 1; var els = gsap.utils.toArray(target);
  window.hwOnUpdate(tl, function () {{ var step = Math.floor((tl.time() * fps) / drop); for (var i = 0; i < els.length; i++) gsap.set(els[i], {{ x: hwHash(step*3+i*97, seed)*amp, y: hwHash(step*3+1+i*97, seed)*amp, rotation: hwHash(step*3+2+i*97, seed)*rot }}); }}); }};
const draw = (sel, at, dur) => {{ const p = document.querySelector(sel); const L = p.getTotalLength(); tl.set(p, {{opacity:0}}, 0); tl.set(p, {{opacity:1}}, at); tl.fromTo(p, {{strokeDasharray:L, strokeDashoffset:L}}, {{strokeDashoffset:0, duration:dur||0.6, ease:"power2.inOut"}}, at); }};
const pop = (sel, at, r) => tl.fromTo(sel, {{scale:0.4, opacity:0, rotation:r||0}}, {{scale:1, opacity:1, rotation:0, duration:0.45, ease:"back.out(2)"}}, at);
const up = (sel, at) => tl.fromTo(sel, {{opacity:0, y:24}}, {{opacity:1, y:0, duration:0.4, ease:EIN}}, at);

SC.forEach(([a,b],i) => {{ const id = "#in"+i;
  if (i > 0) tl.fromTo(id, {{yPercent:6, opacity:0}}, {{yPercent:0, opacity:1, duration:0.4, ease:EIN}}, a);
  if (i < SC.length-1) tl.to(id, {{yPercent:-5, opacity:0, duration:0.3, ease:EOUT}}, b - 0.05); }});

// HOOK: EARN -> TAX visible from frame 0; SPEND -> TAX + AGAIN land on "GST again"
tl.fromTo("#st-think", {{opacity:0, x:60}}, {{opacity:1, x:0, duration:0.5, ease:EIN}}, 0.1);
up("#r2", T.gst0 - 0.6);
pop("#again", T.gst0 - 0.05, -14); draw("#ul0", T.gst0 + 0.3, 0.4);
pop("#st-why", T.gst0 + 0.6, 8);
if (document.querySelector("#st-q")) pop("#st-q", 1.2, -10);

// SALARY -> TAX -> TAKE-HOME
pop("#st-lpa", SC[1][0] + 0.2, -6); pop("#st-salary", T.lakh15 - 0.2, -5);
draw("#a1", T.tax - 2.2, 0.5); draw("#a1h", T.tax - 1.7, 0.2);
pop("#st-tax", T.tax - 0.25, 6); up("#n-regime", T.tax - 3.0);
draw("#a2", T.take - 0.9, 0.5); draw("#a2h", T.take - 0.4, 0.2);
pop("#st-take", T.take - 0.15, -4);
tl.fromTo("#hl-take", {{scaleX:0}}, {{scaleX:1, duration:0.45, ease:"power2.out"}}, T.take + 1.2);
up("#n-take", T.take + 0.5);

// TV + GST
pop("#st-cart", T.tv - 0.6, -8); pop("#st-tv", T.tv - 0.15, 4); pop("#st-price", T.price - 0.1, -10);
pop("#st-gst18", T.inside - 1.2, 12); pop("#st-4576", T.gst - 0.1, -8);
pop("#st-shock", T.gst + 0.3, 6); up("#f1", T.gst + 0.9);

// ₹1 LAKH
up("#st-wallet", SC[3][0] + 0.3);
tl.fromTo("#st-fly", {{opacity:0, x:-80, y:30}}, {{opacity:1, x:0, y:0, duration:0.8, ease:EIN}}, T.lakh1);
tl.to("#st-fly", {{x:40, y:-20, duration:2.5, ease:"sine.inOut"}}, T.lakh1 + 0.8);
pop("#b15", T.gst15 - 0.15, -4); up("#b15l", T.gst15 + 0.5);

// RELIEF
["bx0","bx1","bx2"].forEach((b,k) => draw("#"+b, SC[4][0] + 0.3 + k*0.15, 0.4));
draw("#tk0", T.zero - 0.1, 0.35); draw("#tk1", T.zero + 0.4, 0.35); draw("#tk2", T.zero + 1.0, 0.35);
pop("#zero", T.zero2 - 0.15, -20);

// CTA
pop("#st-cloud", T.earn - 0.25, -4);
tl.fromTo("#st-idea", {{y:100, opacity:0}}, {{y:0, opacity:1, duration:0.5, ease:EIN}}, T.spend);
pop("#fair", T.fair - 0.15, 0);
pop("#cta", T.comment - 0.2, -4);
tl.to("#cta", {{scale:1.06, duration:0.4, yoyo:true, repeat:5, ease:"sine.inOut"}}, T.comment + 0.4);

hwBoil(tl, ".stk", {{amp:1.3, rot:0.5}});

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
