"""10 Indian auto stocks: business, Oct 2026 sales, top seller, export markets, 1-year price change (collage, female VO)"""
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

SH = ROOT + 'autoten/'
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
# name, business, oct sales label, top seller, markets, price, 1y %, kind, phrase for 1y
D = [
 ('MARUTI SUZUKI', 'CARS', '2,76,120', 'WAGON R', ['100+ COUNTRIES', 'AFRICA', 'JAPAN', 'CHILE', 'SAUDI', 'MEXICO'], 13988, -12.1, 'CAR', 'down twelve', 'Top seller'),
 ('TATA MOTORS PV', 'CARS + JAGUAR LAND ROVER', '75,426', 'NEXON', ['INDIA', 'UK', 'US', 'CHINA', 'EUROPE'], 259.75, -27.4, 'CAR', 'Down twenty', 'Top seller'),
 ('MAHINDRA', 'SUVs + TRACTORS', '1,31,109', 'SCORPIO', ['SOUTH AFRICA', 'AUSTRALIA'], 3493.6, -5.4, 'CAR', 'Down five', 'Top seller'),
 ('HYUNDAI INDIA', 'CARS', '82,299', 'CRETA', ['MIDDLE EAST', 'AFRICA', 'LATIN AMERICA', 'MEXICO'], 2013.2, -13.2, 'CAR', 'Down thirteen', 'Top seller'),
 ('BAJAJ AUTO', 'BIKES + 3-WHEELERS', '5,01,194', 'PULSAR / BOXER', ['BRAZIL', 'MEXICO', 'NIGERIA', 'COLOMBIA'], 10739, 18.9, '2W', 'Up nineteen', 'Pulsar'),
 ('TVS MOTOR', 'BIKES + SCOOTERS', '7,00,134', 'JUPITER', ['80+ COUNTRIES', 'ASIA', 'AFRICA', 'LATAM'], 4580, 30.1, '2W', 'up thirty', 'Top seller'),
 ('HERO MOTOCORP', 'BIKES + SCOOTERS', '7,34,403', 'SPLENDOR', ['COLOMBIA', 'MEXICO', 'BANGLADESH', 'NIGERIA'], 5841.5, -5.0, '2W', 'Down five', 'Top seller'),
 ('EICHER MOTORS', 'ROYAL ENFIELD + TRUCKS', '1,33,442', 'CLASSIC 350', ['BRAZIL', 'COLOMBIA', 'MEXICO', 'N. AMERICA'], 8142, 16.3, '2W', 'Up sixteen', 'Top seller'),
 ('ASHOK LEYLAND', 'TRUCKS + BUSES', '21,888', 'TRUCKS & BUSES', ['GULF', 'AFRICA', 'SOUTH ASIA'], 155.25, -1.7, 'CV', 'down two', 'Trucks'),
 ('TATA MOTORS (CV)', 'TRUCKS + BUSES + PICKUPS', '47,652', 'PICKUPS & SCVs', ['INDIA', '+ IVECO: EUROPE', 'LATAM'], 428.3, 25.8, 'CV', 'Up twenty six', 'Sales'),
]
KCOL = {'CAR': BLUE, '2W': ORG, 'CV': TEAL}


@functools.lru_cache(None)
def card(w, h, fill=(253, 251, 246)):
    return cutout(Image.new('RGBA', (w, h), fill + (255,)), border=5, shadow=0.35)


def s_open(c, t):
    i = 0
    dy, a = drop(t, 0.1, 360)
    if a > 0: place(c, SZ.clipping(1.0, '10 AUTO STOCKS', 'INDIA · OCTOBER 2026', 'CARS · BIKES · TRUCKS'), 540, 380 + dy, 0.92, -2, a)
    tr = at(i, 'Record', -0.2)
    if t > tr:
        place(c, card(840, 260), 540, 760, pp(t, tr + 0.3), 1)
        if t > tr + 0.5:
            place(c, text_img('5,00,000+ CARS', 'anton', 84, GRN), 540, 730)
            place(c, text_img('record month for factory dispatches', 'type', 30, GREY, 1), 540, 820)
    tw = at(i, 'why', -0.3)
    if t > tw:
        sc, a2 = slam(t, tw); place(c, stamp_c('CAR STOCKS DOWN?', RED, 92, -5, 3), 540, 1080, sc, 0, a2)
    tt = at(i, 'Ten auto', -0.3)
    if t > tt: place_text(c, 'business · top seller · where they sell', 'mark', 46, INK, 540, 1270, t, 'bt', tt, 'slide', rot=-2)
    src(c, t, 'Oct 2026 dispatches: Autocar India, company releases', 1.0, 1720)


def make_stock(idx):
    nm, biz, sales, top, mk, px, ch, kind, ph1, phtop = D[idx]
    i = idx + 1

    def s(c, t):
        T0 = STARTS[i]
        place(c, label(f'{idx + 1}/10 · ' + kind if kind != 'CV' else f'{idx + 1}/10 · TRUCKS', KCOL[kind]), 540, 250, pp(t, T0 + 0.05))
        place_text(c, nm, 'anton', 110 if len(nm) < 14 else 92, INK, 540, 370, t, 'n%d' % idx, T0 + 0.1, 'pop')
        place(c, text_img(biz, 'osw5', 44, GREY), 540, 470, pp(t, T0 + 0.4))
        # tiles
        place(c, card(440, 260), 300, 700, pp(t, T0 + 0.6), -1.5)
        place(c, card(440, 260), 780, 700, pp(t, T0 + 0.8), 1.5)
        if t > T0 + 0.8:
            place(c, text_img('OCT 2026 SALES', 'type', 28, GREY, 2), 300, 620)
            place(c, text_img(sales, 'anton', 80, INK), 300, 710)
            place(c, text_img('units', 'type', 28, GREY, 1), 300, 790)
        if t > T0 + 1.0:
            place(c, text_img('TOP SELLER', 'type', 28, GREY, 2), 780, 620)
            tt = text_img(top, 'anton', 70 if len(top) < 12 else 52, KCOL[kind])
            place(c, tt, 780, 715)
        # markets chips
        tm = T0 + DURS[i] * 0.45
        c.alpha_composite(text_img('SELLS IN', 'type', 28, GREY, 2), (100, 900)) if t > tm - 0.2 else None
        x, y = 100, 950
        for k, m in enumerate(mk):
            tk = tm + 0.12 * k
            if t < tk: continue
            lb = label(m, NAVY)
            if x + lb.size[0] > 990: x, y = 100, y + lb.size[1] + 16
            place(c, lb, x + lb.size[0] / 2, y + lb.size[1] / 2, eback(prog(t, tk, 0.25)), (-2, 1.5, -1, 2, -1.5, 1)[k % 6])
            x += lb.size[0] + 16
        # 1y stamp
        tc = at(i, ph1, -0.3) if ph1 in SCRIPT[i] else T0 + DURS[i] - 2
        if t > tc:
            col = GRN if ch > 0 else RED
            sc, a = slam(t, tc); place(c, stamp_c(f'{ch:+.0f}% IN 1 YEAR', col, 96, -5 if ch < 0 else 5, 11 + idx), 540, 1330, sc, 0, a)
            place(c, text_img(f'₹{px:,.2f}'.replace('.00', '') if px < 1000 else f'₹{px:,.0f}', 'osw5', 44, INK), 540, 1470, pp(t, tc + 0.3))
        src(c, t, 'Price: NSE via INDmoney, 27 Nov 2026 · sales: company releases', T0 + 1.0, 1720)
    return s


def s_pattern(c, t):
    i = 11; T0 = STARTS[i]
    place_text(c, 'THE PATTERN', 'anton', 110, INK, 540, 260, t, 'pt', T0 + 0.05, 'pop')
    order = sorted(range(10), key=lambda k: D[k][6])
    d = ImageDraw.Draw(c); x0 = 560
    d.line((x0, 380, x0, 1380), fill=INK, width=4)
    for r, k in enumerate(order):
        tk = T0 + 0.3 + 0.12 * r
        if t < tk: continue
        nm, ch, kind = D[k][0], D[k][6], D[k][7]
        y = 420 + r * 96; q = eo(prog(t, tk, 0.5)); w = int(abs(ch) / 31 * 300 * q)
        col = KCOL[kind]
        if ch < 0:
            d.rounded_rectangle((x0 - w, y - 30, x0, y + 30), 8, fill=col, outline=INK, width=4)
            v = text_img(f'{ch:+.0f}%', 'anton', 40, RED); c.alpha_composite(v, (x0 + 14, y - 26))
            n = text_img(nm.replace('TATA MOTORS', 'TATA'), 'osw5', 30, INK); c.alpha_composite(n, (max(20, x0 - w - n.size[0] - 12), y - 22))
        else:
            d.rounded_rectangle((x0, y - 30, x0 + w, y + 30), 8, fill=col, outline=INK, width=4)
            v = text_img(f'{ch:+.0f}%', 'anton', 40, GRN); c.alpha_composite(v, (x0 - v.size[0] - 14, y - 26))
            n = text_img(nm.replace('TATA MOTORS', 'TATA'), 'osw5', 30, INK); c.alpha_composite(n, (min(1060 - n.size[0], x0 + w + 12), y - 22))
    for k, (lab, kc) in enumerate((('CARS', 'CAR'), ('BIKES', '2W'), ('TRUCKS', 'CV'))):
        place(c, label(lab, KCOL[kc]), 300 + k * 240, 1430, pp(t, T0 + 1.5))
    tr = at(i, "Record sales don't", -0.3)
    if t > tr:
        sc, a = slam(t, tr); place(c, stamp_c('SALES ≠ STOCK PRICE' if False else 'SALES UP, STOCK DOWN', RED, 80, -4, 41), 540, 1580, sc, 0, a)


def s_end(c, t):
    i = 12; T0 = STARTS[i]
    place_text(c, 'WHICH ONE DO YOU TRACK?', 'anton', 88, INK, 540, 300, t, 'wo', T0 + 0.05, 'pop')
    for k in range(10):
        r_, cc = divmod(k, 2)
        place(c, label(D[k][0], KCOL[D[k][7]]), 300 + cc * 480, 450 + r_ * 100, pp(t, T0 + 0.2 + 0.05 * k), (-2, 2)[cc])
    tc = at(i, 'Comment', -0.3)
    if t > tc:
        sc, a = slam(t, tc); place(c, stamp_c('COMMENT BELOW', RED, 90, -4, 33), 540, 1020, sc, 0, a)
    SS.save_pulse(c, t, at(i, 'Save', -0.2), 540, 1190, 'SAVE THIS')
    tf = at(i, 'Follow', -0.2)
    if t > tf:
        q2 = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1390, 0.5 + 0.5 * eback(q2), 0, clamp(q2 * 3))
    for k, ln in enumerate(['Sales: Oct 2026 company releases (Autocar India, Rushlane, Autopunditz)', 'Prices: NSE via INDmoney, 27 Nov 2026 · I may hold some of the stocks named', 'Not a buy/sell call. Education only.']):
        place_text(c, ln, 'type', 22, GREY, 540, 1680 + k * 34, t, None, T0 + 0.3, 'fade', track=1)


SCENES = [s_open] + [make_stock(k) for k in range(10)] + [s_pattern, s_end]
DARK_SCENES = set()


def slam_times():
    out = [at(0, 'why', -0.3)]
    for k in range(10):
        ph = D[k][8]
        out.append(at(k + 1, ph, -0.3) if ph in SCRIPT[k + 1] else STARTS[k + 1] + DURS[k + 1] - 2)
    return out + [at(11, "Record sales don't", -0.3), at(12, 'Comment', -0.3)] + [STARTS[k] + 0.05 for k in range(1, 12)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('10 AUTO STOCKS', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
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
