"""10 Indian defence stocks: products, prices, fundamentals, export countries (paper Vox, map, no captions)"""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs, warn_icon
from fridge import follow_btn
import tea as TEA
import saveshare as SS

SH = ROOT + 'defence/'
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
PINK = (230, 90, 140); TEAL = (20, 140, 130); ORG = (230, 120, 30); PURP = (120, 70, 200); OLIVE = (96, 110, 50)
card_box = TEA.card_box; label = TEA.label

# name, ticker, price (29 Oct 2026, 11:33 IST), product, ROE, P/E, TTM profit, export line, colour
S = {
    'HAL': ('HAL', 'HAL', '4,782.80', 'Fighter jets · helicopters', '24.0%', '34.3', '₹9,321 Cr', 'Dornier planes to Guyana', NAVY),
    'BEL': ('BHARAT ELECTRONICS', 'BEL', '365.10', 'Radars · electronic warfare', '27.4%', '43.4', '₹6,148 Cr', 'Exports +33% (FY26)', BLUE),
    'SOLAR': ('SOLAR INDUSTRIES', 'SOLARINDS', '19,362', 'Explosives · rockets', '32.6%', '88.2', '₹2,050 Cr', 'Plants: Zambia, South Africa', ORG),
    'MDL': ('MAZAGON DOCK', 'MAZDOCK', '1,733.60', 'Submarines · destroyers', '29.2%', '28.5', '₹2,451 Cr', 'Owns 51% of Colombo Dockyard', TEAL),
    'BDL': ('BHARAT DYNAMICS', 'BDL', '999.00', 'Missiles · torpedoes', '10.2%', '69.9', '₹521 Cr', 'Akash missiles: Armenia', RED),
    'CSL': ('COCHIN SHIPYARD', 'COCHINSHIP', '1,130.00', 'Aircraft carrier · ships', '12.5%', '43.7', '₹717 Cr*', 'Green cargo ships: Norway', PURP),
    'GRSE': ('GARDEN REACH', 'GRSE', '1,902.40', 'Warships · patrol vessels', '31.6%', '27.2', '₹801 Cr', '8 cargo ships: Germany', OLIVE),
    'DP': ('DATA PATTERNS', 'DATAPATTNS', '4,011.00', 'Defence electronics', 'n/a', '~84', '₹268 Cr', 'Zero debt', PINK),
    'ZEN': ('ZEN TECHNOLOGIES', 'ZENTEC', '1,605.70', 'Simulators · anti-drone', '10.7%', '78.0', '₹197 Cr', 'Offices: UAE, USA', GOLD),
    'PARAS': ('PARAS DEFENCE', 'PARAS', '1,293.80', 'Optics · drones', '~12%', '~110', '₹94 Cr', 'JV with Israel\'s CONTROP', GREY),
}


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def pp(t, t0, d=0.35, s=1.6): return eback(prog(t, t0, d), s)


def src(c, t, txt, t0, y=1700, col=GREY):
    if t > t0: place_text(c, txt, 'type', 25, col, 540, y, t, None, t0, 'fade', track=1)


def chip(txt, col, size=32, fg=CREAM):
    tx = text_img(txt, 'osw5', size, fg); w, h = tx.size[0] + 26, tx.size[1] + 8
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), 12, fill=col)
    im.alpha_composite(tx, (13, 4)); return im


# ---------------- world map ----------------
LON0, LON1, LAT0, LAT1 = -112, 150, -42, 66
MW = 1000; MH = int(MW * (LAT1 - LAT0) / (LON1 - LON0) * 1.12)
LIT = {'Armenia': RED, 'Germany': OLIVE, 'Norway': PURP, 'Guyana': NAVY, 'Sri Lanka': TEAL, 'Mauritius': OLIVE, 'Zambia': ORG,
       'South Africa': ORG, 'United States of America': GOLD, 'France': BLUE, 'United Arab Emirates': GOLD, 'Israel': GREY, 'Philippines': PINK}
PINS = [  # label, lon, lat, colour, label offset
    ('ARMENIA', 45, 40.2, RED, (40, -26)), ('GERMANY', 10.4, 51.2, OLIVE, (-10, -30)), ('NORWAY', 9, 61, PURP, (-70, -14)),
    ('GUYANA', -59, 5, NAVY, (0, 28)), ('SRI LANKA', 80.7, 7.8, TEAL, (10, 30)), ('MAURITIUS', 57.5, -20.2, OLIVE, (40, 24)),
    ('ZAMBIA', 27.8, -13.5, ORG, (-60, 0)), ('S. AFRICA', 24, -29, ORG, (0, 30)), ('USA', -98, 39, GOLD, (0, -30)),
    ('FRANCE', 2.4, 46.6, BLUE, (-60, 10)), ('UAE', 54.3, 24, GOLD, (40, 18)), ('ISRAEL', 35, 31.5, GREY, (-50, 14)),
    ('PHILIPPINES', 122, 12, PINK, (0, -28)),
]


def proj(lon, lat):
    return (lon - LON0) / (LON1 - LON0) * MW, (LAT1 - lat) / (LAT1 - LAT0) * MH


@functools.lru_cache(maxsize=1)
def world():
    d = json.load(open(ROOT + 'tvs/world.geojson')); out = []
    for f in d['features']:
        nm = f['properties']['NAME']; g = f['geometry']
        polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        out.append((nm, [[proj(x, y) for x, y in poly[0]] for poly in polys]))
    return out


@functools.lru_cache(maxsize=4)
def map_img(lit=True):
    S_ = 2; im = Image.new('RGBA', (MW * S_, MH * S_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for nm, polys in world():
        col = (255, 140, 40) if nm == 'India' else (LIT.get(nm, (214, 207, 192)) if lit else (214, 207, 192))
        base = col == (214, 207, 192)
        for pts in polys:
            if len(pts) < 3: continue
            P = [(x * S_, y * S_) for x, y in pts]
            d.polygon(P, fill=col); d.line(P + [P[0]], fill=(150, 142, 128) if base else INK, width=2 if base else 3)
    return im.resize((MW, MH), Image.LANCZOS)


def arc_pts(a, b, k=0.25, n=30):
    (x0, y0), (x1, y1) = a, b; mx, my = (x0 + x1) / 2, (y0 + y1) / 2; dx, dy = x1 - x0, y1 - y0
    cx, cy = mx + dy * k, my - abs(dx) * k * 0.6 - 30
    return [((1 - u) ** 2 * x0 + 2 * (1 - u) * u * cx + u * u * x1, (1 - u) ** 2 * y0 + 2 * (1 - u) * u * cy + u * u * y1) for u in np.linspace(0, 1, n)]


def draw_map(c, t, ox, oy, t0, gap=0.12, labels=True, lit_t=None):
    c.alpha_composite(map_img(lit_t is not None and t > lit_t), (ox, oy))
    d = ImageDraw.Draw(c)
    hx, hy = proj(78.5, 22); hx += ox; hy += oy
    for k, (nm, lon, lat, col, off) in enumerate(PINS):
        tk = t0 + gap * k
        if t < tk: continue
        x, y = proj(lon, lat); x += ox; y += oy
        q = eio(prog(t, tk, 0.6)); pts = arc_pts((hx, hy), (x, y)); m = max(2, int(len(pts) * q)); stroke(c, pts[:m], 4, col)
        if t > tk + 0.4:
            p = pp(t, tk + 0.4, 0.3); rr = 10 * p
            d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=col, outline=INK, width=3)
            if labels and p > 0.5: place(c, text_img(nm, 'osw5', 24, INK), x + off[0], y + off[1])
    pul = 1 + 0.25 * math.sin(t * 6)
    d.ellipse((hx - 16 * pul, hy - 16 * pul, hx + 16 * pul, hy + 16 * pul), outline=RED, width=4)
    d.ellipse((hx - 11, hy - 11, hx + 11, hy + 11), fill=RED, outline=INK, width=3)


# ---------------- stock card ----------------
def stock_card(c, t, tk, key, y, h=600, compact=False):
    if t < tk: return
    nm, tick, pr, prod, roe, pe, prof, exp, col = S[key]
    q = pp(t, tk, 0.4, 1.3)
    place(c, card_box(960, h, SOFT), 540, y, q, random.Random(key).uniform(-0.8, 0.8))
    if q < 0.6: return
    top = y - h / 2
    if compact:
        c.alpha_composite(text_img(nm, 'anton', 50, INK), (85, int(top + 18)))
        pt = text_img('₹' + pr, 'anton', 46, col); c.alpha_composite(pt, (int(990 - pt.size[0]), int(top + 22)))
        ch = chip(prod, col, 28); c.alpha_composite(ch, (88, int(top + 92)))
        row = f'ROE {roe}  ·  P/E {pe}  ·  profit {prof}'
        c.alpha_composite(text_img(row, 'osw5', 32, INK), (88, int(top + 150)))
        if t > tk + 0.5: c.alpha_composite(text_img('Export: ' + exp, 'osw', 30, GREY), (88, int(top + 200)))
        return
    c.alpha_composite(text_img(nm, 'anton', 68, INK), (85, int(top + 24)))
    c.alpha_composite(text_img(tick, 'type', 28, GREY), (90, int(top + 118)))
    pt = text_img('₹' + pr, 'anton', 64, col); c.alpha_composite(pt, (int(990 - pt.size[0]), int(top + 30)))
    ch = chip(prod, col, 34); c.alpha_composite(ch, (88, int(top + 170)))
    stats = [('ROE', roe), ('P/E', pe), ('TTM PROFIT', prof)]
    for j, (lab, val) in enumerate(stats):
        tj = tk + 0.35 + 0.2 * j
        if t < tj: continue
        x = 90 + j * 300; a = pp(t, tj, 0.3)
        c.alpha_composite(text_img(lab, 'osw5', 30, GREY), (x, int(top + 260)))
        place(c, text_img(val, 'anton', 54, INK), x + text_img(val, 'anton', 54, INK).size[0] / 2, top + 340, a)
    te = tk + 1.0
    if t > te:
        q2 = pp(t, te, 0.35)
        place(c, card_box(880, 110, (238, 246, 240)), 540, top + h - 90, q2)
        if q2 > 0.6:
            place(c, plane(), 140, top + h - 90, 0.5)
            c.alpha_composite(text_img(exp, 'anton', 44, GRN), (200, int(top + h - 120)))


@functools.lru_cache(maxsize=1)
def plane(): return SS.plane_icon(110, CREAM)


# ---------------- scenes ----------------
def s1(c, t):
    i = 0
    words_line(c, t, [("SOLD", INK, 0.0), ("IN", INK, 0.1), ("80+", RED, 0.2), ("COUNTRIES", INK, 0.3)], 'anton', 104, 280, key='h')
    place(c, card_box(1040, MH + 40, SOFT), 540, 470 + MH / 2, 1, -0.5)
    draw_map(c, t, 40, 470, 0.1, 0.1, labels=True, lit_t=1.4)
    td = at(i, "Don't buy", -0.3)
    if t > td:
        sh = math.sin(t * 40) * 6 * math.exp(-(t - td) * 3)
        place(c, label("DON'T BUY DEFENCE STOCKS YET", RED), 540 + sh, 470 + MH + 110, 1.15 * pp(t, td), -2)
    place_text(c, 'India defence exports FY26 · Ministry of Defence via ABC Live / WION', 'type', 24, GREY, 540, 470 + MH + 200, t, None, 1.0, 'fade', track=1)
    for k, key in enumerate(['HAL', 'BEL', 'MDL', 'BDL', 'GRSE']):
        tk = 1.6 + 0.15 * k
        if t > tk: place(c, label(S[key][1], S[key][8]), 150 + k * 195, 1650, 0.8 * pp(t, tk), (-3, 3, -2, 2, -4)[k])


def s2(c, t):
    i = 1; T0 = STARTS[i] + 0.05
    place_text(c, 'DEFENCE EXPORTS', 'anton', 110, INK, 540, 270, t, 'de', T0, 'pop')
    te = at(i, 'thirty eight', -0.3)
    if t > te:
        q = pp(t, te, 0.4, 1.3); place(c, card_box(920, 560, SOFT), 540, 690, q, -0.6)
        if q > 0.6:
            d = ImageDraw.Draw(c); base = 900
            d.line((170, base, 910, base), fill=INK, width=5)
            for k, (nm, v, cl, tk) in enumerate((('FY25', 23622, GREY, te + 0.2), ('FY26', 38424, GRN, te + 0.6))):
                if t < tk: continue
                ph = eo(prog(t, tk, 0.9)); hgt = int(v / 38424 * 380 * ph); x = 360 + k * 360
                d.rounded_rectangle((x - 95, base - hgt, x + 95, base), 12, fill=cl, outline=INK, width=4)
                place(c, text_img(f'₹{int(v * ph):,} CR', 'anton', 50, INK), x, base - hgt - 36)
                place(c, text_img(nm, 'osw5', 36, GREY), x, base + 32)
    tu = at(i, 'sixty three', -0.3)
    if t > tu:
        s_, a = slam(t, tu); place(c, stamp_c('+63%', GRN, 130, -6, 22), 540, 1150, s_, 0, a)
    for k, (nm, ph, col) in enumerate((('ARMENIA', 'Armenia', RED), ('GERMANY', 'Germany', OLIVE), ('GUYANA', 'Guyana', NAVY), ('SRI LANKA', 'Sri Lanka', TEAL))):
        tk = at(i, ph, -0.25)
        if t > tk: place(c, label(nm, col), 280 + (k % 2) * 520, 1350 + (k // 2) * 110, 1.15 * pp(t, tk), (-3, 3, 2, -2)[k])
    src(c, t, 'FY26 ₹38,424 Cr vs FY25 ₹23,622 Cr · Ministry of Defence, Apr 2026', STARTS[i] + 1.0, 1600)


def pair(c, t, i, k1, ph1, k2, ph2):
    stock_card(c, t, at(i, ph1, -0.3), k1, 520)
    stock_card(c, t, at(i, ph2, -0.3), k2, 1160)
    src(c, t, 'Price: NSE 29 Oct 2026 11:33 IST via INDmoney · Fundamentals: Screener.in', STARTS[i] + 1.0, 1520 + 0 * i)


def s3(c, t): pair(c, t, 2, 'HAL', 'HAL', 'BEL', 'Bharat Electronics')
def s4(c, t): pair(c, t, 3, 'SOLAR', 'Solar', 'MDL', 'Mazagon')
def s5(c, t): pair(c, t, 4, 'BDL', 'Bharat Dynamics', 'CSL', 'Cochin')


def s6(c, t):
    i = 5
    for k, (key, ph) in enumerate((('GRSE', 'Garden Reach'), ('DP', 'Data Patterns'), ('ZEN', 'Zen'), ('PARAS', 'Paras'))):
        stock_card(c, t, at(i, ph, -0.3), key, 310 + k * 300, h=270, compact=True)
    src(c, t, '~ = my calculation from TTM results · *Cochin: FY26 profit', STARTS[i] + 1.0, 1530)


def s7(c, t):
    i = 6; T0 = STARTS[i] + 0.05
    place_text(c, 'THE CATCH', 'anton', 120, RED, 540, 260, t, 'tc', T0, 'pop')
    tg = at(i, 'A great', -0.3)
    if t > tg: place(c, label('GREAT BUSINESS IS NOT A CHEAP STOCK', NAVY), 540, 390, 1.0 * pp(t, tg), -1)
    rows = [('GRSE', 27.2), ('MAZDOCK', 28.5), ('HAL', 34.3), ('BEL', 43.4), ('COCHINSHIP', 43.7), ('BDL', 69.9), ('ZENTEC', 78.0), ('DATAPATTNS', 84), ('SOLARINDS', 88.2), ('PARAS', 110)]
    tb = at(i, 'Garden Reach', -0.4)
    if t > tb:
        q = pp(t, tb, 0.4, 1.3); place(c, card_box(960, 1000, SOFT), 540, 1000, q, 0.5)
        if q > 0.6:
            c.alpha_composite(text_img('P/E = PRICE / YEARLY PROFIT', 'osw5', 34, GREY), (90, 520))
            d = ImageDraw.Draw(c)
            for k, (nm, v) in enumerate(rows):
                tk = tb + 0.2 + 0.12 * k
                if t < tk: continue
                y = 600 + k * 88; ph = eo(prog(t, tk, 0.6)); w = int(5.4 * v * ph)
                col = GRN if v < 35 else (GOLD if v < 60 else RED)
                c.alpha_composite(text_img(nm, 'osw5', 32, INK), (90, y - 22))
                d.rounded_rectangle((330, y - 24, 330 + w, y + 24), 10, fill=col, outline=INK, width=3)
                c.alpha_composite(text_img(f'{v * ph:.0f}x', 'anton', 40, col), (342 + w, y - 26))
    th = at(i, 'above eighty', -0.3)
    if t > th:
        s_, a = slam(t, th); place(c, stamp_c('80x+ PROFIT', RED, 90, -6, 707), 540, 1590, s_, 0, a)
    src(c, t, 'Screener.in, 29 Oct 2026 · ~84x and ~110x: my calculation', STARTS[i] + 1.0, 1720)


def s8(c, t):
    i = 7; T0 = STARTS[i] + 0.05
    place_text(c, 'NEAR 52-WEEK LOWS', 'anton', 104, INK, 540, 270, t, 'nl', T0, 'pop')
    rows = [('BDL', 999.0, 986.5, 1633.4), ('COCHIN SHIPYARD', 1130.0, 1101.2, 1842.8), ('MAZAGON DOCK', 1733.6, 1687.5, 2881.8),
            ('BEL', 365.1, 354.55, 473.45), ('GARDEN REACH', 1902.4, 1842.0, 3339.0)]
    tf = at(i, 'five of these', -0.3)
    for k, (nm, p, lo, hi) in enumerate(rows):
        tk = tf + 0.25 * k
        if t < tk: continue
        y = 470 + k * 210; q = pp(t, tk, 0.35, 1.3)
        place(c, card_box(940, 180, SOFT), 540, y, q, (-0.8, 0.8, -0.5, 0.6, -0.6)[k])
        if q < 0.6: continue
        c.alpha_composite(text_img(nm, 'anton', 50, INK), (95, int(y - 70)))
        d = ImageDraw.Draw(c); x0, x1, yy = 100, 760, y + 30
        d.line((x0, yy, x1, yy), fill=(210, 204, 192), width=10)
        f = (p - lo) / (hi - lo); xm = x0 + (x1 - x0) * f * eo(prog(t, tk + 0.2, 0.6))
        d.line((x0, yy, xm, yy), fill=RED, width=10); d.ellipse((xm - 13, yy - 13, xm + 13, yy + 13), fill=RED, outline=INK, width=3)
        c.alpha_composite(text_img('52W LOW', 'type', 20, GREY), (x0 - 4, int(yy + 14))); c.alpha_composite(text_img('HIGH', 'type', 20, GREY), (x1 - 40, int(yy + 14)))
        v = text_img(f'+{(p / lo - 1) * 100:.1f}%', 'anton', 54, RED); c.alpha_composite(v, (990 - v.size[0], int(y - 30)))
    tw = at(i, 'Watch', -0.3)
    if t > tw:
        place(c, label('WATCH: ORDER BOOKS', GRN), 300, 1540, 1.1 * pp(t, tw), -3)
        place(c, label('WATCH: VALUATIONS', NAVY), 780, 1540, 1.1 * pp(t, tw + 0.25), 3)
    src(c, t, '% above 52-week low · NSE via INDmoney, 29 Oct 2026, 11:33 IST', STARTS[i] + 1.0, 1660)


def s9(c, t):
    i = 8; T0 = STARTS[i] + 0.05
    q = pp(t, T0, 0.45, 1.2)
    place(c, SS._card(960, 1000), 540, 660, q, -0.4)
    if q > 0.6:
        place(c, text_img('DEFENCE 10 · CHEAT SHEET', 'anton', 56, INK), 540, 220)
        d = ImageDraw.Draw(c); d.line((90, 262, 990, 262), fill=INK, width=4)
        for k, key in enumerate(['HAL', 'BEL', 'SOLAR', 'MDL', 'BDL', 'CSL', 'GRSE', 'DP', 'ZEN', 'PARAS']):
            tk = T0 + 0.3 + 0.08 * k
            if t < tk: continue
            nm, tick, pr, prod, roe, pe, prof, exp, col = S[key]; y = 300 + k * 88
            c.alpha_composite(text_img(tick, 'anton', 38, col), (95, y))
            c.alpha_composite(text_img(prod, 'osw', 30, INK), (370, y + 6))
            v = text_img('P/E ' + pe, 'anton', 36, GRN if float(pe.strip('~')) < 35 else (GOLD if float(pe.strip('~')) < 60 else RED))
            c.alpha_composite(v, (985 - v.size[0], y))
        SS.save_pulse(c, t, T0 + 1.4, 540, 1240, 'SAVE THIS')
    SS.send_frame(c, t, at(i, 'send it', -0.3), 'your defence-stock friend', y=1430)
    tf = at(i, 'Follow', -0.2)
    if t > tf:
        q2 = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1620, 0.5 + 0.5 * eback(q2), 0, clamp(q2 * 3))
    for k, ln in enumerate(['Prices: NSE 29 Oct 2026, 11:33 IST, via INDmoney', 'Fundamentals: Screener.in · Exports: MoD & company news',
                            'No buy/sell call. Not investment advice.']):
        place_text(c, ln, 'type', 22, (210, 204, 192), 540, 1750 + k * 34, t, None, T0 + 0.3, 'fade', track=1)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]


def slam_times():
    return [at(1, 'sixty three', -0.3), at(6, 'above eighty', -0.3)] + [STARTS[k] + 0.05 for k in range(1, 8)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('DEFENCE STOCKS', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
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
            r = random.Random(bi * 10 + layer + 9100)
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
        a = _render(t); b = _render(1.6, loop=True); q = eio((t - (DUR - LOOP)) / LOOP)
        return (a * (1 - q) + b * q).astype(np.uint8)
    return _render(t)


def _render(t, loop=False):
    pbg, dbg = bgs()
    i = scene_at(t); dark = (i == 8)
    c = (dbg if dark else pbg).copy()
    st = STARTS[i]; en = STARTS[i + 1] if i + 1 < len(STARTS) else DUR
    SCENES[i](c, t)
    z = 1.0 + (0.012 if i == 0 else 0.03) * clamp((t - st) / (en - st))
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
