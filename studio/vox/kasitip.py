"""Cloud Family Ep 1: Never trust this uncle's sure-shot tip. 91% of F&O traders lost money (SEBI FY25).
Realistic cast cut-outs, multi-voice dialogue (vo_cast.py), light template, red topic colour."""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, textwrap, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from lib import *
from scenes import stamp_c
from fridge import follow_btn

SH = ROOT + 'kasitip/'
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


# ---------------- scenes ----------------
def s0(c, t):  # hook
    i = 0
    c.alpha_composite(red_bg())
    rise = eo(prog(t, 0.0, 0.6))
    actor(c, t, i, 'kasi_smug', 540, 800, base=H + 10 + (1 - rise) * 300)
    words = [('NEVER TRUST', 150, (255, 247, 230), 0.05), ("THIS UNCLE'S", 120, (255, 247, 230), at(i, 'this', -0.1))]
    y = 300
    for s, sz, col, t0 in words:
        place_text(c, s, 'anton', sz, col, 540, y, t, None, t0, 'pop'); y += sz * 1.05
    if t > at(i, 'sure', -0.15):
        p = prog(t, at(i, 'sure', -0.15), 0.3)
        place(c, pill_text('SURE-SHOT TIP?', YEL, INK, 96), 540, y + 40, 0.6 + 0.4 * eback(p), -3, clamp(p * 3))
    stamp_at(c, t, '91% LOST MONEY', (255, 255, 255), 112, -8, at(i, 'Ninety', -0.1), 540, 1240, 3)


def s1(c, t):
    i = 1
    c.alpha_composite(room_bg())
    nm = 'kasi_laugh' if t < at(i, 'Ten thousand', -0.1) else 'kasi_happy'
    actor(c, t, i, nm, 560, 780, enter=(STARTS[i], 0))
    bubble(c, t, i, 380, 520)
    t1 = at(i, 'Ten thousand', -0.1)
    if t > t1:
        p = prog(t, t1, 0.35)
        place(c, pill_text('₹10,000 TO ₹1,00,000', (36, 170, 90), (255, 255, 255), 70), 540, 770, 0.5 + 0.5 * eback(p), 2, clamp(p * 3))
    stamp_at(c, t, 'SURE-SHOT!', YEL, 96, -10, at(i, 'sure shot', -0.05), 790, 960, 4)


def s2(c, t):
    i = 2
    c.alpha_composite(room_bg())
    actor(c, t, i, 'arjun_laugh', 470, 760, enter=(STARTS[i], 500))
    bubble(c, t, i, 360, 470)
    t1 = at(i, 'opening', -0.25)
    if t > t1:
        p = prog(t, t1, 0.4)
        place(c, phone_img(False), 860, 1060 + (1 - eo(p)) * 500, 0.85, 8 - 6 * eo(p))


def s3(c, t):
    i = 3
    c.alpha_composite(room_bg())
    actor(c, t, i, 'amma_smug', 540, 820, enter=(STARTS[i], -600))
    bubble(c, t, i, 400, 540, size=64)


def s4(c, t):
    i = 4
    c.alpha_composite(room_bg())
    nm = 'kasi_think' if t < at(i, 'Everybody', -0.1) else 'kasi_smug'
    actor(c, t, i, nm, 560, 780)
    bubble(c, t, i, 380, 560)


def s5(c, t):
    i = 5
    c.alpha_composite(room_bg())
    actor(c, t, i, 'amma_think', 330, 640, bob=False)
    caption(c, t, i, 330)
    t1 = at(i, 'the government', -0.3)
    if t > t1:
        p = prog(t, t1, 0.5)
        place(c, doc_card(), 780 + (1 - eo(p)) * 500, 1000, 0.95, 4 - 4 * (1 - eo(p)))
    stamp_at(c, t, 'OFFICIAL DATA', (30, 130, 70), 70, -12, at(i, 'counted', -0.1), 790, 1240, 5)


def s6(c, t):  # data
    i = 6
    c.alpha_composite(data_bg())
    tB = at(i, 'Together', -0.15); tC = at(i, 'The average', -0.15); tD = at(i, 'Ten times', -0.15)
    place_text(c, 'F&O TRADERS · ONE YEAR (FY25)', 'osw', 44, NAVY, 540, 215, t, None, STARTS[i], 'slide')
    if t < tB:
        tr = at(i, 'ninety one', -0.1)
        x0, y0, g = 540 - 4.5 * 84, 330, 84
        for k in range(100):
            r, q = divmod(k, 10)
            tk = STARTS[i] + 0.1 + k * 0.006
            if t < tk: continue
            red = t > tr + k * 0.016 and k < 91
            place(c, icon((226, 58, 44) if red else (36, 170, 90) if t > tr else (150, 156, 170)), x0 + q * g, y0 + r * g,
                  0.6 + 0.4 * eback(prog(t, tk, 0.25)))
        if t > tr:
            n = min(91, int((t - tr) / 0.016))
            place_text(c, f'{n} OUT OF 100', 'anton', 140, (226, 58, 44), 540, 1250, t, None, tr, 'pop')
            place_text(c, 'LOST MONEY', 'anton', 110, INK, 540, 1390, t, None, tr + 0.2, 'pop')
    elif t < tC:
        p = eo(prog(t, tB + 0.2, 1.6))
        place_text(c, 'TOTAL NET LOSS', 'osw', 60, GREY, 540, 430, t, None, tB, 'slide')
        place(c, text_img(f'₹{inr(105603 * p)} CR', 'anton', 150, (226, 58, 44)), 540, 600)
        place_text(c, '(about ₹1.06 lakh crore)', 'osw5', 44, INK, 540, 735, t, None, tB + 1.4, 'fade')
        # red falling line
        pts = []
        for k in range(40):
            q = k / 39
            if q > eo(prog(t, tB, 2.2)): break
            pts.append((120 + q * 840, 880 + q * 360 + 40 * math.sin(q * 11)))
        if len(pts) > 1: stroke(c, pts, 12, (226, 58, 44))
        if t > tB + 1.8:
            place(c, pill_text('UP 41% FROM FY24 (₹74,812 CR)', (255, 255, 255), INK, 44), 540, 1330, 1, -2,
                  clamp((t - tB - 1.8) * 3))
    else:
        place_text(c, 'AVERAGE LOSS PER TRADER', 'osw', 56, GREY, 540, 420, t, None, tC, 'slide')
        place_text(c, '₹1.1 LAKH', 'anton', 170, (226, 58, 44), 540, 600, t, None, tC + 0.3, 'pop')
        place_text(c, 'about', 'osw5', 44, GREY, 540, 500, t, None, tC + 0.3, 'fade')
        if t > tD:
            base = 1300
            for k, (lab, v, colr) in enumerate([("ARJUN'S ₹10,000", 10000, (36, 170, 90)), ('AVG LOSS ₹1,10,000', 110000, (226, 58, 44))]):
                tk = tD + k * 0.5
                if t < tk: continue
                q = eo(prog(t, tk, 0.8)); hgt = int(v / 110000 * 480 * q); x = 560 + k * 300
                ImageDraw.Draw(c).rounded_rectangle((x - 100, base - max(hgt, 6), x + 100, base), 14, fill=colr, outline=INK, width=6)
                place(c, text_img(lab, 'osw', 34, INK), x, base + 44)
            ImageDraw.Draw(c).line((400, base, 1040, base), fill=INK, width=6)
            stamp_at(c, t, '10X', INK, 110, -10, tD + 1.0, 690, 900, 6)
            actor(c, t, i, 'arjun_worried', 200, 340, base=base + 90, bob=False, enter=(tD + 0.6, -300))
    caption(c, t, i, 1600, 50, by_sentence=True)
    src(c, 'Source: SEBI study of individual F&O traders, FY25 (July 2025)')


def s7(c, t):
    i = 7
    c.alpha_composite(room_bg())
    p = prog(t, STARTS[i], 0.25)
    ov = Image.new('RGBA', (W, H), (226, 58, 44, int(110 * (1 - p))))
    actor(c, t, i, 'arjun_shock', 540, 860)
    c.alpha_composite(ov)
    bubble(c, t, i, 360, 540, size=66)
    place(c, phone_img(True), 860, 1250, 0.8, -10)


def s8(c, t):
    i = 8
    c.alpha_composite(room_bg())
    nm = 'paati_think' if t < at(i, 'Who gains', -0.2) else 'paati_laugh'
    actor(c, t, i, nm, 300, 640)
    bubble(c, t, i, 340, 330, size=44)
    items = [('Who gains', 'WHO GAINS?', (40, 100, 200)), ('Will he', 'SHOWS HIS OWN P&L?', (125, 60, 150)),
             ('how much', 'HOW MUCH CAN YOU LOSE?', (226, 58, 44))]
    for k, (ph, txt, colr) in enumerate(items):
        tk = at(i, ph, -0.15)
        if t < tk: continue
        p = prog(t, tk, 0.4)
        place(c, card(k + 1, txt, colr, 560), 760 + (1 - eo(p)) * 400, 820 + k * 150, 1, -2 + k * 1.5, clamp(p * 3))


def s9(c, t):
    i = 9
    c.alpha_composite(room_bg())
    actor(c, t, i, 'thatha_laugh', 470, 800)
    bubble(c, t, i, 380, 470)
    tk = at(i, 'trading account', -0.4)
    if t > tk:
        actor(c, t, i, 'kasi_shock', 880, 420, base=H + 10, bob=False, enter=(tk, 400))
        stamp_at(c, t, 'CAUGHT!', (226, 58, 44), 70, 10, tk + 0.4, 880, 1400, 7)


def s10(c, t):
    i = 10
    c.alpha_composite(room_bg())
    tk = at(i, 'Next time', -0.2)
    caption(c, t, i, 330)
    if t < tk:
        p = prog(t, STARTS[i], 0.5)
        place(c, family_print(), 540, 900 + (1 - eo(p)) * 300, 1, -3, clamp(p * 3))
        tf = at(i, 'Send', -0.1)
        if t > tf:
            place(c, pill_text('SEND TO YOUR FAMILY GROUP', YEL, INK, 58), 540, 1300, 0.6 + 0.4 * eback(prog(t, tf, 0.35)), -2)
        tf2 = at(i, 'Follow', -0.1)
        if t > tf2:
            place(c, follow_btn(), 540, 1480, 0.6 + 0.4 * eback(prog(t, tf2, 0.35)), 2)
    else:
        rise = eo(prog(t, tk, 0.5))
        actor(c, t, i, 'kasi_smug', 540, 800, base=H + 10 + (1 - rise) * 400, bob=False)
        place(c, phone_img(False), 870, 1250, 0.7, 10, clamp((t - tk) * 3))
    src(c, 'Characters are fictional · Education only · Not a buy/sell call', 1880)


SCENES = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]


def slam_times():
    return [at(0, 'Ninety', -0.1), at(1, 'sure shot', -0.05), STARTS[7], at(9, 'trading account', 0.0)]


def footer(c):
    d = ImageDraw.Draw(c)
    d.rectangle((0, 1888, W, H), fill=(20, 22, 30, 255))
    place(c, text_img('Not a buy/sell call · Education only · @moneyincloud', 'osw5', 24, (230, 230, 236)), 540, 1904)


def render(t):
    LOOP = 0.5
    if t > DUR - LOOP:
        a = _render(t); b = _render(0.9, loop=True); q = eio((t - (DUR - LOOP)) / LOOP)
        return (a * (1 - q) + b * q).astype(np.uint8)
    return _render(t)


def _render(t, loop=False):
    i = scene_at(t)
    c = Image.new('RGBA', (W, H), (255, 255, 255, 255))
    st = STARTS[i]; en = STARTS[i + 1] if i + 1 < len(STARTS) else DUR
    SCENES[i](c, t)
    z = 1.0 + 0.035 * clamp((t - st) / (en - st)) + (0.06 * math.exp(-(t - st) * 9) if i > 0 else 0)
    sx = sy = 0
    for ts in slam_times():
        if 0 <= t - ts < 0.35:
            k = math.exp(-(t - ts) * 14) * 10
            sx += k * math.sin((t - ts) * 90); sy += k * math.cos((t - ts) * 77)
    cw, ch = W / z, H / z
    cx, cy = W / 2 + sx, H * 0.5 + sy
    c = c.transform((W, H), Image.EXTENT, (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2), Image.BICUBIC)
    # quick white flash on cuts
    if i > 0 and t - st < 0.08:
        c = Image.blend(c, Image.new('RGBA', (W, H), (255, 255, 255, 255)), 0.5 * (1 - (t - st) / 0.08))
    if i not in (10,): footer(c)
    return np.asarray(c.convert('RGB'))
