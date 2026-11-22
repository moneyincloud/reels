"""Assemble index.html for the tea -> SIP reel.  usage: python3 build.py"""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__))
from scenes import CAPTXT, BG, SCN, EXTRA_CSS, JS_SCENES
T = json.load(open(H + '/t.json'))
DUR = T['DUR']; S = T['STARTS']; V = T['VO']; DU = T['DURS']
caps = []
for i, line in enumerate(CAPTXT):
    gs, cur = [], []
    for w in line.split():
        cur.append(w)
        if len(cur) >= 4 or re.search(r'[.,?!:]$', w): gs.append(cur); cur = []
    if cur: gs.append(cur)
    tot = sum(len(' '.join(g)) for g in gs); acc = 0
    for g in gs:
        txt = ' '.join(g); st = V[i] + DU[i] * acc / tot; acc += len(txt); en = V[i] + DU[i] * acc / tot
        caps.append([round(st, 2), round(en, 2), txt])
for k in range(len(caps) - 1):
    caps[k][1] = round(min(max(caps[k][1], caps[k + 1][0] - 0.02), caps[k][1] + 0.6), 2)
caps = []  # NO subtitles (owner's standing rule)
SC = [(S[i], S[i + 1] if i + 1 < len(S) else DUR) for i in range(len(S))]
esc = lambda s: s.replace('&', '&amp;').replace('<', '&lt;')
body = '\n'.join(f'<section class="scene clip" id="sc{i}" style="--bg:{BG[i]}" data-start="{a:.2f}" data-duration="{min(b + 0.35, DUR) - a:.2f}" data-track-index="{i + 1}"><div class="cam" id="cam{i}">{SCN[i]}</div></section>' for i, (a, b) in enumerate(SC))
caps_html = '\n'.join(f'<div class="cap" id="cap{k}"><span>{esc(t)}</span></div>' for k, (_, _, t) in enumerate(caps))
JS = ('const T = %s, CAPS = %s, SC = %s;\n' % (json.dumps(T), json.dumps(caps), json.dumps(SC))) + '''const tl = gsap.timeline({ paused: true });
const EIN = "expo.out";
const pop = (sel, at, r) => tl.fromTo(sel, {scale:0.3, opacity:0, rotation:(r||0)-8}, {scale:1, opacity:1, rotation:r||0, duration:0.5, ease:"back.out(2.2)"}, at);
const up = (sel, at) => tl.fromTo(sel, {opacity:0, y:30}, {opacity:1, y:0, duration:0.45, ease:EIN}, at);
const shake = (sel, at, a) => { const kf = []; for (let k = 0; k < 8; k++) kf.push({y:(k%2?-1:1)*(a||14)*(1-k/8), duration:0.04, ease:"none"}); kf.push({y:0, duration:0.04}); tl.to(sel, {keyframes:kf}, at); };
tl.to("#world", {rotation:0.35, x:5, y:-4, duration:3, ease:"sine.inOut", repeat:Math.max(0, Math.floor(T.DUR/3)-1), yoyo:true}, 0);
SC.forEach(([a, b], i) => { const s = "#sc" + i;
  if (i > 0) tl.fromTo(s, {x:(i%2? 1150 : -1150), filter:"blur(14px)"}, {x:0, filter:"blur(0px)", duration:0.5, ease:"power3.out"}, a - 0.05);
  if (i < SC.length - 1) tl.to(s, {x:((i+1)%2? -1150 : 1150), filter:"blur(14px)", duration:0.42, ease:"power3.in"}, b - 0.37); });
''' + JS_SCENES + '''
CAPS.forEach(([s, e], k) => { const g = "#cap" + k;
  tl.fromTo(g, {opacity:0, y:14}, {opacity:1, y:0, duration:0.14, ease:"power2.out"}, Math.max(0.15, s - 0.05));
  tl.to(g, {opacity:0, duration:0.1}, e - 0.1); tl.set(g, {opacity:0, visibility:"hidden"}, e); });
window.__timelines = window.__timelines || {};
window.__timelines["main"] = tl;'''
html = open(H + '/template.html').read().replace('</style>', EXTRA_CSS + '</style>', 1)
for k, v in dict(DUR=f'{DUR:.2f}', BODY=body, CAPS_HTML=caps_html, JS=JS).items():
    html = html.replace('__' + k + '__', v)
open(H + '/../index.html', 'w').write(html)
print('caps', len(caps), 'dur', round(DUR, 1))
