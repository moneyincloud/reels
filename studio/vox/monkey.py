"""Animal Friday #3 - Monkey vs Elephant: overtrading (SEBI FY26 F&O study). Paper Vox v2, original animal characters."""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs, follow_btn
import tea as TEA
import saveshare as SS
import animals as A

import os
SH = ROOT + os.environ.get('LDIR', 'monkey') + '/'
CAPS_ON = False  # owner: NO subtitles
SCRIPT = json.load(open(SH + 'script.json'))
DURS = json.load(open(SH + 'vo/durs.json'))
LEAD, TAIL = 0.15, 0.3
HOLD = {7: 1.6}  # cheat-sheet freeze frame
STARTS, VO = [], []
_t = 0.0
for i, d in enumerate(DURS):
    STARTS.append(_t); VO.append(_t + (0.1 if i == 0 else LEAD)); _t = VO[-1] + d + TAIL + HOLD.get(i, 0)
DUR = _t + 1.8
B = STARTS[1:]
SOFT = (253, 251, 246); NAVY = (30, 60, 120); BLUE = (40, 100, 200); GREY = (120, 116, 108); GOLD = (214, 160, 40)
PINK = (230, 90, 140); TEAL = (20, 140, 130); ORG = (230, 120, 30)
card_box = TEA.card_box; label = TEA.label
def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def inr(v):
    v = int(round(v)); s = str(abs(v))
    if len(s) > 3:
        h, t3 = s[:-3], s[-3:]; parts = []
        while len(h) > 2: parts.insert(0, h[-2:]); h = h[:-2]
        if h: parts.insert(0, h)
        s = ','.join(parts) + ',' + t3
    return ('-' if v < 0 else '') + '₹' + s


def short(v):
    if v >= 1e7: return f'₹{v / 1e7:.2f} CR'
    if v >= 1e5: return f'₹{v / 1e5:.1f} L'
    return inr(v)


def pp(t, t0, d=0.35, s=1.6): return eback(prog(t, t0, d), s)


def src(c, t, txt, t0, y=1700, col=GREY, size=24):
    if t > t0: place_text(c, txt, 'type', size, col, 540, y, t, None, t0, 'fade', track=1)


def spark(c, pts, p, col, w=12):
    n = len(pts) - 1; f = p * n; k = int(f); out = pts[:k + 1]
    if k < n: a, b = pts[k], pts[k + 1]; fr = f - k; out = out + [(a[0] + (b[0] - a[0]) * fr, a[1] + (b[1] - a[1]) * fr)]
    if len(out) >= 2: stroke(c, out, w, col)


def step(t, rate=6): return int(t * rate) % 4


ACC = (205, 40, 50)  # theme red (HK.THEME_ACCENT['red'])
BR = [(200, 700), (870, 640), (240, 1080), (860, 1020)]  # branch anchor points (monkey feet)


def mk(c, t, x, y, mood='calm', pose='down', sc=0.6, walk=False, phone=False, a=1.0, rot=0):
    st = step(t, 10) if walk else 0
    bob = math.sin(t * 4 + 1) * 5
    place(c, A.monkey(mood, pose, st, 1.0, phone), x, y + bob, sc, rot + math.sin(t * 3) * 2, a)


def el(c, t, x, y, mood='happy', trunk=0, sc=0.6, a=1.0):
    br = math.sin(t * 1.6) * 0.012
    place(c, A.elephant(mood, trunk), x, y + math.sin(t * 1.6) * 3, sc * (1 + br), math.sin(t * 0.9) * 0.6, a)


def hopper(t, t0, pts, period=0.75, h=260):
    """monkey position hopping along pts in a loop; returns x, y, airborne, jump index"""
    if t < t0: return pts[0][0], pts[0][1], False, 0
    f = (t - t0) / period; k = int(f); q = f - k
    a = pts[k % len(pts)]; b = pts[(k + 1) % len(pts)]
    if q < 0.35: return a[0], a[1] + 8 * math.sin(q / 0.35 * math.pi), False, k
    q = (q - 0.35) / 0.65; e = eio(q)
    return a[0] + (b[0] - a[0]) * e, a[1] + (b[1] - a[1]) * e - h * math.sin(math.pi * q), True, k


def branches(c, ys=((700, False), (640, True), (1080, False), (1020, True))):
    for k, (y, fl) in enumerate(ys):
        x = 300 if not fl else 780
        place(c, A.branch(620, fl), x, y + 60)


def mhop(c, t, t0, pts, period=0.75, mood='happy', sc=0.42, phone=True, h=260):
    x, y, air, k = hopper(t, t0, pts, period, h)
    pose = 'both_up' if air else 'down'
    mk(c, t, x, y - 150, mood, pose, sc, phone=phone and not air, rot=(-12 if air else 0))
    return k, air, x, y


@functools.lru_cache(None)
def qmark(col=RED):
    return cutout(text_img('?', 'anton', 260, col), border=8, shadow=0.35)


@functools.lru_cache(None)
def dot_grid_cell(col):
    im = Image.new('RGBA', (62, 62), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((4, 4, 58, 58), fill=col, outline=INK, width=4)
    d.ellipse((14, 18, 26, 30), fill=INK); d.ellipse((36, 18, 48, 30), fill=INK)
    return im


def grid100(c, t, t0, nred, x0=150, y0=640, step_=78, red_t0=None, red_dur=2.0):
    """100 trader faces; nred turn red one by one from red_t0"""
    for k in range(100):
        tk = t0 + k * 0.006
        if t < tk: continue
        r_, c_ = divmod(k, 10)
        col = (200, 196, 186)
        if red_t0 is not None and t > red_t0:
            if k < nred and t > red_t0 + red_dur * k / nred: col = RED
            elif k >= nred and t > red_t0 + red_dur: col = GRN
        s = eback(prog(t, tk, 0.25), 1.5)
        place(c, dot_grid_cell(col), x0 + c_ * step_, y0 + r_ * step_, s)


# ---------------- scenes ----------------
def s1(c, t):
    i = 0
    tl = at(i, 'lost money', -0.2)
    q = eo(prog(t, 0.0, max(0.9, tl + 0.3)))
    place(c, card_box(940, 330, SOFT), 540, 360, 1.0, -1)
    place(c, text_img('OF F&O TRADERS', 'osw5', 50, GREY), 540, 250)
    jx = math.sin(t * 50) * 4 * (1 - q)
    place(c, text_img(f'{int(round(88 * q))}%', 'anton', 200, RED), 540 + jx, 400)
    if t > tl:
        s_, a = slam(t, tl); place(c, stamp_c('LOST MONEY', RED, 96, -7, 31), 760, 590, s_, 0, a)
    # monkey hopping between two branches from frame 0
    place(c, A.branch(560), 290, 1110); place(c, A.branch(560, True), 790, 990)
    pts = [(250, 1060), (820, 940)]
    k, air, x, y = mhop(c, t, 0.0, pts, 0.6, 'happy' if t < tl + 0.3 else 'cry', 0.55)
    if air: place(c, A.fee_coin('₹'), x, y + 40 + 120 * ((t * 3) % 1), 0.5)
    tn = at(i, 'Never', -0.1)
    if t > tn: place(c, label("DON'T TRADE LIKE THIS", NAVY), 540, 1500, 1.4 * pp(t, tn), -2)
    src(c, t, 'SEBI study, individual F&O traders, FY 2025-26', 0.6, 1640, GREY, 26)


def s2(c, t):
    i = 1; T0 = STARTS[i]
    place_text(c, 'MEET MONKEY', 'anton', 110, INK, 540, 230, t, 'mm', T0 + 0.05, 'pop')
    branches(c)
    pts = [BR[0], BR[1], BR[2], BR[3]]
    tj = at(i, 'jumps', -0.3)
    if t < tj:
        mk(c, t, BR[0][0], BR[0][1] - 150, 'happy', 'point', 0.42, phone=True)
        njump = 0
    else:
        k, air, x, y = mhop(c, t, tj, pts, 0.7, h=170); njump = k + 1
    place(c, card_box(330, 150, SOFT), 820, 1330, pp(t, tj), 2)
    if t > tj:
        place(c, text_img('JUMPS', 'osw5', 34, GREY), 820, 1290)
        place(c, text_img(str(njump), 'anton', 80, RED), 820, 1350)
    for k, (w, col, x, y, rt) in enumerate((('BUY', GRN, 230, 1300, -6), ('SELL', RED, 470, 1380, 5), ('OPTIONS', ORG, 300, 1520, -3), ('AGAIN', NAVY, 650, 1560, 4))):
        tk = at(i, {'BUY': 'Buy', 'SELL': 'sell', 'OPTIONS': 'options', 'AGAIN': 'again'}[w], -0.15)
        if t > tk:
            s_, a = slam(t, tk); place(c, stamp_c(w + '!', col, 70, rt, 40 + k), x, y, s_, 0, a)
    th = at(i, 'hard work', -0.3)
    if t > th:
        place(c, label('BUSY = HARD WORK?', ACC), 540, 1680, 1.2 * pp(t, th), -2)


def s3(c, t):
    i = 2; T0 = STARTS[i]
    place(c, A.tree(), 540, 900, 1.05)
    te = at(i, 'Elephant', -0.4)
    if t > te:
        p = pp(t, te, 0.5, 1.3); el(c, t, 540, 1290, 'happy', 0, 0.62 * p)
        place(c, label('ELEPHANT', TEAL), 830, 1560, 1.2 * pp(t, te + 0.3), 3)
    tb = at(i, 'barely moves', -0.2)
    if t > tb:
        place_text(c, 'barely moves', 'mark', 56, TEAL, 260, 1560, t, 'bm', tb, 'slide', rot=-4)
        place(c, text_img('Zz', 'anton', 60 + 6 * math.sin(t * 3), GREY), 760, 1000 - 12 * ((t * 0.7) % 1))
    k, air, x, y = mhop(c, t, T0, [(300, 640), (780, 600)], 0.65, 'happy', 0.36, h=150)
    tm = at(i, 'Most people', -0.3)
    if t > tm:
        p = pp(t, tm, 0.4, 1.3)
        place(c, card_box(900, 190, YEL), 540, 250, p, -1)
        if p > 0.6:
            place(c, text_img('BUSY MONKEY = WINNING?', 'anton', 70, INK), 500, 250)
            place(c, qmark(RED), 940, 250 + math.sin(t * 6) * 8, 0.36, 10)


def s4(c, t):
    i = 3; T0 = STARTS[i]
    if t - T0 < 0.3: c.alpha_composite(Image.new('RGBA', c.size, (255, 214, 51, int(200 * (1 - (t - T0) / 0.3)))))
    s_, a = slam(t, T0 + 0.08); place(c, stamp_c('BUT…', RED, 160, -6, 61), 540, 330, s_, 0, a)
    place_text(c, 'the part nobody tells you', 'mark', 58, NAVY, 540, 500, t, 'pn', T0 + 0.4, 'slide', rot=-2)
    branches(c, ((980, False), (920, True)))
    tp = at(i, 'Every single', -0.3)
    pts = [(250, 1040), (830, 980)]
    if t > tp:
        k, air, x, y = mhop(c, t, tp, pts, 0.55, 'wow', 0.4, h=200)
        # fee coins fall out on every jump
        for j in range(k + 1):
            tj = tp + j * 0.55 + 0.25
            if t > tj:
                q = clamp((t - tj) / 0.7); xx = pts[j % 2][0] + (pts[(j + 1) % 2][0] - pts[j % 2][0]) * 0.5 + (j % 3 - 1) * 60
                yy = 980 + 440 * q * q
                if q < 1: place(c, A.fee_coin(), xx, yy, 0.6, q * 200)
        nc = sum(1 for j in range(k + 1) if t > tp + j * 0.55 + 0.95)
        if nc: SS.coin_stack(c, t, tp + 1.0, min(nc, 10), 540, 1420, 170)
    else:
        mk(c, t, 250, 1040 - 150, 'calm', 'down', 0.4, phone=True)
    tw = at(i, 'even the winning', -0.3)
    if t > tw:
        place(c, label('EVEN THE WINNING JUMPS', ACC), 540, 1600, 1.25 * pp(t, tw), -2)
    place(c, qmark(RED), 940, 1250 + math.sin(t * 7) * 12, 0.45 * pp(t, T0 + 0.3), -6 + math.sin(t * 4) * 4)


def s5(c, t):
    i = 4; T0 = STARTS[i]
    s_, a = slam(t, T0 + 0.05); place(c, stamp_c('SEBI STUDY', NAVY, 120, -5, 71), 540, 270, s_, 0, a)
    ti = at(i, 'every individual', -0.3)
    if t > ti:
        place_text(c, 'EVERY INDIVIDUAL F&O TRADER', 'anton', 66, INK, 540, 450, t, 'ei', ti, 'pop')
    grid100(c, t, ti, 88)
    ty = at(i, 'for the year', -0.3)
    if t > ty:
        place(c, label('APRIL 2025 – MARCH 2026 (FY26)', ACC), 540, 1490, 1.15 * pp(t, ty), -1.5)
    if t > ty + 0.6:
        place(c, label('87.5 LAKH ACTIVE TRADERS', NAVY), 540, 1610, 1.05 * pp(t, ty + 0.6), 1.5)
    src(c, t, 'SEBI F&O study FY26 · Business Today, 21 Aug 2026', ti + 0.3, 1720, GREY, 22)


def s6(c, t):
    i = 5; T0 = STARTS[i]
    te = at(i, 'Eighty eight', -0.2)
    grid100(c, t, T0 - 1, 88, x0=150, y0=230, step_=62, red_t0=te, red_dur=1.6)
    v = int(round(88 * eo(prog(t, te, 1.6)))) if t > te else 0
    place(c, card_box(420, 200, SOFT), 760, 900, pp(t, te), 2)
    if t > te:
        place(c, text_img(f'{v}%', 'anton', 120, RED), 760, 880); place(c, text_img('LOST MONEY', 'osw5', 34, GREY), 760, 970)
        mk(c, t, 270, 940, 'cry' if t > te + 1.0 else 'wow', 'head', 0.42)
    tt = at(i, 'Together', -0.3); tn = at(i, 'ninety one', -0.3)
    if t > tt:
        p = pp(t, tt, 0.4, 1.3); place(c, card_box(940, 230, SOFT), 540, 1210, p, -1)
        if p > 0.6:
            place(c, text_img('TOTAL LOST IN ONE YEAR', 'osw5', 38, GREY), 540, 1135)
            vv = SS.roll_number(t, tn, 2.0, 0, 91685) if t > tn else 0
            place(c, text_img(f'₹{int(vv):,} CR'.replace('₹91,685', '₹91,685'), 'anton', 104, RED), 540, 1230)
    ta = at(i, 'The average', -0.3)
    if t > ta:
        p = pp(t, ta, 0.4, 1.3); place(c, card_box(800, 200, YEL), 540, 1480, p, 1)
        if p > 0.6:
            place(c, text_img('AVERAGE LOSER', 'osw5', 38, INK), 540, 1420)
            ts = at(i, 'one lakh', -0.3)
            vv = SS.roll_number(t, ts, 1.2, 0, 147000) if t > ts else 0
            place(c, text_img('-' + inr(vv) if vv else '₹ ?', 'anton', 96, RED), 540, 1505)
    if t > ta + 2.2:
        s_, a = slam(t, ta + 2.2); place(c, stamp_c('IN ONE YEAR', RED, 60, -8, 81), 860, 1600, s_, 0, a)
    src(c, t, 'SEBI FY26 study: 87.7% had net losses · Business Today, 21 Aug 2026', te + 0.4, 1720, GREY, 22)


def s7(c, t):
    i = 6; T0 = STARTS[i]
    words_line(c, t, [("THE", INK, T0 + 0.05), ("JUMP", ACC, T0 + 0.2), ("FEES", ACC, T0 + 0.35)], 'anton', 120, 250, key='jf')
    tf = at(i, 'twenty four', -0.3)
    place(c, A.jar(round(clamp((t - T0) / 4) * 8) / 8 * 0.9, 'FEES'), 230, 560, 1.05 * pp(t, T0 + 0.2), -3)
    for k in range(6):
        tk = T0 + 0.4 + k * 0.4
        if tk < t < tk + 0.5:
            q = (t - tk) / 0.5; place(c, A.fee_coin('₹'), 230, 300 + 240 * q * q, 0.4)
    if t < at(i, 'Options alone', -0.3):
        branches(c, ((1400, False), (1340, True)))
        mhop(c, t, T0, [(250, 1460), (830, 1400)], 0.6, 'wow', 0.36, h=200)
    if t > tf:
        p = pp(t, tf, 0.4, 1.3); place(c, card_box(560, 260, SOFT), 680, 560, p, 1.5)
        if p > 0.6:
            place(c, text_img('COSTS PAID IN FY26', 'osw5', 32, GREY), 680, 470)
            vv = SS.roll_number(t, tf, 1.8, 0, 24800)
            place(c, text_img(f'₹{int(vv):,} CR', 'anton', 92, RED), 680, 565)
            place(c, text_img('about', 'mark', 36, GREY), 680, 640)
    tb = at(i, 'brokerage', -0.3)
    for k, (txt, col) in enumerate((('BROKERAGE 44%', NAVY), ('STT 27%', ORG), ('EXCHANGE 16%', TEAL), ('GST 11%', GREY))):
        tk = tb + 0.25 * k
        if t > tk: place(c, label(txt, col), (300, 760, 300, 760)[k], (850, 850, 960, 960)[k], 1.0 * pp(t, tk), (-3, 2, 2, -3)[k])
    to = at(i, 'Options alone', -0.3)
    if t > to:
        p = pp(t, to, 0.4, 1.3); place(c, card_box(940, 420, SOFT), 540, 1340, p, -0.6)
        if p > 0.6:
            place(c, text_img('SHARE OF ALL LOSSES', 'osw5', 38, GREY), 540, 1180)
            q = eo(prog(t, to + 0.3, 1.4)); d = ImageDraw.Draw(c)
            d.rounded_rectangle((120, 1240, 960, 1340), 18, fill=(225, 220, 210), outline=INK, width=5)
            d.rounded_rectangle((120, 1240, 120 + 840 * 0.92 * q, 1340), 18, fill=RED, outline=INK, width=5)
            place(c, text_img(f'OPTIONS {int(round(92 * q))}%', 'anton', 64, CREAM if q > 0.5 else INK), 380, 1290)
            place(c, text_img('everything else 8%', 'type', 26, GREY, 1), 760, 1400)
            mk(c, t, 880, 1500, 'cry', 'head', 0.26)
    src(c, t, 'SEBI FY26 study · Business Today, 21-22 Aug 2026', T0 + 0.6, 1720, GREY, 21)


def s8(c, t):
    i = 7; T0 = STARTS[i]
    tm = at(i, 'More jumps', -0.35); tc = at(i, 'Each trader', -0.3); tb = at(i, 'Busy is not', -0.3)
    if t < tc:
        place_text(c, 'the lesson', 'mark', 70, NAVY, 540, 230, t, 'ls', T0 + 0.05, 'slide', rot=-2)
        SS.myth_fact(c, t, max(T0 + 0.3, tm), ['More jumps', '= more', 'money'], ['88% of', 'traders', 'lost money'], y0=300, y1=1560)
        if t > tm + 1.0: el(c, t, 780, 1400, 'happy', 1, 0.3)
        mk(c, t, 300, 1480, 'sad', 'down', 0.26)
    else:
        SS.cheat_sheet(c, t, tc, 'MONKEY vs ELEPHANT', [
            ('F&O TRADERS WHO LOST', '88%', RED), ('TOTAL LOSS FY26', '₹91,685 CR', RED),
            ('AVERAGE LOSER', '-₹1.47 L', RED), ('COSTS PER TRADER', '₹31,628', ORG), ('RULE', 'FEWER JUMPS', TEAL)], y0=260)
        if t > tb:
            mk(c, t, 260, 1500, 'sad', 'down', 0.28); el(c, t, 820, 1520, 'happy', 1, 0.3)
        src(c, t, 'SEBI FY26: avg cost ₹31,628 per trader · Business Today, 21 Aug 2026', tc + 0.4, 1700, GREY, 24)


def s9(c, t):
    i = 8; T0 = STARTS[i]
    SS.send_frame(c, t, T0 + 0.05, "your options-trading friend", y=400)
    ts = at(i, 'Save this', -0.3)
    if t > ts:
        p = pp(t, ts, 0.4, 1.8); bob = math.sin((t - ts) * 7) * 8 * math.exp(-(t - ts) * 0.8)
        place(c, SS.bookmark_icon(100), 340, 680 + bob, p, -8)
        place(c, text_img('SAVE THIS', 'anton', 84, CREAM), 590, 680, p)
    tfo = at(i, 'follow', -0.2)
    if t > tfo:
        q = prog(t, tfo, 0.35); place(c, follow_btn(), 540, 860, 0.5 + 0.5 * eback(q), 0, clamp(q * 3))
    tmb = at(i, 'The monkey was', -0.3); tep = at(i, 'The elephant was', -0.3)
    if t > tmb:
        mk(c, t, 290, 1180, 'sad', 'down', 0.36, phone=True)
        place(c, label('BUSY', RED), 290, 1430, 1.3 * pp(t, tmb + 0.2), -3)
    if t > tep:
        el(c, t, 780, 1220, 'happy', 1, 0.4)
        place(c, label('PATIENT', GRN), 780, 1430, 1.3 * pp(t, tep + 0.2), 3)
    for k, ln in enumerate(['Data: SEBI F&O study, FY26 (Business Today, 21 Aug 2026).',
                            'Fictional characters. Past data, not a forecast.',
                            'No buy/sell call. Education only, not investment advice.']):
        place_text(c, ln, 'type', 21, (210, 204, 192), 540, 1560 + k * 38, t, None, T0 + 0.3, 'fade', track=1)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]


def SLAMS():
    return [at(0, 'lost money', -0.2), STARTS[3] + 0.08, STARTS[4] + 0.05, at(5, 'Together', 0.0), at(6, 'Options alone', 0.0)] + \
           [at(1, w, -0.15) for w in ('Buy', 'sell', 'options', 'again')] + [STARTS[k] + 0.05 for k in (1, 2, 5, 6, 7)]
def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('ANIMAL FRIDAY', 'type', 30, ACC if not dark else YEL, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
    ImageDraw.Draw(c).line((60, 118, W - 60, 118), fill=col, width=2)
    ImageDraw.Draw(c).line((60, 118, 60 + (W - 120) * clamp(t / DUR), 118), fill=RED if not dark else YEL, width=8)


def transition(c, t):
    cols = [(GRN, INK), (GOLD, INK), (RED, YEL), (YEL, INK), (TEAL, CREAM), (NAVY, CREAM), (GRN, YEL), (INK, RED), (YEL, NAVY)]
    for bi, b in enumerate(B):
        d = 0.5
        if abs(t - b) > d / 2 + 0.12: continue
        for layer, delay in ((0, -0.05), (1, 0.0)):
            p = (t - (b - d / 2) - delay) / d
            if p <= 0 or p >= 1: continue
            p = eio(p); SWd, skew = 2050, 320
            xl = (W + 60) + p * (-(SWd + skew) - (W + 60) - 40)
            r = random.Random(bi * 10 + layer + 7900)
            left = [(xl + r.uniform(-14, 14) - skew * (y / H), y) for y in range(0, H + 1, 40)]
            right = [(xl + SWd + r.uniform(-14, 14) - skew * (y / H), y) for y in range(H, -1, -40)]
            if layer == 0:
                left = [(x - 70, y) for x, y in left]; right = [(x + 70, y) for x, y in right]
            poly_fill(c, left + right, cols[bi % len(cols)][layer], 255, S=1)


def slam_times(): return SLAMS()


def scene_at(t):
    k = 0
    for i, s in enumerate(STARTS):
        if t >= s: k = i
    return k


def render(t):
    LOOP = 0.6
    if t > DUR - LOOP:
        a = _render(t); b = _render(1.15, loop=True); q = eio((t - (DUR - LOOP)) / LOOP)
        return (a * (1 - q) + b * q).astype(np.uint8)
    return _render(t)


def _render(t, loop=False):
    pbg, dbg = bgs()
    i = scene_at(t); dark = (i == 8)
    c = (dbg if dark else pbg).copy()
    st = STARTS[i]; en = STARTS[i + 1] if i + 1 < len(STARTS) else DUR
    SCENES[i](c, t)
    z = 1.0 + 0.035 * clamp((t - st) / (en - st))
    sx = sy = 0
    for ts in slam_times():
        if 0 <= t - ts < 0.35:
            k = math.exp(-(t - ts) * 14) * 8
            sx += k * math.sin((t - ts) * 90); sy += k * math.cos((t - ts) * 77)
    cw, ch = W / z, H / z
    cx, cy = W / 2 + sx, max(ch / 2, H * 0.47) + sy
    c = c.transform((W, H), Image.EXTENT, (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2), Image.BICUBIC)
    header(c, dark, t if not loop else 0); transition(c, t)
    arr = np.asarray(c.convert('RGB')).astype(np.float32)
    g = grain_frames()[int(t * FPS) % 6]
    fl = 1 + 0.012 * math.sin(t * 37) * math.sin(t * 13)
    return np.clip(arr * fl + g[..., None], 0, 255).astype(np.uint8)
