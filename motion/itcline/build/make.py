"""ITC factory film (Assembly-Line Diagram grammar, own drawing code). python3 build/make.py <studio_voice_dir>
World: a tall cut-away tower, 1080 wide, floors 900 tall. Camera = transform on #world."""
import json, os, sys, math, html as H
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = sys.argv[1]
WJ = json.load(open(V + '/vo/words.json'))
PAPER, INK, GROUND, WALL, BODY = '#F1EADB', '#1C1F2B', '#2B2452', '#FBF6EC', '#E7A07E'
OCH, TEAL, GRN, VER = '#F2B134', '#2E9C8F', '#8BC34A', '#E0482E'
OCHL, TEALL, GRNL, VERL = '#FFD77A', '#6CCFC2', '#C5E98F', '#FF8A6E'
SH = '#C9BFAE'   # Holmes shadow (pale flat)
FL = 900
FT = lambda k: 900 + (k - 1) * FL   # floor k top (k=1..6), roof 0..900
TOWER_X0, TOWER_X1, WALLW = 40, 1040, 56
BOTTOM = FT(7)

# ---------------------------------------------------------------- timing
LEAD, TAIL = 0.3, 0.35
starts, vos, t = [], [], 0.0
for i, w in enumerate(WJ):
    starts.append(round(t, 3)); v = t + (0.4 if i == 0 else LEAD); vos.append(round(v, 3)); t = v + w['dur'] + TAIL
DUR = round(t + 2.2, 2)
P0 = [[round(vos[i] + p['t0'], 3) for p in w['phrases']] for i, w in enumerate(WJ)]
WT = [[[round(vos[i] + x['t'], 3) for x in p['words']] for p in w['phrases']] for i, w in enumerate(WJ)]
S = starts

# ---------------------------------------------------------------- drawing helpers
def st(w=6, c=INK): return f'stroke="{c}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'
def rect(x, y, w, h, fill, sw=6, rx=4, sh=0, extra=''):
    s = f'<rect x="{x+sh}" y="{y+sh}" width="{w}" height="{h}" rx="{rx}" fill="{SH}"/>' if sh else ''
    return s + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {st(sw)} {extra}/>'
def txt(x, y, s, size, fill=INK, fam='BS', anchor='start', extra=''):
    fams = {'BS': '"Big Shoulders Display","Poppins",sans-serif', 'AR': '"Archivo","Poppins",sans-serif', 'TA': '"NotoTamil",sans-serif'}
    w = {'BS': 900, 'AR': 800, 'TA': 800}[fam]
    return f'<text x="{x}" y="{y}" font-family=\'{fams[fam]}\' font-weight="{w}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" {extra}>{H.escape(s)}</text>'
def numc(x, y, n, cid):
    return (f'<g id="{cid}"><circle cx="{x+3}" cy="{y+3}" r="30" fill="{SH}"/><circle id="{cid}f" cx="{x}" cy="{y}" r="30" fill="{WALL}" {st(5)}/>'
            + txt(x, y + 13, str(n), 38, INK, 'BS', 'middle') + '</g>')
def plaque(x, y, n, en, ta, cid, w=None):
    w = w or int(110 + len(en) * 23 + (len(ta) * 17 + 30 if ta else 0))
    return (f'<g id="{cid}">' + rect(x, y, w, 76, '#FFF8E6', 4, 3, 6) + numc(x + 40, y + 38, n, cid + 'n')
            + txt(x + 82, y + 56, en, 50, INK, 'BS') + ((f'<line x1="{x+92+len(en)*23}" y1="{y+14}" x2="{x+92+len(en)*23}" y2="{y+62}" {st(3)}/>'
            + txt(x + 104 + len(en) * 23, y + 52, ta, 30, INK, 'TA')) if ta else '') + '</g>')
def pipe(pts, w, col, hl, cid=''):
    d = 'M' + ' L'.join(f'{x} {y}' for x, y in pts)
    return (f'<g id="{cid}"><path d="{d}" fill="none" stroke="{INK}" stroke-width="{w+6}" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="{hl}" stroke-width="{max(2, w*0.2):.1f}" stroke-linejoin="round" stroke-linecap="round" transform="translate({-w*0.18:.1f} {-w*0.18:.1f})" opacity=".9"/></g>')
def worker(x, y, coat, cid, s=1.0, cap=None, arm=-20):
    """faceless figure standing at (x, y=feet)."""
    k = s
    return (f'<g id="{cid}" transform="translate({x} {y}) scale({k})">'
            f'<rect x="-14" y="-40" width="10" height="40" rx="4" fill="{INK}"/><rect x="4" y="-40" width="10" height="40" rx="4" fill="{INK}"/>'
            f'<rect x="-22" y="-104" width="44" height="70" rx="14" fill="{coat}" {st(4)}/>'
            f'<g id="{cid}a" style="transform-origin:16px -96px"><rect x="12" y="-100" width="12" height="52" rx="6" fill="{coat}" {st(4)} transform="rotate({arm} 18 -96)"/></g>'
            f'<circle cx="0" cy="-124" r="18" fill="{BODY}" {st(4)}/>'
            + (f'<path d="M-19 -128 Q0 -156 19 -128 Z" fill="{cap}" {st(4)}/>' if cap else '') + '</g>')
def slab(y):
    r = ''.join(f'<circle cx="{x}" cy="{y+14}" r="4" fill="{INK}"/>' for x in range(TOWER_X0 + WALLW + 30, TOWER_X1 - WALLW, 70))
    return f'<rect x="{TOWER_X0+WALLW}" y="{y}" width="{TOWER_X1-TOWER_X0-2*WALLW}" height="28" fill="{BODY}" {st(5)}/>' + r
def room(x, y, w, h, frame, cid=''):
    return (f'<g id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{frame}" {st(6)}/>'
            f'<rect x="{x+18}" y="{y+18}" width="{w-36}" height="{h-36}" fill="{WALL}" {st(4)}/>'
            f'<rect x="{x+18}" y="{y+h-70}" width="{w-36}" height="52" fill="#E3D9C6" {st(4)}/></g>')
def board(x, y, w, lines, cid, h=None):
    h = h or 40 + 58 * len(lines)
    out = f'<g id="{cid}">' + rect(x, y, w, h, '#1F2A44', 5, 6, 8)
    for i, (s_, col, sz) in enumerate(lines):
        out += txt(x + w / 2, y + 62 + i * 58, s_, sz, col, 'AR', 'middle')
    return out + '</g>'
def tag(x, y, col, en, cid):
    w = len(en) * 24 + 74
    return (f'<g id="{cid}"><line x1="{x+w/2}" y1="{y-60}" x2="{x+w/2}" y2="{y}" stroke="{INK}" stroke-width="4" stroke-dasharray="6 6"/>'
            + rect(x, y, w, 58, '#FFF8E6', 4, 3, 5) + f'<rect x="{x+12}" y="{y+12}" width="34" height="34" rx="4" fill="{col}" {st(3)}/>'
            + txt(x + 58, y + 44, en, 38, INK, 'BS') + '</g>')

# ---------------------------------------------------------------- the world
W = []
W.append(f'<rect x="-3000" y="-3000" width="7080" height="{BOTTOM+6000}" fill="{PAPER}"/>')
# ground line + street
W.append(f'<rect x="-3000" y="{BOTTOM}" width="7080" height="3000" fill="#D9CDB6"/><line x1="-3000" y1="{BOTTOM}" x2="4080" y2="{BOTTOM}" {st(8)}/>')
# tower silhouette: dark ground inside a thick body wall; roof at y=420 with hatch gap 440..640
ROOF = 420
W.append(f'<rect x="{TOWER_X0}" y="{ROOF}" width="{TOWER_X1-TOWER_X0}" height="{BOTTOM-ROOF}" fill="{GROUND}"/>')
W.append(f'<rect x="{TOWER_X0}" y="{ROOF}" width="{WALLW}" height="{BOTTOM-ROOF}" fill="{BODY}" {st(6)}/>')
W.append(f'<rect x="{TOWER_X1-WALLW}" y="{ROOF}" width="{WALLW}" height="{BOTTOM-ROOF}" fill="{BODY}" {st(6)}/>')
W.append(f'<rect x="{TOWER_X0}" y="{ROOF}" width="400" height="{WALLW}" fill="{BODY}" {st(6)}/><rect x="{TOWER_X1-400}" y="{ROOF}" width="400" height="{WALLW}" fill="{BODY}" {st(6)}/>')
# chimney + intake belt on roof
W.append(rect(820, 180, 110, 240, BODY, 6, 4, 12) + f'<rect x="808" y="170" width="134" height="30" fill="{INK}"/>')
W.append(f'<g id="smoke" opacity=".7"><circle cx="875" cy="140" r="28" fill="#D8D0C2"/><circle cx="905" cy="100" r="22" fill="#D8D0C2"/><circle cx="930" cy="60" r="16" fill="#D8D0C2"/></g>')
W.append(f'<rect x="-600" y="356" width="1046" height="26" fill="#3B3F52" {st(5)}/>')
W.append('<g id="beltdash">' + ''.join(f'<rect x="{x}" y="362" width="24" height="14" fill="#6B708A"/>' for x in range(-600, 440, 48)) + '</g>')
W.append(f'<path d="M440 382 L640 382 L600 470 L480 470Z" fill="#3B3F52" {st(5)}/>')   # hatch funnel
# gantry title sign over the infeed
W.append(f'<g id="gantry"><line x1="120" y1="0" x2="120" y2="150" {st(5)}/><line x1="400" y1="0" x2="400" y2="150" {st(5)}/>'
         + rect(60, 150, 400, 120, BODY, 6, 4, 10) + txt(260, 232, 'ITC · THE FACTORY', 58, INK, 'BS', 'middle') + '</g>')
# cargo crate (world group, moves along belt/hatch then into sorter)
W.append(f'<g id="crate"><rect x="-120" y="-100" width="240" height="100" rx="6" fill="#B07A45" {st(6)}/>'
         f'<line x1="-120" y1="-50" x2="120" y2="-50" {st(4)}/><rect x="-104" y="-88" width="208" height="30" fill="#FFF8E6" {st(3)}/>'
         + txt(0, -64, '₹30,431 CR', 30, INK, 'AR', 'middle') + txt(0, -18, 'SALES · Q2', 26, '#FFF8E6', 'AR', 'middle') + '</g>')

# floor slabs
for k in range(1, 7):
    W.append(slab(FT(k) - 14))
# ---- F1 SORTER
y = FT(1)
W.append(room(200, y + 70, 680, 780, OCH))
W.append(f'<path d="M380 {y+150} L700 {y+150} L620 {y+380} L460 {y+380}Z" fill="#5A5F78" {st(6)}/>')   # hopper
W.append(rect(430, y + 380, 220, 150, '#3B3F52', 6, 8, 10))
W.append(f'<g id="sgear" style="transform-origin:540px {y+455}px"><circle cx="540" cy="{y+455}" r="44" fill="{OCH}" {st(5)}/>'
         + ''.join(f'<rect x="534" y="{y+402}" width="12" height="22" fill="{INK}" transform="rotate({a} 540 {y+455})"/>' for a in range(0, 360, 45)) + '</g>')
CH = [(OCH, OCHL, 290), (TEAL, TEALL, 450), (GRN, GRNL, 630), (VER, VERL, 790)]
for i, (c, l, x) in enumerate(CH):
    W.append(pipe([(540, y + 530), (x, y + 640), (x, y + 760)], 30, c, l, f'chute{i}'))
W.append(plaque(220, y + 96, 1, 'SORTER', 'பிரிப்பு', 'p1'))
for i, (nm, x) in enumerate((('CIGARETTES', 120), ('FMCG', 380), ('AGRI', 560), ('PAPER', 730))):
    W.append(tag(x, y + 560 + (i % 2) * 0, CH[i][0], nm, f'tag{i}'))
# vertical legend pipes: left gutter down to each floor (ochre to F2, teal F3, green F4, vermilion F5)
GX = [118, 146, 934, 962]
W.append(pipe([(290, y + 790), (290, y + 860), (GX[0], y + 860), (GX[0], FT(2) + 250), (230, FT(2) + 250)], 22, OCH, OCHL, 'pc'))
W.append(pipe([(450, y + 790), (450, y + 880), (GX[1] + 18, y + 880), (GX[1] + 18, FT(3) + 300), (230, FT(3) + 300)], 16, TEAL, TEALL, 'pf'))
W.append(pipe([(630, y + 790), (630, y + 870), (GX[2] - 18, y + 870), (GX[2] - 18, FT(4) + 300), (850, FT(4) + 300)], 16, GRN, GRNL, 'pa'))
W.append(pipe([(790, y + 790), (790, y + 850), (GX[3] - 10, y + 850), (GX[3] - 10, FT(5) + 260), (850, FT(5) + 260)], 14, VER, VERL, 'pp'))
# ---- F2 CIGARETTE PRESS
y = FT(2)
W.append(room(200, y + 70, 680, 780, OCH))
W.append(plaque(220, y + 96, 2, 'PRESS', 'சிகரெட்', 'p2'))
W.append(rect(300, y + 220, 260, 40, '#5A5F78', 6) + rect(300, y + 600, 260, 40, '#5A5F78', 6)
         + f'<rect x="306" y="{y+260}" width="20" height="340" fill="#5A5F78" {st(5)}/><rect x="534" y="{y+260}" width="20" height="340" fill="#5A5F78" {st(5)}/>')
W.append(f'<g id="ram"><rect x="360" y="{y+260}" width="140" height="150" fill="{OCH}" {st(6)}/><rect x="404" y="{y+250}" width="52" height="30" fill="{INK}"/></g>')
W.append(''.join(rect(330 + i * 70, y + 560, 50, 40, '#FFF8E6', 4, 3) + f'<rect x="{330+i*70}" y="{y+560}" width="50" height="12" fill="{OCH}" {st(3)}/>' for i in range(3)))
W.append(f'<rect x="230" y="{y+640}" width="620" height="22" fill="#3B3F52" {st(4)}/>')
# excise gate: worker with STOP sign + tax chute leaving through the right wall
W.append(f'<g id="gate">' + worker(680, y + 760, '#8A8FA8', 'wtax', 1.6, '#3B3F52', -150)
         + f'<g id="stop"><line x1="712" y1="{y+590}" x2="712" y2="{y+470}" {st(5)}/>' + rect(640, y + 400, 150, 80, VER, 5, 6) + txt(715, y + 456, 'EXCISE', 40, '#FFF8E6', 'BS', 'middle') + '</g></g>')
W.append(pipe([(860, y + 330), (1000, y + 330), (1180, y + 330)], 34, '#8A8FA8', '#C7CADB', 'taxpipe'))
W.append(txt(1080, y + 300, 'TAX', 40, INK, 'BS', 'middle'))
W.append(board(250, y + 680 - 400, 0, [], 'dummy') if False else '')
CIGB = board(570, y + 140, 290, [('SALES', '#C9D2E8', 30), ('₹15,536 CR', '#FFFFFF', 44), ('PROFIT', '#C9D2E8', 30), ('₹3,813 CR', OCHL, 44), ('−27%', VERL, 44)], 'b2', 340)
W.append(CIGB)
W.append(f'<g id="threeq">' + rect(250, y + 690, 420, 90, OCHL, 6, 8, 8) + txt(460, y + 750, '≈ 3/4 OF PROFIT', 48, INK, 'BS', 'middle') + '</g>')
# ---- F3 FMCG PACKING LINE
y = FT(3)
W.append(room(200, y + 70, 680, 780, TEAL))
W.append(plaque(220, y + 96, 3, 'PACKING LINE', 'பொருட்கள்', 'p3'))
W.append(f'<rect x="230" y="{y+560}" width="620" height="34" fill="#3B3F52" {st(5)}/>' + ''.join(f'<circle cx="{x}" cy="{y+594}" r="16" fill="#8A8FA8" {st(4)}/>' for x in range(260, 860, 80)))
PK = ''
for i in range(9):
    x = 240 + i * 150; kind = i % 3
    if kind == 0:   # atta bag
        PK += f'<g transform="translate({x} {y+560})"><path d="M-40 0 L-34 -110 L34 -110 L40 0Z" fill="#F4E6C4" {st(4)}/><rect x="-26" y="-80" width="52" height="34" fill="{TEAL}" {st(3)}/></g>'
    elif kind == 1:  # biscuit box
        PK += f'<g transform="translate({x} {y+560})"><rect x="-44" y="-70" width="88" height="70" fill="{TEALL}" {st(4)}/><circle cx="0" cy="-35" r="18" fill="#C98A4B" {st(3)}/></g>'
    else:            # chips packet
        PK += f'<g transform="translate({x} {y+560})"><path d="M-36 0 Q-46 -50 -36 -100 L36 -100 Q46 -50 36 0Z" fill="{OCHL}" {st(4)}/><path d="M-36 -86 L36 -86" {st(3)}/></g>'
W.append(f'<clipPath id="belt3"><rect x="236" y="{y+380}" width="608" height="200"/></clipPath><g clip-path="url(#belt3)"><g id="packs">{PK}</g></g>')
W.append(worker(300, y + 760, TEAL, 'w3', 1.5, OCH, -60) + worker(760, y + 760, TEAL, 'w3b', 1.5, None, -100))
W.append(board(560, y + 200, 300, [('PROFIT', '#C9D2E8', 30), ('₹558 CR', TEALL, 46), ('+28%', GRNL, 46)], 'b3', 230))
# ---- F4 AGRI SIEVE
y = FT(4)
W.append(room(200, y + 70, 680, 780, GRN))
W.append(plaque(220, y + 96, 4, 'SIEVE', 'விவசாயம்', 'p4'))
W.append(f'<g id="sieve"><rect x="290" y="{y+330}" width="360" height="60" fill="#B07A45" {st(5)}/>'
         + ''.join(f'<line x1="{x}" y1="{y+330}" x2="{x}" y2="{y+390}" {st(2)}/>' for x in range(305, 650, 24)) + '</g>')
W.append(f'<g id="grain">' + ''.join(f'<ellipse cx="{300+ (i*53)%340}" cy="{y+420+(i*37)%120}" rx="9" ry="5" fill="{GRN}" {st(2)}/>' for i in range(22)) + '</g>')
W.append(f'<path d="M290 {y+600} L650 {y+600} L600 {y+700} L340 {y+700}Z" fill="#B07A45" {st(5)}/>')
W.append(worker(720, y + 760, GRN, 'w4', 1.5, OCH, -40))
W.append(board(560, y + 200, 300, [('PROFIT', '#C9D2E8', 30), ('₹511 CR', GRNL, 46), ('+11%', GRNL, 46)], 'b4', 230))
# ---- F5 PAPER ROLLERS + HOTELS room
y = FT(5)
W.append(room(200, y + 70, 450, 780, VER))
W.append(plaque(220, y + 96, 5, 'ROLLERS', 'காகிதம்', 'p5', 410))
for i, cx in enumerate((290, 385, 480)):
    W.append(f'<g id="roll{i}" style="transform-origin:{cx}px {y+420}px"><circle cx="{cx}" cy="{y+420}" r="42" fill="{VERL}" {st(5)}/><line x1="{cx-42}" y1="{y+420}" x2="{cx+42}" y2="{y+420}" {st(4)}/><circle cx="{cx}" cy="{y+420}" r="10" fill="{INK}"/></g>')
W.append(f'<rect x="240" y="{y+468}" width="380" height="16" fill="#FFFDF6" {st(3)}/>')
W.append(board(250, y + 560, 360, [('PROFIT ₹282 CR', VERL, 36), ('+48%', GRNL, 44), ('NEW MILL FROM AUG 2026', '#C9D2E8', 22)], 'b5', 230))
W.append(f'<rect x="668" y="{y+70}" width="270" height="780" fill="{GROUND}"/>')
W.append(f'<g id="hotel">' + room(670, y + 70, 260, 780, BODY) + plaque(684, y + 96, 6, 'HOTELS', '', 'p6', 230)
         + f'<g transform="translate(800 {y+700})"><rect x="-70" y="-300" width="140" height="300" fill="#F4E6C4" {st(5)}/>'
         + ''.join(f'<rect x="{-50+c*36}" y="{-270+r*56}" width="24" height="30" fill="{OCHL}" {st(3)}/>' for r in range(5) for c in range(3))
         + f'<path d="M-84 -300 L0 -350 L84 -300Z" fill="{VER}" {st(5)}/></g></g>')
W.append(f'<g id="hook"><line x1="800" y1="{y-600}" x2="800" y2="{y+300}" {st(5)}/><path d="M780 {y+300} q20 40 40 0" fill="none" {st(6)}/></g>')
W.append(f'<g id="hoteltag" opacity="0">' + rect(500, y + 200, 540, 150, '#FFF8E6', 5, 6, 8) + txt(770, y + 258, 'SEPARATE SINCE JAN 2025', 38, INK, 'BS', 'middle')
         + txt(770, y + 316, 'ITC KEEPS 40%', 44, VER, 'BS', 'middle') + '</g>')
# ---- F6 VAULT
y = FT(6)
W.append(room(200, y + 70, 680, 780, '#8A8FA8'))
W.append(plaque(220, y + 96, 7, 'VAULT', 'லாபம்', 'p7'))
W.append(f'<circle cx="540" cy="{y+470}" r="190" fill="#B7BCCB" {st(8)}/><circle cx="540" cy="{y+470}" r="150" fill="#9CA2B6" {st(5)}/>')
W.append(f'<g id="wheel" style="transform-origin:540px {y+470}px">' + ''.join(f'<line x1="540" y1="{y+470}" x2="{540+110*math.cos(a)}" y2="{y+470+110*math.sin(a)}" {st(10)}/>' for a in (0, 2.09, 4.19)) + f'<circle cx="540" cy="{y+470}" r="26" fill="{INK}"/></g>')
# profit pipes from each floor down the right gutter into the vault (width ~ profit)
for (col, hl, w, fy, x) in ((OCH, OCHL, 44, 2, 990), (TEAL, TEALL, 12, 3, 1010), (GRN, GRNL, 12, 4, 1022), (VER, VERL, 9, 5, 1032)):
    W.append(pipe([(880, FT(fy) + 760), (x - 40, FT(fy) + 760), (x - 40, y + 300), (880, y + 300)], w, col, hl, f'prof{fy}'))
W.append(f'<g id="vnum" opacity="0">' + rect(330, y + 690, 420, 130, '#1F2A44', 5, 6, 8) + txt(540, y + 748, '₹4,137 CR PROFIT', 40, '#FFFFFF', 'AR', 'middle')
         + txt(540, y + 800, '−20% vs last year', 34, VERL, 'AR', 'middle') + '</g>')
# end nameplate on the ground line (world)
W.append(f'<g id="nameplate" opacity="0"><line x1="300" y1="{BOTTOM}" x2="300" y2="{BOTTOM+260}" {st(10)}/><line x1="780" y1="{BOTTOM}" x2="780" y2="{BOTTOM+260}" {st(10)}/>'
         + rect(100, BOTTOM + 260, 880, 560, BODY, 10, 8, 26) + txt(540, BOTTOM + 420, 'ITC LTD', 130, INK, 'BS', 'middle')
         + txt(540, BOTTOM + 560, '₹301 · 23 NOV 2026', 90, INK, 'AR', 'middle')
         + txt(540, BOTTOM + 680, '52W: ₹252.8 – ₹409.5', 70, '#3B3F52', 'AR', 'middle') + txt(540, BOTTOM + 770, 'Results: ITC Q2 FY27 (2 Nov 2026) · NSE via INDmoney', 38, '#3B3F52', 'AR', 'middle') + '</g>')
WORLD = ''.join(W)

# ---------------------------------------------------------------- porthole chart (screen space)
MC = [404.25, 403, 322.15, 313.6, 287.7, 314.9, 286.9, 286.95, 281, 255.5, 262.75, 265.6, 301]
def cx_(i): return 230 + i * (620 / 12)
def cy_(v): return 1180 - (v - 240) / (420 - 240) * 420
CHART = 'M' + ' L'.join(f'{cx_(i):.0f} {cy_(v):.0f}' for i, v in enumerate(MC))

# ---------------------------------------------------------------- camera keys (cx, cy, s) per beat
def cam_at(*a): return a
F = lambda k: FT(k) + 450
CAM = [
    (S[1], 540, 300, 0.95),           # roof
    (S[1] + 2.4, 540, 520, 1.0),
    (S[2], 540, F(1), 1.0),           # sorter
    (S[2] + 1.6, 540, F(1) + 60, 0.88),
    (S[3], 540, F(2), 1.0),           # press
    (P0[3][1], 600, F(2) + 60, 1.12),  # push to gate
    (P0[3][3], 540, F(2) + 120, 0.95),
    (S[4], 540, F(3), 1.0),           # fmcg
    (S[5], 540, F(4), 1.0),           # agri
    (S[6], 480, F(5), 1.0),           # paper
    (S[7], 640, F(5), 0.95),          # hotels
    (S[7] + 3.0, 860, F(5) - 300, 0.8),
    (S[8], 560, F(6), 0.95),          # vault
    (S[9], 540, F(6) + 200, 0.9),
    (S[9] + 3.2, 540, (BOTTOM + 900) / 2 - 40, 0.255),   # great pull-back incl. nameplate
]

# ---------------------------------------------------------------- JS timeline
J = []
J.append(f'tl.fromTo("#progf",{{scaleX:0}},{{scaleX:1,duration:{DUR},ease:"none"}},0);')
# camera
k0 = CAM[0]
J.append(f'const camSet=(cx,cy,s)=>({{x:540-cx*s,y:960-cy*s,scale:s}});')
J.append(f'tl.set("#world",camSet({k0[1]},{k0[2]},{k0[3]}),0);')
for a, b in zip(CAM, CAM[1:]):
    d = max(0.3, b[0] - a[0])
    J.append(f'tl.fromTo("#world",camSet({a[1]},{a[2]},{a[3]}),Object.assign(camSet({b[1]},{b[2]},{b[3]}),{{duration:{min(d,1.4):.2f},ease:"power2.inOut",immediateRender:false}}),{b[0]-min(d,1.4):.2f});')
# porthole: chart draws, then porthole grows and fades away to reveal the world
J.append(f'tl.fromTo("#chartline",{{strokeDashoffset:2000}},{{strokeDashoffset:0,duration:{P0[0][0]+3.6:.2f},ease:"none"}},0.3);')
J.append(f'tl.fromTo("#p409",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3}},{WT[0][0][4] if len(WT[0][0])>4 else 1.2:.2f});')
J.append(f'tl.fromTo("#p253",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3}},{WT[0][0][-4]:.2f});')
J.append(f'tl.fromTo("#porthole",{{scale:1}},{{scale:9,duration:0.8,ease:"power3.in",immediateRender:false}},{S[1]-0.55:.2f});')
J.append(f'tl.to("#porthole",{{opacity:0,duration:0.2}},{S[1]+0.1:.2f});')
# roof: belt runs, crate rides into hatch and falls to the sorter hopper
J.append(f'tl.fromTo("#beltdash",{{x:0}},{{x:48*20,duration:{DUR},ease:"none"}},0);')
J.append(f'tl.fromTo("#gantry",{{y:-300}},{{y:0,duration:0.6,ease:"bounce.out"}},{S[1]+0.2:.2f});')
J.append(f'tl.fromTo("#smoke",{{y:0,opacity:.7}},{{y:-60,opacity:.2,duration:2.2,repeat:{int(DUR/2.2)},ease:"none"}},0);')
J.append(f'tl.set("#crate",{{x:-300,y:356}},0);')
J.append(f'tl.to("#crate",{{x:540,y:356,duration:2.0,ease:"none"}},{S[1]+0.3:.2f});')
J.append(f'tl.to("#crate",{{y:{FT(1)+250},duration:0.9,ease:"power2.in"}},{S[2]-0.6:.2f});')
J.append(f'tl.to("#crate",{{scale:0.4,opacity:0,duration:0.4}},{S[2]+0.5:.2f});')
# station lights (number circles fill) + plaque drops
for n, at in ((1, S[2] + 0.3), (2, S[3] + 0.3), (3, S[4] + 0.3), (4, S[5] + 0.3), (5, S[6] + 0.3), (6, S[7] + 0.3), (7, S[8] + 0.3)):
    J.append(f'tl.fromTo("#p{n}",{{y:-120,opacity:0}},{{y:0,opacity:1,duration:0.55,ease:"bounce.out"}},{at-0.25:.2f});')
    J.append(f'tl.to("#p{n}nf",{{attr:{{fill:"{OCH}"}},duration:0.05}},{at+0.3:.2f}); tl.fromTo("#p{n}n",{{scale:0.9,transformOrigin:"50% 50%"}},{{scale:1,duration:0.35,ease:"back.out(4)"}},{at+0.3:.2f});')
# sorter gear spins, chutes + tags
J.append(f'tl.fromTo("#sgear",{{rotation:0}},{{rotation:720,duration:{DUR},ease:"none"}},0);')
for i in range(4):
    J.append(f'tl.fromTo("#tag{i}",{{y:-200,opacity:0}},{{y:0,opacity:1,duration:0.5,ease:"bounce.out"}},{WT[2][1][min(i,len(WT[2][1])-1)]:.2f});')
# press stamps on a 0.5 s grid; gate STOP
pt = S[3] + 0.4; stamps = []
while pt < S[4]:
    J.append(f'tl.fromTo("#ram",{{y:0}},{{y:150,duration:0.12,ease:"power3.in",yoyo:true,repeat:1,immediateRender:false}},{pt:.2f});'); stamps.append(round(pt + 0.12, 3)); pt += 1.0
J.append(f'tl.fromTo("#stop",{{rotation:-80,transformOrigin:"712px {FT(2)+590}px"}},{{rotation:0,duration:0.4,ease:"back.out(3)"}},{P0[3][1]:.2f});')
J.append(f'tl.fromTo("#b2",{{scale:0.6,opacity:0,transformOrigin:"715px {FT(2)+310}px"}},{{scale:1,opacity:1,duration:0.45,ease:"back.out(2)"}},{P0[3][0]+1.2:.2f});')
J.append(f'tl.fromTo("#threeq",{{scale:0.4,opacity:0,transformOrigin:"460px {FT(2)+735}px"}},{{scale:1,opacity:1,duration:0.45,ease:"back.out(2.5)"}},{P0[3][3]:.2f});')
# fmcg belt, agri sieve, rollers
J.append(f'tl.fromTo("#packs",{{x:-300}},{{x:300,duration:{S[5]-S[4]+2:.2f},ease:"none"}},{S[4]-1:.2f});')
J.append(f'tl.fromTo("#b3",{{scale:0.6,opacity:0,transformOrigin:"710px {FT(3)+315}px"}},{{scale:1,opacity:1,duration:0.45,ease:"back.out(2)"}},{P0[4][1]:.2f});')
J.append(f'tl.fromTo("#sieve",{{x:-12}},{{x:12,duration:0.12,yoyo:true,repeat:{int((S[6]-S[5]+1)/0.12)},ease:"sine.inOut",immediateRender:false}},{S[5]-0.5:.2f});')
J.append(f'tl.fromTo("#grain",{{y:-30}},{{y:30,duration:0.6,repeat:{int((S[6]-S[5]+1)/0.6)},ease:"none",immediateRender:false}},{S[5]-0.5:.2f});')
J.append(f'tl.fromTo("#b4",{{scale:0.6,opacity:0,transformOrigin:"710px {FT(4)+315}px"}},{{scale:1,opacity:1,duration:0.45,ease:"back.out(2)"}},{WT[5][0][-3]:.2f});')
for i in range(3):
    J.append(f'tl.fromTo("#roll{i}",{{rotation:0}},{{rotation:{-1080 if i%2 else 1080},duration:{S[8]-S[6]+1:.2f},ease:"none"}},{S[6]-0.5:.2f});')
J.append(f'tl.fromTo("#b5",{{scale:0.6,opacity:0,transformOrigin:"430px {FT(5)+675}px"}},{{scale:1,opacity:1,duration:0.45,ease:"back.out(2)"}},{WT[6][0][6]:.2f});')
# hotels: hook drops, room lifts up and out to the right
J.append(f'tl.set("#hook",{{opacity:0}},0); tl.set("#hook",{{opacity:1}},{S[7]+0.2:.2f}); tl.fromTo("#hook",{{y:-700}},{{y:0,duration:0.8,ease:"power2.out",immediateRender:false}},{S[7]+0.2:.2f});')
J.append(f'tl.to(["#hotel","#hook"],{{x:520,y:-500,duration:1.8,ease:"power2.inOut"}},{S[7]+1.4:.2f});')
J.append(f'tl.fromTo("#hoteltag",{{opacity:0,y:-40}},{{opacity:1,y:0,duration:0.4,ease:"back.out(2)"}},{P0[7][1]:.2f});')
J.append(f'tl.to("#hoteltag",{{opacity:0,duration:0.3}},{S[8]-0.2:.2f});')
# vault
J.append(f'tl.fromTo("#wheel",{{rotation:0}},{{rotation:270,duration:1.2,ease:"power2.inOut"}},{S[8]+0.4:.2f});')
J.append(f'tl.fromTo("#vnum",{{opacity:0,scale:0.6,transformOrigin:"540px {FT(6)+755}px"}},{{opacity:1,scale:1,duration:0.45,ease:"back.out(2)"}},{WT[8][0][7]:.2f});')
# pull-back: nameplate, question card
J.append(f'tl.fromTo("#nameplate",{{opacity:0,y:-200}},{{opacity:1,y:0,duration:0.6,ease:"bounce.out"}},{S[9]+2.6:.2f});')
J.append(f'tl.fromTo("#qcard",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.45,ease:"back.out(2)"}},{P0[9][1]:.2f});')
J.append(f'tl.fromTo("#follow",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.4,ease:"back.out(3)"}},{P0[9][2]:.2f});')
JS = '\n'.join(J)

HTML = f'''<!doctype html><html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<title>ITC: the factory, cut open</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
@font-face{{font-family:"Big Shoulders Display";src:url("assets/fonts/big-shoulders-display-latin-900-normal.woff2") format("woff2");font-weight:900}}
@font-face{{font-family:"Archivo";src:url("assets/fonts/archivo-latin-800-normal.woff2") format("woff2");font-weight:800}}
@font-face{{font-family:"Poppins";src:url("assets/fonts/Poppins-Bold.ttf") format("truetype");font-weight:700 900}}
@font-face{{font-family:"NotoTamil";src:url("assets/fonts/noto-sans-tamil-tamil-800-normal.woff") format("woff");font-weight:800}}
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:1080px;height:1920px;overflow:hidden;background:{PAPER}}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:{PAPER}}}
#world{{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:0 0;overflow:visible}}
#world svg{{position:absolute;left:0;top:0;overflow:visible}}
#grain{{position:absolute;inset:0;z-index:40;pointer-events:none;mix-blend-mode:multiply;opacity:.35}}
#porthole{{position:absolute;inset:0;z-index:50;transform-origin:540px 900px}}
#handle{{position:absolute;right:40px;top:232px;z-index:60;padding:8px 20px;border:4px solid {INK};background:#FFF8E6;font:900 36px "Big Shoulders Display";color:{INK};box-shadow:6px 6px 0 {SH}}}
#prog{{position:absolute;left:40px;right:40px;top:206px;height:8px;background:rgba(28,31,43,.2);z-index:61;overflow:hidden}} #progf{{position:absolute;inset:0;background:{OCH};transform-origin:0 50%}}
#disc{{position:absolute;left:40px;right:40px;top:1530px;z-index:62;text-align:center;font:800 26px "Archivo";color:{INK};}}
#disc span{{background:rgba(255,248,230,.92);padding:4px 12px;border:2px solid {INK}}}
#qcard{{position:absolute;left:90px;right:90px;top:330px;z-index:55;padding:26px 30px;background:#FFF8E6;border:6px solid {INK};box-shadow:14px 14px 0 {SH};font:900 64px/1.05 "Big Shoulders Display";color:{INK};text-align:center;opacity:0}}
#follow{{position:absolute;left:260px;top:1350px;z-index:55;padding:12px 30px;background:{OCH};border:5px solid {INK};font:900 52px "Big Shoulders Display";color:{INK};opacity:0}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920" data-fps="24">
<div id="world" data-layout-ignore><svg width="1080" height="{BOTTOM+900}" viewBox="0 0 1080 {BOTTOM+900}">{WORLD}</svg></div>
<svg id="porthole" data-layout-ignore viewBox="0 0 1080 1920" width="1080" height="1920"><defs><mask id="ph"><rect width="1080" height="1920" fill="#fff"/><circle cx="540" cy="900" r="400" fill="#000"/></mask></defs>
<rect width="1080" height="1920" fill="{GROUND}" mask="url(#ph)"/>
<circle cx="540" cy="900" r="400" fill="{PAPER}"/>
<path id="chartline" d="{CHART}" fill="none" stroke="{VER}" stroke-width="12" stroke-linejoin="round" stroke-linecap="round" stroke-dasharray="2000" stroke-dashoffset="2000"/>
<g id="p409" opacity="0">{rect(200, 700, 240, 70, '#FFF8E6', 4, 3, 5)}{txt(320, 750, '₹409.5 HIGH', 40, INK, 'BS', 'middle')}</g>
<g id="p253" opacity="0">{rect(640, 1180, 250, 70, '#FFF8E6', 4, 3, 5)}{txt(765, 1230, '₹252.8 LOW', 40, VER, 'BS', 'middle')}</g>
{txt(540, 640, 'ITC SHARE · DEC 2025 – NOV 2026', 30, INK, 'AR', 'middle')}{txt(540, 1440, 'NSE via INDmoney, 23 Nov 2026', 28, '#FFF8E6', 'AR', 'middle')}
<circle cx="540" cy="900" r="400" fill="none" stroke="{INK}" stroke-width="14"/><circle cx="540" cy="900" r="430" fill="none" stroke="{BODY}" stroke-width="40"/>
<circle cx="540" cy="900" r="452" fill="none" stroke="{INK}" stroke-width="6"/>
{''.join(f'<circle cx="{540+430*math.cos(a*math.pi/6):.0f}" cy="{900+430*math.sin(a*math.pi/6):.0f}" r="7" fill="{INK}"/>' for a in range(12))}
</svg>
<svg id="grain" viewBox="0 0 1080 1920" data-layout-ignore><filter id="gn"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 .45  0 0 0 0 .4  0 0 0 0 .33  0 0 0 .55 0"/></filter><rect width="1080" height="1920" filter="url(#gn)"/></svg>
<div id="handle" data-layout-allow-overlap>@moneyincloud</div>
<div id="prog" data-layout-ignore><div id="progf"></div></div>
<div id="qcard" data-layout-allow-overlap>CAN THE NEW FLOORS CARRY THE OLD ONE?</div>
<div id="follow" data-layout-allow-overlap>FOLLOW @moneyincloud</div>
<div id="disc" data-layout-ignore><span>Not a buy/sell call. Education only.</span></div>
<audio id="vo" src="assets/mix.wav" data-start="0" data-duration="{DUR}" data-track-index="40" data-volume="1"></audio>
</div>
<script>
const tl = gsap.timeline({{paused:true}});
{JS}
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;
</script></body></html>'''
open(P + '/index.html', 'w').write(HTML)
json.dump(dict(DUR=DUR, STARTS=starts, VO=vos, P=P0, STAMPS=stamps), open(P + '/build/t.json', 'w'))
print('dur', DUR, 'starts', starts)
