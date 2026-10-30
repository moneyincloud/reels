"""LISTX: reusable 'listicle explainer' engine (clean line-art + host avatar + word-by-word headline).
Style: HUD progress header, word-synced headline with green accent words, numbered item title + stat pill,
'shelf' progress slots that fill per item, line-art diagrams, tilted stickers, count-ups, light/dark theme flips.
A reel module defines SCRIPT/DURS timing, SEGS (per-segment spec) and DRAW (per-item visual functions)."""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import lib as L
from lib import *

L.FONTS['pop'] = ROOT + 'fonts/Poppins-Bold.ttf'
LIGHT = (240, 240, 238); DARK_BG = (16, 17, 18)
ACC = (34, 170, 110); ACC_SOFT = (200, 236, 214); INKL = (20, 20, 22); MUTE = (140, 140, 140)
HOST_PNG = ROOT + 'host/host.png'


def timing(script, durs, lead=0.15, tail=0.25):
    starts, vo = [], []; t = 0.0
    for i, d in enumerate(durs):
        starts.append(t); vo.append(t + (0.1 if i == 0 else lead)); t = vo[-1] + d + tail
    return starts, vo, t + 1.6


def word_times(script, durs, vo):
    out = []
    for i, s in enumerate(script):
        ws = []; pos = 0
        for w in s.split(' '):
            k = s.find(w, pos); pos = k + len(w)
            ws.append((w, vo[i] + durs[i] * (k / max(1, len(s)))))
        out.append(ws)
    return out


# ---------------- host ----------------
@functools.lru_cache(8)
def host_img(h):
    im = Image.open(HOST_PNG).convert('RGBA'); w = int(im.size[0] * h / im.size[1])
    im = im.resize((w, h), Image.LANCZOS)
    # soft dotted halo like the reference (subtle drop shadow)
    pad = 24; S = Image.new('RGBA', (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh.putalpha(im.getchannel('A').point(lambda v: v * 60 // 255))
    S.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)), (pad + 8, pad + 10)); S.alpha_composite(im, (pad, pad))
    return S


@functools.lru_cache(4)
def host_card(w=300, h=330, dark=True):
    src = Image.open(HOST_PNG).convert('RGBA')
    crop = src.crop((0, 0, src.size[0], int(src.size[0] * 1.0)))
    crop = crop.resize((w - 24, w - 24), Image.LANCZOS)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 26, fill=(250, 250, 248), outline=(60, 60, 64) if dark else INKL, width=4)
    m = Image.new('L', crop.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, crop.size[0] - 1, crop.size[1] - 1), 18, fill=255)
    bg = Image.new('RGBA', crop.size, (232, 236, 233, 255)); bg.alpha_composite(crop)
    im.paste(bg, (12, 12), m)
    t = text_img('● @MONEYINCLOUD', 'type', 20, INKL, 1)
    d.rounded_rectangle((w / 2 - t.size[0] / 2 - 12, h - 44, w / 2 + t.size[0] / 2 + 12, h - 12), 14, fill=(250, 250, 248), outline=INKL, width=2)
    im.alpha_composite(t, (int(w / 2 - t.size[0] / 2), h - 42))
    return im


def draw_host(c, t, words, big=True, x=None, y=None):
    """big: full host bottom-left; else card. Pulses slightly on word onsets (talking feel)."""
    kick = 0
    for w, tw in words:
        if 0 <= t - tw < 0.18: kick = max(kick, math.exp(-(t - tw) * 18))
    bob = math.sin(t * 2.2) * 6
    if big:
        im = host_img(760); place(c, im, (x or 300), (y or 1560) + bob, 1 + 0.012 * kick, math.sin(t * 1.3) * 1.2)
    else:
        place(c, host_card(), (x or 230), (y or 1560) + bob * 0.5, 1 + 0.015 * kick, -1.5)


# ---------------- type ----------------
def headline(c, t, words, accent, x0=70, y0=215, size=66, maxw=940, col=INKL, t_hide=None, hl=ACC_SOFT):
    """word-by-word reveal; accent = set of word indexes in green with a soft highlight bar"""
    f = font('pop', size); lh = int(size * 1.12)
    x, y = x0, y0; d = ImageDraw.Draw(c)
    lay = []
    for k, (w, tw) in enumerate(words):
        ww = d.textlength(w + ' ', font=f)
        if x + ww - x0 > maxw: x = x0; y += lh
        lay.append((k, w, tw, x, y, ww)); x += ww
    for k, w, tw, xx, yy, ww in lay:
        if t < tw - 0.05: continue
        a = clamp((t - tw + 0.05) / 0.12); dy = (1 - eo(a)) * 18
        if k in accent:
            hw = d.textlength(w, font=f)
            hp = eo(clamp((t - tw) / 0.25))
            bw = int((hw + 8) * hp); bh = int(size * 0.5)
            if bw > 1: c.alpha_composite(Image.new('RGBA', (bw, bh), hl + (190,)), (int(xx - 4), int(yy + size * 0.6)))
        ti = text_img(w, 'pop', size, ACC if k in accent else col)
        if a < 1: ti = ti.copy(); ti.putalpha(ti.getchannel('A').point(lambda v: int(v * a)))
        c.alpha_composite(ti, (int(xx), int(yy + dy)))


def hud(c, t, idx, slug, done, total, dark, word='SET UP'):
    col = MUTE if not dark else (150, 150, 150)
    left = f'// {idx:02d} · {slug}'
    c.alpha_composite(text_img(left, 'type', 30, col, 2), (70, 150))
    r = text_img(word, 'type', 30, col, 2); n = text_img(f'{done}/{total}', 'type', 30, ACC, 2)
    c.alpha_composite(r, (W - 70 - n.size[0] - 20 - r.size[0], 150)); c.alpha_composite(n, (W - 70 - n.size[0], 150))


def item_title(c, t, t0, n, name, pill, icon_fn, y=600, dark=False):
    if t < t0: return
    p = eback(prog(t, t0, 0.35), 1.6)
    fg = (245, 245, 245) if dark else INKL
    d = ImageDraw.Draw(c)
    cx = 110; r = 38 * p
    d.ellipse((cx - r, y - r, cx + r, y + r), fill=(245, 245, 245) if dark else INKL)
    num = text_img(str(n), 'pop', 46, INKL if dark else (245, 245, 245));
    if p > 0.6: c.alpha_composite(num, (int(cx - num.size[0] / 2), int(y - num.size[1] / 2 - 4)))
    # icon tile
    ix = 190; d.rounded_rectangle((ix - 36, y - 36, ix + 36, y + 36), 14, fill=(250, 250, 248), outline=(80, 80, 84) if dark else INKL, width=3)
    if icon_fn: icon_fn(c, ix, y + 2, 0.3)
    nm = text_img(name, 'pop', 66, fg)
    a = clamp(p); xo = (1 - eo(clamp(p))) * 30
    nm = nm.copy(); nm.putalpha(nm.getchannel('A').point(lambda v: int(v * a)))
    c.alpha_composite(nm, (int(250 + xo), int(y - nm.size[1] / 2 - 10)))
    if pill and t > t0 + 0.25:
        pi = text_img(pill, 'type', 24, (245, 245, 245) if not dark else INKL, 1)
        pw = pi.size[0] + 36; px = 260; py = y + 58
        d.rounded_rectangle((px, py, px + pw, py + 40), 20, fill=INKL if not dark else (240, 240, 240))
        c.alpha_composite(pi, (px + 18, py + 6))


def shelf(c, t, x0, y0, slots, filled_times, icons, w=520, dark=False, label='THE CHECKLIST'):
    """slots dashed boxes on a plank; filled_times[k] = time slot k fills"""
    d = ImageDraw.Draw(c); line = (210, 210, 210) if dark else INKL
    sw = (w - 40) / slots
    for k in range(slots):
        x = x0 + 20 + k * sw + 6; bx0, bx1 = x, x + sw - 12; by0, by1 = y0 - sw + 12, y0 - 4
        ft = filled_times[k]
        if ft is not None and t > ft:
            q = eback(prog(t, ft, 0.3), 2)
            cx, cy = (bx0 + bx1) / 2, (by0 + by1) / 2; hw = (bx1 - bx0) / 2 * q; hh = (by1 - by0) / 2 * q
            d.rounded_rectangle((cx - hw, cy - hh, cx + hw, cy + hh), 10, fill=(250, 250, 248), outline=line, width=3)
            d.rectangle((cx - hw, cy - hh, cx + hw, cy - hh + 10 * q), fill=ACC)
            if q > 0.7 and icons[k]: icons[k](c, cx, cy + 4, 0.42 * min(1.0, 4 / slots))
        else:
            for s in range(0, int(bx1 - bx0), 14):
                d.line((bx0 + s, by0, bx0 + s + 7, by0), fill=line, width=2); d.line((bx0 + s, by1, bx0 + s + 7, by1), fill=line, width=2)
            for s in range(0, int(by1 - by0), 14):
                d.line((bx0, by0 + s, bx0, by0 + s + 7), fill=line, width=2); d.line((bx1, by0 + s, bx1, by0 + s + 7), fill=line, width=2)
            pl = text_img('+', 'pop', 30, line); c.alpha_composite(pl, (int((bx0 + bx1) / 2 - pl.size[0] / 2), int((by0 + by1) / 2 - 22)))
        nb = text_img(str(k + 1), 'pop', 20, (250, 250, 248));
        d.ellipse((bx0 - 8, by0 - 14, bx0 + 20, by0 + 14), fill=INKL if not dark else (90, 90, 96))
        c.alpha_composite(nb, (int(bx0 + 6 - nb.size[0] / 2), int(by0 - 14)))
    d.rounded_rectangle((x0, y0, x0 + w, y0 + 16), 6, fill=(250, 250, 248), outline=line, width=3)
    for lx in (x0 + 30, x0 + w - 30): d.rectangle((lx - 5, y0 + 16, lx + 5, y0 + 40), fill=line)
    lb = text_img(label, 'type', 20, (250, 250, 248), 2); lw = lb.size[0] + 40
    d.rectangle((x0 + w / 2 - lw / 2, y0 + 26, x0 + w / 2 + lw / 2, y0 + 56), fill=INKL)
    c.alpha_composite(lb, (int(x0 + w / 2 - lb.size[0] / 2), int(y0 + 28)))


@functools.lru_cache(64)
def sticker_img(txt, size=46, dark=False):
    t = text_img(txt, 'pop', size, INKL)
    w, h = t.size[0] + 44, t.size[1] + 22
    im = Image.new('RGBA', (w + 10, h + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((8, 8, w + 8, h + 8), 16, fill=INKL)
    d.rounded_rectangle((0, 0, w, h), 16, fill=(252, 252, 250), outline=INKL, width=5)
    im.alpha_composite(t, (22, 6))
    return im


def sticker(c, t, t0, txt, x, y, rot=-6, size=46):
    if t < t0: return
    s = 1.35 - 0.35 * eo(prog(t, t0, 0.22)); a = clamp((t - t0) / 0.08)
    place(c, sticker_img(txt, size), x, y, s, rot, a)


def counter(c, t, t0, v0, v1, fmt, x, y, size=150, col=INKL, d=1.0):
    if t < t0: return
    v = v0 + (v1 - v0) * eo(prog(t, t0, d))
    place(c, text_img(fmt(v), 'pop', size, col), x, y)


def bg(dark):
    if dark:
        im = Image.new('RGBA', (W, H), DARK_BG + (255,))
        g = Image.new('L', (W, H), 0); ImageDraw.Draw(g).ellipse((80, 900, 1000, 1700), fill=60)
        g = g.filter(ImageFilter.GaussianBlur(160)); col = Image.new('RGBA', (W, H), (40, 180, 120, 0)); col.putalpha(g); im.alpha_composite(col)
        return im
    return Image.new('RGBA', (W, H), LIGHT + (255,))


BGS = {}
def bg_cached(dark):
    if dark not in BGS: BGS[dark] = bg(dark)
    return BGS[dark].copy()


def flash(c, t, times, d=0.12):
    for tb in times:
        if 0 <= t - tb < d:
            a = 1 - (t - tb) / d
            ov = Image.new('RGBA', c.size, (255, 255, 255, int(255 * a))); c.alpha_composite(ov)


# ---------------- line-art helpers ----------------
def lw(s): return max(2, int(6 * s))


def ico_jar(c, cx, cy, s, fill=1.0, t=0):
    d = ImageDraw.Draw(c); w, h = 160 * s, 200 * s
    d.rounded_rectangle((cx - w / 2, cy - h / 2 + 30 * s, cx + w / 2, cy + h / 2), 22 * s, fill=(252, 252, 250), outline=INKL, width=lw(s))
    d.rectangle((cx - w / 2 + 14 * s, cy - h / 2, cx + w / 2 - 14 * s, cy - h / 2 + 30 * s), fill=INKL)
    if fill > 0:
        fh = (h - 50 * s) * fill
        d.rounded_rectangle((cx - w / 2 + 12 * s, cy + h / 2 - 12 * s - fh, cx + w / 2 - 12 * s, cy + h / 2 - 12 * s), 12 * s, fill=ACC)
        for k in range(int(fill * 6)):
            yy = cy + h / 2 - 30 * s - k * 22 * s
            d.ellipse((cx - 30 * s + (k % 2) * 20 * s, yy - 9 * s, cx + 10 * s + (k % 2) * 20 * s, yy + 9 * s), fill=(250, 210, 80), outline=INKL, width=max(1, int(3 * s)))


def ico_umbrella(c, cx, cy, s, t=0):
    d = ImageDraw.Draw(c); r = 110 * s
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 180, 360, fill=(252, 252, 250), outline=INKL, width=lw(s))
    for k in (-1, 0, 1): d.arc((cx + k * r * 0.66 - r * 0.34, cy - r * 0.2, cx + k * r * 0.66 + r * 0.34, cy + r * 0.2), 180, 360, fill=INKL, width=lw(s))
    d.line((cx, cy, cx, cy + r * 0.95), fill=INKL, width=lw(s)); d.arc((cx, cy + r * 0.8, cx + 30 * s, cy + r * 1.1), 0, 180, fill=INKL, width=lw(s))
    d.rectangle((cx - r * 0.98, cy - 8 * s, cx + r * 0.98, cy), fill=ACC)


def ico_heart(c, cx, cy, s, t=0):
    d = ImageDraw.Draw(c); r = 50 * s
    d.ellipse((cx - 2 * r, cy - r * 1.4, cx, cy + r * 0.6), fill=(252, 252, 250), outline=INKL, width=lw(s))
    d.ellipse((cx, cy - r * 1.4, cx + 2 * r, cy + r * 0.6), fill=(252, 252, 250), outline=INKL, width=lw(s))
    d.polygon([(cx - 2 * r + 4 * s, cy - r * 0.2), (cx + 2 * r - 4 * s, cy - r * 0.2), (cx, cy + r * 1.9)], fill=(252, 252, 250))
    d.line([(cx - 2 * r + 3 * s, cy - r * 0.15), (cx, cy + r * 1.9), (cx + 2 * r - 3 * s, cy - r * 0.15)], fill=INKL, width=lw(s))
    pts = [(cx - 1.6 * r, cy), (cx - 0.6 * r, cy), (cx - 0.3 * r, cy - 0.7 * r), (cx + 0.1 * r, cy + 0.6 * r), (cx + 0.4 * r, cy), (cx + 1.6 * r, cy)]
    d.line(pts, fill=ACC, width=lw(s))


def ico_plant(c, cx, cy, s, t=0):
    d = ImageDraw.Draw(c); w = 120 * s
    d.polygon([(cx - w / 2, cy + 20 * s), (cx + w / 2, cy + 20 * s), (cx + w * 0.38, cy + 110 * s), (cx - w * 0.38, cy + 110 * s)], fill=(252, 252, 250), outline=INKL)
    d.line([(cx - w / 2, cy + 20 * s), (cx + w / 2, cy + 20 * s), (cx + w * 0.38, cy + 110 * s), (cx - w * 0.38, cy + 110 * s), (cx - w / 2, cy + 20 * s)], fill=INKL, width=lw(s))
    d.line((cx, cy + 20 * s, cx, cy - 80 * s), fill=INKL, width=lw(s))
    for k, (dx, dy) in enumerate(((-50, -20), (50, -50), (-40, -80))):
        x1, y1 = cx + dx * s, cy + dy * s
        d.ellipse((min(cx, x1) - 6 * s, y1 - 18 * s, max(cx, x1) + 6 * s, y1 + 18 * s), fill=ACC, outline=INKL, width=max(1, int(4 * s)))


def ico_phone(c, cx, cy, s, t=0):
    d = ImageDraw.Draw(c); w, h = 110 * s, 190 * s
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), 18 * s, fill=(252, 252, 250), outline=INKL, width=lw(s))
    d.rounded_rectangle((cx - w / 2 + 12 * s, cy - h / 2 + 22 * s, cx + w / 2 - 12 * s, cy + h / 2 - 30 * s), 6 * s, fill=(232, 240, 235))
    d.line((cx - 20 * s, cy - h / 2 + 11 * s, cx + 20 * s, cy - h / 2 + 11 * s), fill=INKL, width=max(2, int(4 * s)))
    pts = [(cx - 32 * s, cy + 30 * s), (cx - 10 * s, cy + 5 * s), (cx + 8 * s, cy + 15 * s), (cx + 32 * s, cy - 30 * s)]
    d.line(pts, fill=ACC, width=lw(s))
    d.ellipse((cx - 10 * s, cy + h / 2 - 22 * s, cx + 10 * s, cy + h / 2 - 8 * s), outline=INKL, width=max(1, int(3 * s)))


def ico_swap(c, cx, cy, s, t=0):
    d = ImageDraw.Draw(c); r = 46 * s
    for dx, sym, col in ((-50, 'R', (252, 252, 250)), (50, '$', ACC)):
        x = cx + dx * s
        d.ellipse((x - r, cy - r, x + r, cy + r), fill=col, outline=INKL, width=lw(s))
        f = font('pop', int(60 * s)); txt = '₹' if sym == 'R' else '$'
        d.text((x, cy + 2 * s), txt, font=f, fill=INKL, anchor='mm')
    d.line((cx - 20 * s, cy - r - 14 * s, cx + 20 * s, cy - r - 14 * s), fill=INKL, width=lw(s))
    d.polygon([(cx + 22 * s, cy - r - 24 * s), (cx + 36 * s, cy - r - 14 * s), (cx + 22 * s, cy - r - 4 * s)], fill=INKL)


def ico_taxdoc(c, cx, cy, s, t=0):
    d = ImageDraw.Draw(c); w, h = 130 * s, 170 * s
    d.polygon([(cx - w / 2, cy - h / 2), (cx + w / 2 - 30 * s, cy - h / 2), (cx + w / 2, cy - h / 2 + 30 * s), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)], fill=(252, 252, 250))
    d.line([(cx - w / 2, cy - h / 2), (cx + w / 2 - 30 * s, cy - h / 2), (cx + w / 2, cy - h / 2 + 30 * s), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2), (cx - w / 2, cy - h / 2)], fill=INKL, width=lw(s))
    for k in range(3): d.line((cx - w / 2 + 18 * s, cy - 30 * s + k * 26 * s, cx + w / 2 - 22 * s, cy - 30 * s + k * 26 * s), fill=(170, 170, 170), width=max(2, int(5 * s)))
    d.text((cx, cy + 58 * s), '%', font=font('pop', int(44 * s)), fill=ACC, anchor='mm')


def ico_scale(c, cx, cy, s, t=0):
    d = ImageDraw.Draw(c); W2 = 90 * s
    d.line((cx, cy - 70 * s, cx, cy + 70 * s), fill=INKL, width=lw(s)); d.line((cx - 40 * s, cy + 70 * s, cx + 40 * s, cy + 70 * s), fill=INKL, width=lw(s))
    d.line((cx - W2, cy - 50 * s, cx + W2, cy - 50 * s), fill=INKL, width=lw(s))
    for dx, col in ((-W2, ACC), (W2, (230, 90, 80))):
        x = cx + dx; d.line((x, cy - 50 * s, x - 30 * s, cy + 10 * s), fill=INKL, width=max(2, int(3 * s))); d.line((x, cy - 50 * s, x + 30 * s, cy + 10 * s), fill=INKL, width=max(2, int(3 * s)))
        d.chord((x - 36 * s, cy - 10 * s, x + 36 * s, cy + 34 * s), 0, 180, fill=col, outline=INKL, width=lw(s))


def ico_grid10(c, cx, cy, s, t=0):
    d = ImageDraw.Draw(c); cs = 34 * s
    for k in range(10):
        r, q = divmod(k, 5); x = cx - 2.5 * cs + q * cs; y = cy - cs + r * cs
        d.rounded_rectangle((x + 3 * s, y + 3 * s, x + cs - 3 * s, y + cs - 3 * s), 6 * s, fill=ACC if (k % 3 == 0) else (252, 252, 250), outline=INKL, width=max(2, int(4 * s)))
