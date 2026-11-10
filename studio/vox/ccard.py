"""Cloud Family Ep 2: Arjun's first credit card - free period, minimum due trap, missed payment, EMI, card types, pros/cons, 3 rules.
Realistic cast cut-outs, multi-voice dialogue (vo_cast.py), light template, red topic colour."""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, textwrap, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from lib import *
from scenes import stamp_c
from fridge import follow_btn

SH = ROOT + 'ccard/'
CAST_DIR = ROOT + 'brand/cast_real/'
LINES = json.load(open(SH + 'lines.json'))
SCRIPT = [l['text'] for l in LINES]
WHO = [l['who'] for l in LINES]
DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO = [], []
_t = 0.0
for i, d in enumerate(DURS):
    gap = 0.12 if WHO[i] != 'narrator' else 0.2
    STARTS.append(_t); VO.append(_t + (0.15 if i == 0 else gap)); _t = VO[-1] + d + 0.22
DUR = _t + 1.3
B = STARTS[1:]
NAVY = (43, 63, 140); SKY = (126, 200, 242); SOFT = (255, 247, 230); GREY = (110, 116, 130)
COL = {'kasi': (200, 30, 40), 'arjun': (235, 110, 30), 'amma': (30, 130, 70), 'paati': (125, 60, 150),
       'thatha': (190, 140, 20), 'appa': (40, 100, 200), 'narrator': NAVY}
NAME = {'kasi': 'KASI MAMA', 'arjun': 'ARJUN', 'amma': 'AMMA', 'paati': 'PAATI', 'thatha': 'THATHA', 'appa': 'APPA',
        'narrator': ''}


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def scene_at(t):
    i = 0
    for k, s in enumerate(STARTS):
        if t >= s: i = k
    return i


# ---------- voice amplitude (talking bob) ----------
@functools.lru_cache(None)
def env(i):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{SH}vo/{i}.wav', '-ac', '1', '-ar', '24000', '-f', 's16le', '-'],
                         capture_output=True).stdout
    x = np.abs(np.frombuffer(raw, np.int16).astype(float) / 32768)
    hop = 24000 // 30; n = len(x) // hop
    e = np.array([x[k * hop:(k + 1) * hop].mean() for k in range(n)])
    return e / (e.max() + 1e-6)


def amp(i, t):
    e = env(i); k = int((t - VO[i]) * 30)
    return float(e[k]) if 0 <= k < len(e) else 0.0


# ---------- assets ----------
@functools.lru_cache(None)
def person(name, w):
    im = Image.open(CAST_DIR + f'cut/{name}.png').convert('RGBA')
    h = int(im.size[1] * w / im.size[0])
    im = im.resize((w, h), Image.LANCZOS)
    rgb = im.convert('RGB').filter(ImageFilter.UnsharpMask(2, 60, 2)); rgb.putalpha(im.getchannel('A'))
    return rgb


@functools.lru_cache(None)
def room_bg():
    im = Image.open(CAST_DIR + 'raw/family_scene.png').convert('RGB')
    im = im.crop((520, 0, 1050, 941)).resize((1080, 1920), Image.LANCZOS).filter(ImageFilter.GaussianBlur(26))
    ov = Image.new('RGB', im.size, SOFT)
    im = Image.blend(im, ov, 0.42)
    g = Image.linear_gradient('L').resize((1080, 1920))
    im = Image.composite(Image.new('RGB', im.size, (255, 250, 240)), im, g.point(lambda v: int(v * 0.35)))
    return im.convert('RGBA')


@functools.lru_cache(None)
def red_bg():
    im = Image.new('RGB', (W, H), (200, 34, 30)); d = ImageDraw.Draw(im)
    cx, cy = 540, 1150
    for k in range(28):
        a0 = k * 2 * math.pi / 28; a1 = a0 + math.pi / 28
        d.polygon([(cx, cy), (cx + 2600 * math.cos(a0), cy + 2600 * math.sin(a0)), (cx + 2600 * math.cos(a1), cy + 2600 * math.sin(a1))],
                  fill=(216, 48, 40))
    g = Image.radial_gradient('L').resize((2400, 2400)).crop((660, 50, 1740, 1970))
    im = Image.composite(im, Image.new('RGB', im.size, (120, 14, 16)), g.point(lambda v: 255 - int(v * 0.8)))
    return im.convert('RGBA')


@functools.lru_cache(None)
def data_bg():
    im = Image.new('RGB', (W, H), (250, 246, 238)); d = ImageDraw.Draw(im)
    for y in range(0, H, 60): d.line((0, y, W, y), fill=(236, 230, 220), width=2)
    for x in range(0, W, 60): d.line((x, 0, x, H), fill=(236, 230, 220), width=2)
    return im.convert('RGBA')


@functools.lru_cache(None)
def family_print():
    im = Image.open(CAST_DIR + 'raw/family_scene.png').convert('RGB').resize((920, 518), Image.LANCZOS)
    return cutout(im.convert('RGBA'), border=18, shadow=0.4)


def inr(n):
    s = str(int(n))
    if len(s) <= 3: return s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2: parts.insert(0, head[-2:]); head = head[:-2]
    if head: parts.insert(0, head)
    return ','.join(parts) + ',' + tail


# ---------- character on stage ----------
def actor(c, t, i, name, cx, w, base=H + 10, enter=None, bob=True):
    """bottom-anchored cut-out. talking bob from voice amplitude when this line is speaking."""
    im = person(name, w)
    a = amp(i, t) if bob else 0
    br = math.sin(t * 2.1) * 3
    sc = 1 + 0.018 * a
    dy = -10 * a + br
    dx = 0
    al = 1.0
    if enter is not None:
        p = prog(t, enter[0], 0.4)
        dx = (1 - eo(p)) * enter[1]; al = clamp(p * 3)
    imr = im if abs(sc - 1) < 0.003 else im.resize((int(im.size[0] * sc), int(im.size[1] * sc)), Image.BILINEAR)
    if al < 0.99:
        imr = imr.copy(); imr.putalpha(imr.getchannel('A').point(lambda v: int(v * al)))
    comp(c, imr, cx - imr.size[0] / 2 + dx, base - imr.size[1] + dy)
    return base - imr.size[1] + dy


# ---------- speech bubble with karaoke words ----------
def segs(i):
    import re
    out = []; pos = 0
    for m in re.finditer(r'[^.!?]+[.!?]*\s*', SCRIPT[i]):
        out.append((m.start(), m.end())); 
    return out


@functools.lru_cache(None)
def bubble_layout(i, size, maxw, seg=None):
    txt = SCRIPT[i] if seg is None else SCRIPT[i][seg[0]:seg[1]]
    words = txt.replace('F and O', 'F&O').split()
    lines, cur = [], []
    for wd in words:
        trial = ' '.join(cur + [wd])
        if cur and text_w(trial, 'pop', size) > maxw:
            lines.append(cur); cur = [wd]
        else:
            cur.append(wd)
    if cur: lines.append(cur)
    return lines


def bubble(c, t, i, cy, tail_x=None, size=50, maxw=860, tag=True, t0=None, seg=None):
    t0 = VO[i] - 0.1 if t0 is None else t0
    p = prog(t, t0, 0.3)
    if p <= 0: return
    lines = bubble_layout(i, size, maxw, seg)
    lh = int(size * 1.32)
    bw = max(text_w(' '.join(l), 'pop', size) for l in lines) + 90
    bh = lh * len(lines) + 60
    im = Image.new('RGBA', (bw + 20, bh + 70), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 14, bw + 10, bh + 14), 46, fill=INK)
    d.rounded_rectangle((0, 0, bw, bh), 46, fill=(255, 255, 255), outline=INK, width=7)
    if tail_x is not None:
        tx = int(clamp((tail_x - (540 - bw / 2)) / bw, 0.15, 0.85) * bw)
        d.polygon([(tx - 26, bh - 8), (tx + 22, bh - 8), (tx - 8, bh + 56)], fill=(255, 255, 255), outline=None)
        d.line([(tx - 26, bh - 4), (tx - 8, bh + 56), (tx + 22, bh - 4)], fill=INK, width=7, joint='curve')
        d.line([(tx - 20, bh - 4), (tx + 16, bh - 4)], fill=(255, 255, 255), width=8)
    # karaoke
    sp = clamp((t - VO[i]) / DURS[i]) * len(SCRIPT[i])
    pos = 0 if seg is None else seg[0]; y = 30 + lh // 2
    for ln in lines:
        s = ' '.join(ln); x = bw / 2 - text_w(s, 'pop', size) / 2
        for wd in ln:
            done = pos <= sp
            col = INK if done else (170, 170, 178)
            if done and any(ch.isdigit() for ch in wd) or wd.startswith('sure') or wd.startswith('Ninety'):
                col = COL[WHO[i]] if done else col
            ti = text_img(wd, 'pop', size, col)
            im.alpha_composite(ti, (int(x - size * 0.12), int(y - ti.size[1] / 2)))
            x += text_w(wd + ' ', 'pop', size); pos += len(wd) + 1
        y += lh
    sc = 0.6 + 0.4 * eback(p, 2.2)
    place(c, im, 540, cy + bh / 2 - (bh + 70) / 2 + (bh + 70) / 2, sc, 0, clamp(p * 3))
    if tag and NAME[WHO[i]]:
        tg = text_img(NAME[WHO[i]], 'anton', 44, (255, 255, 255))
        pill = Image.new('RGBA', (tg.size[0] + 40, tg.size[1] + 8), (0, 0, 0, 0))
        ImageDraw.Draw(pill).rounded_rectangle((0, 0, pill.size[0] - 1, pill.size[1] - 1), 22, fill=COL[WHO[i]], outline=INK, width=5)
        pill.alpha_composite(tg, (20, 4))
        place(c, pill, 540 - bw / 2 + pill.size[0] / 2 + 30, cy - bh / 2 + 6, sc, -3, clamp(p * 3))


def caption(c, t, i, cy, size=48, by_sentence=False):
    """narrator caption: no tail. by_sentence shows only the sentence being spoken"""
    if not by_sentence:
        bubble(c, t, i, cy, None, size, 900, tag=False); return
    sp = clamp((t - VO[i]) / DURS[i]) * len(SCRIPT[i])
    sg = [g for g in segs(i) if g[0] <= sp][-1] if sp > 0 else segs(i)[0]
    bubble(c, t, i, cy, None, size, 900, tag=False, seg=sg)


def src(c, txt, y=1835):
    im = text_img(txt, 'osw5', 26, (90, 92, 104))
    place(c, im, 540, y)


def stamp_at(c, t, txt, colr, size, rot, t0, cx, cy, seed=1):
    if t < t0: return
    p = prog(t, t0, 0.22)
    s = 1 + 1.2 * (1 - eo(p))
    place(c, stamp_c(txt, colr, size, rot, seed), cx, cy, s, 0, clamp(p * 4))


def pill_text(s, bg, fg, size=64, pad=(36, 14), out=INK):
    tt = text_img(s, 'anton', size, fg)
    im = Image.new('RGBA', (tt.size[0] + 2 * pad[0] + 10, tt.size[1] + 2 * pad[1] + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    w, h = tt.size[0] + 2 * pad[0], tt.size[1] + 2 * pad[1]
    d.rounded_rectangle((10, 10, w + 9, h + 9), 30, fill=INK)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 30, fill=bg, outline=out, width=6)
    im.alpha_composite(tt, (pad[0], pad[1]))
    return im


# ---------- props ----------
@functools.lru_cache(None)
def phone_img(red=False):
    w, h = 300, 560
    im = Image.new('RGBA', (w + 16, h + 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((16, 16, w + 15, h + 15), 44, fill=(0, 0, 0, 90))
    d.rounded_rectangle((0, 0, w, h), 44, fill=(22, 24, 30), outline=INK, width=6)
    d.rounded_rectangle((16, 30, w - 16, h - 30), 26, fill=(250, 250, 252))
    d.text((w / 2, 70), 'NIFTY OPTIONS', font=font('osw', 28), fill=(40, 40, 50), anchor='mm')
    rng = np.random.default_rng(4 if not red else 9); y = 300.0
    for k in range(9):
        x = 40 + k * 26
        o = y; y = y + rng.normal(-14 if not red else 22, 18); cl = y
        hi, lo = min(o, cl) - rng.uniform(5, 20), max(o, cl) + rng.uniform(5, 20)
        col = (36, 170, 90) if cl < o else (226, 58, 44)
        d.line((x + 9, hi, x + 9, lo), fill=col, width=3); d.rectangle((x, min(o, cl), x + 18, max(o, cl) + 2), fill=col)
    bc = (36, 170, 90) if not red else (226, 58, 44)
    d.rounded_rectangle((40, h - 130, w - 40, h - 60), 20, fill=bc)
    d.text((w / 2, h - 95), 'BUY NOW' if not red else '-₹1,00,000', font=font('pop', 32), fill='white', anchor='mm')
    return im


@functools.lru_cache(None)
def doc_card():
    w, h = 520, 640
    im = Image.new('RGBA', (w, h), (255, 255, 255, 255)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, w - 1, h - 1), outline=(200, 196, 188), width=3)
    d.rectangle((0, 0, w, 96), fill=NAVY)
    d.text((w / 2, 50), 'SEBI STUDY', font=font('anton', 60), fill='white', anchor='mm')
    d.text((w / 2, 140), 'Individual traders in', font=font('osw5', 34), fill=INK, anchor='mm')
    d.text((w / 2, 184), 'equity F&O · FY25', font=font('osw', 40), fill=INK, anchor='mm')
    for k in range(7):
        y = 250 + k * 46; d.rounded_rectangle((50, y, w - 50 - (k % 3) * 60, y + 16), 8, fill=(222, 222, 228))
    d.text((w / 2, h - 50), 'July 2025', font=font('type', 30), fill=GREY, anchor='mm')
    return cutout(im, border=0, shadow=0.35)


def person_icon(col):
    im = Image.new('RGBA', (60, 74), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((18, 2, 42, 26), fill=col); d.rounded_rectangle((8, 30, 52, 72), 18, fill=col)
    return im


ICON = {}
def icon(col):
    if col not in ICON: ICON[col] = person_icon(col)
    return ICON[col]


def card(n, txt, colr, w=600):
    tt = text_img(txt, 'anton', 52, INK)
    h = 112
    im = Image.new('RGBA', (w + 10, h + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 10, w + 9, h + 9), 26, fill=INK)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 26, fill=(255, 255, 255), outline=INK, width=6)
    d.ellipse((18, 16, 98, 96), fill=colr, outline=INK, width=5)
    d.text((58, 56), str(n), font=font('anton', 54), fill='white', anchor='mm')
    sc = min(1.0, (w - 140) / tt.size[0])
    if sc < 1: tt = tt.resize((int(tt.size[0] * sc), int(tt.size[1] * sc)), Image.LANCZOS)
    im.alpha_composite(tt, (118, int(h / 2 - tt.size[1] / 2)))
    return im


# ---------------- credit card props ----------------
@functools.lru_cache(None)
def cc_img(col=(30, 40, 70), w=520):
    h = int(w * 0.63)
    im = Image.new('RGBA', (w + 16, h + 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((14, 14, w + 13, h + 13), 30, fill=(0, 0, 0, 80))
    d.rounded_rectangle((0, 0, w - 1, h - 1), 30, fill=col, outline=INK, width=6)
    for k in range(6): d.arc((w * 0.45 + k * 30, -h * 0.3 + k * 10, w * 1.4 + k * 30, h * 1.2 + k * 10), 150, 230, fill=(255, 255, 255, 40), width=6)
    d.rounded_rectangle((50, h * 0.33, 130, h * 0.33 + 62), 10, fill=(230, 190, 90), outline=INK, width=3)
    d.line((50, h * 0.33 + 31, 130, h * 0.33 + 31), fill=INK, width=2); d.line((90, h * 0.33, 90, h * 0.33 + 62), fill=INK, width=2)
    im.alpha_composite(text_img('CLOUD CARD', 'anton', 44, (255, 255, 255)), (46, 26))
    im.alpha_composite(text_img('4321  ••••  ••••  0042', 'osw', 38, (240, 240, 245)), (46, int(h * 0.62)))
    im.alpha_composite(text_img('ARJUN', 'osw5', 30, (220, 220, 230)), (46, int(h * 0.80)))
    for k, cc in enumerate([(235, 80, 60), (255, 190, 40)]):
        d.ellipse((w - 150 + k * 50, h - 100, w - 70 + k * 50, h - 20), fill=cc + (230,))
    return im


@functools.lru_cache(None)
def bill_img():
    w, h = 640, 560
    im = Image.new('RGBA', (w + 14, h + 14), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((14, 14, w + 13, h + 13), fill=(0, 0, 0, 70))
    d.rectangle((0, 0, w - 1, h - 1), fill=(255, 255, 255), outline=INK, width=5)
    d.rectangle((0, 0, w, 80), fill=(30, 40, 70))
    im.alpha_composite(text_img('CARD STATEMENT', 'anton', 50, (255, 255, 255)), (30, 12))
    rows = [('Phone purchase', '₹50,000', INK), ('TOTAL DUE', '₹50,000', INK), ('MINIMUM DUE (5%)', '₹2,500', RED), ('Due date', '20 days later', GREY)]
    for k, (a, b, col) in enumerate(rows):
        y = 120 + k * 105
        im.alpha_composite(text_img(a, 'osw', 40, INK), (30, y)); tb = text_img(b, 'anton', 52, col); im.alpha_composite(tb, (w - 30 - tb.size[0], y - 6))
        d.line((30, y + 80, w - 30, y + 80), fill=(225, 225, 230), width=2)
    return im


@functools.lru_cache(None)
def shop_phone():
    w, h = 420, 780
    im = Image.new('RGBA', (w + 16, h + 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((16, 16, w + 15, h + 15), 56, fill=(0, 0, 0, 80))
    d.rounded_rectangle((0, 0, w - 1, h - 1), 56, fill=(25, 25, 32), outline=INK, width=6)
    d.rounded_rectangle((22, 22, w - 23, h - 23), 40, fill=(255, 255, 255))
    d.rounded_rectangle((90, 90, w - 90, 430), 30, fill=(40, 50, 90))
    d.rounded_rectangle((120, 120, w - 120, 400), 22, fill=(120, 170, 240))
    d.ellipse((w // 2 - 18, 370, w // 2 + 18, 406), fill=(255, 255, 255))
    im.alpha_composite(text_img('NEW PHONE', 'anton', 50, INK), (w // 2 - text_img('NEW PHONE', 'anton', 50, INK).size[0] // 2, 460))
    tp = text_img('₹50,000', 'anton', 76, RED); im.alpha_composite(tp, (w // 2 - tp.size[0] // 2, 530))
    d.rounded_rectangle((60, 660, w - 60, 730), 34, fill=(46, 160, 90))
    tb = text_img('PAY BY CARD', 'anton', 40, (255, 255, 255)); im.alpha_composite(tb, (w // 2 - tb.size[0] // 2, 672))
    return im


def info(lines, w=900, col=(30, 40, 70)):
    rows = [text_img(s, 'anton' if k == 0 else 'pop', sz, c_) for k, (s, sz, c_) in enumerate(lines)]
    h = sum(r.size[1] for r in rows) + 26 * len(rows) + 30
    im = Image.new('RGBA', (w + 12, h + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((12, 12, w + 11, h + 11), 30, fill=INK)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 30, fill=(255, 255, 255), outline=INK, width=6)
    d.rounded_rectangle((0, 0, 22, h - 1), 10, fill=col)
    y = 26
    for r in rows:
        s = min(1.0, (w - 70) / r.size[0])
        if s < 1: r = r.resize((int(r.size[0] * s), int(r.size[1] * s)), Image.LANCZOS)
        im.alpha_composite(r, (int(w / 2 + 10 - r.size[0] / 2), y)); y += r.size[1] + 26
    return im


info = functools.lru_cache(None)(info)


def info_at(c, t, t0, lines, y, col=(30, 40, 70), w=900, x=540, rot=-1.5):
    if t < t0: return
    p = prog(t, t0, 0.4)
    place(c, info(tuple(lines), w, col), x + (1 - eo(p)) * 700, y, 1, rot, clamp(p * 3))


@functools.lru_cache(None)
def data_bg():
    im = Image.new('RGB', (W, H), (250, 246, 238)); d = ImageDraw.Draw(im)
    for y in range(0, H, 60): d.line((0, y, W, y), fill=(236, 230, 220), width=2)
    for x in range(0, W, 60): d.line((x, 0, x, H), fill=(236, 230, 220), width=2)
    return im.convert('RGBA')


def head(c, t, i, s, col=(30, 40, 70)):
    place(c, pill_text(s, col, (255, 255, 255), 56), 540, 200, 0.7 + 0.3 * eback(prog(t, STARTS[i], 0.35)), -2)


# ---------------- scenes ----------------
def s0(c, t):
    i = 0
    c.alpha_composite(red_bg())
    place_text(c, 'NEVER PAY ONLY', 'anton', 120, (255, 247, 230), 540, 260, t, None, 0.05, 'pop')
    place_text(c, 'THE MINIMUM DUE', 'anton', 120, YEL, 540, 400, t, None, at(0, 'minimum', -0.2), 'pop')
    p = prog(t, 0.3, 0.6)
    place(c, cc_img(), 540, 760, 0.6 + 0.4 * eback(p), -8 + 6 * math.sin(t * 2))
    actor(c, t, i, 'arjun_happy', 540, 760, base=H + 10, bob=False, enter=(0.2, 0))
    th = at(0, 'Here', -0.1)
    if t > th: place(c, pill_text('UP TO 45% INTEREST A YEAR', INK, YEL, 64), 540, 540, 0.6 + 0.4 * eback(prog(t, th, 0.3)), -4)


def s1(c, t):
    i = 1
    c.alpha_composite(room_bg())
    actor(c, t, i, 'arjun_laugh', 480, 800, enter=(STARTS[i], -400))
    place(c, cc_img(), 820, 1050 + 20 * math.sin(t * 4), 0.75, 12)
    bubble(c, t, i, 360, 470, size=62)


def s2(c, t):
    i = 2
    c.alpha_composite(room_bg())
    actor(c, t, i, 'amma_smug', 540, 820, enter=(STARTS[i], 600))
    bubble(c, t, i, 380, 540)


def s3(c, t):
    i = 3
    c.alpha_composite(data_bg())
    head(c, t, i, 'HOW A CREDIT CARD WORKS')
    d = ImageDraw.Draw(c); y = 760; x0, x1 = 110, 970
    p = eo(prog(t, at(i, 'You swipe', -0.2), 2.6))
    d.line((x0, y, x0 + (x1 - x0) * p, y), fill=INK, width=10)
    pts = [(x0, 'SWIPE', 'day 1', 'You swipe'), (x0 + 520, 'BILL', 'end of cycle', 'The bill'), (x1, 'DUE DATE', '~20 days later', 'about twenty')]
    for (x, a, b, ph) in pts:
        tk = at(i, ph, -0.2)
        if t < tk: continue
        q = eback(prog(t, tk, 0.35))
        d.ellipse((x - 26 * q, y - 26 * q, x + 26 * q, y + 26 * q), fill=YEL, outline=INK, width=5)
        place(c, text_img(a, 'anton', 56, INK), x if x > x0 else x + 40, y - 80); place(c, text_img(b, 'osw5', 32, GREY), x if x > x0 else x + 40, y + 70)
    tk = at(i, 'Up to fifty', -0.2)
    if t > tk:
        pp_ = eo(prog(t, tk, 0.8))
        d.rounded_rectangle((x0, 930, x0 + (x1 - x0) * pp_, 1010), 40, fill=(46, 160, 90), outline=INK, width=5)
        place(c, text_img('20–50 DAYS INTEREST-FREE', 'anton', 54, (255, 255, 255)), 540, 970, 1, 0, clamp((t - tk - 0.4) * 3))
    stamp_at(c, t, 'ONLY IF YOU PAY THE FULL BILL', RED, 64, -6, at(i, 'Only if', -0.1), 540, 1210, 2)
    caption(c, t, i, 1560, by_sentence=True)


def s4(c, t):
    i = 4
    c.alpha_composite(room_bg())
    actor(c, t, i, 'arjun_happy', 220, 520, bob=False)
    p = prog(t, at(i, 'The bill', -0.3), 0.5)
    if p > 0: place(c, bill_img(), 620, 820 + (1 - eo(p)) * 600, 0.95, 3)
    else: place(c, shop_phone(), 700, 900, 1.0, 6)
    caption(c, t, i, 330, by_sentence=True)


def s5(c, t):
    i = 5
    c.alpha_composite(room_bg())
    actor(c, t, i, 'kasi_smug', 540, 800)
    bubble(c, t, i, 380, 560)


def s6(c, t):
    i = 6
    c.alpha_composite(room_bg())
    actor(c, t, i, 'amma_smug', 540, 820)
    bubble(c, t, i, 380, 540)
    if t > at(i, 'interest is zero', -0.2):
        place(c, pill_text('PAY FULL = ₹0 INTEREST', (46, 160, 90), (255, 255, 255), 66), 540, 760, 0.6 + 0.4 * eback(prog(t, at(i, 'interest is zero', -0.2), 0.3)), -3)


def s7(c, t):
    i = 7
    c.alpha_composite(data_bg())
    head(c, t, i, 'OPTION B: MINIMUM DUE ONLY', RED)
    info_at(c, t, at(i, 'up to', -0.2), [('₹47,500 LEFT UNPAID', 70, INK), ('x up to 3.75% a month = ₹1,781', 44, INK)], 470, RED)
    info_at(c, t, at(i, 'plus GST', -0.2), [('+ 18% GST = ₹321', 64, INK)], 760, RED)
    if t > at(i, 'About', -0.2):
        place(c, pill_text('≈ ₹2,100 EXTRA IN 1 MONTH', RED, (255, 255, 255), 70).copy() if False else pill_text('ABOUT ₹2,100 IN 1 MONTH', RED, (255, 255, 255), 70),
              540, 960, 0.6 + 0.4 * eback(prog(t, at(i, 'About', -0.2), 0.3)), -3)
    if t > at(i, 'new purchases', -0.2):
        place(c, text_img('+ new buys lose the free period', 'pop', 40, INK), 370, 1100, 1, 0, clamp((t - at(i, 'new purchases', -0.2)) * 3))
    actor(c, t, i, 'arjun_shock', 870, 320, base=1480, bob=False, enter=(at(i, 'new purchases', -0.3), 300))
    caption(c, t, i, 1560, 42, by_sentence=True)
    place(c, text_img('My example calc · rate up to 3.75%/month (BankBazaar, Nov 2026) · varies by card', 'osw5', 22, GREY), 540, 1840)


def s8(c, t):
    i = 8
    c.alpha_composite(room_bg())
    actor(c, t, i, 'arjun_worried', 540, 840)
    bubble(c, t, i, 380, 540, size=58)


def s9(c, t):
    i = 9
    c.alpha_composite(data_bg())
    head(c, t, i, 'OPTION X: MISSED PAYMENT', RED)
    chips = [('Late fee', 'LATE FEE'), ('plus interest', '+ INTEREST'), ('plus GST', '+ GST')]
    for k, (ph, s) in enumerate(chips):
        tk = at(i, ph, -0.2)
        if t > tk: place(c, pill_text(s, RED, (255, 255, 255), 60), 220 + k * 320, 420, 0.6 + 0.4 * eback(prog(t, tk, 0.3)), [-4, 3, -2][k])
    info_at(c, t, at(i, 'Three days', -0.2), [('3 DAYS PAST DUE DATE', 66, INK), ('can be reported to credit bureaus', 42, INK)], 680, RED)
    tk = at(i, 'CIBIL', -0.3)
    if t > tk:
        d = ImageDraw.Draw(c); cx, cy, R = 540, 1160, 230
        d.pieslice((cx - R, cy - R, cx + R, cy + R), 180, 360, fill=(235, 235, 240), outline=INK, width=6)
        for a0, a1, col in [(180, 240, RED), (240, 300, YEL), (300, 360, (46, 160, 90))]:
            d.pieslice((cx - R + 26, cy - R + 26, cx + R - 26, cy + R - 26), a0, a1, fill=col)
        d.pieslice((cx - 110, cy - 110, cx + 110, cy + 110), 180, 360, fill=(250, 246, 238))
        q = eo(prog(t, tk + 0.2, 1.2)); ang = math.radians(330 - 120 * q)
        d.line((cx, cy, cx + 190 * math.cos(ang), cy + 190 * math.sin(ang)), fill=INK, width=12)
        place(c, text_img('CIBIL SCORE', 'anton', 50, INK), cx, cy + 60)
    caption(c, t, i, 1600, 42, by_sentence=True)
    place(c, text_img('Source: RBI Master Direction on credit cards (2022)', 'osw5', 22, GREY), 540, 1840)


def s10(c, t):
    i = 10
    c.alpha_composite(data_bg())
    head(c, t, i, 'OPTION C: CONVERT TO EMI', (46, 120, 200))
    d = ImageDraw.Draw(c); base = 1160
    rows = [('PAY FULL', 0, (46, 160, 90), STARTS[i] + 0.3), ('EMI 6 MONTHS', 3200, (46, 120, 200), at(i, 'Six months', -0.2)),
            ('MIN DUE, 6 MONTHS*', 13000, RED, at(i, 'costs', -0.2))]
    for k, (lab, v, col, tk) in enumerate(rows):
        if t < tk: continue
        x = 230 + k * 310; q = eo(prog(t, tk, 0.8)); hg = max(8, int(v / 13000 * 560 * q))
        d.rounded_rectangle((x - 110, base - hg, x + 110, base), 14, fill=col, outline=INK, width=5)
        place(c, text_img(f'₹{int(v * q):,}' + (' +' if k == 2 else ''), 'anton', 54, INK), x, base - hg - 40)
        place(c, text_img(lab, 'osw', 34, GREY), x, base + 40)
    d.line((80, base, 1000, base), fill=INK, width=5)
    place(c, text_img('extra cost on a ₹50,000 bill', 'pop', 40, INK), 540, 1290)
    caption(c, t, i, 1560, 42, by_sentence=True)
    place(c, text_img('*my calc: 5% min due at 3.75%/mo + GST, you STILL owe ₹47,658 · EMI ~15%/yr + 1% fee + GST', 'osw5', 21, GREY), 540, 1840)


def s11(c, t):
    i = 11
    c.alpha_composite(room_bg())
    actor(c, t, i, 'paati_happy', 540, 800)
    bubble(c, t, i, 380, 540)


CARDS = [('First card', 'LIFETIME FREE', 'your first card', (120, 130, 150)), ('Shop online', 'CASHBACK', 'online shoppers', (46, 160, 90)),
         ('Big spends', 'REWARDS', 'big monthly spenders', (125, 60, 150)), ('Travel', 'TRAVEL', 'lounges & air miles', (30, 40, 70)),
         ('Ride daily', 'FUEL', 'daily riders', (230, 120, 30)), ('No credit', 'SECURED (FD)', 'no credit history', (196, 160, 40))]


def s12(c, t):
    i = 12
    c.alpha_composite(data_bg())
    head(c, t, i, 'WHICH CARD SUITS YOU?')
    for k, (ph, name, who, col) in enumerate(CARDS):
        tk = at(i, ph, -0.25)
        if t < tk: continue
        x = 290 + (k % 2) * 500; y = 470 + (k // 2) * 360
        p = prog(t, tk, 0.4)
        place(c, cc_img(col, 380), x, y + (1 - eo(p)) * 200, 0.5 + 0.5 * eback(p), [-6, 5][k % 2])
        place(c, text_img(name, 'anton', 52, INK), x, y + 150, 1, 0, clamp(p * 3))
        place(c, text_img(who, 'osw5', 30, GREY), x, y + 198, 1, 0, clamp(p * 3))
    caption(c, t, i, 1580, 42, by_sentence=True)


def s13(c, t):
    i = 13
    c.alpha_composite(data_bg())
    head(c, t, i, 'GOOD vs BAD')
    good = [('interest free', 'INTEREST-FREE CREDIT'), ('rewards', 'REWARDS'), ('better score', 'BETTER CREDIT SCORE')]
    bad = [('forty percent', '40%+ INTEREST'), ('overspending', 'OVERSPENDING'), ('fees', 'FEES'), ('cash withdrawals', 'COSTLY CASH WITHDRAWAL')]
    place(c, text_img('GOOD', 'anton', 72, (46, 160, 90)), 290, 360); place(c, text_img('BAD', 'anton', 72, RED), 790, 360)
    for col_items, x, colr in ((good, 290, (46, 160, 90)), (bad, 790, RED)):
        for k, (ph, s) in enumerate(col_items):
            tk = at(i, ph, -0.25)
            if t < tk: continue
            p = prog(t, tk, 0.35)
            place(c, pill_text(s, colr, (255, 255, 255), 40), x, 500 + k * 150, 0.6 + 0.4 * eback(p), 0)
    caption(c, t, i, 1560, 42, by_sentence=True)


def s14(c, t):
    i = 14
    c.alpha_composite(room_bg())
    actor(c, t, i, 'thatha_happy', 260, 640)
    rules = [('Pay the full', '1. PAY FULL + AUTOPAY', (46, 160, 90)), ('Use less', '2. USE < 30% OF LIMIT', (46, 120, 200)), ('never withdraw', '3. NO CASH ON CARD', RED)]
    for k, (ph, s, col) in enumerate(rules):
        tk = at(i, ph, -0.25)
        if t < tk: continue
        p = prog(t, tk, 0.4)
        place(c, pill_text(s, col, (255, 255, 255), 50), 660 + (1 - eo(p)) * 500, 700 + k * 190, 1, [-3, 2, -2][k])
    bubble(c, t, i, 330, 260, size=42)


def s15(c, t):
    i = 15
    c.alpha_composite(room_bg())
    place(c, family_print(), 540, 860, 1, -3)
    tf = at(i, 'Follow', -0.1)
    if t > tf: place(c, follow_btn(), 540, 1300, 0.6 + 0.4 * eback(prog(t, tf, 0.35)), 2)
    if t > at(i, 'never pay', -0.2):
        place(c, pill_text('NEVER PAY ONLY THE MINIMUM DUE', RED, (255, 255, 255), 56), 540, 1480, 1, -2, clamp((t - at(i, 'never pay', -0.2)) * 3))
    caption(c, t, i, 330, by_sentence=True)
    src(c, 'Characters are fictional · Education only · Not financial advice', 1880)


SCENES = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15]


def slam_times():
    return [at(0, 'Here', -0.1), at(3, 'Only if', -0.1), at(7, 'About', -0.2), at(9, 'CIBIL', -0.3)]


def footer(c):
    d = ImageDraw.Draw(c)
    d.rectangle((0, 1888, W, H), fill=(20, 22, 30, 255))
    place(c, text_img('Not financial advice · Education only · @moneyincloud', 'osw5', 24, (230, 230, 236)), 540, 1904)


def render(t):
    LOOP = 0.5
    if t > DUR - LOOP:
        a = _render(t); b = _render(1.0, loop=True); q = eio((t - (DUR - LOOP)) / LOOP)
        return (a * (1 - q) + b * q).astype(np.uint8)
    return _render(t)


def _render(t, loop=False):
    i = scene_at(t)
    c = Image.new('RGBA', (W, H), (255, 255, 255, 255))
    st = STARTS[i]; en = STARTS[i + 1] if i + 1 < len(STARTS) else DUR
    SCENES[i](c, t)
    z = 1.0 + 0.03 * clamp((t - st) / (en - st)) + (0.05 * math.exp(-(t - st) * 9) if i > 0 else 0)
    sx = sy = 0
    for ts in slam_times():
        if 0 <= t - ts < 0.35:
            k = math.exp(-(t - ts) * 14) * 10
            sx += k * math.sin((t - ts) * 90); sy += k * math.cos((t - ts) * 77)
    cw, ch = W / z, H / z
    cx, cy = W / 2 + sx, H * 0.5 + sy
    c = c.transform((W, H), Image.EXTENT, (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2), Image.BICUBIC)
    if i > 0 and t - st < 0.08:
        c = Image.blend(c, Image.new('RGBA', (W, H), (255, 255, 255, 255)), 0.5 * (1 - (t - st) / 0.08))
    if i != 15: footer(c)
    return np.asarray(c.convert('RGB'))
