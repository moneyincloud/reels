"""Penny stock hype vs reality: a popular 2026 multibagger list (10 stocks) vs today, ₹1 L -> ₹63,810 (collage, male VO)"""
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

SH = ROOT + 'hypecheck/'
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
STK = [('YES BANK', 18.28, 17.73), ('JP POWER', 16.67, 13.07), ('PC JEWELLER', 14.91, 14.26), ('RATTANINDIA PWR', 12.19, 6.43), ('EASEMYTRIP', 14.05, 6.38),
       ('HATHWAY', 15.04, 9.10), ('SALASAR TECHNO', 13.16, 5.26), ('BRIGHTCOM', 10.25, 8.43), ('ORIENT GREEN', 16.44, 8.69), ('RAMA STEEL', 11.91, 3.97)]


@functools.lru_cache(None)
def card(w, h, fill=(253, 251, 246)):
    return cutout(Image.new('RGBA', (w, h), fill + (255,)), border=5, shadow=0.35)


def row(c, t, k, y, t0, show_now=True):
    nm, a, b = STK[k]; q = pp(t, t0, 0.35)
    if q <= 0: return
    c.alpha_composite(text_img(nm, 'osw5', 40, INK), (110, int(y - 26)))
    v = text_img(f'₹{a:.2f}', 'anton', 44, GREY); c.alpha_composite(v, (int(640 - v.size[0]), int(y - 28)))
    if show_now and t > t0 + 0.5:
        ImageDraw.Draw(c).line((640 - v.size[0] - 6, y + 2, 646, y + 2), fill=RED, width=4)
        v2 = text_img(f'₹{b:.2f}', 'anton', 50, RED); c.alpha_composite(v2, (int(860 - v2.size[0]), int(y - 32)))
        pc = text_img(f'{100 * (b / a - 1):+.0f}%', 'anton', 40, RED); c.alpha_composite(pc, (int(990 - pc.size[0]), int(y - 24)))


def sheet(c, t, t0, h=1180):
    place(c, card(960, h), 540, 330 + h / 2, pp(t, t0), -0.5)
    if t > t0 + 0.2:
        c.alpha_composite(text_img('"BEST MULTIBAGGER STOCKS UNDER ₹20 IN 2026"', 'type', 28, GREY, 1), (100, 360))
        c.alpha_composite(text_img('STOCK', 'type', 26, GREY, 2), (110, 420)); c.alpha_composite(text_img('ON LIST', 'type', 26, GREY, 2), (520, 420))
        c.alpha_composite(text_img('TODAY', 'type', 26, GREY, 2), (760, 420))
        ImageDraw.Draw(c).line((100, 460, 980, 460), fill=INK, width=3)


def s1(c, t):
    i = 0
    dy, a = drop(t, 0.1, 360)
    if a > 0: place(c, SZ.clipping(1.0, 'MULTIBAGGER LIST', 'PENNY STOCKS 2026', '10 STOCKS UNDER ₹20 · "BEST PICKS"'), 540, 420 + dy, 0.95, -3, a)
    tl = at(i, 'list', -0.3)
    if t > tl: place_text(c, 'hype vs reality', 'pfi', 100, INK, 540, 820, t, 'hv', tl, 'pop')
    tc = at(i, 'checked', -0.3)
    if t > tc:
        sc, a2 = slam(t, tc); place(c, stamp_c('I CHECKED', RED, 120, -6, 3), 540, 1080, sc, 0, a2)


def s2(c, t):
    i = 1; T0 = STARTS[i]
    sheet(c, t, T0 + 0.05)
    for k in range(10):
        row(c, t, k, 520 + k * 98, T0 + 0.5 + 0.3 * k, False)
    src(c, t, 'List: Jainam blog (published Jan 2025, updated Jun 2026). List prices as printed.', T0 + 1.0, 1720)


def s3(c, t):
    i = 2; T0 = STARTS[i]
    sheet(c, t, T0 - 9)
    for k in range(10):
        on = {0: at(i, 'Yes Bank', -0.2), 1: at(i, 'JP Power', -0.2)}.get(k)
        row(c, t, k, 520 + k * 98, T0 - 9, on is not None and t > on - 0.5)
    src(c, t, 'Today: NSE via INDmoney, 26 Nov 2026', T0 + 1.0, 1720)


def s4(c, t):
    i = 3; T0 = STARTS[i]
    sheet(c, t, T0 - 9)
    ons = {3: at(i, 'RattanIndia', -0.2), 4: at(i, 'EaseMyTrip', -0.2), 6: at(i, 'Salasar', -0.2)}
    for k in range(10):
        shown = k in (0, 1) or (k in ons and t > ons[k] - 0.5)
        row(c, t, k, 520 + k * 98, T0 - 9 if k not in ons else min(T0 - 9, ons[k]), shown)


def s5(c, t):
    i = 4; T0 = STARTS[i]
    sheet(c, t, T0 - 9)
    ons = {5: at(i, 'Hathway', -0.2), 8: at(i, 'Orient', -0.2), 7: at(i, 'Brightcom', -0.2), 2: at(i, 'PC Jeweller', -0.2), 9: at(i, 'Rama', -0.2)}
    for k in range(10):
        shown = k in (0, 1, 3, 4, 6) or (k in ons and t > ons[k] - 0.5)
        row(c, t, k, 520 + k * 98, T0 - 9, shown)
    tr = at(i, 'sixty seven', -0.3)
    if t > tr:
        sc, a = slam(t, tr); place(c, stamp_c('-67%', RED, 120, -8, 7), 820, 1580, sc, 0, a)


def s6(c, t):
    i = 5; T0 = STARTS[i]
    tt = at(i, 'Ten out of ten', -0.3)
    words_line(c, t, [("10", RED, tt), ("OUT", INK, tt + 0.15), ("OF", INK, tt + 0.3), ("10", RED, tt + 0.45)], 'anton', 200, 520, key='ten')
    if t > tt + 0.6: place(c, text_img('BELOW THE LIST PRICE', 'anton', 80, INK), 540, 720, pp(t, tt + 0.6))
    tn = at(i, 'Not one', -0.3)
    if t > tn:
        sc, a = slam(t, tn); place(c, stamp_c('0 MULTIBAGGERS', RED, 110, -5, 11), 540, 1000, sc, 0, a)


def s7(c, t):
    i = 6; T0 = STARTS[i]
    place_text(c, '₹10,000 IN EACH', 'anton', 110, INK, 540, 300, t, 'te', T0 + 0.05, 'pop')
    d = ImageDraw.Draw(c); base = 1250
    tl = at(i, 'one lakh', -0.3)
    if t > tl:
        d.rounded_rectangle((200, base - 700, 440, base), 14, fill=GREY, outline=INK, width=5)
        place(c, text_img('₹1,00,000', 'anton', 60, INK), 320, base - 750, pp(t, tl))
        place(c, text_img('PUT IN', 'osw5', 36, GREY), 320, base + 40)
    tw = at(i, 'sixty three', -0.3)
    if t > tw:
        q = eo(prog(t, tw, 0.8)); hg = int(700 * 0.6381 * q)
        d.rounded_rectangle((640, base - hg, 880, base), 14, fill=RED, outline=INK, width=5)
        place(c, text_img(f'₹{int(63810 * q):,}', 'anton', 64, RED), 760, base - hg - 50)
        place(c, text_img('TODAY', 'osw5', 36, GREY), 760, base + 40)
        if q > 0.95:
            sc, a = slam(t, tw + 0.8); place(c, stamp_c('-36%', RED, 130, -8, 13), 330, 1450, sc, 0, a)
    d.line((120, base, 960, base), fill=INK, width=5)
    src(c, t, 'From list prices to 26 Nov 2026. Excludes costs and dividends.', T0 + 1.0, 1720)


def s8(c, t):
    i = 7; T0 = STARTS[i]
    if t > T0 + 0.1:
        p = prog(t, T0 + 0.1, 0.3); lw = text_w('THE LESSON', 'osw', 54, 2); x0 = 540 - (lw + 70) / 2
        place(c, warn_icon(YEL), x0 + 28, 262, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
        place(c, text_img('THE LESSON', 'osw', 54, YEL, 2), x0 + 70 + lw / 2, 260, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
    tl = at(i, 'low share price', -0.3)
    if t > tl:
        place(c, text_img('LOW PRICE ≠ CHEAP COMPANY' if False else 'LOW PRICE IS NOT', 'anton', 84, CREAM), 540, 430, pp(t, tl))
        place(c, text_img('A CHEAP COMPANY', 'anton', 84, YEL), 540, 530, pp(t, tl + 0.3))
    for k, (txt, ph) in enumerate((('PROFITS?', 'profits'), ('DEBT?', 'debt'), ('PROMOTER PLEDGE?', 'pledge'), ('TRADING VOLUME?', 'volume'))):
        tk = at(i, ph, -0.3)
        if t < tk: continue
        y = 760 + k * 190; q = pp(t, tk, 0.35, 1.3)
        place(c, cutout(Image.new('RGBA', (860, 150), (40, 38, 36, 255)), border=6, shadow=0.4, bcol=YEL), 540, y, q, (-0.8, 0.8, -0.5, 0.6)[k])
        if q > 0.6: place(c, text_img(f'{k + 1}  CHECK {txt}', 'anton', 62, YEL), 540, y)
    typed(c, 'Not a buy/sell call. Education only.', 'type', 30, (200, 194, 182), 1560, t, at(i, 'volume', 0.3), at(i, 'volume', 1.3))


def s9(c, t):
    i = 8; T0 = STARTS[i]
    q = pp(t, T0, 0.45, 1.2)
    place(c, SS._card(960, 900), 540, 640, q, -0.4)
    if q > 0.6:
        place(c, text_img('THE LIST vs TODAY', 'anton', 60, INK), 540, 230)
        d = ImageDraw.Draw(c); d.line((90, 272, 990, 272), fill=INK, width=4)
        for k, (nm, a, b) in enumerate(STK):
            tk = T0 + 0.3 + 0.06 * k
            if t < tk: continue
            y = 300 + k * 74
            c.alpha_composite(text_img(nm, 'osw5', 38, INK), (100, y))
            v = text_img(f'₹{a:.2f} → ₹{b:.2f}' if False else f'{a:.2f} to {b:.2f}', 'osw5', 38, GREY); c.alpha_composite(v, (640 - v.size[0] // 2, y))
            p_ = text_img(f'{100 * (b / a - 1):+.0f}%', 'anton', 44, RED); c.alpha_composite(p_, (980 - p_.size[0], y - 4))
    SS.save_pulse(c, t, at(i, 'Save', -0.2), 540, 1180, 'SAVE THIS')
    tf = at(i, 'Follow', -0.2)
    if t > tf:
        q2 = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1380, 0.5 + 0.5 * eback(q2), 0, clamp(q2 * 3))
    for k, ln in enumerate(['List: Jainam blog "Multibagger Penny Stocks Under 20 Rs" (updated Jun 2026)', 'Today: NSE via INDmoney, 26 Nov 2026 · I may hold some of the stocks named', 'Not a buy/sell call. Education only.']):
        place_text(c, ln, 'type', 22, GREY, 540, 1680 + k * 34, t, None, T0 + 0.3, 'fade', track=1)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
DARK_SCENES = {7}


def slam_times():
    return [at(0, 'checked', -0.3), at(4, 'sixty seven', -0.3), at(5, 'Not one', -0.3), at(6, 'sixty three', 0.5)] + [STARTS[k] + 0.05 for k in range(1, 8)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('HYPE vs REALITY', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
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
