"""Kaadu Bank Ep 1 (Animal Friday) - Ammu's Weekly Grain: small SIP, big pile (AMFI Oct 2026). Paper Vox v2 + camera moves."""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs, follow_btn
import tea as TEA
import saveshare as SS
import animals as A
import kaadu_cast as K

import os
SH = ROOT + os.environ.get('LDIR', 'kaadu1') + '/'
CAPS_ON = False  # owner: NO subtitles
SCRIPT = json.load(open(SH + 'script.json'))
DURS = json.load(open(SH + 'vo/durs.json'))
LEAD, TAIL = 0.15, 0.3
HOLD = {8: 1.6}  # cheat-sheet freeze frame
STARTS, VO = [], []
_t = 0.0
for i, d in enumerate(DURS):
    STARTS.append(_t); VO.append(_t + (0.1 if i == 0 else LEAD)); _t = VO[-1] + d + TAIL + HOLD.get(i, 0)
DUR = _t + 1.8
B = STARTS[1:]
SOFT = (253, 251, 246); NAVY = (30, 60, 120); BLUE = (40, 100, 200); GREY = (120, 116, 108); GOLD = (214, 160, 40)
PINK = (230, 90, 140); TEAL = (20, 140, 130); ORG = (230, 120, 30)
ACC = (30, 110, 72)  # theme green (HK.THEME_ACCENT['green'])
card_box = TEA.card_box; label = TEA.label
LAST = len(SCRIPT) - 1


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def pp(t, t0, d=0.35, s=1.6): return eback(prog(t, t0, d), s)


def src(c, t, txt, t0, y=1700, col=GREY, size=24):
    if t > t0: place_text(c, txt, 'type', size, col, 540, y, t, None, t0, 'fade', track=1)


def step(t, rate=6): return int(t * rate) % 4


def ammu(c, t, x, y, mood='happy', pose='down', sc=0.5, walk=False, a=1.0, rot=0):
    st = step(t, 9) if walk else 0
    bob = abs(math.sin(t * 9)) * -10 if walk else math.sin(t * 3) * 4
    place(c, K.ammu(mood, pose, st), x, y + bob, sc, rot + math.sin(t * 4) * 2, a)


def mani(c, t, x, y, mood='happy', pose='down', sc=0.45, phone=False, a=1.0, rot=0):
    place(c, K.mani(mood, pose, 0, 1.0, phone), x, y + math.sin(t * 5) * 5, sc, rot + math.sin(t * 3) * 2, a)


def thatha(c, t, x, y, mood='happy', trunk=0, sc=0.5, a=1.0):
    br = math.sin(t * 1.6) * 0.012
    place(c, K.thatha(mood, trunk), x, y + math.sin(t * 1.6) * 3, sc * (1 + br), math.sin(t * 0.9) * 0.6, a)


def kili(c, t, x, y, mood='happy', talk=False, sc=0.45, a=1.0):
    ob = talk and (int(t * 8) % 2 == 0); fl = (math.sin(t * 14) * 0.5 + 0.5) if talk else 0
    place(c, K.kili(mood, ob, True, round(fl * 3) / 3), x, y + math.sin(t * 6) * 6, sc, math.sin(t * 5) * 4, a)


@functools.lru_cache(None)
def qmark(col=RED):
    return cutout(text_img('?', 'anton', 260, col), border=8, shadow=0.35)


@functools.lru_cache(None)
def bubble(txt, w=520, h=150, col=INK, fill=SOFT, tail=-1):
    im = Image.new('RGBA', (w + 40, h + 80), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    tx = 60 if tail < 0 else w - 40
    d.polygon([(tx, h - 4), (tx + (40 if tail < 0 else -40), h - 4), (tx - 10 * tail * -1, h + 60)], fill=fill, outline=INK)
    d.rounded_rectangle((6, 6, w, h), 40, fill=fill, outline=INK, width=7)
    d.line([(tx + 6, h - 4), (tx + (34 if tail < 0 else -34), h - 4)], fill=fill, width=10)
    tt = text_img(txt, 'anton', int(h * 0.42), col); im.alpha_composite(tt, ((w + 6) // 2 - tt.size[0] // 2, (h + 6) // 2 - tt.size[1] // 2))
    return im


def falling_grain(c, t, t0, x, y0, y1, dur=0.5, sc=0.6):
    if t0 < t < t0 + dur:
        q = (t - t0) / dur; place(c, K.grain(40), x, y0 + (y1 - y0) * q * q, sc, q * 160)


def cal_week(c, t, t0, n, x0=150, y0=640, cols=8, step_=104, tick_dur=2.4):
    """grid of n week tiles that tick green one by one"""
    d = ImageDraw.Draw(c)
    for k in range(n):
        tk = t0 + tick_dur * k / n
        r_, c_ = divmod(k, cols); x = x0 + c_ * step_; y = y0 + r_ * step_
        if t < t0 + k * 0.004: continue
        s = 1.0
        on = t > tk
        if on: s = 1 + 0.25 * math.exp(-(t - tk) * 10)
        w = 40 * s
        d.rounded_rectangle((x - w, y - w, x + w, y + w), 10, fill=(214, 238, 214) if on else (232, 226, 214), outline=INK, width=4)
        if on: d.line([(x - 20 * s, y), (x - 6 * s, y + 16 * s), (x + 22 * s, y - 18 * s)], fill=GRN, width=9)
    return sum(1 for k in range(n) if t > t0 + tick_dur * k / n)


# ---------------- scenes ----------------
def s1(c, t):
    i = 0
    tl = at(i, 'Almost ten', -0.2)
    q = eo(prog(t, 0.0, 1.1))
    place(c, card_box(940, 330, SOFT), 540, 470, 1.0, -1)
    place(c, text_img('SIP ACCOUNTS THAT PAID IN', 'osw5', 46, GREY), 540, 360)
    jx = math.sin(t * 50) * 4 * (1 - q)
    place(c, text_img(f'{9.99 * q:.2f} CRORE', 'anton', 150, ACC), 540 + jx, 500)
    place(c, text_img('in ONE month · October 2026', 'mark', 44, NAVY), 540, 600, 1, -1)
    # Ammu walks in carrying her grain, Mani laughs
    x = 300 + 40 * math.sin(t * 1.2)
    ammu(c, t, x, 1150, 'happy', 'carry', 0.7, walk=True)
    mani(c, t, 790, 1130, 'happy' if t < tl else 'wow', 'point' if t < tl else 'head', 0.58)
    if 0.35 < t < tl:
        s_, a = slam(t, 0.35); place(c, stamp_c('HA HA!', RED, 70, 8, 11), 820, 800, s_, 0, a)
    if t > tl:
        s_, a = slam(t, tl); place(c, stamp_c('NOT SO SMALL', ACC, 84, -6, 12), 560, 770, s_, 0, a)
    place(c, label('NEVER LAUGH AT A SMALL SIP', RED), 540, 1500, 1.35 * pp(t, -0.3), -2)
    src(c, t, 'AMFI monthly data, October 2026 (released 11 Nov 2026)', 0.6, 1640, GREY, 26)


def s2(c, t):
    i = 1; T0 = STARTS[i]
    place(c, K.bank(), 540, 560, 0.85 * pp(t, T0, 0.45, 1.3))
    te = at(i, 'episode one', -0.25)
    if t > te:
        s_, a = slam(t, te); place(c, stamp_c('EPISODE 1', RED, 90, -7, 21), 790, 300, s_, 0, a)
    tl = at(i, 'Last week', -0.3)
    if t < tl:
        # cast line-up pops in
        cast = [(K.ammu('happy'), 0.34), (K.mani('happy', 'down', 0, 1.0, False), 0.28), (K.thatha('happy', 1), 0.26),
                (K.kili('happy', False, True, 0), 0.3), (K.aandhai('happy'), 0.28), (K.ponni('happy'), 0.28)]
        xs = [120, 290, 480, 670, 830, 980]; ys = [1260, 1250, 1290, 1250, 1260, 1260]
        for k, (im, sc) in enumerate(cast):
            tk = T0 + 0.5 + 0.18 * k
            if t > tk: place(c, im, xs[k], ys[k] + math.sin(t * 3 + k) * 6, sc * pp(t, tk, 0.3, 1.8))
        tk = T0 + 1.4
        if t > tk:
            place(c, label('MEET THE KAADU BANK GANG', ACC), 540, 1560, 1.1 * pp(t, tk), -1.5)
    else:
        p = pp(t, tl, 0.4, 1.3)
        place(c, card_box(940, 640, (255, 246, 214)), 540, 1290, p, 1)
        if p > 0.6:
            place(c, text_img('LAST WEEK', 'anton', 64, NAVY), 540, 1010)
            place(c, A.branch(560), 300, 1420); place(c, A.branch(560, True), 780, 1350)
            f = ((t - tl) / 0.6); k = int(f); q = f - k
            pts = [(270, 1370), (800, 1300)]; a_, b_ = pts[k % 2], pts[(k + 1) % 2]
            xx = a_[0] + (b_[0] - a_[0]) * eio(q); yy = a_[1] + (b_[1] - a_[1]) * eio(q) - 80 * math.sin(math.pi * q)
            place(c, K.mani('happy', 'both_up', 0, 1.0, False), xx, yy - 120, 0.28, -10)
            tf = at(i, 'paid a fee', -0.3)
            if t > tf:
                for j in range(4):
                    tj = tf + j * 0.25
                    if t > tj: place(c, A.fee_coin('FEE'), 240 + j * 190, 1550 - 20 * math.exp(-(t - tj) * 8), 0.55 * pp(t, tj, 0.25, 2))


def s3(c, t):
    i = 2; T0 = STARTS[i]
    place_text(c, 'MEET AMMU', 'anton', 120, INK, 540, 240, t, 'ma', T0 + 0.05, 'pop')
    place(c, label('THE ANT · SAVES A LITTLE, ON PURPOSE', ORG), 540, 380, 0.9 * pp(t, T0 + 0.3), -1)
    place(c, K.bank(), 820, 1050, 0.7)
    td = at(i, 'drops', -0.3)
    # walk from left to the bank door
    q = eio(prog(t, T0 + 0.2, max(0.5, td - T0 - 0.2)))
    x = 180 + 430 * q
    if t < td + 0.2:
        ammu(c, t, x, 1150, 'happy', 'carry', 0.55, walk=q < 1)
    else:
        ammu(c, t, x, 1150, 'happy', 'wave', 0.55)
        falling_grain(c, t, td + 0.1, 800, 1000, 1240, 0.45, 0.8)
    tf = at(i, 'Every Friday', -0.2)
    if t > tf:
        p = pp(t, tf, 0.4, 1.6); place(c, card_box(250, 230, SOFT), 230, 640, p, -4)
        if p > 0.6:
            ImageDraw.Draw(c).rectangle((112, 532, 348, 590), fill=RED)
            place(c, text_img('EVERY', 'osw5', 34, CREAM), 230, 560, 1, -4); place(c, text_img('FRI', 'anton', 100, INK), 230, 670, 1, -4)
    for k, (w, col, xx, yy, rt) in enumerate((('SAME DAY', NAVY, 260, 1450, -5), ('SAME SIZE', ACC, 760, 1500, 4), ('NO TIPS', RED, 470, 1610, -3))):
        tk = at(i, {'SAME DAY': 'Same day', 'SAME SIZE': 'Same size', 'NO TIPS': 'No tips'}[w], -0.15)
        if t > tk:
            s_, a = slam(t, tk); place(c, stamp_c(w, col, 72, rt, 30 + k), xx, yy, s_, 0, a)


def s4(c, t):
    i = 3; T0 = STARTS[i]
    tg = at(i, 'One grain', -0.2); tn = at(i, "That's nothing", -0.2); tk_ = at(i, 'Kili', -0.3); tr = at(i, 'Nothing! Nothing', -0.2)
    mani(c, t, 300, 1000, 'happy', 'head' if t > tn else 'point', 0.55)
    if t > T0 + 0.1:
        for k in range(3):
            tt = T0 + 0.1 + k * 0.35
            if t > tt: place(c, text_img('HA', 'anton', 70, RED), 140 + k * 120, 560 - k * 40 + math.sin(t * 9 + k) * 8, pp(t, tt, 0.2, 2), -10 + k * 8)
    if t > tg:
        place(c, bubble('ONE GRAIN?', 540, 150), 660, 380, pp(t, tg, 0.3, 1.6), 2)
        place(c, K.grain(40), 900, 340, 0.6, math.sin(t * 4) * 15)
    if t > tn:
        s_, a = slam(t, tn); place(c, stamp_c("THAT'S NOTHING!", RED, 76, -6, 41), 540, 1400, s_, 0, a)
    if t > tk_:
        p = pp(t, tk_, 0.4, 1.4)
        kili(c, t, 820, 980, 'happy', t > tr, 0.5 * p)
        place(c, label('KILI THE PARROT', GRN), 820, 1210, 1.0 * pp(t, tk_ + 0.2), 3)
    if t > tr:
        for k in range(2):
            tt = tr + k * 0.5
            if t > tt: place(c, bubble('NOTHING!', 380, 120, GRN, tail=1), 760 - k * 30, 620 + k * 140, pp(t, tt, 0.25, 1.8), -4 + 8 * k)
    ammu(c, t, 560, 1620, 'calm', 'carry', 0.32)


def s5(c, t):
    i = 4; T0 = STARTS[i]
    if t - T0 < 0.3: c.alpha_composite(Image.new('RGBA', c.size, (255, 214, 51, int(200 * (1 - (t - T0) / 0.3)))))
    s_, a = slam(t, T0 + 0.08); place(c, stamp_c('BUT…', RED, 150, -6, 61), 540, 280, s_, 0, a)
    place_text(c, 'what Mani never counted', 'mark', 58, NAVY, 540, 430, t, 'nc', T0 + 0.4, 'slide', rot=-2)
    ta = STARTS[i] + 0.6
    n = cal_week(c, t, ta, 52, x0=176, y0=600, cols=8, step_=104, tick_dur=3.2) if t > ta else 0
    if t > ta:
        p = pp(t, ta, 0.4, 1.4); place(c, card_box(520, 170, SOFT), 300, 1430, p, -2)
        if p > 0.6:
            place(c, text_img('WEEKS SKIPPED', 'osw5', 34, GREY), 300, 1385); place(c, text_img('0', 'anton', 90, ACC), 300, 1460)
        place(c, text_img(f'{n}/52', 'anton', 64, INK), 820, 1330)
    ammu(c, t, 820, 1480, 'happy', 'wave' if t > ta + 2 else 'carry', 0.36)
    place(c, qmark(RED), 940, 330 + math.sin(t * 7) * 12, 0.4 * pp(t, T0 + 0.3), -6 + math.sin(t * 4) * 4)


def s6(c, t):
    i = 5; T0 = STARTS[i]
    words_line(c, t, [("THE", INK, T0 + 0.05), ("REAL", ACC, T0 + 0.2), ("JUNGLE", ACC, T0 + 0.35)], 'anton', 120, 250, key='rj')
    to = at(i, 'October', -0.3); tn = at(i, 'thirty two', -0.3); tm = at(i, 'In one month', -0.2)
    if t > to:
        p = pp(t, to, 0.4, 1.3); place(c, card_box(940, 330, SOFT), 540, 520, p, -1)
        if p > 0.6:
            place(c, text_img('MONTHLY SIP INFLOW · OCT 2026', 'osw5', 40, GREY), 540, 420)
            vv = SS.roll_number(t, tn, 2.6, 0, 32160) if t > tn else 0
            place(c, text_img(f'₹{int(vv):,} CR', 'anton', 140, ACC), 540, 540)
    # grains pouring into the bank
    place(c, K.bank(), 540, 1160, 0.75)
    if t > tn:
        r = random.Random(3)
        for k in range(40):
            tk = tn + k * 0.12 + r.uniform(0, 0.1)
            falling_grain(c, t, tk, 380 + r.uniform(0, 320), 720, 1240, 0.55, 0.45)
    if t > tm:
        s_, a = slam(t, tm); place(c, stamp_c('IN ONE MONTH', RED, 80, -7, 71), 760, 760, s_, 0, a)
    ammu(c, t, 170, 1480, 'wow', 'down', 0.32)
    src(c, t, 'AMFI monthly data, October 2026 (released 11 Nov 2026)', to + 0.2, 1720, GREY, 23)


def s7(c, t):
    i = 6; T0 = STARTS[i]
    ta = at(i, 'Almost ten', -0.2); te = at(i, 'about three', -0.3); tsg = at(i, 'Small grains', -0.3)
    p = pp(t, ta, 0.4, 1.3); place(c, card_box(940, 260, SOFT), 540, 320, p, 1)
    if p > 0.6:
        place(c, text_img('SIP ACCOUNTS THAT PAID IN', 'osw5', 38, GREY), 540, 250)
        vv = SS.roll_number(t, ta, 1.4, 0, 9.99)
        place(c, text_img(f'{vv:.2f} CRORE', 'anton', 110, NAVY), 540, 345)
    if t > te:
        p = pp(t, te, 0.4, 1.3); place(c, card_box(940, 420, YEL), 540, 760, p, -1)
        if p > 0.6:
            place(c, text_img('₹32,160 CR ÷ 9.99 CR ACCOUNTS', 'osw5', 46, INK), 540, 630)
            ImageDraw.Draw(c).line((170, 680, 910, 680), fill=INK, width=4)
            vv = SS.roll_number(t, te + 0.3, 1.2, 0, 3216)
            place(c, text_img(f'ABOUT ₹{int(vv):,}', 'anton', 130, ACC), 540, 790)
            place(c, text_img('per account, that month', 'mark', 44, NAVY), 540, 900, 1, -1)
    # row of ants each carrying one grain
    for k in range(5):
        tk = ta + 0.3 + k * 0.15
        if t > tk: ammu(c, t + k * 0.2, 150 + k * 195, 1300 + (k % 2) * 40, 'happy', 'carry', 0.3 * pp(t, tk, 0.3, 1.8), walk=True)
    if t > tsg:
        place(c, label('SMALL GRAINS. BIG TOTAL.', ACC), 540, 1560, 1.25 * pp(t, tsg), -2)
    src(c, t, 'AMFI Oct 2026: 9,99,87,082 SIP accounts contributed. Average is our maths.', ta + 0.3, 1700, GREY, 22)


def s8(c, t):
    i = 7; T0 = STARTS[i]
    place_text(c, 'AND THE PILE?', 'anton', 120, INK, 540, 250, t, 'tp', T0 + 0.05, 'pop')
    ts = at(i, 'Seventeen', -0.3)
    n = int(6 + 44 * eo(prog(t, T0 + 0.3, max(1.0, ts - T0 + 1.8))))
    place(c, K.bank(), 760, 1000, 0.6)
    place(c, K.grain_pile(n, 560), 300, 1160, 1.0)
    thatha(c, t, 820, 1460, 'happy', 1, 0.34)
    if t > ts:
        p = pp(t, ts, 0.4, 1.3); place(c, card_box(940, 300, SOFT), 540, 520, p, -1)
        if p > 0.6:
            place(c, text_img('SIP ASSETS · OCT 2026', 'osw5', 40, GREY), 540, 420)
            vv = SS.roll_number(t, ts + 0.2, 2.2, 0, 1768217)
            s_ = f'{int(vv):,}'
            # Indian grouping 17,68,217
            v = int(vv); h, t3 = str(v)[:-3], str(v)[-3:]
            parts = []
            while len(h) > 2: parts.insert(0, h[-2:]); h = h[:-2]
            if h: parts.insert(0, h)
            s_ = (','.join(parts) + ',' + t3) if parts else t3
            place(c, text_img(f'₹{s_} CR', 'anton', 120, ACC), 540, 535)
            place(c, text_img('= ₹17.68 lakh crore', 'mark', 44, NAVY), 540, 630, 1, -1)
    if t > ts + 2.2:
        place(c, label('21.2% OF ALL MUTUAL FUND ASSETS', NAVY), 540, 1600, 1.0 * pp(t, ts + 2.2), 1.5)
    src(c, t, 'AMFI Oct 2026. Includes market movement. Past data, not a forecast.', T0 + 0.6, 1710, GREY, 22)


def s9(c, t):
    i = 8; T0 = STARTS[i]
    ts = at(i, 'The size', -0.3); tn = at(i, 'never skipping', -0.2)
    tc = VO[i] + DURS[i] + 0.1
    if t < tc:
        thatha(c, t, 540, 1150, 'happy', 1 if t > ts else 0, 0.75)
        place(c, label('YAANAI THATHA', BLUE), 540, 1530, 1.2 * pp(t, T0 + 0.2), -2)
        if t > ts:
            p = pp(t, ts, 0.4, 1.3); place(c, card_box(940, 330, YEL), 540, 450, p, -1)
            if p > 0.6:
                place(c, text_img('The size of the grain', 'pf', 62, INK), 540, 370)
                place(c, text_img('matters less than', 'pfi', 52, GREY), 540, 450)
                if t > tn:
                    s_, a = slam(t, tn); place(c, stamp_c('NEVER SKIPPING IT', ACC, 74, -3, 91), 540, 545, s_, 0, a)
    else:
        SS.cheat_sheet(c, t, tc, 'KAADU BANK · EP 1', [
            ('SIP INFLOW OCT 2026', '₹32,160 CR', ACC), ('ACCOUNTS THAT PAID', '9.99 CR', NAVY),
            ('AVERAGE PER ACCOUNT', 'ABOUT ₹3,216', ORG), ('SIP ASSETS', '₹17.68 L CR', ACC), ('RULE', 'NEVER SKIP', RED)], y0=240)
        ammu(c, t, 230, 1540, 'happy', 'carry', 0.3); thatha(c, t, 830, 1560, 'happy', 1, 0.3)
        src(c, t, 'Source: AMFI monthly data, Oct 2026 (11 Nov 2026)', tc + 0.4, 1710, GREY, 24)


def s10(c, t):
    i = 9; T0 = STARTS[i]
    SS.send_frame(c, t, T0 + 0.05, "the friend with a tiny SIP", y=360)
    ts = at(i, 'Save this', -0.3)
    if t > ts:
        p = pp(t, ts, 0.4, 1.8); bob = math.sin((t - ts) * 7) * 8 * math.exp(-(t - ts) * 0.8)
        place(c, SS.bookmark_icon(100), 340, 640 + bob, p, -8)
        place(c, text_img('SAVE THIS', 'anton', 84, CREAM), 590, 640, p)
    tfo = at(i, 'follow', -0.2)
    if t > tfo:
        q = prog(t, tfo, 0.35); place(c, follow_btn(), 540, 800, 0.5 + 0.5 * eback(q), 0, clamp(q * 3))
    te = at(i, 'episode two', -0.3)
    if t > te:
        p = pp(t, te, 0.4, 1.3); place(c, card_box(800, 330, (255, 246, 214)), 600, 1170, p, 1.5)
        if p > 0.6:
            place(c, text_img('NEXT · EPISODE 2', 'osw5', 40, GREY), 640, 1060)
            place(c, text_img("KILI'S HOT TIP", 'anton', 90, GRN), 640, 1150)
            place(c, text_img('(a WhatsApp tip story)', 'mark', 40, NAVY), 640, 1240, 1, -1)
        kili(c, t, 200, 1180, 'wow', True, 0.38 * p)
    for k, ln in enumerate(['Data: AMFI monthly data, October 2026 (released 11 Nov 2026).',
                            'Fictional characters. Past data, not a forecast.',
                            'No buy/sell call. Education only, not investment advice.']):
        place_text(c, ln, 'type', 21, (210, 204, 192), 540, 1560 + k * 38, t, None, T0 + 0.3, 'fade', track=1)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]

# camera move per scene: (kind, strength)
CAMS = ['crash', 'pullout', 'track', 'dutch', 'whip', 'crash', 'tilt', 'pullout', 'pushin', 'pushin']


def SLAMS():
    return [at(0, 'Almost ten', -0.2), at(1, 'episode one', -0.25), STARTS[4] + 0.08, at(3, "That's nothing", -0.2), at(5, 'In one month', -0.2),
            at(8, 'never skipping', -0.2)] + [at(2, w, -0.15) for w in ('Same day', 'Same size', 'No tips')] + [STARTS[k] + 0.05 for k in (1, 2, 5, 6, 7)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('KAADU BANK · EP 1', 'type', 30, ACC if not dark else YEL, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
    ImageDraw.Draw(c).line((60, 118, W - 60, 118), fill=col, width=2)
    ImageDraw.Draw(c).line((60, 118, 60 + (W - 120) * clamp(t / DUR), 118), fill=ACC if not dark else YEL, width=8)


def transition(c, t):
    cols = [(GRN, INK), (GOLD, INK), (ORG, YEL), (YEL, INK), (TEAL, CREAM), (NAVY, CREAM), (GRN, YEL), (INK, ACC), (YEL, NAVY), (ACC, CREAM)]
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


def cam(i, t, st, en):
    """returns zoom, dx, dy, rot for scene i at time t (camera kit, paper Vox port)"""
    u = clamp((t - st) / max(0.1, en - st)); e = t - st; kind = CAMS[i]
    z, dx, dy, rot = 1.0, 0.0, 0.0, 0.0
    if kind == 'crash':
        z = 1.0 + 0.12 * math.exp(-e * 7) + 0.03 * u      # crash in then slow push
    elif kind == 'pullout':
        z = 1.12 - 0.10 * eio(u)
    elif kind == 'pushin':
        z = 1.0 + 0.07 * eio(u)
    elif kind == 'track':
        z = 1.06; dx = -40 + 80 * eio(u)                   # follow Ammu to the bank
    elif kind == 'dutch':
        z = 1.07; rot = -3.5 * eio(clamp(e / 0.6)) + 0.6 * math.sin(e * 2)
    elif kind == 'whip':
        z = 1.05 + 0.03 * u; dx = 260 * math.exp(-e * 9) * (1 if e < 0.6 else 0)
    elif kind == 'tilt':
        z = 1.06; dy = 50 - 100 * eio(u)
    return z, dx, dy, rot


def render(t):
    LOOP = 0.6
    if t > DUR - LOOP:
        a = _render(t); b = _render(1.15, loop=True); q = eio((t - (DUR - LOOP)) / LOOP)
        return (a * (1 - q) + b * q).astype(np.uint8)
    return _render(t)


def _render(t, loop=False):
    pbg, dbg = bgs()
    i = scene_at(t); dark = (i == LAST)
    c = (dbg if dark else pbg).copy()
    st = STARTS[i]; en = STARTS[i + 1] if i + 1 < len(STARTS) else DUR
    SCENES[i](c, t)
    z, dx, dy, rot = cam(i, t, st, en)
    sx = sy = 0
    for ts in slam_times():
        if 0 <= t - ts < 0.35:
            k = math.exp(-(t - ts) * 14) * 8
            sx += k * math.sin((t - ts) * 90); sy += k * math.cos((t - ts) * 77)
    if rot:
        c = c.rotate(rot, Image.BICUBIC, center=(W / 2, H / 2), fillcolor=(244, 238, 226, 255)); z *= 1.08
    cw, ch = W / z, H / z
    cx, cy = W / 2 + sx + dx, max(ch / 2, H * 0.47) + sy + dy
    cx = min(max(cx, cw / 2), W - cw / 2); cy = min(max(cy, ch / 2), H - ch / 2)
    c = c.transform((W, H), Image.EXTENT, (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2), Image.BICUBIC)
    # whip blur on scene change
    if CAMS[i] == 'whip' and t - st < 0.25:
        k = int(30 * (1 - (t - st) / 0.25))
        if k > 2:
            arr = np.asarray(c).astype(np.float32); acc = arr.copy()
            for j in (1, 2, 3): acc += np.roll(arr, j * k // 3, axis=1)
            c = Image.fromarray((acc / 4).astype(np.uint8), 'RGBA')
    header(c, dark, t if not loop else 0); transition(c, t)
    arr = np.asarray(c.convert('RGB')).astype(np.float32)
    g = grain_frames()[int(t * FPS) % 6]
    fl = 1 + 0.012 * math.sin(t * 37) * math.sin(t * 13)
    return np.clip(arr * fl + g[..., None], 0, 255).astype(np.uint8)
