"""Chennai Toon builder.  usage: python3 toonkit/build.py <reel_project_dir> <studio_voice_dir>
Reel project needs build/scenes.py with:
  TITLE, DISC (disclaimer line), SUB (illustration label), SCENES = [ {land, chars:[(char, x, flip)], talker, ui(html), js(str), cam}, ... ]
JS in a scene can use: tl, T (TOON), cam (CAM), S (scene start), V (voice start), P[k] (phrase k start), W[k][j] (word j time), E (scene end).
Writes <project>/index.html and <project>/build/t.json (timing for the audio script)."""
import json, os, sys, html as H
KIT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KIT)
import toon
proj, vdir = sys.argv[1], sys.argv[2]
sys.path.insert(0, proj + '/build')
import scenes as SC
WJ = json.load(open(vdir + '/vo/words.json'))
assert len(WJ) == len(SC.SCENES), (len(WJ), len(SC.SCENES))
LEAD, TAIL, END = 0.35, 0.3, 1.4
starts, vos, t = [], [], 0.0
for i, w in enumerate(WJ):
    starts.append(round(t, 3)); v = t + (0.25 if i == 0 else LEAD); vos.append(round(v, 3)); t = v + w['dur'] + TAIL
DUR = round(t + END, 3)
ends = [starts[i + 1] if i + 1 < len(starts) else DUR for i in range(len(starts))]

body, caps, js = [], [], []
words_abs = []
for i, (sc, w) in enumerate(zip(SC.SCENES, WJ)):
    bg, label = toon.backdrop(sc['land'])
    chars = ''.join(toon.place(c, f'{c}{i}', x, sc.get('cy', 880), sc.get('ch', 1000), flip) for c, x, flip in sc.get('chars', []))
    a, b = starts[i], ends[i]
    body.append(f'<section class="scene clip" id="sc{i}" data-start="{a:.2f}" data-duration="{min(b + 0.5, DUR) - a:.2f}" data-track-index="{i+1}">'
                f'<div class="cam" id="cam{i}">{bg}{chars}</div><div class="ui" id="ui{i}">{sc.get("ui", "")}</div>'
                f'<div class="loc" data-layout-allow-overlap><i></i>{H.escape(sc.get("label", label))}</div>'
                f'<div class="sub" data-layout-allow-overlap>{H.escape(sc.get("sub", SC.SUB))}</div></section>')
    P = [round(vos[i] + p['t0'], 3) for p in w['phrases']]
    W = [[round(vos[i] + x['t'], 3) for x in p['words']] for p in w['phrases']]
    words_abs.append(W)
    # captions: chunks of <= 3 words (4 if short)
    for k, p in enumerate(w['phrases']):
        ws = p['words']; n = len(ws)
        size = 3 if n > 4 else n
        groups = [list(range(j, min(j + size, n))) for j in range(0, n, size)]
        if len(groups) > 1 and len(groups[-1]) == 1:
            last = groups.pop(); groups[-1] = groups[-1] + last
        pend = vos[i] + p['t1'] + 0.12
        for g_i, g in enumerate(groups):
            cid = f'c{i}_{k}_{g_i}'
            t0 = W[k][g[0]] - 0.02
            t1 = W[k][groups[g_i + 1][0]] - 0.03 if g_i + 1 < len(groups) else (P[k + 1] - 0.02 if k + 1 < len(P) else min(pend + 0.2, b - 0.05))
            spans = ''.join(f'<span class="w{" k" if ws[j]["key"] else ""}">{H.escape(ws[j]["w"].upper() if ws[j]["key"] else ws[j]["w"])}</span>' for j in g)
            caps.append(f'<div class="chunk" id="{cid}">{spans}</div>')
            js.append(f'T.caption("{cid}", {t0:.3f}, {t1:.3f}, {json.dumps([W[k][j] for j in g])});')
    # characters: idle, blink, talk
    for c, x, flip in sc.get('chars', []):
        cid = f'{c}{i}'
        js.append(f'T.idle("{cid}", {a:.2f}, {b+0.5:.2f}); T.blink("{cid}", {a:.2f}, {b:.2f}); T.rest("{cid}", {a:.2f});')
        if c == sc.get('talker'):
            allw = [x for p in W for x in p]
            js.append(f'T.talk("{cid}", {json.dumps(allw)}, {vos[i] + w["dur"]:.2f});')
    # camera: slow push + parallax, whip in
    camv = sc.get('cam', 'push')
    if camv == 'push':
        js.append(f'cam.pushIn("#cam{i}", {a:.2f}, {{from:1.0, to:1.07, dur:{b-a+0.5:.2f}, ox:"50%", oy:"60%", ease:"none"}});')
    elif camv == 'pull':
        js.append(f'cam.pullOut("#cam{i}", {a:.2f}, {{from:1.12, to:1.0, dur:{b-a+0.5:.2f}, ease:"power1.out"}});')
    js.append(f'["far","mid","near"].forEach((l,j)=>{{const e=document.querySelector("#cam{i} #"+l); if(e) tl.fromTo(e,{{x:0}},{{x:-(10+j*22),duration:{b-a+0.5:.2f},ease:"none"}},{a:.2f});}});')
    if i > 0:
        js.append(f'cam.whip("#sc{i-1}", "#sc{i}", {a+0.2:.2f}, {{dir:{1 if i % 2 else -1}, dur:0.38}});')
    js.append(f'{{ const S={a:.3f}, E={b:.3f}, V={vos[i]:.3f}, P={json.dumps(P)}, W={json.dumps(W)};\n{sc.get("js", "")}\n}}')
    # characters pop in when scene starts (except first if 'enter' set)
JS = ('const tl = gsap.timeline({paused:true}); const T = TOON(tl); const cam = CAM(tl);\n'
      'const pop=(s,at,r)=>tl.fromTo(s,{scale:0.3,opacity:0,rotation:(r||0)-8},{scale:1,opacity:1,rotation:r||0,duration:0.45,ease:"back.out(2.2)",immediateRender:true},at);\n'
      'const up=(s,at)=>tl.fromTo(s,{opacity:0,y:40},{opacity:1,y:0,duration:0.4,ease:"expo.out"},at);\n'
      'const out=(s,at)=>tl.to(s,{opacity:0,scale:0.9,duration:0.25,ease:"power2.in"},at);\n'
      + f'tl.fromTo("#progf",{{scaleX:0}},{{scaleX:1,duration:{DUR},ease:"none"}},0);\n'
      + '\n'.join(js) + '\nwindow.__timelines = window.__timelines || {}; window.__timelines["main"] = tl;')
html = open(KIT + '/template.html').read()
for k, v in dict(TITLE=H.escape(SC.TITLE), DUR=f'{DUR:.2f}', BODY='\n'.join(body), CAPS='\n'.join(caps), JS=JS,
                 DISC=H.escape(SC.DISC), EXTRA_CSS=getattr(SC, 'EXTRA_CSS', '')).items():
    html = html.replace('__' + k + '__', v)
open(proj + '/index.html', 'w').write(html)
SFX = [[k, round(words_abs[i][p][j] + off, 3)] for k, i, p, j, off in getattr(SC, 'SFX', [])]
json.dump(dict(DUR=DUR, STARTS=starts, VO=vos, ENDS=ends, W=words_abs, SFX=SFX), open(proj + '/build/t.json', 'w'))
print('dur', DUR, 'scenes', len(starts), 'chunks', len(caps))
