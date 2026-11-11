"""Style story: Arun vs Bala, same 1 lakh bonus, 10 years; each chapter in a different animation style. Narrator am_michael.
Realistic cast cut-outs, multi-voice dialogue (vo_cast.py), light template, red topic colour."""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, textwrap, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from lib import *
from scenes import stamp_c
from fridge import follow_btn

SH = ROOT + 'stylestory/'
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


# ---------- 1. comic ----------
@functools.lru_cache(None)
def comic_bg():
    im = Image.new('RGB', (W, H), (255, 214, 60)); d = ImageDraw.Draw(im)
    for y in range(0, H, 26):
        for x in range((y // 26) % 2 * 13, W, 26): d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(245, 190, 40))
    return im.convert('RGBA')


@functools.lru_cache(None)
def burst(txt, col=(230, 40, 40), size=80, r=300):
    im = Image.new('RGBA', (r * 2 + 20, r * 2 + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im); cx = cy = r + 10
    pts = []
    for k in range(32):
        rr = r if k % 2 == 0 else r * .72; a = k / 32 * 2 * math.pi
        pts.append((cx + rr * math.cos(a), cy + rr * .62 * math.sin(a)))
    d.polygon(pts, fill=col, outline=INK); d.line(pts + [pts[0]], fill=INK, width=8)
    lines = txt.split('\n'); y = cy - len(lines) * size * .55
    for ln in lines:
        t_ = text_img(ln, 'anton', size, (255, 255, 255)); im.alpha_composite(t_, (int(cx - t_.size[0] / 2), int(y))); y += size * 1.1
    return im


def comic_panel(c, box, fill=(255, 255, 255)):
    d = ImageDraw.Draw(c); x0, y0, x1, y1 = box
    d.rectangle((x0 + 12, y0 + 12, x1 + 12, y1 + 12), fill=INK); d.rectangle(box, fill=fill, outline=INK, width=10)


def speech(c, x, y, txt, size=54, tail=(0, 80)):
    t_ = text_img(txt, 'anton', size, INK); w, h = t_.size[0] + 60, t_.size[1] + 40
    d = ImageDraw.Draw(c)
    d.polygon([(x - 30, y + h / 2 - 6), (x + 30, y + h / 2 - 6), (x + tail[0], y + h / 2 + tail[1])], fill=(255, 255, 255), outline=INK)
    d.ellipse((x - w / 2, y - h / 2, x + w / 2, y + h / 2), fill=(255, 255, 255), outline=INK, width=7)
    c.alpha_composite(t_, (int(x - t_.size[0] / 2), int(y - t_.size[1] / 2)))


def caption_box(c, txt, x, y, size=44):
    t_ = text_img(txt, 'anton', size, INK); d = ImageDraw.Draw(c)
    d.rectangle((x - t_.size[0] / 2 - 20, y - t_.size[1] / 2 - 12, x + t_.size[0] / 2 + 20, y + t_.size[1] / 2 + 12), fill=(255, 245, 200), outline=INK, width=6)
    c.alpha_composite(t_, (int(x - t_.size[0] / 2), int(y - t_.size[1] / 2)))


def s0(c, t):
    i = 0
    c.alpha_composite(comic_bg()); style_chip(c, i)
    tb = 0.1
    place(c, burst('NEVER WASTE A\n₹1 LAKH BONUS', size=78, r=330), 540, 420, 0.5 + 0.5 * eback(prog(t, tb, 0.4)), -4 + 1.5 * math.sin(t * 6))
    tf = at(i, 'Two friends', -0.2)
    if t > tf:
        comic_panel(c, (60, 760, 520, 1380)); comic_panel(c, (560, 760, 1020, 1380))
        place(c, kid('A', 'happy', 300), 290, 1150, 0.8 + 0.2 * eback(prog(t, tf, 0.3))); place(c, kid('B', 'happy', 300), 790, 1150, 0.8 + 0.2 * eback(prog(t, tf + 0.2, 0.3)))
    ty = at(i, 'ten years', -0.2)
    if t > ty: caption_box(c, '10 YEARS LATER...', 540, 1470, 60)
    caption(c, t, i, 1700, 44, by_sentence=True)


def s1(c, t):
    i = 1
    c.alpha_composite(comic_bg()); style_chip(c, i)
    comic_panel(c, (60, 300, 520, 1100)); comic_panel(c, (560, 300, 1020, 1100))
    place(c, kid('A', 'happy', 320), 290, 830); place(c, kid('B', 'happy', 320), 790, 830)
    if t > at(i, 'Arun', -0.1): speech(c, 290, 450, 'ARUN', 56)
    if t > at(i, 'Bala', -0.1): speech(c, 790, 450, 'BALA', 56)
    tb = at(i, 'one lakh', -0.2)
    if t > tb: place(c, burst('₹1,00,000\nEACH!', (40, 170, 90), 72, 260), 540, 1220, 0.5 + 0.5 * eback(prog(t, tb, 0.35)), 4)
    if t > at(i, 'same day', -0.2): caption_box(c, 'SAME DAY. SAME BONUS.', 540, 1470, 54)
    caption(c, t, i, 1700, 44, by_sentence=True)


# ---------- 2. synthwave ----------
@functools.lru_cache(None)
def synth_static():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 255)); d = ImageDraw.Draw(im)
    for y in range(0, 1000):
        k = y / 1000; d.line((0, y, W, y), fill=(int(30 + 90 * k), int(10 + 10 * k), int(60 + 60 * (1 - k)), 255))
    cx, cy, r = 540, 860, 300
    sun = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sun)
    for y in range(cy - r, cy + 1):
        k = (y - (cy - r)) / r; hw = math.sqrt(max(0, r * r - (y - cy) ** 2))
        if y > cy - r * .45 and (y // 14) % 2 == 0 and y > cy - r * .45 + (cy - y) * 0: continue
        sd.line((cx - hw, y, cx + hw, y), fill=(255, int(220 - 140 * k), int(80 + 60 * k), 255))
    im.alpha_composite(sun)
    d.rectangle((0, 1000, W, H), fill=(14, 6, 30, 255))
    return im


def synth_bg(t):
    im = synth_static().copy(); d = ImageDraw.Draw(im); hz = 1000
    for k in range(-14, 15):
        d.line((540 + k * 40, hz, 540 + k * 260, H), fill=(255, 60, 200, 255), width=3)
    off = (t * 0.9) % 1
    for j in range(16):
        z = (j + off) / 16; y = hz + (H - hz) * z ** 2.2
        d.line((0, y, W, y), fill=(255, 60, 200, 255), width=3)
    return im


def s2(c, t):
    i = 2
    c.alpha_composite(synth_bg(t)); style_chip(c, i, True)
    place(c, neon(kid('A', 'happy', 280), (255, 60, 220), 18), 540, 1250, 1, 4 * math.sin(t * 3))
    items = [('Crypto', 'CRYPTO TIPS', (0, 230, 255), 300, 360), ('option', 'OPTION TRADES', (255, 80, 220), 780, 520), ('double', '2X FAST!', (255, 220, 60), 540, 700)]
    for ph, s_, col, x, y in items:
        tk = at(i, ph, -0.25)
        if t > tk: place(c, neon_text(s_, col, 90), x, y + 8 * math.sin(t * 4 + x), 0.6 + 0.4 * eback(prog(t, tk, 0.3)), -5 if x < 540 else 5)
    place(c, neon_text('ARUN CHASES HYPE', (255, 60, 220), 60), 540, 240, 1, 0, clamp((t - STARTS[i] - 0.2) * 3))
    caption(c, t, i, 1700, 44, by_sentence=True)


# ---------- 3. domino ----------
@functools.lru_cache(None)
def domino(txt, col):
    w, h = 170, 420
    im = Image.new('RGBA', (w + 14, h + 14), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((14, 14, w + 13, h + 13), 20, fill=(0, 0, 0, 90)); d.rounded_rectangle((0, 0, w - 1, h - 1), 20, fill=(250, 250, 245), outline=INK, width=7)
    d.line((14, h / 2, w - 14, h / 2), fill=INK, width=5); d.rectangle((7, 7, w - 8, 60), fill=col)
    for k, ln in enumerate(txt.split('\n')):
        t_ = text_img(ln, 'anton', 44, INK).rotate(90, expand=True); im.alpha_composite(t_, (int(w / 2 - t_.size[0] / 2) + (k - (len(txt.split('\n')) - 1) / 2) * 50 if False else int(w / 2 - t_.size[0] / 2 + (k - (len(txt.split('\n')) - 1) / 2) * 50), int(h * .72 - t_.size[1] / 2)))
    return im


def s3(c, t):
    i = 3
    c.alpha_composite(data_bg()); style_chip(c, i)
    head(c, t, i, "ARUN'S CHAIN REACTION", RED)
    dm = [('One loss', 'LOSS'), ('bigger bet', 'BIGGER\nBET'), ('loan', 'LOAN'), ('credit card', 'CARD\nBILL'), ('EMIs', 'EMIs')]
    d = ImageDraw.Draw(c); base = 1150
    d.rectangle((40, base, 1040, base + 20), fill=(120, 90, 60))
    for k, (ph, s_) in enumerate(dm):
        tk = at(i, ph, -0.15); x = 140 + k * 200
        ang = 0 if t < tk else min(68, (t - tk) * 260)
        im = domino(s_, RED if k == 4 else (230, 140, 30)).rotate(-ang, resample=Image.BICUBIC, expand=True, center=(184 * 0 + 0, 434))
        dom = domino(s_, RED if k == 4 else (230, 140, 30))
        rot = dom.rotate(-ang, resample=Image.BICUBIC, expand=True)
        r = math.radians(ang); w, h = dom.size
        px = x + math.sin(r) * h / 2; py = base - math.cos(r) * h / 2
        place(c, rot, px, py)
    host(c, t, [(STARTS[i], 2), (at(i, 'EMIs', -0.2), 12)], 540, 1430, 300)
    caption(c, t, i, 1700, 44, by_sentence=True)


# ---------- 4. isometric ----------
def iso_cube(d, cx, cy, s, h, top, left, right):
    p = lambda x, y, z: (cx + (x - y) * s * .866, cy + (x + y) * s * .5 - z)
    d.polygon([p(0, 0, h), p(1, 0, h), p(1, 1, h), p(0, 1, h)], fill=top, outline=INK)
    d.polygon([p(0, 1, h), p(1, 1, h), p(1, 1, 0), p(0, 1, 0)], fill=left, outline=INK)
    d.polygon([p(1, 0, h), p(1, 1, h), p(1, 1, 0), p(1, 0, 0)], fill=right, outline=INK)


def s4(c, t):
    i = 4
    c.alpha_composite(Image.new('RGBA', (W, H), (226, 240, 250, 255))); style_chip(c, i)
    d = ImageDraw.Draw(c)
    tn = at(i, 'Nifty', -0.3); q = clamp((t - tn) / 2.2)
    cols = [((120, 180, 240), (70, 130, 200), (50, 100, 170)), ((250, 200, 90), (220, 160, 50), (190, 130, 30)), ((140, 220, 160), (80, 170, 110), (60, 140, 90))]
    order = sorted([(x + y, x, y) for x in range(7) for y in range(8)])[:50]
    for n, (_, x, y) in enumerate(order):
        if n / 50 > q: break
        hh = 30 + ((x * 7 + y * 13) % 5) * 28
        top, left, right = cols[(x + y) % 3]
        iso_cube(d, 540 + (x - y) * 80 * .866, 420 + (x + y) * 80 * .5, 76, hh * 1.2, top, left, right)
    if t > tn + 0.6: place(c, pill_text(f'NIFTY 50 = {min(50, int(50 * q))} COMPANIES', BLUEB, (255, 255, 255), 58), 540, 1260, 1, -2)
    ts = at(i, 'tiny slice', -0.3)
    if t > ts: place(c, pill_text('BALA OWNS A TINY SLICE OF ALL', INK, YEL, 50), 540, 1380, 1, 2, clamp((t - ts) * 3))
    place(c, kid('B', 'happy', 200), 920, 1530)
    caption(c, t, i, 1700, 44, by_sentence=True)


# ---------- 5. glow atom ----------
def s5(c, t):
    i = 5
    c.alpha_composite(Image.new('RGBA', (W, H), (8, 12, 40, 255))); style_chip(c, i, True)
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(g); cx, cy = 540, 820
    te = at(i, 'emergency', -0.3)
    orb = [('shares', 'SHARES', (0, 220, 255), 330, 0), ('debt', 'DEBT', (120, 255, 140), 300, 60), ('gold', 'GOLD', (255, 210, 60), 270, -60)]
    for ph, lab, col, R, tilt in orb:
        tk = at(i, ph, -0.3)
        if t < tk: continue
        a0 = math.radians(tilt)
        pts = [(cx + R * math.cos(u) * math.cos(a0) - R * .38 * math.sin(u) * math.sin(a0), cy + R * math.cos(u) * math.sin(a0) + R * .38 * math.sin(u) * math.cos(a0)) for u in np.linspace(0, 2 * math.pi, 120)]
        d.line(pts + [pts[0]], fill=col + (255,), width=5)
        u = t * 1.6 + R; ex = cx + R * math.cos(u) * math.cos(a0) - R * .38 * math.sin(u) * math.sin(a0); ey = cy + R * math.cos(u) * math.sin(a0) + R * .38 * math.sin(u) * math.cos(a0)
        d.ellipse((ex - 26, ey - 26, ex + 26, ey + 26), fill=col + (255,))
    if t > te: d.ellipse((cx - 110, cy - 110, cx + 110, cy + 110), fill=(255, 120, 60, 255))
    glow = g.filter(ImageFilter.GaussianBlur(18)); c.alpha_composite(glow); c.alpha_composite(glow); c.alpha_composite(g)
    if t > te:
        place(c, text_img('EMERGENCY', 'anton', 44, (255, 255, 255)), cx, cy - 22); place(c, text_img('FUND', 'anton', 44, (255, 255, 255)), cx, cy + 26)
    for k, (ph, lab, col, R, tilt) in enumerate(orb):
        if t > at(i, ph, -0.3): place(c, neon_text(lab, col, 64), [220, 860, 540][k], [1230, 1230, 1360][k])
    caption(c, t, i, 1670, 40, by_sentence=True)


# ---------- 6. maths ----------
@functools.lru_cache(None)
def graph_bg():
    im = Image.new('RGB', (W, H), (252, 252, 246)); d = ImageDraw.Draw(im)
    for x in range(0, W, 30): d.line((x, 0, x, H), fill=(214, 232, 240) if x % 150 else (180, 210, 230), width=1 if x % 150 else 2)
    for y in range(0, H, 30): d.line((0, y, W, y), fill=(214, 232, 240) if y % 150 else (180, 210, 230), width=1 if y % 150 else 2)
    return im.convert('RGBA')


def s6(c, t):
    i = 6
    c.alpha_composite(graph_bg()); style_chip(c, i)
    d = ImageDraw.Draw(c); x0, y0, x1, y1 = 140, 1180, 980, 360
    d.line((x0, y0, x1 + 20, y0), fill=INK, width=6); d.line((x0, y0, x0, y1 - 40), fill=INK, width=6)
    ymax = 3.4
    X = lambda yr: x0 + (x1 - x0) * yr / 10; Y = lambda v: y0 - (y0 - y1) * v / ymax
    for yr in range(0, 11, 2): place(c, text_img(str(yr), 'osw', 34, INK), X(yr), y0 + 34)
    for v in (1, 2, 3): place(c, text_img(f'₹{v}L', 'osw', 34, INK), x0 - 55, Y(v))
    place(c, text_img('years', 'osw5', 30, GREY), x1, y0 + 76)
    tw = at(i, 'twelve', -0.3); q = clamp((t - tw) / 4.5)
    pts = [(X(yr), Y(1.12 ** yr)) for yr in np.linspace(0, 10 * q, 60)]
    if len(pts) > 1 and q > 0: d.line(pts, fill=BLUEB, width=9)
    place(c, text_img('V = 1 × (1.12)ⁿ'.replace('ⁿ', '^n'), 'anton', 64, INK), 540, 260, 1, 0, clamp((t - STARTS[i] - 0.3) * 3))
    td = at(i, 'doubles', -0.2)
    if t > td:
        d.line((X(6.1), Y(2), X(6.1), y0), fill=RED, width=4)
        d.ellipse((X(6.1) - 16, Y(2) - 16, X(6.1) + 16, Y(2) + 16), fill=RED)
        place(c, pill_text('72 ÷ 12 = 6 YEARS → 2x'.replace('→', '='), RED, (255, 255, 255), 44), 420, 1330, 1, -2)
    tt = at(i, 'three point one', -0.2)
    if t > tt:
        d.ellipse((X(10) - 18, Y(3.106) - 18, X(10) + 18, Y(3.106) + 18), fill=GREEN)
        place(c, pill_text('10 YEARS = ₹3.1 LAKH', GREEN, (255, 255, 255), 52), 650, 1440, 1, 2)
    caption(c, t, i, 1620, 42, by_sentence=True)
    place(c, text_img('12% a year is an assumption for illustration, not a guaranteed return', 'osw5', 26, GREY), 540, 1840)


# ---------- 7. 3D chart ----------
def bar3d(d, x, base, w, h, col):
    dx, dy = w * .35, w * .25
    dark = tuple(int(v * .7) for v in col); light = tuple(min(255, int(v * 1.2)) for v in col)
    d.polygon([(x, base - h), (x + w, base - h), (x + w + dx, base - h - dy), (x + dx, base - h - dy)], fill=light, outline=INK)
    d.polygon([(x + w, base), (x + w + dx, base - dy), (x + w + dx, base - h - dy), (x + w, base - h)], fill=dark, outline=INK)
    d.rectangle((x, base - h, x + w, base), fill=col, outline=INK, width=4)


def s7(c, t):
    i = 7
    c.alpha_composite(Image.new('RGBA', (W, H), (20, 24, 38, 255))); style_chip(c, i, True)
    d = ImageDraw.Draw(c); base = 1150
    for k in range(6): d.line((80 + k * 40, base - k * 0, 1040, base), fill=(60, 70, 90), width=1)
    d.polygon([(80, base), (1000, base), (1060, base - 50), (140, base - 50)], fill=(40, 46, 66))
    tb = at(i, 'Bala has', -0.2); q = eo(prog(t, tb, 1.0))
    if t > tb:
        bar3d(d, 220, base, 220, int(540 * q), GREEN)
        place(c, text_img(f'₹{1 + 2.1 * q:.1f} LAKH', 'anton', 70, (255, 255, 255)), 330, base - int(540 * q) - 80)
        place(c, kid('B', 'happy', 200), 330, base + 140)
    ta = at(i, 'And Arun', -0.2)
    if t > ta:
        bar3d(d, 640, base, 220, 30, RED); place(c, kid('A', 'sad', 200), 750, base + 140)
    tn = at(i, 'ninety one', -0.2)
    if t > tn:
        place(c, info((('91% OF F&O TRADERS', 60, RED), ('lost money (SEBI study, FY25)', 38, GREY)), 860, RED), 540, 330, 0.6 + 0.4 * eback(prog(t, tn, 0.3)), -2)
        stamp_at(c, t, 'LOST', RED, 110, -10, tn, 750, 1000, 3)
    caption(c, t, i, 1690, 42, by_sentence=True)


# ---------- 8. paper-cut ----------
@functools.lru_cache(None)
def paper_layer(col, y, amp_, seed, sh=True):
    im = Image.new('RGBA', (W + 200, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pts = [(0, H)] + [(x, y + amp_ * math.sin(x / 140 + seed) + amp_ * .5 * math.sin(x / 57 + seed * 2)) for x in range(0, W + 201, 20)] + [(W + 200, H)]
    d.polygon(pts, fill=col)
    if not sh: return im
    shadow = Image.new('RGBA', im.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(shadow); sd.polygon([(x, y_ - 14) for x, y_ in pts], fill=(0, 0, 0, 90))
    out = Image.new('RGBA', im.size, (0, 0, 0, 0)); out.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(10))); out.alpha_composite(im); return out


@functools.lru_cache(None)
def paper_shape(kind):
    im = Image.new('RGBA', (300, 220), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if kind == 'hare':
        d.ellipse((40, 90, 220, 190), fill=(235, 235, 240)); d.ellipse((180, 50, 270, 130), fill=(235, 235, 240))
        d.ellipse((200, 0, 225, 80), fill=(235, 235, 240)); d.ellipse((230, 0, 255, 80), fill=(235, 235, 240)); d.ellipse((240, 80, 252, 92), fill=INK)
    else:
        d.chord((50, 60, 250, 230), 180, 360, fill=(90, 160, 80)); d.ellipse((230, 110, 290, 160), fill=(140, 190, 110)); d.ellipse((268, 122, 278, 132), fill=INK)
        d.rectangle((80, 140, 110, 175), fill=(140, 190, 110)); d.rectangle((190, 140, 220, 175), fill=(140, 190, 110))
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh.putalpha(im.getchannel('A').point(lambda v: v * 90 // 255))
    out = Image.new('RGBA', (320, 240), (0, 0, 0, 0)); out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)), (12, 14)); out.alpha_composite(im); return out


def s8(c, t):
    i = 8
    c.alpha_composite(Image.new('RGBA', (W, H), (250, 236, 210, 255))); style_chip(c, i)
    lt = t - STARTS[i]
    for k, (col, y, a, sp) in enumerate((((240, 190, 140), 700, 60, 10), ((220, 150, 110), 860, 50, 25), ((170, 110, 90), 1020, 40, 45))):
        c.alpha_composite(paper_layer(col, y, a, k * 1.7), (int(-((lt * sp) % 200)), 0))
    th = at(i, 'hare', -0.3); tt = at(i, 'tortoise', -0.3)
    hx = 150 + min(1, (t - th) / 1.0) * 500 if t > th else -300
    if t > tt: hx = 650 + (0 if t < tt else 0)
    place(c, paper_shape('hare'), hx, 1180 - abs(math.sin(lt * 9)) * 40 * (t < tt))
    if t > th: place(c, text_img('z z z', 'anton', 50, INK), hx + 80, 1040, 1, 0, 1 if t > tt else 0)
    tx = 100 + min(1, max(0, (t - th) / 5.5)) * 840
    place(c, paper_shape('tortoise'), tx, 1240)
    tm = at(i, 'Time in', -0.2)
    if t > tm:
        place(c, pill_text('TIME IN THE MARKET', (255, 255, 255), INK, 66), 540, 360, 0.6 + 0.4 * eback(prog(t, tm, 0.3)), -2)
        place(c, text_img('beats', 'anton', 60, INK), 540, 470, 1, 0, clamp((t - tm - 0.4) * 3))
        place(c, pill_text('TIMING THE MARKET', RED, (255, 255, 255), 66), 540, 580, 1, 2, clamp((t - tm - 0.6) * 3))
    caption(c, t, i, 1690, 44, by_sentence=True)


# ---------- 9. flat vector ----------
def s9(c, t):
    i = 9
    c.alpha_composite(Image.new('RGBA', (W, H), (255, 236, 220, 255)))
    d = ImageDraw.Draw(c)
    d.ellipse((-200, 1300, 600, 2100), fill=(255, 200, 170)); d.ellipse((600, -200, 1300, 500), fill=(200, 230, 250))
    style_chip(c, i)
    place(c, pill_text('WHICH FRIEND ARE YOU?', INK, YEL, 70), 540, 290, 0.6 + 0.4 * eback(prog(t, STARTS[i] + 0.1, 0.3)), -2)
    place(c, kid('A', 'sad', 260, flat=True), 280, 640); place(c, kid('B', 'happy', 260, flat=True), 800, 640)
    place(c, text_img('A · HYPE', 'anton', 54, ORANGE), 280, 870); place(c, text_img('B · PATIENCE', 'anton', 54, BLUEB), 800, 870)
    host(c, t, [(STARTS[i], 14), (at(i, 'Save', -0.2), 31)], 540, 1180, 440)
    tf = at(i, 'follow', -0.1)
    if t > tf: place(c, follow_btn(), 540, 1530, 0.6 + 0.4 * eback(prog(t, tf, 0.35)), 2)
    src(c, 'Characters are fictional · Not a buy/sell call · Education only', 1880)


SCENES = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9]


def slam_times():
    return [0.15, at(3, 'EMIs', -0.2), at(7, 'ninety one', -0.2)]


def footer(c):
    d = ImageDraw.Draw(c)
    d.rectangle((0, 1888, W, H), fill=(20, 22, 30, 255))
    place(c, text_img('Fictional story · Education only · Not a buy/sell call · @moneyincloud', 'osw5', 22, (230, 230, 236)), 540, 1904)
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
