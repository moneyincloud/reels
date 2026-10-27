"""Tamil story reel compositor: 2D paper-cutout scenes (paperscenes.py) + Tamil overlays + owner's voice.
Frames: FR/<scene>/NNNN.jpg rendered at 15 fps over RDUR seconds each.
Voice: ROOT+'storyta/vo/<i>.wav' (owner's recordings), durations in vo/durs.json.
"""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from lib import *
from scenes import bgs
import saveshare as SS

FONTS['ta'] = FD + 'noto-sans-tamil-tamil-800-normal.woff'
FR = _os.environ.get('STORY_FR', '/tmp/claude-0/-home-claude/32ef0837-6367-50a7-8b18-d49a84afef86/scratchpad/d3/frst/')
SH = ROOT + 'storyta/'
SCN = ['hook', 'lift', 'cab', 'why', 'scam', 'fight', 'turn', 'home', 'end']
RDUR, RFPS = 9.5, 15
DURS = json.load(open(SH + 'vo/durs.json'))
LEAD, TAIL = 0.25, 0.45
STARTS, VO = [], []
_t = 0.0
for i, d in enumerate(DURS):
    STARTS.append(_t); VO.append(_t + (0.15 if i == 0 else LEAD)); _t = VO[-1] + d + TAIL
DUR = _t + 1.2
B = STARTS[1:]
GREY = (120, 116, 108); NAVY = (30, 60, 120)


from storyta_txt import text_ta
import paperscenes as PS


@functools.lru_cache(maxsize=256)
def chip(txt, size=58, bg=(20, 20, 22, 225), fg=CREAM, pad=34):
    lines = txt.split('\n'); ims = [text_ta(l, size, fg) for l in lines]
    w = max(m.size[0] for m in ims) + pad * 2; h = sum(m.size[1] for m in ims) + 14 * (len(ims) - 1) + pad * 1.4
    im = Image.new('RGBA', (int(w), int(h)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 26, fill=bg); y = pad * 0.7
    for m in ims: im.alpha_composite(m, (int((w - m.size[0]) / 2), int(y))); y += m.size[1] + 14
    return im


@functools.lru_cache(maxsize=128)
def bubble(txt, size=54):
    lines = txt.split('\n'); ims = [text_ta(l, size, INK) for l in lines]
    w = max(m.size[0] for m in ims) + 70; h = sum(m.size[1] for m in ims) + 14 * (len(ims) - 1) + 56
    im = Image.new('RGBA', (w + 10, h + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((8, 8, w + 7, h + 7), 30, fill=INK); d.rounded_rectangle((0, 0, w - 1, h - 1), 30, fill=(255, 255, 255), outline=INK, width=6)
    d.polygon([(70, h - 4), (130, h - 4), (60, h + 50)], fill=(255, 255, 255), outline=INK); d.line([(70, h - 3), (130, h - 3)], fill=(255, 255, 255), width=8)
    y = 28
    for m in ims: im.alpha_composite(m, (35, y)); y += m.size[1] + 14
    return im


@functools.lru_cache(maxsize=64)
def stamp(txt, col=RED, size=110, rot=-6):
    ls = [text_ta(l, size, col) for l in txt.split('\n')]
    t = Image.new('RGBA', (max(m.size[0] for m in ls), sum(m.size[1] for m in ls) + 10 * (len(ls) - 1)), (0, 0, 0, 0)); y = 0
    for m in ls: t.alpha_composite(m, ((t.size[0] - m.size[0]) // 2, y)); y += m.size[1] + 10
    w, h = t.size[0] + 70, t.size[1] + 50
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((4, 4, w - 5, h - 5), 18, outline=col, width=10); im.alpha_composite(t, (35, 25))
    a = np.asarray(im).copy(); rnd = np.random.default_rng(len(txt)).random(a.shape[:2]) < 0.12; a[rnd, 3] = (a[rnd, 3] * 0.35).astype(np.uint8)
    return Image.fromarray(a).rotate(rot, Image.BICUBIC, expand=True)


def pop(t, t0, d=0.35): return eback(prog(t, t0, d), 1.6)


def at_f(i, f): return VO[i] + DURS[i] * f


# overlays: (scene, fraction of the voice line, kind, text, x, y)
OV = [
    (0, 0.00, 'stamp', 'நாள் 92', 540, 300), (0, 0.18, 'chip', 'கையில் ₹0', 540, 470), (0, 0.62, 'chip', 'ஒரு லாரி டிரைவரின்\nகதை…', 540, 1500),
    (1, 0.05, 'chip', 'லிஃப்ட் கேட்டேன்', 540, 300), (1, 0.45, 'bubble', 'எங்க போறீங்க?', 330, 520), (1, 0.75, 'chip', '"நீங்க போற இடத்துக்கே"', 540, 1520),
    (2, 0.5, 'bubble', '15 வருஷமா\nவீட்டுக்கே போகல…', 380, 330),
    (3, 0.05, 'stamp', 'ஏன்?', 540, 360), (3, 0.55, 'chip', 'நம்ம வீட்டுலயும்\nநடந்தது தான்…', 540, 1500),
    (4, 0.0, 'chip', 'அப்பாவின் சேமிப்பு', 540, 300), (4, 0.3, 'stamp', '"இரட்டிப்பு!"', 540, 1480), (4, 0.75, 'stampx', 'போலி திட்டம்', 540, 1690),
    (5, 0.05, 'bubble', '"உன்னால தான்!"', 330, 330), (5, 0.55, 'chip', '15 வயசுல வீட்ட விட்டு…', 540, 1520),
    (6, 0.05, 'bubble', 'பணம் திரும்ப வரும்…\nஅம்மா காத்திருப்பாங்களா?', 470, 330), (6, 0.8, 'chip', 'லாரி வழி மாறுச்சு', 540, 1540),
    (7, 0.0, 'stamp', '15 வருஷம்\nகழிச்சு', 540, 330), (7, 0.62, 'answer', '', 540, 1350),
]


def overlays(c, t):
    for (i, f, kind, txt, x, y) in OV:
        t0 = at_f(i, f)
        if not (STARTS[i] <= t < (STARTS[i + 1] if i + 1 < len(STARTS) else DUR)) or t < t0: continue
        p = pop(t, t0)
        if kind == 'chip': place(c, chip(txt), x, y, p)
        elif kind == 'bubble': place(c, bubble(txt), x, y, p)
        elif kind in ('stamp', 'stampx'):
            s_ = 1.0 + 0.8 * (1 - eo(prog(t, t0, 0.22))); a = clamp((t - t0) / 0.12)
            place(c, stamp(txt, RED if kind == 'stamp' else (200, 30, 30)), x, y, s_, 0, a)
            if kind == 'stampx' and t > t0 + 0.3:
                k = 90 * eo(prog(t, t0 + 0.3, 0.25)); d = ImageDraw.Draw(c)
                d.line((x - 260, y - k * 0.6, x - 260 + 520 * eo(prog(t, t0 + 0.3, 0.25)), y + k * 0.6), fill=RED, width=16)
        elif kind == 'answer':
            q = eback(prog(t, t0, 0.5), 1.2)
            card = SS._card(940, 330, CREAM); place(c, card, x, y, q, -1)
            if q > 0.6:
                place(c, text_ta('போன பணம் திரும்ப வரும்.', 64, INK), x, y - 70)
                place(c, text_ta('போன குடும்பம் வராது.', 80, RED), x, y + 50)


def end_card(c, t):
    i = 8; T0 = STARTS[8]
    dim = Image.new('RGBA', c.size, (15, 15, 20, int(200 * clamp((t - T0) / 0.6)))); c.alpha_composite(dim)
    if t > T0 + 0.2:
        place(c, stamp('"இரட்டிப்பு"\nதிட்டங்களை', RED, 66, -3), 540, 400, pop(t, T0 + 0.2))
        place(c, stamp('நம்பாதீங்க!', RED, 92, 4), 540, 620, pop(t, T0 + 0.5))
    ts = at_f(i, 0.4)
    if t > ts:
        p = pop(t, ts, 0.4); place(c, SS._card(980, 280, YEL), 540, 900, p, -1.5)
        if p > 0.6: place(c, text_ta('இதை உங்க அப்பா அம்மாவுக்கு', 44, INK), 540, 860); place(c, text_ta('அனுப்புங்க', 64, NAVY), 540, 950)
        q = prog(t, ts + 0.3, 1.1)
        if 0 < q < 1: place(c, SS.plane_icon(110), 80 + 920 * eio(q), 700 - 160 * math.sin(math.pi * q), 1, 15 - 30 * q)
    tf = at_f(i, 0.75)
    if t > tf: place(c, chip('@moneyincloud\nஃபாலோ பண்ணுங்க', 50, YEL + (255,), INK), 540, 1180, pop(t, tf))
    if t > T0 + 0.5:
        place(c, text_ta('கற்பனை கதை · கல்வி நோக்கம் மட்டும்', 34, (210, 204, 192)), 540, 1420)


def header(c, t):
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, INK, 1), (52, 64))
    lb = chip('கற்பனை கதை', 30, (198, 40, 40, 230), CREAM, 18); c.alpha_composite(lb, (W - 52 - lb.size[0], 52))
    d = ImageDraw.Draw(c); d.line((60, 128, W - 60, 128), fill=(27, 27, 27, 90), width=2)
    d.line((60, 128, 60 + (W - 120) * clamp(t / DUR), 128), fill=YEL, width=8)


def transition(c, t):
    cols = [(TEAL if 'TEAL' in globals() else (20, 140, 130), INK), (YEL, INK), (RED, YEL), ((230, 120, 30), CREAM)]
    for bi, b in enumerate(B):
        d = 0.5
        if abs(t - b) > d / 2 + 0.12: continue
        for layer, delay in ((0, -0.05), (1, 0.0)):
            p = (t - (b - d / 2) - delay) / d
            if p <= 0 or p >= 1: continue
            p = eio(p); SWd, skew = 2050, 320
            xl = (W + 60) + p * (-(SWd + skew) - (W + 60) - 40)
            r = random.Random(bi * 10 + layer + 4400)
            left = [(xl + r.uniform(-14, 14) - skew * (y / H), y) for y in range(0, H + 1, 40)]
            right = [(xl + SWd + r.uniform(-14, 14) - skew * (y / H), y) for y in range(H, -1, -40)]
            if layer == 0: left = [(x - 70, y) for x, y in left]; right = [(x + 70, y) for x, y in right]
            poly_fill(c, left + right, cols[bi % len(cols)][layer], 255, S=1)


def scene_at(t):
    k = 0
    for i, s in enumerate(STARTS):
        if t >= s: k = i
    return k


@functools.lru_cache(maxsize=4)
def frame3d(sc, idx):
    p = f'{FR}{sc}/{idx:04d}.jpg'
    if not _os.path.exists(p):
        fs = sorted(_os.listdir(FR + sc)); p = FR + sc + '/' + fs[min(idx, len(fs) - 1)]
    return Image.open(p).convert('RGB').resize((W, H), Image.LANCZOS)


@functools.lru_cache(maxsize=1)
def vign():
    y, x = np.mgrid[0:H, 0:W]; r = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
    return np.clip(1.04 - 0.14 * r ** 2, 0.8, 1.0)[..., None]


def _render(t, loop=False):
    i = scene_at(t); st = STARTS[i]; en = STARTS[i + 1] if i + 1 < len(STARTS) else DUR
    c = PS.scene(i, t - st, en - st)
    if i == 8: end_card(c, t)
    else: overlays(c, t)
    if not loop: header(c, t)
    transition(c, t)
    arr = np.asarray(c.convert('RGB')).astype(np.float32) * vign()
    g = grain_frames()[int(t * FPS) % 6]
    return np.clip(arr + g[..., None] * 0.6, 0, 255).astype(np.uint8)


def render(t):
    LOOP = 0.6
    if t > DUR - LOOP:
        a = _render(t); b = _render(0.4, loop=True); q = eio((t - (DUR - LOOP)) / LOOP)
        return (a * (1 - q) + b * q).astype(np.uint8)
    return _render(t)


def slam_times(): return []


def at(i, phrase='', off=0.0):
    return VO[i] + off
