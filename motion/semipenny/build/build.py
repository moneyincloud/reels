"""Assemble index.html for the semiconductor penny stocks reel (Silicon Noir).  usage: python3 build.py"""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
from scenes import BG, SCN, JS_SCENES, TRACES, BGIMG
T = json.load(open(H + '/t.json'))
DUR = T['DUR']; S = T['STARTS']
SC = [(S[i], S[i + 1] if i + 1 < len(S) else DUR) for i in range(len(S))]
body = '\n'.join(f'<section class="scene clip" id="sc{i}" data-start="{a:.2f}" data-duration="{min(b + 0.45, DUR) - a:.2f}" data-track-index="{i + 1}"><div class="cam" id="cam{i}">{SCN[i]}</div></section>' for i, (a, b) in enumerate(SC))
JS = ('const T = %s, SC = %s;\n' % (json.dumps(T), json.dumps(SC))) + '''const tl = gsap.timeline({ paused: true });
const EIN = "expo.out";
const pop = (sel, at, r) => tl.fromTo(sel, {scale:0.3, opacity:0, rotation:(r||0)-8}, {scale:1, opacity:1, rotation:r||0, duration:0.5, ease:"back.out(2.2)"}, at);
const up = (sel, at) => tl.fromTo(sel, {opacity:0, y:30}, {opacity:1, y:0, duration:0.45, ease:EIN}, at);
''' + JS_SCENES + '''
window.__timelines = window.__timelines || {};
window.__timelines["main"] = tl;'''
html = open(H + '/template.html').read()
for k, v in dict(DUR=f'{DUR:.2f}', BODY=body, JS=JS, TRACES=TRACES, BGIMG=BGIMG).items():
    html = html.replace('__' + k + '__', v)
open(H + '/../index.html', 'w').write(html)
print('dur', round(DUR, 1), 'scenes', len(SC))
