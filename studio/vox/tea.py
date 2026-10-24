"""REAL P&L EP 9: Tea money into TFCI (paper Vox style)."""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random, datetime as dt
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs
from fridge import follow_btn

SH = ROOT + 'tea/'
SCRIPT = json.load(open(SH + 'script.json'))
DURS = json.load(open(SH + 'vo/durs.json'))
LEAD, TAIL = 0.15, 0.26
STARTS, VO = [], []
_t = 0.0
for i, d in enumerate(DURS):
    STARTS.append(_t); VO.append(_t + (0.1 if i == 0 else LEAD)); _t = VO[-1] + d + TAIL
DUR = _t + 1.6
B = STARTS[1:]
TEA = (176, 110, 60); CUPW = (250, 248, 242); SOFT = (253, 251, 246)

ROWS = [(dt.date.fromisoformat(a), float(b)) for a, b in (l.split() for l in open(SH + 'closes.txt'))]
# daily SIP model
SER = []
_prev = dt.date(2026, 2, 1); _u = 0; _inv = 0
for d, p in ROWS:
    amt = (d - _prev).days * 60; _prev = d; _u += amt / p; _inv += amt
    SER.append((d, p, _inv, _u * p))


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def card_box(w, h, fill=SOFT, out=INK, r=22, sh=10):
    im = Image.new('RGBA', (w + sh, h + sh), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((sh, sh, w + sh - 1, h + sh - 1), radius=r, fill=INK)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=r, fill=fill, outline=out, width=6)
    return im


@functools.lru_cache(None)
def cup(steam=0):
    S = 2; w, h = 200, 220
    im = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda pts: [(x * S, y * S) for x, y in pts]
    d.ellipse(P([(10, 190), (190, 215)]), fill=(230, 226, 216), outline=INK, width=5 * S)
    d.polygon(P([(30, 90), (170, 90), (150, 200), (50, 200)]), fill=CUPW, outline=INK)
    d.line(P([(30, 90), (170, 90), (150, 200), (50, 200), (30, 90)]), fill=INK, width=6 * S, joint='curve')
    d.ellipse(P([(30, 80), (170, 104)]), fill=TEA, outline=INK, width=5 * S)
    d.arc(P([(150, 110), (200, 170)]), 270, 90, fill=INK, width=10 * S)
    d.rectangle(P([(60, 130), (140, 160)]), fill=(214, 90, 60))
    for k in range(3):
        x = 65 + k * 35; ph = steam + k * 1.7
        pts = [(x + 8 * math.sin(ph + j * 0.8), 70 - j * 10) for j in range(6)]
        d.line(P(pts), fill=(170, 166, 158), width=5 * S, joint='curve')
    return cutout(im.resize((w, h), Image.LANCZOS), border=8)


@functools.lru_cache(None)
def coin(r=60):
    S = 3; im = Image.new('RGBA', (r * S, r * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((0, 0, r * S - 1, r * S - 1), fill=(214, 150, 30), outline=INK, width=3 * S)
    d.ellipse((4 * S, 3 * S, r * S - 6 * S, r * S - 8 * S), fill=YEL)
    im = im.resize((r, r), Image.LANCZOS)
    tx = text_img('₹', 'pop', int(r * 0.55), (150, 96, 10)); comp(im, tx, (r - tx.size[0]) / 2, (r - tx.size[1]) / 2 - 2)
    return im


@functools.lru_cache(None)
def stock_card():
    im = card_box(520, 300, SOFT)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, 519, 90), radius=22, fill=INK); d.rectangle((0, 60, 519, 90), fill=INK)
    t1 = text_img('TFCI', 'anton', 64, YEL); comp(im, t1, 30, 45 - t1.size[1] // 2)
    t2 = text_img('NSE', 'type', 30, CREAM, 2); comp(im, t2, 520 - t2.size[0] - 30, 45 - t2.size[1] // 2)
    t3 = text_img('Tourism Finance', 'osw', 44, INK); comp(im, t3, 30, 120)
    t4 = text_img('Corporation of India', 'osw', 44, INK); comp(im, t4, 30, 180)
    return im


# chart helpers
CX0, CX1, CY0, CY1 = 120, 980, 430, 1150


def chart(c, t, upto_date, t0, show_inv=True):
    d = ImageDraw.Draw(c)
    d.rounded_rectangle((80, 390, 1000, 1240), radius=24, fill=SOFT, outline=INK, width=6)
    vmin, vmax = 55, 165
    n = len(ROWS)
    x_of = lambda k: CX0 + (CX1 - CX0) * k / (n - 1)
    y_of = lambda v: CY1 - (CY1 - CY0) * (v - vmin) / (vmax - vmin)
    for v in (60, 80, 100, 120, 140, 160):
        y = y_of(v); d.line((CX0, y, CX1, y), fill=(220, 214, 200), width=2)
        place(c, text_img(f'₹{v}', 'osw5', 26, (130, 124, 112)), CX0 - 2, y - 16)
    for m, lab in ((2, 'FEB'), (4, 'APR'), (6, 'JUN'), (8, 'AUG'), (10, 'OCT')):
        k = next(i for i, (dd, _) in enumerate(ROWS) if dd.month == m)
        place(c, text_img(lab, 'osw', 28, (110, 104, 96)), x_of(k), CY1 + 50)
    kmax = max(i for i, (dd, _) in enumerate(ROWS) if dd <= upto_date)
    f = eio(prog(t, t0, 1.6))
    kshow = int(kmax * f) if t0 is not None else kmax
    pts = [(x_of(k), y_of(ROWS[k][1])) for k in range(0, kshow + 1)]
    if len(pts) > 1: stroke(c, pts, 8, GRN if upto_date.month >= 7 else INK)
    return x_of, y_of, kshow


# ---------- scenes ----------
def s1(c, t):
    i = 0
    words_line(c, t, [("6", INK, 0.0), ("CUPS", INK, 0.08), ("TO", INK, 0.16), ("2", RED, 0.26)], 'anton', 150, 270, key='h')
    for k in range(6):
        x = 190 + (k % 3) * 350; y = 640 + (k // 3) * 360
        tk = 0.05 + k * 0.08
        p = eback(prog(t, tk, 0.35), 1.5)
        jx, jy, jr = jit(('cup', k), t, 1.5, 0.5)
        place(c, cup(round(t * 6) % 6 * 1.0), x + jx, y + jy, 1.25 * p, jr)
        if k >= 2:
            tx = at(i, 'two', -0.4) + (k - 2) * 0.12
            if t > tx:
                pp = prog(t, tx, 0.18)
                stroke(c, [(x - 110, y - 110), (x - 110 + 220 * pp, y - 110 + 220 * pp)], 14, RED)
                if pp >= 1:
                    q = prog(t, tx + 0.18, 0.18)
                    stroke(c, [(x + 110, y - 110), (x + 110 - 220 * q, y - 110 + 220 * q)], 14, RED)
    tw = at(i, 'whole plan', -0.3)
    if t > tw:
        place_text(c, 'that was the whole plan', 'mark', 66, RED, 540, 1400, t, 'wp', tw, 'slide', rot=-2)


def s2(c, t):
    i = 1
    place_text(c, 'THE MATH', 'anton', 130, INK, 540, 270, t, 'mt', STARTS[1] + 0.05, 'pop')
    rows = [('Four cups', '4 cups', INK), ('fifteen', '× ₹15', INK), ('sixty', '= ₹60/day', GRN)]
    for k, (ph, lab, col) in enumerate(rows):
        tk = at(i, ph, -0.25)
        if t > tk:
            place_text(c, lab.replace('×', 'x'), 'anton', 150, col, 540, 520 + k * 210, t, ('m', k), tk, 'pop')
    tm = at(i, 'miss', -0.3)
    if t > tm:
        place_text(c, "too small to miss", 'mark', 70, RED, 540, 1260, t, 'sm', tm, 'slide', rot=-2)
        for k in range(5):
            tk = tm + k * 0.1
            place(c, coin(70), 240 + k * 150, 1430 - 30 * math.sin(k), eback(prog(t, tk, 0.3), 1.5))


def s3(c, t):
    i = 2
    place_text(c, 'TEA MONEY GOES TO...', 'anton', 100, INK, 540, 270, t, 'tm', STARTS[2] + 0.05, 'pop')
    place(c, cup(round(t * 6) % 6), 300, 620, 1.3, -18)
    st = STARTS[2] + 0.3
    for k in range(6):
        ph = ((t - st) * 1.4 + k / 6) % 1
        if t < st: break
        x = 380 + ph * 240; y = 680 + ph * ph * 380
        place(c, coin(56), x, y, 1, ph * 300)
    tt = at(i, 'Tourism', -0.4)
    if t > tt:
        p = eback(prog(t, tt, 0.4), 1.5)
        jx, jy, jr = jit('sc', t, 1.5, 0.4)
        place(c, stock_card(), 600 + jx, 1180 + jy, p, jr - 2)
    if t > at(i, 'one stock', -0.2):
        place_text(c, 'one stock only', 'mark', 60, RED, 560, 1470, t, 'os', at(i, 'one stock', -0.2), 'slide', rot=-2)


def s4(c, t):
    i = 3
    items = [('Two hundred', 260, 'DAYS', INK), ('One thousand', 1040, 'CUPS SKIPPED', RED), ('Fifteen', 15600, 'INVESTED', GRN)]
    for k, (ph, v, lab, col) in enumerate(items):
        tk = at(i, ph, -0.25)
        if t < tk: continue
        f = eo(prog(t, tk, 0.9))
        y = 380 + k * 400
        p = eback(prog(t, tk, 0.35), 1.5)
        place(c, card_box(820, 320), 540, y + 140, p)
        txt = ('₹' if k == 2 else '') + f'{int(v * f):,}'
        if k == 2: txt = '₹' + C_inr(int(v * f))
        place(c, text_img(txt, 'anton', 150, col), 540, y + 110, p)
        place(c, text_img(lab, 'osw', 50, INK, 3), 540, y + 235, p)


def C_inr(v):
    s = str(int(v))
    if len(s) <= 3: return s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2: parts.insert(0, head[-2:]); head = head[:-2]
    if head: parts.insert(0, head)
    return ','.join(parts + [tail])


def s5(c, t):
    i = 4
    place_text(c, '5 MONTHS: NOTHING', 'anton', 104, INK, 540, 270, t, 'nm', STARTS[4] + 0.05, 'pop')
    x_of, y_of, ks = chart(c, t, dt.date(2026, 6, 30), STARTS[4] + 0.2)
    ts = at(i, 'sideways', -0.2)
    if t > ts:
        sc, a = slam(t, ts)
        place(c, stamp_c('SIDEWAYS', GREY_(), 110, -6, 401), 540, 760, sc, 0, a)
    if t > at(i, 'sat there', -0.3):
        place_text(c, 'value ~ invested', 'mark', 60, RED, 540, 1380, t, 'vi', at(i, 'sat there', -0.3), 'slide', rot=-2)


def GREY_():
    return (110, 104, 96)


def s6(c, t):
    i = 5
    place_text(c, 'THEN JULY CAME', 'anton', 120, GRN, 540, 270, t, 'jc', STARTS[5] + 0.05, 'pop')
    x_of, y_of, ks = chart(c, t, dt.date(2026, 10, 19), STARTS[5] + 0.3)
    k75 = next(i2 for i2, (dd, _) in enumerate(ROWS) if dd == dt.date(2026, 7, 10))
    if t > at(i, 'seventy', -0.3):
        place(c, label(f'₹75', INK), x_of(k75) - 20, y_of(75) + 70)
    if t > at(i, 'one fifty', -0.3):
        place(c, label('₹156', GRN), x_of(len(ROWS) - 1) - 170, y_of(156) + 10)
        marker_ellipse(c, x_of(len(ROWS) - 1) - 10, y_of(156), 70, 50, prog(t, at(i, 'one fifty', -0.3), 0.5), RED, 8, seed=7)
    tc = at(i, 'climbing', -0.2)
    if t > tc:
        place_text(c, 'TFCI doubled', 'mark', 66, RED, 540, 1380, t, 'db', tc, 'slide', rot=-2)


@functools.lru_cache(None)
def label(txt, col):
    tx = text_img(txt, 'anton', 52, CREAM)
    w, h = tx.size[0] + 30, tx.size[1] + 8
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=14, fill=col)
    comp(im, tx, 15, 4); return im


def s7(c, t):
    i = 6
    place_text(c, 'TODAY', 'anton', 140, INK, 540, 270, t, 'td', STARTS[6] + 0.05, 'pop')
    p = eback(prog(t, STARTS[6] + 0.2, 0.35), 1.5)
    place(c, card_box(820, 230), 540, 520, p)
    place(c, text_img('TEA MONEY IN', 'osw', 40, (110, 104, 96), 3), 540, 470, p)
    place(c, text_img('₹15,600', 'anton', 110, INK), 540, 555, p)
    tw = at(i, 'twenty', -0.3)
    if t > tw:
        f = eo(prog(t, tw, 1.0))
        pp = eback(prog(t, tw, 0.35), 1.5)
        place(c, card_box(820, 300, (235, 248, 238), GRN), 540, 880, pp)
        place(c, text_img('WORTH NOW', 'osw', 40, GRN, 3), 540, 790, pp)
        place(c, text_img('₹' + C_inr(15600 + 12980 * f), 'anton', 150, GRN), 540, 900, pp)
    tp = at(i, 'profit', -0.3)
    if t > tp:
        sc, a = slam(t, tp)
        place(c, stamp_c('+₹12,980', GRN, 110, -6, 402), 540, 1200, sc, 0, a)
    tq = at(i, 'eighty', -0.2)
    if t > tq:
        place_text(c, '+83%', 'anton', 140, RED, 540, 1420, t, 'pc', tq, 'pop')


def s8(c, t):
    i = 7
    place_text(c, 'NOT SELLING', 'anton', 130, INK, 540, 270, t, 'ns', STARTS[7] + 0.05, 'pop')
    p = eback(prog(t, STARTS[7] + 0.2, 0.4), 1.5)
    # calendar
    place(c, card_box(460, 420), 540, 680, p)
    d = ImageDraw.Draw(c)
    if p > 0.9:
        d.rounded_rectangle((316, 476, 770, 560), radius=20, fill=RED)
        place(c, text_img('1 YEAR', 'anton', 64, CREAM), 543, 516)
        place(c, text_img('FEB 2027', 'anton', 110, INK), 545, 700)
        place(c, text_img('first buys turn long-term', 'osw5', 34, (90, 85, 80)), 545, 810)
    tl = at(i, 'long term', -0.2)
    if t > tl:
        place_text(c, 'LTCG: first ₹1.25 lakh/yr tax-free', 'anton', 58, INK, 540, 1060, t, 'lt', tl, 'slide')
    tz = at(i, 'tax free', -0.2)
    if t > tz:
        sc, a = slam(t, tz)
        place(c, stamp_c('TAX ₹0', GRN, 140, -8, 403), 540, 1300, sc, 0, a)


def s9(c, t):
    i = 8
    place_text(c, '4 CUPS OF TEA.', 'anton', 120, CREAM, 540, 300, t, 'fc', STARTS[8] + 0.05, 'pop')
    place_text(c, "that's all it took", 'mark', 64, YEL, 540, 430, t, 'at', at(i, "That's all", -0.2), 'slide', rot=-2)
    tw = at(i, 'What small', -0.2)
    if t > tw:
        place_text(c, 'WHAT HABIT WOULD YOU SWAP?', 'anton', 70, CREAM, 540, 600, t, 'wh', tw, 'pop')
    tfo = at(i, 'Follow', -0.2)
    if t > tfo:
        pp = prog(t, tfo, 0.35)
        place(c, follow_btn(), 540, 800, 0.5 + 0.5 * eback(pp), 0, clamp(pp * 3))
    place_text(c, '*Modelled: ₹60/day at daily closing price', 'type', 28, (210, 204, 192), 540, 980, t, None, STARTS[8] + 0.3, 'fade', track=1)
    place_text(c, '2 Feb - 19 Oct 2026 · Not investment advice', 'type', 28, (210, 204, 192), 540, 1025, t, None, STARTS[8] + 0.4, 'fade', track=1)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]


def header(c, dark):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('REAL P&L · EP 9', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
    ImageDraw.Draw(c).line((60, 118, W - 60, 118), fill=col, width=2)
    ImageDraw.Draw(c).line((60, 118, 300, 118), fill=col, width=6)


def transition(c, t):
    cols = [(YEL, INK), (TEA, CREAM), (INK, YEL), (GRN, INK), (RED, YEL), (INK, GRN), (YEL, TEA), (TEA, YEL)]
    for bi, b in enumerate(B):
        d = 0.5
        if abs(t - b) > d / 2 + 0.12: continue
        for layer, delay in ((0, -0.05), (1, 0.0)):
            p = (t - (b - d / 2) - delay) / d
            if p <= 0 or p >= 1: continue
            p = eio(p); SWd, skew = 2050, 320
            xl = (W + 60) + p * (-(SWd + skew) - (W + 60) - 40)
            r = random.Random(bi * 10 + layer + 5300)
            left = [(xl + r.uniform(-14, 14) - skew * (y / H), y) for y in range(0, H + 1, 40)]
            right = [(xl + SWd + r.uniform(-14, 14) - skew * (y / H), y) for y in range(H, -1, -40)]
            if layer == 0:
                left = [(x - 70, y) for x, y in left]; right = [(x + 70, y) for x, y in right]
            poly_fill(c, left + right, cols[bi % len(cols)][layer], 255, S=1)


def slam_times():
    return [at(4, 'sideways', -0.2), at(6, 'profit', -0.3), at(7, 'tax free', -0.2)]


def scene_at(t):
    k = 0
    for i, s in enumerate(STARTS):
        if t >= s: k = i
    return k


def render(t):
    pbg, dbg = bgs()
    i = scene_at(t); dark = (i == 8)
    c = (dbg if dark else pbg).copy()
    st = STARTS[i]; en = STARTS[i + 1] if i + 1 < len(STARTS) else DUR
    SCENES[i](c, t)
    z = 1.0 + 0.035 * clamp((t - st) / (en - st))
    sx = sy = 0
    for ts in slam_times():
        if 0 <= t - ts < 0.35:
            k = math.exp(-(t - ts) * 14) * 8
            sx += k * math.sin((t - ts) * 90); sy += k * math.cos((t - ts) * 77)
    cw, ch = W / z, H / z
    cx, cy = W / 2 + sx, max(ch / 2, H * 0.47) + sy
    c = c.transform((W, H), Image.EXTENT, (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2), Image.BICUBIC)
    header(c, dark); transition(c, t)
    arr = np.asarray(c.convert('RGB')).astype(np.float32)
    g = grain_frames()[int(t * FPS) % 6]
    fl = 1 + 0.012 * math.sin(t * 37) * math.sin(t * 13)
    return np.clip(arr * fl + g[..., None], 0, 255).astype(np.uint8)
