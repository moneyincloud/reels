"""Cupid Ltd: products, revenue mix, export countries, tenders, splits/bonuses, profit, the catch (paper Vox, male VO)"""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs, typed, drop, warn_icon
from fridge import follow_btn
import saveshare as SS
import tea as TEA
import defence as DF

SH = ROOT + 'cupid/'
SCRIPT = json.load(open(SH + 'script.json'))
DURS = json.load(open(SH + 'vo/durs.json'))
LEAD, TAIL = 0.15, 0.3
STARTS, VO = [], []
_t = 0.0
for i, d in enumerate(DURS):
    STARTS.append(_t); VO.append(_t + (0.1 if i == 0 else LEAD)); _t = VO[-1] + d + TAIL
DUR = _t + 1.8
B = STARTS[1:]
NAVY = (30, 60, 120); BLUE = (40, 100, 200); GREY = (120, 112, 104); TEAL = (20, 140, 130); GOLD = (214, 160, 40); ORG = (230, 120, 30)
PINK = (230, 90, 140); PURP = (120, 70, 200); SOFT = (252, 250, 244)
label = TEA.label
MONTHLY = [46.72, 65.85, 103.62, 80.2, 81.32, 83.1, 119.58, 129.06, 189.93, 230.62, 280.46, 311.65, 324.7]
MLAB = ['OCT 25', '', '', 'JAN', '', '', 'APR', '', '', 'JUL', '', '', 'OCT 26']


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def pp(t, t0, d=0.35, s=1.6): return eback(prog(t, t0, d), s)


def src(c, t, txt, t0, y=1740, col=GREY):
    if t > t0: place_text(c, txt, 'type', 24, col, 540, y, t, None, t0, 'fade', track=1)


@functools.lru_cache(4)
def grid(w, h):
    im = Image.new('RGBA', (w, h), (252, 250, 244, 255)); d = ImageDraw.Draw(im)
    for x in range(0, w, 30): d.line((x, 0, x, h), fill=(205, 218, 228), width=1)
    for y in range(0, h, 30): d.line((0, y, w, y), fill=(205, 218, 228), width=1)
    return cutout(im, border=0, shadow=0.3)


def mini_chart(c, t, ox, oy, w, h, f):
    n = len(MONTHLY); vmin, vmax = 0, 380
    def P(i, v): return (ox + 80 + (w - 140) * i / (n - 1), oy + h - 60 - (v - vmin) / (vmax - vmin) * (h - 120))
    d = ImageDraw.Draw(c); d.line((ox + 70, oy + h - 60, ox + w - 40, oy + h - 60), fill=INK, width=4)
    for i, lb in enumerate(MLAB):
        if lb: li = text_img(lb, 'type', 22, (90, 85, 80), 1); x, _ = P(i, 0); c.alpha_composite(li, (int(x - li.size[0] / 2), int(oy + h - 50)))
    pts = []
    for k in range(int(f * (n - 1) * 15) + 1):
        u = k / 15; i = min(int(u), n - 2); s = u - i
        v = MONTHLY[i] + (MONTHLY[i + 1] - MONTHLY[i]) * (s * s * (3 - 2 * s))
        pts.append(P(i + s, v))
    if len(pts) > 1:
        poly_fill(c, pts + [(pts[-1][0], oy + h - 60), (pts[0][0], oy + h - 60)], (160, 220, 170), 150)
        stroke(c, pts, 9, INK); tx, ty = pts[-1]; d.ellipse((tx - 12, ty - 12, tx + 12, ty + 12), fill=GRN, outline=INK, width=4)
        return pts[-1]


def share_grid(c, t, cx, cy, n, t0, col=GOLD):
    """draw n little share tiles in a grid"""
    cols = 1 if n == 1 else (5 if n <= 20 else 10)
    sz = 150 if n == 1 else (54 if n <= 20 else 40); gap = 10 if n > 1 else 0
    rows = math.ceil(n / cols)
    W_ = cols * sz + (cols - 1) * gap; H_ = rows * sz + (rows - 1) * gap
    d = ImageDraw.Draw(c)
    for k in range(n):
        tk = t0 + 0.012 * k
        if t < tk: continue
        r_, cc = divmod(k, cols); x = cx - W_ / 2 + cc * (sz + gap); y = cy - H_ / 2 + r_ * (sz + gap)
        s = eback(prog(t, tk, 0.25)); m = sz * (1 - s) / 2
        d.rounded_rectangle((x + m, y + m, x + sz - m, y + sz - m), 8, fill=col, outline=INK, width=4 if n > 1 else 7)
    return H_


# product icons
@functools.lru_cache(None)
def icon(kind):
    w = h = 220
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if kind == 'condom':
        d.rounded_rectangle((20, 20, 200, 200), 18, fill=(200, 205, 215), outline=INK, width=6)
        for x in range(20, 200, 16): d.line((x, 20, x + 8, 28), fill=INK, width=2); d.line((x, 200, x + 8, 192), fill=INK, width=2)
        d.ellipse((60, 60, 160, 160), outline=INK, width=8); d.ellipse((85, 85, 135, 135), outline=(150, 155, 165), width=5)
    elif kind == 'lube':
        d.rounded_rectangle((70, 30, 150, 190), 26, fill=(120, 190, 235), outline=INK, width=6)
        d.rectangle((90, 10, 130, 34), fill=INK)
        d.ellipse((92, 90, 128, 126), fill=CREAM)
    elif kind == 'kit':
        d.rounded_rectangle((60, 20, 160, 200), 14, fill=SOFT, outline=INK, width=6)
        d.rectangle((85, 60, 135, 90), fill=(230, 230, 230), outline=INK, width=3)
        for y in (68, 80): d.line((88, y, 132, y), fill=RED, width=4)
        d.ellipse((95, 130, 125, 160), outline=INK, width=4)
    elif kind == 'deo':
        d.rounded_rectangle((75, 50, 145, 200), 20, fill=(40, 40, 60), outline=INK, width=6)
        d.rectangle((90, 22, 130, 52), fill=(200, 200, 210), outline=INK, width=4)
        d.rectangle((75, 110, 145, 140), fill=GOLD)
    else:
        d.polygon([(80, 70), (140, 70), (160, 110), (160, 200), (60, 200), (60, 110)], fill=(240, 200, 80), outline=INK)
        d.line([(80, 70), (140, 70), (160, 110), (160, 200), (60, 200), (60, 110), (80, 70)], fill=INK, width=6)
        d.rectangle((92, 30, 128, 70), fill=GRN, outline=INK, width=4)
    return cutout(im, border=8, shadow=0.38)


# ---------------- scenes ----------------
def s1(c, t):
    i = 0
    words_line(c, t, [("OWN", INK, 0.1), ("CUPID?", RED, 0.3)], 'anton', 140, 280, key='h1')
    tb = at(i, 'one share', -0.2); th = at(i, 'one hundred', -0.2)
    if t > tb:
        n = 100 if t > th else 1
        share_grid(c, t, 540, 610, n, th if n == 100 else tb)
        place(c, text_img('1 SHARE' if n == 1 else '100 SHARES', 'anton', 64, INK), 540, 900 if n == 100 else 790)
    tr = at(i, "Don't miss", -0.2)
    if t > tr:
        place_text(c, "don't miss the risk!", 'mark', 60, RED, 540, 990, t, 'dr', tr, 'slide', rot=-3)
    tp = at(i, 'seven times', -0.8)
    if t > tp:
        p = prog(t, tp, 0.45); ox, oy, w, h = 90, 1070 + (1 - eo(p)) * 500, 900, 520
        place(c, grid(w, h), ox + w / 2, oy + h / 2, 1, 0, clamp(p * 3))
        tip = mini_chart(c, t, ox, oy, w, h, eio(prog(t, tp + 0.3, 1.6)))
        if t > tp + 1.8:
            sc, a = slam(t, tp + 1.8); place(c, stamp_c('7X IN 1 YEAR', GRN, 72, -6, 3), ox + 300, oy + 130, sc, 0, a)
    src(c, t, 'Bonus-adjusted monthly close · NSE via INDmoney · 30 Oct 2026', 1.5, 1720)


def s2(c, t):
    i = 1; T0 = STARTS[i]
    place_text(c, 'WHAT CUPID MAKES', 'anton', 100, INK, 540, 260, t, 'wm', T0 + 0.05, 'pop')
    items = [('condom', 'condoms', 'CONDOMS', 'male + female', 300, 560), ('lube', 'lubricants', 'LUBRICANTS', 'water-based', 780, 560),
             ('kit', 'test kits', 'TEST KITS', 'HIV, pregnancy', 300, 1010), ('deo', 'deodorants', 'DEODORANTS', 'new: FMCG', 780, 1010),
             ('oil', 'hair oil', 'HAIR OIL', 'new: FMCG', 540, 1420)]
    for k, (kind, ph, lab, sub, x, y) in enumerate(items):
        tk = at(i, ph, -0.3)
        if t < tk: continue
        p = prog(t, tk, 0.4); jx, jy, jr = jit(('ic', k), t, 1.4, 0.4)
        place(c, icon(kind), x + jx, y + jy, 0.6 + 0.4 * eback(p), (-4, 3, -2, 4, -3)[k] + jr, clamp(p * 3))
        c.alpha_composite(text_img(lab, 'anton', 50, INK), (int(x - text_w(lab, 'anton', 50) / 2), int(y + 125)))
        place_text(c, sub, 'mark', 36, RED, x, y + 210, t, ('sb', k), tk + 0.3, 'fade')


def s3(c, t):
    i = 2; T0 = STARTS[i]
    place_text(c, 'FY26 REVENUE BY PRODUCT', 'anton', 80, INK, 540, 260, t, 'rp', T0 + 0.05, 'pop')
    rows = [('MALE CONDOMS', 181.11, BLUE, 'male condoms'), ('FMCG', 84.26, ORG, 'FMCG'), ('FEMALE CONDOMS', 60.72, PINK, 'Female'), ('KITS + LUBRICANTS', 24.97, TEAL, 'Kits')]
    d = ImageDraw.Draw(c)
    for k, (nm, v, col, ph) in enumerate(rows):
        tk = at(i, ph, -0.3)
        if t < tk: continue
        y = 470 + k * 230; q = eo(prog(t, tk, 0.8)); w = int(v / 181.11 * 720 * q)
        c.alpha_composite(text_img(nm, 'osw5', 40, INK), (110, int(y - 98)))
        d.rounded_rectangle((110, y - 30, 110 + w, y + 50), 14, fill=col, outline=INK, width=5)
        place(c, text_img(f'₹{v * q:.0f} CR', 'anton', 58, INK), min(110 + w + 120, 930), y + 8)
    if t > at(i, 'twenty five', 0.3):
        place(c, label('TOTAL ₹358 CR · OPERATING MARGIN 33%', NAVY), 540, 1440, pp(t, at(i, 'twenty five', 0.3)), -1)
        place_text(c, 'profit by product: not disclosed', 'mark', 42, RED, 540, 1560, t, 'nd', at(i, 'twenty five', 0.6), 'slide', rot=-2)
    src(c, t, 'Company FY26 results release (May 2026) · margin: Screener.in', T0 + 1.0, 1720)


AF = [('S. AFRICA', 24, -29, BLUE, (0, 34)), ('KENYA', 37.9, 0.2, GRN, (70, -6)), ('TANZANIA', 35, -6.3, ORG, (90, 22)), ('ANGOLA', 17.9, -11.2, PINK, (-70, 0)), ('BRAZIL', -51, -10, GOLD, (0, -32))]
LIT = {'South Africa': BLUE, 'Kenya': GRN, 'Tanzania': ORG, 'United Republic of Tanzania': ORG, 'Angola': PINK, 'Brazil': GOLD}


@functools.lru_cache(4)
def map_img(lit):
    S_ = 2; im = Image.new('RGBA', (DF.MW * S_, DF.MH * S_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for nm, polys in DF.world():
        col = (255, 140, 40) if nm == 'India' else (LIT.get(nm, (214, 207, 192)) if lit else (214, 207, 192))
        base = col == (214, 207, 192)
        for pts in polys:
            if len(pts) < 3: continue
            P = [(x * S_, y * S_) for x, y in pts]
            d.polygon(P, fill=col); d.line(P + [P[0]], fill=(150, 142, 128) if base else INK, width=2 if base else 3)
    return im.resize((DF.MW, DF.MH), Image.LANCZOS)


def s4(c, t):
    i = 3; T0 = STARTS[i]
    tx = at(i, 'sixty percent', -0.4)
    if t > T0 + 0.1:
        v = 59.3 * eo(prog(t, tx, 1.0)) if t > tx else 0
        place(c, text_img(f'{v:.1f}%', 'anton', 170, GRN), 540, 300)
        place_text(c, 'of revenue from exports', 'mark', 52, INK, 540, 410, t, 'ex', tx + 0.3, 'slide', rot=-3)
    p = prog(t, T0 + 0.5, 0.45); oy = 500 + (1 - eo(p)) * 500
    place(c, cutout(Image.new('RGBA', (DF.MW + 40, DF.MH + 40), SOFT + (255,)), border=0, shadow=0.3), 540, oy + DF.MH / 2, 1, -0.6, clamp(p * 3))
    if p > 0.2:
        ta = at(i, 'Mostly Africa', -0.3)
        c.alpha_composite(map_img(t > ta), (40, int(oy)))
        d = ImageDraw.Draw(c); hx, hy = DF.proj(78.5, 22); hx += 40; hy += oy
        for k, (nm, lon, lat, col, off) in enumerate(AF):
            tk = ta + 0.2 * k if k < 4 else at(i, 'Brazil', -0.3)
            if t < tk: continue
            x, y = DF.proj(lon, lat); x += 40; y += oy
            q = eio(prog(t, tk, 0.6)); pts = DF.arc_pts((hx, hy), (x, y)); m = max(2, int(len(pts) * q)); stroke(c, pts, 4, col)
            if t > tk + 0.4:
                pr = eback(prog(t, tk + 0.4, 0.3)); rr = 11 * pr
                d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=col, outline=INK, width=3)
                place(c, text_img(nm, 'anton', 28, INK), x + off[0], y + off[1])
        tc = at(i, 'hundred and twenty five', -0.4)
        if t > tc:
            sc, a = slam(t, tc); place(c, stamp_c('125+ COUNTRIES', RED, 84, -5, 9), 540, oy + DF.MH + 110, sc, 0, a)
    src(c, t, 'Exports ₹208 Cr of FY26 revenue · company releases', T0 + 1.0, 1640)


def s5(c, t):
    i = 4; T0 = STARTS[i]
    place_text(c, 'THE REAL ENGINE', 'anton', 110, INK, 540, 260, t, 're', T0 + 0.05, 'pop')
    tg = at(i, 'Government tenders', -0.3)
    if t > tg: place_text(c, 'government tenders', 'pfi', 76, RED, 540, 380, t, 'gt', tg, 'pop')
    tw = at(i, 'WHO', -0.3)
    for k, (txt, col) in enumerate((('WHO', BLUE), ('UNFPA', TEAL))):
        if t > tw + 0.2 * k:
            p = pp(t, tw + 0.2 * k)
            place(c, cutout(Image.new('RGBA', (360, 200), SOFT + (255,)), border=8, shadow=0.35, bcol=col), 330 + k * 420, 600, p, (-3, 3)[k])
            if p > 0.6:
                place(c, text_img(txt, 'anton', 80, col), 330 + k * 420, 570)
                place(c, text_img('PREQUALIFIED', 'type', 24, GREY, 2), 330 + k * 420, 650)
    if t > at(i, 'both types', -0.3):
        place_text(c, 'male AND female condoms', 'mark', 46, INK, 540, 760, t, 'mf', at(i, 'both types', -0.3), 'slide', rot=-2)
    ts = at(i, 'South Africa', -0.3)
    if t > ts:
        q = pp(t, ts, 0.4, 1.3); place(c, cutout(Image.new('RGBA', (920, 560), SOFT + (255,)), border=0, shadow=0.35), 540, 1170, q, -0.8)
        if q > 0.6:
            c.alpha_composite(text_img('SOUTH AFRICA · GOVT TENDER', 'anton', 54, INK), (110, 920))
            c.alpha_composite(text_img('eligible to supply up to 100% of its condom needs', 'type', 26, GREY, 1), (114, 990))
            d = ImageDraw.Draw(c); x0, x1, y = 130, 950, 1180
            d.line((x0, y, x1, y), fill=(210, 204, 192), width=14)
            f = eo(prog(t, ts + 0.6, 1.4)); d.line((x0, y, x0 + (x1 - x0) * f, y), fill=GRN, width=14)
            for k, yr in enumerate(('2026', '2027', '2028', '2029', '2030', '2031')):
                x = x0 + (x1 - x0) * k / 5; d.ellipse((x - 10, y - 10, x + 10, y + 10), fill=INK)
                li = text_img(yr, 'type', 24, GREY); c.alpha_composite(li, (int(x - li.size[0] / 2), y + 22))
            tf = at(i, 'five year', -0.3)
            if t > tf:
                sc, a = slam(t, tf + 0.6); place(c, stamp_c('5-YEAR TENDER', GRN, 76, -5, 15), 540, 1340, sc, 0, a)
    src(c, t, '5-yr tender from Q4 FY26 (company, Sep 2025) · timeline approx.', T0 + 1.0, 1720)


def s6(c, t):
    i = 5; T0 = STARTS[i]
    place_text(c, 'HOW 1 SHARE BECAME 100', 'anton', 86, INK, 540, 260, t, 'hs', T0 + 0.05, 'pop')
    steps = [('one share split', 10, 'APR 2024 · SPLIT 1:10', BLUE), ('bonus made it', 20, 'APR 2024 · BONUS 1:1', ORG), ('four to one', 100, 'MAR 2026 · BONUS 4:1', GRN)]
    n = 1; lab = 'BEFORE 2024'; col = GOLD; t0 = T0 + 0.2
    for ph, nn, lb, cl in steps:
        tk = at(i, ph, -0.2)
        if t > tk: n, lab, col, t0 = nn, lb, cl, tk
    share_grid(c, t, 540, 760, n, t0, col)
    place(c, label(lab, col if n > 1 else INK), 540, 1170, pp(t, t0), -2)
    v = text_img(f'{n} SHARE' + ('S' if n > 1 else ''), 'anton', 120, INK); place(c, v, 540, 1330)
    if t > at(i, 'One became', -0.2):
        place_text(c, '1 x 10 x 2 x 5 = 100', 'osw5', 50, GRN, 540, 1470, t, 'eq', at(i, 'One became', -0.2), 'pop')
    src(c, t, 'Ex-date 4 Apr 2024 · 4:1 bonus record date 9 Mar 2026', T0 + 1.0, 1700)


def s7(c, t):
    i = 6; T0 = STARTS[i]
    place_text(c, 'NET PROFIT', 'anton', 120, INK, 540, 260, t, 'np', T0 + 0.05, 'pop')
    rows = [('FY24', 40, GREY), ('FY25', 41, GREY), ('FY26', 108, GRN), ('FY27*', 250, None)]
    d = ImageDraw.Draw(c); base = 1300
    d.line((100, base, 980, base), fill=INK, width=5)
    for k, (yr, v, col) in enumerate(rows):
        tk = (T0 + 0.4 + 0.25 * k) if k < 3 else at(i, 'guides', -0.2)
        if k == 2: tk = at(i, 'one hundred eight', -0.4)
        if t < tk: continue
        x = 210 + k * 220; q = eo(prog(t, tk, 0.8)); hg = int(v / 250 * 760 * q)
        if col:
            d.rounded_rectangle((x - 75, base - hg, x + 75, base), 12, fill=col, outline=INK, width=5)
        else:
            for yy in range(base - hg, base, 24): d.line((x - 75, yy, x + 75, yy), fill=ORG, width=4)
            d.rectangle((x - 75, base - hg, x + 75, base), outline=ORG, width=5)
        place(c, text_img(f'₹{v * q:.0f}' + ('+' if not col else ''), 'anton', 56, INK), x, base - hg - 40)
        place(c, text_img(yr, 'osw5', 36, GREY), x, base + 34)
    if t > at(i, 'guides', 0.3):
        place_text(c, '*company guidance, not a fact yet', 'mark', 40, ORG, 540, 1430, t, 'cg', at(i, 'guides', 0.3), 'slide', rot=-2)
    src(c, t, '₹ Cr · Screener.in · FY27: company guidance, Oct 2026', T0 + 1.0, 1700)


def s8(c, t):
    i = 7; T0 = STARTS[i]
    if t > T0 + 0.1:
        p = prog(t, T0 + 0.1, 0.3); lw = text_w('THE CATCH', 'osw', 54, 2); x0 = 540 - (lw + 70) / 2
        place(c, warn_icon(RED), x0 + 28, 262, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
        place(c, text_img('THE CATCH', 'osw', 54, RED, 2), x0 + 70 + lw / 2, 260, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
    rows = [('P/E above 300', 'price = 308x yearly profit (Screener)', 'three hundred', RED),
            ('Donor-funded demand', 'tenders depend on aid budgets', 'donor funding', ORG),
            ('Guidance is not a guarantee', 'FY27 target ₹250 Cr+ profit', 'guarantee', YEL)]
    for k, (h1, h2, ph, col) in enumerate(rows):
        tk = at(i, ph, -0.3)
        if t < tk: continue
        y = 520 + k * 300; q = pp(t, tk, 0.35, 1.3)
        place(c, cutout(Image.new('RGBA', (920, 230), (40, 38, 36, 255)), border=6, shadow=0.4, bcol=col), 540, y, q, (-0.8, 0.8, -0.6)[k])
        if q < 0.6: continue
        c.alpha_composite(text_img(h1, 'anton', 64, col), (130, int(y - 66)))
        c.alpha_composite(text_img(h2, 'type', 30, (200, 194, 182), 1), (134, int(y + 26)))
    if t > at(i, 'guarantee', 0.8):
        place(c, text_img('Promoters own 47.7% · 4.7 lakh shareholders', 'osw5', 38, CREAM), 540, 1450, pp(t, at(i, 'guarantee', 0.8)))
    typed(c, 'Not investment advice. DYOR.', 'type', 30, (200, 194, 182), 1580, t, at(i, 'guarantee', 1.0), at(i, 'guarantee', 2.0))


def s9(c, t):
    i = 8; T0 = STARTS[i]
    q = pp(t, T0, 0.45, 1.2)
    place(c, SS._card(960, 860), 540, 590, q, -0.4)
    if q > 0.6:
        place(c, text_img('CUPID · CHEAT SHEET', 'anton', 56, INK), 540, 220)
        d = ImageDraw.Draw(c); d.line((90, 262, 990, 262), fill=INK, width=4)
        rows = [('Price (30 Oct, 12:14)', '₹324.70', INK), ('1-year move', '7x', GRN), ('FY26 revenue / profit', '₹358 / ₹108 Cr', INK), ('Exports', '59% · 125+ countries', TEAL),
                ('1 old share is now', '100 shares', GOLD), ('P/E', '308', RED), ('Promoter holding', '47.7%', INK), ('FY27 guidance (co.)', '₹250 Cr+ profit', ORG)]
        for k, (a_, b_, col) in enumerate(rows):
            tk = T0 + 0.3 + 0.08 * k
            if t < tk: continue
            y = 290 + k * 82
            c.alpha_composite(text_img(a_, 'osw5', 36, INK), (100, y))
            v = text_img(b_, 'anton', 42, col); c.alpha_composite(v, (980 - v.size[0], y - 2))
        SS.save_pulse(c, t, T0 + 1.3, 540, 1080, 'SAVE THIS')
    SS.send_frame(c, t, at(i, 'send it', -0.3), 'your friend who tracks Cupid', y=1300)
    tf = at(i, 'Follow', -0.2)
    if t > tf:
        q2 = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1530, 0.5 + 0.5 * eback(q2), 0, clamp(q2 * 3))
    for k, ln in enumerate(['Price: NSE via INDmoney · Fundamentals: Screener.in', 'Revenue mix & guidance: company releases (May & Oct 2026)', 'Not a buy/sell call. Education only.']):
        place_text(c, ln, 'type', 22, GREY, 540, 1680 + k * 34, t, None, T0 + 0.3, 'fade', track=1)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
DARK_SCENES = {7}


def slam_times():
    return [at(0, 'seven times', 1.0), at(3, 'hundred and twenty five', -0.4), at(4, 'five year', 0.3)] + [STARTS[k] + 0.05 for k in range(1, 8)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('CUPID LTD · DEEP DIVE', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
    ImageDraw.Draw(c).line((60, 118, W - 60, 118), fill=col, width=2)
    ImageDraw.Draw(c).line((60, 118, 60 + (W - 120) * clamp(t / DUR), 118), fill=RED if not dark else YEL, width=8)


def transition(c, t):
    cols = [(PINK, CREAM), (YEL, INK), (BLUE, CREAM), (GRN, YEL), (ORG, INK), (GOLD, INK), (INK, RED), (YEL, RED)]
    for bi, b in enumerate(B):
        d = 0.55
        if abs(t - b) > d / 2 + 0.12: continue
        for layer, delay in ((0, -0.07), (1, 0.0)):
            p = (t - (b - d / 2) - delay) / d
            if p <= 0 or p >= 1: continue
            p = eio(p); SWd, skew = 2050, 320
            xl = (W + 60) + p * (-(SWd + skew) - (W + 60) - 40)
            r = random.Random(bi * 10 + layer + 666)
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
    i = scene_at(t); dark = i in DARK_SCENES
    c = (dbg if dark else pbg).copy()
    st = STARTS[i]; en = STARTS[i + 1] if i + 1 < len(STARTS) else DUR
    SCENES[i](c, t)
    z = 1.0 + 0.035 * clamp((t - st) / (en - st))
    sx = sy = 0
    for ts in slam_times():
        if 0 <= t - ts < 0.35:
            k = math.exp(-(t - ts) * 14) * 9
            sx += k * math.sin((t - ts) * 90); sy += k * math.cos((t - ts) * 77)
    cw, ch = W / z, H / z
    cx, cy = W / 2 + sx, H * 0.47 + sy
    c = c.transform((W, H), Image.EXTENT, (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2), Image.BICUBIC)
    header(c, dark, t if not loop else 0); transition(c, t)
    arr = np.asarray(c.convert('RGB')).astype(np.float32)
    g = grain_frames()[int(t * FPS) % 6]
    fl = 1 + 0.012 * math.sin(t * 37) * math.sin(t * 13)
    return np.clip(arr * fl + g[..., None], 0, 255).astype(np.uint8)
