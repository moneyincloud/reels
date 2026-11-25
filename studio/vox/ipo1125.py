"""IPO listing report 25 Nov 2026: Mahanadi Coalfields, Crystal Crop, EAAA. PCJ paper collage (male VO)"""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs, typed, drop, warn_icon, receipt
from fridge import follow_btn
import saveshare as SS
import defence as DF

SH = ROOT + _os.environ.get('LDIR', 'ipo1125') + '/'
SCRIPT = json.load(open(SH + 'script.json'))
DURS = json.load(open(SH + 'vo/durs.json'))
LEAD, TAIL = 0.15, 0.3
STARTS, VO = [], []
_t = 0.0
for i, d in enumerate(DURS):
    STARTS.append(_t); VO.append(_t + (0.1 if i == 0 else LEAD)); _t = VO[-1] + d + TAIL
DUR = _t + 1.8
B = STARTS[1:]
NAVY = (30, 60, 120); BLUE = (40, 100, 200); GREY = (120, 112, 104); TEAL = (20, 140, 130); ORG = (230, 120, 30); GOLD = (214, 160, 40)
SOFT = (252, 250, 244)


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def src(c, t, txt, t0, y=1720, col=GREY):
    if t > t0: place_text(c, txt, 'type', 24, col, 540, y, t, None, t0, 'fade', track=1)


# ---------------- assets ----------------
@functools.lru_cache(16)
def clipping(hp, head='IRFC', top='THE MARKET PAGE', sub='RAILWAY FINANCE · NSE: IRFC'):
    w, h = 880, 360
    im = torn_rect(w, h, (234, 228, 212), seed=7, jag=12)
    d = ImageDraw.Draw(im)
    mt = text_img(top, 'pf', 30, INK, 3); im.alpha_composite(mt, (w // 2 - mt.size[0] // 2, 14))
    d.line((40, 66, w - 40, 66), fill=INK, width=3); d.line((40, 72, w - 40, 72), fill=INK, width=1)
    st = text_img(sub, 'type', 22, (90, 85, 80), 2); im.alpha_composite(st, (w // 2 - st.size[0] // 2, 78))
    hl = text_img(head, 'pf', 104 if len(head) < 14 else 84, INK)
    hx, hy = w // 2 - hl.size[0] // 2, 112
    if hp > 0: highlight(im, hx + 14, hy + 46, hx + hl.size[0] - 14, hy + hl.size[1] - 6, hp, seed=11, alpha=225)
    im.alpha_composite(hl, (hx, hy))
    r = random.Random(4)
    for col in range(3):
        x0 = 44 + col * 270
        for k in range(4):
            y = 272 + k * 18; ln = r.uniform(170, 240) if k < 3 else r.uniform(80, 150)
            d.line((x0, y, x0 + ln, y), fill=(160, 152, 140), width=7)
    return cutout(im, border=0, shadow=0.36, blur=10, off=(8, 14))


@functools.lru_cache(None)
def qtag(txt, col):
    t = text_img(txt, 'anton', 84, CREAM)
    w, h = t.size[0] + 60, t.size[1] + 16
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), radius=20, fill=col)
    im.alpha_composite(t, (30, 8))
    return cutout(im, border=10, shadow=0.5)


@functools.lru_cache(None)
def ticket(state, line2):
    w, h = 820, 170
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 18, fill=(254, 252, 246))
    for y in range(10, h - 10, 18): d.ellipse((150 - 5, y, 150 + 5, y + 10), fill=(225, 218, 204))
    ic = text_img('STEP', 'type', 22, GREY, 2); im.alpha_composite(ic, (75 - ic.size[0] // 2, 30))
    d.rectangle((40, 90, 110, 140), fill=INK); d.polygon([(40, 90), (63, 70), (63, 90), (86, 70), (86, 90), (110, 70), (110, 90)], fill=INK)
    d.rectangle((92, 50, 104, 80), fill=INK)
    a = text_img(state, 'anton', 70, INK); im.alpha_composite(a, (185, 20))
    b = text_img(line2, 'type', 26, GREY, 1); im.alpha_composite(b, (190, 112))
    return cutout(im, border=10, shadow=0.4)


def turbine(c, cx, cy, s, t, col=INK, rpm=1.6):
    d = ImageDraw.Draw(c)
    d.polygon([(cx - 10 * s, cy + 300 * s), (cx + 10 * s, cy + 300 * s), (cx + 4 * s, cy), (cx - 4 * s, cy)], fill=col)
    a0 = t * rpm * 2 * math.pi
    for k in range(3):
        a = a0 + k * 2 * math.pi / 3
        tip = (cx + math.cos(a) * 170 * s, cy + math.sin(a) * 170 * s)
        side = (cx + math.cos(a + 0.12) * 60 * s, cy + math.sin(a + 0.12) * 60 * s)
        side2 = (cx + math.cos(a - 0.05) * 50 * s, cy + math.sin(a - 0.05) * 50 * s)
        d.polygon([(cx, cy), side, tip, side2], fill=col)
    d.ellipse((cx - 14 * s, cy - 14 * s, cx + 14 * s, cy + 14 * s), fill=RED, outline=col, width=max(2, int(4 * s)))


# grid sheet chart
def grid_sheet(w, h):
    im = Image.new('RGBA', (w, h), (252, 250, 244, 255)); d = ImageDraw.Draw(im)
    for x in range(0, w, 30): d.line((x, 0, x, h), fill=(205, 218, 228), width=1)
    for y in range(0, h, 30): d.line((0, y, w, y), fill=(205, 218, 228), width=1)
    return im


@functools.lru_cache(4)
def sheet_cut(w, h): return cutout(grid_sheet(w, h), border=0, shadow=0.3)


def hand_chart(c, t, ox, oy, w, h, vals, labels, vmin, vmax, f, col=INK, fill=YEL):
    """f in 0..1 reveal; returns tip point"""
    n = len(vals)
    def P(i, v): return (ox + 90 + (w - 160) * i / (n - 1), oy + h - 70 - (v - vmin) / (vmax - vmin) * (h - 140))
    d = ImageDraw.Draw(c)
    d.line((ox + 80, oy + h - 70, ox + w - 50, oy + h - 70), fill=INK, width=4)
    for i, lb in enumerate(labels):
        if lb:
            li = text_img(lb, 'type', 24, (90, 85, 80), 1); x, _ = P(i, vmin); c.alpha_composite(li, (int(x - li.size[0] / 2), int(oy + h - 58)))
    pts = []
    for k in range(int(f * (n - 1) * 20) + 1):
        u = k / 20; i = min(int(u), n - 2); s = u - i
        v = vals[i] + (vals[i + 1] - vals[i]) * (s * s * (3 - 2 * s)) + math.sin(k * 1.7) * (vmax - vmin) * 0.006
        pts.append(P(i + s, v))
    if len(pts) > 1:
        poly_fill(c, pts + [(pts[-1][0], oy + h - 70), (pts[0][0], oy + h - 70)], fill, 140)
        stroke(c, pts, 9, col)
        tx, ty = pts[-1]; d.ellipse((tx - 13, ty - 13, tx + 13, ty + 13), fill=RED, outline=INK, width=4)
        return pts[-1]
    return None


# ---------------- IREDA assets ----------------
def sun(c, cx, cy, s, t, col=GOLD):
    d = ImageDraw.Draw(c)
    for k in range(12):
        a = t * 0.8 + k * math.pi / 6
        d.line((cx + math.cos(a) * 70 * s, cy + math.sin(a) * 70 * s, cx + math.cos(a) * 110 * s, cy + math.sin(a) * 110 * s), fill=col, width=max(3, int(10 * s)))
    d.ellipse((cx - 55 * s, cy - 55 * s, cx + 55 * s, cy + 55 * s), fill=YEL, outline=INK, width=max(2, int(5 * s)))


def panel(c, cx, cy, s, col=NAVY):
    d = ImageDraw.Draw(c)
    w, h = 180 * s, 110 * s
    d.polygon([(cx - w / 2, cy), (cx + w / 2, cy), (cx + w / 2 - 30 * s, cy - h), (cx - w / 2 + 30 * s, cy - h)], fill=col, outline=INK)
    for k in range(1, 4):
        x0 = cx - w / 2 + k * w / 4; x1 = cx - w / 2 + 30 * s + k * (w - 60 * s) / 4
        d.line((x0, cy, x1, cy - h), fill=(170, 200, 240), width=max(1, int(3 * s)))
    d.line((cx - w / 2 + 15 * s, cy - h / 2, cx + w / 2 - 15 * s, cy - h / 2), fill=(170, 200, 240), width=max(1, int(3 * s)))
    d.rectangle((cx - 6 * s, cy, cx + 6 * s, cy + 60 * s), fill=INK)


@functools.lru_cache(None)
def step_ticket(num, title, line2, col):
    w, h = 900, 150
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 18, fill=(254, 252, 246))
    for y in range(10, h - 10, 18): d.ellipse((140 - 5, y, 140 + 5, y + 10), fill=(225, 218, 204))
    d.ellipse((30, 30, 110, 110), fill=col, outline=INK, width=4)
    nn = text_img(num, 'anton', 56, CREAM); im.alpha_composite(nn, (70 - nn.size[0] // 2, 70 - nn.size[1] // 2))
    a = text_img(title, 'anton', 60, INK); im.alpha_composite(a, (175, 14))
    b = text_img(line2, 'type', 26, GREY, 1); im.alpha_composite(b, (180, 96))
    return cutout(im, border=10, shadow=0.4)


@functools.lru_cache(None)
def risk_card(title, big, sub, col):
    w, h = 900, 230
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 18, fill=(254, 252, 246))
    d.rectangle((0, 0, 22, h - 1), fill=col)
    a = text_img(title, 'type', 28, GREY, 2); im.alpha_composite(a, (50, 20))
    b = text_img(big, 'anton', 84, col); im.alpha_composite(b, (50, 60))
    s_ = text_img(sub, 'osw5', 32, INK); im.alpha_composite(s_, (50, 172))
    return cutout(im, border=10, shadow=0.4)


# ---------------- IPO 25 Nov assets ----------------
PURP = (110, 50, 150)


def fill_meter(c, t, t0, cx, cy, w, frac, col, label, sub):
    """quota meter: box = 100% of the quota; fills to frac (can exceed 1 visually capped)"""
    q = eo(prog(t, t0, 1.1)); d = ImageDraw.Draw(c)
    x0, y0, x1, y1 = cx - w // 2, cy - 55, cx + w // 2, cy + 55
    d.rounded_rectangle((x0 + 8, y0 + 10, x1 + 8, y1 + 10), 18, fill=(200, 192, 178))
    d.rounded_rectangle((x0, y0, x1, y1), 18, fill=(254, 252, 246), outline=INK, width=6)
    fw = int((w - 20) * min(frac, 1.0) * q)
    if fw > 6: d.rounded_rectangle((x0 + 10, y0 + 10, x0 + 10 + fw, y1 - 10), 12, fill=col)
    pct = text_img(f'{frac * 100 * q:.0f}%', 'anton', 78, INK); c.alpha_composite(pct, (int(x1 - pct.size[0] - 24), int(cy - pct.size[1] / 2)))
    lb = text_img(label, 'osw5', 34, INK); c.alpha_composite(lb, (int(x0), int(y0 - 56)))
    sb = text_img(sub, 'type', 24, GREY, 1); c.alpha_composite(sb, (int(x0), int(y1 + 18)))


def coal_cart(c, cx, cy, s, t):
    d = ImageDraw.Draw(c); bob = math.sin(t * 6) * 3 * s
    r = random.Random(3)
    for k in range(14):
        x = cx + r.uniform(-120, 120) * s; y = cy - 70 * s + r.uniform(-30, 10) * s + bob
        rr = r.uniform(22, 38) * s
        d.polygon([(x - rr, y), (x - rr * 0.3, y - rr), (x + rr * 0.8, y - rr * 0.6), (x + rr, y + rr * 0.3), (x, y + rr * 0.6)], fill=(40, 38, 36), outline=INK)
    d.polygon([(cx - 170 * s, cy - 60 * s + bob), (cx + 170 * s, cy - 60 * s + bob), (cx + 130 * s, cy + 70 * s + bob), (cx - 130 * s, cy + 70 * s + bob)], fill=ORG, outline=INK, width=max(2, int(6 * s)))
    for wx in (-85, 85):
        a = t * 4
        x, y = cx + wx * s, cy + 90 * s
        d.ellipse((x - 34 * s, y - 34 * s, x + 34 * s, y + 34 * s), fill=INK)
        d.line((x, y, x + math.cos(a) * 26 * s, y + math.sin(a) * 26 * s), fill=CREAM, width=max(2, int(5 * s)))
    d.line((cx - 260 * s, cy + 128 * s, cx + 260 * s, cy + 128 * s), fill=INK, width=max(2, int(8 * s)))


def leaf(c, cx, cy, s, rot, col=GRN):
    d = ImageDraw.Draw(c); pts = []
    for k in range(25):
        u = k / 24; x = (u - 0.5) * 160 * s; y = math.sin(u * math.pi) * 45 * s
        pts.append((x, -y))
    pts += [((0.5 - k / 24) * 160 * s, math.sin((1 - k / 24) * math.pi) * 45 * s) for k in range(25)]
    ca, sa = math.cos(rot), math.sin(rot)
    P = [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]
    d.polygon(P, fill=col, outline=INK)
    d.line((cx - 80 * s * ca, cy - 80 * s * sa, cx + 80 * s * ca, cy + 80 * s * sa), fill=INK, width=max(2, int(4 * s)))


def sprayer(c, cx, cy, s, t):
    d = ImageDraw.Draw(c)
    d.rounded_rectangle((cx - 60 * s, cy - 90 * s, cx + 60 * s, cy + 110 * s), int(26 * s), fill=TEAL, outline=INK, width=max(2, int(6 * s)))
    d.rectangle((cx - 20 * s, cy - 130 * s, cx + 20 * s, cy - 90 * s), fill=INK)
    d.line((cx + 20 * s, cy - 120 * s, cx + 110 * s, cy - 150 * s), fill=INK, width=max(2, int(10 * s)))
    r = random.Random(int(t * 12))
    for k in range(18):
        a = r.uniform(-0.5, 0.4); L = r.uniform(30, 150) * s
        x, y = cx + 115 * s + math.cos(a) * L, cy - 152 * s + math.sin(a) * L
        d.ellipse((x - 5 * s, y - 5 * s, x + 5 * s, y + 5 * s), fill=(120, 190, 230))
    lb = text_img('CROP', 'anton', int(40 * s) + 1, CREAM); c.alpha_composite(lb, (int(cx - lb.size[0] / 2), int(cy - 10 * s)))


def sub_bars(c, t, rows, base, x0, gap, maxv, hmax, t_list, onex=True):
    """rows: (label, value, colour); bar heights scale by value (capped), 1x line drawn"""
    d = ImageDraw.Draw(c)
    if onex:
        y1 = base - hmax / maxv * 1.0 if maxv else base
        for xx in range(x0 - 130, x0 + gap * (len(rows) - 1) + 130, 34): d.line((xx, y1, xx + 18, y1), fill=INK, width=4)
        tl = text_img('1x', 'anton', 34, INK); c.alpha_composite(tl, (x0 - 130, int(y1 - 44)))
        lg = text_img('dashed line = 1x, fully booked', 'type', 24, GREY, 1); c.alpha_composite(lg, (540 - lg.size[0] // 2, int(base + 70)))
    for k, (lab, v, col) in enumerate(rows):
        tk = t_list[k]
        if t < tk: continue
        ph = eo(prog(t, tk, 0.7)); hg = int(max(10, min(v, maxv) / maxv * hmax) * ph); x = x0 + k * gap
        d.rounded_rectangle((x - 90, base - hg, x + 90, base), 14, fill=col, outline=INK, width=5)
        vv = v * ph
        ly = base - hg - 46
        if onex and v < 1.0: ly = min(ly, base - hmax / maxv - 46)
        place(c, text_img(f'{vv:.2f}x' if v < 10 else f'{vv:.1f}x', 'anton', 64, INK), x, ly)
        place(c, text_img(lab, 'osw5', 32, INK), x, base + 34)


@functools.lru_cache(None)
def score_row(lab, sub, col):
    w, h = 940, 150
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 16, fill=(28, 30, 34), outline=col, width=6)
    a = text_img(lab, 'anton', 52, CREAM); im.alpha_composite(a, (34, 18))
    b = text_img(sub, 'type', 24, (190, 184, 172), 1); im.alpha_composite(b, (36, 96))
    return cutout(im, border=6, shadow=0.45)


def score_line(c, t, t0, y, lab, sub, price, pct, col):
    q = pp(t, t0, 0.35, 1.3)
    if q <= 0: return
    jx, jy, jr = jit(('sr', lab), t, 1.0, 0.2)
    place(c, score_row(lab, sub, col), 540 + jx, y + jy, q, jr * 0.5)
    if q < 0.6: return
    v = roll_number(t, t0 + 0.1, 0.8, 1665, price)
    pi = text_img(f'₹{v:,.2f}', 'anton', 60, YEL); c.alpha_composite(pi, (int(440 + jx), int(y - pi.size[1] / 2 + jy)))
    if pct is not None:
        pc = text_img(pct, 'anton', 60, col); c.alpha_composite(pc, (int(985 - pc.size[0] + jx), int(y - pc.size[1] / 2 + jy)))


def roll_number(t, t0, dur, v0, v1): return v0 + (v1 - v0) * eo(prog(t, t0, dur))


# ---------------- scenes ----------------
def s1(c, t):
    i = 0
    words_line(c, t, [("NEVER", INK, 0.05), ("TRUST", INK, 0.2), ("IPO", RED, 0.35), ("HYPE", RED, 0.5)], 'anton', 112, 270, key='h1')
    dy, a = drop(t, 0.25, 360)
    if a > 0:
        hp = round(prog(t, 1.0, 0.5) * 20) / 20
        jx, jy, jr = jit('clip', t, 2, 0.5)
        place(c, clipping(hp, '₹8,981 CR IPO', 'THE IPO PAGE', 'MAHANADI COALFIELDS · CLOSED 23 NOV 2026'), 540 + jx, 590 + dy + jy, 1.0, -3 + jr + (1 - a) * 8, a)
    tr = min(at(i, 'retail', -0.3), 1.0)
    if t > tr:
        fill_meter(c, t, tr, 540, 1010, 820, 0.48, RED, 'RETAIL QUOTA BOOKED', 'bids vs shares kept for retail · final day')
    tf = at(i, 'forty eight', -0.2)
    if t > tf:
        sc, a2 = slam(t, tf); place(c, stamp_c('ONLY 0.48x', RED, 80, -6, 11), 760, 1210, sc, 0, a2)
    tw = at(i, 'Why', -0.2)
    if t > tw:
        p = prog(t, tw, 0.32); jx, jy, jr = jit('t1', t, 1.5, 0.4)
        place(c, qtag('WHY?', INK), 300 + jx, 1300 + jy, 0.55 + 0.45 * eback(p), -4 + jr, clamp(p * 3))
    src(c, t, 'Subscription: Chittorgarh, Trendlyne (close 23 Nov 2026)', 1.2, 1480)


def s2(c, t):
    i = 1; T0 = STARTS[i]
    words_line(c, t, [("COAL", INK, T0 + 0.1), ("INDIA'S", INK, T0 + 0.25), ("MINER", PURP, T0 + 0.4)], 'anton', 110, 280, key='cm')
    if t > T0 + 0.3:
        q = eo(prog(t, T0 + 0.3, 0.6))
        coal_cart(c, 540, 560, 1.0 * q + 0.01, t)
        place_text(c, 'Talcher + Ib Valley, Odisha', 'mark', 50, PURP, 540, 790, t, 'od', at(i, 'Odisha', -0.4), 'slide', rot=-3)
    cards = [('COAL MINED (FY26)', '218 MT', 'about 21% of India\'s coal output', INK, 'Two hundred'),
             ('NET PROFIT (FY26)', '₹10,698 CR', 'revenue ₹30,550 Cr', GRN, 'ten thousand')]
    for k, (a_, b_, s_, col, ph) in enumerate(cards):
        tk = at(i, ph, -0.3); pk = prog(t, tk, 0.45)
        if pk <= 0: continue
        jx, jy, jr = jit(('mc', k), t, 1.2, 0.2)
        place(c, risk_card(a_, b_, s_, col), 540 + (1 - eo(pk)) * (900 if k == 0 else -900) + jx, 980 + k * 270 + jy, 0.98, (-1.0, 1.0)[k] + jr)
    src(c, t, 'RHP figures via Business Standard (19 Nov 2026)', T0 + 1.0, 1440)


def s3(c, t):
    i = 2; T0 = STARTS[i]
    dy, a = drop(t, T0 + 0.05, 300)
    if a > 0:
        hp = round(prog(t, T0 + 0.6, 0.5) * 20) / 20
        place(c, clipping(hp, 'THE OFFER', 'MAHANADI COALFIELDS IPO', 'OPEN 19 NOV · CLOSE 23 NOV 2026'), 540, 360 + dy, 0.82, -2, a)
    pr = prog(t, at(i, 'Price band', -0.2), 0.45)
    if pr <= 0: return
    rc = receipt(); rx0, ry0 = 130, 620 + (1 - eo(pr)) * 700
    place(c, rc, rx0 + rc.size[0] / 2 - (rc.size[0] - 820) / 2 + 3, ry0 + rc.size[1] / 2 - (rc.size[1] - 720) / 2 + 7, 1.0, 0, clamp(pr * 3))
    def row(t0, y, lab, sub, amt, col, hl=None):
        q = prog(t, t0, 0.3)
        if q <= 0: return
        dx = (1 - eo(q)) * 40; a_ = clamp(q * 3)
        if hl is not None: highlight(c, rx0 + 40, ry0 + y - 46, rx0 + 780, ry0 + y + 46, prog(t, hl, 0.45), seed=21)
        li = text_img(lab, 'osw5', 46, INK); place(c, li, rx0 + 60 + li.size[0] / 2 + dx, ry0 + y - 14, 1, 0, a_)
        si = text_img(sub, 'type', 24, GREY, 1); place(c, si, rx0 + 60 + si.size[0] / 2 + dx, ry0 + y + 32, 1, 0, a_)
        ai = text_img(amt, 'anton', 66, col); place(c, ai, rx0 + 770 - ai.size[0] / 2 - dx, ry0 + y, 1, 0, a_)
    row(at(i, 'Price band', 0.1), 100, 'Price band', 'lot 110 shares', '₹129-136', INK)
    row(at(i, 'offer for sale', -0.3), 260, 'Issue size', 'all offer for sale (OFS)', '₹8,981 CR', INK, hl=at(i, 'offer for sale', 0.2))
    row(at(i, 'Coal India is', -0.2), 420, 'Seller', 'Coal India Ltd (promoter)', 'COAL INDIA', PURP)
    row(at(i, 'No new', -0.2), 580, 'Fresh issue', 'new money to the company', '₹0', RED)
    tn = at(i, 'company', 0.0)
    if t > tn:
        sc, a2 = slam(t, tn); place(c, stamp_c('100% OFS', RED, 84, 8, 33), 820, 1420, sc, 0, a2)
    src(c, t, 'Business Standard (19 Nov 2026) · Chittorgarh (24 Nov 2026)', T0 + 1.0, 1640)


def s4(c, t):
    i = 3; T0 = STARTS[i]
    tw = at(i, 'strange', -0.3)
    words_line(c, t, [("THE", INK, tw), ("STRANGE", RED, tw + 0.15), ("PART", INK, tw + 0.3)], 'anton', 120, 300, key='sp')
    ts = at(i, 'smaller', -0.3)
    dy, a = drop(t, ts, 360)
    if a > 0:
        hp = round(prog(t, ts + 0.6, 0.5) * 20) / 20
        place(c, clipping(hp, 'CRYSTAL CROP', 'SAME WEEK', 'CRYSTAL CROP PROTECTION · ₹455 CR'), 540, 600 + dy, 0.9, 3, a)
    te = at(i, 'eighteen', -1.0)
    if t > te:
        v = roll_number(t, te, 1.2, 0, 17.68)
        jx, jy, jr = jit('cn', t, 1.2, 0.3)
        place(c, text_img(f'{v:.2f}x', 'anton', 260, GRN if v > 1 else INK), 540 + jx, 1060 + jy, 1.0, jr)
        place(c, text_img('subscribed, final day (20 Nov 2026)', 'osw5', 40, INK), 540, 1240, pp(t, te + 0.8))
    if ts + 0.4 < t < te:
        place(c, text_img('?', 'anton', 300, RED), 540, 1060, 1.0 + 0.06 * math.sin(t * 9), 6 * math.sin(t * 3))
    src(c, t, 'Chittorgarh 20 Nov 2026, 5:54 PM (Trendlyne: 17.1x)', T0 + 1.0, 1420)


def s5(c, t):
    i = 4; T0 = STARTS[i]
    words_line(c, t, [("CRYSTAL", GRN, T0 + 0.05), ("CROP", GRN, T0 + 0.2)], 'anton', 110, 260, key='cc')
    if t > T0 + 0.3:
        q = eo(prog(t, T0 + 0.3, 0.5))
        sprayer(c, 250, 520, 0.95 * q + 0.01, t)
        for k, (x, y, r_) in enumerate(((620, 470, -0.5), (760, 560, 0.4), (880, 450, -0.2))):
            leaf(c, x, y + math.sin(t * 3 + k) * 6, 0.9 * q + 0.01, r_ + 0.1 * math.sin(t * 2 + k))
        place(c, text_img('herbicides · insecticides · fungicides · seeds', 'type', 28, INK, 1), 540, 700, pp(t, at(i, 'sprays', 0.0)))
    tb = at(i, 'four hundred', -0.2)
    if t > tb:
        place_text(c, '₹455 Cr: ₹355 Cr new + ₹101 Cr OFS · band ₹259-272', 'osw5', 36, INK, 540, 780, t, 'cs', tb, 'slide')
    sub_bars(c, t, [('RICH (NII)', 39.16, GRN), ('INSTITUTIONS', 15.81, BLUE), ('RETAIL', 9.71, ORG)], 1330, 230, 310, 40, 420,
             [at(i, 'Rich', -0.2), at(i, 'Rich', 1.0), at(i, 'Retail', -0.2)])
    src(c, t, 'Chittorgarh 20 Nov 2026 · business: RHP (12 Nov 2026)', T0 + 1.0, 1450)


def s6(c, t):
    i = 5; T0 = STARTS[i]
    words_line(c, t, [("MAHANADI'S", PURP, T0 + 0.05), ("FINAL", INK, T0 + 0.25), ("COUNT", INK, T0 + 0.4)], 'anton', 100, 280, key='mf')
    tt = at(i, 'One point', -0.2)
    if t > tt:
        sc, a = slam(t, tt); place(c, stamp_c('TOTAL 1.52x', PURP, 90, -4, 51), 540, 470, sc, 0, a)
    sub_bars(c, t, [('INSTITUTIONS', 4.95, BLUE), ('RICH (NII)', 0.66, GRN), ('RETAIL', 0.48, RED)], 1180, 230, 310, 5.5, 520,
             [at(i, 'Institutions', -0.2), at(i, 'Institutions', 0.8), at(i, 'Retail', -0.2)])
    tr = at(i, 'zero point', 0.2)
    if t > tr:
        marker_ellipse(c, 850, 1180 - 520 / 5.5 - 46, 120, 60, prog(t, tr, 0.45), RED, 8, seed=5)
        place_text(c, 'retail quota not filled', 'mark', 46, RED, 720, 1330, t, 'rq', tr + 0.2, 'slide', rot=-3)
    src(c, t, 'Chittorgarh 23 Nov 2026, 5:54 PM (Trendlyne: 1.5x)', T0 + 1.0, 1460)


EAAA = [1727.8, 1722.3, 1689.9, 1700.1, 1682.2, 1667.3, 1695.5, 1746, 1833.2, 1974.2, 1949.6, 1963.4, 1915.7, 1960.2, 1895.9, 1822.2]
ELAB = ['2 NOV'] + [''] * 8 + ['13 NOV'] + [''] * 5 + ['23 NOV']


def s7(c, t):
    i = 6; T0 = STARTS[i]
    tq = at(i, 'big demand', -0.4)
    place_text(c, 'big demand = big listing?', 'pfi', 70, INK, 540, 270, t, 'bd', tq, 'pop')
    te = at(i, 'Look at', -0.1)
    dy, a = drop(t, te, 300)
    if a > 0:
        hp = round(prog(t, te + 0.6, 0.5) * 20) / 20
        place(c, clipping(hp, 'EAAA INDIA ALTS', 'LISTED 2 NOV 2026', 'EAAA INDIA ALTERNATIVES · ₹1,200 CR OFS'), 540, 560 + dy, 0.85, -2, a)
    tf = at(i, 'Five point', -0.2)
    if t > tf:
        sc, a2 = slam(t, tf); place(c, stamp_c('5.3x SUBSCRIBED', NAVY, 70, 5, 61), 540, 830, sc, 0, a2)
    score_line(c, t, at(i, 'opened', -1.2), 1030, 'ISSUE PRICE', 'final price, Oct 2026', 1665, None, GREY)
    score_line(c, t, at(i, 'opened', -0.2), 1210, 'LISTING OPEN', 'NSE, 2 Nov 2026', 1675.5, '+0.6%', YEL)
    to = at(i, 'zero point', 0.4)
    if t > to:
        place_text(c, 'almost flat', 'mark', 56, RED, 760, 1360, t, 'af', to, 'slide', rot=-4)
    src(c, t, '5.25x Groww / 5.51x 5paisa · open: NSE, 2 Nov 2026', T0 + 1.0, 1460)


def s8(c, t):
    i = 7; T0 = STARTS[i]
    tl = at(i, 'Subscription shows', -0.3)
    if t < tl:
        place(c, text_img('EAAA SCOREBOARD', 'osw', 54, YEL, 2), 540, 250, pp(t, T0 + 0.05))
        score_line(c, t, T0 + 0.05, 400, 'ISSUE PRICE', 'final price', 1665, None, GREY)
        score_line(c, t, T0 + 0.15, 570, 'LISTING OPEN', 'NSE, 2 Nov 2026', 1675.5, '+0.6%', YEL)
        score_line(c, t, at(i, 'closed day', -0.2), 740, 'DAY-1 CLOSE', 'NSE, 2 Nov 2026', 1727.8, '+3.8%', GRN)
        score_line(c, t, at(i, 'November', -0.2), 910, 'LATEST CLOSE', 'NSE, 23 Nov 2026', 1822.2, '+9.4%', GRN)
        p = prog(t, T0 + 0.6, 0.45)
        if p > 0:
            ox, oy = 70, 1030 + (1 - eo(p)) * 500; w, h = 940, 470
            place(c, sheet_cut(w, h), ox + w / 2, oy + h / 2, 1.0, 0, clamp(p * 3))
            d = ImageDraw.Draw(c); yi = oy + h - 70 - (1665 - 1600) / 450 * (h - 140)
            for xx in range(ox + 80, ox + w - 50, 30): d.line((xx, yi, xx + 16, yi), fill=RED, width=4)
            hand_chart(c, t, ox, oy, w, h, EAAA, ELAB, 1600, 2050, eio(prog(t, T0 + 0.9, 3.0)), INK, (150, 220, 170))
            c.alpha_composite(text_img('issue ₹1,665', 'type', 26, RED, 1), (ox + w - 260, int(yi + 8)))
    else:
        SS.myth_fact(c, t, tl, ['big', 'subscription', '= big listing'], ['subscription', '= demand,', 'not the price'], y0=230, y1=1180)
        rows = [('CRYSTAL CROP', 'lists THU 26 NOV', 'Crystal', GRN), ('MAHANADI', 'lists FRI 27 NOV', 'Mahanadi', PURP)]
        for k, (h1, h2, ph, col) in enumerate(rows):
            tk = at(i, ph, -0.3)
            if t < tk: continue
            y = 1300 + k * 170; q = pp(t, tk, 0.35, 1.3)
            jx, jy, jr = jit(('v', k), t, 1.2, 0.2)
            place(c, score_row(h1, 'tentative listing date, NSE + BSE', col), 540 + jx, y + jy, q, (-0.6, 0.6)[k] + jr)
            if q > 0.6:
                hi = text_img(h2, 'anton', 52, col); c.alpha_composite(hi, (int(980 - hi.size[0] + jx), int(y - 40 + jy)))
    src(c, t, 'NSE closes via INDmoney, 2-23 Nov 2026', T0 + 1.0, 1640, (190, 184, 172))


def s9(c, t):
    i = 8; T0 = STARTS[i]
    q = pp(t, T0, 0.45, 1.2)
    place(c, SS._card(960, 860), 540, 600, q, -0.4)
    if q > 0.6:
        place(c, text_img('IPO REPORT · 25 NOV 2026', 'anton', 56, INK), 540, 230)
        d = ImageDraw.Draw(c); d.line((90, 272, 990, 272), fill=INK, width=4)
        rows = [('Mahanadi: size / fresh money', '₹8,981 Cr / ₹0', PURP), ('Mahanadi subscribed', '1.52x', PURP),
                ('Mahanadi retail', '0.48x', RED), ('Crystal Crop subscribed', '17.68x', GRN),
                ('Crystal Crop NII / retail', '39.2x / 9.7x', GRN), ('EAAA 5.3x: open vs issue', '+0.6%', INK),
                ('EAAA day-1 close / 23 Nov', '+3.8% / +9.4%', GRN), ('Listing: Crystal / Mahanadi', '26 / 27 NOV', NAVY)]
        for k, (a_, b_, col) in enumerate(rows):
            tk = T0 + 0.3 + 0.08 * k
            if t < tk: continue
            y = 300 + k * 78
            c.alpha_composite(text_img(a_, 'osw5', 38, INK), (100, y))
            v = text_img(b_, 'anton', 44, col); c.alpha_composite(v, (980 - v.size[0], y - 2))
        SS.save_pulse(c, t, T0 + 1.2, 540, 1080, 'SAVE THIS')
    SS.send_frame(c, t, at(i, 'send it', -0.3), 'the friend who loves IPOs', y=1300)
    tf = at(i, 'Follow', -0.2)
    if t > tf:
        q2 = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1530, 0.5 + 0.5 * eback(q2), 0, clamp(q2 * 3))
    for k, ln in enumerate(['Data: Chittorgarh, Trendlyne, NSE via INDmoney (23 Nov 2026)',
                            'Not a recommendation to apply for any IPO. No GMP. I may hold stocks named.',
                            'Not a buy/sell call. Education only, not investment advice.']):
        place_text(c, ln, 'type', 22, GREY, 540, 1680 + k * 34, t, None, T0 + 0.3, 'fade', track=1)

def pp(t, t0, d=0.35, s=1.6): return eback(prog(t, t0, d), s)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
DARK_SCENES = {7}


def slam_times():
    return [at(0, 'forty eight', -0.2), at(2, 'company', 0.0), at(3, 'eighteen', 0.2), at(5, 'One point', -0.2), at(6, 'Five point', -0.2)] + [STARTS[k] + 0.05 for k in range(1, 8)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('IPO LISTING REPORT', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
    ImageDraw.Draw(c).line((60, 118, W - 60, 118), fill=col, width=2)
    ImageDraw.Draw(c).line((60, 118, 60 + (W - 120) * clamp(t / DUR), 118), fill=RED if not dark else YEL, width=8)


def transition(c, t):
    cols = [(RED, INK), (YEL, INK), (INK, RED), (TEAL, YEL), (YEL, RED), (INK, YEL), (RED, YEL), (YEL, INK)]
    for bi, b in enumerate(B):
        d = 0.62
        if abs(t - b) > d / 2 + 0.12: continue
        for layer, delay in ((0, -0.07), (1, 0.0)):
            p = (t - (b - d / 2) - delay) / d
            if p <= 0 or p >= 1: continue
            p = eio(p); SWd, skew = 2050, 320
            xl = (W + 60) + p * (-(SWd + skew) - (W + 60) - 40)
            r = random.Random(bi * 10 + layer + 777)
            left = [(xl + r.uniform(-14, 14) - skew * (y / H), y) for y in range(0, H + 1, 40)]
            right = [(xl + SWd + r.uniform(-14, 14) - skew * (y / H), y) for y in range(H, -1, -40)]
            if layer == 0: left = [(x - 70, y) for x, y in left]; right = [(x + 70, y) for x, y in right]
            poly_fill(c, left + right, cols[bi % len(cols)][layer], 255, S=1)


def scene_at(t):
    k = 0
    for i, s in enumerate(STARTS):
        if t >= s: k = i
    return k


def render(t):
    LOOP = 0.6
    if t > DUR - LOOP:
        a = _render(t); b = _render(1.4, loop=True); q = eio((t - (DUR - LOOP)) / LOOP)
        return (a * (1 - q) + b * q).astype(np.uint8)
    return _render(t)


def _render(t, loop=False):
    pbg, dbg = bgs()
    i = scene_at(t); dark = i in DARK_SCENES
    c = (dbg if dark else pbg).copy()
    st = STARTS[i]; en = STARTS[i + 1] if i + 1 < len(STARTS) else DUR
    SCENES[i](c, t)
    z = 1.0 + 0.04 * clamp((t - st) / (en - st))
    sx = sy = 0
    for ts in slam_times():
        if 0 <= t - ts < 0.35:
            k = math.exp(-(t - ts) * 14) * 9
            sx += k * math.sin((t - ts) * 90); sy += k * math.cos((t - ts) * 77)
    cw, ch = W / z, H / z
    cx, cy = W / 2 + sx, H * 0.47 + sy
    c = c.transform((W, H), Image.EXTENT, (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2), Image.BICUBIC)
    header(c, dark, t if not loop else 0); transition(c, t)
    arr = np.asarray(c.convert('RGB')).astype(np.float32)
    g = grain_frames()[int(t * FPS) % 6]
    fl = 1 + 0.012 * math.sin(t * 37) * math.sin(t * 13)
    return np.clip(arr * fl + g[..., None], 0, 255).astype(np.uint8)
