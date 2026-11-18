"""Anthropic IPO: opportunity or bubble? paper-collage style (male VO)"""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs, typed, drop, warn_icon, receipt
from fridge import follow_btn
import saveshare as SS
import defence as DF

SH = ROOT + 'antipo/'
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


# ---------------- scenes ----------------
def s1(c, t):
    i = 0
    words_line(c, t, [("19 NOV", INK, 0.1), ("· 8 PM IST", RED, 0.35)], 'anton', 110, 290, key='h1')
    dy, a = drop(t, 0.6, 360)
    if a > 0:
        hp = round(prog(t, 1.2, 0.5) * 20) / 20
        jx, jy, jr = jit('clip', t, 2, 0.5)
        place(c, clipping(hp), 540 + jx, 600 + dy + jy, 1.0, -3 + jr + (1 - a) * 8, a)
    tv = at(i, 'one point four', -0.3)
    if t > tv:
        v = 1.4 * eo(prog(t, tv, 1.0))
        place(c, text_img(f'${v:.1f} TRILLION', 'anton', 120, PURPLE), 540, 880)
    to = at(i, 'Big opportunity', -0.25)
    if t > to:
        p = prog(t, to, 0.32); jx, jy, jr = jit('t1', t, 1.5, 0.4)
        place(c, qtag('OPPORTUNITY?', GRN), 540 + jx, 1110 + jy, 0.55 + 0.45 * eback(p), -3 + jr, clamp(p * 3))
    tt = at(i, 'bubble', -0.2)
    if t > tt:
        sc, a2 = slam(t, tt); place(c, qtag('OR BUBBLE?', RED), 540, 1300, sc, 3, a2)
        marker_ellipse(c, 540, 1300, 260, 90, prog(t, tt + 0.35, 0.5), INK, 8, seed=5)


def s2(c, t):
    i = 1; T0 = STARTS[i]
    words_line(c, t, [("NASDAQ:", INK, T0 + 0.1), ("ANT", PURPLE, T0 + 0.35)], 'anton', 150, 310, key='nq')
    rows = [('SHARES OFFERED', '825 million', 'Eight hundred'), ('PRICE BAND', '$70 – $78', 'priced between'), ('TRADING STARTS', '19 Nov, 8 PM IST', 'priced between')]
    for k, (lab, val, ph) in enumerate(rows):
        tk = at(i, ph, -0.3 + (1.6 if k == 2 else 0))
        if t < tk: continue
        q = pp(t, tk, 0.35, 1.3); y = 560 + k * 230
        jx, jy, jr = jit(('r', k), t, 1.2, 0.2)
        place(c, cutout(Image.new('RGBA', (900, 190), SOFT + (255,)), border=0, shadow=0.3), 540 + jx, y + jy, q, (-1, 0.8, -0.6)[k] + jr)
        if q > 0.6:
            c.alpha_composite(text_img(lab, 'type', 28, GREY, 2), (130, int(y - 70)))
            c.alpha_composite(text_img(val, 'anton', 88, INK if k != 1 else GRN), (130, int(y - 30)))
    src(c, t, 'Updated S-1 filing, 10 Nov 2026 · Yahoo Finance, CNBC', T0 + 1.0, 1400)


def s3(c, t):
    i = 2; T0 = STARTS[i]
    if t > T0 + 0.1:
        v = 64.4 * eo(prog(t, T0 + 0.2, 1.4))
        place(c, text_img(f'${v:.1f} BILLION', 'anton', 150, GRN), 540, 420)
        place_text(c, 'raised at the top price', 'mark', 56, INK, 540, 540, t, 'rs', T0 + 0.6, 'slide', rot=-3)
    rocket(c, 540, 1000 - 200 * eo(prog(t, T0 + 0.4, 3.0)), 1.0, t)
    tg = at(i, 'giant', -0.2)
    if t > tg:
        sc, a = slam(t, tg); place(c, stamp_c('GIANT IPO', RED, 90, -8, 21), 760, 760, sc, 0, a)
    src(c, t, '825M shares × $78 incl. selling shareholders · Yahoo Finance', T0 + 0.8, 1440)


def s4(c, t):
    i = 3; T0 = STARTS[i]
    words_line(c, t, [("WHAT IT", INK, T0 + 0.1), ("SELLS", PURPLE, T0 + 0.35)], 'anton', 130, 300, key='ws')
    tc = at(i, 'Claude', -0.2)
    if t > tc:
        sc, a = slam(t, tc); place(c, text_img('CLAUDE', 'anton', 170, PURPLE), 540, 500, sc, 0, a)
        place_text(c, 'an AI model family', 'mark', 52, INK, 540, 620, t, 'cl', tc + 0.4, 'slide', rot=-3)
    steps = [('1', 'CODING', 'write & fix software', 'coding', BLUE), ('2', 'WRITING', 'drafts, docs, emails', 'writing', ORG), ('3', 'ANALYSIS', 'data, research, reports', 'analysis', GRN)]
    for k, (n, tt_, sub, ph, col) in enumerate(steps):
        tk = at(i, ph, -0.3); pk = prog(t, tk, 0.45)
        if pk <= 0: continue
        jx, jy, jr = jit(('tk', k), t, 1.4, 0.25)
        place(c, step_ticket(n, tt_, sub, col), 540 + (1 - eo(pk)) * 900 + jx, 790 + k * 180 + jy, 0.92, (-1.2, 1.0, -0.6)[k] + jr)
    ta = at(i, 'through apps', -0.2)
    if t > ta:
        place_text(c, 'via apps + API · for businesses & developers', 'osw5', 38, GREY, 540, 1330, t, 'ap', ta, 'slide')


def s5(c, t):
    i = 4; T0 = STARTS[i]
    words_line(c, t, [("WILD", GRN, T0 + 0.1), ("GROWTH", INK, T0 + 0.35)], 'anton', 130, 300, key='wg')
    d = ImageDraw.Draw(c); base = 1000
    ta = at(i, 'one point two', -0.3); tb = at(i, 'sixteen point', -0.3)
    for k, (lab, v, tk, col) in enumerate((('H1 2025', 1.163, ta, (200, 190, 175)), ('H1 2026', 16.286, tb, GRN))):
        if t < tk: continue
        ph = eo(prog(t, tk, 0.8)); hg = max(14, int(v / 16.286 * 480 * ph)); x = 330 + k * 420
        d.rounded_rectangle((x - 110, base - hg, x + 110, base), 14, fill=col, outline=INK, width=5)
        place(c, text_img(f'${v * ph:.1f}B', 'anton', 64, INK), x, base - hg - 44)
        place(c, text_img(lab, 'osw5', 38, INK), x, base + 36)
    tx = at(i, 'up from', 0.6)
    if t > tx:
        sc, a = slam(t, tx); place(c, stamp_c('14x', GRN, 110, -8, 31), 320, 600, sc, 0, a)
    tr = at(i, 'run rate', -0.3)
    if t > tr:
        q = pp(t, tr, 0.35, 1.3)
        place(c, cutout(Image.new('RGBA', (900, 170), (40, 38, 36, 255)), border=6, shadow=0.4, bcol=GRN), 540, 1210, q, -1)
        if q > 0.6:
            c.alpha_composite(text_img('RUN RATE (31 OCT 2026)', 'type', 26, (200, 194, 182), 2), (130, 1150))
            c.alpha_composite(text_img('~$81 BILLION / YEAR', 'anton', 72, CREAM), (130, 1180))
    src(c, t, 'Revenue: S-1 (H1) · run rate: S-1/A-3, 17 Nov 2026', T0 + 1.0, 1440)


def s6(c, t):
    i = 5; T0 = STARTS[i]
    words_line(c, t, [("THE", INK, T0 + 0.05), ("CATCH", RED, T0 + 0.25)], 'anton', 130, 300, key='ct')
    tl = at(i, 'net loss', -0.3)
    if t > tl:
        v = 80.7 * eo(prog(t, tl, 1.2))
        place(c, text_img(f'-${v:.1f} BILLION', 'anton', 130, RED), 540, 480)
        place_text(c, 'net loss, H1 2026', 'mark', 50, INK, 540, 590, t, 'nl', tl + 0.5, 'slide', rot=-3)
    tm = at(i, 'Most of it', -0.3)
    if t > tm:
        d = ImageDraw.Draw(c); f = eo(prog(t, tm, 1.0))
        x0, y0, x1, y1 = 120, 700, 960, 820
        d.rounded_rectangle((x0, y0, x1, y1), 30, fill=(240, 200, 190), outline=INK, width=5)
        xr = x0 + (x1 - x0) * (72.4 / 80.7) * f
        d.rounded_rectangle((x0, y0, max(x0 + 60, xr), y1), 30, fill=(200, 190, 175), outline=INK, width=5)
        if f > 0.6:
            c.alpha_composite(text_img('$72.4B PAPER LOSS', 'anton', 50, INK), (x0 + 30, y0 + 30))
            c.alpha_composite(text_img('convertible notes, SAFEs, derivatives (non-cash)', 'type', 26, GREY, 1), (x0, y1 + 16))
    tc = at(i, 'computing costs', -0.3)
    if t > tc:
        sc, a = slam(t, tc); place(c, stamp_c('COMPUTE COSTS UP', RED, 74, -6, 41), 540, 1060, sc, 0, a)
        place_text(c, 'compute & infra spend +300% in Q2', 'mark', 44, RED, 540, 1170, t, 'cc', tc + 0.5, 'slide', rot=-3)
    src(c, t, 'S-1 (H1 2026) via The VC Corner', T0 + 1.0, 1440)


def s7(c, t):
    i = 6; T0 = STARTS[i]
    words_line(c, t, [("WHO", INK, T0 + 0.05), ("CONTROLS IT?", PURPLE, T0 + 0.25)], 'anton', 120, 300, key='wc')
    tv = at(i, 'Seven', -0.3)
    if t > tv:
        f = eo(prog(t, tv, 1.2)); d = ImageDraw.Draw(c); cx, cy, r = 540, 760, 260
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(220, 214, 200), outline=INK, width=6)
        d.pieslice((cx - r, cy - r, cx + r, cy + r), -90, -90 + 360 * 0.501 * f, fill=PURPLE, outline=INK, width=6)
        if f > 0.7:
            place(c, text_img('50.1%', 'anton', 70, CREAM), cx + 128, cy - 10)
            place(c, text_img('VOTES', 'osw5', 34, CREAM), cx + 128, cy + 50)
    tf = at(i, 'special share', -0.3)
    if t > tf:
        place_text(c, '7 co-founders · one "Class F" share', 'mark', 48, INK, 540, 1080, t, 'cf', tf, 'slide', rot=-3)
    tw = at(i, 'steering wheel', -0.4)
    if t > tw:
        sc, a = slam(t, tw); place(c, stamp_c('YOU OWN, THEY STEER', RED, 64, -6, 51), 540, 1220, sc, 0, a)
    src(c, t, 'S-1: Class F share held by a Founder LLC', T0 + 1.0, 1440)


def s8(c, t):
    i = 7; T0 = STARTS[i]
    if t > T0 + 0.1:
        p = prog(t, T0 + 0.1, 0.3); lw = text_w('THE VERDICT', 'osw', 54, 2); x0 = 540 - (lw + 70) / 2
        place(c, warn_icon(YEL), x0 + 28, 262, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
        place(c, text_img('THE VERDICT', 'osw', 54, YEL, 2), x0 + 70 + lw / 2, 260, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
    tn = at(i, 'seventeen', -0.3)
    words_line(c, t, [("~17x", CREAM, tn), ("RUN RATE", YEL, tn + 0.3)], 'anton', 120, 420, key='ny')
    rows = [('Growth is real', 'revenue 14x in a year', 'seventeen', GRN, True),
            ('Lots of cash', '$131.7B cash & investments', 'seventeen', GRN, True),
            ('Priced for perfection', '~17x run rate at $78', 'priced for', RED, False),
            ('If growth slows', 'the price can fall hard', 'If growth', RED, False)]
    for k, (h1, h2, ph, col, ok) in enumerate(rows):
        tk = at(i, ph, -0.3 + (0.7 if k == 0 else 1.4 if k == 1 else 0))
        if t < tk: continue
        y = 640 + k * 200; q = pp(t, tk, 0.35, 1.3)
        jx, jy, jr = jit(('v', k), t, 1.2, 0.2)
        place(c, cutout(Image.new('RGBA', (900, 160), (40, 38, 36, 255)), border=6, shadow=0.4, bcol=col), 540 + jx, y + jy, q, (-0.8, 0.8, -0.6, 0.6)[k] + jr)
        if q < 0.6: continue
        d = ImageDraw.Draw(c); bx, by = 150, y
        if ok: d.line((bx - 22, by + 2, bx - 6, by + 20, bx + 24, by - 18), fill=col, width=10, joint='curve')
        else: d.line((bx - 18, by - 18, bx + 18, by + 18), fill=col, width=10); d.line((bx - 18, by + 18, bx + 18, by - 18), fill=col, width=10)
        c.alpha_composite(text_img(h1, 'anton', 56, CREAM), (210, int(y - 58)))
        c.alpha_composite(text_img(h2, 'type', 28, (200, 194, 182), 1), (214, int(y + 18)))
    typed(c, 'Not investment advice. DYOR.', 'type', 30, (200, 194, 182), 1560, t, at(i, 'fall hard', 0.2), at(i, 'fall hard', 1.2))


def s9(c, t):
    i = 8; T0 = STARTS[i]
    q = pp(t, T0, 0.45, 1.2)
    place(c, SS._card(960, 860), 540, 600, q, -0.4)
    if q > 0.6:
        place(c, text_img('ANTHROPIC IPO · CHEAT SHEET', 'anton', 50, INK), 540, 230)
        d = ImageDraw.Draw(c); d.line((90, 272, 990, 272), fill=INK, width=4)
        rows = [('Ticker', 'ANT · Nasdaq', INK), ('Price band', '$70 – $78', GRN), ('Trading starts', '19 Nov · 8 PM IST', INK), ('Valuation (top)', '~$1.4 trillion', PURPLE),
                ('H1 2026 revenue', '$16.3B (14x)', GRN), ('H1 2026 net loss', '$80.7B ($72B non-cash)', RED), ('Founder votes', '50.1%', NAVY), ('Run rate', '~$81B / yr', INK)]
        for k, (a_, b_, col) in enumerate(rows):
            tk = T0 + 0.3 + 0.08 * k
            if t < tk: continue
            y = 300 + k * 78
            c.alpha_composite(text_img(a_, 'osw5', 38, INK), (100, y))
            v = text_img(b_, 'anton', 42, col); c.alpha_composite(v, (980 - v.size[0], y - 2))
        SS.save_pulse(c, t, T0 + 1.2, 540, 1080, 'SAVE THIS')
    tq = at(i, 'Tell me', -0.3)
    if t > tq:
        place_text(c, 'invest, or watch first? comment 👇'.replace(' 👇', ''), 'mark', 54, RED, 540, 1300, t, 'iq', tq, 'slide', rot=-3)
    tf = at(i, 'follow', -0.2)
    if t > tf:
        q2 = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1500, 0.5 + 0.5 * eback(q2), 0, clamp(q2 * 3))
    for k, ln in enumerate(['Sources: Anthropic S-1 & amendments (Nov 2026), CNBC, Yahoo Finance', 'Price band, not final IPO price · final price set 18 Nov (US)',
                            'Not a buy/sell call. Education only.']):
        place_text(c, ln, 'type', 22, GREY, 540, 1680 + k * 34, t, None, T0 + 0.3, 'fade', track=1)


def pp(t, t0, d=0.35, s=1.6): return eback(prog(t, t0, d), s)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
DARK_SCENES = {7}


def slam_times():
    return [at(0, 'bubble', -0.2), at(2, 'giant', -0.2), at(5, 'eighty point', -0.3), at(7, 'fall hard', -0.3)] + [STARTS[k] + 0.05 for k in range(1, 8)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('IPO: OPPORTUNITY OR BUBBLE?', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
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
