"""3 friends, ₹1 lakh each in 2006: FD vs gold vs Nifty (paper Vox story with paper characters)"""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs, typed, drop, warn_icon
from fridge import follow_btn
import saveshare as SS
import paperchars as PC

SH = ROOT + 'friends/'
SCRIPT = json.load(open(SH + 'script.json'))
DURS = json.load(open(SH + 'vo/durs.json'))
LEAD, TAIL = 0.15, 0.3
STARTS, VO = [], []
_t = 0.0
for i, d in enumerate(DURS):
    STARTS.append(_t); VO.append(_t + (0.1 if i == 0 else LEAD)); _t = VO[-1] + d + TAIL
DUR = _t + 1.8
B = STARTS[1:]
NAVY = (30, 60, 120); BLUE = (40, 100, 200); GREY = (120, 112, 104); TEAL = (20, 140, 130); GOLD = (214, 160, 40)
SOFT = (252, 250, 244)
COL = {'R': BLUE, 'M': GOLD, 'K': GRN}
VAL = {'R': 3.87, 'K': 5.78, 'M': 16.95}
NAME = {'R': 'RAVI', 'M': 'MEENA', 'K': 'KARTHIK'}


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def pp(t, t0, d=0.35, s=1.6): return eback(prog(t, t0, d), s)


def src(c, t, txt, t0, y=1740, col=GREY):
    if t > t0: place_text(c, txt, 'type', 24, col, 540, y, t, None, t0, 'fade', track=1)


@functools.lru_cache(32)
def friend(who, mood='calm', pose='down', scale=0.62):
    if who == 'R': return PC.person('man', mood, pose, 'b', shirt=(120, 170, 235), pants=(60, 60, 80), scale=scale)
    if who == 'M': return PC.person('woman', mood, pose, 'a', shirt=(235, 90, 120), saree=True, hair=(30, 20, 15), scale=scale)
    return PC.person('man', mood, pose, 'c', shirt=(110, 200, 120), pants=(70, 55, 45), mustache=True, scale=scale)


@functools.lru_cache(None)
def note(txt='₹1 LAKH', col=(150, 200, 150)):
    w, h = 250, 120
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 12, fill=col, outline=INK, width=5)
    d.ellipse((w // 2 - 32, h // 2 - 32, w // 2 + 32, h // 2 + 32), outline=(80, 120, 80), width=4)
    t = text_img(txt, 'anton', 40, INK); im.alpha_composite(t, (w // 2 - t.size[0] // 2, h // 2 - t.size[1] // 2 - 4))
    return cutout(im, border=6, shadow=0.35)


@functools.lru_cache(None)
def prop(kind):
    w, h = 260, 200
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if kind == 'R':
        d.rounded_rectangle((10, 20, w - 10, h - 10), 14, fill=(40, 70, 140), outline=INK, width=6)
        d.rectangle((10, 60, w - 10, 80), fill=(250, 230, 120))
        t = text_img('FD', 'anton', 70, CREAM); im.alpha_composite(t, (w // 2 - t.size[0] // 2, 90))
        t2 = text_img('PASSBOOK', 'type', 22, CREAM, 2); im.alpha_composite(t2, (w // 2 - t2.size[0] // 2, 28))
    elif kind == 'M':
        for k, (x, y) in enumerate(((40, 110), (130, 110), (85, 40))):
            d.polygon([(x, y + 70), (x + 120, y + 70), (x + 100, y), (x + 20, y)], fill=(255, 200, 60), outline=INK)
            d.line([(x, y + 70), (x + 120, y + 70), (x + 100, y), (x + 20, y), (x, y + 70)], fill=INK, width=5)
            d.line([(x + 30, y + 14), (x + 60, y + 14)], fill=(255, 240, 180), width=6)
    else:
        d.rounded_rectangle((10, 10, w - 10, h - 10), 14, fill=SOFT, outline=INK, width=6)
        pts = [(30, 160), (70, 130), (100, 145), (140, 90), (175, 110), (230, 40)]
        d.line(pts, fill=GRN, width=10, joint='curve')
        t = text_img('NIFTY 50', 'anton', 34, INK); im.alpha_composite(t, (30, 18))
    return cutout(im, border=8, shadow=0.35)


def trio(c, t, t0, y=1180, moods=('calm', 'calm', 'calm'), poses=('down', 'down', 'down'), names=None, gap=0.15):
    for k, who in enumerate('RMK'):
        tk = t0 + gap * k
        if t < tk: continue
        p = prog(t, tk, 0.45); x = 200 + k * 340
        jx, jy, jr = jit(('fr', who), t, 1.6, 0.4)
        bob = math.sin(t * 3 + k) * 4
        place(c, friend(who, moods[k], poses[k]), x + jx + (1 - eo(p)) * 700, y + bob + jy, 1.0, jr, clamp(p * 3))
        if names and t > names:
            place(c, TEA_label(NAME[who], COL[who]), x, y + 290, pp(t, names + 0.12 * k), (-3, 2, -2)[k])


def TEA_label(txt, col):
    import tea
    return tea.label(txt, col)


# ---------------- scenes ----------------
def s1(c, t):
    i = 0
    words_line(c, t, [("YOU", RED, 0.1), ("+", INK, 0.3), ("2", INK, 0.4), ("FRIENDS", INK, 0.55)], 'anton', 130, 290, key='h1')
    trio(c, t, 0.4, 1080)
    for k in range(3):
        tk = 1.3 + 0.15 * k
        if t > tk:
            jx, jy, jr = jit(('nt', k), t, 1.4, 0.4)
            place(c, note(), 200 + k * 340 + jx, 620 + jy - 30 * eo(prog(t, tk, 0.5)), pp(t, tk), (-6, 4, -3)[k] + jr)
    to = at(i, 'Only one', -0.2)
    if t > to:
        sc, a = slam(t, to); place(c, stamp_c('ONLY 1 GETS RICH', RED, 84, -5, 3), 540, 440, sc, 0, a)
    tm = at(i, 'Meet', -0.2)
    if tm < t:
        for k, who in enumerate('RMK'):
            place(c, TEA_label(NAME[who], COL[who]), 200 + k * 340, 1400, pp(t, tm + 0.35 * k), (-3, 2, -2)[k])
    ty = at(i, '2006', -0.3)
    if t > ty:
        p = prog(t, ty, 0.4); place(c, cal('2006'), 540, 1600, 0.6 + 0.4 * eback(p), 2, clamp(p * 3))


@functools.lru_cache(None)
def cal(year):
    w, h = 300, 190
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 16, fill=SOFT, outline=INK, width=6)
    d.rectangle((0, 0, w - 1, 52), fill=RED, outline=INK, width=6)
    for x in (70, 230): d.ellipse((x - 12, -10, x + 12, 14), fill=INK)
    t = text_img(year, 'anton', 96, INK); im.alpha_composite(t, (w // 2 - t.size[0] // 2, 62))
    return cutout(im, border=6, shadow=0.35)


def s2(c, t):
    i = 1; T0 = STARTS[i]
    place_text(c, 'WHERE EACH ONE PUT ₹1 LAKH', 'anton', 72, INK, 540, 270, t, 'wp', T0 + 0.05, 'pop')
    rows = [('R', 'fixed deposit', 'FIXED DEPOSIT', 'safe'), ('M', 'gold', 'GOLD', "like mum said"), ('K', 'Nifty', 'NIFTY INDEX FUND', 'top 50 companies')]
    for k, (who, ph, lab, note_) in enumerate(rows):
        tk = at(i, ph, -0.4)
        if t < tk: continue
        y = 520 + k * 410; p = prog(t, tk, 0.45)
        jx, jy, jr = jit(('r2', k), t, 1.4, 0.3)
        place(c, friend(who, 'happy' if k else 'calm', 'up' if k == 2 else 'down', 0.48), 190 + jx - (1 - eo(p)) * 500, y + jy, 1.0, jr, clamp(p * 3))
        place(c, prop(who), 470 + jx, y - 40 + jy, pp(t, tk + 0.2), (-4, 3, -2)[k])
        if t > tk + 0.4:
            c.alpha_composite(text_img(lab, 'anton', 50, COL[who]), (620, int(y - 90)))
            place_text(c, note_, 'mark', 40, RED, 760, y + 10, t, ('n2', k), tk + 0.6, 'slide', rot=-3)


NIFTY_Y = [(2006, 3966.40), (2007, 6138.60), (2008, 2959.15)]


def s3(c, t):
    i = 2; T0 = STARTS[i]
    words_line(c, t, [("2008", RED, T0 + 0.05), ("CRASH", INK, T0 + 0.3)], 'anton', 150, 290, key='cr')
    p = prog(t, T0 + 0.3, 0.45)
    ox, oy, w, h = 90, 420 + (1 - eo(p)) * 500, 900, 560
    place(c, cutout(grid(w, h), border=0, shadow=0.3), ox + w / 2, oy + h / 2, 1, -0.5, clamp(p * 3))
    if p > 0.5:
        def P(k, v): return (ox + 120 + k * 330, oy + h - 70 - (v - 2000) / 4500 * (h - 140))
        d = ImageDraw.Draw(c); d.line((ox + 80, oy + h - 70, ox + w - 40, oy + h - 70), fill=INK, width=4)
        tg = at(i, 'grown', -0.3); tf = at(i, 'In one year', -0.2)
        f = 0 if t < tg else (min(1, (t - tg) / 0.9) if t < tf else 1 + min(1, (t - tf) / 0.9))
        pts = []
        for s in range(int(f * 20) + 1):
            u = s / 20; k = min(int(u), 1); fr = u - k
            v = NIFTY_Y[k][1] + (NIFTY_Y[k + 1][1] - NIFTY_Y[k][1]) * fr + math.sin(s * 1.9) * 60
            pts.append(P(k + fr, v))
        if len(pts) > 1:
            stroke(c, pts, 10, RED if f > 1.05 else GRN)
            tx, ty = pts[-1]; d.ellipse((tx - 13, ty - 13, tx + 13, ty + 13), fill=RED, outline=INK, width=4)
        for k, (yr, v) in enumerate(NIFTY_Y):
            x, _ = P(k, 2000); li = text_img(f'DEC {yr}', 'type', 24, (90, 85, 80), 1); c.alpha_composite(li, (int(x - li.size[0] / 2), int(oy + h - 58)))
        amt = 100000 if f <= 0 else (100000 + 54765 * eo(min(1, f)) if f <= 1 else 154765 - 80160 * eo(f - 1))
        place(c, text_img(f'₹{int(amt):,}', 'anton', 92, RED if f > 1 else INK), ox + 250, oy + 80)
        if t > tf + 0.8:
            sc, a = slam(t, tf + 0.8); place(c, stamp_c('-52%', RED, 110, -8, 9), ox + 650, oy + 300, sc, 0, a)
    tl = at(i, 'laughed', -0.4)
    if t > T0 + 1.0:
        mk = 'cry' if t > at(i, 'In one year', 0.6) else 'calm'
        place(c, friend('K', mk, 'head' if mk == 'cry' else 'down', 0.5), 260, 1320 + math.sin(t * 20) * (3 if mk == 'cry' else 0))
    if t > tl:
        place(c, friend('M', 'happy', 'down', 0.42), 560, 1360)
        place_text(c, 'ha ha!', 'mark', 52, RED, 560, 1120, t, 'hh', tl, 'pop')
    ts = at(i, 'slept', -0.4)
    if t > ts:
        place(c, friend('R', 'happy', 'down', 0.42), 840, 1360)
        for k in range(3):
            tk = ts + 0.2 + 0.2 * k
            if t > tk: place_text(c, 'z', 'mark', 44 + 10 * k, BLUE, 900 + 30 * k, 1130 - 40 * k + math.sin(t * 2 + k) * 6, t, ('z', k), tk, 'fade')
    src(c, t, 'Nifty 50: 3,966.40 (Dec 2006), 6,138.60 (Dec 2007), 2,959.15 (Dec 2008) · 1stock1', T0 + 1.0, 1700)


@functools.lru_cache(4)
def grid(w, h):
    im = Image.new('RGBA', (w, h), (252, 250, 244, 255)); d = ImageDraw.Draw(im)
    for x in range(0, w, 30): d.line((x, 0, x, h), fill=(205, 218, 228), width=1)
    for y in range(0, h, 30): d.line((0, y, w, y), fill=(205, 218, 228), width=1)
    return im


def s4(c, t):
    i = 3; T0 = STARTS[i]
    tk = T0 + 0.1
    place(c, friend('K', 'angry', 'down', 0.5), 230, 720)
    if t > at(i, "didn't sell", -0.3):
        sc, a = slam(t, at(i, "didn't sell", -0.3)); place(c, stamp_c('HELD', GRN, 96, -8, 11), 230, 400, sc, 0, a)
    tm = at(i, 'Meena', -0.3)
    if t > tm:
        q = pp(t, tm, 0.4, 1.3); place(c, cutout(grid(560, 380), border=0, shadow=0.3), 700, 600, q, 1)
        if q > 0.6:
            c.alpha_composite(text_img('GOLD ₹/10g (AVG)', 'type', 24, GREY, 2), (440, 430))
            d = ImageDraw.Draw(c)
            pts = [(470, 650), (560, 640), (650, 660), (740, 690), (830, 668)]
            m = max(2, int(len(pts) * eo(prog(t, tm + 0.4, 1.0))))
            d.line(pts[:m], fill=GOLD, width=10, joint='curve')
            for (x, _), yr in zip(pts[::2], ('2012', '2013', '2015')): c.alpha_composite(text_img(yr, 'type', 22, GREY), (x - 24, 740))
            if t > tm + 1.2: place_text(c, 'went nowhere', 'mark', 46, RED, 700, 540, t, 'gn', tm + 1.2, 'slide', rot=-4)
    tw = at(i, 'who won', -0.3)
    if t > tw:
        q = pp(t, tw, 0.4, 1.3); place(c, cutout(Image.new('RGBA', (960, 620), SOFT + (255,)), border=0, shadow=0.35), 540, 1250, q, -0.6)
        if q > 0.6:
            place(c, text_img('WHO WON AFTER 20 YEARS?', 'anton', 70, INK), 540, 1010)
            for k, who in enumerate('RMK'):
                place(c, friend(who, 'wow', 'down', 0.36), 230 + k * 310, 1270)
                place(c, text_img('?', 'anton', 110, COL[who]), 300 + k * 310, 1120 + math.sin(t * 4 + k) * 8)
    tg = at(i, 'Guess', -0.3)
    if t > tg:
        sh = math.sin(t * 30) * 5 * math.exp(-(t - tg) * 3)
        place(c, TEA_label('GUESS IN THE COMMENTS!', RED), 540 + sh, 1620, 1.2 * pp(t, tg), -2)
    src(c, t, 'Gold avg ₹29,926 (2012) to ₹26,671 (2015) · Aditya Birla Capital', T0 + 1.0, 1740)


def race(c, t, upto, t0s):
    """bars for R, K, M (order of reveal) with values; upto = number shown"""
    order = ['R', 'K', 'M']
    base = 1250; maxh = 820
    d = ImageDraw.Draw(c)
    d.line((90, base, 990, base), fill=INK, width=5)
    for k, who in enumerate(order):
        x = 230 + k * 310
        place(c, friend(who, 'happy' if (who == 'M' and upto == 3) else ('calm' if k < upto else 'wow'), 'both_up' if (who == 'M' and upto == 3 and t > t0s[2] + 1.0) else 'down', 0.34), x, base + 190)
        place(c, TEA_label(NAME[who], COL[who]), x, base + 360, 0.7, (-2, 2, -1)[k])
        if k >= upto:
            place(c, text_img('?', 'anton', 120, (200, 194, 182)), x, base - 90)
            continue
        q = eo(prog(t, t0s[k], 1.1 if who != 'M' else 1.8))
        v = VAL[who] * q; hg = int(v / 16.95 * maxh)
        d.rounded_rectangle((x - 95, base - hg, x + 95, base), 14, fill=COL[who], outline=INK, width=5)
        lab = text_img(f'₹{v:.2f} L', 'anton', 64, INK)
        place(c, lab, x, base - hg - 44)
    place(c, text_img('AFTER 20 YEARS', 'anton', 110, INK), 540, 240)
    place(c, text_img('₹1 lakh in Dec 2006 became (29 Oct 2026)', 'type', 28, GREY, 1), 540, 330)


def t0s_now():
    return [at(4, 'Three point', -0.3), at(5, 'Five point', -0.3), at(6, 'Sixteen', -0.3)]


def s5(c, t):
    i = 4
    race(c, t, 1, t0s_now())
    tt = at(i, 'taxed', -0.4)
    if t > tt: place_text(c, 'taxed every year', 'mark', 50, RED, 540, 430, t, 'tx', tt, 'slide', rot=-3)
    src(c, t, 'FD: 7% a year assumed, compounded, before tax (my calculation)', STARTS[i] + 0.5, 1780)


def s6(c, t):
    i = 5
    race(c, t, 2, t0s_now())
    tb = at(i, 'before dividends', -0.4)
    if t > tb: place_text(c, 'before dividends', 'mark', 50, GRN, 540, 430, t, 'bd', tb, 'slide', rot=-3)
    src(c, t, 'Nifty 50: 3,966.40 (Dec 2006) to 22,936.75 (29 Oct 2026) · price only', STARTS[i] + 0.5, 1780)


def s7(c, t):
    i = 6
    race(c, t, 3, t0s_now())
    tg = at(i, 'Gold won', -0.3)
    if t > tg:
        sc, a = slam(t, tg); place(c, stamp_c('GOLD WON', GOLD, 110, -6, 77), 370, 640, sc, 0, a)
        r = random.Random(5)
        for k in range(40):
            x0 = r.uniform(80, 1000); sp = r.uniform(300, 700); ph = r.uniform(0, 6)
            y = 150 + ((t - tg) * sp + r.uniform(0, 400)) % 1400
            col = (GOLD, RED, GRN, BLUE, YEL)[k % 5]
            d = ImageDraw.Draw(c); s_ = 10
            d.rectangle((x0 + math.sin(t * 3 + ph) * 30 - s_, y - s_ / 2, x0 + math.sin(t * 3 + ph) * 30 + s_, y + s_ / 2), fill=col)
    src(c, t, 'Gold ₹8,400/10g (2006 avg) to ₹1,42,351 (MCX, 29 Oct 2026)', STARTS[i] + 0.5, 1780)


def s8(c, t):
    i = 7; T0 = STARTS[i]
    if t > T0 + 0.1:
        p = prog(t, T0 + 0.1, 0.3); lw = text_w('THE LESSON', 'osw', 54, 2); x0 = 540 - (lw + 70) / 2
        place(c, warn_icon(YEL), x0 + 28, 262, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
        place(c, text_img('THE LESSON', 'osw', 54, YEL, 2), x0 + 70 + lw / 2, 260, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
    tn = at(i, 'No asset', -0.2)
    words_line(c, t, [("NO", CREAM, tn), ("ASSET", CREAM, tn + 0.1), ("WINS", RED, tn + 0.25)], 'anton', 128, 420, key='na1')
    words_line(c, t, [("EVERY", CREAM, tn + 0.4), ("TIME", CREAM, tn + 0.5)], 'anton', 128, 560, key='na2')
    tf = at(i, 'could flip', -0.3)
    if t > tf: place_text(c, 'next 20 years could flip', 'mark', 52, YEL, 540, 690, t, 'fl', tf, 'slide', rot=-3)
    ts = at(i, 'Split', -0.3)
    if t > ts:
        d = ImageDraw.Draw(c); base = 1300
        for k, (who, v) in enumerate((('R', 3.87), ('K', 5.78), ('M', 16.95))):
            x = 220 + k * 150; q = eo(prog(t, ts + 0.15 * k, 0.6)); hg = int(v / 16.95 * 420 * q)
            d.rounded_rectangle((x - 55, base - hg, x + 55, base), 10, fill=COL[who], outline=CREAM, width=4)
            c.alpha_composite(text_img(NAME[who], 'osw5', 26, CREAM), (int(x - 50), base + 12))
            c.alpha_composite(text_img(f'{v}L', 'anton', 34, CREAM), (int(x - 40), int(base - hg - 44)))
        c.alpha_composite(text_img('₹33,333 IN EACH', 'osw5', 32, (200, 194, 182)), (165, base - 500))
        c.alpha_composite(text_img('SPLIT 3 WAYS', 'osw5', 32, YEL), (668, base + 12))
        te = at(i, 'Eight point', -0.3)
        if t > te:
            q = eo(prog(t, te, 0.8)); hg = int(8.87 / 16.95 * 420 * q)
            d.rounded_rectangle((760 - 90, base - hg, 760 + 90, base), 12, fill=YEL, outline=CREAM, width=5)
            place(c, text_img(f'₹{8.87 * q:.2f} L', 'anton', 64, YEL), 760, base - hg - 44)
            marker_line(c, curve((620, base - 260), (680, base - 330), (690, base - 240)), prog(t, te, 0.4), YEL, 7, head=True, head_size=20)
        if t > at(i, 'no guessing', -0.2):
            place_text(c, 'no guessing needed', 'mark', 50, GRN, 540, 1480, t, 'ng', at(i, 'no guessing', -0.2), 'slide', rot=-2)
    typed(c, 'Past returns are not a promise. Not advice.', 'type', 28, (200, 194, 182), 1620, t, T0 + 2.0, T0 + 3.5)


def s9(c, t):
    i = 8; T0 = STARTS[i]
    q = pp(t, T0, 0.45, 1.2)
    place(c, SS._card(960, 720), 540, 540, q, -0.4)
    if q > 0.6:
        place(c, text_img('₹1 LAKH · 2006 TO 2026', 'anton', 56, INK), 540, 240)
        d = ImageDraw.Draw(c); d.line((90, 282, 990, 282), fill=INK, width=4)
        rows = [('Ravi · FD (7% assumed)', '₹3.87 L', BLUE), ('Karthik · Nifty 50', '₹5.78 L', GRN), ('Meena · Gold', '₹16.95 L', GOLD), ('Split 3 ways', '₹8.87 L', INK)]
        for k, (a_, b_, col) in enumerate(rows):
            tk = T0 + 0.3 + 0.1 * k
            if t < tk: continue
            y = 320 + k * 100
            c.alpha_composite(text_img(a_, 'osw5', 42, INK), (100, y))
            v = text_img(b_, 'anton', 54, col); c.alpha_composite(v, (980 - v.size[0], y - 6))
        if t > at(i, 'Comment', -0.2):
            for k, who in enumerate('RMK'):
                place(c, TEA_label(NAME[who] + '?', COL[who]), 230 + k * 310, 800, pp(t, at(i, 'Comment', 0.2) + 0.25 * k), (-3, 2, -2)[k])
    SS.save_pulse(c, t, at(i, 'Save', -0.3), 540, 1000, 'SAVE THIS')
    SS.send_frame(c, t, at(i, 'send it', -0.3), 'your 2 friends', y=1250)
    tf = at(i, 'Follow', -0.2)
    if t > tf:
        q2 = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1480, 0.5 + 0.5 * eback(q2), 0, clamp(q2 * 3))
    for k, ln in enumerate(['Nifty: NSE via INDmoney, 1stock1 · Gold: Aditya Birla Capital, MCX via INDmoney', 'FD at 7% is an assumption · Nifty price only, no dividends',
                            'Past returns are not a promise. Education only.']):
        place_text(c, ln, 'type', 22, GREY, 540, 1640 + k * 34, t, None, T0 + 0.3, 'fade', track=1)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
DARK_SCENES = {7}


def slam_times():
    return [at(0, 'Only one', -0.2), at(3, "didn't sell", -0.3), at(6, 'Gold won', -0.3)] + [STARTS[k] + 0.05 for k in (1, 2, 3, 4, 7, 8)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('3 FRIENDS · 20 YEARS', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
    ImageDraw.Draw(c).line((60, 118, W - 60, 118), fill=col, width=2)
    ImageDraw.Draw(c).line((60, 118, 60 + (W - 120) * clamp(t / DUR), 118), fill=RED if not dark else YEL, width=8)


def transition(c, t):
    cols = [(BLUE, CREAM), (YEL, INK), (RED, YEL), (INK, RED), (BLUE, YEL), (GRN, CREAM), (GOLD, INK), (YEL, RED)]
    for bi, b in enumerate(B):
        if bi in (4, 5): continue  # race scenes flow without swipe
        d = 0.6
        if abs(t - b) > d / 2 + 0.12: continue
        for layer, delay in ((0, -0.07), (1, 0.0)):
            p = (t - (b - d / 2) - delay) / d
            if p <= 0 or p >= 1: continue
            p = eio(p); SWd, skew = 2050, 320
            xl = (W + 60) + p * (-(SWd + skew) - (W + 60) - 40)
            r = random.Random(bi * 10 + layer + 555)
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
        a = _render(t); b = _render(1.6, loop=True); q = eio((t - (DUR - LOOP)) / LOOP)
        return (a * (1 - q) + b * q).astype(np.uint8)
    return _render(t)


def _render(t, loop=False):
    pbg, dbg = bgs()
    i = scene_at(t); dark = i in DARK_SCENES
    c = (dbg if dark else pbg).copy()
    st = STARTS[i]; en = STARTS[i + 1] if i + 1 < len(STARTS) else DUR
    SCENES[i](c, t)
    z = 1.0 + (0.0 if i in (4, 5, 6) else 0.035) * clamp((t - st) / (en - st))
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
