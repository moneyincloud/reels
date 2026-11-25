"""Big Bull lesson: Rakesh Jhunjhunwala ₹5,000 -> ₹46,000 Cr, Titan, time (collage style, female VO)"""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs, typed, drop, warn_icon, receipt
from fridge import follow_btn
import saveshare as SS
import suzlon as SZ
import tea as TEA

SH = ROOT + 'bigbull/'
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


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def pp(t, t0, d=0.35, s=1.6): return eback(prog(t, t0, d), s)


def src(c, t, txt, t0, y=1720, col=GREY):
    if t > t0: place_text(c, txt, 'type', 24, col, 540, y, t, None, t0, 'fade', track=1)


def bars(c, t, rows, base, maxh, vmax, x0=200, gap=230, w=150, unit='₹', suffix=' CR', neg_base=None):
    d = ImageDraw.Draw(c)
    for k, (lab, v, col, tk) in enumerate(rows):
        if t < tk: continue
        x = x0 + k * gap; q = eo(prog(t, tk, 0.8)); hg = int(abs(v) / vmax * maxh * q)
        if v >= 0:
            d.rounded_rectangle((x - w / 2, base - hg, x + w / 2, base), 12, fill=col, outline=INK, width=5)
            place(c, text_img(f'{unit}{int(v * q):,}{suffix}', 'anton', 46, INK), x, base - hg - 34)
        else:
            d.rounded_rectangle((x - w / 2, base, x + w / 2, base + hg), 12, fill=col, outline=INK, width=5)
            place(c, text_img(f'-{unit}{int(-v * q):,}{suffix}', 'anton', 46, RED), x, base + hg + 34)
        place(c, text_img(lab, 'osw5', 34, GREY), x, base + (40 if v >= 0 else -30))
    d.line((80, base, 1000, base), fill=INK, width=5)


# ---------------- scenes ----------------
def counter(v0, v1, t, t0, d=1.2):
    return v0 + (v1 - v0) * eo(prog(t, t0, d))


def s1(c, t):
    i = 0
    dy, a = drop(t, 0.1, 360)
    if a > 0:
        place(c, SZ.clipping(1.0, 'THE BIG BULL', 'DALAL STREET STORIES', 'RAKESH JHUNJHUNWALA · 1960-2022'), 540, 420 + dy, 0.95, -3, a)
    place(c, text_img('₹5,000', 'anton', 170, INK), 540, 740, pp(t, 0.3))
    tc = at(i, 'forty six', -0.3)
    if t > tc:
        place(c, text_img('↓', 'anton', 90, GREY) if False else text_img('INTO', 'type', 40, GREY, 3), 540, 860, pp(t, tc - 0.1))
        v = counter(5000, 46000, t, tc, 1.0)
        place(c, text_img(f'₹{int(v):,} CR', 'anton', 170, GRN), 540, 990, pp(t, tc))
    tf = at(i, 'fifty five', -0.3)
    if t > tf:
        sc, a2 = slam(t, tf); place(c, stamp_c('MOST CAME AFTER AGE 55', RED, 70, -5, 3), 540, 1220, sc, 0, a2)
    src(c, t, 'Start capital & net worth: Business Standard, Forbes India (2022)', 1.0, 1720)


def s2(c, t):
    i = 1; T0 = STARTS[i]
    place_text(c, '1985', 'anton', 200, INK, 540, 330, t, 'y85', T0 + 0.05, 'pop')
    tn = at(i, 'Rakesh', -0.2)
    if t > tn: place(c, label('RAKESH JHUNJHUNWALA', NAVY), 540, 520, pp(t, tn), -2)
    tca = at(i, 'chartered', -0.2)
    if t > tca: place_text(c, 'young CA, Bombay', 'mark', 50, INK, 540, 620, t, 'ca', tca, 'slide', rot=-2)
    tm = at(i, 'five thousand', -0.3)
    if t > tm:
        for k in range(5):
            tk = tm + 0.1 * k
            if t < tk: continue
            place(c, cutout(Image.new('RGBA', (360, 170), (196, 222, 190, 255)), border=5, shadow=0.35, bcol=GRN), 540 + (k - 2) * 14, 860 - k * 16, eback(prog(t, tk, 0.3)), (-6, 3, -2, 5, -3)[k])
        if t > tm + 0.5: place(c, text_img('₹5,000', 'anton', 96, INK), 540, 800)
    ts = at(i, 'Sensex', -0.3)
    if t > ts:
        sc, a = slam(t, ts + 0.2); place(c, stamp_c('SENSEX: 150', RED, 96, 6, 9), 540, 1150, sc, 0, a)
        place(c, text_img('today: 80,000+', 'mark', 52, GRN), 540, 1300, pp(t, ts + 0.8))
    src(c, t, 'Business Standard · The Quint · Wikipedia', T0 + 1.0, 1720)


def s3(c, t):
    i = 2; T0 = STARTS[i]
    dy, a = drop(t, T0 + 0.05, 360)
    if a > 0: place(c, SZ.clipping(1.0, 'TITAN', 'THE MARKET PAGE', '2002 · TATA GROUP · NSE: TITAN'), 540, 420 + dy, 0.95, 2, a)
    tw = at(i, 'Watches', -0.2)
    if t > tw: place(c, label('WATCHES', NAVY), 360, 720, pp(t, tw), -3)
    tj = at(i, 'Tanishq', -0.2)
    if t > tj: place(c, label('TANISHQ JEWELLERY', GOLD), 640, 830, pp(t, tj), 3)
    tf = at(i, 'few people', -0.3)
    if t > tf:
        place_text(c, 'few believed in it', 'pfi', 96, INK, 540, 1060, t, 'fb', tf, 'pop')
        place(c, text_img('Business Today, Jun 2026', 'type', 26, GREY, 1), 540, 1160, pp(t, tf + 0.4))
    src(c, t, 'First Titan buys 2002-03: Business Standard, Open magazine', T0 + 1.0, 1720)


def s4(c, t):
    i = 3; T0 = STARTS[i]
    place_text(c, 'HIS COST vs TODAY', 'anton', 100, INK, 540, 260, t, 'ct', T0 + 0.05, 'pop')
    d = ImageDraw.Draw(c); base = 1150
    tc = at(i, 'Under five', -0.3)
    if t > tc:
        d.rounded_rectangle((230, base - 20, 410, base), 8, fill=GREY, outline=INK, width=5)
        place(c, text_img('UNDER ₹5', 'anton', 60, INK), 320, base - 70, pp(t, tc))
        place(c, text_img('2002-03*', 'osw5', 34, GREY), 320, base + 40, pp(t, tc))
    tt = at(i, 'Today', -0.2)
    if t > tt:
        q = eo(prog(t, tt, 1.0)); hg = int(720 * q)
        d.rounded_rectangle((640, base - hg, 860, base), 12, fill=GOLD, outline=INK, width=5)
        place(c, text_img(f'₹{int(4650 * q):,}', 'anton', 70, INK), 750, base - hg - 46)
        place(c, text_img('25 NOV 2026', 'osw5', 34, GREY), 750, base + 40)
    d.line((120, base, 960, base), fill=INK, width=5)
    tm = at(i, 'nine hundred', -0.3)
    if t > tm:
        sc, a = slam(t, tm); place(c, stamp_c('900X+', RED, 140, -8, 17), 330, 640, sc, 0, a)
    place(c, text_img('*adjusted for split & bonus', 'type', 26, GREY, 1), 540, 1300, pp(t, tc + 0.5) if t > tc + 0.5 else 0)
    src(c, t, 'Cost: 5paisa, Yahoo Finance · Price: NSE via INDmoney', T0 + 1.0, 1720)


def s5(c, t):
    i = 4; T0 = STARTS[i]
    words_line(c, t, [("20", RED, T0 + 0.05), ("YEARS", INK, T0 + 0.25), ("HELD", INK, T0 + 0.45)], 'anton', 130, 290, key='yh')
    if t > T0 + 0.6:
        for k in range(20):
            tk = T0 + 0.6 + 0.07 * k
            if t < tk: continue
            r_, cc = divmod(k, 10)
            x = 120 + cc * 93; y = 480 + r_ * 110
            place(c, label(str(2003 + k)[2:], (NAVY, TEAL)[k % 2]), x, y, 0.8 * eback(prog(t, tk, 0.25)))
    tf = at(i, 'family', -0.3)
    if t > tf:
        place(c, text_img('4.72 CR TITAN SHARES', 'anton', 72, INK), 540, 820, pp(t, tf))
        place(c, text_img('Rekha Jhunjhunwala, Sep 2026 quarter', 'type', 28, GREY, 1), 540, 890, pp(t, tf + 0.2))
    tw = at(i, 'worth', -0.3)
    if t > tw:
        v = counter(0, 21943, t, tw, 1.1)
        place(c, text_img(f'₹{int(v):,} CR', 'anton', 150, GRN), 540, 1080)
        if t > tw + 1.0:
            sc, a = slam(t, tw + 1.0); place(c, stamp_c('STILL HOLDING', GRN, 70, 5, 23), 540, 1280, sc, 0, a)
    src(c, t, '47,184,470 shares (5.31%) × ₹4,650.6 (NSE, 25 Nov 2026)', T0 + 1.0, 1720)


PORT = [8431, 9500, 12000, 16000, 22000, 26000, 30652]
PLAB = ['MAR 20', '', '', '', '', '', 'AUG 22']


def s6(c, t):
    i = 5; T0 = STARTS[i]
    place_text(c, 'THE TWIST', 'anton', 120, RED, 540, 250, t, 'tw', T0 + 0.05, 'pop')
    c.alpha_composite(text_img('DISCLOSED PORTFOLIO (₹ CR)', 'type', 30, GREY, 2), (110, 380))
    ts = at(i, 'eight thousand', -0.3); te0 = at(i, 'thirty thousand', -0.3)
    rows = [('MAR 2020', 8431, GREY, ts), ('AUG 2022', 30652, GRN, te0)]
    bars(c, t, rows, 1050, 560, 30652, x0=330, gap=420, w=220)
    te = at(i, 'thirty thousand', -0.3)
    if t > te:
        sc, a = slam(t, te + 0.8); place(c, stamp_c('3.6X IN 2.5 YEARS', RED, 70, -5, 29), 360, 640, sc, 0, a)
        place_text(c, 'his age then: 59 to 62', 'mark', 48, INK, 540, 1250, t, 'ag', te + 0.9, 'slide', rot=-2)
    src(c, t, 'Disclosed portfolio value · Business Standard, Aug 2022', T0 + 1.0, 1720)


def s7(c, t):
    i = 6; T0 = STARTS[i]
    if t > T0 + 0.1:
        p = prog(t, T0 + 0.1, 0.3); lw = text_w('THE LESSON', 'osw', 54, 2); x0 = 540 - (lw + 70) / 2
        place(c, warn_icon(YEL), x0 + 28, 262, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
        place(c, text_img('THE LESSON', 'osw', 54, YEL, 2), x0 + 70 + lw / 2, 260, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
    tt = at(i, 'trader', -0.3)
    if t > tt:
        place(c, text_img('STARTED AS A TRADER', 'anton', 70, (200, 194, 182)), 540, 480, pp(t, tt))
    tr = at(i, 'real fortune', -0.3)
    if t > tr:
        place(c, text_img('FORTUNE CAME FROM', 'anton', 70, CREAM), 540, 640, pp(t, tr))
    tm = at(i, 'Time', -0.3)
    if t > tm:
        sc, a = slam(t, tm); place(c, stamp_c('TIME', YEL, 260, -6, 37), 540, 960, sc, 0, a)
        place(c, text_img('a good business, held for years', 'type', 34, (200, 194, 182), 1), 540, 1200, pp(t, tm + 0.5))
    typed(c, 'Not a buy/sell call. Education only.', 'type', 30, (200, 194, 182), 1500, t, T0 + 0.6, T0 + 1.6)


def s8(c, t):
    i = 7; T0 = STARTS[i]
    q = pp(t, T0, 0.45, 1.2)
    place(c, SS._card(960, 800), 540, 580, q, -0.4)
    if q > 0.6:
        place(c, text_img('THE BIG BULL · IN NUMBERS', 'anton', 56, INK), 540, 230)
        d = ImageDraw.Draw(c); d.line((90, 272, 990, 272), fill=INK, width=4)
        rows = [('Started (1985)', '₹5,000', INK), ('Sensex then', '150', INK), ('Net worth (2022)', '~₹46,000 Cr', GRN), ('First Titan buys', '2002-03', INK),
                ('Titan cost (adj.)', 'under ₹5', INK), ('Titan today', '₹4,650', GRN), ('Family Titan stake', '₹21,943 Cr', GRN)]
        for k, (a_, b_, col) in enumerate(rows):
            tk = T0 + 0.3 + 0.08 * k
            if t < tk: continue
            y = 300 + k * 78
            c.alpha_composite(text_img(a_, 'osw5', 38, INK), (100, y))
            v = text_img(b_, 'anton', 44, col); c.alpha_composite(v, (980 - v.size[0], y - 2))
    tq = at(i, 'Comment', -0.3)
    if t > tq:
        place(c, label('COMMENT: YOUR 20-YEAR STOCK', RED), 540, 1060, pp(t, tq), -2)
    SS.save_pulse(c, t, at(i, 'Save', -0.2), 540, 1200, 'SAVE THIS')
    tf = at(i, 'follow', -0.2)
    if t > tf:
        q2 = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1420, 0.5 + 0.5 * eback(q2), 0, clamp(q2 * 3))
    for k, ln in enumerate(['Price: NSE via INDmoney, 25 Nov 2026', 'Facts: Business Standard, Business Today, 5paisa', 'Not a buy/sell call. Education only.']):
        place_text(c, ln, 'type', 22, GREY, 540, 1680 + k * 34, t, None, T0 + 0.3, 'fade', track=1)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
DARK_SCENES = {6}


def slam_times():
    return [at(0, 'fifty five', 0), at(1, 'Sensex', -0.1), at(3, 'nine hundred', -0.3), at(5, 'thirty thousand', 0.2), at(6, 'Time', -0.3)] + [STARTS[k] + 0.05 for k in range(1, 7)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('THE BIG BULL LESSON', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
    ImageDraw.Draw(c).line((60, 118, W - 60, 118), fill=col, width=2)
    ImageDraw.Draw(c).line((60, 118, 60 + (W - 120) * clamp(t / DUR), 118), fill=RED if not dark else YEL, width=8)


def scene_at(t):
    k = 0
    for i, s in enumerate(STARTS):
        if t >= s: k = i
    return k


def _trans(c, t):
    cols = [(GOLD, INK), (YEL, INK), (RED, YEL), (GRN, CREAM), (YEL, RED), (INK, YEL), (RED, YEL), (YEL, INK)]
    for bi, b in enumerate(B):
        d = 0.62
        if abs(t - b) > d / 2 + 0.12: continue
        for layer, delay in ((0, -0.07), (1, 0.0)):
            p = (t - (b - d / 2) - delay) / d
            if p <= 0 or p >= 1: continue
            p = eio(p); SWd, skew = 2050, 320
            xl = (W + 60) + p * (-(SWd + skew) - (W + 60) - 40)
            r = random.Random(bi * 10 + layer + 999)
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
