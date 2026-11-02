"""reliance: best day in 6.5 years - rally or trap? (LISTX + emotion avatar, male VO, 2 Nov 2026)."""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, re
import numpy as np
from PIL import Image, ImageDraw
from lib import *
import listx as LX
from listx import INKL, ACC, MUTE
from onepoint import card, slide_in, catch_row, pop_in

SH = ROOT + 'reliance/'
SCRIPT = json.load(open(SH + 'script.json'))
DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO, DUR = LX.timing(SCRIPT, DURS)
WORDS = LX.word_times(SCRIPT, DURS, VO)
WORDS_ALL = [w for seg in WORDS for w in seg]
RED = (225, 80, 70); LIGHTT = (240, 240, 240); BLUE = (40, 110, 200)
DARK = {5, 6}
SWITCH = [STARTS[k] for k in (5, 7)]
ACCENTS = [["Don't sell", "what changed today."], ["eleven point six percent", "best day", "seventeen percent"],
           ["forty one percent", "twenty five thousand five hundred crore,", "three lakh sixty thousand crore"],
           ["Oil and chemicals.", "sixty eight percent,"], ["thirty six million users", "five hundred and forty two million.", "two hundred and nineteen rupees"],
           ["most people miss."], ["profit fall twenty four percent.", "turn just as fast"],
           ["rally or trap?", "raised its earnings forecasts.", "must deliver.", "retail must recover"], ["hold or sell.", "dead money."]]


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


P = lambda tag, k=0: LX.POSE[tag][k]
CUES = sorted([
    (0, P('stop')), (at(0, 'what changed', -0.1), P('insider')),
    (VO[1], P('gap_up')), (at(1, 'best day', -0.1), P('celebrate')), (at(1, 'Before today', -0.1), P('bear')),
    (VO[2], P('analysis')), (at(2, 'forty one', -0.1), P('jackpot')), (at(2, 'Revenue', -0.1), P('money_rain')),
    (VO[3], P('eureka_up')),
    (VO[4], P('rich_phone')), (at(4, 'each user', -0.1), P('math')),
    (VO[5], P('secret')),
    (VO[6], P('broke')), (at(6, 'oil margins', -0.1), P('speculator')),
    (VO[7], P('think')), (at(7, 'Jefferies', -0.1), P('bull')), (at(7, 'Citi', -0.1), P('analysis')), (at(7, 'For it', -0.1), P('idea')),
    (VO[8], P('point')), (at(8, 'send', -0.1), P('proud', 1))])


@functools.lru_cache(2)
def price_card():
    w, h = 720, 400; im = Image.new('RGBA', (w + 12, h + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 10, w + 10, h + 10), 28, fill=INKL)
    d.rounded_rectangle((0, 0, w, h), 28, fill=(252, 252, 250), outline=INKL, width=6)
    im.alpha_composite(text_img('RELIANCE INDUSTRIES', 'type', 28, MUTE, 3), (40, 34))
    im.alpha_composite(text_img('₹1,300', 'pop', 150, INKL), (36, 70))
    im.alpha_composite(text_img('NSE · CLOSE 2 NOV 2026 (SESSION HIGH)', 'type', 20, MUTE, 2), (42, 262))
    d.rounded_rectangle((40, 302, 340, 356), 27, fill=ACC)
    im.alpha_composite(text_img('+11.6% TODAY', 'pop', 30, (252, 252, 250)), (66, 309))
    return im


def v0(c, t):
    p = pop_in(t, VO[0] + 0.1, 0.4)
    if p: place(c, price_card(), 540, 1000, p, -2)
    LX.sticker(c, t, at(0, 'what changed'), 'WHAT CHANGED?', 560, 1320, 4, 44)


def v1(c, t):
    t0 = at(1, 'eleven')
    if t > t0:
        v = 11.6 * eo(prog(t, t0, 1.0))
        place(c, text_img(f'+{v:.1f}%', 'pop', 200, ACC), 520, 900, pop_in(t, t0, 0.3))
    LX.sticker(c, t, at(1, 'best day'), 'BEST DAY SINCE EARLY 2020', 540, 1080, -4, 40)
    tb = at(1, 'Before today')
    if t > tb:
        q = eo(prog(t, tb, 0.6)); d = ImageDraw.Draw(c); x0, y0 = 160, 1230
        d.text((x0, y0 - 50), '2026 BEFORE TODAY', font=font('type', 24), fill=MUTE)
        d.rounded_rectangle((x0, y0, x0 + 520 * q, y0 + 60), 14, fill=RED, outline=INKL, width=4)
        if q > 0.7: c.alpha_composite(text_img('-17%', 'pop', 48, INKL), (x0 + 540, y0))


def v2(c, t):
    d = ImageDraw.Draw(c); yb, hmax = 1300, 420
    bars = [('Q2 FY26', 18171, (180, 214, 198)), ('Q2 FY27', 25548, ACC)]
    t0 = at(2, 'Profit')
    for k, (lb, v, col) in enumerate(bars):
        tk = t0 + 0.5 * k
        if t < tk: continue
        q = eo(prog(t, tk, 0.6)); h = hmax * v / 25548 * q; x = 160 + k * 230
        d.rounded_rectangle((x, yb - h, x + 170, yb), 14, fill=col, outline=INKL, width=4)
        c.alpha_composite(text_img(lb, 'type', 24, MUTE, 1), (x + 16, yb + 12))
        if q > 0.6:
            vt = text_img(f'₹{int(v * q):,} Cr', 'pop', 34, INKL); c.alpha_composite(vt, (int(x + 85 - vt.size[0] / 2), int(yb - h - 50)))
    if t > t0: c.alpha_composite(text_img('NET PROFIT (OWNERS)', 'type', 22, MUTE, 2), (160, yb + 50))
    LX.sticker(c, t, at(2, 'forty one'), '+41%', 820, 900, -6, 80)
    LX.sticker(c, t, at(2, 'beating'), 'BEAT EST. ₹21,419 Cr', 800, 1060, 4, 30)
    tr = at(2, 'Revenue')
    if t > tr: slide_in(c, t, tr, card('Revenue ₹3,62,268 Cr', '+27.8% vs Q2 FY26', 520), 790, 1220)


def v3(c, t):
    d = ImageDraw.Draw(c); t0 = at(3, 'Earnings')
    q = pop_in(t, VO[3] + 0.1, 0.4)
    if q: place(c, refinery_img(), 300, 900, q)
    if t > t0:
        k = eo(prog(t, t0, 1.0)); v = 15011 + (25203 - 15011) * k
        place(c, text_img(f'₹{int(v):,} Cr', 'pop', 72, INKL), 760, 820)
        place(c, text_img('O2C EBITDA, Q2 FY27', 'type', 22, MUTE, 2), 760, 890)
        LX.sticker(c, t, t0 + 0.6, '+68%', 760, 1000, -5, 70)
    tm = at(3, 'refining margins')
    if t > tm:
        slide_in(c, t, tm, card('Margin 9.3% -> 10.9%', 'EBITDA margin, O2C', 520), 540, 1200)
        LX.sticker(c, t, tm + 0.7, '~85% OF THE PROFIT JUMP', 560, 1340, 3, 30)


@functools.lru_cache(2)
def refinery_img():
    im = Image.new('RGBA', (380, 380), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k, (x, h) in enumerate(((70, 220), (170, 280), (270, 180))):
        d.rounded_rectangle((x - 34, 330 - h, x + 34, 330), 10, fill=(252, 252, 250), outline=INKL, width=6)
        for yy in range(330 - h + 30, 330, 50): d.line((x - 34, yy, x + 34, yy), fill=INKL, width=3)
    d.ellipse((150, 20, 190, 60), fill=(240, 140, 40), outline=INKL, width=4)
    d.rectangle((20, 330, 360, 350), fill=INKL)
    return im


def v4(c, t):
    t0 = at(4, 'Jio added')
    if t > t0:
        k = eo(prog(t, t0 + 0.3, 1.2)); v = 506.4 + 36 * k
        place(c, text_img(f'{v:.1f} M', 'pop', 110, BLUE), 540, 860)
        place(c, text_img('JIO CUSTOMERS', 'type', 26, MUTE, 3), 540, 950)
        LX.sticker(c, t, at(4, 'thirty six'), '+36 MILLION IN A YEAR', 560, 1040, -4, 36)
    ta = at(4, 'each user')
    if t > ta:
        k = eo(prog(t, ta, 1.0)); v = 211.4 + 7.4 * k
        slide_in(c, t, ta, card(f'ARPU ₹{v:.1f} / month', 'was ₹211.4 a year ago', 560), 520, 1220)
        slide_in(c, t, ta + 0.6, card('Jio profit +13.7%', '₹8,387 Cr in Q2', 560), 520, 1340)


def v5(c, t):
    q = pop_in(t, VO[5], 0.35)
    if q: place(c, text_img('BUT...', 'pop', 220, RED), 520, 1050, q, -4)


def v6(c, t):
    rows = [('Retail', 'RELIANCE RETAIL', 'Profit ₹3,449 Cr -> ₹2,611 Cr (-24%)'),
            ('fall', 'RETAIL SALES', 'Revenue only +6.4% (₹91,716 Cr)'),
            ('oil margins', 'O2C RISK', 'Refining margins move with crude & demand')]
    for k, (ph, a, b) in enumerate(rows):
        slide_in(c, t, at(6, ph, -0.2), catch_row(a, b), 540, 820 + k * 160)


def v7(c, t):
    place(c, text_img('RALLY?', 'pop', 40, ACC), 300, 790); place(c, text_img('TRAP?', 'pop', 40, RED), 780, 790)
    good = [('Jefferies', 'O2C record quarter'), ('Jefferies', 'Jio adding users'), ('Jefferies', 'Jefferies: EPS up')]
    bad = [('Citi', 'Retail profit -24%'), ('Citi', 'New energy: unproven'), ('oil margins', 'Margins can reverse')]
    for k, (ph, tx) in enumerate(good):
        t0 = at(7, ph, -0.2 + 0.25 * k)
        if t > t0: place(c, card('+ ' + tx, None, 420, fill=(226, 242, 234), size=30), 300, 890 + k * 100, pop_in(t, t0, 0.25))
    for k, (ph, tx) in enumerate(bad):
        t0 = at(7, ph, -0.2 + 0.25 * k)
        if t > t0: place(c, card('- ' + tx, None, 420, fill=(250, 226, 222), size=30), 780, 890 + k * 100, pop_in(t, t0, 0.25))
    LX.sticker(c, t, at(7, 'For it'), 'WATCH RETAIL NEXT QUARTER', 420, 1260, -4, 36)


def v8(c, t):
    LX.sticker(c, t, at(8, 'hold or'), 'HOLD', 250, 1020, -7, 70)
    LX.sticker(c, t, at(8, 'sell.'), 'SELL', 580, 1020, 6, 70)
    LX.sticker(c, t, at(8, 'Save'), 'SAVE', 300, 1220, 5, 52)
    LX.sticker(c, t, at(8, 'send'), 'SEND TO "DEAD MONEY" FRIEND', 460, 1380, -3, 32)


VIS = [v0, v1, v2, v3, v4, v5, v6, v7, v8]
SRC = ('Price: INDmoney, 2 Nov 2026 · Q2 FY27 results: Reliance via INDmoney blog & Business Recorder (2 Nov 2026) · '
       'Q2 FY26 & O2C/Retail base: back-calculated from reported growth · Analysts: Business Recorder')


def _render(t, loop=False):
    i = seg_at(t); dark = i in DARK
    c = LX.bg_cached(dark)
    hc = (150, 150, 150) if dark else MUTE
    c.alpha_composite(text_img(f'// {i + 1:02d} · RELIANCE · rally or trap?', 'type', 30, hc, 2), (70, 150))
    pr = text_img('NSE ₹1,300 +11.6%', 'type', 30, ACC, 2); c.alpha_composite(pr, (W - 70 - pr.size[0], 150))
    head(c, t, i, dark)
    VIS[i](c, t)
    col = (150, 150, 150) if dark else MUTE
    rows = []
    for ptxt in (SRC, 'Not a buy/sell call. Education only.'):
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
    ts = [float(x) for x in sys.argv[1:]] or [2, 8, 12, 18, 24, 29, 35, 42, 45, 50, 57, 64, 72]
    ims = [Image.fromarray(render(x)).resize((270, 480)) for x in ts]
    sheet = Image.new('RGB', (270 * 7, 480 * ((len(ims) + 6) // 7)), (0, 0, 0))
    for k, im in enumerate(ims): sheet.paste(im, ((k % 7) * 270, (k // 7) * 480))
    sheet.save('/tmp/claude-0/-home-claude/32ef0837-6367-50a7-8b18-d49a84afef86/scratchpad/rel_sheet.jpg', quality=88)
    print('DUR', round(DUR, 2), [round(s, 2) for s in STARTS])
