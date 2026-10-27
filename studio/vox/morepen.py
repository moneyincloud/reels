"""Morepen Labs Q2 FY27 results — multibagger or trap? (paper Vox, template v2, no captions)"""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs, warn_icon
from fridge import follow_btn
import tea as TEA
import saveshare as SS

SH = ROOT + 'morepen/'
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
card_box = TEA.card_box; label = TEA.label
CLOSES = json.load(open(SH + 'closes.json'))


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def pp(t, t0, d=0.35, s=1.6): return eback(prog(t, t0, d), s)


def spark(c, pts, p, col, w=12):
    n = len(pts) - 1; f = p * n; k = int(f); out = pts[:k + 1]
    if k < n: a, b = pts[k], pts[k + 1]; fr = f - k; out = out + [(a[0] + (b[0] - a[0]) * fr, a[1] + (b[1] - a[1]) * fr)]
    if len(out) >= 2: stroke(c, out, w, col)
    return out[-1]


# ---------- icons ----------
@functools.lru_cache(maxsize=None)
def meter_icon():
    im = Image.new('RGBA', (220, 260), (0, 0, 0, 0)); d = ImageDraw.Draw(im); O = INK
    d.rounded_rectangle((30, 20, 190, 240), 40, fill=BLUE, outline=O, width=7)
    d.rounded_rectangle((55, 50, 165, 130), 14, fill=(220, 240, 230), outline=O, width=5)
    tx = text_img('108', 'anton', 54, INK); im.alpha_composite(tx, (110 - tx.size[0] // 2, 62))
    for x in (80, 140): d.ellipse((x - 18, 160, x + 18, 196), fill=CREAM, outline=O, width=5)
    d.rectangle((95, 236, 125, 258), fill=(240, 240, 240), outline=O, width=4)
    d.ellipse((102, 0, 118, 20), fill=RED, outline=O, width=3)
    return im


@functools.lru_cache(maxsize=None)
def factory_icon():
    im = Image.new('RGBA', (260, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(im); O = INK
    d.polygon([(20, 190), (20, 90), (80, 120), (80, 90), (140, 120), (140, 90), (200, 120), (200, 190)], fill=TEAL, outline=O)
    d.line([(20, 190), (20, 90), (80, 120), (80, 90), (140, 120), (140, 90), (200, 120), (200, 190), (20, 190)], fill=O, width=6)
    d.rectangle((205, 30, 240, 190), fill=GREY, outline=O, width=6)
    for x in (45, 105, 165): d.rectangle((x - 14, 145, x + 14, 175), fill=YEL, outline=O, width=4)
    return im


@functools.lru_cache(maxsize=None)
def gavel_icon():
    im = Image.new('RGBA', (240, 220), (0, 0, 0, 0)); d = ImageDraw.Draw(im); O = INK
    hd = Image.new('RGBA', (240, 220), (0, 0, 0, 0)); dh = ImageDraw.Draw(hd)
    dh.rounded_rectangle((60, 40, 180, 100), 14, fill=(140, 90, 50), outline=O, width=6)
    dh.rectangle((40, 50, 62, 90), fill=(110, 70, 40), outline=O, width=5); dh.rectangle((178, 50, 200, 90), fill=(110, 70, 40), outline=O, width=5)
    dh.rounded_rectangle((112, 96, 128, 200), 6, fill=(160, 110, 60), outline=O, width=5)
    im.alpha_composite(hd.rotate(35, Image.BICUBIC, center=(120, 110)))
    d.rounded_rectangle((20, 180, 150, 212), 8, fill=(110, 70, 40), outline=O, width=5)
    return im


@functools.lru_cache(maxsize=None)
def doc_icon(txt='₹825 CR'):
    im = Image.new('RGBA', (200, 240), (0, 0, 0, 0)); d = ImageDraw.Draw(im); O = INK
    d.rectangle((20, 10, 180, 230), fill=CREAM, outline=O, width=6)
    for y in (50, 80, 110): d.line((45, y, 155, y), fill=GREY, width=6)
    tx = text_img(txt, 'anton', 40, GRN); im.alpha_composite(tx, (100 - tx.size[0] // 2, 135))
    d.line((50, 205, 90, 190, 120, 210, 150, 195), fill=NAVY, width=5)
    return im


def chart(c, t, t0, dur=1.8, x0=140, x1=940, yt=520, yb=960, col=GRN, show_price=True):
    v = CLOSES; lo, hi = 33.05, max(v)
    pts = [(x0 + (x1 - x0) * k / (len(v) - 1), yb - (yb - yt) * (p - lo) / (hi - lo)) for k, p in enumerate(v)]
    d = ImageDraw.Draw(c)
    for gy in (yt, (yt + yb) / 2, yb): d.line((x0, gy, x1, gy), fill=(225, 220, 210), width=2)
    p = eio(prog(t, t0, dur)); tx, ty = spark(c, pts, p, col, 11)
    f = p * (len(v) - 1); k = min(int(f), len(v) - 2); val = v[k] + (v[k + 1] - v[k]) * (f - k)
    d.ellipse((tx - 13, ty - 13, tx + 13, ty + 13), fill=col, outline=INK, width=4)
    if show_price: place(c, text_img(f'₹{val:.0f}', 'anton', 58, INK), min(tx, 860), ty - 50)
    return p


def src(c, t, txt, t0, y=1700):
    if t > t0: place_text(c, txt, 'type', 28, GREY, 540, y, t, None, t0, 'fade', track=1)


# ---------- scenes ----------
def s1(c, t):
    i = 0
    words_line(c, t, [("4X", GRN, 0.0), ("IN", INK, 0.12), ("7 MONTHS", INK, 0.22)], 'anton', 150, 290, key='h')
    p = chart(c, t, 0.0, 2.2, yt=480, yb=900)
    if t > 0.05: place(c, text_img('₹33 · MAR 2026 LOW', 'osw5', 34, GREY), 300, 935)
    tb = at(i, "Don't buy", -0.2)
    if t > tb:
        sh = math.sin(t * 40) * 6 * math.exp(-(t - tb) * 3)
        place(c, label("DON'T BUY BEFORE YOU SEE THIS", RED), 540 + sh, 1040, 1.15 * pp(t, tb), -2)
    tp = at(i, 'profit more', -0.3)
    if t > tp:
        s_, a = slam(t, tp); place(c, stamp_c('PROFIT 2X TODAY', GRN, 110, -5, 101), 540, 1220, s_, 0, a)
    tm = at(i, 'Multibagger', -0.3)
    if t > tm: place(c, label('MULTIBAGGER?', GRN), 300, 1420, 1.35 * pp(t, tm), -5)
    tt = at(i, 'trap', -0.3)
    if t > tt:
        sh = math.sin(t * 40) * 6 * math.exp(-(t - tt) * 3)
        place(c, label('TRAP?', RED), 800 + sh, 1420, 1.5 * pp(t, tt), 5)
    src(c, t, 'weekly close, NSE via INDmoney · to 27 Oct 2026', 0.6, 1560)


def s2(c, t):
    i = 1; T0 = STARTS[i] + 0.05
    place(c, meter_icon(), 200, 360, 0.95 * pp(t, T0), -6) if t > T0 else None
    place_text(c, 'MOREPEN', 'anton', 120, INK, 640, 310, t, 'mn', T0 + 0.05, 'pop')
    place_text(c, 'LABORATORIES', 'osw5', 52, BLUE, 640, 410, t, 'ml', T0 + 0.2, 'slide')
    tg = at(i, 'glucose', -0.3)
    if t > tg: place(c, label('DR MOREPEN GLUCOSE METERS', NAVY), 540, 560, 1.1 * pp(t, tg), -1)
    tc = at(i, 'five percent', -0.3)
    if t > tc:
        q = pp(t, tc, 0.4, 1.3); place(c, card_box(860, 380, SOFT), 540, 860, q, -1)
        if q > 0.6:
            v = SS.roll_number(t, tc + 0.2, 1.2, 126.01, 132.18)
            place(c, text_img('YESTERDAY ₹126.01', 'anton', 58, GREY), 540, 750)
            place(c, text_img(f'TODAY ₹{v:.2f}', 'anton', 100, GRN), 540, 870)
            place(c, text_img('+4.9%', 'anton', 64, GRN), 540, 975)
    tu = at(i, 'upper circuit', -0.1)
    if t > tu:
        s_, a = slam(t, tu); place(c, stamp_c('UPPER CIRCUIT', RED, 120, -6, 202), 540, 1170, s_, 0, a)
    src(c, t, 'NSE close 27 Oct 2026 · market cap ~₹6,905 Cr', STARTS[i] + 0.8, 1380)


def stat_row(c, t, t0, y, name, val_fn, chg, col=GRN):
    if t < t0: return
    q = pp(t, t0, 0.4, 1.3); place(c, card_box(900, 200, SOFT), 540, y, q, (-1, 1, -0.5)[int(y) % 3])
    if q < 0.6: return
    c.alpha_composite(text_img(name, 'osw5', 42, GREY), (130, int(y - 82)))
    c.alpha_composite(text_img(val_fn(t), 'anton', 84, INK), (130, int(y - 40)))
    lb = label(chg, col); place(c, lb, 820, y + 10, 1.2 * pp(t, t0 + 0.5), -4)


def s3(c, t):
    i = 2; T0 = STARTS[i] + 0.05
    place_text(c, 'Q2 RESULTS', 'anton', 130, INK, 540, 290, t, 'q2', T0, 'pop')
    place_text(c, 'July – September 2026', 'mark', 56, NAVY, 540, 400, t, 'q2b', T0 + 0.2, 'slide', rot=-2)
    tr = at(i, 'Revenue', -0.3)
    stat_row(c, t, tr, 600, 'REVENUE', lambda t: f'₹{SS.roll_number(t, tr + 0.3, 1.0, 0, 755):.0f} CR', '+81%')
    tp = at(i, 'Profit', -0.3)
    stat_row(c, t, tp, 860, 'NET PROFIT', lambda t: f'₹{SS.roll_number(t, tp + 0.3, 1.0, 0, 89):.0f} CR', '+117%')
    tm = at(i, 'Margins', -0.3)
    if t > tm:
        q = pp(t, tm, 0.4, 1.3); place(c, card_box(900, 300, SOFT), 540, 1170, q, 0.6)
        if q > 0.6:
            c.alpha_composite(text_img('EBITDA MARGIN', 'osw5', 46, GREY), (130, 1050))
            ph = eo(prog(t, tm + 0.3, 1.0)); d = ImageDraw.Draw(c)
            for k, (nm, v, cl) in enumerate((('Q2 LAST YEAR', 8.1, GREY), ('Q2 NOW', 17.5, GRN))):
                y = 1140 + k * 90; w = int(27 * v * ph)
                c.alpha_composite(text_img(nm, 'osw5', 34, INK), (130, y - 22))
                d.rounded_rectangle((330, y - 26, 330 + w, y + 26), 10, fill=cl, outline=INK, width=3)
                c.alpha_composite(text_img(f'{v * ph:.1f}%', 'anton', 46, cl if k else INK), (345 + w, y - 28))
    src(c, t, 'Company release, 27 Oct 2026 · consolidated Q2 FY27', STARTS[i] + 0.8, 1420)


def s4(c, t):
    i = 3; T0 = STARTS[i] + 0.05
    place_text(c, 'THE ENGINE', 'anton', 130, INK, 540, 290, t, 'en', T0, 'pop')
    tc = at(i, 'CDMO', -0.3)
    if t > tc:
        place(c, factory_icon(), 220, 470, 0.9 * pp(t, tc), -4)
        place(c, label('CDMO = MAKING MEDICINES FOR', TEAL), 620, 440, 1.0 * pp(t, tc + 0.1), -1)
        place(c, label('OTHER PHARMA COMPANIES', TEAL), 620, 515, 1.0 * pp(t, tc + 0.25), 1)
    t58 = at(i, 'fifty eight', -0.3); t253 = at(i, 'two fifty three', -0.3)
    if t > t58:
        q = pp(t, t58, 0.4, 1.3); place(c, card_box(880, 560, SOFT), 540, 930, q, -0.6)
        if q > 0.6:
            d = ImageDraw.Draw(c); base = 1110
            d.line((150, base, 930, base), fill=INK, width=5)
            for k, (nm, v, tk, cl) in enumerate((('Q1', 58, t58, GREY), ('Q2', 253, t253, TEAL))):
                ph = eo(prog(t, tk, 0.9)); h = int(1.4 * v * ph); x = 340 + k * 380
                if t > tk:
                    d.rounded_rectangle((x - 90, base - h, x + 90, base), 12, fill=cl, outline=INK, width=4)
                    place(c, text_img(f'₹{v * ph:.0f} CR', 'anton', 60, INK), x, base - h - 44)
                place(c, text_img(nm + ' FY27', 'osw5', 38, GREY), x, base + 40)
    if t > t253 + 0.9:
        s_, a = slam(t, t253 + 0.9); place(c, stamp_c('4.4X IN ONE QUARTER', RED, 90, -5, 404), 540, 1330, s_, 0, a)
    td = at(i, 'eight twenty five', -0.3)
    if t > td:
        place(c, doc_icon(), 230, 1540, 0.75 * pp(t, td), -6)
        place(c, label('₹825 CR GLOBAL CDMO DEAL', NAVY), 650, 1540, 1.1 * pp(t, td + 0.1), -2)


def s5(c, t):
    i = 4; T0 = STARTS[i] + 0.05
    place_text(c, '2 MORE WINS', 'anton', 130, INK, 540, 290, t, 'mw', T0, 'pop')
    tc = at(i, 'court', -0.3)
    if t > tc:
        place(c, gavel_icon(), 540, 540, pp(t, tc), -5 + 10 * math.exp(-(t - tc) * 4) * math.sin((t - tc) * 20))
        place(c, label('TAX DEMAND QUASHED', NAVY), 540, 720, 1.2 * pp(t, tc + 0.2), -2)
    t3 = at(i, 'three hundred', -0.3)
    if t > t3:
        s_, a = slam(t, t3); place(c, stamp_c('₹317 CR RISK REMOVED', GRN, 92, -4, 505), 540, 880, s_, 0, a)
    src(c, t, 'HP High Court order · 14 Oct 2026', t3 + 0.4 if t > t3 else 1e9, 1030)
    te = at(i, 'exports', -0.3)
    if t > te:
        q = pp(t, te, 0.4, 1.3); place(c, card_box(880, 300, SOFT), 540, 1250, q, 0.8)
        if q > 0.6:
            place(c, text_img('EXPORTS · Q2', 'osw5', 46, GREY), 540, 1150)
            place(c, text_img(f'₹{SS.roll_number(t, te + 0.3, 1.0, 172, 397):.0f} CR', 'anton', 100, INK), 450, 1260)
            place(c, label('+131%', GRN), 800, 1265, 1.3 * pp(t, te + 0.8), -5)


def s6(c, t):
    i = 5; T0 = STARTS[i] + 0.05
    place_text(c, 'SOUNDS LIKE A', 'anton', 80, INK, 540, 240, t, 'sl', T0, 'pop')
    place_text(c, 'MULTIBAGGER?', 'anton', 110, GRN, 540, 335, t, 'sl2', T0 + 0.15, 'pop')
    tb = at(i, 'nobody', -0.4)
    if t > tb:
        s_, a = slam(t, tb); place(c, stamp_c('BUT…', RED, 140, -8, 606), 540, 530, s_, 0, a)
    tf = at(i, 'four times', -0.3)
    if t > tf:
        q = pp(t, tf, 0.4, 1.3); place(c, card_box(880, 380, SOFT), 540, 880, q, -0.8)
        if q > 0.6:
            chart(c, t, tf + 0.1, 0.9, 170, 910, 740, 1000, GRN, False)
            place(c, label('ALREADY 4X FROM LOW', RED), 540, 1050, 1.1 * pp(t, tf + 0.9), 2)
    tp = at(i, 'thirty six', -0.3)
    if t > tp:
        q = pp(t, tp, 0.4, 1.3); place(c, card_box(880, 380, SOFT), 540, 1340, q, 0.6)
        if q > 0.6:
            d = ImageDraw.Draw(c); cx, cy, r = 540, 1440, 160
            for k in range(30):
                a0 = 180 + k * 6; cl = GRN if k < 10 else (YEL if k < 20 else RED)
                d.arc((cx - r, cy - r, cx + r, cy + r), a0, a0 + 6.5, fill=cl, width=40)
            v = SS.roll_number(t, tp + 0.2, 1.0, 0, 36.5); ang = math.radians(180 + 180 * min(v, 60) / 60)
            d.line((cx, cy, cx + (r - 30) * math.cos(ang), cy + (r - 30) * math.sin(ang)), fill=INK, width=12)
            d.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=INK)
            place(c, text_img(f'~{v:.0f}X YEARLY PROFIT', 'anton', 60, RED), 540, 1205)
            place(c, text_img('market cap ÷ last 4 quarters profit (my calc)', 'type', 24, GREY), 540, 1495)


def s7(c, t):
    i = 6; T0 = STARTS[i] + 0.05
    place_text(c, 'RED FLAGS', 'anton', 140, RED, 540, 290, t, 'rf', T0, 'pop')
    items = [('ONE BIG CONTRACT', 'CDMO jump = mostly one ₹825 Cr deal', 'one big contract'),
             ('PROMOTER STAKE 35.7%', 'was 38.2% in 2024', 'Promoter'),
             ('BORROWINGS 2X', '₹105 Cr to ₹208 Cr (Mar 2025 to Mar 2026)', 'Borrowings'),
             ('5% PRICE BAND', 'trade-for-trade: exits can get stuck', 'price band')]
    for k, (h, s, ph) in enumerate(items):
        tk = at(i, ph, -0.35)
        if t < tk: continue
        y = 520 + k * 270; q = pp(t, tk, 0.4, 1.3)
        place(c, card_box(900, 220, SOFT), 540, y, q, (-1, 1, -0.6, 0.8)[k])
        if q > 0.6:
            place(c, warn_icon(RED), 170, y, 1.4)
            c.alpha_composite(text_img(h, 'anton', 68, INK), (250, int(y - 70)))
            c.alpha_composite(text_img(s, 'osw', 38, GREY), (250, int(y + 18)))
    src(c, t, 'Screener.in (company filings) · NSE/INDmoney · 27 Oct 2026', STARTS[i] + 0.8, 1640)


def s8(c, t):
    i = 7; T0 = STARTS[i] + 0.05
    place(c, label('MULTIBAGGER?', GRN), 300, 300, 1.35 * pp(t, T0), -5) if t > T0 else None
    place(c, label('TRAP?', RED), 800, 300, 1.5 * pp(t, T0 + 0.15), 5) if t > T0 + 0.15 else None
    tn = at(i, 'Neither', -0.3)
    if t > tn:
        q = eo(prog(t, tn, 0.3)); d = ImageDraw.Draw(c)
        for x in (300, 800):
            d.line((x - 130 * q, 260, x + 130 * q, 340), fill=INK, width=10)
        s_, a = slam(t, tn + 0.3); place(c, stamp_c('NEITHER, YET', NAVY, 140, -5, 808), 540, 500, s_, 0, a)
    tr = at(i, 'turnaround', -0.3)
    if t > tr: place(c, label('TURNAROUND = REAL', GRN), 320, 680, 1.05 * pp(t, tr), -3)
    te = at(i, 'expects a lot', -0.3)
    if t > te: place(c, label('PRICE = ALREADY HIGH HOPES', ORG), 620, 770, 1.05 * pp(t, te), 2)
    tw = at(i, 'Watch three', -0.3)
    if t > tw: place_text(c, 'WATCH NEXT 2 QUARTERS', 'anton', 72, INK, 540, 900, t, 'w3', tw, 'pop')
    SS.checklist(c, t, [('CDMO REPEATS?', at(i, 'Does CDMO', 0.2)), ('MARGIN STAYS >15%?', at(i, 'Do margins', 0.2)),
                        ('PROMOTER STAKE STABLE?', at(i, 'Does promoter', 0.2))], y0=1060, gap=165)


def s9(c, t):
    i = 8; T0 = STARTS[i] + 0.05
    SS.cheat_sheet(c, t, T0, 'MOREPEN · Q2 FY27 CHEAT SHEET',
                   [('PROFIT', '+117% · ₹89 CR', GRN), ('CDMO', '₹58 TO ₹253 CR', GRN), ('VALUATION', '~36X PROFIT', RED), ('PROMOTER', '35.7% & FALLING', RED)], y0=170)
    ts = at(i, 'send it', -0.3)
    SS.send_frame(c, t, ts, 'the friend who holds Morepen', y=1080)
    tf = at(i, 'Follow', -0.2)
    if t > tf:
        q = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1300, 0.5 + 0.5 * eback(q), 0, clamp(q * 3))
    for k, ln in enumerate(['Sources: company release & NSE filings (27 Oct 2026), INDmoney prices,',
                            'Screener.in, HP High Court order (14 Oct 2026). Valuation = my calculation.',
                            'No buy/sell recommendation. Education only. Not investment advice.']):
        place_text(c, ln, 'type', 24, (210, 204, 192), 540, 1450 + k * 38, t, None, T0 + 0.3, 'fade', track=1)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]


def slam_times():
    return [at(0, 'profit more', -0.3), at(1, 'upper circuit', -0.1), at(3, 'two fifty three', 0.6), at(4, 'three hundred', -0.3),
            at(5, 'nobody', -0.4), at(7, 'Neither', 0.0)] + [STARTS[k] + 0.05 for k in range(1, 8)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('RESULTS CHECK', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
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
            r = random.Random(bi * 10 + layer + 5100)
            left = [(xl + r.uniform(-14, 14) - skew * (y / H), y) for y in range(0, H + 1, 40)]
            right = [(xl + SWd + r.uniform(-14, 14) - skew * (y / H), y) for y in range(H, -1, -40)]
            if layer == 0: left = [(x - 70, y) for x, y in left]; right = [(x + 70, y) for x, y in right]
            poly_fill(c, left + right, cols[bi % len(cols)][layer], 255, S=1)


def scene_at(t):
    k = 0
    for i, s in enumerate(STARTS):
        if t >= s: k = i
    return k


def render(t):
    LOOP = 0.6
    if t > DUR - LOOP:
        a = _render(t); b = _render(1.2, loop=True); q = eio((t - (DUR - LOOP)) / LOOP)
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
    header(c, dark, t if not loop else 0); transition(c, t)
    arr = np.asarray(c.convert('RGB')).astype(np.float32)
    g = grain_frames()[int(t * FPS) % 6]
    fl = 1 + 0.012 * math.sin(t * 37) * math.sin(t * 13)
    return np.clip(arr * fl + g[..., None], 0, 255).astype(np.uint8)
