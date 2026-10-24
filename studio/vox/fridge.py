import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, typed, slam, drop, warn_icon, stamp_c, bgs

FR = ROOT + 'fridge/'
SCRIPT = json.load(open(FR + 'script.json'))
DURS = json.load(open(FR + 'vo/durs.json'))
LEAD, TAIL = 0.25, 0.45
STARTS = []; VO = []
t = 0.0
for i, d in enumerate(DURS):
    STARTS.append(t)
    VO.append(t + (0.15 if i == 0 else LEAD))
    t = VO[-1] + d + TAIL
DUR = t + 1.6  # hold end card
B = STARTS[1:]
SLAMS = []


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def inr(n):
    s = str(int(round(n)))
    if len(s) <= 3: return s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:]); head = head[:-2]
    if head: parts.insert(0, head)
    return ','.join(parts) + ',' + tail


# ---------------- assets ----------------
@functools.lru_cache(None)
def fridge(old=False):
    S = 2; w, h = 330 * S, 600 * S
    body = (60, 76, 72) if old else (196, 226, 216)
    side = (40, 52, 50) if old else (150, 192, 180)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    ow = 10 * S
    bx = (10 * S, 10 * S, 320 * S, 570 * S)
    if old: body, side = (170, 168, 160), (128, 126, 120)
    d.rounded_rectangle(bx, radius=34 * S, fill=body, outline=INK, width=ow)
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle(bx, radius=34 * S, fill=255)
    sh = Image.new('L', (w, h), 0); ImageDraw.Draw(sh).rectangle((250 * S, 0, w, h), fill=255)
    sl = Image.new('RGBA', (w, h), side + (255,)); sl.putalpha(ImageChops.multiply(m, sh)); im.alpha_composite(sl)
    ht = halftone(w, h, tuple(max(0, c - 50) for c in side), spacing=16 * S, maxr=4 * S)
    ht.putalpha(ImageChops.multiply(ht.getchannel('A'), ImageChops.multiply(m, sh))); im.alpha_composite(ht)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(bx, radius=34 * S, outline=INK, width=ow)
    d.line((10 * S, 200 * S, 320 * S, 200 * S), fill=INK, width=8 * S)
    for (y0, y1) in ((70, 160), (240, 400)):
        d.rounded_rectangle((44 * S, y0 * S, 62 * S, y1 * S), radius=9 * S, fill=(235, 235, 230), outline=INK, width=5 * S)
    # feet
    d.rectangle((40 * S, 566 * S, 80 * S, 592 * S), fill=INK); d.rectangle((250 * S, 566 * S, 290 * S, 592 * S), fill=INK)
    if not old:
        # magnet note + gloss
        d.rectangle((150 * S, 260 * S, 228 * S, 340 * S), fill=YEL, outline=INK, width=4 * S)
        for k in range(3): d.line((162 * S, (282 + k * 16) * S, 216 * S, (282 + k * 16) * S), fill=INK, width=3 * S)
        d.ellipse((182 * S, 250 * S, 198 * S, 266 * S), fill=RED, outline=INK, width=3 * S)
        d.line((90 * S, 40 * S, 90 * S, 150 * S), fill=(240, 250, 246), width=8 * S)
        d.line((90 * S, 230 * S, 90 * S, 520 * S), fill=(240, 250, 246), width=8 * S)
    im = im.resize((w // S, h // S), Image.LANCZOS)
    return cutout(im, border=14)


@functools.lru_cache(None)
def price_tag():
    t = text_img('₹35,000', 'anton', 92, INK)
    w, h = t.size[0] + 70, t.size[1] + 20
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(0, h / 2), (36, 0), (w, 0), (w, h), (36, h)], fill=YEL, outline=INK)
    d.line([(0, h / 2), (36, 0), (w - 1, 0), (w - 1, h - 1), (36, h - 1), (0, h / 2)], fill=INK, width=6)
    d.ellipse((22, h / 2 - 9, 40, h / 2 + 9), fill=PAPER, outline=INK, width=4)
    im.alpha_composite(t, (58, 10))
    return cutout(im, border=10)


@functools.lru_cache(16)
def notebook(n_lines, hp):
    w, h = 880, 640
    im = Image.new('RGBA', (w, h), (251, 249, 240, 255)); d = ImageDraw.Draw(im)
    for y in range(110, h, 64): d.line((0, y, w, y), fill=(168, 196, 222), width=2)
    d.line((96, 0, 96, h), fill=(232, 120, 110), width=3)
    for y in (90, 320, 550): d.ellipse((30, y, 58, y + 28), fill=PAPER)
    rows = [('Fridge', '₹35,000', INK), ('+ 20% tax', '₹7,000', INK), ('Target', '₹42,000', RED)]
    ys = [150, 278, 470]
    for k in range(min(n_lines, 3)):
        lab, amt, col = rows[k]; y = ys[k]
        if k == 2:
            d.line((130, 395, 820, 395), fill=INK, width=5)
            if hp > 0: highlight(im, 120, y - 46, 840, y + 50, hp, seed=41)
        li = text_img(lab, 'mark', 64, col); im.alpha_composite(li, (130, y - li.size[1] // 2))
        ai = text_img(amt, 'mark', 70, col); im.alpha_composite(ai, (820 - ai.size[0], y - ai.size[1] // 2))
    return cutout(im, border=0, shadow=0.34, blur=10)


@functools.lru_cache(64)
def clipping(hp):
    w, h = 840, 360
    im = torn_rect(w, h, (234, 228, 212), seed=8, jag=12)
    d = ImageDraw.Draw(im)
    mt = text_img('THE MARKET PAGE', 'pf', 30, INK, 3); im.alpha_composite(mt, (w // 2 - mt.size[0] // 2, 14))
    d.line((40, 66, w - 40, 66), fill=INK, width=3); d.line((40, 72, w - 40, 72), fill=INK, width=1)
    st = text_img('MID-CAP  ·  MY PICK', 'type', 22, (90, 85, 80), 2); im.alpha_composite(st, (w // 2 - st.size[0] // 2, 78))
    hl = text_img('CUPID LTD', 'pf', 124, INK)
    hx, hy = w // 2 - hl.size[0] // 2, 104
    if hp > 0: highlight(im, hx + 18, hy + 54, hx + hl.size[0] - 18, hy + 146, hp, seed=12, alpha=225)
    im.alpha_composite(hl, (hx, hy))
    r = random.Random(9)
    for col in range(3):
        x0 = 44 + col * 258
        for k in range(4):
            y = 272 + k * 18; ln = r.uniform(170, 232) if k < 3 else r.uniform(80, 150)
            d.line((x0, y, x0 + ln, y), fill=(160, 152, 140), width=7)
    return cutout(im, border=0, shadow=0.36, blur=10)


@functools.lru_cache(None)
def buy_card():
    w, h = 680, 180
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=22, fill=(24, 24, 24))
    d.line((w // 2, 30, w // 2, h - 30), fill=(90, 90, 90), width=3)
    for cx, lab, val, col in ((w // 4, 'AVG BUY', '₹224.61', CREAM), (3 * w // 4, 'SHARES', '367', YEL)):
        li = text_img(lab, 'type', 26, (180, 175, 165), 2); im.alpha_composite(li, (cx - li.size[0] // 2, 18))
        vi = text_img(val, 'anton', 84, col); im.alpha_composite(vi, (cx - vi.size[0] // 2, 52))
    return cutout(im, border=12)


# real weekly closes, Cupid Ltd (INDmoney), 1 Jun -> 12 Oct 2026
WEEKS = [137.1, 159.97, 176.92, 182.61, 198.84, 212.24, 214.78, 213.43, 230.62, 262.13, 293.88, 284.58,
         282.33, 283.15, 280.0, 265.0, 270.0, 312.5, 366.1, 353.7]
MLAB = [(0, 'JUN'), (5, 'JUL'), (9, 'AUG'), (13, 'SEP'), (17, 'OCT')]
SW_, SH_ = 960, 760
PX0, PX1, PY0, PY1 = 120, 900, 680, 70
LO, HI = 100, 400


def py(p): return PY0 + (p - LO) / (HI - LO) * (PY1 - PY0)
def px(f): return PX0 + (PX1 - PX0) * f


@functools.lru_cache(None)
def series():
    P = WEEKS; n = len(P) - 1; out = []
    for i in range(n):
        p0 = P[max(0, i - 1)]; p1 = P[i]; p2 = P[i + 1]; p3 = P[min(n, i + 2)]
        for k in range(10):
            s = k / 10
            v = 0.5 * ((2 * p1) + (-p0 + p2) * s + (2 * p0 - 5 * p1 + 4 * p2 - p3) * s * s + (-p0 + 3 * p1 - 3 * p2 + p3) * s ** 3)
            out.append(((i + s) / n, v))
    out.append((1.0, P[-1]))
    return out


def price_at(f):
    s = series(); idx = f * (len(s) - 1); i = int(idx); fr = idx - i
    if i >= len(s) - 1: return s[-1][1]
    return s[i][1] * (1 - fr) + s[i + 1][1] * fr


@functools.lru_cache(None)
def sheet():
    im = Image.new('RGBA', (SW_, SH_), (252, 250, 244, 255)); d = ImageDraw.Draw(im)
    for x in range(0, SW_, 30): d.line((x, 0, x, SH_), fill=(205, 218, 228), width=1)
    for y in range(0, SH_, 30): d.line((0, y, SW_, y), fill=(205, 218, 228), width=1)
    for v in (100, 150, 200, 250, 300, 350, 400):
        li = text_img(f'₹{v}', 'type', 24, (120, 115, 108)); im.alpha_composite(li, (20, int(py(v)) - li.size[1] // 2))
    n = len(WEEKS) - 1
    for i, m in MLAB:
        li = text_img(m, 'type', 26, (90, 85, 80), 1); im.alpha_composite(li, (int(px(i / n)) - li.size[0] // 2, PY0 + 18))
    d.line((PX0, PY0, PX1 + 20, PY0), fill=INK, width=4)
    yb = py(224.61)
    for x in range(PX0, PX1, 26): d.line((x, yb, x + 13, yb), fill=RED, width=3)
    bl = text_img('MY AVG ₹224.61', 'type', 24, RED, 1); im.alpha_composite(bl, (PX0 + 14, int(yb) - bl.size[1] - 2))
    return cutout(im, border=0, shadow=0.3)


@functools.lru_cache(None)
def receipt():
    w, h = 840, 860
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pts = [(0, 0), (w, 0), (w, h - 24)]
    n = 28
    for i in range(n, -1, -1): pts.append((w * i / n, h - (24 if i % 2 == 0 else 0)))
    pts += [(0, h - 24)]
    d.polygon(pts, fill=(254, 253, 249))
    return cutout(im, border=0, shadow=0.34, blur=12, off=(6, 14))


@functools.lru_cache(None)
def follow_btn():
    t = text_img('FOLLOW @moneyincloud', 'anton', 66, INK)
    w, h = t.size[0] + 80, t.size[1] + 30
    im = Image.new('RGBA', (w + 14, h + 14), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((14, 14, w + 13, h + 13), radius=34, fill=INK)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=34, fill=YEL, outline=INK, width=7)
    im.alpha_composite(t, (40, 15))
    return im


def check(c, x, y, p, col=GRN, s=1.0):
    marker_line(c, [(x - 30 * s, y), (x - 8 * s, y + 26 * s), (x + 38 * s, y - 30 * s)], p, col, 10)


# ---------------- scenes ----------------
def s1(c, t):
    i = 0
    # frame 0 already moving: big fridge rising + swinging price tag (Virality checklist 1-3)
    rise = eo(prog(t, 0.0, 0.7))
    jx, jy, jr = jit('fn1', t, 2, 0.6)
    fy = 1080 + (1 - rise) * 260
    place(c, fridge(False), 450 + jx, fy + jy, 1.38, 2 + jr - (1 - rise) * 6)
    sw = math.sin(t * 4.2) * 9 * math.exp(-t * 0.35)
    stroke(c, [(600, fy - 230), (700, fy - 190)], 5, INK)
    place(c, price_tag(), 845, fy - 150, 1.0, -14 + sw)
    # claim word by word, synced to voice, lands ~0.2-1.4s
    words_line(c, t, [("A", INK, at(i, 'A stock')), ("STOCK", INK, at(i, 'stock')), ("PAID", RED, at(i, 'paid'))], 'anton', 160, 290, key='h1')
    words_line(c, t, [("FOR", INK, at(i, 'for')), ("MY", INK, at(i, 'my new')), ("FRIDGE", INK, at(i, 'fridge'))], 'anton', 160, 455, key='h2')
    # the extraordinary event: PAID slams across the fridge
    ts = at(i, 'fridge', 0.25)
    sc, a = slam(t, ts)
    if a > 0:
        place(c, stamp_c('PAID', RED, 160, 14, 31), 470, 1110, sc, 0, a)
    tz = at(i, 'and zero')
    if t > tz:
        place_text(c, '₹0 from savings', 'mark', 72, RED, 540, 1540, t, 'sav', tz, 'slide', rot=-3)
        marker_ellipse(c, 300, 1542, 95, 62, prog(t, tz + 0.5, 0.5), RED, 8, seed=5)


def s2(c, t):
    i = 1
    words_line(c, t, [("MY", INK, at(i, 'My')), ("RULE", RED, at(i, 'rule'))], 'anton', 140, 300, key='f2')
    n = 0; hp = 0
    for k, ph in enumerate(('Write', 'add twenty', 'and let')):
        if t > at(i, ph): n = k + 1
    if n >= 3: hp = round(prog(t, at(i, 'and let', 0.3), 0.45) * 20) / 20
    p = prog(t, STARTS[1] + 0.1, 0.45)
    jx, jy, jr = jit('nb', t, 1.5, 0.3)
    place(c, notebook(n, hp), 540 + jx, 820 + jy + (1 - eo(p)) * 900, 1.0, -1.5 + jr, clamp(p * 3))
    if t > at(i, 'and let', 0.5):
        tt = at(i, 'let a stock')
        place_text(c, 'let a stock earn it', 'pfi', 84, INK, 540, 1290, t, 'earn', tt, 'slide')
        marker_line(c, [(250, 1350), (540, 1344), (830, 1336)], prog(t, tt + 0.4, 0.45), RED, 8)


def s3(c, t):
    i = 2
    words_line(c, t, [("THE", INK, at(i, 'The')), ("PICK", RED, at(i, 'stock'))], 'anton', 140, 300, key='f3')
    tc = at(i, 'Cupid', -0.25)
    if t > tc:
        dy, a = drop(t, tc, 300)
        hp = round(prog(t, tc + 0.6, 0.5) * 20) / 20
        jx, jy, jr = jit('clip', t, 2, 0.5)
        place(c, clipping(hp), 540 + jx, 680 + dy + jy, 1.0, -3 + jr + (1 - a) * 8, a)
    tb = at(i, 'Three')
    if t > tb:
        p = prog(t, tb, 0.4)
        jx, jy, jr = jit('buy', t, 1.5, 0.3)
        place(c, buy_card(), 540 + jx, 1030 + (1 - eo(p)) * 160 + jy, 1.0, 1.5 + jr, clamp(p * 3))
    ti = at(i, 'at an')
    if t > ti:
        place_text(c, '= ₹82,433 invested', 'mark', 60, RED, 540, 1240, t, 'inv', ti, 'slide', rot=-2)


def s4(c, t):
    i = 3
    t0, t1 = at(i, 'Today', -0.2), at(i, 'one lakh', 0.4)
    if t > STARTS[3] + 0.15:
        place_text(c, 'MY ₹82,433 IS NOW', 'type', 42, INK, 540, 300, t, 'yn', STARTS[3] + 0.15, 'fade', track=2)
    f = eio(prog(t, t0, t1 - t0))
    val = 82433 + (129808 - 82433) * f
    jx, jy, jr = jit('cnt', t, 1.2, 0.3)
    place(c, text_img('₹' + inr(val), 'anton', 190, GRN), 540 + jx, 455 + jy, 1.0, jr)
    p = prog(t, STARTS[3] + 0.05, 0.45)
    sjx, sjy, _ = jit('sheet', t, 1.3, 0)
    ox, oy = 540 - SW_ // 2 + sjx, 640 + sjy + (1 - eo(p)) * 600
    place(c, sheet(), ox + SW_ / 2, oy + SH_ / 2, 1.0, 0, clamp(p * 3))
    if f > 0:
        s = series()
        pr = price_at(f)
        pts = [(ox + px(fr), oy + py(v)) for fr, v in s if fr <= f] + [(ox + px(f), oy + py(pr))]
        if len(pts) > 1:
            poly_fill(c, pts + [(pts[-1][0], oy + PY0), (pts[0][0], oy + PY0)], YEL, 150)
            stroke(c, pts, 9, INK)
        tx, ty = pts[-1]
        ImageDraw.Draw(c).ellipse((tx - 13, ty - 13, tx + 13, ty + 13), fill=RED, outline=INK, width=4)
        tg = text_img(f'₹{pr:.2f}', 'anton', 44, CREAM)
        bx, by = min(tx - tg.size[0] / 2, ox + SW_ - tg.size[0] - 20), ty - 70
        ImageDraw.Draw(c).rounded_rectangle((bx - 6, by - 4, bx + tg.size[0] + 6, by + tg.size[1] - 6), radius=10, fill=INK)
        c.alpha_composite(tg, (int(bx), int(by - 4)))
    ts = t1 + 0.1
    sc, a = slam(t, ts)
    if a > 0:
        if ts not in SLAMS: SLAMS.append(ts)
        place(c, stamp_c('+57%', GRN, 100, 10, 17), ox + 290, oy + 170, sc, 0, a)


def s5(c, t):
    i = 4
    words_line(c, t, [("THE", INK, STARTS[4] + 0.1), ("MATH", RED, STARTS[4] + 0.3)], 'anton', 124, 300, key='f5')
    p = prog(t, STARTS[4] + 0.1, 0.45)
    jx, jy, jr = jit('rc', t, 1.0, 0)
    rx0, ry0 = 540 - 420 + jx, 420 + jy + (1 - eo(p)) * 800
    place(c, receipt(), rx0 + 420, ry0 + 430, 1.0, 0, clamp(p * 3))
    if p <= 0: return

    def row(t0, y, lab, sub, amt, col, hl=None, big=False):
        q = prog(t, t0, 0.3)
        if q <= 0: return
        dx = (1 - eo(q)) * 40; a = clamp(q * 3)
        if hl is not None:
            highlight(c, rx0 + 40, ry0 + y - 48, rx0 + 800, ry0 + y + 48, prog(t, hl, 0.45), seed=51)
        li = text_img(lab, 'osw5', 48, INK); place(c, li, rx0 + 54 + li.size[0] / 2 + dx, ry0 + y - 14, 1, 0, a)
        if sub:
            si = text_img(sub, 'type', 25, (120, 112, 104), 1); place(c, si, rx0 + 57 + si.size[0] / 2 + dx, ry0 + y + 32, 1, 0, a)
        ai = text_img(amt, 'anton', 86 if big else 74, col); place(c, ai, rx0 + 800 - ai.size[0] / 2 - dx, ry0 + y - 2, 1, 0, a)
    row(at(i, "That's"), 100, 'Profit', '367 × (₹353.70 − ₹224.61)', '₹47,375', GRN)
    row(at(i, 'more than'), 235, 'Target', 'fridge + 20% tax', '₹42,000', INK)
    check(c, rx0 + 420, ry0 + 225, prog(t, at(i, 'target'), 0.35))
    row(at(i, 'Selling'), 385, 'Sell ~107 shares', '107 × ₹353.70', '₹37,846', INK)
    row(at(i, 'covers'), 520, 'Tax (20% on gain)', 'gain ₹13,813', '−₹2,763', RED)
    q = prog(t, at(i, 'even', -0.2), 0.3)
    if q > 0:
        d = ImageDraw.Draw(c)
        for x in range(int(rx0 + 50), int(rx0 + 50 + 740 * eo(q)), 22):
            d.line((x, ry0 + 610, x + 11, ry0 + 610), fill=INK, width=4)
    row(at(i, 'even'), 705, 'In hand', '', '₹35,083', INK, hl=at(i, 'after'), big=True)
    if t > at(i, 'after', 0.4):
        place_text(c, '= FRIDGE PAID', 'mark', 58, GRN, 540, ry0 + 920, t, 'fp', at(i, 'after', 0.4), 'pop', rot=-3)
    if t > STARTS[4] + 0.8:
        place_text(c, 'Approx. · before brokerage · price 16 Oct ₹353.70', 'type', 24, (120, 112, 104), 540, 1440, t, None, STARTS[4] + 0.8, 'fade')


def s6(c, t):
    i = 5
    words_line(c, t, [("THE", INK, at(i, 'So')), ("STOCK", INK, at(i, 'stock'))], 'anton', 140, 300, key='f6a')
    words_line(c, t, [("BOUGHT", INK, at(i, 'bought')), ("OUR", INK, at(i, 'our'))], 'anton', 140, 455, key='f6b')
    fw = text_w('FRIDGE', 'anton', 140)
    highlight(c, 540 - fw / 2 - 18, 545, 540 + fw / 2 + 18, 680, prog(t, at(i, 'fridge', 0.15), 0.4), seed=61)
    words_line(c, t, [("FRIDGE", RED, at(i, 'fridge'))], 'anton', 140, 610, key='f6c')
    dy, a = drop(t, STARTS[5] + 0.2, 380)
    if a > 0:
        jx, jy, jr = jit('f6', t, 2.5, 0.8)
        place(c, fridge(False), 400 + jx, 1010 + dy + jy, 0.72, 4 + jr, a)
    ts = at(i, 'fridge', 0.3)
    sc, a = slam(t, ts)
    if a > 0:
        if ts not in SLAMS: SLAMS.append(ts)
        place(c, stamp_c('PAID', GRN, 110, 14, 23), 740, 1030, sc, 0, a)
    tt = at(i, 'And')
    if t > tt:
        place_text(c, '260 shares still working', 'pfi', 72, INK, 540, 1330, t, 'work', tt, 'slide')
        marker_line(c, [(200, 1392), (540, 1386), (880, 1376)], prog(t, tt + 0.5, 0.45), GRN, 9)
        place_text(c, '~₹91,962 still invested', 'type', 32, (90, 85, 80), 540, 1450, t, None, tt + 0.7, 'fade', track=1)


def s7(c, t):
    i = 6
    t0 = STARTS[6] + 0.2
    if t > t0:
        p = prog(t, t0, 0.3)
        lw = text_w('REALITY CHECK', 'osw', 54, 2); x0 = 540 - (lw + 70) / 2
        place(c, warn_icon(RED), x0 + 28, 302, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
        place(c, text_img('REALITY CHECK', 'osw', 54, RED, 2), x0 + 70 + lw / 2, 300, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
    words_line(c, t, [("PROFIT", CREAM, at(i, 'Profit')), ("ON", CREAM, at(i, 'on screen')), ("SCREEN", CREAM, at(i, 'screen'))], 'anton', 132, 470, key='f7a')
    words_line(c, t, [("IS", RED, at(i, 'is not')), ("NOT", RED, at(i, 'not money'))], 'anton', 132, 615, key='f7b')
    words_line(c, t, [("MONEY", CREAM, at(i, 'money')), ("IN", CREAM, at(i, 'in hand')), ("HAND", CREAM, at(i, 'hand'))], 'anton', 132, 760, key='f7c')
    marker_line(c, [(400, 692), (540, 686), (680, 680)], prog(t, at(i, 'money', -0.1), 0.35), RED, 10)
    tf = at(i, 'Small')
    if t > tf:
        place_text(c, 'small caps can fall just as fast', 'mark', 52, RED, 500, 930, t, 'fall', tf, 'slide', rot=-3)
        marker_line(c, [(960, 885), (968, 935), (962, 985)], prog(t, tf + 0.4, 0.35), RED, 9, head=True, head_size=24)
    typed(c, 'Not investment advice. DYOR.', 'type', 32, (200, 194, 182), 1060, t, tf + 0.9, tf + 2.0)
    tfo = at(i, 'Follow', -0.1)
    if t > tfo:
        p = prog(t, tfo, 0.35)
        pul = 1 + 0.035 * math.sin((t - tfo - 0.4) * 6) if t > tfo + 0.4 else 1
        place(c, follow_btn(), 540, 1230, (0.5 + 0.5 * eback(p)) * pul, 0, clamp(p * 3))
    if t > tfo + 0.6:
        place_text(c, 'Comment "FRIDGE" if you\'d do this', 'osw5', 40, CREAM, 540, 1360, t, None, tfo + 0.6, 'slide')


SCENES = [s1, s2, s3, s4, s5, s6, s7]


def header(c, dark):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('REAL P&L · EP 3', 'type', 30, RED, 1)
    c.alpha_composite(b, (W - 52 - b.size[0], 64))
    ImageDraw.Draw(c).line((60, 118, W - 60, 118), fill=col, width=2)
    ImageDraw.Draw(c).line((60, 118, 300, 118), fill=col, width=6)


def transition(c, t):
    cols = [(YEL, INK), (RED, INK), (INK, YEL), (YEL, RED), (RED, YEL), (INK, RED)]
    for bi, b in enumerate(B):
        d = 0.62
        if abs(t - b) > d / 2 + 0.12: continue
        for layer, delay in ((0, -0.07), (1, 0.0)):
            p = (t - (b - d / 2) - delay) / d
            if p <= 0 or p >= 1: continue
            p = eio(p)
            SWd, skew = 2050, 320
            xl = (W + 60) + p * (-(SWd + skew) - (W + 60) - 40)
            r = random.Random(bi * 10 + layer + 100)
            left = [(xl + r.uniform(-14, 14) - skew * (y / H), y) for y in range(0, H + 1, 40)]
            right = [(xl + SWd + r.uniform(-14, 14) - skew * (y / H), y) for y in range(H, -1, -40)]
            if layer == 0:
                left = [(x - 70, y) for x, y in left]; right = [(x + 70, y) for x, y in right]
            poly_fill(c, left + right, cols[bi % 6][layer], 255, S=1)


def scene_at(t):
    k = 0
    for i, s in enumerate(STARTS):
        if t >= s: k = i
    return k


ALL_SLAMS = None
def slam_times():
    # computed statically so every worker shakes identically
    return [at(0, 'fridge', 0.25), at(3, 'one lakh', 0.5), at(5, 'fridge', 0.3), STARTS[5] + 0.45, at(2, 'Cupid', 0.05)]


def render(t):
    pbg, dbg = bgs()
    i = scene_at(t); dark = (i == 6)
    c = (dbg if dark else pbg).copy()
    st = STARTS[i]; en = STARTS[i + 1] if i + 1 < len(STARTS) else DUR
    SCENES[i](c, t)
    z = 1.0 + 0.045 * clamp((t - st) / (en - st))
    sx = sy = 0
    for ts in slam_times():
        if 0 <= t - ts < 0.35:
            k = math.exp(-(t - ts) * 14) * 9
            sx += k * math.sin((t - ts) * 90); sy += k * math.cos((t - ts) * 77)
    cw, ch = W / z, H / z
    cx, cy = W / 2 + sx, H * 0.47 + sy
    c = c.transform((W, H), Image.EXTENT, (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2), Image.BICUBIC)
    header(c, dark); transition(c, t)
    arr = np.asarray(c.convert('RGB')).astype(np.float32)
    g = grain_frames()[int(t * FPS) % 6]
    fl = 1 + 0.012 * math.sin(t * 37) * math.sin(t * 13)
    return np.clip(arr * fl + g[..., None], 0, 255).astype(np.uint8)
