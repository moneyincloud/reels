"""Original paper-cutout animal characters for "Animal Friday" reels (moneyincloud paper Vox style).
tortoise(mood, step, scale) - side view, walking right.  hare(mood, pose, step, scale) - front view, red tracksuit.
Moods use paperchars._face: calm happy sad cry angry wow. All results cached RGBA with a soft paper shadow."""
import math, functools
from PIL import Image, ImageDraw
from lib import INK, CREAM, YEL, RED, GRN
from paperchars import _face, shadowed, OUT

SHELL = (96, 140, 70); SHELL_D = (70, 108, 50); SCUTE = (196, 170, 96); SKIN_T = (150, 182, 104)
FUR = (206, 150, 92); FUR_L = (246, 228, 200); PINKI = (240, 160, 170); SUIT = (214, 52, 48)


@functools.lru_cache(maxsize=64)
def tortoise(mood='calm', step=0, scale=1.0, shades=False):
    W_, H_ = 600, 420; im = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    ph = step % 4
    # legs (back pair darker), walking phase lifts alternate legs
    for k, (x, back) in enumerate(((140, True), (330, True), (110, False), (300, False))):
        lift = 18 if (k + ph) % 2 == 0 and ph in (1, 3) else 0
        sw = (-12 if ph == 1 else 12 if ph == 3 else 0) * (1 if k % 2 else -1)
        col = SKIN_T if not back else (128, 160, 88)
        d.rounded_rectangle((x + sw, 270 - lift, x + 70 + sw, 380 - lift), 26, fill=col, outline=INK, width=OUT)
        for j in range(3): d.ellipse((x + sw + 8 + j * 20, 360 - lift, x + sw + 24 + j * 20, 376 - lift), fill=CREAM, outline=INK, width=3)
    # tail
    d.polygon([(70, 270), (30, 300), (78, 300)], fill=SKIN_T, outline=INK); d.line([(70, 270), (30, 300), (78, 300)], fill=INK, width=5)
    # shell dome + rim
    d.chord((60, 40, 440, 420), 180, 360, fill=SHELL, outline=INK, width=OUT)
    d.rounded_rectangle((52, 214, 448, 262), 22, fill=SCUTE, outline=INK, width=OUT)
    for x in range(92, 440, 62): d.line((x, 220, x - 10, 256), fill=(150, 126, 64), width=4)
    # scutes (hex-ish plates)
    for (cx, cy, rr) in ((250, 120, 58), (140, 170, 40), (360, 170, 40), (190, 85, 30), (310, 85, 30)):
        pts = [(cx + rr * math.cos(math.radians(a)), cy + rr * 0.8 * math.sin(math.radians(a))) for a in range(0, 360, 60)]
        d.polygon(pts, fill=SCUTE); d.line(pts + [pts[0]], fill=SHELL_D, width=6)
    d.arc((90, 70, 410, 380), 200, 250, fill=(150, 190, 120), width=8)
    # neck + head
    d.rounded_rectangle((400, 180, 490, 280), 40, fill=SKIN_T, outline=INK, width=OUT)
    hx, hy, r = 498, 150, 92
    d.ellipse((hx - r, hy - r, hx + r, hy + r), fill=SKIN_T, outline=INK, width=OUT)
    _face(d, hx + 6, hy + 4, r, mood)
    if shades:
        for s in (-1, 1): d.rounded_rectangle((hx + 6 + s * 32 - 30, hy - 22, hx + 6 + s * 32 + 30, hy + 16), 10, fill=INK)
        d.line((hx - 22, hy - 10, hx + 34, hy - 10), fill=INK, width=6)
    if mood == 'cry':
        for s in (-1, 1): d.ellipse((hx + 6 + s * 32 - 8, hy + 22, hx + 6 + s * 32 + 8, hy + 46), fill=(120, 190, 240), outline=INK, width=3)
    if scale != 1.0: im = im.resize((int(W_ * scale), int(H_ * scale)), Image.LANCZOS)
    return shadowed(im)


@functools.lru_cache(maxsize=96)
def hare(mood='calm', pose='down', step=0, scale=1.0):
    W_, H_ = 420, 820; im = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx = W_ // 2; ph = step % 4
    # ears (own taller layer behind the body)
    EY = 110; ears = Image.new('RGBA', (W_, H_ + EY), (0, 0, 0, 0)); de = ImageDraw.Draw(ears)
    tilt = {'sad': 32, 'cry': 38}.get(mood, 10)
    for s in (-1, 1):
        a = math.radians(-90 + s * tilt); bx, by = cx + s * 50, 160 + EY
        ux, uy = math.cos(a), math.sin(a); vx, vy = -uy, ux
        def ell(L, Wd, off):
            return [(bx + ux * (off + L * math.cos(q)) + vx * Wd * math.sin(q), by + uy * (off + L * math.cos(q)) + vy * Wd * math.sin(q)) for q in [k * math.pi / 24 for k in range(48)]]
        o = ell(105, 40, 95); de.polygon(o, fill=FUR); de.line(o + [o[0]], fill=INK, width=OUT)
        de.polygon(ell(80, 20, 100), fill=PINKI)
    # legs + big feet (walking phase)
    for s in (-1, 1):
        lift = 22 if ((s == -1 and ph == 1) or (s == 1 and ph == 3)) else 0
        d.rounded_rectangle((cx + s * 48 - 34, 560 - lift, cx + s * 48 + 34, 740 - lift), 22, fill=SUIT, outline=INK, width=OUT)
        d.line((cx + s * 48 - 30, 600 - lift, cx + s * 48 - 30, 720 - lift), fill=CREAM, width=8)
        d.rounded_rectangle((cx + s * 56 - 62, 720 - lift, cx + s * 56 + 56, 780 - lift), 28, fill=CREAM, outline=INK, width=OUT)
        d.line((cx + s * 56 - 40, 740 - lift, cx + s * 56 + 30, 740 - lift), fill=RED, width=6)
    # torso: tracksuit jacket + white belly + zip
    d.rounded_rectangle((cx - 96, 330, cx + 96, 600), 66, fill=SUIT, outline=INK, width=OUT)
    d.rounded_rectangle((cx - 46, 360, cx + 46, 560), 40, fill=FUR_L, outline=INK, width=5)
    d.line((cx, 345, cx, 590), fill=INK, width=4)
    # arms
    for s in (-1, 1):
        if pose == 'both_up' or (pose == 'up' and s == 1):
            pts = [(cx + s * 86, 370), (cx + s * 160, 250)]; hand = (cx + s * 168, 226)
        elif pose == 'head':
            pts = [(cx + s * 86, 370), (cx + s * 130, 270)]; hand = (cx + s * 104, 222)
        elif pose == 'point' and s == 1:
            pts = [(cx + s * 86, 370), (cx + s * 180, 360)]; hand = (cx + s * 196, 356)
        elif pose == 'hips':
            pts = [(cx + s * 86, 370), (cx + s * 140, 450)]; hand = (cx + s * 100, 500)
        else:
            sw = (14 if ph == 1 else -14 if ph == 3 else 0) * s
            pts = [(cx + s * 86, 370), (cx + s * 108 + sw, 500)]; hand = (cx + s * 110 + sw, 524)
        d.line(pts + [hand], fill=INK, width=48); d.line(pts + [hand], fill=SUIT, width=34)
        d.ellipse((hand[0] - 26, hand[1] - 26, hand[0] + 26, hand[1] + 26), fill=FUR, outline=INK, width=6)
    # head
    r = 112; hy = 228
    d.ellipse((cx - r, hy - r, cx + r, hy + r), fill=FUR, outline=INK, width=OUT)
    d.ellipse((cx - 62, hy + 18, cx + 62, hy + 104), fill=FUR_L)
    _face(d, cx, hy + 4, r, mood)
    d.polygon([(cx - 14, hy + 36), (cx + 14, hy + 36), (cx, hy + 52)], fill=(220, 90, 110), outline=INK)
    for s in (-1, 1):
        for k in (-1, 0, 1): d.line((cx + s * 40, hy + 52 + k * 10, cx + s * 120, hy + 44 + k * 22), fill=INK, width=3)
    if mood == 'cry':
        for s in (-1, 1): d.ellipse((cx + s * 39 - 9, hy + 26, cx + s * 39 + 9, hy + 52), fill=(120, 190, 240), outline=INK, width=3)
    ears.alpha_composite(im, (0, EY)); im = ears; H_ = H_ + EY
    if scale != 1.0: im = im.resize((int(W_ * scale), int(H_ * scale)), Image.LANCZOS)
    return shadowed(im)


@functools.lru_cache(maxsize=16)
def jar(level=0.0, label='SIP'):
    """coin jar, level 0..1 (quantise before calling)"""
    w, h = 220, 260; im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((20, 50, w - 20, h - 10), 40, fill=(225, 240, 245), outline=INK, width=6)
    top = h - 20 - int((h - 90) * level)
    if level > 0:
        d.rounded_rectangle((28, top, w - 28, h - 18), 30, fill=(214, 160, 40))
        for y in range(h - 30, top, -22): d.line((40, y, w - 40, y), fill=(170, 120, 20), width=3)
    d.rounded_rectangle((40, 20, w - 40, 56), 10, fill=(180, 120, 70), outline=INK, width=6)
    d.rectangle((90, 28, 130, 36), fill=INK)
    if label:
        from lib import text_img
        t = text_img(label, 'anton', 40, INK); im.alpha_composite(t, (w // 2 - t.size[0] // 2, 70))
    return im


@functools.lru_cache(maxsize=4)
def bag(txt='₹'):
    from lib import text_img
    w, h = 220, 240; im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((10, 60, w - 10, h - 6), fill=(196, 150, 90), outline=INK, width=6)
    d.polygon([(70, 70), (150, 70), (176, 14), (44, 14)], fill=(196, 150, 90), outline=INK)
    d.line([(70, 70), (150, 70), (176, 14), (44, 14), (70, 70)], fill=INK, width=6)
    d.line((64, 70, 156, 70), fill=RED, width=12)
    t = text_img(txt, 'anton', 90, INK); im.alpha_composite(t, (w // 2 - t.size[0] // 2, 110))
    return im


@functools.lru_cache(maxsize=4)
def finish_flag():
    w, h = 200, 300; im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((20, 10, 34, h - 4), fill=(120, 90, 60), outline=INK, width=4)
    for r_ in range(4):
        for c_ in range(5):
            col = INK if (r_ + c_) % 2 == 0 else CREAM
            d.rectangle((34 + c_ * 30, 14 + r_ * 28, 64 + c_ * 30, 42 + r_ * 28), fill=col)
    d.rectangle((34, 14, 184, 126), outline=INK, width=5)
    return im
