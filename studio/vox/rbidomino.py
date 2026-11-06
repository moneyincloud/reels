"""Domino Reveal style: One RBI decision hits your wallet (repo 5.25 -> 5.50, 7 Oct 2026).
Narrator am_michael via vo_cast.py. Orange topic colour. Cloud Family faces as reactions."""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, re
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from lib import *
from scenes import stamp_c
from fridge import follow_btn

SH = ROOT + 'rbidomino/'
CAST_DIR = ROOT + 'brand/cast_real/'
SCRIPT = [l['text'] for l in json.load(open(SH + 'lines.json'))]
DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO = [], []
_t = 0.0
for i, d in enumerate(DURS):
    STARTS.append(_t); VO.append(_t + (0.15 if i == 0 else 0.18)); _t = VO[-1] + d + 0.22
DUR = _t + 1.2
B = STARTS[1:]
OR = (255, 138, 61); OR2 = (214, 96, 24); GRN = (36, 160, 90); RED = (226, 58, 44); GREY = (100, 104, 118)
CREAM = (255, 250, 242)


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def line_at(t):
    i = 0
    for k, s in enumerate(STARTS):
        if t >= s: i = k
    return i


# ---------- helpers ----------
@functools.lru_cache(None)
def person(name, w):
    im = Image.open(CAST_DIR + f'cut/{name}.png').convert('RGBA')
    h = int(im.size[1] * w / im.size[0]); im = im.resize((w, h), Image.LANCZOS)
    rgb = im.convert('RGB').filter(ImageFilter.UnsharpMask(2, 60, 2)); rgb.putalpha(im.getchannel('A'))
    return rgb


def actor(c, t, name, cx, w, base, t0):
    if t < t0: return
    p = eo(prog(t, t0, 0.45))
    im = person(name, w)
    comp(c, im, cx - im.size[0] / 2, base - im.size[1] * p + (1 - p) * 0 + math.sin(t * 2.4) * 3)


def pill_text(s, bg, fg, size=64, pad=(36, 14)):
    tt = text_img(s, 'anton', size, fg)
    w, h = tt.size[0] + 2 * pad[0], tt.size[1] + 2 * pad[1]
    im = Image.new('RGBA', (w + 10, h + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 10, w + 9, h + 9), 30, fill=INK)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 30, fill=bg, outline=INK, width=6)
    im.alpha_composite(tt, (pad[0], pad[1]))
    return im


def stamp_at(c, t, txt, colr, size, rot, t0, cx, cy, seed=1):
    if t < t0: return
    p = prog(t, t0, 0.22)
    place(c, stamp_c(txt, colr, size, rot, seed), cx, cy, 1 + 1.2 * (1 - eo(p)), 0, clamp(p * 4))


def segs(i):
    return [(m.start(), m.end()) for m in re.finditer(r'[^.!?:]+[.!?:]*\s*', SCRIPT[i])]


@functools.lru_cache(None)
def lay(i, seg, size, maxw):
    words = SCRIPT[i][seg[0]:seg[1]].split(); lines, cur = [], []
    for wd in words:
        if cur and text_w(' '.join(cur + [wd]), 'pop', size) > maxw: lines.append(cur); cur = [wd]
        else: cur.append(wd)
    if cur: lines.append(cur)
    return lines


def caption(c, t, i, cy, size=46):
    if t < VO[i] - 0.1: return
    sp = clamp((t - VO[i]) / DURS[i]) * len(SCRIPT[i])
    sg = [g for g in segs(i) if g[0] <= sp][-1] if sp > 0 else segs(i)[0]
    lines = lay(i, sg, size, 880); lh = int(size * 1.3)
    bw = max(text_w(' '.join(l), 'pop', size) for l in lines) + 80; bh = lh * len(lines) + 46
    im = Image.new('RGBA', (bw + 12, bh + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 10, bw + 9, bh + 9), 36, fill=INK)
    d.rounded_rectangle((0, 0, bw - 1, bh - 1), 36, fill=(255, 255, 255), outline=INK, width=6)
    pos = sg[0]; y = 23 + lh // 2
    for ln in lines:
        x = bw / 2 - text_w(' '.join(ln), 'pop', size) / 2
        for wd in ln:
            done = pos <= sp
            col = (OR2 if any(ch.isdigit() for ch in wd) or wd.startswith(('seven', 'five', 'one', 'quarter')) else INK) if done else (175, 175, 182)
            ti = text_img(wd, 'pop', size, col)
            im.alpha_composite(ti, (int(x - size * 0.12), int(y - ti.size[1] / 2)))
            x += text_w(wd + ' ', 'pop', size); pos += len(wd) + 1
        y += lh
    place(c, im, 540, cy)


def src(c, txt, y=1850):
    place(c, text_img(txt, 'osw5', 25, (90, 92, 104)), 540, y)


# ---------- world ----------
@functools.lru_cache(None)
def bg():
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        q = y / H; d.line((0, y, W, y), fill=(int(255 - 6 * q), int(243 - 22 * q), int(228 - 34 * q)))
    for k in range(0, W + 200, 90):
        d.ellipse((k - 4, 80, k + 4, 88), fill=(246, 222, 196))
    return im.convert('RGBA')


DW, DH, DEP = 230, 430, 24
SP = 470
X0 = 300
BASE = 1160
LAB = [('RBI HIKES', 'REPO RATE'), ('BANKS RAISE', 'LOAN RATES'), ('YOUR EMI', 'GOES UP'), ('FAMILIES', 'SPEND LESS'),
       ('SALES', 'SLOW DOWN'), ('FD RATES', 'CAN RISE')]


@functools.lru_cache(None)
def dom_img(k, lit):
    w, h, dep = DW, DH, DEP
    im = Image.new('RGBA', (w + dep + 14, h + dep + 14), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    side = OR2 if k < 5 else (20, 120, 64)
    face = (OR if k < 5 else GRN) if lit else CREAM
    d.rounded_rectangle((dep + 10, 10, w + dep + 9, h + 9), 26, fill=INK)
    d.rounded_rectangle((dep, 0, w + dep - 1, h - 1), 26, fill=side, outline=INK, width=6)
    d.rounded_rectangle((0, dep, w - 1, h + dep - 1), 26, fill=face, outline=INK, width=6)
    d.line((22, dep + h * 0.44, w - 22, dep + h * 0.44), fill=INK, width=5)
    numc = (255, 255, 255) if lit else (OR if k < 5 else GRN)
    nt = text_img(str(k + 1) if k < 5 else '+', 'anton', 120, numc)
    im.alpha_composite(nt, (w // 2 - nt.size[0] // 2, dep + 34))
    y = dep + h * 0.44 + 26
    for ln in LAB[k]:
        t = text_img(ln, 'anton', 44, (255, 255, 255) if lit else INK)
        s = min(1.0, (w - 28) / t.size[0])
        if s < 1: t = t.resize((int(t.size[0] * s), int(t.size[1] * s)), Image.LANCZOS)
        im.alpha_composite(t, (w // 2 - t.size[0] // 2, int(y))); y += t.size[1] + 8
    return im


# fall times per domino (line index -> domino)
FALL_LINE = {0: 2, 1: 3, 2: 5, 3: 6, 4: 7}


def fall_t(k):
    if k == 5: return at(8, 'other way', -0.2)
    return VO[FALL_LINE[k]] + 0.25


REST = [84] * 5 + [70]


def angle(k, t):
    tf = fall_t(k)
    if t < tf:
        # small nudge when the previous one hits it
        if 0 < k < 5 and t > fall_t(k - 1) + 0.3:
            return 5 * eo(prog(t, fall_t(k - 1) + 0.3, 0.2))
        return 0.0
    p = prog(t, tf, 0.5)
    a = REST[k] * (eio(p) if p < 1 else 1)
    if p >= 1: a += 2 * math.exp(-(t - tf - 0.5) * 6) * math.sin((t - tf - 0.5) * 30)
    return a


def wx(k):
    return X0 + k * SP if k < 5 else X0 + 4 * SP + 760


# camera keyframes: (time, camx, zoom)
def cam(t):
    K = [(0, wx(0) + 60, 1.25), (STARTS[1], wx(0) + 60, 1.25), (STARTS[1] + 1.4, wx(2) + 115, 0.45),
         (STARTS[2], wx(0) + 130, 1.0), (STARTS[3], wx(1) + 130, 1.0), (STARTS[4], wx(1) + 260, 0.75),
         (STARTS[5], wx(2) + 130, 1.0), (STARTS[6], wx(3) + 130, 1.0), (STARTS[7], wx(4) + 160, 1.0),
         (STARTS[8], wx(5) - 250, 0.8), (STARTS[9], (wx(0) + wx(5)) / 2 + 100, 0.36)]
    for a, b in zip(K, K[1:]):
        if t < b[0]:
            return a[1], a[2]
        if t < b[0] + 0.7 or b is K[-1]:
            q = eio(clamp((t - b[0]) / 0.7))
            nxt = K[K.index(b) + 1] if b is not K[-1] else None
            if nxt is None or t < nxt[0]:
                return a[1] + (b[1] - a[1]) * q, a[2] + (b[2] - a[2]) * q
    return K[-1][1], K[-1][2]


def to_screen(x, y, cx, z):
    return 540 + (x - cx) * z, BASE + (y - BASE) * z


def draw_world(c, t):
    cx, z = cam(t)
    # floor band
    d = ImageDraw.Draw(c)
    fy = BASE + 6
    d.rectangle((0, fy, W, fy + 34 * z + 10), fill=(236, 206, 172)); d.line((0, fy, W, fy), fill=INK, width=5)
    order = [0, 1, 2, 3, 4, 5]
    for k in order:
        if k == 5 and t < at(8, 'But', -0.3): continue
        a = angle(k, t)
        lit = t >= fall_t(k) - 0.05
        im = dom_img(k, lit)
        th = math.radians(a)
        w_, h_ = im.size
        if k < 5:  # pivot bottom-right, falls right (clockwise)
            px, py = wx(k) + DW / 2, BASE
            vx, vy = -w_ / 2 + 10, -h_ / 2 + 10
            rx, ry = vx * math.cos(th) - vy * math.sin(th), vx * math.sin(th) + vy * math.cos(th)
            rot = -a
        else:      # falls left
            px, py = wx(k) - DW / 2, BASE
            vx, vy = w_ / 2 - 10, -h_ / 2 + 10
            rx, ry = vx * math.cos(th) + vy * math.sin(th), -vx * math.sin(th) + vy * math.cos(th)
            rot = a
        sx, sy = to_screen(px + rx, py + ry, cx, z)
        if k == 5:
            p = prog(t, at(8, 'But', -0.3), 0.4); sy -= (1 - eback(p)) * 0
            place(c, im, sx, sy, z * (0.4 + 0.6 * eback(p)), rot)
        else:
            place(c, im, sx, sy, z, rot)
        if 0 <= t - fall_t(k) < 0.3 and k < 5:
            # impact burst
            bx, by = to_screen(wx(k) + DW / 2 + 40, BASE - DH * 0.8, cx, z)
            q = (t - fall_t(k)) / 0.3
            for j in range(6):
                ang = -math.pi / 2 + (j - 2.5) * 0.35
                r0, r1 = 20 + 60 * q, 60 + 90 * q
                ImageDraw.Draw(c).line((bx + r0 * math.cos(ang), by + r0 * math.sin(ang), bx + r1 * math.cos(ang), by + r1 * math.sin(ang)),
                                       fill=INK, width=6)


def info_card(lines, colr=OR2, w=720):
    rows = [text_img(s, 'anton' if k == 0 else 'pop', sz, col) for k, (s, sz, col) in enumerate(lines)]
    h = sum(r.size[1] for r in rows) + 30 * len(rows) + 30
    im = Image.new('RGBA', (w + 12, h + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((12, 12, w + 11, h + 11), 32, fill=INK)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 32, fill=(255, 255, 255), outline=INK, width=6)
    d.rounded_rectangle((0, 0, 22, h - 1), 10, fill=colr)
    y = 28
    for r in rows:
        s = min(1.0, (w - 80) / r.size[0])
        if s < 1: r = r.resize((int(r.size[0] * s), int(r.size[1] * s)), Image.LANCZOS)
        im.alpha_composite(r, (int(w / 2 + 8 - r.size[0] / 2), y)); y += r.size[1] + 30
    return im


def card_at(c, t, t0, lines, colr=OR2, x=680, y=1480, w=720):
    if t < t0: return
    p = prog(t, t0, 0.4)
    place(c, info_card(tuple(lines), colr, w), x, y + (1 - eo(p)) * 160, 1, -1.5, clamp(p * 3))


info_card = functools.lru_cache(None)(info_card)


def heading(c, t, i, s, colr=OR2):
    p = prog(t, STARTS[i], 0.35)
    place(c, pill_text(s, colr, (255, 255, 255), 58), 540, 190, 0.7 + 0.3 * eback(p), -2, clamp(p * 3))


def footer(c):
    ImageDraw.Draw(c).rectangle((0, 1888, W, H), fill=(20, 22, 30, 255))
    place(c, text_img('Not a buy/sell call · Education only · @moneyincloud', 'osw5', 24, (230, 230, 236)), 540, 1904)


# ---------- frame ----------
def _render(t):
    i = line_at(t)
    c = bg().copy()
    draw_world(c, t)
    if i == 0:
        place_text(c, 'STOP IGNORING', 'anton', 140, INK, 540, 230, t, None, 0.05, 'pop')
        place_text(c, 'THIS RBI NEWS', 'anton', 140, OR2, 540, 380, t, None, at(0, 'RBI', -0.2), 'pop')
        if t > at(0, 'raised', -0.1):
            p = prog(t, at(0, 'raised', -0.1), 0.35)
            place(c, pill_text('EMI +₹768 A MONTH', RED, (255, 255, 255), 70), 420, 1400, 0.5 + 0.5 * eback(p), -3)
        actor(c, t, 'appa_shock', 890, 340, 1888, at(0, 'raised', 0.1))
    elif i == 1:
        caption(c, t, i, 330)
        p = prog(t, at(1, 'fifty', -0.1), 0.35)
        if p > 0: place(c, pill_text('₹50 LAKH · 20-YEAR HOME LOAN', OR, INK, 60), 540, 1420, 0.5 + 0.5 * eback(p), -2)
    elif i == 2:
        heading(c, t, i, 'DOMINO 1 · RBI')
        caption(c, t, i, 380)
        card_at(c, t, at(2, 'raised', -0.2), [('REPO 5.25% TO 5.50%', 84, RED), ('RBI policy · 7 Oct 2026', 40, INK),
                                              ('stance: "calibrated tightening"', 34, GREY)], x=540, w=860)
    elif i == 3:
        heading(c, t, i, 'DOMINO 2 · YOUR BANK')
        caption(c, t, i, 380)
        card_at(c, t, at(3, 'SBI', -0.2), [('SBI LOAN RATES +0.25%', 84, RED), ('EBLR-linked loans, from 15 Oct 2026', 38, INK),
                                           ('home loans now 7.50% to 8.80%', 34, GREY)], x=540, w=860)
    elif i == 4:
        place_text(c, 'NOW WATCH', 'anton', 130, INK, 540, 300, t, None, STARTS[4], 'pop')
        place_text(c, 'YOUR MONEY', 'anton', 150, OR2, 540, 450, t, None, STARTS[4] + 0.25, 'pop')
    elif i == 5:
        heading(c, t, i, 'DOMINO 3 · YOUR EMI')
        caption(c, t, i, 380)
        card_at(c, t, at(5, 'Your loan', -0.2), [('7.50% TO 7.75%', 80, OR2), ('your loan rate (if passed on fully)', 34, GREY)])
        if t > at(5, 'EMI jumps', -0.2):
            card_at(c, t, at(5, 'EMI jumps', -0.2), [('+₹768 A MONTH', 90, RED), ('EMI ₹40,280 to ₹41,047', 40, INK),
                                                     ('₹50 lakh · 20 years', 32, GREY)])
        if t > at(5, 'About', -0.2):
            card_at(c, t, at(5, 'About', -0.2), [('₹1.84 LAKH MORE', 90, RED), ('extra interest over 20 years', 40, INK),
                                                 ('my calculation', 30, GREY)])
        actor(c, t, 'appa_shock', 175, 330, 1888, at(5, 'EMI jumps', 0))
        if t > at(5, 'EMI jumps', 0.3): stamp_at(c, t, 'OUCH', RED, 70, 12, at(5, 'EMI jumps', 0.3), 175, 1330, 3)
    elif i == 6:
        heading(c, t, i, 'DOMINO 4 · SPENDING')
        caption(c, t, i, 380)
        card_at(c, t, at(6, 'Families', -0.3), [('LESS TO SPEND', 90, OR2), ('more salary goes to EMI', 40, INK),
                                                ('fewer trips, gadgets, eating out', 32, GREY)])
        actor(c, t, 'amma_worried', 175, 330, 1888, at(6, 'Families', -0.2))
    elif i == 7:
        heading(c, t, i, 'DOMINO 5 · COMPANIES')
        caption(c, t, i, 380)
        card_at(c, t, at(7, 'Companies', -0.2), [('SALES SLOW', 90, OR2), ('lower demand, lower profits', 40, INK),
                                                 ('stock prices can feel it', 34, GREY)], x=540, w=860)
        if t > at(7, 'stock', -0.2):
            stamp_at(c, t, 'STOCKS CAN FALL', RED, 70, -8, at(7, 'stock', -0.2), 540, 1720, 4)
    elif i == 8:
        heading(c, t, i, 'THE TWIST', GRN)
        caption(c, t, i, 380)
        card_at(c, t, at(8, 'FD rates', -0.2), [('FD RATES CAN RISE', 84, GRN), ('savers can earn more', 40, INK),
                                                ('compare rates before you book', 32, GREY)], colr=GRN)
        actor(c, t, 'paati_happy', 175, 330, 1888, at(8, 'FD rates', 0))
    else:
        caption(c, t, i, 330)
        tf = at(9, 'Follow', -0.1)
        if t > tf: place(c, follow_btn(), 540, 1480, 0.6 + 0.4 * eback(prog(t, tf, 0.35)), 2)
        if t > at(9, 'stop ignoring', -0.2):
            place_text(c, 'STOP IGNORING THIS RBI NEWS', 'anton', 76, OR2, 540, 1680, t, None, at(9, 'stop ignoring', -0.2), 'pop')
    if i in (2, 3):
        src(c, 'Sources: RBI policy statement 7 Oct 2026 (via SCC Online); Business Today 21 Oct 2026')
    if i == 5:
        src(c, 'Example: SBI-style EBLR loan, full 0.25% pass-through. Your bank and spread may differ.')
    if i in (5, 6, 8):
        src(c, 'Characters are fictional', 1815)
    footer(c)
    # punch on line change
    st = STARTS[i]
    z = 1.0 + (0.05 * math.exp(-(t - st) * 9) if i > 0 else 0)
    if z > 1.001:
        cw, ch = W / z, H / z
        c = c.transform((W, H), Image.EXTENT, (540 - cw / 2, 960 - ch / 2, 540 + cw / 2, 960 + ch / 2), Image.BICUBIC)
    return c


def render(t):
    LOOP = 0.5
    if t > DUR - LOOP:
        a = np.asarray(_render(t).convert('RGB')).astype(float); b = np.asarray(_render(1.2).convert('RGB')).astype(float)
        q = eio((t - (DUR - LOOP)) / LOOP)
        return (a * (1 - q) + b * q).astype(np.uint8)
    return np.asarray(_render(t).convert('RGB'))
