"""IREDA: multibagger or trap? PCJ-style paper collage (female VO)"""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs, typed, drop, warn_icon, receipt
from fridge import follow_btn
import saveshare as SS
import defence as DF

SH = ROOT + _os.environ.get('LDIR', 'ireda') + '/'
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


# ---------------- scenes ----------------
def s1(c, t):
    i = 0
    words_line(c, t, [("NOBODY", INK, 0.05), ("TELLS", INK, 0.2), ("YOU", RED, 0.35)], 'anton', 112, 270, key='h1')
    dy, a = drop(t, 0.3, 360)
    if a > 0:
        hp = round(prog(t, 1.0, 0.5) * 20) / 20
        jx, jy, jr = jit('clip', t, 2, 0.5)
        place(c, clipping(hp, 'IREDA', 'THE MARKET PAGE', 'GREEN ENERGY LENDER · NSE: IREDA'), 540 + jx, 590 + dy + jy, 1.0, -3 + jr + (1 - a) * 8, a)
    tf = at(i, 'fell', -0.25)
    if t > tf:
        sc, a2 = slam(t, tf); place(c, stamp_c('STOCK -57%', RED, 76, -6, 11), 290, 860, sc, 0, a2)
        place(c, text_img('from ₹310 top', 'osw5', 34, RED), 290, 965, pp(t, tf + 0.3))
    tn = at(i, 'new loans', -0.2)
    if t > tn:
        sc, a2 = slam(t, tn); place(c, stamp_c('NEW LOANS +31%', GRN, 62, 5, 12), 740, 1010, sc, 0, a2)
        place(c, text_img('Q2 FY27 vs Q2 FY26', 'osw5', 30, GRN), 740, 1105, pp(t, tn + 0.3))
    tm = at(i, 'Multibagger', -0.25)
    if t > tm:
        p = prog(t, tm, 0.32); jx, jy, jr = jit('t1', t, 1.5, 0.4)
        place(c, qtag('MULTIBAGGER?', GRN), 540 + jx, 1230 + jy, 0.55 + 0.45 * eback(p), -3 + jr, clamp(p * 3))
    tt = at(i, 'trap', -0.2)
    if t > tt:
        sc, a2 = slam(t, tt); place(c, qtag('OR TRAP?', RED), 540, 1410, sc, 3, a2)
        marker_ellipse(c, 540, 1410, 250, 90, prog(t, tt + 0.35, 0.5), INK, 8, seed=5)
    src(c, t, 'NSE price via INDmoney (23 Nov 2026) · IREDA Q2 FY27 update', 1.2, 1550)


def s2(c, t):
    i = 1; T0 = STARTS[i]
    tl = at(i, 'issue price', -0.2)
    if t > T0 + 0.1:
        place(c, text_img('NOV 2023 · IPO', 'anton', 120, INK), 540, 300, pp(t, T0 + 0.1))
        place_text(c, 'issue price ₹32', 'mark', 56, RED, 540, 410, t, 'ipo', tl, 'slide', rot=-3)
    p = prog(t, at(i, 'thirty two', -0.4), 0.45)
    if p > 0:
        ox, oy = 60, 500 + (1 - eo(p)) * 600; w, h = 960, 820
        place(c, sheet_cut(w, h), ox + w / 2, oy + h / 2, 1.0, 0, clamp(p * 3))
        vals = [32, 60, 310]
        labs = ['NOV 23 IPO', 'DAY 1', 'JUL 24']
        t1 = at(i, 'By July', -0.3); t2 = at(i, 'three hundred', 0.6)
        f = clamp((t - t1) / max(0.1, t2 - t1))
        place(c, text_img('₹32', 'anton', 64, INK), ox + 170, oy + h - 170, pp(t, at(i, 'thirty two', -0.2)))
        if t > t1:
            tip = hand_chart(c, t, ox, oy, w, h, vals, labs, 0, 330, eio(f), INK, (150, 220, 170))
            if t > t2 - 0.3 and tip:
                tg = text_img('₹310', 'anton', 76, GRN); c.alpha_composite(tg, (int(tip[0] - 210), int(tip[1] - 30)))
        tn = at(i, 'Almost ten', -0.2)
        if t > tn:
            sc, a = slam(t, tn); place(c, stamp_c('~9.7x', GRN, 120, -8, 21), ox + 330, oy + 260, sc, 0, a)
            place(c, text_img('in 8 months', 'osw5', 40, GRN), ox + 330, oy + 395, pp(t, tn + 0.3))
    src(c, t, 'Line simplified, 3 real points · IPO ₹32, day-1 close ₹60 (29 Nov 2023, 5paisa)', T0 + 1.0, 1400)
    src(c, t, 'record high ₹310 intraday (15 Jul 2024, Business Standard)', T0 + 1.0, 1440)


MONTHLY = [142.9, 139.9, 132.08, 122.25, 108.98, 135.1, 133.25, 128.69, 119.59, 116.5, 111.68, 99.5, 132.2]
MLAB = ['NOV 25', '', '', 'FEB', '', '', 'MAY', '', '', 'AUG', '', '', 'NOV 26']


def s3(c, t):
    i = 2; T0 = STARTS[i]
    jx, jy, jr = jit('cnt', t, 1.2, 0.3)
    if t > T0 + 0.1:
        v = 310 - (310 - 132.2) * eo(prog(t, T0 + 0.2, 1.4))
        place(c, text_img(f'₹{v:.2f}', 'anton', 190, RED if v < 200 else INK), 540 + jx, 320 + jy, 1.0, jr)
        typed(c, 'IREDA · NSE CLOSE 23 NOV 2026', 'type', 32, GREY, 450, t, T0 + 0.2, T0 + 1.0)
    p = prog(t, T0 + 0.4, 0.45)
    if p > 0:
        ox, oy = 60, 520 + (1 - eo(p)) * 600; w, h = 960, 640
        place(c, sheet_cut(w, h), ox + w / 2, oy + h / 2, 1.0, 0, clamp(p * 3))
        f = eio(prog(t, T0 + 0.8, 2.2))
        hand_chart(c, t, ox, oy, w, h, MONTHLY, MLAB, 90, 155, f, INK, YEL)
        th = T0 + 2.4
        if t > th:
            x = ox + 90 + (w - 160) * 11 / 12; y = oy + h - 70 - (99.5 - 90) / 65 * (h - 140)
            marker_ellipse(c, x, y, 60, 42, prog(t, th, 0.45), RED, 7, seed=8)
            place_text(c, '52-wk low ₹98.78 (Oct)', 'mark', 42, RED, x - 300, y - 30, t, 'lo', th + 0.2, 'slide', rot=-4)
        tf = at(i, 'Fifty seven', -0.3)
        if t > tf:
            sc, a = slam(t, tf); place(c, stamp_c('-57%', RED, 96, -6, 31), 300, 1250, sc, 0, a)
            place(c, text_img('from the ₹310 top', 'osw5', 44, RED), 720, 1250, pp(t, tf + 0.3))
    tw = at(i, 'So what', -0.2)
    if t > tw:
        place_text(c, 'so what does it actually do?', 'pfi', 64, INK, 540, 1380, t, 'sw', tw, 'pop')
    src(c, t, 'Monthly close, Nov 2025 to Nov 2026 · NSE via INDmoney', T0 + 1.0, 1470)


def s4(c, t):
    i = 3; T0 = STARTS[i]
    words_line(c, t, [("GREEN", GRN, T0 + 0.1), ("ENERGY", GRN, T0 + 0.3), ("LENDER", INK, T0 + 0.5)], 'anton', 100, 290, key='gl')
    if t > T0 + 0.4:
        q = eo(prog(t, T0 + 0.4, 0.6))
        sun(c, 230, 520, 0.9 * q + 0.01, t)
        turbine(c, 820, 430, 0.55 * q + 0.01, t, INK, 0.9)
        panel(c, 530, 600, 1.0 * q + 0.01, NAVY)
        place(c, text_img('owned by Govt of India', 'mark', 44, NAVY), 540, 700, pp(t, T0 + 0.8))
    steps = [('1', 'BORROWS', 'bonds and bank loans', 'borrows', BLUE),
             ('2', 'LENDS', 'solar, wind and clean power projects', 'lends to', GRN),
             ('3', 'EARNS THE GAP', 'interest in minus interest out', 'projects', ORG)]
    for k, (n, tt_, sub, ph, col) in enumerate(steps):
        tk = at(i, ph, -0.3) + (0.3 if k == 2 else 0); pk = prog(t, tk, 0.45)
        if pk <= 0: continue
        jx, jy, jr = jit(('tk', k), t, 1.4, 0.25)
        place(c, step_ticket(n, tt_, sub, col), 540 + (1 - eo(pk)) * 900 + jx, 830 + k * 180 + jy, 0.95, (-1.2, 1.0, -0.6)[k] + jr)
    tw = at(i, 'twist', -0.3)
    if t > tw:
        sc, a = slam(t, tw); place(c, stamp_c('THE TWIST: BUSINESS KEPT GROWING', RED, 52, -4, 41), 540, 1370, sc, 0, a)
    src(c, t, 'ireda.in · Mini Ratna PSU under the Ministry of New and Renewable Energy', T0 + 1.0, 1480)


def s5(c, t):
    i = 4; T0 = STARTS[i]
    dy, a = drop(t, T0 + 0.05, 300)
    if a > 0:
        hp = round(prog(t, T0 + 0.6, 0.5) * 20) / 20
        place(c, clipping(hp, 'LATEST QUARTER', 'Q2 FY27 · 19 OCT 2026', 'IREDA · JUL-SEP 2026'), 540, 380 + dy, 0.82, -2, a)
    pr = prog(t, at(i, 'Income', -0.4), 0.45)
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
    row(at(i, 'Income', 0.1), 120, 'Total income', '₹2,345 Cr vs ₹2,057 Cr', '+14%', GRN)
    row(at(i, 'New loans', -0.2), 320, 'New loans', 'disbursed ₹10,579 Cr vs ₹8,062 Cr', '+31%', GRN, hl=at(i, 'thirty one', 0.2))
    row(at(i, 'Net bad', -0.2), 520, 'Net NPA', 'down from 1.97% a year ago', '1.08%', GRN)
    src(c, t, 'IREDA Q2 FY27 results (19 Oct 2026) · Indian Masterminds, Kotak Neo', T0 + 1.0, 1520)


def s6(c, t):
    i = 5; T0 = STARTS[i]
    words_line(c, t, [("THE", INK, T0 + 0.05), ("CATCH", RED, T0 + 0.25)], 'anton', 130, 290, key='bp')
    d = ImageDraw.Draw(c); base = 1000
    bars = [('PROFIT', 1.0, '+1%', GRN, at(i, 'profit grew', -0.2)),
            ('INTEREST COST', 13.5, '+13%', RED, at(i, 'Interest costs', -0.2)),
            ('BAD-LOAN PROVISIONS', 167, '2.7x', RED, at(i, 'provisions', -0.2))]
    for k, (lab, v, txt, col, tk) in enumerate(bars):
        if t < tk: continue
        ph = eo(prog(t, tk, 0.7)); hg = int(max(14, min(v, 60) / 60 * 520) * ph); x = 220 + k * 320
        if k == 2: hg = int(560 * ph)
        d.rounded_rectangle((x - 105, base - hg, x + 105, base), 14, fill=col, outline=INK, width=5)
        place(c, text_img(txt, 'anton', 72, INK), x, base - hg - 50)
        lb = text_img(lab, 'osw5', 30 if k < 2 else 26, INK); place(c, lb, x, base + 34)
    if t > at(i, 'profit grew', -0.2):
        c.alpha_composite(text_img('Q2 FY27 vs Q2 FY26', 'type', 28, GREY, 2), (380, 380))
        place(c, text_img('PAT ₹554 Cr vs ₹549 Cr', 'osw5', 34, GRN), 220, 1120, pp(t, at(i, 'profit grew', 0.3)))
    if t > at(i, 'Interest costs', 0.2):
        place(c, text_img('₹1,376 Cr vs ₹1,213 Cr', 'osw5', 34, RED), 540, 1170, pp(t, at(i, 'Interest costs', 0.2)))
    tp = at(i, 'provisions', 0.2)
    if t > tp:
        place(c, text_img('₹187 Cr vs ₹70 Cr', 'osw5', 34, RED), 860, 1120, pp(t, tp))
        sc, a = slam(t, tp + 0.4); place(c, stamp_c('MARGIN SQUEEZE', RED, 64, -6, 61), 540, 1310, sc, 0, a)
    src(c, t, 'IREDA Q2 FY27 results (19 Oct 2026) · Indian Masterminds, INDmoney', T0 + 1.0, 1440)


def s7(c, t):
    i = 6; T0 = STARTS[i]
    words_line(c, t, [("MORE", INK, T0 + 0.05), ("RISKS", RED, T0 + 0.25)], 'anton', 120, 290, key='mr')
    cards = [('FRAUD-TAGGED LOANS', '₹673 CR', 'disclosed exposure linked to Gensol', RED, 'Six hundred'),
             ('GOVT STAKE AFTER QIP (JUN 2025)', '75% TO 71.76%', 'new shares issued, floor ₹173.83', NAVY, 'Q I P'),
             ('PRICE vs BOOK VALUE', '2.6x BOOK', 'book value ₹51 a share', ORG, 'two and a half')]
    for k, (a_, b_, s_, col, ph) in enumerate(cards):
        tk = at(i, ph, -0.3); pk = prog(t, tk, 0.45)
        if pk <= 0: continue
        jx, jy, jr = jit(('rc', k), t, 1.2, 0.2)
        place(c, risk_card(a_, b_, s_, col), 540 + (1 - eo(pk)) * (900 if k % 2 == 0 else -900) + jx, 520 + k * 290 + jy, 0.98, (-1.0, 1.0, -0.6)[k] + jr)
    if t > at(i, 'Gensol', 0.4):
        marker_ellipse(c, 260, 512, 150, 50, prog(t, at(i, 'Gensol', 0.4), 0.45), RED, 7, seed=9)
    src(c, t, 'Fraud exposure: INDmoney (21 Oct 2026) · stake: Screener, Sep 2026 pattern', T0 + 1.0, 1400)
    src(c, t, 'QIP: Business Standard (6 Jun 2025) · book value: Screener (23 Nov 2026)', T0 + 1.0, 1440)


def s8(c, t):
    i = 7; T0 = STARTS[i]
    if t > T0 + 0.1:
        p = prog(t, T0 + 0.1, 0.3); lw = text_w('THE VERDICT', 'osw', 54, 2); x0 = 540 - (lw + 70) / 2
        place(c, warn_icon(YEL), x0 + 28, 262, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
        place(c, text_img('THE VERDICT', 'osw', 54, YEL, 2), x0 + 70 + lw / 2, 260, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
    tn = at(i, 'Neither', -0.2)
    words_line(c, t, [("NEITHER,", CREAM, tn), ("FOR NOW.", RED, tn + 0.35)], 'anton', 130, 420, key='ny')
    rows = [('Price ran ahead', '₹310 top = about 9.7x the IPO price', 'ran far', RED, False),
            ('Lending grows fast', 'new loans +31% · net NPA 1.08%', 'lending grows', GRN, True),
            ('Profit lags', 'Q2 profit +1% only', "profit doesn't", RED, False),
            ('Watch these', 'bad loans + borrowing costs', 'Watch', YEL, True)]
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
    typed(c, 'No prediction. Not a buy/sell call.', 'type', 30, (200, 194, 182), 1520, t, at(i, 'Watch', 0.8), at(i, 'Watch', 1.8))


def s9(c, t):
    i = 8; T0 = STARTS[i]
    q = pp(t, T0, 0.45, 1.2)
    place(c, SS._card(960, 860), 540, 600, q, -0.4)
    if q > 0.6:
        place(c, text_img('IREDA · CHEAT SHEET', 'anton', 56, INK), 540, 230)
        d = ImageDraw.Draw(c); d.line((90, 272, 990, 272), fill=INK, width=4)
        rows = [('IPO price (Nov 2023)', '₹32', INK), ('Record high (Jul 2024)', '₹310', GRN), ('Price (23 Nov 2026)', '₹132.20', INK),
                ('From the top', '-57%', RED), ('Q2 new loans', '+31%', GRN), ('Q2 profit', '+1%', RED),
                ('Net NPA', '1.08%', GRN), ('Govt stake / P/B', '71.76% / 2.6x', NAVY)]
        for k, (a_, b_, col) in enumerate(rows):
            tk = T0 + 0.3 + 0.08 * k
            if t < tk: continue
            y = 300 + k * 78
            c.alpha_composite(text_img(a_, 'osw5', 38, INK), (100, y))
            v = text_img(b_, 'anton', 44, col); c.alpha_composite(v, (980 - v.size[0], y - 2))
        SS.save_pulse(c, t, T0 + 1.2, 540, 1080, 'SAVE THIS')
    SS.send_frame(c, t, at(i, 'send it', -0.3), 'the friend who bought IREDA', y=1300)
    tf = at(i, 'Follow', -0.2)
    if t > tf:
        q2 = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1530, 0.5 + 0.5 * eback(q2), 0, clamp(q2 * 3))
    for k, ln in enumerate(['Price: NSE via INDmoney, 23 Nov 2026 · IPO: 5paisa · high: Business Standard',
                            'Results: IREDA Q2 FY27 (19 Oct 2026) · stake, book value: Screener',
                            'Not a buy/sell call. Education only. I may hold some stocks named.']):
        place_text(c, ln, 'type', 22, GREY, 540, 1680 + k * 34, t, None, T0 + 0.3, 'fade', track=1)


def pp(t, t0, d=0.35, s=1.6): return eback(prog(t, t0, d), s)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
DARK_SCENES = {7}


def slam_times():
    return [at(0, 'fell', -0.25), at(0, 'trap', -0.2), at(1, 'Almost ten', -0.2), at(2, 'Fifty seven', -0.3), at(3, 'twist', -0.3), at(5, 'provisions', 0.6)] + [STARTS[k] + 0.05 for k in range(1, 8)]


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
