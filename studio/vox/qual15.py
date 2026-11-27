"""15 largest stocks in NSE Nifty Smallcap250 Quality 50: business, P/E, ROCE; quality != cheap (collage, male VO)"""
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

SH = ROOT + 'qual15/'
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
PURP = (120, 70, 170)
# name, business, sector colour, P/E, ROCE, extra stat (label) or None, emoji-free icon word
Q = [
 ('SONA COMSTAR', 'EV gears & motors for global carmakers', BLUE, 68.1, 15.1, None),
 ('ANAND RATHI WEALTH', 'Wealth management for rich families', NAVY, 89.0, 57.47, 'ROCE 57%'),
 ('KARUR VYSYA BANK', 'Tamil Nadu private bank, from Karur', NAVY, 12.0, 7.6, 'P/E 12'),
 ('DR LAL PATHLABS', 'Blood tests & diagnostic labs', TEAL, 55.9, 28.0, None),
 ('ANGEL ONE', 'Stock trading app', NAVY, 28.5, 14.8, 'QTR PROFIT +58%'),
 ('CDSL', 'Holds your demat shares', NAVY, 59.7, 32.0, None),
 ('ADITYA BIRLA SL AMC', 'Mutual funds', NAVY, 28.9, 32.2, None),
 ('MOTHERSON WIRING', 'Wiring harnesses inside cars', BLUE, 40.6, 38.9, None),
 ('HIMADRI', 'Carbon chemicals & battery materials', PURP, 32.2, 22.1, None),
 ('SUN TV', 'Tamil TV channels, Chennai', ORG, 16.0, 16.4, None),
 ('ZF COMMERCIAL', 'Brakes for trucks & buses', BLUE, 49.0, 19.1, None),
 ('GILLETTE INDIA', 'Razors & Oral-B', ORG, 34.4, 90.7, 'ROCE 91%'),
 ('AFFLE 3i', 'Mobile advertising tech', PURP, 46.7, 16.8, None),
 ('INDRAPRASTHA GAS', 'CNG & piped gas, Delhi', TEAL, 20.7, 17.5, None),
 ('KAJARIA CERAMICS', 'Floor & wall tiles', ORG, 30.4, 23.4, None),
]


@functools.lru_cache(None)
def card(w, h, fill=(253, 251, 246)):
    return cutout(Image.new('RGBA', (w, h), fill + (255,)), border=5, shadow=0.35)


def s_open(c, t):
    i = 0
    dy, a = drop(t, 0.1, 360)
    if a > 0: place(c, SZ.clipping(1.0, '15 SMALL CAPS', "NSE'S OWN QUALITY TEST", 'NIFTY SMALLCAP250 QUALITY 50 INDEX'), 540, 380 + dy, 0.92, -2, a)
    for k, (txt, ph, col) in enumerate((('HIGH RETURN ON EQUITY', 'High return', GRN), ('LOW DEBT', 'low debt', BLUE), ('STEADY EARNINGS', 'steady', ORG))):
        tk = at(i, ph, -0.2)
        if t < tk: continue
        place(c, label(txt, col), 540, 720 + k * 120, eback(prog(t, tk, 0.3)), (-2, 2, -1)[k])
    tw = at(i, 'what each', -0.3)
    if t > tw:
        sc, a2 = slam(t, tw); place(c, stamp_c('WHAT EACH ONE DOES', RED, 80, -5, 3), 540, 1180, sc, 0, a2)
    src(c, t, 'Index methodology: NSE Indices factsheet, 30 Oct 2026', 1.0, 1720)


def make_q(idx):
    nm, biz, col, pe, roce, extra = Q[idx]
    i = idx + 1

    def s(c, t):
        T0 = STARTS[i]
        # running counter row of dots
        for k in range(15):
            x = 105 + k * 62; on = k <= idx
            d = ImageDraw.Draw(c); d.ellipse((x - 18, 232, x + 18, 268), fill=(col if k == idx else (GRN if on else (220, 214, 202))), outline=INK, width=3)
        place(c, text_img(f'{idx + 1}/15', 'anton', 60, INK), 540, 340, pp(t, T0 + 0.05))
        place_text(c, nm, 'anton', 104 if len(nm) < 15 else 84, INK, 540, 480, t, 'q%d' % idx, T0 + 0.05, 'pop')
        place(c, card(900, 220), 540, 700, pp(t, T0 + 0.25), -1)
        if t > T0 + 0.4:
            place(c, text_img(biz, 'osw5', 52 if len(biz) < 30 else 44, col), 540, 700)
        for k, (lab, v) in enumerate((('P/E', f'{pe:.0f}'), ('ROCE', f'{roce:.0f}%'))):
            place(c, card(380, 220), 300 + k * 480, 1000, pp(t, T0 + 0.5 + 0.15 * k), (-2, 2)[k])
            if t > T0 + 0.6 + 0.15 * k:
                place(c, text_img(lab, 'type', 32, GREY, 2), 300 + k * 480, 940)
                place(c, text_img(v, 'anton', 96, INK), 300 + k * 480, 1030)
        if extra and t > T0 + DURS[i] * 0.5:
            sc, a = slam(t, T0 + DURS[i] * 0.5); place(c, stamp_c(extra, GRN if 'P/E' not in extra else NAVY, 90, -5, 7 + idx), 540, 1300, sc, 0, a)
        src(c, t, 'Screener.in, 26 Nov 2026 · ROCE: return on capital employed', T0 + 0.6, 1720)
    return s


def s_warn(c, t):
    i = 16; T0 = STARTS[i]
    if t > T0 + 0.1:
        p = prog(t, T0 + 0.1, 0.3); lw = text_w('QUALITY IS NOT CHEAP', 'osw', 54, 2); x0 = 540 - (lw + 70) / 2
        place(c, warn_icon(YEL), x0 + 28, 262, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
        place(c, text_img('QUALITY IS NOT CHEAP', 'osw', 54, YEL, 2), x0 + 70 + lw / 2, 260, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
    ti = at(i, 'twelve', -0.3)
    if t > ti:
        sc, a = slam(t, ti); place(c, stamp_c('INDEX -12% IN 1 YEAR', RED, 86, -5, 41), 540, 520, sc, 0, a)
    ts = at(i, 'sixty', -0.3)
    if t > ts:
        hi = sorted(Q, key=lambda r: -r[3])[:3]
        for k, r in enumerate(hi):
            y = 780 + k * 170; q = pp(t, ts + 0.15 * k, 0.35, 1.3)
            place(c, cutout(Image.new('RGBA', (900, 140), (40, 38, 36, 255)), border=6, shadow=0.4, bcol=YEL), 540, y, q, (-0.8, 0.8, -0.5)[k])
            if q > 0.6:
                c.alpha_composite(text_img(r[0], 'anton', 54, CREAM), (130, int(y - 32)))
                v = text_img(f'P/E {r[3]:.0f}', 'anton', 58, YEL); c.alpha_composite(v, (int(950 - v.size[0]), int(y - 34)))
    tc = at(i, 'Check the price', -0.3)
    if t > tc: place_text(c, 'check the price you pay', 'mark', 56, CREAM, 540, 1340, t, 'cp', tc, 'slide', rot=-2)
    typed(c, 'Not a buy/sell call. Education only.', 'type', 30, (200, 194, 182), 1520, t, tc + 0.3, tc + 1.3)


def s_end(c, t):
    i = 17; T0 = STARTS[i]
    q = pp(t, T0, 0.45, 1.2)
    place(c, SS._card(960, 1000), 540, 650, q, -0.4)
    if q > 0.6:
        place(c, text_img('15 QUALITY SMALL CAPS', 'anton', 56, INK), 540, 200)
        d = ImageDraw.Draw(c); d.line((90, 240, 990, 240), fill=INK, width=4)
        for k, r in enumerate(Q):
            tk = T0 + 0.2 + 0.04 * k
            if t < tk: continue
            y = 258 + k * 56
            c.alpha_composite(text_img(r[0], 'osw5', 34, INK), (100, y))
            v = text_img(f'P/E {r[3]:.0f} · ROCE {r[4]:.0f}%', 'osw5', 32, GREY); c.alpha_composite(v, (980 - v.size[0], y + 2))
    SS.save_pulse(c, t, at(i, 'Save', -0.2), 540, 1250, 'SAVE THIS')
    tf = at(i, 'Follow', -0.2)
    if t > tf:
        q2 = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1440, 0.5 + 0.5 * eback(q2), 0, clamp(q2 * 3))
    for k, ln in enumerate(['15 largest by market cap in Nifty Smallcap250 Quality 50 (NSE)', 'Data: Screener.in 26 Nov 2026 · I may hold some of the stocks named', 'Not a buy/sell call. Education only.']):
        place_text(c, ln, 'type', 22, GREY, 540, 1680 + k * 34, t, None, T0 + 0.3, 'fade', track=1)


SCENES = [s_open] + [make_q(k) for k in range(15)] + [s_warn, s_end]
DARK_SCENES = {16}


def slam_times():
    return [at(0, 'what each', -0.3), at(16, 'twelve', -0.3)] + [STARTS[k + 1] + DURS[k + 1] * 0.5 for k in range(15) if Q[k][5]] + [STARTS[k] + 0.05 for k in range(1, 17)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('15 QUALITY SMALL CAPS', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
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
