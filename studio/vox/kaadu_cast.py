"""Kaadu Bank (Animal Friday series) fixed cast - original paper-cut characters. See studio/series/jungle_bank.md.
ammu(ant, orange scarf) mani(monkey, yellow cap) thatha(elephant, blue shawl) kili(parrot, green, phone)
aandhai(owl, round glasses) ponni(squirrel, pink bow). Moods: calm happy sad cry angry wow.
Props: grain(), grain_pile(n), bank() (the Kaadu Bank tree-trunk bank), ledger()."""
import math, functools
from PIL import Image, ImageDraw
from lib import INK, CREAM, YEL, RED, GRN
from paperchars import _face, shadowed, OUT
import animals as A

ORANGE = (238, 122, 32); ANT = (176, 70, 46); ANT_D = (130, 48, 32)
PGREEN = (70, 170, 80); PGREEN_D = (40, 120, 60); BEAK = (245, 180, 40)
OWL = (150, 110, 75); OWL_L = (236, 214, 176); SQ = (214, 130, 70); SQ_L = (248, 222, 190); PINK = (240, 110, 160)
GRAIN = (238, 200, 110)


def _scale(im, scale):
    if scale != 1.0: im = im.resize((int(im.size[0] * scale), int(im.size[1] * scale)), Image.LANCZOS)
    return shadowed(im)


def _grain(d, x, y, r=26, rot=0):
    d.ellipse((x - r, y - r * 0.7, x + r, y + r * 0.7), fill=GRAIN, outline=INK, width=5)
    d.arc((x - r * 0.6, y - r * 0.4, x + r * 0.6, y + r * 0.3), 200, 340, fill=(200, 150, 60), width=4)


@functools.lru_cache(maxsize=64)
def ammu(mood='happy', pose='down', step=0, scale=1.0):
    """Ammu the ant, front view, orange scarf. poses: down carry (grain over head) wave point"""
    W_, H_ = 440, 640; im = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im); cx = W_ // 2; ph = step % 4
    # legs (4 small legs + 2 feet)
    for s in (-1, 1):
        lift = 16 if ((s == -1 and ph == 1) or (s == 1 and ph == 3)) else 0
        pts = [(cx + s * 40, 470), (cx + s * 80, 540 - lift), (cx + s * 70, 600 - lift)]
        d.line(pts, fill=INK, width=24); d.line(pts, fill=ANT_D, width=12)
        d.ellipse((cx + s * 70 - 26, 588 - lift, cx + s * 70 + 26, 616 - lift), fill=ANT_D, outline=INK, width=5)
        d.line([(cx + s * 70, 420), (cx + s * 150, 450), (cx + s * 170, 500)], fill=INK, width=12)
    # abdomen + thorax
    d.ellipse((cx - 110, 380, cx + 110, 560), fill=ANT, outline=INK, width=OUT)
    d.arc((cx - 80, 420, cx + 80, 520), 20, 160, fill=ANT_D, width=6)
    d.ellipse((cx - 70, 300, cx + 70, 420), fill=ANT, outline=INK, width=OUT)
    # arms
    for s in (-1, 1):
        if pose == 'carry' or (pose == 'wave' and s == 1):
            pts = [(cx + s * 55, 340), (cx + s * 110, 260), (cx + s * 70, 160)]
        elif pose == 'point' and s == 1:
            pts = [(cx + s * 55, 340), (cx + s * 160, 330), (cx + s * 200, 320)]
        else:
            sw = (12 if ph == 1 else -12 if ph == 3 else 0) * s
            pts = [(cx + s * 60, 340), (cx + s * 110 + sw, 420), (cx + s * 100 + sw, 470)]
        d.line(pts, fill=INK, width=26); d.line(pts, fill=ANT_D, width=14)
        hx, hy = pts[-1]; d.ellipse((hx - 18, hy - 18, hx + 18, hy + 18), fill=ANT_D, outline=INK, width=5)
    # head + antennae
    hy, r = 200, 110
    for s in (-1, 1):
        a = [(cx + s * 40, hy - 90), (cx + s * 70, hy - 160), (cx + s * 120, hy - 175)]
        d.line(a, fill=INK, width=10); d.ellipse((a[-1][0] - 16, a[-1][1] - 16, a[-1][0] + 16, a[-1][1] + 16), fill=ORANGE, outline=INK, width=5)
    d.ellipse((cx - r, hy - r, cx + r, hy + r * 0.95), fill=ANT, outline=INK, width=OUT)
    d.ellipse((cx - 72, hy - 30, cx + 72, hy + 92), fill=(205, 105, 80))
    _face(d, cx, hy + 6, r, mood)
    # orange scarf
    sc = [(cx - 90, hy + 92), (cx + 90, hy + 92), (cx + 84, hy + 130), (cx - 84, hy + 130)]
    d.polygon(sc, fill=ORANGE); d.line(sc + [sc[0]], fill=INK, width=6)
    tail = [(cx + 40, hy + 120), (cx + 96, hy + 210), (cx + 50, hy + 220), (cx + 14, hy + 128)]
    d.polygon(tail, fill=ORANGE); d.line(tail + [tail[0]], fill=INK, width=6)
    for k in range(-2, 3): d.line((cx + k * 30, hy + 98, cx + k * 30, hy + 126), fill=(200, 90, 20), width=4)
    if pose == 'carry': _grain(d, cx, 120 - 40, 60)
    if mood == 'cry':
        for s in (-1, 1): d.ellipse((cx + s * 38 - 8, hy + 22, cx + s * 38 + 8, hy + 48), fill=(120, 190, 240), outline=INK, width=3)
    return _scale(im, scale)


@functools.lru_cache(maxsize=64)
def kili(mood='happy', open_beak=False, phone=True, flap=0, scale=1.0):
    """Kili the parrot, green, holding a phone"""
    W_, H_ = 460, 640; im = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im); cx = W_ // 2
    # tail feathers
    for k, col in ((-1, (40, 140, 200)), (0, RED), (1, PGREEN_D)):
        tp = [(cx + k * 18 - 20, 520), (cx + k * 40 - 10, 630), (cx + k * 40 + 20, 630), (cx + k * 18 + 20, 520)]
        d.polygon(tp, fill=col); d.line(tp + [tp[0]], fill=INK, width=5)
    d.ellipse((cx - 120, 250, cx + 120, 560), fill=PGREEN, outline=INK, width=OUT)
    d.ellipse((cx - 70, 320, cx + 70, 540), fill=(150, 210, 110))
    # wings (flap 0..1)
    for s in (-1, 1):
        a = -0.6 * flap
        wp = [(cx + s * 100, 300), (cx + s * (200 + 40 * flap), 340 - 160 * flap), (cx + s * 170, 470 - 60 * flap), (cx + s * 110, 480)]
        d.polygon(wp, fill=PGREEN_D); d.line(wp + [wp[0]], fill=INK, width=OUT, joint='curve')
    # feet
    for s in (-1, 1): d.line([(cx + s * 40, 550), (cx + s * 40, 590), (cx + s * 60, 600)], fill=(240, 150, 60), width=10)
    hy, r = 190, 110
    d.ellipse((cx - r, hy - r, cx + r, hy + r), fill=PGREEN, outline=INK, width=OUT)
    for k in (-1, 0, 1): d.polygon([(cx + k * 30 - 14, hy - r + 10), (cx + k * 34, hy - r - 50), (cx + k * 30 + 14, hy - r + 10)], fill=PGREEN, outline=INK)
    d.ellipse((cx - 80, hy - 40, cx + 80, hy + 60), fill=(220, 240, 200))
    _face(d, cx, hy - 10, r * 0.9, 'happy' if mood == 'happy' else mood)
    # beak covers mouth
    by = hy + 40
    d.chord((cx - 40, by - 30, cx + 40, by + 50), 180, 360, fill=BEAK, outline=INK, width=5)
    d.polygon([(cx - 36, by + 8), (cx + 36, by + 8), (cx, by + 54)], fill=BEAK, outline=INK)
    if open_beak: d.polygon([(cx - 26, by + 18), (cx + 26, by + 18), (cx, by + 70)], fill=(140, 40, 40), outline=INK)
    for s in (-1, 1): d.ellipse((cx + s * 70 - 14, hy + 20, cx + s * 70 + 14, hy + 44), fill=(240, 100, 90))
    if phone:
        px, py = cx + 140, 410
        d.rounded_rectangle((px - 44, py - 76, px + 44, py + 76), 14, fill=INK)
        d.rectangle((px - 34, py - 62, px + 34, py + 62), fill=(230, 245, 235))
        for k in range(3): d.rounded_rectangle((px - 26, py - 50 + k * 34, px + 26, py - 28 + k * 34), 6, fill=(120, 200, 120) if k % 2 == 0 else (200, 200, 200))
    return _scale(im, scale)


@functools.lru_cache(maxsize=32)
def aandhai(mood='calm', paper=True, scale=1.0):
    """Aandhai the owl with round glasses, reading the fine print"""
    W_, H_ = 460, 620; im = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im); cx = W_ // 2
    d.ellipse((cx - 150, 160, cx + 150, 580), fill=OWL, outline=INK, width=OUT)
    d.ellipse((cx - 95, 300, cx + 95, 560), fill=OWL_L)
    for k in range(3):
        for j in (-1, 0, 1): d.arc((cx + j * 44 - 16, 340 + k * 60, cx + j * 44 + 16, 370 + k * 60), 20, 160, fill=OWL, width=4)
    for s in (-1, 1):
        d.polygon([(cx + s * 70, 180), (cx + s * 130, 90), (cx + s * 140, 210)], fill=OWL, outline=INK)
        d.line([(cx + s * 40, 575), (cx + s * 40, 605)], fill=(240, 150, 60), width=12)
    hy = 260
    _face(d, cx, hy, 150, mood)
    d.polygon([(cx - 22, hy + 20), (cx + 22, hy + 20), (cx, hy + 64)], fill=BEAK, outline=INK)
    for s in (-1, 1):
        ex = cx + s * 52
        d.ellipse((ex - 46, hy - 54, ex + 46, hy + 38), outline=INK, width=10)
    d.line((cx - 8, hy - 10, cx + 8, hy - 10), fill=INK, width=8)
    if paper:
        d.polygon([(cx - 120, 400), (cx + 120, 390), (cx + 130, 540), (cx - 110, 550)], fill=CREAM, outline=INK)
        for k in range(5): d.line((cx - 90, 420 + k * 24, cx + (90 if k % 2 else 50), 416 + k * 24), fill=(150, 140, 130), width=4)
    return _scale(im, scale)


@functools.lru_cache(maxsize=32)
def ponni(mood='happy', nut=True, scale=1.0):
    """Ponni the squirrel with a pink bow and a big tail"""
    W_, H_ = 520, 640; im = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im); cx = W_ // 2 - 40
    tail = [(cx + 90, 560), (cx + 230, 470), (cx + 240, 280), (cx + 160, 120), (cx + 90, 160), (cx + 150, 300), (cx + 120, 460)]
    d.polygon(tail, fill=SQ); d.line(tail + [tail[0]], fill=INK, width=OUT, joint='curve')
    d.line([(cx + 130, 480), (cx + 200, 300), (cx + 150, 180)], fill=SQ_L, width=18, joint='curve')
    d.ellipse((cx - 100, 300, cx + 100, 590), fill=SQ, outline=INK, width=OUT)
    d.ellipse((cx - 60, 350, cx + 60, 570), fill=SQ_L)
    for s in (-1, 1): d.ellipse((cx + s * 50 - 30, 570, cx + s * 50 + 30, 606), fill=SQ, outline=INK, width=5)
    hy, r = 220, 100
    for s in (-1, 1): d.polygon([(cx + s * 50, hy - 70), (cx + s * 90, hy - 150), (cx + s * 100, hy - 50)], fill=SQ, outline=INK)
    d.ellipse((cx - r, hy - r, cx + r, hy + r), fill=SQ, outline=INK, width=OUT)
    d.ellipse((cx - 60, hy, cx + 60, hy + 86), fill=SQ_L)
    _face(d, cx, hy, r, mood)
    d.ellipse((cx - 8, hy + 22, cx + 8, hy + 34), fill=INK)
    # pink bow
    bx, by = cx + 60, hy - 86
    for s in (-1, 1): d.polygon([(bx, by), (bx + s * 50, by - 30), (bx + s * 50, by + 30)], fill=PINK, outline=INK)
    d.ellipse((bx - 14, by - 14, bx + 14, by + 14), fill=PINK, outline=INK, width=5)
    if nut:
        d.ellipse((cx - 44, 380, cx + 44, 460), fill=(150, 100, 50), outline=INK, width=5)
        d.chord((cx - 44, 370, cx + 44, 410), 180, 360, fill=(110, 70, 40), outline=INK, width=5)
    return _scale(im, scale)


def mani(mood='happy', pose='down', step=0, scale=1.0, phone=False):
    return A.monkey(mood, pose, step, scale, phone, True)


def thatha(mood='happy', trunk=0, scale=1.0):
    return A.elephant(mood, trunk, scale, True, True)


@functools.lru_cache(maxsize=4)
def grain(r=40):
    im = Image.new('RGBA', (r * 3, r * 3), (0, 0, 0, 0)); _grain(ImageDraw.Draw(im), r * 1.5, r * 1.5, r); return im


@functools.lru_cache(maxsize=64)
def grain_pile(n, w=520):
    """pile of n grains (deterministic layout)"""
    import random
    H_ = 420; im = Image.new('RGBA', (w, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im); r = random.Random(7)
    rows = []; k = 0; row = 0
    while k < n:
        cnt = max(1, 9 - row); y = H_ - 30 - row * 34
        for j in range(cnt):
            if k >= n: break
            x = w / 2 + (j - (cnt - 1) / 2) * 52 + r.uniform(-6, 6)
            _grain(d, x, y + r.uniform(-4, 4), 24); k += 1
        row += 1
    return im


@functools.lru_cache(maxsize=2)
def bank(w=620):
    """Kaadu Bank: a hollow tree trunk with a door and a hanging sign"""
    H_ = 700; im = Image.new('RGBA', (w, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im); cx = w // 2
    tr = [(cx - 200, H_ - 10), (cx + 200, H_ - 10), (cx + 160, 260), (cx - 160, 260)]
    d.polygon(tr, fill=(140, 96, 58)); d.line(tr + [tr[0]], fill=INK, width=OUT)
    for k in range(-2, 3): d.line((cx + k * 60, 300, cx + k * 70, H_ - 30), fill=(110, 74, 44), width=6)
    for (x, y, r, col) in ((cx, 160, 230, (70, 140, 70)), (cx - 190, 230, 140, (90, 160, 80)), (cx + 190, 230, 140, (90, 160, 80))):
        d.ellipse((x - r, y - r * 0.7, x + r, y + r * 0.7), fill=col, outline=INK, width=OUT)
    d.chord((cx - 90, 470, cx + 90, 760), 180, 360, fill=(60, 40, 25), outline=INK, width=OUT)
    d.rectangle((cx - 90, 615, cx + 90, H_ - 10), fill=(60, 40, 25))
    d.rounded_rectangle((cx - 170, 330, cx + 170, 430), 16, fill=CREAM, outline=INK, width=OUT)
    from lib import text_img
    t = text_img('KAADU BANK', 'anton', 64, INK); im.alpha_composite(t, (cx - t.size[0] // 2, 380 - t.size[1] // 2))
    return shadowed(im)
