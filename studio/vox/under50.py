"""Under ₹50: 10 stocks tested on 5 fundamental rules — 5 passed, 5 failed (paper Vox, no captions)"""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs, warn_icon
from fridge import follow_btn
import tea as TEA
import saveshare as SS

SH = ROOT + 'under50/'
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

FAILS = [  # name, industry, price, reason, phrase, colour
    ('YES BANK', 'Private bank', '15.61', 'ROE just 7.1%', 'Yes Bank', BLUE),
    ('TRIDENT', 'Textiles', '21.28', 'Profit 3-yr CAGR -6%', 'Trident', PINK),
    ('IRB INFRA', 'Roads & tolls', '16.07', 'Debt ₹20,027 Cr, as big as reserves', 'IRB', ORG),
    ('JP POWER', 'Power', '12.97', '73% promoter shares pledged', 'JP Power', GOLD),
    ('EASEMYTRIP', 'Online travel', '5.81', 'Losses in 3 of 4 quarters', 'EaseMyTrip', TEAL),
]


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def pp(t, t0, d=0.35, s=1.6): return eback(prog(t, t0, d), s)


def src(c, t, txt, t0, y=1700, col=GREY):
    if t > t0: place_text(c, txt, 'type', 26, col, 540, y, t, None, t0, 'fade', track=1)


def chip(txt, col, size=34, fg=CREAM):
    tx = text_img(txt, 'osw5', size, fg); w, h = tx.size[0] + 28, tx.size[1] + 8
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), 12, fill=col)
    im.alpha_composite(tx, (14, 4)); return im


# ---------------- scenes ----------------
NAMES = ['SUZLON', 'SYNCOM', 'SAGILITY', 'IOB', 'CENTRAL BK', 'YES BANK', 'TRIDENT', 'IRB', 'JP POWER', 'EASEMYTRIP']
COLS = [TEAL, PURP, BLUE, NAVY, ORG, BLUE, PINK, ORG, GOLD, TEAL]


def s1(c, t):
    i = 0
    words_line(c, t, [("UNDER", INK, 0.0), ("₹50", RED, 0.12)], 'anton', 190, 300, key='u')
    for k, nm in enumerate(NAMES):
        tk = 0.15 + 0.09 * k
        if t < tk: continue
        x = 280 + (k % 2) * 520; y = 560 + (k // 2) * 150
        wob = 4 * math.sin(t * 3 + k)
        place(c, label(nm, COLS[k]), x, y, 1.0 * pp(t, tk), (-3, 3, -2, 2, -4, 4, -1, 1, -3, 3)[k] + wob * 0.3)
    tt = at(i, 'trap', -0.3)
    if t > tt:
        s_, a = slam(t, tt); place(c, stamp_c('TRAP?', RED, 150, -8, 11), 540, 1360, s_, 0, a)
    tp = at(i, 'Only five', -0.3)
    if t > tp:
        place(c, label('5 PASSED', GRN), 300, 1560, 1.4 * pp(t, tp), -4)
        place(c, label('5 FAILED', RED), 780, 1560, 1.4 * pp(t, tp + 0.25), 4)
    src(c, t, 'NSE prices via INDmoney, 28 Oct 2026 close', 0.8, 1690)


def s2(c, t):
    i = 1; T0 = STARTS[i] + 0.05
    place_text(c, 'THE 5 RULES', 'anton', 130, INK, 540, 290, t, 'r5', T0, 'pop')
    SS.checklist(c, t, [('PROFIT EVERY QUARTER', at(i, 'Profit every', 0.3)), ('LOW DEBT', at(i, 'Low debt', 0.3)),
                        ('ROE ABOVE 10%', at(i, 'Return on equity', 0.4)), ('NO PROMOTER PLEDGE', at(i, 'No promoter', 0.3)),
                        ('PROFIT GROWING', at(i, 'Growing', 0.3))], y0=520, gap=180)
    src(c, t, 'ROE = profit / shareholders\' money · bank NPA = bad loans', STARTS[i] + 1.0, 1520)


def s3(c, t):
    i = 2; T0 = STARTS[i] + 0.05
    place_text(c, '5 FAILED', 'anton', 130, RED, 540, 270, t, 'ff', T0, 'pop')
    for k, (nm, ind, pr, why, ph, col) in enumerate(FAILS):
        tk = at(i, ph, -0.25)
        if t < tk: continue
        y = 480 + k * 250; q = pp(t, tk, 0.35, 1.3)
        place(c, card_box(960, 228, SOFT), 540, y, q, (-0.8, 0.8, -0.5, 0.6, -0.6)[k])
        if q < 0.6: continue
        c.alpha_composite(text_img(nm, 'anton', 58, INK), (90, int(y - 96)))
        ch = chip(ind, col, 30); c.alpha_composite(ch, (95, int(y - 10)))
        c.alpha_composite(text_img('₹' + pr, 'anton', 44, GREY), (110 + ch.size[0], int(y - 16)))
        c.alpha_composite(text_img(why, 'osw5', 34, RED), (95, int(y + 42)))
        ts = tk + 0.45
        if t > ts:
            s_, a = slam(t, ts); place(c, stamp_c('FAILED', RED, 72, -8, 300 + k), 850, y - 20, s_, 0, a)
    src(c, t, 'Fundamentals: Screener.in (company filings), Sep 2026 quarter', STARTS[i] + 1.0, 1720)


def s4(c, t):
    i = 3; T0 = STARTS[i] + 0.05
    place_text(c, 'NOW THE', 'anton', 120, INK, 540, 520, t, 'n1', T0, 'pop')
    place_text(c, '5 THAT PASSED', 'anton', 140, GRN, 540, 680, t, 'n2', T0 + 0.15, 'pop')
    tl = at(i, 'low price', -0.3)
    if t > tl:
        place(c, label('LOW PRICE = THE REASON', ORG), 540, 940, 1.2 * pp(t, tl), -2)
        q = eo(prog(t, tl + 0.5, 0.3)); d = ImageDraw.Draw(c)
        d.line((170, 940, 170 + 740 * q, 930), fill=RED, width=16)
        if t > tl + 0.7:
            s_, a = slam(t, tl + 0.7); place(c, stamp_c('NO.', RED, 120, -6, 77), 540, 1150, s_, 0, a)


def pass_card(c, t, tk, y, nm, ind, col, pr, stats, k):
    if t < tk: return
    q = pp(t, tk, 0.4, 1.3)
    place(c, card_box(960, 560, SOFT), 540, y, q, (-0.6, 0.6)[k % 2])
    if q < 0.6: return
    c.alpha_composite(text_img(nm, 'anton', 64 if len(nm) > 14 else 76, INK), (90, int(y - 250)))
    ch = chip(ind, col, 36); c.alpha_composite(ch, (95, int(y - 150)))
    c.alpha_composite(text_img('₹' + pr, 'anton', 60, GREY), (115 + ch.size[0], int(y - 160)))
    for j, (lab, val, tj) in enumerate(stats):
        if t < tj: continue
        yy = y - 60 + j * 95; a = pp(t, tj, 0.3)
        c.alpha_composite(text_img(lab, 'osw5', 38, GREY), (100, int(yy)))
        v = text_img(val, 'anton', 56, GRN); place(c, v, 960 - v.size[0] / 2, yy + 26, a)
        if j < len(stats) - 1: ImageDraw.Draw(c).line((100, yy + 80, 960, yy + 80), fill=(225, 220, 210), width=2)
    ts = tk + 0.6
    if t > ts:
        s_, a = slam(t, ts); place(c, stamp_c('PASSED', GRN, 64, 7, 500 + k), 820, y - 125, s_, 0, a)


def s5(c, t):
    i = 4
    t1 = at(i, 'Syncom', -0.3); t2 = at(i, 'Sagility', -0.3)
    pass_card(c, t, t1, 500, 'SYNCOM FORMULATIONS', 'Pharma', PURP, '20.33',
              [('ROE', '17.6%', at(i, 'Return on', 0)), ('DEBT', 'ABOUT ₹1 CR', at(i, 'almost no', 0)), ('PROFIT 3-YR CAGR', '+50%', at(i, 'almost no', 0.6))], 0)
    pass_card(c, t, t2, 1140, 'SAGILITY', 'Healthcare services', BLUE, '45.29',
              [('PROFIT 3-YR CAGR', '+86%', at(i, 'Profit up', 0)), ('ROE', '10.6%', at(i, 'Profit up', 0.4)), ('DEBT VS RESERVES', '16%', at(i, 'Profit up', 0.8))], 1)
    src(c, t, 'Screener.in (company filings), 28 Oct 2026', STARTS[i] + 1.0, 1730)


def s6(c, t):
    i = 5
    t1 = at(i, 'Indian Overseas', -0.3); t2 = at(i, 'Central Bank', -0.3)
    pass_card(c, t, t1, 500, 'INDIAN OVERSEAS BANK', 'PSU bank', NAVY, '29.02',
              [('ROE', '14.9%', at(i, 'Return on', 0)), ('NET BAD LOANS (NNPA)', '0.16%', at(i, 'net bad', 0)), ('Q2 PROFIT', '+56% YoY', at(i, 'net bad', 0.8))], 0)
    pass_card(c, t, t2, 1140, 'CENTRAL BANK OF INDIA', 'PSU bank', ORG, '28.93',
              [('PROFIT 3-YR CAGR', '+40%', at(i, 'Profit growing', 0)), ('ROE', '11.6%', at(i, 'Profit growing', 0.4)), ('NET BAD LOANS (NNPA)', '0.31%', at(i, 'Profit growing', 0.8))], 1)
    src(c, t, 'Screener.in & bank results, Sep 2026 quarter', STARTS[i] + 1.0, 1730)


def s7(c, t):
    i = 6
    t1 = at(i, 'Suzlon', -0.3)
    pass_card(c, t, t1, 640, 'SUZLON ENERGY', 'Wind energy', TEAL, '37.30',
              [('ROE', '39.7%', at(i, 'Return on', 0)), ('DEBT VS RESERVES', '8%', at(i, 'almost debt', 0)), ('PROFIT 3-YR CAGR', '+163%', at(i, 'almost debt', 0.6))], 0)
    tb = at(i, 'But promoters', -0.3)
    if t > tb:
        q = pp(t, tb, 0.4, 1.3); place(c, card_box(900, 230, (255, 238, 232)), 540, 1180, q, 1)
        if q > 0.6:
            place(c, warn_icon(RED), 160, 1180, 1.5)
            c.alpha_composite(text_img('CATCH: PROMOTERS OWN 11.7%', 'anton', 54, RED), (230, 1120))
            c.alpha_composite(text_img('Q2 results due 29 Oct 2026', 'osw', 36, GREY), (232, 1196))
    src(c, t, 'Screener.in (company filings), 28 Oct 2026', STARTS[i] + 1.0, 1450)


def s8(c, t):
    i = 7; T0 = STARTS[i] + 0.05
    if t > T0:
        s_, a = slam(t, T0 + 0.05); place(c, stamp_c('PASSED IS NOT BUY', RED, 130, -5, 808), 540, 330, s_, 0, a)
    catches = [('IOB · CENTRAL BK', 'Govt may sell stake / raise money (dilution)', 'government'),
               ('SYNCOM', '₹33 Cr of profit is other income', 'one-time'),
               ('SAGILITY', '3-year average ROE only 7.6%', 'one-time'),
               ('SUZLON', 'Promoter 11.7% · results due 29 Oct', 'Check the latest')]
    for k, (h, s, ph) in enumerate(catches):
        tk = at(i, ph, -0.35) + (0.5 if k == 2 else 0)
        if t < tk: continue
        y = 580 + k * 250; q = pp(t, tk, 0.35, 1.3)
        place(c, card_box(940, 210, SOFT), 540, y, q, (-1, 1, -0.6, 0.8)[k])
        if q > 0.6:
            place(c, warn_icon(ORG), 150, y, 1.4)
            c.alpha_composite(text_img(h, 'anton', 56, INK), (220, int(y - 62)))
            c.alpha_composite(text_img(s, 'osw', 36, GREY), (222, int(y + 12)))


def s9(c, t):
    i = 8; T0 = STARTS[i] + 0.05
    SS.cheat_sheet(c, t, T0, 'UNDER ₹50 · 5 PASSED', [('SUZLON', 'WIND · ROE 39.7%', GRN), ('IOB', 'PSU BANK · ROE 14.9%', GRN),
                                                      ('SYNCOM', 'PHARMA · ROE 17.6%', GRN), ('CENTRAL BK', 'PSU BANK · ROE 11.6%', GRN),
                                                      ('SAGILITY', 'HEALTHCARE · ROE 10.6%', GRN)], y0=160)
    SS.send_frame(c, t, at(i, 'send it', -0.3), 'your cheap-stock friend', y=1150)
    tf = at(i, 'Follow', -0.2)
    if t > tf:
        q = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1360, 0.5 + 0.5 * eback(q), 0, clamp(q * 3))
    for k, ln in enumerate(['Prices: NSE close 28 Oct 2026 via INDmoney.', 'Fundamentals: Screener.in (company filings).',
                            'A rules check, not a recommendation.', 'I may hold some of these stocks.',
                            'Education only. Not investment advice.']):
        place_text(c, ln, 'type', 24, (210, 204, 192), 540, 1500 + k * 38, t, None, T0 + 0.3, 'fade', track=1)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]


def slam_times():
    return [at(0, 'trap', -0.3)] + [at(2, ph, 0.2) for *_, ph, _c in FAILS] + [STARTS[k] + 0.05 for k in range(1, 8)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('UNDER ₹50 CHECK', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
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
            r = random.Random(bi * 10 + layer + 8100)
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
    z = 1.0 + 0.03 * clamp((t - st) / (en - st))
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
