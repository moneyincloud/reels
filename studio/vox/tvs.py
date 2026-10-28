"""TVS Motor Q2 FY27 results — last year vs this year, products, revenue sources, world map (paper Vox, no captions)"""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs, warn_icon
from fridge import follow_btn
import tea as TEA
import saveshare as SS

SH = ROOT + 'tvs/'
SCRIPT = json.load(open(SH + 'script.json'))
DURS = json.load(open(SH + 'vo/durs.json'))
LEAD, TAIL = 0.15, 0.3
STARTS, VO = [], []
_t = 0.0
for i, d in enumerate(DURS):
    STARTS.append(_t); VO.append(_t + (0.1 if i == 0 else LEAD)); _t = VO[-1] + d + TAIL
DUR = _t + 1.8
B = STARTS[1:]
SOFT = (253, 251, 246); NAVY = (30, 60, 120); BLUE = (40, 100, 200); GREY = (120, 116, 108); GOLD = (214, 160, 40)
PINK = (230, 90, 140); TEAL = (20, 140, 130); ORG = (230, 120, 30); PURP = (120, 70, 200)
card_box = TEA.card_box; label = TEA.label
CLOSES = json.load(open(SH + 'closes.json'))


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def pp(t, t0, d=0.35, s=1.6): return eback(prog(t, t0, d), s)


def src(c, t, txt, t0, y=1700, col=GREY):
    if t > t0: place_text(c, txt, 'type', 26, col, 540, y, t, None, t0, 'fade', track=1)


def fmt_in(v):
    v = int(round(v)); s = str(v)
    if len(s) > 3:
        h, t3 = s[:-3], s[-3:]; parts = []
        while len(h) > 2: parts.insert(0, h[-2:]); h = h[:-2]
        if h: parts.insert(0, h)
        s = ','.join(parts) + ',' + t3
    return s


# ---------------- world map ----------------
LON0, LON1, LAT0, LAT1 = -112, 150, -42, 64
MW = 1000; MH = int(MW * (LAT1 - LAT0) / (LON1 - LON0) * 1.12)
REG = {
    'asia': ['Nepal', 'Sri Lanka', 'Bangladesh', 'Indonesia', 'Philippines'],
    'africa': ['Morocco', 'Egypt', 'Kenya', 'South Africa', 'United Arab Emirates'],
    'latam': ['Mexico', 'Colombia', 'Honduras', 'Panama'],
    'europe': ['United Kingdom', 'France', 'Italy', 'Spain', 'Portugal'],
}
RCOL = {'asia': TEAL, 'africa': ORG, 'latam': PINK, 'europe': BLUE}
PINS = {  # label, lon, lat, region, label offset
    'India': (78.5, 22, 'home', (0, 0)), 'Nepal': (84, 28.3, 'asia', (-10, -34)), 'Sri Lanka': (80.7, 7.8, 'asia', (0, 28)),
    'Bangladesh': (90.3, 23.8, 'asia', (62, -18)), 'Indonesia': (113, -2.5, 'asia', (0, 34)), 'Philippines': (122, 12, 'asia', (10, -30)),
    'Singapore': (103.8, 1.35, 'asia', (-70, 4)),
    'Mexico': (-102, 23.5, 'latam', (0, -32)), 'Honduras': (-86.5, 14.8, 'latam', (60, -18)), 'Panama': (-80, 8.6, 'latam', (60, 6)), 'Colombia': (-74, 4, 'latam', (40, 32)),
    'Morocco': (-6.5, 31.8, 'africa', (-60, 18)), 'Egypt': (30, 26.8, 'africa', (0, -30)), 'UAE': (54.3, 24, 'africa', (0, 30)),
    'Kenya': (37.9, 0.4, 'africa', (-60, 8)), 'South Africa': (24, -29, 'africa', (0, 32)),
    'UK': (-2, 53.5, 'europe', (-40, -24)), 'France': (2.4, 46.6, 'europe', (-56, 4)), 'Italy': (12.5, 42.8, 'europe', (48, -6)),
    'Spain': (-3.7, 40.2, 'europe', (-40, 22)), 'Portugal': (-8.2, 39.6, 'europe', (-70, 0)),
}
PLANTS = [('Hosur', 77.8, 12.7), ('Mysuru', 76.6, 12.3), ('Nalagarh', 76.7, 31.0), ('Karawang', 107.3, -6.3), ('Solihull', -1.8, 52.4)]


def proj(lon, lat):
    return (lon - LON0) / (LON1 - LON0) * MW, (LAT1 - lat) / (LAT1 - LAT0) * MH


@functools.lru_cache(maxsize=1)
def world():
    d = json.load(open(SH + 'world.geojson')); out = []
    for f in d['features']:
        nm = f['properties']['NAME']; g = f['geometry']
        polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        out.append((nm, [[proj(x, y) for x, y in poly[0]] for poly in polys]))
    return out


@functools.lru_cache(maxsize=32)
def map_img(regs=()):
    S = 2; im = Image.new('RGBA', (MW * S, MH * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    lit = {n: RCOL[r] for r in regs for n in REG[r]}
    for nm, polys in world():
        col = NAVY if nm == 'India' else lit.get(nm, (214, 207, 192))
        for pts in polys:
            if len(pts) < 3: continue
            P = [(x * S, y * S) for x, y in pts]
            d.polygon(P, fill=col); d.line(P + [P[0]], fill=(150, 142, 128) if col == (214, 207, 192) else INK, width=2 if col == (214, 207, 192) else 3)
    return im.resize((MW, MH), Image.LANCZOS)


def arc_pts(a, b, k=0.25, n=30):
    (x0, y0), (x1, y1) = a, b; mx, my = (x0 + x1) / 2, (y0 + y1) / 2; dx, dy = x1 - x0, y1 - y0
    cx, cy = mx + dy * k, my - abs(dx) * k * 0.6 - 30
    return [((1 - u) ** 2 * x0 + 2 * (1 - u) * u * cx + u * u * x1, (1 - u) ** 2 * y0 + 2 * (1 - u) * u * cy + u * u * y1) for u in np.linspace(0, 1, n)]


def draw_map(c, t, ox, oy, regs, reg_times, labels=True, arrows=True, plants_t=None):
    """regs: tuple of lit regions; reg_times: {region: t0}"""
    c.alpha_composite(map_img(tuple(r for r in regs if t > reg_times.get(r, 0))), (ox, oy))
    d = ImageDraw.Draw(c)
    hx, hy = proj(*PINS['India'][:2]); hx += ox; hy += oy
    for nm, (lon, lat, r, off) in PINS.items():
        if r == 'home': continue
        t0 = reg_times.get(r)
        if t0 is None or t < t0: continue
        k = list(n for n, v in PINS.items() if v[2] == r).index(nm); tk = t0 + 0.12 * k
        if t < tk: continue
        x, y = proj(lon, lat); x += ox; y += oy
        if arrows:
            q = eio(prog(t, tk, 0.6)); pts = arc_pts((hx, hy), (x, y))
            m = max(2, int(len(pts) * q)); stroke(c, pts[:m], 4, RCOL[r])
        p = pp(t, tk + 0.4, 0.3)
        if t > tk + 0.4:
            rr = 11 * p; d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=RCOL[r], outline=INK, width=3)
            if labels and p > 0.5 and nm not in ('France', 'Spain', 'Portugal', 'Italy', 'Honduras', 'Panama', 'Singapore'):
                place(c, text_img(nm.upper(), 'osw5', 24, INK), x + off[0], y + off[1])
    pul = 1 + 0.25 * math.sin(t * 6)
    d.ellipse((hx - 16 * pul, hy - 16 * pul, hx + 16 * pul, hy + 16 * pul), outline=RED, width=4)
    d.ellipse((hx - 11, hy - 11, hx + 11, hy + 11), fill=RED, outline=INK, width=3)
    if plants_t is not None and t > plants_t:
        for k, (nm, lon, lat) in enumerate(PLANTS):
            if t < plants_t + 0.15 * k: continue
            x, y = proj(lon, lat); x += ox; y += oy; s = 13 * pp(t, plants_t + 0.15 * k)
            star = [(x + s * (1 if j % 2 == 0 else 0.45) * math.cos(-math.pi / 2 + j * math.pi / 5), y + s * (1 if j % 2 == 0 else 0.45) * math.sin(-math.pi / 2 + j * math.pi / 5)) for j in range(10)]
            d.polygon(star, fill=YEL, outline=INK)


# ---------------- icons ----------------
def _wheel(d, x, y, r, O=INK):
    d.ellipse((x - r, y - r, x + r, y + r), fill=O); d.ellipse((x - r * 0.45, y - r * 0.45, x + r * 0.45, y + r * 0.45), fill=(190, 190, 190))


@functools.lru_cache(maxsize=None)
def bike_icon(col=RED):
    im = Image.new('RGBA', (240, 160), (0, 0, 0, 0)); d = ImageDraw.Draw(im); O = INK
    _wheel(d, 50, 118, 36); _wheel(d, 190, 118, 36)
    d.polygon([(60, 110), (100, 60), (170, 60), (190, 110), (130, 112)], fill=col, outline=O); d.line([(60, 110), (100, 60), (170, 60), (190, 110), (130, 112), (60, 110)], fill=O, width=5)
    d.rounded_rectangle((70, 46, 140, 66), 8, fill=INK); d.line((165, 62, 200, 30), fill=O, width=8); d.line((190, 30, 215, 26), fill=O, width=8)
    return im


@functools.lru_cache(maxsize=None)
def scooter_icon(col=BLUE, ev=False):
    im = Image.new('RGBA', (240, 170), (0, 0, 0, 0)); d = ImageDraw.Draw(im); O = INK
    _wheel(d, 50, 132, 30); _wheel(d, 190, 132, 30)
    d.polygon([(30, 125), (40, 85), (130, 85), (160, 125)], fill=col, outline=O); d.line([(30, 125), (40, 85), (130, 85), (160, 125), (30, 125)], fill=O, width=5)
    d.polygon([(150, 125), (175, 40), (200, 40), (205, 125)], fill=col, outline=O); d.line([(150, 125), (175, 40), (200, 40), (205, 125)], fill=O, width=5)
    d.rounded_rectangle((45, 70, 125, 88), 8, fill=INK); d.line((175, 40, 210, 22), fill=O, width=8)
    if ev:
        bolt = [(105, 18), (85, 50), (100, 50), (92, 76), (118, 40), (103, 40), (112, 18)]; d.polygon(bolt, fill=YEL); d.line(bolt + [bolt[0]], fill=O, width=4)
    return im


@functools.lru_cache(maxsize=None)
def auto_icon(col=GOLD):
    im = Image.new('RGBA', (240, 170), (0, 0, 0, 0)); d = ImageDraw.Draw(im); O = INK
    d.polygon([(40, 130), (40, 50), (80, 20), (200, 20), (210, 130)], fill=col, outline=O); d.line([(40, 130), (40, 50), (80, 20), (200, 20), (210, 130), (40, 130)], fill=O, width=6)
    d.rectangle((60, 20, 200, 34), fill=INK); d.polygon([(55, 55), (85, 34), (120, 34), (120, 90), (55, 90)], fill=(200, 230, 245), outline=O)
    _wheel(d, 70, 135, 26); _wheel(d, 185, 135, 26)
    return im


@functools.lru_cache(maxsize=None)
def coin_im(r=46, txt='₹'):
    im = Image.new('RGBA', (r * 2 + 8, r * 2 + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((4, 4, r * 2 + 4, r * 2 + 4), fill=(255, 205, 64), outline=INK, width=5)
    tx = text_img(txt, 'anton', int(r * 1.1), INK); im.alpha_composite(tx, (r + 4 - tx.size[0] // 2, r + 4 - tx.size[1] // 2))
    return im


# ---------------- scenes ----------------
def s1(c, t):
    i = 0
    words_line(c, t, [("1 IN 4", RED, 0.0), ("RUPEES", INK, 0.15)], 'anton', 140, 270, key='h1')
    words_line(c, t, [("COMES", INK, 0.3), ("FROM", INK, 0.4), ("ABROAD", GRN, 0.5)], 'anton', 110, 400, key='h2')
    place(c, card_box(1040, MH + 40, SOFT), 540, 540 + MH / 2, 1, -0.5)
    rt = {'africa': 0.2, 'latam': 0.45, 'asia': 0.7, 'europe': 0.95}
    draw_map(c, t, 40, 540, tuple(rt), rt, labels=False)
    tm = at(i, 'this map', -0.3)
    if t > tm: place(c, label("YOU'VE NEVER SEEN THIS MAP", NAVY), 540, 540 + MH + 90, 1.1 * pp(t, tm), -2)
    tp = at(i, 'Profit up', -0.3)
    if t > tp:
        s_, a = slam(t, tp); place(c, stamp_c('PROFIT +52%', GRN, 130, -5, 111), 540, 1330, s_, 0, a)
    # coins flowing to India
    for k in range(6):
        q = ((t * 0.7 + k / 6) % 1.0)
        if t < 1.2: break
        x = 900 - 300 * q; y = 1560 - 60 * math.sin(math.pi * q)
        place(c, coin_im(36), x, y, 1, q * 300, clamp((1 - q) * 3))
    src(c, t, 'TVS Motor Q2 FY27 (Jul–Sep 2026) · exports ₹4,378 Cr of ₹17,103 Cr', 1.0, 1690)


def s2(c, t):
    i = 1; T0 = STARTS[i] + 0.05
    if t > T0:
        q = pp(t, T0); place(c, card_box(520, 170, NAVY), 540, 300, q, -3)
        if q > 0.5: place(c, text_img('TVS MOTOR', 'anton', 110, CREAM), 540, 298, q, -3)
    place_text(c, 'Q2 RESULTS · JUL–SEP 2026', 'osw5', 46, GREY, 540, 440, t, 'qr', T0 + 0.2, 'slide')
    tj = at(i, 'stock jumped', -0.3)
    if t > tj:
        q = pp(t, tj, 0.4, 1.3); place(c, card_box(900, 620, SOFT), 540, 860, q, -0.8)
        if q > 0.6:
            v = CLOSES; lo, hi = min(v), max(v); x0, x1, yt, yb = 150, 930, 640, 900
            pts = [(x0 + (x1 - x0) * k / (len(v) - 1), yb - (yb - yt) * (p - lo) / (hi - lo)) for k, p in enumerate(v)]
            dd = ImageDraw.Draw(c)
            for gy in (yt, yb): dd.line((x0, gy, x1, gy), fill=(225, 220, 210), width=2)
            pr = eio(prog(t, tj + 0.2, 1.4)); n = max(2, int(len(pts) * pr)); stroke(c, pts[:n], 9, GRN)
            ex, ey = pts[n - 1]; dd.ellipse((ex - 12, ey - 12, ex + 12, ey + 12), fill=GRN, outline=INK, width=3)
            pv = SS.roll_number(t, tj + 0.4, 1.2, 4087, 4239.9)
            place(c, text_img(f'₹{fmt_in(pv)}', 'anton', 110, INK), 420, 1050)
            place(c, label('+3.74% TODAY', GRN), 800, 1050, 1.2 * pp(t, tj + 1.2), -4)
            place(c, text_img('weekly close · 12 months', 'type', 24, GREY), 540, 1135)
    src(c, t, 'NSE close 28 Oct 2026 · market cap ~₹1.94 lakh Cr · via INDmoney', STARTS[i] + 1.0, 1260)


def pair_bars(c, t, t0, t1, y, name, a, b, unit, pct, col):
    """last year bar (grey) vs this year bar (col)"""
    if t < t0: return
    q = pp(t, t0, 0.4, 1.3); place(c, card_box(940, 330, SOFT), 540, y, q, (-0.7, 0.7)[int(y) % 2])
    if q < 0.6: return
    c.alpha_composite(text_img(name, 'anton', 52, INK), (100, int(y - 150)))
    d = ImageDraw.Draw(c); mx = max(a, b); L = 560
    for k, (nm, v, cl, tk) in enumerate((('Q2 FY26', a, GREY, t0 + 0.2), ('Q2 FY27', b, col, t1))):
        if t < tk: continue
        ph = eo(prog(t, tk, 0.8)); w = int(L * v / mx * ph); yy = y - 10 + k * 88
        c.alpha_composite(text_img(nm, 'osw5', 34, INK), (100, yy - 22))
        d.rounded_rectangle((270, yy - 30, 270 + w, yy + 30), 10, fill=cl, outline=INK, width=3)
        c.alpha_composite(text_img(f'{unit}{fmt_in(v * ph)}', 'anton', 46, INK if k == 0 else cl), (285 + w, yy - 30))
    if t > t1 + 0.6: place(c, label(pct, GRN), 860, y - 130, 1.3 * pp(t, t1 + 0.6), -5)


def s3(c, t):
    i = 2; T0 = STARTS[i] + 0.05
    words_line(c, t, [("LAST", GREY, T0), ("YEAR", GREY, T0 + 0.1), ("vs", RED, T0 + 0.2), ("THIS", INK, T0 + 0.3), ("YEAR", INK, T0 + 0.4)], 'anton', 110, 280, key='ly')
    pair_bars(c, t, at(i, 'Revenue', -0.3), at(i, 'seventeen', -0.2), 590, 'REVENUE (₹ CR)', 11905, 17103, '₹', '+44%', NAVY)
    pair_bars(c, t, at(i, 'Profit', -0.3), at(i, 'thirteen', -0.2), 960, 'NET PROFIT (₹ CR)', 904, 1377, '₹', '+52%', GRN)
    tu = at(i, 'thirteen', 0.8)
    if t > tu:
        rows = [('VEHICLES SOLD', '15 LAKH TO 19 LAKH', '+27%'), ('EBITDA MARGIN', '12.7% TO 13.0%', '+0.3 PT')]
        for k, (a, b, p) in enumerate(rows):
            tk = tu + 0.3 * k
            if t < tk: continue
            y = 1240 + k * 120; q = pp(t, tk, 0.35, 1.3)
            place(c, card_box(940, 100, SOFT), 540, y, q)
            if q > 0.6:
                c.alpha_composite(text_img(a, 'osw5', 38, GREY), (100, y - 26))
                b2 = b.replace('→', 'to'); c.alpha_composite(text_img(b2, 'anton', 46, INK), (440, y - 30))
                pl = label(p, GRN); place(c, pl, 900, y, 0.9)
    src(c, t, 'Standalone · company release & BSE filing, 28 Oct 2026', STARTS[i] + 1.0, 1510)


def s4(c, t):
    i = 3; T0 = STARTS[i] + 0.05
    place_text(c, 'THE SURPRISE', 'anton', 130, INK, 540, 280, t, 'su', T0, 'pop')
    te = at(i, 'Electric', -0.3)
    if t > te:
        place(c, scooter_icon(TEAL, True), 540, 520, 1.6 * pp(t, te), -4 + 3 * math.sin(t * 3))
        place(c, label('ELECTRIC 2-WHEELERS (iQUBE + ORBITER)', TEAL), 540, 700, 1.0 * pp(t, te + 0.2), -1)
    t8 = at(i, 'eighty thousand', -0.3); t1 = at(i, 'one lakh', -0.3)
    if t > t8:
        q = pp(t, t8, 0.4, 1.3); place(c, card_box(900, 420, SOFT), 540, 1010, q, 0.6)
        if q > 0.6:
            d = ImageDraw.Draw(c); base = 1170
            d.line((150, base, 930, base), fill=INK, width=5)
            for k, (nm, v, tk, cl) in enumerate((('Q2 FY26', 80009, t8, GREY), ('Q2 FY27', 186186, t1, TEAL))):
                if t < tk: continue
                ph = eo(prog(t, tk, 0.9)); h = int(0.0014 * v * ph); x = 340 + k * 380
                d.rounded_rectangle((x - 90, base - h, x + 90, base), 12, fill=cl, outline=INK, width=4)
                place(c, text_img(fmt_in(v * ph), 'anton', 58, INK), x, base - h - 40)
                place(c, text_img(nm, 'osw5', 34, GREY), x, base + 30)
    if t > t1 + 1.0:
        s_, a = slam(t, t1 + 1.0); place(c, stamp_c('+133%', RED, 170, -6, 404), 540, 1420, s_, 0, a)
    src(c, t, 'EV 2W units incl. exports · company release, 28 Oct 2026', STARTS[i] + 1.0, 1580)


def s5(c, t):
    i = 4; T0 = STARTS[i] + 0.05
    place_text(c, 'WHAT TVS SELLS', 'anton', 120, INK, 540, 270, t, 'ws', T0, 'pop')
    items = [('MOTORCYCLES', 'Apache · Raider · Ronin', bike_icon(RED), 'Apache', '9 LAKH · +28%'),
             ('SCOOTERS', 'Jupiter · NTORQ', scooter_icon(BLUE), 'Jupiter', '8 LAKH · +29%'),
             ('ELECTRIC', 'iQube · Orbiter', scooter_icon(TEAL, True), 'iQube', '1.86 LAKH · +133%'),
             ('3-WHEELERS', 'King · King EV Max', auto_icon(GOLD), 'King', 'INDIA + AFRICA'),
             ('NORTON (UK)', 'British superbikes · Manx R, Atlas', bike_icon(INK), 'Norton', 'EUROPE LAUNCH')]
    for k, (h, sub, ic, ph, tag) in enumerate(items):
        tk = at(i, ph, -0.3)
        if t < tk: continue
        y = 450 + k * 235; q = pp(t, tk, 0.4, 1.3)
        place(c, card_box(960, 205, SOFT), 540, y, q, (-0.8, 0.8, -0.5, 0.6, -0.6)[k])
        if q > 0.6:
            place(c, ic, 175, y, 0.72, (-4, 3, -3, 4, -2)[k])
            c.alpha_composite(text_img(h, 'anton', 60, INK), (320, int(y - 70)))
            c.alpha_composite(text_img(sub, 'osw', 36, GREY), (320, int(y + 10)))
            place(c, label(tag, (GRN, GRN, TEAL, ORG, NAVY)[k]), 830, y - 45, 0.62 * pp(t, tk + 0.3))
    src(c, t, 'Units: company release, 28 Oct 2026', STARTS[i] + 1.0, 1660)


def s6(c, t):
    i = 5; T0 = STARTS[i] + 0.05
    place_text(c, 'WHERE THE MONEY', 'anton', 100, INK, 540, 260, t, 'wm1', T0, 'pop')
    place_text(c, 'COMES FROM', 'anton', 100, INK, 540, 370, t, 'wm2', T0 + 0.15, 'pop')
    te = at(i, 'Exports', -0.3)
    segs = [('INDIA VEHICLES + OTHERS', 11411, NAVY), ('EXPORTS', 4378, ORG), ('SPARE PARTS', 1314, TEAL)]
    tot = 17103
    if t > T0 + 0.3:
        q = pp(t, T0 + 0.3, 0.4, 1.3); place(c, card_box(920, 820, SOFT), 540, 900, q, -0.5)
        if q > 0.6:
            S = 2; R = 230; cx, cy = 540, 790
            im = Image.new('RGBA', (R * 2 * S + 20, R * 2 * S + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
            a0 = -90; grow = eio(prog(t, T0 + 0.5, 1.2))
            for k, (nm, v, cl) in enumerate(segs):
                sweep = 360 * v / tot * grow
                big = 1.0 if (k == 1 and t > te) else 0.0
                ex = int(18 * S * big * eo(prog(t, te, 0.3))); mid = math.radians(a0 + sweep / 2)
                dx, dy = ex * math.cos(mid), ex * math.sin(mid)
                d.pieslice((10 + dx, 10 + dy, 10 + R * 2 * S + dx, 10 + R * 2 * S + dy), a0, a0 + sweep, fill=cl, outline=INK, width=6)
                a0 += sweep
            hole = R * S * 0.5; d.ellipse((10 + R * S - hole, 10 + R * S - hole, 10 + R * S + hole, 10 + R * S + hole), fill=SOFT, outline=INK, width=6)
            im = im.resize((im.size[0] // S, im.size[1] // S), Image.LANCZOS); place(c, im, cx, cy)
            place(c, text_img('₹17,103', 'anton', 54, INK), cx, cy - 18); place(c, text_img('CRORE', 'osw5', 30, GREY), cx, cy + 30)
            for k, (nm, v, cl) in enumerate(segs):
                tk = T0 + 0.8 + 0.2 * k if k != 1 else te
                if t < tk: continue
                y = 1100 + k * 70; a = clamp((t - tk) / 0.25)
                d2 = ImageDraw.Draw(c); d2.rounded_rectangle((130, y - 20, 170, y + 20), 6, fill=cl, outline=INK, width=3)
                c.alpha_composite(text_img(nm, 'osw5', 36, INK), (190, y - 24))
                rt = text_img(f'₹{fmt_in(v)} CR · {round(100 * v / tot)}%', 'anton', 42, cl); c.alpha_composite(rt, (950 - rt.size[0], y - 26))
    tf = at(i, 'one in every', -0.3)
    if t > tf:
        s_, a = slam(t, tf); place(c, stamp_c('1 IN EVERY 4 ₹ = EXPORTS', ORG, 84, -4, 606), 540, 1450, s_, 0, a)
    src(c, t, 'Company release, 28 Oct 2026 · balance = my calc', STARTS[i] + 1.0, 1580)


@functools.lru_cache(maxsize=None)
def small_chip(txt, col):
    tx = text_img(txt, 'anton', 38, CREAM); w, h = tx.size[0] + 28, tx.size[1] + 6
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), 12, fill=col)
    im.alpha_composite(tx, (14, 3)); return im


def s7(c, t):
    i = 6; T0 = STARTS[i] + 0.05
    tn = at(i, 'ninety', -0.3)
    v = SS.roll_number(t, tn, 1.0, 0, 90)
    place_text(c, 'SOLD IN', 'anton', 90, INK, 300, 270, t, 'si', T0, 'pop')
    if t > tn - 0.1: place(c, text_img(f'{v:.0f}+', 'anton', 150, RED), 640, 265, pp(t, tn - 0.1))
    place_text(c, 'COUNTRIES', 'anton', 90, INK, 540, 390, t, 'co', tn + 0.2, 'pop')
    rt = {'africa': at(i, 'Africa', -0.3), 'latam': at(i, 'Mexico', -0.3), 'asia': at(i, 'Nepal', -0.3), 'europe': at(i, 'Europe', -0.3)}
    oy = 480
    place(c, card_box(1050, MH + 40, SOFT), 540, oy + MH / 2, 1, 0)
    draw_map(c, t, 40, oy, tuple(rt), rt, labels=True, plants_t=at(i, 'Norton', -0.2))
    # region list
    lists = [('africa', 'AFRICA & MIDDLE EAST', 'Morocco · Egypt · Kenya · South Africa · UAE'),
             ('latam', 'LATIN AMERICA', 'Mexico · Colombia · Honduras · Panama'),
             ('asia', 'ASIA', 'Nepal · Sri Lanka · Bangladesh · Indonesia · Philippines · Singapore'),
             ('europe', 'EUROPE', 'UK · France · Italy · Spain · Portugal')]
    y0 = oy + MH + 70
    for k, (r, h, cs) in enumerate(lists):
        if t < rt[r]: continue
        y = y0 + k * 130; q = pp(t, rt[r] + 0.2, 0.35, 1.3)
        ch_ = small_chip(h, RCOL[r]); place(c, ch_, 60 + ch_.size[0] / 2, y - 18, q)
        if q > 0.6: c.alpha_composite(text_img(cs, 'osw', 34, INK), (60, int(y + 16)))
    tp = at(i, 'Norton', -0.2)
    if t > tp:
        place(c, text_img('YELLOW STARS = PLANTS: Hosur · Mysuru · Nalagarh · Karawang · Solihull (UK)', 'osw', 26, INK), 540, y0 + 4 * 130 + 10, clamp((t - tp) / 0.3))
    src(c, t, 'TVS Annual Report 2025-26 & Q2 call · named markets only', STARTS[i] + 1.0, 1830)


def s8(c, t):
    i = 7; T0 = STARTS[i] + 0.05
    place_text(c, 'UNSTOPPABLE?', 'anton', 140, INK, 540, 290, t, 'un', T0, 'pop')
    tg = at(i, 'Growth is strong', -0.3)
    if t > tg: place(c, label('GROWTH = STRONG', GRN), 540, 440, 1.3 * pp(t, tg), -2)
    tw = at(i, 'watch three', -0.3)
    if t > tw: place_text(c, 'BUT WATCH 3 THINGS', 'anton', 80, RED, 540, 570, t, 'w3', tw, 'pop')
    items = [('HIGH BASE NEXT YEAR', 'growth looks smaller vs a big year', 'high base'),
             ('MATERIAL COSTS RISING', 'can price hikes keep up?', 'material costs'),
             ('NORTON IN INVESTMENT MODE', 'still losing money for now', 'Norton')]
    for k, (h, s, ph) in enumerate(items):
        tk = at(i, ph, -0.35)
        if t < tk: continue
        y = 760 + k * 250; q = pp(t, tk, 0.4, 1.3)
        place(c, card_box(920, 210, SOFT), 540, y, q, (-1, 1, -0.6)[k])
        if q > 0.6:
            place(c, warn_icon(ORG), 160, y, 1.4)
            c.alpha_composite(text_img(h, 'anton', 58, INK), (240, int(y - 62)))
            c.alpha_composite(text_img(s, 'osw', 36, GREY), (240, int(y + 14)))
    src(c, t, 'Risks: Q2 FY27 earnings call commentary, 28 Oct 2026', STARTS[i] + 1.0, 1560)


def s9(c, t):
    i = 8; T0 = STARTS[i] + 0.05
    SS.cheat_sheet(c, t, T0, 'TVS MOTOR · Q2 FY27 CHEAT SHEET',
                   [('REVENUE', '₹17,103 CR · +44%', GRN), ('PROFIT', '₹1,377 CR · +52%', GRN), ('EV 2-WHEELERS', '+133%', TEAL), ('EXPORTS', '1 IN 4 RUPEES', ORG)], y0=170)
    ts = at(i, 'send it', -0.3)
    SS.send_frame(c, t, ts, 'the friend who rides a TVS', y=1080)
    tf = at(i, 'Follow', -0.2)
    if t > tf:
        q = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1300, 0.5 + 0.5 * eback(q), 0, clamp(q * 3))
    for k, ln in enumerate(['Sources: TVS Motor Q2 FY27 release & BSE filing (28 Oct 2026), earnings call,',
                            'Annual Report 2025-26, NSE prices via INDmoney. Standalone figures.',
                            'No buy/sell recommendation. Education only. Not investment advice.']):
        place_text(c, ln, 'type', 24, (210, 204, 192), 540, 1450 + k * 38, t, None, T0 + 0.3, 'fade', track=1)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]


def slam_times():
    return [at(0, 'Profit up', -0.3), at(3, 'one lakh', 0.7), at(5, 'one in every', -0.3)] + [STARTS[k] + 0.05 for k in range(1, 8)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('RESULTS CHECK', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
    ImageDraw.Draw(c).line((60, 118, W - 60, 118), fill=col, width=2)
    ImageDraw.Draw(c).line((60, 118, 60 + (W - 120) * clamp(t / DUR), 118), fill=RED if not dark else YEL, width=8)


def transition(c, t):
    cols = [(TEAL, INK), (GOLD, INK), (ORG, CREAM), (RED, YEL), (PINK, CREAM), (YEL, INK), (BLUE, CREAM), (INK, RED), (YEL, NAVY)]
    for bi, b in enumerate(B):
        d = 0.5
        if abs(t - b) > d / 2 + 0.12: continue
        for layer, delay in ((0, -0.05), (1, 0.0)):
            p = (t - (b - d / 2) - delay) / d
            if p <= 0 or p >= 1: continue
            p = eio(p); SWd, skew = 2050, 320
            xl = (W + 60) + p * (-(SWd + skew) - (W + 60) - 40)
            r = random.Random(bi * 10 + layer + 6100)
            left = [(xl + r.uniform(-14, 14) - skew * (y / H), y) for y in range(0, H + 1, 40)]
            right = [(xl + SWd + r.uniform(-14, 14) - skew * (y / H), y) for y in range(H, -1, -40)]
            if layer == 0: left = [(x - 70, y) for x, y in left]; right = [(x + 70, y) for x, y in right]
            poly_fill(c, left + right, cols[bi % len(cols)][layer], 255, S=1)


def scene_at(t):
    k = 0
    for i, s in enumerate(STARTS):
        if t >= s: k = i
    return k


def render(t):
    LOOP = 0.6
    if t > DUR - LOOP:
        a = _render(t); b = _render(1.4, loop=True); q = eio((t - (DUR - LOOP)) / LOOP)
        return (a * (1 - q) + b * q).astype(np.uint8)
    return _render(t)


def _render(t, loop=False):
    pbg, dbg = bgs()
    i = scene_at(t); dark = (i == 8)
    c = (dbg if dark else pbg).copy()
    st = STARTS[i]; en = STARTS[i + 1] if i + 1 < len(STARTS) else DUR
    SCENES[i](c, t)
    z = 1.0 + (0.035 if i not in (0, 6) else 0.012) * clamp((t - st) / (en - st))
    sx = sy = 0
    for ts in slam_times():
        if 0 <= t - ts < 0.35:
            k = math.exp(-(t - ts) * 14) * 8
            sx += k * math.sin((t - ts) * 90); sy += k * math.cos((t - ts) * 77)
    cw, ch = W / z, H / z
    cx, cy = W / 2 + sx, max(ch / 2, H * 0.47) + sy
    c = c.transform((W, H), Image.EXTENT, (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2), Image.BICUBIC)
    header(c, dark, t if not loop else 0); transition(c, t)
    arr = np.asarray(c.convert('RGB')).astype(np.float32)
    g = grain_frames()[int(t * FPS) % 6]
    fl = 1 + 0.012 * math.sin(t * 37) * math.sin(t * 13)
    return np.clip(arr * fl + g[..., None], 0, 255).astype(np.uint8)
