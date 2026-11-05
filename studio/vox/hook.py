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
    'cream': ((246, 240, 228), (255, 252, 244), (255, 214, 150)),
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


# ---- one colour per reel, picked from the stock/topic (added 5 Nov 2026) ----
THEMES.update({
    'red': ((150, 18, 30), (205, 40, 50), (255, 170, 120)),
    'orange': ((200, 80, 10), (240, 130, 30), (255, 220, 150)),
    'gold': ((150, 105, 10), (205, 160, 40), (255, 235, 160)),
    'pink': ((170, 30, 100), (225, 70, 145), (255, 190, 220)),
    'oil': ((18, 18, 22), (44, 40, 36), (240, 150, 40)),
    'sky': ((20, 130, 210), (80, 180, 245), (220, 245, 255)),
    'emerald': ((6, 110, 70), (20, 160, 100), (150, 240, 190)),
})
# topic keyword -> colour (first match wins): the stock/sector first, then the mood (crash = red, rally = green).
TOPIC_COLOURS = [
    (('oil', 'crude', 'ongc', 'petrol', 'brent'), 'oil'),
    (('gold', 'jewel', 'silver', 'diwali', 'muhurat'), 'gold'),
    (('pharma', 'health', 'hospital', 'drug', 'laurus', 'syncom'), 'teal'),
    (('it', 'tech', 'ai', 'software', 'infosys', 'tcs', 'wipro'), 'navy'),
    (('bank', 'nbfc', 'loan', 'credit', 'hdfc', 'sbi'), 'blue'),
    (('power', 'solar', 'wind', 'energy', 'suzlon', 'sjvn', 'ntpc', 'green'), 'emerald'),
    (('milk', 'dairy', 'food', 'fmcg', 'tea', 'chai'), 'sky'),
    (('ipo', 'listing', 'jio', 'telecom', 'recharge'), 'purple'),
    (('auto', 'car', 'truck', 'tvs', 'maruti', 'tata motors'), 'orange'),
    (('crash', 'fall', 'fell', 'loss', 'low', 'trap', 'scam', 'sebi', 'fraud', 'down'), 'red'),
    (('jump', 'rally', 'surge', 'multibagger', 'record', 'gain'), 'green'),
    (('women', 'beauty', 'fashion', 'wedding'), 'pink'),
]
SOLID = ['red', 'orange', 'gold', 'green', 'emerald', 'teal', 'sky', 'blue', 'navy', 'purple', 'pink', 'maroon']


def theme_for(topic, recent=()):
    """One colour for this reel: matched from the stock/topic, else a colour not used in the last few reels."""
    import random as _r
    import re as _re
    t = topic.lower()
    for keys, col in TOPIC_COLOURS:
        if any(_re.search(r'\b' + _re.escape(k.strip()), t) for k in keys): return col
    pool = [c for c in SOLID if c not in recent] or SOLID
    return _r.choice(pool)


THEME_ACCENT = {  # bright accent of each colour, for the video (headers, bars, chips) to match the thumbnail
    k: v[1] for k, v in THEMES.items()}


def follow_sticker(line='FOLLOW FOR DAILY MONEY TRUTHS', handle='@moneyincloud', size=64, rot=-3):
    """Audience-gain sticker: red '+ FOLLOW' button plus a promise line."""
    btn = text_img('+ FOLLOW', 'anton', size, (255, 255, 255))
    ln = text_img(line, 'anton', int(size * 0.62), INK)
    hd = text_img(handle, 'anton', int(size * 0.5), (90, 90, 90)) if handle else None
    bw, bh = btn.size[0] + 60, btn.size[1] + 24
    w = max(bw, ln.size[0], hd.size[0] if hd else 0) + 70
    h = bh + ln.size[1] + (hd.size[1] + 6 if hd else 0) + 70
    im = Image.new('RGBA', (w + 24, h + 24), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((14, 18, w + 14, h + 18), 30, fill=(0, 0, 0, 100))
    d.rounded_rectangle((0, 0, w, h), 30, fill=(255, 255, 255))
    bx = (w - bw) // 2; d.rounded_rectangle((bx, 24, bx + bw, 24 + bh), 22, fill=(237, 50, 80))
    im.alpha_composite(btn, (bx + 30, 24 + 4))
    y = 24 + bh + 14; im.alpha_composite(ln, ((w - ln.size[0]) // 2, y))
    if hd: im.alpha_composite(hd, ((w - hd.size[0]) // 2, y + ln.size[1] + 6))
    return im.rotate(rot, expand=True, resample=Image.BICUBIC)


def follow_pill(line='for daily money truths', handle='@moneyincloud', size=46):
    """Compact one-line FOLLOW pill for in-video use (sits over the header strip)."""
    btn = text_img('+ FOLLOW', 'anton', size, (255, 255, 255))
    txt = text_img(line, 'anton', int(size * 0.8), INK)
    hd = text_img(handle, 'anton', int(size * 0.55), (110, 110, 110)) if handle else None
    bw, bh = btn.size[0] + 44, btn.size[1] + 16
    tw = max(txt.size[0], hd.size[0] if hd else 0)
    w, h = bw + tw + 70, bh + 28
    im = Image.new('RGBA', (w + 16, h + 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((8, 12, w + 8, h + 12), h // 2, fill=(0, 0, 0, 90))
    d.rounded_rectangle((0, 0, w, h), h // 2, fill=(255, 255, 255))
    d.rounded_rectangle((14, 14, 14 + bw, 14 + bh), bh // 2, fill=(237, 50, 80))
    im.alpha_composite(btn, (14 + 22, 14 + 2))
    if hd:
        y = (h - txt.size[1] - hd.size[1]) // 2
        im.alpha_composite(txt, (bw + 40, y)); im.alpha_composite(hd, (bw + 40, y + txt.size[1]))
    else:
        im.alpha_composite(txt, (bw + 40, (h - txt.size[1]) // 2))
    return im


def title_ink(theme):
    """Title colour that reads on this theme: dark ink on light colours, cream on dark ones."""
    r, g, b = THEMES[theme][0]
    return INK if (0.299 * r + 0.587 * g + 0.114 * b) > 150 else (255, 250, 240)
