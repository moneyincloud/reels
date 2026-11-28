"""₹50 L home loan, 20 y at 8%: 4 ways to cut interest (13th EMI, ₹1 L/yr, 5% EMI step-up, lower rate) (collage, female VO)"""
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

SH = ROOT + 'homeloan/'
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
@functools.lru_cache(None)
def card(w, h, fill=(253, 251, 246)):
    return cutout(Image.new('RGBA', (w, h), fill + (255,)), border=5, shadow=0.35)


@functools.lru_cache(None)
def house(w=360):
    h = int(w * 0.9); im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(w * 0.08, h * 0.45), (w * 0.5, h * 0.05), (w * 0.92, h * 0.45)], fill=RED, outline=INK, width=8)
    d.rectangle((w * 0.16, h * 0.45, w * 0.84, h * 0.95), fill=(240, 220, 170), outline=INK, width=8)
    d.rectangle((w * 0.42, h * 0.62, w * 0.58, h * 0.95), fill=(140, 95, 55), outline=INK, width=6)
    d.rectangle((w * 0.22, h * 0.55, w * 0.36, h * 0.69), fill=(170, 210, 230), outline=INK, width=5)
    d.rectangle((w * 0.64, h * 0.55, w * 0.78, h * 0.69), fill=(170, 210, 230), outline=INK, width=5)
    return cutout(im, border=6, shadow=0.35)


def tbar(c, t, t0, years, y, col, lab):
    d = ImageDraw.Draw(c); x0, W = 120, 840
    q = eo(prog(t, t0, 0.8))
    d.rounded_rectangle((x0, y - 26, x0 + W, y + 26), 12, fill=(225, 219, 207), outline=INK, width=4)
    w = int(W * years / 20 * q)
    if w > 10: d.rounded_rectangle((x0, y - 26, x0 + w, y + 26), 12, fill=col, outline=INK, width=4)
    c.alpha_composite(text_img(lab, 'osw5', 34, INK), (x0, int(y - 80)))
    v = text_img(f'{years * q:.1f} YRS' if years % 1 else f'{int(years * q)} YRS', 'anton', 40, INK); c.alpha_composite(v, (x0 + W - v.size[0], int(y - 84)))


def s1(c, t):
    i = 0
    place(c, house(), 540, 470, eback(prog(t, 0.1, 0.4)), -2)
    place(c, label('₹50 LAKH · 20 YEARS', NAVY), 540, 760, pp(t, 0.3))
    tf = at(i, 'fifty lakh more', -0.3)
    if t > tf:
        sc, a = slam(t, tf); place(c, stamp_c('+₹50 L INTEREST', RED, 110, -6, 3), 540, 980, sc, 0, a)
    tc = at(i, 'cut it', -0.4)
    if t > tc: place_text(c, "here's how to cut it", 'mark', 60, INK, 540, 1200, t, 'cut', tc, 'slide', rot=-2)


def s2(c, t):
    i = 1; T0 = STARTS[i]
    place(c, label('AT 8% INTEREST', NAVY), 540, 280, pp(t, T0 + 0.05))
    te = at(i, 'EMI', -0.3)
    if t > te:
        place(c, card(800, 200), 540, 450, pp(t, te), -1)
        if t > te + 0.2:
            place(c, text_img('EMI', 'type', 30, GREY, 2), 540, 400)
            place(c, text_img('₹41,822 / MONTH', 'anton', 80, INK), 540, 475)
    d = ImageDraw.Draw(c); base = 1300
    d.rounded_rectangle((220, base - 600, 440, base), 14, fill=GREY, outline=INK, width=5)
    place(c, text_img('₹50 L', 'anton', 64, INK), 330, base - 650); place(c, text_img('LOAN', 'osw5', 36, GREY), 330, base + 40)
    ti = at(i, 'Total interest', -0.3)
    if t > ti:
        q = eo(prog(t, ti, 0.8)); hg = int(600 * 50.37 / 50 * q)
        d.rounded_rectangle((640, base - hg, 860, base), 14, fill=RED, outline=INK, width=5)
        place(c, text_img(f'₹{50.4 * q:.1f} L', 'anton', 64, RED), 750, base - hg - 50); place(c, text_img('INTEREST', 'osw5', 36, GREY), 750, base + 40)
    d.line((120, base, 960, base), fill=INK, width=5)
    tm = at(i, 'More than', -0.3)
    if t > tm:
        sc, a = slam(t, tm); place(c, stamp_c('MORE THAN THE LOAN', RED, 70, -5, 5), 540, 1480, sc, 0, a)
    src(c, t, 'Standard EMI formula. Rates today ~7.25%-8.7% (bank sites, Nov 2026)', T0 + 1.0, 1720)


def trick(c, t, i, num, title, sub, save, years, col, best=False):
    T0 = STARTS[i]
    place(c, label(f'TRICK {num}' + (' · THE BEST' if best else ''), col), 540, 270, pp(t, T0 + 0.05))
    place_text(c, title, 'anton', 92 if len(title) < 18 else 76, INK, 540, 410, t, 't%d' % num, T0 + 0.15, 'pop')
    if sub: place(c, text_img(sub, 'osw5', 44, GREY), 540, 510, pp(t, T0 + 0.5))
    ts = at(i, 'Save', -0.3) if 'Save' in SCRIPT[i] else at(i, 'saves', -0.3)
    if t > ts:
        sc, a = slam(t, ts); place(c, stamp_c(f'SAVE {save}', GRN, 120, -5, 7 + num), 540, 760, sc, 0, a)
    if years:
        tbar(c, t, T0 + 0.6, 20, 1060, GREY, 'NORMAL LOAN')
        td = at(i, 'Done', -0.3) if 'Done' in SCRIPT[i] else at(i, 'finish', -0.3)
        if t > td: tbar(c, t, td, years, 1240, col, 'WITH THIS TRICK')


def s3(c, t): trick(c, t, 2, 1, 'ONE EXTRA EMI A YEAR', '13 EMIs instead of 12', '₹9.1 L', 17, BLUE)
def s4(c, t): trick(c, t, 3, 2, 'PREPAY ₹1 LAKH A YEAR', 'bonus, incentive, savings', '₹17 L', 14, TEAL)
def s5(c, t): trick(c, t, 4, 3, 'EMI +5% EVERY YEAR', 'as your salary grows', '₹17.7 L', 12.3, GRN, True)


def s6(c, t):
    trick(c, t, 5, 4, 'ASK FOR A LOWER RATE', '8% to 7.5%', '₹3.7 L', 0, ORG)
    T0 = STARTS[5]
    if t > T0 + 1.5:
        place(c, card(860, 260), 540, 1150, pp(t, T0 + 1.5), 1)
        if t > T0 + 1.7:
            place(c, text_img('EMI ₹41,822 to ₹40,280', 'anton', 60, INK), 540, 1110)
            place(c, text_img('bank fee to switch is usually small', 'type', 30, GREY, 1), 540, 1200)


def s7(c, t):
    i = 6; T0 = STARTS[i]
    place_text(c, 'EVERY TIME YOU PREPAY', 'anton', 90, INK, 540, 300, t, 'ep', T0 + 0.05, 'pop')
    tr = at(i, 'Reduce my tenure', -0.3)
    if t > tr:
        place(c, card(880, 300), 540, 640, pp(t, tr), -1)
        if t > tr + 0.2:
            place(c, text_img('REDUCE MY TENURE', 'anton', 90, GRN), 540, 640)
    tn = at(i, 'not my EMI', -0.3)
    if t > tn:
        place(c, card(880, 220), 540, 960, pp(t, tn), 1)
        if t > tn + 0.2:
            place(c, text_img('NOT MY EMI', 'anton', 84, RED), 540, 960)
            ImageDraw.Draw(c).line((330, 960, 750, 960), fill=RED, width=8)
    if t > tn + 0.5: place_text(c, 'tenure cut saves far more', 'mark', 54, INK, 540, 1180, t, 'tc', tn + 0.5, 'slide', rot=-2)


def s8(c, t):
    i = 7; T0 = STARTS[i]
    if t > T0 + 0.1:
        p = prog(t, T0 + 0.1, 0.3); lw = text_w('BEFORE YOU PREPAY', 'osw', 54, 2); x0 = 540 - (lw + 70) / 2
        place(c, warn_icon(YEL), x0 + 28, 262, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
        place(c, text_img('BEFORE YOU PREPAY', 'osw', 54, YEL, 2), x0 + 70 + lw / 2, 260, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
    for k, (h1, ph, col) in enumerate((('6 MONTHS EMERGENCY FUND', 'six months', YEL), ('NO PREPAYMENT CHARGE?', 'no prepayment', YEL), ('CHECK WITH YOUR BANK', 'check with', RED))):
        tk = at(i, ph, -0.3)
        if t < tk: continue
        y = 520 + k * 250; q = pp(t, tk, 0.35, 1.3)
        place(c, cutout(Image.new('RGBA', (920, 190), (40, 38, 36, 255)), border=6, shadow=0.4, bcol=col), 540, y, q, (-0.8, 0.8, -0.5)[k])
        if q > 0.6: place(c, text_img(h1, 'anton', 66, col), 540, y)
    typed(c, 'usually nil on floating-rate loans for individuals', 'type', 30, (200, 194, 182), 1320, t, at(i, 'no prepayment', 0.3), at(i, 'no prepayment', 1.5))
    typed(c, 'Not financial advice. Education only.', 'type', 30, (200, 194, 182), 1500, t, at(i, 'check with', 0.3), at(i, 'check with', 1.3))


def s9(c, t):
    i = 8; T0 = STARTS[i]
    q = pp(t, T0, 0.45, 1.2)
    place(c, SS._card(960, 820), 540, 600, q, -0.4)
    if q > 0.6:
        place(c, text_img('₹50 L · 20 YRS · 8%', 'anton', 60, INK), 540, 240)
        d = ImageDraw.Draw(c); d.line((90, 282, 990, 282), fill=INK, width=4)
        rows = [('Normal: interest', '₹50.4 L', RED), ('13th EMI a year', 'save ₹9.1 L', GRN), ('₹1 L prepay a year', 'save ₹17 L', GRN),
                ('EMI +5% a year', 'save ₹17.7 L', GRN), ('Rate 8% to 7.5%', 'save ₹3.7 L', GRN), ('Prepay = cut', 'TENURE', INK)]
        for k, (a_, b_, col) in enumerate(rows):
            tk = T0 + 0.3 + 0.08 * k
            if t < tk: continue
            y = 310 + k * 90
            c.alpha_composite(text_img(a_, 'osw5', 42, INK), (100, y))
            v = text_img(b_, 'anton', 48, col); c.alpha_composite(v, (980 - v.size[0], y - 4))
    ts = at(i, 'send it', -0.3)
    if t > ts:
        sc, a = slam(t, ts); place(c, stamp_c('SEND TO A HOME LOAN FRIEND', RED, 60, -4, 33), 540, 1100, sc, 0, a)
    SS.save_pulse(c, t, at(i, 'Save', -0.2), 540, 1260, 'SAVE THIS')
    tf = at(i, 'Follow', -0.2)
    if t > tf:
        q2 = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1440, 0.5 + 0.5 * eback(q2), 0, clamp(q2 * 3))
    for k, ln in enumerate(['Illustration: ₹50 L, 20 years, 8% floating. Your rate may differ.', 'Savings = interest saved over the loan. Not financial advice.', 'Education only.']):
        place_text(c, ln, 'type', 22, GREY, 540, 1680 + k * 34, t, None, T0 + 0.3, 'fade', track=1)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
DARK_SCENES = {7}


def slam_times():
    out = [at(0, 'fifty lakh more', -0.3), at(1, 'More than', -0.3), at(8, 'send it', -0.3)]
    for i in (2, 3, 4, 5):
        out.append(at(i, 'Save', -0.3) if 'Save' in SCRIPT[i] else at(i, 'saves', -0.3))
    return out + [STARTS[k] + 0.05 for k in range(1, 8)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('HOME LOAN HACKS', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
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
