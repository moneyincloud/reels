"""Kaadu Bank Ep 2 (Animal Friday) - Kili's Hot Tip: free tips, pump and dump (SEBI order 26 Apr 2023, Telegram channel). Paper Vox v2 + camera moves."""
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
SH = ROOT + os.environ.get('LDIR', 'kaadu2') + '/'
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
ACC = (205, 40, 50)  # theme red (HK.THEME_ACCENT['red'])
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


# ---------------- Ep 2 helpers ----------------
@functools.lru_cache(None)
def phone_card(title='GOLDEN BANANA GROUP', w=560, h=820):
    im = Image.new('RGBA', (w + 30, h + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((18, 22, w + 18, h + 22), 60, fill=(0, 0, 0, 90))
    d.rounded_rectangle((0, 0, w, h), 60, fill=INK)
    d.rounded_rectangle((22, 70, w - 22, h - 60), 26, fill=(236, 244, 232))
    d.rounded_rectangle((w // 2 - 60, 26, w // 2 + 60, 44), 9, fill=(70, 70, 70))
    d.rectangle((22, 70, w - 22, 160), fill=(40, 120, 90))
    tt = text_img(title, 'osw5', 34, CREAM); im.alpha_composite(tt, (w // 2 - tt.size[0] // 2, 115 - tt.size[1] // 2))
    return im


@functools.lru_cache(None)
def msg(txt, w=460, col=INK, fill=(255, 255, 255), size=40):
    tt = text_img(txt, 'osw5', size, col)
    h = tt.size[1] + 40; w = max(w, tt.size[0] + 50)
    im = Image.new('RGBA', (w + 10, h + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((4, 6, w + 4, h + 6), 22, fill=(0, 0, 0, 50)); d.rounded_rectangle((0, 0, w, h), 22, fill=fill, outline=(180, 180, 170), width=3)
    im.alpha_composite(tt, (w // 2 - tt.size[0] // 2, h // 2 - tt.size[1] // 2)); return im


def phone(c, t, t0, x, y, msgs, sc=1.0, title='GOLDEN BANANA GROUP'):
    """phone with chat bubbles that pop in at the given times; msgs = [(text, t, col)]"""
    p = pp(t, t0, 0.4, 1.4); ph = phone_card(title)
    place(c, ph, x, y + math.sin(t * 2.4) * 6, sc * p, math.sin(t * 1.3) * 1.2)
    if p < 0.7: return
    yy = y - 175 * sc
    for k, (m, tm, col) in enumerate(msgs):
        if t > tm:
            place(c, msg(m, 440, col), x, yy + k * 118 * sc + math.sin(t * 2.4) * 6, sc * pp(t, tm, 0.25, 2.0))


def ping(c, t, t0, x, y):
    if t0 < t < t0 + 0.8:
        q = (t - t0) / 0.8; d = ImageDraw.Draw(c)
        for k in range(3):
            r = 40 + 110 * q + k * 30; a = int(255 * (1 - q))
            d.arc((x - r, y - r, x + r, y + r), 200, 340, fill=(*ACC, a) if False else ACC, width=8)


def price_line(c, t, t0, dur, pts, col, w=10, dot=True):
    """draw polyline progressively; pts in canvas coords. returns tip (x, y)"""
    q = clamp((t - t0) / dur) if dur > 0 else 1
    if q <= 0: return pts[0]
    n = len(pts) - 1; f = q * n; k = int(f); r = f - k
    sub = pts[:k + 1]
    if k < n: sub = sub + [(pts[k][0] + (pts[k + 1][0] - pts[k][0]) * r, pts[k][1] + (pts[k + 1][1] - pts[k][1]) * r)]
    d = ImageDraw.Draw(c)
    if len(sub) > 1:
        d.line(sub, fill=INK, width=w + 8, joint='curve'); d.line(sub, fill=col, width=w, joint='curve')
    tip = sub[-1]
    if dot: d.ellipse((tip[0] - 16, tip[1] - 16, tip[0] + 16, tip[1] + 16), fill=col, outline=INK, width=5)
    return tip


def axes(c, x0, y0, x1, y1):
    d = ImageDraw.Draw(c); d.line((x0, y0, x0, y1, x1, y1), fill=INK, width=5)
    for k in range(1, 4): d.line((x0, y1 - (y1 - y0) * k / 4, x1, y1 - (y1 - y0) * k / 4), fill=(220, 212, 198), width=2)


def aandhai(c, t, x, y, mood='calm', sc=0.5, paper=True):
    place(c, K.aandhai(mood, paper), x, y + math.sin(t * 2.2) * 4, sc, math.sin(t * 1.4) * 2)


def ponni(c, t, x, y, mood='happy', sc=0.4):
    place(c, K.ponni(mood, True), x, y + abs(math.sin(t * 5)) * -8, sc, math.sin(t * 3) * 3)


# ---------------- scenes ----------------
def s1(c, t):
    i = 0
    tf = at(i, 'Fifty thousand', -0.2)
    # phone already on screen and pinging at frame 0
    phone(c, t, -1, 330, 760, [('FREE TIP!!', -1, RED), ('BUY THIS STOCK NOW', 0.25, INK), ('HURRY!!!', 0.6, RED)], 0.82)
    ping(c, t, 0.0, 330, 380); ping(c, t, 0.8, 330, 380)
    kili(c, t, 800, 760, 'wow', True, 0.6)
    q = eo(prog(t, 0.0, max(0.8, tf - 0.0 + 1.0)))
    place(c, card_box(900, 250, SOFT), 540, 1330, 1.0, 1)
    place(c, text_img('PEOPLE WHO GOT THE SAME TIP', 'osw5', 40, GREY), 540, 1250)
    place(c, text_img(f'~{int(50000 * q):,}', 'anton', 140, ACC), 540, 1360)
    if t > tf:
        s_, a = slam(t, tf); place(c, stamp_c('NEVER TRUST A FREE TIP', RED, 74, -5, 11), 540, 1560, s_, 0, a)
    src(c, t, 'Real case: SEBI order, 26 Apr 2023 (Telegram tip channel)', 0.6, 1700, GREY, 26)


def s2(c, t):
    i = 1; T0 = STARTS[i]
    place(c, K.bank(), 540, 560, 0.85 * pp(t, T0, 0.45, 1.3))
    te = at(i, 'episode two', -0.25)
    if t > te:
        s_, a = slam(t, te); place(c, stamp_c('EPISODE 2', RED, 90, -7, 21), 790, 300, s_, 0, a)
    tl = at(i, 'Last week', -0.3); tw = at(i, 'This week', -0.3); ts = at(i, 'shortcut', -0.2)
    if t < tl:
        cast = [(K.ammu('happy'), 0.34), (K.mani('happy', 'down', 0, 1.0, False), 0.28), (K.thatha('happy', 1), 0.26),
                (K.kili('happy', False, True, 0), 0.3), (K.aandhai('happy'), 0.28), (K.ponni('happy'), 0.28)]
        xs = [120, 290, 480, 670, 830, 980]; ys = [1260, 1250, 1290, 1250, 1260, 1260]
        for k, (im, sc) in enumerate(cast):
            tk = T0 + 0.4 + 0.12 * k
            if t > tk: place(c, im, xs[k], ys[k] + math.sin(t * 3 + k) * 6, sc * pp(t, tk, 0.3, 1.8))
    elif t < tw:
        p = pp(t, tl, 0.4, 1.3)
        place(c, card_box(940, 640, (255, 246, 214)), 540, 1290, p, 1)
        if p > 0.6:
            place(c, text_img('LAST WEEK', 'anton', 64, NAVY), 540, 1010)
            ammu(c, t, 300, 1330, 'calm', 'carry', 0.4)
            kili(c, t, 760, 1300, 'happy', True, 0.42)
            place(c, bubble('NOTHING!', 380, 120, GRN, tail=1), 780, 1170, pp(t, tl + 0.3, 0.25, 1.8), -4)
            place(c, label('EP 1 · AMMU NEVER SKIPPED A WEEK', ORG), 540, 1560, 0.9 * pp(t, tl + 0.6), -1)
    else:
        kili(c, t, 540, 1250, 'wow', False, 0.75)
        place(c, label('KILI THE PARROT · REPEATS WHAT TRENDS', GRN), 540, 1600, 0.9 * pp(t, tw + 0.1), -1)
        if t > ts:
            s_, a = slam(t, ts); place(c, stamp_c('A SHORTCUT?', ACC, 90, 6, 22), 560, 930, s_, 0, a)
            place(c, qmark(RED), 900, 1000 + math.sin(t * 7) * 12, 0.4 * pp(t, ts + 0.1), 8)


def s3(c, t):
    i = 2; T0 = STARTS[i]
    tb = at(i, 'Buy this', -0.2); th = at(i, 'Hurry', -0.2); tk_ = at(i, 'And Kili', -0.2); tbb = at(i, 'Buy! Buy', -0.2)
    place(c, phone_card(), 0, 0, 0)  # warm cache
    phone(c, t, T0 + 0.05, 330, 820, [('PING!  NEW MESSAGE', T0 + 0.1, GREY), ('BUY THIS TINY STOCK TODAY', tb, INK), ('HURRY!!!', th, RED)], 0.9)
    ping(c, t, T0 + 0.1, 330, 380)
    if t < tk_:
        kili(c, t, 820, 900, 'wow', False, 0.55)
    else:
        kili(c, t, 820, 900, 'happy', True, 0.6)
        r = random.Random(5)
        for k in range(6):
            tt = tbb + k * 0.22
            if t > tt: place(c, bubble('BUY!', 240, 110, GRN, tail=1 if k % 2 else -1), 640 + r.uniform(-60, 320), 420 + k * 170 * 0.6 + r.uniform(-20, 20), pp(t, tt, 0.2, 2.0), r.uniform(-12, 12))
        # tiny jungle crowd hearing it
        for k, xx in enumerate((620, 760, 900)):
            if t > tk_ + 0.2 * k: place(c, [K.ammu('wow'), K.mani('wow', 'down', 0, 1.0, False), K.ponni('wow')][k], xx, 1480, 0.24 * pp(t, tk_ + 0.2 * k, 0.3, 1.8))
    place(c, label('FICTIONAL GROUP · FOR THE STORY', GREY), 330, 1360, 0.7 * pp(t, T0 + 0.5), -1)


def s4(c, t):
    i = 3; T0 = STARTS[i]
    tm = at(i, 'Mani', -0.3); tw = at(i, 'But who', -0.2); tf = at(i, 'why for free', -0.2)
    place_text(c, 'THE PRICE JUMPS', 'anton', 110, INK, 540, 230, t, 'pj', T0 + 0.05, 'pop')
    x0, y0, x1, y1 = 120, 400, 960, 1100
    axes(c, x0, y0, x1, y1)
    pts = [(140, 1060), (260, 1040), (380, 1050), (480, 960), (580, 820), (680, 640), (780, 520), (880, 440)]
    tip = price_line(c, t, T0 + 0.2, 2.2, pts, GRN)
    place(c, text_img('illustration', 'type', 26, GREY), 860, 1130)
    if t > tm:
        f = clamp((t - tm) / 0.6); yy = 1350 - 160 * math.sin(math.pi * min(1, f)) if f < 1 else 1350 - abs(math.sin(t * 6)) * 40
        place(c, K.mani('wow' if f < 1 else 'happy', 'both_up', 0, 1.0, False), 300, yy, 0.42)
    kili(c, t, 800, 1380, 'happy', False, 0.4)
    if t > tw:
        p = pp(t, tw, 0.3, 1.6); place(c, card_box(880, 160, YEL), 540, 1600, p, -1.5)
        if p > 0.6: place(c, text_img('WHO SENT THE TIP?', 'anton', 80, INK), 540, 1600, 1, -1.5)
        place(c, qmark(RED), 950, 470 + math.sin(t * 7) * 12, 0.45 * pp(t, tw + 0.1), -6)
    if t > tf:
        s_, a = slam(t, tf); place(c, stamp_c('WHY FREE?', RED, 90, 7, 41), 560, 600, s_, 0, a)


def s5(c, t):
    i = 4; T0 = STARTS[i]
    if t - T0 < 0.3: c.alpha_composite(Image.new('RGBA', c.size, (255, 214, 51, int(200 * (1 - (t - T0) / 0.3)))))
    s_, a = slam(t, T0 + 0.08); place(c, stamp_c('THE TWIST', RED, 110, -6, 61), 540, 290, s_, 0, a)
    ta = at(i, 'Aandhai', -0.3); tbf = at(i, 'bought the stock', -0.3); tbm = at(i, 'before the message', -0.2); ts = at(i, 'Then they sold', -0.2)
    aandhai(c, t, 880, 540, 'calm', 0.42 * pp(t, ta, 0.4, 1.6))
    if t > ta: place(c, label('AANDHAI THE OWL · READS THE TRADES', NAVY), 420, 460, 0.75 * pp(t, ta + 0.1), -1)
    x0, y0, x1, y1 = 110, 640, 970, 1230
    axes(c, x0, y0, x1, y1)
    pts = [(130, 1190), (250, 1180), (350, 1170), (450, 1060), (550, 900), (640, 760), (700, 720), (780, 900), (860, 1100), (950, 1190)]
    if t > tbf:
        price_line(c, t, tbf, max(0.5, ts + 1.4 - tbf), pts, ACC)
    steps = [('1 · THEY BUY FIRST', tbf, (250, 1180), NAVY), ('2 · TIP SENT: BUY!', tbm, (450, 1060), GRN), ('3 · THEY SELL TO YOU', ts, (700, 720), RED)]
    for k, (txt, tk, (px, py), col) in enumerate(steps):
        if t > tk:
            s2_, a2 = slam(t, tk); place(c, stamp_c(txt, col, 54, (-4, 3, -3)[k], 62 + k), 540, 1330 + k * 110, s2_, 0, a2)
            pr = pp(t, tk, 0.3, 2); d = ImageDraw.Draw(c); d.ellipse((px - 26 * pr, py - 26 * pr, px + 26 * pr, py + 26 * pr), outline=col, width=8)
    place(c, text_img('illustration of a pump and dump', 'type', 24, GREY), 540, 1690)


def s6(c, t):
    i = 5; T0 = STARTS[i]
    words_line(c, t, [("THE", INK, T0 + 0.05), ("REAL", ACC, T0 + 0.2), ("JUNGLE", ACC, T0 + 0.35)], 'anton', 120, 250, key='rj')
    ta = at(i, 'April', -0.3); ts = at(i, 'SEBI passed', -0.3); tt = at(i, 'Telegram', -0.3); tf = at(i, 'fifty thousand', -0.3)
    if t > ta:
        p = pp(t, ta, 0.4, 1.3); place(c, card_box(940, 300, SOFT), 540, 520, p, -1)
        if p > 0.6:
            place(c, text_img('SEBI FINAL ORDER', 'osw5', 44, GREY), 540, 430)
            place(c, text_img('26 APRIL 2023', 'anton', 120, NAVY), 540, 545)
    if t > ts:
        phone(c, t, ts, 330, 1100, [('TIP CHANNEL', tt, INK), ('"BUY CALL" POSTS', tt + 0.4, GRN)], 0.62, 'TELEGRAM CHANNEL')
    if t > tf:
        p = pp(t, tf, 0.4, 1.3); place(c, card_box(460, 300, YEL), 780, 1100, p, 2)
        if p > 0.6:
            place(c, text_img('SUBSCRIBERS', 'osw5', 36, INK), 780, 1010, 1, 2)
            vv = SS.roll_number(t, tf, 1.6, 0, 50000)
            place(c, text_img(f'~{int(vv):,}', 'anton', 100, ACC), 780, 1110, 1, 2)
            place(c, text_img('(51,980 in Dec 2021)', 'mark', 32, NAVY), 780, 1200, 1, 2)
    aandhai(c, t, 860, 1480, 'calm', 0.3)
    src(c, t, 'SEBI order 26 Apr 2023; interim order Jan 2022 (via PTI, Reuters, Bar & Bench)', ta + 0.2, 1700, GREY, 22)


def s7(c, t):
    i = 6; T0 = STARTS[i]
    tb = at(i, 'bought first', -0.3); tp = at(i, 'posted buy', -0.3); ts = at(i, 'sold into', -0.3); tu = at(i, 'Unlawful', -0.3)
    place_text(c, 'WHAT SEBI FOUND', 'anton', 100, INK, 540, 230, t, 'sf', T0 + 0.05, 'pop')
    items = [('Admins bought the shares first', tb), ('Posted buy calls, did not disclose', tp), ('Sold into the price rise', ts)]
    d = ImageDraw.Draw(c)
    for k, (txt, tk) in enumerate(items):
        y = 420 + k * 170
        if t > tk - 0.4:
            p = pp(t, tk - 0.4, 0.3, 1.5); place(c, card_box(900, 140, SOFT), 540, y, p, (-1, 1, -1)[k])
            if p > 0.6:
                place(c, text_img(txt, 'osw5', 46, INK), 590, y)
                d.rounded_rectangle((120, y - 36, 192, y + 36), 12, outline=INK, width=5, fill=(255, 255, 255))
                if t > tk:
                    s = 1 + 0.3 * math.exp(-(t - tk) * 10)
                    d.line([(132, y), (150 * s if False else 150, y + 22), (184, y - 26)], fill=RED, width=11)
    if t > tu:
        p = pp(t, tu, 0.4, 1.3); place(c, card_box(940, 330, YEL), 540, 1110, p, -1)
        if p > 0.6:
            place(c, text_img('UNLAWFUL GAINS (SEBI)', 'osw5', 46, INK), 540, 1000)
            vv = SS.roll_number(t, tu + 0.2, 1.8, 0, 2.84)
            place(c, text_img(f'₹{vv:.2f} CRORE', 'anton', 130, ACC), 540, 1125)
        coins = int(clamp((t - tu) / 2.0) * 10)
        for k in range(coins): place(c, A.fee_coin('₹'), 200 + k * 76, 1420 - (k % 2) * 30, 0.42, k * 9)
    src(c, t, 'SEBI final order, 26 Apr 2023 (as reported by PTI)', tb, 1700, GREY, 24)


def s8(c, t):
    i = 7; T0 = STARTS[i]
    tp = at(i, 'Penalties', -0.3); tb = at(i, 'market bans', -0.3)
    place_text(c, 'THE RESULT', 'anton', 120, INK, 540, 240, t, 'rs', T0 + 0.05, 'pop')
    if t > tp:
        p = pp(t, tp, 0.4, 1.3); place(c, card_box(940, 320, SOFT), 540, 540, p, 1)
        if p > 0.6:
            place(c, text_img('PENALTIES (6 PEOPLE)', 'osw5', 44, GREY), 540, 440)
            vv = SS.roll_number(t, tp + 0.2, 1.6, 0, 5.8)
            place(c, text_img(f'~₹{vv:.1f} CRORE', 'anton', 130, ACC), 540, 560)
    if t > tb:
        s_, a = slam(t, tb); place(c, stamp_c('BANNED UP TO 3 YEARS', RED, 74, -5, 81), 540, 820, s_, 0, a)
    kili(c, t, 300, 1250, 'sad', False, 0.5)
    mani(c, t, 760, 1260, 'sad', 'head', 0.46)
    if t > tb + 0.6: place(c, label('PLUS: GAINS TO BE GIVEN BACK', NAVY), 540, 1570, 0.9 * pp(t, tb + 0.6), 1)
    src(c, t, 'SEBI order 26 Apr 2023 via PTI/Reuters. Bans of 1–3 years.', tp, 1700, GREY, 24)


def s9(c, t):
    i = 8; T0 = STARTS[i]
    ts = at(i, 'when a stranger', -0.3); te = at(i, 'You are the exit', -0.2)
    tc = VO[i] + DURS[i] + 0.1
    if t < tc:
        thatha(c, t, 540, 1150, 'happy', 1 if t > ts else 0, 0.75)
        place(c, label('YAANAI THATHA', BLUE), 540, 1530, 1.2 * pp(t, T0 + 0.2), -2)
        if t > ts:
            p = pp(t, ts, 0.4, 1.3); place(c, card_box(940, 420, YEL), 540, 480, p, -1)
            if p > 0.6:
                place(c, text_img("When a stranger's tip is free,", 'pf', 54, INK), 540, 370)
                place(c, text_img('you are not the customer.', 'pfi', 52, GREY), 540, 450)
                if t > te:
                    s_, a = slam(t, te); place(c, stamp_c('YOU ARE THE EXIT', ACC, 78, -3, 91), 540, 590, s_, 0, a)
    else:
        SS.cheat_sheet(c, t, tc, 'KAADU BANK · EP 2', [
            ('THE TRICK', 'BUY · TIP · SELL', ACC), ('SUBSCRIBERS', '~50,000', NAVY),
            ('UNLAWFUL GAINS', '₹2.84 CR', ORG), ('PENALTIES', '~₹5.8 CR', ACC), ('RULE', 'FREE TIP = EXIT', RED)], y0=240)
        kili(c, t, 230, 1540, 'calm', False, 0.3); thatha(c, t, 830, 1560, 'happy', 1, 0.3)
        src(c, t, 'Source: SEBI order, 26 Apr 2023 (via PTI, Reuters)', tc + 0.4, 1710, GREY, 24)


def s10(c, t):
    i = 9; T0 = STARTS[i]
    SS.send_frame(c, t, T0 + 0.05, "the friend in five tip groups", y=360)
    ts = at(i, 'Save this', -0.3)
    if t > ts:
        p = pp(t, ts, 0.4, 1.8); bob = math.sin((t - ts) * 7) * 8 * math.exp(-(t - ts) * 0.8)
        place(c, SS.bookmark_icon(100), 340, 640 + bob, p, -8)
        place(c, text_img('SAVE THIS', 'anton', 84, CREAM), 590, 640, p)
    tfo = at(i, 'follow', -0.2)
    if t > tfo:
        q = prog(t, tfo, 0.35); place(c, follow_btn(), 540, 800, 0.5 + 0.5 * eback(q), 0, clamp(q * 3))
    te = at(i, 'episode three', -0.3)
    if t > te:
        p = pp(t, te, 0.4, 1.3); place(c, card_box(800, 330, (255, 246, 214)), 600, 1170, p, 1.5)
        if p > 0.6:
            place(c, text_img('NEXT · EPISODE 3', 'osw5', 40, GREY), 640, 1060)
            place(c, text_img("PONNI'S HIDDEN NUTS", 'anton', 76, PINK), 640, 1150)
            place(c, text_img('(an emergency fund story)', 'mark', 40, NAVY), 640, 1240, 1, -1)
        ponni(c, t, 190, 1190, 'happy', 0.34 * p)
    for k, ln in enumerate(['Data: SEBI order, 26 Apr 2023 (via PTI, Reuters).',
                            'Fictional characters and group. Real case numbers.',
                            'No buy/sell call. Education only, not investment advice.']):
        place_text(c, ln, 'type', 21, (210, 204, 192), 540, 1560 + k * 38, t, None, T0 + 0.3, 'fade', track=1)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]

# camera move per scene: (kind, strength)
CAMS = ['crash', 'pullout', 'track', 'tilt', 'dutch', 'crash', 'pushin', 'whip', 'pushin', 'pushin']


def SLAMS():
    return [at(0, 'Fifty thousand', -0.2), at(1, 'episode two', -0.25), at(1, 'shortcut', -0.2), at(3, 'why for free', -0.2), STARTS[4] + 0.08,
            at(4, 'bought the stock', -0.3), at(4, 'before the message', -0.2), at(4, 'Then they sold', -0.2), at(7, 'market bans', -0.3),
            at(8, 'You are the exit', -0.2)] + [STARTS[k] + 0.05 for k in (1, 2, 5, 6, 7)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('KAADU BANK · EP 2', 'type', 30, ACC if not dark else YEL, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
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
