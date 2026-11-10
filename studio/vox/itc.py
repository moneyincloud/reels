"""ITC: you use it every day - products, business split, profit share, future plans, stock. Collage style, female VO."""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import slam, stamp_c, bgs, drop
from fridge import follow_btn
import tea as TEA

SH = ROOT + 'itc/'
SCRIPT = json.load(open(SH + 'script.json'))
DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO = [], []
_t = 0.0
for i, d in enumerate(DURS):
    STARTS.append(_t); VO.append(_t + (0.1 if i == 0 else 0.15)); _t = VO[-1] + d + 0.28
DUR = _t + 1.6
B = STARTS[1:]
NAVY = (12, 48, 104); BLUE = (40, 100, 200); GREY = (120, 112, 104); GOLD = (214, 160, 40); TEAL = (20, 140, 130)
SOFT = (252, 250, 244)
label = TEA.label
IMG = SH + 'img/'


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase); assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def pp(t, t0, d=0.35, s=1.6): return eback(prog(t, t0, d), s)


def src(c, t, txt, t0, y=1720, col=GREY):
    if t > t0: place_text(c, txt, 'type', 24, col, 540, y, t, None, t0, 'fade', track=1)


@functools.lru_cache(None)
def _img(name): return Image.open(IMG + name).convert('RGB')


@functools.lru_cache(None)
def print_card(name, w):
    im = _img(name); h = int(w * im.size[1] / im.size[0])
    return cutout(im.resize((w, h), Image.LANCZOS).convert('RGBA'), border=16, shadow=0.38)


@functools.lru_cache(None)
def logo_card(h=200):
    lg = _img('logo.png'); w = int(h * lg.size[0] / lg.size[1])
    lg = lg.resize((w, h), Image.LANCZOS).convert('RGBA')
    card = Image.new('RGBA', (w + 60, h + 50), (255, 255, 255, 255)); card.alpha_composite(lg, (30, 25))
    return cutout(card, border=0, shadow=0.35)


@functools.lru_cache(None)
def notebook():
    w, h = 340, 400
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((20, 0, w - 1, h - 1), 18, fill=(40, 110, 200), outline=INK, width=5)
    for y in range(30, h - 20, 34): d.ellipse((6, y, 34, y + 18), outline=INK, width=4)
    d.rectangle((52, 150, w - 18, 230), fill=(255, 255, 255), outline=INK, width=4)
    im.alpha_composite(text_img('Classmate', 'pop', 38, INK), (62, 165))
    return cutout(im, border=0, shadow=0.3)


def tape(c, x, y, rot):
    place(c, Image.new('RGBA', (150, 44), (246, 226, 150, 190)), x, y, 1.0, rot)


def flash(c, t, t0, d=0.14, a=0.85):
    if 0 <= t - t0 < d:
        c.alpha_composite(Image.new('RGBA', c.size, (255, 255, 255, int(255 * (1 - (t - t0) / d) * a))))


def product(c, t, t0, name, x, y, w, rot, nb=False):
    if t < t0: return
    p = pp(t, t0, 0.35, 1.5)
    im = notebook() if nb else print_card(name, w)
    place(c, im, x, y + (1 - eo(prog(t, t0, 0.35))) * 140, p, rot)
    tape(c, x, y - im.size[1] / 2 + 10, rot * 2)


def hbar(c, t, rows, y0, gap, maxw, vmax, x0=120):
    d = ImageDraw.Draw(c)
    for k, (lab, v, col, tk, note) in enumerate(rows):
        if t < tk: continue
        y = y0 + k * gap; q = eo(prog(t, tk, 0.8)); wv = int(v / vmax * maxw * q)
        place(c, text_img(lab, 'osw', 40, INK), x0 + text_img(lab, 'osw', 40, INK).size[0] / 2, y - 48)
        d.rounded_rectangle((x0, y, x0 + max(wv, 8), y + 70), 14, fill=col, outline=INK, width=5)
        place(c, text_img(f'₹{int(v * q):,} CR', 'anton', 52, INK), x0 + wv + 130, y + 36)
        if note and q > 0.9: place(c, text_img(note, 'osw5', 30, GREY), x0 + text_img(note, 'osw5', 30, GREY).size[0] / 2, y + 104)


# ---------------- scenes ----------------
def s0(c, t):
    i = 0
    flash(c, t, 0.0, 0.18, 0.9)
    place(c, logo_card(230), 540, 560, pp(t, 0.05, 0.35, 1.3), -2)
    place_text(c, 'YOU USE ITC', 'anton', 120, INK, 540, 880, t, 'h1', at(i, 'You use', -0.15), 'pop')
    place_text(c, 'EVERY DAY', 'anton', 120, BLUE, 540, 1010, t, 'h2', at(i, 'every day', -0.15), 'pop')
    for k, (n, x, y, r) in enumerate([('aashirvaad.png', 200, 1500, -6), ('bingo.png', 540, 1520, 3), ('darkfantasy.png', 880, 1500, 5)]):
        product(c, t, 0.4 + k * 0.15, n, x, y, 270, r)
    tb = at(i, 'seventy', -0.2)
    if t > tb:
        sc, a = slam(t, tb); place(c, stamp_c('74% OF PROFIT = CIGARETTES', RED, 64, -6, 3), 540, 1200, sc, 0, a)
    if t > 0.3: place_text(c, 'Logo & product photos: ITC, for identification only. Not sponsored.', 'type', 22, GREY, 540, 1720, t, None, 0.3, 'fade', track=1)


def s1(c, t):
    i = 1
    place(c, label('A DAY WITH ITC', BLUE), 540, 230, pp(t, STARTS[i]), -3)
    items = [('Aashirvaad', 'aashirvaad.png', 290, 620, -5), ('Dark Fantasy', 'darkfantasy.png', 800, 600, 4),
             ('Bingo', 'bingo.png', 290, 1170, 4), ('Yippee', 'yippee.png', 800, 1180, -4)]
    for k, (ph, n, x, y, r) in enumerate(items):
        product(c, t, at(i, ph, -0.25), n, x, y, 400, r)
    for k, (ph, tm) in enumerate([('Aashirvaad', '7 AM'), ('Dark Fantasy', '11 AM'), ('Bingo', '5 PM'), ('Yippee', '9 PM')]):
        tk = at(i, ph, -0.25)
        if t > tk:
            x, y = items[k][2], items[k][3]
            place(c, label(tm, INK), x, y - 270, pp(t, tk + 0.1), -4)


def s2(c, t):
    i = 2
    place(c, label('A DAY WITH ITC', BLUE), 540, 230, 1, -3)
    items = [('Classmate', None, 290, 620, -4, True), ('Savlon', 'savlon.png', 800, 610, 4, False),
             ('Fiama', 'fiama.png', 300, 1170, 3, False), ('Mangaldeep', 'mangaldeep.png', 800, 1170, -4, False)]
    for k, (ph, n, x, y, r, nb) in enumerate(items):
        product(c, t, at(i, ph, -0.25), n, x, y, 380, r, nb)
    ta = at(i, 'All ITC', -0.2)
    if t > ta:
        sc, a = slam(t, ta); place(c, logo_card(170), 540, 1500, sc, -3, a)
        place(c, stamp_c('ALL ITC', BLUE, 90, 6, 4), 820, 1560, sc, 0, a)


def s3(c, t):
    i = 3
    place(c, logo_card(200), 540, 600, pp(t, STARTS[i]), 2)
    place_text(c, 'SO HOW DOES ITC', 'anton', 100, INK, 540, 900, t, 'q1', STARTS[i] + 0.1, 'pop')
    place_text(c, 'MAKE ITS MONEY?', 'anton', 110, RED, 540, 1030, t, 'q2', at(i, 'make', -0.2), 'pop')


def s4(c, t):
    i = 4
    place(c, label('REVENUE · JUL–SEP 2026 (Q2 FY27)', INK), 540, 230, pp(t, STARTS[i]), -2)
    rows = [('CIGARETTES', 15536, RED, at(i, 'cigarettes', -0.2), 'gross, incl. taxes'),
            ('FMCG – OTHERS', 6967, BLUE, at(i, 'Other FMCG', -0.2), 'up 15.7% · atta, biscuits, snacks…'),
            ('AGRI', 4452, GRN, at(i, 'Agri', -0.2), ''),
            ('PAPER & PACKAGING', 3016, GOLD, at(i, 'Paper', -0.2), '')]
    hbar(c, t, rows, 470, 270, 600, 15536)
    src(c, t, 'Consolidated segment revenue, Q2 FY27 · ITC results via Investywise', STARTS[i] + 0.5)


def s5(c, t):
    i = 5
    place(c, label('BUT LOOK AT PROFIT', RED), 540, 230, pp(t, STARTS[i]), -3)
    d = ImageDraw.Draw(c)
    cx, cy, R = 540, 820, 330
    parts = [(74, RED, 'CIGARETTES'), (11, BLUE, 'FMCG'), (10, GRN, 'AGRI'), (5, GOLD, 'PAPER')]
    p = eo(prog(t, at(i, 'seventy', -0.3), 1.2)); a0 = -90
    for v, col, lab in parts:
        sweep = 360 * v / 100 * p
        if sweep > 0.5: d.pieslice((cx - R, cy - R, cx + R, cy + R), a0, a0 + sweep, fill=col, outline=INK, width=5)
        a0 += sweep
    d.ellipse((cx - R * 0.5, cy - R * 0.5, cx + R * 0.5, cy + R * 0.5), fill=SOFT, outline=INK, width=5)
    place(c, text_img('SEGMENT', 'osw', 34, GREY), cx, cy - 30); place(c, text_img('PROFIT', 'osw', 34, GREY), cx, cy + 14)
    tb = at(i, 'seventy', -0.2)
    if t > tb:
        sc, a = slam(t, tb); place(c, stamp_c('74% CIGARETTES', RED, 80, -6, 5), 540, 1300, sc, 0, a)
    if t > at(i, 'FMCG', -0.2):
        place_text(c, 'FMCG: just 11%', 'mark', 70, BLUE, 540, 1470, t, 'fm', at(i, 'FMCG', -0.2), 'slide', rot=-2)
    src(c, t, 'Share of segment EBIT, Q2 FY27 · INDmoney analysis of ITC results', STARTS[i] + 0.5)


def s6(c, t):
    i = 6
    place(c, label('PROFIT · Q2', INK), 540, 230, pp(t, STARTS[i]), -2)
    d = ImageDraw.Draw(c); base = 1150
    for k, (lab, v, col, tk) in enumerate([('Q2 FY26', 5176, GREY, STARTS[i] + 0.2), ('Q2 FY27', 4137, RED, at(i, 'fell', -0.2))]):
        if t < tk: continue
        x = 330 + k * 420; q = eo(prog(t, tk, 0.8)); hg = int(v / 5176 * 560 * q)
        d.rounded_rectangle((x - 120, base - hg, x + 120, base), 14, fill=col, outline=INK, width=5)
        place(c, text_img(f'₹{int(v * q):,} CR', 'anton', 58, INK), x, base - hg - 44)
        place(c, text_img(lab, 'osw', 40, GREY), x, base + 44)
    d.line((100, base, 980, base), fill=INK, width=5)
    tb = at(i, 'twenty percent', -0.2)
    if t > tb:
        sc, a = slam(t, tb); place(c, stamp_c('-20.1%', RED, 110, -8, 6), 760, 420, sc, 0, a)
    if t > at(i, 'cigarette taxes', -0.2):
        place_text(c, 'cigarette taxes up from 1 Feb 2026', 'mark', 52, INK, 540, 1380, t, 'tx', at(i, 'cigarette taxes', -0.2), 'slide', rot=-2)
    src(c, t, 'Standalone net profit · INDmoney (3 Nov 2026)', STARTS[i] + 0.5)


def s7(c, t):
    i = 7
    place(c, label('THE FUTURE PLAN', GRN), 540, 230, pp(t, STARTS[i]), -3)
    cards = [('twenty thousand', '₹20,000 CR', 'investment push, 8 new facilities', GRN),
             ('New brands', 'NEW BRANDS', '24 Mantra · Yoga Bar · Prasuma · Mother Sparsh', BLUE),
             ('Century', 'CENTURY PULP & PAPER', 'bought Aug 2026 · ₹3,498 cr', GOLD)]
    for k, (ph, a, b, col) in enumerate(cards):
        tk = at(i, ph, -0.2)
        if t < tk: continue
        p = prog(t, tk, 0.4)
        ta = text_img(a, 'anton', 74, col); tb_ = text_img(b, 'osw5', 34, INK)
        w = max(ta.size[0], tb_.size[0]) + 80; h = ta.size[1] + tb_.size[1] + 50
        card = Image.new('RGBA', (w, h), SOFT + (255,)); dd = ImageDraw.Draw(card)
        dd.rectangle((0, 0, w - 1, h - 1), outline=INK, width=5)
        card.alpha_composite(ta, ((w - ta.size[0]) // 2, 16)); card.alpha_composite(tb_, ((w - tb_.size[0]) // 2, ta.size[1] + 30))
        place(c, cutout(card, border=0, shadow=0.3), 540 + (1 - eo(p)) * (700 if k % 2 else -700), 520 + k * 330, 1, [-2, 2, -1][k])
    if t > at(i, 'Century', 0.6):
        place_text(c, 'eyeing an ₹8 lakh cr FMCG market by 2035', 'mark', 46, INK, 540, 1510, t, 'fm2', at(i, 'Century', 0.6), 'fade', rot=-1)
    src(c, t, 'Angel One (Jul 2026) · StartupTalky (Oct 2026) · INDmoney (Nov 2026)', STARTS[i] + 0.5)


def s8(c, t):
    i = 8
    place(c, label('THE STOCK · NSE: ITC', INK), 540, 230, pp(t, STARTS[i]), -2)
    place_text(c, '₹278.80', 'anton', 190, INK, 540, 520, t, 'px', STARTS[i] + 0.2, 'pop')
    place(c, text_img('close, 9 Nov 2026', 'osw5', 34, GREY), 540, 650)
    d = ImageDraw.Draw(c); x0, x1, y = 140, 940, 900
    lo, hi, px = 252.8, 413.3, 278.8
    p = eo(prog(t, STARTS[i] + 0.4, 1.0))
    d.rounded_rectangle((x0, y - 18, x1, y + 18), 18, fill=(230, 224, 210), outline=INK, width=4)
    xp = x0 + (x1 - x0) * (px - lo) / (hi - lo)
    xm = x1 + (xp - x1) * p
    d.ellipse((xm - 28, y - 28, xm + 28, y + 28), fill=RED, outline=INK, width=5)
    place(c, text_img('52W LOW ₹252.80', 'osw', 32, GREY), x0 + 110, y + 70); place(c, text_img('52W HIGH ₹413.30', 'osw', 32, GREY), x1 - 120, y + 70)
    tb = at(i, 'thirty three', -0.2)
    if t > tb:
        sc, a = slam(t, tb); place(c, stamp_c('-33% FROM HIGH', RED, 90, -6, 7), 540, 1170, sc, 0, a)
    if t > tb + 0.6: place(c, text_img('market cap ₹3.49 lakh crore', 'osw5', 40, INK), 540, 1340)
    src(c, t, 'INDmoney, NSE close 9 Nov 2026 · I may hold some of the stocks named', STARTS[i] + 0.5)


def s9(c, t):
    i = 9
    place_text(c, 'FMCG', 'anton', 140, BLUE, 280, 520, t, 'f', STARTS[i] + 0.1, 'pop')
    place_text(c, 'vs', 'pfi', 90, INK, 540, 530, t, 'v', STARTS[i] + 0.2, 'pop')
    place_text(c, 'CIGARETTES', 'anton', 100, RED, 800, 520, t, 'cg', STARTS[i] + 0.25, 'pop')
    place(c, label('PART 2 SOON', INK), 540, 720, pp(t, STARTS[i] + 0.4), -3)
    tf = at(i, 'Follow', -0.1)
    if t > tf: place(c, follow_btn(), 540, 1000, 0.6 + 0.4 * eback(prog(t, tf, 0.35)), 2)
    place(c, logo_card(150), 540, 1330, pp(t, STARTS[i] + 0.3), 2)


SCENES = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9]


def slam_times():
    return [at(0, 'seventy', -0.2), at(2, 'All ITC', -0.2), at(5, 'seventy', -0.2), at(6, 'twenty percent', -0.2), at(8, 'thirty three', -0.2)]


def header(c, t=0):
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, INK, 1), (52, 64))
    b = text_img('ITC · BUSINESS BREAKDOWN', 'type', 30, BLUE, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
    ImageDraw.Draw(c).line((60, 118, W - 60, 118), fill=INK, width=2)
    ImageDraw.Draw(c).line((60, 118, 60 + (W - 120) * clamp(t / DUR), 118), fill=BLUE, width=8)


def scene_at(t):
    k = 0
    for i, s in enumerate(STARTS):
        if t >= s: k = i
    return k


def _trans(c, t):
    cols = [(BLUE, INK), (YEL, INK), (RED, YEL), (GRN, CREAM), (YEL, RED), (INK, YEL), (RED, YEL), (YEL, INK), (BLUE, CREAM)]
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
    i = scene_at(t)
    c = pbg.copy()
    st = STARTS[i]; en = STARTS[i + 1] if i + 1 < len(STARTS) else DUR
    SCENES[i](c, t)
    place(c, text_img('Not a buy/sell call · Education only · I may hold some of the stocks named', 'type', 22, GREY, 1), 540, 1860)
    z = 1.0 + 0.04 * clamp((t - st) / (en - st)) + (0.06 * math.exp(-(t - st) * 9) if i > 0 else 0)
    sx = sy = 0
    for ts in slam_times():
        if 0 <= t - ts < 0.35:
            k = math.exp(-(t - ts) * 14) * 9
            sx += k * math.sin((t - ts) * 90); sy += k * math.cos((t - ts) * 77)
    cw, ch = W / z, H / z
    cx, cy = W / 2 + sx, H * 0.47 + sy
    c = c.transform((W, H), Image.EXTENT, (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2), Image.BICUBIC)
    header(c, t if not loop else 0); _trans(c, t)
    arr = np.asarray(c.convert('RGB')).astype(np.float32)
    g = grain_frames()[int(t * FPS) % 6]
    return np.clip(arr + g[..., None], 0, 255).astype(np.uint8)
