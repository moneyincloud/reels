"""IPO regret club: 9 famous IPOs, issue price vs today (paper collage, tickets, stamps, bar race)"""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs, typed, drop, warn_icon
from fridge import follow_btn
import saveshare as SS
import tea as TEA

SH = ROOT + 'ipo/'
SCRIPT = json.load(open(SH + 'script.json'))
DURS = json.load(open(SH + 'vo/durs.json'))
LEAD, TAIL = 0.15, 0.3
STARTS, VO = [], []
_t = 0.0
for i, d in enumerate(DURS):
    STARTS.append(_t); VO.append(_t + (0.1 if i == 0 else LEAD)); _t = VO[-1] + d + TAIL
DUR = _t + 1.8
B = STARTS[1:]
NAVY = (30, 60, 120); BLUE = (40, 100, 200); GREY = (120, 112, 104); TEAL = (20, 140, 130); GOLD = (214, 160, 40); ORG = (230, 120, 30)
PURP = (120, 70, 200); PINK = (230, 90, 140); SOFT = (252, 250, 244)
label = TEA.label

# key: name, ipo price (adjusted), now (30 Oct 2026 11:42 IST), year, colour, note
D = {
    'PAYTM': ('PAYTM', 2150, 1660.0, 2021, BLUE, ''),
    'LIC': ('LIC', 474.5, 387.4, 2022, NAVY, '₹949, halved by 1:1 bonus'),
    'SWIGGY': ('SWIGGY', 390, 177.3, 2024, ORG, ''),
    'OLA': ('OLA ELECTRIC', 76, 34.07, 2024, GRN, ''),
    'HYUNDAI': ('HYUNDAI', 1960, 1904.2, 2024, NAVY, ''),
    'PB': ('POLICYBAZAAR', 980, 1013.3, 2021, TEAL, ''),
    'TATA': ('TATA TECH', 500, 653.35, 2023, BLUE, ''),
    'NYKAA': ('NYKAA', 187.5, 350.35, 2021, PINK, '₹1,125, adjusted for 5:1 bonus'),
    'ZOM': ('ZOMATO / ETERNAL', 76, 344.3, 2021, RED, ''),
}
ORDER = ['OLA', 'SWIGGY', 'PAYTM', 'LIC', 'HYUNDAI', 'PB', 'TATA', 'NYKAA', 'ZOM']


def chg(k): n, ip, now, *_ = D[k]; return (now / ip - 1) * 100


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def pp(t, t0, d=0.35, s=1.6): return eback(prog(t, t0, d), s)


def src(c, t, txt, t0, y=1740, col=GREY):
    if t > t0: place_text(c, txt, 'type', 24, col, 540, y, t, None, t0, 'fade', track=1)


def fmt(v): return f'{v:,.0f}' if v >= 100 else f'{v:,.2f}'.rstrip('0').rstrip('.')


@functools.lru_cache(None)
def ticket(k, big=True):
    n, ip, now, yr, col, note = D[k]
    w, h = (900, 330) if big else (900, 200)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 20, fill=(254, 252, 246))
    d.rectangle((0, 0, 26, h), fill=col)
    for y in range(12, h - 12, 22): d.ellipse((640 - 5, y, 640 + 5, y + 10), fill=(225, 218, 204))
    t = text_img(n, 'anton', 64 if big else 52, INK); im.alpha_composite(t, (56, 18))
    yt = text_img(f'IPO {yr}', 'type', 24, GREY, 2); im.alpha_composite(yt, (56 + t.size[0] + 18, 18 + t.size[1] - 34))
    y0 = 128 if big else 98
    a = text_img('IPO PRICE', 'type', 22, GREY, 2); im.alpha_composite(a, (60, y0 + 10))
    b = text_img(f'₹{fmt(ip)}', 'anton', 72 if big else 54, INK); im.alpha_composite(b, (60, y0 + 34))
    a2 = text_img('TODAY', 'type', 22, GREY, 2); im.alpha_composite(a2, (360, y0 + 10))
    up = now >= ip
    b2 = text_img(f'₹{fmt(now)}', 'anton', 72 if big else 54, GRN if up else RED); im.alpha_composite(b2, (360, y0 + 34))
    pc = (now / ip - 1) * 100
    fs = 110 if big else 80
    p = text_img(f'{pc:+.0f}%', 'anton', fs, GRN if up else RED)
    if p.size[0] > 230: p = text_img(f'{pc:+.0f}%', 'anton', int(fs * 230 / p.size[0]), GRN if up else RED)
    im.alpha_composite(p, (int(770 - p.size[0] / 2), int(h / 2 - p.size[1] / 2 - 6)))
    if note and big:
        nt = text_img(note, 'type', 22, GREY, 1); im.alpha_composite(nt, (60, h - 40))
    return cutout(im, border=8, shadow=0.38)


def show_ticket(c, t, t0, k, y, big=True, rot=None):
    if t < t0: return
    p = prog(t, t0, 0.45); jx, jy, jr = jit(('tk', k), t, 1.4, 0.3)
    r = rot if rot is not None else random.Random(k).uniform(-1.6, 1.6)
    place(c, ticket(k, big), 540 + jx + (1 - eo(p)) * 900, y + jy, 1.0, r + jr + (1 - eo(p)) * -8, clamp(p * 3))
    up = D[k][2] >= D[k][1]


# ---------------- scenes ----------------
def s1(c, t):
    i = 0
    words_line(c, t, [("YOUR", INK, 0.1), ("IPO", RED, 0.25), ("MONEY", INK, 0.4)], 'anton', 140, 290, key='h1')
    # grid of 9 mini logos (name chips) shuffle in
    for k, key in enumerate(ORDER):
        tk = 0.4 + 0.09 * k
        if t < tk: continue
        r_, cc = divmod(k, 3); x = 200 + cc * 340; y = 520 + r_ * 200
        p = pp(t, tk); jx, jy, jr = jit(('g', k), t, 1.4, 0.3)
        up = chg(key) >= 0
        reveal = t > at(i, 'five of', 0.2) + 0.12 * k
        col = (GRN if up else RED) if reveal else D[key][4]
        place(c, label(D[key][0].split(' /')[0], col), x + jx, y + jy, 0.78 * p, (-3, 2, -2, 3, -1, 2, -3, 1, -2)[k] + jr)
    tf = at(i, 'five of', -0.2)
    if t > tf:
        sc, a = slam(t, tf + 0.9); place(c, stamp_c('5 OF 9 BELOW IPO PRICE', RED, 72, -4, 5), 540, 1210, sc, 0, a)
    th = at(i, 'full list', -0.3)
    if t > th: place_text(c, 'prices: 30 Oct 2026', 'mark', 48, INK, 540, 1360, t, 'pr', th, 'slide', rot=-3)
    src(c, t, 'NSE via INDmoney, 30 Oct 2026, 11:42 IST · IPO issue prices', 1.2, 1720)


def s2(c, t):
    i = 1; T0 = STARTS[i]
    place_text(c, 'BELOW IPO PRICE', 'anton', 100, RED, 540, 260, t, 'b1', T0 + 0.05, 'pop')
    show_ticket(c, t, at(i, 'Paytm', -0.3), 'PAYTM', 600)
    show_ticket(c, t, at(i, 'LIC', -0.3), 'LIC', 1020)
    tb = at(i, 'bonus', -0.3)
    if t > tb: place_text(c, 'adjusted for 1:1 bonus', 'mark', 44, INK, 540, 1260, t, 'bn', tb, 'slide', rot=-3)
    src(c, t, 'IPO: Paytm ₹2,150 (2021), LIC ₹949 (2022, 1:1 bonus 2026)', T0 + 1.0, 1720)


def s3(c, t):
    i = 2; T0 = STARTS[i]
    place_text(c, 'HALF GONE', 'anton', 120, RED, 540, 260, t, 'hg', T0 + 0.05, 'pop')
    show_ticket(c, t, at(i, 'Swiggy', -0.3), 'SWIGGY', 600)
    show_ticket(c, t, at(i, 'Ola', -0.3), 'OLA', 1020)
    tf = at(i, 'Both down', -0.3)
    if t > tf:
        place_text(c, '₹1 lakh = ₹45,000', 'pfi', 70, RED, 540, 1290, t, 'hl', tf, 'pop')
        marker_line(c, [(250, 1340), (540, 1334), (830, 1326)], prog(t, tf + 0.3, 0.4), RED, 8)
    src(c, t, 'IPO: Swiggy ₹390, Ola ₹76 (2024) · ₹1 lakh value: my calc', T0 + 1.0, 1720)


def s4(c, t):
    i = 3; T0 = STARTS[i]
    place_text(c, "INDIA'S BIGGEST IPO", 'anton', 92, INK, 540, 260, t, 'bi', T0 + 0.05, 'pop')
    show_ticket(c, t, at(i, 'Hyundai', -0.3), 'HYUNDAI', 560)
    tw = at(i, 'did anyone', -0.3)
    if t > tw:
        place_text(c, 'did anyone win?', 'pfi', 80, INK, 540, 900, t, 'dw', tw, 'pop')
    ty = at(i, 'Yes', -0.2)
    if t > ty:
        sc, a = slam(t, ty); place(c, stamp_c('YES!', GRN, 120, -8, 13), 540, 1080, sc, 0, a)
    tq = at(i, 'quadrupled', -0.4)
    if t > tq:
        p = pp(t, tq); place(c, label('ONE IPO MORE THAN 4X', GOLD), 540, 1280, 1.1 * p, -2)
        marker_ellipse(c, 540, 1280, 320, 70, prog(t, tq + 0.4, 0.5), RED, 7, seed=4)
    src(c, t, 'Hyundai Motor India IPO price ₹1,960 (Oct 2024)', T0 + 1.0, 1720)


def s5(c, t):
    i = 4; T0 = STARTS[i]
    place_text(c, 'THE WINNERS', 'anton', 120, GRN, 540, 260, t, 'tw', T0 + 0.05, 'pop')
    show_ticket(c, t, at(i, 'Policybazaar', -0.3), 'PB', 520, big=False)
    show_ticket(c, t, at(i, 'Tata', -0.3), 'TATA', 790, big=False)
    show_ticket(c, t, at(i, 'Nykaa', -0.3), 'NYKAA', 1060, big=False)
    tb = at(i, 'bonus', -0.3)
    if t > tb: place_text(c, 'Nykaa: ₹1,125 adjusted for 5:1 bonus', 'mark', 42, INK, 540, 1270, t, 'nb', tb, 'slide', rot=-2)
    src(c, t, 'IPO: Policybazaar ₹980, Nykaa ₹1,125, Tata Tech ₹500', T0 + 1.0, 1720)


def s6(c, t):
    i = 5; T0 = STARTS[i]
    words_line(c, t, [("THE", INK, T0 + 0.05), ("4X", GRN, T0 + 0.2), ("WINNER", INK, T0 + 0.35)], 'anton', 130, 270, key='w4')
    show_ticket(c, t, at(i, 'Zomato', -0.3), 'ZOM', 560)
    tl = at(i, 'One lakh', -0.3)
    if t > tl:
        v = 100000 + (453026 - 100000) * eo(prog(t, tl + 0.2, 1.4))
        place(c, text_img(f'₹1,00,000', 'anton', 80, GREY), 540, 900, pp(t, tl))
        marker_line(c, [(540, 950), (538, 1000), (540, 1050)], prog(t, tl + 0.2, 0.3), INK, 8, head=True)
        place(c, text_img(f'₹{int(v):,}', 'anton', 150, GRN), 540, 1140)
        r = random.Random(3); d = ImageDraw.Draw(c)
        if t > tl + 1.4:
            for k in range(30):
                x0 = r.uniform(80, 1000); sp = r.uniform(300, 700); ph = r.uniform(0, 6)
                y = 150 + ((t - tl) * sp + r.uniform(0, 400)) % 1300
                s_ = 10; xx = x0 + math.sin(t * 3 + ph) * 30
                d.rectangle((xx - s_, y - s_ / 2, xx + s_, y + s_ / 2), fill=(GOLD, RED, GRN, BLUE, YEL)[k % 5])
    src(c, t, 'Zomato IPO ₹76 (Jul 2021) · Eternal ₹344.30 · my calc', T0 + 1.0, 1720)


def s7(c, t):
    i = 6; T0 = STARTS[i]
    if t > T0 + 0.1:
        p = prog(t, T0 + 0.1, 0.3); lw = text_w('THE LESSON', 'osw', 54, 2); x0 = 540 - (lw + 70) / 2
        place(c, warn_icon(YEL), x0 + 28, 262, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
        place(c, text_img('THE LESSON', 'osw', 54, YEL, 2), x0 + 70 + lw / 2, 260, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
    th = at(i, 'Hype', -0.2)
    words_line(c, t, [("HYPE", RED, th), ("IS", CREAM, th + 0.15), ("NOT", CREAM, th + 0.25)], 'anton', 130, 430, key='hy1')
    words_line(c, t, [("A", CREAM, th + 0.4), ("BUSINESS", CREAM, th + 0.5)], 'anton', 130, 580, key='hy2')
    # bar race of all 9 % changes
    tb = at(i, 'allotment', -0.4)
    if t > tb:
        d = ImageDraw.Draw(c); cx0 = 430
        d.line((cx0, 700, cx0, 1530), fill=(200, 194, 182), width=3)
        for k, key in enumerate(ORDER):
            tk = tb + 0.1 * k;
            if t < tk: continue
            y = 730 + k * 90; pc = chg(key); ph = eo(prog(t, tk, 0.6)); w = int(abs(pc) * 1.1 * ph)
            col = GRN if pc >= 0 else RED
            if pc >= 0: d.rounded_rectangle((cx0, y - 26, cx0 + w, y + 26), 8, fill=col)
            else: d.rounded_rectangle((cx0 - w, y - 26, cx0, y + 26), 8, fill=col)
            nm = text_img(D[key][0].split(' /')[0], 'osw5', 30, CREAM)
            if pc >= 0: c.alpha_composite(nm, (cx0 - nm.size[0] - 14, y - 20)); v = text_img(f'{pc * ph:+.0f}%', 'anton', 38, col); c.alpha_composite(v, (cx0 + w + 10, y - 24))
            else: c.alpha_composite(nm, (cx0 + 14, y - 20)); v = text_img(f'{pc * ph:+.0f}%', 'anton', 38, col); c.alpha_composite(v, (cx0 - w - v.size[0] - 10, y - 24))
    tp = at(i, 'profit and price', -0.3)
    if t > tp: place_text(c, 'profit + price decide it', 'mark', 50, YEL, 540, 1620, t, 'pp', tp, 'slide', rot=-3)


def s8(c, t):
    i = 7; T0 = STARTS[i]
    place_text(c, 'BEFORE YOUR NEXT IPO', 'anton', 92, INK, 540, 260, t, 'bn', T0 + 0.05, 'pop')
    items = [('Is it making profit?', 'Is it making profit', 'check the last 3 years'), ('Is the price high vs peers?', 'price high', 'compare P/E with listed rivals'),
             ('Are old owners selling?', 'old owners', 'check the offer for sale (OFS) part')]
    for k, (h1, ph, sub) in enumerate(items):
        tk = at(i, ph, -0.3)
        if t < tk: continue
        y = 520 + k * 330; q = pp(t, tk, 0.35, 1.3)
        place(c, cutout(Image.new('RGBA', (920, 260), SOFT + (255,)), border=0, shadow=0.35), 540, y, q, (-0.8, 0.8, -0.6)[k])
        if q < 0.6: continue
        n = text_img(str(k + 1), 'anton', 120, RED); c.alpha_composite(n, (110, int(y - 80)))
        c.alpha_composite(text_img(h1, 'anton', 58, INK), (220, int(y - 70)))
        c.alpha_composite(text_img(sub, 'type', 30, GREY, 1), (224, int(y + 20)))
        d = ImageDraw.Draw(c); bx = 930
        if t > tk + 0.6: d.line((bx - 22, y + 2, bx - 6, y + 20, bx + 24, y - 18), fill=GRN, width=10, joint='curve')
    src(c, t, 'Read the IPO prospectus (RHP) on SEBI / exchange websites', T0 + 1.0, 1560)


def s9(c, t):
    i = 8; T0 = STARTS[i]
    q = pp(t, T0, 0.45, 1.2)
    place(c, SS._card(960, 880), 540, 600, q, -0.4)
    if q > 0.6:
        place(c, text_img('IPO PRICE VS TODAY', 'anton', 56, INK), 540, 220)
        d = ImageDraw.Draw(c); d.line((90, 262, 990, 262), fill=INK, width=4)
        for k, key in enumerate(ORDER[::-1]):
            tk = T0 + 0.3 + 0.07 * k
            if t < tk: continue
            y = 290 + k * 82; pc = chg(key)
            c.alpha_composite(text_img(D[key][0], 'osw5', 38, INK), (100, y))
            v = text_img(f'{pc:+.0f}%', 'anton', 46, GRN if pc >= 0 else RED); c.alpha_composite(v, (980 - v.size[0], y - 4))
    SS.send_frame(c, t, at(i, 'Tag the friend', -0.3), 'the friend who applied for all 9', y=1180)
    SS.save_pulse(c, t, at(i, 'Save this', -0.3), 540, 1380, 'SAVE THIS')
    tf = at(i, 'Follow', -0.2)
    if t > tf:
        q2 = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1560, 0.5 + 0.5 * eback(q2), 0, clamp(q2 * 3))
    for k, ln in enumerate(['Prices: NSE via INDmoney, 30 Oct 2026 11:42 IST', 'LIC & Nykaa IPO prices adjusted for bonus shares', 'Not a buy/sell call. Education only.']):
        place_text(c, ln, 'type', 22, GREY, 540, 1700 + k * 34, t, None, T0 + 0.3, 'fade', track=1)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
DARK_SCENES = {6}


def slam_times():
    return [at(0, 'five of', 0.7), at(3, 'Yes', -0.2)] + [STARTS[k] + 0.05 for k in range(1, 8)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('IPO REGRET CLUB', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
    ImageDraw.Draw(c).line((60, 118, W - 60, 118), fill=col, width=2)
    ImageDraw.Draw(c).line((60, 118, 60 + (W - 120) * clamp(t / DUR), 118), fill=RED if not dark else YEL, width=8)


def transition(c, t):
    cols = [(RED, INK), (YEL, INK), (ORG, CREAM), (NAVY, YEL), (GRN, CREAM), (INK, YEL), (YEL, RED), (RED, YEL)]
    for bi, b in enumerate(B):
        d = 0.55
        if abs(t - b) > d / 2 + 0.12: continue
        for layer, delay in ((0, -0.07), (1, 0.0)):
            p = (t - (b - d / 2) - delay) / d
            if p <= 0 or p >= 1: continue
            p = eio(p); SWd, skew = 2050, 320
            xl = (W + 60) + p * (-(SWd + skew) - (W + 60) - 40)
            r = random.Random(bi * 10 + layer + 333)
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
        a = _render(t); b = _render(1.6, loop=True); q = eio((t - (DUR - LOOP)) / LOOP)
        return (a * (1 - q) + b * q).astype(np.uint8)
    return _render(t)


def _render(t, loop=False):
    pbg, dbg = bgs()
    i = scene_at(t); dark = i in DARK_SCENES
    c = (dbg if dark else pbg).copy()
    st = STARTS[i]; en = STARTS[i + 1] if i + 1 < len(STARTS) else DUR
    SCENES[i](c, t)
    z = 1.0 + 0.035 * clamp((t - st) / (en - st))
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
