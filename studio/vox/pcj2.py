"""PC Jeweller Part 2: debt-free, profit up, but stock -23% from high. What's the catch? (collage style, male VO)"""
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

SH = ROOT + 'pcj2/'
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
MONTHLY = [11.62, 9.9, 9.53, 10.63, 9.92, 7.57, 9.37, 9.6, 8.76, 9.26, 10.99, 13.2, 15.48]
MLAB = ['OCT 25', '', '', 'JAN', '', 'MAR', '', '', '', 'JUL', '', '', 'OCT 26']


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
def s1(c, t):
    i = 0
    place(c, label('PART 2', RED), 540, 230, pp(t, 0.05), -3)
    dy, a = drop(t, 0.2, 360)
    if a > 0:
        hp = round(prog(t, 0.8, 0.5) * 20) / 20
        place(c, SZ.clipping(hp, 'PC JEWELLER', 'THE MARKET PAGE', 'JEWELLERY · NSE: PCJEWELLER'), 540, 520 + dy, 0.95, -3, a)
    td = at(i, 'debt free', -0.2)
    if t > td:
        sc, a2 = slam(t, td); place(c, stamp_c('DEBT FREE', GRN, 110, -8, 3), 540, 840, sc, 0, a2)
    tf = at(i, 'twenty three', -0.3)
    if t > tf:
        place(c, text_img('BUT', 'anton', 90, INK), 540, 1010, pp(t, tf - 0.2))
        sc, a3 = slam(t, tf + 0.1); place(c, stamp_c('-23% FROM HIGH', RED, 96, 5, 7), 540, 1170, sc, 0, a3)
    tw = at(i, 'Why', -0.2)
    if t > tw: place_text(c, 'why?', 'pfi', 120, INK, 540, 1380, t, 'why', tw, 'pop')
    src(c, t, '52-wk high ₹20.10 · 30 Oct close ₹15.48 · NSE via INDmoney', 1.0, 1720)


def s2(c, t):
    i = 1; T0 = STARTS[i]
    place_text(c, 'QUICK RECAP', 'anton', 120, INK, 540, 260, t, 'qr', T0 + 0.05, 'pop')
    c.alpha_composite(text_img('SALES (₹ CR)', 'type', 30, GREY, 2), (110, 380))
    rows = [('FY18', 9610, BLUE, at(i, '2018', -0.2)), ('FY24', 604, RED, at(i, 'six hundred', -0.4))]
    bars(c, t, rows, 1150, 640, 9610, x0=330, gap=420, w=200)
    tc = at(i, 'crashed', -0.3)
    if t > tc:
        sc, a = slam(t, tc + 0.4); place(c, stamp_c('-94%', RED, 110, -8, 11), 760, 650, sc, 0, a)
    tl = at(i, 'big loss', -0.3)
    if t > tl:
        place(c, label('FY24 LOSS: ₹629 CR', RED), 540, 1330, pp(t, tl), -2)
        place_text(c, 'banks wanted their money back', 'mark', 46, INK, 540, 1440, t, 'bw', tl + 0.5, 'slide', rot=-2)
    src(c, t, 'Consolidated sales & profit · Screener.in', T0 + 1.0, 1720)


def s3(c, t):
    i = 2; T0 = STARTS[i]
    place_text(c, 'THE COMEBACK', 'anton', 120, GRN, 540, 260, t, 'cb', T0 + 0.05, 'pop')
    c.alpha_composite(text_img('NET PROFIT (₹ CR)', 'type', 30, GREY, 2), (110, 380))
    rows = [('FY24', -629, RED, T0 + 0.3), ('FY25', 578, GRN, at(i, 'five seventy', -0.3)), ('FY26', 714, GRN, at(i, 'seven fourteen', -0.3)), ('Q2 FY27', 331, TEAL, at(i, 'three thirty', -0.3))]
    bars(c, t, rows, 900, 380, 714, x0=200, gap=230, w=150)
    tq = at(i, 'this quarter', 0.2)
    if t > tq:
        sc, a = slam(t, tq); place(c, stamp_c('+58% YoY', GRN, 84, -6, 21), 780, 1380, sc, 0, a)
        place_text(c, 'one quarter = ₹331 Cr', 'mark', 44, INK, 300, 1420, t, 'oq', tq + 0.2, 'slide', rot=-3)
    src(c, t, 'Screener.in · Q2 FY27 results (5paisa, Oct 2026)', T0 + 1.0, 1720)


def s4(c, t):
    i = 3; T0 = STARTS[i]
    words_line(c, t, [("DEBT", INK, T0 + 0.05), ("MELTING", RED, T0 + 0.25)], 'anton', 130, 270, key='dm')
    c.alpha_composite(text_img('BORROWINGS (₹ CR)', 'type', 30, GREY, 2), (110, 380))
    rows = [('MAR 24', 4150, RED, at(i, 'four thousand', -0.3)), ('MAR 25', 2151, ORG, at(i, 'four thousand', 0.5)),
            ('MAR 26', 1167, GOLD, at(i, 'four thousand', 1.0)), ('SEP 26', 339, GRN, at(i, 'four thousand', 1.5))]
    bars(c, t, rows, 1100, 600, 4150, x0=200, gap=230, w=150)
    tb = at(i, 'fourteen banks', -0.3)
    if t > tb:
        sc, a = slam(t, tb + 0.3); place(c, stamp_c('14 BANKS REPAID', GRN, 80, -5, 31), 620, 600, sc, 0, a)
    ts = at(i, 'says the company', -0.4)
    if t > ts:
        place_text(c, '"debt free" = bank dues cleared', 'mark', 44, INK, 540, 1280, t, 'df', ts, 'slide', rot=-2)
        place(c, text_img('Screener still shows ₹339 Cr other borrowings (Sep 2026)', 'type', 26, GREY, 1), 540, 1360, pp(t, ts + 0.4))
    src(c, t, 'Borrowings: Screener.in · bank repayment: company, Q2 FY27', T0 + 1.0, 1720)


@functools.lru_cache(None)
def store(col):
    w, h = 80, 70
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((6, 24, w - 6, h - 4), fill=SOFT, outline=INK, width=3)
    d.polygon([(0, 26), (w, 26), (w - 8, 6), (8, 6)], fill=col, outline=INK)
    d.rectangle((30, 40, 50, h - 4), fill=GOLD, outline=INK, width=2)
    return im


def s5(c, t):
    i = 4; T0 = STARTS[i]
    place_text(c, "WHAT'S NEXT", 'anton', 120, INK, 540, 260, t, 'wn', T0 + 0.05, 'pop')
    ts = at(i, 'hundred new', -0.4)
    if t > ts:
        for k in range(100):
            tk = ts + 0.012 * k
            if t < tk: continue
            r_, cc = divmod(k, 10); x = 140 + cc * 89; y = 400 + r_ * 62
            place(c, store((RED, GOLD, NAVY)[k % 3]), x, y, 0.75 * eback(prog(t, tk, 0.25)))
        place(c, label('UP TO 100 SHOWROOMS IN 12-18 MONTHS', NAVY), 540, 1060, pp(t, ts + 1.2), -1)
    tb = at(i, 'new brand', -0.3)
    if t > tb: place(c, label('NEW BRAND: LIGHTWEIGHT + LAB-GROWN DIAMONDS', PINK if False else ORG), 540, 1190, pp(t, tb), 1)
    te = at(i, 'one forty two', -0.3)
    if t > te:
        sc, a = slam(t, te + 0.3); place(c, stamp_c('₹142 CR COLLECTED', GRN, 76, -4, 41), 540, 1360, sc, 0, a)
        place_text(c, 'from old export dues (Q2)', 'mark', 42, INK, 540, 1470, t, 'ed', te + 0.5, 'slide', rot=-2)
    src(c, t, 'Company Q2 FY27 update (5paisa, Oct 2026)', T0 + 1.0, 1720)


def s6(c, t):
    i = 5; T0 = STARTS[i]
    p = prog(t, T0 + 0.1, 0.45)
    ox, oy, w, h = 60, 300 + (1 - eo(p)) * 600, 960, 760
    place(c, SZ.sheet_cut(w, h), ox + w / 2, oy + h / 2, 1.0, 0, clamp(p * 3))
    f = eio(prog(t, T0 + 0.4, 2.6))
    SZ.hand_chart(c, t, ox, oy, w, h, MONTHLY, MLAB, 5, 22, f, INK, YEL)
    tl = at(i, 'seven rupees', -0.3)
    if t > tl:
        x = ox + 90 + (w - 160) * 5 / 12; y = oy + h - 70 - (7.57 - 5) / 17 * (h - 140)
        marker_ellipse(c, x, y, 60, 40, prog(t, tl, 0.4), RED, 7, seed=3)
        place_text(c, 'low ₹7.47', 'mark', 44, RED, x, y + 70, t, 'lo', tl + 0.2, 'slide', rot=-3)
    th = at(i, 'twenty', -0.3)
    if t > th:
        place_text(c, 'intraday high ₹20.10 (Oct)', 'mark', 44, GRN, ox + w - 300, oy + 70, t, 'hi', th, 'slide', rot=-3)
    tn = at(i, 'near fifteen', -0.3)
    if t > tn: place(c, text_img('₹15.48', 'anton', 70, RED), ox + w - 160, oy + h - 220, pp(t, tn))
    tc = at(i, 'catch', -0.3)
    if t > tc: place_text(c, "so what's the catch?", 'pfi', 72, INK, 540, 1220, t, 'wc', tc, 'pop')
    src(c, t, 'Monthly close · NSE via INDmoney · 52-wk ₹7.47 to ₹20.10', T0 + 0.6, 1400)


def s7(c, t):
    i = 6; T0 = STARTS[i]
    words_line(c, t, [("CATCH", RED, T0 + 0.05), ("1:", RED, T0 + 0.2), ("DILUTION", INK, T0 + 0.35)], 'anton', 110, 270, key='c1')
    c.alpha_composite(text_img('EQUITY SHARE CAPITAL (₹ CR)', 'type', 30, GREY, 2), (110, 380))
    rows = [('FY24', 465, GREY, at(i, 'new shares', -0.3)), ('SEP 26', 981, RED, at(i, 'more than doubled', -0.3))]
    bars(c, t, rows, 1000, 480, 981, x0=330, gap=420, w=200)
    td = at(i, 'more than doubled', 0.6)
    if t > td:
        sc, a = slam(t, td); place(c, stamp_c('2.1X SHARES', RED, 84, -6, 51), 330, 560, sc, 0, a)
    tp = at(i, 'Promoters', -0.3)
    if t > tp:
        d = ImageDraw.Draw(c)
        c.alpha_composite(text_img('PROMOTER HOLDING', 'type', 28, GREY, 2), (110, 1150))
        for k, (lab, v, col) in enumerate((('MAR 24', 54.53, GREY), ('SEP 26', 39.11, RED))):
            y = 1240 + k * 110; q = eo(prog(t, tp + 0.3 * k, 0.7)); ww = int(v / 60 * 640 * q)
            c.alpha_composite(text_img(lab, 'osw5', 34, INK), (110, y - 22))
            d.rounded_rectangle((280, y - 30, 280 + ww, y + 30), 10, fill=col, outline=INK, width=4)
            c.alpha_composite(text_img(f'{v * q:.1f}%', 'anton', 50, col), (296 + ww, y - 32))
    src(c, t, 'Screener.in · 9.72 Cr warrants converted (per Screener notes)', T0 + 1.0, 1720)


def s8(c, t):
    i = 7; T0 = STARTS[i]
    if t > T0 + 0.1:
        p = prog(t, T0 + 0.1, 0.3); lw = text_w('THE VERDICT', 'osw', 54, 2); x0 = 540 - (lw + 70) / 2
        place(c, warn_icon(YEL), x0 + 28, 262, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
        place(c, text_img('THE VERDICT', 'osw', 54, YEL, 2), x0 + 70 + lw / 2, 260, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
    ts = at(i, 'third of 2018', -0.3)
    if t > ts:
        place(c, text_img('SALES: ₹3,352 CR (FY26) vs ₹9,610 CR (FY18)', 'osw5', 40, CREAM), 540, 400, pp(t, ts))
    th = at(i, 'Eleven lakh', -0.3)
    if t > th:
        v = 2.1 + (11.15 - 2.1) * eo(prog(t, th, 1.0))
        place(c, text_img(f'{v:.1f} LAKH', 'anton', 130, YEL), 540, 560)
        place(c, text_img('shareholders now (2.1 lakh in Mar 2024)', 'type', 30, (200, 194, 182), 1), 540, 660, pp(t, th + 0.4))
    rows = [('TURNAROUND', 'REAL', GRN, True, 'turnaround is real'), ('MULTIBAGGER', 'NOT PROVEN', RED, False, 'not proven')]
    for k, (h1, h2, col, ok, ph) in enumerate(rows):
        tk = at(i, ph, -0.3)
        if t < tk: continue
        y = 900 + k * 260; q = pp(t, tk, 0.35, 1.3)
        place(c, cutout(Image.new('RGBA', (900, 210), (40, 38, 36, 255)), border=6, shadow=0.4, bcol=col), 540, y, q, (-0.8, 0.8)[k])
        if q < 0.6: continue
        d = ImageDraw.Draw(c); bx = 160
        if ok: d.line((bx - 28, y + 2, bx - 8, y + 26, bx + 30, y - 24), fill=col, width=12, joint='curve')
        else: d.line((bx - 24, y - 24, bx + 24, y + 24), fill=col, width=12); d.line((bx - 24, y + 24, bx + 24, y - 24), fill=col, width=12)
        c.alpha_composite(text_img(h1, 'anton', 64, CREAM), (230, int(y - 80)))
        c.alpha_composite(text_img(h2, 'anton', 64, col), (230, int(y)))
    typed(c, 'Not investment advice. DYOR.', 'type', 30, (200, 194, 182), 1500, t, at(i, 'not proven', 0.1), at(i, 'not proven', 0.8))


def s9(c, t):
    i = 8; T0 = STARTS[i]
    q = pp(t, T0, 0.45, 1.2)
    place(c, SS._card(960, 860), 540, 600, q, -0.4)
    if q > 0.6:
        place(c, text_img('PC JEWELLER · PART 2', 'anton', 56, INK), 540, 230)
        d = ImageDraw.Draw(c); d.line((90, 272, 990, 272), fill=INK, width=4)
        rows = [('Price (30 Oct close)', '₹15.48', INK), ('From 52-wk high', '-23%', RED), ('Q2 FY27 profit', '₹331 Cr (+58%)', GRN), ('Bank dues', 'repaid', GRN),
                ('Borrowings (Screener)', '₹339 Cr', ORG), ('Share capital', '2.1x since FY24', RED), ('Promoters', '39.1%', RED), ('P/E', '16.9', INK)]
        for k, (a_, b_, col) in enumerate(rows):
            tk = T0 + 0.3 + 0.08 * k
            if t < tk: continue
            y = 300 + k * 78
            c.alpha_composite(text_img(a_, 'osw5', 38, INK), (100, y))
            v = text_img(b_, 'anton', 44, col); c.alpha_composite(v, (980 - v.size[0], y - 2))
        SS.save_pulse(c, t, T0 + 1.2, 540, 1080, 'SAVE THIS')
    SS.send_frame(c, t, at(i, 'send it', -0.3), 'your PC Jeweller group', y=1300)
    tf = at(i, 'Follow', -0.2)
    if t > tf:
        q2 = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1530, 0.5 + 0.5 * eback(q2), 0, clamp(q2 * 3))
    for k, ln in enumerate(['Price: NSE via INDmoney, 30 Oct 2026', 'Fundamentals: Screener.in · Q2 FY27 company update', 'Not a buy/sell call. Education only.']):
        place_text(c, ln, 'type', 22, GREY, 540, 1680 + k * 34, t, None, T0 + 0.3, 'fade', track=1)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
DARK_SCENES = {7}


def slam_times():
    return [at(0, 'debt free', -0.2), at(0, 'twenty three', -0.2), at(1, 'crashed', 0.1), at(6, 'more than doubled', 0.6)] + [STARTS[k] + 0.05 for k in range(1, 8)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('MULTIBAGGER OR TRAP? · PART 2', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
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
