"""bestdays — 5 days decided the Nifty year: missing the best days (4 Nov 2026)"""
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
SH = ROOT + '' + os.environ.get('LDIR', 'bestdays') + '/'
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


def spark(c, pts, p, col, w=12):
    n = len(pts) - 1; f = p * n; k = int(f); out = pts[:k + 1]
    if k < n: a, b = pts[k], pts[k + 1]; fr = f - k; out = out + [(a[0] + (b[0] - a[0]) * fr, a[1] + (b[1] - a[1]) * fr)]
    if len(out) >= 2: stroke(c, out, w, col)




CLOSES = json.load(open(SH + 'closes.json'))
TA = SCRIPT  # captions are OFF; Tamil track not used
LCOL, ICOL = GRN, RED


def rs(v):
    return inr(v) if v >= 1000 else '₹' + (f'{v:.0f}' if v >= 100 else f'{v:.2f}')


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


# ---------- data ----------
DATES = CLOSES['dates']; NC = CLOSES['closes']; VAL = CLOSES['v']; MIS = CLOSES['m']
BEST5 = CLOSES['best5']; WORST10 = CLOSES['worst10']
MON = ['', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
def dlab(i):
    y, m, d = DATES[i].split('-'); return f'{int(d)} {MON[int(m)]}'
def pct(i): return (NC[i] / NC[i - 1] - 1) * 100


def series_pts(v, x0, x1, yt, yb, lo=None, hi=None):
    lo = min(v) if lo is None else lo; hi = max(v) if hi is None else hi
    return [(x0 + (x1 - x0) * k / (len(v) - 1), yt + (yb - yt) * (hi - p) / (hi - lo)) for k, p in enumerate(v)]


def grid(c, x0, x1, yt, yb):
    d = ImageDraw.Draw(c)
    for gy in (yt, (yt + yb) / 2, yb): d.line((x0, gy, x1, gy), fill=(225, 220, 210), width=2)


def tip(c, pts, v, p, col, fmt, t, lab_dy=-50):
    d = ImageDraw.Draw(c)
    f = p * (len(pts) - 1); k = min(int(f), len(pts) - 2); fr = f - k
    tx = pts[k][0] + (pts[k + 1][0] - pts[k][0]) * fr; ty = pts[k][1] + (pts[k + 1][1] - pts[k][1]) * fr
    val = v[k] + (v[k + 1] - v[k]) * fr
    r = 10 if p < 1 else 14 + 2 * math.sin(t * 8)
    d.ellipse((tx - r, ty - r, tx + r, ty + r), fill=col, outline=INK, width=3)
    return tx, ty, val


# ---------- scenes ----------
def s1(c, t):  # HOOK: big moving 5 DAYS on frame 0
    i = 0
    place_text(c, 'NOBODY TELLS YOU THIS', 'osw5', 54, INK, 540, 250, t, 'nt', 0.0, 'slide')
    n = min(5, 1 + int(eo(prog(t, -0.2, 1.0)) * 4.999))
    shake = math.sin(t * 50) * 10 * math.exp(-max(0, t - 1.0) * 5) if t > 1.0 else 0
    big = text_img(f'{n}', 'anton', 420, RED)
    place(c, big, 330 + shake, 560, 1.0 + 0.05 * math.sin(t * 3), -3)
    place(c, text_img('DAYS', 'anton', 210, INK), 720, 600, 1.0 + 0.03 * math.sin(t * 3 + 1), 2)
    # flipping calendar tiles under the number
    for k in range(5):
        tk = 0.05 + k * 0.16
        if t > tk:
            p = eback(prog(t, tk, 0.3), 1.6); bob = math.sin(t * 5 + k) * 6
            x = 170 + k * 185
            tile = card_box(150, 150, SOFT); dd = ImageDraw.Draw(tile)
            dd.rectangle((8, 8, 142, 44), fill=GRN)
            tile.alpha_composite(text_img(dlab(BEST5[k]).split()[1], 'osw5', 26, CREAM), (48, 8))
            tile.alpha_composite(text_img(dlab(BEST5[k]).split()[0], 'anton', 64, INK), (52 if len(dlab(BEST5[k]).split()[0]) == 1 else 38, 54))
            place(c, tile, x, 880 + bob, p, (-5, 3, -2, 4, -4)[k])
    tw = at(i, 'decided', -0.25)
    if t > tw:
        s_, a = slam(t, tw); place(c, stamp_c('DECIDED THE', RED, 100, -4, 101), 540, 1110, s_, 0, a)
    if t > tw + 0.25:
        s_, a = slam(t, tw + 0.25); place(c, stamp_c('WHOLE YEAR', RED, 120, 3, 102), 540, 1260, s_, 0, a)
    if t > tw + 0.6:
        bob = math.sin(t * 6) * 10; place(c, text_img('?', 'anton', 170, NAVY), 960, 1180 + bob, 1, 10)
    src_line(c, t, 1.2, 'NIFTY 50 daily closes, 4 Nov 2025 - 3 Nov 2026 · NSE via INDmoney', 1500)


def s2(c, t):  # 1 lakh in the Nifty, real chart with value counter
    i = 1; T0 = STARTS[1] + 0.05
    place_text(c, '₹1 LAKH IN NIFTY 50', 'anton', 104, INK, 540, 270, t, 'l2', T0, 'pop')
    place_text(c, 'invested 4 Nov 2025 · price index', 'osw5', 40, GREY, 540, 370, t, 'l2s', T0 + 0.2, 'slide')
    tc = at(i, 'Today', -1.6)
    tc = min(tc, T0 + 1.0)
    if t > T0 + 0.3:
        p = eback(prog(t, T0 + 0.3, 0.4), 1.3); place(c, card_box(960, 640, SOFT), 540, 790, p, -0.4)
        if p > 0.6:
            x0, x1, yt, yb = 120, 920, 560, 1010; grid(c, x0, x1, yt, yb)
            pts = series_pts(VAL, x0, x1, yt, yb, 82000, 104000)
            q = eio(prog(t, tc, 3.2)); spark(c, pts, q, NAVY, 8)
            tx, ty, val = tip(c, pts, VAL, max(q, 0.001), NAVY, inr, t)
            for xx, txt in ((x0, 'NOV 25'), ((x0 + x1) / 2, 'MAY 26'), (x1, 'NOV 26')):
                place(c, text_img(txt, 'type', 26, GREY), xx, 1050)
            place(c, text_img(inr(val), 'anton', 120, INK if q < 1 else RED), 540, 1230, 1.0 + 0.03 * math.sin(t * 5))
    td = at(i, 'Down seven', -0.3)
    if t > td:
        s_, a = slam(t, td); place(c, stamp_c('-7% IN A YEAR', RED, 96, -5, 201), 540, 1390, s_, 0, a)
    src_line(c, t, T0 + 0.5, 'NIFTY 50: 25,598 (4 Nov 2025) -> 23,811 (3 Nov 2026) · INDmoney', 1560)
    src_line(c, t, T0 + 0.5, 'Price index only, excludes dividends. Past data.', 1600)


def day_grid(c, t, t0, x0=105, y0=420, cols=18, cell=48, highlight=None, removed=0.0):
    """246 trading days as small squares; best-5 glow green, then get crossed out."""
    if t < t0: return
    n = 246; d = ImageDraw.Draw(c)
    shown = int(n * eo(prog(t, t0, 1.2)))
    for k in range(shown):
        idx = k + 1; r_, cc = divmod(k, cols)
        x = x0 + cc * cell; y = y0 + r_ * cell
        isb = idx in BEST5 and highlight is not None and t > highlight
        fill = GRN if isb else ((235, 228, 214) if pct(idx) >= 0 else (222, 210, 196))
        if isb:
            g = 1 + 0.25 * math.sin(t * 9)
            d.rounded_rectangle((x - 6 * g, y - 6 * g, x + cell - 4 + 6 * g, y + cell - 4 + 6 * g), 8, fill=YEL)
        d.rounded_rectangle((x, y, x + cell - 6, y + cell - 6), 6, fill=fill, outline=(150, 140, 125), width=2)
        if isb and removed > 0:
            q = clamp(removed)
            d.line((x - 4, y - 4, x - 4 + (cell + 2) * q, y - 4 + (cell + 2) * q), fill=RED, width=8)
            d.line((x + cell + 2, y - 4, x + cell + 2 - (cell + 6) * q, y - 4 + (cell + 2) * q), fill=RED, width=8)


def s3(c, t):  # stayed out on the 5 best days: grid + question + countdown
    i = 2; T0 = STARTS[2] + 0.05
    place_text(c, 'SCARED OUT ON 5 DAYS', 'anton', 92, INK, 540, 260, t, 'l3', T0, 'pop')
    place_text(c, '5 best days out of 246 trading days', 'osw5', 40, GREY, 540, 355, t, 'l3s', T0 + 0.3, 'slide')
    tb = at(i, 'five best', -0.3); tr = at(i, 'Five, out', 0.0)
    day_grid(c, t, T0 + 0.2, highlight=tb, removed=prog(t, tr, 0.6))
    tq = at(i, 'How much', -0.3)
    if t > tq:
        place(c, label('HOW MUCH IS LEFT?', RED), 540, 1250, 1.3 * eback(prog(t, tq, 0.35), 1.6), -3)
        SS.countdown_ring(c, t, tq + 0.2, 3, 540, 1440, 100)
    src_line(c, t, T0 + 0.5, 'Green = the 5 biggest one-day gains, NIFTY 50, Nov 2025 - Nov 2026', 1600)


def s4(c, t):  # REHOOK: tear reveal + compare bars
    i = 3; T0 = STARTS[3] + 0.05
    if t - T0 < 0.25: c.alpha_composite(Image.new('RGBA', c.size, (240, 196, 40, int(110 * (1 - clamp((t - T0) / 0.25))))))
    place_text(c, 'MISSED 5 BEST DAYS', 'anton', 90, INK, 540, 260, t, 'l4', T0, 'pop')
    big = card_box(820, 260, SOFT); place(big, text_img('₹82,781', 'anton', 170, RED), 405, 125)
    SS.tear_reveal(c, t, T0 + 0.1, big, 540, 500)
    tl = at(i, 'A seven', -0.3)
    if t > tl:
        p = eback(prog(t, tl, 0.4), 1.3); place(c, card_box(920, 330, SOFT), 540, 840, p, 0.4)
        if p > 0.6:
            d = ImageDraw.Draw(c)
            for k, (nm, v, col, pc) in enumerate((('STAYED IN', 93020, NAVY, '-7%'), ('MISSED 5', 82781, RED, '-17%'))):
                y = 770 + k * 130; ph = eo(prog(t, tl + 0.2 + 0.4 * k, 0.8))
                w = int(520 * (v - 60000) / 40000 * ph)
                place(c, text_img(nm, 'osw5', 42, INK), 220, y)
                d.rounded_rectangle((350, y - 34, 350 + max(w, 12), y + 34), 12, fill=col, outline=INK, width=4)
                c.alpha_composite(text_img(pc, 'anton', 60, col), (350 + max(w, 12) + 16, int(y - 38)))
    tb = at(i, 'But here', -0.3)
    if t > tb:
        if t - tb < 0.25: c.alpha_composite(Image.new('RGBA', c.size, (230, 90, 140, int(70 * (1 - (t - tb) / 0.25)))))
        s_, a = slam(t, tb); place(c, stamp_c('BUT WAIT...', NAVY, 120, -4, 401), 540, 1160, s_, 0, a)
        place_text(c, 'the strange part nobody tells you', 'mark', 56, PINK, 540, 1330, t, 'sp', tb + 0.4, 'slide', rot=-2)
    src_line(c, t, T0 + 0.5, '₹1 lakh, NIFTY 50 price index, 4 Nov 2025 - 3 Nov 2026 · NSE via INDmoney', 1600)


def s5(c, t):  # quiz with countdown
    i = 4; T0 = STARTS[4] + 0.05
    place_text(c, 'QUIZ', 'anton', 80, RED, 540, 240, t, 'qz', T0, 'pop')
    place_text(c, 'WHEN DID THE BEST', 'anton', 96, INK, 540, 350, t, 'q5a', T0 + 0.1, 'pop')
    place_text(c, 'DAY OF THE YEAR COME?', 'anton', 96, INK, 540, 460, t, 'q5b', T0 + 0.2, 'pop')
    for k, (ph, ltr, txt, col, y) in enumerate((('calm', 'A', 'IN A CALM, HAPPY MARKET', GRN, 700), ('right after', 'B', 'RIGHT AFTER A CRASH', RED, 900))):
        tk = at(i, ph, -0.4)
        if t > tk:
            p = eback(prog(t, tk, 0.35), 1.4); bob = math.sin(t * 4 + k) * 5
            place(c, card_box(900, 160, SOFT), 540, y + bob, p, (-1, 1)[k])
            if p > 0.6:
                d = ImageDraw.Draw(c); d.ellipse((120, y - 50 + bob, 220, y + 50 + bob), fill=col, outline=INK, width=4)
                place(c, text_img(ltr, 'anton', 70, CREAM), 170, y + bob)
                c.alpha_composite(text_img(txt, 'anton', 62, INK), (250, int(y - 40 + bob)))
    tcd = at(i, 'Three', -0.2)
    SS.countdown_ring(c, t, tcd, 3, 540, 1250, 120)
    src_line(c, t, T0 + 0.5, 'Answer uses NIFTY 50 daily closes, Nov 2025 - Nov 2026', 1600)


def s6(c, t):  # answer: right after the crash, zoomed real chart
    i = 5; T0 = STARTS[5] + 0.05
    s_, a = slam(t, T0); place(c, stamp_c('B · RIGHT AFTER A CRASH', RED, 78, -3, 601), 540, 260, s_, 0, a)
    a0, a1 = DATES.index('2026-03-02'), DATES.index('2026-04-17')
    seg = NC[a0:a1 + 1]
    if t > T0 + 0.3:
        p = eback(prog(t, T0 + 0.3, 0.4), 1.3); place(c, card_box(960, 760, SOFT), 540, 800, p, 0.4)
        if p > 0.6:
            c.alpha_composite(text_img('NIFTY 50 · 2 MAR - 17 APR 2026', 'osw5', 38, GREY), (100, 450))
            x0, x1, yt, yb = 120, 940, 560, 1080; grid(c, x0, x1, yt, yb)
            pts = series_pts(seg, x0, x1, yt, yb, 22000, 25100)
            q = eio(prog(t, T0 + 0.6, 2.6)); spark(c, pts, q, NAVY, 8)
            tx, ty, val = tip(c, pts, seg, max(q, 0.001), NAVY, None, t)
            if q < 1: place(c, text_img(f'{val:,.0f}', 'anton', 44, INK), min(max(tx, 200), 860), ty - 46)
            kc = DATES.index('2026-03-30') - a0; kb = DATES.index('2026-04-08') - a0
            fq = q * (len(pts) - 1)
            if fq >= kc:
                place(c, label(f'30 MAR  {pct(a0 + kc):.1f}%', RED), pts[kc][0] - 120, pts[kc][1] + 70, 0.9, -3)
            if fq >= kb:
                g = 1 + 0.06 * math.sin(t * 7)
                place(c, label(f'8 APR  +{pct(a0 + kb):.1f}%', GRN), pts[kb][0] - 60, pts[kb][1] - 80, 0.95 * g, 3)
    tj = at(i, 'almost four', -0.3)
    if t > tj:
        v = SS.roll_number(t, tj, 0.8, 0, pct(DATES.index('2026-04-08')))
        place(c, text_img(f'+{v:.1f}%', 'anton', 150, GRN), 540, 1300, 1.0 + 0.04 * math.sin(t * 5))
        place(c, text_img('best day of the year · 8 April 2026', 'osw5', 42, INK), 540, 1410)
    src_line(c, t, T0 + 0.5, 'NIFTY 50 daily closes · NSE via INDmoney', 1600)


def s7(c, t):  # timeline: best days sit next to worst days
    i = 6; T0 = STARTS[6] + 0.05
    place_text(c, 'NOT A ONE-OFF', 'anton', 110, INK, 540, 270, t, 'l7', T0, 'pop')
    x0, x1, ya = 100, 980, 760
    d = ImageDraw.Draw(c)
    if t > T0 + 0.2:
        q = eo(prog(t, T0 + 0.2, 0.6)); d.line((x0, ya, x0 + (x1 - x0) * q, ya), fill=INK, width=6)
        for xx, txt in ((x0, 'NOV 25'), ((x0 + x1) / 2, 'MAY 26'), (x1, 'NOV 26')):
            place(c, text_img(txt, 'type', 26, GREY), xx, ya + 210)
    X = lambda k: x0 + (x1 - x0) * k / 246
    tw = at(i, 'ten worst', -1.2)
    for n, k in enumerate(WORST10):
        tk = tw + 0.06 * n
        if t > tk:
            h = 150 * eback(prog(t, tk, 0.3), 1.5); d.rounded_rectangle((X(k) - 7, ya, X(k) + 7, ya + h), 4, fill=RED)
    tb = at(i, 'Four of', -0.3)
    for n, k in enumerate(BEST5):
        tk = tb + 0.1 * n
        if t > tk:
            h = 170 * eback(prog(t, tk, 0.3), 1.5); d.rounded_rectangle((X(k) - 8, ya - h, X(k) + 8, ya), 4, fill=GRN)
    place(c, text_img('GREEN = 5 BEST DAYS', 'osw5', 38, GRN), 770, 570) if t > tb else None
    place(c, text_img('RED = 10 WORST DAYS', 'osw5', 38, RED), 700, 1030) if t > tw else None
    th = at(i, 'within two', -0.3)
    if t > th:  # highlight the cluster around Feb-Apr
        q = eo(prog(t, th, 0.5)); xa, xb = X(58) - 20, X(106) + 20
        d.rounded_rectangle((xa, ya - 210, xa + (xb - xa) * q, ya + 180), 20, outline=ORG, width=8)
        v = int(SS.roll_number(t, th + 0.2, 0.8, 0, 4))
        place(c, text_img(f'{v} OF 5', 'anton', 140, ORG), 540, 1150, 1.0 + 0.04 * math.sin(t * 5))
        place(c, text_img('best days came within 2 weeks of a worst day', 'osw5', 40, INK), 540, 1260)
    tf = at(i, 'fear is highest', -0.6)
    if t > tf:
        place_text(c, 'the bounce comes when fear is highest', 'mark', 52, NAVY, 540, 1400, t, 'fh', tf, 'slide', rot=-2)
    src_line(c, t, T0 + 0.5, 'Biggest one-day % moves, NIFTY 50, 4 Nov 2025 - 3 Nov 2026 · NSE via INDmoney', 1600)


def s8(c, t):  # ANSWER + cheat sheet
    i = 7; T0 = STARTS[7] + 0.05
    place_text(c, 'THE LESSON', 'anton', 110, INK, 540, 260, t, 'ru', T0, 'pop')
    ts = at(i, "You can't", -0.3)
    if t > ts:
        s_, a = slam(t, ts); place(c, stamp_c("CAN'T SKIP THE WORST WITHOUT THE BEST", NAVY, 50, -2, 801), 540, 390, s_, 0, a)
    tc = at(i, 'without missing', -0.3)
    SS.cheat_sheet(c, t, tc, '₹1 LAKH · NIFTY 50 · 1 YEAR', [
        ('STAYED INVESTED', '₹93,020', NAVY),
        ('MISSED 5 BEST DAYS', '₹82,781', RED),
        ('MISSED 10 BEST DAYS', '₹76,334', RED),
        ('BEST DAYS ARRIVE', 'NEAR THE WORST', ORG),
        ('5 MISSED DAYS COST', '₹10,239', RED)], y0=480)
    tp = at(i, 'Past data', -0.3)
    if t > tp:
        s_, a = slam(t, tp); place(c, stamp_c('PAST DATA · NOT A PROMISE', GREY, 56, 3, 802), 540, 1470, s_, 0, a)
    src_line(c, t, tc + 1.0, 'NIFTY 50 price index, 4 Nov 2025 - 3 Nov 2026, NSE via INDmoney · excludes dividends & costs', 1600)


def s9(c, t):  # CTA + loop (dark)
    i = 8; T0 = STARTS[8] + 0.05
    SS.send_frame(c, t, at(i, 'Send this', -0.3), 'the friend who sells every fall', y=430)
    tsv = at(i, 'Save this', -0.3)
    if t > tsv:
        p = eback(prog(t, tsv, 0.4), 1.8); bob = math.sin((t - tsv) * 7) * 8 * math.exp(-(t - tsv) * 0.8)
        place(c, SS.bookmark_icon(100), 360, 700 + bob, p, -8); place(c, text_img('SAVE THIS', 'anton', 84, CREAM), 600, 700, p)
    tfo = at(i, 'follow', -0.2)
    if t > tfo:
        pp = prog(t, tfo, 0.35); place(c, follow_btn(), 540, 870, 0.5 + 0.5 * eback(pp), 0, clamp(pp * 3))
    for k, ln in enumerate(['NIFTY 50 daily closes: NSE via INDmoney, 4 Nov 2025 - 3 Nov 2026.',
                            'Price index, excludes dividends, taxes and costs. Past data.',
                            'Past performance does not guarantee future returns.',
                            'Education only. Not investment advice.']):
        place_text(c, ln, 'type', 25, (210, 204, 192), 540, 1020 + k * 40, t, None, T0 + 0.3, 'fade', track=1)
    te = at(i, 'Five days', -0.2)
    if t > te:
        place(c, label('5 DAYS.', RED), 540, 1300, 1.3 * eback(prog(t, te, 0.35), 1.6), -3)
        tq = at(i, "That's all", -0.2)
        if t > tq: place(c, label("THAT'S ALL IT TOOK.", YEL), 540, 1420, 1.3 * eback(prog(t, tq, 0.35), 1.6), 3)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]


def SLAMS():
    return [1.0, at(0, 'decided', -0.25), at(1, 'Down seven', -0.3), at(3, 'But here', -0.3), STARTS[5] + 0.05,
            at(7, "You can't", -0.3), at(7, 'Past data', -0.3)] + [STARTS[k] + 0.05 for k in range(1, 8)]


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
    b = text_img('PAST MATHS · NIFTY 50', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
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
