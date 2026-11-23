"""ITC "Live Chart Story" reel: weekly candles are the hero; camera zooms to 3 moments. python3 build/make.py <voice_dir>"""
import json, os, sys, html as H
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = sys.argv[1]
WJ = json.load(open(V + '/vo/words.json'))
D = json.load(open(P + '/build/ohlc.json'))
BG, GRID, TXT, MUT, RED, GRN, YEL = '#0B0F17', '#1C2431', '#F3F5F8', '#8A94A6', '#FF4D5E', '#22D38A', '#FFD23F'
LEAD, TAIL = 0.3, 0.3
starts, vos, t = [], [], 0.0
for i, w in enumerate(WJ):
    starts.append(round(t, 3)); v = t + (0.2 if i == 0 else LEAD); vos.append(round(v, 3)); t = v + w['dur'] + TAIL
DUR = round(t + 1.6, 2)
PH = [[round(vos[i] + p['t0'], 3) for p in w['phrases']] for i, w in enumerate(WJ)]
WT = [[[round(vos[i] + x['t'], 3) for x in p['words']] for p in w['phrases']] for i, w in enumerate(WJ)]
S = starts
# chart geometry (chart-space px == screen px at zoom 1)
X0, X1, Y0, Y1, LO, HI = 80, 1000, 600, 1320, 245, 415
n = len(D); step = (X1 - X0) / (n - 1)
X = lambda i: X0 + i * step
Y = lambda p: Y1 - (p - LO) / (HI - LO) * (Y1 - Y0)
g = []
for p in range(250, 420, 25):   # grid + price labels
    g.append(f'<line x1="{X0-20}" y1="{Y(p):.0f}" x2="{X1+20}" y2="{Y(p):.0f}" stroke="{GRID}" stroke-width="2"/>'
             f'<text x="{X1+28}" y="{Y(p)+9:.0f}" fill="{MUT}" font-size="24" font-family="Archivo" font-weight="800">{p}</text>')
for i, (d, o, h, l, c) in enumerate(D):
    if d[8:10] <= '07' and i % 2 == 0 or i == 0:
        pass
for i, (d, o, h, l, c) in enumerate(D):
    col = GRN if c >= o else RED
    x = X(i); top, bot = Y(max(o, c)), Y(min(o, c))
    g.append(f'<g class="cd" id="cd{i}"><line x1="{x:.1f}" y1="{Y(h):.1f}" x2="{x:.1f}" y2="{Y(l):.1f}" stroke="{col}" stroke-width="3"/>'
             f'<rect x="{x-6:.1f}" y="{top:.1f}" width="12" height="{max(3, bot-top):.1f}" rx="2" fill="{col}"/></g>')
months = {'2025-12': 'DEC', '2026-01': 'JAN', '2026-03': 'MAR', '2026-05': 'MAY', '2026-07': 'JUL', '2026-09': 'SEP', '2026-11': 'NOV'}
seen = set()
for i, (d, *_r) in enumerate(D):
    m = d[:7]
    if m in months and m not in seen:
        seen.add(m); g.append(f'<text x="{X(i):.0f}" y="{Y1+44}" fill="{MUT}" font-size="26" font-family="Archivo" font-weight="800" text-anchor="middle">{months[m]}</text>')
# annotations (chart space)
hiI, crashI, lowI, nowI = 4, 5, 48, 52
def callout(cid, x, y, w, lines, col, anchor='left'):
    bx = x + 24 if anchor == 'left' else x - 24 - w
    hgt = 18 + 40 * len(lines)
    s_ = f'<g id="{cid}" opacity="0"><line x1="{x}" y1="{y}" x2="{bx + (0 if anchor=="left" else w)}" y2="{y-30}" stroke="{col}" stroke-width="3"/>'
    s_ += f'<rect x="{bx}" y="{y-30-hgt}" width="{w}" height="{hgt}" rx="10" fill="#111827" stroke="{col}" stroke-width="3"/>'
    for k, (tx, sz, c2) in enumerate(lines):
        s_ += f'<text x="{bx+16}" y="{y-30-hgt+42+k*40}" fill="{c2}" font-size="{sz}" font-family="Archivo" font-weight="800">{H.escape(tx)}</text>'
    return s_ + f'<circle cx="{x}" cy="{y}" r="9" fill="{col}"/></g>'
g.append(callout('a_hi', X(hiI), Y(409.5), 250, [('HIGH ₹409.5', 30, TXT), ('24 DEC 2025', 22, MUT)], YEL))
g.append(callout('a_crash', X(crashI) + 4, Y(363.85), 320, [('1 JAN 2026', 22, MUT), ('−9.7% IN ONE DAY', 30, RED)], RED))
g.append(callout('a_low', X(lowI), Y(252.8), 280, [('LOW ₹252.8', 30, TXT), ('28 OCT 2026', 22, MUT)], YEL, 'right'))
g.append(callout('a_now', X(nowI), Y(301), 270, [('NOW ₹301', 30, TXT), ('+19% FROM LOW', 26, GRN)], GRN, 'right'))
g.append(f'<path id="trend" d="M{X(6):.0f} {Y(352):.0f} L{X(47):.0f} {Y(262):.0f}" stroke="{RED}" stroke-width="5" stroke-dasharray="14 12" fill="none" opacity="0" marker-end="url(#ah)"/>')
g.append(f'<circle id="nowdot" cx="{X(nowI):.1f}" cy="{Y(301):.1f}" r="12" fill="{GRN}"/>')
CHART = ''.join(g)

def cam(fx, fy, s): return f'{{x:{540 - fx*s:.1f},y:{960 - fy*s:.1f},scale:{s}}}'
FULL = cam(540, 960, 1.0)
J = [f'tl.fromTo("#progf",{{scaleX:0}},{{scaleX:1,duration:{DUR},ease:"none"}},0);', f'tl.set("#cz",{FULL},0);']
# hook: candles pop in left to right in 1.8 s
for i in range(n):
    J.append(f'tl.fromTo("#cd{i}",{{scaleY:0,opacity:0,transformOrigin:"50% 50%"}},{{scaleY:1,opacity:1,duration:0.16,ease:"back.out(2)"}},{0.1 + i*0.034:.3f});')
J.append(f'tl.fromTo("#pct",{{scale:2.2,opacity:0}},{{scale:1,opacity:1,duration:0.35,ease:"back.out(2)"}},{WT[0][0][3]-0.1:.2f});')
J.append(f'tl.fromTo("#a_hi",{{opacity:0}},{{opacity:1,duration:0.25}},{WT[0][0][-1]:.2f});')
J.append(f'tl.fromTo("#nowdot",{{scale:0.6,transformOrigin:"50% 50%"}},{{scale:1.5,duration:0.5,yoyo:true,repeat:{int(DUR/0.5)},ease:"sine.inOut"}},1.9);')
# moment 1: zoom on the crash week
fx1, fy1 = X(crashI) + 120, Y(380)
J.append(f'tl.to("#a_hi",{{opacity:0,duration:0.2}},{S[1]-0.2:.2f});')
J.append(f'tl.to("#cz",Object.assign({cam(fx1, fy1, 2.3)},{{duration:0.9,ease:"power3.inOut"}}),{S[1]-0.2:.2f});')
J.append(f'tl.fromTo("#a_crash",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:0.3}},{PH[1][2]:.2f});')
J.append(f'tl.fromTo("#flash",{{opacity:0.55}},{{opacity:0,duration:0.5,immediateRender:false}},{PH[1][2]+0.2:.2f});')
J.append(f'tl.fromTo("#cz",{{rotation:0}},{{rotation:0.6,duration:0.05,yoyo:true,repeat:5,immediateRender:false}},{PH[1][2]+0.2:.2f});')
J.append(f'tl.fromTo("#c1",{{y:80,opacity:0}},{{y:0,opacity:1,duration:0.4,ease:"back.out(2)"}},{PH[1][1]:.2f}); tl.to("#c1",{{opacity:0,duration:0.25}},{S[2]-0.1:.2f});')
# moment 2: track the slow bleed
J.append(f'tl.to("#cz",Object.assign({cam(X(12), Y(320), 1.6)},{{duration:0.8,ease:"power2.inOut"}}),{S[2]-0.2:.2f});')
J.append(f'tl.to("#cz",Object.assign({cam(X(42), Y(275), 1.6)},{{duration:{PH[2][2]-S[2]-0.4:.2f},ease:"none"}}),{S[2]+0.6:.2f});')
J.append(f'tl.fromTo("#trend",{{opacity:0,strokeDashoffset:600}},{{opacity:1,strokeDashoffset:0,duration:1.6,ease:"none"}},{PH[2][1]:.2f});')
J.append(f'tl.fromTo("#a_low",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:0.3}},{WT[2][1][4] if len(WT[2][1])>4 else PH[2][1]+1:.2f});')
J.append(f'tl.fromTo("#c2",{{y:80,opacity:0}},{{y:0,opacity:1,duration:0.4,ease:"back.out(2)"}},{PH[2][2]:.2f}); tl.to("#c2",{{opacity:0,duration:0.25}},{S[3]-0.1:.2f});')
# moment 3: the bounce
J.append(f'tl.to(["#a_low","#trend","#a_crash"],{{opacity:0,duration:0.2}},{S[3]-0.2:.2f});')
J.append(f'tl.to("#cz",Object.assign({cam(X(50)-60, Y(285), 2.0)},{{duration:0.9,ease:"power3.inOut"}}),{S[3]-0.2:.2f});')
J.append(f'tl.fromTo("#a_now",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:0.3}},{PH[3][1]:.2f});')
J.append(f'tl.fromTo("#glow",{{opacity:0}},{{opacity:0.5,duration:0.3,yoyo:true,repeat:1}},{PH[3][1]:.2f});')
J.append(f'tl.fromTo("#c3",{{y:80,opacity:0}},{{y:0,opacity:1,duration:0.4,ease:"back.out(2)"}},{PH[3][2]:.2f}); tl.to("#c3",{{opacity:0,duration:0.25}},{S[4]-0.1:.2f});')
# end: pull out, question + follow
J.append(f'tl.to(["#a_hi","#a_low"],{{opacity:1,duration:0.3}},{S[4]+0.3:.2f});')
J.append(f'tl.to("#cz",Object.assign({FULL},{{duration:0.9,ease:"power3.inOut"}}),{S[4]-0.2:.2f});')
J.append(f'tl.fromTo("#q",{{scale:0.5,opacity:0}},{{scale:1,opacity:1,duration:0.45,ease:"back.out(2.2)"}},{PH[4][0]+0.2:.2f});')
J.append(f'tl.fromTo("#fol",{{y:60,opacity:0}},{{y:0,opacity:1,duration:0.4,ease:"back.out(2)"}},{PH[4][1]:.2f});')
JS = '\n'.join(J)

def card(cid, big, small, col):
    return (f'<div class="card" id="{cid}" style="border-color:{col}"><div class="cb" style="color:{col}">{H.escape(big)}</div>'
            f'<div class="cs">{H.escape(small)}</div></div>')
HTML = f'''<!doctype html><html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<title>ITC: one year, three moments</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
@font-face{{font-family:"Archivo";src:url("assets/fonts/archivo-latin-800-normal.woff2") format("woff2");font-weight:800}}
@font-face{{font-family:"BS";src:url("assets/fonts/big-shoulders-display-latin-900-normal.woff2") format("woff2");font-weight:900}}
@font-face{{font-family:"Poppins";src:url("assets/fonts/Poppins-Bold.ttf") format("truetype");font-weight:700 900}}
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:1080px;height:1920px;overflow:hidden;background:{BG}}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:radial-gradient(120% 70% at 50% 45%,#141B28 0%,{BG} 70%);font-family:"Archivo","Poppins",sans-serif;color:{TXT}}}
#cz{{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:0 0}}
#cz svg{{position:absolute;left:0;top:0;overflow:visible}}
#hdr{{position:absolute;left:0;right:0;top:0;height:560px;z-index:30;background:linear-gradient({BG} 78%,rgba(11,15,23,0))}}
#tk{{position:absolute;left:60px;top:300px;font:900 150px/1 "BS";letter-spacing:2px}}
#tks{{position:absolute;left:66px;top:455px;font:800 28px "Archivo";color:{MUT};letter-spacing:3px}}
#px{{position:absolute;right:60px;top:300px;text-align:right;font:800 84px/1 "Archivo","Poppins"}}
#pct{{position:absolute;right:60px;top:400px;text-align:right;font:800 46px "Archivo","Poppins";color:{RED};transform-origin:100% 50%}}
#handle{{position:absolute;right:40px;top:226px;z-index:60;padding:6px 18px;border-radius:999px;background:{YEL};color:{BG};font:800 28px "Archivo"}}
#prog{{position:absolute;left:40px;right:40px;top:200px;height:6px;background:{GRID};z-index:61;border-radius:3px;overflow:hidden}} #progf{{position:absolute;inset:0;background:{YEL};transform-origin:0 50%}}
.card{{position:absolute;left:60px;right:60px;top:1350px;z-index:40;padding:20px 28px;border-radius:22px;background:#111827;border:4px solid;opacity:0}}
.cb{{font:800 50px/1.1 "Archivo","Poppins"}} .cs{{font:800 26px "Archivo","Poppins";color:{MUT};margin-top:8px;letter-spacing:1px}}
#q{{position:absolute;left:80px;right:80px;top:760px;z-index:45;padding:34px;border-radius:26px;background:{YEL};color:{BG};text-align:center;font:900 92px/1.02 "BS";opacity:0;box-shadow:0 20px 60px rgba(0,0,0,.5)}}
#fol{{position:absolute;left:200px;right:200px;top:1360px;z-index:45;padding:16px;border-radius:999px;background:{TXT};color:{BG};text-align:center;font:800 40px "Archivo";opacity:0}}
#disc{{position:absolute;left:0;right:0;top:1530px;z-index:50;text-align:center;font:800 24px "Archivo";color:{MUT}}}
#ftr{{position:absolute;left:0;right:0;top:1330px;bottom:0;z-index:31;background:linear-gradient(rgba(11,15,23,0),{BG} 22%)}}
#flash{{position:absolute;inset:0;background:{RED};z-index:35;opacity:0;mix-blend-mode:screen}}
#glow{{position:absolute;inset:0;z-index:35;opacity:0;background:radial-gradient(60% 40% at 60% 55%,rgba(34,211,138,.55),transparent 70%)}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920" data-fps="30">
<div id="cz" data-layout-ignore><svg width="1080" height="1920" viewBox="0 0 1080 1920"><defs><marker id="ah" markerWidth="10" markerHeight="10" refX="6" refY="5" orient="auto"><path d="M0 0 L10 5 L0 10Z" fill="{RED}"/></marker></defs>{CHART}</svg></div>
<div id="ftr" data-layout-ignore></div><div id="flash" data-layout-ignore></div><div id="glow" data-layout-ignore></div>
<div id="hdr" data-layout-ignore><div id="tk">ITC</div><div id="tks">NSE · WEEKLY · 1 YEAR</div>
<div id="px">₹301.00</div><div id="pct">−26.5% FROM HIGH</div></div>
<div id="handle" data-layout-allow-overlap>@moneyincloud</div>
<div id="prog" data-layout-ignore><div id="progf"></div></div>
{card('c1', 'New excise duty on cigarettes', 'Announced 31 Dec 2025 · applies from 1 Feb 2026', RED)}
{card('c2', 'Cigarette profit −27%', 'Q2 FY27 (Jul–Sep 2026) · ₹3,813 Cr', RED)}
{card('c3', 'FMCG profit +28% · Paper +48%', 'Q2 FY27 segment results · 2 Nov 2026', GRN)}
<div id="q" data-layout-allow-overlap>IS THE WORST PRICED IN?</div>
<div id="fol" data-layout-allow-overlap>SAVE + FOLLOW @moneyincloud</div>
<div id="disc" data-layout-ignore>NSE via INDmoney, 23 Nov 2026 · Not a buy/sell call. Education only.</div>
<audio id="vo" src="assets/mix.wav" data-start="0" data-duration="{DUR}" data-track-index="40" data-volume="1"></audio>
</div>
<script>
const tl = gsap.timeline({{paused:true}});
{JS}
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;
</script></body></html>'''
open(P + '/index.html', 'w').write(HTML)
json.dump(dict(DUR=DUR, STARTS=starts, VO=vos, PH=PH, CANDLES=[0.1 + i * 0.034 for i in range(n)]), open(P + '/build/t.json', 'w'))
print('dur', DUR, starts)
