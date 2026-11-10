"""Glow Atom style: 2027 watchlist - 5 sectors HSBC named (9 Nov 2026), Citi Nifty 28,000 end-2027.
Nifty nucleus, 5 glowing orbits/electrons, dark navy space. Narrator am_michael."""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, re
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from lib import W, H, place, prog, eo, eio, eback, clamp, text_img, text_w
from fridge import follow_btn

SH = ROOT + 'watch27/'
SCRIPT = [l['text'] for l in json.load(open(SH + 'lines.json'))]
DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO = [], []
_t = 0.0
for i, d in enumerate(DURS):
    STARTS.append(_t); VO.append(_t + (0.15 if i == 0 else 0.14)); _t = VO[-1] + d + 0.22
DUR = _t + 1.2
B = STARTS[1:]
GOLD = (255, 200, 70); CYAN = (90, 220, 255); WHITE = (240, 246, 255); DIM = (70, 90, 140); RED = (255, 90, 80)
SEC = [('BANKS', 'strong credit growth', (90, 220, 255)),
       ('INDUSTRIALS', 'capital goods · cement · ports · EMS', (255, 200, 70)),
       ('CONSUMER DISC.', 'retailers · autos', (255, 120, 200)),
       ('REAL ESTATE', 'housing & property', (140, 255, 160)),
       ('HOSPITALS', 'healthcare demand', (190, 150, 255))]
CX, CY = 540, 960


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase); assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def line_at(t):
    i = 0
    for k, s in enumerate(STARTS):
        if t >= s: i = k
    return i


@functools.lru_cache(None)
def space():
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt((xx - CX) ** 2 + (yy - CY) ** 2) / 1100
    base = np.stack([12 + 20 * (1 - r), 20 + 30 * (1 - r), 48 + 60 * (1 - r)], -1).clip(0, 255)
    rng = np.random.default_rng(7)
    for _ in range(260):
        x, y = rng.integers(0, W), rng.integers(0, H); b = rng.uniform(80, 220)
        base[y, x] = [b, b, b + 20]
    im = Image.fromarray(base.astype(np.uint8)).convert('RGBA')
    d = ImageDraw.Draw(im)
    for x in range(0, W, 90): d.line((x, 0, x, H), fill=(30, 44, 80), width=1)
    for y in range(0, H, 90): d.line((0, y, W, y), fill=(30, 44, 80), width=1)
    return im


ORB = [(440, 150, k * 36 - 72) for k in range(5)]


def orbit_pts(k, n=120):
    a, b, rho = ORB[k]; r = math.radians(rho)
    return [(CX + a * math.cos(th) * math.cos(r) - b * math.sin(th) * math.sin(r),
             CY + a * math.cos(th) * math.sin(r) + b * math.sin(th) * math.cos(r)) for th in np.linspace(0, 2 * math.pi, n)]


def electron(k, t):
    a, b, rho = ORB[k]; r = math.radians(rho); th = t * (0.9 + 0.12 * k) + k * 1.3
    return (CX + a * math.cos(th) * math.cos(r) - b * math.sin(th) * math.sin(r),
            CY + a * math.cos(th) * math.sin(r) + b * math.sin(th) * math.cos(r))


def lit_t(k):
    return VO[4 + k] + 0.2


CARD_XY = [(250, 470), (830, 470), (870, 1440), (540, 1500), (210, 1440)]


def sector_card(k, active):
    name, why, col = SEC[k]
    t1 = text_img(name, 'anton', 58 if active else 40, col)
    t2 = text_img(why, 'osw5', 30 if active else 24, WHITE)
    w = max(t1.size[0], t2.size[0]) + 50; h = t1.size[1] + t2.size[1] + 36
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 22, fill=(10, 18, 40, 220), outline=col, width=4 if active else 2)
    im.alpha_composite(t1, ((w - t1.size[0]) // 2, 10)); im.alpha_composite(t2, ((w - t2.size[0]) // 2, t1.size[1] + 18))
    return im


sector_card = functools.lru_cache(None)(sector_card)


def glow_layer(t, i):
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
    sharp = Image.new('RGBA', (W, H), (0, 0, 0, 0)); s = ImageDraw.Draw(sharp)
    on = clamp(t / 0.8)
    # orbits
    for k in range(5):
        lit = t >= lit_t(k)
        col = SEC[k][2] if lit else DIM
        pts = orbit_pts(k)
        alpha = 255 if lit else int(130 * on)
        s.line(pts, fill=(*col, alpha), width=4 if lit else 2)
        if lit: d.line(pts, fill=(*col, 200), width=14)
    # staples ghost orbit
    if i >= 9:
        a = 0.5 + 0.5 * math.sin(t * 9)
        pts = [(CX + 560 * math.cos(th), CY + 560 * 0.3 * math.sin(th)) for th in np.linspace(0, 2 * math.pi, 140)]
        s.line(pts, fill=(150, 150, 160, int(120 + 100 * a)), width=3)
    # citi target ring
    if t > at(2, 'Citi', -0.2):
        p = eo(prog(t, at(2, 'Citi', -0.2), 0.8)); R = 280 + 330 * p
        for k in range(0, 360, 8):
            a0 = math.radians(k + t * 10)
            s.arc((CX - R, CY - R, CX + R, CY + R), k + t * 10, k + t * 10 + 4, fill=(*GOLD, 200), width=4)
    # nucleus
    pulse = 1 + 0.06 * math.sin(t * 3)
    R = 110 * pulse * (0.3 + 0.7 * eback(clamp(t / 0.9)))
    d.ellipse((CX - R * 1.6, CY - R * 1.6, CX + R * 1.6, CY + R * 1.6), fill=(255, 190, 80, 160))
    s.ellipse((CX - R, CY - R, CX + R, CY + R), fill=(255, 220, 140, 255), outline=(255, 255, 230), width=4)
    # electrons
    for k in range(5):
        if t < lit_t(k) - 0.05 and i < 3: continue
        x, y = electron(k, t)
        lit = t >= lit_t(k)
        col = SEC[k][2] if lit else (120, 140, 190)
        r = 20 if lit else 10
        if lit: d.ellipse((x - 46, y - 46, x + 46, y + 46), fill=(*col, 220))
        s.ellipse((x - r, y - r, x + r, y + r), fill=(*WHITE, 255) if lit else (*col, 255))
    blur = g.filter(ImageFilter.GaussianBlur(22))
    return blur, sharp


def segs(i):
    return [(m.start(), m.end()) for m in re.finditer(r'[^.!?]+[.!?]*\s*', SCRIPT[i])]


def caption(c, t, i, cy=1700, size=46):
    if t < VO[i] - 0.05: return
    sp = clamp((t - VO[i]) / DURS[i]) * len(SCRIPT[i])
    sg = [g for g in segs(i) if g[0] <= sp][-1] if sp > 0 else segs(i)[0]
    words = SCRIPT[i][sg[0]:sg[1]].replace('twenty twenty seven', '2027').split()
    lines, cur = [], []
    for wd in words:
        if cur and text_w(' '.join(cur + [wd]), 'pop', size) > 880: lines.append(cur); cur = [wd]
        else: cur.append(wd)
    if cur: lines.append(cur)
    lh = int(size * 1.3); w = max(text_w(' '.join(l), 'pop', size) for l in lines) + 70; h = lh * len(lines) + 34
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 26, fill=(8, 14, 34, 225), outline=(70, 90, 140), width=2)
    # map displayed words back onto spoken progress (approx by word fraction)
    allw = sum(len(l) for l in lines); done = int(clamp((sp - sg[0]) / max(1, sg[1] - sg[0])) * allw + 0.999)
    k = 0; y = 17 + lh // 2
    for ln in lines:
        x = w / 2 - text_w(' '.join(ln), 'pop', size) / 2
        for wd in ln:
            col = (GOLD if any(ch.isdigit() for ch in wd) else WHITE) if k < done else (110, 120, 150)
            ti = text_img(wd, 'pop', size, col); im.alpha_composite(ti, (int(x - size * 0.12), int(y - ti.size[1] / 2)))
            x += text_w(wd + ' ', 'pop', size); k += 1
        y += lh
    place(c, im, 540, cy)


def pill(s, bg, fg, size=56):
    t = text_img(s, 'anton', size, fg)
    im = Image.new('RGBA', (t.size[0] + 60, t.size[1] + 26), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, im.size[0] - 1, im.size[1] - 1), 30, fill=bg)
    im.alpha_composite(t, (30, 13)); return im


pill = functools.lru_cache(None)(pill)


def _render(t):
    i = line_at(t)
    c = space().copy()
    blur, sharp = glow_layer(t, i)
    c = Image.fromarray(np.minimum(255, np.asarray(c).astype(np.int16) + np.asarray(blur).astype(np.int16) *
                                   (np.asarray(blur)[..., 3:4] / 255.0)).astype(np.uint8))
    c.alpha_composite(sharp)
    # nucleus label / counter
    if i == 1:
        tk = at(1, 'jumped', -0.2); v = 22363 + (25044.65 - 22363) * eo(prog(t, tk, 1.6)) if t > tk else 22363
        place(c, text_img(f'{v:,.0f}', 'anton', 64, (40, 26, 10)), CX, CY)
        if t > tk + 0.6: place(c, pill('+11.99% IN 30 DAYS', (40, 170, 90), WHITE, 56), 540, 420, 0.6 + 0.4 * eback(prog(t, tk + 0.6, 0.3)))
    elif i == 2:
        place(c, text_img('25,044', 'anton', 64, (40, 26, 10)), CX, CY)
        if t > at(2, 'Citi', -0.2):
            place(c, pill('CITI: 28,000 BY END-2027', GOLD, (20, 20, 30), 60), 540, 380, 0.6 + 0.4 * eback(prog(t, at(2, 'Citi', -0.2), 0.3)))
            place(c, text_img('about 12% above the last close', 'osw5', 34, WHITE), 540, 470)
    else:
        place(c, text_img('NIFTY', 'anton', 52, (40, 26, 10)), CX, CY - 18)
        place(c, text_img('50', 'anton', 46, (40, 26, 10)), CX, CY + 34)
    if i == 0:
        place(c, text_img('STOP.', 'anton', 140, RED), 540, 260, 0.7 + 0.3 * eback(prog(t, 0.05, 0.3)))
        if t > at(0, 'HSBC', -0.2):
            place(c, text_img('HSBC NAMED 5 SECTORS', 'anton', 78, WHITE), 540, 400, 1, 0, clamp((t - at(0, 'HSBC', -0.2)) * 4))
            place(c, text_img('FOR YOUR 2027 WATCHLIST', 'anton', 64, GOLD), 540, 490, 1, 0, clamp((t - at(0, 'watchlist', -0.4)) * 4))
    if i == 3:
        place(c, text_img('TARGET', 'anton', 90, WHITE), 540, 320)
        place(c, text_img('+ RIGHT SECTORS?', 'anton', 90, GOLD), 540, 430, 1, 0, clamp((t - at(3, 'without', -0.2)) * 4))
        for k in range(5):
            x, y = electron(k, t); place(c, text_img('?', 'anton', 50, (180, 190, 230)), x, y - 40)
    if 4 <= i <= 8 or i >= 9:
        cur = i - 4 if 4 <= i <= 8 else None
        for k in range(5):
            if t < lit_t(k): continue
            active = (k == cur)
            x, y = CARD_XY[k]; ex, ey = electron(k, t)
            card = sector_card(k, active)
            ImageDraw.Draw(c).line((x, y, ex, ey), fill=(*SEC[k][2], 160 if active else 70), width=2)
            p = prog(t, lit_t(k), 0.35)
            place(c, card, x, y, (0.5 + 0.5 * eback(p)) if active else 1, 0, 1 if not active else clamp(p * 3))
        if cur is not None:
            place(c, pill(f'SECTOR {cur + 1}', SEC[cur][2], (10, 14, 30), 44), 540, 220)
    if i == 9:
        place(c, pill('LESS PREFERRED: CONSUMER STAPLES', (90, 90, 100), WHITE, 46), 540, 230, 0.6 + 0.4 * eback(prog(t, STARTS[9] + 0.2, 0.3)))
    if i == 10:
        p = prog(t, at(10, 'watchlist', -0.2), 0.25)
        place(c, pill('WATCHLIST, NOT A BUY LIST', RED, WHITE, 70), 540, 260, 1 + 1.0 * (1 - eo(p)), -4, clamp(p * 4))
        if t > at(10, 'Brokerage', -0.2): place(c, text_img('Brokerage views can be wrong', 'osw', 44, WHITE), 540, 380)
    if i == 11:
        tf = at(11, 'Follow', -0.1)
        if t > tf: place(c, follow_btn(), 540, 300, 0.6 + 0.4 * eback(prog(t, tf, 0.35)), 2)
    caption(c, t, i)
    place(c, text_img('Source: HSBC & Citi views via Business Standard/Reuters (9 Nov 2026); Nifty via Goodreturns (10 Nov 2026)', 'osw5', 21, (150, 160, 190)), 540, 1830)
    place(c, text_img('Not a buy/sell call · Education only · @moneyincloud', 'osw5', 24, (200, 205, 220)), 540, 1880)
    return c


def render(t):
    LOOP = 0.5
    if t > DUR - LOOP:
        a = np.asarray(_render(t).convert('RGB')).astype(float); b = np.asarray(_render(1.6).convert('RGB')).astype(float)
        q = eio((t - (DUR - LOOP)) / LOOP)
        return (a * (1 - q) + b * q).astype(np.uint8)
    return np.asarray(_render(t).convert('RGB'))
