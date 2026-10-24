import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, random, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

W, H, FPS = 1080, 1920, 30
FD = ROOT + 'fonts/'
FONTS = {
    'anton': FD + 'anton-latin-400-normal.woff',
    'osw': FD + 'oswald-latin-700-normal.woff',
    'osw5': FD + 'oswald-latin-500-normal.woff',
    'mark': FD + 'permanent-marker-latin-400-normal.woff',
    'pfi': FD + 'playfair-display-latin-800-italic.woff',
    'pf': FD + 'playfair-display-latin-900-normal.woff',
    'type': FD + 'special-elite-latin-400-normal.woff',
    'pop': FD + 'Poppins-Bold.ttf',
}
PAPER = (239, 232, 218)
INK = (27, 27, 27)
CREAM = (246, 241, 230)
YEL = (255, 214, 51)
RED = (226, 58, 44)
GRN = (36, 138, 84)
DARK = (30, 29, 28)


@functools.lru_cache(None)
def font(name, size):
    return ImageFont.truetype(FONTS[name], int(size))


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def eo(p):  # ease out cubic
    p = clamp(p); return 1 - (1 - p) ** 3


def eio(p):
    p = clamp(p); return 3 * p * p - 2 * p * p * p


def eback(p, s=1.9):
    p = clamp(p); p -= 1; return p * p * ((s + 1) * p + s) + 1


def prog(t, t0, d):
    return clamp((t - t0) / d)


def rnd(*key):
    return random.Random(hash(key) & 0xffffffff)


def jit(key, t, amp=3.0, ramp=0.7):
    """stop-motion boil: changes 12 times a second"""
    r = rnd(key, int(t * 12))
    return r.uniform(-amp, amp), r.uniform(-amp, amp), r.uniform(-ramp, ramp)


@functools.lru_cache(512)
def text_img(s, fn, size, fill, track=0):
    f = font(fn, size)
    asc, desc = f.getmetrics()
    ch = -f.getbbox('H', anchor='ls')[1]
    rf = None
    if '₹' in s:
        pf = font('pop', 100); rh = -pf.getbbox('₹', anchor='ls')[1]
        rf = font('pop', max(8, int(100 * ch / rh)))
    segs = []
    if track:
        for c in s: segs.append(c)
    else:
        cur = ''
        for c in s:
            if c == '₹':
                if cur: segs.append(cur)
                segs.append('₹'); cur = ''
            else:
                cur += c
        if cur: segs.append(cur)
    x = 0; lay = []
    for sg in segs:
        ff = rf if sg == '₹' else f
        lay.append((x, sg, ff))
        x += ff.getlength(sg) + track
        if sg == '₹': x += size * 0.04
    pad = int(size * 0.12)
    im = Image.new('RGBA', (int(x) + 2 * pad, asc + desc + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for (lx, sg, ff) in lay:
        d.text((pad + lx, pad + asc), sg, font=ff, fill=fill, anchor='ls')
    return im


def text_w(s, fn, size, track=0):
    im = text_img(s, fn, size, (0, 0, 0), track)
    return im.size[0] - 2 * int(size * 0.12)


def comp(canvas, im, x, y):
    x, y = int(x), int(y)
    cw, ch = canvas.size; w, h = im.size
    if x >= cw or y >= ch or x + w <= 0 or y + h <= 0: return
    sx, sy = max(0, -x), max(0, -y)
    ex, ey = min(w, cw - x), min(h, ch - y)
    canvas.alpha_composite(im.crop((sx, sy, ex, ey)), (max(0, x), max(0, y)))


def place(canvas, img, cx, cy, scale=1.0, rot=0.0, alpha=1.0):
    if img is None or alpha <= 0.003 or scale <= 0.01: return
    im = img
    if abs(scale - 1) > 0.002:
        im = im.resize((max(1, int(im.size[0] * scale)), max(1, int(im.size[1] * scale))), Image.BICUBIC)
    if abs(rot) > 0.05:
        im = im.rotate(rot, Image.BICUBIC, expand=True)
    if alpha < 0.999:
        a = im.getchannel('A').point(lambda v: int(v * alpha))
        im = im.copy(); im.putalpha(a)
    x = int(cx - im.size[0] / 2); y = int(cy - im.size[1] / 2)
    comp(canvas, im, x, y)


def place_text(canvas, s, fn, size, fill, cx, cy, t=None, key=None, t0=None, mode='pop',
               track=0, amp=1.5, scale=1.0, rot=0.0):
    """animated text. mode pop/slide/fade. returns (w,h) box"""
    im = text_img(s, fn, int(size), fill, track)
    a = 1.0; sc = scale; dy = 0; r = rot
    if t0 is not None:
        p = prog(t, t0, 0.32)
        if p <= 0: return im.size
        if mode == 'pop':
            sc = scale * (0.55 + 0.45 * eback(p)); a = clamp(p * 3)
        elif mode == 'slide':
            dy = (1 - eo(p)) * 60; a = clamp(p * 2.5)
        elif mode == 'fade':
            a = p
    if key is not None:
        jx, jy, jr = jit(key, t, amp, 0.4)
        cx += jx; cy += jy; r += jr
    place(canvas, im, cx, cy + dy, sc, r, a)
    return im.size


def stroke(canvas, pts, width, color, alpha=255):
    """antialiased polyline via 3x supersampling of its bbox"""
    if len(pts) < 2: return
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    pad = width + 4
    x0, y0 = int(min(xs) - pad), int(min(ys) - pad)
    x1, y1 = int(max(xs) + pad), int(max(ys) + pad)
    S = 3
    lay = Image.new('L', ((x1 - x0) * S, (y1 - y0) * S), 0)
    d = ImageDraw.Draw(lay)
    sp = [((x - x0) * S, (y - y0) * S) for x, y in pts]
    d.line(sp, fill=alpha, width=int(width * S), joint='curve')
    rr = width * S / 2
    for px, py in (sp[0], sp[-1]):
        d.ellipse((px - rr, py - rr, px + rr, py + rr), fill=alpha)
    lay = lay.resize((x1 - x0, y1 - y0), Image.LANCZOS)
    col = Image.new('RGBA', lay.size, color + (0,)); col.putalpha(lay)
    comp(canvas, col, x0, y0)


def poly_fill(canvas, pts, color, alpha=255, S=2):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    x0, y0 = int(min(xs) - 2), int(min(ys) - 2); x1, y1 = int(max(xs) + 2), int(max(ys) + 2)
    lay = Image.new('L', ((x1 - x0) * S, (y1 - y0) * S), 0)
    ImageDraw.Draw(lay).polygon([((x - x0) * S, (y - y0) * S) for x, y in pts], fill=alpha)
    lay = lay.resize((x1 - x0, y1 - y0), Image.LANCZOS)
    col = Image.new('RGBA', lay.size, color + (0,)); col.putalpha(lay)
    comp(canvas, col, x0, y0)


def highlight(canvas, x0, y0, x1, y1, p, color=YEL, seed=1, alpha=235):
    """Vox marker-highlighter swipe, left to right"""
    p = eo(p)
    if p <= 0: return
    r = random.Random(seed)
    xe = x0 + (x1 - x0) * p
    n = 14
    top = [(x0 + (xe - x0) * i / n, y0 + r.uniform(-5, 5) - 6 * i / n) for i in range(n + 1)]
    bot = [(x0 + (xe - x0) * i / n, y1 + r.uniform(-5, 5) - 6 * i / n) for i in range(n, -1, -1)]
    cap = [(xe + 10, (y0 + y1) / 2 - 3)]
    poly_fill(canvas, [(x0 - 10, (y0 + y1) / 2)] + top + cap + bot, color, alpha)


def marker_ellipse(canvas, cx, cy, rx, ry, p, color=RED, width=9, seed=3):
    p = eio(p)
    if p <= 0: return
    r = random.Random(seed)
    a0 = r.uniform(2.2, 2.8); tot = 2 * math.pi * 1.12 * p
    ph = r.uniform(0, 6)
    pts = []
    n = max(2, int(80 * p))
    for i in range(n + 1):
        a = a0 + tot * i / n
        k = 1 + 0.05 * math.sin(3 * a + ph) + 0.04 * (i / n)
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    stroke(canvas, pts, width, color)


def marker_line(canvas, pts, p, color=RED, width=9, head=False, head_size=30):
    """draw polyline progressively (p 0..1), optional arrow head at end"""
    p = eio(p)
    if p <= 0: return
    # resample
    L = [0]
    for i in range(1, len(pts)):
        L.append(L[-1] + math.dist(pts[i - 1], pts[i]))
    tl = L[-1] * p
    out = [pts[0]]
    for i in range(1, len(pts)):
        if L[i] <= tl: out.append(pts[i])
        else:
            f = (tl - L[i - 1]) / max(1e-6, L[i] - L[i - 1])
            out.append((pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * f,
                        pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * f)); break
    stroke(canvas, out, width, color)
    if head and p > 0.9 and len(out) >= 2:
        (ax, ay), (bx, by) = out[-2], out[-1]
        ang = math.atan2(by - ay, bx - ax)
        for s in (2.6, -2.6):
            stroke(canvas, [(bx, by), (bx + head_size * math.cos(ang + s), by + head_size * math.sin(ang + s))], width, color)


def curve(p0, p1, p2, n=30):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in [i / n for i in range(n + 1)]]


def cutout(img, border=12, shadow=0.38, blur=10, off=(8, 14), bcol=(252, 249, 242)):
    """paper cut-out: white rough border + soft drop shadow"""
    pad = border + blur * 2 + 20
    w, h = img.size
    big = Image.new('RGBA', (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    big.alpha_composite(img, (pad, pad))
    a = big.getchannel('A')
    if border > 0:
        ba = a.filter(ImageFilter.GaussianBlur(border * 0.55)).point(lambda v: 255 if v > 14 else 0)
        ba = ba.filter(ImageFilter.GaussianBlur(0.8))
    else:
        ba = a
    out = Image.new('RGBA', big.size, (0, 0, 0, 0))
    if shadow > 0:
        sh = ba.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * shadow))
        shim = Image.new('RGBA', big.size, (20, 15, 10, 0)); shim.putalpha(sh)
        out.alpha_composite(shim, off)
    if border > 0:
        bim = Image.new('RGBA', big.size, bcol + (0,)); bim.putalpha(ba)
        out.alpha_composite(bim)
    out.alpha_composite(big)
    return out


def rough_mask(size, seed=0, speck=0.12):
    """grunge mask for stamps"""
    r = np.random.default_rng(seed)
    n = r.random((size[1] // 3 + 1, size[0] // 3 + 1))
    n = np.kron(n, np.ones((3, 3)))[:size[1], :size[0]]
    m = (n > speck).astype(np.uint8) * 255
    return Image.fromarray(m, 'L').filter(ImageFilter.GaussianBlur(0.7))


def stamp(text, color, size=110, rot=-9, seed=0, pad=(36, 14), fn='anton', border=9):
    tim = text_img(text, fn, size, color)
    w, h = tim.size[0] + pad[0] * 2, tim.size[1] + pad[1] * 2
    im = Image.new('RGBA', (w + 20, h + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 10, 10 + w, 10 + h), radius=18, outline=color, width=border)
    im.alpha_composite(tim, (10 + pad[0], 10 + pad[1]))
    a = ImageChops.multiply(im.getchannel('A'), rough_mask(im.size, seed))
    im.putalpha(a)
    return im.rotate(rot, Image.BICUBIC, expand=True)


def torn_rect(w, h, color, seed=0, jag=10, edges='tblr'):
    r = random.Random(seed)
    pts = []
    step = 18
    def j(e): return r.uniform(0, jag) if e in edges else 0
    for x in range(0, w + 1, step): pts.append((x, j('t')))
    for y in range(0, h + 1, step): pts.append((w - j('r'), y))
    for x in range(w, -1, -step): pts.append((x, h - j('b')))
    for y in range(h, -1, -step): pts.append((j('l'), y))
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    S = 2
    m = Image.new('L', (w * S, h * S), 0)
    ImageDraw.Draw(m).polygon([(x * S, y * S) for x, y in pts], fill=255)
    m = m.resize((w, h), Image.LANCZOS)
    c = Image.new('RGBA', (w, h), color + (255,)); c.putalpha(m)
    return c


def halftone(w, h, color, spacing=14, maxr=5.5, direction='diag', seed=0):
    im = Image.new('RGBA', (w * 2, h * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    s = spacing * 2
    for yy in range(0, h * 2 + s, s):
        for xx in range(0, w * 2 + s, s):
            ox = (s // 2) if (yy // s) % 2 else 0
            x = xx + ox
            f = clamp((x / (w * 2)) * 0.6 + (yy / (h * 2)) * 0.6) if direction == 'diag' else clamp(yy / (h * 2))
            rr = maxr * 2 * f
            if rr > 0.6: d.ellipse((x - rr, yy - rr, x + rr, yy + rr), fill=color + (255,))
    return im.resize((w, h), Image.LANCZOS)


# ---------- background textures ----------
def make_paper(base, seed=0, dark=False):
    r = np.random.default_rng(seed)
    img = np.ones((H, W, 3), np.float32) * np.array(base, np.float32)
    # low freq blotches
    lo = r.random((12, 7)).astype(np.float32)
    lo = np.array(Image.fromarray((lo * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 255 - 0.5
    img += lo[..., None] * (10 if not dark else 8)
    # mid noise
    mid = r.random((H // 4, W // 4)).astype(np.float32)
    mid = np.array(Image.fromarray((mid * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 255 - 0.5
    img += mid[..., None] * 9
    # fibers
    fib = Image.new('L', (W, H), 0); d = ImageDraw.Draw(fib)
    rr = random.Random(seed)
    for _ in range(900):
        x, y = rr.uniform(0, W), rr.uniform(0, H); a = rr.uniform(0, math.pi); l = rr.uniform(6, 30)
        d.line((x, y, x + l * math.cos(a), y + l * math.sin(a)), fill=rr.randint(20, 60), width=1)
    fib = np.array(fib.filter(ImageFilter.GaussianBlur(0.6)), np.float32) / 255
    img += (fib[..., None] * (-25 if not dark else 18))
    # vignette
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    v = ((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H / 2) / (H * 0.7)) ** 2
    img *= (1 - 0.22 * np.clip(v, 0, 1.5))[..., None]
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert('RGBA')


GRAIN = None
def grain_frames(n=6):
    global GRAIN
    if GRAIN is None:
        r = np.random.default_rng(7)
        GRAIN = [(r.normal(0, 9, (H // 2, W // 2)).astype(np.float32)) for _ in range(n)]
        GRAIN = [np.array(Image.fromarray(g).resize((W, H), Image.BILINEAR)) for g in GRAIN]
    return GRAIN
