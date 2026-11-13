"""Generate index.html for the HyperFrames dividend reel (Tamil audio, English text)."""
import json, re, os
T = {"VO": [0.15, 5.46, 13.68, 19.15, 26.93, 34.88, 39.98], "DURS": [4.89, 7.8, 5.05, 7.36, 7.53, 4.68, 4.7],
     "STARTS": [0.0, 5.26, 13.48, 18.95, 26.73, 34.68, 39.78], "DUR": 46.2,
     "rows": [5.26, 13.48, 16.25, 18.95, 21.02, 23.82], "sixty": 11.25, "catch": 27.48, "taxed": 30.63, "yield": 31.38,
     "fell": 32.88, "guar": 35.84, "cut": 38.73, "comment": 42.66, "follow": 43.73}
SCRIPT = ['Nobody tells you these six stocks pay you every year.', 'Coal India, about 6.6%. Invest ₹1 lakh, get ₹6,600 a year.',
          'Wipro, 5.9%. ONGC, 5.7%.', 'Indian Oil, 5.5%. BPCL, 5.4%. ITC, 5.1%.',
          "But there's a catch. Dividends are taxed at your slab rate. A high yield can mean the price fell.",
          "Dividends aren't guaranteed. A company can cut them any year.", 'Which stock do you hold? Comment DIVIDEND and follow!']
ROWS = [('Coal India', 6.6), ('Wipro', 5.9), ('ONGC', 5.7), ('Indian Oil', 5.5), ('BPCL', 5.4), ('ITC', 5.1)]
DUR = T['DUR']; S = T['STARTS']
SC = [(0, S[1]), (S[1], S[4]), (S[4], S[5]), (S[5], S[6]), (S[6], DUR)]  # scene windows

# ---- caption groups: split each line into groups of <=4 words, ending at punctuation; time by char weight
groups = []
for i, line in enumerate(SCRIPT):
    words = line.split(); cur = []; gs = []
    for w in words:
        cur.append(w)
        if len(cur) >= 4 or re.search(r'[.,?!]$', w): gs.append(cur); cur = []
    if cur: gs.append(cur)
    tot = sum(len(' '.join(g)) for g in gs); t0 = T['VO'][i]; d = T['DURS'][i]; acc = 0
    for g in gs:
        txt = ' '.join(g); st = t0 + d * acc / tot; acc += len(txt); en = t0 + d * acc / tot
        groups.append((round(st, 2), round(en, 2), txt))
# extend each group to the next one's start (no flicker), cap at line end + 0.3
caps = []
for k, (st, en, txt) in enumerate(groups):
    nxt = groups[k + 1][0] if k + 1 < len(groups) else DUR - 0.2
    caps.append((st, round(min(max(en, nxt - 0.02), en + 0.6), 2), txt))

def wm(words, cls):
    # reel-director: each word in its own overflow mask, slides up from 115% with a 7deg tilt
    out = []
    for w in words:
        inner = f'<i>{w[1:-1]}</i>' if w.startswith('*') else w
        out.append(f'<span class="wm"><span class="w {cls}">{inner}</span></span>')
    return ' '.join(out)

def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;')

def rows_html(prefix, small=False):
    out = []
    for k, (nm, y) in enumerate(ROWS):
        out.append(f'''<div class="row{' sm' if small else ''}" id="{prefix}-r{k}"><svg class="hl" viewBox="0 0 100 20" preserveAspectRatio="none"><path id="{prefix}-hl{k}" d="M1 11 C 25 9, 60 13, 99 10" /></svg>
<span class="nm">{k + 1}. {esc(nm.upper())}</span><span class="yl">{y:.1f}%</span><span class="rs">₹{int(y * 1000):,}</span></div>''')
    return '\n'.join(out)

coins = '\n'.join(f'<div class="coin" data-layout-ignore id="coin{k}" style="left:{60 + (k * 149) % 940}px;width:{44 + (k % 3) * 12}px;height:{44 + (k % 3) * 12}px;font-size:{26 + (k % 3) * 7}px">₹</div>' for k in range(14))
caps_html = '\n'.join(f'<div class="cap" id="cap{k}"><span>{esc(t)}</span></div>' for k, (_, _, t) in enumerate(caps))

html = f'''<!doctype html>
<html lang="en" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<title>Dividend cheat sheet (Tamil audio)</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
@font-face {{ font-family: "Anton"; src: url("assets/fonts/anton-latin-400-normal.woff") format("woff"); }}
@font-face {{ font-family: "Poppins"; src: url("assets/fonts/Poppins-Bold.ttf") format("truetype"); font-weight: 700; }}
@font-face {{ font-family: "Playfair"; src: url("assets/fonts/playfair-display-latin-700-italic.woff") format("woff"); font-style: italic; font-weight: 700; }}
@font-face {{ font-family: "Oswald"; src: url("assets/fonts/oswald-latin-500-normal.woff") format("woff"); font-weight: 500; }}
:root {{ --bg:#F4FCF6; --ink:#10221A; --green:#16965A; --mut:#5A6E64; --gold:#E6AF28; --red:#D63C32; --hl:#FFE978; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:var(--bg); }}
#root {{ position:relative; width:100%; height:100%; overflow:hidden; font-family:"Anton","Poppins",sans-serif; color:var(--ink); }}
#bg {{ position:absolute; inset:0; background: repeating-linear-gradient(45deg, rgba(200,236,214,.55) 0 18px, transparent 18px 70px); }}
.blob {{ position:absolute; border-radius:50%; filter:blur(70px); opacity:.55; }}
.scene {{ position:absolute; inset:0; }}
.inner {{ position:absolute; inset:0; }}
.title {{ position:absolute; left:0; right:0; top:205px; text-align:center; font-size:92px; line-height:1.05; }}
.title i {{ font-family:"Playfair",serif; color:var(--green); font-weight:700; }}
.mask {{ overflow:hidden; display:block; padding:0 0 10px; }}
.wm {{ display:inline-block; overflow:hidden; vertical-align:top; padding:0 4px 12px; margin-bottom:-12px; }}
.w {{ display:inline-block; }}
#vignette {{ position:absolute; inset:0; pointer-events:none; z-index:99; background:radial-gradient(ellipse at center, transparent 58%, rgba(16,34,26,.13) 100%); }}
#kw {{ position:absolute; left:0; right:0; top:250px; text-align:center; }}
#kw span {{ display:inline-block; background:var(--ink); color:#fff; font-family:"Oswald",sans-serif; font-size:40px; letter-spacing:2px; padding:10px 30px; border-radius:999px; }}
.mask > span {{ display:inline-block; }}
.handle {{ position:absolute; left:40px; top:120px; font-family:"Oswald",sans-serif; font-size:30px; color:#6E8578; z-index:50; }}
.coin {{ position:absolute; top:0; border-radius:50%; background:var(--gold); border:4px solid #A87A0C; color:#7A5200; display:flex; align-items:center; justify-content:center; font-family:"Poppins",sans-serif; font-weight:700; }}
#hook-lakh {{ position:absolute; left:0; right:0; top:350px; text-align:center; font-size:230px; line-height:1; }}
#hook-l1 {{ position:absolute; left:0; right:0; top:640px; text-align:center; font-size:88px; }}
#hook-l1 i {{ font-family:"Playfair",serif; color:var(--green); }}
#hook-l2 {{ position:absolute; left:0; right:0; top:770px; text-align:center; font-family:"Playfair",serif; font-style:italic; font-size:120px; color:var(--green); }}
.table {{ position:absolute; left:60px; right:60px; top:360px; }}
.thead {{ display:flex; font-family:"Oswald",sans-serif; font-size:30px; color:var(--mut); padding:0 30px 10px; }}
.thead span:nth-child(1) {{ flex:1; }} .thead span:nth-child(2) {{ width:200px; text-align:right; }} .thead span:nth-child(3) {{ width:250px; text-align:right; }}
.row {{ position:relative; display:flex; align-items:center; height:104px; margin-bottom:14px; padding:0 30px; background:#fff; border:2px solid #CDEBD7; border-radius:22px; box-shadow:0 8px 18px rgba(16,34,26,.08); font-size:60px; }}
.row .hl {{ position:absolute; left:10px; top:10px; width:calc(100% - 20px); height:calc(100% - 20px); }}
.row .hl path {{ fill:none; stroke:var(--hl); stroke-width:16; stroke-linecap:round; }}
.row span {{ position:relative; }}
.row .nm {{ flex:1; }} .row .yl {{ width:200px; text-align:right; color:var(--green); }} .row .rs {{ width:250px; text-align:right; }}
.row.sm .hl {{ display:none; }}
.row.sm {{ height:80px; font-size:46px; margin-bottom:10px; }}
#callout {{ position:absolute; left:0; right:0; top:700px; text-align:center; }}
#callout .big {{ font-size:128px; color:var(--green); display:block; }}
#callout .sub {{ font-family:"Playfair",serif; font-style:italic; font-size:52px; color:var(--mut); display:block; margin-top:6px; }}
.card {{ position:absolute; left:80px; right:80px; background:#fff; border-radius:26px; border-left:16px solid var(--red); box-shadow:0 10px 24px rgba(16,34,26,.12); padding:26px 34px; }}
.card b {{ display:block; font-weight:400; font-size:64px; }}
.card small {{ display:block; font-family:"Oswald",sans-serif; font-size:34px; color:var(--mut); margin-top:6px; }}
#formula {{ position:absolute; left:0; right:0; top:585px; text-align:center; font-size:66px; }}
.bar {{ position:absolute; bottom:0; width:170px; border-radius:18px 18px 0 0; }}
#bars {{ position:absolute; left:0; right:0; top:770px; height:300px; }}
#bar-price {{ left:270px; height:270px; background:#9AA59F; }}
#bar-yield {{ left:640px; height:120px; background:var(--green); }}
.blab {{ position:absolute; top:1080px; width:170px; text-align:center; font-size:48px; }}
.tag {{ position:absolute; width:260px; text-align:center; font-size:42px; }}
#stamp {{ position:absolute; left:0; right:0; top:250px; text-align:center; }}
#stamp span {{ display:inline-block; background:var(--red); color:#fff; font-size:92px; padding:14px 46px; border-radius:22px; }}
.host {{ position:absolute; }}
.pill {{ position:absolute; display:inline-block; border-radius:22px; padding:14px 34px; font-size:56px; color:#fff; border:5px solid var(--ink); box-shadow:8px 8px 0 var(--ink); white-space:nowrap; }}
#cta-comment {{ left:430px; top:945px; background:var(--green); }}
#cta-follow {{ left:430px; top:1055px; background:#FFD43B; color:var(--ink); }}
.cap {{ position:absolute; left:0; right:0; top:1165px; text-align:center; opacity:0; }}
.cap span {{ display:inline-block; max-width:900px; background:#fff; border:6px solid var(--ink); box-shadow:0 10px 0 var(--ink); border-radius:40px; padding:16px 40px; font-family:"Poppins",sans-serif; font-weight:700; font-size:46px; line-height:1.25; color:var(--ink); }}
#disc {{ position:absolute; left:0; right:0; top:1300px; text-align:center; font-family:"Oswald",sans-serif; font-size:28px; color:rgb(84,100,91); z-index:30; }}
.srcline {{ position:absolute; left:40px; right:40px; top:1112px; text-align:center; font-family:"Oswald",sans-serif; font-size:28px; color:rgb(84,100,91); }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{DUR}" data-fps="30">
  <div id="bg"></div>
  <div class="blob" id="blob0" style="left:-120px;top:180px;width:520px;height:520px;background:#96E6B4"></div>
  <div class="blob" id="blob1" style="left:640px;top:760px;width:420px;height:420px;background:#FFDC82"></div>
  <div class="blob" id="blob2" style="left:560px;top:1460px;width:600px;height:600px;background:#8CDCC8"></div>
  <div class="blob" id="blob3" style="left:40px;top:1200px;width:360px;height:360px;background:#C8EBA0"></div>
  <div class="handle">@moneyincloud</div>
  <audio id="vo" src="assets/vo_mix.wav" data-start="0" data-duration="{DUR}" data-track-index="9" data-volume="1"></audio>

  <section class="scene clip" id="sc0" data-start="0" data-duration="{SC[0][1] + 0.3:.2f}" data-track-index="1"><div class="inner" id="in0">
    {coins}
    <div id="kw"><span id="kw-s">HIGHEST DIVIDEND PAYING STOCKS · INDIA 2026</span></div>
    <div id="hook-lakh">₹1 LAKH</div>
    <div id="hook-l1">{wm(["6","stocks","that","*pay*","you"],"wh1")}</div>
    <div id="hook-l2">{wm(["every","year"],"wh2")}</div>
  </div></section>

  <section class="scene clip" id="sc1" data-start="{SC[1][0]}" data-duration="{SC[1][1] - SC[1][0] + 0.3:.2f}" data-track-index="2"><div class="inner" id="in1">
    <div class="title">{wm(["Dividend","*cheat*","sheet"],"wt1")}</div>
    <div class="table" id="tb1"><div class="thead"><span>STOCK</span><span>YIELD</span><span>₹1 LAKH TO ₹/YEAR</span></div>
    {rows_html('a')}
    </div>
    <div class="srcline">Yields: Equitymaster, 06 Nov 2026 · ₹/year = yield × ₹1 lakh, before tax</div>
    <div id="callout"><span class="big" id="co-big">₹6,600 a year</span><span class="sub" id="co-sub">from ₹1 lakh in Coal India</span></div>
  </div></section>

  <section class="scene clip" id="sc2" data-start="{SC[2][0]}" data-duration="{SC[2][1] - SC[2][0] + 0.3:.2f}" data-track-index="3"><div class="inner" id="in2">
    <div class="title">{wm(["The","*catch*"],"wt2")}</div>
    <div class="card" id="card-tax" style="top:380px"><b>TAXED AT YOUR SLAB</b><small>+10% TDS if one company pays you over ₹10,000 a year</small></div>
    <div id="formula">YIELD = DIVIDEND ÷ PRICE</div>
    <div id="bars"><div class="bar" id="bar-price"></div><div class="bar" id="bar-yield"></div>
      <div class="tag" id="tag-price" style="left:225px;top:-60px;color:var(--red)">PRICE FALLS</div>
      <div class="tag" id="tag-yield" style="left:820px;top:20px;width:230px;text-align:left;color:var(--green)">YIELD LOOKS BIG</div></div>
    <div class="blab" id="lab-price" style="left:270px">PRICE</div><div class="blab" id="lab-yield" style="left:640px">YIELD</div>
  </div></section>

  <section class="scene clip" id="sc3" data-start="{SC[3][0]}" data-duration="{SC[3][1] - SC[3][0] + 0.3:.2f}" data-track-index="4"><div class="inner" id="in3">
    <div id="stamp"><span id="stamp-s">NOT GUARANTEED</span></div>
    <img class="host" id="host-shock" src="assets/img/p02.png" style="left:300px;top:390px;width:480px" />
    <div class="card" id="card-cut" style="top:930px"><b>PAYOUTS CAN BE CUT</b><small>past dividends are not future dividends</small></div>
  </div></section>

  <section class="scene clip" id="sc4" data-start="{SC[4][0]}" data-duration="{DUR - SC[4][0]:.2f}" data-track-index="5"><div class="inner" id="in4">
    <div class="title" style="top:200px;font-size:70px;color:var(--green)">{wm(["SAVE","THIS","CHEAT","SHEET"],"wt4")}</div>
    <div class="table" id="tb4" style="top:310px"><div class="thead"><span>STOCK</span><span>YIELD</span><span>₹1 LAKH TO ₹/YEAR</span></div>
    {rows_html('b', small=True)}
    </div>
    <img class="host" id="host-wave" src="assets/img/p31.png" style="left:50px;top:905px;width:330px" />
    <div class="pill" id="cta-comment">COMMENT "DIVIDEND"</div>
    <div class="pill" id="cta-follow">FOLLOW @moneyincloud</div>
  </div></section>

  <section class="clip" id="caps" data-start="0" data-duration="{DUR}" data-track-index="6" data-track-kind="captions" style="position:absolute;inset:0;z-index:40">
    {caps_html}
  </section>
  <div id="disc">Not a buy/sell call · Education only · I may hold some of the stocks named</div>

  <div id="vignette"></div>
  <!-- grain-overlay (registry component) -->
  <div id="grain-overlay" style="position:absolute;inset:0;pointer-events:none;z-index:100;opacity:.55"><div class="grain-texture"></div></div>
  <style>
    @keyframes hf-grain-noise {{ 0%,100%{{transform:translate(0,0)}} 10%{{transform:translate(-5%,-5%)}} 20%{{transform:translate(-10%,5%)}} 30%{{transform:translate(5%,-10%)}} 40%{{transform:translate(-5%,15%)}} 50%{{transform:translate(-10%,5%)}} 60%{{transform:translate(15%,0)}} 70%{{transform:translate(0,10%)}} 80%{{transform:translate(-15%,0)}} 90%{{transform:translate(10%,5%)}} }}
    #grain-overlay .grain-texture {{ position:absolute; top:-50%; left:-50%; width:200%; height:200%; background:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E"); opacity:.15; animation:hf-grain-noise .5s steps(1) infinite; }}
  </style>
</div>
<script>
const T = {json.dumps(T)};
const CAPS = {json.dumps(caps)};
const SC = {json.dumps(SC)};
const EIN = "expo.out", EOUT = "expo.in";
const words = (cls, at) => tl.fromTo("."+cls, {{yPercent:115, rotation:7}}, {{yPercent:0, rotation:0, duration:0.5, ease:EIN, stagger:0.13}}, at);
const tl = gsap.timeline({{ paused: true }});
const D = T.DUR;

// background drift (whole film)
[[0,60,40],[1,-50,60],[2,40,-50],[3,-40,40]].forEach(([k,dx,dy]) => {{
  tl.fromTo("#blob"+k, {{x:0,y:0}}, {{x:dx,y:dy,duration:D,ease:"sine.inOut"}}, 0);
}});

// scene enter/exit: next scene slides in over the old one
SC.forEach(([a,b],i) => {{
  if (i > 0) tl.fromTo("#in"+i, {{xPercent:22, opacity:0}}, {{xPercent:0, opacity:1, duration:0.45, ease:EIN}}, a);
  if (i < SC.length-1) tl.to("#in"+i, {{xPercent:-18, opacity:0, duration:0.4, ease:EOUT}}, b - 0.1);
}});

// HOOK: coins already falling on frame 0
for (let k = 0; k < 14; k++) {{
  const sp = 1.7 + (k % 4) * 0.35, ph = (k * 0.37) % 1;
  tl.fromTo("#coin"+k, {{y: -120 + ph * 1500, rotation: k*20}}, {{y: 1500, rotation: k*20 + 160, duration: sp * (1 - ph), ease:"none"}}, 0);
  let t = sp * (1 - ph);
  while (t < SC[0][1] + 0.3) {{ tl.fromTo("#coin"+k, {{y:-120}}, {{y:1500, duration: sp, ease:"none", immediateRender:false}}, t); t += sp; }}
}}
tl.fromTo("#hook-lakh", {{scale:1.0}}, {{scale:1.06, duration:4.8, ease:"sine.inOut"}}, 0);
words("wh1", 0.05);
words("wh2", 0.75);
tl.fromTo("#kw-s", {{scale:1}}, {{scale:1.04, duration:0.6, repeat:3, yoyo:true, ease:"sine.inOut"}}, 0.2);

// TABLE: rows slide in with a marker swipe
words("wt1", SC[1][0] + 0.15);
T.rows.forEach((tr, k) => {{
  tl.fromTo("#a-r"+k, {{x:220, opacity:0, filter:"blur(10px)"}}, {{x:0, opacity:1, filter:"blur(0px)", duration:0.5, ease:EIN}}, tr + 0.05);
  const p = document.getElementById("a-hl"+k); const L = p.getTotalLength();
  tl.fromTo(p, {{strokeDasharray:L, strokeDashoffset:L, opacity:1}}, {{strokeDashoffset:0, duration:0.45, ease:"power2.out"}}, tr + 0.25);
  tl.to(p, {{opacity:0, duration:0.4}}, tr + 1.9);
}});
tl.fromTo("#co-big", {{scale:0.6, opacity:0}}, {{scale:1, opacity:1, duration:0.5, ease:"back.out(2)"}}, T.sixty - 0.4);
tl.fromTo("#co-sub", {{y:20, opacity:0}}, {{y:0, opacity:1, duration:0.4, ease:EIN}}, T.sixty - 0.1);
tl.to("#callout", {{opacity:0, y:-30, duration:0.3, ease:EOUT}}, T.rows[1] - 0.35);
const ctr = {{v:0}}; const cb = document.getElementById("co-big");
tl.to(ctr, {{v:6600, duration:0.9, ease:"power2.out", onUpdate:() => {{ cb.textContent = "₹" + Math.round(ctr.v).toLocaleString("en-IN") + " a year"; }}}}, T.sixty - 0.4);

// CATCH
words("wt2", SC[2][0] + 0.15);
tl.fromTo("#card-tax", {{x:-220, opacity:0, filter:"blur(10px)"}}, {{x:0, opacity:1, filter:"blur(0px)", duration:0.5, ease:EIN}}, T.taxed - 0.4);
tl.fromTo("#formula", {{scale:0.8, opacity:0}}, {{scale:1, opacity:1, duration:0.45, ease:"back.out(1.7)"}}, T.yield - 0.3);
["#bar-price","#bar-yield","#lab-price","#lab-yield"].forEach(s => tl.fromTo(s, {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.4, ease:EIN}}, T.yield));
tl.to("#bar-price", {{height:150, duration:1.0, ease:"power3.inOut"}}, T.fell - 0.5);
tl.to("#bar-yield", {{height:270, duration:1.0, ease:"power3.inOut"}}, T.fell - 0.5);
tl.fromTo("#tag-price", {{opacity:0, y:125}}, {{opacity:1, y:120, duration:0.3}}, T.fell + 0.2);
tl.fromTo("#tag-yield", {{opacity:0, y:10}}, {{opacity:1, y:0, duration:0.3}}, T.fell + 0.2);

// NOT GUARANTEED
tl.fromTo("#host-shock", {{y:80, opacity:0}}, {{y:0, opacity:1, duration:0.5, ease:EIN}}, SC[3][0] + 0.1);
tl.fromTo("#stamp-s", {{scale:2.4, rotation:-14, opacity:0}}, {{scale:1, rotation:-5, opacity:1, duration:0.45, ease:"back.out(1.6)"}}, T.guar - 0.3);
tl.fromTo("#host-shock", {{x:0}}, {{x:10, duration:0.06, repeat:7, yoyo:true, ease:"none"}}, T.guar - 0.1);
tl.fromTo("#card-cut", {{x:-220, opacity:0, filter:"blur(10px)"}}, {{x:0, opacity:1, filter:"blur(0px)", duration:0.5, ease:EIN}}, T.guar + 0.6);

// END CARD
words("wt4", SC[4][0] + 0.15);
for (let k = 0; k < 6; k++) tl.fromTo("#b-r"+k, {{x:120, opacity:0}}, {{x:0, opacity:1, duration:0.4, ease:EIN}}, SC[4][0] + 0.3 + k*0.12);
tl.fromTo("#host-wave", {{y:120, opacity:0}}, {{y:0, opacity:1, duration:0.5, ease:EIN}}, SC[4][0] + 0.6);
tl.fromTo("#cta-comment", {{scale:0.4, opacity:0}}, {{scale:1, opacity:1, duration:0.45, ease:"back.out(2)"}}, T.comment - 0.2);
tl.fromTo("#cta-follow", {{scale:0.4, opacity:0}}, {{scale:1, opacity:1, duration:0.45, ease:"back.out(2)"}}, T.follow - 0.1);
tl.to("#cta-follow", {{scale:1.06, duration:0.5, repeat:3, yoyo:true, ease:"sine.inOut"}}, T.follow + 0.5);

// CAPTIONS: one group at a time, hard kill
CAPS.forEach(([st, en, txt], k) => {{
  const g = "#cap"+k;
  tl.fromTo(g, {{opacity:0, y:16}}, {{opacity:1, y:0, duration:0.14, ease:"power2.out"}}, Math.max(0.15, st - 0.05));
  tl.to(g, {{opacity:0, duration:0.1, ease:EOUT}}, en - 0.1);
  tl.set(g, {{opacity:0, visibility:"hidden"}}, en);
}});

window.__timelines["main"] = tl;
</script>
</body>
</html>
'''
open(os.path.join(os.path.dirname(__file__), '..', 'index.html'), 'w').write(html)
print('caption groups', len(caps))
