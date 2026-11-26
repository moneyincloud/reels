"""Paytm: multibagger or trap? PCJ/IRFC-style paper collage (female VO)"""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs, typed, drop, warn_icon, receipt
from fridge import follow_btn
import saveshare as SS
import defence as DF

SH = ROOT + _os.environ.get('LDIR', 'paytm') + '/'
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
def clipping(hp, head='PAYTM', top='THE MARKET PAGE', sub='FINTECH · NSE: PAYTM'):
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



ACC = (70, 160, 240)   # blue theme accent (thumbnail theme 'blue')


def counter_txt(v, dec=2):
    return f'₹{v:,.{dec}f}'


def price_tag(lab, val, col, sub):
    w, h = 820, 200
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 22, fill=(254, 252, 246))
    for y in range(12, h - 12, 18): d.ellipse((215, y, 225, y + 10), fill=(225, 218, 204))
    a = text_img(lab, 'osw5', 40, INK); im.alpha_composite(a, (110 - a.size[0] // 2, 60))
    s = text_img(sub, 'type', 22, GREY, 1); im.alpha_composite(s, (110 - s.size[0] // 2, 120))
    v = text_img(val, 'anton', 120, col); im.alpha_composite(v, (250, h // 2 - v.size[1] // 2))
    return cutout(im, border=10, shadow=0.4)


# ---------------- scenes ----------------
def s1(c, t):
    i = 0
    words_line(c, t, [("NEVER JUDGE", INK, 0.05), ("PAYTM", ACC, 0.3)], 'anton', 120, 270, key='h1')
    place_text(c, 'by its IPO', 'mark', 58, RED, 540, 370, t, 'byipo', at(i, 'by its', -0.2), 'slide', rot=-3)
    dy, a = drop(t, 0.05, 360)
    if a > 0:
        hp = round(prog(t, 0.6, 0.5) * 20) / 20
        jx, jy, jr = jit('clip', t, 2, 0.5)
        place(c, clipping(hp), 540 + jx, 640 + dy + jy, 0.9, -3 + jr + (1 - a) * 8, a)
    tc = at(i, 'crashed', -0.2)
    if t > tc:
        sc, a2 = slam(t, tc); place(c, stamp_c('-86%', RED, 120, -7, 3), 290, 950, sc, 0, a2)
        place(c, text_img('IPO to low', 'osw5', 40, RED), 290, 1110, pp(t, tc + 0.3))
    tr = at(i, 'rose five', -0.2)
    if t > tr:
        sc, a2 = slam(t, tr); place(c, stamp_c('5.7x', GRN, 120, 6, 4), 790, 950, sc, 0, a2)
        place(c, text_img('low to today', 'osw5', 40, GRN), 790, 1110, pp(t, tr + 0.3))
    tm = at(i, 'Multibagger', -0.25)
    if t > tm:
        p = prog(t, tm, 0.32); jx, jy, jr = jit('t1', t, 1.5, 0.4)
        place(c, qtag('MULTIBAGGER?', GRN), 540 + jx, 1250 + jy, 0.55 + 0.45 * eback(p), -3 + jr, clamp(p * 3))
    tt = at(i, 'trap', -0.2)
    if t > tt:
        sc, a2 = slam(t, tt); place(c, qtag('OR TRAP?', RED), 540, 1440, sc, 3, a2)
        marker_ellipse(c, 540, 1440, 250, 90, prog(t, tt + 0.35, 0.5), INK, 8, seed=5)


def s2(c, t):
    i = 1; T0 = STARTS[i]
    if t > T0 + 0.1:
        place(c, text_img('NOV 2021 · IPO', 'anton', 120, INK), 540, 300, pp(t, T0 + 0.1))
        place_text(c, 'listing day: 18 Nov 2021', 'mark', 50, ACC, 540, 405, t, 'hy', T0 + 0.5, 'slide', rot=-3)
    ti = at(i, 'I P O price', -0.2)
    if t > ti:
        q = pp(t, ti, 0.35, 1.3)
        place(c, price_tag('IPO', '₹2,150', INK, 'issue price'), 540 + (1 - clamp(q)) * 600, 600, 1.0, -1.5, clamp(q * 2))
    td = at(i, 'Day one', -0.2)
    if t > td:
        q = pp(t, td, 0.35, 1.3)
        v = 2150 - (2150 - 1564) * eo(prog(t, td + 0.2, 1.2))
        place(c, price_tag('DAY 1', f'₹{v:,.0f}', RED, 'close (BSE)'), 540 - (1 - clamp(q)) * 600, 860, 1.0, 1.2, clamp(q * 2))
        marker_line(c, curve((120, 650), (60, 760), (120, 860)), prog(t, td + 0.3, 0.4), RED, 8, head=True, head_size=22)
    tw = at(i, 'Down twenty', -0.2)
    if t > tw:
        sc, a = slam(t, tw); place(c, stamp_c('-27% ON DAY ONE', RED, 92, -5, 12), 540, 1120, sc, 0, a)
        place_text(c, 'about ₹38,000 cr of value gone in a day', 'mark', 46, INK, 540, 1260, t, 'w38', tw + 0.5, 'slide', rot=-2)
    src(c, t, 'Issue ₹2,150 · listing-day close ₹1,564 (BSE) · Business Standard, 18 Nov 2021', T0 + 1.0, 1420)


def s3(c, t):
    i = 2; T0 = STARTS[i]
    dy, a = drop(t, T0 + 0.05, 300)
    if a > 0:
        hp = round(prog(t, T0 + 0.6, 0.5) * 20) / 20
        place(c, clipping(hp, 'RBI ACTION', 'JAN 2024', 'PAYTM PAYMENTS BANK'), 540, 360 + dy, 0.8, -2, a)
    ts = at(i, 'stopped', -0.2)
    if t > ts:
        sc, a2 = slam(t, ts); place(c, stamp_c('NO NEW DEPOSITS', RED, 70, -6, 33), 700, 610, sc, 0, a2)
    p = prog(t, at(i, 'By May', -0.6), 0.45)
    if p > 0:
        ox, oy = 60, 740 + (1 - eo(p)) * 600; w, h = 960, 700
        place(c, sheet_cut(w, h), ox + w / 2, oy + h / 2, 1.0, 0, clamp(p * 3))
        f = eio(prog(t, at(i, 'By May', -0.1), 1.6))
        tip = hand_chart(c, t, ox, oy, w, h, [2150, 1564, 310], ['IPO NOV 21', 'DAY 1', 'LOW MAY 24'], 0, 2400, f, INK, (240, 190, 180))
        c.alpha_composite(text_img('₹2,150', 'anton', 56, INK), (ox + 110, int(oy + 50)))
        tl = at(i, 'three hundred', -0.1)
        if t > tl and tip:
            tg = text_img('₹310', 'anton', 80, RED); c.alpha_composite(tg, (int(tip[0] - 230), int(tip[1] - 110)))
            sc, a3 = slam(t, tl + 0.4); place(c, stamp_c('-86% FROM IPO', RED, 64, 6, 35), ox + 640, oy + 150, sc, 0, a3)
    src(c, t, 'Line joins 3 sourced points · low ₹310 intraday: Business Today, 9 May 2024', T0 + 1.0, 1500)


MONTHLY = [1320.6, 1298.9, 1137.5, 1098.3, 959.0, 1095.8, 1118.8, 1141.5, 1343.0, 1717.1, 1678.0, 1634.3, 1768.9]
MLAB = ['NOV 25', '', '', 'FEB', '', '', 'MAY', '', '', 'AUG', '', '', 'NOV 26']


def s4(c, t):
    i = 3; T0 = STARTS[i]
    jx, jy, jr = jit('cnt', t, 1.2, 0.3)
    if t > T0 + 0.1:
        v = 310 + (1768.9 - 310) * eo(prog(t, at(i, 'Today', -0.3), 1.6))
        place(c, text_img(counter_txt(v), 'anton', 170, GRN if v > 1000 else RED), 540 + jx, 310 + jy, 1.0, jr)
        typed(c, 'PAYTM · NSE · 26 NOV 2026, 3:50 PM', 'type', 30, GREY, 430, t, T0 + 0.2, T0 + 1.0)
    p = prog(t, T0 + 0.3, 0.45)
    if p > 0:
        ox, oy = 60, 500 + (1 - eo(p)) * 600; w, h = 960, 640
        place(c, sheet_cut(w, h), ox + w / 2, oy + h / 2, 1.0, 0, clamp(p * 3))
        f = eio(prog(t, T0 + 0.6, 2.4))
        hand_chart(c, t, ox, oy, w, h, MONTHLY, MLAB, 850, 2000, f, INK, (150, 220, 170))
        th = T0 + 1.6
        if t > th:
            x = ox + 90 + (w - 160) * 4 / 12; y = oy + h - 70 - (959 - 850) / 1150 * (h - 140)
            marker_ellipse(c, x, y, 70, 46, prog(t, th, 0.45), RED, 7, seed=8)
            place_text(c, '52-wk low ₹930.60', 'mark', 42, RED, x + 60, y - 230, t, 'lo', th + 0.2, 'slide', rot=-4)
        tf = at(i, 'Today', 0.6)
        if t > tf:
            sc, a = slam(t, tf); place(c, stamp_c('5.7x FROM ₹310', GRN, 80, -4, 31), 540, 1245, sc, 0, a)
    tw = at(i, 'So what', -0.2)
    if t > tw:
        place_text(c, 'so what changed?', 'pfi', 76, INK, 540, 1395, t, 'sw', tw, 'pop')
    src(c, t, 'Monthly close · NSE via INDmoney · 26 Nov 2026 · 5.7x = ₹1,768.90 / ₹310', T0 + 1.0, 1480)


def s5(c, t):
    i = 4; T0 = STARTS[i]
    dy, a = drop(t, T0 + 0.05, 300)
    if a > 0:
        hp = round(prog(t, T0 + 0.6, 0.5) * 20) / 20
        place(c, clipping(hp, 'LATEST RESULT', 'Q2 FY27 · 26 OCT 2026', 'PAYTM · JUL-SEP 2026'), 540, 380 + dy, 0.82, -2, a)
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
    row(at(i, 'Revenue', 0.1), 120, 'Revenue', '₹2,648 Cr vs ₹2,061 Cr', '+28%', GRN)
    row(at(i, 'Profit', -0.2), 320, 'Profit (PAT)', '₹225 Cr vs ₹21 Cr', '₹225 Cr', GRN, hl=at(i, 'twenty one', 0.0))
    row(at(i, 'year ago', 0.1), 520, 'EBITDA', '₹270 Cr, up 90% YoY', '+90%', TEAL)
    src(c, t, 'Q2 FY27 filing, 26 Oct 2026 · via Inc42, Free Press Journal', T0 + 1.0, 1520)


def s6(c, t):
    i = 5; T0 = STARTS[i]
    words_line(c, t, [("WHAT", INK, T0 + 0.05), ("CHANGED", ACC, T0 + 0.25)], 'anton', 120, 290, key='wc')
    tg = at(i, 'seven point', -0.4)
    if t > tg:
        v = 7.1 * eo(prog(t, tg, 1.0))
        place(c, text_img(f'₹{v:.1f} LAKH CR', 'anton', 120, NAVY), 540, 480)
        place_text(c, 'merchant payments (GMV), Jul-Sep 2026', 'mark', 44, INK, 540, 585, t, 'gmv', tg + 0.4, 'slide', rot=-2)
    tb = at(i, 'up twenty', -0.3)
    if t > tb:
        d = ImageDraw.Draw(c); base = 1260
        c.alpha_composite(text_img('Q2 FY27 vs a year ago', 'type', 28, GREY, 2), (330, base + 90))
        bars = (('GMV', 26, NAVY, tb), ('REVENUE', 28, GRN, tb + 0.3), ('FIN. SERVICES', 49, ACC, at(i, 'Financial', -0.2)))
        for k, (lab, v, col, t0) in enumerate(bars):
            if t < t0: continue
            ph = eo(prog(t, t0, 0.7)); hg = int(v / 49 * 380 * ph); x = 220 + k * 320
            d.rounded_rectangle((x - 100, base - hg, x + 100, base), 14, fill=col, outline=INK, width=5)
            place(c, text_img(f'+{v * ph:.0f}%', 'anton', 60, INK), x, base - hg - 40)
            place(c, text_img(lab, 'osw5', 32, INK), x, base + 34)
        tf = at(i, 'forty nine', 0.3)
        if t > tf:
            place_text(c, '₹912 Cr', 'mark', 52, RED, 860, 770, t, 'fs', tf, 'slide', rot=-5)
    src(c, t, 'Q2 FY27 vs Q2 FY26 · Inc42, Free Press Journal, 26-27 Oct 2026', T0 + 1.0, 1480)


DAILY = [1925.0, 1939.9, 1890.8, 1903.4, 1890.0, 1725.9, 1740.0, 1730.6, 1719.0, 1768.9]
DLAB = ['12 NOV', '', '', '', '18', '19', '', '', '', '26']


def s7(c, t):
    i = 6; T0 = STARTS[i]
    words_line(c, t, [("THE", INK, T0 + 0.05), ("CATCH", RED, T0 + 0.25)], 'anton', 130, 290, key='bp')
    p = prog(t, at(i, 'November', -0.4), 0.45)
    if p > 0:
        ox, oy = 60, 420 + (1 - eo(p)) * 600; w, h = 960, 560
        place(c, sheet_cut(w, h), ox + w / 2, oy + h / 2, 1.0, 0, clamp(p * 3))
        f = eio(prog(t, at(i, 'November', 0.0), 1.6))
        hand_chart(c, t, ox, oy, w, h, DAILY, DLAB, 1650, 1980, f, INK, YEL)
        tn = at(i, 'almost nine', -0.2)
        if t > tn:
            x = ox + 90 + (w - 160) * 5 / 9; y = oy + h - 70 - (1725.9 - 1650) / 330 * (h - 140)
            marker_ellipse(c, x, y, 60, 44, prog(t, tn, 0.45), RED, 7, seed=9)
            sc, a = slam(t, tn + 0.2); place(c, stamp_c('-8.7% IN A DAY', RED, 64, -5, 41), ox + 700, oy + 120, sc, 0, a)
    tr = at(i, 'report', -0.2)
    if t > tr:
        place_text(c, 'report: new UPI fee (MDR) may be delayed', 'mark', 46, INK, 540, 1050, t, 'rp', tr, 'slide', rot=-2)
    ta = at(i, 'And in April', -0.2)
    if t > ta:
        q = pp(t, ta, 0.35, 1.3)
        place(c, cutout(Image.new('RGBA', (900, 190), (40, 38, 36, 255)), border=6, shadow=0.4, bcol=RED), 540, 1230, q, -1)
        if q > 0.6:
            c.alpha_composite(text_img('APR 2026 · RBI CANCELS', 'anton', 56, CREAM), (130, 1150))
            c.alpha_composite(text_img('Paytm Payments Bank licence · stock -7.5% after', 'type', 28, (220, 214, 200), 1), (134, 1235))
    src(c, t, '19 Nov close ₹1,725.90 (-8.68%) · NSE via INDmoney', T0 + 1.0, 1400)
    src(c, t, 'Business Today 19 Nov & 27 Apr 2026 · RBI order 24 Apr 2026', T0 + 1.0, 1440)


def s8(c, t):
    i = 7; T0 = STARTS[i]
    if t > T0 + 0.1:
        p = prog(t, T0 + 0.1, 0.3); lw = text_w('THE VERDICT', 'osw', 54, 2); x0 = 540 - (lw + 70) / 2
        place(c, warn_icon(YEL), x0 + 28, 262, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
        place(c, text_img('THE VERDICT', 'osw', 54, YEL, 2), x0 + 70 + lw / 2, 260, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
    tb = at(i, 'Both', -0.2)
    if t > tb:
        sc, a = slam(t, tb); place(c, text_img('BOTH.', 'anton', 150, CREAM), 540, 410, sc, 0, a)
    td = at(i, 'depends', -0.2)
    if t > td:
        place_text(c, 'it depends on when you bought', 'mark', 52, YEL, 540, 530, t, 'dep', td, 'slide', rot=-2)
    rows = [('IPO buyer: -18%', '₹2,150 (2021) to ₹1,768.90 today', 'I P O buyers', RED, False),
            ('Low buyer: 5.7x', '₹310 (May 2024) to ₹1,768.90 today', 'Buyers at', GRN, True),
            ('Profitable now', '₹225 Cr profit, Jul-Sep 2026', 'five point seven', GRN, True),
            ('Next leg needs a fee', 'UPI MDR: not approved yet', 'next leg', RED, False)]
    for k, (h1, h2, ph, col, ok) in enumerate(rows):
        tk = at(i, ph, -0.3) + (0.9 if k == 2 else 0)
        if t < tk: continue
        y = 680 + k * 190; q = pp(t, tk, 0.35, 1.3)
        jx, jy, jr = jit(('v', k), t, 1.2, 0.2)
        place(c, cutout(Image.new('RGBA', (900, 160), (40, 38, 36, 255)), border=6, shadow=0.4, bcol=col), 540 + jx, y + jy, q, (-0.8, 0.8, -0.6, 0.6)[k] + jr)
        if q < 0.6: continue
        d = ImageDraw.Draw(c); bx, by = 150, y
        if ok: d.line((bx - 22, by + 2, bx - 6, by + 20, bx + 24, by - 18), fill=col, width=10, joint='curve')
        else: d.line((bx - 18, by - 18, bx + 18, by + 18), fill=col, width=10); d.line((bx - 18, by + 18, bx + 18, by - 18), fill=col, width=10)
        c.alpha_composite(text_img(h1, 'anton', 56, CREAM), (210, int(y - 64)))
        c.alpha_composite(text_img(h2, 'type', 28, (200, 194, 182), 1), (214, int(y + 22)))
    tw = at(i, 'approved', 0.5)
    if t > tw:
        place_text(c, 'watch: UPI fee decision + profits', 'mark', 48, YEL, 540, 1500, t, 'w2', tw, 'slide', rot=-3)
    typed(c, 'Not investment advice. No prediction.', 'type', 30, (200, 194, 182), 1620, t, tw + 0.3, tw + 1.4)


def s9(c, t):
    i = 8; T0 = STARTS[i]
    q = pp(t, T0, 0.45, 1.2)
    place(c, SS._card(960, 860), 540, 600, q, -0.4)
    if q > 0.6:
        place(c, text_img('PAYTM · CHEAT SHEET', 'anton', 56, INK), 540, 230)
        d = ImageDraw.Draw(c); d.line((90, 272, 990, 272), fill=INK, width=4)
        rows = [('Price (26 Nov 2026)', '₹1,768.90', INK), ('IPO price (Nov 2021)', '₹2,150', INK), ('vs IPO price', '-18%', RED),
                ('All-time low (May 2024)', '₹310', RED), ('From the low', '5.7x', GRN), ('Q2 FY27 revenue', '+28%', GRN),
                ('Q2 FY27 profit', '₹225 Cr', GRN), ('19 Nov move', '-8.7%', RED)]
        for k, (a_, b_, col) in enumerate(rows):
            tk = T0 + 0.3 + 0.08 * k
            if t < tk: continue
            y = 300 + k * 78
            c.alpha_composite(text_img(a_, 'osw5', 38, INK), (100, y))
            v = text_img(b_, 'anton', 44, col); c.alpha_composite(v, (980 - v.size[0], y - 2))
        SS.save_pulse(c, t, T0 + 1.2, 540, 1080, 'SAVE THIS')
    SS.send_frame(c, t, at(i, 'send it', -0.3), 'your friend who holds Paytm', y=1300)
    tf = at(i, 'Follow', -0.2)
    if t > tf:
        q2 = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1530, 0.5 + 0.5 * eback(q2), 0, clamp(q2 * 3))
    for k, ln in enumerate(['Price: NSE via INDmoney, 26 Nov 2026 · IPO: Business Standard 18 Nov 2021',
                            'Low: Business Today 9 May 2024 · Results: Q2 FY27 filing, 26 Oct 2026',
                            'Not a buy/sell call. Education only. I may hold some stocks named.']):
        place_text(c, ln, 'type', 22, GREY, 540, 1680 + k * 34, t, None, T0 + 0.3, 'fade', track=1)


def pp(t, t0, d=0.35, s=1.6): return eback(prog(t, t0, d), s)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
DARK_SCENES = {7}


def slam_times():
    return [at(0, 'crashed', -0.2), at(0, 'rose five', -0.2), at(0, 'trap', -0.2), at(1, 'Down twenty', -0.2), at(2, 'stopped', -0.2),
            at(2, 'three hundred', 0.3), at(3, 'Today', 0.6), at(6, 'almost nine', 0.0), at(7, 'Both', -0.2)] + [STARTS[k] + 0.05 for k in range(1, 8)]


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
