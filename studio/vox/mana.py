"""Manappuram Finance: branches, profit per branch, how gold loans work, growth, risks. User cartoon host, narrator am_michael.
Realistic cast cut-outs, multi-voice dialogue (vo_cast.py), light template, red topic colour."""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, textwrap, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from lib import *
from scenes import stamp_c
from fridge import follow_btn

SH = ROOT + 'mana/'
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


GOLD = (212, 160, 30); GOLD2 = (245, 200, 70); DARKG = (120, 80, 10)


@functools.lru_cache(None)
def gold_bg():
    im = Image.new('RGB', (W, H), (150, 100, 10)); d = ImageDraw.Draw(im)
    cx, cy = 540, 1150
    for k in range(28):
        a0 = k * 2 * math.pi / 28; a1 = a0 + math.pi / 28
        d.polygon([(cx, cy), (cx + 2600 * math.cos(a0), cy + 2600 * math.sin(a0)), (cx + 2600 * math.cos(a1), cy + 2600 * math.sin(a1))], fill=(176, 122, 18))
    g = Image.radial_gradient('L').resize((2400, 2400)).crop((660, 50, 1740, 1970))
    im = Image.composite(im, Image.new('RGB', im.size, (60, 36, 4)), g.point(lambda v: 255 - int(v * 0.8)))
    return im.convert('RGBA')


@functools.lru_cache(None)
def shop(s=60, col=GOLD):
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(s * .1, s * .4), (s * .5, s * .1), (s * .9, s * .4)], fill=(200, 40, 40))
    d.rectangle((s * .18, s * .4, s * .82, s * .9), fill=col, outline=INK, width=max(2, s // 20))
    d.rectangle((s * .42, s * .6, s * .58, s * .9), fill=INK)
    return im


@functools.lru_cache(None)
def chain(s=360):
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    n = 18
    for k in range(n):
        a = math.pi * 0.1 + k / (n - 1) * math.pi * 0.8
        x = s / 2 + s * .38 * math.cos(a); y = s * .2 + s * .55 * math.sin(a)
        d.ellipse((x - 18, y - 12, x + 18, y + 12), outline=DARKG, width=9, fill=None); d.ellipse((x - 18, y - 12, x + 18, y + 12), outline=GOLD2, width=5)
    d.ellipse((s / 2 - 45, s * .72, s / 2 + 45, s * .72 + 90), fill=GOLD2, outline=DARKG, width=6)
    return im


def scale_img(t, tilt=0.0, s=520):
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx = s / 2; d.rectangle((cx - 12, s * .25, cx + 12, s * .85), fill=(90, 90, 100)); d.rectangle((cx - 120, s * .85, cx + 120, s * .9), fill=(90, 90, 100))
    a = math.radians(tilt); L = s * .4
    x1, y1 = cx - L * math.cos(a), s * .25 - L * math.sin(a); x2, y2 = cx + L * math.cos(a), s * .25 + L * math.sin(a)
    d.line((x1, y1, x2, y2), fill=(90, 90, 100), width=12)
    for x, y in ((x1, y1), (x2, y2)):
        d.line((x, y, x - 60, y + 120), fill=(90, 90, 100), width=4); d.line((x, y, x + 60, y + 120), fill=(90, 90, 100), width=4)
        d.chord((x - 90, y + 80, x + 90, y + 170), 0, 180, fill=(170, 170, 180), outline=INK, width=4)
    return im


# ---------------- scenes ----------------
def s0(c, t):
    i = 0
    c.alpha_composite(gold_bg())
    place_text(c, '₹12,000 PROFIT', 'anton', 120, YEL, 540, 250, t, None, at(0, 'twelve', -0.2), 'pop')
    place_text(c, 'PER BRANCH, PER DAY', 'anton', 90, (255, 247, 230), 540, 390, t, None, at(0, 'a day', -0.3), 'pop')
    place(c, pill_text('MANAPPURAM FINANCE', INK, YEL, 60), 540, 540, 0.6 + 0.4 * eback(prog(t, 0.1, 0.3)), -3)
    place(c, chain(360), 800, 860 + 10 * math.sin(t * 2), 1, 8)
    host(c, t, [(0, 2), (at(0, 'twelve', -0.2), 50)], 420, 1250, 720)


def s1(c, t):
    i = 1
    c.alpha_composite(data_bg())
    head(c, t, i, 'MANAPPURAM IN NUMBERS', GOLD)
    tb = at(i, 'five thousand', -0.2)
    if t > tb:
        q = eo(prog(t, tb, 2.0)); n = int(5328 * q); shown = int(240 * q)
        for k in range(shown):
            x = 110 + (k % 20) * 45; y = 360 + (k // 20) * 45
            place(c, shop(40), x, y)
        place(c, pill_text(f'{n:,} BRANCHES', GOLD, INK, 70), 540, 960, 1, -2)
    tp = at(i, 'five hundred', -0.2)
    if t > tp: place(c, info((('₹585 CRORE PROFIT', 80, INK), ('in 3 months (Apr–Jun 2026) · +341% vs last year', 36, GREY)), 900, GOLD), 540 + (1 - eo(prog(t, tp, 0.4))) * 900, 1180, 1, -1.5)
    host(c, t, [(STARTS[i], 34)], 870, 1440, 320)
    caption(c, t, i, 1650, 42, by_sentence=True)
    place(c, text_img('Q1 FY27 consolidated results (via Upstox / Investywise, Aug 2026)', 'osw5', 24, GREY), 540, 1840)


def s2(c, t):
    i = 2
    c.alpha_composite(gold_bg())
    place(c, pill_text('THE MATH', INK, YEL, 80), 540, 230, 1, -2)
    place(c, info((('₹585 cr ÷ 5,328', 80, INK), ('group profit ÷ all branches', 36, GREY)), 900, GOLD), 540, 450, 1, -1.5)
    tl = at(i, 'eleven lakh', -0.2)
    if t > tl: place(c, pill_text('≈ ₹11 LAKH A QUARTER'.replace('≈ ', 'ABOUT '), (255, 255, 255), INK, 66), 540, 700, 0.6 + 0.4 * eback(prog(t, tl, 0.3)), 2)
    big_num(c, t, at(i, 'twelve thousand', -0.2), '₹12,000 / DAY', YEL, 540, 920, 150)
    host(c, t, [(STARTS[i], 57), (at(i, 'twelve thousand', -0.2), 46)], 540, 1330, 520)
    caption(c, t, i, 1680, 42, by_sentence=True)
    place(c, text_img('My calculation: average across all branches, 91-day quarter', 'osw5', 26, (255, 240, 200)), 540, 1840)


def s3(c, t):
    i = 3
    c.alpha_composite(data_bg())
    head(c, t, i, 'HOW A GOLD LOAN WORKS', GOLD)
    tw = at(i, 'weigh', -0.3)
    tilt = 0 if t < tw else 12 * math.exp(-(t - tw) * 2) * math.cos((t - tw) * 9) + 6
    place(c, scale_img(t, tilt), 540, 640)
    if t > at(i, 'walk in', -0.3):
        place(c, chain(200), 540 - 162 + (0 if t > tw else 0), 640 - 70 + 0, 1, 0)
    for k, (ph, s_) in enumerate((('test it', '1. TEST'), ('weigh it', '2. WEIGH'), ('sixty five', '3. LEND ~65% OF VALUE'))):
        tk = at(i, ph, -0.25)
        if t > tk: place(c, pill_text(s_, GOLD if k < 2 else (40, 160, 90), INK if k < 2 else (255, 255, 255), 54), 540, 1010 + k * 120, 0.6 + 0.4 * eback(prog(t, tk, 0.3)), [-2, 2, -1][k])
    host(c, t, [(STARTS[i], 34), (at(i, 'in minutes', -0.2), 17)], 880, 1450, 300)
    caption(c, t, i, 1660, 42, by_sentence=True)
    place(c, text_img('Avg loan-to-value 65.6% (standalone, Oct 2026)', 'osw5', 24, GREY), 540, 1840)


def s4(c, t):
    i = 4
    c.alpha_composite(gold_bg())
    big_num(c, t, at(i, 'eighteen', -0.2), '~18%', YEL, 540, 380, 230)
    if t > at(i, 'eighteen', -0.2): place(c, text_img('GOLD LOAN YIELD, A YEAR', 'anton', 60, (255, 247, 230)), 540, 560)
    tr = at(i, 'if you do not', -0.3)
    if t > tr:
        place(c, info((("DON'T REPAY?", 70, INK), ('the pledged gold covers the loan (auction)', 36, GREY)), 900, RED), 540 + (1 - eo(prog(t, tr, 0.4))) * 900, 780, 1, -1.5)
    host(c, t, [(STARTS[i], 61), (tr, 8)], 540, 1300, 560)
    caption(c, t, i, 1680, 42, by_sentence=True)


def s5(c, t):
    i = 5
    c.alpha_composite(data_bg())
    head(c, t, i, 'GOLD LOAN BOOK', GOLD)
    d = ImageDraw.Draw(c); base = 1080
    for k, (lab, v, col, tk) in enumerate((('JUN 2025', 28802, (190, 170, 120), STARTS[i] + 0.3), ('JUN 2026', 57006, GOLD, at(i, 'fifty seven', -0.3)))):
        if t < tk: continue
        q = eo(prog(t, tk, 0.9)); x = 330 + k * 420; hg = int(v / 57006 * 560 * q)
        d.rounded_rectangle((x - 130, base - hg, x + 130, base), 18, fill=col, outline=INK, width=6)
        place(c, text_img(f'₹{int(v * q):,} cr', 'anton', 64, INK), x, base - hg - 50)
        place(c, text_img(lab, 'anton', 48, INK), x, base + 50)
    ta = at(i, 'almost double', -0.2)
    if t > ta: place(c, pill_text('~2x IN ONE YEAR', RED, (255, 255, 255), 70), 540, 1260, 0.6 + 0.4 * eback(prog(t, ta, 0.3)), -3)
    caption(c, t, i, 1620, 42, by_sentence=True)
    place(c, text_img('Consolidated gold loan AUM, Q1 FY27 vs Q1 FY26 (Upstox, Aug 2026)', 'osw5', 24, GREY), 540, 1840)


def s6(c, t):
    i = 6
    c.alpha_composite(gold_bg())
    big_num(c, t, STARTS[i] + 0.2, '86%', YEL, 540, 380, 240)
    if t > STARTS[i] + 0.2: place(c, text_img('OF GOLD LOANS TAKEN ONLINE', 'anton', 60, (255, 247, 230)), 540, 560)
    tc = at(i, 'twenty six', -0.2)
    if t > tc: place(c, pill_text('26.5 LAKH CUSTOMERS', INK, YEL, 70), 540, 720, 0.6 + 0.4 * eback(prog(t, tc, 0.3)), -2)
    host(c, t, [(STARTS[i], 45)], 540, 1250, 640)
    caption(c, t, i, 1680, 44, by_sentence=True)


def s7(c, t):
    i = 7
    c.alpha_composite(data_bg())
    head(c, t, i, 'THE PLAN', GOLD)
    card_at(c, t, at(i, 'Five hundred', -0.3), [('+500 NEW BRANCHES', 62, INK), ('this year (FY27)', 38, GREY)], 540, 450, GOLD)
    card_at(c, t, at(i, 'twenty five', -0.3), [('+25–30% GOLD LOANS', 62, INK), ('growth target for FY27', 38, GREY)], 540, 720, (40, 160, 90))
    card_at(c, t, at(i, 'Bain', -0.3), [('BAIN CAPITAL', 62, INK), ('now co-promoter (Apr 2026)', 38, GREY)], 540, 990, (40, 120, 200))
    card_at(c, t, at(i, 'new CEO', -0.3), [('NEW CEO: ASHISH SINGH', 56, INK), ('from 1 Jan 2027', 38, GREY)], 540, 1260, (120, 60, 170))
    host(c, t, [(STARTS[i], 35)], 900, 1500, 260)
    caption(c, t, i, 1680, 42, by_sentence=True)


def s8(c, t):
    i = 8
    c.alpha_composite(gold_bg())
    big_num(c, t, at(i, 'three hundred', -0.2), '₹323.75', YEL, 540, 400, 200)
    if t > at(i, 'three hundred', -0.2): place(c, text_img('NSE CLOSE, 9 NOV 2026', 'anton', 50, (255, 247, 230)), 540, 560)
    tm = at(i, 'Market value', -0.2)
    if t > tm: place(c, pill_text('MARKET CAP ~₹30,411 cr', INK, YEL, 64), 540, 720, 0.6 + 0.4 * eback(prog(t, tm, 0.3)), -2)
    place(c, text_img('52-week range ₹245 – ₹382', 'osw', 40, (255, 240, 200)), 540, 840, 1, 0, clamp((t - STARTS[i] - 1) * 3))
    host(c, t, [(STARTS[i], 53)], 540, 1300, 560)
    caption(c, t, i, 1680, 44, by_sentence=True)


def s9(c, t):
    i = 9
    c.alpha_composite(data_bg())
    head(c, t, i, 'RISK CHECK', RED)
    card_at(c, t, at(i, 'gold prices fall', -0.3), [('GOLD PRICE FALLS', 64, INK), ('smaller loans · more auctions', 40, GREY)], 540, 470, RED)
    card_at(c, t, at(i, 'vehicle', -0.3), [('VEHICLE LOANS: 13.3% BAD', 58, INK), ('gross NPA, Q1 FY27 (up from 10.4%)', 38, GREY)], 540, 770, RED)
    host(c, t, [(STARTS[i], 8), (at(i, 'vehicle', -0.3), 41)], 540, 1280, 520)
    caption(c, t, i, 1660, 42, by_sentence=True)


def s10(c, t):
    i = 10
    c.alpha_composite(gold_bg())
    host(c, t, [(STARTS[i], 31)], 540, 800, 700)
    tf = at(i, 'follow', -0.1)
    if t > tf: place(c, follow_btn(), 540, 1320, 0.6 + 0.4 * eback(prog(t, tf, 0.35)), 2)
    tw = at(i, 'Have you', -0.2)
    if t > tw: place(c, pill_text('EVER TAKEN A GOLD LOAN? YES / NO', INK, YEL, 52), 540, 1500, 1, -2, clamp((t - tw) * 3))
    src(c, 'Not a buy/sell call · I may hold some of the stocks named · Sources in caption', 1880)


SCENES = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]


def slam_times():
    return [at(0, 'twelve', -0.2), at(2, 'twelve thousand', -0.2), at(5, 'almost double', -0.2), at(9, 'vehicle', -0.3)]
def footer(c):
    d = ImageDraw.Draw(c)
    d.rectangle((0, 1888, W, H), fill=(20, 22, 30, 255))
    place(c, text_img('Not a buy/sell call · Education only · I may hold some stocks named', 'osw5', 22, (230, 230, 236)), 540, 1904)
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
