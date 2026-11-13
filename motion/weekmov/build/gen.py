"""Doodle leaderboard reel: top 10 weekly gainers OR losers in Nifty 100 / Midcap 150 / Smallcap 250.
usage: python3 gen.py <gain|loss>   (reads build/<mode>.json + build/t_<mode>.json, writes ../index.html)"""
import json, re, os, sys
H = os.path.dirname(os.path.abspath(__file__))
MODE = sys.argv[1]
D = json.load(open(os.path.join(H, f'{MODE}.json')))
T = json.load(open(os.path.join(H, f't_{MODE}.json')))
DUR = T['DUR']; S = T['STARTS']
GAIN = MODE == 'gain'
COL = '#1E8E4E' if GAIN else '#D93A2B'
SPOKEN = D['spoken']           # caption text per VO line
G = D['groups']                # 3 groups: label, sub, rows[{name, pct}]
# scenes: 0 hook | 1..3 groups | 4 context | 5 CTA  (VO line i == scene i)
SC = [(S[i], S[i + 1] if i + 1 < len(S) else DUR) for i in range(len(S))]

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
def fmt(p): return f"{'+' if p > 0 else '−' if p < 0 else ''}{abs(p):.1f}%"

def board(gi, g):
    mx = max(abs(r['pct']) for r in g['rows'])
    rows = []
    for k, r in enumerate(g['rows']):
        w = 40 + 330 * abs(r['pct']) / mx
        top = 395 + k * 80
        rows.append(f'''<div class="row" id="r{gi}_{k}" style="top:{top}px"><div class="rk">{k + 1}</div><div class="nm">{esc(r['name'])}</div>
<div class="bar" id="b{gi}_{k}" style="width:{w:.0f}px"></div><div class="pc">{fmt(r['pct'])}</div></div>''')
    return '\n'.join(rows)

top = D['top']
scenes = []
for gi, g in enumerate(G):
    i = gi + 1
    scenes.append(f'''  <section class="scene clip" id="sc{i}" data-start="{SC[i][0]:.2f}" data-duration="{SC[i][1] - SC[i][0] + 0.3:.2f}" data-track-index="{i + 1}"><div class="inner" id="in{i}">
    <div class="hdr"><span class="cap-t hand">{esc(g['label'])}</span><span class="sub">{esc(g['sub'])}</span></div>
    <svg class="ov" style="left:90px;top:330px;width:900px;height:30px" viewBox="0 0 900 30"><path id="ul{i}" d="M5 18 C 250 6, 600 28, 895 10" style="stroke:{COL}" /></svg>
    {board(gi, g)}
  </div></section>''')
scenes = '\n'.join(scenes)
caps_html = '\n'.join(f'<div class="cap" id="cap{k}"><span>{esc(t)}</span></div>' for k, (_, _, t) in enumerate(caps))
ctx = D['context']

html = f'''<!doctype html>
<html lang="en" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<title>{esc(D['title'])}</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
@font-face {{ font-family:"Caveat"; src:url("assets/fonts/Caveat-700-latin.woff2") format("woff2"); font-weight:700; }}
@font-face {{ font-family:"Anton"; src:url("assets/fonts/anton-latin-400-normal.woff") format("woff"); }}
@font-face {{ font-family:"Poppins"; src:url("assets/fonts/Poppins-Bold.ttf") format("truetype"); font-weight:700; }}
@font-face {{ font-family:"Oswald"; src:url("assets/fonts/oswald-latin-500-normal.woff") format("woff"); font-weight:500; }}
:root {{ --paper:#FBF8F0; --ink:#1B1B1F; --col:{COL}; --hl:#FFE45C; --mut:#5B5B66; }}
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
#kw span {{ display:inline-block; background:var(--ink); color:#fff; font-family:"Oswald",sans-serif; font-size:40px; letter-spacing:2px; padding:10px 30px; border-radius:999px; }}
svg.ov {{ position:absolute; overflow:visible; }}
path {{ fill:none; stroke:var(--ink); stroke-width:7; stroke-linecap:round; stroke-linejoin:round; }}
#topbox {{ position:absolute; left:90px; right:90px; top:430px; height:470px; }}
#topbox svg {{ position:absolute; inset:0; width:100%; height:100%; overflow:visible; }}
#topname {{ position:absolute; left:0; right:0; top:80px; text-align:center; font-family:"Anton",sans-serif; font-size:96px; line-height:1.05; }}
#toppct {{ position:absolute; left:0; right:0; top:215px; text-align:center; font-family:"Anton",sans-serif; font-size:170px; color:var(--col); line-height:1; }}
#topsub {{ position:absolute; left:0; right:0; top:400px; text-align:center; font-family:"Oswald",sans-serif; font-size:34px; color:var(--mut); }}
#hook2 {{ position:absolute; left:60px; right:60px; top:960px; text-align:center; font-size:76px; line-height:1.1; }}
.hdr {{ position:absolute; left:90px; right:90px; top:225px; display:flex; align-items:baseline; gap:24px; }}
.cap-t {{ font-size:104px; line-height:1; color:var(--col); }}
.hdr .sub {{ font-family:"Oswald",sans-serif; font-size:34px; color:var(--mut); }}
.row {{ position:absolute; left:70px; right:70px; height:70px; display:flex; align-items:center; }}
.rk {{ width:62px; height:62px; flex:none; border:4px solid var(--ink); border-radius:50%; display:flex; align-items:center; justify-content:center; font-family:"Anton",sans-serif; font-size:34px; background:#fff; }}
.nm {{ width:400px; flex:none; padding-left:18px; font-family:"Poppins",sans-serif; font-weight:700; font-size:33px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
.bar {{ height:40px; background:var(--col); border:3px solid var(--ink); border-radius:8px; transform-origin:left center; flex:none; }}
.pc {{ padding-left:14px; font-family:"Anton",sans-serif; font-size:44px; color:var(--col); white-space:nowrap; }}
.row.hot .nm {{ background:linear-gradient(transparent 55%, rgba(255,228,92,.85) 55%); }}
#ctx {{ position:absolute; left:80px; right:80px; top:300px; }}
.ix {{ position:relative; height:150px; display:flex; align-items:center; justify-content:space-between; border-bottom:4px dashed rgba(27,27,31,.25); }}
.ix .l {{ font-size:78px; }}
.ix .v {{ font-family:"Anton",sans-serif; font-size:84px; }}
#ctxline {{ position:absolute; left:70px; right:70px; top:860px; text-align:center; font-size:72px; line-height:1.1; }}
.host {{ position:absolute; height:auto; }}
.pill {{ position:absolute; display:inline-block; border-radius:22px; padding:12px 34px; font-family:"Anton",sans-serif; font-size:62px; color:#fff; border:5px solid var(--ink); box-shadow:8px 8px 0 var(--ink); white-space:nowrap; }}
.cap {{ position:absolute; left:0; right:0; top:1215px; text-align:center; opacity:0; }}
.cap span {{ display:inline-block; max-width:920px; background:#fff; border:5px solid var(--ink); border-radius:18px; box-shadow:6px 8px 0 var(--ink); padding:10px 34px; font-family:"Poppins",sans-serif; font-weight:700; font-size:44px; line-height:1.25; }}
#disc {{ position:absolute; left:0; right:0; top:1305px; text-align:center; font-family:"Oswald",sans-serif; font-size:28px; color:rgb(84,84,96); z-index:30; }}
#vignette {{ position:absolute; inset:0; pointer-events:none; z-index:99; background:radial-gradient(ellipse at center, transparent 60%, rgba(27,27,31,.10) 100%); }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{DUR:.2f}" data-fps="30">
  <div id="paper"></div>
  <div class="handle">@moneyincloud</div>
  <audio id="vo" src="assets/vo_mix.wav" data-start="0" data-duration="{DUR:.2f}" data-track-index="9" data-volume="1"></audio>

  <section class="scene clip" id="sc0" data-start="0" data-duration="{SC[0][1] + 0.3:.2f}" data-track-index="1"><div class="inner" id="in0">
    <div id="kw"><span>{esc(D['kw'])}</span></div>
    <div class="ttl hand" style="top:300px">{esc(D['hook_ttl'])}</div>
    <div id="topbox"><svg viewBox="0 0 900 470"><path id="tb" d="" style="stroke:var(--col)" /></svg>
      <div id="topname">{esc(top['name'])}</div><div id="toppct">{fmt(top['pct'])}</div><div id="topsub">{esc(top['sub'])}</div></div>
    <div id="hook2" class="hand">{D['hook2']}</div>
  </div></section>

{scenes}

  <section class="scene clip" id="sc4" data-start="{SC[4][0]:.2f}" data-duration="{SC[4][1] - SC[4][0] + 0.3:.2f}" data-track-index="5"><div class="inner" id="in4">
    <div class="ttl hand" style="top:200px">meanwhile, the index…</div>
    <div id="ctx">
      {''.join(f'<div class="ix" id="ix{k}"><span class="l hand">{esc(a)}</span><span class="v" style="color:{"#1E8E4E" if b > 0 else "#D93A2B"}">{fmt(b)}</span></div>' for k, (a, b) in enumerate(ctx['rows']))}
    </div>
    <div id="ctxline" class="hand">{ctx['line']}</div>
  </div></section>

  <section class="scene clip" id="sc5" data-start="{SC[5][0]:.2f}" data-duration="{DUR - SC[5][0]:.2f}" data-track-index="6"><div class="inner" id="in5">
    <div class="ttl hand" style="top:280px">{D['cta_ttl']}</div>
    <img class="host" id="host" src="assets/img/s0_008.png" style="left:50px;top:560px;width:380px" />
    <div class="pill" id="cta1" style="left:440px;top:640px;background:var(--col)">COMMENT "{D['cta_kw']}"</div>
    <div class="pill" id="cta2" style="left:440px;top:790px;background:var(--hl);color:var(--ink);font-size:48px">FOLLOW FOR NEXT WEEK</div>
  </div></section>

  <section class="clip" id="caps" data-start="0" data-duration="{DUR:.2f}" data-track-index="7" data-track-kind="captions" style="position:absolute;inset:0;z-index:40">
    {caps_html}
  </section>
  <div id="disc">{esc(D['disc'])}</div>
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
window.hwRect = function (w, h, seed) {{ const j = k => hwHash(k, seed) * 6; return `M${{8+j(1)}} ${{8+j(2)}} L${{w-8+j(3)}} ${{6+j(4)}} L${{w-6+j(5)}} ${{h-8+j(6)}} L${{6+j(7)}} ${{h-6+j(8)}} Z`; }};
const draw = (sel, at, dur) => {{ const p = document.querySelector(sel); const L = p.getTotalLength(); tl.set(p, {{opacity:0}}, 0); tl.set(p, {{opacity:1}}, at); tl.fromTo(p, {{strokeDasharray:L, strokeDashoffset:L}}, {{strokeDashoffset:0, duration:dur||0.6, ease:"power2.inOut"}}, at); }};
const pop = (sel, at, r) => tl.fromTo(sel, {{scale:0.4, opacity:0, rotation:r||0}}, {{scale:1, opacity:1, rotation:0, duration:0.45, ease:"back.out(2)"}}, at);
const up = (sel, at) => tl.fromTo(sel, {{opacity:0, y:24}}, {{opacity:1, y:0, duration:0.4, ease:EIN}}, at);
document.getElementById("tb").setAttribute("d", hwRect(900, 470, 5));

SC.forEach(([a,b],i) => {{ const id = "#in"+i;
  if (i > 0) tl.fromTo(id, {{yPercent:6, opacity:0}}, {{yPercent:0, opacity:1, duration:0.4, ease:EIN}}, a);
  if (i < SC.length-1) tl.to(id, {{yPercent:-5, opacity:0, duration:0.3, ease:EOUT}}, b - 0.05); }});

// HOOK: keyword + top stock visible at frame 0
draw("#tb", 0.05, 0.8);
tl.fromTo("#toppct", {{scale:0.6}}, {{scale:1, duration:0.5, ease:"back.out(2.5)"}}, T.toppct - 0.1);
up("#hook2", T.hook2);

// BOARDS: rows cascade in, bars grow, spoken top 3 get highlighted
[1,2,3].forEach(i => {{ const gi = i-1, a = SC[i][0];
  draw("#ul"+i, a + 0.2, 0.5);
  for (let k = 0; k < 10; k++) {{
    tl.fromTo("#r"+gi+"_"+k, {{opacity:0, x:-40}}, {{opacity:1, x:0, duration:0.3, ease:EIN}}, a + 0.35 + k*0.12);
    tl.fromTo("#b"+gi+"_"+k, {{scaleX:0}}, {{scaleX:1, duration:0.5, ease:"power3.out"}}, a + 0.45 + k*0.12);
  }}
  T.hot[gi].forEach((ts, k) => {{ tl.set("#r"+gi+"_"+k, {{className:"row hot"}}, ts - 0.05);
    tl.fromTo("#r"+gi+"_"+k+" .rk", {{scale:1.5}}, {{scale:1, duration:0.35, ease:"back.out(2)"}}, ts - 0.05); }});
}});

// CONTEXT
document.querySelectorAll(".ix").forEach((el,k) => up(el, SC[4][0] + 0.3 + k*0.35));
up("#ctxline", T.ctxline);

// CTA
tl.fromTo("#host", {{y:100, opacity:0}}, {{y:0, opacity:1, duration:0.5, ease:EIN}}, SC[5][0] + 0.2);
pop("#cta1", T.comment - 0.2, -4); pop("#cta2", T.follow - 0.1, 3);
hwBoil(tl, "#host,#topbox", {{amp:1.2, rot:0.4}});

CAPS.forEach(([st, en, txt], k) => {{ const g = "#cap"+k;
  tl.fromTo(g, {{opacity:0, y:14}}, {{opacity:1, y:0, duration:0.14, ease:"power2.out"}}, Math.max(0.15, st - 0.05));
  tl.to(g, {{opacity:0, duration:0.1}}, en - 0.1); tl.set(g, {{opacity:0, visibility:"hidden"}}, en); }});
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''
open(os.path.join(H, '..', f'index.html'), 'w').write(html)
print('caps', len(caps), 'dur', round(DUR, 1))
