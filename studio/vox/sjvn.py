"""SJVN: profit doubled, stock fell. Multibagger or trap? (Suzlon collage style, female VO)"""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs, typed, drop, warn_icon, receipt
from fridge import follow_btn
import saveshare as SS
import defence as DF
import suzlon as SZ
import tea as TEA

SH = ROOT + 'sjvn/'
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
SOFT = (252, 250, 244)
label = TEA.label
MONTHLY = [88.03, 77.86, 74.76, 72.5, 73.03, 63.35, 78.98, 75.16, 73.15, 68.62, 64.71, 59.32, 51.68]
MLAB = ['OCT 25', '', '', 'JAN', '', '', 'APR', '', '', 'JUL', '', '', 'OCT 26']


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def pp(t, t0, d=0.35, s=1.6): return eback(prog(t, t0, d), s)


def src(c, t, txt, t0, y=1720, col=GREY):
    if t > t0: place_text(c, txt, 'type', 24, col, 540, y, t, None, t0, 'fade', track=1)


@functools.lru_cache(None)
def dam(w=420, h=300):
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(0, 60), (w * 0.35, 40), (w * 0.35, h), (0, h)], fill=(120, 170, 220))
    d.polygon([(w * 0.35, 40), (w * 0.55, 40), (w * 0.7, h), (w * 0.35, h)], fill=(200, 196, 186), outline=INK)
    d.line([(w * 0.35, 40), (w * 0.55, 40), (w * 0.7, h), (w * 0.35, h), (w * 0.35, 40)], fill=INK, width=6)
    for k in range(4):
        x = w * 0.72 + k * 22; d.line((x, h * 0.55, x + 30, h), fill=(120, 170, 220), width=10)
    d.rectangle((w * 0.75, h * 0.55, w - 10, h - 6), fill=(90, 96, 110), outline=INK, width=5)
    d.polygon([(w * 0.88, h * 0.2), (w * 0.94, h * 0.2), (w * 0.96, h * 0.55), (w * 0.86, h * 0.55)], fill=(150, 150, 160), outline=INK)
    return cutout(im, border=8, shadow=0.35)


@functools.lru_cache(None)
def plant(kind):
    w, h = 300, 240
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if kind == 'coal':
        d.rectangle((30, 120, 270, 230), fill=(110, 110, 120), outline=INK, width=6)
        for x in (80, 180):
            d.polygon([(x, 120), (x + 50, 120), (x + 40, 20), (x + 10, 20)], fill=(170, 170, 178), outline=INK)
            d.ellipse((x + 5, 0, x + 45, 26), fill=(220, 220, 225))
    elif kind == 'solar':
        for k in range(3):
            x = 20 + k * 92; d.polygon([(x, 200), (x + 80, 200), (x + 90, 120), (x + 10, 120)], fill=(40, 80, 160), outline=INK)
            d.line([(x, 200), (x + 80, 200), (x + 90, 120), (x + 10, 120), (x, 200)], fill=INK, width=4)
        d.ellipse((220, 10, 290, 80), fill=YEL, outline=INK, width=4)
    return cutout(im, border=8, shadow=0.35)


# ---------------- scenes ----------------
def s1(c, t):
    i = 0
    words_line(c, t, [("PROFIT", INK, 0.1), ("2X", GRN, 0.3)], 'anton', 140, 290, key='p2')
    words_line(c, t, [("STOCK", INK, at(i, 'The stock', -0.1)), ("FELL", RED, at(i, 'fell', -0.1))], 'anton', 140, 440, key='sf')
    dy, a = drop(t, at(i, "Don't decide", -0.3), 360)
    if a > 0:
        hp = round(prog(t, at(i, "Don't decide", 0.3), 0.5) * 20) / 20
        place(c, SZ.clipping(hp, 'SJVN LTD', 'THE MARKET PAGE', 'POWER · NSE: SJVN'), 540, 760 + dy, 0.95, -3, a)
    tm = at(i, 'multibagger', -0.25)
    if t > tm:
        p = prog(t, tm, 0.32); place(c, SZ.qtag('MULTIBAGGER?', GRN), 540, 1080, 0.55 + 0.45 * eback(p), -3, clamp(p * 3))
    tt = at(i, 'trap', -0.2)
    if t > tt:
        sc, a2 = slam(t, tt); place(c, SZ.qtag('OR TRAP?', RED), 540, 1270, sc, 3, a2)
        marker_ellipse(c, 540, 1270, 250, 90, prog(t, tt + 0.35, 0.5), INK, 8, seed=5)


def s2(c, t):
    i = 1; T0 = STARTS[i]
    tl = at(i, 'Thirteen lakh', -0.2)
    if t > T0 + 0.1:
        place_text(c, 'GOVT POWER COMPANY', 'anton', 84, INK, 540, 260, t, 'gp', T0 + 0.1, 'pop')
    if t > tl:
        v = int(13.44 * 10 * eo(prog(t, tl, 1.0))) / 10
        place(c, text_img(f'{v:.1f} LAKH', 'anton', 120, NAVY), 540, 390)
        place_text(c, 'Indians own it', 'mark', 50, RED, 540, 480, t, 'own', tl + 0.4, 'slide', rot=-3)
    p = prog(t, at(i, 'A year ago', -0.4), 0.45)
    if p > 0:
        ox, oy, w, h = 60, 560 + (1 - eo(p)) * 600, 960, 700
        place(c, SZ.sheet_cut(w, h), ox + w / 2, oy + h / 2, 1.0, 0, clamp(p * 3))
        f = eio(prog(t, at(i, 'eighty eight', -0.2), 2.4))
        SZ.hand_chart(c, t, ox, oy, w, h, MONTHLY, MLAB, 40, 95, f, INK, (240, 140, 130))
        th = at(i, 'eighty eight', -0.2)
        if t > th: place(c, text_img('₹88', 'anton', 64, INK), ox + 200, oy + 70, pp(t, th))
        tt = at(i, 'fifty two', -0.3)
        if t > tt:
            sc, a = slam(t, tt); place(c, stamp_c('-41%', RED, 100, -8, 21), ox + 700, oy + 220, sc, 0, a)
            place(c, text_img('₹51.68', 'anton', 70, RED), ox + 800, oy + h - 170, pp(t, tt + 0.2))
    src(c, t, 'Monthly close · NSE via INDmoney · 30 Oct 2026 · 13.44 lakh holders: Screener', T0 + 1.0, 1400)


def s3(c, t):
    i = 2; T0 = STARTS[i]
    words_line(c, t, [("IT", INK, T0 + 0.1), ("MAKES", INK, T0 + 0.25), ("POWER", ORG, T0 + 0.4)], 'anton', 130, 280, key='mp')
    th = at(i, 'Hydro', -0.3)
    if t > th:
        p = prog(t, th, 0.45); place(c, dam(), 540, 560 + (1 - eo(p)) * 300, 1.0, -1, clamp(p * 3))
        place(c, label('HYDRO · HIMACHAL', BLUE), 540, 760, pp(t, th + 0.3), -2)
    tn = at(i, 'Nathpa', -0.3)
    if t > tn: place_text(c, 'Nathpa Jhakri · Rampur · Naitwar Mori', 'mark', 40, INK, 540, 840, t, 'nj', tn, 'slide', rot=-2)
    tc = at(i, 'coal plant', -0.3)
    if t > tc:
        p = prog(t, tc, 0.45); place(c, plant('coal'), 280, 1080 + (1 - eo(p)) * 300, 1.0, -3, clamp(p * 3))
        place(c, label('BUXAR · 1,320 MW', GREY), 280, 1240, pp(t, tc + 0.3), -2)
    ts = at(i, 'solar', -0.3)
    if t > ts:
        p = prog(t, ts, 0.45); place(c, plant('solar'), 800, 1080 + (1 - eo(p)) * 300, 1.0, 3, clamp(p * 3))
        SZ.turbine(c, 960, 990, 0.35, t, INK, 0.6)
        place(c, label('SOLAR + WIND', GRN), 800, 1240, pp(t, ts + 0.3), 2)
    tf = at(i, 'five thousand', -0.4)
    if t > tf:
        v = int(4931.5 * eo(prog(t, tf, 1.0)))
        fw = text_w('4,931 MW', 'anton', 130)
        highlight(c, 540 - fw / 2 - 20, 1360, 540 + fw / 2 + 20, 1480, prog(t, tf + 1.0, 0.4), seed=2)
        place(c, text_img(f'{v:,} MW', 'anton', 130, INK), 540, 1420)
        place_text(c, 'installed', 'mark', 44, RED, 540, 1530, t, 'in', tf + 0.6, 'slide', rot=-3)
    src(c, t, 'SJVN company profile (sjvn.nic.in) · 16 commissioned projects', T0 + 1.0, 1720)


LIT = {'Nepal': RED}


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


def s4(c, t):
    i = 3; T0 = STARTS[i]
    place_text(c, 'BUILDING ABROAD', 'anton', 110, INK, 540, 260, t, 'ba', T0 + 0.05, 'pop')
    p = prog(t, T0 + 0.2, 0.45)
    # zoomed map of South Asia
    full = map_img(t > at(i, 'Nepal', -0.2))
    x0, y0 = DF.proj(60, 38); x1, y1 = DF.proj(100, 5)
    crop = full.crop((int(x0), int(y0), int(x1), int(y1)))
    sc = 900 / crop.size[0]; crop = crop.resize((900, int(crop.size[1] * sc)), Image.LANCZOS)
    oy = 380 + (1 - eo(p)) * 500
    place(c, cutout(Image.new('RGBA', (crop.size[0] + 40, crop.size[1] + 40), SOFT + (255,)), border=0, shadow=0.3), 540, oy + crop.size[1] / 2, 1, -0.6, clamp(p * 3))
    c.alpha_composite(crop, (90, int(oy)))
    def P(lon, lat):
        x, y = DF.proj(lon, lat); return 90 + (x - x0) * sc, oy + (y - y0) * sc
    hx, hy = P(77.2, 31.1)  # Himachal
    d = ImageDraw.Draw(c)
    d.ellipse((hx - 14, hy - 14, hx + 14, hy + 14), fill=BLUE, outline=INK, width=4)
    place(c, text_img('HIMACHAL', 'anton', 30, INK), hx - 40, hy - 36)
    ta = at(i, 'Arun three', -0.3)
    if t > ta:
        nx, ny = P(87.2, 27.5)
        pts = SZ.DF.arc_pts((hx, hy), (nx, ny)) if hasattr(SZ, 'DF') else DF.arc_pts((hx, hy), (nx, ny))
        m = max(2, int(len(pts) * eio(prog(t, ta, 0.7)))); stroke(c, pts[:m], 6, RED)
        if t > ta + 0.5:
            rr = 14 * eback(prog(t, ta + 0.5, 0.3)); d.ellipse((nx - rr, ny - rr, nx + rr, ny + rr), fill=RED, outline=INK, width=4)
            place(c, label('NEPAL · ARUN-3 · 900 MW', RED), 540, oy + crop.size[1] + 90, pp(t, ta + 0.5), -2)
    tl = at(i, 'Lower Arun', -0.3)
    if t > tl: place(c, label('+ LOWER ARUN · 669 MW', ORG), 540, oy + crop.size[1] + 200, pp(t, tl), 2)
    tp = at(i, 'power line', -0.3)
    if t > tp: place_text(c, '217 km power line across the border', 'mark', 44, INK, 540, oy + crop.size[1] + 310, t, 'pl', tp, 'slide', rot=-2)
    src(c, t, 'SJVN company profile · Nepal projects via subsidiaries', T0 + 1.0, 1720)


def s5(c, t):
    i = 4; T0 = STARTS[i]
    dy, a = drop(t, T0 + 0.05, 300)
    if a > 0:
        hp = round(prog(t, T0 + 0.6, 0.5) * 20) / 20
        place(c, SZ.clipping(hp, "TODAY'S RESULT", 'Q2 FY27 · 30 OCT 2026', 'SJVN LTD · JUL-SEP 2026'), 540, 380 + dy, 0.82, -2, a)
    pr = prog(t, at(i, 'Revenue', -0.4), 0.45)
    if pr <= 0: return
    rc = receipt(); rx0, ry0 = 130, 700 + (1 - eo(pr)) * 700
    place(c, rc, rx0 + rc.size[0] / 2 - (rc.size[0] - 820) / 2 + 3, ry0 + rc.size[1] / 2 - (rc.size[1] - 720) / 2 + 7, 1.0, 0, clamp(pr * 3))
    def row(t0, y, lab, sub, amt, col):
        q = prog(t, t0, 0.3)
        if q <= 0: return
        dx = (1 - eo(q)) * 40; a_ = clamp(q * 3)
        li = text_img(lab, 'osw5', 50, INK); place(c, li, rx0 + 60 + li.size[0] / 2 + dx, ry0 + y - 14, 1, 0, a_)
        si = text_img(sub, 'type', 26, GREY, 1); place(c, si, rx0 + 60 + si.size[0] / 2 + dx, ry0 + y + 34, 1, 0, a_)
        ai = text_img(amt, 'anton', 80, col); place(c, ai, rx0 + 770 - ai.size[0] / 2 - dx, ry0 + y, 1, 0, a_)
    row(at(i, 'Revenue', 0.1), 150, 'Revenue', '₹2,244 Cr vs ₹1,032 Cr', '+117%', GRN)
    row(at(i, 'Profit up', -0.1), 380, 'Net profit', '₹658 Cr vs ₹308 Cr', '+114%', GRN)
    tp = at(i, 'six hundred', 0.4)
    if t > tp:
        sc, a = slam(t, tp); place(c, stamp_c('PROFIT 2X', GRN, 90, -8, 51), 760, 1380, sc, 0, a)
    src(c, t, 'SJVN Q2 FY27 consolidated results, 30 Oct 2026 (via InCred Money)', T0 + 1.0, 1720)


def s6(c, t):
    i = 5; T0 = STARTS[i]
    words_line(c, t, [("READ", INK, T0 + 0.05), ("THE", INK, T0 + 0.2), ("FINE", RED, T0 + 0.35), ("PRINT", RED, T0 + 0.5)], 'anton', 120, 290, key='fp')
    tt = at(i, 'Two hundred', -0.3)
    if t > tt:
        q = pp(t, tt, 0.4, 1.3); place(c, cutout(Image.new('RGBA', (920, 360), SOFT + (255,)), border=0, shadow=0.35), 540, 610, q, 1)
        if q > 0.6:
            c.alpha_composite(text_img('₹283 CR', 'anton', 120, ORG), (130, 450))
            c.alpha_composite(text_img('tariffs for EARLIER years', 'osw5', 44, INK), (140, 600))
            c.alpha_composite(text_img('Nathpa Jhakri ₹243 Cr · Buxar ₹40 Cr', 'type', 28, GREY, 1), (140, 666))
    to = at(i, 'one time', -0.3)
    if t > to:
        sc, a = slam(t, to); place(c, stamp_c('ONE-TIME', RED, 90, -8, 61), 800, 470, sc, 0, a)
        place(c, text_img('Without it, revenue growth: ~+90%', 'anton', 56, INK), 540, 880, pp(t, to + 0.5))
        place_text(c, '(₹2,244 - ₹283) vs ₹1,032 Cr · my calculation', 'type', 26, GREY, 540, 940, t, 'mc', to + 0.7, 'fade')
    ti = at(i, 'interest costs', -0.4)
    if t > ti:
        d = ImageDraw.Draw(c); base = 1500
        c.alpha_composite(text_img('INTEREST (FINANCE) COST', 'type', 28, GREY, 2), (140, 1040))
        for k, (lab, v, col) in enumerate((('Q2 FY26', 315.1, GREY), ('Q2 FY27', 488.1, RED))):
            ph = eo(prog(t, ti + 0.2 * k, 0.7)); hg = int(v / 488.1 * 330 * ph); x = 380 + k * 320
            d.rounded_rectangle((x - 80, base - hg, x + 80, base), 12, fill=col, outline=INK, width=4)
            place(c, text_img(f'₹{v * ph:.0f} CR', 'anton', 48, INK), x, base - hg - 32)
            place(c, text_img(lab, 'type', 26, GREY), x, base + 26)
        if t > ti + 0.9:
            sc, a = slam(t, ti + 0.9); place(c, stamp_c('+55%', RED, 84, 8, 63), 880, 1250, sc, 0, a)
    src(c, t, 'Q2 FY27 results (InCred Money), 30 Oct 2026', T0 + 1.0, 1720)


def s7(c, t):
    i = 6; T0 = STARTS[i]
    words_line(c, t, [("DEBT", RED, T0 + 0.05), ("EXPLODED", INK, T0 + 0.25)], 'anton', 130, 290, key='de')
    yrs = [('FY21', 2174), ('FY22', 0), ('FY23', 0), ('FY24', 0), ('FY25', 0), ('FY26', 32278)]
    d = ImageDraw.Draw(c); base = 1150
    d.line((100, base, 980, base), fill=INK, width=5)
    for k, (yr, v) in enumerate((('FY21', 2174), ('FY26', 32278))):
        tk = at(i, ('two thousand', 'thirty two')[k], -0.3)
        if t < tk: continue
        x = 330 + k * 420; q = eo(prog(t, tk, 1.0)); hg = int(v / 32278 * 700 * q)
        d.rounded_rectangle((x - 110, base - hg, x + 110, base), 14, fill=GREY if k == 0 else RED, outline=INK, width=5)
        place(c, text_img(f'₹{int(v * q):,} CR', 'anton', 60, INK), x, base - hg - 42)
        place(c, text_img(yr, 'osw5', 40, GREY), x, base + 36)
    tx = at(i, 'thirty two', 1.0)
    if t > tx:
        sc, a = slam(t, tx); place(c, stamp_c('15X', RED, 110, -8, 71), 330, 600, sc, 0, a)
    tr = at(i, 'Return on equity', -0.3)
    if t > tr:
        place(c, label('RETURN ON EQUITY: 4.6%', NAVY), 540, 1330, pp(t, tr), -2)
        place_text(c, 'reserves only ₹10,309 Cr', 'mark', 44, RED, 540, 1440, t, 'rs', tr + 0.4, 'slide', rot=-3)
    src(c, t, 'Borrowings, reserves, ROE: Screener.in consolidated, FY21-FY26', T0 + 1.0, 1720)


def s8(c, t):
    i = 7; T0 = STARTS[i]
    if t > T0 + 0.1:
        p = prog(t, T0 + 0.1, 0.3); lw = text_w('THE VERDICT', 'osw', 54, 2); x0 = 540 - (lw + 70) / 2
        place(c, warn_icon(YEL), x0 + 28, 262, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
        place(c, text_img('THE VERDICT', 'osw', 54, YEL, 2), x0 + 70 + lw / 2, 260, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
    tn = at(i, 'Neither', -0.2)
    words_line(c, t, [("NEITHER.", CREAM, tn), ("YET.", RED, tn + 0.35)], 'anton', 150, 420, key='ny')
    rows = [('Govt owns 81.85%', 'India 55% · Himachal 26.85%', 'government owns', GRN, True),
            ('Dividend ~2.9%', '₹1.50 per share for FY26', 'dividend', GRN, True),
            ('New projects must earn', '3,860 MW still under construction', 'new projects', RED, False),
            ('Debt must shrink', '₹32,278 Cr borrowings', 'debt must', RED, False)]
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
    typed(c, 'Not investment advice. DYOR.', 'type', 30, (200, 194, 182), 1560, t, at(i, 'debt must', 1.0), at(i, 'debt must', 2.0))


def s9(c, t):
    i = 8; T0 = STARTS[i]
    q = pp(t, T0, 0.45, 1.2)
    place(c, SS._card(960, 860), 540, 600, q, -0.4)
    if q > 0.6:
        place(c, text_img('SJVN · CHEAT SHEET', 'anton', 56, INK), 540, 230)
        d = ImageDraw.Draw(c); d.line((90, 272, 990, 272), fill=INK, width=4)
        rows = [('Price (30 Oct close)', '₹51.68', INK), ('1-year change', '-41%', RED), ('Q2 profit', '+114%*', GRN), ('*one-time tariff', '₹283 Cr', ORG),
                ('Borrowings', '₹32,278 Cr', RED), ('ROE', '4.6%', RED), ('Govt holding', '81.85%', INK), ('Dividend yield', '~2.9%', GRN)]
        for k, (a_, b_, col) in enumerate(rows):
            tk = T0 + 0.3 + 0.08 * k
            if t < tk: continue
            y = 300 + k * 78
            c.alpha_composite(text_img(a_, 'osw5', 38, INK), (100, y))
            v = text_img(b_, 'anton', 44, col); c.alpha_composite(v, (980 - v.size[0], y - 2))
        SS.save_pulse(c, t, T0 + 1.2, 540, 1080, 'SAVE THIS')
    SS.send_frame(c, t, at(i, 'send it', -0.3), 'your friend who holds SJVN', y=1300)
    tf = at(i, 'Follow', -0.2)
    if t > tf:
        q2 = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1530, 0.5 + 0.5 * eback(q2), 0, clamp(q2 * 3))
    for k, ln in enumerate(['Price: NSE via INDmoney, 30 Oct 2026', 'Fundamentals: Screener.in · Q2 FY27 results 30 Oct 2026', 'Not a buy/sell call. Education only.']):
        place_text(c, ln, 'type', 22, GREY, 540, 1680 + k * 34, t, None, T0 + 0.3, 'fade', track=1)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
DARK_SCENES = {7}


def slam_times():
    return [at(0, 'trap', -0.2), at(1, 'fifty two', -0.3), at(5, 'one time', -0.3), at(6, 'thirty two', 1.0)] + [STARTS[k] + 0.05 for k in range(1, 8)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('MULTIBAGGER OR TRAP?', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
    ImageDraw.Draw(c).line((60, 118, W - 60, 118), fill=col, width=2)
    ImageDraw.Draw(c).line((60, 118, 60 + (W - 120) * clamp(t / DUR), 118), fill=RED if not dark else YEL, width=8)


transition = SZ.transition


def scene_at(t):
    k = 0
    for i, s in enumerate(STARTS):
        if t >= s: k = i
    return k


def _trans(c, t):
    cols = [(RED, INK), (YEL, INK), (BLUE, YEL), (TEAL, YEL), (YEL, RED), (INK, YEL), (RED, YEL), (YEL, INK)]
    for bi, b in enumerate(B):
        d = 0.62
        if abs(t - b) > d / 2 + 0.12: continue
        for layer, delay in ((0, -0.07), (1, 0.0)):
            p = (t - (b - d / 2) - delay) / d
            if p <= 0 or p >= 1: continue
            p = eio(p); SWd, skew = 2050, 320
            xl = (W + 60) + p * (-(SWd + skew) - (W + 60) - 40)
            r = random.Random(bi * 10 + layer + 888)
            left = [(xl + r.uniform(-14, 14) - skew * (y / H), y) for y in range(0, H + 1, 40)]
            right = [(xl + SWd + r.uniform(-14, 14) - skew * (y / H), y) for y in range(H, -1, -40)]
            if layer == 0: left = [(x - 70, y) for x, y in left]; right = [(x + 70, y) for x, y in right]
            poly_fill(c, left + right, cols[bi % len(cols)][layer], 255, S=1)


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
    header(c, dark, t if not loop else 0); _trans(c, t)
    arr = np.asarray(c.convert('RGB')).astype(np.float32)
    g = grain_frames()[int(t * FPS) % 6]
    fl = 1 + 0.012 * math.sin(t * 37) * math.sin(t * 13)
    return np.clip(arr * fl + g[..., None], 0, 255).astype(np.uint8)
