"""IRFC: multibagger or trap? Suzlon/PC Jeweller-style paper collage (male VO)"""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs, typed, drop, warn_icon, receipt
from fridge import follow_btn
import saveshare as SS
import defence as DF

SH = ROOT + 'irfc/'
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


# ---------------- IRFC assets ----------------
def train(c, x, y, s=1.0, n=3, col=NAVY, wcol=INK, t=0):
    """simple side-view train: loco + n coaches, x = nose position (train runs right)"""
    d = ImageDraw.Draw(c)
    L = 230 * s; Hh = 120 * s
    # loco
    x0 = x - L
    d.rounded_rectangle((x0, y - Hh, x, y), int(18 * s), fill=col, outline=wcol, width=max(2, int(5 * s)))
    d.polygon([(x - 8 * s, y - Hh), (x + 40 * s, y - Hh * 0.45), (x + 40 * s, y), (x - 8 * s, y)], fill=col, outline=wcol)
    d.rectangle((x - 70 * s, y - Hh + 18 * s, x - 18 * s, y - Hh + 58 * s), fill=(220, 236, 250), outline=wcol, width=max(2, int(4 * s)))
    d.rectangle((x0 + 10 * s, y - 34 * s, x + 40 * s, y - 22 * s), fill=YEL)
    for k in range(n):
        cx1 = x0 - 12 * s - k * (L + 12 * s); cx0 = cx1 - L
        d.rounded_rectangle((cx0, y - Hh, cx1, y), int(14 * s), fill=(214, 70, 50) if k % 2 == 0 else ORG, outline=wcol, width=max(2, int(5 * s)))
        for w_ in range(4):
            wx = cx0 + 22 * s + w_ * 52 * s
            d.rectangle((wx, y - Hh + 20 * s, wx + 36 * s, y - Hh + 56 * s), fill=(220, 236, 250), outline=wcol, width=max(2, int(3 * s)))
    # wheels
    xs = [x0 + 40 * s, x0 + L - 60 * s] + [x0 - 12 * s - k * (L + 12 * s) - p for k in range(n) for p in (40 * s, L - 40 * s)]
    for wx in xs:
        r = 20 * s; d.ellipse((wx - r, y - r * 0.6, wx + r, y + r * 1.4), fill=INK)
        a = t * 12; d.line((wx, y + r * 0.4, wx + math.cos(a) * r * 0.8, y + r * 0.4 + math.sin(a) * r * 0.8), fill=(200, 200, 200), width=max(2, int(3 * s)))


def rails(c, y, x0=0, x1=W):
    d = ImageDraw.Draw(c)
    d.line((x0, y + 34, x1, y + 34), fill=INK, width=6)
    for x in range(int(x0), int(x1), 46): d.line((x, y + 30, x + 26, y + 44), fill=(120, 90, 60), width=8)


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


# ---------------- scenes ----------------
def s1(c, t):
    i = 0
    words_line(c, t, [("HOLDING", INK, 0.1), ("IRFC?", RED, 0.35)], 'anton', 132, 300, key='h1')
    dy, a = drop(t, 0.5, 360)
    if a > 0:
        hp = round(prog(t, 1.2, 0.5) * 20) / 20
        jx, jy, jr = jit('clip', t, 2, 0.5)
        place(c, clipping(hp), 540 + jx, 640 + dy + jy, 1.0, -3 + jr + (1 - a) * 8, a)
    td = at(i, "Don't average", -0.2)
    if t > td:
        place_text(c, "don't average down yet!", 'mark', 66, RED, 540, 900, t, 'dbm', td, 'slide', rot=-4, amp=1.5)
        marker_line(c, [(200, 960), (540, 952), (880, 942)], prog(t, td + 0.4, 0.4), RED, 9)
    tm = at(i, 'Multibagger', -0.25)
    if t > tm:
        p = prog(t, tm, 0.32); jx, jy, jr = jit('t1', t, 1.5, 0.4)
        place(c, qtag('MULTIBAGGER?', GRN), 540 + jx, 1170 + jy, 0.55 + 0.45 * eback(p), -3 + jr, clamp(p * 3))
    tt = at(i, 'trap', -0.2)
    if t > tt:
        sc, a2 = slam(t, tt); place(c, qtag('OR TRAP?', RED), 540, 1360, sc, 3, a2)
        marker_ellipse(c, 540, 1360, 250, 90, prog(t, tt + 0.35, 0.5), INK, 8, seed=5)


def s2(c, t):
    i = 1; T0 = STARTS[i]
    tl = at(i, 'listed', -0.2)
    if t > T0 + 0.1:
        place(c, text_img('JAN 2021 · IPO', 'anton', 120, INK), 540, 300, pp(t, T0 + 0.1))
        place_text(c, 'issue price ₹26', 'mark', 56, RED, 540, 410, t, 'ipo', tl, 'slide', rot=-3)
    p = prog(t, at(i, 'twenty six', -0.4), 0.45)
    if p > 0:
        ox, oy = 60, 500 + (1 - eo(p)) * 600; w, h = 960, 820
        place(c, sheet_cut(w, h), ox + w / 2, oy + h / 2, 1.0, 0, clamp(p * 3))
        vals = [26, 22, 20, 30, 70, 155, 190, 229]
        labs = ['2021', '', '2022', '', '2023', '', '', 'JUL 24']
        t1 = at(i, 'By July', -0.3); t2 = at(i, 'two hundred', 0.6)
        f = clamp((t - t1) / max(0.1, t2 - t1))
        place(c, text_img('₹26', 'anton', 64, INK), ox + 170, oy + h - 170, pp(t, at(i, 'twenty six', -0.2)))
        if t > t1:
            tip = hand_chart(c, t, ox, oy, w, h, vals, labs, 0, 250, eio(f), INK, (150, 220, 170))
            if t > t2 - 0.3 and tip:
                tg = text_img('₹229', 'anton', 76, GRN); c.alpha_composite(tg, (int(tip[0] - 200), int(tip[1] - 40)))
        tn = at(i, 'Almost nine', -0.2)
        if t > tn:
            sc, a = slam(t, tn); place(c, stamp_c('~9x', GRN, 130, -8, 21), ox + 330, oy + 260, sc, 0, a)
    src(c, t, 'Line simplified · IPO ₹26 (Jan 2021) · high ₹229 (Jul 2024)', T0 + 1.0, 1440)


MONTHLY = [117.57, 124.62, 120.1, 103.55, 87.23, 104.21, 97.51, 90.53, 89.15, 83.34, 79.28, 73.37, 81.1]
MLAB = ['NOV 25', '', '', 'FEB', '', '', 'MAY', '', '', 'AUG', '', '', 'NOV 26']


def s3(c, t):
    i = 2; T0 = STARTS[i]
    jx, jy, jr = jit('cnt', t, 1.2, 0.3)
    if t > T0 + 0.1:
        v = 229 - (229 - 81.1) * eo(prog(t, T0 + 0.2, 1.4))
        place(c, text_img(f'₹{v:.2f}', 'anton', 190, RED if v < 150 else INK), 540 + jx, 320 + jy, 1.0, jr)
        typed(c, 'IRFC · 18 NOV 2026', 'type', 32, GREY, 450, t, T0 + 0.2, T0 + 1.0)
    p = prog(t, T0 + 0.4, 0.45)
    if p > 0:
        ox, oy = 60, 520 + (1 - eo(p)) * 600; w, h = 960, 640
        place(c, sheet_cut(w, h), ox + w / 2, oy + h / 2, 1.0, 0, clamp(p * 3))
        f = eio(prog(t, T0 + 0.8, 2.2))
        hand_chart(c, t, ox, oy, w, h, MONTHLY, MLAB, 65, 135, f, INK, YEL)
        th = T0 + 2.4
        if t > th:
            x = ox + 90 + (w - 160) * 1 / 12; y = oy + h - 70 - (124.62 - 65) / 70 * (h - 140)
            marker_ellipse(c, x, y, 70, 46, prog(t, th, 0.45), RED, 7, seed=8)
            place_text(c, '52-wk high ₹137', 'mark', 44, RED, x + 250, y - 20, t, 'hi', th + 0.2, 'slide', rot=-4)
        tf = at(i, 'Sixty five', -0.3)
        if t > tf:
            sc, a = slam(t, tf); place(c, stamp_c('-65%', RED, 96, 8, 31), ox + 800, oy - 40, sc, 0, a)
            place(c, text_img('from the ₹229 top', 'osw5', 40, RED), ox + 800, oy + 50, pp(t, tf + 0.3))
    tw = at(i, 'So what', -0.2)
    if t > tw:
        place_text(c, 'so what does it actually do?', 'pfi', 64, INK, 540, 1290, t, 'sw', tw, 'pop')
    src(c, t, 'Monthly close · NSE via INDmoney · 18 Nov 2026', T0 + 1.0, 1400)


def s4(c, t):
    i = 3; T0 = STARTS[i]
    words_line(c, t, [("RAILWAYS'", INK, T0 + 0.1), ("MONEY ARM", NAVY, T0 + 0.35)], 'anton', 100, 300, key='rm')
    if t > T0 + 0.4:
        rails(c, 560)
        x = 120 + 520 * eo(prog(t, T0 + 0.4, 2.5)) + 30 * (t - T0)
        train(c, x, 560, 0.8, 2, NAVY, INK, t)
    steps = [('1', 'BORROWS', 'bonds & loans from the market', 'borrows', BLUE),
             ('2', 'PAYS FOR', 'trains, coaches, wagons, projects', 'pays for', ORG),
             ('3', '30-YEAR LEASE', 'to Indian Railways', 'leases', GRN)]
    for k, (n, tt_, sub, ph, col) in enumerate(steps):
        tk = at(i, ph, -0.3); pk = prog(t, tk, 0.45)
        if pk <= 0: continue
        jx, jy, jr = jit(('tk', k), t, 1.4, 0.25)
        place(c, step_ticket(n, tt_, sub, col), 540 + (1 - eo(pk)) * 900 + jx, 760 + k * 190 + jy, 0.95, (-1.2, 1.0, -0.6)[k] + jr)
        if k < 2 and t > tk + 0.5:
            marker_line(c, [(140, 830 + k * 190), (125, 860 + k * 190), (140, 890 + k * 190)], prog(t, tk + 0.5, 0.3), RED, 7, head=True, head_size=18)
    src(c, t, 'IRFC leasing model: irfc.co.in · lease period typically 30 years', T0 + 1.0, 1400)


def s5(c, t):
    i = 4; T0 = STARTS[i]
    if t > T0 + 0.1:
        hw = text_w('COST + MARGIN', 'anton', 110)
        highlight(c, 540 - hw / 2 - 16, 262, 540 + hw / 2 + 16, 350, prog(t, at(i, 'small fixed', -0.2), 0.4), seed=41, alpha=200)
        place(c, text_img('COST + MARGIN', 'anton', 110, INK), 540, 300, pp(t, T0 + 0.1))
    tb = at(i, 'no bad', -0.3)
    if t > tb:
        sc, a = slam(t, tb); place(c, stamp_c('0 BAD LOANS', GRN, 90, -5, 51), 540, 470, sc, 0, a)
    tl = at(i, 'four point', -0.4)
    if t > tl:
        v = 4.8 * eo(prog(t, tl, 1.0))
        place(c, text_img(f'₹{v:.1f} LAKH CR', 'anton', 120, NAVY), 540, 680)
        place_text(c, 'lent out (AUM, June 2026)', 'mark', 50, INK, 540, 790, t, 'aum', tl + 0.4, 'slide', rot=-3)
    tn = at(i, 'over ninety', -0.4)
    if t > tn:
        d = ImageDraw.Draw(c); f = eo(prog(t, tn, 1.0))
        x0, y0, x1, y1 = 120, 900, 960, 1010
        d.rounded_rectangle((x0, y0, x1, y1), 30, fill=(230, 224, 210), outline=INK, width=5)
        xr = x0 + (x1 - x0) * 0.9243 * f
        d.rounded_rectangle((x0, y0, max(x0 + 60, xr), y1), 30, fill=NAVY, outline=INK, width=5)
        if f > 0.5:
            c.alpha_composite(text_img(f'RAILWAYS {92.4 * f:.0f}%', 'anton', 58, CREAM), (x0 + 30, y0 + 22))
        place(c, text_img('others', 'type', 26, GREY, 1), 900, 1050, pp(t, tn + 0.9))
    src(c, t, 'irfc.co.in · AUM ₹4.79 lakh cr, 92.43% Railways (Q1 FY27 deck)', T0 + 1.0, 1400)


def s6(c, t):
    i = 5; T0 = STARTS[i]
    dy, a = drop(t, T0 + 0.05, 300)
    if a > 0:
        hp = round(prog(t, T0 + 0.6, 0.5) * 20) / 20
        place(c, clipping(hp, 'LATEST RESULT', 'Q2 FY27 · 15 OCT 2026', 'IRFC · JUL-SEP 2026'), 540, 380 + dy, 0.82, -2, a)
    pr = prog(t, at(i, 'Revenue', -0.4), 0.45)
    if pr <= 0: return
    rc = receipt(); rx0, ry0 = 130, 700 + (1 - eo(pr)) * 700
    place(c, rc, rx0 + rc.size[0] / 2 - (rc.size[0] - 820) / 2 + 3, ry0 + rc.size[1] / 2 - (rc.size[1] - 720) / 2 + 7, 1.0, 0, clamp(pr * 3))
    def row(t0, y, lab, sub, amt, col, hl=None):
        q = prog(t, t0, 0.3)
        if q <= 0: return
        dx = (1 - eo(q)) * 40; a_ = clamp(q * 3)
        if hl is not None: highlight(c, rx0 + 40, ry0 + y - 46, rx0 + 780, ry0 + y + 46, prog(t, hl, 0.45), seed=21)
        li = text_img(lab, 'osw5', 50, INK); place(c, li, rx0 + 60 + li.size[0] / 2 + dx, ry0 + y - 14, 1, 0, a_)
        si = text_img(sub, 'type', 26, GREY, 1); place(c, si, rx0 + 60 + si.size[0] / 2 + dx, ry0 + y + 34, 1, 0, a_)
        ai = text_img(amt, 'anton', 80, col); place(c, ai, rx0 + 770 - ai.size[0] / 2 - dx, ry0 + y, 1, 0, a_)
    row(at(i, 'Revenue', 0.1), 120, 'Revenue', '₹7,866 Cr vs ₹6,372 Cr', '+23%', GRN)
    row(at(i, 'Profit up', -0.2), 320, 'Profit', '₹1,958 Cr vs ₹1,777 Cr', '+10%', GRN, hl=at(i, 'one thousand', 0.2))
    row(at(i, 'dividend', -0.2), 520, 'Dividend', 'interim, per share', '₹1.15', TEAL)
    src(c, t, 'IRFC Q2 FY27 results, 15 Oct 2026 (standalone) · PSU Connect, Lapaas Voice', T0 + 1.0, 1520)


def s7(c, t):
    i = 6; T0 = STARTS[i]
    words_line(c, t, [("THE", INK, T0 + 0.05), ("CATCH", RED, T0 + 0.25)], 'anton', 130, 300, key='bp')
    ti = at(i, 'Interest costs', -0.3)
    if t > ti:
        d = ImageDraw.Draw(c); base = 820
        c.alpha_composite(text_img('Q2 FY27 vs a year ago', 'type', 28, GREY, 2), (360, 900))
        for k, (lab, v, col) in enumerate((('REVENUE', 23.5, GRN), ('INTEREST COST', 30.2, RED))):
            ph = eo(prog(t, ti + 0.25 * k, 0.7)); hg = int(v / 30.2 * 300 * ph); x = 330 + k * 420
            d.rounded_rectangle((x - 100, base - hg, x + 100, base), 14, fill=col, outline=INK, width=5)
            place(c, text_img(f'+{v * ph:.1f}%', 'anton', 60, INK), x, base - hg - 40)
            place(c, text_img(lab, 'osw5', 34, INK), x, base + 34)
        if t > ti + 1.0:
            marker_line(c, curve((480, 560), (580, 470), (680, 500)), prog(t, ti + 1.0, 0.4), RED, 7, head=True, head_size=20)
            place_text(c, 'margin squeeze', 'mark', 46, RED, 560, 400, t, 'ms', ti + 1.1, 'slide', rot=-5)
    tg = at(i, 'government keeps', -0.3)
    if t > tg:
        q = pp(t, tg, 0.35, 1.3)
        place(c, cutout(Image.new('RGBA', (900, 300), SOFT + (255,)), border=0, shadow=0.3), 540, 1110, q, 1)
        if q > 0.6:
            c.alpha_composite(text_img('GOVERNMENT STAKE', 'type', 28, GREY, 2), (120, 980))
            v = 86.36 - (86.36 - 82.90) * eo(prog(t, tg + 0.3, 1.2))
            c.alpha_composite(text_img(f'86.36% to {v:.2f}%', 'anton', 72, INK), (120, 1020))
            c.alpha_composite(text_img('OFS: Feb 2026 at ₹104 · Jun 2026 at ₹91', 'osw5', 36, NAVY), (120, 1120))
    tb = at(i, 'Both sales', -0.3)
    if t > tb:
        sc, a = slam(t, tb); place(c, stamp_c('PRICE DIPPED', RED, 64, -6, 61), 760, 1310, sc, 0, a)
    src(c, t, 'Q2 FY27 results · stake: Feb, Jun & Sep 2026 filings', T0 + 1.0, 1440)


def s8(c, t):
    i = 7; T0 = STARTS[i]
    if t > T0 + 0.1:
        p = prog(t, T0 + 0.1, 0.3); lw = text_w('THE VERDICT', 'osw', 54, 2); x0 = 540 - (lw + 70) / 2
        place(c, warn_icon(YEL), x0 + 28, 262, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
        place(c, text_img('THE VERDICT', 'osw', 54, YEL, 2), x0 + 70 + lw / 2, 260, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
    tn = at(i, 'Neither', -0.2)
    words_line(c, t, [("NEITHER,", CREAM, tn), ("FOR NOW.", RED, tn + 0.35)], 'anton', 130, 420, key='ny')
    rows = [('Priced like a rocket', 'valued at ~₹3 lakh cr at the ₹229 top', 'priced like', RED, False),
            ('Runs like a train', 'cost-plus · Railways client', 'runs like', GRN, True),
            ('Safe and steady', 'profit +10% · 0 bad loans', 'Safe', GRN, True),
            ('But slow', 'interest cost rising faster', 'slow', RED, False)]
    for k, (h1, h2, ph, col, ok) in enumerate(rows):
        tk = at(i, ph, -0.3)
        if t < tk: continue
        y = 640 + k * 200; q = pp(t, tk, 0.35, 1.3)
        jx, jy, jr = jit(('v', k), t, 1.2, 0.2)
        place(c, cutout(Image.new('RGBA', (900, 160), (40, 38, 36, 255)), border=6, shadow=0.4, bcol=col), 540 + jx, y + jy, q, (-0.8, 0.8, -0.6, 0.6)[k] + jr)
        if q < 0.6: continue
        d = ImageDraw.Draw(c); bx, by = 150, y
        if ok: d.line((bx - 22, by + 2, bx - 6, by + 20, bx + 24, by - 18), fill=col, width=10, joint='curve')
        else: d.line((bx - 18, by - 18, bx + 18, by + 18), fill=col, width=10); d.line((bx - 18, by + 18, bx + 18, by - 18), fill=col, width=10)
        c.alpha_composite(text_img(h1, 'anton', 56, CREAM), (210, int(y - 58)))
        c.alpha_composite(text_img(h2, 'type', 28, (200, 194, 182), 1), (214, int(y + 18)))
    if t > at(i, 'slow', 0.6):
        place_text(c, 'watch: margins + govt stake sales', 'mark', 48, YEL, 540, 1500, t, 'w2', at(i, 'slow', 0.6), 'slide', rot=-3)
    typed(c, 'Not investment advice. DYOR.', 'type', 30, (200, 194, 182), 1620, t, at(i, 'slow', 1.0), at(i, 'slow', 2.0))


def s9(c, t):
    i = 8; T0 = STARTS[i]
    q = pp(t, T0, 0.45, 1.2)
    place(c, SS._card(960, 860), 540, 600, q, -0.4)
    if q > 0.6:
        place(c, text_img('IRFC · CHEAT SHEET', 'anton', 56, INK), 540, 230)
        d = ImageDraw.Draw(c); d.line((90, 272, 990, 272), fill=INK, width=4)
        rows = [('Price (18 Nov)', '₹81.10', INK), ('From ₹229 top', '-65%', RED), ('IPO price (2021)', '₹26', INK), ('Q2 revenue', '+23%', GRN),
                ('Q2 profit', '+10%', GRN), ('Interest cost', '+30%', RED), ('Govt stake', '82.9%', NAVY), ('Market cap', '₹1.08 lakh cr', INK)]
        for k, (a_, b_, col) in enumerate(rows):
            tk = T0 + 0.3 + 0.08 * k
            if t < tk: continue
            y = 300 + k * 78
            c.alpha_composite(text_img(a_, 'osw5', 38, INK), (100, y))
            v = text_img(b_, 'anton', 44, col); c.alpha_composite(v, (980 - v.size[0], y - 2))
        SS.save_pulse(c, t, T0 + 1.2, 540, 1080, 'SAVE THIS')
    SS.send_frame(c, t, at(i, 'send it', -0.3), 'your friend who holds IRFC', y=1300)
    tf = at(i, 'Follow', -0.2)
    if t > tf:
        q2 = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1530, 0.5 + 0.5 * eback(q2), 0, clamp(q2 * 3))
    for k, ln in enumerate(['Price: NSE via INDmoney, 18 Nov 2026', 'Results: IRFC Q2 FY27 (15 Oct 2026) · stake: Sep 2026 filing',
                            'Not a buy/sell call. Education only. I may hold some stocks named.']):
        place_text(c, ln, 'type', 22, GREY, 540, 1680 + k * 34, t, None, T0 + 0.3, 'fade', track=1)


def pp(t, t0, d=0.35, s=1.6): return eback(prog(t, t0, d), s)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
DARK_SCENES = {7}


def slam_times():
    return [at(0, 'trap', -0.2), at(1, 'Almost nine', -0.2), at(2, 'Sixty five', -0.3), at(6, 'Both sales', -0.3)] + [STARTS[k] + 0.05 for k in range(1, 8)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('MULTIBAGGER OR TRAP?', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
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
