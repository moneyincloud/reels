"""10-second animation test for the storybook format (Karthi, lifestyle creep).
Layers: inpainted background + cut-out foreground (Karthi + props) with parallax, breathing, hops, emotion FX."""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, re
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from lib import *
from scenes import stamp_c

SH = ROOT + 'storytest/'
LAY = ROOT + 'storyreel/layers/'
SCRIPT = [l['text'] for l in json.load(open(SH + 'lines.json'))]
DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO = [], []
_t = 0.0
for i, d in enumerate(DURS):
    STARTS.append(_t); VO.append(_t + 0.25); _t = VO[-1] + d + 0.35
DUR = _t + 0.8
B = STARTS[1:]
SC = ['02', '05', '08']
MUST = (232, 160, 30); TERRA = (196, 92, 48); CREAM = (255, 246, 228); BROWN = (92, 52, 24); RED = (214, 52, 40); GRN = (40, 150, 80)


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase); assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def line_at(t):
    i = 0
    for k, s in enumerate(STARTS):
        if t >= s: i = k
    return i


@functools.lru_cache(None)
def layer(kind, n):
    im = Image.open(f'{LAY}{kind}{n}.png').convert('RGBA')
    s = max(W * 1.12 / im.size[0], H * 1.12 / im.size[1])     # cover + margin for motion
    return im.resize((int(im.size[0] * s), int(im.size[1] * s)), Image.LANCZOS)


@functools.lru_cache(None)
def head_xy(n):
    a = np.asarray(layer('fg', n))[..., 3] > 100
    ys, xs = np.where(a)
    # topmost 6% of the figure ~ head
    top = ys.min(); sel = ys < top + (ys.max() - top) * 0.12
    return float(xs[sel].mean()), float(top)


@functools.lru_cache(None)
def frame_border():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k, (w, col) in enumerate([(26, (150, 70, 20)), (16, (226, 150, 40)), (6, (120, 50, 15))]):
        o = [0, 26, 42][k]
        d.rectangle((o, o, W - 1 - o, H - 1 - o), outline=col, width=w)
    for cx, cy in [(48, 48), (W - 48, 48), (48, H - 48), (W - 48, H - 48)]:
        for r, col in [(46, (226, 150, 40)), (32, (150, 70, 20)), (16, (255, 214, 120))]:
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col)
        for a in range(8):
            ang = a * math.pi / 4
            d.ellipse((cx + 58 * math.cos(ang) - 9, cy + 58 * math.sin(ang) - 9, cx + 58 * math.cos(ang) + 9, cy + 58 * math.sin(ang) + 9), fill=(226, 150, 40))
    for x in range(140, W - 140, 70):
        for y in (21, H - 21):
            d.polygon([(x, y - 9), (x + 9, y), (x, y + 9), (x - 9, y)], fill=(255, 214, 120))
    for y in range(140, H - 140, 70):
        for x in (21, W - 21):
            d.polygon([(x, y - 9), (x + 9, y), (x, y + 9), (x - 9, y)], fill=(255, 214, 120))
    return im


def scene(c, t, n, st, en, mood):
    q = clamp((t - st) / (en - st))
    bg, fg = layer('bg', n), layer('fg', n)
    # camera: slow push + drift; fg moves 1.6x more (parallax)
    z = 1.0 + 0.06 * q
    dx = -18 + 36 * q
    def put(im, k, extra_y=0.0, sx=1.0, sy=1.0, rot=0.0):
        w, h = int(im.size[0] * z * sx), int(im.size[1] * z * sy)
        r = im.resize((w, h), Image.BILINEAR)
        if rot: r = r.rotate(rot, Image.BILINEAR, expand=False, center=(w / 2, h))
        c.alpha_composite(r, (int(W / 2 - w / 2 + dx * k), int(H / 2 - h / 2 + extra_y + (h - h / sy * 1) * 0)))
    put(bg, 1.0)
    breathe = 1 + 0.010 * math.sin(t * 2.6)
    hop = 0.0; rot = 0.4 * math.sin(t * 1.3)
    if mood == 'happy':
        k = (t - at(0, 'fifteen', 0)) if t > at(0, 'fifteen', 0) else -1
        if 0 <= k < 0.6: hop = -40 * math.sin(k / 0.6 * math.pi)
        rot += 1.2 * math.sin(t * 5)
    if mood == 'sad':
        hop = 12 * eo(prog(t, st, 0.8)); rot = 0.2 * math.sin(t * 1.0)
    fgh = fg.size[1] * z
    put(fg, 1.6, hop + fgh * (1 - breathe) * 0.5, 1.0, breathe, rot)
    return z, dx


def head_screen(n, z, dx):
    hx, hy = head_xy(n); fg = layer('fg', n)
    return W / 2 + (hx - fg.size[0] / 2) * z + dx * 1.6, H / 2 + (hy - fg.size[1] / 2) * z


def sparkle(c, x, y, t, k):
    d = ImageDraw.Draw(c); a = 0.5 + 0.5 * math.sin(t * 7 + k * 2.1); r = 10 + 18 * a
    d.polygon([(x, y - r), (x + r * 0.25, y - r * 0.25), (x + r, y), (x + r * 0.25, y + r * 0.25), (x, y + r), (x - r * 0.25, y + r * 0.25),
               (x - r, y), (x - r * 0.25, y - r * 0.25)], fill=(255, 236, 140), outline=BROWN)


def coin(c, x, y, s=1.0):
    d = ImageDraw.Draw(c); r = 30 * s
    d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 200, 50), outline=BROWN, width=4)
    d.text((x, y + 2), '₹', font=font('pop', int(34 * s)), fill=BROWN, anchor='mm')


def rain_cloud(c, x, y, t, a):
    d = ImageDraw.Draw(c, 'RGBA')
    for (ox, oy, r) in [(-60, 10, 48), (0, -14, 62), (64, 8, 50), (-20, 30, 44), (34, 32, 44)]:
        d.ellipse((x + ox - r, y + oy - r, x + ox + r, y + oy + r), fill=(110, 116, 130, int(235 * a)), outline=(60, 60, 70, int(255 * a)), width=4)
    for k in range(9):
        ph = (t * 1.8 + k * 0.37) % 1
        rx = x - 80 + k * 20; ry = y + 60 + ph * 220
        d.line((rx, ry, rx - 6, ry + 26), fill=(90, 150, 230, int(220 * a * (1 - ph))), width=5)


def sweat(c, x, y, t):
    ph = (t * 0.9) % 1
    d = ImageDraw.Draw(c, 'RGBA'); yy = y + ph * 60
    d.polygon([(x, yy - 26), (x + 16, yy + 6), (x - 16, yy + 6)], fill=(140, 200, 255, int(255 * (1 - ph))))
    d.ellipse((x - 16, yy - 6, x + 16, yy + 22), fill=(140, 200, 255, int(255 * (1 - ph))), outline=(40, 90, 160, int(255 * (1 - ph))), width=3)


def tag(s, bg, fg=(255, 255, 255), size=64):
    tt = text_img(s, 'anton', size, fg)
    w, h = tt.size[0] + 64, tt.size[1] + 30
    im = Image.new('RGBA', (w + 12, h + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((12, 12, w + 11, h + 11), 26, fill=BROWN)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 26, fill=bg, outline=BROWN, width=6)
    im.alpha_composite(tt, (32, 15))
    return im


tag = functools.lru_cache(None)(tag)


def segs(i):
    return [(m.start(), m.end()) for m in re.finditer(r'[^.!?]+[.!?]*\s*', SCRIPT[i])]


def caption(c, t, i, cy=1660, size=50):
    if t < VO[i] - 0.05: return
    sp = clamp((t - VO[i]) / DURS[i]) * len(SCRIPT[i])
    sg = [g for g in segs(i) if g[0] <= sp][-1] if sp > 0 else segs(i)[0]
    words = SCRIPT[i][sg[0]:sg[1]].split()
    s = ' '.join(words); w = text_w(s, 'pop', size) + 80
    im = Image.new('RGBA', (w + 10, int(size * 1.9) + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 10, w + 9, int(size * 1.9) + 9), 30, fill=BROWN)
    d.rounded_rectangle((0, 0, w - 1, int(size * 1.9) - 1), 30, fill=CREAM, outline=BROWN, width=5)
    x = 40; pos = sg[0]
    for wd in words:
        col = BROWN if pos <= sp else (190, 160, 130)
        if pos <= sp and (wd.lower().startswith(('fifteen', 'zero', 'one')) or any(ch.isdigit() for ch in wd)): col = TERRA
        ti = text_img(wd, 'pop', size, col); im.alpha_composite(ti, (int(x - size * 0.12), int(size * 0.95 - ti.size[1] / 2)))
        x += text_w(wd + ' ', 'pop', size); pos += len(wd) + 1
    sc = min(1.0, 980 / im.size[0])
    place(c, im, 540, cy, sc)


def _render(t):
    i = line_at(t)
    c = Image.new('RGBA', (W, H), CREAM)
    st = STARTS[i]; en = STARTS[i + 1] if i + 1 < len(STARTS) else DUR
    mood = ['happy', 'spend', 'sad'][i]
    z, dx = scene(c, t, SC[i], st, en, mood)
    hx, hy = head_screen(SC[i], z, dx)
    if i == 0:
        t1 = at(0, 'fifteen', -0.1)
        if t > t1:
            p = prog(t, t1, 0.35)
            place(c, tag('+₹15,000 HIKE', GRN, size=80), 540, 330, 0.5 + 0.5 * eback(p), -3)
            for k in range(8):
                kk = (t - t1 - k * 0.05)
                if 0 < kk < 1.4:
                    ang = -math.pi / 2 + (k - 3.5) * 0.32
                    coin(c, hx + math.cos(ang) * 420 * kk, hy + 60 + math.sin(ang) * 420 * kk + 380 * kk * kk, 0.9)
        for k, (ox, oy) in enumerate([(-170, 20), (160, -10), (-120, -90), (140, 110)]):
            if t > 0.6: sparkle(c, hx + ox, hy + oy, t, k)
    elif i == 1:
        items = [('Bigger flat', '+₹6,000 RENT'), ('New bike', '+₹5,000 EMI'), ('Food delivery', '+₹2,500 FOOD')]
        spent = 0; amt = [6000, 5000, 2500]
        for k, (ph, s) in enumerate(items):
            tk = at(1, ph, -0.15)
            if t < tk: continue
            spent += amt[k]
            p = prog(t, tk, 0.4)
            x = [300, 780, 330][k]; y = [300, 470, 640][k]
            place(c, tag(s, RED, size=58), x + (1 - eo(p)) * (600 if k % 2 else -600), y, 1, [-5, 4, -3][k])
        if spent:
            place(c, tag(f'SPENT ₹{spent:,} OF ₹15,000', BROWN, CREAM, 50), 540, 820, 1, 0)
    else:
        t1 = STARTS[2]
        p = prog(t, t1, 0.3)
        if t < at(2, 'Zero', -0.2):
            place(c, tag('1 YEAR LATER', TERRA, size=90), 540, 420, 1.6 - 0.6 * eback(p), -3, clamp(p * 3))
        else:
            c.alpha_composite(Image.new('RGBA', (W, H), (120, 20, 10, int(70 * clamp((t - at(2, 'Zero', -0.2)) * 3)))))
            pz = prog(t, at(2, 'Zero', -0.2), 0.22)
            place(c, stamp_c('₹0 SAVED', RED, 130, -8, 3), 540, 420, 1 + 1.2 * (1 - eo(pz)), 0, clamp(pz * 4))
        rain_cloud(c, hx, hy - 120, t, clamp((t - t1 - 0.3) * 3))
        sweat(c, hx + 110, hy + 60, t)
    caption(c, t, i)
    c.alpha_composite(frame_border())
    # shake on the shock
    if i == 2 and 0 <= t - at(2, 'Zero', -0.2) < 0.4:
        k = math.exp(-(t - at(2, 'Zero', -0.2)) * 10) * 14; ox = k * math.sin(t * 90); oy = k * math.cos(t * 70)
        c = c.transform((W, H), Image.AFFINE, (1, 0, ox, 0, 1, oy), Image.BICUBIC)
    # cross-dissolve between scenes
    for b in B:
        if 0 <= t - b < 0.25:
            pass
    return c


def render(t):
    for b in B:
        if b - 0.18 <= t < b:
            a = np.asarray(_render(t).convert('RGB')).astype(float); bb = np.asarray(_render(b + 0.01).convert('RGB')).astype(float)
            q = (t - (b - 0.18)) / 0.18
            return (a * (1 - q) + bb * q).astype(np.uint8)
    return np.asarray(_render(t).convert('RGB'))
