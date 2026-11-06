"""Isometric style: how your bank makes money from your savings (SBI savings 2.5% vs home loans from 7.50%).
Narrator af_heart. Green topic colour."""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, re
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import stamp_c
from fridge import follow_btn

SH = ROOT + 'isobank/'
SCRIPT = [l['text'] for l in json.load(open(SH + 'lines.json'))]
DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO = [], []
_t = 0.0
for i, d in enumerate(DURS):
    STARTS.append(_t); VO.append(_t + (0.15 if i == 0 else 0.18)); _t = VO[-1] + d + 0.22
DUR = _t + 1.2
B = STARTS[1:]
GRN = (30, 130, 70); GOLD = (255, 197, 49); ORG = (255, 140, 60); NAVY = (43, 63, 140); RED = (226, 58, 44)
GREY = (100, 104, 118)


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def line_at(t):
    i = 0
    for k, s in enumerate(STARTS):
        if t >= s: i = k
    return i


# ---------- caption ----------
def segs(i):
    return [(m.start(), m.end()) for m in re.finditer(r'[^.!?]+[.!?]*\s*', SCRIPT[i])]


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
            num = any(ch.isdigit() for ch in wd) or wd.lower().startswith(('three', 'two', 'seven', 'five', 'one', 'six'))
            col = (GRN if num else INK) if done else (175, 175, 182)
            ti = text_img(wd, 'pop', size, col)
            im.alpha_composite(ti, (int(x - size * 0.12), int(y - ti.size[1] / 2)))
            x += text_w(wd + ' ', 'pop', size); pos += len(wd) + 1
        y += lh
    place(c, im, 540, cy)


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


# ---------- isometric world ----------
class Cam:
    S = 58; CX = 540; CY = 930


def P(x, y, z=0):
    return (Cam.CX + (x - y) * Cam.S * 0.866, Cam.CY + (x + y) * Cam.S * 0.5 - z * Cam.S)


def shade(c, f): return tuple(max(0, min(255, int(v * f))) for v in c)


def box(d, x, y, w, dp, h, col, z=0, top=None):
    a, b, c_, e = P(x, y, z + h), P(x + w, y, z + h), P(x + w, y + dp, z + h), P(x, y + dp, z + h)
    d.polygon([P(x, y + dp, z), P(x + w, y + dp, z), P(x + w, y + dp, z + h), P(x, y + dp, z + h)], fill=shade(col, 0.78), outline=INK)
    d.polygon([P(x + w, y, z), P(x + w, y + dp, z), P(x + w, y + dp, z + h), P(x + w, y, z + h)], fill=shade(col, 0.62), outline=INK)
    d.polygon([a, b, c_, e], fill=top or shade(col, 1.08), outline=INK)


def roof(d, x, y, w, dp, z, h, col):
    r1, r2 = P(x + w / 2, y, z + h), P(x + w / 2, y + dp, z + h)
    d.polygon([P(x + w, y, z), P(x + w, y + dp, z), r2, r1], fill=shade(col, 0.75), outline=INK)
    d.polygon([P(x, y + dp, z), P(x + w, y + dp, z), r2], fill=shade(col, 0.95), outline=INK)
    d.polygon([P(x, y, z), P(x, y + dp, z), r2, r1], fill=col, outline=INK)


def coin(d, x, y, z, c=GOLD, s=1.0):
    sx, sy = P(x, y, z); r = 32 * s * Cam.S / 58
    d.ellipse((sx - r, sy - r * 0.55, sx + r, sy + r * 0.55), fill=shade(c, 0.75), outline=INK, width=3)
    d.ellipse((sx - r, sy - r * 0.85, sx + r, sy + r * 0.25), fill=c, outline=INK, width=3)


@functools.lru_cache(None)
def sky():
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        q = y / H; d.line((0, y, W, y), fill=(int(214 + 30 * q), int(240 + 10 * q), 250))
    return im.convert('RGBA')


PATH_IN = [(-3.5, 1.3), (-3.5, 0), (0, 0), (0, -1.1), (3.5, -1.1), (3.5, -1.6)]   # you -> bank
PATH_LOAN = [(3.5, -1.6), (3.5, -1.1), (0, -1.1), (0, 1.0), (3.5, 1.0), (3.5, 1.9)]  # bank -> buyer


def along(path, q):
    segl = [math.dist(a, b) for a, b in zip(path, path[1:])]; L = sum(segl); s = q * L
    for (a, b), l in zip(zip(path, path[1:]), segl):
        if s <= l: f = s / l; return a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f
        s -= l
    return path[-1]


def flow(d, t, path, t0, t1, n, col, travel=1.6, rev=False, s=1.0):
    if t < t0: return
    for k in range(n):
        ts = t0 + (t1 - t0) * k / max(1, n)
        q = (t - ts) / travel
        if 0 <= q <= 1:
            x, y = along(path[::-1] if rev else path, q)
            coin(d, x, y, 0.75 + 0.15 * math.sin(q * math.pi), col, s)


def bank_h(t):
    return 2.8 + 1.4 * eo(prog(t, at(5, 'gap', -0.2), 1.5))


def draw_town(c, t):
    d = ImageDraw.Draw(c, 'RGBA')
    box(d, -6, -6, 12, 12, 0.5, (120, 205, 150), top=(150, 222, 170))
    for k in range(-6, 6):
        d.polygon([P(k, -0.6, 0.5), P(k + 1, -0.6, 0.5), P(k + 1, 0.6, 0.5), P(k, 0.6, 0.5)], fill=(90, 96, 110))
        d.polygon([P(-0.6, k, 0.5), P(0.6, k, 0.5), P(0.6, k + 1, 0.5), P(-0.6, k + 1, 0.5)], fill=(90, 96, 110))
    for k in range(-6, 6, 2):
        d.line([P(k + 0.3, 0, 0.51), P(k + 0.9, 0, 0.51)], fill=(255, 240, 180), width=4)
        d.line([P(0, k + 0.3, 0.51), P(0, k + 0.9, 0.51)], fill=(255, 240, 180), width=4)
    # bank (back)
    bh = bank_h(t)
    box(d, 1.5, -5.2, 4, 3.5, 0.4, (235, 235, 240), 0.5)
    box(d, 1.8, -4.9, 3.4, 2.9, bh, (245, 245, 250), 0.9)
    for k in range(5):
        x = 1.9 + k * 0.8; d.line([P(x, -2.0, 0.9), P(x, -2.0, 0.9 + bh)], fill=(180, 184, 196), width=max(4, int(10 * Cam.S / 58)))
    box(d, 1.6, -5.1, 3.8, 3.3, 0.35, NAVY, 0.9 + bh); roof(d, 1.6, -5.1, 3.8, 3.3, 1.25 + bh, 1.0, NAVY)
    sx, sy = P(3.5, -3.45, 2.6 + bh); d.text((sx, sy), '₹', font=font('pop', int(60 * Cam.S / 58)), fill=GOLD, anchor='mm')
    # your house
    box(d, -5, 1.5, 3, 3, 2, (255, 210, 120), 0.5); roof(d, -5, 1.5, 3, 3, 2.5, 1.4, (230, 90, 70))
    # trees
    for (tx, ty) in [(-4.5, -4.5), (-2.5, -3.8), (4.8, -0.7), (-4.6, 5), (1.2, 5.2)]:
        box(d, tx, ty, 0.3, 0.3, 0.6, (120, 80, 40), 0.5); x0, y0 = P(tx + 0.15, ty + 0.15, 1.5); r = 34 * Cam.S / 58
        d.ellipse((x0 - r, y0 - r, x0 + r, y0 + r), fill=(50, 160, 90), outline=INK, width=3)
    # coin flows (on the road, before the front house)
    flow(d, t, PATH_IN, at(1, 'one lakh', -0.3), at(1, 'one lakh', 2.2), 10, GOLD)
    flow(d, t, PATH_IN, at(2, 'pays you', 0), at(2, 'pays you', 3.5), 3, GOLD, 1.8, rev=True, s=0.75)
    flow(d, t, PATH_LOAN, at(4, 'lends', -0.2), at(4, 'lends', 2.0), 10, GOLD, 1.6)
    flow(d, t, PATH_LOAN, at(4, 'That is', -0.3), STARTS[6], 14, ORG, 1.7, rev=True)
    # home buyer (front)
    box(d, 2, 2, 3, 3, 2.4, (140, 190, 250), 0.5); roof(d, 2, 2, 3, 3, 2.9, 1.3, (60, 120, 210))


def tag_img(s, sub, colr):
    t = text_img(s, 'anton', 50, (255, 255, 255)); u = text_img(sub, 'pop', 30, INK)
    w = max(t.size[0], u.size[0]) + 50; h = t.size[1] + u.size[1] + 34
    card = Image.new('RGBA', (w + 10, h + 10), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
    cd.rounded_rectangle((10, 10, w + 9, h + 9), 22, fill=INK)
    cd.rounded_rectangle((0, 0, w - 1, h - 1), 22, fill='white', outline=INK, width=5)
    cd.rounded_rectangle((8, 8, w - 9, t.size[1] + 20), 16, fill=colr)
    card.alpha_composite(t, (int(w / 2 - t.size[0] / 2), 10)); card.alpha_composite(u, (int(w / 2 - u.size[0] / 2), t.size[1] + 22))
    return card


tag_img = functools.lru_cache(None)(tag_img)


def tag(c, t, t0, s, sub, colr, x, y, z):
    if t < t0: return
    p = prog(t, t0, 0.35); sx, sy = P(x, y, z)
    place(c, tag_img(s, sub, colr), sx, sy - 80, 0.5 + 0.5 * eback(p), 0, clamp(p * 3))


def ledger(c, t):
    rows = []
    if t > at(2, 'two thousand', -0.2): rows.append(('YOU GET', '₹2,500 / yr', GOLD))
    if t > at(4, 'seven thousand', -0.2): rows.append(('BANK GETS', '₹7,500 / yr', ORG))
    if t > at(5, 'gap', -0.2): rows.append(('GAP', 'about ₹5,000', GRN))
    if not rows: return
    w, h = 900, 80 + 92 * len(rows)
    im = Image.new('RGBA', (w + 12, h + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((12, 12, w + 11, h + 11), 30, fill=INK)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 30, fill='white', outline=INK, width=6)
    hd = text_img('ON YOUR ₹1 LAKH, PER YEAR', 'osw', 34, GREY); im.alpha_composite(hd, (int(w / 2 - hd.size[0] / 2), 18))
    for k, (a, b, col) in enumerate(rows):
        y = 80 + k * 92
        d.rounded_rectangle((30, y + 8, 80, y + 58), 12, fill=col, outline=INK, width=4)
        im.alpha_composite(text_img(a, 'anton', 56, INK), (110, y))
        tb = text_img(b, 'anton', 60, GRN if a == 'GAP' else INK); im.alpha_composite(tb, (w - 40 - tb.size[0], y - 2))
    place(c, im, 540, 1560 + (h - 172) / 2 * 0)


def footer(c):
    ImageDraw.Draw(c).rectangle((0, 1888, W, H), fill=(20, 22, 30, 255))
    place(c, text_img('Not a buy/sell call · Education only · @moneyincloud', 'osw5', 24, (230, 230, 236)), 540, 1904)


def set_cam(t):
    # drop-in on hook, gentle zooms per beat
    p = eo(prog(t, 0.0, 1.6))
    S = 34 + 24 * p; CY = 780 + 150 * p
    i = line_at(t)
    if i in (2,):
        q = eio(prog(t, STARTS[2], 0.8)); S += 8 * q; CY += 40 * q
    if i in (4, 5):
        q = eio(prog(t, STARTS[4], 0.8)); S += 4 * q
    if i >= 6:
        q = eio(prog(t, STARTS[6], 0.8)); S -= 16 * q; CY -= 120 * q
    Cam.S, Cam.CX, Cam.CY = S, 540, CY


def _render(t):
    i = line_at(t)
    set_cam(t)
    c = sky().copy()
    draw_town(c, t)
    tag(c, t, at(1, 'You put', -0.2), 'YOU', 'deposit ₹1 lakh', (230, 90, 70), -4.2, 3.2, 4.4)
    tag(c, t, at(2, 'pays you', -0.2), 'BANK', 'pays you 2.5%', NAVY, 3.6, -3.6, 4.2 + bank_h(t) - 2.8)
    tag(c, t, at(4, 'home buyer', -0.2), 'HOME BUYER', 'pays bank 7.5%+', (60, 120, 210), 4.6, 4.6, -1.2)
    if i == 0:
        place_text(c, 'STOP KEEPING BIG MONEY', 'anton', 92, INK, 540, 200, t, None, 0.05, 'pop')
        place_text(c, 'IN SAVINGS', 'anton', 150, GRN, 540, 340, t, None, at(0, 'savings', -0.2), 'pop')
        stamp_at(c, t, 'BANK EARNS 3X', RED, 90, -8, at(0, 'three times', -0.1), 540, 1560, 2)
    elif i == 3:
        place_text(c, 'WHERE DOES THE', 'anton', 110, INK, 540, 230, t, None, STARTS[3], 'pop')
        place_text(c, 'REST GO?', 'anton', 160, GRN, 540, 380, t, None, STARTS[3] + 0.2, 'pop')
    elif i == 6:
        caption(c, t, i, 300)
        items = [('Three to six', '1', '3–6 MONTHS OF EXPENSES', 'keep in savings'), ('sweep-in', '2', 'SWEEP-IN FD', 'compare rates'),
                 ('liquid fund', '3', 'LIQUID FUND', 'compare returns & risk')]
        for k, (ph, n, a, b) in enumerate(items):
            tk = at(6, ph if ph != 'Three to six' else 'three to six', -0.2)
            if t < tk: continue
            p = prog(t, tk, 0.4)
            place(c, tag_img(a, b, (GRN, NAVY, ORG)[k]), 540, 1380 + k * 170 + (1 - eo(p)) * 100, 1.15, 0, clamp(p * 3))
    elif i == 7:
        caption(c, t, i, 300)
        tf = at(7, 'Follow', -0.1)
        if t > tf: place(c, follow_btn(), 540, 1500, 0.6 + 0.4 * eback(prog(t, tf, 0.35)), 2)
        if t > at(7, 'stop', -0.2):
            place_text(c, 'STOP KEEPING BIG MONEY IN SAVINGS', 'anton', 64, GRN, 540, 1700, t, None, at(7, 'stop', -0.2), 'pop')
    else:
        caption(c, t, i, 260)
    if i in (1, 2, 4, 5):
        ledger(c, t)
    if i == 5:
        place(c, text_img('Simplified: banks also pay for staff, branches, reserves (CRR/SLR) and bad loans.', 'osw5', 25, GREY), 540, 1835)
    if i in (2, 4):
        place(c, text_img('SBI savings 2.50% (StableMoney, Feb 2026) · SBI home loans 7.50%–8.80% (Business Today, Oct 2026)', 'osw5', 22, GREY), 540, 1855)
    footer(c)
    st = STARTS[i]
    z = 1.0 + (0.04 * math.exp(-(t - st) * 9) if i > 0 else 0)
    if z > 1.001:
        cw, ch = W / z, H / z
        c = c.transform((W, H), Image.EXTENT, (540 - cw / 2, 960 - ch / 2, 540 + cw / 2, 960 + ch / 2), Image.BICUBIC)
    return c


def render(t):
    LOOP = 0.5
    if t > DUR - LOOP:
        a = np.asarray(_render(t).convert('RGB')).astype(float); b = np.asarray(_render(1.8).convert('RGB')).astype(float)
        q = eio((t - (DUR - LOOP)) / LOOP)
        return (a * (1 - q) + b * q).astype(np.uint8)
    return np.asarray(_render(t).convert('RGB'))
