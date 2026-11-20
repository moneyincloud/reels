"""Gold in India 1990-2026: every big fall and jump, and why. paper-collage style (male VO)"""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs, typed, drop, warn_icon
from fridge import follow_btn
import saveshare as SS
from antipo import sheet_cut, hand_chart, pp, src
from goldpredict import inr, card, tag, gold_stack, CLOSES, CLAB, transition as _tr

SH = ROOT + 'goldhist/'
SCRIPT = json.load(open(SH + 'script.json'))
DURS = json.load(open(SH + 'vo/durs.json'))
LEAD, TAIL = 0.15, 0.3
STARTS, VO = [], []
_t = 0.0
for i, d in enumerate(DURS):
    STARTS.append(_t); VO.append(_t + (0.1 if i == 0 else LEAD)); _t = VO[-1] + d + TAIL
DUR = _t + 1.8
B = STARTS[1:]
GREY = (120, 112, 104); TEAL = (20, 140, 130); ORG = (230, 120, 30); BLUE = (40, 100, 200); NAVY = (30, 60, 120)
GOLD = (214, 160, 40); GOLD2 = (245, 200, 80); SOFT = (252, 250, 244)

# RBI Handbook Table 35: average Mumbai gold price, Rs per 10 g, fiscal years 1990-91 .. 2025-26
FY = ['90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '00', '01', '02', '03', '04', '05', '06', '07', '08',
      '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25']
PX = [3451.52, 4297.63, 4103.66, 4531.87, 4667.24, 4957.60, 5070.71, 4347.07, 4268.17, 4393.56, 4473.60, 4579.12,
      5332.36, 5718.95, 6145.38, 6900.56, 9240.32, 9995.62, 12889.74, 15756.09, 19227.08, 25722.42, 30163.93,
      29190.39, 27414.55, 26534.26, 29665.28, 29300.08, 31193.41, 37017.91, 48723.22, 47999.25, 52730.77,
      60623.95, 75841.87, 118420.90]
LO, HI = math.log10(2500), math.log10(140000)


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def bars(c, t, show_to, hi=None, col=GRN, f=1.0, ox=70, oy=360, w=940, h=640, labels=True):
    """log-scale bar chart of FY prices. show_to: last index shown (float for growth); hi=(a,b) highlighted range"""
    place(c, sheet_cut(w, h), ox + w / 2, oy + h / 2, 1.0, -0.4)
    d = ImageDraw.Draw(c)
    x0, x1, y0, y1 = ox + 50, ox + w - 30, oy + 60, oy + h - 70
    n = len(PX); bw = (x1 - x0) / n
    d.line((x0, y1, x1, y1), fill=INK, width=4)
    for v, lb in ((5000, '5k'), (10000, '10k'), (30000, '30k'), (100000, '1L')):
        y = y1 - (math.log10(v) - LO) / (HI - LO) * (y1 - y0)
        d.line((x0, y, x1, y), fill=(200, 200, 210), width=2)
        c.alpha_composite(text_img(lb, 'osw5', 22, GREY), (ox + 6, int(y - 14)))
    for k, v in enumerate(PX):
        if k <= int(show_to): g = 1.0
        elif k == int(show_to) + 1: g = show_to - int(show_to)
        else: break
        hgt = (math.log10(v) - LO) / (HI - LO) * (y1 - y0) * g
        inh = hi and hi[0] <= k <= hi[1]
        fc = (col if inh else (205, 196, 180))
        xx = x0 + k * bw
        d.rectangle((xx + 2, y1 - hgt, xx + bw - 3, y1), fill=fc, outline=INK, width=2)
        if labels and (k % 5 == 0 or k == n - 1):
            lb = text_img("'" + FY[k], 'osw5', 22, GREY); c.alpha_composite(lb, (int(xx + bw / 2 - lb.size[0] / 2), int(y1 + 8)))
    c.alpha_composite(text_img('Rs per 10 g · yearly avg · log scale', 'osw5', 24, GREY), (ox + 60, oy + 18))
    return x0, x1, y0, y1, bw


def bar_xy(k, ox=70, oy=360, w=940, h=640):
    x0, x1, y0, y1 = ox + 50, ox + w - 30, oy + 60, oy + h - 70
    bw = (x1 - x0) / len(PX)
    return x0 + k * bw + bw / 2, y1 - (math.log10(PX[k]) - LO) / (HI - LO) * (y1 - y0)


def era(c, t, i, title, a, b, chg, col, tags, note=None, srcs=''):
    T0 = STARTS[i]
    words_line(c, t, title, 'anton', 104, 270, key=('t', i))
    show = min(len(PX) - 1, a + (b - a) * eo(prog(t, T0 + 0.4, 1.4))) if b > a else b
    bars(c, t, max(b, show) if i == 0 else show, (a, b), col)
    if t > T0 + 0.6:
        fy = lambda k: f"{1990 + k}-{(1991 + k) % 100:02d}"
        ln = f"₹{inr(PX[a])} ({fy(a)})  to  ₹{inr(PX[b])} ({fy(b)})"
        place(c, text_img(ln, 'anton', 46, INK), 540, 1050, pp(t, T0 + 0.6, 0.35))
    ts = T0 + 2.0
    if t > ts:
        sc, al = slam(t, ts); place(c, stamp_c(chg, col, 80, -5, i + 3), 540, 1180, sc, 0, al)
    for k, (ph, txt, tc, x, y, r) in enumerate(tags):
        tk = at(i, ph, -0.3)
        if t > tk:
            jx, jy, jr = jit(('e', i, k), t, 1.6, 0.3)
            place(c, tag(txt, tc, 50), x + jx, y + jy + 60, pp(t, tk, 0.35, 1.4), r + jr)
    if note:
        ph, txt = note; tn = at(i, ph, -0.2)
        if t > tn: place_text(c, txt, 'mark', 44, INK, 540, 1600, t, ('n', i), tn, 'slide', rot=-2)
    src(c, t, srcs, T0 + 1.0, 1680)


RBI = 'RBI Handbook of Statistics, Table 35 (Mumbai avg, FY)'


def s1(c, t):
    i = 0
    words_line(c, t, [("GOLD IN INDIA", INK, 0.1), ("1990-2026", GOLD, 0.4)], 'anton', 96, 270, key='h1')
    show = (len(PX) - 1) * eo(prog(t, 0.5, 3.2))
    bars(c, t, show, (0, 35), GOLD)
    k = int(show)
    xb, yb = bar_xy(k); place(c, text_img('₹' + inr(PX[k]), 'anton', 54, RED), min(max(xb, 160), 880), yb - 44)
    tc = at(i, 'crashed', -0.2)
    if t > tc:
        sc, a = slam(t, tc); place(c, stamp_c('IT CRASHED MANY TIMES', RED, 70, -5, 2), 540, 1110, sc, 0, a)
    tw = at(i, 'every big fall', -0.2)
    if t > tw:
        place(c, tag('EVERY FALL', RED, 60), 330, 1290, pp(t, tw, 0.35), -3)
        place(c, tag('EVERY JUMP', GRN, 60), 750, 1290, pp(t, tw + 0.5, 0.35), 3)
    ty = at(i, 'and why', -0.1)
    if t > ty:
        place_text(c, '...and WHY', 'mark', 70, INK, 540, 1460, t, 'wy', ty, 'slide', rot=-3)
    src(c, t, RBI, 1.0, 1680)


def s2(c, t):
    era(c, t, 1, [("1991", INK, STARTS[1] + 0.05), ("CRISIS", RED, STARTS[1] + 0.3)], 0, 1, '+24.5% IN 1 YEAR', GRN,
        [('bankrupt', 'FOREX CRISIS', RED, 300, 1270, -3), ('rupee crashed', 'RUPEE CRASHED', ORG, 760, 1290, 3)],
        ('world price fell', 'world gold: $375 → $357 (it FELL)'), RBI + ' · London $ price')


def s3(c, t):
    era(c, t, 2, [("1992", INK, STARTS[2] + 0.05), ("IMPORTS OPEN", BLUE, STARTS[2] + 0.3)], 1, 2, '-4.5%', RED,
        [('opened gold imports', 'GOLD CONTROL ACT GONE', BLUE, 540, 1260, -2), ('Smuggling', 'SMUGGLING DIED', INK, 320, 1400, 3),
         ('premium', 'PREMIUM VANISHED', TEAL, 760, 1410, -3)],
        None, 'Gold Control Act repealed 6 Jun 1990; ~110 t imported legally in 1992 · ' + 'RBI')


def s4(c, t):
    era(c, t, 3, [("1997-2001", INK, STARTS[3] + 0.05), ("NOWHERE", RED, STARTS[3] + 0.3)], 6, 11, '-10%, THEN FLAT', RED,
        [('central banks', 'EUROPE SELLING GOLD', RED, 540, 1260, -2), ('two hundred fifty two', '$252 · 20 JUL 1999', INK, 330, 1400, 3),
         ('twenty year low', '20-YEAR LOW', ORG, 770, 1410, -3)],
        None, 'UK sold half its reserves, 1999 (Kitco, LBMA) · ' + 'RBI')


def s5(c, t):
    era(c, t, 4, [("2002-2012", INK, STARTS[4] + 0.05), ("THE BIG RUN", GRN, STARTS[4] + 0.3)], 11, 22, '6.6x IN 11 YEARS', GRN,
        [('crisis', '2008 CRISIS', RED, 320, 1270, -3), ('printing money', 'US PRINTING MONEY', BLUE, 750, 1280, 3)],
        None, RBI)


def s6(c, t):
    era(c, t, 5, [("2013", INK, STARTS[5] + 0.05), ("TAPER TANTRUM", RED, STARTS[5] + 0.3)], 22, 25, '-12% OVER 3 YEARS', RED,
        [('slow money printing', 'FED: LESS MONEY', BLUE, 320, 1270, -3), ('twenty nine', 'WORLD GOLD -29% IN 2013', RED, 640, 1410, 2)],
        None, 'Taper tantrum: LBMA Alchemist · ' + 'RBI')


def s7(c, t):
    era(c, t, 6, [("2020", INK, STARTS[6] + 0.05), ("COVID", RED, STARTS[6] + 0.3)], 29, 30, '+31.6% IN 1 YEAR', GRN,
        [('Near zero', 'RATES NEAR ZERO', BLUE, 320, 1270, -3), ('stimulus', 'HUGE STIMULUS', ORG, 760, 1280, 3),
         ('two thousand dollars', '$2,000 FIRST TIME · AUG 2020', INK, 540, 1420, -2)],
        None, 'Reuters, Bloomberg (Aug 2020) · ' + 'RBI')


def s8(c, t):
    era(c, t, 7, [("2022-26", INK, STARTS[7] + 0.05), ("RECORDS", GRN, STARTS[7] + 0.3)], 31, 35, '2.5x IN 4 YEARS', GRN,
        [('wars', 'WARS', RED, 260, 1270, -3), ('central banks', 'CENTRAL BANKS BUYING', BLUE, 680, 1280, 3),
         ('Eight hundred', '863 TONNES IN 2025', GOLD, 540, 1420, -2)],
        ('one lakh eighteen', 'record $5,405/oz on 28 Jan 2026'), 'World Gold Council · ' + 'RBI')


def s9(c, t):
    i = 8; T0 = STARTS[i]
    words_line(c, t, [("NOW:", INK, T0 + 0.05), ("FALLING AGAIN", RED, T0 + 0.3)], 'anton', 104, 270, key='nw')
    place(c, sheet_cut(940, 600), 540, 690, 1.0, -0.6)
    f = clamp(prog(t, T0 + 0.4, 2.4))
    tip = hand_chart(c, t, 70, 390, 940, 600, CLOSES, CLAB, 120000, 146000, eo(f), col=INK, fill=GOLD2)
    place(c, text_img('MCX gold, Nov 2026 · Rs per 10 g', 'osw5', 30, GREY), 540, 430)
    if tip:
        k = min(len(CLOSES) - 1, int(eo(f) * (len(CLOSES) - 1) + 0.5))
        lab = text_img('₹' + inr(CLOSES[k]), 'anton', 58, RED if k > 2 else INK)
        c.alpha_composite(lab, (int(min(tip[0] - lab.size[0] / 2, 1000 - lab.size[0])), int(tip[1] - 90)))
    tf = at(i, 'almost fourteen', -0.3)
    if t > tf:
        sc, a = slam(t, tf); place(c, stamp_c('-13.7% SINCE 9 NOV', RED, 80, -5, 15), 540, 1110, sc, 0, a)
    for k, (ph, txt, col, x, y, r) in enumerate((('strong dollar', 'DOLLAR: 19-MONTH HIGH', BLUE, 540, 1270, -2), ('tough talking', 'HAWKISH FED', RED, 540, 1410, 2))):
        tk = at(i, ph, -0.3)
        if t > tk: place(c, tag(txt, col, 54), x, y, pp(t, tk, 0.35, 1.4), r)
    src(c, t, 'MCX Dec futures: INDmoney (9 Nov close → 20 Nov 2:53 PM) · PTI, 18 Nov', T0 + 1.0, 1680)


def s10(c, t):
    i = 9; T0 = STARTS[i]
    q = pp(t, T0, 0.45, 1.2)
    place(c, SS._card(960, 900), 540, 640, q, -0.4)
    if q > 0.6:
        place(c, text_img('WHY GOLD MOVES · CHEAT SHEET', 'anton', 50, INK), 540, 240)
        d = ImageDraw.Draw(c); d.line((90, 282, 990, 282), fill=INK, width=4)
        up = ['Fear: crises, wars, pandemics', 'Weak US dollar', 'Falling rupee', 'Rate cuts, money printing', 'Central banks buying']
        dn = ['Strong US dollar', 'Rate hikes (taper 2013)', 'Central banks selling (1999)', 'Lower import barriers (1992)']
        c.alpha_composite(text_img('RISES WHEN', 'anton', 48, GRN), (100, 300))
        for k, s in enumerate(up):
            if t > T0 + 0.4 + 0.1 * k: c.alpha_composite(text_img('+ ' + s, 'osw5', 36, INK), (110, 365 + k * 52))
        c.alpha_composite(text_img('FALLS WHEN', 'anton', 48, RED), (100, 640))
        for k, s in enumerate(dn):
            if t > T0 + 1.0 + 0.1 * k: c.alpha_composite(text_img('- ' + s, 'osw5', 36, INK), (110, 705 + k * 52))
        SS.save_pulse(c, t, T0 + 1.6, 540, 1160, 'SAVE THIS')
    tf = at(i, 'follow', -0.2)
    if t > tf:
        q2 = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1380, 0.5 + 0.5 * eback(q2), 0, clamp(q2 * 3))
    for k, ln in enumerate(['Sources: RBI Handbook Table 35, World Gold Council, LBMA, Reuters, PTI, INDmoney',
                            'Past moves do not predict future prices', 'Not a buy/sell call. Education only.']):
        place_text(c, ln, 'type', 22, GREY, 540, 1620 + k * 34, t, None, T0 + 0.3, 'fade', track=1)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]
DARK_SCENES = set()


def slam_times():
    return [at(0, 'crashed', -0.2), at(8, 'almost fourteen', -0.3)] + [STARTS[k] + 2.0 for k in range(1, 8)] + [STARTS[k] + 0.05 for k in range(1, 10)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('GOLD: WHY IT FELL & ROSE', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
    ImageDraw.Draw(c).line((60, 118, W - 60, 118), fill=col, width=2)
    ImageDraw.Draw(c).line((60, 118, 60 + (W - 120) * clamp(t / DUR), 118), fill=RED if not dark else YEL, width=8)


def transition(c, t):
    cols = [(GOLD, INK), (YEL, INK), (INK, GOLD), (TEAL, YEL), (YEL, RED), (INK, YEL), (RED, YEL), (GOLD, INK)]
    for bi, b in enumerate(B):
        d = 0.62
        if abs(t - b) > d / 2 + 0.12: continue
        for layer, delay in ((0, -0.07), (1, 0.0)):
            p = (t - (b - d / 2) - delay) / d
            if p <= 0 or p >= 1: continue
            p = eio(p); SWd, skew = 2050, 320
            xl = (W + 60) + p * (-(SWd + skew) - (W + 60) - 40)
            r = random.Random(bi * 10 + layer + 777)
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
    header(c, dark, t if not loop else 0); transition(c, t)
    arr = np.asarray(c.convert('RGB')).astype(np.float32)
    g = grain_frames()[int(t * FPS) % 6]
    fl = 1 + 0.012 * math.sin(t * 37) * math.sin(t * 13)
    return np.clip(arr * fl + g[..., None], 0, 255).astype(np.uint8)
