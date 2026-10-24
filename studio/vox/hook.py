"""Hook-style thumbnail template (sunburst rays + bold Anton title + yellow band + central art + badge)."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from lib import *

THEMES = {  # base, ray (lighter), glow
    'maroon': ((80, 14, 30), (140, 28, 50), (230, 140, 70)),
    'night': ((28, 28, 36), (52, 52, 64), (230, 190, 80)),
    'chai': ((62, 34, 18), (120, 70, 36), (230, 160, 80)),
    'blue': ((30, 110, 200), (70, 160, 240), (200, 235, 255)),
    'navy': ((16, 38, 100), (34, 70, 150), (160, 180, 230)),
    'teal': ((12, 90, 84), (30, 140, 125), (120, 220, 200)),
    'purple': ((60, 30, 120), (100, 55, 175), (190, 150, 240)),
    'green': ((14, 70, 46), (30, 110, 72), (90, 200, 140)),
    'yellow': ((214, 170, 30), (245, 205, 60), (255, 240, 170)),
}
SHADOW = (20, 20, 20)


def rays_bg(theme, n=26, cx=540, cy=1000):
    base, ray, glow = THEMES[theme]
    S = 2; im = Image.new('RGB', (W * S, H * S), base); d = ImageDraw.Draw(im)
    R = 3000 * S
    for k in range(n):
        if k % 2: continue
        a0 = 2 * math.pi * k / n; a1 = 2 * math.pi * (k + 1) / n
        d.polygon([(cx * S, cy * S), (cx * S + R * math.cos(a0), cy * S + R * math.sin(a0)), (cx * S + R * math.cos(a1), cy * S + R * math.sin(a1))], fill=ray)
    im = im.resize((W, H), Image.LANCZOS).convert('RGBA')
    # center glow
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).ellipse((cx - 330, cy - 330, cx + 330, cy + 330), fill=170)
    m = m.filter(ImageFilter.GaussianBlur(150))
    g = Image.new('RGBA', (W, H), glow + (0,)); g.putalpha(m); im.alpha_composite(g)
    # vignette
    yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2)
    v = (np.clip((r - 0.35) * 1.6, 0, 1) * 150).astype(np.uint8)
    vi = Image.new('RGBA', (W, H), (0, 0, 0, 255)); vi.putalpha(Image.fromarray(v)); im.alpha_composite(vi)
    return im


def shadow_text(s, size, fill, fn='anton', off=10):
    t = text_img(s, fn, size, fill); sh = text_img(s, fn, size, SHADOW)
    im = Image.new('RGBA', (t.size[0] + off, t.size[1] + off), (0, 0, 0, 0))
    im.alpha_composite(sh, (off, off)); im.alpha_composite(t, (0, 0))
    return im


def fit_text(s, size, fill, maxw=980, fn='anton', off=10):
    while text_w(s, fn, size) > maxw and size > 40: size -= 4
    return shadow_text(s, size, fill, fn, off)


def band(s, size=130, txt=INK, bg=YEL, maxw=900, rot=-1):
    while text_w(s, 'anton', size) > maxw and size > 40: size -= 4
    t = text_img(s, 'anton', size, txt)
    pw, ph = t.size[0] + 70, int(t.size[1] * 1.02)
    im = Image.new('RGBA', (pw, ph), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(0, 8), (pw - 4, 0), (pw, ph - 6), (6, ph)], fill=bg)
    im.alpha_composite(t, (35, int(ph * 0.0) - int(size * 0.06)))
    return im.rotate(rot, expand=True, resample=Image.BICUBIC)


def pill(s, bg, fg=INK, size=84, maxw=760):
    while text_w(s, 'anton', size) > maxw and size > 30: size -= 4
    t = text_img(s, 'anton', size, fg)
    w, h = t.size[0] + 90, t.size[1] + 40
    im = Image.new('RGBA', (w + 16, h + 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((12, 14, w + 12, h + 14), radius=h // 2, fill=SHADOW)
    d.rounded_rectangle((0, 0, w, h), radius=h // 2, fill=bg, outline=SHADOW, width=7)
    im.alpha_composite(t, (45, 14))
    return im


def tag(s, bg=RED, fg=CREAM, size=110, rot=-6, sub=None):
    t = text_img(s, 'anton', size, fg)
    st = text_img(sub, 'anton', int(size * 0.45), fg) if sub else None
    w = max(t.size[0], st.size[0] if st else 0) + 100; h = t.size[1] + (st.size[1] + 10 if st else 0) + 60
    im = Image.new('RGBA', (w + 30, h + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((16, 20, w + 16, h + 20), radius=26, fill=(0, 0, 0, 110))
    d.rounded_rectangle((0, 0, w, h), radius=26, fill=CREAM)
    d.rounded_rectangle((12, 12, w - 12, h - 12), radius=20, fill=bg)
    y = 30
    if st: im.alpha_composite(st, ((w - st.size[0]) // 2, y)); y += st.size[1] + 10
    im.alpha_composite(t, ((w - t.size[0]) // 2, y - 8))
    return im.rotate(rot, expand=True, resample=Image.BICUBIC)


def art_glow(c, art, cx, cy, scale=1.0, rot=0):
    sh = Image.new('RGBA', art.size, (0, 0, 0, 0)); sh.putalpha(art.getchannel('A').point(lambda v: int(v * 0.45)))
    place(c, sh, cx + 14, cy + 18, scale, rot)
    place(c, art, cx, cy, scale, rot)


def finish(c, path):
    arr = np.asarray(c.convert('RGB')).astype(np.float32) + grain_frames()[0][..., None] * 0.7
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(path, quality=93)
