"""Manappuram Finance: multibagger or trap? paper-collage style (female VO)"""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs, typed, drop, warn_icon, receipt
from fridge import follow_btn
import saveshare as SS
import defence as DF

SH = ROOT + 'mana/'
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
def clipping(hp, head='MANAPPURAM', top='THE MARKET PAGE', sub='GOLD LOANS · NSE: MANAPPURAM'):
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


GOLDC = (226, 172, 40); GOLDD = (176, 122, 20)


def necklace(c, cx, cy, s=1.0, t=0, p=1.0):
    """hand-drawn gold necklace: chain arc of beads + pendant; p = reveal 0..1"""
    d = ImageDraw.Draw(c)
    n = 22; m = max(1, int(n * p))
    for k in range(m):
        a = math.pi * (0.12 + 0.76 * k / (n - 1))
        x = cx + math.cos(a) * 300 * s; y = cy - 160 * s + math.sin(a) * 240 * s
        r = 20 * s
        d.ellipse((x - r, y - r, x + r, y + r), fill=GOLDC, outline=INK, width=max(2, int(4 * s)))
        d.ellipse((x - r * 0.4, y - r * 0.6, x - r * 0.05, y - r * 0.25), fill=(255, 236, 170))
    if p >= 1:
        py = cy + 90 * s
        d.polygon([(cx, py - 50 * s), (cx + 55 * s, py + 10 * s), (cx, py + 90 * s), (cx - 55 * s, py + 10 * s)], fill=GOLDC, outline=INK)
        d.ellipse((cx - 22 * s, py - 2 * s, cx + 22 * s, py + 42 * s), fill=RED, outline=INK, width=max(2, int(4 * s)))
        sp = 0.5 + 0.5 * math.sin(t * 5)
        for (ox, oy) in ((-90, -40), (100, -10), (40, 140)):
            rr = 14 * s * sp; x = cx + ox * s; y = py + oy * s
            d.polygon([(x, y - rr * 2), (x + rr * 0.5, y), (x, y + rr * 2), (x - rr * 0.5, y)], fill=(255, 245, 200))
            d.polygon([(x - rr * 2, y), (x, y - rr * 0.5), (x + rr * 2, y), (x, y + rr * 0.5)], fill=(255, 245, 200))


def coins(c, cx, cy, n, s=1.0):
    d = ImageDraw.Draw(c)
    for k in range(n):
        y = cy - k * 22 * s
        d.ellipse((cx - 70 * s, y - 22 * s, cx + 70 * s, y + 22 * s), fill=GOLDC if k % 2 else GOLDD, outline=INK, width=max(2, int(4 * s)))


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
    tp = at(i, 'Profit up', 0.0)
    if t > 0.1:
        v = int(223 * eo(prog(t, 0.15, 1.2)))
        place(c, text_img(f'PROFIT +{v}%', 'anton', 140, GRN), 540, 300)
    dy, a = drop(t, 1.0, 360)
    if a > 0:
        hp = round(prog(t, 1.6, 0.5) * 20) / 20
        jx, jy, jr = jit('clip', t, 2, 0.5)
        place(c, clipping(hp), 540 + jx, 620 + dy + jy, 1.0, -3 + jr + (1 - a) * 8, a)
    tf = at(i, 'fell almost', -0.2)
    if t > tf:
        sc, a2 = slam(t, tf); place(c, stamp_c('-4.6% ON 18 NOV', RED, 72, -6, 11), 720, 880, sc, 0, a2)
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
    words_line(c, t, [("GOLD", GOLDD, T0 + 0.1), ("LOANS", INK, T0 + 0.3)], 'anton', 140, 300, key='gl')
    place_text(c, 'a Kerala company', 'mark', 56, RED, 540, 410, t, 'ker', at(i, 'from Kerala', -0.2), 'slide', rot=-3)
    if t > T0 + 0.3:
        necklace(c, 540, 700, 0.9, t, eo(prog(t, T0 + 0.3, 1.2)))
    steps = [('1', 'PLEDGE GOLD', 'your jewellery is the security', 'You pledge', GOLDD),
             ('2', 'CASH IN MINUTES', 'loan against the gold value', 'get cash', GRN),
             ('3', 'REPAY + INTEREST', 'and take your gold home', 'Pay back', BLUE)]
    for k, (n, tt_, sub, ph, col) in enumerate(steps):
        tk = at(i, ph, -0.3); pk = prog(t, tk, 0.45)
        if pk <= 0: continue
        jx, jy, jr = jit(('tk', k), t, 1.4, 0.25)
        place(c, step_ticket(n, tt_, sub, col), 540 + (1 - eo(pk)) * 900 + jx, 980 + k * 170 + jy, 0.92, (-1.2, 1.0, -0.6)[k] + jr)
    src(c, t, 'How a gold loan works (simplified)', T0 + 1.0, 1520)


def s3(c, t):
    i = 2; T0 = STARTS[i]
    words_line(c, t, [("GOLD", GOLDD, T0 + 0.1), ("LOAN BOOK", INK, T0 + 0.3)], 'anton', 120, 300, key='gb')
    d = ImageDraw.Draw(c); base = 1060
    ta = at(i, 'thirty one', -0.3); tb = at(i, 'sixty thousand', -0.3)
    for k, (lab, v, tk, col) in enumerate((('SEP 2025', 31505, ta, (200, 180, 140)), ('SEP 2026', 60640, tb, GOLDC))):
        if t < tk: continue
        ph = eo(prog(t, tk, 0.8)); hg = int(v / 60640 * 520 * ph); x = 330 + k * 420
        d.rounded_rectangle((x - 120, base - hg, x + 120, base), 16, fill=col, outline=INK, width=5)
        coins(c, x, base - hg - 10, 3 if k == 0 else 5, 0.7)
        place(c, text_img(f'₹{int(v * ph):,} Cr', 'anton', 58, INK), x, base - hg - 150)
        place(c, text_img(lab, 'osw5', 38, INK), x, base + 36)
    td = at(i, 'almost doubled', -0.2)
    if t > td:
        sc, a = slam(t, td); place(c, stamp_c('+92.5%', GRN, 100, -8, 21), 330, 450, sc, 0, a)
    src(c, t, 'Gold loan AUM, Q2 FY26 vs Q2 FY27 · results 12 Nov 2026', T0 + 1.0, 1440)


def s4(c, t):
    i = 3; T0 = STARTS[i]
    words_line(c, t, [("ENTER", INK, T0 + 0.1), ("BAIN CAPITAL", NAVY, T0 + 0.3)], 'anton', 120, 300, key='bc')
    tb = at(i, 'four thousand', -0.4)
    if t > tb:
        v = int(4385 * eo(prog(t, tb, 1.2)))
        place(c, text_img(f'₹{v:,} CR', 'anton', 150, NAVY), 540, 500)
        place_text(c, 'invested at ₹236 a share', 'mark', 50, INK, 540, 610, t, 'b236', tb + 0.5, 'slide', rot=-3)
    tr = at(i, 'now runs', -0.3)
    if t > tr:
        q = pp(t, tr, 0.35, 1.3)
        place(c, cutout(Image.new('RGBA', (900, 330), SOFT + (255,)), border=0, shadow=0.3), 540, 900, q, 1)
        if q > 0.6:
            c.alpha_composite(text_img('JOINT CONTROL · SINCE APRIL 2026', 'type', 28, GREY, 2), (120, 760))
            c.alpha_composite(text_img('FOUNDER FAMILY', 'anton', 64, INK), (120, 810))
            c.alpha_composite(text_img('+ BAIN CAPITAL', 'anton', 64, NAVY), (120, 900))
            c.alpha_composite(text_img('co-promoters, run the company together', 'osw5', 34, GREY), (120, 990))
        sc, a = slam(t, tr + 0.5); place(c, stamp_c('NEW BOSS', RED, 72, -8, 33), 800, 820, sc, 0, a)
    src(c, t, 'Bain Capital deal: RBI approval Mar 2026 · open offer closed 20 Apr 2026', T0 + 1.0, 1440)


def s5(c, t):
    i = 4; T0 = STARTS[i]
    dy, a = drop(t, T0 + 0.05, 300)
    if a > 0:
        hp = round(prog(t, T0 + 0.6, 0.5) * 20) / 20
        place(c, clipping(hp, 'LATEST RESULT', 'Q2 FY27 · 12 NOV 2026', 'MANAPPURAM · JUL-SEP 2026'), 540, 380 + dy, 0.82, -2, a)
    d = ImageDraw.Draw(c); base = 1150
    ta = at(i, 'two hundred', -0.3); tb = at(i, 'seven hundred', -0.3)
    for k, (lab, v, tk, col) in enumerate((('Q2 FY26', 217, ta, (200, 190, 175)), ('Q2 FY27', 701, tb, GRN))):
        if t < tk: continue
        ph = eo(prog(t, tk, 0.7)); hg = int(v / 701 * 450 * ph); x = 330 + k * 420
        d.rounded_rectangle((x - 110, base - hg, x + 110, base), 14, fill=col, outline=INK, width=5)
        place(c, text_img(f'₹{int(v * ph)} Cr', 'anton', 64, INK), x, base - hg - 44)
        place(c, text_img(lab, 'osw5', 38, INK), x, base + 36)
    tm = at(i, 'more than three', -0.3)
    if t > tm:
        sc, a = slam(t, tm); place(c, stamp_c('3.2x PROFIT', GRN, 84, -7, 41), 330, 800, sc, 0, a)
    src(c, t, 'Consolidated PAT · Manappuram Q2 FY27 results, 12 Nov 2026', T0 + 1.0, 1440)


def s6(c, t):
    i = 5; T0 = STARTS[i]
    words_line(c, t, [("THE", INK, T0 + 0.05), ("CATCH", RED, T0 + 0.25)], 'anton', 130, 300, key='ct')
    ta = at(i, 'A year ago', -0.3)
    if t > ta:
        q = pp(t, ta, 0.35, 1.3)
        place(c, cutout(Image.new('RGBA', (900, 470), SOFT + (255,)), border=0, shadow=0.3), 540, 700, q, -1)
        if q > 0.6:
            c.alpha_composite(text_img('ASIRVAD MICROFINANCE (SUBSIDIARY)', 'type', 26, GREY, 2), (120, 490))
            d = ImageDraw.Draw(c); zero = 700
            d.line((140, zero, 940, zero), fill=INK, width=4)
            for k, (lab, v, tk, col) in enumerate((('Q2 FY26', -168, at(i, 'lost', -0.3), RED), ('Q2 FY27', 32, at(i, 'it made', -0.3), GRN))):
                if t < tk: continue
                ph = eo(prog(t, tk, 0.6)); hg = int(abs(v) / 168 * 180 * ph); x = 360 + k * 360
                if v < 0: d.rounded_rectangle((x - 90, zero, x + 90, zero + hg), 12, fill=col, outline=INK, width=4); ly = zero + hg + 40
                else: d.rounded_rectangle((x - 90, zero - hg, x + 90, zero), 12, fill=col, outline=INK, width=4); ly = zero - hg - 40
                place(c, text_img(f'{"-" if v < 0 else "+"}₹{abs(int(v * ph))} Cr', 'anton', 56, col), x, ly)
                place(c, text_img(lab, 'osw5', 34, INK), x, zero - 24 if v < 0 else zero + 30)
    tb = at(i, 'bad year', -0.3)
    if t > tb:
        place_text(c, 'part of the jump = a bad year going away', 'mark', 40, RED, 540, 1040, t, 'by', tb, 'slide', rot=-3)
        marker_line(c, [(140, 1090), (540, 1082), (940, 1074)], prog(t, tb + 0.4, 0.4), RED, 8)
    src(c, t, 'Asirvad PAT ₹32 Cr vs loss ₹168 Cr a year ago · Q2 FY27 results', T0 + 1.0, 1440)


MONTHLY = [284.95, 308.55, 284.65, 283.25, 251.1, 294.35, 325.4, 324.2, 371.85, 340.1, 315.85, 289, 283]
MLAB = ['NOV 25', '', '', 'FEB', '', '', 'MAY', '', 'JUL', '', '', '', 'NOV 26']


def s7(c, t):
    i = 6; T0 = STARTS[i]
    words_line(c, t, [("RIDES ON", INK, T0 + 0.1), ("GOLD", GOLDD, T0 + 0.35)], 'anton', 130, 300, key='rg')
    tg = at(i, 'If gold falls', -0.3)
    if t > T0 + 0.3:
        s_ = 0.7; y = 560 + (12 * math.sin((t - tg) * 3) if t > tg else 0)
        necklace(c, 540, y, s_, t, 1.0)
        if t > tg:
            q = eo(prog(t, tg, 0.8))
            place(c, text_img('IF GOLD PRICE FALLS', 'anton', 64, RED), 540, 760, q)
            place(c, text_img('= less value behind each loan', 'osw5', 40, INK), 540, 830, q)
    ts = at(i, 'The stock', -0.3)
    if t > ts:
        p = prog(t, ts, 0.45); ox, oy = 60, 900 + (1 - eo(p)) * 500; w, h = 960, 480
        place(c, sheet_cut(w, h), ox + w / 2, oy + h / 2, 1.0, 0, clamp(p * 3))
        f = eio(prog(t, ts + 0.3, 1.8))
        hand_chart(c, t, ox, oy, w, h, MONTHLY, MLAB, 240, 390, f, INK, YEL)
        th = at(i, 'three hundred', -0.3)
        if t > th:
            x = ox + 90 + (w - 160) * 8 / 12; y = oy + h - 70 - (371.85 - 240) / 150 * (h - 140)
            marker_ellipse(c, x, y, 70, 46, prog(t, th, 0.45), RED, 7, seed=8)
            place_text(c, 'high ₹381', 'mark', 44, RED, x - 220, y - 10, t, 'hi', th + 0.2, 'slide', rot=-4)
        tf = at(i, 'twenty six', -0.3)
        if t > tf:
            sc, a = slam(t, tf); place(c, stamp_c('-26%', RED, 96, 8, 31), ox + 820, oy - 20, sc, 0, a)
    src(c, t, 'Monthly close · NSE via INDmoney · 18 Nov 2026 (₹283)', T0 + 1.0, 1440)


def s8(c, t):
    i = 7; T0 = STARTS[i]
    if t > T0 + 0.1:
        p = prog(t, T0 + 0.1, 0.3); lw = text_w('THE VERDICT', 'osw', 54, 2); x0 = 540 - (lw + 70) / 2
        place(c, warn_icon(YEL), x0 + 28, 262, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
        place(c, text_img('THE VERDICT', 'osw', 54, YEL, 2), x0 + 70 + lw / 2, 260, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
    tn = at(i, 'Right now', -0.2)
    words_line(c, t, [("STRONG,", CREAM, tn), ("BUT GOLD-LINKED.", YEL, tn + 0.35)], 'anton', 100, 420, key='ny')
    rows = [('Business is strong', 'gold book +92.5% · profit 3.2x', 'business is strong', GRN, True),
            ('Bain Capital on board', '₹4,385 Cr in · joint control', 'business is strong', GRN, True),
            ('Rides on gold', 'gold price falls = smaller loans', 'rides on gold', RED, False),
            ('Asirvad base effect', 'last year\'s loss flatters growth', 'watch Aashirvaad', RED, False)]
    for k, (h1, h2, ph, col, ok) in enumerate(rows):
        tk = at(i, ph, -0.3 + (0.6 if k == 1 else 0))
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
    if t > at(i, 'Aashirvaad', 0.5):
        place_text(c, 'watch: gold price + Asirvad', 'mark', 50, YEL, 540, 1500, t, 'w2', at(i, 'Aashirvaad', 0.5), 'slide', rot=-3)
    typed(c, 'Not investment advice. DYOR.', 'type', 30, (200, 194, 182), 1620, t, at(i, 'Aashirvaad', 0.8), at(i, 'Aashirvaad', 1.8))


def s9(c, t):
    i = 8; T0 = STARTS[i]
    q = pp(t, T0, 0.45, 1.2)
    place(c, SS._card(960, 860), 540, 600, q, -0.4)
    if q > 0.6:
        place(c, text_img('MANAPPURAM · CHEAT SHEET', 'anton', 52, INK), 540, 230)
        d = ImageDraw.Draw(c); d.line((90, 272, 990, 272), fill=INK, width=4)
        rows = [('Price (18 Nov)', '₹283', INK), ('From 52-wk high', '-26%', RED), ('Q2 profit', '₹701 Cr (3.2x)', GRN), ('Gold loan book', '₹60,640 Cr', GOLDD),
                ('Gold book growth', '+92.5%', GRN), ('Total AUM', '₹73,303 Cr', INK), ('Asirvad Q2', '+₹32 Cr', TEAL), ('Bain Capital', 'co-promoter', NAVY)]
        for k, (a_, b_, col) in enumerate(rows):
            tk = T0 + 0.3 + 0.08 * k
            if t < tk: continue
            y = 300 + k * 78
            c.alpha_composite(text_img(a_, 'osw5', 38, INK), (100, y))
            v = text_img(b_, 'anton', 44, col); c.alpha_composite(v, (980 - v.size[0], y - 2))
        SS.save_pulse(c, t, T0 + 1.2, 540, 1080, 'SAVE THIS')
    SS.send_frame(c, t, at(i, 'send it', -0.3), 'friends holding Manappuram', y=1300)
    tf = at(i, 'Follow', -0.2)
    if t > tf:
        q2 = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1530, 0.5 + 0.5 * eback(q2), 0, clamp(q2 * 3))
    for k, ln in enumerate(['Price: NSE via INDmoney, 18 Nov 2026', 'Results: Manappuram Q2 FY27 (12 Nov 2026) · Bain deal filings',
                            'Not a buy/sell call. Education only. I may hold some stocks named.']):
        place_text(c, ln, 'type', 22, GREY, 540, 1680 + k * 34, t, None, T0 + 0.3, 'fade', track=1)


def pp(t, t0, d=0.35, s=1.6): return eback(prog(t, t0, d), s)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
DARK_SCENES = {7}


def slam_times():
    return [at(0, 'trap', -0.2), at(2, 'almost doubled', -0.2), at(4, 'more than three', -0.3), at(5, 'bad year', -0.3), at(6, 'twenty six', -0.3)] + [STARTS[k] + 0.05 for k in range(1, 8)]


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
