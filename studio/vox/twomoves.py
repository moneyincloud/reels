"""twomoves — Same results season, opposite moves: Laurus Labs vs Intellect Design (2 Nov 2026)"""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs
from fridge import follow_btn
import tea as TEA
import saveshare as SS

import os
SH = ROOT + '' + os.environ.get('LDIR', 'twomoves') + '/'
CAP = os.environ.get('CAP', 'en')
CAPS_ON = os.environ.get('CAPS', '0') == '1'  # owner prefers NO on-screen subtitles
FONTS['ta'] = FD + 'noto-sans-tamil-tamil-800-normal.woff'
SCRIPT = json.load(open(SH + 'script.json'))
DURS = json.load(open(SH + 'vo/durs.json'))
LEAD, TAIL = 0.15, 0.3
STARTS, VO = [], []
_t = 0.0
for i, d in enumerate(DURS):
    STARTS.append(_t); VO.append(_t + (0.1 if i == 0 else LEAD)); _t = VO[-1] + d + TAIL
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



def biz_card(name, col, tags, w=900):
    h = 150 + 70 * len(tags)
    im = card_box(w, h, SOFT); comp(im, text_img(name, 'anton', 80, col), 40, 24)
    for k, t in enumerate(tags):
        comp(im, text_img('•  ' + t, 'osw', 44, INK), 50, 140 + k * 70)
    return im


def value_line(c, t, t0, v, y=1430, col=GRN, dur=1.2):
    if t < t0: return
    p = eo(prog(t, t0, dur)); vv = 100000 + (v - 100000) * p
    place(c, card_box(820, 200, SOFT), 540, y)
    place(c, text_img('₹1 lakh', 'osw', 56, GREY), 260, y)
    marker_line(c, [(370, y), (450, y)], 1, GREY, 8, head=True, head_size=22)
    place(c, text_img(inr(vv), 'anton', 96, col), 700, y)


def stock_header(c, t, i, n, key):
    nm, col, v, mult = STOCKS[key][:4]
    t0 = STARTS[i] + 0.05
    if t > t0:
        sc, a = slam(t, t0); place(c, stamp_c(f'#{n}', col, 110, -6, 950 + n), 160, 290, sc, 0, a)
    place_text(c, nm, 'anton', 104, INK, 620, 290, t, f'nm{i}', t0 + 0.1, 'pop')


def spark(c, pts, p, col, w=12):
    n = len(pts) - 1; f = p * n; k = int(f); out = pts[:k + 1]
    if k < n: a, b = pts[k], pts[k + 1]; fr = f - k; out = out + [(a[0] + (b[0] - a[0]) * fr, a[1] + (b[1] - a[1]) * fr)]
    if len(out) >= 2: stroke(c, out, w, col)




CLOSES = json.load(open(SH + 'closes.json'))
TA = SCRIPT  # captions are OFF; Tamil track not used
LCOL, ICOL = GRN, RED


def rs(v):
    return inr(v) if v >= 1000 else '₹' + (f'{v:.0f}' if v >= 100 else f'{v:.2f}')


@functools.lru_cache(maxsize=None)
def icon(key):
    im = Image.new('RGBA', (200, 160), (0, 0, 0, 0)); d = ImageDraw.Draw(im); O = INK; w = 6
    if key == 'INTELLECT':  # laptop with a bank on screen
        d.rounded_rectangle((35, 15, 165, 105), 10, fill=CREAM, outline=O, width=w)
        d.polygon([(10, 112), (190, 112), (175, 140), (25, 140)], fill=GREY, outline=O)
        d.line([(10, 112), (190, 112), (175, 140), (25, 140), (10, 112)], fill=O, width=w)
        d.polygon([(100, 28), (60, 50), (140, 50)], fill=NAVY)
        for x in (70, 92, 114, 132): d.rectangle((x - 4, 55, x + 4, 85), fill=NAVY)
        d.rectangle((58, 86, 142, 94), fill=NAVY)
    else:  # capsule pill + tablet
        d.rounded_rectangle((20, 50, 150, 110), 30, fill=CREAM, outline=O, width=w)
        d.pieslice((20, 50, 80, 110), 90, 270, fill=GRN); d.rectangle((50, 53, 85, 107), fill=GRN)
        d.rounded_rectangle((20, 50, 150, 110), 30, outline=O, width=w); d.line((85, 52, 85, 108), fill=O, width=w)
        d.ellipse((135, 85, 195, 145), fill=(220, 236, 255), outline=O, width=w); d.line((145, 115, 185, 115), fill=O, width=4)
    return im


def chart_pts(key, x0, x1, yt, yb):
    v = CLOSES[key]; lo, hi = min(v), max(v)
    return [(x0 + (x1 - x0) * k / (len(v) - 1), yt + (yb - yt) * (hi - p) / (hi - lo)) for k, p in enumerate(v)], v


def tip_chart(c, t, t0, key, col, x0, x1, yt, yb, dur=1.4, fmt=rs, tag=None):
    """Real weekly closes drawn left-to-right with a ticking price counter at the tip."""
    if t < t0: return 0
    pts, v = chart_pts(key, x0, x1, yt, yb); d = ImageDraw.Draw(c)
    for gy in (yt, (yt + yb) / 2, yb): d.line((x0, gy, x1, gy), fill=(225, 220, 210), width=2)
    p = eio(prog(t, t0, dur)); spark(c, pts, p, col, 9)
    f = p * (len(pts) - 1); k = min(int(f), len(pts) - 2); fr = f - k
    tx = pts[k][0] + (pts[k + 1][0] - pts[k][0]) * fr; ty = pts[k][1] + (pts[k + 1][1] - pts[k][1]) * fr
    val = v[k] + (v[k + 1] - v[k]) * fr
    r = 9 if p < 1 else 13 + 2 * math.sin(t * 8)
    d.ellipse((tx - r, ty - r, tx + r, ty + r), fill=col, outline=INK, width=3)
    if p < 1:
        lab = text_img(fmt(val), 'anton', 46, INK)
        place(c, lab, min(max(tx, x0 + 120), x1 - lab.size[0] / 2 + 30), ty - 44 if ty > yt + 60 else ty + 44)
    else:
        lab = label(tag or fmt(val), col)
        place(c, lab, tx - lab.size[0] / 2 - 30, ty + 50 if ty < (yt + yb) / 2 else ty - 50, 1.0 + 0.04 * math.sin(t * 6))
    return p


def bar(c, t, t0, y, name, pct, maxpct, col, x0=330, wmax=560, suffix='%'):
    if t < t0: return
    ph = eo(prog(t, t0, 0.9)); w = int(wmax * min(pct, maxpct) / maxpct * ph)
    place(c, text_img(name, 'osw5', 44, INK), 200, y)
    d = ImageDraw.Draw(c); d.rounded_rectangle((x0, y - 32, x0 + max(w, 12), y + 32), 12, fill=col, outline=INK, width=4)
    c.alpha_composite(text_img(f'+{pct * ph:.0f}{suffix}', 'anton', 58, col), (x0 + max(w, 12) + 16, int(y - 36)))


def src_line(c, t, t0, txt, y=1640):
    if t > t0:
        sz = 26
        while sz > 16 and text_w(txt, 'type', sz, 1) > 960: sz -= 1
        place_text(c, txt, 'type', sz, GREY, 540, y, t, None, t0, 'fade', track=1)


# ---------- scenes ----------
def s1(c, t):  # HOOK: frame 0 = big counter already moving
    i = 0
    words_line(c, t, [("SALES", GRN, 0.0), ("GREW", GRN, 0.12)], 'anton', 150, 300, key='h')
    if t < 2.5:
        aw = ImageDraw.Draw(c); y = 300 - 12 * math.sin(t * 6)
        aw.polygon([(950, y + 35), (1005, y - 35), (1060, y + 35)], fill=GRN, outline=INK)
    pv = -16.31 * eo(prog(t, -0.3, 1.4))
    shake = math.sin(t * 50) * 10 * math.exp(-max(0, t - 1.1) * 5) if t > 1.1 else 0
    big = text_img(f'{pv:.0f}%', 'anton', 330, RED)
    place(c, big, 540 + shake, 640, 1.0 + 0.05 * math.sin(t * 3))
    # falling arrow beside the number
    q = prog(t, 0.0, 1.1); d = ImageDraw.Draw(c)
    ya = 470 + 260 * eo(q)
    d.line((960, 470, 960, ya), fill=RED, width=18); d.polygon([(925, ya), (995, ya), (960, ya + 50)], fill=RED)
    place_text(c, 'IN ONE DAY · 30 OCT 2026', 'osw5', 46, INK, 540, 860, t, 'od', 0.6, 'slide')
    tb = at(i, 'still crashed', -0.2)
    if t > tb: place(c, icon('INTELLECT'), 540, 1020, 1.2 * eback(prog(t, tb, 0.35), 1.6), -4)
    tw = at(i, "You're reading", -0.25)
    if t > tw:
        s_, a = slam(t, tw); place(c, stamp_c("YOU'RE READING", RED, 96, -5, 901), 540, 1220, s_, 0, a)
    if t > tw + 0.25:
        s_, a = slam(t, tw + 0.25); place(c, stamp_c('RESULTS WRONG', RED, 110, 4, 902), 540, 1360, s_, 0, a)
    if t > tw + 0.6:
        bob = math.sin(t * 6) * 10; place(c, text_img('?', 'anton', 180, NAVY), 985, 1180 + bob, 1, 10)
    src_line(c, t, 1.4, 'Intellect Design Arena · NSE close 30 Oct 2026 · INDmoney', 1560)


def stock_card(c, t, t0, y, key, nm, sub, col, pct, tag):
    if t < t0: return
    p = eback(prog(t, t0, 0.4), 1.3); place(c, card_box(940, 500, SOFT), 540, y, p, -0.6 if key == 'INTELLECT' else 0.6)
    if p < 0.6: return
    place(c, icon(key), 160, y - 170, 0.55, -4)
    c.alpha_composite(text_img(nm, 'anton', 64, INK), (240, int(y - 215)))
    c.alpha_composite(text_img(sub, 'osw5', 34, GREY), (242, int(y - 135)))
    tip_chart(c, t, t0 + 0.35, key, col, 130, 880, y - 60, y + 150, 1.5, tag=tag)
    tp = t0 + 1.6
    if t > tp:
        s_, a = slam(t, tp); place(c, stamp_c(pct, col, 70, -6 if key == 'INTELLECT' else 6, 930 + len(key)), 850, y - 150, s_, 0, a)


def s2(c, t):
    i = 1
    stock_card(c, t, at(i, 'Intellect', -0.3), 560, 'INTELLECT', 'INTELLECT DESIGN', 'fell to a 52-week low', ICOL, '-16%', '₹505')
    stock_card(c, t, at(i, 'Laurus', -0.3), 1170, 'LAURUS', 'LAURUS LABS', 'jumped to a record high', LCOL, '+7%', '₹2,406')
    src_line(c, t, STARTS[1] + 0.4, 'weekly closes, 12 months to 30 Oct 2026 · NSE via INDmoney', 1500)


def s3(c, t):
    i = 2
    for k, (key, txt, x, ph) in enumerate([('INTELLECT', 'BANK SOFTWARE', 290, 'bank software'), ('LAURUS', 'MEDICINES', 790, 'medicines')]):
        tk = at(i, ph, -0.4)
        if t > tk:
            p = eback(prog(t, tk, 0.35), 1.6); bob = math.sin(t * 4 + k) * 6
            place(c, icon(key), x, 380 + bob, 1.1 * p, (-4, 4)[k])
            place(c, label(txt, NAVY), x, 530, 1.0 * p, (-2, 2)[k])
    tg = at(i, 'Both grew', -0.3)
    if t > tg:
        place_text(c, 'BOTH GREW SALES', 'anton', 100, GRN, 540, 700, t, 'bg', tg, 'pop')
        bar(c, t, tg + 0.2, 850, 'LAURUS', 33, 40, LCOL)
        bar(c, t, tg + 0.4, 950, 'INTELLECT', 11, 40, LCOL)
        place_text(c, 'Q2 FY27 revenue / income growth, YoY · company results 29-30 Oct 2026', 'type', 22, GREY, 540, 1030, t, None, tg + 0.5, 'fade', track=1)
    tc = at(i, 'cheer one', -0.3)
    if t > tc: place(c, label('CHEER?', GRN), 310, 1180, 1.4 * eback(prog(t, tc, 0.35), 1.6), -5)
    td = at(i, 'dump the other', -0.3)
    if t > td:
        sh = math.sin(t * 40) * 6 * math.exp(-(t - td) * 3)
        place(c, label('DUMP?', RED), 770 + sh, 1180, 1.4 * eback(prog(t, td, 0.35), 1.6), 5)
    if t > td + 0.3:  # visible open loop
        q = 1 + 0.08 * math.sin(t * 7); place(c, text_img('?', 'anton', 260, NAVY), 540, 1420, q * eback(prog(t, td + 0.3, 0.4), 1.6))


def s4(c, t):  # REHOOK: myth vs fact
    i = 3
    T0 = STARTS[3] + 0.05
    if t - T0 < 0.25: c.alpha_composite(Image.new('RGBA', c.size, (240, 196, 40, int(110 * (1 - clamp((t - T0) / 0.25))))))
    SS.myth_fact(c, t, at(i, 'Most people', -0.2), ['SALES UP', '=', 'STOCK UP'], ['WATCH', 'THE PROFIT', 'LINE'], y0=250, y1=1560)
    tw = at(i, 'wait till', -0.3)
    if t > tw: place(c, label('WAIT FOR IT...', NAVY), 540, 1500, 1.2 * eback(prog(t, tw, 0.35), 1.6), -3)


def s5(c, t):  # Laurus numbers
    i = 4; T0 = STARTS[4] + 0.05
    if t > T0: place(c, icon('LAURUS'), 170, 280, 0.7 * eback(prog(t, T0, 0.35), 1.6), -5)
    place_text(c, 'LAURUS LABS', 'anton', 110, INK, 600, 280, t, 'l5', T0, 'pop')
    place_text(c, 'Q2 FY27 · July-Sept 2026 · vs last year', 'osw5', 40, GREY, 540, 385, t, 'l5s', T0 + 0.2, 'slide')
    tr = at(i, 'Revenue', -0.3)
    if t > tr:
        p = eback(prog(t, tr, 0.4), 1.3); place(c, card_box(920, 420, SOFT), 540, 640, p, -0.5)
        if p > 0.6:
            bar(c, t, tr + 0.2, 560, 'REVENUE', 33, 126, LCOL, x0=360, wmax=430)
            tp = at(i, 'Profit up', -0.3)
            bar(c, t, tp, 700, 'PROFIT', 126, 126, LCOL, x0=360, wmax=430)
            if t > tp + 0.9: place(c, text_img('profit grew ~4x faster than sales', 'mark', 46, NAVY), 540, 790, 1, -1)
    t4 = at(i, 'four hundred', -0.3)
    if t > t4:
        v = SS.roll_number(t, t4, 1.0, 0, 441)
        place(c, text_img(f'₹{v:.0f} CR', 'anton', 140, GRN), 540, 990, 1.0 + 0.04 * math.sin(t * 5))
        place(c, text_img('net profit', 'osw5', 40, GREY), 540, 1090)
    tm = at(i, 'Margins', -0.3)
    if t > tm:
        p = eback(prog(t, tm, 0.4), 1.3); place(c, card_box(920, 260, SOFT), 540, 1320, p, 0.5)
        if p > 0.6:
            m = SS.roll_number(t, tm + 0.3, 1.2, 26, 34.5)
            place(c, text_img('EBITDA MARGIN', 'osw5', 42, GREY), 540, 1235)
            place(c, text_img('26%', 'anton', 90, GREY), 300, 1335)
            marker_line(c, [(400, 1335), (560, 1335)], clamp((t - tm - 0.3) / 0.4), GRN, 10, head=True, head_size=28)
            place(c, text_img(f'{m:.1f}%', 'anton', 110, GRN), 760, 1335)
    src_line(c, t, T0 + 0.5, 'Source: Laurus Labs Q2 FY27 results, 29 Oct 2026 (NSE filing)', 1550)


def s6(c, t):  # Intellect numbers
    i = 5; T0 = STARTS[5] + 0.05
    if t > T0: place(c, icon('INTELLECT'), 160, 280, 0.7 * eback(prog(t, T0, 0.35), 1.6), -5)
    place_text(c, 'INTELLECT', 'anton', 120, INK, 590, 280, t, 'i6', T0, 'pop')
    place_text(c, 'Q2 FY27 · July-Sept 2026', 'osw5', 40, GREY, 540, 390, t, 'i6s', T0 + 0.2, 'slide')
    ti = at(i, 'Income up', -0.3)
    if t > ti:
        p = eback(prog(t, ti, 0.4), 1.3); place(c, card_box(920, 200, SOFT), 540, 560, p, -0.5)
        if p > 0.6:
            bar(c, t, ti + 0.2, 540, 'INCOME', 11, 40, LCOL, x0=330, wmax=520)
            place(c, text_img('total income ₹878 Cr vs ₹789 Cr a year ago', 'type', 26, GREY), 540, 615)
    tp = at(i, 'profit barely', -0.3)
    if t > tp:
        p = eback(prog(t, tp, 0.4), 1.3); place(c, card_box(920, 380, SOFT), 540, 900, p, 0.5)
        if p > 0.6:
            place(c, text_img('NET PROFIT · vs last quarter', 'osw5', 42, GREY), 540, 760)
            place(c, text_img('₹102 CR', 'anton', 96, GREY), 300, 880)
            marker_line(c, [(470, 880), (590, 880)], clamp((t - tp - 0.4) / 0.4), GREY, 10, head=True, head_size=28)
            v = SS.roll_number(t, tp + 0.6, 1.0, 102, 104)
            place(c, text_img(f'₹{v:.0f} CR', 'anton', 96, INK), 790, 880)
            if t > tp + 1.4:
                place(c, text_img('only ~2% more', 'mark', 52, RED), 540, 1010, 1, -2)
    tx = at(i, 'missed expectations', -0.4)
    if t > tx:
        s_, a = slam(t, tx); place(c, stamp_c('REVENUE MISSED', RED, 100, -6, 961), 540, 1210, s_, 0, a)
        if t - tx < 0.25: c.alpha_composite(Image.new('RGBA', c.size, (226, 58, 44, int(80 * (1 - (t - tx) / 0.25)))))
    if t > tx + 0.7:
        place(c, label('NOW -59% FROM 52W HIGH ₹1,245', RED), 540, 1380, 1.0 * eback(prog(t, tx + 0.7, 0.35), 1.6), 2)
    src_line(c, t, T0 + 0.5, 'Sources: company results 30 Oct 2026 (Free Press Journal, INDmoney news)', 1550)


def s7(c, t):  # second tension: risk next to the upside
    i = 6; T0 = STARTS[6] + 0.05
    place_text(c, 'RECORD HIGH', 'anton', 120, INK, 540, 280, t, 'r7', T0, 'pop')
    place_text(c, '= RISK TOO', 'anton', 100, RED, 540, 400, t, 'r7b', T0 + 0.3, 'pop')
    tl = at(i, 'Laurus is up', -0.3)
    if t > tl:
        p = eback(prog(t, tl, 0.4), 1.3); place(c, card_box(920, 480, SOFT), 540, 760, p, -0.5)
        if p > 0.6:
            c.alpha_composite(text_img('LAURUS · 12 MONTHS', 'osw5', 40, GREY), (130, 545))
            q = tip_chart(c, t, tl + 0.3, 'LAURUS', LCOL, 140, 900, 640, 920, 1.6, tag='₹2,406')
            if q >= 1: place(c, text_img('₹982', 'anton', 44, GREY), 200, 850)
    t25 = at(i, 'two and a half', -0.3)
    if t > t25:
        s_, a = slam(t, t25); place(c, stamp_c('~2.5x IN A YEAR', GRN, 90, -5, 971), 540, 1135, s_, 0, a)
    tk = at(i, 'Kotak', -0.3)
    if t > tk:
        s_, a = slam(t, tk); place(c, stamp_c('KOTAK: SELL RATING', RED, 84, 4, 972), 540, 1290, s_, 0, a)
    th = at(i, 'High expectations', -0.3)
    if t > th:
        place_text(c, 'high expectations are easy to disappoint', 'mark', 50, NAVY, 540, 1440, t, 'he', th, 'slide', rot=-2)
    src_line(c, t, T0 + 0.5, 'Weekly closes to 30 Oct 2026, NSE via INDmoney', 1560)
    src_line(c, t, T0 + 0.5, 'Kotak rating: INDmoney news, 28 Oct 2026', 1600)


def s8(c, t):  # ANSWER + cheat sheet
    i = 7; T0 = STARTS[7] + 0.05
    place_text(c, 'THE RULE', 'anton', 110, INK, 540, 270, t, 'ru', T0, 'pop')
    ts = at(i, 'surprise', -0.3)
    if t > ts:
        s_, a = slam(t, ts); place(c, stamp_c('STOCKS MOVE ON SURPRISE', NAVY, 74, -3, 981), 540, 410, s_, 0, a)
    tc = at(i, 'Check three', -0.3)
    SS.cheat_sheet(c, t, tc, 'RESULTS DAY CHEAT SHEET', [
        ('1  PROFIT GROWTH', 'vs sales?', GRN),
        ('2  MARGINS', 'up or down?', ORG),
        ('3  EXPECTATIONS', 'beat or miss?', RED),
        ('LAURUS', 'PROFIT SURGED  +7%', GRN),
        ('INTELLECT', 'PROFIT FLAT  -16%', RED)], y0=520)
    src_line(c, t, tc + 1.0, 'Stock moves: NSE close 30 Oct 2026 via INDmoney · results: company filings 29-30 Oct 2026', 1560)


def s9(c, t):  # CTA + loop (dark)
    i = 8; T0 = STARTS[8] + 0.05
    SS.send_frame(c, t, at(i, 'Send this', -0.3), 'your sales-only friend', y=430)
    tsv = at(i, 'Save this', -0.3)
    if t > tsv:
        p = eback(prog(t, tsv, 0.4), 1.8); bob = math.sin((t - tsv) * 7) * 8 * math.exp(-(t - tsv) * 0.8)
        place(c, SS.bookmark_icon(100), 360, 700 + bob, p, -8); place(c, text_img('SAVE THIS', 'anton', 84, CREAM), 600, 700, p)
    tfo = at(i, 'follow', -0.2)
    if t > tfo:
        pp = prog(t, tfo, 0.35); place(c, follow_btn(), 540, 870, 0.5 + 0.5 * eback(pp), 0, clamp(pp * 3))
    for k, ln in enumerate(['Prices & charts: NSE via INDmoney, weekly closes to 30 Oct 2026.',
                            'Results: company filings & news reports, 29-30 Oct 2026.',
                            'No buy/sell recommendation. I may hold some of these stocks.',
                            'Education only. Not investment advice.']):
        place_text(c, ln, 'type', 25, (210, 204, 192), 540, 1020 + k * 40, t, None, T0 + 0.3, 'fade', track=1)
    te = at(i, 'Sales grew', -0.2)
    if t > te:
        place(c, label('SALES GREW.', GRN), 540, 1300, 1.3 * eback(prog(t, te, 0.35), 1.6), -3)
        tq = at(i, 'why the crash', -0.2)
        if t > tq: place(c, label('SO WHY THE CRASH?', RED), 540, 1420, 1.3 * eback(prog(t, tq, 0.35), 1.6), 3)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]


def SLAMS():
    return [1.1, at(0, "You're reading", -0.25), at(5, 'missed expectations', -0.4), at(6, 'two and a half', -0.3),
            at(6, 'Kotak', -0.3), at(7, 'surprise', -0.3)] + [STARTS[k] + 0.05 for k in range(1, 8)]


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
    b = text_img('RESULTS DAY CHECK', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
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
    if not loop and (CAPS_ON or CAP == 'ta'): captions(c, t)
    header(c, dark, t if not loop else 0); transition(c, t)
    arr = np.asarray(c.convert('RGB')).astype(np.float32)
    g = grain_frames()[int(t * FPS) % 6]
    fl = 1 + 0.012 * math.sin(t * 37) * math.sin(t * 13)
    return np.clip(arr * fl + g[..., None], 0, 255).astype(np.uint8)
