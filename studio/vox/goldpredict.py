"""Can you predict India's gold rate? Comex x rupee formula. paper-collage style (female VO)"""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs, typed, drop, warn_icon
from fridge import follow_btn
import saveshare as SS
from antipo import clipping, qtag, sheet_cut, hand_chart, pp, src, PURPLE

SH = ROOT + 'goldpredict/'
SCRIPT = json.load(open(SH + 'script.json'))
DURS = json.load(open(SH + 'vo/durs.json'))
LEAD, TAIL = 0.15, 0.3
STARTS, VO = [], []
_t = 0.0
for i, d in enumerate(DURS):
    STARTS.append(_t); VO.append(_t + (0.1 if i == 0 else LEAD)); _t = VO[-1] + d + TAIL
DUR = _t + 1.8
B = STARTS[1:]
NAVY = (30, 60, 120); BLUE = (40, 100, 200); GREY = (120, 112, 104); TEAL = (20, 140, 130); ORG = (230, 120, 30)
GOLD = (214, 160, 40); GOLD2 = (245, 200, 80); SOFT = (252, 250, 244)

# MCX gold Dec-26 futures daily closes (INDmoney), 6 Nov .. 20 Nov 2026 (20 Nov = 2:53 PM)
CLOSES = [142357, 142520, 143160, 140623, 139755, 136200, 136750, 134550, 134243, 129866, 127499, 123539]
CLAB = ['6', '', '9', '', '', '12', '', '16', '', '18', '', '20']


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def inr(n):
    s = str(int(round(n))); last = s[-3:]; rest = s[:-3]; parts = []
    while len(rest) > 2: parts.insert(0, rest[-2:]); rest = rest[:-2]
    if rest: parts.insert(0, rest)
    return ','.join(parts + [last]) if parts else last


def card(w, h, col=SOFT, bcol=(252, 249, 242), border=8):
    return cutout(Image.new('RGBA', (w, h), col + (255,)), border=border, shadow=0.35, bcol=bcol)


@functools.lru_cache(None)
def bar_gold(w=150, h=70):
    im = Image.new('RGBA', (w + 40, h + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(20, h + 10), (w + 20, h + 10), (w, 20), (40, 20)], fill=GOLD, outline=INK)
    d.polygon([(40, 20), (w, 20), (w - 12, 8), (52, 8)], fill=GOLD2, outline=INK)
    d.line((60, 40, w - 30, 40), fill=(255, 235, 160), width=5)
    return im


def gold_stack(c, cx, cy, n=3, s=1.0):
    b = bar_gold()
    for k in range(n):
        place(c, b, cx + (k - (n - 1) / 2) * 130 * s, cy, s)
    if n > 1: place(c, b, cx, cy - 55 * s, s)


def clock(c, cx, cy, r, hh, mm, face, hand=INK, label=None, lcol=INK):
    d = ImageDraw.Draw(c)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=face, outline=INK, width=7)
    for k in range(12):
        a = k * math.pi / 6
        d.line((cx + math.sin(a) * r * 0.82, cy - math.cos(a) * r * 0.82, cx + math.sin(a) * r * 0.93, cy - math.cos(a) * r * 0.93), fill=hand, width=5)
    am = mm / 60 * 2 * math.pi; ah = (hh % 12 + mm / 60) / 12 * 2 * math.pi
    d.line((cx, cy, cx + math.sin(ah) * r * 0.5, cy - math.cos(ah) * r * 0.5), fill=hand, width=12)
    d.line((cx, cy, cx + math.sin(am) * r * 0.75, cy - math.cos(am) * r * 0.75), fill=hand, width=7)
    d.ellipse((cx - 12, cy - 12, cx + 12, cy + 12), fill=RED)
    if label: place(c, text_img(label, 'anton', 52, lcol), cx, cy + r + 50)


def moon(c, cx, cy, r, bg):
    d = ImageDraw.Draw(c)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(250, 236, 170))
    d.ellipse((cx - r + r * 0.55, cy - r - r * 0.1, cx + r + r * 0.55, cy + r - r * 0.1), fill=bg)


def sun(c, cx, cy, r, t):
    d = ImageDraw.Draw(c)
    for k in range(12):
        a = k * math.pi / 6 + t * 0.6
        d.line((cx + math.cos(a) * r * 1.25, cy + math.sin(a) * r * 1.25, cx + math.cos(a) * r * 1.6, cy + math.sin(a) * r * 1.6), fill=ORG, width=10)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=YEL, outline=INK, width=5)


@functools.lru_cache(None)
def tag(txt, col, size=60):
    t = text_img(txt, 'anton', size, CREAM)
    w, h = t.size[0] + 50, t.size[1] + 14
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), radius=16, fill=col)
    im.alpha_composite(t, (25, 7))
    return cutout(im, border=8, shadow=0.45)


# ---------------- scenes ----------------
def s1(c, t):
    i = 0
    words_line(c, t, [("MCX", INK, 0.1), ("GOLD", GOLD, 0.3)], 'anton', 120, 270, key='h1')
    place(c, sheet_cut(940, 600), 540, 690, 1.0, -0.6)
    f = clamp(prog(t, 0.4, 2.6))
    tip = hand_chart(c, t, 70, 390, 940, 600, CLOSES, CLAB, 120000, 146000, eo(f), col=INK, fill=GOLD2)
    place(c, text_img('NOV 2026 · Rs per 10 g (Dec futures)', 'osw5', 30, GREY), 540, 430)
    if tip and f > 0.02:
        k = min(len(CLOSES) - 1, int(eo(f) * (len(CLOSES) - 1) + 0.5))
        v = CLOSES[k]
        lab = text_img('₹' + inr(v), 'anton', 58, RED if k > 2 else INK)
        c.alpha_composite(lab, (int(min(tip[0] - lab.size[0] / 2, 1000 - lab.size[0])), int(tip[1] - 90)))
    tn = at(i, 'nineteen', -0.3)
    if t > tn:
        sc, a = slam(t, tn); place(c, stamp_c('-₹19,621 IN 9 DAYS', RED, 78, -5, 3), 540, 1110, sc, 0, a)
    tk = at(i, 'Could you', -0.2)
    if t > tk:
        place_text(c, 'could you know before your jeweller?', 'mark', 50, INK, 540, 1250, t, 'k1', tk, 'slide', rot=-2)
    tp = at(i, 'not prediction', -0.3)
    if t > tp:
        p = prog(t, tp, 0.32); place(c, qtag('PREDICT?', RED), 540, 1420, 0.55 + 0.45 * eback(p), 3, clamp(p * 3))
    src(c, t, 'MCX gold Dec futures closes · INDmoney · 20 Nov 2:53 PM', 0.8, 1660)


def s2(c, t):
    i = 1; T0 = STARTS[i]
    words_line(c, t, [("MADE IN", INK, T0 + 0.1), ("AMERICA", BLUE, T0 + 0.35)], 'anton', 130, 300, key='ma')
    ti = at(i, 'imports', -0.2)
    if t > ti:
        p = eo(prog(t, ti, 0.9))
        # ship carrying gold from left (US) to right (India)
        x = 200 + 640 * p; y = 700 + 10 * math.sin(t * 3)
        d = ImageDraw.Draw(c)
        d.polygon([(x - 150, y), (x + 150, y), (x + 110, y + 70), (x - 110, y + 70)], fill=NAVY, outline=INK)
        gold_stack(c, x, y - 40, 2, 0.8)
        place(c, tag('USA', BLUE, 54), 170, 560); place(c, tag('INDIA', ORG, 54), 900, 560)
        stroke(c, [(120, y + 90), (960, y + 90)], 6, (120, 160, 200))
    tm = at(i, 'not made here', -0.3)
    if t > tm:
        sc, a = slam(t, tm); place(c, stamp_c('IMPORTED', RED, 84, -7, 5), 540, 920, sc, 0, a)
    tc = at(i, 'Comex', -0.3)
    if t > tc:
        hp = round(prog(t, tc + 0.3, 0.5) * 20) / 20
        dy, a = drop(t, tc, 300)
        place(c, clipping(hp, 'COMEX GOLD', 'NEW YORK', 'PRICED IN US $ PER OUNCE'), 540, 1260 + dy, 0.95, -2, a)
    src(c, t, 'India price = global benchmark + rupee + duty', T0 + 1.0, 1660)


def s3(c, t):
    i = 2; T0 = STARTS[i]
    words_line(c, t, [("WHILE INDIA", INK, T0 + 0.1), ("SLEEPS", NAVY, T0 + 0.35)], 'anton', 120, 300, key='ws')
    d = ImageDraw.Draw(c)
    if t > T0 + 0.2:
        q = pp(t, T0 + 0.2, 0.4, 1.3)
        place(c, card(440, 520, (36, 44, 78)), 290, 720, q, -1.5)
        place(c, card(440, 520, (252, 236, 190)), 790, 720, pp(t, at(i, 'opens', -0.4), 0.4, 1.3), 1.5)
        if q > 0.6:
            moon(c, 380, 540, 46, (36, 44, 78))
            clock(c, 290, 740, 120, 22, 30, (60, 70, 110), CREAM)
            place(c, text_img('NIGHT IN INDIA', 'anton', 46, CREAM), 290, 900)
            place(c, text_img('COMEX TRADING', 'osw', 34, YEL), 290, 950)
    to = at(i, 'opens', -0.4)
    if t > to + 0.3:
        sun(c, 880, 540, 40, t)
        clock(c, 790, 740, 120, 9, 0, CREAM, INK)
        place(c, text_img('9:00 AM', 'anton', 46, INK), 790, 900)
        place(c, text_img('MCX OPENS', 'osw', 34, RED), 790, 950)
    ta = at(i, 'already done', -0.3)
    if t > ta:
        sc, a = slam(t, ta); place(c, stamp_c('MOVE ALREADY DONE', RED, 70, -5, 7), 540, 1130, sc, 0, a)
    tg = at(i, 'opens', 1.0)
    if t > tg:
        rows = [('18 NOV', 'prev close ₹1,34,243', 'opened ₹1,31,624', '-2.0%'), ('20 NOV', 'prev close ₹1,27,499', 'opened ₹1,23,629', '-3.0%')]
        for k, (dd, a_, b_, g) in enumerate(rows):
            tk = tg + 0.35 * k; q = pp(t, tk, 0.35, 1.3); y = 1300 + k * 150
            place(c, card(900, 130), 540, y, q, (-0.6, 0.6)[k])
            if q > 0.6:
                c.alpha_composite(text_img(dd, 'anton', 50, INK), (120, int(y - 32)))
                c.alpha_composite(text_img(a_, 'osw5', 30, GREY), (300, int(y - 40)))
                c.alpha_composite(text_img(b_, 'osw5', 30, INK), (300, int(y + 2)))
                gg = text_img('GAP ' + g, 'anton', 50, RED); c.alpha_composite(gg, (960 - gg.size[0], int(y - 32)))
    src(c, t, 'MCX gold Dec-26 futures, daily OHLC · INDmoney', T0 + 1.0, 1660)


def s4(c, t):
    i = 3; T0 = STARTS[i]
    words_line(c, t, [("THE", INK, T0 + 0.05), ("FORMULA", GOLD, T0 + 0.25)], 'anton', 140, 300, key='tf')
    q = pp(t, T0 + 0.3, 0.4, 1.3)
    place(c, SS._card(960, 900), 540, 900, q, -0.4)
    if q < 0.6: return
    steps = [('Comex', 'COMEX GOLD', '$ per ounce', BLUE, ''),
             ('multiply', 'x RUPEE RATE', 'Rs per $', ORG, ''),
             ('three point', '÷ 3.11', '1 ounce = 31.1 g, so 10 g = ÷ 3.11', INK, ''),
             ('fifteen', 'x 1.15', '15% import duty (since 13 May 2026)', RED, '')]
    for k, (ph, big, small, col, _) in enumerate(steps):
        tk = at(i, ph, -0.3)
        if t < tk: continue
        p = prog(t, tk, 0.3); y = 560 + k * 170
        place(c, text_img(big, 'anton', 92, col), 540 + (1 - eo(p)) * 300, y, 1.0, 0, clamp(p * 3))
        if p > 0.5: place(c, text_img(small, 'type', 30, GREY, 1), 540, y + 66)
    te = at(i, 'import duty', 0.5)
    if t > te:
        d = ImageDraw.Draw(c); d.line((140, 1250, 940, 1250), fill=INK, width=5)
        sc, a = slam(t, te); place(c, text_img('= Rs per 10 g (before 3% GST)', 'anton', 60, GRN), 540, 1310, sc, 0, a)


def s5(c, t):
    i = 4; T0 = STARTS[i]
    words_line(c, t, [("REAL", INK, T0 + 0.05), ("CHECK", GRN, T0 + 0.25), ("· 18 NOV", RED, T0 + 0.45)], 'anton', 110, 290, key='rc')
    rows = [('three thousand', 'Spot gold (9:07 AM)', '$3,797', BLUE),
            ('ninety three', 'Rupee (18 Nov close)', 'x 93.44', ORG),
            ('ninety three', 'Ounce to 10 g', '÷ 3.11035', INK),
            ('ninety three', 'Import duty 15%', 'x 1.15', RED)]
    for k, (ph, lab, val, col) in enumerate(rows):
        tk = at(i, ph, -0.3 + (0.0 if k < 2 else 0.6 + 0.4 * (k - 2)))
        if t < tk: continue
        y = 470 + k * 145; q = pp(t, tk, 0.35, 1.3)
        place(c, card(900, 125), 540, y, q, (-0.5, 0.5, -0.4, 0.4)[k])
        if q > 0.6:
            c.alpha_composite(text_img(lab, 'osw5', 38, GREY), (130, int(y - 26)))
            v = text_img(val, 'anton', 64, col); c.alpha_composite(v, (950 - v.size[0], int(y - 38)))
    tf = at(i, 'formula says', -0.2)
    if t > tf:
        v = 131178 * eo(prog(t, tf, 1.0))
        place(c, text_img('FORMULA ₹' + inr(v), 'anton', 84, INK), 540, 1100)
    tm = at(i, 'opened at', -0.2)
    if t > tm:
        sc, a = slam(t, tm); place(c, text_img('MCX OPEN ₹1,31,624', 'anton', 84, GRN), 540, 1220, sc, 0, a)
        tq = tm + 0.8
        if t > tq:
            sc2, a2 = slam(t, tq); place(c, stamp_c('0.3% APART', RED, 80, -6, 9), 540, 1390, sc2, 0, a2)
    src(c, t, 'Spot: Ascendants · Rupee: PTI · MCX: INDmoney', T0 + 1.0, 1660)


def s6(c, t):
    i = 5; T0 = STARTS[i]
    words_line(c, t, [("THIS", INK, T0 + 0.05), ("MORNING", RED, T0 + 0.25), ("· 20 NOV", INK, T0 + 0.45)], 'anton', 110, 290, key='tm')
    tf = at(i, 'fell overnight', -0.3)
    if t > tf:
        f = eo(prog(t, tf, 0.9)); d = ImageDraw.Draw(c)
        base = 900; x1, x2 = 330, 750
        h1 = 400; h2 = 290  # visual: exaggerated 3% drop
        d.rounded_rectangle((x1 - 110, base - h1, x1 + 110, base), 14, fill=(200, 190, 175), outline=INK, width=5)
        hh = int(h1 + (h2 - h1) * f)
        d.rounded_rectangle((x2 - 110, base - hh, x2 + 110, base), 14, fill=GOLD2, outline=INK, width=5)
        place(c, text_img('₹1,27,499', 'anton', 56, INK), x1, base - h1 - 40); place(c, text_img('19 NOV CLOSE', 'osw5', 32, GREY), x1, base + 36)
        place(c, text_img('₹1,23,629', 'anton', 56, RED), x2, base - hh - 40); place(c, text_img('20 NOV OPEN', 'osw5', 32, GREY), x2, base + 36)
        if f > 0.8: marker_line(c, [(x1 + 120, base - h1 + 30), (x2 - 120, base - hh + 10)], prog(t, tf + 0.8, 0.4), RED, 8, head=True)
    tx = at(i, 'three percent lower', -0.3)
    if t > tx:
        sc, a = slam(t, tx); place(c, stamp_c('-3.0% AT THE OPEN', RED, 70, -5, 11), 540, 1060, sc, 0, a)
    tj = at(i, 'jeweller', -0.3)
    if t > tj:
        place_text(c, 'jeweller = same base price', 'mark', 52, INK, 540, 1220, t, 'jw', tj, 'slide', rot=-2)
    tg = at(i, 'G S T', -0.3)
    if t > tg:
        place(c, tag('+3% GST', TEAL, 54), 330, 1370, pp(t, tg, 0.35, 1.3), -3)
        place(c, tag('+ MAKING CHARGES', ORG, 54), 700, 1370, pp(t, tg + 0.4, 0.35, 1.3), 3)
    src(c, t, 'MCX gold Dec-26 futures · INDmoney, 20 Nov 2026', T0 + 1.0, 1660)


def s7(c, t):
    i = 6; T0 = STARTS[i]
    if t > T0 + 0.1:
        p = prog(t, T0 + 0.1, 0.3); lw = text_w('NOT A PREDICTION', 'osw', 54, 2); x0 = 540 - (lw + 70) / 2
        place(c, warn_icon(YEL), x0 + 28, 262, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
        place(c, text_img('NOT A PREDICTION', 'osw', 54, YEL, 2), x0 + 70 + lw / 2, 260, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
    tn = at(i, 'next morning', -0.3)
    if t > tn:
        place(c, card(860, 150, (40, 38, 36), (120, 200, 140)), 540, 470, pp(t, tn, 0.35, 1.3), -1)
        if prog(t, tn, 0.35) > 0.6:
            c.alpha_composite(text_img('NEXT MORNING', 'anton', 64, CREAM), (150, 420))
            ok = text_img('YOU CAN SEE IT', 'anton', 50, (120, 200, 140)); c.alpha_composite(ok, (930 - ok.size[0], 430))
    tm = at(i, 'next month', -0.3)
    if t > tm:
        place(c, card(860, 150, (40, 38, 36), RED), 540, 660, pp(t, tm, 0.35, 1.3), 1)
        if prog(t, tm, 0.35) > 0.6:
            c.alpha_composite(text_img('NEXT MONTH', 'anton', 64, CREAM), (150, 610))
            no = text_img('NOBODY KNOWS', 'anton', 50, RED); c.alpha_composite(no, (930 - no.size[0], 620))
    tags = [('US FED', 'US Fed', BLUE, 290, 900, -5), ('THE DOLLAR', 'dollar', TEAL, 760, 920, 4), ('WARS', 'wars', RED, 300, 1090, 3), ('CENTRAL BANKS', 'central banks', GOLD, 740, 1100, -3)]
    for k, (txt, ph, col, x, y, r) in enumerate(tags):
        tk = at(i, ph, -0.3)
        if t > tk:
            jx, jy, jr = jit(('g', k), t, 2.0, 0.3)
            place(c, tag(txt, col, 64), x + jx, y + jy, pp(t, tk, 0.35, 1.4), r + jr)
    te = at(i, 'every night', -0.2)
    if t > te:
        place_text(c, 'they move Comex every night', 'mark', 48, YEL, 540, 1290, t, 'en', te, 'slide', rot=-2)


def s8(c, t):
    i = 7; T0 = STARTS[i]
    words_line(c, t, [("GOVT", INK, T0 + 0.05), ("SWITCH", RED, T0 + 0.25)], 'anton', 140, 300, key='gs')
    tm = at(i, 'In May', -0.3)
    if t > tm:
        dy, a = drop(t, tm, 300); hp = round(prog(t, tm + 0.4, 0.5) * 20) / 20
        place(c, clipping(hp, 'DUTY HIKED', 'CUSTOMS NOTIFICATION 16/2026', '13 MAY 2026 · GOLD & SILVER'), 540, 560 + dy, 0.95, -2, a)
    d = ImageDraw.Draw(c); base = 1250
    t6 = at(i, 'six', -0.3); t15 = at(i, 'fifteen', -0.3)
    for k, (lab, v, tk, col) in enumerate((('BEFORE', 6, t6, (200, 190, 175)), ('NOW', 15, t15, RED))):
        if t < tk: continue
        ph = eo(prog(t, tk, 0.7)); hg = max(14, int(v / 15 * 380 * ph)); x = 340 + k * 400
        d.rounded_rectangle((x - 110, base - hg, x + 110, base), 14, fill=col, outline=INK, width=5)
        place(c, text_img(f'{v * ph:.0f}%', 'anton', 80, INK), x, base - hg - 52)
        place(c, text_img(lab, 'osw5', 38, INK), x, base + 36)
    tx = t15 + 1.0
    if t > tx:
        sc, a = slam(t, tx); place(c, stamp_c('OVERNIGHT', RED, 80, 8, 13), 800, 820, sc, 0, a)
    src(c, t, 'Customs Notification 16/2026: BCD 10% + AIDC 5%', T0 + 1.0, 1660)


def s9(c, t):
    i = 8; T0 = STARTS[i]
    q = pp(t, T0, 0.45, 1.2)
    place(c, SS._card(960, 860), 540, 600, q, -0.4)
    if q > 0.6:
        place(c, text_img('GOLD RATE · CHEAT SHEET', 'anton', 54, INK), 540, 230)
        d = ImageDraw.Draw(c); d.line((90, 272, 990, 272), fill=INK, width=4)
        rows = [('Starts at', 'Comex, US $ / oz', BLUE), ('x Rupee', 'Rs per US $', ORG), ('÷ 3.11', 'ounce to 10 grams', INK),
                ('x 1.15', '15% import duty', RED), ('+ 3% GST', 'when you buy', TEAL), ('+ making', 'jewellery only', GREY),
                ('Know early', 'check Comex before 9 AM', GRN), ('Predict?', 'nobody can', RED)]
        for k, (a_, b_, col) in enumerate(rows):
            tk = T0 + 0.3 + 0.08 * k
            if t < tk: continue
            y = 300 + k * 78
            c.alpha_composite(text_img(a_, 'anton', 42, col), (100, y - 2))
            v = text_img(b_, 'osw5', 38, INK); c.alpha_composite(v, (980 - v.size[0], y))
        SS.save_pulse(c, t, T0 + 1.2, 540, 1080, 'SAVE THIS')
    tf = at(i, 'follow', -0.2)
    if t > tf:
        q2 = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1300, 0.5 + 0.5 * eback(q2), 0, clamp(q2 * 3))
    for k, ln in enumerate(['Sources: INDmoney (MCX), PTI, Ascendants, Customs Notification 16/2026',
                            'Formula is an approximation; dealer premium/discount varies',
                            'Not a buy/sell call. Education only.']):
        place_text(c, ln, 'type', 22, GREY, 540, 1620 + k * 34, t, None, T0 + 0.3, 'fade', track=1)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
DARK_SCENES = {6}


def slam_times():
    return [at(0, 'nineteen', -0.3), at(1, 'not made here', -0.3), at(2, 'already done', -0.3), at(4, 'opened at', -0.2),
            at(5, 'three percent lower', -0.3), at(7, 'fifteen', 0.7)] + [STARTS[k] + 0.05 for k in range(1, 8)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('CAN YOU PREDICT GOLD?', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
    ImageDraw.Draw(c).line((60, 118, W - 60, 118), fill=col, width=2)
    ImageDraw.Draw(c).line((60, 118, 60 + (W - 120) * clamp(t / DUR), 118), fill=RED if not dark else YEL, width=8)


def transition(c, t):
    cols = [(GOLD, INK), (YEL, INK), (INK, GOLD), (TEAL, YEL), (YEL, RED), (INK, YEL), (RED, YEL), (GOLD, INK)]
    for bi, b in enumerate(B):
        d = 0.62
        if abs(t - b) > d / 2 + 0.12: continue
        for layer, delay in ((0, -0.07), (1, 0.0)):
            p = (t - (b - d / 2) - delay) / d
            if p <= 0 or p >= 1: continue
            p = eio(p); SWd, skew = 2050, 320
            xl = (W + 60) + p * (-(SWd + skew) - (W + 60) - 40)
            r = random.Random(bi * 10 + layer + 777)
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
    header(c, dark, t if not loop else 0); transition(c, t)
    arr = np.asarray(c.convert('RGB')).astype(np.float32)
    g = grain_frames()[int(t * FPS) % 6]
    fl = 1 + 0.012 * math.sin(t * 37) * math.sin(t * 13)
    return np.clip(arr * fl + g[..., None], 0, 255).astype(np.uint8)
