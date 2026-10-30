"""usstock: 'Don't buy a US stock before you know these 5 things' (LISTX style, male VO)."""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, re
import numpy as np
from PIL import Image, ImageDraw
from lib import *
import listx as LX
from listx import INKL, ACC, MUTE

SH = ROOT + 'usstock/'
SCRIPT = json.load(open(SH + 'script.json'))
DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO, DUR = LX.timing(SCRIPT, DURS)
WORDS = LX.word_times(SCRIPT, DURS, VO)
def _merge(i, a, b, new):
    ws = WORDS[i]
    for k in range(len(ws) - 1):
        if ws[k][0] == a and ws[k + 1][0] == b:
            ws[k] = (new, ws[k][1]); del ws[k + 1]; return


_merge(2, 'IND', 'money', 'INDmoney'); _merge(2, 'W-8', 'BEN,', 'W-8BEN,'); _merge(6, 'F', 'A.', 'FA.')
ALLW = [w for seg in WORDS for w in seg]
RED = (225, 80, 70)
LIGHTT = (240, 240, 240)

ACCENTS = [["five things."], ["How to buy."], ["W-8BEN,", "fraction"], ["real cost."],
           ["half to one point two percent", "point two five percent", "twenty percent TCS", "claim it back"],
           ["Tax.", "surprises"], ["slab rate.", "twelve point five percent.", "twenty five percent", "Schedule FA."],
           ["Pros and cons."], ["Pros.", "Cons.", "biggest companies,", "dollar rises.", "both ways,", "late at night,", "stronger rupee"],
           ["already use."], [], ["Not a buy call,", "Save this,"]]
DARK = {3, 4, 7, 8}
SWITCH = [STARTS[k] for k in (3, 5, 7, 9, 11)]
NI = 5
FILL = [VO[1 + 2 * k] + 0.5 for k in range(NI)]
ICONS = [LX.ico_phone, LX.ico_swap, LX.ico_taxdoc, LX.ico_scale, LX.ico_grid10]
NAMES = ['How to buy', 'The real cost', 'Tax', 'Pros & cons', '10 companies']
PILLS = ['4 STEPS · FRACTIONS OK', 'FX + BROKERAGE + TCS', 'THE 2-YEAR LINE', 'KNOW BOTH SIDES', 'YOU USE THEM DAILY']
SLUGS = ['how to buy', 'real cost', 'tax', 'pros & cons', 'the 10']
SRC = ['Steps as in the INDmoney app (Oct 2026) · app I use',
       'FX 0.5-1.2% & brokerage 0.25% (max $25) + GST: INDmoney · TCS: Business Today, Oct 2026',
       'Tax rules: Tickertape (Sep 2026) · ask a CA for your case',
       'NYSE 9:30 AM-4 PM New York = 8 PM-2:30 AM IST (from 2 Nov 2026)',
       'Prices: INDmoney live, 30 Oct 2026, 11:09 PM IST · not a buy/sell call']
CO = [('Google', 'GOOGL', 278.94, 'Search, YouTube'), ('Apple', 'AAPL', 346.27, 'iPhone, Mac'),
      ('Microsoft', 'MSFT', 519.98, 'Windows, Office'), ('Amazon', 'AMZN', 239.11, 'Shopping, Prime'),
      ('Meta', 'META', 618.21, 'Instagram, WhatsApp'), ('Netflix', 'NFLX', 62.11, 'Streaming'),
      ('Nvidia', 'NVDA', 203.15, 'AI & gaming chips'), ('Visa', 'V', 416.28, 'Card payments'),
      ('Coca-Cola', 'KO', 94.60, 'Coke, Thums Up'), ("McDonald's", 'MCD', 259.49, 'Burgers')]


def acc_idx(i):
    ws = [w for w, _ in WORDS[i]]; out = set()
    for ph in ACCENTS[i]:
        p = ph.split(' ')
        for k in range(len(ws) - len(p) + 1):
            if ws[k:k + len(p)] == p: out |= set(range(k, k + len(p))); break
    return out


ACC_IDX = [acc_idx(i) for i in range(len(SCRIPT))]


def pages(i):
    """split a segment's words into sentence pages so the headline never overflows"""
    ws = WORDS[i]; out = []; st = 0
    for k, (w, _) in enumerate(ws):
        if re.search(r'[.?!]$', w) and k < len(ws) - 1 and k - st >= 3:
            out.append((st, k + 1)); st = k + 1
    out.append((st, len(ws)))
    # merge tiny pages (e.g. 'Pros.' 'Cons.') with the next one
    merged = []
    for a, b in out:
        if merged and merged[-1][1] - merged[-1][0] <= 2: merged[-1] = (merged[-1][0], b)
        else: merged.append((a, b))
    return merged


PAGES = [pages(i) for i in range(len(SCRIPT))]


def seg_at(t):
    i = 0
    for k, s in enumerate(STARTS):
        if t >= s: i = k
    return i


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def head(c, t, i, dark):
    pg = PAGES[i][0]
    for a, b in PAGES[i]:
        if t >= WORDS[i][a][1] - 0.05: pg = (a, b)
    a, b = pg; ws = WORDS[i][a:b]
    txt = ' '.join(w for w, _ in ws); n = len(txt)
    size = 70 if n < 40 else 62 if n < 75 else 56
    LX.headline(c, t, ws, {k - a for k in ACC_IDX[i] if a <= k < b}, size=size,
                col=LIGHTT if dark else INKL, hl=(30, 80, 58) if dark else LX.ACC_SOFT)


def pop_in(t, t0, d=0.3):
    return eback(prog(t, t0, d), 1.7) if t >= t0 else 0


# ---------------- visuals ----------------
def v_intro(c, t):
    p = pop_in(t, VO[0] + 0.2, 0.4)
    if p: place(c, text_img('0/5', 'pop', 300, INKL), 640, 980, p)
    LX.sticker(c, t, at(0, "Don't"), "DON'T BUY YET", 660, 790, -7, 44)
    LX.sticker(c, t, at(0, 'five'), '5 THINGS FIRST', 690, 1170, 5, 40)


def step_card(c, t, t0, n, title, sub, x, y, w=500, dark=False):
    if t < t0: return
    q = eo(prog(t, t0, 0.3)); xo = (1 - q) * 80
    im = card_img(n, title, sub, w)
    place(c, im, x + w / 2 + xo, y, 1, 0, q)


@functools.lru_cache(32)
def card_img(n, title, sub, w):
    h = 104; im = Image.new('RGBA', (w + 10, h + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((8, 8, w + 8, h + 8), 18, fill=INKL)
    d.rounded_rectangle((0, 0, w, h), 18, fill=(252, 252, 250), outline=INKL, width=4)
    d.ellipse((18, 26, 70, 78), fill=ACC); nt = text_img(str(n), 'pop', 32, (252, 252, 250)); im.alpha_composite(nt, (44 - nt.size[0] // 2, 28))
    im.alpha_composite(text_img(title, 'pop', 34, INKL), (88, 12))
    im.alpha_composite(text_img(sub, 'type', 22, MUTE), (90, 64))
    return im


def v_buy(c, t):
    rows = [('open US stocks', 'Open US stocks', 'inside the INDmoney app'),
            ('KYC', 'Finish KYC', 'PAN, address, bank'),
            ('W-8', 'Sign form W-8BEN', 'US dividend tax 30% -> 25%'),
            ('add money', 'Add money', 'rupees go out under LRS'),
            ('and buy', 'Buy', 'even a fraction of 1 share')]
    for k, (ph, ti, sb) in enumerate(rows):
        step_card(c, t, at(2, ph, -0.15), k + 1, ti, sb, 500, 800 + k * 112)
    if t > at(2, 'fraction'):
        # fraction pie
        q = eo(prog(t, at(2, 'fraction'), 0.8)); d = ImageDraw.Draw(c); cx, cy, r = 250, 880, 110
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(252, 252, 250), outline=INKL, width=6)
        d.pieslice((cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8), -90, -90 + 36 * q, fill=ACC)
        place(c, text_img('0.1 SHARE', 'type', 26, INKL, 2), cx, cy + r + 30)


@functools.lru_cache(16)
def cost_row(label, big, sub, w=520):
    h = 150; im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 20, fill=(32, 34, 36), outline=(80, 84, 88), width=3)
    im.alpha_composite(text_img(label, 'type', 22, (170, 170, 170), 2), (24, 14))
    im.alpha_composite(text_img(big, 'pop', 48, ACC), (24, 40))
    im.alpha_composite(text_img(sub, 'type', 22, (220, 220, 220)), (24, 108))
    return im


def v_cost(c, t):
    p = pop_in(t, VO[4] + 0.1, 0.45)
    if p: place(c, swap_img(), 270, 900, p)
    rows = [('half to one', 'FX CONVERSION', '0.5% - 1.2%', 'charged by your bank'),
            ('Brokerage', 'BROKERAGE', '0.25% a trade', '+ GST, max $25 per trade'),
            ('Above ten lakh', 'TCS (ABOVE ₹10 LAKH/YR)', '20%', 'only on the extra · claim back in ITR')]
    for k, (ph, a, b, s) in enumerate(rows):
        t0 = at(4, ph, -0.2)
        if t > t0:
            q = eo(prog(t, t0, 0.3)); place(c, cost_row(a, b, s), 780 + (1 - q) * 60, 830 + k * 170, 1, 0, q)
    t1 = at(4, 'GST', 0.6)
    if t > t1:
        v = 100000 - 1292 * eo(prog(t, t1, 1.2))
        place(c, text_img('ON ₹1 LAKH (AT 1% FX):', 'type', 24, (190, 190, 190), 2), 270, 1080)
        place(c, text_img(f'₹{int(v):,}'.replace(',', '_').replace('_', ','), 'pop', 64, LIGHTT), 270, 1140)
        place(c, text_img('reaches the stock', 'type', 22, (190, 190, 190)), 270, 1195)
    LX.sticker(c, t, at(4, 'claim it back'), 'TCS IS NOT LOST', 300, 1330, -6, 32)


@functools.lru_cache(2)
def swap_img():
    im = Image.new('RGBA', (420, 300), (0, 0, 0, 0)); LX.ico_swap(im, 210, 170, 1.7); return im


def v_tax(c, t):
    d = ImageDraw.Draw(c); x0, x1, y = 110, 990, 930; mid = x0 + (x1 - x0) * 0.5
    t0 = at(6, 'Sell'); t2 = at(6, 'Hold')
    if t > t0:
        q = eo(prog(t, t0, 0.5))
        d.rounded_rectangle((x0, y - 22, x0 + (mid - x0) * q, y + 22), 12, fill=RED, outline=INKL, width=4)
        place(c, text_img('SELL WITHIN 2 YEARS', 'type', 24, MUTE, 2), (x0 + mid) / 2, y - 90)
        if t > at(6, 'slab'): place(c, text_img('YOUR SLAB RATE', 'pop', 40, RED), (x0 + mid) / 2, y + 70, pop_in(t, at(6, 'slab')))
    if t > t2:
        q = eo(prog(t, t2, 0.5))
        d.rounded_rectangle((mid, y - 22, mid + (x1 - mid) * q, y + 22), 12, fill=ACC, outline=INKL, width=4)
        place(c, text_img('HOLD 2+ YEARS', 'type', 24, MUTE, 2), (mid + x1) / 2, y - 90)
        if t > at(6, 'twelve'):
            v = 12.5 * eo(prog(t, at(6, 'twelve'), 0.8))
            place(c, text_img(f'{v:.1f}%', 'pop', 64, ACC), (mid + x1) / 2, y + 80)
            place(c, text_img('+ surcharge & cess', 'type', 22, MUTE), (mid + x1) / 2, y + 135)
    if t > t0:
        place(c, text_img('24 MONTHS', 'type', 22, INKL, 2), mid, y - 46)
        d.line((mid, y - 30, mid, y + 30), fill=INKL, width=5)
        # marker travelling along the holding period
        u = clamp((t - t0) / max(0.1, at(6, 'Dividends') - t0))
        mx = x0 + (x1 - x0) * u; d.ellipse((mx - 16, y - 16, mx + 16, y + 16), fill=(252, 252, 250), outline=INKL, width=5)
    td = at(6, 'Dividends')
    if t > td:
        v = 100 - 25 * eo(prog(t, td + 0.5, 0.8))
        place(c, text_img('$100 DIVIDEND', 'type', 26, MUTE, 2), 300, 1060)
        place(c, text_img(f'${v:.0f}', 'pop', 84, INKL), 300, 1125)
        if t > at(6, 'claim'): LX.sticker(c, t, at(6, 'claim'), 'CLAIM CREDIT IN INDIA', 760, 1110, 4, 32)
    LX.sticker(c, t, at(6, 'Schedule'), 'REPORT IN SCHEDULE FA', 770, 1290, -5, 34)


@functools.lru_cache(16)
def pc_row(txt, good, w=440):
    h = 92; im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 18, fill=(32, 34, 36), outline=(80, 84, 88), width=3)
    col = ACC if good else RED
    d.ellipse((16, 22, 64, 70), fill=col)
    if good: d.line([(28, 46), (38, 57), (54, 36)], fill=(252, 252, 250), width=6)
    else: d.line((30, 36, 50, 56), fill=(252, 252, 250), width=6); d.line((50, 36, 30, 56), fill=(252, 252, 250), width=6)
    f = 30
    while text_w(txt, 'pop', f) > w - 100 and f > 18: f -= 2
    ti = text_img(txt, 'pop', f, LIGHTT); im.alpha_composite(ti, (80, (h - ti.size[1]) // 2 - 4))
    return im


def v_pc(c, t):
    place(c, text_img('PROS', 'pop', 46, ACC), 290, 800); place(c, text_img('CONS', 'pop', 46, RED), 790, 800)
    pros = [('biggest', "World's biggest companies"), ('dollar rises', 'Gain if the dollar rises')]
    cons = [('both ways', 'FX cost in and out'), ('late at night', 'Opens 8 PM IST (winter)'), ('stronger rupee', 'Strong rupee cuts returns')]
    for k, (ph, tx) in enumerate(pros):
        t0 = at(8, ph, -0.3)
        if t > t0: place(c, pc_row(tx, True), 290, 900 + k * 110, pop_in(t, t0, 0.25))
    for k, (ph, tx) in enumerate(cons):
        t0 = at(8, ph, -0.3)
        if t > t0: place(c, pc_row(tx, False), 790, 900 + k * 110, pop_in(t, t0, 0.25))


@functools.lru_cache(16)
def co_card(k):
    name, tk, px, use = CO[k]; w, h = 460, 96
    im = Image.new('RGBA', (w + 8, h + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((7, 7, w + 7, h + 7), 16, fill=INKL)
    d.rounded_rectangle((0, 0, w, h), 16, fill=(252, 252, 250), outline=INKL, width=4)
    nb = text_img(str(k + 1), 'pop', 24, (252, 252, 250)); d.ellipse((12, 12, 46, 46), fill=ACC); im.alpha_composite(nb, (29 - nb.size[0] // 2, 13))
    im.alpha_composite(text_img(name, 'pop', 32, INKL), (56, 6))
    im.alpha_composite(text_img(use, 'type', 20, MUTE), (58, 58))
    pt = text_img(f'${px:,.2f}', 'pop', 30, ACC); im.alpha_composite(pt, (w - 18 - pt.size[0], 8))
    tt = text_img(tk, 'type', 20, INKL, 2); im.alpha_composite(tt, (w - 18 - tt.size[0], 58))
    return im


def v_ten(c, t, title_seg=False):
    ws = WORDS[10]
    for k in range(10):
        r, q = divmod(k, 2) if False else (k % 5, k // 5)
        x = 300 + q * 490; y = 800 + r * 112
        tk = ws[k][1] if k < len(ws) else 1e9
        if t < tk - 0.1:
            d = ImageDraw.Draw(c)
            for s in range(0, 460, 16): d.line((x - 230 + s, y - 48, x - 230 + s + 8, y - 48), fill=(170, 170, 170), width=2); d.line((x - 230 + s, y + 48, x - 230 + s + 8, y + 48), fill=(170, 170, 170), width=2)
            place(c, text_img('?', 'pop', 40, (170, 170, 170)), x, y)
        else:
            place(c, co_card(k), x, y, pop_in(t, tk - 0.1, 0.25))


def v_outro(c, t):
    p = pop_in(t, VO[11], 0.4)
    if p: place(c, text_img('5/5', 'pop', 260, ACC), 680, 900, p)
    LX.sticker(c, t, at(11, 'Not a buy'), 'NOT A BUY CALL', 690, 1100, -5, 40)
    LX.sticker(c, t, at(11, 'Save'), 'SAVE', 900, 1270, 7, 52)
    LX.sticker(c, t, at(11, 'send'), 'SEND TO THAT FRIEND', 710, 1420, -6, 36)


VIS = {0: v_intro, 2: v_buy, 4: v_cost, 6: v_tax, 8: v_pc, 9: v_ten, 10: v_ten, 11: v_outro}


@functools.lru_cache(8)
def big_icon(k):
    im = Image.new('RGBA', (600, 600), (0, 0, 0, 0)); ICONS[k](im, 300, 300, 2.0); return im


def _render(t, loop=False):
    i = seg_at(t); dark = i in DARK
    c = LX.bg_cached(dark)
    item = (i - 1) // 2 if 1 <= i <= 2 * NI else None
    done = sum(1 for ft in FILL if t > ft)
    LX.hud(c, t, item + 2 if item is not None else (1 if i == 0 else NI + 2),
           f'#{item + 1} · {SLUGS[item]}' if item is not None else ('before you buy' if i == 0 else 'ready'),
           done, NI, dark, 'LEARNED')
    head(c, t, i, dark)
    if item is not None:
        LX.item_title(c, t, VO[1 + 2 * item], item + 1, NAMES[item], PILLS[item], ICONS[item], y=640, dark=dark)
        if i % 2 == 1 and i != 9:
            q = pop_in(t, VO[i] + 0.15, 0.45)
            if q > 0.02: place(c, big_icon(item), 720, 1050, q, math.sin(t * 2) * 3)
    if i in VIS: VIS[i](c, t)
    if item is not None and t > VO[1 + 2 * item]:
        c.alpha_composite(text_img(SRC[item], 'type', 21, (150, 150, 150) if dark else MUTE), (60, 1870))
    if i in (0, 11):
        c.alpha_composite(text_img('Not a buy/sell call. Education only.', 'type', 22, MUTE), (60, 1870))
    LX.shelf(c, t, 560, 1690, NI, FILL, ICONS, w=470, dark=dark, label='WHAT YOU KNOW')
    LX.draw_host(c, t, ALLW, big=not dark and i not in (9, 10))
    LX.flash(c, t, SWITCH)
    return np.asarray(c.convert('RGB'))


def render(t):
    LOOP = 0.6
    if t > DUR - LOOP:
        a = _render(t).astype(np.float32); b = _render(0.35, True).astype(np.float32); q = eio((t - (DUR - LOOP)) / LOOP)
        return (a * (1 - q) + b * q).astype(np.uint8)
    return _render(t)


if __name__ == '__main__':
    import sys
    ts = [float(x) for x in sys.argv[1:]] or [1.5, 6, 12, 16, 22, 30, 36, 40, 46, 52, 58, 64, 68, 71, 74, 78]
    ims = [Image.fromarray(render(x)).resize((270, 480)) for x in ts]
    sheet = Image.new('RGB', (270 * 8, 480 * ((len(ims) + 7) // 8)), (0, 0, 0))
    for k, im in enumerate(ims): sheet.paste(im, ((k % 8) * 270, (k // 8) * 480))
    sheet.save('/tmp/claude-0/-home-claude/32ef0837-6367-50a7-8b18-d49a84afef86/scratchpad/us_sheet.jpg', quality=88)
    print('DUR', round(DUR, 2), [round(s, 2) for s in STARTS])
