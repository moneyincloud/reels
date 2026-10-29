"""Suzlon: multibagger or trap? PC Jeweller-style paper collage (clipping, highlighter, hand chart, marker, stamps, receipt)"""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs, typed, drop, warn_icon, receipt
from fridge import follow_btn
import saveshare as SS
import defence as DF

SH = ROOT + 'suzlon/'
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
def clipping(hp, head='SUZLON ENERGY', top='THE MARKET PAGE', sub='WIND · NSE: SUZLON'):
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
    ic = text_img('FACTORY', 'type', 22, GREY, 2); im.alpha_composite(ic, (75 - ic.size[0] // 2, 30))
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


# ---------------- scenes ----------------
def s1(c, t):
    i = 0
    words_line(c, t, [("HOLDING", INK, 0.1), ("SUZLON?", RED, 0.35)], 'anton', 132, 300, key='h1')
    dy, a = drop(t, 0.5, 360)
    if a > 0:
        hp = round(prog(t, 1.2, 0.5) * 20) / 20
        jx, jy, jr = jit('clip', t, 2, 0.5)
        place(c, clipping(hp), 540 + jx, 640 + dy + jy, 1.0, -3 + jr + (1 - a) * 8, a)
    td = at(i, "Don't buy", -0.2)
    if t > td:
        place_text(c, "don't buy more yet!", 'mark', 70, RED, 540, 900, t, 'dbm', td, 'slide', rot=-4, amp=1.5)
        marker_line(c, [(220, 960), (540, 952), (860, 942)], prog(t, td + 0.4, 0.4), RED, 9)
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
    tl = at(i, 'Fifty six', -0.2)
    if t > tl:
        v = int(56 * eo(prog(t, tl, 1.0)))
        place(c, text_img(f'{v} LAKH', 'anton', 150, INK), 540, 300)
        place_text(c, 'Indians own it', 'mark', 56, RED, 540, 410, t, 'own', tl + 0.4, 'slide', rot=-3)
    p = prog(t, at(i, 'In 2008', -0.4), 0.45)
    if p > 0:
        ox, oy = 60, 500 + (1 - eo(p)) * 600; w, h = 960, 820
        place(c, sheet_cut(w, h), ox + w / 2, oy + h / 2, 1.0, 0, clamp(p * 3))
        vals = [459.8, 220, 60, 30, 18, 12, 10, 6, 5, 3, 8.15]
        labs = ['2008', '', '', '2011', '', '', '2015', '', '', '2020', '2023']
        t1 = at(i, 'four hundred', -0.2); t2 = at(i, '2023', 0.4)
        f = clamp((t - t1) / max(0.1, t2 - t1))
        if t > t1:
            tip = hand_chart(c, t, ox, oy, w, h, vals, labs, 0, 500, eio(f), INK, (240, 120, 110))
            if t > t1:
                place(c, text_img('₹460', 'anton', 64, INK), ox + 200, oy + 90, pp(t, t1 + 0.2))
            tc = at(i, 'debt crushed', -0.2)
            if t > tc:
                place_text(c, 'debt crushed it', 'mark', 52, RED, ox + 560, oy + 230, t, 'dc', tc, 'slide', rot=-6)
                marker_line(c, curve((ox + 470, oy + 270), (ox + 330, oy + 340), (ox + 290, oy + 470)), prog(t, tc + 0.25, 0.45), RED, 7, head=True, head_size=22)
            if t > t2 - 0.3 and tip:
                tg = text_img('₹8', 'anton', 70, RED); c.alpha_composite(tg, (int(tip[0] - 70), int(tip[1] - 110)))
                sc, a = slam(t, t2); place(c, stamp_c('-98%', RED, 110, -8, 21), ox + 700, oy + 420, sc, 0, a)
    src(c, t, 'Line simplified · dots: ₹459.80 Jan 2008, ₹8.15 May 2023 (Business Today)', T0 + 1.0, 1440)


MONTHLY = [59.3, 54.01, 52.67, 47.67, 42.67, 39.56, 55.58, 56.99, 58.9, 48.01, 47.52, 39.49, 36.79]
MLAB = ['OCT', '', '', 'JAN', '', '', 'APR', '', '', 'JUL', '', '', 'OCT']


def s3(c, t):
    i = 2; T0 = STARTS[i]
    jx, jy, jr = jit('cnt', t, 1.2, 0.3)
    if t > T0 + 0.1:
        v = 61.5 - (61.5 - 36.79) * eo(prog(t, T0 + 0.2, 1.4))
        place(c, text_img(f'₹{v:.2f}', 'anton', 190, RED if v < 45 else INK), 540 + jx, 320 + jy, 1.0, jr)
        typed(c, 'SUZLON · 29 OCT 2026 CLOSE', 'type', 32, GREY, 450, t, T0 + 0.2, T0 + 1.0)
    p = prog(t, T0 + 0.4, 0.45)
    if p > 0:
        ox, oy = 60, 520 + (1 - eo(p)) * 600; w, h = 960, 640
        place(c, sheet_cut(w, h), ox + w / 2, oy + h / 2, 1.0, 0, clamp(p * 3))
        f = eio(prog(t, T0 + 0.8, 2.2))
        hand_chart(c, t, ox, oy, w, h, MONTHLY, MLAB, 30, 65, f, INK, YEL)
        th = at(i, 'sixty one', -0.4)
        if t > th:
            x = ox + 90 + (w - 160) * 1 / 12; y = oy + h - 70 - (61.5 - 30) / 35 * (h - 140)
            marker_ellipse(c, x, y, 70, 46, prog(t, th, 0.45), RED, 7, seed=8)
            place_text(c, 'high ₹61.50', 'mark', 46, RED, x + 230, y - 10, t, 'hi', th + 0.2, 'slide', rot=-4)
        tf = at(i, 'Forty', -0.3)
        if t > tf:
            sc, a = slam(t, tf); place(c, stamp_c('-40%', RED, 96, 8, 31), ox + 800, oy - 40, sc, 0, a)
    tw = at(i, 'So what', -0.2)
    if t > tw:
        place_text(c, 'so what does it actually do?', 'pfi', 64, INK, 540, 1290, t, 'sw', tw, 'pop')
    src(c, t, 'Monthly close · NSE via INDmoney · 29 Oct 2026', T0 + 1.0, 1400)


def s4(c, t):
    i = 3; T0 = STARTS[i]
    words_line(c, t, [("WIND", INK, T0 + 0.1), ("TURBINES", TEAL, T0 + 0.3)], 'anton', 140, 300, key='wt')
    tp = at(i, 'giant fans', -0.3)
    if t > T0 + 0.3:
        s = 0.9 * eback(prog(t, T0 + 0.3, 0.5))
        turbine(c, 300, 520, s, t, INK, 0.5); turbine(c, 560, 470, s * 1.15, t + 0.2, INK, 0.45); turbine(c, 800, 540, s * 0.85, t + 0.4, INK, 0.55)
    if t > tp:
        place_text(c, 'wind in, electricity out', 'mark', 52, RED, 540, 880, t, 'wi', tp, 'slide', rot=-3)
        marker_line(c, [(250, 930), (540, 924), (830, 916)], prog(t, tp + 0.3, 0.4), RED, 8)
    tf = at(i, 'fifteen', -0.3)
    if t > tf:
        v = int(15 * eo(prog(t, tf, 0.6)))
        hw = text_w('15 FACTORY HUBS', 'anton', 92)
        highlight(c, 540 - hw / 2 - 16, 990, 540 + hw / 2 + 16, 1090, prog(t, tf + 0.5, 0.4), seed=41)
        place(c, text_img(f'{v} FACTORY HUBS', 'anton', 92, INK), 540, 1040)
    for k, (st_, ph, rot) in enumerate((('GUJARAT', 'Gujarat', -1.5), ('KARNATAKA', 'Karnataka', 1.2), ('TAMIL NADU', 'Tamil Nadu', -0.8))):
        tk = at(i, ph, -0.3); pk = prog(t, tk, 0.45)
        if pk <= 0: continue
        jx, jy, jr = jit(('tk', k), t, 1.4, 0.25)
        place(c, ticket(st_, 'smart factory'), 540 + (1 - eo(pk)) * 900 + jx, 1210 + k * 190 + jy, 0.92, rot + jr)
    src(c, t, 'Suzlon Q2 FY27 · Free Press Journal, 29 Oct 2026', T0 + 1.0, 1790)


PINS = [('USA', -98, 39, BLUE, (0, -32)), ('GERMANY', 10.4, 51.2, NAVY, (0, -32)), ('AUSTRALIA', 134, -25, ORG, (0, 34))]
LIT = {'United States of America': BLUE, 'Germany': NAVY, 'Australia': ORG}


@functools.lru_cache(4)
def map_img(lit):
    S_ = 2; im = Image.new('RGBA', (DF.MW * S_, DF.MH * S_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for nm, polys in DF.world():
        col = (255, 140, 40) if nm == 'India' else (LIT.get(nm, (214, 207, 192)) if lit else (214, 207, 192))
        base = col == (214, 207, 192)
        for pts in polys:
            if len(pts) < 3: continue
            P = [(x * S_, y * S_) for x, y in pts]
            d.polygon(P, fill=col); d.line(P + [P[0]], fill=(150, 142, 128) if base else INK, width=2 if base else 3)
    return im.resize((DF.MW, DF.MH), Image.LANCZOS)


def s5(c, t):
    i = 4; T0 = STARTS[i]
    ts = at(i, 'nine thousand', -0.4)
    if t > T0 + 0.1:
        v = int(9600 * eo(prog(t, ts, 1.0))) if t > ts else 0
        place(c, text_img(f'{v:,}+', 'anton', 150, TEAL), 540, 300)
        place_text(c, 'turbines it services', 'mark', 54, INK, 540, 410, t, 'svc', ts + 0.3, 'slide', rot=-3)
    tm = at(i, 'seventeen', -0.6)
    if t > tm:
        p = prog(t, tm, 0.45); oy = 520 + (1 - eo(p)) * 500
        place(c, cutout(Image.new('RGBA', (DF.MW + 40, DF.MH + 40), SOFT + (255,)), border=0, shadow=0.3), 540, oy + DF.MH / 2, 1, -0.6, clamp(p * 3))
        c.alpha_composite(map_img(t > tm + 0.6), (40, int(oy)))
        d = ImageDraw.Draw(c); hx, hy = DF.proj(78.5, 22); hx += 40; hy += oy
        for k, (nm, lon, lat, col, off) in enumerate(PINS):
            tk = at(i, ('US', 'Australia', 'Germany')[k], -0.3)
            if t < tk: continue
            x, y = DF.proj(lon, lat); x += 40; y += oy
            q = eio(prog(t, tk, 0.6)); pts = DF.arc_pts((hx, hy), (x, y)); m = max(2, int(len(pts) * q)); stroke(c, pts, 5, col)
            if t > tk + 0.4:
                pr = eback(prog(t, tk + 0.4, 0.3)); rr = 12 * pr
                d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=col, outline=INK, width=3)
                place(c, text_img(nm, 'anton', 34, INK), x + off[0], y + off[1])
        pul = 1 + 0.25 * math.sin(t * 6)
        d.ellipse((hx - 16 * pul, hy - 16 * pul, hx + 16 * pul, hy + 16 * pul), outline=RED, width=4)
        sc, a = slam(t, tm + 0.3); place(c, stamp_c('17 COUNTRIES', RED, 92, -5, 51), 540, oy + DF.MH + 110, sc, 0, a)
        if t > tm + 1.2:
            place_text(c, 'India 15.5 GW · abroad ~6 GW', 'osw5', 44, NAVY, 540, oy + DF.MH + 240, t, 'gw', tm + 1.2, 'fade')
    src(c, t, '17 countries: Screener · GW split: Business Today, Apr 2026', T0 + 1.0, 1640)
    src(c, t, '9,600+ turbines serviced: Suzlon Q2 FY27', T0 + 1.0, 1676)


def s6(c, t):
    i = 5; T0 = STARTS[i]
    dy, a = drop(t, T0 + 0.05, 300)
    if a > 0:
        hp = round(prog(t, T0 + 0.6, 0.5) * 20) / 20
        place(c, clipping(hp, "TODAY'S RESULT", 'Q2 FY27 · 29 OCT 2026', 'SUZLON ENERGY · JUL-SEP 2026'), 540, 380 + dy, 0.82, -2, a)
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
    row(at(i, 'Revenue', 0.1), 120, 'Revenue', '₹4,869 Cr vs ₹3,866 Cr', '+26%', GRN)
    row(at(i, 'seven hundred', -0.2), 320, 'Delivered', 'record quarter', '710 MW', INK, hl=at(i, 'record', 0.2))
    row(at(i, 'order book', -0.2), 520, 'Order book', 'still to deliver', '6+ GW', TEAL)
    src(c, t, 'Suzlon Q2 FY27 results, 29 Oct 2026 · Business Today, Free Press Journal', T0 + 1.0, 1520)


def s7(c, t):
    i = 6; T0 = STARTS[i]
    words_line(c, t, [("BUT", RED, T0 + 0.05), ("PROFIT", INK, T0 + 0.25)], 'anton', 130, 300, key='bp')
    tf = at(i, 'sixty nine', -0.3)
    if t > tf:
        sc, a = slam(t, tf); place(c, stamp_c('-69%', RED, 140, -6, 61), 540, 530, sc, 0, a)
        place(c, text_img('₹1,279 Cr to ₹394 Cr', 'osw5', 48, INK), 540, 690, pp(t, tf + 0.3))
    tp = at(i, "Don't panic", -0.2)
    if t > tp:
        place_text(c, "don't panic!", 'mark', 60, TEAL, 540, 790, t, 'dp2', tp, 'slide', rot=-4)
    tt = at(i, 'one time', -0.3)
    if t > tt:
        q = pp(t, tt, 0.35, 1.3); place(c, cutout(Image.new('RGBA', (900, 230), SOFT + (255,)), border=0, shadow=0.3), 540, 960, q, 1)
        if q > 0.6:
            c.alpha_composite(text_img('LAST YEAR INCLUDED', 'type', 28, GREY, 2), (120, 870))
            c.alpha_composite(text_img('₹891 Cr one-time tax gain', 'anton', 58, INK), (120, 910))
            marker_line(c, [(120, 1010), (560, 1004), (930, 996)], prog(t, tt + 0.6, 0.4), RED, 8)
    tw = at(i, 'Without', -0.3)
    if t > tw:
        place(c, text_img('WITHOUT IT:', 'osw5', 40, GREY), 330, 1110, pp(t, tw))
        place(c, text_img('+1.3%', 'anton', 120, ORG), 720, 1110, pp(t, tw + 0.3))
    tm = at(i, 'margins', -0.4)
    if t > tm:
        d = ImageDraw.Draw(c); base = 1500
        c.alpha_composite(text_img('EBITDA MARGIN', 'type', 28, GREY, 2), (140, 1210))
        for k, (lab, v, col) in enumerate((('Q2 FY26', 18.6, GREY), ('Q2 FY27', 14.8, RED))):
            ph = eo(prog(t, tm + 0.2 * k, 0.6)); hg = int(v / 18.6 * 200 * ph); x = 380 + k * 320
            d.rounded_rectangle((x - 80, base - hg, x + 80, base), 12, fill=col, outline=INK, width=4)
            place(c, text_img(f'{v * ph:.1f}%', 'anton', 50, INK), x, base - hg - 32)
            place(c, text_img(lab, 'type', 26, GREY), x, base + 26)
        marker_line(c, curve((470, 1290), (560, 1260), (650, 1330)), prog(t, tm + 0.6, 0.4), RED, 7, head=True, head_size=20)
    src(c, t, 'Free Press Journal, 29 Oct 2026', T0 + 1.0, 1640)


def s8(c, t):
    i = 7; T0 = STARTS[i]
    if t > T0 + 0.1:
        p = prog(t, T0 + 0.1, 0.3); lw = text_w('THE VERDICT', 'osw', 54, 2); x0 = 540 - (lw + 70) / 2
        place(c, warn_icon(YEL), x0 + 28, 262, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
        place(c, text_img('THE VERDICT', 'osw', 54, YEL, 2), x0 + 70 + lw / 2, 260, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
    tn = at(i, 'Neither', -0.2)
    words_line(c, t, [("NEITHER.", CREAM, tn), ("YET.", RED, tn + 0.35)], 'anton', 150, 420, key='ny')
    if t > tn + 0.6:
        marker_line(c, [(620, 490), (760, 484), (900, 478)], prog(t, tn + 0.6, 0.35), RED, 10)
    rows = [('Debt almost gone', '₹556 Cr vs ₹6,719 Cr reserves', 'Debt is', GRN, True),
            ('Profit is real', 'ROE 39.7% · net worth ₹10,000 Cr+', 'profit is real', GRN, True),
            ('Promoters own 11.7%', 'down from 21% in 2017', 'promoters', RED, False),
            ('Growth just slowed', 'comparable profit +1.3%', 'growth just', RED, False)]
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
    if t > at(i, 'growth just', 1.0):
        place_text(c, 'watch the next 2 quarters', 'mark', 52, YEL, 540, 1500, t, 'w2', at(i, 'growth just', 1.0), 'slide', rot=-3)
    typed(c, 'Not investment advice. DYOR.', 'type', 30, (200, 194, 182), 1620, t, at(i, 'growth just', 1.4), at(i, 'growth just', 2.4))


def s9(c, t):
    i = 8; T0 = STARTS[i]
    q = pp(t, T0, 0.45, 1.2)
    place(c, SS._card(960, 860), 540, 600, q, -0.4)
    if q > 0.6:
        place(c, text_img('SUZLON · CHEAT SHEET', 'anton', 56, INK), 540, 230)
        d = ImageDraw.Draw(c); d.line((90, 272, 990, 272), fill=INK, width=4)
        rows = [('Price (29 Oct)', '₹36.79', INK), ('From 52-wk high', '-40%', RED), ('Q2 revenue', '+26%', GRN), ('Q2 profit (comparable)', '+1.3%', ORG),
                ('Order book', '6+ GW', TEAL), ('Borrowings', '₹556 Cr', GRN), ('Promoter holding', '11.7%', RED), ('P/E', '16.2', INK)]
        for k, (a_, b_, col) in enumerate(rows):
            tk = T0 + 0.3 + 0.08 * k
            if t < tk: continue
            y = 300 + k * 78
            c.alpha_composite(text_img(a_, 'osw5', 38, INK), (100, y))
            v = text_img(b_, 'anton', 44, col); c.alpha_composite(v, (980 - v.size[0], y - 2))
        SS.save_pulse(c, t, T0 + 1.2, 540, 1080, 'SAVE THIS')
    SS.send_frame(c, t, at(i, 'send it', -0.3), 'your friend who holds Suzlon', y=1300)
    tf = at(i, 'Follow', -0.2)
    if t > tf:
        q2 = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1530, 0.5 + 0.5 * eback(q2), 0, clamp(q2 * 3))
    for k, ln in enumerate(['Price: NSE via INDmoney, 29 Oct 2026 close', 'Fundamentals: Screener.in · Q2 FY27 results 29 Oct 2026',
                            'Not a buy/sell call. Education only.']):
        place_text(c, ln, 'type', 22, GREY, 540, 1680 + k * 34, t, None, T0 + 0.3, 'fade', track=1)


def pp(t, t0, d=0.35, s=1.6): return eback(prog(t, t0, d), s)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
DARK_SCENES = {7}


def slam_times():
    return [at(0, 'trap', -0.2), at(1, '2023', 0.4), at(2, 'Forty', -0.3), at(6, 'sixty nine', -0.3)] + [STARTS[k] + 0.05 for k in range(1, 8)]


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
