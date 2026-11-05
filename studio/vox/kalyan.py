"""Kalyan Jewellers Part 1: 1 shop to 546, sales 3.7x, profit to ₹1,350 Cr. Multibagger or trap? (PCJ collage style, female VO)"""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs, typed, drop, warn_icon, receipt
from fridge import follow_btn
import saveshare as SS
import suzlon as SZ
import tea as TEA

SH = ROOT + 'kalyan/'
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
SOFT = (252, 250, 244)
label = TEA.label
WEEKLY = [495.5,496.45,505.35,492.5,479.3,484.85,491.15,495.7,506.9,467.5,367.2,368.9,380.25,418.05,401.2,410.1,395.55,379,382.7,388.35,394.35,449.15,426.85,405.3,412.75,424.55,353.05,352.4,355.05,371.85,344.75,383.5,377.8,382.05,476.15,574.4,573.55,612.6,606.3,608.25,603.55,615.8,598.8,601.15,581.85,573,528.5,554,558,512,498,560]
WLAB = ['NOV 25'] + ['']*12 + ['FEB'] + ['']*12 + ['MAY'] + ['']*12 + ['AUG'] + ['']*11 + ['NOV 26']


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def pp(t, t0, d=0.35, s=1.6): return eback(prog(t, t0, d), s)


def src(c, t, txt, t0, y=1720, col=GREY):
    if t > t0: place_text(c, txt, 'type', 24, col, 540, y, t, None, t0, 'fade', track=1)


def bars(c, t, rows, base, maxh, vmax, x0=200, gap=230, w=150, unit='₹', suffix=' CR', neg_base=None):
    d = ImageDraw.Draw(c)
    for k, (lab, v, col, tk) in enumerate(rows):
        if t < tk: continue
        x = x0 + k * gap; q = eo(prog(t, tk, 0.8)); hg = int(abs(v) / vmax * maxh * q)
        if v >= 0:
            d.rounded_rectangle((x - w / 2, base - hg, x + w / 2, base), 12, fill=col, outline=INK, width=5)
            place(c, text_img(f'{unit}{int(v * q):,}{suffix}', 'anton', 46, INK), x, base - hg - 34)
        else:
            d.rounded_rectangle((x - w / 2, base, x + w / 2, base + hg), 12, fill=col, outline=INK, width=5)
            place(c, text_img(f'-{unit}{int(-v * q):,}{suffix}', 'anton', 46, RED), x, base + hg + 34)
        place(c, text_img(lab, 'osw5', 34, GREY), x, base + (40 if v >= 0 else -30))
    d.line((80, base, 1000, base), fill=INK, width=5)


# ---------------- scenes ----------------
@functools.lru_cache(None)
def store(col):
    w, h = 80, 70
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((6, 24, w - 6, h - 4), fill=SOFT, outline=INK, width=3)
    d.polygon([(0, 26), (w, 26), (w - 8, 6), (8, 6)], fill=col, outline=INK)
    d.rectangle((30, 40, 50, h - 4), fill=GOLD, outline=INK, width=2)
    return im



def s1(c, t):
    i = 0
    place(c, label('PART 1', RED), 540, 230, pp(t, 0.05), -3)
    dy, a = drop(t, 0.2, 360)
    if a > 0:
        hp = round(prog(t, 0.8, 0.5) * 20) / 20
        place(c, SZ.clipping(hp, 'KALYAN JEWELLERS', 'THE MARKET PAGE', 'JEWELLERY · NSE: KALYANKJIL'), 540, 520 + dy, 0.95, -3, a)
    ts = at(i, 'One shop', -0.2)
    if t > ts:
        place(c, store(GOLD), 250, 860, 1.6 * pp(t, ts))
        place_text(c, '1 shop, 1993', 'mark', 50, INK, 250, 970, t, 'one', ts + 0.2, 'slide', rot=-3)
    tb = at(i, 'five hundred', -0.3)
    if t > tb:
        sc, a2 = slam(t, tb); place(c, stamp_c('546 SHOWROOMS', GRN, 84, -6, 3), 690, 880, sc, 0, a2)
    tm = at(i, 'Multibagger', -0.2)
    if t > tm: place_text(c, 'multibagger or trap?', 'pfi', 90, INK, 540, 1250, t, 'mt', tm, 'pop')
    src(c, t, 'Showrooms at 30 Sep 2026 · company update (Business Today)', 1.0, 1720)


def s2(c, t):
    i = 1; T0 = STARTS[i]
    place_text(c, 'THE EMPIRE', 'anton', 120, INK, 540, 260, t, 'em', T0 + 0.05, 'pop')
    tk = at(i, '1993', -0.3)
    if t > tk: place(c, label('SINCE 1993 · THRISSUR, KERALA', NAVY), 540, 400, pp(t, tk), -1)
    rows = [('INDIA (KALYAN)', 365, RED, 'three hundred sixty'), ('MIDDLE EAST', 38, ORG, 'thirty eight'), ('USA', 2, BLUE, 'two in the US'),
            ('UK', 2, NAVY, 'two in the UK'), ('CANDERE (ONLINE BRAND)', 138, TEAL, 'one hundred thirty')]
    d = ImageDraw.Draw(c)
    for k, (lab, v, col, ph) in enumerate(rows):
        tr = at(i, ph, -0.3)
        if t < tr: continue
        y = 530 + k * 170; q = eo(prog(t, tr, 0.8))
        c.alpha_composite(text_img(lab, 'osw5', 36, INK), (110, y - 70))
        n = max(1, round(min(v, 20) * q))
        for j in range(n):
            place(c, store(col), 150 + j * 33, y + 8, 0.6)
        num = text_img(f'{int(round(v * q))}', 'anton', 90, col); c.alpha_composite(num, (1000 - num.size[0], y - 52))
    src(c, t, 'Company Q2 FY27 update (Business Today) · up to 20 icons drawn', T0 + 1.0, 1720)


def s3(c, t):
    i = 2; T0 = STARTS[i]
    place_text(c, 'SALES', 'anton', 130, INK, 540, 260, t, 'sl', T0 + 0.05, 'pop')
    c.alpha_composite(text_img('REVENUE (₹ CR)', 'type', 30, GREY, 2), (110, 380))
    ta = at(i, 'nine thousand', -0.3); tb = at(i, 'thirty five', -0.6)
    rows = [('FY19', 9771, GREY, ta), ('FY21', 8573, GREY, ta + 0.4), ('FY23', 14071, BLUE, ta + 0.8), ('FY25', 25045, BLUE, tb - 0.4), ('FY26', 35743, GRN, tb)]
    bars(c, t, rows, 1200, 640, 35743, x0=160, gap=190, w=130)
    tf = at(i, 'four times', -0.3)
    if t > tf:
        sc, a = slam(t, tf); place(c, stamp_c('3.7X IN 7 YEARS', GRN, 80, -6, 11), 400, 560, sc, 0, a)
    src(c, t, 'Consolidated sales · Screener.in (FY19-FY26)', T0 + 1.0, 1720)


def s4(c, t):
    i = 3; T0 = STARTS[i]
    place_text(c, 'PROFIT', 'anton', 130, GRN, 540, 260, t, 'pf', T0 + 0.05, 'pop')
    c.alpha_composite(text_img('NET PROFIT (₹ CR)', 'type', 30, GREY, 2), (110, 380))
    tl = at(i, 'a loss', -0.3); tp = at(i, 'one thousand', -0.6)
    rows = [('FY21', -6, RED, tl), ('FY23', 432, BLUE, tl + 0.5), ('FY24', 596, BLUE, tl + 0.9), ('FY25', 714, BLUE, tp - 0.4), ('FY26', 1350, GRN, tp)]
    bars(c, t, rows, 1080, 560, 1350, x0=160, gap=190, w=130)
    tq = at(i, 'June quarter', -0.3)
    if t > tq:
        sc, a = slam(t, tq); place(c, stamp_c('JUNE QTR: ₹349 CR', TEAL, 70, -5, 21), 540, 1300, sc, 0, a)
        place_text(c, '+32% vs last year', 'mark', 46, INK, 540, 1420, t, 'jq', tq + 0.3, 'slide', rot=-2)
    tfy = at(i, 'in FY26', 0.0)
    if t > tfy:
        sc, a = slam(t, tfy); place(c, stamp_c('+89%', GRN, 80, 6, 22), 330, 560, sc, 0, a)
    src(c, t, 'Screener.in consolidated · Q1 FY27 results (Kotak Neo)', T0 + 1.0, 1720)


def s5(c, t):
    i = 4; T0 = STARTS[i]
    place_text(c, 'LAST QUARTER', 'anton', 110, INK, 540, 260, t, 'lq', T0 + 0.05, 'pop')
    tr = at(i, 'twenty six', -0.3)
    if t > tr:
        sc, a = slam(t, tr); place(c, stamp_c('REVENUE +26%', GRN, 96, -5, 31), 540, 520, sc, 0, a)
    ts = at(i, 'same store', -0.3)
    if t > ts:
        sc, a = slam(t, ts + 0.4); place(c, stamp_c('SAME-STORE +20%', ORG, 90, 4, 32), 540, 760, sc, 0, a)
    to = at(i, 'Old showrooms', -0.3)
    if t > to:
        for k in range(3):
            place(c, store((RED, GOLD, NAVY)[k]), 300 + k * 240, 1040, 1.5 * pp(t, to + 0.12 * k))
            if t > to + 0.6:
                q = eo(prog(t, to + 0.6 + 0.1 * k, 0.4)); d = ImageDraw.Draw(c); x = 300 + k * 240
                d.line((x, 1000 - 60 * q, x, 960), fill=GRN, width=10)
                d.polygon([(x - 22, 1000 - 60 * q), (x + 22, 1000 - 60 * q), (x, 960 - 60 * q - 30)], fill=GRN)
        place_text(c, 'old shops selling more = real demand', 'mark', 46, INK, 540, 1220, t, 'os', to + 0.6, 'slide', rot=-2)
    src(c, t, 'Q2 FY27 business update (Business Today, Kotak Neo, 7 Oct 2026)', T0 + 1.0, 1720)


def s6(c, t):
    i = 5; T0 = STARTS[i]
    ti = at(i, 'eighty seven', -0.3)
    if t > ti:
        place(c, label('IPO MAR 2021: ₹87 · LISTED 15% LOWER', NAVY), 540, 230, pp(t, ti), -1)
    p = prog(t, T0 + 0.1, 0.45)
    ox, oy, w, h = 60, 330 + (1 - eo(p)) * 600, 960, 760
    place(c, SZ.sheet_cut(w, h), ox + w / 2, oy + h / 2, 1.0, 0, clamp(p * 3))
    f = eio(prog(t, T0 + 0.4, 3.0))
    SZ.hand_chart(c, t, ox, oy, w, h, WEEKLY, WLAB, 300, 680, f, INK, YEL)
    n = len(WEEKLY)
    def xy(k, v): return ox + 90 + (w - 160) * k / (n - 1), oy + h - 70 - (v - 300) / 380 * (h - 140)
    if f > 0.6:
        x, y = xy(30, 344.75); marker_ellipse(c, x, y, 60, 40, prog(t, T0 + 2.6, 0.4), RED, 7, seed=3)
        place_text(c, '52-wk low ₹327', 'mark', 40, RED, x, y + 70, t, 'lo', T0 + 2.7, 'slide', rot=-3)
    if f > 0.8:
        x, y = xy(37, 612.6); place_text(c, 'high ₹648.95 (Jul)', 'mark', 40, GRN, x - 230, y - 40, t, 'hi', T0 + 3.0, 'slide', rot=-3)
    tn = at(i, 'five hundred sixty', -0.3)
    if t > tn:
        x, y = xy(n - 1, 560); place(c, text_img('₹560', 'anton', 80, GRN), x - 40, y + 90, pp(t, tn))
    tw = at(i, 'who owns', -0.3)
    if t > tw: place_text(c, 'so who owns it now?', 'pfi', 72, INK, 540, 1260, t, 'wo', tw, 'pop')
    src(c, t, 'Weekly closes: NSE via INDmoney · IPO listing: Business Standard', T0 + 0.6, 1440)


def s7(c, t):
    i = 6; T0 = STARTS[i]
    words_line(c, t, [("WHO", INK, T0 + 0.05), ("OWNS", INK, T0 + 0.2), ("IT", RED, T0 + 0.35)], 'anton', 120, 260, key='wo2')
    d = ImageDraw.Draw(c)
    tp = at(i, 'Promoters', -0.3)
    if t > tp:
        q = eo(prog(t, tp, 0.8)); c.alpha_composite(text_img('PROMOTERS (SEP 2026)', 'type', 28, GREY, 2), (110, 380))
        ww = int(62.85 / 70 * 700 * q); d.rounded_rectangle((110, 430, 110 + ww, 510), 12, fill=NAVY, outline=INK, width=4)
        c.alpha_composite(text_img(f'{62.85 * q:.1f}%', 'anton', 64, NAVY), (130 + ww, 428))
    th = at(i, 'Shareholders', -0.3)
    if t > th:
        v = 3.72 + (6.75 - 3.72) * eo(prog(t, at(i, 'six point seven', -0.3), 1.0)) if t > at(i, 'six point seven', -0.3) else 3.72
        c.alpha_composite(text_img('SHAREHOLDERS', 'type', 28, GREY, 2), (110, 580))
        place(c, text_img(f'{v:.2f} LAKH', 'anton', 120, GRN), 540, 700, pp(t, th))
        place(c, text_img('Dec 2023: 3.72 lakh  ·  Sep 2026: 6.75 lakh', 'type', 28, GREY, 1), 540, 790, pp(t, th + 0.4))
    tf = at(i, 'foreign investors', -0.3)
    if t > tf:
        c.alpha_composite(text_img('FOREIGN (FII) vs INDIAN FUNDS (DII)', 'type', 28, GREY, 2), (110, 900))
        rows = (('FII DEC 23', 26.21, GREY), ('FII SEP 26', 13.83, RED), ('DII DEC 23', 5.48, GREY), ('DII SEP 26', 14.41, GRN))
        for k, (lab, v, col) in enumerate(rows):
            y = 990 + k * 105; q = eo(prog(t, tf + 0.25 * k, 0.7)); ww = int(v / 30 * 560 * q)
            c.alpha_composite(text_img(lab, 'osw5', 34, INK), (110, y - 22))
            d.rounded_rectangle((330, y - 30, 330 + ww, y + 30), 10, fill=col, outline=INK, width=4)
            c.alpha_composite(text_img(f'{v * q:.1f}%', 'anton', 50, col), (346 + ww, y - 32))
    src(c, t, 'Shareholding & shareholder count: Screener.in (Dec 2023 vs Sep 2026)', T0 + 1.0, 1720)


def s8(c, t):
    i = 7; T0 = STARTS[i]
    if t > T0 + 0.1:
        p = prog(t, T0 + 0.1, 0.3); lw = text_w('THE CATCH', 'osw', 54, 2); x0 = 540 - (lw + 70) / 2
        place(c, warn_icon(YEL), x0 + 28, 262, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
        place(c, text_img('THE CATCH', 'osw', 54, YEL, 2), x0 + 70 + lw / 2, 260, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
    rows = [('P/E ABOUT 40', 'PRICED FOR GROWTH', ORG, 'forty times', 'Screener P/E 39.5 · 5 Nov 2026'),
            ('BORROWINGS ₹6,117 CR', 'MOSTLY GOLD LOANS', RED, 'six thousand', 'Mar 2026 · non-gold-loan debt: zero (Sep 2026)'),
            ('GOLD DEMAND', 'DRIVES EVERYTHING', RED, 'gold demand', 'Price swings + wedding season = sales swings')]
    for k, (h1, h2, col, ph, note) in enumerate(rows):
        tk = at(i, ph, -0.3)
        if t < tk: continue
        y = 520 + k * 330; q = pp(t, tk, 0.35, 1.3)
        place(c, cutout(Image.new('RGBA', (920, 260), (40, 38, 36, 255)), border=6, shadow=0.4, bcol=col), 540, y, q, (-0.8, 0.6, -0.5)[k])
        if q < 0.6: continue
        d = ImageDraw.Draw(c); bx = 150
        d.line((bx - 24, y - 44, bx + 24, y + 4), fill=col, width=12); d.line((bx - 24, y + 4, bx + 24, y - 44), fill=col, width=12)
        c.alpha_composite(text_img(h1, 'anton', 60, CREAM), (220, int(y - 100)))
        c.alpha_composite(text_img(h2, 'anton', 52, col), (220, int(y - 26)))
        c.alpha_composite(text_img(note, 'type', 24, (200, 194, 182), 1), (220, int(y + 50)))
    typed(c, 'Part 2: multibagger or trap? Not investment advice.', 'type', 28, (200, 194, 182), 1560, t, at(i, 'gold demand', 0.4), at(i, 'gold demand', 1.4))


def s9(c, t):
    i = 8; T0 = STARTS[i]
    q = pp(t, T0, 0.45, 1.2)
    place(c, SS._card(960, 860), 540, 600, q, -0.4)
    if q > 0.6:
        place(c, text_img('KALYAN JEWELLERS · PART 1', 'anton', 56, INK), 540, 230)
        d = ImageDraw.Draw(c); d.line((90, 272, 990, 272), fill=INK, width=4)
        rows = [('Price (5 Nov close)', '₹560 (+5.9%)', INK), ('IPO price (2021)', '₹87', INK), ('Showrooms', '546 · 4 regions', GRN), ('Sales FY26', '₹35,743 Cr', GRN),
                ('Profit FY26', '₹1,350 Cr', GRN), ('Promoters', '62.9%', NAVY), ('FII stake', '26.2% to 13.8%', RED), ('P/E', '39.5', ORG)]
        for k, (a_, b_, col) in enumerate(rows):
            tk = T0 + 0.3 + 0.08 * k
            if t < tk: continue
            y = 300 + k * 78
            c.alpha_composite(text_img(a_, 'osw5', 38, INK), (100, y))
            v = text_img(b_, 'anton', 44, col); c.alpha_composite(v, (980 - v.size[0], y - 2))
        SS.save_pulse(c, t, T0 + 1.2, 540, 1080, 'SAVE THIS')
    SS.send_frame(c, t, at(i, 'send it', -0.3), 'your Kalyan Jewellers group', y=1300)
    tf = at(i, 'Follow', -0.2)
    if t > tf:
        q2 = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1530, 0.5 + 0.5 * eback(q2), 0, clamp(q2 * 3))
    for k, ln in enumerate(['Price: NSE via INDmoney, 5 Nov 2026 · Fundamentals: Screener.in', 'Showrooms: company Q2 FY27 update (7 Oct 2026)', 'Not a buy/sell call. Education only. I may hold stocks named.']):
        place_text(c, ln, 'type', 22, GREY, 540, 1680 + k * 34, t, None, T0 + 0.3, 'fade', track=1)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
DARK_SCENES = {7}


def slam_times():
    return [at(0, 'five hundred', -0.3), at(2, 'four times', -0.3), at(3, 'June quarter', -0.3), at(4, 'twenty six', -0.3)] + [STARTS[k] + 0.05 for k in range(1, 8)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('MULTIBAGGER OR TRAP? · PART 1', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
    ImageDraw.Draw(c).line((60, 118, W - 60, 118), fill=col, width=2)
    ImageDraw.Draw(c).line((60, 118, 60 + (W - 120) * clamp(t / DUR), 118), fill=RED if not dark else YEL, width=8)


def scene_at(t):
    k = 0
    for i, s in enumerate(STARTS):
        if t >= s: k = i
    return k


def _trans(c, t):
    cols = [(GOLD, INK), (YEL, INK), (RED, YEL), (GRN, CREAM), (YEL, RED), (INK, YEL), (RED, YEL), (YEL, INK)]
    for bi, b in enumerate(B):
        d = 0.62
        if abs(t - b) > d / 2 + 0.12: continue
        for layer, delay in ((0, -0.07), (1, 0.0)):
            p = (t - (b - d / 2) - delay) / d
            if p <= 0 or p >= 1: continue
            p = eio(p); SWd, skew = 2050, 320
            xl = (W + 60) + p * (-(SWd + skew) - (W + 60) - 40)
            r = random.Random(bi * 10 + layer + 999)
            left = [(xl + r.uniform(-14, 14) - skew * (y / H), y) for y in range(0, H + 1, 40)]
            right = [(xl + SWd + r.uniform(-14, 14) - skew * (y / H), y) for y in range(H, -1, -40)]
            if layer == 0: left = [(x - 70, y) for x, y in left]; right = [(x + 70, y) for x, y in right]
            poly_fill(c, left + right, cols[bi % len(cols)][layer], 255, S=1)


def render(t):
    LOOP = 0.6
    if t > DUR - LOOP:
        a = _render(t); b = _render(1.4, loop=True); q = eio((t - (DUR - LOOP)) / LOOP)
        return (a * (1 - q) + b * q).astype(np.uint8)
    return _render(t)


def _render(t, loop=False):
    pbg, dbg = bgs()
    i = scene_at(t); dark = i in DARK_SCENES
    c = (dbg if dark else pbg).copy()
    st = STARTS[i]; en = STARTS[i + 1] if i + 1 < len(STARTS) else DUR
    SCENES[i](c, t)
    z = 1.0 + 0.04 * clamp((t - st) / (en - st))
    sx = sy = 0
    for ts in slam_times():
        if 0 <= t - ts < 0.35:
            k = math.exp(-(t - ts) * 14) * 9
            sx += k * math.sin((t - ts) * 90); sy += k * math.cos((t - ts) * 77)
    cw, ch = W / z, H / z
    cx, cy = W / 2 + sx, H * 0.47 + sy
    c = c.transform((W, H), Image.EXTENT, (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2), Image.BICUBIC)
    header(c, dark, t if not loop else 0); _trans(c, t)
    arr = np.asarray(c.convert('RGB')).astype(np.float32)
    g = grain_frames()[int(t * FPS) % 6]
    fl = 1 + 0.012 * math.sin(t * 37) * math.sin(t * 13)
    return np.clip(arr * fl + g[..., None], 0, 255).astype(np.uint8)
