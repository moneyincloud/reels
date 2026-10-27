"""Paper-cutout 2D characters & props for story reels (moneyincloud paper Vox style).
All return RGBA images with ink outlines + a soft paper drop shadow. Cached."""
import math, functools
from PIL import Image, ImageDraw, ImageFilter
from lib import INK, CREAM, YEL, RED, GRN

SKIN = {'a': (214, 160, 120), 'b': (190, 135, 95), 'c': (170, 115, 80)}
OUT = 7


def shadowed(im, off=10, blur=8, alpha=70):
    w, h = im.size; S = Image.new('RGBA', (w + off * 2 + blur * 2, h + off * 2 + blur * 2), (0, 0, 0, 0))
    sh = Image.new('RGBA', im.size, (40, 30, 20, 0)); sh.putalpha(im.getchannel('A').point(lambda v: v * alpha // 255))
    S.alpha_composite(sh, (blur + off, blur + off)); S = S.filter(ImageFilter.GaussianBlur(blur)); S.alpha_composite(im, (blur, blur)); return S


def _face(d, cx, cy, r, mood, mask=False, mustache=False, old=False, bindi=False):
    if mask:
        for s in (-1, 1): d.ellipse((cx + s * r * 0.35 - 20, cy - 12, cx + s * r * 0.35 + 20, cy + 6), fill=INK)
        return
    ey = cy - r * 0.05
    for s in (-1, 1):
        ex = cx + s * r * 0.35
        if mood == 'happy': d.arc((ex - 18, ey - 14, ex + 18, ey + 14), 200, 340, fill=INK, width=7)
        else: d.ellipse((ex - 11, ey - 14, ex + 11, ey + 12), fill=INK); d.ellipse((ex - 3, ey - 10, ex + 4, ey - 3), fill=(255, 255, 255))
        by = ey - 34
        if mood in ('sad', 'cry'): d.line((ex - s * 22, by + 2, ex + s * 18, by - 12), fill=INK, width=7)
        elif mood == 'angry': d.line((ex - s * 22, by - 12, ex + s * 18, by + 4), fill=INK, width=8)
        elif mood == 'wow': d.arc((ex - 20, by - 18, ex + 20, by + 6), 200, 340, fill=INK, width=6)
        else: d.line((ex - 18, by - 4, ex + 18, by - 4), fill=INK, width=6)
        d.ellipse((ex - s * 6 - 18, ey + 22, ex - s * 6 + 18, ey + 38), fill=(240, 130, 130, 140))
    my = cy + r * 0.45
    if mood == 'happy': d.chord((cx - 34, my - 26, cx + 34, my + 22), 0, 180, fill=(140, 40, 40), outline=INK, width=5)
    elif mood == 'wow': d.ellipse((cx - 16, my - 14, cx + 16, my + 20), fill=(120, 30, 30), outline=INK, width=4)
    elif mood == 'angry': d.chord((cx - 34, my - 6, cx + 34, my + 30), 180, 360, fill=(120, 30, 30), outline=INK, width=5)
    else: d.arc((cx - 28, my - 4, cx + 28, my + 30), 200, 340, fill=INK, width=7)
    if mustache: d.chord((cx - 40, my - 30, cx + 40, my + 2), 180, 360, fill=(40, 30, 25))
    if old: d.line((cx - 40, cy - r * 0.62, cx - 10, cy - r * 0.66), fill=(120, 90, 70), width=4)
    if bindi: d.ellipse((cx - 8, cy - r * 0.5, cx + 8, cy - r * 0.5 + 16), fill=(200, 20, 30))


@functools.lru_cache(maxsize=256)
def person(kind='man', mood='calm', pose='down', skin='b', shirt=(240, 230, 210), pants=(70, 55, 45), mask=False,
           mustache=False, hair=(35, 25, 20), old=False, saree=False, kid=False, bag=False, scale=1.0):
    W_, H_ = 360, 720; im = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    sk = SKIN[skin]; cx = W_ // 2
    # legs / saree
    if saree:
        d.polygon([(cx - 95, 690), (cx + 95, 690), (cx + 70, 360), (cx - 70, 360)], fill=shirt, outline=INK)
        d.line([(cx - 95, 690), (cx + 95, 690), (cx + 70, 360), (cx - 70, 360), (cx - 95, 690)], fill=INK, width=OUT)
        d.line([(cx - 90, 660), (cx + 90, 660)], fill=YEL, width=14)
    else:
        for s in (-1, 1):
            d.rounded_rectangle((cx + s * 40 - 34, 450, cx + s * 40 + 34, 680), 20, fill=pants, outline=INK, width=OUT)
            d.rounded_rectangle((cx + s * 44 - 44, 660, cx + s * 44 + 40, 705), 18, fill=(60, 40, 30), outline=INK, width=OUT)
    if bag: d.rounded_rectangle((cx - 120, 280, cx + 10, 470), 30, fill=(70, 85, 95), outline=INK, width=OUT)
    # torso
    d.rounded_rectangle((cx - 88, 270, cx + 88, 490), 60, fill=shirt, outline=INK, width=OUT)
    if saree: d.polygon([(cx - 88, 300), (cx + 60, 480), (cx + 20, 490), (cx - 88, 340)], fill=(255, 200, 60))
    # arms
    for s in (-1, 1):
        if (pose == 'up' and s == 1) or pose == 'both_up':
            pts = [(cx + s * 80, 300), (cx + s * 150, 170)]; hand = (cx + s * 160, 150)
        elif pose == 'head':
            pts = [(cx + s * 80, 300), (cx + s * 120, 200)]; hand = (cx + s * 100, 160)
        elif pose == 'hug':
            pts = [(cx + s * 80, 300), (cx + s * 40, 380)]; hand = (cx - s * 10, 390)
        elif pose == 'wheel':
            pts = [(cx + s * 80, 300), (cx + s * 70, 400)]; hand = (cx + s * 50, 420)
        else:
            pts = [(cx + s * 80, 300), (cx + s * 100, 450)]; hand = (cx + s * 102, 470)
        d.line(pts + [hand], fill=INK, width=46); d.line(pts + [hand], fill=sk if saree else shirt, width=32)
        d.ellipse((hand[0] - 24, hand[1] - 24, hand[0] + 24, hand[1] + 24), fill=sk, outline=INK, width=6)
    # neck + head
    d.rectangle((cx - 22, 240, cx + 22, 285), fill=sk, outline=INK, width=6)
    r = 105; hy = 150
    head_col = (242, 242, 242) if mask else sk
    d.ellipse((cx - r, hy - r, cx + r, hy + r), fill=head_col, outline=INK, width=OUT)
    if not mask:
        for s in (-1, 1): d.ellipse((cx + s * r - 18, hy - 10, cx + s * r + 18, hy + 26), fill=sk, outline=INK, width=5)
        hc = (200, 200, 200) if old else hair
        d.chord((cx - r - 4, hy - r - 6, cx + r + 4, hy + r * 0.5), 180, 360, fill=hc, outline=INK, width=OUT)
        if saree: d.ellipse((cx - 40, hy - r - 50, cx + 40, hy - r + 20), fill=hc, outline=INK, width=6)
    else:
        d.ellipse((cx - 22, hy - r - 26, cx + 22, hy - r + 14), fill=(225, 225, 225), outline=INK, width=5)
    _face(d, cx, hy + 10, r, mood, mask, mustache, old, saree)
    if mood == 'cry':
        for s in (-1, 1): d.ellipse((cx + s * 36 - 9, hy + 40, cx + s * 36 + 9, hy + 66), fill=(120, 190, 240), outline=INK, width=3)
    if kid: im = im.resize((int(W_ * 0.7), int(H_ * 0.7)), Image.LANCZOS)
    if scale != 1.0: im = im.resize((int(im.size[0] * scale), int(im.size[1] * scale)), Image.LANCZOS)
    return shadowed(im)


@functools.lru_cache(maxsize=8)
def lorry(front=False):
    if front:
        im = Image.new('RGBA', (560, 560), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((60, 60, 500, 480), 40, fill=(245, 124, 0), outline=INK, width=OUT)
        d.rounded_rectangle((100, 110, 460, 270), 20, fill=(40, 55, 75), outline=INK, width=OUT)
        d.rectangle((60, 300, 500, 330), fill=(21, 101, 192))
        for x in (140, 420): d.ellipse((x - 40, 360, x + 40, 440), fill=(255, 250, 200), outline=INK, width=OUT)
        d.rounded_rectangle((180, 20, 380, 70), 12, fill=YEL, outline=INK, width=5)
        for x in (110, 450): d.rounded_rectangle((x - 40, 470, x + 40, 545), 16, fill=(30, 30, 30), outline=INK, width=OUT)
        return shadowed(im)
    im = Image.new('RGBA', (1100, 520), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((20, 60, 700, 400), 24, fill=(46, 125, 50), outline=INK, width=OUT)
    for x in range(120, 700, 140): d.line((x, 70, x, 390), fill=(30, 90, 35), width=6)
    d.rounded_rectangle((690, 140, 1060, 400), 40, fill=(245, 124, 0), outline=INK, width=OUT)
    d.polygon([(870, 160), (1030, 160), (1050, 260), (870, 260)], fill=(40, 55, 75), outline=INK); d.line([(870, 160), (1030, 160), (1050, 260), (870, 260), (870, 160)], fill=INK, width=6)
    d.rectangle((690, 300, 1060, 325), fill=(21, 101, 192))
    d.rectangle((20, 400, 1060, 430), fill=(40, 40, 40))
    for x in (160, 330, 880): d.ellipse((x - 70, 360, x + 70, 500), fill=(30, 30, 30), outline=INK, width=OUT); d.ellipse((x - 26, 404, x + 26, 456), fill=(180, 180, 180))
    d.ellipse((1030, 330, 1075, 370), fill=(255, 250, 200), outline=INK, width=4)
    return shadowed(im)


@functools.lru_cache(maxsize=8)
def tree(kind=0, s=1.0):
    im = Image.new('RGBA', (300, 460), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if kind == 0:
        d.rounded_rectangle((132, 230, 168, 450), 10, fill=(120, 80, 50), outline=INK, width=6)
        for (x, y, r) in ((150, 150, 110), (90, 200, 70), (210, 200, 70)): d.ellipse((x - r, y - r, x + r, y + r), fill=(76, 160, 70), outline=INK, width=6)
    else:
        d.line([(160, 450), (140, 300), (150, 120)], fill=INK, width=30); d.line([(160, 450), (140, 300), (150, 120)], fill=(140, 100, 60), width=18)
        for a in range(0, 360, 60):
            x2 = 150 + 120 * math.cos(math.radians(a)); y2 = 120 + 60 * math.sin(math.radians(a)) + 40
            d.line([(150, 120), (x2, y2)], fill=INK, width=24); d.line([(150, 120), (x2, y2)], fill=(56, 142, 60), width=14)
    if s != 1.0: im = im.resize((int(300 * s), int(460 * s)), Image.LANCZOS)
    return shadowed(im, 6, 6, 50)


@functools.lru_cache(maxsize=4)
def house():
    im = Image.new('RGBA', (900, 700), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((90, 300, 810, 660), fill=(243, 201, 139), outline=INK, width=OUT)
    d.polygon([(40, 320), (450, 60), (860, 320)], fill=(181, 83, 42), outline=INK); d.line([(40, 320), (450, 60), (860, 320), (40, 320)], fill=INK, width=OUT)
    for y in range(120, 320, 40): d.line((450 - (y - 60) * 1.58, y, 450 + (y - 60) * 1.58, y), fill=(150, 65, 30), width=4)
    d.rounded_rectangle((380, 430, 520, 660), 14, fill=(109, 76, 65), outline=INK, width=OUT)
    for x in (200, 700): d.rectangle((x - 70, 400, x + 70, 510), fill=(78, 127, 168), outline=INK, width=OUT); d.line((x, 400, x, 510), fill=INK, width=5)
    d.rectangle((60, 650, 840, 690), fill=(215, 204, 200), outline=INK, width=6)
    return shadowed(im)


@functools.lru_cache(maxsize=4)
def booth(sign_img=None):
    im = Image.new('RGBA', (520, 560), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((40, 200, 480, 540), 24, fill=(142, 36, 170), outline=INK, width=OUT)
    d.rounded_rectangle((90, 260, 430, 380), 16, fill=(60, 20, 80), outline=INK, width=6)
    d.rounded_rectangle((10, 40, 510, 190), 20, fill=YEL, outline=INK, width=OUT)
    return shadowed(im)


def coin_img(r=30):
    im = Image.new('RGBA', (r * 2 + 8, r * 2 + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((4, 4, r * 2 + 4, r * 2 + 4), fill=(255, 205, 64), outline=INK, width=5); d.ellipse((14, 14, r * 2 - 6, r * 2 - 6), outline=(200, 150, 30), width=3)
    return im
