"""Animal Friday #1 - Tortoise vs Hare: time beats amount (compounding). Paper Vox v2, original animal characters."""
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
SH = ROOT + os.environ.get('LDIR', 'tortoise') + '/'
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
CLOSES = json.load(open(ROOT + 'tortoise/closes.json'))['NIFTY']

# illustrative compounding (10% a year, monthly SIP, start of month) - same maths as the caption
R = 0.10 / 12


def sip_path(amt, start_age):
    v, out = 0.0, []
    for m in range((55 - 25) * 12 + 1):
        age = 25 + m / 12
        out.append(v)
        if age >= start_age and m < 360: v = (v + amt) * (1 + R)
    return out


TORT = sip_path(5000, 25); HARE = sip_path(10000, 35)
T_END, H_END = TORT[-1], HARE[-1]   # 1,13,96,627 and 76,56,969


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


def tort(c, t, x, y, mood='calm', sc=0.7, walk=False, shades=False, a=1.0, rot=0):
    st = step(t) if walk else 0
    bob = math.sin(t * 3) * 4 + (abs(math.sin(t * 6)) * -6 if walk else 0)
    place(c, A.tortoise(mood, st, 1.0, shades), x, y + bob, sc, rot + math.sin(t * 2) * 0.8, a)


def hr(c, t, x, y, mood='calm', pose='down', sc=0.6, walk=False, a=1.0, rot=0):
    st = step(t, 10) if walk else 0
    bob = math.sin(t * 3.3 + 1) * 5 + (abs(math.sin(t * 10)) * -14 if walk else 0)
    place(c, A.hare(mood, pose, st), x, y + bob, sc, rot + math.sin(t * 2.4) * 1.0, a)


def ground(c, y=1420, x0=60, x1=1020):
    d = ImageDraw.Draw(c); d.line((x0, y, x1, y), fill=INK, width=5)
    for x in range(x0 + 20, x1, 70): d.line((x, y + 14, x + 30, y + 14), fill=(190, 180, 160), width=4)


@functools.lru_cache(None)
def cal(txt, col=RED):
    w, h = 300, 210
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 16, fill=SOFT, outline=INK, width=6)
    d.rectangle((0, 0, w - 1, 56), fill=col, outline=INK, width=6)
    for x in (70, 230): d.ellipse((x - 12, -10, x + 12, 14), fill=INK)
    t1 = text_img('AGE', 'type', 26, CREAM, 2); im.alpha_composite(t1, (w // 2 - t1.size[0] // 2, 12))
    t = text_img(txt, 'anton', 110, INK); im.alpha_composite(t, (w // 2 - t.size[0] // 2, 64))
    return cutout(im, border=6, shadow=0.35)


@functools.lru_cache(None)
def qmark(col=RED):
    return cutout(text_img('?', 'anton', 260, col), border=8, shadow=0.35)


def coin_drop(c, t, t0, x, y, n=6, gap=0.22):
    for k in range(n):
        tk = t0 + k * gap
        if tk < t < tk + 0.5:
            q = (t - tk) / 0.5; yy = y - 260 + 260 * q * q
            d = ImageDraw.Draw(c); d.ellipse((x - 26, yy - 26, x + 26, yy + 26), fill=GOLD, outline=INK, width=5)
            d.text((x - 9, yy - 18), '₹', fill=INK, font=font('anton', 30))


# ---------------- scenes ----------------
def s1(c, t):
    i = 0
    # frame 0: the loss counter is already rolling (biggest element, moving)
    tl = at(i, 'still lost', -0.2)
    q = eo(prog(t, 0.0, max(0.8, tl + 0.4)))
    v = 3700000 * q
    place(c, card_box(940, 300, SOFT), 540, 400, 1.0, -1)
    place(c, text_img('HARE LOST', 'osw5', 52, GREY), 540, 300)
    jx = math.sin(t * 50) * 4 * (1 - q)
    place(c, text_img('-' + inr(v), 'anton', 170, RED), 540 + jx, 425)
    if t > tl:
        s_, a = slam(t, tl); place(c, stamp_c('STILL LOST', RED, 96, -7, 31), 760, 600, s_, 0, a)
    ground(c, 1430)
    ti = at(i, 'invested more', -0.3)
    mood = 'cry' if t > tl + 0.2 else 'happy'
    hr(c, t, 300, 1010, mood, 'head' if mood == 'cry' else 'up', 0.8)
    if t > ti:
        place(c, A.bag('₹'), 560, 1290 - (0 if t > tl else 30 * math.sin(t * 6)), 0.75 * pp(t, ti), -6)
        place(c, label('+₹6 LAKH MORE', ORG), 330, 700, 1.1 * pp(t, ti + 0.15), -3)
    if t > tl + 0.1:
        p = prog(t, tl + 0.1, 0.6)
        tort(c, t, 800 + (1 - eo(p)) * 500, 1300, 'happy', 0.7, walk=p < 1, shades=True)
        place(c, A.finish_flag(), 990, 1270, 0.8 * pp(t, tl + 0.3), 3)
    ty = at(i, 'You might', -0.25)
    if t > ty:
        sh = math.sin(t * 40) * 6 * math.exp(-(t - ty) * 3)
        place(c, label('YOU MIGHT TOO', NAVY), 540 + sh, 1560, 1.5 * pp(t, ty), -2)


def s2(c, t):
    i = 1; T0 = STARTS[i]
    place_text(c, 'MEET THE RACERS', 'anton', 110, INK, 540, 260, t, 'mr', T0 + 0.05, 'pop')
    ground(c, 1010)
    tt = at(i, 'Tortoise and', -0.3); th = at(i, 'and Hare', -0.1)
    if t > tt:
        p = prog(t, tt, 0.9); tort(c, t, 290 - (1 - eo(p)) * 600, 900, 'happy', 0.62, walk=p < 1)
        place(c, label('TORTOISE', GRN), 290, 1080, 1.2 * pp(t, tt + 0.3), -3)
    if t > th:
        p = prog(t, th, 0.5); hr(c, t, 800 + (1 - eo(p)) * 600, 720, 'happy', 'hips', 0.55, walk=p < 1)
        place(c, label('HARE', RED), 800, 1080, 1.2 * pp(t, th + 0.3), 3)
    tr = at(i, 'retire', -0.3)
    if t > tr:
        place(c, A.finish_flag(), 545, 640, 0.75 * pp(t, tr), 2)
        place(c, label('GOAL: RETIRE AT 55', NAVY), 540, 420, 1.3 * pp(t, tr + 0.1), -1)
    ta = at(i, 'starts at twenty five', -0.2)
    if t > ta:
        place(c, cal('25', GRN), 250, 1320, pp(t, ta), -4)
    tf = at(i, 'five thousand', -0.3)
    if t > tf:
        lv = round(clamp((t - tf) / 2.2) * 8) / 8 * 0.85
        place(c, A.jar(lv, 'SIP'), 560, 1340, 0.9 * pp(t, tf), 2)
        coin_drop(c, t, tf + 0.2, 560, 1290, 8, 0.25)
        place(c, label('₹5,000 / MONTH', GRN), 840, 1300, 1.15 * pp(t, tf + 0.2), 4)
        src(c, t, 'every month, from age 25', tf + 0.5, 1490, GREY, 26)
    if t > ta + 1.0:
        place(c, qmark(RED), 900, 1560 + math.sin(t * 5) * 10, 0.45 * pp(t, ta + 1.0), 8)
        place_text(c, 'who wins?', 'mark', 56, RED, 700, 1590, t, 'ww', ta + 1.1, 'slide', rot=-3)


def s3(c, t):
    i = 2; T0 = STARTS[i]
    tl = at(i, 'laughs', -0.3)
    hr(c, t, 330, 900, 'happy', 'hips' if t < at(i, 'ten thousand', -0.3) else 'up', 0.72)
    if t > tl:
        for k, (x, y) in enumerate(((170, 430), (330, 380), (490, 450))):
            if t > tl + 0.15 * k: place_text(c, 'HA!', 'anton', 80 + 10 * k, RED, x + math.sin(t * 8 + k) * 6, y, t, ('ha', k), tl + 0.15 * k, 'pop', rot=(-8, 6, -3)[k])
    t35 = at(i, 'thirty five', -0.3)
    if t > t35:
        flip = '25' if t < t35 + 0.35 else '35'
        place(c, cal(flip, RED), 840, 480, pp(t, t35), 4)
        place(c, label('STARTS 10 YEARS LATER', ORG), 690, 760, 1.05 * pp(t, t35 + 0.35), -2)
    t10 = at(i, 'ten thousand', -0.3)
    if t > t10:
        place(c, A.bag('₹'), 760, 1020, 0.85 * pp(t, t10), 5)
        place(c, label('₹10,000 / MONTH', RED), 760, 1220, 1.2 * pp(t, t10 + 0.1), 3)
    td = at(i, 'double', -0.25)
    if t > td:
        s_, a = slam(t, td); place(c, stamp_c('2X MONEY', RED, 110, -8, 51), 760, 1380, s_, 0, a)
    tm = at(i, 'Most people', -0.3)
    if t > tm:
        p = pp(t, tm, 0.4, 1.3)
        place(c, card_box(880, 190, YEL), 540, 1600, p, -1)
        if p > 0.6:
            place(c, text_img('HARE WINS EASILY?', 'anton', 80, INK), 500, 1600)
            place(c, qmark(RED), 900, 1590 + math.sin(t * 6) * 8, 0.38, 10)


def s4(c, t):
    i = 3; T0 = STARTS[i]
    if t - T0 < 0.3: c.alpha_composite(Image.new('RGBA', c.size, (255, 214, 51, int(200 * (1 - (t - T0) / 0.3)))))
    s_, a = slam(t, T0 + 0.08); place(c, stamp_c('BUT WAIT…', RED, 150, -6, 61), 540, 380, s_, 0, a)
    ground(c, 1150)
    p = prog(t, T0 + 0.2, 2.4)
    hx = 140 + 900 * eio(min(1, p * 1.6))
    hr(c, t, hx, 880, 'happy', 'down', 0.5, walk=True)
    tort(c, t, 200 + 180 * p, 1060, 'calm', 0.5, walk=True)
    place(c, A.finish_flag(), 990, 1020, 0.8, 2)
    tr = at(i, 'race', -0.3)
    if t > tr: place_text(c, "this race doesn't end the way you think", 'mark', 52, NAVY, 540, 1300, t, 'rc', tr, 'slide', rot=-2)
    place(c, qmark(RED), 540, 1540 + math.sin(t * 7) * 12, 0.7 * pp(t, T0 + 0.3), -6 + math.sin(t * 4) * 4)


def bar_col(c, t, t0, x, v, col, who, sub, maxv=2400000, base=1500, hpx=520):
    if t < t0: return
    q = eo(prog(t, t0, 1.2)); h = hpx * v / maxv * q
    d = ImageDraw.Draw(c)
    d.rounded_rectangle((x - 120, base - h, x + 120, base), 16, fill=col, outline=INK, width=6)
    for y in range(int(base - 30), int(base - h + 10), -36): d.line((x - 100, y, x + 100, y), fill=tuple(max(0, k - 40) for k in col), width=3)
    place(c, text_img(short(v * q) if q < 1 else short(v).replace('.0', ''), 'anton', 84, INK), x, base - h - 60)
    place(c, text_img(sub, 'osw5', 38, GREY), x, base + 50)


def s5(c, t):
    i = 4; T0 = STARTS[i]
    s_, a = slam(t, T0 + 0.05); place(c, stamp_c('AGE 55', NAVY, 130, -5, 71), 330, 280, s_, 0, a)
    place_text(c, 'MONEY PUT IN', 'anton', 70, INK, 770, 280, t, 'pi', T0 + 0.3, 'pop')
    tort(c, t, 300, 760, 'calm', 0.45)
    hr(c, t, 780, 700, 'happy' if t > at(i, 'twenty four', 0.4) else 'calm', 'hips', 0.4)
    d = ImageDraw.Draw(c); d.line((100, 1500, 980, 1500), fill=INK, width=6)
    bar_col(c, t, at(i, 'eighteen lakh', -0.3), 300, 1800000, GRN, 'T', '₹5,000 × 30 YEARS')
    bar_col(c, t, at(i, 'twenty four', -0.3), 780, 2400000, RED, 'H', '₹10,000 × 20 YEARS')
    tm = at(i, 'twenty years', 0.4)
    if t > tm: place(c, label('HARE PUT IN ₹6 LAKH MORE', ORG), 540, 1650, 1.15 * pp(t, tm), -2)


def s6(c, t):
    i = 5; T0 = STARTS[i]
    place_text(c, 'THE FINAL COUNT', 'anton', 110, INK, 540, 260, t, 'fc', T0 + 0.05, 'pop')
    ti = at(i, 'At ten percent', -0.3)
    ox, oy, w, h = 90, 370, 900, 600
    if t > ti:
        p = pp(t, ti, 0.45, 1.3); place(c, card_box(w, h, SOFT), ox + w / 2, oy + h / 2, p, -0.5)
        if p > 0.7:
            place(c, text_img('ILLUSTRATION · 10% A YEAR · NOT A PROMISE', 'type', 26, RED, 1), 540, oy + 40)
            X = lambda m: ox + 80 + (w - 140) * m / 360
            Y = lambda v: oy + h - 70 - (h - 150) * v / 1.2e7
            d = ImageDraw.Draw(c); d.line((ox + 70, oy + h - 70, ox + w - 50, oy + h - 70), fill=INK, width=4)
            for age in (25, 35, 45, 55):
                xx = X((age - 25) * 12); li = text_img(f'AGE {age}', 'type', 24, GREY, 1); c.alpha_composite(li, (int(xx - li.size[0] / 2), oy + h - 58))
            g = clamp((t - (ti + 0.3)) / (at(i, 'one crore', -0.2) - ti - 0.3))
            n = int(g * 360)
            for arr, col in ((TORT, GRN), (HARE, RED)):
                pts = [(X(m), Y(arr[m])) for m in range(0, n + 1, 4)]
                if len(pts) > 1: stroke(c, pts, 11, col)
                if n > 0:
                    tx, ty = X(n), Y(arr[n]); d.ellipse((tx - 12, ty - 12, tx + 12, ty + 12), fill=col, outline=INK, width=4)
            if g > 0.05:
                place(c, label('TORTOISE', GRN), 300, oy + 130, 0.9, -2)
                place(c, label('HARE', RED), 300, oy + 210, 0.9, 2)
    to = at(i, 'one crore', -0.3)
    if t > to:
        place(c, card_box(430, 260, SOFT), 290, 1180, pp(t, to), -1.5)
        v = SS.roll_number(t, to, 1.0, 0, T_END)
        place(c, text_img(short(v), 'anton', 92, GRN), 290, 1210)
        place(c, text_img('TORTOISE', 'osw5', 40, GREY), 290, 1110)
        tort(c, t, 290, 1440, 'happy', 0.42, shades=True)
    th = at(i, 'Seventy six', -0.3)
    if t > at(i, 'Hare?', -0.2):
        place(c, card_box(430, 260, SOFT), 790, 1180, pp(t, at(i, 'Hare?', -0.2)), 1.5)
        v = SS.roll_number(t, th, 1.0, 0, H_END) if t > th else 0
        place(c, text_img(short(v) if v else '₹ ?', 'anton', 92, RED), 790, 1210)
        place(c, text_img('HARE', 'osw5', 40, GREY), 790, 1110)
        hr(c, t, 790, 1420, 'cry' if t > th + 0.8 else 'wow', 'head' if t > th + 0.8 else 'down', 0.3)
    if t > th + 1.0:
        s_, a = slam(t, th + 1.0); place(c, stamp_c('-₹37 LAKH', RED, 100, -8, 81), 790, 990, s_, 0, a)
    src(c, t, 'monthly SIP, 10% a year compounded monthly · my own calculation', ti + 0.6, 1700)


def s7(c, t):
    i = 6; T0 = STARTS[i]
    words_line(c, t, [("IS", INK, T0 + 0.05), ("10%", RED, T0 + 0.2), ("A", INK, T0 + 0.35), ("FANTASY?", INK, T0 + 0.45)], 'anton', 104, 260, key='fz')
    tn = at(i, 'Nifty fifty', -0.3)
    if t > tn:
        p = pp(t, tn, 0.45, 1.3); place(c, card_box(900, 360, SOFT), 540, 560, p, -0.6)
        if p > 0.7:
            place(c, text_img('NIFTY 50', 'osw5', 48, GREY), 540, 430)
            t1 = at(i, 'one thousand', -0.3); t2 = at(i, 'twenty three thousand', -0.4)
            if t > t1:
                place(c, text_img('NOV 1995', 'osw5', 40, GREY), 260, 520)
                place(c, text_img('1,000', 'anton', 100, INK), 260, 610, pp(t, t1))
            if t > at(i, 'Today', -0.3):
                marker_line(c, [(400, 600), (560, 600)], eo(prog(t, at(i, 'Today', -0.3), 0.4)), GREY, 8, head=True, head_size=24)
                place(c, text_img('30 OCT 2026', 'osw5', 40, GREY), 760, 520)
                v = SS.roll_number(t, t2, 1.4, 1000, 23053.1) if t > t2 else 1000
                place(c, text_img(f'{int(v):,}', 'anton', 110, GRN), 760, 615)
    ta = at(i, 'About ten', -0.3)
    t2 = at(i, 'twenty three thousand', -0.4)
    if t > t2 + 1.2:
        s_, a = slam(t, t2 + 1.2); place(c, stamp_c('23X IN 31 YEARS', GRN, 80, -5, 91), 540, 800, s_, 0, a)
    if t > ta: place(c, label('ABOUT 10.6% A YEAR (PRICE ONLY)', NAVY), 540, 940, 1.2 * pp(t, ta), -1)
    tb = at(i, 'big crashes', -0.35)
    if t > tb:
        p = pp(t, tb, 0.45, 1.3); place(c, card_box(900, 500, SOFT), 540, 1290, p, 0.6)
        if p > 0.7:
            place(c, text_img('NOT A STRAIGHT LINE · LAST 12 MONTHS', 'type', 26, RED, 1), 540, 1080)
            v = CLOSES; lo, hi = min(v), max(v)
            pts = [(150 + 780 * k / (len(v) - 1), 1140 + 300 * (hi - x) / (hi - lo)) for k, x in enumerate(v)]
            d = ImageDraw.Draw(c)
            for gy in (1140, 1290, 1440): d.line((150, gy, 930, gy), fill=(225, 220, 210), width=2)
            q = eio(prog(t, tb + 0.3, 1.1)); spark(c, pts, q, RED, 9)
            if q >= 1:
                place(c, label('-12% FROM ITS HIGH', RED), 700, 1500, 1.0 * pp(t, tb + 1.4), -2)
        for k, (txt, x, y, rt) in enumerate((('2008 CRASH', 210, 1630, -6), ('2020 CRASH', 540, 1600, 4), ('2026 FALL', 870, 1630, -3))):
            tk = tb + 0.6 + 0.35 * k
            if t > tk:
                s_, a = slam(t, tk); place(c, stamp_c(txt, RED, 50, rt, 100 + k), x, y, s_, 0, a)
    src(c, t, 'Nifty 50 base 1,000 (3 Nov 1995, NSE) · close 23,053.10 on 30 Oct 2026 (INDmoney)', tn + 0.4, 1735, size=22)


def s8(c, t):
    i = 7; T0 = STARTS[i]
    tm = at(i, 'Ten lost', -0.35); tc = at(i, 'Start small', -0.3)
    if t < tm:
        SS.tear_reveal(c, t, T0 + 0.1, stamp_c('TIME > AMOUNT', GRN, 140, -4, 111), 540, 640)
        place_text(c, 'the lesson', 'mark', 70, NAVY, 540, 420, t, 'ls', T0 + 0.05, 'slide', rot=-2)
        tort(c, t, 330, 1150, 'happy', 0.7, shades=True)
        hr(c, t, 800, 1060, 'sad', 'down', 0.5)
    elif t < tc:
        SS.myth_fact(c, t, tm, ['Start late,', 'invest double,', 'catch up'], ['10 lost years', 'cost more than', '2× money fixes'], y0=230, y1=1560)
        hr(c, t, 300, 1340, 'sad', 'down', 0.32, a=clamp((t - tm) / 0.4))
        if t > tm + 1.0: tort(c, t, 780, 1400, 'happy', 0.42, shades=True)
    else:
        SS.cheat_sheet(c, t, tc, 'TORTOISE vs HARE', [
            ('TORTOISE ₹5K X 30Y', '₹1.14 CR', GRN), ('HARE ₹10K X 20Y', '₹76.6 L', RED),
            ('MONEY PUT IN', '₹18 L vs ₹24 L', INK), ('RULE', 'START EARLY', NAVY)], y0=300)
        if t > tc + 1.0:
            tort(c, t, 330, 1380, 'happy', 0.5, shades=True)
            hr(c, t, 800, 1330, 'sad', 'down', 0.32)
        src(c, t, 'illustration at 10% a year, not a promise or forecast', tc + 0.4, 1640, GREY, 26)


def s9(c, t):
    i = 8; T0 = STARTS[i]
    SS.send_frame(c, t, T0 + 0.05, "your 'I'll start later' friend", y=420)
    ts = at(i, 'Save this', -0.3)
    if t > ts:
        p = pp(t, ts, 0.4, 1.8); bob = math.sin((t - ts) * 7) * 8 * math.exp(-(t - ts) * 0.8)
        place(c, SS.bookmark_icon(100), 340, 700 + bob, p, -8)
        place(c, text_img('SAVE THIS', 'anton', 84, CREAM), 590, 700, p)
    tfo = at(i, 'follow', -0.2)
    if t > tfo:
        q = prog(t, tfo, 0.35); place(c, follow_btn(), 540, 880, 0.5 + 0.5 * eback(q), 0, clamp(q * 3))
    th = at(i, 'The Hare had', -0.3); tt = at(i, 'The Tortoise had', -0.3)
    if t > th:
        hr(c, t, 290, 1210, 'sad', 'down', 0.4)
        place(c, label('MORE MONEY', RED), 290, 1440, 1.2 * pp(t, th + 0.2), -3)
    if t > tt:
        tort(c, t, 780, 1280, 'happy', 0.55, shades=True)
        place(c, label('MORE TIME', GRN), 780, 1440, 1.2 * pp(t, tt + 0.2), 3)
    for k, ln in enumerate(['Illustration at 10% a year: not a promise or forecast.', 'Nifty 50: NSE / INDmoney, 30 Oct 2026. Past returns are not a guarantee.',
                            'Education only. Not investment advice. No buy/sell recommendation.']):
        place_text(c, ln, 'type', 23, (210, 204, 192), 540, 1570 + k * 40, t, None, T0 + 0.3, 'fade', track=1)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]


def SLAMS():
    return [at(0, 'still lost', -0.2), at(2, 'double', -0.25), STARTS[3] + 0.08, STARTS[4] + 0.05,
            at(5, 'Seventy six', 0.7), at(6, 'twenty three thousand', 0.8)] + [STARTS[k] + 0.05 for k in (1, 2, 5, 6, 7)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('ANIMAL FRIDAY', 'type', 30, RED if not dark else YEL, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
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
