"""Retro ticket-style explainer: Diwali bonus engha poguthu? (Tamil narration from user's Sarvam audio).
Own mascot 'Cloudy', cloud-blue + gold on cream paper, monospace labels, one idea per screen."""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from lib import W, H, place, prog, eo, eio, eback, clamp

SH = ROOT + 'bonusexp_en/'
SCRIPT = [l['text'] for l in json.load(open(SH + 'lines.json'))]
_d = SH + 'vo/durs.json'
DURS = json.load(open(_d if _os.path.exists(_d) else SH + 'vo/durs_est.json'))
STARTS, VO = [], []
_t = 0.0
for i, d in enumerate(DURS):
    STARTS.append(_t); VO.append(_t + (0.15 if i == 0 else 0.12)); _t = VO[-1] + d + 0.2
DUR = _t + 1.2
B = STARTS[1:]

PAPER = (244, 236, 216); INK = (31, 45, 74); NAVY = (31, 58, 95); SKY = (126, 200, 242); GOLD = (242, 179, 61)
RED = (214, 73, 51); GRN = (46, 150, 90); MUTE = (120, 120, 120); CARD = (250, 244, 228)
MONO = ROOT + 'brand/DejaVuSansMono-Bold.ttf'; POP = ROOT + 'brand/Poppins-Bold.ttf'
TAM = ROOT + 'bonusexp/fonts/NotoSansTamil-700.ttf'


@functools.lru_cache(None)
def F(path, size):
    return ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)


def at(i, frac):
    return VO[i] + DURS[i] * frac


def line_at(t):
    i = 0
    for k, s in enumerate(STARTS):
        if t >= s: i = k
    return i


def txt(s, size, col=INK, font=MONO):
    f = F(font, size)
    l, tp, r, b = f.getbbox(s)
    im = Image.new('RGBA', (r - l + 8, b - tp + 8), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((4 - l, 4 - tp), s, font=f, fill=col)
    return im


def is_tamil(ch): return '஀' <= ch <= '௿'


def mixed(s, size, col=INK):
    """Tamil runs in Noto Sans Tamil, everything else in Poppins."""
    runs, cur, mode = [], '', None
    for ch in s:
        m = is_tamil(ch) if ch.strip() else mode
        if mode is None or m == mode: cur += ch; mode = m
        else: runs.append((cur, mode)); cur, mode = ch, m
    if cur: runs.append((cur, mode))
    ims = [txt(r, size, col, TAM if m else POP) for r, m in runs]
    w = sum(i.size[0] - 8 for i in ims) + 8; h = max(i.size[1] for i in ims)
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0)); x = 0
    for i in ims: out.alpha_composite(i, (x, (h - i.size[1]) // 2)); x += i.size[0] - 8
    return out


@functools.lru_cache(None)
def paper():
    rng = np.random.default_rng(3)
    a = np.full((H, W, 3), PAPER, np.float32)
    a += rng.normal(0, 5, (H, W, 1))
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA')
    d = ImageDraw.Draw(im)
    for y in range(0, H, 44): d.line((0, y, W, y), fill=(236, 226, 202), width=1)
    # faint watermark logos
    for y in range(120, H, 260):
        for x in range(-60 + (y // 260 % 2) * 180, W, 360):
            im.alpha_composite(txt('moneyincloud', 22, (232, 220, 194)), (x, y))
    return im


def header(c):
    cloud_icon(c, 70, 72, 0.32)
    c.alpha_composite(txt('moneyincloud · MONEY, SIMPLE', 24, INK), (104, 58))


def label(c, s, y=150, col=SKY, t=None, t0=0):
    a = clamp((t - t0) * 4) if t is not None else 1
    im = txt(s, 30, (60, 140, 190))
    if a < 1: im.putalpha(im.getchannel('A').point(lambda v: int(v * a)))
    c.alpha_composite(im, (70, y))


def title(c, s, y=200, size=74, t=None, t0=0, col=INK):
    """typewriter reveal"""
    n = len(s) if t is None else int(clamp((t - t0) / 0.6) * len(s))
    if n <= 0: return
    c.alpha_composite(txt(s[:n], size, col), (70, y))


# ---------- Cloudy the mascot ----------
def cloud_icon(c, x, y, s):
    d = ImageDraw.Draw(c)
    for (ox, oy, r) in [(-48, 12, 38), (0, -14, 52), (50, 10, 40)]:
        d.ellipse((x + (ox - r - 6) * s, y + (oy - r - 6) * s, x + (ox + r + 6) * s, y + (oy + r + 6) * s), fill=INK)
    d.rounded_rectangle((x - 86 * s, y + 6 * s, x + 90 * s, y + 52 * s), int(22 * s), fill=INK)
    for (ox, oy, r) in [(-48, 12, 38), (0, -14, 52), (50, 10, 40)]:
        d.ellipse((x + (ox - r) * s, y + (oy - r) * s, x + (ox + r) * s, y + (oy + r) * s), fill=(255, 255, 255))
    d.rounded_rectangle((x - 80 * s, y + 10 * s, x + 84 * s, y + 46 * s), int(18 * s), fill=(255, 255, 255))


def cloudy(c, x, y, s, t, mood='happy', wave=False):
    y += math.sin(t * 3) * 6 * s
    cloud_icon(c, x, y, s)
    d = ImageDraw.Draw(c)
    blink = (t % 3.2) < 0.12
    for ex in (-26, 26):
        if blink: d.line((x + (ex - 10) * s, y + 4 * s, x + (ex + 10) * s, y + 4 * s), fill=INK, width=max(2, int(5 * s)))
        else: d.ellipse((x + (ex - 8) * s, y + (-8) * s, x + (ex + 8) * s, y + 12 * s), fill=INK)
    d.ellipse((x - 52 * s, y + 14 * s, x - 36 * s, y + 24 * s), fill=(255, 160, 160))
    d.ellipse((x + 36 * s, y + 14 * s, x + 52 * s, y + 24 * s), fill=(255, 160, 160))
    if mood == 'happy': d.arc((x - 16 * s, y + 8 * s, x + 16 * s, y + 32 * s), 20, 160, fill=INK, width=max(2, int(5 * s)))
    elif mood == 'wow': d.ellipse((x - 9 * s, y + 14 * s, x + 9 * s, y + 34 * s), fill=INK)
    else: d.arc((x - 16 * s, y + 22 * s, x + 16 * s, y + 46 * s), 200, 340, fill=INK, width=max(2, int(5 * s)))
    c.alpha_composite(txt('₹', int(30 * s), GOLD, POP), (int(x - 10 * s), int(y + 30 * s)))
    if wave:
        a = math.sin(t * 9) * 0.5
        hx, hy = x + 90 * s, y + 10 * s
        d.line((hx, hy, hx + 40 * s * math.cos(-1.0 + a), hy + 40 * s * math.sin(-1.0 + a)), fill=INK, width=max(3, int(8 * s)))


# ---------- props ----------
def train(c, x, y, s, t, moving=True):
    d = ImageDraw.Draw(c)
    # coaches
    for k in range(2):
        cx0 = x + (230 + k * 330) * s
        d.rounded_rectangle((cx0, y - 150 * s, cx0 + 310 * s, y), int(26 * s), fill=SKY, outline=INK, width=max(3, int(6 * s)))
        for w in range(4):
            wx = cx0 + (24 + w * 70) * s
            d.rounded_rectangle((wx, y - 124 * s, wx + 52 * s, y - 80 * s), int(8 * s), fill=(255, 240, 190) if (w + k) % 2 else (255, 225, 150), outline=INK, width=3)
        d.rectangle((cx0 + 6 * s, y - 62 * s, cx0 + 304 * s, y - 46 * s), fill=GOLD)
    # engine
    d.rounded_rectangle((x, y - 170 * s, x + 220 * s, y), int(30 * s), fill=NAVY, outline=INK, width=max(3, int(6 * s)))
    d.rounded_rectangle((x + 120 * s, y - 230 * s, x + 210 * s, y - 160 * s), int(12 * s), fill=NAVY, outline=INK, width=max(3, int(6 * s)))
    d.rounded_rectangle((x + 136 * s, y - 214 * s, x + 194 * s, y - 176 * s), int(8 * s), fill=(255, 225, 150))
    d.rectangle((x + 30 * s, y - 230 * s, x + 64 * s, y - 170 * s), fill=INK)
    d.rectangle((x + 6 * s, y - 70 * s, x + 214 * s, y - 52 * s), fill=GOLD)
    d.ellipse((x - 18 * s, y - 120 * s, x + 18 * s, y - 84 * s), fill=(255, 236, 140), outline=INK, width=3)
    lab = txt('BONUS EXPRESS', int(26 * s), INK)
    c.alpha_composite(lab, (int(x + 240 * s), int(y - 46 * s)))
    # wheels
    for wx in [50, 170, 280, 470, 610, 800]:
        cx, cy, r = x + wx * s, y + 8 * s, 30 * s
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=INK)
        d.ellipse((cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55), fill=(200, 200, 210))
        a = t * (8 if moving else 0)
        d.line((cx + r * 0.5 * math.cos(a), cy + r * 0.5 * math.sin(a), cx - r * 0.5 * math.cos(a), cy - r * 0.5 * math.sin(a)), fill=INK, width=4)
    # smoke
    for k in range(4):
        ph = (t * 0.8 + k * 0.25) % 1
        r = (14 + 30 * ph) * s
        sx, sy = x + 47 * s - ph * 120 * s, y - 250 * s - ph * 160 * s
        d.ellipse((sx - r, sy - r, sx + r, sy + r), fill=(255, 255, 255, int(220 * (1 - ph))), outline=(200, 200, 210))


def night_panel(c, t, y0=430, h=520):
    x0, x1 = 60, W - 60
    pan = Image.new('RGBA', (x1 - x0, h), (0, 0, 0, 0)); d = ImageDraw.Draw(pan)
    d.rounded_rectangle((0, 0, x1 - x0 - 1, h - 1), 26, fill=(28, 44, 70), outline=INK, width=8)
    for k in range(14):
        lx = 40 + k * 68; ly = 70 + 22 * math.sin(k * 0.9)
        on = 0.6 + 0.4 * math.sin(t * 4 + k)
        d.ellipse((lx - 7, ly - 7, lx + 7, ly + 7), fill=(255, int(200 * on + 40), 90))
    d.line([(40 + k * 68, 70 + 22 * math.sin(k * 0.9)) for k in range(14)], fill=(90, 90, 110), width=2)
    d.ellipse((780, 110, 860, 190), fill=(255, 246, 210)); d.ellipse((805, 100, 885, 180), fill=(28, 44, 70))
    for k in range(5):  # diyas
        dx = 80 + k * 190
        d.chord((dx - 30, h - 92, dx + 30, h - 50), 0, 180, fill=(190, 100, 40))
        fl = 1 + 0.15 * math.sin(t * 12 + k)
        d.ellipse((dx - 8, h - 112 * fl, dx + 8, h - 86), fill=(255, 200, 60))
    d.rectangle((0, h - 50, x1 - x0, h - 44), fill=(200, 180, 120))
    c.alpha_composite(pan, (x0, y0))
    return x0, y0, h


@functools.lru_cache(None)
def ticket_img(to_text, to_col, struck=None):
    w, h = 900, 300
    im = Image.new('RGBA', (w + 14, h + 14), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((14, 14, w + 13, h + 13), fill=(0, 0, 0, 60))
    d.rectangle((0, 0, w - 1, h - 1), fill=CARD, outline=(200, 186, 150), width=3)
    d.rectangle((0, 0, w, 60), fill=NAVY)
    im.alpha_composite(txt('BONUS EXPRESS', 30, (255, 255, 255)), (24, 12)); im.alpha_composite(txt('No. 1111', 30, (255, 255, 255)), (w - 200, 12))
    im.alpha_composite(txt('FROM', 22, MUTE), (40, 90)); im.alpha_composite(txt('TO', 22, MUTE), (w - 330, 90))
    im.alpha_composite(txt('Diwali Bonus', 44, INK), (40, 120))
    im.alpha_composite(txt('- - - >', 40, MUTE), (380, 122))
    if struck:
        s = txt(struck, 44, MUTE); im.alpha_composite(s, (w - 330, 120))
        ImageDraw.Draw(im).line((w - 330, 150, w - 330 + s.size[0], 146), fill=RED, width=6)
        im.alpha_composite(txt(to_text, 54, to_col), (w - 330, 176))
    else:
        im.alpha_composite(txt(to_text, 60, to_col), (w - 330, 112))
    im.alpha_composite(txt('Date  11 NOV', 22, MUTE), (40, 210)); im.alpha_composite(txt('Class  SMART', 22, MUTE), (40, 244))
    for k in range(18): d.ellipse((w - 18 - 6, 70 + k * 12, w - 18 + 6, 70 + k * 12 + 6), fill=(220, 206, 170))
    return im


def stamp(c, s, col, cx, cy, t, t0, rot=-8, size=60):
    if t < t0: return
    p = prog(t, t0, 0.22)
    im = txt(s, size, col)
    w, h = im.size
    box = Image.new('RGBA', (w + 40, h + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(box)
    d.rounded_rectangle((3, 3, w + 36, h + 26), 10, outline=col, width=6)
    box.alpha_composite(im, (20, 15))
    place(c, box, cx, cy, 1 + 1.2 * (1 - eo(p)), rot, clamp(p * 4))


def item_card(name, price, kind):
    w, h = 260, 300
    im = Image.new('RGBA', (w + 12, h + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((12, 12, w + 11, h + 11), 22, fill=(0, 0, 0, 60))
    d.rounded_rectangle((0, 0, w - 1, h - 1), 22, fill=CARD, outline=INK, width=5)
    cx, cy = w / 2, 120
    if kind == 'phone':
        d.rounded_rectangle((cx - 50, cy - 80, cx + 50, cy + 80), 16, fill=INK); d.rounded_rectangle((cx - 40, cy - 66, cx + 40, cy + 62), 8, fill=SKY)
    elif kind == 'coin':
        d.ellipse((cx - 70, cy - 70, cx + 70, cy + 70), fill=GOLD, outline=INK, width=6); im.alpha_composite(txt('₹', 70, INK, POP), (int(cx - 22), int(cy - 52)))
    else:
        d.rounded_rectangle((cx - 90, cy - 50, cx + 90, cy + 50), 12, fill=(255, 255, 255), outline=INK, width=5)
        d.polygon([(cx - 30, cy), (cx + 40, cy - 20), (cx + 46, cy - 10), (cx - 10, cy + 6)], fill=SKY)
        d.line((cx - 90, cy + 20, cx + 90, cy + 20), fill=INK, width=3)
    t1 = txt(name, 30, INK); im.alpha_composite(t1, (int(w / 2 - t1.size[0] / 2), 220))
    t2 = txt(price, 30, RED); im.alpha_composite(t2, (int(w / 2 - t2.size[0] / 2), 256))
    return im


def stop_card(n, ttl, sub, col, icon):
    w, h = 700, 230
    im = Image.new('RGBA', (w + 12, h + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((12, 12, w + 11, h + 11), 18, fill=(0, 0, 0, 60))
    d.rounded_rectangle((0, 0, w - 1, h - 1), 18, fill=CARD, outline=INK, width=5)
    d.rectangle((0, 0, w, 48), fill=col)
    im.alpha_composite(txt(n, 26, (255, 255, 255)), (20, 8))
    cx, cy = 80, 138
    if icon == 'shield':
        d.polygon([(cx, cy - 46), (cx + 40, cy - 30), (cx + 34, cy + 20), (cx, cy + 46), (cx - 34, cy + 20), (cx - 40, cy - 30)], fill=SKY, outline=INK, width=4)
        d.line((cx - 14, cy, cx - 2, cy + 14, cx + 18, cy - 12), fill=INK, width=6)
    elif icon == 'card':
        d.rounded_rectangle((cx - 50, cy - 32, cx + 50, cy + 32), 8, fill=RED, outline=INK, width=4); d.rectangle((cx - 50, cy - 18, cx + 50, cy - 6), fill=INK)
    elif icon == 'plant':
        d.rectangle((cx - 26, cy + 10, cx + 26, cy + 44), fill=(196, 92, 48), outline=INK, width=4)
        d.line((cx, cy + 10, cx, cy - 34), fill=GRN, width=6); d.ellipse((cx - 34, cy - 40, cx, cy - 18), fill=GRN); d.ellipse((cx, cy - 50, cx + 34, cy - 28), fill=GRN)
    else:
        for k in range(10):
            a = k * 0.63; d.rectangle((cx + 40 * math.cos(a) - 6, cy + 40 * math.sin(a) - 6, cx + 40 * math.cos(a) + 6, cy + 40 * math.sin(a) + 6),
                                      fill=[GOLD, RED, SKY, GRN][k % 4])
        im.alpha_composite(txt('%', 46, INK), (int(cx - 16), int(cy - 30)))
    im.alpha_composite(txt(ttl, 46, INK), (150, 74)); im.alpha_composite(txt(sub, 30, MUTE), (150, 140))
    return im


STOPS = [(4, 'STOP 1', 'EMERGENCY FUND', '3-6 months of expenses', SKY, 'shield'),
         (5, 'STOP 2', 'CREDIT CARD DEBT', 'up to 3.75%/mo = ~45%/yr', RED, 'card'),
         (6, 'STOP 3', 'SIP', 'for your goal', GRN, 'plant'),
         (7, 'LAST STOP', '10% FOR YOU', 'enjoy, guilt-free', GOLD, 'party')]


def route(c, t, i):
    d = ImageDraw.Draw(c)
    x = 150; ys = [520, 860, 1200, 1540]
    for k in range(3):
        for yy in range(ys[k] + 30, ys[k + 1] - 30, 30):
            d.line((x, yy, x, yy + 14), fill=(60, 140, 190), width=8)
    cur = [s[0] for s in STOPS].index(i) if i in [s[0] for s in STOPS] else 3
    for k, (li, n, ttl, sub, col, icon) in enumerate(STOPS):
        y = ys[k]
        reached = k <= cur
        d.ellipse((x - 26, y - 26, x + 26, y + 26), fill=(255, 255, 255), outline=INK, width=6)
        if reached: d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=col)
        if k < cur or (k == cur and t > STARTS[li] + 0.3):
            p = prog(t, STARTS[li] + 0.3, 0.4) if k == cur else 1
            card = stop_card(n, ttl, sub, col, icon)
            if k < cur: card.putalpha(card.getchannel('A').point(lambda v: int(v * 0.45)))
            place(c, card, x + 60 + card.size[0] / 2 + (1 - eo(p)) * 300, y, 1, 0, clamp(p * 3))
    # mini train moving between stops
    st = STARTS[STOPS[cur][0]]
    y_from = ys[max(0, cur - 1)] if cur > 0 else ys[0] - 120
    yy = y_from + (ys[cur] - y_from) * eio(prog(t, st, 0.6))
    d.rounded_rectangle((x - 30, yy - 70, x + 30, yy - 30), 10, fill=NAVY, outline=INK, width=4)
    if i == 5: stamp(c, 'PAY OFF FIRST', RED, 640, 1060, t, at(5, 0.85), -8, 56)
    if i == 7:
        rng = random.Random(int(t * 10))
        for k in range(40):
            ph = ((t - STARTS[7]) * 0.6 + k / 40) % 1
            cx = (k * 97) % W; cy = ph * H
            d.rectangle((cx - 8, cy - 8, cx + 8, cy + 8), fill=[GOLD, RED, SKY, GRN][k % 4])


def comment_box(c, t, t0):
    d = ImageDraw.Draw(c)
    x0, y0, x1, y1 = 110, 880, 970, 990
    d.rounded_rectangle((x0, y0, x1, y1), 50, fill=(255, 255, 255), outline=INK, width=6)
    d.ellipse((x0 + 20, y0 + 22, x0 + 76, y0 + 78), fill=GOLD, outline=INK, width=4)
    n = int(clamp((t - t0) / 0.8) * 4)
    c.alpha_composite(txt('PLAN'[:n] + ('|' if (t * 2) % 1 < 0.5 else ''), 44, INK), (x0 + 100, y0 + 24))
    if n >= 4:
        p = 1 + 0.12 * math.sin((t - t0) * 10)
        r = 34 * p; cx, cy = x1 - 60, (y0 + y1) / 2
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=GRN, outline=INK, width=4)
        d.polygon([(cx - 12, cy - 16), (cx + 18, cy), (cx - 12, cy + 16)], fill=(255, 255, 255))


def _render(t):
    i = line_at(t)
    c = paper().copy()
    header(c)
    st = STARTS[i]
    if i in (0, 1):
        label(c, 'AFTER DIWALI')
        title(c, 'Bonus arrived', t=t, t0=0.1 if i == 0 else -9)
        x0, y0, h = night_panel(c, t)
        tx = 1100 - 1000 * eo(prog(t, 0.2, 2.4))
        clip = Image.new('RGBA', c.size, (0, 0, 0, 0)); train(clip, tx, y0 + h - 60, 0.95, t, moving=t < 2.6)
        mask = Image.new('L', c.size, 0); ImageDraw.Draw(mask).rounded_rectangle((68, y0 + 8, W - 68, y0 + h - 8), 20, fill=255)
        clip.putalpha(Image.fromarray(np.minimum(np.asarray(clip.getchannel('A')), np.asarray(mask))))
        c.alpha_composite(clip)
        cloudy(c, 300, y0 + 200, 0.8, t, 'happy', wave=True)
        if i == 0: cloudy(c, 540, 1380, 1.7, t, 'happy', wave=True)
        if i == 1:
            p = prog(t, st + 0.1, 0.5)
            place(c, ticket_img('?', RED), 540, 1300 + (1 - eo(p)) * 500, 1.05, -2)
            stamp(c, 'WHERE?', RED, 820, 1180, t, at(1, 0.75), 10, 64)
    elif i == 2:
        label(c, 'MOST OF US'); title(c, 'Gone in a week', t=t, t0=st + 0.05)
        items = [('New phone', '-Rs 20,000', 'phone', 0.25), ('Gold coin', '-Rs 15,000', 'coin', 0.38), ('Trip', '-Rs 15,000', 'trip', 0.5)]
        for k, (n, pr, kd, f) in enumerate(items):
            tk = at(2, f)
            if t < tk: continue
            p = prog(t, tk, 0.35)
            place(c, item_card(n, pr, kd), 200 + k * 340, 560, 0.5 + 0.5 * eback(p), [-4, 3, -2][k])
        # bonus bar draining
        left = 1 - 0.333 * sum(1 for (_, _, _, f) in items if t > at(2, f) + 0.2)
        if t > at(2, 0.85): left = 0
        d = ImageDraw.Draw(c)
        c.alpha_composite(txt('BONUS LEFT', 30, MUTE), (110, 980))
        d.rounded_rectangle((110, 1030, 970, 1100), 35, fill=CARD, outline=INK, width=6)
        if left > 0: d.rounded_rectangle((120, 1040, 120 + 840 * left, 1090), 28, fill=GOLD)
        stamp(c, 'EMPTY', RED, 760, 1240, t, at(2, 0.88), -10, 70)
        cloudy(c, 540, 1480, 1.7, t, 'sad')
    elif i == 3:
        label(c, 'THIS YEAR'); title(c, 'Book a better ticket', t=t, t0=st + 0.05, size=58)
        reb = t > at(3, 0.55)
        place(c, ticket_img('WEALTH', GRN, '?') if reb else ticket_img('?', RED), 540, 600, 1.05, -2)
        if reb: stamp(c, 'CONFIRMED', GRN, 760, 840, t, at(3, 0.55), -8, 60)
        cloudy(c, 540, 1330, 1.9, t, 'wow' if reb else 'happy', wave=reb)
    elif 4 <= i <= 7:
        label(c, 'YOUR ROUTE'); title(c, 'Bonus Express', t=None)
        route(c, t, i)
        cloudy(c, 900, 1730, 0.7, t, 'happy', wave=(i == 7))
    elif i == 8:
        label(c, 'WANT THE CHECKLIST?')
        place(c, ticket_img('PLAN', RED), 540, 560, 1.05, -2)
        comment_box(c, t, at(8, 0.45))
        cloudy(c, 540, 1420, 1.8, t, 'wow')
    else:
        label(c, 'NEXT TRIP')
        d = ImageDraw.Draw(c)
        d.rounded_rectangle((140, 380, 940, 1220), 30, fill=CARD, outline=INK, width=6)
        d.rectangle((140, 380, 940, 450), fill=NAVY)
        c.alpha_composite(txt('BONUS EXPRESS · NEXT TRIP', 28, (255, 255, 255)), (180, 398))
        cloudy(c, 540, 640, 1.3, t, 'happy', wave=True)
        place(c, txt('moneyincloud', 64, INK), 540, 860)
        place(c, txt('Money, made simple', 32, MUTE), 540, 940)
        fol = t > at(9, 0.75)
        bw = 300; d.rounded_rectangle((540 - bw / 2, 1020, 540 + bw / 2, 1110), 45, fill=RED if fol else (255, 255, 255), outline=INK, width=5)
        place(c, txt('Following' if fol else 'Follow', 40, (255, 255, 255) if fol else INK), 540, 1065)
    place(c, txt('Not a buy/sell call · Education only', 22, MUTE), 540, 1860)
    return c


def render(t):
    LOOP = 0.5
    if t > DUR - LOOP:
        a = np.asarray(_render(t).convert('RGB')).astype(float); b = np.asarray(_render(1.4).convert('RGB')).astype(float)
        q = eio((t - (DUR - LOOP)) / LOOP)
        return (a * (1 - q) + b * q).astype(np.uint8)
    for b in B:
        if b - 0.15 <= t < b:
            a = np.asarray(_render(t).convert('RGB')).astype(float); bb = np.asarray(_render(b + 0.01).convert('RGB')).astype(float)
            q = (t - (b - 0.15)) / 0.15
            return (a * (1 - q) + bb * q).astype(np.uint8)
    return np.asarray(_render(t).convert('RGB'))
