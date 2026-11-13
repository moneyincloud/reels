"""Tamil voice (vidIQ Sarah) + English on-screen text. Six high-dividend stocks: ₹1 lakh -> yearly dividend cheat sheet. Light mint theme, narrator am_michael."""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, textwrap, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from lib import *
from scenes import stamp_c
from fridge import follow_btn

SH = ROOT + 'divi6ta/'
CAST_DIR = ROOT + 'brand/cast_real/'
LINES = json.load(open(SH + 'lines.json'))
TASCRIPT = [l['text'] for l in LINES]  # Tamil voice text: used only for timing
SCRIPT = ["Nobody tells you these six stocks pay you every year.",
          "Coal India, about 6.6%. Invest ₹1 lakh, get ₹6,600 a year.",
          "Wipro, 5.9%. ONGC, 5.7%.",
          "Indian Oil, 5.5%. BPCL, 5.4%. ITC, 5.1%.",
          "But there's a catch. Dividends are taxed at your slab rate. A high yield can mean the price fell.",
          "Dividends aren't guaranteed. A company can cut them any year.",
          "Which stock do you hold? Comment DIVIDEND and follow!"]  # English on-screen captions
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


FONTS['ta'] = FD + 'noto-sans-tamil-tamil-800-normal.woff'
import lib as _lib
_TA = lambda ch: '\u0b80' <= ch <= '\u0bff'


@functools.lru_cache(2048)
def text_img(s, fn, size, fill, track=0):
    if not any(_TA(ch) for ch in s):
        return _lib.text_img(s, fn, size, fill, track)
    runs = []; cur = ''; ct = None
    for ch in s:
        tt = ct if ch == ' ' else (False if ch in '-.,?!\'"' else _TA(ch))
        if ct is None or tt == ct: cur += ch
        else: runs.append((cur, ct)); cur = ch
        ct = tt
    runs.append((cur, ct))
    ims = [_lib.text_img(r, 'ta' if tt else fn, int(size * 0.82) if tt else size, fill) for r, tt in runs]
    pad = int(size * 0.12); h = max(im.size[1] for im in ims)
    w = sum(im.size[0] - 2 * pad for im in ims) + 2 * pad
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0)); x = 0
    for im in ims:
        out.alpha_composite(im, (x, (h - im.size[1]) // 2)); x += im.size[0] - 2 * pad
    return out


def text_w(s, fn, size, track=0):
    return text_img(s, fn, size, (0, 0, 0), track).size[0] - 2 * int(size * 0.12)


TAMAP = {(1, 'sixty six'): 'ஆறாயிரத்து', (4, 'taxed'): 'tax', (4, 'high yield'): 'Yield', (4, 'price fell'): 'விலை',
         (5, 'never guaranteed'): 'guarantee', (5, 'cut them'): 'குறைக்கலாம்', (6, 'Comment'): 'comment'}


def at(i, phrase, off=0.0):
    phrase = TAMAP.get((i, phrase), phrase)
    s = TASCRIPT[i]; k = s.find(phrase)
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


TEAL = (14, 128, 128); TEAL2 = (20, 160, 150); GREEN = (46, 160, 90); BLUE = (46, 120, 200)


@functools.lru_cache(None)
def teal_bg():
    im = Image.new('RGB', (W, H), (12, 110, 112)); d = ImageDraw.Draw(im)
    cx, cy = 540, 1150
    for k in range(28):
        a0 = k * 2 * math.pi / 28; a1 = a0 + math.pi / 28
        d.polygon([(cx, cy), (cx + 2600 * math.cos(a0), cy + 2600 * math.sin(a0)), (cx + 2600 * math.cos(a1), cy + 2600 * math.sin(a1))], fill=(22, 132, 132))
    g = Image.radial_gradient('L').resize((2400, 2400)).crop((660, 50, 1740, 1970))
    im = Image.composite(im, Image.new('RGB', im.size, (6, 60, 64)), g.point(lambda v: 255 - int(v * 0.8)))
    return im.convert('RGBA')


@functools.lru_cache(None)
def app_frame(title, col=TEAL, w=760, h=980):
    im = Image.new('RGBA', (w + 18, h + 18), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((18, 18, w + 17, h + 17), 60, fill=(0, 0, 0, 90))
    d.rounded_rectangle((0, 0, w - 1, h - 1), 60, fill=(25, 25, 32), outline=INK, width=6)
    d.rounded_rectangle((20, 20, w - 21, h - 21), 44, fill=(248, 250, 252))
    d.rounded_rectangle((20, 20, w - 21, 150), 44, fill=col); d.rectangle((20, 100, w - 21, 150), fill=col)
    tt = text_img(title, 'anton', 50, (255, 255, 255)); im.alpha_composite(tt, (w // 2 - tt.size[0] // 2, 52))
    return im


def row(d, im, y, txt, sub, chip=None, chip_col=GREEN, w=760):
    d.rounded_rectangle((50, y, w - 50, y + 130), 24, fill=(255, 255, 255), outline=(215, 220, 228), width=3)
    im.alpha_composite(text_img(txt, 'osw', 40, INK), (80, y + 16))
    im.alpha_composite(text_img(sub, 'osw5', 28, GREY), (80, y + 74))
    if chip:
        ct = text_img(chip, 'anton', 36, (255, 255, 255))
        d.rounded_rectangle((w - 80 - ct.size[0] - 30, y + 36, w - 80, y + 96), 30, fill=chip_col)
        im.alpha_composite(ct, (w - 80 - ct.size[0] - 15, y + 42))


def step_screen(c, t, k, t0):
    """screens for the 5 steps; k = 1..5"""
    if t < t0: return
    p = prog(t, t0, 0.45)
    titles = {1: 'STEP 1 · YOUR PROFILE', 2: 'STEP 2 · NEW JOBS TODAY', 3: 'STEP 3 · MATCH SCORE', 4: 'STEP 4 · TAILORED RESUME', 5: 'STEP 5 · TRACKER'}
    im = app_frame(titles[k]).copy(); d = ImageDraw.Draw(im); lt = t - t0
    if k == 1:
        items = [('Resume', 'DevOps · 5 yrs · AWS, Azure'), ('Skills', 'Kubernetes, Terraform, CI/CD'), ('Salary goal', '₹18 L+ a year'), ('City', 'Chennai / Remote')]
        for j, (a, b) in enumerate(items):
            if lt > 0.3 + j * 0.45: row(d, im, 190 + j * 165, a, b, '✓' if False else 'OK', GREEN)
    elif k == 2:
        jobs = [('DevOps Engineer', 'Chennai · posted 2h ago'), ('Cloud Engineer', 'Remote · posted 5h ago'), ('SRE', 'Bengaluru · posted today'), ('Platform Engineer', 'Chennai · posted today'), ('Build & Release', 'Hyderabad · posted today')]
        for j, (a, b) in enumerate(jobs):
            if lt > 0.2 + j * 0.3: row(d, im, 190 + j * 150, a, b, 'NEW', BLUE)
    elif k == 3:
        jobs = [('DevOps Engineer', 92, GREEN), ('Cloud Engineer', 85, GREEN), ('SRE', 74, (230, 160, 30)), ('Data Analyst', 31, RED), ('Java Developer', 22, RED)]
        for j, (a, s, col) in enumerate(jobs):
            if lt > 0.2 + j * 0.35:
                row(d, im, 190 + j * 150, a, 'match with your profile' if s >= 50 else 'weak match: skipped', f'{s}%', col)
                if s < 50: d.line((80, 190 + j * 150 + 65, 520, 190 + j * 150 + 65), fill=RED, width=6)
    elif k == 4:
        d.rounded_rectangle((60, 190, 700, 920), 20, fill=(255, 255, 255), outline=(215, 220, 228), width=3)
        im.alpha_composite(text_img('YOU · DevOps Engineer', 'anton', 44, INK), (90, 215))
        lines = [('Matched to this job:', INK), ('✔ CI/CD pipelines (Azure DevOps)', GREEN), ('✔ Terraform on AWS', GREEN), ('✔ Kubernetes deployments', GREEN), ('Only REAL experience', BLUE), ('No fake skills added', RED)]
        for j, (s, col) in enumerate(lines):
            if lt > 0.3 + j * 0.4:
                s2 = s.replace('✔', '+')
                im.alpha_composite(text_img(s2, 'osw', 38, col), (90, 310 + j * 95))
    elif k == 5:
        rows_ = [('DevOps Engineer', 'Applied 3 Nov', 'INTERVIEW', GREEN), ('Cloud Engineer', 'Applied 4 Nov', 'FOLLOW UP', (230, 160, 30)), ('SRE', 'Applied 5 Nov', 'WAITING', BLUE), ('Platform Eng.', 'Applied 6 Nov', 'APPLIED', GREY)]
        for j, (a, b, ch, col) in enumerate(rows_):
            if lt > 0.2 + j * 0.4: row(d, im, 190 + j * 165, a, b, ch, col)
    place(c, im, 540 + (1 - eo(p)) * 900, 860, 1, 0)


@functools.lru_cache(None)
def resume_card():
    w, h = 300, 400
    im = Image.new('RGBA', (w + 10, h + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((10, 10, w + 9, h + 9), fill=(0, 0, 0, 70)); d.rectangle((0, 0, w - 1, h - 1), fill=(255, 255, 255), outline=INK, width=4)
    im.alpha_composite(text_img('RESUME', 'anton', 44, INK), (24, 20))
    d.ellipse((24, 90, 104, 170), fill=(200, 205, 215))
    for k in range(8): d.rectangle((24 if k > 1 else 120, 100 + k * 34 if k < 2 else 160 + k * 26, w - 30 - (k % 3) * 30, 112 + k * 34 if k < 2 else 172 + k * 26), fill=(205, 210, 220))
    im.alpha_composite(text_img('COPY x200', 'anton', 30, RED), (24, h - 56))
    return im


@functools.lru_cache(64)
def pose(pid, h):
    im = Image.open(ROOT + f'host/poses_x4/p{pid:02d}.png').convert('RGBA')
    w = int(im.size[0] * h / im.size[1]); im = im.resize((w, h), Image.LANCZOS)
    out = Image.new('RGBA', (w + 30, h + 30), (0, 0, 0, 0))
    sh = Image.new('RGBA', im.size, (0, 0, 0, 255)); sh.putalpha(im.getchannel('A').point(lambda v: v * 80 // 255))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)), (14, 18)); out.alpha_composite(im, (0, 0))
    return out


def host(c, t, cues, cx, cy, h=640, rot=0):
    pid, t0 = cues[0][1], -9
    for tc, p in cues:
        if t >= tc: pid, t0 = p, tc
    s = 0.85 + 0.15 * eback(clamp((t - t0) / 0.25)) if t0 > -9 else 1.0
    place(c, pose(pid, h), cx, cy + 6 * math.sin(t * 2.4), s, rot + 1.5 * math.sin(t * 1.3))


BLU = (30, 90, 190); BLU2 = (40, 110, 215)


@functools.lru_cache(None)
def blue_bg():
    im = Image.new('RGB', (W, H), (26, 80, 170)); d = ImageDraw.Draw(im)
    cx, cy = 540, 1150
    for k in range(28):
        a0 = k * 2 * math.pi / 28; a1 = a0 + math.pi / 28
        d.polygon([(cx, cy), (cx + 2600 * math.cos(a0), cy + 2600 * math.sin(a0)), (cx + 2600 * math.cos(a1), cy + 2600 * math.sin(a1))], fill=(36, 96, 190))
    g = Image.radial_gradient('L').resize((2400, 2400)).crop((660, 50, 1740, 1970))
    im = Image.composite(im, Image.new('RGB', im.size, (10, 36, 90)), g.point(lambda v: 255 - int(v * 0.8)))
    return im.convert('RGBA')


@functools.lru_cache(None)
def shelf_bg():
    im = Image.new('RGBA', (W, H), (236, 244, 252, 255)); d = ImageDraw.Draw(im)
    for y in (560, 1180):
        d.rectangle((0, y, W, y + 34), fill=(190, 150, 100)); d.rectangle((0, y + 34, W, y + 50), fill=(150, 110, 70))
    for x in range(0, W, 120): d.line((x, 0, x, H), fill=(226, 236, 248), width=2)
    return im


def med_icon(kind, s=200):
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im); o = INK; w = max(4, s // 40)
    if kind == 'pill':
        d.rounded_rectangle((s * .1, s * .35, s * .9, s * .65), s * .15, fill=(255, 255, 255), outline=o, width=w)
        d.rounded_rectangle((s * .1, s * .35, s * .5, s * .65), s * .15, fill=(240, 80, 70), outline=o, width=w)
    elif kind == 'tablet':
        for k, (x, y) in enumerate(((.3, .35), (.68, .4), (.48, .7))):
            d.ellipse((s * (x - .17), s * (y - .17), s * (x + .17), s * (y + .17)), fill=(255, 255, 255), outline=o, width=w)
            d.line((s * (x - .12), s * y, s * (x + .12), s * y), fill=o, width=w)
    elif kind == 'inhaler':
        d.rounded_rectangle((s * .3, s * .1, s * .62, s * .7), s * .08, fill=(80, 160, 230), outline=o, width=w)
        d.rounded_rectangle((s * .2, s * .6, s * .8, s * .85), s * .06, fill=(255, 255, 255), outline=o, width=w)
    elif kind == 'tube':
        d.polygon([(s * .15, s * .2), (s * .7, s * .2), (s * .62, s * .85), (s * .23, s * .85)], fill=(250, 250, 255), outline=o)
        d.rectangle((s * .7, s * .3, s * .88, s * .45), fill=(240, 160, 40), outline=o, width=w)
        d.rectangle((s * .25, s * .4, s * .6, s * .55), fill=(60, 170, 110))
    elif kind == 'syringe':
        d.rounded_rectangle((s * .2, s * .38, s * .72, s * .62), s * .04, fill=(220, 240, 255), outline=o, width=w)
        d.rectangle((s * .24, s * .42, s * .5, s * .58), fill=(90, 190, 240))
        d.line((s * .72, s * .5, s * .95, s * .5), fill=o, width=w); d.rectangle((s * .05, s * .44, s * .2, s * .56), fill=(200, 200, 210), outline=o, width=w)
    elif kind == 'vial':
        d.rounded_rectangle((s * .3, s * .3, s * .7, s * .88), s * .06, fill=(230, 245, 255), outline=o, width=w)
        d.rectangle((s * .33, s * .55, s * .67, s * .85), fill=(110, 200, 240)); d.rectangle((s * .34, s * .14, s * .66, s * .3), fill=(150, 60, 160), outline=o, width=w)
    elif kind == 'heart':
        d.ellipse((s * .12, s * .2, s * .52, s * .58), fill=(230, 60, 70)); d.ellipse((s * .48, s * .2, s * .88, s * .58), fill=(230, 60, 70))
        d.polygon([(s * .14, s * .46), (s * .86, s * .46), (s * .5, s * .88)], fill=(230, 60, 70))
    elif kind == 'eye':
        d.ellipse((s * .08, s * .3, s * .92, s * .7), fill=(255, 255, 255), outline=o, width=w)
        d.ellipse((s * .36, s * .34, s * .64, s * .66), fill=(60, 120, 200)); d.ellipse((s * .45, s * .43, s * .55, s * .57), fill=o)
    elif kind == 'test':
        d.rounded_rectangle((s * .1, s * .38, s * .9, s * .62), s * .1, fill=(255, 255, 255), outline=o, width=w)
        d.rectangle((s * .45, s * .43, s * .62, s * .57), fill=(230, 240, 250), outline=o, width=w // 2)
        d.line((s * .5, s * .44, s * .5, s * .56), fill=(220, 60, 120), width=w); d.line((s * .57, s * .44, s * .57, s * .56), fill=(220, 60, 120), width=w)
    elif kind == 'globe':
        d.ellipse((s * .12, s * .12, s * .88, s * .88), fill=(90, 170, 240), outline=o, width=w)
        d.ellipse((s * .3, s * .25, s * .55, s * .5), fill=(80, 180, 100)); d.ellipse((s * .5, s * .5, s * .75, s * .75), fill=(80, 180, 100))
    elif kind == 'drop':
        d.polygon([(s * .5, s * .1), (s * .25, s * .55), (s * .75, s * .55)], fill=(80, 170, 240)); d.ellipse((s * .25, s * .38, s * .75, s * .88), fill=(80, 170, 240))
    elif kind == 'bug':
        d.ellipse((s * .28, s * .25, s * .72, s * .8), fill=(120, 190, 80), outline=o, width=w)
        for k in range(3):
            y = s * (.38 + k * .14); d.line((s * .1, y, s * .3, y), fill=o, width=w); d.line((s * .7, y, s * .9, y), fill=o, width=w)
        d.line((s * .2, s * .1, s * .9, s * .9), fill=(230, 50, 50), width=w * 2)
    elif kind == 'spray':
        d.rounded_rectangle((s * .3, s * .35, s * .7, s * .9), s * .08, fill=(255, 255, 255), outline=o, width=w)
        d.rectangle((s * .42, s * .15, s * .58, s * .35), fill=(80, 160, 230), outline=o, width=w)
        for k in range(4): d.ellipse((s * (.62 + k * .06), s * (.1 + k * .03), s * (.66 + k * .06), s * (.14 + k * .03)), fill=(80, 160, 230))
    return im


@functools.lru_cache(None)
def chip(label, icon, col):
    ic = med_icon(icon, 130); tt = text_img(label, 'anton', 50, INK)
    w = 150 + tt.size[0] + 40; h = 150
    im = Image.new('RGBA', (w + 10, h + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 10, w + 9, h + 9), 30, fill=INK); d.rounded_rectangle((0, 0, w - 1, h - 1), 30, fill=(255, 255, 255), outline=col, width=7)
    im.alpha_composite(ic, (12, 10)); im.alpha_composite(tt, (150, h // 2 - tt.size[1] // 2))
    return im

PINK = (200, 30, 90); PINK2 = (230, 60, 120)


@functools.lru_cache(None)
def pink_bg():
    im = Image.new('RGB', (W, H), (176, 26, 80)); d = ImageDraw.Draw(im)
    cx, cy = 540, 1150
    for k in range(28):
        a0 = k * 2 * math.pi / 28; a1 = a0 + math.pi / 28
        d.polygon([(cx, cy), (cx + 2600 * math.cos(a0), cy + 2600 * math.sin(a0)), (cx + 2600 * math.cos(a1), cy + 2600 * math.sin(a1))], fill=(196, 40, 98))
    g = Image.radial_gradient('L').resize((2400, 2400)).crop((660, 50, 1740, 1970))
    im = Image.composite(im, Image.new('RGB', im.size, (90, 10, 44)), g.point(lambda v: 255 - int(v * 0.8)))
    return im.convert('RGBA')


def prod_icon(kind, s=220):
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im); o = INK; w = max(4, s // 40)
    if kind == 'pack':
        for k in range(8):
            y = s * .12 + k * (s * .76 / 7)
            d.line((s * .12, y, s * .16, y), fill=o, width=2)
        d.rectangle((s * .14, s * .14, s * .86, s * .86), fill=(235, 50, 100), outline=o, width=w)
        d.ellipse((s * .3, s * .3, s * .7, s * .7), outline=(255, 200, 220), width=w)
        d.ellipse((s * .38, s * .38, s * .62, s * .62), outline=(255, 200, 220), width=w // 2)
    elif kind == 'pack2':
        d.rectangle((s * .14, s * .14, s * .86, s * .86), fill=(130, 60, 180), outline=o, width=w)
        d.ellipse((s * .3, s * .3, s * .7, s * .7), outline=(230, 210, 255), width=w)
    elif kind == 'lube':
        d.rounded_rectangle((s * .3, s * .3, s * .7, s * .9), s * .08, fill=(120, 200, 240), outline=o, width=w)
        d.rectangle((s * .4, s * .12, s * .6, s * .3), fill=(255, 255, 255), outline=o, width=w)
    elif kind == 'perfume':
        d.rounded_rectangle((s * .22, s * .38, s * .78, s * .9), s * .1, fill=(250, 200, 120), outline=o, width=w)
        d.rectangle((s * .42, s * .2, s * .58, s * .38), fill=(60, 60, 70), outline=o, width=w)
        d.ellipse((s * .4, s * .55, s * .6, s * .75), outline=(255, 255, 255), width=w)
    else:
        return med_icon(kind, s)
    return im


def big_num(c, t, t0, s, col, cx, cy, size=200):
    if t < t0: return
    place(c, text_img(s, 'anton', size, col), cx, cy, 0.6 + 0.4 * eback(prog(t, t0, 0.35)), -3)


def card_at(c, t, t0, lines, x, y, col, w=900, rot=-1.5):
    if t < t0: return
    p = prog(t, t0, 0.4)
    place(c, info(tuple(lines), w, col), x + (1 - eo(p)) * 900, y, 1, rot, clamp(p * 3))


ORANGE = (235, 110, 40); BLUEB = (40, 110, 210); SKIN = (232, 180, 140); HAIR = (40, 30, 30)
STY = ['COMIC ART', 'COMIC ART', 'SYNTHWAVE', 'DOMINO REVEAL', 'ISOMETRIC', 'GLOW ATOM', 'MATHS DIAGRAM', '3D DATA CHART', 'PAPER-CUT', 'FLAT VECTOR']
NUM = [1, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def style_chip(c, i, dark=False):
    s = f'STYLE {NUM[i]}/9 · {STY[i]}'
    place(c, pill_text(s, (255, 255, 255) if dark else INK, INK if dark else (255, 255, 255), 34), 540, 120, 1, 0)


@functools.lru_cache(None)
def kid(who, mood='happy', s=300, outline=INK, ow=8, flat=False):
    shirt = ORANGE if who == 'A' else BLUEB
    im = Image.new('RGBA', (s, int(s * 1.25)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    o = None if flat else outline; w = 0 if flat else ow
    d.rounded_rectangle((s * .12, s * .78, s * .88, s * 1.24), s * .2, fill=shirt, outline=o, width=w)
    d.ellipse((s * .2, s * .12, s * .8, s * .78), fill=SKIN, outline=o, width=w)
    d.chord((s * .18, s * .06, s * .82, s * .5), 180, 360, fill=HAIR)
    if who == 'B': d.rectangle((s * .22, s * .26, s * .78, s * .3), fill=HAIR)
    for ex in (.39, .61):
        d.ellipse((s * (ex - .045), s * .42, s * (ex + .045), s * .51), fill=INK)
    if mood == 'happy': d.arc((s * .36, s * .5, s * .64, s * .68), 15, 165, fill=INK, width=max(4, s // 40))
    elif mood == 'sad': d.arc((s * .36, s * .6, s * .64, s * .76), 200, 340, fill=INK, width=max(4, s // 40))
    else: d.ellipse((s * .45, s * .58, s * .55, s * .68), fill=INK)
    tl = text_img(who, 'anton', int(s * .2), (255, 255, 255)); im.alpha_composite(tl, (int(s * .5 - tl.size[0] / 2), int(s * .9)))
    return im


def neon(im, col, r=14):
    a = im.getchannel('A'); g = Image.new('RGBA', im.size, col + (0,)); g.putalpha(a.filter(ImageFilter.GaussianBlur(r)))
    out = Image.new('RGBA', im.size, (0, 0, 0, 0)); out.alpha_composite(g); out.alpha_composite(g); out.alpha_composite(im); return out


@functools.lru_cache(None)
def neon_text(s, col, size):
    t_ = text_img(s, 'anton', size, (255, 255, 255))
    pad = 40; im = Image.new('RGBA', (t_.size[0] + pad * 2, t_.size[1] + pad * 2), (0, 0, 0, 0)); im.alpha_composite(t_, (pad, pad))
    return neon(im, col, 16)


TEALP = (42, 140, 140); CORAL = (232, 96, 76); MUST = (238, 186, 60); NAVYP = (34, 52, 92); HL = (255, 230, 60)


@functools.lru_cache(None)
def paper_bg(col=(244, 236, 220)):
    rng = np.random.default_rng(7)
    a = np.zeros((H, W, 3), np.float32) + np.array(col, np.float32)
    a += rng.normal(0, 6, (H, W, 1)); a += rng.normal(0, 3, (H, W, 3))
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA')
    d = ImageDraw.Draw(im)
    for k in range(10):
        y = rng.integers(0, H); d.line((0, y, W, y + rng.integers(-40, 40)), fill=col[:3] + (0,), width=1)
    return im


def torn(w, h, col, seed=1, edge=10):
    rng = np.random.default_rng(seed)
    im = Image.new('RGBA', (w + 30, h + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pts = []
    for x in range(0, w + 1, 18): pts.append((x, rng.integers(0, edge)))
    for y in range(0, h + 1, 18): pts.append((w - rng.integers(0, edge), y))
    for x in range(w, -1, -18): pts.append((x, h - rng.integers(0, edge)))
    for y in range(h, -1, -18): pts.append((rng.integers(0, edge), y))
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).polygon([(x + 12, y + 14) for x, y in pts], fill=(0, 0, 0, 80))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    d.polygon(pts, fill=col)
    return im


@functools.lru_cache(None)
def note(lines, col=(255, 252, 240), w=880, seed=3, tape=True):
    rows = [text_img(s, f, sz, c_) for s, f, sz, c_ in lines]
    h = sum(r.size[1] for r in rows) + 26 * len(rows) + 50
    im = torn(w, h, col, seed)
    y = 30
    for r in rows:
        if r.size[0] > w - 70: r = r.resize((w - 70, int(r.size[1] * (w - 70) / r.size[0])), Image.LANCZOS)
        im.alpha_composite(r, (int(w / 2 - r.size[0] / 2), y)); y += r.size[1] + 26
    if tape:
        tp = Image.new('RGBA', (170, 50), (240, 230, 190, 190)); tp = tp.rotate(-8, expand=True)
        im.alpha_composite(tp, (int(w / 2 - 85), 0))
    return im


def note_at(c, t, t0, lines, x, y, col=(255, 252, 240), w=880, rot=-2, seed=3):
    if t < t0: return
    p = prog(t, t0, 0.35)
    place(c, note(tuple(lines), col, w, seed), x, y + (1 - eo(p)) * 60, 0.85 + 0.15 * eback(p), rot, clamp(p * 3))


def highlight(c, t, t0, x0, y0, x1, y1, col=HL, dur=0.45):
    if t < t0: return
    q = eo(clamp((t - t0) / dur)); ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    d.rectangle((x0, y0, x0 + (x1 - x0) * q, y1), fill=col + (140,)); c.alpha_composite(ov)


def marker_circle(c, t, t0, cx, cy, rx, ry, col=(220, 40, 40), dur=0.6):
    if t < t0: return
    q = clamp((t - t0) / dur); d = ImageDraw.Draw(c)
    pts = [(cx + rx * math.cos(a) * (1 + 0.04 * math.sin(a * 3)), cy + ry * math.sin(a)) for a in np.linspace(-2.2, -2.2 + 2 * math.pi * 1.08 * q, 80)]
    if len(pts) > 1: d.line(pts, fill=col, width=9, joint='curve')


def vox_title(c, t, t0, s, y=240, col=INK, size=86):
    if t < t0: return
    place(c, text_img(s, 'pf', size, col), 540, y, 1, 0, clamp((t - t0) * 3))


def sticker(c, t, cues, x, y, h=420, rot=-3):
    host(c, t, cues, x, y, h, rot)


@functools.lru_cache(None)
def person_cut(letter, col, s=240):
    im = Image.new('RGBA', (s, int(s * 1.3)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((s * .1, s * .8, s * .9, s * 1.28), s * .25, fill=col)
    d.ellipse((s * .22, s * .12, s * .78, s * .74), fill=SKIN)
    if letter == 'P': d.chord((s * .16, s * .04, s * .84, s * .72), 160, 380, fill=HAIR); d.ellipse((s * .66, s * .1, s * .9, s * .34), fill=HAIR)
    else: d.chord((s * .2, s * .06, s * .8, s * .5), 180, 360, fill=HAIR)
    for ex in (.4, .6): d.ellipse((s * (ex - .04), s * .4, s * (ex + .04), s * .48), fill=INK)
    d.arc((s * .38, s * .48, s * .62, s * .64), 15, 165, fill=INK, width=5)
    t_ = text_img(letter, 'anton', int(s * .22), (255, 255, 255)); im.alpha_composite(t_, (int(s * .5 - t_.size[0] / 2), int(s * .9)))
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh.putalpha(im.getchannel('A').point(lambda v: v * 90 // 255))
    out = Image.new('RGBA', (im.size[0] + 20, im.size[1] + 20), (0, 0, 0, 0)); out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)), (10, 14))
    wht = Image.new('RGBA', im.size, (255, 255, 255, 0)); wht.putalpha(im.getchannel('A').filter(ImageFilter.MaxFilter(13)))
    out.alpha_composite(wht, (0, 0)); out.alpha_composite(im, (0, 0)); return out


@functools.lru_cache(None)
def share_chit(lab='CO. X', col=CORAL, w=120):
    im = Image.new('RGBA', (w, int(w * .7)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, w - 1, int(w * .7) - 1), fill=(255, 250, 235), outline=col, width=5)
    t_ = text_img(lab, 'anton', int(w * .22), col); im.alpha_composite(t_, (int(w / 2 - t_.size[0] / 2), int(w * .35 - t_.size[1] / 2)))
    return im


def paper_layers(c, t, cols, base=1300):
    for k, col in enumerate(cols):
        c.alpha_composite(paper_layer(col, base + k * 150, 40 - k * 8, k * 1.3 + 0.5), (int(-((t * (8 + k * 10)) % 200)), 0))


@functools.lru_cache(None)
def paper_layer(col, y, amp_, seed):
    im = Image.new('RGBA', (W + 200, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pts = [(0, H)] + [(x, y + amp_ * math.sin(x / 140 + seed) + amp_ * .5 * math.sin(x / 57 + seed * 2)) for x in range(0, W + 201, 20)] + [(W + 200, H)]
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).polygon([(x, y_ - 14) for x, y_ in pts], fill=(0, 0, 0, 80))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10))); d.polygon(pts, fill=col); return im


def bg(c, t, cols=((214, 228, 222), (178, 212, 204))):
    c.alpha_composite(paper_bg()); paper_layers(c, t - 0, cols, 1500)


BK = (10, 10, 11); CRM = (239, 230, 210); OR = (255, 79, 18); BL = (31, 59, 255); ASPH = (38, 40, 46); GRN2 = (40, 170, 100)


def ease_out(x): return 1 - (1 - clamp(x)) ** 4


def mask_reveal(c, t, t0, s, font, size, col, cx, cy, stagger=0.1, dur=0.45, serif_word=None):
    """pro text: each word slides up from a clip mask, staggered"""
    words = s.split(' '); imgs = []
    for w_ in words:
        f_ = 'pfi' if serif_word and w_.strip('.,').lower() == serif_word else font
        imgs.append(text_img(w_, f_, size if f_ == font else int(size * 1.05), OR if f_ == 'pfi' else col))
    gap = size * 0.25; tw = sum(i.size[0] for i in imgs) + gap * (len(imgs) - 1)
    x = cx - tw / 2
    for k, im in enumerate(imgs):
        q = ease_out((t - t0 - k * stagger) / dur)
        if q > 0:
            h_ = im.size[1]; dy = int((1 - q) * h_ * 1.15)
            crop = im.crop((0, 0, im.size[0], max(1, h_ - dy)))
            c.alpha_composite(crop, (int(x), int(cy - h_ / 2 + dy)))
        x += im.size[0] + gap


def handle(c):
    place(c, text_img('@moneyincloud', 'osw5', 30, (200, 200, 205)), 160, 70)


@functools.lru_cache(None)
def grain_frames():
    rng = np.random.default_rng(3); out = []
    for k in range(6):
        g = rng.normal(0, 14, (H // 2, W // 2)).astype(np.float32)
        out.append(np.kron(g, np.ones((2, 2), np.float32))[..., None])
    return out


@functools.lru_cache(None)
def vignette():
    y, x = np.mgrid[0:H, 0:W]; r = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
    return (1 - 0.13 * np.clip((r - 0.6) / 0.8, 0, 1))[..., None].astype(np.float32)


def finish(arr, t):
    a = arr.astype(np.float32) * vignette() + grain_frames()[int(t * 30) % 6] * 0.6
    return np.clip(a, 0, 255).astype(np.uint8)


@functools.lru_cache(None)
def dark_bg():
    im = Image.new('RGBA', (W, H), BK + (255,)); d = ImageDraw.Draw(im)
    for y in range(0, H, 90): d.line((0, y, W, y), fill=(22, 22, 26), width=1)
    return im


def road(c, t, y0=900, speed=1.0, col=ASPH):
    d = ImageDraw.Draw(c); vx = 540
    d.polygon([(vx - 60, y0), (vx + 60, y0), (W + 300, H), (-300, H)], fill=col)
    for k in range(14):
        z = ((k / 14) + t * 0.35 * speed) % 1; z2 = z + 0.03
        ya = y0 + (H - y0) * z ** 2; yb = y0 + (H - y0) * z2 ** 2
        wa = 4 + 30 * z; d.polygon([(vx - wa / 2, ya), (vx + wa / 2, ya), (vx + wa, yb), (vx - wa, yb)], fill=CRM)
    for side in (-1, 1):
        d.line((vx + side * 60, y0, vx + side * (W / 2 + 300), H), fill=OR, width=8)


@functools.lru_cache(None)
def plane(s=220, col=CRM):
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(s * .1, s * .5), (s * .9, s * .44), (s * .98, s * .5), (s * .9, s * .56)], fill=col)
    d.polygon([(s * .45, s * .48), (s * .3, s * .15), (s * .4, s * .15), (s * .62, s * .48)], fill=col)
    d.polygon([(s * .45, s * .52), (s * .3, s * .85), (s * .4, s * .85), (s * .62, s * .52)], fill=col)
    d.polygon([(s * .1, s * .5), (s * .05, s * .35), (s * .12, s * .35), (s * .2, s * .48)], fill=col)
    return im


@functools.lru_cache(None)
def card_pro(title, sub, accent=OR, w=900, h=180):
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 26, fill=(26, 26, 30), outline=(60, 60, 66), width=2)
    d.rounded_rectangle((0, 0, 14, h - 1), 7, fill=accent)
    t1 = text_img(title, 'anton', 64, CRM); im.alpha_composite(t1, (44, 24))
    t2 = text_img(sub, 'osw5', 36, (170, 170, 178)); im.alpha_composite(t2, (46, h - 64))
    return im


def card_in(c, t, t0, title, sub, y, accent=OR, x=540):
    if t < t0: return
    q = ease_out((t - t0) / 0.5)
    im = card_pro(title, sub, accent)
    if q < 1:
        blur = int((1 - q) * 10)
        if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
    place(c, im, x + (1 - q) * 500, y, 1, 0, clamp(q * 2))


def cap(c, t, i, cy=1700):
    caption(c, t, i, cy, 42, by_sentence=True)


# ---------------- light theme ----------------
TX = (16, 34, 26); BASE = (244, 252, 246)


@functools.lru_cache(None)
def light_base():
    im = Image.new('RGBA', (W, H), BASE + (255,)); d = ImageDraw.Draw(im)
    for x in range(-H, W, 70): d.line((x, 0, x + H, H), fill=(228, 246, 234), width=18)
    return im


@functools.lru_cache(None)
def blob(r, col):
    a = Image.new('L', (r * 3, r * 3), 0); ImageDraw.Draw(a).ellipse((r, r, 2 * r, 2 * r), fill=150)
    im = Image.new('RGBA', a.size, col + (0,)); im.putalpha(a.filter(ImageFilter.GaussianBlur(r // 3)))
    return im


def bgl(c, t):
    c.alpha_composite(light_base())
    for k, (r, col, x0, y0, sx, sy) in enumerate(((260, (150, 230, 180), 160, 420, 60, 40), (200, (255, 220, 130), 900, 900, -50, 60),
                                                    (300, (140, 220, 200), 820, 1650, 40, -50), (180, (200, 235, 160), 220, 1380, -40, 40))):
        x = x0 + sx * math.sin(t * 0.6 + k); y = y0 + sy * math.cos(t * 0.5 + k * 1.7)
        b_ = blob(r, col); c.alpha_composite(b_, (int(x - b_.size[0] / 2), int(y - b_.size[1] / 2)))


@functools.lru_cache(None)
def card_pro(title, sub, accent=(255, 70, 140), w=900, h=180):
    im = Image.new('RGBA', (w + 16, h + 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((8, 12, w + 7, h + 11), 26, fill=(0, 0, 0, 40))
    im = im.filter(ImageFilter.GaussianBlur(6)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 26, fill=(255, 255, 255), outline=(205, 235, 215), width=2)
    d.rounded_rectangle((0, 0, 14, h - 1), 7, fill=accent)
    im.alpha_composite(text_img(title, 'anton', 64, TX), (44, 24))
    im.alpha_composite(text_img(sub, 'osw5', 36, (110, 100, 110)), (46, h - 64))
    return im


def handle(c):
    place(c, text_img('@moneyincloud', 'osw5', 30, (120, 100, 115)), 160, 70)


# ---------------- Divi6 scenes ----------------
GN = (22, 150, 90); OR = GN
RED2 = (220, 60, 50); MUT = (90, 110, 100); GOLDC = (230, 175, 40)
ROWS = [('COAL INDIA', 6.6), ('WIPRO', 5.9), ('ONGC', 5.7), ('INDIAN OIL', 5.5), ('BPCL', 5.4), ('ITC', 5.1)]
SRCLINE = 'Trailing dividend yields: Equitymaster screener, close 06 Nov 2026 · ₹/yr = yield × ₹1 lakh, before tax'


def rain(c, t, t0=0.0, n=14, top=0, bot=1100):
    d = ImageDraw.Draw(c)
    for k in range(n):
        ph = (k * 0.37) % 1; sp = 520 + 90 * (k % 4)
        y = top + ((t - t0) * sp + ph * (bot - top)) % (bot - top); x = 70 + (k * 149) % 940
        r = 22 + (k % 3) * 6
        d.ellipse((x - r, y - r, x + r, y + r), fill=GOLDC, outline=(170, 120, 10), width=3)
        place(c, text_img('₹', 'anton', int(r * 1.2), (150, 100, 0)), x, y)


def row_times():
    return [at(1, 'Coal India', -0.2), at(2, 'Wipro', -0.2), at(2, 'ONGC', -0.2), at(3, 'Indian Oil', -0.2), at(3, 'BPCL', -0.2), at(3, 'ITC', -0.2)]


def table(c, t, top=420, rh=150, show_all=False, small=False):
    d = ImageDraw.Draw(c); x0, x1 = 70, 1010
    if small: rh = 92
    hy = top - (62 if small else 80)
    place(c, text_img('STOCK', 'osw5', 30, MUT), 160, hy)
    place(c, text_img('YIELD', 'osw5', 30, MUT), 640, hy)
    place(c, text_img('₹1 LAKH → ₹/YEAR'.replace('→', 'TO'), 'osw5', 30, MUT), 870, hy)
    for k, ((nm, y), tr) in enumerate(zip(ROWS, row_times())):
        if not show_all and t < tr: break
        q = 1 if show_all else ease_out((t - tr) / 0.4)
        yy = top + k * rh
        im = Image.new('RGBA', (x1 - x0, rh - 14), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
        dd.rounded_rectangle((0, 0, x1 - x0 - 1, rh - 15), 20, fill=(255, 255, 255), outline=(205, 235, 215), width=2)
        if not show_all and t - tr < 1.6:  # highlighter swipe
            hq = ease_out((t - tr) / 0.5)
            dd.rounded_rectangle((10, 12, 10 + (x1 - x0 - 20) * hq, rh - 27), 14, fill=(255, 236, 120))
        fs = 48 if small else 64
        im.alpha_composite(text_img(f'{k + 1}. {nm}', 'anton', fs, TX), (24, (rh - 14 - text_img('A', 'anton', fs, TX).size[1]) // 2))
        place(im, text_img(f'{y:.1f}%', 'anton', fs, GN), 570, (rh - 14) / 2)
        place(im, text_img(f'₹{int(y * 1000):,}', 'anton', fs, TX), 800, (rh - 14) / 2)
        c.alpha_composite(im.rotate(0), (x0 + int((1 - q) * 120), int(yy - (rh - 14) / 2)))


def s0(c, t):
    i = 0
    bgl(c, t); rain(c, t, 0.0, 14, 0, 1400)
    place(c, text_img('₹1 LAKH', 'anton', 230, TX), 540, 560, 1, -2)
    mask_reveal(c, t, 0.05, '6 stocks that pay you', 'anton', 86, TX, 540, 820, serif_word='pay')
    mask_reveal(c, t, 0.6, 'every year', 'pfi', 110, GN, 540, 960)
    cap(c, t, i, 1600)


def s1(c, t):
    i = 1
    bgl(c, t)
    mask_reveal(c, t, STARTS[i] + 0.05, 'Dividend cheat sheet', 'anton', 92, TX, 540, 210, serif_word='cheat')
    table(c, t, 470)
    tm = at(i, 'sixty six', -0.4)
    if t > tm:
        q = ease_out((t - tm) / 0.9)
        place(c, text_img(f'₹{int(6600 * q):,} a year', 'anton', 120, GN), 540, 1230, 1, -2)
        place(c, text_img('from ₹1 lakh in Coal India', 'pfi', 48, MUT), 540, 1350, 1, 0, clamp(q * 2))
    cap(c, t, i, 1620)
    place(c, text_img(SRCLINE, 'osw5', 22, (100, 115, 105)), 540, 1845)


def s2(c, t):
    i = 2
    bgl(c, t)
    mask_reveal(c, t, STARTS[i] + 0.05, 'Dividend cheat sheet', 'anton', 92, TX, 540, 210, serif_word='cheat')
    table(c, t, 470)
    cap(c, t, i, 1620)
    place(c, text_img(SRCLINE, 'osw5', 22, (100, 115, 105)), 540, 1845)


def s3(c, t):
    i = 3
    bgl(c, t)
    mask_reveal(c, t, STARTS[i] + 0.05, 'Dividend cheat sheet', 'anton', 92, TX, 540, 210, serif_word='cheat')
    table(c, t, 470)
    cap(c, t, i, 1620)
    place(c, text_img(SRCLINE, 'osw5', 22, (100, 115, 105)), 540, 1845)


def s4(c, t):
    i = 4
    bgl(c, t)
    mask_reveal(c, t, STARTS[i] + 0.05, 'The catch', 'anton', 110, TX, 540, 220, serif_word='catch')
    card_in(c, t, at(i, 'taxed', -0.4), 'TAXED AT YOUR SLAB', '+10% TDS above ₹10,000 a year per company', 460, RED2)
    th = at(i, 'high yield', -0.4)
    if t > th:
        q = ease_out((t - th) / 0.5)
        place(c, text_img('YIELD  =  DIVIDEND ÷ PRICE', 'anton', 64, TX), 540, 760, 1, 0, clamp(q * 2))
        tp = at(i, 'price fell', -0.6)
        d = ImageDraw.Draw(c)
        f = ease_out((t - tp) / 1.0) if t > tp else 0
        ph = 360 * (1 - 0.45 * f); yh = 160 * (1 + 0.8 * f)
        d.rounded_rectangle((250, 1360 - ph, 410, 1360), 16, fill=(150, 160, 155))
        d.rounded_rectangle((670, 1360 - yh, 830, 1360), 16, fill=GN)
        place(c, text_img('PRICE', 'anton', 52, TX), 330, 1410); place(c, text_img('YIELD', 'anton', 52, TX), 750, 1410)
        if f > 0.3:
            place(c, text_img('↓', 'anton', 90, RED2) if False else text_img('FALLS', 'anton', 44, RED2), 330, 1360 - ph - 50)
            place(c, text_img('LOOKS BIG', 'anton', 44, GN), 750, 1360 - yh - 50)
    cap(c, t, i, 1620)
    place(c, text_img('Dividends are taxed at slab rates; TDS 10% when a company pays you over ₹10,000 in a year (Sec 194, from 1 Apr 2025)', 'osw5', 21, (100, 115, 105)), 540, 1845)


def s5(c, t):
    i = 5
    bgl(c, t)
    host(c, t, [(STARTS[i], 2)], 540, 820, 600)
    tg = at(i, 'never guaranteed', -0.3)
    if t > tg:
        q = eback(prog(t, tg, 0.35))
        place(c, pill_text('NOT GUARANTEED', RED2, (255, 255, 255), 96), 540, 300, 0.6 + 0.4 * q, -5)
    tc = at(i, 'cut them', -0.3)
    if t > tc:
        card_in(c, t, tc, 'PAYOUTS CAN BE CUT', 'past dividends ≠ future dividends'.replace('≠', 'are not'), 1220, RED2)
    cap(c, t, i, 1620)


def s6(c, t):
    i = 6
    bgl(c, t)
    place(c, text_img('SAVE THIS CHEAT SHEET', 'anton', 64, GN), 540, 280)
    table(c, t, 470, show_all=True, small=True)
    host(c, t, [(STARTS[i], 31)], 230, 1230, 380)
    tc = at(i, 'Comment', -0.2)
    if t > tc:
        q = eback(prog(t, tc, 0.35))
        place(c, pill_text('COMMENT "DIVIDEND"', GN, (255, 255, 255), 60), 650, 1180, 0.6 + 0.4 * q, -2)
    tf = at(i, 'follow', -0.1)
    if t > tf: place(c, follow_btn(), 650, 1340, 0.6 + 0.4 * eback(prog(t, tf, 0.35)), 2)
    place(c, text_img('Yields: Equitymaster, 06 Nov 2026 · before tax', 'osw5', 26, MUT), 540, 1500)
    src(c, 'Not a buy/sell call · Education only · I may hold some of the stocks named', 1880)


SCENES = [s0, s1, s2, s3, s4, s5, s6]


def slam_times():
    return [at(1, 'sixty six', -0.4), at(4, 'catch', -0.2), at(5, 'never guaranteed', -0.3)]
def footer(c):
    d = ImageDraw.Draw(c)
    d.rectangle((0, 1888, W, H), fill=(222, 244, 230, 255))
    place(c, text_img('Not a buy/sell call · Education only · @moneyincloud', 'osw5', 22, (110, 90, 105)), 540, 1904)


def render(t):
    LOOP = 0.5
    if t > DUR - LOOP:
        a = _render(t); b = _render(1.0); q = eio((t - (DUR - LOOP)) / LOOP)
        return finish((a * (1 - q) + b * q).astype(np.uint8), t)
    return finish(_render(t), t)


def _render(t):
    i = scene_at(t)
    st = STARTS[i]; en = STARTS[i + 1] if i + 1 < len(STARTS) else DUR
    c = Image.new('RGBA', (W, H), BK + (255,))
    SCENES[i](c, t)
    z = 1.0 + 0.025 * clamp((t - st) / (en - st))
    sx = sy = 0
    for ts in slam_times():
        if 0 <= t - ts < 0.35:
            k = math.exp(-(t - ts) * 14) * 9; sx += k * math.sin((t - ts) * 90); sy += k * math.cos((t - ts) * 77)
    cw, ch = W / z, H / z
    c = c.transform((W, H), Image.EXTENT, (W / 2 + sx - cw / 2, H / 2 + sy - ch / 2, W / 2 + sx + cw / 2, H / 2 + sy + ch / 2), Image.BICUBIC)
    if i > 0 and t - st < 0.3:
        q = ease_out((t - st) / 0.3)
        prev = Image.new('RGBA', (W, H), BK + (255,)); SCENES[i - 1](prev, st - 0.01)
        out = Image.new('RGBA', (W, H), BK + (255,))
        pb = prev.filter(ImageFilter.BoxBlur(int(8 * q)))
        out.alpha_composite(pb, (int(-W * 0.35 * q), 0))
        mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).rectangle((int(W * (1 - q)), 0, W, H), fill=255)
        out.paste(c, (0, 0), mask); c = out
    handle(c)
    if i != len(SCENES) - 1: footer(c)
    return np.asarray(c.convert('RGB'))
