"""IT stocks: 40 tested on 20%/yr profit growth + near-zero debt; 7 pass, 3 almost (paper Vox, map, no captions)"""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs
from fridge import follow_btn
import tea as TEA
import saveshare as SS
import defence as DF

SH = ROOT + 'itstocks/'
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
chip = DF.chip

# name, ticker, price ₹ (Screener 28-29 Oct 2026), business, 3y profit CAGR, borrowings vs reserves, P/E, ROE, where, catch, colour
S = {
    'NPST': ('NPST', 'NPST', '1,687', 'UPI & payment software', '84%', '₹14 Cr vs ₹420 Cr', '78.9', '15.1%', 'India · Sri Lanka deal', 'P/E near 79', TEAL),
    'ZEN': ('ZENSAR', 'ZENSARTECH', '497', 'IT services for banks', '34%', '₹79 Cr vs ₹4,674 Cr', '14.2', '17.3%', 'US · Europe · Africa', 'Sales grew only 5%/yr', BLUE),
    'AUR': ('AURIONPRO', 'AURIONPRO', '538', 'Banking software · metro tickets', '30%', '₹61 Cr vs ₹1,684 Cr', '14.2', '13.2%', '30+ countries', 'Last qtr profit -12%', ORG),
    'PER': ('PERSISTENT', 'PERSISTENT', '5,872', 'AI & digital engineering', '28%', '₹575 Cr vs ₹8,511 Cr', '49.6', '27.2%', 'Software, BFSI, healthcare', 'Q2 profit -25%', PURP),
    'AFF': ('AFFLE 3i', 'AFFLE', '1,378', 'Mobile advertising', '23%', '₹15 Cr vs ₹3,624 Cr', '41.5', '13.8%', '72% India & emerging mkts', 'ROE below 15%', PINK),
    'NEW': ('NEWGEN', 'NEWGEN', '455', 'Software for banks & govts', '22%', '₹43 Cr vs ₹1,711 Cr', '18.7', '19.6%', 'EMEA 30 · India 28 · US 23 · APAC 19', 'FY26 profit -4.7%', NAVY),
    'EMU': ('eMUDHRA', 'EMUDHRA', '352', 'Digital signatures · cyber', '~22%', '₹29 Cr vs ₹870 Cr', '25.3', '12.6%', '66% of revenue abroad', 'Exiting global SSL', OLIVE),
}
ALMOST = {
    'NET': ('NETWEB', '4,400', 'AI servers · supercomputers', 'Profit +64%/yr', 'Debt 16% of reserves', 'P/E 71.4', GOLD),
    'ZAG': ('ZAGGLE', '168*', 'Expense cards for 3,915 firms', 'FY24 ₹44 Cr to FY26 ₹138 Cr', 'Only 2 yrs of data', 'D/E 0.04', TEAL),
    'UNI': ('UNICOMMERCE', '83.7', 'E-commerce SaaS', '~24%/yr (FY24-26)', 'Only 2 yrs of data', 'P/E 43', BLUE),
}
ORDER = ['NPST', 'ZEN', 'AUR', 'PER', 'AFF', 'NEW', 'EMU']


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def pp(t, t0, d=0.35, s=1.6): return eback(prog(t, t0, d), s)


def src(c, t, txt, t0, y=1700, col=GREY):
    if t > t0: place_text(c, txt, 'type', 25, col, 540, y, t, None, t0, 'fade', track=1)


# ---------------- map (reuse defence projection) ----------------
LIT = {'United States of America': BLUE, 'United Kingdom': BLUE, 'Germany': OLIVE, 'Austria': OLIVE, 'Netherlands': PINK,
       'United Arab Emirates': ORG, 'Kenya': OLIVE, 'South Africa': BLUE, 'Kazakhstan': OLIVE, 'Sri Lanka': TEAL, 'Indonesia': PINK}
PINS = [
    ('USA', -98, 39, BLUE, (0, -30)), ('UK', -2, 53, BLUE, (-46, -10)), ('NETHERLANDS', 5.3, 52.2, PINK, (-40, -34)),
    ('GERMANY', 10.4, 51.2, OLIVE, (60, -24)), ('AUSTRIA', 14.5, 47.5, OLIVE, (58, 14)), ('UAE', 54.3, 24, ORG, (40, 20)),
    ('KENYA', 37.9, 0.2, OLIVE, (50, 8)), ('S. AFRICA', 24, -29, BLUE, (0, 30)), ('KAZAKHSTAN', 67, 48, OLIVE, (20, -30)),
    ('SRI LANKA', 80.7, 7.8, TEAL, (10, 30)), ('INDONESIA', 113, -1, PINK, (0, 32)),
]


@functools.lru_cache(maxsize=4)
def map_img(lit=True):
    S_ = 2; im = Image.new('RGBA', (DF.MW * S_, DF.MH * S_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for nm, polys in DF.world():
        col = (255, 140, 40) if nm == 'India' else (LIT.get(nm, (214, 207, 192)) if lit else (214, 207, 192))
        base = col == (214, 207, 192)
        for pts in polys:
            if len(pts) < 3: continue
            P = [(x * S_, y * S_) for x, y in pts]
            d.polygon(P, fill=col); d.line(P + [P[0]], fill=(150, 142, 128) if base else INK, width=2 if base else 3)
    return im.resize((DF.MW, DF.MH), Image.LANCZOS)


def draw_map(c, t, ox, oy, t0, gap=0.12, labels=True, lit_t=None):
    c.alpha_composite(map_img(lit_t is not None and t > lit_t), (ox, oy))
    d = ImageDraw.Draw(c)
    hx, hy = DF.proj(78.5, 22); hx += ox; hy += oy
    for k, (nm, lon, lat, col, off) in enumerate(PINS):
        tk = t0 + gap * k
        if t < tk: continue
        x, y = DF.proj(lon, lat); x += ox; y += oy
        q = eio(prog(t, tk, 0.6)); pts = DF.arc_pts((hx, hy), (x, y)); m = max(2, int(len(pts) * q)); stroke(c, pts[:m], 4, col)
        if t > tk + 0.4:
            p = pp(t, tk + 0.4, 0.3); rr = 10 * p
            d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=col, outline=INK, width=3)
            if labels and p > 0.5: place(c, text_img(nm, 'osw5', 24, INK), x + off[0], y + off[1])
    pul = 1 + 0.25 * math.sin(t * 6)
    d.ellipse((hx - 16 * pul, hy - 16 * pul, hx + 16 * pul, hy + 16 * pul), outline=RED, width=4)
    d.ellipse((hx - 11, hy - 11, hx + 11, hy + 11), fill=RED, outline=INK, width=3)


# ---------------- cards ----------------
def stock_card(c, t, tk, key, y, h=620, compact=False):
    if t < tk: return
    nm, tick, pr, biz, g, debt, pe, roe, where, catch, col = S[key]
    q = pp(t, tk, 0.4, 1.3)
    place(c, card_box(960, h, SOFT), 540, y, q, random.Random(key).uniform(-0.8, 0.8))
    if q < 0.6: return
    top = y - h / 2
    if compact:
        c.alpha_composite(text_img(nm, 'anton', 50, INK), (85, int(top + 16)))
        pt = text_img('₹' + pr, 'anton', 46, col); c.alpha_composite(pt, (int(990 - pt.size[0]), int(top + 20)))
        c.alpha_composite(chip(biz, col, 28), (88, int(top + 88)))
        c.alpha_composite(text_img(f'PROFIT +{g.strip("~")}/YR  ·  P/E {pe}  ·  ROE {roe}', 'osw5', 32, INK), (88, int(top + 146)))
        if t > tk + 0.35: c.alpha_composite(text_img('Borrowed ' + debt + ' reserves', 'osw', 28, GRN), (88, int(top + 196)))
        if t > tk + 0.55: c.alpha_composite(text_img('Where: ' + where, 'osw', 28, NAVY), (88, int(top + 240)))
        if t > tk + 0.8: place(c, label('CATCH: ' + catch, RED), 540, top + h - 40, 0.62 * pp(t, tk + 0.8), -1)
        return
    c.alpha_composite(text_img(nm, 'anton', 68, INK), (85, int(top + 24)))
    if tick != nm: c.alpha_composite(text_img(tick, 'type', 28, GREY), (90, int(top + 118)))
    pt = text_img('₹' + pr, 'anton', 64, col); c.alpha_composite(pt, (int(990 - pt.size[0]), int(top + 30)))
    c.alpha_composite(chip(biz, col, 34), (88, int(top + 168)))
    stats = [('PROFIT/YR (3Y)', g if g[0] == '~' else '+' + g), ('P/E', pe), ('ROE', roe)]
    for j, (lab, val) in enumerate(stats):
        tj = tk + 0.35 + 0.2 * j
        if t < tj: continue
        x = 90 + j * 300; a = pp(t, tj, 0.3)
        c.alpha_composite(text_img(lab, 'osw5', 30, GREY), (x, int(top + 256)))
        vi = text_img(val, 'anton', 58, GRN if j == 0 else INK)
        place(c, vi, x + vi.size[0] / 2, top + 338, a)
    if t > tk + 0.9:
        c.alpha_composite(text_img('Borrowed ' + debt + ' reserves', 'osw5', 32, GRN), (90, int(top + 398)))
    te = tk + 1.1
    if t > te:
        q2 = pp(t, te, 0.35)
        place(c, card_box(880, 92, (238, 242, 250)), 540, top + h - 120, q2)
        if q2 > 0.6:
            place(c, plane(), 130, top + h - 120, 0.42)
            c.alpha_composite(text_img(where, 'anton', 40, NAVY), (185, int(top + h - 146)))
    if t > tk + 1.4: place(c, label('CATCH: ' + catch, RED), 540, top + h - 30, 0.7 * pp(t, tk + 1.4), 1)


@functools.lru_cache(maxsize=1)
def plane(): return SS.plane_icon(110, CREAM)


def almost_card(c, t, tk, key, y, h=330):
    if t < tk: return
    nm, pr, biz, g, why, pe, col = ALMOST[key]
    q = pp(t, tk, 0.4, 1.3)
    place(c, card_box(960, h, SOFT), 540, y, q, random.Random(key).uniform(-0.8, 0.8))
    if q < 0.6: return
    top = y - h / 2
    c.alpha_composite(text_img(nm, 'anton', 52, INK), (85, int(top + 18)))
    pt = text_img('₹' + pr, 'anton', 46, col); c.alpha_composite(pt, (int(990 - pt.size[0]), int(top + 22)))
    c.alpha_composite(chip(biz, col, 28), (88, int(top + 92)))
    c.alpha_composite(text_img(g + '  ·  ' + pe, 'osw5', 32, INK), (88, int(top + 150)))
    if t > tk + 0.5:
        c.alpha_composite(text_img(why, 'anton', 40, ORG), (88, int(top + 200)))
        s_, a = slam(t, tk + 0.5, 0.3); place(c, stamp_c('ALMOST', GOLD, 56, -8, 31 + len(key)), 850, top + 230, s_, 0, a)


# ---------------- scenes ----------------
def s1(c, t):
    i = 0
    words_line(c, t, [("40", RED, 0.0), ("IT", INK, 0.1), ("STOCKS", INK, 0.2), ("TESTED", INK, 0.3)], 'anton', 108, 270, key='h')
    place(c, card_box(980, 700, SOFT), 540, 720, 1, -0.4)
    tp = at(i, 'Only seven', -0.2)
    pass_idx = {3, 9, 14, 20, 26, 31, 37}
    d = ImageDraw.Draw(c)
    for k in range(40):
        r, col_ = divmod(k, 8); x = 175 + col_ * 104; y = 460 + r * 120
        tk = 0.15 + 0.03 * k
        if t < tk: continue
        s_ = pp(t, tk, 0.25)
        fail = t > tp + 0.02 * k and k not in pass_idx
        ok = t > tp and k in pass_idx
        fill = (225, 70, 60) if fail else (GRN if ok else (205, 198, 184))
        rr = 38 * s_
        d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=fill, outline=INK, width=4)
        if fail:
            d.line((x - 16, y - 16, x + 16, y + 16), fill=CREAM, width=7); d.line((x - 16, y + 16, x + 16, y - 16), fill=CREAM, width=7)
        if ok:
            d.line((x - 18, y + 2, x - 4, y + 16, x + 20, y - 14), fill=CREAM, width=8, joint='curve')
    if t > tp + 0.5:
        s_, a = slam(t, tp + 0.5); place(c, stamp_c('ONLY 7 PASSED', GRN, 100, -5, 41), 540, 1170, s_, 0, a)
    tr = at(i, 'profit up', -0.3)
    if t > tr: place(c, label('RULE 1: PROFIT +20% A YEAR (3 YRS)', NAVY), 540, 1340, 1.0 * pp(t, tr), -2)
    tz = at(i, 'almost zero', -0.3)
    if t > tz: place(c, label('RULE 2: ALMOST ZERO DEBT', TEAL), 540, 1460, 1.0 * pp(t, tz), 2)
    src(c, t, 'Screener.in consolidated, FY23-FY26, data 28-29 Oct 2026', 1.2, 1580)


def s2(c, t):
    i = 1; T0 = STARTS[i] + 0.05
    place_text(c, 'BIG NAMES FAILED', 'anton', 110, INK, 540, 260, t, 'bf', T0, 'pop')
    rows = [('COFORGE', 'Profit +33%/yr', 'Borrowed ₹6,026 Cr', 'Coforge', -0.6), ('RATEGAIN', 'Profit +48%/yr', 'Borrowed ₹949 Cr', 'RateGain', 0.6),
            ('MAPMYINDIA', 'Debt only ₹7 Cr', 'Profit +2%/yr', 'MapmyIndia', -0.5)]
    for k, (nm, good, bad, ph, rot) in enumerate(rows):
        tk = at(i, ph, -0.3)
        if t < tk: continue
        y = 500 + k * 300; q = pp(t, tk, 0.35, 1.3)
        place(c, card_box(940, 250, SOFT), 540, y, q, rot)
        if q < 0.6: continue
        c.alpha_composite(text_img(nm, 'anton', 58, INK), (100, int(y - 100)))
        c.alpha_composite(text_img(good, 'osw5', 36, GRN), (100, int(y - 10)))
        c.alpha_composite(text_img(bad, 'anton', 46, RED), (100, int(y + 40)))
        tf = tk + 0.6 if k < 2 else at(i, 'barely', -0.2)
        if t > tf:
            s_, a = slam(t, tf, 0.3); place(c, stamp_c('FAIL', RED, 80, -10, 50 + k), 850, y + 10, s_, 0, a)
    tq = at(i, 'So who', -0.3)
    if t > tq:
        sh = math.sin(t * 30) * 5 * math.exp(-(t - tq) * 3)
        place(c, label('SO WHO MADE IT?', YEL), 540 + sh, 1420, 1.3 * pp(t, tq), -2)
    src(c, t, 'Borrowings: latest balance sheet · Profit: 3-yr CAGR · Screener.in', STARTS[i] + 1.0, 1590)


SRC_CARD = 'Screener.in, 28-29 Oct 2026 · borrowings: latest balance sheet'


def pair(c, t, i, k1, ph1, k2, ph2):
    stock_card(c, t, at(i, ph1, -0.3), k1, 520)
    stock_card(c, t, at(i, ph2, -0.3), k2, 1170)
    src(c, t, SRC_CARD, STARTS[i] + 1.0, 1540)


def s3(c, t): pair(c, t, 2, 'NPST', 'NPST', 'ZEN', 'Zensar')
def s4(c, t): pair(c, t, 3, 'AUR', 'Aurionpro', 'PER', 'Persistent')


def s5(c, t):
    i = 4
    for k, (key, ph) in enumerate((('AFF', 'Affle'), ('NEW', 'Newgen'), ('EMU', 'eMudhra'))):
        stock_card(c, t, at(i, ph, -0.3), key, 400 + k * 400, h=360, compact=True)
    src(c, t, '~22%: my calculation, FY23 ₹61 Cr to FY26 ₹110 Cr (Screener shows 19%)', STARTS[i] + 1.0, 1640)


def s6(c, t):
    i = 5; T0 = STARTS[i] + 0.05
    place_text(c, 'ALMOST PASSED', 'anton', 110, GOLD, 540, 250, t, 'ap', T0, 'pop')
    for k, (key, ph) in enumerate((('NET', 'Netweb'), ('ZAG', 'Zaggle'), ('UNI', 'Unicommerce'))):
        almost_card(c, t, at(i, ph, -0.3), key, 540 + k * 370)
    src(c, t, '*Zaggle price 9 Oct 2026 (Sharpely) · others Screener.in 28-29 Oct', STARTS[i] + 1.0, 1640)


def s7(c, t):
    i = 6; T0 = STARTS[i] + 0.05
    place_text(c, 'THE CATCH', 'anton', 120, RED, 540, 250, t, 'tc', T0, 'pop')
    tg = at(i, 'Passing', -0.3)
    if t > tg: place(c, label('PASSING IS NOT A BUY SIGNAL', NAVY), 540, 380, 1.0 * pp(t, tg), -1)
    tp = at(i, "Persistent's", -0.3)
    if t > tp:
        q = pp(t, tp, 0.4, 1.3); place(c, card_box(940, 470, SOFT), 540, 700, q, -0.5)
        if q > 0.6:
            c.alpha_composite(text_img('PERSISTENT · QUARTERLY PROFIT', 'osw5', 34, GREY), (100, 485))
            d = ImageDraw.Draw(c); base = 830
            d.line((150, base, 930, base), fill=INK, width=5)
            for k, (nm, v, cl, tk) in enumerate((('SEP 2025', 471, GREY, tp + 0.2), ('SEP 2026', 352, RED, tp + 0.6))):
                if t < tk: continue
                ph = eo(prog(t, tk, 0.8)); hg = int(v / 471 * 210 * ph); x = 330 + k * 300
                d.rounded_rectangle((x - 85, base - hg, x + 85, base), 12, fill=cl, outline=INK, width=4)
                place(c, text_img(f'₹{int(v * ph)} CR', 'anton', 44, INK), x, base - hg - 30)
                place(c, text_img(nm, 'osw5', 30, GREY), x, base + 28)
            tf = at(i, 'twenty five', -0.3)
            if t > tf:
                s_, a = slam(t, tf); place(c, stamp_c('-25%', RED, 84, -8, 71), 860, 560, s_, 0, a)
            ta = at(i, 'acquisition', -0.3)
            if t > ta: c.alpha_composite(text_img('₹185 Cr one-time Nagarro acquisition cost', 'osw', 28, GREY), (100, 885))
    tn = at(i, 'NPST trades', -0.3)
    rows = [('NPST', 78.9), ('NETWEB', 71.4), ('PERSISTENT', 49.6), ('AFFLE', 41.5), ('EMUDHRA', 25.3), ('NEWGEN', 18.7), ('ZENSAR', 14.2), ('AURIONPRO', 14.2)]
    if t > tn:
        q = pp(t, tn, 0.4, 1.3); place(c, card_box(940, 640, SOFT), 540, 1300, q, 0.5)
        if q > 0.6:
            c.alpha_composite(text_img('P/E = PRICE / YEARLY PROFIT', 'osw5', 32, GREY), (100, 1000))
            d = ImageDraw.Draw(c)
            for k, (nm, v) in enumerate(rows):
                tk = tn + 0.15 + 0.1 * k
                if t < tk: continue
                y = 1080 + k * 68; ph = eo(prog(t, tk, 0.5)); w = int(6.6 * v * ph)
                col = GRN if v < 30 else (GOLD if v < 60 else RED)
                c.alpha_composite(text_img(nm, 'osw5', 30, INK), (100, y - 20))
                d.rounded_rectangle((320, y - 22, 320 + w, y + 22), 10, fill=col, outline=INK, width=3)
                c.alpha_composite(text_img(f'{v * ph:.0f}x', 'anton', 38, col), (332 + w, y - 24))
    src(c, t, 'Persistent Q2 FY27 via INDmoney blog · P/E: Screener.in, 28-29 Oct 2026', STARTS[i] + 1.0, 1690)


def s8(c, t):
    i = 7; T0 = STARTS[i] + 0.05
    words_line(c, t, [("WHERE", INK, T0), ("THE", INK, T0 + 0.1), ("MONEY", GRN, T0 + 0.2), ("COMES", INK, T0 + 0.3), ("FROM", INK, T0 + 0.4)], 'anton', 78, 270, key='w')
    place(c, card_box(1040, DF.MH + 40, SOFT), 540, 420 + DF.MH / 2, 1, -0.5)
    draw_map(c, t, 40, 420, T0 + 0.3, 0.13, labels=True, lit_t=T0 + 1.5)
    te = at(i, 'sixty six', -0.3)
    if t > te:
        s_, a = slam(t, te); place(c, stamp_c('eMUDHRA: 66% ABROAD', GRN, 78, -4, 81), 540, 420 + DF.MH + 110, s_, 0, a)
    for k, (txt, ph, col) in enumerate((('USA', 'US', BLUE), ('KENYA', 'Kenya', OLIVE), ('KAZAKHSTAN', 'Kazakhstan', OLIVE))):
        tk = at(i, ph, -0.25)
        if t > tk: place(c, label(txt, col), 220 + k * 320, 420 + DF.MH + 260, 1.0 * pp(t, tk), (-3, 2, -2)[k])
    place_text(c, 'Newgen: EMEA 30% · India 28% · USA 23% · APAC 19%', 'osw5', 32, NAVY, 540, 420 + DF.MH + 370, t, None, T0 + 2.0, 'fade')
    src(c, t, 'Company results Q1-Q2 FY27 · ICICI Direct (Newgen mix)', T0 + 1.0, 1730)


def s9(c, t):
    i = 8; T0 = STARTS[i] + 0.05
    q = pp(t, T0, 0.45, 1.2)
    place(c, SS._card(960, 1000), 540, 660, q, -0.4)
    if q > 0.6:
        place(c, text_img('IT 7 · CHEAT SHEET', 'anton', 56, INK), 540, 220)
        d = ImageDraw.Draw(c); d.line((90, 262, 990, 262), fill=INK, width=4)
        hdr = [('STOCK', 95), ('PROFIT/YR', 520), ('P/E', 760)]
        for txt, x in hdr: c.alpha_composite(text_img(txt, 'osw5', 26, GREY), (x, 275))
        for k, key in enumerate(ORDER):
            tk = T0 + 0.3 + 0.08 * k
            if t < tk: continue
            nm, tick, pr, biz, g, debt, pe, roe, where, catch, col = S[key]; y = 320 + k * 92
            c.alpha_composite(text_img(tick, 'anton', 40, col), (95, y))
            c.alpha_composite(text_img(g if g[0] == '~' else '+' + g, 'anton', 40, GRN), (520, y))
            v = float(pe); c.alpha_composite(text_img(pe, 'anton', 40, GRN if v < 30 else (GOLD if v < 60 else RED)), (760, y))
        if t > T0 + 1.0:
            c.alpha_composite(text_img('ALMOST: NETWEB · ZAGGLE · UNICOMMERCE', 'osw5', 32, ORG), (95, 975))
        SS.save_pulse(c, t, T0 + 1.4, 540, 1240, 'SAVE THIS')
    SS.send_frame(c, t, at(i, 'send it', -0.3), 'your friend in IT', y=1430)
    tf = at(i, 'Follow', -0.2)
    if t > tf:
        q2 = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1620, 0.5 + 0.5 * eback(q2), 0, clamp(q2 * 3))
    for k, ln in enumerate(['Data: Screener.in consolidated, 28-29 Oct 2026', 'Rules check, not a recommendation',
                            'Education only. Not investment advice.']):
        place_text(c, ln, 'type', 22, (210, 204, 192), 540, 1750 + k * 34, t, None, T0 + 0.3, 'fade', track=1)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]


def slam_times():
    return [at(0, 'Only seven', 0.3), at(6, 'twenty five', -0.3), at(7, 'sixty six', -0.3)] + [STARTS[k] + 0.05 for k in range(1, 8)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('IT STOCKS TEST', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
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
            r = random.Random(bi * 10 + layer + 9300)
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
    z = 1.0 + (0.012 if i in (0, 7) else 0.03) * clamp((t - st) / (en - st))
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
