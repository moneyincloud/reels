"""Equity vs mutual fund: Vox-style collage + paper-cut layers. Narrator af_heart, user cartoon as paper sticker.
Realistic cast cut-outs, multi-voice dialogue (vo_cast.py), light template, red topic colour."""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, textwrap, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from lib import *
from scenes import stamp_c
from fridge import follow_btn

SH = ROOT + 'eqmf/'
CAST_DIR = ROOT + 'brand/cast_real/'
LINES = json.load(open(SH + 'lines.json'))
SCRIPT = [l['text'].replace('N. A. V.', 'NAV') for l in LINES]
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


# ---------------- scenes ----------------
def s0(c, t):
    i = 0
    bg(c, t)
    vox_title(c, t, 0.05, 'Stocks', 300, CORAL, 130)
    place(c, text_img('vs', 'mark', 80, INK), 540, 430, 1, 0, clamp((t - 0.3) * 3))
    vox_title(c, t, 0.4, 'Mutual Funds', 560, TEALP, 120)
    marker_circle(c, t, at(i, 'Same ten', -0.3), 540, 770, 300, 90)
    if t > at(i, 'Same ten', -0.3): place(c, text_img('₹10,000', 'anton', 120, INK), 540, 770)
    tr = at(i, 'two very', -0.2)
    if t > tr: highlight(c, t, tr, 240, 880, 840, 950); place(c, text_img('two very different rides', 'type', 52, INK), 540, 915)
    sticker(c, t, [(0, 14), (tr, 26)], 540, 1380, 520)


def s1(c, t):
    i = 1
    bg(c, t, ((250, 220, 200), (240, 190, 170)))
    vox_title(c, t, STARTS[i], 'Equity = ownership', 260, INK, 84)
    note_at(c, t, STARTS[i] + 0.3, [('SHARE CERTIFICATE', 'pf', 64, CORAL), ('1 share of "Company X"', 'type', 46, INK), ('= a tiny piece of the business', 'type', 46, INK)], 540, 620, (255, 250, 238), 880, -2, 5)
    tp = at(i, 'tiny piece', -0.2)
    if t > tp: highlight(c, t, tp, 200, 700, 900, 760)
    tb = at(i, 'Buy one', -0.2)
    if t > tb:
        d = ImageDraw.Draw(c); q = eo(prog(t, tb, 0.8))
        d.rectangle((300, 1150 - 300 * q, 780, 1150), fill=CORAL, outline=INK, width=6)
        for r in range(4):
            for k in range(5): d.rectangle((330 + k * 90, 1120 - r * 70 - 300 * (1 - q) * 0, 380 + k * 90, 1150 - r * 70 - 300 * (1 - q) * 0 - 10), fill=(255, 240, 220) if 1150 - r * 70 > 1150 - 300 * q else CORAL)
        if t > tp: d.polygon([(780, 1150), (780, 1000), (700, 1150)], fill=MUST, outline=INK)
    caption(c, t, i, 1660, 44, by_sentence=True)


def s2(c, t):
    i = 2
    bg(c, t)
    vox_title(c, t, STARTS[i], 'Mutual fund = a basket', 260, INK, 80)
    d = ImageDraw.Draw(c)
    d.chord((260, 700, 820, 1200), 0, 180, fill=(196, 140, 80), outline=INK, width=8)
    for k in range(7): d.line((300 + k * 80, 950, 330 + k * 75, 1190), fill=(150, 100, 50), width=4)
    tp = at(i, 'pool', -0.3)
    for k in range(12):
        tk = tp + k * 0.15
        if t < tk: continue
        q = clamp((t - tk) / 0.8); x = 120 + (k % 6) * 170; y0 = 420 + (k // 6) * 120
        place(c, med_icon('globe', 1) if False else share_chit('₹', TEALP, 70), x + (540 - x) * q, y0 + (900 - y0) * q, 1, 0, 1 - q * 0.6)
    for k in range(6): place(c, person_cut('K' if k % 2 else 'P', [CORAL, TEALP, MUST, NAVYP][k % 4], 110), 120 + k * 170, 470 - (0 if t > tp else 0))
    tm = at(i, 'fund manager', -0.3)
    if t > tm:
        note_at(c, t, tm, [('FUND MANAGER', 'anton', 54, NAVYP), ('buys many stocks / bonds', 'type', 40, INK)], 540, 1310, (255, 252, 240), 700, 2, 9)
    caption(c, t, i, 1660, 42, by_sentence=True)


def s3(c, t):
    i = 3
    bg(c, t, ((250, 230, 190), (240, 205, 150)))
    tw = at(i, 'twist', -0.2)
    if t > tw: place(c, text_img('The twist', 'pfi', 110, CORAL), 540, 280, 0.6 + 0.4 * eback(prog(t, tw, 0.3)), -3)
    ta = at(i, 'also buys', -0.3)
    if t > ta:
        note_at(c, t, ta, [('An EQUITY mutual fund', 'pf', 60, INK), ('ALSO BUYS EQUITY', 'anton', 80, TEALP)], 540, 560, (255, 252, 240), 900, -1.5, 11)
        marker_circle(c, t, ta + 0.5, 540, 615, 330, 70)
    tr = at(i, 'who picks', -0.3)
    if t > tr:
        note_at(c, t, tr, [('WHO PICKS?', 'anton', 58, INK), ('Stocks: YOU  ·  Fund: a MANAGER', 'type', 42, INK)], 540, 900, (230, 245, 240), 900, 1.5, 13)
    th = at(i, 'how many', -0.3)
    if t > th:
        note_at(c, t, th, [('HOW MANY?', 'anton', 58, INK), ('Stocks: a FEW  ·  Fund: DOZENS', 'type', 42, INK)], 540, 1180, (250, 235, 230), 900, -1.5, 17)
    sticker(c, t, [(STARTS[i], 14), (ta, 2)], 900, 1450, 300)
    caption(c, t, i, 1660, 44, by_sentence=True)


def two_people(c, t, i):
    place(c, person_cut('P', CORAL, 200), 220, 480); place(c, text_img('PRIYA', 'anton', 50, CORAL), 220, 650)
    place(c, person_cut('K', TEALP, 200), 860, 480); place(c, text_img('KIRAN', 'anton', 50, TEALP), 860, 650)
    place(c, text_img('₹10,000 each', 'pf', 70, INK), 540, 260, 1, 0, clamp((t - STARTS[i]) * 3))


def s4(c, t):
    i = 4
    bg(c, t)
    two_people(c, t, i)
    ts = at(i, 'seven shares', -0.3)
    if t > ts:
        d = ImageDraw.Draw(c)
        d.rounded_rectangle((90, 760, 600, 1260), 20, fill=(250, 214, 160), outline=INK, width=6)
        place(c, text_img('DEMAT', 'anton', 50, INK), 345, 810)
        for k in range(7):
            if t > ts + k * 0.15: place(c, share_chit('CO. X', CORAL, 130), 170 + (k % 4) * 115, 940 + (k // 4) * 130, 1, [-6, 4, -3, 5, -4, 3, -2][k])
        place(c, text_img('7 shares × ~₹1,400', 'type', 40, INK), 345, 1210, 1, 0, clamp((t - ts - 1) * 3))
    th = at(i, 'herself', -0.2)
    if t > th: highlight(c, t, th, 640, 900, 1000, 970, CORAL); place(c, text_img('1 company', 'mark', 60, INK), 820, 935)
    caption(c, t, i, 1660, 44, by_sentence=True)


def s5(c, t):
    i = 5
    bg(c, t)
    two_people(c, t, i)
    tn = at(i, 'Nifty', -0.3)
    if t > tn:
        d = ImageDraw.Draw(c); q = clamp((t - tn) / 2.5)
        d.rounded_rectangle((480, 760, 1010, 1300), 20, fill=(200, 236, 228), outline=INK, width=6)
        place(c, text_img('NIFTY 50 INDEX FUND', 'anton', 42, INK), 745, 805)
        for k in range(int(50 * q)): place(c, share_chit(str(k + 1), TEALP, 70), 530 + (k % 8) * 62, 870 + (k // 8) * 56)
    tu = at(i, 'units', -0.2)
    if t > tu: note_at(c, t, tu, [('UNITS @ NAV', 'anton', 54, NAVYP), ('NAV = price of one unit', 'type', 36, INK)], 260, 1000, (255, 252, 240), 380, -3, 21)
    tf = at(i, 'fifty companies', -0.3)
    if t > tf: highlight(c, t, tf, 500, 1320, 1000, 1390, TEALP); place(c, text_img('50 companies', 'mark', 60, INK), 750, 1355)
    caption(c, t, i, 1660, 42, by_sentence=True)


def s6(c, t):
    i = 6
    bg(c, t, ((240, 210, 210), (225, 170, 170)))
    tf = at(i, 'thirty percent', -0.25)
    vox_title(c, t, STARTS[i] + 0.1, 'Bad news hits Company X', 240, INK, 74)
    if t > tf: place(c, text_img('-30%', 'anton', 200, (210, 40, 40)), 540, 450, 0.6 + 0.4 * eback(prog(t, tf, 0.3)), -4)
    tp = at(i, 'Priya loses', -0.25)
    if t > tp:
        note_at(c, t, tp, [('PRIYA', 'anton', 54, CORAL), ('-₹3,000', 'anton', 110, (210, 40, 40)), ('all eggs in one basket', 'type', 34, INK)], 290, 900, (255, 250, 238), 460, -3, 23)
    tk = at(i, 'For Kiran', -0.25)
    if t > tk:
        note_at(c, t, tk, [('KIRAN', 'anton', 54, TEALP), ('1 of 50', 'anton', 110, NAVYP), ('a much smaller dent', 'type', 34, INK)], 790, 900, (236, 248, 244), 460, 3, 29)
    sticker(c, t, [(STARTS[i], 2), (tk, 17)], 540, 1400, 330)
    caption(c, t, i, 1660, 42, by_sentence=True)


def s7(c, t):
    i = 7
    bg(c, t, ((214, 236, 214), (178, 220, 180)))
    td = at(i, 'doubles', -0.25)
    vox_title(c, t, STARTS[i] + 0.1, 'But if Company X doubles...', 240, INK, 70)
    if t > td: place(c, text_img('2x', 'anton', 220, (30, 150, 70)), 540, 470, 0.6 + 0.4 * eback(prog(t, td, 0.3)), 3)
    tp = at(i, "Priya's money", -0.25)
    if t > tp: note_at(c, t, tp, [('PRIYA', 'anton', 54, CORAL), ('₹10,000 → ₹20,000'.replace('→', 'to'), 'anton', 60, (30, 150, 70))], 290, 860, (255, 250, 238), 460, -3, 31)
    tk = at(i, 'Kiran gets', -0.25)
    if t > tk: note_at(c, t, tk, [('KIRAN', 'anton', 54, TEALP), ('small part of the gain', 'type', 38, INK)], 790, 860, (236, 248, 244), 460, 3, 37)
    tr = at(i, 'Higher risk', -0.25)
    if t > tr:
        place(c, pill_text('HIGHER RISK = HIGHER POSSIBLE REWARD', INK, HL, 46), 540, 1180, 0.6 + 0.4 * eback(prog(t, tr, 0.3)), -2)
    sticker(c, t, [(STARTS[i], 50), (tr, 35)], 540, 1430, 300)
    caption(c, t, i, 1660, 44, by_sentence=True)


def s8(c, t):
    i = 8
    bg(c, t)
    vox_title(c, t, STARTS[i], 'Costs', 260, INK, 110)
    ts = at(i, 'Stocks have', -0.3)
    if t > ts:
        note_at(c, t, ts, [('STOCKS', 'anton', 60, CORAL), ('brokerage', 'type', 44, INK), ('+ STT & other charges', 'type', 44, INK), ('every time you trade', 'mark', 44, CORAL)], 290, 700, (255, 250, 238), 470, -3, 41)
    tm = at(i, 'Mutual funds take', -0.3)
    if t > tm:
        note_at(c, t, tm, [('MUTUAL FUNDS', 'anton', 56, TEALP), ('expense ratio', 'type', 44, INK), ('a yearly % fee', 'type', 44, INK), ('taken from fund value', 'mark', 40, TEALP)], 790, 700, (236, 248, 244), 470, 3, 43)
    te = at(i, 'expense ratio', -0.2)
    if t > te: marker_circle(c, t, te, 790, 700, 220, 60, TEALP)
    sticker(c, t, [(STARTS[i], 57)], 540, 1330, 380)
    caption(c, t, i, 1660, 44, by_sentence=True)


def s9(c, t):
    i = 9
    bg(c, t, ((235, 225, 250), (210, 196, 240)))
    vox_title(c, t, STARTS[i], 'Tax: same for both', 260, INK, 90)
    d = ImageDraw.Draw(c)
    tw = at(i, 'within a year', -0.3); ta = at(i, 'After a year', -0.3)
    if t > tw:
        note_at(c, t, tw, [('SELL WITHIN 1 YEAR', 'anton', 58, INK), ('20%', 'anton', 110, CORAL), ('short-term capital gains', 'type', 36, INK)], 540, 570, (255, 250, 238), 820, -2, 47)
    if t > ta:
        note_at(c, t, ta, [('HOLD MORE THAN 1 YEAR', 'anton', 58, INK), ('12.5%', 'anton', 110, TEALP), ('on gains above ₹1.25 lakh a year', 'type', 36, INK)], 540, 1090, (236, 248, 244), 820, 2, 53)
    th = at(i, 'one point two five', -0.2)
    if t > th: highlight(c, t, th, 200, 1222, 880, 1262)
    caption(c, t, i, 1620, 42, by_sentence=True)
    place(c, text_img('Listed equity shares & equity mutual funds · FY2026-27 rules (Sec 111A/112A)', 'osw5', 24, GREY), 540, 1845)


def s10(c, t):
    i = 10
    bg(c, t, ((250, 230, 190), (240, 205, 150)))
    vox_title(c, t, STARTS[i], 'Who should pick what?', 250, INK, 82)
    tn = at(i, 'No time', -0.3)
    if t > tn: note_at(c, t, tn, [('NO TIME TO RESEARCH?', 'anton', 54, INK), ('Start a mutual fund SIP', 'pf', 56, TEALP)], 540, 520, (236, 248, 244), 900, -2, 59)
    tl = at(i, 'Love studying', -0.3)
    if t > tl: note_at(c, t, tl, [('LOVE STUDYING COMPANIES', 'anton', 50, INK), ('+ can handle big swings?', 'type', 40, INK), ('Direct stocks', 'pf', 56, CORAL)], 540, 840, (255, 250, 238), 900, 2, 61)
    tb = at(i, 'Many investors', -0.3)
    if t > tb:
        place(c, pill_text('MANY INVESTORS DO BOTH', INK, HL, 60), 540, 1120, 0.6 + 0.4 * eback(prog(t, tb, 0.3)), -2)
    sticker(c, t, [(STARTS[i], 14), (tb, 26)], 540, 1400, 330)
    caption(c, t, i, 1660, 42, by_sentence=True)


def s11(c, t):
    i = 11
    bg(c, t)
    sticker(c, t, [(STARTS[i], 31)], 540, 760, 640)
    tf = at(i, 'follow', -0.1)
    if t > tf: place(c, follow_btn(), 540, 1270, 0.6 + 0.4 * eback(prog(t, tf, 0.35)), 2)
    ta = at(i, 'Are you', -0.2)
    if t > ta:
        place(c, pill_text('TEAM STOCKS', CORAL, (255, 255, 255), 56), 300, 1460, 1, -4, clamp((t - ta) * 3))
        place(c, pill_text('TEAM MF', TEALP, (255, 255, 255), 56), 790, 1460, 1, 4, clamp((t - ta - 0.3) * 3))
    src(c, 'Education only · Not a buy/sell call · Characters are fictional', 1880)


SCENES = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11]


def slam_times():
    return [at(6, 'thirty percent', -0.25), at(7, 'doubles', -0.25)]


def footer(c):
    d = ImageDraw.Draw(c)
    d.rectangle((0, 1888, W, H), fill=(20, 22, 30, 255))
    place(c, text_img('Education only · Not a buy/sell call · Not tax advice · @moneyincloud', 'osw5', 22, (230, 230, 236)), 540, 1904)
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
    if i != len(SCENES) - 1: footer(c)
    return np.asarray(c.convert('RGB'))
