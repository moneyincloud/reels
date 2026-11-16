"""Vox-style explainer: intraday vs swing vs F&O with real trades. Camera moves via GSAP on each scene's .cam.
usage: python3 gen.py   (reads build/t.json, writes ../index.html)"""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(H + '/t.json'))
DUR = T['DUR']; S = T['STARTS']; V = T['VO']; DU = T['DURS']

# on-screen caption text (digits), one per VO line
CAPTXT = [
    "Intraday, swing or F&O? What each really means, with real trades from last week.",
    "Intraday = buy and sell the same day. 11 Nov: Kalyan Jewellers opened at ₹630 and hit ₹689 within an hour.",
    "But an intraday trade must close the same day. By the closing bell it slipped back to ₹664.",
    "Swing trading = hold for days or weeks. From the Diwali close of ₹592, Kalyan reached ₹711 in 3 sessions. That's +20%.",
    "The risk? You hold overnight. Next morning it opened at ₹718 and dropped to ₹685 in 15 minutes.",
    "F&O = futures and options: contracts on a stock or index, traded in fixed lots. 1 Nifty lot = 65 units ≈ ₹16.5 lakh of Nifty.",
    "This morning Nifty futures rose 179 points. That's ≈ ₹11,600 on one lot, and the same loss if you bet the other way.",
    "That leverage is why SEBI found nearly 9 in 10 F&O traders lost money.",
    "So which one do you do? Comment INTRADAY, SWING or F&O, and save this for later.",
]
caps = []
for i, line in enumerate(CAPTXT):
    words = line.split(); gs, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= 5 or re.search(r'[.,?!:=]$', w): gs.append(cur); cur = []
    if cur: gs.append(cur)
    tot = sum(len(' '.join(g)) for g in gs); acc = 0
    for g in gs:
        txt = ' '.join(g); st = V[i] + DU[i] * acc / tot; acc += len(txt); en = V[i] + DU[i] * acc / tot
        caps.append([round(st, 2), round(en, 2), txt])
for k in range(len(caps) - 1):
    caps[k][1] = round(min(max(caps[k][1], caps[k + 1][0] - 0.02), caps[k][1] + 0.6), 2)

# scenes: 0 hook | 1 intraday (VO1-2) | 2 swing (VO3-4) | 3 F&O (VO5-6) | 4 SEBI (VO7) | 5 CTA (VO8)
SC = [(0, S[1]), (S[1], S[3]), (S[3], S[5]), (S[5], S[7]), (S[7], S[8]), (S[8], DUR)]

# --- intraday chart: Kalyan Jewellers 15-min candles, 11 Nov 2026 (INDmoney) ---
C11 = [(630,672.1,620,663.5),(664,673.45,663.85,667.85),(668.15,689,668,682.5),(682.5,686,679.3,680.2),(680.15,680.15,672,677.6),
       (677.3,679.9,673.05,673.6),(673.75,673.75,666.2,669),(669,672,667.2,669.25),(669,670.95,667.35,667.7),(667.95,671.75,667.6,671.15),
       (671.2,674.4,670.45,671.3),(671.45,673.45,670.5,672),(672.05,673.8,670.85,673.35),(673.35,678,673.05,674),(673.55,676,671.5,672.65),
       (672.65,674.9,672.5,673.35),(673.35,673.7,669,672),(672.05,672.75,669.75,672.75),(672.75,672.75,668.7,668.85),(668.65,672,668.65,670.45),
       (670.45,670.55,669.05,669.95),(670.1,671.1,669.5,670.7),(670.75,670.75,664.8,665.35),(665.1,665.6,658.85,662),(660.2,663.75,660.1,663.75)]
TIMES = [f"{(9*60+15+15*k)//60 if (9*60+15+15*k)//60 <= 12 else (9*60+15+15*k)//60-12}:{(15+15*k)%60:02d}" for k in range(25)]
CW, CH, PX = 58, 560, 50                       # candle step, chart height, left pad
lo, hi = 612, 696
Y = lambda p: CH - (p - lo) / (hi - lo) * CH
cand = []
for k, (o, h, l, c) in enumerate(C11):
    x = PX + k * CW; up = c >= o; col = '#1E8E4E' if up else '#D93A2B'
    top, bot = Y(max(o, c)), Y(min(o, c))
    cand.append(f'<g class="cd" id="cd{k}"><line x1="{x+18}" y1="{Y(h):.1f}" x2="{x+18}" y2="{Y(l):.1f}" stroke="#1B1B1F" stroke-width="4"/>'
                f'<rect x="{x+4}" y="{top:.1f}" width="28" height="{max(4, bot-top):.1f}" fill="{col}" stroke="#1B1B1F" stroke-width="3" rx="3"/></g>')
cand = '\n'.join(cand)
CHW = PX + 25 * CW + 40

# --- swing: daily closes (INDmoney) ---
SW = [('8 Nov', 'Diwali', 592), ('9 Nov', '', 611), ('11 Nov', '', 663.75), ('12 Nov', '', 710.9)]
SWX = [120, 360, 600, 840]; slo, shi, SHH = 570, 735, 620
SY = lambda p: SHH - (p - slo) / (shi - slo) * SHH
swpath = 'M' + ' L'.join(f'{x} {SY(p):.1f}' for x, (_, _, p) in zip(SWX, SW))
swdots = '\n'.join(f'<g class="sd" id="sd{k}"><circle cx="{x}" cy="{SY(p):.1f}" r="16" fill="#fff" stroke="#1B1B1F" stroke-width="6"/>'
                   f'<text x="{x}" y="{SY(p) - 34:.1f}" text-anchor="middle" class="svl">₹{p:,.0f}</text>'
                   f'<text x="{x}" y="{SHH + 60}" text-anchor="middle" class="sdl">{d}</text></g>' for k, (x, (d, _, p)) in enumerate(zip(SWX, SW)))
moons = '\n'.join(f'<text class="moon" id="mn{k}" x="{(SWX[k] + SWX[k + 1]) / 2:.0f}" y="{SHH + 62}" text-anchor="middle">🌙</text>' for k in range(3))
# 13 Nov first 15-min candle: open 718, high 718.05, low 685.1
gx = 1010
gap = (f'<g id="gapc"><line x1="{gx}" y1="{SY(718.05):.1f}" x2="{gx}" y2="{SY(685.1):.1f}" stroke="#1B1B1F" stroke-width="5"/>'
       f'<rect id="gapr" x="{gx-22}" y="{SY(718):.1f}" width="44" height="{SY(685.1)-SY(718):.1f}" fill="#D93A2B" stroke="#1B1B1F" stroke-width="4" rx="4"/>'
       f'<text x="{gx}" y="{SY(718) - 26:.1f}" text-anchor="middle" class="svl">₹718</text>'
       f'<text x="{gx}" y="{SY(685.1) + 52:.1f}" text-anchor="middle" class="svl" fill="#D93A2B">₹685</text>'
       f'<text x="{gx}" y="{SHH + 60}" text-anchor="middle" class="sdl">13 Nov</text></g>')

people = '\n'.join(f'<svg class="pp" id="pp{k}" style="left:{110 + (k % 5) * 176}px;top:{390 + (k // 5) * 270}px" viewBox="0 0 120 220">'
                   f'<circle cx="60" cy="42" r="34"/><path d="M14 210 C 14 120, 106 120, 106 210 Z"/></svg>' for k in range(10))

def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;')
caps_html = '\n'.join(f'<div class="cap" id="cap{k}"><span>{esc(t)}</span></div>' for k, (_, _, t) in enumerate(caps))

def scene(i, body, hdr=''):
    a, b = SC[i]
    return (f'<section class="scene clip" id="sc{i}" data-start="{a:.2f}" data-duration="{b - a + 0.35:.2f}" data-track-index="{i + 1}">'
            f'<div class="cam" id="cam{i}">{body}</div>{hdr}</section>')

HOOK = '''<div class="ttl hand" style="top:240px">3 ways to trade</div>
<div class="tag" id="tg0" style="left:70px;top:420px;background:#2F6FE4;transform:rotate(-4deg)">INTRADAY<small>same day</small></div>
<div class="tag" id="tg1" style="left:330px;top:640px;background:#C25E00;transform:rotate(3deg)">SWING<small>days to weeks</small></div>
<div class="tag" id="tg2" style="left:600px;top:860px;background:#D93A2B;transform:rotate(-3deg)">F&amp;O<small>contracts, lots</small></div>
<div class="hand" id="real" style="position:absolute;left:0;right:0;top:1080px;text-align:center;font-size:62px">real trades · real prices 👇</div>'''

INTRA = f'''<div class="chart" id="ichart" style="left:0;top:330px;width:{CHW}px;height:{CH + 80}px">
<svg viewBox="0 0 {CHW} {CH + 80}" style="width:{CHW}px;height:{CH + 80}px;overflow:visible">
<line x1="{PX}" y1="{Y(630):.1f}" x2="{CHW}" y2="{Y(630):.1f}" class="dash"/>
{cand}
<g id="hpin"><circle cx="{PX + 2 * CW + 18}" cy="{Y(689):.1f}" r="22" fill="none" stroke="#1E8E4E" stroke-width="7"/>
<text x="{PX + 2 * CW + 50}" y="{Y(689) - 10:.1f}" class="lbl" fill="#1E8E4E">HIGH ₹689 · 10:00</text></g>
<text id="olbl" x="{PX + 40}" y="{Y(630) + 52:.1f}" class="lbl">OPEN ₹630 · 9:15</text>
<g id="clbl"><text x="{PX + 24 * CW - 260}" y="{Y(663.75) + 70:.1f}" class="lbl">CLOSE ₹664 · 3:30</text></g>
</svg></div>
<div class="stamp" id="istamp" style="left:610px;top:1000px;transform:rotate(-6deg)">SAME DAY: IN → OUT</div>'''
INTRA_H = '''<div class="hdr"><span class="cap-t hand" style="color:#2F6FE4">Intraday</span><span class="sub">Kalyan Jewellers · 11 Nov · 15-min</span></div>
<div class="clock" id="clock"><span>🕘</span><b id="clk">9:15</b></div><div class="bell" id="bell">🔔</div>'''

SWING = f'''<div class="chart" id="schart" style="left:0;top:360px;width:1080px;height:{SHH + 90}px">
<svg viewBox="0 0 1080 {SHH + 90}" style="width:1080px;height:{SHH + 90}px;overflow:visible">
<path id="swl" d="{swpath}" style="stroke:#C25E00;stroke-width:10"/>
{swdots}{moons}{gap}</svg></div>
<div class="big" id="sw20" style="left:150px;top:350px;color:#1E8E4E">+20%</div>
<div class="stamp" id="gstamp" style="left:330px;top:340px;transform:rotate(5deg);background:#D93A2B;color:#fff">OVERNIGHT GAP</div>
<div id="night"></div>'''
SWING_H = '<div class="hdr"><span class="cap-t hand" style="color:#C25E00">Swing</span><span class="sub">Kalyan Jewellers · daily closes</span></div>'

FNO = '''<div id="ticket"><div class="tk-h">NIFTY · NOV FUTURES</div>
<div class="tk-r"><span>1 lot</span><b id="u65">65 units</b></div>
<div class="tk-r"><span>× price (16 Nov, 9:52 AM)</span><b>₹25,350</b></div>
<div class="tk-r tot"><span>= contract value</span><b id="lakh">₹16.5 lakh</b></div></div>
<div class="big" id="p179" style="left:0;right:0;top:1960px;text-align:center;color:#1E8E4E;font-size:120px">+179 pts</div>
<div id="saw"><div id="plank"><div class="side l">BUYER<b>+₹11,642</b></div><div class="side r">SELLER<b>−₹11,642</b></div></div><div id="pivot"></div></div>
<div class="hand" id="math" style="position:absolute;left:0;right:0;top:2655px;text-align:center;font-size:52px">179 points × 65 units = ₹11,642 per lot</div>'''
FNO_H = '<div class="hdr"><span class="cap-t hand" style="color:#D93A2B">F&amp;O</span><span class="sub">futures &amp; options · fixed lots</span></div>'

SEBI = f'''<div class="ttl hand" style="top:230px">F&amp;O traders</div>{people}
<div class="big" id="n9" style="left:0;right:0;top:930px;text-align:center;color:#D93A2B;font-size:110px">~9 in 10 lost money</div>
<div id="src">Source: SEBI study, individual traders in equity derivatives, FY26 (Aug 2026)</div>'''

CTA = '''<div class="ttl hand" style="top:240px">Which one do you do?</div>
<img id="host" src="assets/img/s0_008.png" style="position:absolute;left:40px;top:600px;width:360px"/>
<div class="pill" id="o0" style="left:430px;top:470px;background:#2F6FE4">INTRADAY</div>
<div class="pill" id="o1" style="left:430px;top:620px;background:#C25E00">SWING</div>
<div class="pill" id="o2" style="left:430px;top:770px;background:#D93A2B">F&amp;O</div>
<div class="pill" id="sv" style="left:430px;top:960px;background:#FFE45C;color:#1B1B1F;font-size:50px">💾 SAVE THIS</div>'''

body = '\n'.join([scene(0, HOOK), scene(1, INTRA, INTRA_H), scene(2, SWING, SWING_H), scene(3, FNO, FNO_H), scene(4, SEBI), scene(5, CTA)])
CANDT = [T['open630'] + (T['high'] - T['open630']) * k / 2 if k <= 2 else T['high'] + (T['close'] - 0.3 - T['high']) * (k - 2) / 22 for k in range(25)]

html = open(H + '/template.html').read()
for k, v in dict(DUR=f'{DUR:.2f}', BODY=body, CAPS_HTML=caps_html, TJSON=json.dumps(T), CAPS=json.dumps(caps), SC=json.dumps(SC),
                 CANDT=json.dumps(CANDT), TIMES=json.dumps(TIMES), CHW=str(CHW)).items():
    html = html.replace('__' + k + '__', v)
open(H + '/../index.html', 'w').write(html)
print('caps', len(caps), 'dur', round(DUR, 1))
