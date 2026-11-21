"""Anthropic (ANT) listed on Nasdaq: what happened on day 1 & 2. paper-collage style (male VO)"""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs, typed, drop, warn_icon, receipt
from fridge import follow_btn
import saveshare as SS
import defence as DF

SH = ROOT + _os.environ.get('LDIR', 'antday1') + '/'
SCRIPT = json.load(open(SH + 'script.json'))
DURS = json.load(open(SH + 'vo/durs.json'))
LEAD, TAIL = 0.15, 0.3
STARTS, VO = [], []
_t = 0.0
for i, d in enumerate(DURS):
    STARTS.append(_t); VO.append(_t + (0.1 if i == 0 else LEAD)); _t = VO[-1] + d + TAIL
DUR = _t + 1.8
B = STARTS[1:]
NAVY = (30, 60, 120); BLUE = (40, 100, 200); GREY = (120, 112, 104); TEAL = (20, 140, 130); ORG = (230, 120, 30); GOLD = (214, 160, 40)
SOFT = (252, 250, 244)


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def src(c, t, txt, t0, y=1720, col=GREY):
    if t > t0: place_text(c, txt, 'type', 24, col, 540, y, t, None, t0, 'fade', track=1)


# ---------------- assets ----------------
@functools.lru_cache(16)
def clipping(hp, head='ANTHROPIC IPO', top='THE MARKET PAGE', sub='NASDAQ: ANT · 19 NOV 2026'):
    w, h = 880, 360
    im = torn_rect(w, h, (234, 228, 212), seed=7, jag=12)
    d = ImageDraw.Draw(im)
    mt = text_img(top, 'pf', 30, INK, 3); im.alpha_composite(mt, (w // 2 - mt.size[0] // 2, 14))
    d.line((40, 66, w - 40, 66), fill=INK, width=3); d.line((40, 72, w - 40, 72), fill=INK, width=1)
    st = text_img(sub, 'type', 22, (90, 85, 80), 2); im.alpha_composite(st, (w // 2 - st.size[0] // 2, 78))
    hl = text_img(head, 'pf', 104 if len(head) < 14 else 84, INK)
    hx, hy = w // 2 - hl.size[0] // 2, 112
    if hp > 0: highlight(im, hx + 14, hy + 46, hx + hl.size[0] - 14, hy + hl.size[1] - 6, hp, seed=11, alpha=225)
    im.alpha_composite(hl, (hx, hy))
    r = random.Random(4)
    for col in range(3):
        x0 = 44 + col * 270
        for k in range(4):
            y = 272 + k * 18; ln = r.uniform(170, 240) if k < 3 else r.uniform(80, 150)
            d.line((x0, y, x0 + ln, y), fill=(160, 152, 140), width=7)
    return cutout(im, border=0, shadow=0.36, blur=10, off=(8, 14))


@functools.lru_cache(None)
def qtag(txt, col):
    t = text_img(txt, 'anton', 84, CREAM)
    w, h = t.size[0] + 60, t.size[1] + 16
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), radius=20, fill=col)
    im.alpha_composite(t, (30, 8))
    return cutout(im, border=10, shadow=0.5)


@functools.lru_cache(None)
def ticket(state, line2):
    w, h = 820, 170
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 18, fill=(254, 252, 246))
    for y in range(10, h - 10, 18): d.ellipse((150 - 5, y, 150 + 5, y + 10), fill=(225, 218, 204))
    ic = text_img('STEP', 'type', 22, GREY, 2); im.alpha_composite(ic, (75 - ic.size[0] // 2, 30))
    d.rectangle((40, 90, 110, 140), fill=INK); d.polygon([(40, 90), (63, 70), (63, 90), (86, 70), (86, 90), (110, 70), (110, 90)], fill=INK)
    d.rectangle((92, 50, 104, 80), fill=INK)
    a = text_img(state, 'anton', 70, INK); im.alpha_composite(a, (185, 20))
    b = text_img(line2, 'type', 26, GREY, 1); im.alpha_composite(b, (190, 112))
    return cutout(im, border=10, shadow=0.4)


def turbine(c, cx, cy, s, t, col=INK, rpm=1.6):
    d = ImageDraw.Draw(c)
    d.polygon([(cx - 10 * s, cy + 300 * s), (cx + 10 * s, cy + 300 * s), (cx + 4 * s, cy), (cx - 4 * s, cy)], fill=col)
    a0 = t * rpm * 2 * math.pi
    for k in range(3):
        a = a0 + k * 2 * math.pi / 3
        tip = (cx + math.cos(a) * 170 * s, cy + math.sin(a) * 170 * s)
        side = (cx + math.cos(a + 0.12) * 60 * s, cy + math.sin(a + 0.12) * 60 * s)
        side2 = (cx + math.cos(a - 0.05) * 50 * s, cy + math.sin(a - 0.05) * 50 * s)
        d.polygon([(cx, cy), side, tip, side2], fill=col)
    d.ellipse((cx - 14 * s, cy - 14 * s, cx + 14 * s, cy + 14 * s), fill=RED, outline=col, width=max(2, int(4 * s)))


# grid sheet chart
def grid_sheet(w, h):
    im = Image.new('RGBA', (w, h), (252, 250, 244, 255)); d = ImageDraw.Draw(im)
    for x in range(0, w, 30): d.line((x, 0, x, h), fill=(205, 218, 228), width=1)
    for y in range(0, h, 30): d.line((0, y, w, y), fill=(205, 218, 228), width=1)
    return im


@functools.lru_cache(4)
def sheet_cut(w, h): return cutout(grid_sheet(w, h), border=0, shadow=0.3)


def hand_chart(c, t, ox, oy, w, h, vals, labels, vmin, vmax, f, col=INK, fill=YEL):
    """f in 0..1 reveal; returns tip point"""
    n = len(vals)
    def P(i, v): return (ox + 90 + (w - 160) * i / (n - 1), oy + h - 70 - (v - vmin) / (vmax - vmin) * (h - 140))
    d = ImageDraw.Draw(c)
    d.line((ox + 80, oy + h - 70, ox + w - 50, oy + h - 70), fill=INK, width=4)
    for i, lb in enumerate(labels):
        if lb:
            li = text_img(lb, 'type', 24, (90, 85, 80), 1); x, _ = P(i, vmin); c.alpha_composite(li, (int(x - li.size[0] / 2), int(oy + h - 58)))
    pts = []
    for k in range(int(f * (n - 1) * 20) + 1):
        u = k / 20; i = min(int(u), n - 2); s = u - i
        v = vals[i] + (vals[i + 1] - vals[i]) * (s * s * (3 - 2 * s)) + math.sin(k * 1.7) * (vmax - vmin) * 0.006
        pts.append(P(i + s, v))
    if len(pts) > 1:
        poly_fill(c, pts + [(pts[-1][0], oy + h - 70), (pts[0][0], oy + h - 70)], fill, 140)
        stroke(c, pts, 9, col)
        tx, ty = pts[-1]; d.ellipse((tx - 13, ty - 13, tx + 13, ty + 13), fill=RED, outline=INK, width=4)
        return pts[-1]
    return None


PURPLE = (92, 60, 170)


def rocket(c, cx, cy, s=1.0, t=0, flame=True):
    d = ImageDraw.Draw(c)
    w, h = 90 * s, 260 * s
    d.polygon([(cx, cy - h / 2 - 70 * s), (cx + w / 2, cy - h / 2), (cx - w / 2, cy - h / 2)], fill=RED, outline=INK)
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), int(20 * s), fill=CREAM, outline=INK, width=max(2, int(5 * s)))
    d.ellipse((cx - 26 * s, cy - h / 2 + 40 * s, cx + 26 * s, cy - h / 2 + 92 * s), fill=BLUE, outline=INK, width=max(2, int(5 * s)))
    for sgn in (-1, 1):
        d.polygon([(cx + sgn * w / 2, cy + h / 2 - 70 * s), (cx + sgn * (w / 2 + 50 * s), cy + h / 2 + 10 * s), (cx + sgn * w / 2, cy + h / 2)], fill=RED, outline=INK)
    if flame:
        fl = 70 * s * (1 + 0.25 * math.sin(t * 22))
        d.polygon([(cx - 30 * s, cy + h / 2), (cx, cy + h / 2 + fl), (cx + 30 * s, cy + h / 2)], fill=ORG)
        d.polygon([(cx - 14 * s, cy + h / 2), (cx, cy + h / 2 + fl * 0.6), (cx + 14 * s, cy + h / 2)], fill=YEL)


def bubble(c, cx, cy, r, t=0):
    lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(180, 220, 255, 70), outline=(80, 140, 210, 220), width=8)
    d.arc((cx - r * 0.7, cy - r * 0.7, cx + r * 0.3, cy + r * 0.3), 200, 260, fill=(255, 255, 255, 230), width=14)
    c.alpha_composite(lay)


@functools.lru_cache(None)
def step_ticket(num, title, line2, col):
    w, h = 900, 150
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 18, fill=(254, 252, 246))
    for y in range(10, h - 10, 18): d.ellipse((140 - 5, y, 140 + 5, y + 10), fill=(225, 218, 204))
    d.ellipse((30, 30, 110, 110), fill=col, outline=INK, width=4)
    nn = text_img(num, 'anton', 56, CREAM); im.alpha_composite(nn, (70 - nn.size[0] // 2, 70 - nn.size[1] // 2))
    a = text_img(title, 'anton', 60, INK); im.alpha_composite(a, (175, 14))
    b = text_img(line2, 'type', 26, GREY, 1); im.alpha_composite(b, (180, 96))
    return cutout(im, border=10, shadow=0.4)



# ---------------- data (INDmoney daily OHLC, 19-20 Nov 2026; IPO price: SEC filing via TechCrunch/AP) ----------------
IPO = 83.0
D1 = dict(o=111.50, h=115.10, l=92.72, c=97.17)
D2 = dict(o=89.86, h=92.56, l=83.05, c=88.91)
PMIN, PMAX = 76.0, 120.0
CY0, CY1 = 1260, 470   # y of PMIN, PMAX


def py(v): return CY0 + (v - PMIN) / (PMAX - PMIN) * (CY1 - CY0)


def axis(c, t, t0):
    d = ImageDraw.Draw(c)
    if t < t0: return
    f = eo(prog(t, t0, 0.5))
    sheet = sheet_cut(900, 900); place(c, sheet, 540, 870, 0.4 + 0.6 * f, -0.6, clamp(f * 2))
    if f < 0.9: return
    for v in (80, 90, 100, 110, 120):
        y = py(v); d.line((150, y, 930, y), fill=(200, 196, 186), width=2)
        li = text_img(f'${v}', 'type', 24, GREY, 1); c.alpha_composite(li, (100, int(y - 14)))
    # dashed IPO line
    y = py(IPO); x = 150
    while x < 930: d.line((x, y, min(930, x + 26), y), fill=PURPLE, width=6); x += 44
    lb = text_img('IPO PRICE $83', 'anton', 34, PURPLE); c.alpha_composite(lb, (930 - lb.size[0], int(y + 10)))


def candle(c, cx, k, f, lab, up=None):
    """draw daily candle k (dict), f = reveal 0..1"""
    d = ImageDraw.Draw(c)
    if f <= 0: return
    col = GRN if k['c'] >= IPO else RED
    o, cl = k['o'], k['o'] + (k['c'] - k['o']) * f
    hi = k['o'] + (k['h'] - k['o']) * min(1, f * 2)
    lo = k['o'] + (k['l'] - k['o']) * f
    d.line((cx, py(hi), cx, py(lo)), fill=INK, width=8)
    top, bot = sorted((py(o), py(cl)))
    d.rectangle((cx - 70, top, cx + 70, max(bot, top + 8)), fill=RED if cl < o else GRN, outline=INK, width=5)
    li = text_img(lab, 'osw5', 34, INK); c.alpha_composite(li, (int(cx - li.size[0] / 2), CY0 + 18))


def tagv(c, txt, col, x, y, t, t0, key):
    if t > t0: place_text(c, txt, 'anton', 46, col, x, y, t, key, t0, 'pop')


def s1(c, t):
    i = 0
    # frame 0: big falling price counter
    v = 115.10 - (115.10 - 88.91) * eo(prog(t, 0.0, 1.6))
    sc = 1.0 + 0.06 * math.sin(t * 6)
    place(c, text_img(f'${v:.2f}', 'anton', 240, RED), 540, 560, sc, -2)
    place_text(c, 'ANT · Nasdaq · high to latest close', 'type', 30, GREY, 540, 705, t, 'pc', 0.3, 'fade', track=1)
    words_line(c, t, [("NOBODY", INK, 0.2), ("TELLS", INK, 0.4), ("YOU", RED, 0.6)], 'anton', 120, 300, key='nt')
    dy, a = drop(t, 0.5, 360)
    if a > 0:
        hp = round(prog(t, 1.1, 0.5) * 20) / 20
        jx, jy, jr = jit('clip', t, 2, 0.5)
        place(c, clipping(hp, 'ANTHROPIC · DAY 1', 'THE MARKET PAGE', 'NASDAQ: ANT · 19–20 NOV 2026'), 540 + jx, 950 + dy + jy, 0.9, -3 + jr + (1 - a) * 8, a)
    to = at(i, 'Opening buyers', -0.25)
    if t > to:
        sc2, a2 = slam(t, to); place(c, qtag('OPENING BUYERS: DOWN', RED), 540, 1220, sc2 * 0.8, -3, a2)
    tw = at(i, "Who's up", -0.2)
    if t > tw:
        p = prog(t, tw, 0.32); place(c, qtag("WHO'S UP?", GRN), 540, 1400, 0.6 + 0.4 * eback(p), 3, clamp(p * 3))
        marker_ellipse(c, 540, 1400, 250, 90, prog(t, tw + 0.35, 0.5), INK, 8, seed=5)
    place_text(c, 'Made with Claude, an Anthropic AI · conflict of interest · check every number', 'type', 22, GREY, 540, 1560, t, None, 0.6, 'fade', track=1)


def s2(c, t):
    i = 1; T0 = STARTS[i]
    if t > T0 + 0.05:
        p = prog(t, T0 + 0.05, 0.3); lw = text_w('DISCLOSURE', 'anton', 120); x0 = 540 - (lw + 110) / 2
        place(c, warn_icon(YEL), x0 + 40, 330, 0.8 + 0.4 * eback(p), 0, clamp(p * 3))
        place(c, text_img('DISCLOSURE', 'anton', 120, INK), x0 + 110 + lw / 2, 330, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
    rows = [('MADE WITH CLAUDE', 'an AI built by Anthropic', "I'm made", PURPLE),
            ('CONFLICT OF INTEREST', 'this reel is about Anthropic', 'conflict', RED),
            ('CHECK EVERY NUMBER', 'sources on every screen + caption', 'check every', GRN)]
    for k, (h1, h2, ph, col) in enumerate(rows):
        tk = at(i, ph, -0.3)
        if t < tk: continue
        y = 620 + k * 260; q = pp(t, tk, 0.35, 1.3)
        jx, jy, jr = jit(('d', k), t, 1.2, 0.2)
        place(c, cutout(Image.new('RGBA', (900, 200), SOFT + (255,)), border=6, shadow=0.35, bcol=col), 540 + jx, y + jy, q, (-0.8, 0.8, -0.6)[k] + jr)
        if q > 0.6:
            c.alpha_composite(text_img(h1, 'anton', 70, col), (130, int(y - 66)))
            c.alpha_composite(text_img(h2, 'type', 30, GREY, 1), (134, int(y + 26)))
    ts = at(i, 'yourself', -0.2)
    if t > ts:
        sc, a = slam(t, ts); place(c, stamp_c('VERIFY', RED, 100, -10, 61), 820, 1420, sc, 0, a)


def s3(c, t):
    i = 2; T0 = STARTS[i]
    words_line(c, t, [("IPO", INK, T0 + 0.1), ("PRICE", PURPLE, T0 + 0.3)], 'anton', 130, 290, key='ip')
    # old band, crossed
    if t > T0 + 0.2:
        place(c, text_img('BAND $70 – $78', 'anton', 70, GREY), 540, 440, 1, -2)
        tx = at(i, 'above its range', -0.2)
        if t > tx:
            f = eo(prog(t, tx, 0.4)); d = ImageDraw.Draw(c); d.line((250, 450, 250 + 580 * f, 430), fill=RED, width=12)
    tp = at(i, 'eighty three', -0.3)
    if t > tp:
        sc, a = slam(t, tp); place(c, text_img('$83', 'anton', 260, GRN), 540, 640, sc, 0, a)
        place_text(c, 'final IPO price · set 18 Nov 2026', 'mark', 46, INK, 540, 790, t, 'fp', tp + 0.4, 'slide', rot=-3)
    ts = at(i, 'Nine hundred', -0.3)
    if t > ts:
        q = pp(t, ts, 0.35, 1.3)
        place(c, cutout(Image.new('RGBA', (900, 300), (40, 38, 36, 255)), border=6, shadow=0.4, bcol=GRN), 540, 1030, q, -1)
        if q > 0.6:
            c.alpha_composite(text_img('980 MILLION SHARES', 'anton', 64, CREAM), (130, 905))
            rv = 81.3 * eo(prog(t, at(i, 'raised', -0.2), 1.2)) if t > at(i, 'raised', -0.2) else 0
            c.alpha_composite(text_img(f'${rv:.1f} BILLION RAISED', 'anton', 80, YEL), (130, 1000))
    tb = at(i, 'biggest', -0.2)
    if t > tb:
        sc, a = slam(t, tb); place(c, stamp_c('BIGGEST IPO ON RECORD', RED, 70, -6, 71), 540, 1290, sc, 0, a)
    src(c, t, 'IPO price & size: SEC filing via TechCrunch, AP, Forbes (18–19 Nov 2026)', T0 + 1.0, 1450)


def s4(c, t):
    i = 3; T0 = STARTS[i]
    words_line(c, t, [("DAY 1", INK, T0 + 0.1), ("· 19 NOV", RED, 0.3 + T0)], 'anton', 120, 290, key='d1')
    axis(c, t, T0 + 0.1)
    to = at(i, 'It opened', -0.2)
    if t > to:
        f = 0.001 + 0.0
        # open tick + jump to high
        d = ImageDraw.Draw(c); yo = py(D1['o'])
        fo = eo(prog(t, to, 0.5)); y = py(IPO) + (yo - py(IPO)) * fo
        d.line((360, y, 500, y), fill=INK, width=10)
        rocket(c, 260, y + 40 - 30 * math.sin(t * 3), 0.45, t)
        if fo > 0.9:
            tagv(c, 'OPEN $111.50', INK, 720, yo + 45, t, to + 0.5, 'op')
            sc, a = slam(t, to + 0.5); place(c, stamp_c('+34% vs IPO', GRN, 90, -8, 81), 640, 900, sc, 0, a)
    th = at(i, 'touched', -0.2)
    if t > th:
        d = ImageDraw.Draw(c); fh = eo(prog(t, th, 0.5))
        d.line((430, py(D1['o']), 430, py(D1['o']) + (py(D1['h']) - py(D1['o'])) * fh), fill=INK, width=8)
        if fh > 0.9: tagv(c, 'HIGH $115.10', GRN, 720, py(D1['h']) - 45, t, th + 0.4, 'hi')
    src(c, t, 'Open/high: INDmoney daily OHLC, Forbes (19 Nov 2026)', T0 + 1.0, 1450)


def s5(c, t):
    i = 4; T0 = STARTS[i]
    words_line(c, t, [("DAY 1", INK, T0 + 0.05), ("CLOSE", GRN, T0 + 0.25)], 'anton', 120, 290, key='d1c')
    axis(c, t, T0 - 1)
    f = eo(prog(t, at(i, 'slid', -0.3), 1.6))
    candle(c, 430, D1, f, '19 NOV')
    tc = at(i, 'ninety seven', -0.3)
    if t > tc:
        tagv(c, 'CLOSE $97.17', INK, 740, py(D1['c']), t, tc, 'cl')
        tagv(c, 'LOW $92.72', GREY, 740, py(D1['l']) + 50, t, tc + 0.3, 'lo')
    tu = at(i, 'still up', -0.2)
    if t > tu:
        sc, a = slam(t, tu); place(c, stamp_c('+17.1% vs IPO', GRN, 76, -6, 91), 790, 560, sc, 0, a)
    tv = at(i, 'Value', -0.2)
    if t > tv:
        v = 1.76 * eo(prog(t, tv, 1.0))
        q = pp(t, tv, 0.35, 1.3)
        place(c, cutout(Image.new('RGBA', (900, 150), (40, 38, 36, 255)), border=6, shadow=0.4, bcol=PURPLE), 540, 1370, q, -1)
        if q > 0.6:
            place(c, text_img(f'VALUE ~${v:.2f} TRILLION', 'anton', 70, CREAM), 540, 1370)
    src(c, t, 'Close: INDmoney, Forbes · value at close: CNN (19 Nov 2026)', T0 + 1.0, 1490)


def s6(c, t):
    i = 5; T0 = STARTS[i]
    words_line(c, t, [("DAY 2", INK, T0 + 0.05), ("· 20 NOV", RED, T0 + 0.25)], 'anton', 120, 290, key='d2')
    axis(c, t, T0 - 1)
    candle(c, 330, D1, 1, '19 NOV')
    f = eo(prog(t, at(i, 'it fell', -0.3), 1.6))
    candle(c, 640, D2, f, '20 NOV')
    tf = at(i, 'eight and a half', -0.3)
    if t > tf:
        sc, a = slam(t, tf); place(c, stamp_c('-8.5%', RED, 110, 8, 101), 840, 560, sc, 0, a)
        tagv(c, '$88.91', INK, 840, py(D2['c']) - 70, t, tf + 0.6, 'c2')
    tl = at(i, 'Its low', -0.2)
    if t > tl:
        tagv(c, 'LOW $83.05', RED, 840, py(D2['l']) - 50, t, tl, 'l2')
        marker_ellipse(c, 640, py(D2['l']), 120, 50, prog(t, tl + 0.3, 0.5), RED, 8, seed=9)
    t5 = at(i, 'five cents', -0.2)
    if t > t5:
        sc, a = slam(t, t5); place(c, stamp_c('5 CENTS ABOVE IPO PRICE', RED, 60, -4, 111), 540, 1420, sc, 0, a)
    src(c, t, 'INDmoney daily OHLC, 20 Nov 2026 (latest close)', T0 + 1.0, 1545)


def s7(c, t):
    i = 6; T0 = STARTS[i]
    words_line(c, t, [("THE", INK, T0 + 0.05), ("RISKS", RED, T0 + 0.25)], 'anton', 130, 290, key='rk')
    d = ImageDraw.Draw(c); base = 900
    tr = at(i, 'revenue', -0.3); tn = at(i, 'Net loss', -0.3)
    for k, (lab, v, tk, col) in enumerate((('REVENUE', 16.3, tr, GRN), ('NET LOSS', 80.7, tn, RED))):
        if t < tk: continue
        ph = eo(prog(t, tk, 0.8)); hg = max(14, int(v / 80.7 * 420 * ph)); x = 330 + k * 420
        d.rounded_rectangle((x - 110, base - hg, x + 110, base), 14, fill=col, outline=INK, width=5)
        place(c, text_img(f'${v * ph:.1f}B', 'anton', 64, INK), x, base - hg - 44)
        place(c, text_img(lab, 'osw5', 38, INK), x, base + 36)
    place_text(c, 'first half of 2026', 'mark', 44, INK, 540, 1000, t, 'h1', tr + 0.3, 'slide', rot=-2) if t > tr + 0.3 else None
    tp = at(i, 'mostly on paper', -0.2)
    if t > tp:
        place_text(c, '~$72.4B of the loss is non-cash', 'type', 30, GREY, 540, 1060, t, 'nc', tp, 'fade', track=1)
    tv = at(i, 'founders', -0.3)
    if t > tv:
        f = eo(prog(t, tv, 1.0)); cx, cy, r = 300, 1280, 120
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(220, 214, 200), outline=INK, width=5)
        d.pieslice((cx - r, cy - r, cx + r, cy + r), -90, -90 + 360 * 0.501 * f, fill=PURPLE, outline=INK, width=5)
        if f > 0.7:
            c.alpha_composite(text_img('50.1% OF VOTES', 'anton', 64, PURPLE), (460, 1210))
            c.alpha_composite(text_img('kept by 7 co-founders', 'type', 30, GREY, 1), (464, 1295))
    src(c, t, 'Anthropic S-1 & amendments (Oct–Nov 2026)', T0 + 1.0, 1490)


def s8(c, t):
    i = 7; T0 = STARTS[i]
    if t > T0 + 0.1:
        p = prog(t, T0 + 0.1, 0.3); lw = text_w("SO WHO'S UP?", 'osw', 54, 2); x0 = 540 - (lw + 70) / 2
        place(c, warn_icon(YEL), x0 + 28, 262, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
        place(c, text_img("SO WHO'S UP?", 'osw', 54, YEL, 2), x0 + 70 + lw / 2, 260, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
    rows = [('BOUGHT AT THE OPEN', '$111.50, now $88.91', 'Buyers at the open', '-20.3%', RED),
            ('BOUGHT AT IPO PRICE', '$83, now $88.91', 'IPO buyers', '+7.1%', GRN)]
    for k, (h1, h2, ph, pc, col) in enumerate(rows):
        tk = at(i, ph, -0.3)
        if t < tk: continue
        y = 520 + k * 300; q = pp(t, tk, 0.35, 1.3)
        jx, jy, jr = jit(('v', k), t, 1.2, 0.2)
        place(c, cutout(Image.new('RGBA', (920, 240), (40, 38, 36, 255)), border=6, shadow=0.4, bcol=col), 540 + jx, y + jy, q, (-0.8, 0.8)[k] + jr)
        if q < 0.6: continue
        c.alpha_composite(text_img(h1, 'anton', 52, CREAM), (120, int(y - 90)))
        c.alpha_composite(text_img(h2, 'type', 30, (200, 194, 182), 1), (124, int(y - 20)))
        pv = text_img(pc, 'anton', 110, col); c.alpha_composite(pv, (960 - pv.size[0], int(y - 30)))
    tw = at(i, 'Where you got in', -0.2)
    if t > tw:
        sc, a = slam(t, tw); place(c, stamp_c('ENTRY PRICE > HYPE', YEL, 76, -5, 121), 540, 1180, sc, 0, a)
    place_text(c, 'Latest close 20 Nov 2026 (INDmoney). Past moves, not a prediction.', 'type', 24, (200, 194, 182), 540, 1400, t, None, T0 + 1.0, 'fade', track=1)


def s9(c, t):
    i = 8; T0 = STARTS[i]
    q = pp(t, T0, 0.45, 1.2)
    place(c, SS._card(960, 820), 540, 590, q, -0.4)
    if q > 0.6:
        place(c, text_img('ANTHROPIC (ANT) · CHEAT SHEET', 'anton', 50, INK), 540, 230)
        d = ImageDraw.Draw(c); d.line((90, 272, 990, 272), fill=INK, width=4)
        rows = [('IPO price (band $70–78)', '$83', PURPLE), ('Raised', '$81.3B · 980M shares', INK), ('Day 1 open / high', '$111.50 / $115.10', GRN),
                ('Day 1 close', '$97.17 (+17.1%)', GRN), ('Day 2 close (20 Nov)', '$88.91 (+7.1%)', INK), ('Day 2 low', '$83.05', RED),
                ('H1 2026 rev / loss', '$16.3B / $80.7B', RED), ('Founder votes', '50.1%', NAVY)]
        for k, (a_, b_, col) in enumerate(rows):
            tk = T0 + 0.3 + 0.08 * k
            if t < tk: continue
            y = 300 + k * 76
            c.alpha_composite(text_img(a_, 'osw5', 36, INK), (100, y))
            v = text_img(b_, 'anton', 42, col); c.alpha_composite(v, (980 - v.size[0], y - 2))
    SS.send_frame(c, t, T0 + 0.2, 'the opening-bell buyer', y=1150)
    ts = at(i, 'Save it', -0.2)
    if t > ts: SS.save_pulse(c, t, ts, 540, 1340, 'SAVE THIS')
    tf = at(i, 'follow', -0.2)
    if t > tf:
        q2 = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1465, 0.5 + 0.5 * eback(q2), 0, clamp(q2 * 3))
    for k, ln in enumerate(['Made with Claude (an Anthropic AI): conflict of interest. Check every number.',
                            'Sources: INDmoney, SEC filing via TechCrunch/AP, Forbes, CNN, Anthropic S-1',
                            'Not a buy/sell call. Education only.']):
        place_text(c, ln, 'type', 22, GREY, 540, 1585 + k * 34, t, None, T0 + 0.3, 'fade', track=1)


def pp(t, t0, d=0.35, s=1.6): return eback(prog(t, t0, d), s)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
DARK_SCENES = {7}


def slam_times():
    return [at(0, 'Opening buyers', -0.25), at(2, 'eighty three', -0.3), at(2, 'biggest', -0.2), at(3, 'It opened', 0.3), at(5, 'eight and a half', -0.3), at(5, 'five cents', -0.2), at(7, 'Where you got in', -0.2)] + [STARTS[k] + 0.05 for k in range(1, 8)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('ANTHROPIC LISTED · DAY 1 & 2', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
    ImageDraw.Draw(c).line((60, 118, W - 60, 118), fill=col, width=2)
    ImageDraw.Draw(c).line((60, 118, 60 + (W - 120) * clamp(t / DUR), 118), fill=RED if not dark else YEL, width=8)


def transition(c, t):
    cols = [(RED, INK), (YEL, INK), (INK, RED), (TEAL, YEL), (YEL, RED), (INK, YEL), (RED, YEL), (YEL, INK)]
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
