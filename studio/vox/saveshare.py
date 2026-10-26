"""Save/share animation helpers for @moneyincloud reels (paper Vox style).

Use inside scene functions. Every helper is time-based: pass the current time t and a start time t0
(usually from at(i, 'phrase', -0.3)).

  bookmark_icon(size)                 -> RGBA bookmark (save) icon
  plane_icon(size)                    -> RGBA paper-plane (share) icon
  save_pulse(c, t, t0, x, y)          -> bouncing bookmark + "SAVE THIS"
  send_frame(c, t, t0, who, y)        -> "Send this to <who>" card with a flying paper plane
  cheat_sheet(c, t, t0, title, rows)  -> one-screen summary card (screenshot-able), rows = [(left, right, colour)]
  checklist(c, t, items, y0)          -> items = [(text, tick_time)], boxes tick themselves
  myth_fact(c, t, t0, myth, fact)     -> paper-tear split screen, MYTH stamped X, FACT stamped tick
  countdown_ring(c, t, t0, secs, x, y)-> quiz countdown ring 3-2-1
  roll_number(t, t0, dur, v0, v1)     -> eased number for counters / calculators
  coin_stack(c, t, t0, n, x, y)       -> growing coin stack (calculator reels; past/illustrative maths only)
  tear_reveal(c, t, t0, img, x, y)    -> paper curtain tears open to reveal img
Sound cues (in <slug>_audio.py): pop on save_pulse, whoosh on send_frame plane, ding per checklist tick,
paper rip (whoosh + hit) on myth_fact / tear_reveal, beep per countdown second.
"""
import math, functools, random
from PIL import Image, ImageDraw
from lib import *
from scenes import stamp_c

SOFT = (253, 251, 246); NAVY = (30, 60, 120); GREY = (120, 116, 108); BLUE = (40, 100, 200)


def _card(w, h, fill=SOFT, r=22, sh=10):
    im = Image.new('RGBA', (w + sh, h + sh), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((sh, sh, w + sh - 1, h + sh - 1), r, fill=INK)
    d.rounded_rectangle((0, 0, w - 1, h - 1), r, fill=fill, outline=INK, width=6)
    return im


@functools.lru_cache(maxsize=None)
def bookmark_icon(size=120, col=YEL):
    s = size; im = Image.new('RGBA', (s, int(s * 1.25)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pts = [(s * .12, s * .06), (s * .88, s * .06), (s * .88, s * 1.18), (s * .5, s * .86), (s * .12, s * 1.18)]
    d.polygon(pts, fill=col); d.line(pts + [pts[0]], fill=INK, width=max(4, s // 18))
    return im


@functools.lru_cache(maxsize=None)
def plane_icon(size=120, col=CREAM):
    s = size; im = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    a = [(s * .05, s * .45), (s * .95, s * .08), (s * .55, s * .92), (s * .42, s * .58)]
    d.polygon(a, fill=col); d.line(a + [a[0]], fill=INK, width=max(4, s // 18))
    d.line([(s * .42, s * .58), (s * .95, s * .08)], fill=INK, width=max(3, s // 24))
    return im


def save_pulse(c, t, t0, x=540, y=1500, text='SAVE THIS'):
    if t < t0: return
    p = eback(prog(t, t0, 0.4), 1.8); bob = math.sin((t - t0) * 7) * 8 * math.exp(-(t - t0) * 0.8)
    place(c, bookmark_icon(110), x - 170, y + bob, p, -8)
    place(c, text_img(text, 'anton', 84, INK), x + 60, y, p)


def send_frame(c, t, t0, who='the friend who buys every dip', y=1350):
    if t < t0: return
    p = eback(prog(t, t0, 0.4), 1.3)
    place(c, _card(900, 250, YEL), 540, y, p, -1.5)
    if p > 0.6:
        place(c, text_img('SEND THIS TO', 'anton', 64, INK), 540, y - 55)
        place(c, text_img(who, 'mark', 54, NAVY), 540, y + 35, 1, -1)
    q = prog(t, t0 + 0.3, 1.1)
    if 0 < q < 1:
        x = 80 + 920 * eio(q); yy = y - 200 - 160 * math.sin(math.pi * q)
        place(c, plane_icon(110), x, yy, 1, 15 - 30 * q)


def cheat_sheet(c, t, t0, title, rows, y0=560, dark=False):
    """Freeze-frame summary. rows: [(left_text, right_text, colour)], up to 6."""
    if t < t0: return
    p = eback(prog(t, t0, 0.45), 1.2)
    h = 150 + 110 * len(rows)
    place(c, _card(940, h), 540, y0 + h / 2, p, -0.5)
    if p < 0.6: return
    place(c, text_img(title, 'anton', 64, INK), 540, y0 + 70)
    d = ImageDraw.Draw(c); d.line((110, y0 + 125, 970, y0 + 125), fill=INK, width=4)
    for k, (l, r, col) in enumerate(rows):
        tk = t0 + 0.35 + 0.12 * k
        if t < tk: continue
        a = clamp((t - tk) / 0.2); yy = y0 + 185 + 110 * k
        c.alpha_composite(text_img(l, 'anton', 56, INK), (130, int(yy - 34)))
        rt = text_img(r, 'anton', 56, col); c.alpha_composite(rt, (950 - rt.size[0], int(yy - 34)))
        if k < len(rows) - 1: d.line((130, yy + 50, 950, yy + 50), fill=(220, 214, 200), width=2)
    save_pulse(c, t, t0 + 0.6 + 0.12 * len(rows), 540, y0 + h + 110, 'SAVE THIS')


def checklist(c, t, items, y0=520, gap=170):
    for k, (txt, tk) in enumerate(items):
        if t < tk - 0.4: continue
        p = eback(prog(t, tk - 0.4, 0.4), 1.3); y = y0 + k * gap
        place(c, _card(880, 130), 540, y, p, (-1, 1, -0.5, 0.8, -0.8)[k % 5])
        if p > 0.6:
            place(c, text_img(txt, 'anton', 56, INK), 500, y)
            d = ImageDraw.Draw(c); d.rounded_rectangle((850, y - 32, 914, y + 32), 10, outline=INK, width=6)
            if t > tk:
                q = clamp((t - tk) / 0.25)
                pts = [(862, y), (878, y + 20), (906, y - 24)]
                if q < 0.5: d.line([pts[0], (pts[0][0] + (pts[1][0] - pts[0][0]) * q * 2, pts[0][1] + (pts[1][1] - pts[0][1]) * q * 2)], fill=GRN, width=10)
                else: d.line([pts[0], pts[1], (pts[1][0] + (pts[2][0] - pts[1][0]) * (q - .5) * 2, pts[1][1] + (pts[2][1] - pts[1][1]) * (q - .5) * 2)], fill=GRN, width=10)


def myth_fact(c, t, t0, myth, fact, y=900, y0=300, y1=1560):
    if t < t0: return
    q = eio(prog(t, t0, 0.5)); gapx = 14 * q
    r = random.Random(42); tear = [(540 + r.uniform(-18, 18), yy) for yy in range(y0, y1, 45)] + [(540, y1)]
    left = Image.new('RGBA', c.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(left)
    dl.polygon([(60, y0)] + [(x - gapx, yy) for x, yy in tear] + [(60, y1)], fill=(255, 226, 222))
    right = Image.new('RGBA', c.size, (0, 0, 0, 0)); dr = ImageDraw.Draw(right)
    dr.polygon([(1020, y0)] + [(x + gapx, yy) for x, yy in tear] + [(1020, y1)], fill=(222, 245, 228))
    c.alpha_composite(left); c.alpha_composite(right)
    d = ImageDraw.Draw(c); d.line([(x - gapx, yy) for x, yy in tear], fill=INK, width=4); d.line([(x + gapx, yy) for x, yy in tear], fill=INK, width=4)
    place(c, text_img('MYTH', 'anton', 100, RED), 300, y0 + 100, q); place(c, text_img('FACT', 'anton', 100, GRN), 780, y0 + 100, q)
    ym = y0 + int((y1 - y0) * 0.68)
    for k, ln in enumerate(myth): place(c, text_img(ln, 'osw', 46, INK), 300, y0 + 280 + k * 70, q)
    tf = t0 + 1.0
    if t > tf:
        for k, ln in enumerate(fact): place(c, text_img(ln, 'osw', 46, INK), 780, y0 + 280 + k * 70, eo(prog(t, tf, 0.3)))
    tx = t0 + 0.6
    if t > tx:
        s_, a = (1.0 + 0.6 * (1 - eo(prog(t, tx, 0.25))), 1)
        d2 = ImageDraw.Draw(c); k = 70 * s_
        d2.line((300 - k, ym - k, 300 + k, ym + k), fill=RED, width=22); d2.line((300 + k, ym - k, 300 - k, ym + k), fill=RED, width=22)
    if t > tf + 0.4:
        k = 70 * (1.0 + 0.6 * (1 - eo(prog(t, tf + 0.4, 0.25))))
        ImageDraw.Draw(c).line((780 - k, ym, 780 - k * 0.3, ym + k * 0.7, 780 + k, ym - k * 0.8), fill=GRN, width=24)


def countdown_ring(c, t, t0, secs=3, x=540, y=1350, r=110):
    if t < t0 or t > t0 + secs + 0.3: return
    e = t - t0; left = max(0, secs - int(e))
    d = ImageDraw.Draw(c)
    d.ellipse((x - r, y - r, x + r, y + r), fill=SOFT, outline=INK, width=8)
    frac = clamp(e / secs); d.arc((x - r + 14, y - r + 14, x + r - 14, y + r - 14), -90, -90 + 360 * (1 - frac), fill=RED, width=22)
    place(c, text_img(str(left) if left else '!', 'anton', 120, INK), x, y)


def roll_number(t, t0, dur, v0, v1):
    return v0 + (v1 - v0) * eo(prog(t, t0, dur))


def coin_stack(c, t, t0, n=12, x=540, y=1400, w=170):
    if t < t0: return
    d = ImageDraw.Draw(c); k = int(clamp((t - t0) / 1.6) * n + 0.999)
    for j in range(k):
        yy = y - j * 30
        d.ellipse((x - w / 2, yy - 22, x + w / 2, yy + 22), fill=(214, 160, 40), outline=INK, width=5)


def tear_reveal(c, t, t0, img, x=540, y=900):
    if t < t0: return
    q = eio(prog(t, t0, 0.6))
    place(c, img, x, y, 0.8 + 0.2 * eback(q, 1.4))
    if q < 1:
        r = random.Random(7); h = img.size[1] + 80; w = img.size[0] + 80
        top = y - h / 2; edge = [(x + r.uniform(-16, 16), top + k * h / 20) for k in range(21)]
        L = Image.new('RGBA', c.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
        dl.polygon([(x - w / 2 - w / 2 * q, top), *[(ex - w / 2 * q, ey) for ex, ey in edge], (x - w / 2 - w / 2 * q, top + h)], fill=PAPER)
        dl.polygon([(x + w / 2 + w / 2 * q, top), *[(ex + w / 2 * q, ey) for ex, ey in edge], (x + w / 2 + w / 2 * q, top + h)], fill=PAPER)
        c.alpha_composite(L)
