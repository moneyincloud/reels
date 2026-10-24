import math, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from lib import *

B = [6.5, 15.8, 24.6, 32.9, 41.0, 45.6]
DUR = 56.4
SLAMS = [(0.42, 10), (10.2, 9), (10.6, 7), (20.75, 8), (31.3, 9), (42.45, 6), (42.8, 10)]

# ---------------- assets ----------------
@functools.lru_cache(None)
def backpack():
    S = 2; w, h = 360 * S, 430 * S
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    ow = 11 * S
    # handle
    d.rounded_rectangle((120 * S, 10 * S, 240 * S, 110 * S), radius=50 * S, outline=INK, width=22 * S)
    d.rounded_rectangle((120 * S, 10 * S, 240 * S, 110 * S), radius=50 * S, outline=(40, 40, 40), width=12 * S)
    # body
    body = (30 * S, 70 * S, 330 * S, 420 * S)
    d.rounded_rectangle(body, radius=70 * S, fill=(214, 64, 46), outline=INK, width=ow)
    # side shading
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle(body, radius=70 * S, fill=255)
    sh = Image.new('L', (w, h), 0); ImageDraw.Draw(sh).rectangle((250 * S, 0, w, h), fill=255)
    shade = Image.new('RGBA', (w, h), (160, 38, 28, 255)); shade.putalpha(ImageChops.multiply(m, sh))
    im.alpha_composite(shade)
    ht = halftone(w, h, (120, 25, 20), spacing=16 * S, maxr=4.5 * S)
    ht.putalpha(ImageChops.multiply(ht.getchannel('A'), ImageChops.multiply(m, sh)))
    im.alpha_composite(ht)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(body, radius=70 * S, outline=INK, width=ow)
    # gloss
    d.ellipse((62 * S, 112 * S, 102 * S, 152 * S), fill=(255, 245, 235), outline=INK, width=5 * S)
    # pocket
    d.rounded_rectangle((70 * S, 220 * S, 290 * S, 380 * S), radius=30 * S, fill=YEL, outline=INK, width=ow)
    d.line((70 * S, 270 * S, 290 * S, 270 * S), fill=INK, width=7 * S)
    d.rounded_rectangle((155 * S, 250 * S, 205 * S, 295 * S), radius=8 * S, fill=CREAM, outline=INK, width=6 * S)
    im = im.resize((w // S, h // S), Image.LANCZOS)
    return cutout(im, border=14)


@functools.lru_cache(None)
def ticket(label, amount, month, alert=False):
    w, h = 860, 200
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=18, fill=(253, 251, 246),
                        outline=RED if alert else INK, width=7 if alert else 5)
    for y in range(18, h - 18, 22): d.line((630, y, 630, y + 11), fill=(150, 140, 130), width=3)
    d.ellipse((612, -18, 648, 18), fill=PAPER); d.ellipse((612, h - 18, 648, h + 18), fill=PAPER)
    im.alpha_composite(text_img(label, 'type', 30, (110, 100, 92), 2), (40, 18))
    im.alpha_composite(text_img(amount, 'anton', 96, INK), (34, 52))
    mi = text_img(month, 'osw', 46, RED if alert else INK)
    im.alpha_composite(mi, (745 - mi.size[0] // 2, h // 2 - mi.size[1] // 2))
    return cutout(im, border=0, shadow=0.32, blur=9, off=(6, 12))


@functools.lru_cache(None)
def stamp_c(text, color, size, rot, seed):
    return stamp(text, color, size, rot, seed)


@functools.lru_cache(64)
def clipping(hp):
    w, h = 840, 360
    im = torn_rect(w, h, (234, 228, 212), seed=5, jag=12)
    d = ImageDraw.Draw(im)
    mt = text_img('THE MARKET PAGE', 'pf', 30, INK, 3)
    im.alpha_composite(mt, (w // 2 - mt.size[0] // 2, 14))
    d.line((40, 66, w - 40, 66), fill=INK, width=3); d.line((40, 72, w - 40, 72), fill=INK, width=1)
    st = text_img('SMALL-CAP  ·  1 APRIL', 'type', 22, (90, 85, 80), 2)
    im.alpha_composite(st, (w // 2 - st.size[0] // 2, 78))
    hl = text_img('PC JEWELLER', 'pf', 118, INK)
    hx, hy = w // 2 - hl.size[0] // 2, 108
    if hp > 0:
        highlight(im, hx + 18, hy + 52, hx + hl.size[0] - 18, hy + 140, hp, seed=11, alpha=225)
    im.alpha_composite(hl, (hx, hy))
    r = random.Random(4)
    for col in range(3):
        x0 = 44 + col * 258
        for k in range(4):
            y = 272 + k * 18; ln = r.uniform(170, 232) if k < 3 else r.uniform(80, 150)
            d.line((x0, y, x0 + ln, y), fill=(160, 152, 140), width=7)
    return cutout(im, border=0, shadow=0.36, blur=10, off=(8, 14))


@functools.lru_cache(None)
def buy_card():
    w, h = 660, 180
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=22, fill=(24, 24, 24))
    d.line((w // 2, 30, w // 2, h - 30), fill=(90, 90, 90), width=3)
    for cx, lab, val, col in ((w // 4, 'BUY · 1 APR', '₹8.25', CREAM), (3 * w // 4, 'SHARES', '3,393', YEL)):
        li = text_img(lab, 'type', 26, (180, 175, 165), 2); im.alpha_composite(li, (cx - li.size[0] // 2, 18))
        vi = text_img(val, 'anton', 84, col); im.alpha_composite(vi, (cx - vi.size[0] // 2, 52))
    return cutout(im, border=12)


# chart geometry (sheet coords)
SW_, SH_ = 960, 760
PX0, PX1, PY0, PY1 = 120, 900, 680, 70  # y for price 6 -> PY0, 18 -> PY1
MONTHS = ['APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT']
PRICES = [8.25, 9.45, 8.76, 9.7, 11.6, 13.5, 16.28]


def py(p): return PY0 + (p - 6) / 12 * (PY1 - PY0)


def px(i): return PX0 + (PX1 - PX0) * i / 6


@functools.lru_cache(None)
def series():
    P = PRICES; out = []
    N = 40
    for i in range(6):
        p0 = P[max(0, i - 1)]; p1 = P[i]; p2 = P[i + 1]; p3 = P[min(6, i + 2)]
        for k in range(N):
            s = k / N
            v = 0.5 * ((2 * p1) + (-p0 + p2) * s + (2 * p0 - 5 * p1 + 4 * p2 - p3) * s * s + (-p0 + 3 * p1 - 3 * p2 + p3) * s ** 3)
            # small wiggle like real price action
            v += 0.12 * math.sin(i * 7 + k * 1.3) * math.sin(k / N * math.pi)
            out.append(((i + s) / 6, v))
    out.append((1.0, P[6]))
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
    for v in (6, 8, 10, 12, 14, 16, 18):
        li = text_img(f'₹{v}', 'type', 24, (120, 115, 108)); im.alpha_composite(li, (30, int(py(v)) - li.size[1] // 2))
    for i, m in enumerate(MONTHS):
        li = text_img(m, 'type', 26, (90, 85, 80), 1); im.alpha_composite(li, (int(px(i)) - li.size[0] // 2, PY0 + 18))
    d.line((PX0, PY0, PX1 + 20, PY0), fill=INK, width=4)
    yb = py(8.25)
    for x in range(PX0, PX1, 26): d.line((x, yb, x + 13, yb), fill=RED, width=3)
    bl = text_img('BUY ₹8.25', 'type', 24, RED, 1); im.alpha_composite(bl, (PX1 - bl.size[0] + 10, int(yb) + 4))
    return im


@functools.lru_cache(None)
def receipt():
    w, h = 820, 720
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pts = [(0, 0), (w, 0), (w, h - 24)]
    n = 26
    for i in range(n, -1, -1):
        pts.append((w * i / n, h - (24 if i % 2 == 0 else 0)))
    pts += [(0, h - 24)]
    d.polygon(pts, fill=(254, 253, 249))
    return cutout(im, border=0, shadow=0.34, blur=12, off=(6, 14))


@functools.lru_cache(None)
def tag_green():
    t = text_img('+12.7% IN ONE DAY', 'anton', 72, CREAM)
    w, h = t.size[0] + 60, t.size[1] + 16
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), radius=20, fill=GRN)
    im.alpha_composite(t, (30, 8))
    return cutout(im, border=10, shadow=0.5)


@functools.lru_cache(None)
def follow_btn():
    t = text_img('FOLLOW @moneyincloud', 'anton', 66, INK)
    w, h = t.size[0] + 80, t.size[1] + 30
    im = Image.new('RGBA', (w + 14, h + 14), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((14, 14, w + 13, h + 13), radius=34, fill=INK)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=34, fill=YEL, outline=INK, width=7)
    im.alpha_composite(t, (40, 15))
    return im


@functools.lru_cache(None)
def warn_icon(col):
    S = 3; s = 56
    im = Image.new('RGBA', (s * S, s * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(s * S / 2, 2 * S), (s * S - 2 * S, s * S - 4 * S), (2 * S, s * S - 4 * S)], fill=col)
    d.rectangle((s * S / 2 - 3 * S, 18 * S, s * S / 2 + 3 * S, 36 * S), fill=DARK)
    d.ellipse((s * S / 2 - 3.5 * S, 40 * S, s * S / 2 + 3.5 * S, 47 * S), fill=DARK)
    return im.resize((s, s), Image.LANCZOS)


PAPER_BG = None; DARK_BG = None
def bgs():
    global PAPER_BG, DARK_BG
    if PAPER_BG is None:
        PAPER_BG = make_paper(PAPER, 1); DARK_BG = make_paper(DARK, 2, dark=True)
    return PAPER_BG, DARK_BG


# ---------------- helpers ----------------
def words_line(c, t, words, fn, size, cy, gap=None, key='w', amp=1.2):
    """words: list of (text, color, t0). centred line, each word pops in"""
    gap = size * 0.22 if gap is None else gap
    ws = [text_w(w, fn, size) for w, _, _ in words]
    tot = sum(ws) + gap * (len(ws) - 1)
    x = W / 2 - tot / 2; boxes = []
    for (w, col, t0), ww in zip(words, ws):
        place_text(c, w, fn, size, col, x + ww / 2, cy, t, (key, w), t0, 'pop', amp=amp)
        boxes.append((x, ww)); x += ww + gap
    return boxes


def typed(c, s, fn, size, col, cy, t, t0, t1, cursor=True, track=2):
    p = prog(t, t0, t1 - t0)
    if p <= 0: return
    n = int(round(len(s) * p))
    full = text_w(s, fn, size, track); x0 = W / 2 - full / 2
    pad = int(size * 0.12)
    if n > 0:
        im = text_img(s[:n], fn, size, col, track)
        c.alpha_composite(im, (int(x0 - pad), int(cy - im.size[1] / 2)))
    if cursor and (p < 1 or int(t * 2.5) % 2 == 0):
        cw = text_w(s[:n], fn, size, track) if n else 0
        ImageDraw.Draw(c).rectangle((x0 + cw + 6, cy - size * 0.38, x0 + cw + 6 + size * 0.45, cy + size * 0.3), fill=col)


def slam(t, t0, d=0.2):
    p = prog(t, t0, d)
    if t < t0: return 0, 0
    return 1 + 1.3 * (1 - eo(p)), clamp(p * 4)


def drop(t, t0, dist=420):
    p = prog(t, t0, 0.5)
    return -(1 - eback(p, 1.4)) * dist, clamp(p * 4)


# ---------------- scenes ----------------
def s1(c, t):
    bp = backpack()
    dy, a = drop(t, 0.15)
    if a > 0:
        jx, jy, jr = jit('bp', t, 2.5, 0.8)
        place(c, bp, 540 + jx, 560 + dy + jy, 1.0, -4 + jr + (1 - a) * 12, a)
    words_line(c, t, [("MY", INK, 0.45), ("SON'S", INK, 0.62)], 'anton', 150, 900, key='s1a')
    words_line(c, t, [("SCHOOL", INK, 0.95), ("FEE", RED, 1.45)], 'anton', 150, 1065, key='s1b')
    if t >= 2.0:
        v = int(64000 * eo(prog(t, 2.0, 1.25)))
        s = f'₹{v:,}'
        fw = text_w('₹64,000', 'anton', 220)
        highlight(c, 540 - fw / 2 - 20, 1230, 540 + fw / 2 + 20, 1365, prog(t, 3.3, 0.45), seed=2)
        jx, jy, jr = jit('num', t, 1.2, 0.3)
        sc = 1 + 0.08 * math.exp(-max(0, t - 3.25) * 9) if t > 3.25 else 1
        place(c, text_img(s, 'anton', 220, INK), 540 + jx, 1290 + jy, sc, jr)
    if t >= 3.95:
        place_text(c, 'only ₹36,000 from savings', 'mark', 56, RED, 540, 1450, t, 'sav', 3.95, 'slide', rot=-3, amp=1.5)
        marker_line(c, [(250, 1505), (540, 1497), (830, 1488)], prog(t, 4.5, 0.5), RED, 8)


def s2(c, t):
    boxes = words_line(c, t, [("THE", INK, 6.75), ("SCHOOL", INK, 6.9), ("SPLIT", INK, 7.05), ("IT", INK, 7.2)], 'anton', 104, 330, key='s2h')
    tk = [(ticket('TERM 1', '₹28,000', 'APRIL'), 7.3, 590, -1.6),
          (ticket('STATIONERY', '₹8,000', 'APRIL'), 8.4, 830, 1.1),
          (ticket('TERM 2', '₹28,000', 'OCTOBER', True), 11.4, 1070, -0.8)]
    offs = []
    for i, (im, t0, y, r0) in enumerate(tk):
        p = prog(t, t0, 0.45)
        if p <= 0: offs.append(None); continue
        jx, jy, jr = jit(('tk', i), t, 1.6, 0.25)
        x = 540 + (1 - eo(p)) * 900 + jx
        place(c, im, x, y + jy, 1.0, r0 + jr + (1 - eo(p)) * -10)
        offs.append((x, y + jy))
    for i, t0 in ((0, 10.2), (1, 10.6)):
        sc, a = slam(t, t0)
        if a > 0 and offs[i]:
            place(c, stamp_c('PAID', GRN, 64, 12, i), offs[i][0] + 120, offs[i][1] + 4, sc, 0, a)
    if offs[2]:
        marker_ellipse(c, offs[2][0] + 205, offs[2][1] + 2, 125, 62, prog(t, 12.8, 0.55), RED, 8, seed=9)
    typed(c, '6 MONTHS AWAY.', 'type', 50, INK, 1265, t, 12.0, 13.0)
    if t > 14.4:
        place_text(c, 'idle money?', 'pfi', 96, RED, 540, 1395, t, 'idle2', 14.4, 'pop')


def s3(c, t):
    words_line(c, t, [("WHY", INK, 16.0), ("LET", INK, 16.25), ("IT", INK, 16.45), ("SIT", INK, 16.65)], 'anton', 136, 330, key='s3h')
    if t > 17.0:
        place_text(c, 'idle?', 'pfi', 180, RED, 540, 510, t, 'idle', 17.0, 'pop')
        for k, (zx, zy, zs) in enumerate(((800, 540, 44), (848, 488, 54), (900, 428, 64))):
            tt = t - 17.3 - k * 0.18
            if tt > 0:
                fl = math.sin(t * 2.2 + k) * 6
                place_text(c, 'z', 'mark', zs, INK, zx, zy + fl, t, ('z', k), 17.3 + k * 0.18, 'fade')
    if t > 18.2:
        place_text(c, '₹28,000', 'anton', 140, INK, 540, 700, t, 'n28', 18.2, 'pop')
    marker_line(c, [(540, 790), (538, 860), (540, 925)], prog(t, 18.8, 0.4), INK, 9, head=True)
    if t > 19.2:
        place_text(c, 'one stock', 'mark', 52, RED, 720, 860, t, 'one', 19.2, 'slide', rot=-5)
    if t > 20.55:
        dy, a = drop(t, 20.55, 300)
        hp = round(prog(t, 21.3, 0.5) * 20) / 20
        jx, jy, jr = jit('clip', t, 2, 0.5)
        place(c, clipping(hp), 540 + jx, 1115 + dy + jy, 1.0, -3 + jr + (1 - a) * 8, a)
    if t > 22.0:
        p = prog(t, 22.0, 0.4)
        jx, jy, jr = jit('buy', t, 1.5, 0.3)
        place(c, buy_card(), 540 + jx, 1420 + (1 - eo(p)) * 160 + jy, 1.0, 1.5 + jr, clamp(p * 3))


def chart_f(t):
    # fraction of chart revealed over time
    keys = [(24.95, 0.0), (26.6, 0.34), (28.2, 0.42), (31.2, 1.0)]
    if t <= keys[0][0]: return 0.0
    for (t0, f0), (t1, f1) in zip(keys, keys[1:]):
        if t <= t1: return f0 + (f1 - f0) * eio((t - t0) / (t1 - t0))
    return 1.0


def s4(c, t):
    if t > 24.85:
        place_text(c, 'YOUR ₹28,000 IS NOW', 'type', 42, INK, 540, 300, t, 'yn', 24.85, 'fade', track=2)
    f = chart_f(t)
    pr = price_at(f) if f > 0 else 8.25
    val = int(round(3393 * pr)) if f < 1 else 55238
    jx, jy, jr = jit('cnt', t, 1.2, 0.3)
    place(c, text_img(f'₹{val:,}', 'anton', 200, GRN), 540 + jx, 455 + jy, 1.0, jr)
    # sheet
    p = prog(t, 24.7, 0.45)
    sx0 = 540 - SW_ // 2; sy0 = 640
    sjx, sjy, _ = jit('sheet', t, 1.3, 0)
    ox, oy = sx0 + sjx, sy0 + sjy + (1 - eo(p)) * 600
    sh = cutout(sheet(), border=0, shadow=0.3) if not hasattr(s4, 'shc') else s4.shc
    s4.shc = sh
    place(c, sh, ox + SW_ / 2, oy + SH_ / 2, 1.0, 0, clamp(p * 3))
    # cutout() pads; compensate: padded image centred on sheet centre + shadow offset is fine visually
    if f > 0:
        s = series(); pts = [(ox + px(0) + (PX1 - PX0) * fr, oy + py(v)) for fr, v in s if fr <= f]
        pts.append((ox + px(0) + (PX1 - PX0) * f, oy + py(pr)))
        if len(pts) > 1:
            poly_fill(c, pts + [(pts[-1][0], oy + PY0), (pts[0][0], oy + PY0)], YEL, 150)
            stroke(c, pts, 9, INK)
        tx, ty = pts[-1]
        ImageDraw.Draw(c).ellipse((tx - 13, ty - 13, tx + 13, ty + 13), fill=RED, outline=INK, width=4)
        tg = text_img(f'₹{pr:.2f}', 'anton', 44, CREAM)
        bx, by = tx - tg.size[0] / 2, ty - 70
        ImageDraw.Draw(c).rounded_rectangle((bx - 6, by - 4, bx + tg.size[0] + 6, by + tg.size[1] - 6), radius=10, fill=INK)
        c.alpha_composite(tg, (int(bx), int(by - 4)))
    if t > 27.0:
        jxx = ox + px(2); jyy = oy + py(8.76)
        place_text(c, 'almost back to buy!', 'mark', 46, RED, ox + 420, oy + 330, t, 'abb', 27.0, 'slide', rot=-6)
        marker_line(c, curve((ox + 340, oy + 365), (jxx - 60, jyy - 140), (jxx - 6, jyy - 30)), prog(t, 27.25, 0.45), RED, 7, head=True, head_size=22)
    sc, a = slam(t, 31.3)
    if a > 0:
        place(c, stamp_c('+97%', GRN, 96, 10, 7), ox + 280, oy + 140, sc, 0, a)


def s5(c, t):
    words_line(c, t, [("THE", INK, 33.0), ("MATH", RED, 33.2)], 'anton', 124, 330, key='s5h')
    p = prog(t, 33.05, 0.45)
    jx, jy, jr = jit('rc', t, 1.0, 0)
    rc = receipt()
    rx0, ry0 = 540 - 410 + jx, 500 + jy + (1 - eo(p)) * 700
    place(c, rc, rx0 + rc.size[0] / 2 - (rc.size[0] - 820) / 2 + 3, ry0 + rc.size[1] / 2 - (rc.size[1] - 720) / 2 + 7, 1.0, 0, clamp(p * 3))
    if p <= 0: return
    def row(t0, y, lab, sub, amt, col, hl=None):
        q = prog(t, t0, 0.3)
        if q <= 0: return
        dx = (1 - eo(q)) * 40; a = clamp(q * 3)
        if hl is not None:
            highlight(c, rx0 + 40, ry0 + y - 46, rx0 + 780, ry0 + y + 46, prog(t, hl, 0.45), seed=21)
        li = text_img(lab, 'osw5', 50, INK); place(c, li, rx0 + 60 + li.size[0] / 2 - 6 + dx, ry0 + y - 14, 1, 0, a)
        if sub:
            si = text_img(sub, 'type', 26, (120, 112, 104), 1); place(c, si, rx0 + 60 + si.size[0] / 2 - 3 + dx, ry0 + y + 34, 1, 0, a)
        ai = text_img(amt, 'anton', 82, col); place(c, ai, rx0 + 770 - ai.size[0] / 2 + 10 - dx, ry0 + y, 1, 0, a)
    row(33.6, 120, 'Worth today', '3,393 × ₹16.28', '₹55,238', GRN)
    row(35.6, 290, 'Term 2 fee', 'sell ~1,720 shares', '−₹28,000', RED)
    q = prog(t, 37.25, 0.35)
    if q > 0:
        d = ImageDraw.Draw(c)
        for x in range(int(rx0 + 50), int(rx0 + 50 + 720 * eo(q)), 22):
            d.line((x, ry0 + 420, x + 11, ry0 + 420), fill=INK, width=4)
    row(37.6, 530, 'Left over', '', '₹27,238', INK, hl=38.0)
    typed(c, 'FEE PAID. ₹27,238 STILL INVESTED.', 'type', 36, INK, 1305, t, 38.6, 39.9)
    if t > 33.8:
        place_text(c, 'Approx. · bought 1 Apr @ ₹8.25 · price 16 Oct ₹16.28', 'type', 24, (120, 112, 104), 540, 1390, t, None, 33.8, 'fade')


def s6(c, t):
    words_line(c, t, [("THE", INK, 41.15), ("STOCK", INK, 41.35), ("PAID", INK, 41.6)], 'anton', 140, 400, key='s6a')
    words_line(c, t, [("MY", INK, 41.85), ("SON'S", INK, 41.95)], 'anton', 140, 560, key='s6b')
    tw = text_w('TERM 2', 'anton', 140); fw = text_w('FEE', 'anton', 140); g = 140 * 0.22
    x0 = 540 - (tw + g + fw) / 2
    highlight(c, x0 - 14, 655, x0 + tw + 14, 790, prog(t, 42.3, 0.4), seed=31)
    words_line(c, t, [("TERM 2", RED, 42.1), ("FEE", INK, 42.2)], 'anton', 140, 720, key='s6c')
    dy, a = drop(t, 42.3, 380)
    if a > 0:
        jx, jy, jr = jit('bp6', t, 2.5, 0.8)
        place(c, backpack(), 430 + jx, 1050 + dy + jy, 0.85, 5 + jr, a)
    sc, a = slam(t, 42.8)
    if a > 0:
        place(c, stamp_c('PAID', GRN, 110, 14, 3), 760, 1070, sc, 0, a)
    if t > 43.3:
        place_text(c, '+ ₹27,238 to spare', 'pfi', 76, INK, 540, 1330, t, 'spare', 43.3, 'slide')
        marker_line(c, [(250, 1395), (540, 1390), (830, 1380)], prog(t, 43.65, 0.45), GRN, 9)


def s7(c, t):
    if t > 45.8:
        p = prog(t, 45.8, 0.3)
        lw = text_w('REALITY CHECK', 'osw', 54, 2)
        x0 = 540 - (lw + 70) / 2
        place(c, warn_icon(RED), x0 + 28, 302, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
        place(c, text_img('REALITY CHECK', 'osw', 54, RED, 2), x0 + 70 + lw / 2, 300, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
    words_line(c, t, [("FEE", CREAM, 46.5), ("MONEY", CREAM, 46.65)], 'anton', 160, 480, key='s7a')
    words_line(c, t, [("IS", RED, 46.95), ("NOT", RED, 47.05)], 'anton', 160, 650, key='s7b')
    words_line(c, t, [("RISK", CREAM, 47.4), ("MONEY", CREAM, 47.55)], 'anton', 160, 820, key='s7c')
    marker_line(c, [(380, 752), (540, 746), (700, 740)], prog(t, 47.8, 0.35), RED, 10)
    if t > 48.9:
        p = prog(t, 48.9, 0.32)
        jx, jy, jr = jit('tag', t, 1.5, 0.4)
        place(c, tag_green(), 540 + jx, 1000 + jy, 0.55 + 0.45 * eback(p), -2 + jr, clamp(p * 3))
    if t > 49.95:
        place_text(c, 'can fall just as fast', 'mark', 58, RED, 500, 1135, t, 'fall', 49.95, 'slide', rot=-3)
        marker_line(c, [(860, 1090), (868, 1140), (862, 1185)], prog(t, 50.3, 0.35), RED, 9, head=True, head_size=24)
    typed(c, 'Not investment advice. DYOR.', 'type', 32, (200, 194, 182), 1250, t, 51.3, 52.6)
    if t > 53.9:
        p = prog(t, 53.9, 0.35)
        pul = 1 + 0.035 * math.sin((t - 54.3) * 6) if t > 54.3 else 1
        place(c, follow_btn(), 540, 1380, (0.5 + 0.5 * eback(p)) * pul, 0, clamp(p * 3))
    if t > 54.5:
        place_text(c, 'Comment "FEE" if you\'d do this', 'osw5', 40, CREAM, 540, 1505, t, None, 54.5, 'slide')


SCENES = [(0, s1), (6.5, s2), (15.8, s3), (24.6, s4), (32.9, s5), (41.0, s6), (45.6, s7)]


def scene_at(t):
    idx = 0
    for i, (st, _) in enumerate(SCENES):
        if t >= st: idx = i
    return idx


def header(c, dark):
    col = CREAM if dark else INK
    a = text_img('@moneyincloud', 'type', 30, col, 1)
    c.alpha_composite(a, (52, 64))
    b = text_img('REAL P&L · EP 2', 'type', 30, RED, 1)
    c.alpha_composite(b, (W - 52 - b.size[0], 64))
    ImageDraw.Draw(c).line((60, 118, W - 60, 118), fill=col, width=2)
    ImageDraw.Draw(c).line((60, 118, 300, 118), fill=col, width=6)


def transition(c, t):
    cols = [(RED, INK), (YEL, INK), (INK, RED), (RED, YEL), (YEL, RED), (INK, YEL)]
    for bi, b in enumerate(B):
        d = 0.62
        if abs(t - b) > d / 2 + 0.12: continue
        for layer, delay in ((0, -0.07), (1, 0.0)):
            p = (t - (b - d / 2) - delay) / d
            if p <= 0 or p >= 1: continue
            p = eio(p)
            SWd, skew = 2050, 320
            xl = (W + 60) + p * (-(SWd + skew) - (W + 60) - 40)
            r = random.Random(bi * 10 + layer)
            left = [(xl + r.uniform(-14, 14) - skew * (y / H), y) for y in range(0, H + 1, 40)]
            right = [(xl + SWd + r.uniform(-14, 14) - skew * (y / H), y) for y in range(H, -1, -40)]
            colr = cols[bi][layer]
            if layer == 0:
                left = [(x - 70, y) for x, y in left]; right = [(x + 70, y) for x, y in right]
            poly_fill(c, left + right, colr, 255, S=1)


def render(t):
    pbg, dbg = bgs()
    i = scene_at(t)
    dark = (i == 6)
    c = (dbg if dark else pbg).copy()
    st = SCENES[i][0]; en = SCENES[i + 1][0] if i + 1 < len(SCENES) else DUR
    SCENES[i][1](c, t)
    # camera: slow push-in + slam shake
    z = 1.0 + 0.045 * clamp((t - st) / (en - st))
    sx = sy = 0
    for (ts, amp) in SLAMS:
        if 0 <= t - ts < 0.35:
            k = math.exp(-(t - ts) * 14) * amp
            sx += k * math.sin((t - ts) * 90); sy += k * math.cos((t - ts) * 77)
    cw, ch = W / z, H / z
    cx, cy = W / 2 + sx, H * 0.47 + sy
    box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
    c = c.transform((W, H), Image.EXTENT, box, Image.BICUBIC)
    header(c, dark)
    transition(c, t)
    arr = np.asarray(c.convert('RGB')).astype(np.float32)
    g = grain_frames()[int(t * FPS) % 6]
    # flicker
    fl = 1 + 0.012 * math.sin(t * 37) * math.sin(t * 13)
    arr = arr * fl + g[..., None]
    return np.clip(arr, 0, 255).astype(np.uint8)
