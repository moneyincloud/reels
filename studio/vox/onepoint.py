"""onepoint: One Point One Solutions - multibagger or trap? (LISTX style + emotion avatar, male VO)."""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, re
import numpy as np
from PIL import Image, ImageDraw
from lib import *
import listx as LX
from listx import INKL, ACC, MUTE
import defence as DF

SH = ROOT + 'onepoint/'
SCRIPT = json.load(open(SH + 'script.json'))
DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO, DUR = LX.timing(SCRIPT, DURS)
WORDS = LX.word_times(SCRIPT, DURS, VO)
WORDS_ALL = [w for seg in WORDS for w in seg]
RED = (225, 80, 70); ORANGE = (240, 140, 40); LIGHTT = (240, 240, 240); BLUE = (70, 120, 200)
DARK = {6, 7}
SWITCH = [STARTS[k] for k in (6, 8)]

ACCENTS = [["seventy two rupee", "really works for."], ["insurance company,", "bank", "airline,", "KYC,"],
           ["Navi Mumbai.", "Chennai.", "eight thousand"], ["global.", "Ohio,", "Costa Rica,", "Colombia", "Panama."],
           ["life insurers,", "Indian airline,", "motorcycle brand."], ["real.", "three hundred and thirteen crore", "one hundred and twenty nine percent."],
           ["most people miss."], ["buying other companies.", "two hundred and twenty crore.", "thirty nine percent", "forty three times"],
           ["multibagger or trap?", "growing fast.", "must pay off.", "November third."], ["yes or no.", "Save this,"]]


def acc_idx(i):
    ws = [w for w, _ in WORDS[i]]; out = set()
    for ph in ACCENTS[i]:
        p = ph.split(' ')
        for k in range(len(ws) - len(p) + 1):
            if ws[k:k + len(p)] == p: out |= set(range(k, k + len(p))); break
    return out


ACC_IDX = [acc_idx(i) for i in range(len(SCRIPT))]


def pages(i):
    ws = WORDS[i]; out = []; st = 0
    for k, (w, _) in enumerate(ws):
        if re.search(r'[.?!]$', w) and k < len(ws) - 1 and k - st >= 3 and len(' '.join(x for x, _ in ws[st:k + 1])) > 26:
            out.append((st, k + 1)); st = k + 1
    out.append((st, len(ws)))
    return out


PAGES = [pages(i) for i in range(len(SCRIPT))]


def seg_at(t):
    i = 0
    for k, s in enumerate(STARTS):
        if t >= s: i = k
    return i


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase); assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def head(c, t, i, dark):
    pg = PAGES[i][0]
    for a, b in PAGES[i]:
        if t >= WORDS[i][a][1] - 0.05: pg = (a, b)
    a, b = pg; ws = WORDS[i][a:b]; n = len(' '.join(w for w, _ in ws))
    size = 72 if n < 40 else 64 if n < 75 else 58
    LX.headline(c, t, ws, {k - a for k in ACC_IDX[i] if a <= k < b}, y0=230, size=size,
                col=LIGHTT if dark else INKL, hl=(30, 80, 58) if dark else LX.ACC_SOFT)


def pop_in(t, t0, d=0.3):
    return eback(prog(t, t0, d), 1.7) if t >= t0 else 0


P = lambda tag, k=0: LX.POSE[tag][k]
CUES = sorted([
    (0, P('inspect')), (at(0, 'really works', -0.1), P('insider')),
    (VO[1], P('alert')), (at(1, 'Customer care', -0.1), P('typing')),
    (VO[2], P('idea')), (at(2, 'Over eight', -0.1), P('confident')),
    (VO[3], P('moon_point')),
    (VO[4], P('think')), (at(4, 'European', -0.1), P('proud')),
    (VO[5], P('bull')), (at(5, 'jumped', -0.1), P('jackpot')),
    (VO[6], P('secret')),
    (VO[7], P('analysis')), (at(7, 'Debt', -0.1), P('stress')), (at(7, 'Promoters', -0.1), P('nervous', 1)), (at(7, 'forty three', -0.1), P('shock')),
    (VO[8], P('think')), (at(8, 'growing fast', -0.3), P('confident')), (at(8, 'must pay', -0.3), P('speculator')), (at(8, 'Results', -0.1), P('alert')),
    (VO[9], P('point')), (at(9, 'send', -0.1), P('proud', 1))])


# ---------------- shared bits ----------------
@functools.lru_cache(32)
def card(txt, sub, w=470, fill=(252, 252, 250), fg=INKL, size=34):
    h = 96 if sub else 74
    im = Image.new('RGBA', (w + 8, h + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((7, 7, w + 7, h + 7), 16, fill=INKL)
    d.rounded_rectangle((0, 0, w, h), 16, fill=fill, outline=INKL, width=4)
    f = size
    while text_w(txt, 'pop', f) > w - 40 and f > 18: f -= 2
    im.alpha_composite(text_img(txt, 'pop', f, fg), (20, 10))
    if sub: im.alpha_composite(text_img(sub, 'type', 20, MUTE), (22, 60))
    return im


def slide_in(c, t, t0, im, x, y, dx=80):
    if t < t0: return
    q = eo(prog(t, t0, 0.3)); place(c, im, x + (1 - q) * dx, y, 1, 0, q)


# ---------------- per-segment visuals ----------------
def v0(c, t):
    p = pop_in(t, VO[0] + 0.1, 0.4)
    if p:
        place(c, price_card(), 540, 1000, p, -2)
    LX.sticker(c, t, at(0, 'who it'), 'WHO DOES IT WORK FOR?', 560, 1300, 4, 38)


@functools.lru_cache(2)
def price_card():
    w, h = 700, 380; im = Image.new('RGBA', (w + 12, h + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 10, w + 10, h + 10), 28, fill=INKL)
    d.rounded_rectangle((0, 0, w, h), 28, fill=(252, 252, 250), outline=INKL, width=6)
    im.alpha_composite(text_img('ONE POINT ONE SOLUTIONS', 'type', 28, MUTE, 3), (40, 34))
    im.alpha_composite(text_img('₹72.62', 'pop', 150, INKL), (36, 70))
    im.alpha_composite(text_img('NSE: ONEPOINT · 30 OCT 2026', 'type', 22, MUTE, 2), (42, 262))
    d.rounded_rectangle((40, 300, 330, 350), 25, fill=ACC)
    im.alpha_composite(text_img('+64% IN 1 YEAR', 'pop', 28, (252, 252, 250)), (62, 306))
    return im


def v1(c, t):
    # phone ringing + callers
    q = pop_in(t, VO[1] + 0.1, 0.4)
    if q:
        place(c, phone_img(), 300, 1020, q, math.sin(t * 30) * 3 if (t * 2) % 2 < 0.6 else 0)
    for k, (ph, tx) in enumerate((('insurance', 'Insurance company'), ('bank', 'Bank'), ('airline', 'Airline'))):
        slide_in(c, t, at(1, ph, -0.15), card(tx, 'calling...', 420), 790, 840 + k * 120)
    for k, (ph, tx) in enumerate((('Customer care', 'CUSTOMER CARE'), ('collections', 'COLLECTIONS'), ('KYC', 'KYC'))):
        LX.sticker(c, t, at(1, ph, -0.1), tx, 260 + k * 250, 1290 + (k % 2) * 30, (-5, 4, -3)[k], 32)


@functools.lru_cache(2)
def phone_img():
    im = Image.new('RGBA', (360, 440), (0, 0, 0, 0)); LX.ico_phone(im, 180, 230, 1.9); d = ImageDraw.Draw(im)
    for r in (60, 90, 120):
        d.arc((180 + 70 - r, 70 - r, 180 + 70 + r, 70 + r), -60, 10, fill=ACC, width=6)
    return im


# India map
IN_LON0, IN_LON1, IN_LAT0, IN_LAT1 = 67.5, 98.5, 6.0, 37.5
IMW = 760; IMH = int(IMW * (IN_LAT1 - IN_LAT0) / (IN_LON1 - IN_LON0) * 1.08)


def iproj(lon, lat):
    return (lon - IN_LON0) / (IN_LON1 - IN_LON0) * IMW, (IN_LAT1 - lat) / (IN_LAT1 - IN_LAT0) * IMH


@functools.lru_cache(2)
def india_img():
    d0 = json.load(open(ROOT + 'tvs/world.geojson')); S_ = 2
    im = Image.new('RGBA', (IMW * S_, IMH * S_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for f in d0['features']:
        nm = f['properties']['NAME']; g = f['geometry']
        polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        for poly in polys:
            pts = [iproj(x, y) for x, y in poly[0]]
            if not any(-50 < x < IMW + 50 and -50 < y < IMH + 50 for x, y in pts): continue
            P_ = [(x * S_, y * S_) for x, y in pts]
            if nm == 'India': d.polygon(P_, fill=(252, 226, 196)); d.line(P_ + [P_[0]], fill=INKL, width=6)
    return im.resize((IMW, IMH), Image.LANCZOS)


CITIES = [('Navi Mumbai', 'Maharashtra · HQ', 73.0, 19.03, 'Navi Mumbai', (-1, 0)), ('Pune', 'Maharashtra', 73.86, 18.52, 'Pune', (1, 0)),
          ('Gurugram', 'Haryana', 77.03, 28.46, 'Gurugram', (1, 0)), ('Bengaluru', 'Karnataka', 77.59, 12.97, 'Bengaluru', (-1, 0)),
          ('Indore', 'Madhya Pradesh', 75.86, 22.72, 'Indore', (1, 0)), ('Chennai', 'Tamil Nadu', 80.27, 13.08, 'Chennai', (1, 0))]


def v2(c, t):
    q = pop_in(t, VO[2], 0.4)
    if not q: return
    ox, oy = 540 - IMW / 2 - 30, 660
    place(c, india_img(), ox + IMW / 2, oy + IMH / 2, 0.9 + 0.1 * q)
    d = ImageDraw.Draw(c)
    for k, (nm, st, lon, lat, ph, (sx, sy)) in enumerate(CITIES):
        t0 = at(2, ph, -0.1)
        if t < t0: continue
        x, y = iproj(lon, lat); x += ox; y += oy
        pq = pop_in(t, t0, 0.3); r = 13 * pq
        col = RED if k == 0 else ACC
        d.ellipse((x - r, y - r, x + r, y + r), fill=col, outline=INKL, width=3)
        lb = city_label(nm, st, k == 0)
        lx = x + 22 if sx > 0 else x - 22 - lb.size[0]
        ly = y - 24 + sy * 34
        if pq > 0.5: c.alpha_composite(lb, (int(lx), int(ly)))
    if t > at(2, 'Over eight'):
        v = int(8000 * eo(prog(t, at(2, 'Over eight'), 0.8)))
        place(c, text_img(f'{v:,}+', 'pop', 84, INKL), 820, 1460)
        place(c, text_img('PEOPLE', 'type', 26, MUTE, 3), 820, 1525)


@functools.lru_cache(16)
def city_label(nm, st, hq):
    a = text_img(nm, 'pop', 28, INKL); b = text_img(st, 'type', 18, RED if hq else MUTE, 1)
    w = max(a.size[0], b.size[0]) + 20; h = 66
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 10, fill=(252, 252, 250, 235), outline=INKL, width=2)
    im.alpha_composite(a, (10, 2)); im.alpha_composite(b, (11, 40))
    return im


GLOBAL = [('OHIO, USA', -84.5, 39.1, 'Ohio', (0, -36)), ('COSTA RICA', -84.0, 9.9, 'Costa Rica', (0, 34)),
          ('COLOMBIA', -74.0, 4.6, 'Colombia', (80, 64)), ('PANAMA', -79.5, 9.0, 'Panama', (70, -20))]


def v3(c, t):
    q = pop_in(t, VO[3], 0.4)
    if not q: return
    mw = DF.MW; sc = 1.0; ox, oy = 40, 780
    place(c, DF.map_img(False), ox + mw / 2, oy + DF.MH / 2, (0.92 + 0.08 * q) * sc)
    d = ImageDraw.Draw(c)
    hx, hy = DF.proj(73.0, 19.0); hx += ox; hy += oy
    d.ellipse((hx - 12, hy - 12, hx + 12, hy + 12), fill=RED, outline=INKL, width=3)
    for k, (nm, lon, lat, ph, (lx, ly)) in enumerate(GLOBAL):
        t0 = at(3, ph, -0.1)
        if t < t0: continue
        x, y = DF.proj(lon, lat); x += ox; y += oy
        u = eo(prog(t, t0, 0.6))
        pts = DF.arc_pts((hx, hy), (x, y), 0.22)
        n = max(2, int(len(pts) * u)); d.line(pts[:n], fill=ACC, width=5)
        if u > 0.95:
            d.ellipse((x - 11, y - 11, x + 11, y + 11), fill=ACC, outline=INKL, width=3)
            lb = text_img(nm, 'pop', 26, INKL); place(c, lb, x + lx, y + ly)
    LX.sticker(c, t, at(3, 'Panama', 0.5), '10 CENTRES · 4 CONTINENTS', 540, 1390, -3, 34)


def v4(c, t):
    rows = [('Two of', "2 of India's biggest life insurers"), ('a leading', 'A leading Indian airline'),
            ('banks in', 'Banks in Central America'), ('European', 'A European motorcycle brand')]
    for k, (ph, tx) in enumerate(rows):
        slide_in(c, t, at(4, ph, -0.15), card(tx, None, 760, size=36), 470, 820 + k * 125)
    LX.sticker(c, t, at(4, 'motorcycle', 0.5), '100+ CLIENTS', 300, 1360, -6, 44)
    LX.sticker(c, t, at(4, 'motorcycle', 0.9), 'NAMES NOT DISCLOSED', 640, 1440, 4, 28)


SALES = [('FY21', 102), ('FY22', 132), ('FY23', 140), ('FY24', 170), ('FY25', 256), ('FY26', 313)]


def v5(c, t):
    d = ImageDraw.Draw(c); x0, yb, bw, gap, hmax = 100, 1400, 80, 26, 520
    t0 = at(5, 'Sales went'); t1 = at(5, 'last year')
    for k, (yr, v) in enumerate(SALES):
        tk = t0 + (t1 - t0) * k / 5
        if t < tk: continue
        q = eo(prog(t, tk, 0.5)); h = hmax * v / 313 * q; x = x0 + k * (bw + gap)
        d.rounded_rectangle((x, yb - h, x + bw, yb), 10, fill=ACC if k == 5 else (180, 214, 198), outline=INKL, width=4)
        c.alpha_composite(text_img(yr, 'type', 22, MUTE, 1), (int(x + 14), yb + 10))
        if q > 0.6:
            vt = text_img(f'₹{v}', 'pop', 30, INKL); c.alpha_composite(vt, (int(x + bw / 2 - vt.size[0] / 2), int(yb - h - 44)))
    if t > t0: c.alpha_composite(text_img('SALES, ₹ CRORE', 'type', 22, MUTE, 2), (x0, yb + 46))
    t2 = at(5, 'June quarter')
    if t > t2:
        q = pop_in(t, t2, 0.4)
        place(c, quarter_card(), 890, 780, q, 3)
        if t > at(5, 'one hundred and twenty nine'):
            LX.sticker(c, t, at(5, 'one hundred and twenty nine'), '+129%', 900, 1080, -6, 70)


@functools.lru_cache(2)
def quarter_card():
    w, h = 300, 220; im = Image.new('RGBA', (w + 10, h + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((8, 8, w + 8, h + 8), 20, fill=INKL); d.rounded_rectangle((0, 0, w, h), 20, fill=(252, 252, 250), outline=INKL, width=4)
    im.alpha_composite(text_img('JUNE QUARTER', 'type', 20, MUTE, 2), (22, 16))
    im.alpha_composite(text_img('₹69 Cr', 'pop', 34, MUTE), (22, 50))
    im.alpha_composite(text_img('->', 'pop', 34, MUTE), (150, 50))
    im.alpha_composite(text_img('₹158 Cr', 'pop', 54, ACC), (22, 100))
    im.alpha_composite(text_img('Q1 FY26 vs Q1 FY27', 'type', 18, MUTE), (22, 180))
    return im


def v6(c, t):
    q = pop_in(t, VO[6], 0.35)
    if q: place(c, text_img('BUT...', 'pop', 220, RED), 520, 1050, q, -4)


@functools.lru_cache(16)
def catch_row(lbl, val, w=920):
    h = 120; im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 20, fill=(32, 34, 36), outline=(90, 60, 58), width=3)
    d.ellipse((22, 34, 74, 86), fill=RED); d.line((36, 48, 60, 72), fill=(252, 252, 250), width=7); d.line((60, 48, 36, 72), fill=(252, 252, 250), width=7)
    im.alpha_composite(text_img(lbl, 'type', 22, (180, 180, 180), 2), (96, 18))
    f = 44
    while text_w(val, 'pop', f) > w - 120 and f > 24: f -= 2
    im.alpha_composite(text_img(val, 'pop', f, LIGHTT), (96, 48))
    return im


def v7(c, t):
    rows = [('buying', 'GROWTH SOURCE', 'Acquisitions: Netcom (Costa Rica) & ITCube'),
            ('Debt', 'BORROWINGS', '₹47 Cr (FY25) -> ₹220 Cr (FY26)'),
            ('Promoters', 'PROMOTER PLEDGE', '39% of their shares pledged'),
            ('forty three', 'VALUATION', 'P/E about 43 · ROE about 7%')]
    for k, (ph, a, b) in enumerate(rows):
        slide_in(c, t, at(7, ph, -0.2), catch_row(a, b), 540, 790 + k * 150)


def v8(c, t):
    place(c, text_img('MULTIBAGGER?', 'pop', 40, ACC), 300, 790); place(c, text_img('TRAP?', 'pop', 40, RED), 780, 790)
    good = [('growing fast', 'Sales growing fast'), ('growing fast', '8,000+ people'), ('growing fast', '100+ clients')]
    bad = [('the debt', 'Debt up 4.7x'), ('the pledge', '39% pledged'), ('acquisitions', 'Must pay off')]
    for k, (ph, tx) in enumerate(good):
        t0 = at(8, ph, -0.2 + 0.25 * k)
        if t > t0: place(c, card('+ ' + tx, None, 420, fill=(226, 242, 234), size=30), 300, 890 + k * 100, pop_in(t, t0, 0.25))
    for k, (ph, tx) in enumerate(bad):
        t0 = at(8, ph, -0.2)
        if t > t0: place(c, card('- ' + tx, None, 420, fill=(250, 226, 222), size=30), 780, 890 + k * 100, pop_in(t, t0, 0.25))
    LX.sticker(c, t, at(8, 'Results'), 'RESULTS: 3 NOV 2026', 420, 1260, -4, 44)


def v9(c, t):
    LX.sticker(c, t, at(9, 'yes'), 'YES', 250, 1020, -7, 70)
    LX.sticker(c, t, at(9, 'no.'), 'NO', 560, 1020, 6, 70)
    LX.sticker(c, t, at(9, 'Save'), 'SAVE', 300, 1220, 5, 52)
    LX.sticker(c, t, at(9, 'send'), 'SEND TO A CALL-CENTRE FRIEND', 470, 1380, -3, 32)


VIS = [v0, v1, v2, v3, v4, v5, v6, v7, v8, v9]
SRC = ('Price: INDmoney, 30 Oct 2026 · Sales/debt/pledge/P-E: Screener (consolidated) · Q1 FY27 & centres: company releases (Aug & Mar 2026), '
       'ITCube & India centres: DSIJ, YourStory')


def _render(t, loop=False):
    i = seg_at(t); dark = i in DARK
    c = LX.bg_cached(dark)
    hc = (150, 150, 150) if dark else MUTE
    c.alpha_composite(text_img(f'// {i + 1:02d} · ONEPOINT · multibagger or trap?', 'type', 30, hc, 2), (70, 150))
    pr = text_img('NSE ₹72.62', 'type', 30, ACC, 2); c.alpha_composite(pr, (W - 70 - pr.size[0], 150))
    head(c, t, i, dark)
    VIS[i](c, t)
    col = (150, 150, 150) if dark else MUTE
    parts = [SRC, 'Not a buy/sell call. Education only.']
    rows = []
    for ptxt in parts:
        cur = ''
        for wd in ptxt.split(' '):
            nxt = (cur + ' ' + wd).strip()
            if text_w(nxt, 'type', 18) > 640 and cur: rows.append(cur); cur = wd
            else: cur = nxt
        rows.append(cur)
    for r, row in enumerate(rows):
        c.alpha_composite(text_img(row, 'type', 18, col), (50, 1900 - 28 * (len(rows) - r)))
    LX.draw_pose(c, t, CUES, WORDS_ALL, 880, 1920 - 205 + 30, 410)
    LX.flash(c, t, SWITCH)
    return np.asarray(c.convert('RGB'))


def render(t):
    LOOP = 0.6
    if t > DUR - LOOP:
        a = _render(t).astype(np.float32); b = _render(0.4, True).astype(np.float32); q = eio((t - (DUR - LOOP)) / LOOP)
        return (a * (1 - q) + b * q).astype(np.uint8)
    return _render(t)


if __name__ == '__main__':
    import sys
    ts = [float(x) for x in sys.argv[1:]] or [3, 10, 15, 21, 27, 33, 40, 46, 48.5, 55, 62, 70, 76, 81]
    ims = [Image.fromarray(render(x)).resize((270, 480)) for x in ts]
    sheet = Image.new('RGB', (270 * 7, 480 * ((len(ims) + 6) // 7)), (0, 0, 0))
    for k, im in enumerate(ims): sheet.paste(im, ((k % 7) * 270, (k // 7) * 480))
    sheet.save('/tmp/claude-0/-home-claude/32ef0837-6367-50a7-8b18-d49a84afef86/scratchpad/op_sheet.jpg', quality=88)
    print('DUR', round(DUR, 2), [round(s, 2) for s in STARTS])
