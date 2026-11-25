"""Two friends: Arun SIP from 25 (₹5.5 Cr) vs Karthik from 45 (₹47.6 L), 12% illustration + inflation note (collage, female VO)"""
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

SH = ROOT + 'twofriends/'
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
R = 1.12 ** (1 / 12) - 1
def fv(n): return 10000 * ((1 + R) ** n - 1) / R * (1 + R) if n > 0 else 0
def arun(age): return fv(max(0, (age - 25) * 12))
def karthik(age): return fv(max(0, (age - 45) * 12))


@functools.lru_cache(None)
def card(w, h, fill=(253, 251, 246)):
    return cutout(Image.new('RGBA', (w, h), fill + (255,)), border=5, shadow=0.35)


@functools.lru_cache(None)
def person(name, col, shirt):
    w, h = 300, 380
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((40, 200, 260, 380), 60, fill=shirt, outline=INK, width=6)          # body
    d.ellipse((90, 60, 210, 190), fill=(176, 122, 86), outline=INK, width=6)                 # head
    d.chord((84, 44, 216, 150), 180, 360, fill=(30, 26, 24), outline=INK, width=6)           # hair
    d.ellipse((122, 112, 136, 126), fill=INK); d.ellipse((164, 112, 178, 126), fill=INK)
    d.arc((128, 130, 172, 166), 20, 160, fill=INK, width=5)
    im = cutout(im, border=6, shadow=0.35)
    lab = label(name, col)
    out = Image.new('RGBA', (max(im.size[0], lab.size[0]), im.size[1] + lab.size[1] - 10), (0, 0, 0, 0))
    out.alpha_composite(im, ((out.size[0] - im.size[0]) // 2, 0)); out.alpha_composite(lab, ((out.size[0] - lab.size[0]) // 2, im.size[1] - 10))
    return out


def money(v):
    return f'₹{v / 1e7:.2f} CR' if v >= 1e7 else f'₹{v / 1e5:.1f} L'


def s1(c, t):
    i = 0
    words_line(c, t, [("TWO", INK, 0.1), ("FRIENDS", RED, 0.3)], 'anton', 150, 300, key='tf')
    for k, (nm, col, sh, ph) in enumerate((('ARUN', GRN, (90, 150, 110), 'Same college'), ('KARTHIK', ORG, (210, 140, 80), 'same office'))):
        tk = at(i, ph, -0.3)
        if t > tk: place(c, person(nm, col, sh), 300 + k * 480, 700, eback(prog(t, tk, 0.35)), (-4, 4)[k])
    tc = at(i, 'crores', -0.3)
    if t > tc:
        sc, a = slam(t, tc); place(c, stamp_c('CRORES', GRN, 120, -8, 3), 300, 1120, sc, 0, a)
    tl = at(i, 'lakhs', -0.3)
    if t > tl:
        sc, a = slam(t, tl); place(c, stamp_c('LAKHS', RED, 120, 7, 5), 780, 1120, sc, 0, a)
    place_text(c, 'same salary', 'mark', 56, INK, 540, 1330, t, 'ss', at(i, 'same salary', -0.3), 'slide', rot=-2)


def s2(c, t):
    i = 1; T0 = STARTS[i]
    place(c, person('ARUN', GRN, (90, 150, 110)), 300, 620, pp(t, at(i, 'Arun', -0.2)), -3)
    place(c, person('KARTHIK', ORG, (210, 140, 80)), 780, 620, pp(t, at(i, 'Karthik', -0.2)), 3)
    ta = at(i, 'twenty five', -0.3)
    if t > ta:
        place(c, label('AGE 25', NAVY), 300, 960, pp(t, ta)); place(c, label('AGE 25', NAVY), 780, 960, pp(t, ta + 0.1))
    ts = at(i, 'fifty thousand', -0.3)
    if t > ts:
        place(c, card(860, 220), 540, 1200, pp(t, ts), -1)
        if t > ts + 0.2:
            place(c, text_img('₹50,000 / MONTH', 'anton', 80, INK), 540, 1170)
            place(c, text_img('both · Chennai IT jobs', 'type', 30, GREY, 1), 540, 1250)
    src(c, t, 'Illustration: names and people are fictional', T0 + 1.0, 1720)


def s3(c, t):
    i = 2; T0 = STARTS[i]
    place(c, person('ARUN', GRN, (90, 150, 110)), 540, 470, pp(t, T0 + 0.05))
    ts = at(i, 'ten thousand', -0.3)
    if t > ts:
        sc, a = slam(t, ts); place(c, stamp_c('₹10,000 SIP', GRN, 110, -5, 7), 540, 830, sc, 0, a)
    tn = at(i, 'Nifty', -0.2)
    if t > tn: place(c, label('NIFTY 50 INDEX FUND', NAVY), 540, 990, pp(t, tn), 2)
    te = at(i, 'Every month', -0.3)
    if t > te:
        for k in range(12):
            tk = te + 0.08 * k
            if t < tk: continue
            r_, cc = divmod(k, 6); x = 160 + cc * 152; y = 1180 + r_ * 120
            place(c, label(('JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC')[k], GRN), x, y, 0.75 * eback(prog(t, tk, 0.25)), (-3, 2, -1, 3, -2, 1)[cc])
    tk = at(i, 'No skipping', -0.3)
    if t > tk: place_text(c, 'no skipping', 'mark', 60, INK, 540, 1460, t, 'nsk', tk, 'slide', rot=-2)


def s4(c, t):
    i = 3; T0 = STARTS[i]
    place(c, person('KARTHIK', ORG, (210, 140, 80)), 540, 470, pp(t, T0 + 0.05))
    tl = at(i, 'later', -0.3)
    if t > tl: place_text(c, '"I\'ll start later"', 'pfi', 84, INK, 540, 820, t, 'isl', tl, 'pop')
    for k, (txt, ph) in enumerate((('BIKE EMI', 'bike'), ('NEW PHONE', 'phone'), ('WEDDING', 'wedding'), ('CAR EMI', 'car'))):
        tk = at(i, ph, -0.2)
        if t < tk: continue
        sc, a = slam(t, tk); place(c, stamp_c(txt, RED, 76, (-8, 6, -5, 9)[k], 11 + k), (300, 780, 330, 760)[k], (1020, 1080, 1260, 1320)[k], sc, 0, a)


def axis(c, t, t0, f_a, f_k, show_k=True):
    ox, oy, w, h = 60, 300, 960, 900
    place(c, SZ.sheet_cut(w, h), ox + w / 2, oy + h / 2, 1.0, 0, 1)
    d = ImageDraw.Draw(c); vmax = 5.6e7
    def P(age, v): return (ox + 90 + (w - 160) * (age - 25) / 35, oy + h - 80 - v / vmax * (h - 170))
    d.line((ox + 80, oy + h - 80, ox + w - 50, oy + h - 80), fill=INK, width=4)
    for age in (25, 35, 45, 55, 60):
        x, _ = P(age, 0); li = text_img(str(age), 'osw5', 30, GREY); c.alpha_composite(li, (int(x - li.size[0] / 2), oy + h - 66))
    c.alpha_composite(text_img('AGE', 'type', 26, GREY, 2), (ox + w - 120, oy + h - 120))
    for who, fn, f, col, start in (('A', arun, f_a, GRN, 25), ('K', karthik, f_k, ORG, 45)):
        if f <= 0 or (who == 'K' and not show_k): continue
        end = 25 + 35 * f
        pts = [P(a / 4, fn(a / 4)) for a in range(100, int(end * 4) + 1)]
        if len(pts) > 1:
            stroke(c, pts, 10, col)
            x, y = pts[-1]; d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=col, outline=INK, width=4)
    return P


def s5(c, t):
    i = 4; T0 = STARTS[i]
    place_text(c, 'AGE 45: KARTHIK STARTS', 'anton', 88, INK, 540, 1320, t, 'k45', T0 + 0.05, 'pop')
    P = axis(c, t, T0, 20 / 35 + 0 * t, 0)
    x, y = P(45, arun(45))
    place(c, label('ARUN AT 45: ' + money(arun(45)), GRN), min(x, 760), y - 70, pp(t, T0 + 0.2))
    tk = at(i, 'same ten', -0.3)
    if t > tk:
        x2, y2 = P(45, 0); place(c, label('KARTHIK: ₹0', ORG), x2, y2 - 60, pp(t, tk))


def s6(c, t):
    i = 5; T0 = STARTS[i]
    f = 20 / 35 + 15 / 35 * eio(prog(t, T0 + 0.1, 3.0))
    P = axis(c, t, T0, f, f)
    ta = at(i, 'forty two', -0.3)
    if t > ta: place(c, label('ARUN PUT IN ₹42 L', GRN), 330, 1320, pp(t, ta), -2)
    tk = at(i, 'eighteen', -0.3)
    if t > tk: place(c, label('KARTHIK PUT IN ₹18 L', ORG), 750, 1420, pp(t, tk), 2)


def s7(c, t):
    i = 6; T0 = STARTS[i]
    P = axis(c, t, T0, 1, 1)
    place(c, label('12% A YEAR (ILLUSTRATION)', NAVY), 540, 360, pp(t, T0 + 0.1))
    ta = at(i, 'five point five', -0.3)
    if t > ta:
        x, y = P(60, arun(60)); place(c, label(money(arun(60)), GRN), x - 120, y + 60, pp(t, ta))
        sc, a = slam(t, ta + 0.2); place(c, stamp_c('ARUN: ₹5.5 CR', GRN, 92, -5, 21), 540, 1300, sc, 0, a)
    tk = at(i, 'forty seven', -0.3)
    if t > tk:
        x, y = P(60, karthik(60)); place(c, label('₹47.6 L', ORG), x - 100, y - 60, pp(t, tk))
        sc, a = slam(t, tk); place(c, stamp_c('KARTHIK: ₹47.6 L', RED, 80, 5, 23), 540, 1450, sc, 0, a)
    src(c, t, 'Nifty 50 TRI 20-yr CAGR 12.44% (NSE whitepaper 2026). Past returns do not repeat.', T0 + 1.0, 1720)


def s8(c, t):
    i = 7; T0 = STARTS[i]
    place_text(c, 'THE MATHS', 'anton', 120, INK, 540, 280, t, 'tm', T0 + 0.05, 'pop')
    for k, (h1, a_, b_, ph, col) in enumerate((('PUT IN', '₹42 L', '₹18 L', 'two times', NAVY), ('ENDED WITH', '₹5.5 CR', '₹47.6 L', 'eleven times', GRN))):
        tk = at(i, ph, -0.4)
        if t < tk: continue
        y = 560 + k * 360
        place(c, card(900, 300), 540, y, pp(t, tk), (-1, 1)[k])
        if t > tk + 0.2:
            place(c, text_img(h1, 'type', 34, GREY, 3), 540, y - 100)
            place(c, text_img('ARUN ' + a_, 'anton', 64, GRN), 540, y - 20)
            place(c, text_img('KARTHIK ' + b_, 'anton', 56, ORG), 540, y + 70)
        sc, a = slam(t, tk + 0.5); place(c, stamp_c(('2.3X', '11.6X')[k], col if k else RED, 90, (-8, 8)[k], 27 + k), 900, y - 120, sc, 0, a)
    th = at(i, 'heavy lifting', -0.4)
    if t > th: place_text(c, '20 extra years = the real money', 'mark', 52, INK, 540, 1330, t, 'hl', th, 'slide', rot=-2)


def s9(c, t):
    i = 8; T0 = STARTS[i]
    if t > T0 + 0.1:
        p = prog(t, T0 + 0.1, 0.3); lw = text_w('HONEST NOTE', 'osw', 54, 2); x0 = 540 - (lw + 70) / 2
        place(c, warn_icon(YEL), x0 + 28, 262, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
        place(c, text_img('HONEST NOTE', 'osw', 54, YEL, 2), x0 + 70 + lw / 2, 260, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
    tg = at(i, 'not guaranteed', -0.3)
    if t > tg: place(c, text_img('RETURNS ARE NOT GUARANTEED', 'anton', 60, CREAM), 540, 430, pp(t, tg))
    ti = at(i, 'inflation', -0.3)
    if t > ti: place(c, text_img('INFLATION IS REAL (6% A YEAR ASSUMED)', 'osw5', 40, (200, 194, 182)), 540, 520, pp(t, ti))
    for k, (nm, v1, v2, ph, col) in enumerate((('ARUN', '₹5.5 CR', '~₹72 L', "Arun's", GRN), ('KARTHIK', '₹47.6 L', '~₹6 L', "Karthik's", ORG))):
        tk = at(i, ph, -0.3)
        if t < tk: continue
        y = 780 + k * 360; q = pp(t, tk, 0.35, 1.3)
        place(c, cutout(Image.new('RGBA', (920, 300), (40, 38, 36, 255)), border=6, shadow=0.4, bcol=col), 540, y, q, (-0.8, 0.8)[k])
        if q > 0.6:
            place(c, text_img(nm + ' AT 60: ' + v1, 'osw5', 46, (200, 194, 182)), 540, y - 80)
            place(c, text_img(v2, 'anton', 110, col), 540, y + 20)
            place(c, text_img("in today's money", 'type', 30, CREAM, 1), 540, y + 110)
    typed(c, 'Still an 11.6x gap. Not a buy/sell call. Education only.', 'type', 30, (200, 194, 182), 1520, t, at(i, 'six lakh', 0.2), at(i, 'six lakh', 1.4))


def s10(c, t):
    i = 9; T0 = STARTS[i]
    place_text(c, 'WHICH FRIEND ARE YOU?', 'anton', 96, INK, 540, 280, t, 'wf', T0 + 0.05, 'pop')
    place(c, person('ARUN', GRN, (90, 150, 110)), 300, 640, pp(t, T0 + 0.2), -3)
    place(c, person('KARTHIK', ORG, (210, 140, 80)), 780, 640, pp(t, T0 + 0.3), 3)
    tt = at(i, 'Tag', -0.3)
    if t > tt:
        sc, a = slam(t, tt); place(c, stamp_c('TAG YOUR KARTHIK', RED, 96, -4, 33), 540, 1020, sc, 0, a)
    SS.save_pulse(c, t, at(i, 'Save', -0.2), 540, 1200, 'SAVE THIS')
    tf = at(i, 'follow', -0.2)
    if t > tf:
        q2 = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1400, 0.5 + 0.5 * eback(q2), 0, clamp(q2 * 3))
    for k, ln in enumerate(['₹10,000/month SIP, 12% a year (illustration), 6% inflation', 'Nifty 50 TRI 20-yr CAGR 12.44%: NSE Nifty 50 whitepaper 2026', 'Not a buy/sell call. Education only.']):
        place_text(c, ln, 'type', 22, GREY, 540, 1680 + k * 34, t, None, T0 + 0.3, 'fade', track=1)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]
DARK_SCENES = {8}


def slam_times():
    return [at(0, 'crores', -0.3), at(0, 'lakhs', -0.3), at(2, 'ten thousand', -0.3)] + [at(3, p, -0.2) for p in ('bike', 'phone', 'wedding', 'car')] + \
           [at(6, 'five point five', -0.1), at(6, 'forty seven', -0.3), at(9, 'Tag', -0.3)] + [STARTS[k] + 0.05 for k in range(1, 9)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('TWO FRIENDS · ONE LESSON', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
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
