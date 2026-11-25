"""AI software company: 8 agents (PM, architect, devs, tester, security, release) build a store in a week; you approve (collage, female VO)"""
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

SH = ROOT + 'swteam/'
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
ROLES = [('CEO', NAVY), ('PRODUCT', ORG), ('ARCHITECT', TEAL), ('DESIGN', PURP), ('DEV x3', BLUE), ('TESTER', RED), ('SECURITY', GRN), ('RELEASE', GOLD)]


@functools.lru_cache(None)
def card(w, h, fill=(253, 251, 246)):
    return cutout(Image.new('RGBA', (w, h), fill + (255,)), border=5, shadow=0.35)


@functools.lru_cache(None)
def desk(name, col, big=False):
    w, h = (420, 330) if big else (220, 190)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    s = w / 220
    d.rectangle((10 * s, 120 * s, w - 10 * s, 140 * s), fill=(170, 120, 70), outline=INK, width=3)       # desk top
    d.rectangle((25 * s, 140 * s, 35 * s, h - 4), fill=(140, 95, 55)); d.rectangle((w - 35 * s, 140 * s, w - 25 * s, h - 4), fill=(140, 95, 55))
    d.rounded_rectangle((55 * s, 30 * s, w - 55 * s, 108 * s), 6, fill=(30, 34, 44), outline=INK, width=3)  # monitor
    d.rectangle((w / 2 - 6 * s, 108 * s, w / 2 + 6 * s, 120 * s), fill=INK)
    for k in range(4): d.line((70 * s, (44 + k * 14) * s, (70 + (90, 60, 80, 40)[k]) * s, (44 + k * 14) * s), fill=col, width=max(2, int(4 * s)))
    tx = text_img(name, 'anton', int(30 * s), CREAM); bw = tx.size[0] + 20
    lab = Image.new('RGBA', (bw, tx.size[1] + 8), col + (255,)); lab.alpha_composite(tx, (10, 4))
    im.alpha_composite(lab, (int(w / 2 - bw / 2), int(h - lab.size[1] - 2)))
    return im


def office(c, t, t0, hi=None, y0=520):
    for k, (nm, col) in enumerate(ROLES):
        tk = t0 + 0.07 * k
        if t < tk: continue
        r_, cc = divmod(k, 4); x = 160 + cc * 253; y = y0 + r_ * 230
        sc = eback(prog(t, tk, 0.3)) * (1.12 if hi == k else 1.0)
        place(c, desk(nm, col if hi in (None, k) else (150, 144, 136)), x, y, sc)


def ticket(txt, col):
    return cutout(Image.new('RGBA', (text_w(txt, 'osw5', 40, 0) + 60, 80), (253, 251, 246, 255)), border=5, shadow=0.3, bcol=col)


def s1(c, t):
    i = 0
    dy, a = drop(t, 0.1, 360)
    if a > 0: place(c, SZ.clipping(1.0, 'MARINA CODE LABS', 'AN AI SOFTWARE COMPANY', 'EXAMPLE · 8 AGENTS · 1 HUMAN'), 540, 330 + dy, 0.9, -2, a)
    office(c, t, at(i, 'eight', -0.3), None, 640)
    tw = at(i, 'one week', -0.3)
    if t > tw:
        sc, a2 = slam(t, tw); place(c, stamp_c('ONE WEEK INSIDE', RED, 84, -5, 3), 540, 1250, sc, 0, a2)


def s2(c, t):
    i = 1; T0 = STARTS[i]
    place_text(c, 'MONDAY 9:00 AM', 'anton', 120, INK, 540, 260, t, 'mo', T0 + 0.05, 'pop')
    tc = at(i, 'client', -0.3)
    if t > tc:
        place(c, card(860, 560), 540, 720, pp(t, tc), -1.5)
        if t > tc + 0.2:
            place(c, text_img('CLIENT BRIEF', 'type', 34, GREY, 3), 540, 500)
            place(c, text_img('Online saree store', 'anton', 72, INK), 540, 590)
    for k, (txt, ph) in enumerate((('UPI payments', 'UPI'), ('Order tracking', 'tracking'))):
        tk = at(i, ph, -0.2)
        if t > tk: place(c, text_img('• ' + txt, 'osw5', 50, INK), 540, 700 + k * 80, pp(t, tk))
    tf = at(i, 'Friday', -0.3)
    if t > tf:
        sc, a = slam(t, tf); place(c, stamp_c('LIVE BY FRIDAY', RED, 90, 6, 9), 540, 1150, sc, 0, a)
    src(c, t, 'Example project (fictional client)', T0 + 1.0, 1720)


def role_head(c, t, T0, k, title):
    place(c, desk(ROLES[k][0], ROLES[k][1], True), 540, 430, pp(t, T0 + 0.05))
    place_text(c, title, 'anton', 84, INK, 540, 680, t, 'rh%d' % k, T0 + 0.2, 'pop')


def s3(c, t):
    i = 2; T0 = STARTS[i]
    role_head(c, t, T0, 1, 'PRODUCT AGENT: THE SPEC')
    place(c, card(820, 620), 540, 1150, pp(t, T0 + 0.4), 1)
    items = [('Catalogue', 'Catalogue', True), ('Cart', 'cart', True), ('UPI', 'UPI,', True), ('Tracking', 'tracking', True), ('Loyalty points', 'Loyalty', False)]
    for k, (txt, ph, ok) in enumerate(items):
        tk = at(i, ph, -0.2)
        if t < tk: continue
        y = 900 + k * 100
        c.alpha_composite(text_img(txt, 'osw5', 50, INK if ok else GREY), (240, int(y - 32)))
        if ok: place(c, text_img('V1', 'anton', 46, GRN), 820, y, pp(t, tk))
        else:
            ImageDraw.Draw(c).line((230, y, 640, y), fill=RED, width=6)
            place(c, text_img('LATER', 'anton', 46, RED), 820, y, pp(t, tk))


def s4(c, t):
    i = 3; T0 = STARTS[i]
    role_head(c, t, T0, 2, 'ARCHITECT AGENT: THE PLAN')
    boxes = [('WEB APP', 'Web app', 270, 900, BLUE), ('API SERVER', 'API', 810, 900, TEAL), ('DATABASE', 'database', 270, 1260, NAVY), ('PAYMENT GATEWAY', 'payment', 810, 1260, GRN)]
    d = ImageDraw.Draw(c); shown = []
    for nm, ph, x, y, col in boxes:
        tk = at(i, ph, -0.2)
        if t < tk: continue
        shown.append((x, y))
    if len(shown) >= 2: d.line((shown[0][0] + 160, shown[0][1], shown[1][0] - 160, shown[1][1]), fill=INK, width=6)
    if len(shown) >= 3: d.line((shown[1][0] - 120, shown[1][1] + 70, shown[2][0] + 120, shown[2][1] - 70), fill=INK, width=6)
    if len(shown) >= 4: d.line((shown[1][0], shown[1][1] + 70, shown[3][0], shown[3][1] - 70), fill=INK, width=6)
    for nm, ph, x, y, col in boxes:
        tk = at(i, ph, -0.2)
        if t < tk: continue
        place(c, card(380, 150), x, y, pp(t, tk))
        place(c, label(nm, col), x, y, pp(t, tk + 0.1))


def s5(c, t):
    i = 4; T0 = STARTS[i]
    role_head(c, t, T0, 4, 'DEVELOPER AGENTS: BUILD')
    for k, (nm, col, ph) in enumerate((('FRONTEND', BLUE, 'Frontend'), ('BACKEND', TEAL, 'backend'), ('DEVOPS', ORG, 'DevOps'))):
        tk = at(i, ph, -0.2)
        if t < tk: continue
        x = 200 + k * 340
        place(c, cutout(Image.new('RGBA', (300, 380), (30, 34, 44, 255)), border=5, shadow=0.35), x, 1010, pp(t, tk), (-2, 1, 3)[k])
        place(c, text_img(nm, 'anton', 44, col), x, 860, pp(t, tk))
        n = int(clamp((t - tk) / 1.6) * 7)
        for r in range(n):
            ImageDraw.Draw(c).line((x - 110 + (r % 3) * 20, 920 + r * 34, x - 110 + (r % 3) * 20 + (180, 120, 150, 90, 160, 110, 140)[r], 920 + r * 34), fill=col, width=8)
    tr = at(i, 'code review', -0.3)
    if t > tr:
        sc, a = slam(t, tr); place(c, stamp_c('CODE REVIEWED', GRN, 84, -5, 13), 540, 1330, sc, 0, a)


def s6(c, t):
    i = 5; T0 = STARTS[i]
    role_head(c, t, T0, 5, 'TESTER AGENT: BREAK IT')
    for k, (txt, ph) in enumerate((('BUG: empty cart crash', 'Empty carts'), ('BUG: slow network timeout', 'slow networks'), ('BUG: failed UPI payment', 'failed payments'))):
        tk = at(i, ph, -0.2)
        if t < tk: continue
        y = 860 + k * 130
        place(c, ticket(txt, RED), 540 + (-30, 20, -10)[k], y, pp(t, tk), (-2, 1.5, -1)[k])
        place(c, text_img(txt, 'osw5', 40, RED), 540 + (-30, 20, -10)[k], y, pp(t, tk + 0.1))
    tb = at(i, 'back to', -0.3)
    if t > tb:
        sc, a = slam(t, tb); place(c, stamp_c('SENT BACK TO DEVS', RED, 80, 5, 19), 540, 1320, sc, 0, a)


def s7(c, t):
    i = 6; T0 = STARTS[i]
    place(c, desk('SECURITY', GRN, True), 300, 470, pp(t, T0 + 0.05))
    tp = at(i, 'payments', -0.3)
    if t > tp:
        place(c, label('PAYMENTS: SAFE', GRN), 300, 720, pp(t, tp))
        place(c, label('CUSTOMER DATA: SAFE', GRN), 300, 810, pp(t, tp + 0.5))
    tr = at(i, 'release', -0.3)
    if t > tr:
        place(c, desk('RELEASE', GOLD, True), 780, 1050, pp(t, tr))
    tl = at(i, 'live', -0.3)
    if t > tl:
        sc, a = slam(t, tl); place(c, stamp_c('LIVE ON FRIDAY', GRN, 100, -6, 23), 540, 1360, sc, 0, a)


def s8(c, t):
    i = 7; T0 = STARTS[i]
    if t > T0 + 0.1:
        p = prog(t, T0 + 0.1, 0.3); lw = text_w('ONE HUMAN DESK', 'osw', 54, 2); x0 = 540 - (lw + 70) / 2
        place(c, warn_icon(YEL), x0 + 28, 262, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
        place(c, text_img('ONE HUMAN DESK', 'osw', 54, YEL, 2), x0 + 70 + lw / 2, 260, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
    ty = at(i, 'You.', -0.3)
    if t > ty:
        sc, a = slam(t, ty); place(c, stamp_c('YOU', YEL, 230, -5, 31), 540, 560, sc, 0, a)
    for k, (txt, ph) in enumerate((('APPROVE THE SPEC', 'spec'), ('APPROVE THE DESIGN', 'design'), ('APPROVE THE RELEASE', 'release'))):
        tk = at(i, ph, -0.3)
        if t < tk: continue
        y = 900 + k * 200; q = pp(t, tk, 0.35, 1.3)
        place(c, cutout(Image.new('RGBA', (900, 160), (40, 38, 36, 255)), border=6, shadow=0.4, bcol=YEL), 540, y, q, (-0.8, 0.8, -0.5)[k])
        if q > 0.6: place(c, text_img(txt, 'anton', 64, YEL), 540, y)


def s9(c, t):
    i = 8; T0 = STARTS[i]
    place_text(c, 'YOUR TURN', 'anton', 120, INK, 540, 260, t, 'yt', T0 + 0.05, 'pop')
    office(c, t, T0 + 0.2, None, 470)
    tq = at(i, 'Comment', -0.3)
    place_text(c, 'Which job goes to AI first?', 'pfi', 70, INK, 540, 1000, t, 'wj', T0 + 0.5, 'pop')
    if t > tq:
        sc, a = slam(t, tq); place(c, stamp_c('COMMENT BELOW', RED, 96, -4, 33), 540, 1170, sc, 0, a)
    tf = at(i, 'follow', -0.2)
    if t > tf:
        q2 = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1400, 0.5 + 0.5 * eback(q2), 0, clamp(q2 * 3))
    place_text(c, 'Example company and client. Education only.', 'type', 22, GREY, 540, 1700, t, None, T0 + 0.3, 'fade', track=1)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
DARK_SCENES = {7}


def slam_times():
    return [at(0, 'one week', -0.3), at(1, 'Friday', -0.3), at(4, 'code review', -0.3), at(5, 'back to', -0.3), at(6, 'live', -0.3), at(7, 'You.', -0.3), at(8, 'Comment', -0.3)] + [STARTS[k] + 0.05 for k in range(1, 8)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('AI SOFTWARE TEAM', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
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
