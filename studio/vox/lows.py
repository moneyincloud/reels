"""VIRAL 3X STOCKS — fact check (paper Vox, Heart voice)"""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs
from fridge import follow_btn
import tea as TEA

SH = ROOT + 'lows/'
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



STK = {
    'HUL': ('HINDUSTAN UNILEVER', 'FMCG · ₹4.26 LAKH CR', 2667.2, 1814.7, '-32%', BLUE),
    'MARUTI': ('MARUTI SUZUKI', 'AUTO · ₹3.53 LAKH CR', 17370, 11230, '-35%', NAVY),
    'DMART': ('DMART', 'RETAIL · ₹2.06 LAKH CR', 4644, 3157.7, '-32%', GRN),
    'SWIGGY': ('SWIGGY', 'FOOD + QUICK COMMERCE', 434, 176, '-59%', ORG),
    'NTPC': ('NTPC', 'POWER · ₹2.89 LAKH CR', 414.4, 298, '-28%', TEAL),
}


def rs(v):
    return inr(v) if v >= 1000 else '₹' + (f'{v:.0f}' if v >= 100 else f'{v:.2f}')


def low_card(c, t, i, key, t_pct, reasons):
    nm, sub, hi, lo, pct, col = STK[key]
    T0 = STARTS[i] + 0.05
    place_text(c, nm, 'anton', 104 if len(nm) < 14 else 88, INK, 540, 290, t, f'n{i}', T0, 'pop')
    place_text(c, sub, 'osw5', 44, col, 540, 395, t, f's{i}', T0 + 0.2, 'slide')
    if t > T0 + 0.35:
        p = eback(prog(t, T0 + 0.35, 0.4), 1.3); place(c, card_box(900, 560, SOFT), 540, 770, p, -0.6)
    if t > T0 + 0.7:
        x0, x1, yt, yb = 170, 910, 610, 900
        pts = [(x0, yt + 30), (x0 + 110, yt), (x0 + 210, yt + 70), (x0 + 330, yt + 50), (x0 + 440, yt + 150), (x0 + 560, yt + 130), (x0 + 660, yt + 230), (x1, yb - 20)]
        p = eio(prog(t, T0 + 0.7, 1.3)); spark(c, pts, p, RED, 12)
        place(c, text_img('52W HIGH ' + rs(hi), 'osw5', 40, GREY), 360, 570)
        if p >= 1:
            place(c, text_img('NOW ' + rs(lo), 'anton', 66, RED), 700, 960)
            d = ImageDraw.Draw(c); d.ellipse((x1 - 14, yb - 34, x1 + 14, yb - 6), fill=RED, outline=INK, width=3)
    if t > t_pct:
        s_, a = slam(t, t_pct); place(c, stamp_c(pct, RED, 170, -7, 800 + i), 540, 1170, s_, 0, a)
        if t - t_pct < 0.25: c.alpha_composite(Image.new('RGBA', c.size, (226, 58, 44, int(80 * (1 - (t - t_pct) / 0.25)))))
    for k, (txt, ph, cl) in enumerate(reasons):
        tk = at(i, ph, -0.3)
        if t > tk: place(c, label(txt, cl), 540, 1380 + k * 140, 1.2 * eback(prog(t, tk, 0.35), 1.6), (-2, 2, -1)[k % 3])


def s1(c, t):
    i = 0
    words_line(c, t, [("52-WEEK", INK, 0.05), ("LOWS", RED, 0.25)], 'anton', 170, 300, key='h')
    tb = at(i, 'biggest brands', -0.2)
    for k, nm in enumerate(['HUL', 'MARUTI', 'DMART', 'SWIGGY', 'NTPC']):
        tk = tb + 0.12 * k
        if t > tk:
            x = (240, 540, 840, 380, 700)[k]; y = (560, 560, 560, 720, 720)[k]
            dy = 0 if t < at(i, 'fifty two', 0) else 40 * eio(prog(t, at(i, 'fifty two', 0) + k * 0.06, 0.6))
            place(c, label(nm, (BLUE, NAVY, GRN, ORG, TEAL)[k]), x, y + dy, 1.2 * eback(prog(t, tk, 0.3), 1.6), (-4, 3, -2, 4, -3)[k])
            if dy > 5: ImageDraw.Draw(c).polygon([(x - 22, y + dy + 55), (x + 22, y + dy + 55), (x, y + dy + 85)], fill=RED)
    tq = at(i, 'bargain', -0.3)
    if t > tq: place(c, label('BARGAIN?', GRN), 300, 1060, 1.4 * eback(prog(t, tq, 0.35), 1.6), -5)
    tw = at(i, 'warning', -0.3)
    if t > tw:
        sh = math.sin(t * 40) * 6 * math.exp(-(t - tw) * 3)
        place(c, label('WARNING?', RED), 780 + sh, 1060, 1.4 * eback(prog(t, tw, 0.35), 1.6), 5)
    tc = at(i, 'why they fell', -0.3)
    if t > tc: place_text(c, "let's check why they fell", 'mark', 66, NAVY, 540, 1300, t, 'wf', tc, 'slide', rot=-2)
    if t > tc + 0.3: place_text(c, 'prices: NSE close, 23 Oct 2026', 'type', 30, GREY, 540, 1420, t, None, tc + 0.3, 'fade', track=1)


def s2(c, t):
    i = 1
    place_text(c, 'THE MARKET', 'anton', 130, INK, 540, 300, t, 'm', STARTS[1] + 0.05, 'pop')
    tn = at(i, 'Nifty', -0.3)
    if t > tn:
        p = eback(prog(t, tn, 0.4), 1.3); place(c, card_box(880, 380, SOFT), 540, 640, p, -1)
        if p > 0.6:
            place(c, text_img('NIFTY 50', 'osw5', 50, GREY), 540, 530)
            place(c, text_img('HIGH 26,373', 'anton', 70, GREY), 540, 620)
            place(c, text_img('NOW 22,600', 'anton', 90, RED), 540, 730)
    tf = at(i, 'fourteen percent', -0.3)
    if t > tf: place(c, label('-14% FROM HIGH', RED), 540, 900, 1.3 * eback(prog(t, tf, 0.35), 1.6), 2)
    tg = at(i, 'giants', -0.3)
    if t > tg:
        ph = eo(prog(t, tg, 0.9))
        bars = [('NIFTY', 14, GREY), ('NTPC', 28, TEAL), ('HUL', 32, BLUE), ('DMART', 32, GRN), ('MARUTI', 35, NAVY), ('SWIGGY', 59, ORG)]
        d = ImageDraw.Draw(c)
        for k, (nm, v, cl) in enumerate(bars):
            y = 1060 + k * 105; w = int(9 * v * ph)
            place(c, text_img(nm, 'osw5', 40, INK), 170, y)
            d.rounded_rectangle((300, y - 30, 300 + w, y + 30), 10, fill=cl, outline=INK, width=3)
            if ph > 0.8: c.alpha_composite(text_img(f'-{v}%', 'anton', 50, RED), (320 + w, y - 32))
    th = at(i, 'much harder', -0.3)
    if t > th: place_text(c, 'fall from 52-week high', 'type', 30, GREY, 540, 1720, t, None, th, 'fade', track=1)


def s3(c, t): low_card(c, t, 2, 'HUL', at(2, 'thirty two', -0.3), [('PROFIT SLIPPED', 'Profits slipped', RED), ('INPUT COSTS UP', 'input costs', ORG), ('DETERGENT PRICES RAISED', 'detergent', NAVY)])
def s4(c, t): low_card(c, t, 3, 'MARUTI', at(3, 'thirty five', -0.3), [('SEPT SALES UP', 'September sales', GRN), ('MARGINS IN FOCUS', 'margins', ORG), ('Q2 RESULTS: 27 OCT', 'October twenty', NAVY)])
def s5(c, t): low_card(c, t, 4, 'DMART', at(4, 'thirty two', -0.3), [('REVENUE +18%', 'eighteen percent', GRN), ('MARGINS NARROWED', 'margins narrowed', RED), ('TARGETS CUT', 'brokerages', ORG)])
def s6(c, t): low_card(c, t, 5, 'SWIGGY', at(5, 'fifty nine', -0.3), [('-17% IN ONE DAY', 'seventeen percent', RED), ('INSTAMART LOSSES WIDER', 'Instamart', ORG)])
def s7(c, t): low_card(c, t, 6, 'NTPC', at(6, 'twenty eight', -0.3), [('NUCLEAR + GREEN PLANS', 'nuclear', GRN), ('COAL SUPPLY WORRIES', 'coal supply', ORG), ('BIG SPENDING AHEAD', 'big spending', NAVY)])


def s8(c, t):
    i = 7
    place_text(c, '52-WEEK LOW', 'anton', 120, INK, 540, 290, t, 'q', STARTS[7] + 0.05, 'pop')
    td = at(i, 'discount sticker', -0.4)
    if t > td:
        p = eback(prog(t, td, 0.4), 1.5)
        place(c, stamp_c('SALE 30% OFF', ORG, 110, -8, 977), 540, 520, p, 0, 1)
        tx = td + 0.6
        if t > tx:
            q = eo(prog(t, tx, 0.3)); d = ImageDraw.Draw(c)
            d.line((180, 420, 180 + 720 * q, 420 + 200 * q), fill=RED, width=22)
            d.line((900, 420, 900 - 720 * q, 420 + 200 * q), fill=RED, width=22)
            place_text(c, 'not a discount sticker', 'mark', 62, RED, 540, 700, t, 'nd', tx, 'slide', rot=-2)
    tq = at(i, 'three questions', -0.3)
    if t > tq: place_text(c, 'ASK 3 QUESTIONS', 'anton', 90, NAVY, 540, 860, t, 'aq', tq, 'pop')
    for k, (txt, ph) in enumerate([('1  WHY DID IT FALL?', 'Why did'), ('2  ARE PROFITS GROWING?', 'Are profits'), ('3  IS DEBT UNDER CONTROL?', 'debt')]):
        tk = at(i, ph, -0.3)
        if t > tk:
            p = eback(prog(t, tk, 0.4), 1.3); y = 1040 + k * 190
            place(c, card_box(860, 150, SOFT), 540, y, p, (-1, 1, -0.5)[k])
            if p > 0.6:
                place(c, text_img(txt, 'anton', 62, INK), 520, y)
                d = ImageDraw.Draw(c); d.rounded_rectangle((860, y - 30, 920, y + 30), 8, outline=GRN, width=6)
                if t > tk + 0.5: d.line((872, y, 886, y + 18, 912, y - 22), fill=GRN, width=8)


def s9(c, t):
    i = 8
    place_text(c, 'CHEAP CAN GET', 'anton', 120, CREAM, 540, 300, t, 'c1', STARTS[8] + 0.05, 'pop')
    place_text(c, 'CHEAPER', 'anton', 150, YEL, 540, 440, t, 'c2', STARTS[8] + 0.2, 'pop')
    ts = at(i, 'Save this', -0.3)
    if t > ts: place_text(c, 'save this before you buy any dip', 'mark', 56, CREAM, 540, 600, t, 'sv', ts, 'slide', rot=-2)
    tfo = at(i, 'follow', -0.2)
    if t > tfo:
        pp = prog(t, tfo, 0.35); place(c, follow_btn(), 540, 820, 0.5 + 0.5 * eback(pp), 0, clamp(pp * 3))
    for k, ln in enumerate(['Prices & 52-week range: NSE via INDmoney, close 23 Oct 2026.', 'Reasons: company filings & news reports, Oct 2026.', 'No buy/sell recommendation. I may hold some of these stocks.', 'Education only. Not investment advice.']):
        place_text(c, ln, 'type', 25, (210, 204, 192), 540, 1000 + k * 40, t, None, STARTS[8] + 0.3, 'fade', track=1)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]


def SLAMS():
    return [at(2, 'thirty two', -0.3), at(3, 'thirty five', -0.3), at(4, 'thirty two', -0.3), at(5, 'fifty nine', -0.3), at(6, 'twenty eight', -0.3)] + [STARTS[k] + 0.05 for k in range(1, 8)]


def header(c, dark):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('52-WEEK LOW CHECK', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
    ImageDraw.Draw(c).line((60, 118, W - 60, 118), fill=col, width=2)
    ImageDraw.Draw(c).line((60, 118, 300, 118), fill=col, width=6)


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
    header(c, dark); transition(c, t)
    arr = np.asarray(c.convert('RGB')).astype(np.float32)
    g = grain_frames()[int(t * FPS) % 6]
    fl = 1 + 0.012 * math.sin(t * 37) * math.sin(t * 13)
    return np.clip(arr * fl + g[..., None], 0, 255).astype(np.uint8)
