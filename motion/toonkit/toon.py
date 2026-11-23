"""@moneyincloud "Chennai Toon" kit: original flat 2D characters + Chennai landmark backdrops, drawn as SVG.
All art is code-drawn and original (no copied characters, logos or downloaded images).
Characters: ARJUN (host: teal shirt, round specs, stubble) and KAVYA (magenta kurta, yellow dupatta, braid).
Landmarks: marina, tnagar, mylapore, central, ripon, napier, valluvar, metro, itpark.
Each character part has an id (<cid>-armR, -foreR, -armL, -foreL, -head, -eyes, -mo, -mc, -body) for toon.js."""
O = '#2a1810'   # outline ink
SW = 6

def _st(w=SW):
    return f'stroke="{O}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'

# ---------------------------------------------------------------- characters
def _arm(p, side, sleeve, skin, sleeve_len=78, cuff=None):
    """arm hanging down from shoulder; side 'R' at x~281 (viewer right), 'L' mirrored."""
    sx = 281 if side == 'R' else 119
    s = _st()
    fore_y = 470
    sl = f'<rect x="{sx-23}" y="342" width="46" height="{sleeve_len}" rx="22" fill="{sleeve}" {s}/>'
    up = f'<rect x="{sx-19}" y="{342+sleeve_len-14}" width="38" height="{fore_y-(342+sleeve_len-14)+16}" rx="18" fill="{skin}" {s}/>' if sleeve_len < 120 else ''
    cf = f'<rect x="{sx-22}" y="{342+sleeve_len-16}" width="44" height="14" rx="6" fill="{cuff}" {s}/>' if cuff else ''
    fore = (f'<g id="{p}-fore{side}" style="transform-origin:{sx}px {fore_y}px">'
            f'<rect x="{sx-19}" y="{fore_y-8}" width="38" height="112" rx="18" fill="{skin}" {s}/>'
            f'<circle cx="{sx}" cy="{fore_y+112}" r="25" fill="{skin}" {s}/>'
            f'<path d="M{sx-10} {fore_y+104} q10 8 20 0" fill="none" {_st(3)}/></g>')
    if sleeve_len >= 120:   # long sleeve covers part of forearm
        fore = fore.replace(f'fill="{skin}" {s}/>', f'fill="{sleeve}" {s}/>', 1)
    return f'<g id="{p}-arm{side}" style="transform-origin:{sx}px 352px">{up}{fore}{sl}{cf}</g>'


def _face(p, skin, mouth_open='#5b1b16', specs=False, lashes=False, stubble=None):
    s = _st()
    eyes = ''
    for ex in (168, 232):
        eyes += (f'<ellipse cx="{ex}" cy="222" rx="14" ry="16" fill="#fff" {_st(4)}/>'
                 f'<circle cx="{ex+2}" cy="225" r="7.5" fill="{O}"/><circle cx="{ex+4}" cy="222" r="2.4" fill="#fff"/>')
        if lashes:
            eyes += f'<path d="M{ex-16} 210 q16 -12 32 0" fill="none" {_st(5)}/>'
    g = ''
    if stubble:
        g += f'<path d="M124 232 Q130 312 200 316 Q270 312 276 232 Q262 292 200 296 Q138 292 124 232Z" fill="{stubble}" opacity=".55"/>'
    g += f'<g id="{p}-eyes" style="transform-origin:200px 222px">{eyes}</g>'
    g += (f'<path d="M150 192 q18 -10 36 -2" fill="none" {_st(7)}/><path d="M214 190 q18 -8 36 2" fill="none" {_st(7)}/>'
          f'<path d="M200 232 q-10 24 5 28" fill="none" {_st(4)}/>')
    if specs:
        g += (f'<circle cx="168" cy="224" r="27" fill="rgba(255,255,255,.12)" stroke="#1b1b1b" stroke-width="6"/>'
              f'<circle cx="232" cy="224" r="27" fill="rgba(255,255,255,.12)" stroke="#1b1b1b" stroke-width="6"/>'
              f'<path d="M195 222 q5 -5 10 0" fill="none" stroke="#1b1b1b" stroke-width="5"/>')
    g += (f'<path id="{p}-mc" d="M176 274 Q200 292 224 274" fill="none" {_st(5)}/>'
          f'<g id="{p}-mo" opacity="0"><path d="M174 268 Q200 312 226 268 Z" fill="{mouth_open}" {_st(5)}/>'
          f'<path d="M186 290 q14 -10 28 0 q-14 12 -28 0z" fill="#e0645a"/></g>')
    return g


def arjun(cid='arjun'):
    skin, shirt, shirt_d, pant = '#b9774c', '#169e91', '#0f7f75', '#2c3a62'
    s = _st()
    legs = (f'<rect x="146" y="566" width="52" height="292" rx="18" fill="{pant}" {s}/>'
            f'<rect x="202" y="566" width="52" height="292" rx="18" fill="{pant}" {s}/>'
            f'<path d="M134 858 q0 -26 34 -26 h30 q12 0 12 26 v14 h-76z" fill="#f4efe6" {s}/>'
            f'<path d="M190 858 q0 -26 34 -26 h30 q12 0 12 26 v14 h-76z" fill="#f4efe6" {s}/>'
            f'<path d="M134 866 h76 M190 866 h76" {_st(5)}/>')
    torso = (f'<path d="M126 350 Q200 322 274 350 L288 592 Q200 614 112 592 Z" fill="{shirt}" {s}/>'
             f'<path d="M236 340 Q262 344 274 350 L288 592 Q262 600 240 603 Z" fill="{shirt_d}" opacity=".7"/>'
             f'<path d="M168 338 L200 392 L232 338" fill="#f3f0e8" {s}/><path d="M170 336 l-6 34 l30 -6z M230 336 l6 34 l-30 -6z" fill="{shirt_d}" {_st(4)}/>'
             f'<path d="M200 392 V590" {_st(4)}/><circle cx="200" cy="430" r="5" fill="{O}"/><circle cx="200" cy="480" r="5" fill="{O}"/><circle cx="200" cy="530" r="5" fill="{O}"/>'
             f'<rect x="222" y="420" width="40" height="40" rx="6" fill="none" {_st(4)}/>'
             f'<rect x="114" y="580" width="172" height="22" rx="8" fill="#3b2a1e" {s}/><rect x="188" y="580" width="24" height="22" rx="4" fill="#d8b24a" {_st(4)}/>')
    head = (f'<rect x="180" y="286" width="40" height="56" rx="12" fill="{skin}" {s}/>'
            f'<circle cx="120" cy="228" r="18" fill="{skin}" {s}/><circle cx="280" cy="228" r="18" fill="{skin}" {s}/>'
            f'<ellipse cx="200" cy="216" rx="82" ry="94" fill="{skin}" {s}/>'
            + _face(cid, skin, specs=True, stubble='#6b3f22') +
            f'<path d="M116 214 Q104 104 200 100 Q298 102 286 208 Q276 162 246 150 Q222 178 186 150 Q156 172 128 166 Q120 186 116 214Z" fill="#1c120c" {s}/>'
            f'<path d="M150 118 q20 -14 44 -6 M214 112 q26 -6 44 12" fill="none" stroke="#3a2a20" stroke-width="5" stroke-linecap="round"/>')
    arms = _arm(cid, 'L', shirt, skin) + _arm(cid, 'R', shirt, skin)
    return (f'<svg class="chr" id="{cid}" viewBox="0 0 400 900"><g id="{cid}-body" style="transform-origin:200px 880px">'
            f'{legs}{torso}<g id="{cid}-head" style="transform-origin:200px 330px">{head}</g>{arms}</g></svg>')


def kavya(cid='kavya'):
    skin, kurta, kurta_d, gold, dup = '#9d6440', '#c2185b', '#97134a', '#f2b21b', '#f6c21c'
    s = _st()
    braid = ''.join(f'<ellipse cx="{262+i*3}" cy="{300+i*44}" rx="{22-i*1.6}" ry="28" fill="#1a110b" {_st(4)}/>' for i in range(7))
    braid += f'<path d="M272 600 l-8 22 h22z" fill="{gold}" {_st(4)}/>'
    legs = (f'<rect x="158" y="640" width="40" height="220" rx="14" fill="#efe1c6" {s}/>'
            f'<rect x="202" y="640" width="40" height="220" rx="14" fill="#efe1c6" {s}/>'
            f'<path d="M146 862 q0 -18 28 -18 h26 v24 h-54z" fill="#8a4b22" {s}/><path d="M200 862 q0 -18 28 -18 h26 v24 h-54z" fill="#8a4b22" {s}/>')
    torso = (f'<path d="M128 350 Q200 322 272 350 L300 708 Q200 728 100 708 Z" fill="{kurta}" {s}/>'
             f'<path d="M238 340 Q262 344 272 350 L300 708 Q270 716 244 718 Z" fill="{kurta_d}" opacity=".7"/>'
             f'<path d="M104 680 Q200 700 296 680 L300 708 Q200 728 100 708Z" fill="{gold}" {_st(4)}/>'
             + ''.join(f'<circle cx="{120+i*20}" cy="{694+(4 if i%2 else 0)}" r="3.5" fill="{kurta_d}"/>' for i in range(9)) +
             f'<path d="M174 338 Q200 372 226 338" fill="{kurta_d}" {_st(4)}/>'
             f'<path d="M126 352 Q150 340 174 340 L286 560 L262 590 Z" fill="{dup}" {s}/>'
             f'<path d="M150 360 L268 572" stroke="#d49a0c" stroke-width="5" stroke-dasharray="10 12"/>')
    head = (f'<rect x="182" y="286" width="36" height="56" rx="12" fill="{skin}" {s}/>'
            f'<circle cx="120" cy="230" r="17" fill="{skin}" {s}/><circle cx="280" cy="230" r="17" fill="{skin}" {s}/>'
            f'<circle cx="120" cy="262" r="10" fill="{gold}" {_st(4)}/><circle cx="280" cy="262" r="10" fill="{gold}" {_st(4)}/>'
            f'<ellipse cx="200" cy="218" rx="80" ry="92" fill="{skin}" {s}/>'
            + _face(cid, skin, lashes=True) +
            f'<circle cx="200" cy="176" r="6" fill="#d7263d"/>'
            f'<path d="M114 226 Q100 104 200 100 Q300 104 286 226 Q284 160 252 140 Q226 132 202 146 Q176 130 150 140 Q118 160 114 226Z" fill="#1a110b" {s}/>'
            f'<path d="M200 104 V146" stroke="#3a2a20" stroke-width="4"/>'
            f'<circle cx="252" cy="122" r="12" fill="#fff" {_st(3)}/><circle cx="266" cy="132" r="9" fill="#fff" {_st(3)}/>')
    arms = _arm(cid, 'L', kurta, skin, sleeve_len=120, cuff=gold) + _arm(cid, 'R', kurta, skin, sleeve_len=120, cuff=gold)
    return (f'<svg class="chr" id="{cid}" viewBox="0 0 400 900"><g id="{cid}-body" style="transform-origin:200px 880px">'
            f'<g id="{cid}-braid">{braid}</g>{legs}{torso}<g id="{cid}-head" style="transform-origin:200px 330px">{head}</g>{arms}</g></svg>')


CHARS = {'arjun': arjun, 'kavya': kavya}

# ---------------------------------------------------------------- landmark helpers
def _sky(c1, c2, c3=None, sid='sky'):
    stops = f'<stop offset="0" stop-color="{c1}"/><stop offset=".6" stop-color="{c2}"/>' + (f'<stop offset="1" stop-color="{c3}"/>' if c3 else '')
    return f'<defs><linearGradient id="{sid}" x1="0" y1="0" x2="0" y2="1">{stops}</linearGradient></defs><rect width="1080" height="1920" fill="url(#{sid})"/>'


def _clouds(y, col='#fff', op=.75, xs=(120, 520, 860)):
    out = ''
    for i, x in enumerate(xs):
        yy = y + (i % 2) * 70
        out += (f'<g opacity="{op}" fill="{col}"><ellipse cx="{x}" cy="{yy}" rx="110" ry="34"/><ellipse cx="{x-50}" cy="{yy-18}" rx="60" ry="40"/>'
                f'<ellipse cx="{x+40}" cy="{yy-26}" rx="70" ry="46"/></g>')
    return out


def _skyline(y, col, seed=1, h=260, lit=None):
    import random
    r = random.Random(seed); x = -20; out = ''
    while x < 1100:
        w = r.randint(70, 150); hh = r.randint(int(h * .4), h)
        out += f'<rect x="{x}" y="{y-hh}" width="{w}" height="{hh+40}" fill="{col}"/>'
        if lit:
            for wy in range(y - hh + 20, y - 10, 34):
                for wx in range(x + 12, x + w - 16, 26):
                    if r.random() < .38:
                        out += f'<rect x="{wx}" y="{wy}" width="12" height="16" fill="{lit}" opacity=".85"/>'
        x += w + r.randint(4, 18)
    return out


def _stars(n=60, seed=3, ymax=900):
    import random
    r = random.Random(seed)
    return ''.join(f'<circle cx="{r.randint(0,1080)}" cy="{r.randint(0,ymax)}" r="{r.choice([1.5,2,2.5,3])}" fill="#fff" opacity="{r.uniform(.4,.95):.2f}"/>' for _ in range(n))


def _ground(y, col, top=None):
    g = f'<rect x="0" y="{y}" width="1080" height="{1920-y}" fill="{col}"/>'
    if top:
        g += f'<rect x="0" y="{y}" width="1080" height="18" fill="{top}"/>'
    return g


def _bunting(y, cols=('#e63946', '#f6c21c', '#2a9d8f', '#ff7aa8', '#4361ee'), sag=60):
    out = f'<path d="M-20 {y} Q540 {y+sag} 1100 {y}" fill="none" stroke="#3a2a20" stroke-width="4"/>'
    for i in range(22):
        x = -10 + i * 52; t = (x + 20) / 1120; yy = y + 4 * sag * t * (1 - t)
        out += f'<path d="M{x} {yy:.0f} l40 2 l-22 44z" fill="{cols[i%len(cols)]}" {_st(3)}/>'
    return out


def _road(y, col='#5b5f6b'):
    out = f'<rect x="0" y="{y}" width="1080" height="{1920-y}" fill="{col}"/><rect x="0" y="{y}" width="1080" height="20" fill="#c9c2b3"/>'
    out += ''.join(f'<rect x="{x}" y="{y+210}" width="90" height="14" fill="#f1e9d8" opacity=".8"/>' for x in range(20, 1080, 170))
    return out


def _auto(x, y, s=1.0):
    st = _st(5)
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M0 120 L10 30 Q20 0 70 0 H150 Q180 0 186 40 L196 120Z" fill="#f2c318" {st}/>'
            f'<path d="M0 60 H196" stroke="#1d1d1d" stroke-width="22"/><path d="M30 20 H150 L160 58 H24Z" fill="#9fd3e6" {st}/>'
            f'<rect x="-6" y="110" width="210" height="22" rx="8" fill="#1d1d1d"/>'
            f'<circle cx="34" cy="140" r="24" fill="#222" {st}/><circle cx="34" cy="140" r="9" fill="#bbb"/>'
            f'<circle cx="170" cy="140" r="24" fill="#222" {st}/><circle cx="170" cy="140" r="9" fill="#bbb"/></g>')


def _tree(x, y, s=1.0, c='#3c9a4a'):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-12" y="-10" width="24" height="120" fill="#7a4a26" {_st(5)}/>'
            f'<circle cx="0" cy="-60" r="70" fill="{c}" {_st(5)}/><circle cx="-50" cy="-20" r="46" fill="{c}" {_st(5)}/><circle cx="50" cy="-24" r="50" fill="{c}" {_st(5)}/></g>')


def _palm(x, y, s=1.0):
    fr = ''.join(f'<path d="M0 -300 q{dx} {dy} {dx*2} {dy*1.6}" fill="none" stroke="#2f8a3c" stroke-width="22" stroke-linecap="round"/>'
                 for dx, dy in ((-90, 10), (90, 10), (-60, -40), (60, -40), (-100, 60), (100, 60)))
    return f'<g transform="translate({x} {y}) scale({s})"><path d="M-10 0 Q-30 -150 0 -300 L14 -300 Q-10 -150 12 0Z" fill="#8a5a2b" {_st(5)}/>{fr}</g>'


# ---------------------------------------------------------------- landmarks (1080x1920)
def marina():
    lh = ''.join(f'<path d="M{790+i*6} {560+i*100} h{100-i*12} l6 100 h-{112-i*12}z" fill="{"#d7263d" if i%2==0 else "#fbf6ec"}"/>' for i in range(6))
    return (_sky('#ff8a5b', '#ffc38a', '#ffe1b0', 'skyM') + _clouds(300, '#ffe6d0', .7) +
            '<g id="far"><circle cx="300" cy="1060" r="120" fill="#fff0b8"/><circle cx="300" cy="1060" r="170" fill="#fff0b8" opacity=".25"/>'
            '<rect x="0" y="1060" width="1080" height="240" fill="#3f8fb8"/>'
            + ''.join(f'<rect x="{x}" y="{y}" width="{w}" height="6" rx="3" fill="#bfe6f5" opacity=".7"/>' for x, y, w in
                      ((80, 1100, 160), (420, 1130, 220), (760, 1090, 140), (220, 1180, 260), (640, 1210, 200), (40, 1250, 180)))
            + '<rect x="0" y="1060" width="1080" height="12" fill="#fff6dc" opacity=".6"/></g>'
            f'<g id="mid"><path d="M770 1180 L800 520 H880 L910 1180Z" fill="#fbf6ec" {_st()}/>{lh}'
            f'<rect x="806" y="470" width="68" height="60" fill="#3a3a3a" {_st()}/><rect x="814" y="480" width="52" height="40" fill="#ffe38a"/>'
            f'<path d="M796 470 L840 420 L884 470Z" fill="#d7263d" {_st()}/>'
            f'<path d="M770 1180 L800 520 H880 L910 1180Z" fill="none" {_st()}/></g>'
            f'<g id="near"><path d="M0 1260 Q540 1220 1080 1270 V1920 H0Z" fill="#f2cc8f"/>'
            f'<g transform="translate(70 1240)"><rect x="0" y="80" width="230" height="110" rx="10" fill="#2a9d8f" {_st(5)}/>'
            f'<rect x="-10" y="40" width="250" height="44" rx="8" fill="#f6c21c" {_st(5)}/>'
            f'<text x="115" y="72" text-anchor="middle" font-family="Oswald" font-size="30" fill="#2a1810">ELANEER · 40</text>'
            + ''.join(f'<circle cx="{30+i*42}" cy="70" r="22" fill="#4caf50" {_st(4)}/>' for i in range(0)) +
            ''.join(f'<circle cx="{38+i*38}" cy="{128+(i%2)*14}" r="20" fill="#5bb04a" {_st(4)}/>' for i in range(5)) +
            f'<circle cx="40" cy="200" r="22" fill="#333"/><circle cx="190" cy="200" r="22" fill="#333"/></g>'
            f'<path d="M760 1300 l120 -60 l20 30z" fill="#e63946" {_st(4)}/><path d="M880 1240 Q960 1140 1000 1000" fill="none" stroke="#fff" stroke-width="2"/></g>')


def tnagar():
    shops = ''
    cols = ['#f4a261', '#e9c46a', '#8ecae6', '#ffafcc', '#90be6d', '#cdb4db']
    names = ['SILKS', 'THANGAM JEWELLERY', 'SWEETS', 'TEXTILES', 'BANGLES', 'MOBILES']
    xs = [-30, 160, 520, 700, 880, 1060]
    for i, (x, w) in enumerate(((-30, 190), (160, 360), (520, 180), (700, 180), (880, 230))):
        h = 520 if i == 1 else 420 + (i % 2) * 60
        top = 1180 - h
        c = '#f2c94c' if i == 1 else cols[i]
        shops += (f'<rect x="{x}" y="{top}" width="{w}" height="{h}" fill="{c}" {_st()}/>'
                  + ''.join(f'<rect x="{x+18+j*((w-36)//3)}" y="{top+120}" width="{(w-36)//3-14}" height="70" fill="#fff7e0" {_st(4)}/>' for j in range(3))
                  + f'<rect x="{x+10}" y="{top+30}" width="{w-20}" height="66" rx="8" fill="{"#7b1e1e" if i==1 else "#2a1810"}" {_st(4)}/>'
                  f'<text x="{x+w/2}" y="{top+76}" text-anchor="middle" font-family="Oswald" font-size="{34 if i==1 else 28}" fill="{"#ffd166" if i==1 else "#fff"}">{names[i]}</text>'
                  f'<rect x="{x+20}" y="{1180-220}" width="{w-40}" height="220" fill="#3a2a20" opacity=".85"/>'
                  f'<path d="M{x} {1180-250} h{w} l-14 40 h-{w-28}z" fill="{"#c1121f" if i%2 else "#fff"}" {_st(4)}/>')
    shops += ''.join(f'<path d="M{x} {930} h{w} l-14 40 h-{w-28}z" fill="none" stroke="#c1121f" stroke-width="10" stroke-dasharray="20 20"/>'
                     for x, w in ((160, 360),))
    return (_sky('#7ec8f0', '#c8ecff', None, 'skyT') + _clouds(260) +
            f'<g id="far">{_skyline(800, "#a9c7d8", 7, 300)}</g>'
            f'<g id="mid">{shops}{_bunting(470)}{_bunting(590, sag=36)}</g>'
            f'<g id="near">{_road(1180, "#6a6e78")}{_auto(780, 1250, 1.15)}</g>')


def mylapore():
    tiers = ''
    cols = ['#e76f51', '#2a9d8f', '#f4a261', '#e9c46a', '#8ab17d', '#ef476f', '#118ab2']
    base_w, y = 560, 1150
    for i in range(8):
        w = base_w - i * 58; h = 86 - i * 3
        x = 540 - w / 2
        tiers += f'<path d="M{x} {y} L{x+14} {y-h} H{x+w-14} L{x+w} {y}Z" fill="{cols[i%len(cols)]}" {_st(5)}/>'
        n = max(3, int(w // 52))
        for j in range(n):
            fx = x + 22 + j * (w - 44) / (n - 1) - 12 if n > 1 else 540
            tiers += f'<rect x="{fx:.0f}" y="{y-h+16}" width="24" height="{h-28}" rx="10" fill="{cols[(i+j+2)%len(cols)]}" {_st(3)}/>'
        y -= h
    top = (f'<path d="M{540-140} {y} Q540 {y-130} {540+140} {y}Z" fill="#e9c46a" {_st(5)}/>'
           + ''.join(f'<path d="M{540+dx-10} {y-60+abs(dx)*0.25} q10 -40 20 0z" fill="#f6c21c" {_st(3)}/>' for dx in (-90, -45, 0, 45, 90)))
    return (_sky('#ff9e7a', '#ffd3a5', '#fff0d0', 'skyY') + _clouds(240, '#fff2e2', .6) +
            f'<g id="far">{_skyline(1150, "#e7b98f", 4, 220)}</g>'
            f'<g id="mid"><rect x="210" y="1120" width="660" height="70" fill="#f1e3c8" {_st()}/>{tiers}{top}</g>'
            f'<g id="near">{_ground(1180, "#d9b38c", "#c79a6b")}'
            f'<rect x="0" y="1300" width="1080" height="30" fill="#c79a6b" opacity=".6"/><rect x="0" y="1400" width="1080" height="30" fill="#c79a6b" opacity=".5"/>'
            f'<g transform="translate(760 1190)"><rect x="0" y="60" width="240" height="110" rx="10" fill="#7b2cbf" {_st(5)}/>'
            + ''.join(f'<circle cx="{30+i*30}" cy="{50+(i%3)*8}" r="16" fill="{["#ff8fab","#ffd166","#fff"][i%3]}" {_st(3)}/>' for i in range(7)) +
            f'<text x="120" y="130" text-anchor="middle" font-family="Oswald" font-size="30" fill="#fff">POO KADAI</text></g></g>')


def central():
    red, trim = '#c0392b', '#f6ead4'
    wing = lambda x, w: (f'<rect x="{x}" y="820" width="{w}" height="380" fill="{red}" {_st()}/>'
                         + ''.join(f'<path d="M{x+20+j*60} 1190 v-120 q24 -34 48 0 v120z" fill="{trim}" {_st(4)}/>' for j in range(int((w-30)//60)))
                         + ''.join(f'<path d="M{x+20+j*60} 1010 v-110 q24 -34 48 0 v110z" fill="{trim}" {_st(4)}/>' for j in range(int((w-30)//60)))
                         + f'<rect x="{x-10}" y="800" width="{w+20}" height="30" fill="{trim}" {_st(4)}/>')
    tower = (f'<rect x="460" y="420" width="160" height="780" fill="{red}" {_st()}/>'
             f'<rect x="450" y="400" width="180" height="30" fill="{trim}" {_st(4)}/>'
             f'<path d="M455 400 L540 250 L625 400Z" fill="{red}" {_st()}/><path d="M540 250 V200" {_st(5)}/>'
             f'<circle cx="540" cy="520" r="62" fill="#fffdf6" {_st()}/><path d="M540 520 V476 M540 520 L572 532" {_st(6)}/>'
             + ''.join(f'<path d="M490 {660+k*150} v-90 q50 -50 100 0 v90z" fill="{trim}" {_st(4)}/>' for k in range(3)))
    side = lambda x: (f'<rect x="{x}" y="640" width="90" height="200" fill="{red}" {_st()}/><path d="M{x-6} 640 L{x+45} 560 L{x+96} 640Z" fill="{trim}" {_st(5)}/>')
    return (_sky('#6ec6ff', '#cdefff', None, 'skyC') + _clouds(260) +
            f'<g id="far">{_skyline(900, "#b9d6e6", 11, 260)}</g>'
            f'<g id="mid">{wing(40, 400)}{wing(640, 400)}{side(60)}{side(930)}{tower}</g>'
            f'<g id="near">{_road(1200)}{_auto(90, 1260, 1.05)}</g>')


def ripon():
    w, trim = '#fbfaf5', '#d8d2c2'
    body = (f'<rect x="60" y="760" width="960" height="430" fill="{w}" {_st()}/>'
            + ''.join(f'<rect x="{90+j*78}" y="{r}" width="44" height="86" rx="20" fill="#9cc3d5" {_st(4)}/>' for j in range(12) for r in (800, 930, 1060))
            + f'<rect x="40" y="740" width="1000" height="30" fill="{trim}" {_st(4)}/>')
    tower = (f'<rect x="440" y="420" width="200" height="420" fill="{w}" {_st()}/><circle cx="540" cy="520" r="64" fill="#fff" {_st()}/>'
             f'<path d="M540 520 V474 M540 520 L574 536" {_st(6)}/>'
             f'<path d="M430 420 Q540 300 650 420Z" fill="{w}" {_st()}/><rect x="520" y="300" width="40" height="40" fill="{w}" {_st(4)}/>'
             f'<path d="M540 300 V250" {_st(5)}/><circle cx="540" cy="246" r="8" fill="#f6c21c" {_st(3)}/>')
    domes = ''.join(f'<rect x="{x}" y="660" width="80" height="100" fill="{w}" {_st()}/><path d="M{x-6} 660 Q{x+40} 600 {x+86} 660Z" fill="{w}" {_st()}/>' for x in (60, 940))
    return (_sky('#5fb8f5', '#d3f0ff', None, 'skyR') + _clouds(240) +
            f'<g id="far">{_tree(140, 820, 1.1)}{_tree(960, 830, 1.2)}</g>'
            f'<g id="mid">{body}{domes}{tower}</g>'
            f'<g id="near">{_ground(1190, "#6dbb5a", "#4e9a42")}<rect x="380" y="1190" width="320" height="730" fill="#d9cdb3"/></g>')


def napier():
    arches = ''
    for i in range(6):
        x = -60 + i * 210
        arches += (f'<path d="M{x} 1040 Q{x+105} 860 {x+210} 1040" fill="none" stroke="#d9d3ee" stroke-width="16"/>'
                   f'<path d="M{x+30} 1040 V{1040-0} M{x+60} 1040 V985 M{x+105} 1040 V950 M{x+150} 1040 V985" stroke="#d9d3ee" stroke-width="5"/>'
                   f'<path d="M{x} 1040 Q{x+105} 860 {x+210} 1040" fill="none" stroke="{["#ff4fa3","#4cc9f0","#ffd166"][i%3]}" stroke-width="8" stroke-dasharray="2 18" stroke-linecap="round"/>')
    return (_sky('#140f3d', '#3b2a78', '#7a3d8f', 'skyN') + _stars() +
            f'<g id="far"><circle cx="860" cy="300" r="70" fill="#fff4c8"/><circle cx="860" cy="300" r="120" fill="#fff4c8" opacity=".15"/>'
            f'{_skyline(980, "#24184f", 9, 380, lit="#ffd166")}</g>'
            f'<g id="mid"><rect x="0" y="1040" width="1080" height="40" fill="#2b1d4f"/>{arches}'
            + ''.join(f'<rect x="{x}" y="1080" width="30" height="120" fill="#2b1d4f"/>' for x in range(30, 1080, 210)) + '</g>'
            f'<g id="near"><rect x="0" y="1180" width="1080" height="740" fill="#1c2a5c"/>'
            + ''.join(f'<rect x="{x}" y="{y}" width="{w}" height="6" rx="3" fill="{c}" opacity=".55"/>' for x, y, w, c in
                      ((60, 1230, 200, '#ff4fa3'), (420, 1260, 160, '#4cc9f0'), (760, 1240, 220, '#ffd166'), (200, 1320, 260, '#4cc9f0'), (620, 1350, 180, '#ff4fa3')))
            + '<rect x="0" y="1480" width="1080" height="440" fill="#3a3550"/><rect x="0" y="1480" width="1080" height="16" fill="#8a84a8"/></g>')


def valluvar():
    st = _st()
    wheels = ''.join(f'<g><circle cx="{x}" cy="1110" r="80" fill="#cbb79a" {st}/><circle cx="{x}" cy="1110" r="22" fill="#a8916f" {st}/>'
                     + ''.join(f'<path d="M{x} 1110 l{80*__import__("math").cos(a*0.785):.0f} {80*__import__("math").sin(a*0.785):.0f}" {_st(5)}/>' for a in range(8))
                     + '</g>' for x in (330, 750))
    body = (f'<rect x="250" y="900" width="580" height="160" fill="#d9c7a7" {st}/>'
            + ''.join(f'<rect x="{280+j*70}" y="925" width="40" height="110" fill="#bfa882" {_st(4)}/>' for j in range(8))
            + f'<rect x="320" y="640" width="440" height="260" fill="#e2d2b4" {st}/>'
            + ''.join(f'<rect x="{350+j*90}" y="660" width="34" height="240" fill="#c7b08a" {_st(4)}/>' for j in range(5))
            + f'<path d="M300 640 L540 440 L780 640Z" fill="#d6c3a0" {st}/><path d="M440 520 Q540 400 640 520" fill="#cfb98f" {st}/>'
            f'<path d="M540 440 V380" {_st(6)}/><circle cx="540" cy="370" r="14" fill="#f6c21c" {_st(4)}/>')
    horses = ''.join(f'<path d="M{x} 1060 l40 -120 q30 -30 60 0 l-10 40 l30 80z" fill="#d9c7a7" {st}/>' for x in (140, 880))
    return (_sky('#ff7e5f', '#feb47b', '#ffe0b5', 'skyV') + _clouds(220, '#ffe9d6', .6) +
            f'<g id="far">{_skyline(1000, "#e59c6f", 5, 260)}<circle cx="880" cy="760" r="90" fill="#fff1c1" opacity=".9"/></g>'
            f'<g id="mid" transform="translate(0 -120)">{body}{wheels}{horses}<rect x="200" y="1190" width="680" height="60" fill="#cdb38c" {st}/></g>'
            f'<g id="near">{_ground(1130, "#e8c99b", "#c9a679")}{_palm(80, 1300, 1.0)}{_palm(1010, 1320, 1.1)}</g>')


def metro():
    st = _st()
    train = (f'<g id="train"><rect x="60" y="780" width="1100" height="250" rx="40" fill="#f4f6fa" {st}/>'
             f'<rect x="60" y="960" width="1100" height="34" fill="#1d6fd1"/><rect x="60" y="800" width="1100" height="18" fill="#1d6fd1"/>'
             + ''.join(f'<rect x="{110+j*170}" y="840" width="120" height="100" rx="14" fill="#2b3d55" {_st(4)}/>' for j in range(6))
             + f'<text x="560" y="1022" text-anchor="middle" font-family="Oswald" font-size="30" fill="#fff">CHENNAI METRO</text></g>')
    return (_sky('#ff7aa8', '#b07ad6', '#6a4bb0', 'skyMe') + _stars(25, 9, 500) +
            f'<g id="far">{_skyline(900, "#6e4a9e", 13, 320, lit="#ffd166")}</g>'
            f'<g id="mid"><rect x="0" y="560" width="1080" height="40" fill="#3a2d5c"/>{train}'
            f'<rect x="0" y="1030" width="1080" height="60" fill="#c9c2d9" {st}/><rect x="0" y="1040" width="1080" height="14" fill="#f6c21c"/>'
            + ''.join(f'<rect x="{x}" y="600" width="44" height="430" fill="#8f86ad" {_st(4)}/>' for x in (40, 520, 1000))
            + f'<rect x="340" y="610" width="400" height="90" rx="14" fill="#1d6fd1" {st}/>'
            f'<text x="540" y="672" text-anchor="middle" font-family="Oswald" font-size="46" fill="#fff">METRO STATION</text></g>'
            f'<g id="near">{_ground(1090, "#a99fbf", "#8a80a3")}</g>')


def itpark():
    st = _st()
    towers = ''
    for x, w, h in ((40, 220, 640), (290, 260, 760), (580, 200, 580), (810, 240, 700)):
        towers += f'<rect x="{x}" y="{1180-h}" width="{w}" height="{h}" fill="#5fb3c9" {st}/>'
        towers += ''.join(f'<rect x="{x+14}" y="{y}" width="{w-28}" height="22" fill="#bfe8f2" opacity=".8"/>' for y in range(1180 - h + 30, 1160, 54))
    return (_sky('#7fd0ff', '#e2f6ff', None, 'skyI') + _clouds(220) +
            f'<g id="far">{_skyline(900, "#b6dbe8", 17, 300)}</g><g id="mid">{towers}'
            f'<rect x="330" y="{1180-800}" width="180" height="60" rx="10" fill="#2a1810"/>'
            f'<text x="420" y="{1180-758}" text-anchor="middle" font-family="Oswald" font-size="34" fill="#fff">IT PARK</text></g>'
            f'<g id="near">{_road(1180)}</g>')


LANDMARKS = {
    'marina': (marina, 'MARINA BEACH · CHENNAI'), 'tnagar': (tnagar, 'T. NAGAR · CHENNAI'),
    'mylapore': (mylapore, 'MYLAPORE · CHENNAI'), 'central': (central, 'CHENNAI CENTRAL'),
    'ripon': (ripon, 'RIPON BUILDING · CHENNAI'), 'napier': (napier, 'NAPIER BRIDGE · CHENNAI'),
    'valluvar': (valluvar, 'VALLUVAR KOTTAM · CHENNAI'), 'metro': (metro, 'CHENNAI METRO'),
    'itpark': (itpark, 'OMR IT CORRIDOR · CHENNAI'),
}


def backdrop(name):
    fn, label = LANDMARKS[name]
    return f'<svg class="bgsvg" data-layout-ignore viewBox="0 0 1080 1920" preserveAspectRatio="xMidYMid slice">{fn()}</svg>', label


def place(char, cid, x, y=930, h=860, flip=False):
    """character html placed at left x, top y, height h (px)."""
    svg = CHARS[char](cid)
    return f'<div class="chrw" id="{cid}w" style="left:{x}px;top:{y}px;height:{h}px;width:{h*400/900:.0f}px;{"transform:scaleX(-1);" if flip else ""}">{svg}</div>'
