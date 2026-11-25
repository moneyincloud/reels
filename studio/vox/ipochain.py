"""How an IPO works, the full chain with Lenskart: papers, bid, allotment, where money goes, listing, 1-year timeline, sell costs (STT/GST/DP), tax (collage, male VO)"""
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

SH = ROOT + 'ipochain/'
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
PURP = (120, 70, 170)
PX = json.load(open(SH + 'ohlc.json'))
NODES = ['PAPERS', 'BID', 'ALLOT', 'MONEY', 'LIST', '1 YEAR', 'COSTS', 'TAX']
NODE_OF = {1: 0, 2: 1, 3: 2, 4: 3, 5: 3, 6: 4, 7: 5, 8: 5, 9: 6, 10: 7, 11: 7}


@functools.lru_cache(None)
def card(w, h, fill=(253, 251, 246)):
    return cutout(Image.new('RGBA', (w, h), fill + (255,)), border=5, shadow=0.35)


@functools.lru_cache(None)
def node_img(txt, state):
    col = {0: (200, 194, 182), 1: RED, 2: GRN}[state]
    tx = text_img(txt, 'anton', 26, CREAM if state else INK)
    w, h = tx.size[0] + 22, tx.size[1] + 10
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 10, fill=col, outline=INK, width=3); im.alpha_composite(tx, (11, 5))
    return im


def chain(c, t, i, y=165):
    if i not in NODE_OF: return
    cur = NODE_OF[i]; xs = [72 + k * 133 for k in range(8)]
    d = ImageDraw.Draw(c)
    d.line((xs[0], y, xs[-1], y), fill=INK, width=4)
    for k, nm in enumerate(NODES):
        st = 2 if k < cur else (1 if k == cur else 0)
        place(c, node_img(nm, st), xs[k], y, 1.12 if k == cur else 0.95)


def s1(c, t):
    i = 0
    dy, a = drop(t, 0.1, 360)
    if a > 0: place(c, SZ.clipping(1.0, 'HOW AN IPO WORKS', 'THE FULL CHAIN', 'REAL EXAMPLE: LENSKART · NOV 2025 TO NOV 2026'), 540, 380 + dy, 0.92, -2, a)
    tc = at(i, 'full chain', -0.3)
    for k, nm in enumerate(NODES):
        tk = tc + 0.12 * k
        if t < tk: continue
        r_, cc = divmod(k, 4); x = 170 + cc * 247; y = 720 + r_ * 170
        place(c, label(nm, (NAVY, TEAL, BLUE, GRN, ORG, PURP, RED, INK)[k]), x, y, eback(prog(t, tk, 0.3)), (-3, 2, -2, 3)[cc])
    tw = at(i, 'what you pay', -0.3)
    if t > tw: place_text(c, 'money · GST · brokerage · tax', 'mark', 50, INK, 540, 1120, t, 'mg', tw, 'slide', rot=-2)
    tl = at(i, 'Lenskart', -0.3)
    if t > tl:
        sc, a2 = slam(t, tl); place(c, stamp_c('REAL EXAMPLE: LENSKART', RED, 76, -5, 3), 540, 1300, sc, 0, a2)


def s2(c, t):
    i = 1; T0 = STARTS[i]; chain(c, t, i)
    place_text(c, 'STEP 1: PAPERS', 'anton', 110, INK, 540, 300, t, 'p1', T0 + 0.05, 'pop')
    ts = at(i, 'SEBI', -0.3)
    if t > ts:
        place(c, card(800, 330), 540, 560, pp(t, ts), -1.5)
        if t > ts + 0.2:
            place(c, text_img('DRAFT PROSPECTUS → SEBI', 'anton', 52, INK) if False else text_img('DRAFT PAPERS TO SEBI', 'anton', 56, INK), 540, 480)
            place(c, text_img('filed Jul 2025 · approved Oct 2025', 'type', 30, GREY, 1), 540, 560)
    tb = at(i, 'bankers', -0.3)
    if t > tb: place(c, label('BANKERS PRICE THE ISSUE', NAVY), 540, 660, pp(t, tb), 2)
    tp = at(i, 'price band', -0.3)
    if t > tp:
        place(c, text_img('PRICE BAND', 'type', 36, GREY, 3), 540, 880, pp(t, tp))
        sc, a = slam(t, tp + 0.4); place(c, stamp_c('₹382 - ₹402', RED, 120, -4, 5), 540, 1040, sc, 0, a)
    src(c, t, 'Business Standard (DRHP Jul 2025, SEBI nod Oct 2025) · RHP', T0 + 1.0, 1720)


def s3(c, t):
    i = 2; T0 = STARTS[i]; chain(c, t, i)
    place_text(c, 'STEP 2: YOU BID', 'anton', 110, INK, 540, 300, t, 'p2', T0 + 0.05, 'pop')
    tu = at(i, 'UPI', -0.3)
    if t > tu:
        place(c, cutout(Image.new('RGBA', (560, 760), (30, 34, 44, 255)), border=6, shadow=0.4), 540, 820, pp(t, tu), -1)
        if t > tu + 0.2:
            place(c, cutout(Image.new('RGBA', (480, 640), (253, 251, 246, 255)), border=0, shadow=0), 540, 820)
            place(c, text_img('UPI MANDATE', 'anton', 52, INK), 540, 560)
            place(c, text_img('Lenskart IPO', 'osw5', 40, GREY), 540, 630)
            tl = at(i, 'thirty seven', -0.3)
            if t > tl:
                place(c, text_img('37 shares × ₹402', 'osw5', 44, INK), 540, 740, pp(t, tl))
                place(c, text_img('₹14,874', 'anton', 100, INK), 540, 850, pp(t, tl + 0.3))
            tk = at(i, 'blocks', -0.3)
            if t > tk:
                sc, a = slam(t, tk); place(c, stamp_c('BLOCKED, NOT DEBITED', RED, 46, -6, 7), 540, 1010, sc, 0, a)
    src(c, t, 'Lot size & price: RHP via Business Standard, Chittorgarh', T0 + 1.0, 1720)


def s4(c, t):
    i = 3; T0 = STARTS[i]; chain(c, t, i)
    place_text(c, 'STEP 3: ALLOTMENT', 'anton', 110, INK, 540, 300, t, 'p3', T0 + 0.05, 'pop')
    c.alpha_composite(text_img('SUBSCRIBED (TIMES)', 'type', 30, GREY, 2), (110, 420))
    d = ImageDraw.Draw(c)
    rows = [('BIG FUNDS (QIB)', 40.35, NAVY), ('RETAIL', 7.46, ORG), ('TOTAL', 28.24, RED)]
    tt = at(i, 'twenty eight', -0.4)
    for k, (lab, v, col) in enumerate(rows):
        tk = tt + 0.25 * k
        if t < tk: continue
        y = 540 + k * 130; q = eo(prog(t, tk, 0.8)); ww = int(v / 41 * 620 * q)
        c.alpha_composite(text_img(lab, 'osw5', 38, INK), (110, y - 70))
        d.rounded_rectangle((110, y - 22, 110 + ww, y + 34), 10, fill=col, outline=INK, width=4)
        c.alpha_composite(text_img(f'{v * q:.1f}x', 'anton', 52, col), (126 + ww, y - 26))
    tn = at(i, 'No shares', -0.3)
    if t > tn:
        place(c, card(860, 260), 540, 1120, pp(t, tn), 1)
        if t > tn + 0.2:
            place(c, text_img('NOT ALLOTTED?', 'anton', 64, INK), 540, 1070)
            place(c, text_img('the UPI block is released', 'osw5', 44, GRN), 540, 1160)
    src(c, t, 'Subscription: Kotak Neo · allotment 6 Nov 2025 (Zerodha)', T0 + 1.0, 1720)


def s5(c, t):
    i = 4; T0 = STARTS[i]; chain(c, t, i)
    place_text(c, 'WHERE THE MONEY WENT', 'anton', 88, INK, 540, 300, t, 'wm', T0 + 0.05, 'pop')
    tt = at(i, 'seven thousand', -0.3)
    if t > tt:
        place(c, text_img('₹7,278 CR RAISED', 'anton', 90, INK), 540, 460, pp(t, tt))
    d = ImageDraw.Draw(c); x0, x1, y0, y1 = 90, 990, 560, 760
    tl = at(i, 'Only two', -0.3); to = at(i, 'Five thousand', -0.3)
    split = x0 + (x1 - x0) * 2150 / 7278
    if t > tl:
        q = eo(prog(t, tl, 0.6)); d.rounded_rectangle((x0, y0, x0 + (split - x0) * q, y1), 14, fill=GRN, outline=INK, width=5)
        if q > 0.9:
            place(c, text_img('₹2,150', 'anton', 60, CREAM), (x0 + split) / 2, 640)
            place(c, text_img('30%', 'anton', 40, CREAM), (x0 + split) / 2, 710)
            place(c, label('TO LENSKART', GRN), (x0 + split) / 2 + 40, 850, pp(t, tl + 0.5), -2)
            place(c, text_img('fresh issue: new shares', 'type', 28, GREY, 1), (x0 + split) / 2 + 60, 930, pp(t, tl + 0.7))
    if t > to:
        q = eo(prog(t, to, 0.6)); d.rounded_rectangle((split, y0, split + (x1 - split) * q, y1), 14, fill=ORG, outline=INK, width=5)
        if q > 0.9:
            place(c, text_img('₹5,128', 'anton', 72, CREAM), (split + x1) / 2, 640)
            place(c, text_img('70%', 'anton', 40, CREAM), (split + x1) / 2, 710)
            place(c, label('TO OLD SHAREHOLDERS', ORG), 640, 1060, pp(t, to + 0.5), 2)
            place(c, text_img('offer for sale (OFS): founders, funds sold', 'type', 28, GREY, 1), 600, 1140, pp(t, to + 0.7))
    ts = at(i, 'who sold', -0.2)
    if t > ts:
        sc, a = slam(t, ts); place(c, stamp_c('COMPANY GOT ONLY 30%', RED, 76, -5, 15), 540, 1340, sc, 0, a)
    src(c, t, 'RHP via Chittorgarh · OFS money never reaches the company', T0 + 1.0, 1720)


def s6(c, t):
    i = 5; T0 = STARTS[i]; chain(c, t, i)
    place_text(c, "LENSKART'S ₹2,150 CR", 'anton', 90, INK, 540, 300, t, 'ls', T0 + 0.05, 'pop')
    c.alpha_composite(text_img('PLANNED USE (₹ CR)', 'type', 30, GREY, 2), (110, 420))
    rows = [('NEW STORES', 272.6, 'new stores', BLUE), ('STORE RENT', 591.4, 'rent', TEAL), ('TECH & CLOUD', 213.4, 'tech', PURP), ('MARKETING', 320.1, 'marketing', ORG)]
    d = ImageDraw.Draw(c)
    for k, (lab, v, ph, col) in enumerate(rows):
        tk = at(i, ph, -0.2)
        if t < tk: continue
        y = 540 + k * 150; q = eo(prog(t, tk, 0.6)); ww = int(v / 600 * 560 * q)
        c.alpha_composite(text_img(lab, 'osw5', 40, INK), (110, y - 74))
        d.rounded_rectangle((110, y - 20, 110 + ww, y + 36), 10, fill=col, outline=INK, width=4)
        c.alpha_composite(text_img(f'₹{v * q:,.1f}', 'anton', 48, col), (126 + ww, y - 24))
    if t > at(i, 'marketing', 0.4):
        place(c, text_img('rest: acquisitions + general use', 'type', 30, GREY, 1), 540, 1170, pp(t, at(i, 'marketing', 0.4)))
    src(c, t, 'Objects of the issue: RHP (Zerodha, Inc42, Business Standard)', T0 + 0.6, 1720)


def s7(c, t):
    i = 6; T0 = STARTS[i]; chain(c, t, i)
    place_text(c, 'LISTING DAY', 'anton', 120, INK, 540, 300, t, 'ld', T0 + 0.05, 'pop')
    place(c, label('10 NOV 2025', NAVY), 540, 410, pp(t, T0 + 0.3), -2)
    d = ImageDraw.Draw(c); base = 1150
    to = at(i, 'three ninety', -0.3)
    d.rounded_rectangle((230, base - 560, 410, base), 12, fill=GREY, outline=INK, width=5)
    place(c, text_img('₹402', 'anton', 70, INK), 320, base - 610)
    place(c, text_img('ISSUE PRICE', 'osw5', 34, GREY), 320, base + 40)
    if t > to:
        q = eo(prog(t, to, 0.6)); hg = int(560 * (390 / 402) * q)
        d.rounded_rectangle((670, base - hg, 850, base), 12, fill=RED, outline=INK, width=5)
        place(c, text_img('₹390', 'anton', 70, RED), 760, base - hg - 50)
        place(c, text_img('LISTING OPEN', 'osw5', 34, GREY), 760, base + 40)
    d.line((120, base, 960, base), fill=INK, width=5)
    tp = at(i, 'Three percent', -0.3)
    if t > tp:
        sc, a = slam(t, tp); place(c, stamp_c('-3% ON DAY 1', RED, 100, -6, 17), 540, 1330, sc, 0, a)
    src(c, t, 'Listing price: 5paisa, Kotak Neo', T0 + 1.0, 1720)


MARKS = [(1, '30 DAYS', 'anchors 50%'), (10, '90 DAYS', 'anchors rest'), (23, '6 MONTHS', '60% unlocked'), (52, '1 YEAR', '')]
MLABS = [''] * 53
MLABS[0] = 'NOV 25'; MLABS[13] = 'FEB'; MLABS[26] = 'MAY'; MLABS[39] = 'AUG'; MLABS[52] = 'NOV 26'


def tl_chart(c, t, f, marks_t):
    ox, oy, w, h = 50, 300, 980, 760
    place(c, SZ.sheet_cut(w, h), ox + w / 2, oy + h / 2, 1.0, 0, 1)
    SZ.hand_chart(c, t, ox, oy, w, h, PX, MLABS, 350, 780, f, INK, YEL)
    def P(k, v): return (ox + 90 + (w - 160) * k / 52, oy + h - 70 - (v - 350) / 430 * (h - 140))
    d = ImageDraw.Draw(c)
    x0, y0 = P(0, 402); x1, _ = P(52, 402)
    for xx in range(int(x0), int(x1), 28): d.line((xx, y0, xx + 14, y0), fill=RED, width=3)
    c.alpha_composite(text_img('issue ₹402', 'type', 26, RED, 1), (int(x1 - 160), int(y0 + 8)))
    for (k, nm, sub), tm in zip(MARKS, marks_t):
        if t < tm: continue
        x, y = P(k, PX[k]); q = pp(t, tm, 0.3)
        mi = MARKS.index((k, nm, sub)); hh = (150, 260, 170, 120)[mi]
        d.line((x, y - 20, x, y - hh + 30), fill=INK, width=3)
        place(c, label(nm, (NAVY, TEAL, RED, GRN)[mi]), min(max(x, 150), 930), y - hh, 0.62 * q)
        if sub: place(c, text_img(sub, 'type', 24, INK, 1), min(max(x, 150), 930), y - hh + 48, q)
        d.ellipse((x - 10, y - 10, x + 10, y + 10), fill=CREAM, outline=INK, width=4)


def s8(c, t):
    i = 7; T0 = STARTS[i]; chain(c, t, i)
    place_text(c, 'THE ONE-YEAR TIMELINE', 'anton', 90, INK, 540, 1170, t, 'ty', T0 + 0.05, 'pop')
    ts = at(i, 'six months', 0)
    f = eio(prog(t, T0 + 0.3, ts - T0 + 0.5))
    tl_chart(c, t, f * 23 / 52 + 0.0, [at(i, 'thirty', -0.2), at(i, 'ninety', -0.2), at(i, 'six months', -0.2), 1e9])
    tb = at(i, 'block deals', -0.4)
    if t > tb:
        sc, a = slam(t, tb); place(c, stamp_c('BLOCK DEALS: BIG SELLERS', RED, 64, -4, 19), 540, 1320, sc, 0, a)
    src(c, t, 'Weekly closes: NSE via INDmoney · lock-ins: BSE, Business Today', T0 + 1.0, 1720)


def s9(c, t):
    i = 8; T0 = STARTS[i]; chain(c, t, i)
    f = 23 / 52 + (1 - 23 / 52) * eio(prog(t, T0 + 0.1, 2.2))
    tl_chart(c, t, f, [T0 - 9, T0 - 9, T0 - 9, T0 + 2.3])
    tp = at(i, 'seven twenty', -0.3)
    if t > tp:
        place(c, text_img('₹723', 'anton', 120, GRN), 540, 1180, pp(t, tp))
    tu = at(i, 'eighty', -0.3)
    if t > tu:
        sc, a = slam(t, tu); place(c, stamp_c('+80% IN ONE YEAR', GRN, 90, -5, 23), 540, 1360, sc, 0, a)
    src(c, t, 'Price 25 Nov 2026, NSE via INDmoney. Past returns do not repeat.', T0 + 1.0, 1720)


def s10(c, t):
    i = 9; T0 = STARTS[i]; chain(c, t, i)
    place_text(c, 'COSTS TO SELL 1 LOT', 'anton', 100, INK, 540, 300, t, 'cs', T0 + 0.05, 'pop')
    place(c, receipt() if False else card(900, 1000), 540, 900, pp(t, T0 + 0.2), -0.6)
    if t > T0 + 0.4:
        place(c, text_img('SALE: 37 × ₹723.35 = ₹26,764', 'osw5', 44, INK), 540, 470)
        ImageDraw.Draw(c).line((130, 510, 950, 510), fill=INK, width=3)
    rows = [('Brokerage (delivery)', '₹0*', 'Brokerage'), ('STT 0.1% (to govt)', '₹26.76', 'STT'), ('Exchange + SEBI fees', '₹0.85', 'Exchange'),
            ('GST 18% on fees', '₹0.15', 'GST'), ('DP charge (per sale)', '₹21.83', 'DP charge')]
    for k, (a_, b_, ph) in enumerate(rows):
        tk = at(i, ph, -0.2)
        if t < tk: continue
        y = 560 + k * 100
        c.alpha_composite(text_img(a_, 'osw5', 44, INK), (140, y))
        v = text_img(b_, 'anton', 50, INK); c.alpha_composite(v, (940 - v.size[0], y - 4))
    ta = at(i, 'About fifty', -0.3)
    if t > ta:
        ImageDraw.Draw(c).line((130, 1080, 950, 1080), fill=INK, width=4)
        c.alpha_composite(text_img('TOTAL', 'anton', 60, INK), (140, 1100))
        v = text_img('≈ ₹50', 'anton', 70, RED) if False else text_img('~₹50', 'anton', 70, RED); c.alpha_composite(v, (940 - v.size[0], 1094))
        sc, a = slam(t, ta + 0.3); place(c, stamp_c('0.2% OF SALE', RED, 70, -6, 41), 540, 1320, sc, 0, a)
    src(c, t, '*varies by broker · DP ₹18.5+GST (INDmoney) · Zerodha, INDmoney pricing', T0 + 1.0, 1720)


def s11(c, t):
    i = 10; T0 = STARTS[i]
    if t > T0 + 0.1:
        p = prog(t, T0 + 0.1, 0.3); lw = text_w('THEN TAX', 'osw', 54, 2); x0 = 540 - (lw + 70) / 2
        place(c, warn_icon(YEL), x0 + 28, 262, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
        place(c, text_img('THEN TAX', 'osw', 54, YEL, 2), x0 + 70 + lw / 2, 260, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
    tg = at(i, 'eleven thousand', -0.3)
    if t > tg:
        place(c, text_img('GAIN: ₹26,764 - ₹14,874 = ₹11,890', 'osw5', 46, CREAM), 540, 400, pp(t, tg))
    for k, (h1, h2, h3, ph, col) in enumerate((('SOLD WITHIN 1 YEAR', '20% STCG', '= ₹2,378 tax', 'Within a year', RED),
                                             ('SOLD AFTER 1 YEAR', '12.5% LTCG', 'only above ₹1.25 lakh gains/yr', 'After a year', GRN))):
        tk = at(i, ph, -0.3)
        if t < tk: continue
        y = 700 + k * 380; q = pp(t, tk, 0.35, 1.3)
        place(c, cutout(Image.new('RGBA', (920, 320), (40, 38, 36, 255)), border=6, shadow=0.4, bcol=col), 540, y, q, (-0.8, 0.8)[k])
        if q > 0.6:
            place(c, text_img(h1, 'osw5', 44, (200, 194, 182)), 540, y - 100)
            place(c, text_img(h2, 'anton', 100, col), 540, y)
            place(c, text_img(h3, 'osw5', 42, CREAM), 540, y + 100)
    typed(c, 'Rates FY 2026-27 (Budget 2026). Plus cess. Not tax advice.', 'type', 28, (200, 194, 182), 1480, t, at(i, 'After a year', 0.5), at(i, 'After a year', 1.6))


def s12(c, t):
    i = 11; T0 = STARTS[i]
    q = pp(t, T0, 0.45, 1.2)
    place(c, SS._card(960, 980), 540, 680, q, -0.4)
    if q > 0.6:
        place(c, text_img('IPO CHAIN · CHEAT SHEET', 'anton', 56, INK), 540, 230)
        d = ImageDraw.Draw(c); d.line((90, 272, 990, 272), fill=INK, width=4)
        rows = [('1. Papers to SEBI', 'price band', INK), ('2. You bid (UPI)', 'money blocked', INK), ('3. Allotment', 'or unblocked', INK),
                ('4. Fresh issue', 'to company', GRN), ('   OFS', 'to sellers', ORG), ('5. Listing day', 'can fall', RED),
                ('6. Lock-ins', '30d · 90d · 6m', RED), ('7. Sell costs', 'STT + fees + GST + DP', INK), ('8. Tax', '20% / 12.5%', INK)]
        for k, (a_, b_, col) in enumerate(rows):
            tk = T0 + 0.3 + 0.07 * k
            if t < tk: continue
            y = 300 + k * 86
            c.alpha_composite(text_img(a_, 'osw5', 40, INK), (100, y))
            v = text_img(b_, 'anton', 42, col); c.alpha_composite(v, (980 - v.size[0], y - 2))
    SS.save_pulse(c, t, at(i, 'Save', -0.2), 540, 1270, 'SAVE THIS')
    tf = at(i, 'Follow', -0.2)
    if t > tf:
        q2 = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1460, 0.5 + 0.5 * eback(q2), 0, clamp(q2 * 3))
    for k, ln in enumerate(['Prices: NSE via INDmoney, 25 Nov 2026', 'IPO facts: RHP via Chittorgarh, Zerodha, Business Standard', 'Not a buy/sell call. Education only.']):
        place_text(c, ln, 'type', 22, GREY, 540, 1680 + k * 34, t, None, T0 + 0.3, 'fade', track=1)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12]
DARK_SCENES = {10}


def slam_times():
    return [at(0, 'Lenskart', -0.3), at(1, 'price band', 0.1), at(2, 'blocks', -0.3), at(4, 'who sold', -0.2), at(6, 'Three percent', -0.3),
            at(7, 'block deals', -0.4), at(8, 'eighty', -0.3), at(9, 'About fifty', 0)] + [STARTS[k] + 0.05 for k in range(1, 11)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('HOW AN IPO WORKS', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
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
