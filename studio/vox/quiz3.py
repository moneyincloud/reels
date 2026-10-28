"""Money quiz: 3 questions (rule of 72, inflation, loss recovery) — paper Vox v2"""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs
from fridge import follow_btn
import tea as TEA

import os
SH = ROOT + '' + os.environ.get('LDIR', 'quiz3') + '/'
CAP = os.environ.get('CAP', 'en')
CAPS_ON = os.environ.get('CAPS', '0') == '1'  # owner prefers NO on-screen subtitles
FONTS['ta'] = FD + 'noto-sans-tamil-tamil-800-normal.woff'
SCRIPT = json.load(open(SH + 'script.json'))
DURS = json.load(open(SH + 'vo/durs.json'))
LEAD, TAIL = 0.15, 0.3
STARTS, VO = [], []
_t = 0.0
PAUSE = {1: 0.9, 3: 0.9, 5: 0.9}   # thinking time after each question
for i, d in enumerate(DURS):
    STARTS.append(_t); VO.append(_t + (0.1 if i == 0 else LEAD)); _t = VO[-1] + d + TAIL + PAUSE.get(i, 0)
DUR = _t + 1.8
B = STARTS[1:]
SOFT = (253, 251, 246); NAVY = (30, 60, 120); BLUE = (40, 100, 200); GREY = (120, 116, 108); GOLD = (214, 160, 40)
PINK = (230, 90, 140); TEAL = (20, 140, 130); ORG = (230, 120, 30)
card_box = TEA.card_box; label = TEA.label; coin = TEA.coin

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
    if v >= 1e7: return f'₹{v / 1e7:.2f} Cr'
    if v >= 1e5: return f'₹{v / 1e5:.1f} L'
    return inr(v)



import saveshare as SS
TA = SCRIPT
NF = json.load(open(SH + 'closes.json'))


def spark(c, pts, p, col, w=12):
    n = len(pts) - 1; f = p * n; k = int(f); out = pts[:k + 1]
    if k < n: a, b = pts[k], pts[k + 1]; fr = f - k; out = out + [(a[0] + (b[0] - a[0]) * fr, a[1] + (b[1] - a[1]) * fr)]
    if len(out) >= 2: stroke(c, out, w, col)


def qnum(c, t, i, n, col=INK, txt=None):
    T0 = STARTS[i] + 0.05
    if t > T0:
        place(c, label(f'{n}/3', col), 120, 200, 1.1 * eback(prog(t, T0, 0.3), 1.6), -4)
    place_text(c, txt or f'QUESTION {n}', 'anton', 120, col, 560, 300, t, f'qn{i}', T0, 'pop')


def q_card(c, t, t0, lines, y=640, w=900):
    if t < t0: return
    h = 90 + 82 * len(lines)
    p = eback(prog(t, t0, 0.4), 1.3); place(c, card_box(w, h, SOFT), 540, y, p, -0.8)
    if p > 0.6:
        for k, (ln, col) in enumerate(lines):
            place(c, text_img(ln, 'anton', 66, col), 540, y - h / 2 + 80 + 82 * k)


def options(c, t, items, y0=980, pick=None, t_pick=None):
    """items: [(letter, text, t_in)]"""
    for k, (L, txt, tk) in enumerate(items):
        if t < tk: continue
        y = y0 + k * 120; p = eback(prog(t, tk, 0.35), 1.5)
        good = pick == k and t_pick is not None and t > t_pick
        col = GRN if good else (GREY if (t_pick is not None and t > t_pick) else NAVY)
        wob = math.sin(t * 3 + k) * 1.2
        im = card_box(700, 100, (226, 245, 232) if good else SOFT)
        place(c, im, 540, y, p, wob)
        if p > 0.6:
            place(c, label(L, col), 260, y, 1.0, 0)
            place(c, text_img(txt, 'anton', 60, INK), 580, y)


def countdown(c, t, i, x=540, y=1450, r=115):
    t3 = at(i, 'Three. Two', -0.05); t2 = at(i, 'Two. One', -0.05); t1 = at(i, 'One.', -0.05)
    tend = STARTS[i + 1] - 0.05
    if t < t3 or t > tend: return
    n = '3' if t < t2 else ('2' if t < t1 else '1')
    d = ImageDraw.Draw(c); pulse = 1 + 0.08 * math.exp(-((t - max(tt for tt in (t3, t2, t1) if tt <= t)) * 8))
    rr = r * pulse
    d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=SOFT, outline=INK, width=8)
    frac = clamp((t - t3) / (tend - t3))
    d.arc((x - rr + 14, y - rr + 14, x + rr - 14, y + rr - 14), -90, -90 + 360 * (1 - frac), fill=RED, width=22)
    if t > VO[i] + DURS[i]:
        n = '?'
    place(c, text_img(n, 'anton', 130, INK), x, y, pulse)
    place(c, text_img('think…', 'mark', 50, GREY), x + 250, y + 10, 1, -6)


def s1(c, t):
    i = 0
    # frame 0: giant "3" already slamming
    s_, a = slam(t, -0.12, 0.35)
    bob = math.sin(t * 4) * 6
    place(c, stamp_c('3', RED, 250, -6, 31), 270, 500 + bob, s_, 0, max(a, 0.6))
    place_text(c, 'MONEY', 'anton', 150, INK, 690, 430, t, 'h1', -0.1, 'pop')
    place_text(c, 'QUESTIONS', 'anton', 120, INK, 690, 580, t, 'h2', 0.15, 'pop')
    tw = at(i, 'most people', -0.2)
    if t > tw:
        s2_, a2 = slam(t, tw); place(c, stamp_c('MOST PEOPLE GET THEM WRONG', NAVY, 66, -3, 32), 540, 850, s2_, 0, a2)
    tc = at(i, 'Can you', -0.2)
    if t > tc:
        q = eback(prog(t, tc, 0.4), 1.6); sw = math.sin(t * 5) * 8
        place(c, text_img('?', 'anton', 260, YEL), 950, 1040, q, sw)
        place_text(c, 'can you answer them?', 'mark', 66, INK, 470, 1050, t, 'cy', tc, 'slide', rot=-2)
    ts = at(i, 'three seconds each', -0.2)
    for k in range(3):
        tk = ts + 0.15 * k
        if t > tk:
            x = 220 + 320 * k; y = 1310
            sh = 0
            if k == 2 and t > at(i, 'hurts', -0.3):
                sh = math.sin(t * 40) * 7
            place(c, card_box(260, 200, (255, 226, 222) if k == 2 else SOFT), x + sh, y, eback(prog(t, tk, 0.35), 1.5), (-4, 2, 5)[k])
            if t > tk + 0.15:
                place(c, text_img(f'Q{k + 1}', 'anton', 90, RED if k == 2 else INK), x + sh, y - 20, 1, (-4, 2, 5)[k])
                place(c, text_img('3 SEC', 'osw5', 38, GREY), x + sh, y + 60, 1, (-4, 2, 5)[k])
    th = at(i, 'hurts', -0.3)
    if t > th:
        s3_, a3 = slam(t, th); place(c, stamp_c('#3 HURTS THE MOST', RED, 80, 4, 33), 620, 1540, s3_, 0, a3)


def s2(c, t):
    i = 1
    qnum(c, t, i, 1)
    tm = at(i, 'Your money', -0.3)
    q_card(c, t, tm, [('MONEY GROWS 8% A YEAR.', INK), ('YEARS TO DOUBLE?', RED)], 600)
    options(c, t, [('A', '5 YEARS', at(i, 'How many', -0.2)), ('B', '9 YEARS', at(i, 'How many', 0.0)), ('C', '12 YEARS', at(i, 'How many', 0.2))], 900)
    if t > tm:  # idle coin stack growing
        n = 4 + int((t - tm) * 2) % 6
        d = ImageDraw.Draw(c)
        for j in range(n):
            yy = 1480 - j * 26; d.ellipse((780, yy - 20, 930, yy + 20), fill=GOLD, outline=INK, width=5)
    countdown(c, t, i, 400, 1430)


def doubling_chart(c, t, t0, rate=0.08, years=9, y0=1400, col=GRN):
    if t < t0: return
    p = eo(prog(t, t0, 1.8)); d = ImageDraw.Draw(c)
    vals = [(1 + rate) ** n for n in range(years + 1)]
    bw = 70; gap = 20; x0 = 540 - ((years + 1) * (bw + gap) - gap) / 2
    for n, v in enumerate(vals):
        if n / years > p + 1e-6: break
        hpx = 260 * v / 2
        x = x0 + n * (bw + gap)
        d.rounded_rectangle((x, y0 - hpx, x + bw, y0), 8, fill=col if n < years else YEL, outline=INK, width=3)
        if n in (0, years):
            c.alpha_composite(text_img(f'Y{n}', 'osw5', 30, GREY), (int(x + 10), int(y0 + 8)))
    lead = SS.roll_number(t, t0, 1.8, 100000, 100000 * vals[-1])
    place(c, text_img(inr(lead), 'anton', 72, INK), 540, y0 - 330)
    place(c, text_img('maths at a fixed 8% a year · illustration, not a forecast', 'type', 24, GREY), 540, y0 + 70)


def s3(c, t):
    i = 2
    T0 = STARTS[i] + 0.05
    s_, a = slam(t, T0); place(c, stamp_c('ABOUT 9 YEARS', GRN, 120, -4, 41), 540, 310, s_, 0, a)
    place(c, label('ANSWER: B', GRN), 540, 450, 1.2 * eback(prog(t, T0 + 0.1, 0.3), 1.6), -6)
    td = at(i, 'divide', -0.3)
    if t > td:
        place(c, card_box(860, 230, SOFT), 540, 640, eback(prog(t, td, 0.4), 1.3), 0.6)
        if t > td + 0.3:
            words_line(c, t, [('72', NAVY, td + 0.3), ('÷', INK, td + 0.45), ('RATE', RED, td + 0.6), ('=', INK, td + 0.75), ('YEARS', GRN, td + 0.9)], 'anton', 100, 610, key='eq')
            place_text(c, 'to double your money', 'mark', 44, GREY, 540, 710, t, None, td + 1.0, 'fade')
    te = at(i, 'Seventy two divided', -0.3)
    if t > te:
        words_line(c, t, [('72', NAVY, te), ('÷', INK, te + 0.15), ('8', RED, te + 0.3), ('=', INK, te + 0.45), ('9', GRN, te + 0.6)], 'anton', 130, 880, key='eq2')
    doubling_chart(c, t, at(i, 'divide', 0.3), 0.08, 9, 1460)
    tr = at(i, 'rule of', -0.3)
    if t > tr:
        s2_, a2 = slam(t, tr); place(c, stamp_c('RULE OF 72', NAVY, 80, 4, 42), 800, 1610, s2_, 0, a2)


def rupee_note(scale_v, fade=0):
    w, h = int(520 * scale_v), int(260 * scale_v)
    im = Image.new('RGBA', (w + 12, h + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((12, 12, w + 11, h + 11), 18, fill=INK)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 18, fill=(196, 170, 220), outline=INK, width=6)
    d.ellipse((w * 0.62, h * 0.18, w * 0.9, h * 0.82), outline=INK, width=4)
    t_ = text_img('₹100', 'anton', max(20, int(110 * scale_v)), INK); im.alpha_composite(t_, (int(w * 0.08), int(h / 2 - t_.size[1] / 2)))
    return im


def s4(c, t):
    i = 3
    T0 = STARTS[i] + 0.05
    if t - T0 < 0.25: c.alpha_composite(Image.new('RGBA', c.size, (255, 214, 51, int(140 * (1 - (t - T0) / 0.25)))))
    tg = at(i, 'Now it gets', -0.3)
    if t < at(i, 'Prices', -0.4):
        place_text(c, 'GOT IT?', 'anton', 130, INK, 540, 400, t, 'gi', T0, 'pop')
        if t > tg:
            s_, a = slam(t, tg); place(c, stamp_c('NOW IT GETS HARDER', RED, 100, -4, 51), 540, 650, s_, 0, a)
        for k in range(3):
            x = 220 + 320 * k; y = 1050 + math.sin(t * 4 + k) * 10
            place(c, card_box(260, 200, (226, 245, 232) if k == 0 else SOFT), x, y, eback(prog(t, T0 + 0.2 + 0.1 * k, 0.35), 1.5), (-4, 2, 5)[k])
            place(c, text_img(f'Q{k + 1}', 'anton', 90, GRN if k == 0 else INK), x, y - 20, 1, (-4, 2, 5)[k])
            if k == 0: ImageDraw.Draw(c).line((x - 50, y + 50, x - 15, y + 85, x + 60, y + 15), fill=GRN, width=14)
            if k == 1 and t > tg: place(c, text_img('NEXT', 'osw5', 38, RED), x, y + 62)
        return
    qnum(c, t, i, 2)
    tp = at(i, 'Prices', -0.4)
    q_card(c, t, tp, [('PRICES RISE 6% A YEAR.', INK), ('AFTER 12 YEARS,', INK), ('₹100 BUYS…?', RED)], 640)
    options(c, t, [('A', '₹94 WORTH', at(i, 'what does', -0.2)), ('B', '₹72 WORTH', at(i, 'what does', 0.0)), ('C', '₹50 WORTH', at(i, 'what does', 0.2))], 960)
    countdown(c, t, i, 400, 1430)
    place(c, rupee_note(0.45), 840, 1640 + math.sin(t * 3) * 8, 1, math.sin(t * 2) * 4)


def s5(c, t):
    i = 4
    T0 = STARTS[i] + 0.05
    s_, a = slam(t, T0); place(c, stamp_c('ONLY ₹50 WORTH', RED, 120, -4, 61), 540, 310, s_, 0, a)
    place(c, label('ANSWER: C', GRN), 540, 450, 1.2 * eback(prog(t, T0 + 0.1, 0.3), 1.6), -6)
    # shrinking note + year counter
    t0 = T0 + 0.4
    q = eio(prog(t, t0, 4.0)); yrs = 12 * q; val = 100 / 1.06 ** yrs
    if t > t0:
        place(c, rupee_note(0.4 + 0.6 * (val / 100)), 540, 700, 1, -2)
        place(c, text_img(f'YEAR {int(yrs):d}', 'osw5', 50, GREY), 300, 960)
        place(c, text_img(f'buys ₹{val:.0f} worth', 'anton', 70, RED if val < 70 else INK), 700, 960)
    te = at(i, 'Seventy two divided', -0.3)
    if t > te:
        words_line(c, t, [('72', NAVY, te), ('÷', INK, te + 0.15), ('6%', RED, te + 0.3), ('=', INK, te + 0.45), ('12 YRS', GRN, te + 0.6)], 'anton', 110, 1130, key='eq3')
    ta_ = at(i, 'against you', -0.4)
    if t > ta_:
        place(c, label('SAME RULE, WORKING AGAINST YOU', RED), 540, 1290, 1.2 * eback(prog(t, ta_, 0.35), 1.6), -2)
    th = at(i, 'halved', -0.3)
    if t > th:
        place_text(c, 'your money halved — and you never spent it', 'mark', 46, NAVY, 540, 1420, t, 'hv', th, 'slide', rot=-2)
        place(c, text_img('maths at a fixed 6% inflation · illustration · RBI target is 4% ±2%', 'type', 24, GREY), 540, 1520)


def s6(c, t):
    i = 5
    T0 = STARTS[i] + 0.05
    if t - T0 < 0.3: c.alpha_composite(Image.new('RGBA', c.size, (226, 58, 44, int(120 * (1 - (t - T0) / 0.3)))))
    qnum(c, t, i, 3, RED, 'FINAL QUESTION')
    th = at(i, 'this one hurts', -0.3)
    if t > th:
        s_, a = slam(t, th); place(c, stamp_c('THIS ONE HURTS', RED, 70, 5, 71), 780, 460, s_, 0, a)
    tf = at(i, 'Your investment', -0.3)
    q_card(c, t, tf, [('YOUR MONEY FALLS 50%.', INK), ('RISE NEEDED TO', INK), ('GET BACK?', RED)], 700)
    options(c, t, [('A', '+50%', at(i, 'How much', -0.2)), ('B', '+75%', at(i, 'How much', 0.0)), ('C', '+100%', at(i, 'How much', 0.2))], 1010)
    countdown(c, t, i, 400, 1450)
    if t > tf:  # falling arrow idle
        y = 1450 + 20 * math.sin(t * 4); d = ImageDraw.Draw(c)
        d.polygon([(800, y - 80), (880, y - 80), (880, y + 10), (920, y + 10), (840, y + 90), (760, y + 10), (800, y + 10)], fill=RED, outline=INK)


def nifty_chart(c, t, t0, x0=150, x1=930, yt=760, yb=1180):
    v = NF['NIFTY']; hi = NF['high']; lo = min(v)
    sc = lambda p: yt + (yb - yt) * (hi - p) / (hi - lo)
    pts = [(x0 + (x1 - x0) * k / (len(v) - 1), sc(p)) for k, p in enumerate(v)]
    p = eio(prog(t, t0, 1.8)); d = ImageDraw.Draw(c)
    place(c, card_box(920, 600, SOFT), 540, 960, eback(prog(t, t0 - 0.3, 0.4), 1.3), -0.4)
    if t < t0: return
    for gy in (yt, (yt + yb) / 2, yb): d.line((x0, gy, x1, gy), fill=(225, 220, 210), width=2)
    d.line((x0, sc(hi), x1, sc(hi)), fill=GRN, width=4)
    place(c, text_img('JAN HIGH 26,373', 'osw5', 34, GRN), 300, sc(hi) - 30)
    spark(c, pts, p, NAVY, 9)
    f = p * (len(pts) - 1); k = min(int(f), len(pts) - 2); fr = f - k
    tx = pts[k][0] + (pts[k + 1][0] - pts[k][0]) * fr; ty = pts[k][1] + (pts[k + 1][1] - pts[k][1]) * fr
    val = v[k] + (v[k + 1] - v[k]) * fr
    d.ellipse((tx - 11, ty - 11, tx + 11, ty + 11), fill=RED, outline=INK, width=3)
    place(c, text_img(f'{val:,.0f}', 'anton', 48, INK), min(tx, 850), ty + 45 if ty < 1120 else ty - 45)
    place(c, text_img('NIFTY 50 · weekly close · last 12 months · NSE via INDmoney, to 27 Oct 2026', 'type', 21, GREY), 540, 1230)


def s7(c, t):
    i = 6
    T0 = STARTS[i] + 0.05
    tc = at(i, 'real clue', -0.4)
    if t < tc + 0.2:
        SS.myth_fact(c, t, T0, ['Falls 50%', 'needs +50%', 'to recover'], ['Falls 50%', 'needs MORE', 'than 50%'], y0=250, y1=1500)
        return
    place_text(c, 'REAL CLUE', 'anton', 120, INK, 540, 300, t, 'rc', tc + 0.2, 'pop')
    place_text(c, 'most people say +50%. wrong.', 'mark', 44, RED, 540, 420, t, None, tc + 0.3, 'fade')
    tn = at(i, 'The Nifty', -0.3)
    nifty_chart(c, t, tn + 0.3)
    tf = at(i, 'fourteen percent below', -0.3)
    if t > tf:
        s_, a = slam(t, tf); place(c, stamp_c('-14% FROM HIGH', RED, 80, -4, 81), 330, 1390, s_, 0, a)
    tg = at(i, 'sixteen percent', -0.3)
    if t > tg:
        s_, a = slam(t, tg); place(c, stamp_c('NEEDS +16% BACK', GRN, 80, 4, 82), 740, 1530, s_, 0, a)
        place_text(c, '22,750 TO 26,373 = +16%', 'osw5', 44, INK, 540, 1660, t, None, tg + 0.3, 'fade')


def s8(c, t):
    i = 7
    T0 = STARTS[i] + 0.05
    tch = at(i, 'Big losses', -0.6)
    if t < tch:
        tr = at(i, 'one hundred', -0.5)
        place_text(c, 'THE ANSWER', 'anton', 110, INK, 540, 290, t, 'an', T0, 'pop')
        place(c, label('ANSWER: C', GRN), 540, 770, 1.2 * eback(prog(t, tr + 0.4, 0.3), 1.6), -3)
        if t > tr:
            SS.tear_reveal(c, t, tr, stamp_c('+100%', GRN, 190, -4, 91), 540, 560)
        tl = at(i, 'One lakh falls', -0.3)
        d = ImageDraw.Draw(c)
        bars = [('START', 100000, NAVY, tl), ('AFTER -50%', 50000, RED, at(i, 'fifty thousand,', -0.3)), ('NEEDS ×2', 100000, GRN, at(i, 'must double', -0.3))]
        for k, (nm, v, cl, tk) in enumerate(bars):
            if t < tk: continue
            q = eo(prog(t, tk, 0.6)); x = 240 + 300 * k; hpx = 440 * v / 100000 * q
            d.rounded_rectangle((x - 90, 1400 - hpx, x + 90, 1400), 12, fill=cl, outline=INK, width=4)
            place(c, text_img(nm, 'osw5', 40, INK), x, 1450)
            place(c, text_img(inr(v * q), 'anton', 50, INK), x, 1400 - hpx - 40)
        if t > at(i, 'must double', 0.1):
            marker_line(c, [(560, 1100), (690, 950)], eo(prog(t, at(i, 'must double', 0.1), 0.4)), GRN, 10, head=True)
        return
    SS.cheat_sheet(c, t, tch, 'MONEY QUIZ CHEAT SHEET', [
        ('72 ÷ RATE', '= YEARS TO DOUBLE', NAVY),
        ('6% INFLATION, 12 YRS', 'HALF THE VALUE', RED),
        ('FALL 20%', 'NEEDS +25%', ORG),
        ('FALL 50%', 'NEEDS +100%', GRN),
        ('NIFTY -14% (27 OCT)', 'NEEDS +16%', BLUE),
    ], y0=420)


def s9(c, t):
    i = 8
    T0 = STARTS[8]
    t0 = T0 + 0.1; y = 400
    if t > t0:
        p = eback(prog(t, t0, 0.4), 1.3)
        place(c, SS._card(900, 300, YEL), 540, y, p, -1.5)
        if p > 0.6:
            place(c, text_img('SEND THIS TO', 'anton', 64, INK), 540, y - 80)
            place(c, text_img('the friend who thinks', 'mark', 54, NAVY), 540, y + 5, 1, -1)
            place(c, text_img("he's great with money", 'mark', 54, NAVY), 540, y + 85, 1, -1)
        q = prog(t, t0 + 0.3, 1.1)
        if 0 < q < 1:
            place(c, SS.plane_icon(110), 80 + 920 * eio(q), y - 230 - 160 * math.sin(math.pi * q), 1, 15 - 30 * q)
    ts = at(i, 'Save this', -0.3)
    SS.save_pulse(c, t, ts, 560, 680)
    if t > ts: c.alpha_composite(text_img('SAVE THIS', 'anton', 84, CREAM), (int(560 + 60 - text_img('SAVE THIS', 'anton', 84, CREAM).size[0] / 2), int(680 - text_img('SAVE THIS', 'anton', 84, CREAM).size[1] / 2)))
    tfo = at(i, 'follow', -0.2)
    if t > tfo:
        pp = prog(t, tfo, 0.35); place(c, follow_btn(), 540, 820, 0.5 + 0.5 * eback(pp), 0, clamp(pp * 3))
    for k, ln in enumerate(['Nifty data: NSE via INDmoney, weekly closes to 27 Oct 2026.', 'Doubling & inflation: simple maths at fixed rates, illustration only.', 'Not a forecast. Past data does not predict future returns.', 'Education only. Not investment advice.']):
        place_text(c, ln, 'type', 25, (210, 204, 192), 540, 980 + k * 40, t, None, T0 + 0.3, 'fade', track=1)
    tb = at(i, 'how many', -0.3)
    if t > tb:
        place_text(c, 'HOW MANY DID YOU', 'anton', 100, CREAM, 540, 1250, t, 'hm', tb, 'pop')
        place_text(c, 'GET RIGHT?', 'anton', 130, YEL, 540, 1380, t, 'hm2', tb + 0.15, 'pop')
        for k, s in enumerate(['0/3', '1/3', '2/3', '3/3']):
            place(c, label(s, (RED, ORG, BLUE, GRN)[k]), 210 + 220 * k, 1540, 1.2 * eback(prog(t, tb + 0.4 + 0.1 * k, 0.3), 1.6), (-4, 3, -2, 4)[k])


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]


def SLAMS():
    return [STARTS[k] + 0.05 for k in range(1, 9)] + [at(0, 'hurts', -0.3), at(6, 'fourteen percent below', -0.3), at(6, 'sixteen percent', -0.3), at(7, 'one hundred', -0.5)]

# ---------- captions ----------
def text_ta(word, size, col):
    runs, cur, isT = [], '', None
    for ch in word:
        t_ = 0x0B80 <= ord(ch) <= 0x0BFF or ch in '\u200c\u200d'
        if isT is None or t_ == isT: cur += ch
        else: runs.append((cur, isT)); cur = ch
        isT = t_
    if cur: runs.append((cur, isT))
    ims = [text_img(r, 'ta' if tt else 'osw', size if tt else int(size * 1.05), col) for r, tt in runs]
    h = max(m.size[1] for m in ims); w = sum(m.size[0] for m in ims)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); x = 0
    for m in ims: im.alpha_composite(m, (x, h - m.size[1])); x += m.size[0]
    return im


@functools.lru_cache(maxsize=None)
def cap_chunks(i):
    txt = TA[i] if CAP == 'ta' else SCRIPT[i]
    fn, size = ('ta', 50) if CAP == 'ta' else ('anton', 66)
    words = txt.split(); pos = []; c0 = 0
    for w_ in words:
        k = txt.find(w_, c0); pos.append(k / len(txt)); c0 = k + len(w_)
    chunks, cur, cw = [], [], 0
    for j, w_ in enumerate(words):
        ww = font(fn, size).getlength(w_ + ' ')
        if cur and (cw + ww > 860 or len(cur) >= (3 if CAP == 'ta' else 4) or words[cur[-1]][-1] in '.?!,:'):
            chunks.append(cur); cur, cw = [], 0
        cur.append(j); cw += ww
    if cur: chunks.append(cur)
    return words, pos, chunks, fn, size


@functools.lru_cache(maxsize=512)
def cap_img(i, ci, hj):
    words, pos, chunks, fn, size = cap_chunks(i)
    ims = [(text_ta(words[j], size, CREAM) if CAP == 'ta' else text_img(words[j].upper(), fn, size, YEL if j == hj else CREAM)) for j in chunks[ci]]
    gap = 18; w = sum(m.size[0] for m in ims) + gap * (len(ims) - 1) + 56; h = max(m.size[1] for m in ims) + 30
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 22, fill=(20, 20, 22, 215))
    x = 28
    for m in ims: im.alpha_composite(m, (x, (h - m.size[1]) // 2)); x += m.size[0] + gap
    return im


def captions(c, t):
    i = scene_at(t)
    if t < VO[i] or t > VO[i] + DURS[i] + 0.25: return
    words, pos, chunks, fn, size = cap_chunks(i)
    f = (t - VO[i]) / DURS[i]; hj = 0
    for j, p in enumerate(pos):
        if f >= p: hj = j
    ci = next(k for k, ch in enumerate(chunks) if hj in ch)
    place(c, cap_img(i, ci, hj), 540, 1665)


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('MONEY QUIZ · 3 QUESTIONS', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
    ImageDraw.Draw(c).line((60, 118, W - 60, 118), fill=col, width=2)
    ImageDraw.Draw(c).line((60, 118, 60 + (W - 120) * clamp(t / DUR), 118), fill=RED if not dark else YEL, width=8)


def transition(c, t):
    cols = [(TEAL, INK), (GOLD, INK), (ORG, CREAM), (RED, YEL), (PINK, CREAM), (YEL, INK), (BLUE, CREAM), (INK, RED), (YEL, NAVY)]
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


def slam_times():
    return SLAMS()


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
    if not loop and (CAPS_ON or CAP == 'ta'): captions(c, t)
    header(c, dark, t if not loop else 0); transition(c, t)
    arr = np.asarray(c.convert('RGB')).astype(np.float32)
    g = grain_frames()[int(t * FPS) % 6]
    fl = 1 + 0.012 * math.sin(t * 37) * math.sin(t * 13)
    return np.clip(arr * fl + g[..., None], 0, 255).astype(np.uint8)
