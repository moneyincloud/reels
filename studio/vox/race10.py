"""race10: ₹1 lakh, 4 choices, 10 years (cash, SBI FD, Nifty 50 TRI, gold). Race-bar reel, no avatar."""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, re
import numpy as np
from PIL import Image, ImageDraw
from lib import *
import listx as LX
from listx import INKL, ACC, MUTE

SH = ROOT + 'race10/'
SCRIPT = json.load(open(SH + 'script.json'))
DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO, DUR = LX.timing(SCRIPT, DURS)
WORDS = LX.word_times(SCRIPT, DURS, VO)
RED = (225, 80, 70); GOLD = (232, 176, 40); LIGHTT = (240, 240, 240)
DARK = {4, 7}
SWITCH = [STARTS[k] for k in (4, 5, 7, 8)]

ACCENTS = [["Your favourite", "probably lost."], ["never touch it."], ["sixty three percent,", "sixty one thousand"],
           ["One lakh eighty five thousand,", "barely moved."], ["which one won."], ["Two lakh ninety six thousand.", "eleven and a half percent"],
           ["Gold.", "Four lakh seventy one thousand.", "five times"], ["twenty two percent", "don't promise"], ["gold or Nifty.", "send this"]]

# lanes: (name, sub, final ₹ lakh, colour, reveal seg)
LANES = [('Cash', 'in the cupboard', 1.00, (150, 150, 150), 2),
         ('SBI FD', '1-yr, renewed', 1.85, (90, 140, 210), 3),
         ('Nifty 50', 'with dividends', 2.96, ACC, 5),
         ('Gold', 'domestic price', 4.71, GOLD, 6)]
CAGR = ['0%', '6.36%/yr', '11.47%/yr', '16.8%/yr']


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
        if re.search(r'[.?!]$', w) and k < len(ws) - 1 and k - st >= 3 and len(' '.join(x for x, _ in ws[st:k + 1])) > 28:
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


# reveal times: the moment the value is spoken
WORDS_ALL = [w for seg in WORDS for w in seg]
P = lambda tag, k=0: LX.POSE[tag][k]
REVEAL = [at(2, 'Still one lakh'), at(3, 'One lakh eighty'), at(5, 'Two lakh'), at(6, 'Four lakh')]
INTRO = at(1, 'Same one lakh')
CUES = sorted([(0, P('idea')), (at(0, 'probably', -0.1), P('smug')),
        (VO[1], P('inspect')), (VO[2], P('shrug')), (at(2, 'But prices', -0.1), P('stress')), (at(2, 'only what', -0.1), P('cry')),
        (VO[3], P('cross')), (at(3, 'barely', -0.1), P('bored')),
        (VO[4], P('think')), (at(4, 'Most people', -0.1), P('secret')),
        (VO[5], P('typing')), (at(5, 'Two lakh', -0.1), P('proud')), (at(5, 'through', -0.1), P('nervous', 1)),
        (VO[6], P('shock', 3)), (at(6, 'Four lakh', 0.2), P('celebrate', 1)), (at(6, 'Almost five', -0.1), P('celebrate')),
        (VO[7], P('stop')), (at(7, 'fallen', -0.1), P('shock', 4)), (at(7, "The last", -0.1), P('idea')),
        (VO[8], P('think')), (at(8, 'Comment', -0.1), P('point')), (at(8, 'send', -0.1), P('proud', 1))])
X0, X1 = 360, 1010; PER = (X1 - X0) / 5.0
LANE_Y = [800, 1000, 1200, 1400]


# ---------------- line-art lane icons ----------------
def ic_cash(c, cx, cy, s):
    d = ImageDraw.Draw(c)
    for k in range(3):
        o = k * 10 * s
        d.rounded_rectangle((cx - 50 * s + o, cy - 28 * s - o, cx + 50 * s + o, cy + 28 * s - o), 6 * s, fill=(236, 246, 238), outline=INKL, width=max(2, int(5 * s)))
    d.ellipse((cx - 14 * s + 20 * s, cy - 14 * s - 20 * s, cx + 14 * s + 20 * s, cy + 14 * s - 20 * s), outline=INKL, width=max(2, int(4 * s)))


def ic_bank(c, cx, cy, s):
    d = ImageDraw.Draw(c); w = 100 * s
    d.polygon([(cx - w / 2 - 8 * s, cy - 18 * s), (cx, cy - 55 * s), (cx + w / 2 + 8 * s, cy - 18 * s)], fill=(252, 252, 250), outline=INKL)
    d.line([(cx - w / 2 - 8 * s, cy - 18 * s), (cx, cy - 55 * s), (cx + w / 2 + 8 * s, cy - 18 * s), (cx - w / 2 - 8 * s, cy - 18 * s)], fill=INKL, width=max(2, int(5 * s)))
    for k in range(4):
        x = cx - w / 2 + 12 * s + k * 25 * s; d.rectangle((x - 5 * s, cy - 12 * s, x + 5 * s, cy + 34 * s), fill=(252, 252, 250), outline=INKL, width=max(1, int(4 * s)))
    d.rectangle((cx - w / 2 - 8 * s, cy + 36 * s, cx + w / 2 + 8 * s, cy + 48 * s), fill=INKL)


def ic_chart(c, cx, cy, s):
    d = ImageDraw.Draw(c); w, h = 110 * s, 90 * s
    d.line((cx - w / 2, cy - h / 2, cx - w / 2, cy + h / 2, cx + w / 2, cy + h / 2), fill=INKL, width=max(2, int(5 * s)))
    pts = [(cx - w / 2 + 8 * s, cy + 25 * s), (cx - 15 * s, cy - 2 * s), (cx + 5 * s, cy + 12 * s), (cx + w / 2 - 6 * s, cy - h / 2 + 6 * s)]
    d.line(pts, fill=ACC, width=max(3, int(8 * s)), joint='curve')


def ic_gold(c, cx, cy, s):
    d = ImageDraw.Draw(c)
    for dx, dy in ((-30, 14), (30, 14), (0, -22)):
        x, y = cx + dx * s, cy + dy * s
        d.polygon([(x - 34 * s, y + 16 * s), (x + 34 * s, y + 16 * s), (x + 24 * s, y - 16 * s), (x - 24 * s, y - 16 * s)], fill=GOLD)
        d.line([(x - 34 * s, y + 16 * s), (x + 34 * s, y + 16 * s), (x + 24 * s, y - 16 * s), (x - 24 * s, y - 16 * s), (x - 34 * s, y + 16 * s)], fill=INKL, width=max(2, int(5 * s)))


ICS = [ic_cash, ic_bank, ic_chart, ic_gold]


def fmt_l(v):
    return f'₹{v:.2f}L'


def lane(c, t, k, dark):
    name, sub, final, col, seg = LANES[k]; y = LANE_Y[k]; d = ImageDraw.Draw(c)
    if t < INTRO + 0.25 * k: return
    a = clamp((t - INTRO - 0.25 * k) / 0.3)
    fg = LIGHTT if dark else INKL
    # icon tile + name
    tile = (250, 250, 248)
    d.rounded_rectangle((70, y - 52, 174, y + 52), 18, fill=tile, outline=(90, 90, 96) if dark else INKL, width=4)
    ICS[k](c, 122, y + 4, 0.62)
    c.alpha_composite(text_img(name, 'pop', 40, fg), (190, y - 50))
    c.alpha_composite(text_img(sub, 'type', 20, (170, 170, 170) if dark else MUTE), (192, y + 6))
    # track
    d.rounded_rectangle((X0, y - 40, X1, y + 40), 20, fill=(40, 42, 44) if dark else (226, 226, 222))
    # 1 lakh start marker
    xm = X0 + PER * 1.0
    for yy in range(int(y - 44), int(y + 44), 12): d.line((xm, yy, xm, yy + 6), fill=(120, 120, 120), width=3)
    r0 = REVEAL[k]
    if t < r0:
        # waiting: base 1 lakh bar
        w = PER * 1.0 * eo(a)
        d.rounded_rectangle((X0, y - 34, X0 + max(36, w), y + 34), 18, fill=(200, 200, 196) if not dark else (80, 82, 86))
        if k >= 2 and t > STARTS[4] - 0.2:
            pulse = 0.5 + 0.5 * math.sin(t * 8)
            place(c, text_img('?', 'pop', 60, (170, 170, 170)), X0 + PER * 2.5, y, 1 + 0.08 * pulse)
        return
    q = eo(prog(t, r0, 1.6 if k >= 2 else 1.0))
    v = 1.0 + (final - 1.0) * q
    w = PER * v
    d.rounded_rectangle((X0, y - 34, X0 + w, y + 34), 18, fill=col, outline=INKL, width=4)
    if k == 3 and q > 0.3:  # gold shine
        sh = (t * 400) % (w + 200) - 100
        ov = Image.new('RGBA', (80, 60), (255, 255, 255, 90)); c.alpha_composite(ov, (int(X0 + max(0, min(w - 80, sh))), y - 30)) if w > 90 else None
    vt = text_img(fmt_l(v), 'pop', 40, fg)
    vx = X0 + w + 14
    if vx + vt.size[0] > W - 20: vx = X0 + w - vt.size[0] - 14; vt = text_img(fmt_l(v), 'pop', 40, INKL)
    c.alpha_composite(vt, (int(vx), y - 26))
    if q > 0.95:
        ct = text_img(CAGR[k], 'type', 20, (190, 190, 190) if dark else MUTE, 1)
        c.alpha_composite(ct, (int(X0 + 16), y + 44))


def year_ticker(c, t, dark):
    if t < VO[1]: return
    t0 = at(1, 'Ten years'); t1 = at(1, 'Same one lakh')
    q = eo(prog(t, t0, max(0.5, t1 - t0)))
    yr = 2016 + int(round(10 * q))
    fg = LIGHTT if dark else INKL; d = ImageDraw.Draw(c)
    x0, x1, y = 110, 620, 1630
    d.line((x0, y, x1, y), fill=(120, 120, 120), width=4)
    for k in range(11):
        x = x0 + (x1 - x0) * k / 10; d.line((x, y - 10, x, y + 10), fill=(120, 120, 120), width=3)
    xm = x0 + (x1 - x0) * q
    d.line((x0, y, xm, y), fill=ACC, width=8); d.ellipse((xm - 14, y - 14, xm + 14, y + 14), fill=ACC, outline=INKL, width=4)
    c.alpha_composite(text_img('SEP 2016', 'type', 22, MUTE, 2), (x0 - 40, y + 22))
    tt = text_img('SEP 2026', 'type', 22, MUTE, 2); c.alpha_composite(tt, (x1 - tt.size[0] + 40, y + 22))
    place(c, text_img(str(yr), 'pop', 64, fg), xm, y - 60)


# ---------------- per-segment extras ----------------
def v_intro(c, t):
    p = pop_in(t, VO[0] + 0.1, 0.45)
    if p: place(c, bundle_img(), 540, 1000, p, math.sin(t * 2) * 2)
    LX.sticker(c, t, at(0, 'Four'), '4 CHOICES', 300, 1330, -7, 44)
    LX.sticker(c, t, at(0, 'probably'), 'YOURS LOST?', 780, 1360, 6, 44)


@functools.lru_cache(2)
def bundle_img():
    im = Image.new('RGBA', (700, 440), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k in range(4):
        o = k * 16
        d.rounded_rectangle((70 + o, 120 - o, 590 + o, 360 - o), 18, fill=(236, 246, 238), outline=INKL, width=6)
    d.rectangle((110, 90, 170, 330), fill=GOLD, outline=INKL, width=5)
    t = text_img('₹1,00,000', 'pop', 84, INKL); im.alpha_composite(t, (370 - t.size[0] // 2, 140))
    t2 = text_img('IN 2016', 'type', 30, INKL, 3); im.alpha_composite(t2, (370 - t2.size[0] // 2, 250))
    return im


def v_cash_extra(c, t):
    t0 = at(2, 'only what')
    if t > t0:
        y = LANE_Y[0]; q = eo(prog(t, t0, 0.8)); d = ImageDraw.Draw(c)
        w = PER * (1.0 - 0.39 * q)
        # red hatch over the part inflation ate
        for x in range(int(X0 + w), int(X0 + PER), 10): d.line((x, y - 30, x - 14, y + 30), fill=RED, width=3)
        if q > 0.5: LX.sticker(c, t, t0 + 0.4, 'BUYS ONLY ₹61K', 760, y - 70, -4, 32)


def v_fd_extra(c, t):
    LX.sticker(c, t, at(3, 'before tax'), 'BEFORE TAX', 820, LANE_Y[1] - 75, 5, 30)


def v_guess(c, t):
    LX.sticker(c, t, at(4, 'guess'), 'NIFTY OR GOLD?', 560, 560, -4, 48)


def v_gold_extra(c, t):
    if t > at(6, 'Almost five'):
        LX.sticker(c, t, at(6, 'Almost five'), '4.7X', 860, LANE_Y[3] - 90, 8, 50)


def v_twist(c, t):
    t0 = at(7, 'fallen')
    if t > t0:
        y = LANE_Y[3]; q = eo(prog(t, t0, 0.6))
        place(c, arrow_img(), X0 + PER * 3.7, y - 70, 0.6 * q)
        LX.sticker(c, t, at(7, 'twenty two'), '-22% FROM 2026 PEAK', 600, 1560, -4, 42)
    LX.sticker(c, t, at(7, "don't promise"), 'PAST IS NOT A PROMISE', 380, 1680, 3, 34)


@functools.lru_cache(2)
def arrow_img():
    im = Image.new('RGBA', (140, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(45, 0), (95, 0), (95, 120), (135, 120), (70, 195), (5, 120), (45, 120)], fill=RED, outline=INKL)
    d.line([(45, 0), (95, 0), (95, 120), (135, 120), (70, 195), (5, 120), (45, 120), (45, 0)], fill=INKL, width=5)
    return im


def v_cta(c, t):
    LX.sticker(c, t, at(8, 'gold'), 'GOLD', 230, 1560, -6, 60)
    LX.sticker(c, t, at(8, 'Nifty'), 'NIFTY', 540, 1560, 6, 60)
    LX.sticker(c, t, at(8, 'send'), 'SEND TO YOUR FD FRIEND', 380, 1680, -3, 34)


EXTRA = {0: v_intro, 2: v_cash_extra, 3: v_fd_extra, 4: v_guess, 6: v_gold_extra, 7: v_twist, 8: v_cta}


def _render(t, loop=False):
    i = seg_at(t); dark = i in DARK
    c = LX.bg_cached(dark)
    done = sum(1 for r in REVEAL if t > r)
    LX.hud(c, t, min(i + 1, 9), '₹1 lakh · 10 years', done, 4, dark, 'REVEALED')
    head(c, t, i, dark)
    if i >= 1:
        for k in range(4): lane(c, t, k, dark)
    if 1 <= i <= 6: year_ticker(c, t, dark)
    for k in range(i + 1):
        if k in EXTRA and (k == i or k in (2, 3, 6) and i < 7):
            EXTRA[k](c, t)
    src1 = 'Sep 2016-Sep 2026 · Trade Brains, 26 Oct 2026 · FD pre-tax · ~5%/yr inflation assumed'
    src2 = 'Gold -22% from 52-wk high: Gold BeES ₹148.14 -> ₹115.23, INDmoney, 30 Oct 2026'
    col = (150, 150, 150) if dark else MUTE
    parts = []
    if i >= 1: parts.append(src1)
    if i >= 7: parts.append(src2)
    parts.append('Past returns, not a promise. Not a buy/sell call. Education only.' if i >= 1 else 'Not a buy/sell call. Education only.')
    rows = []
    for ptxt in parts:
        cur = ''
        for wd in ptxt.split(' '):
            nxt = (cur + ' ' + wd).strip()
            if text_w(nxt, 'type', 19) > 640 and cur: rows.append(cur); cur = wd
            else: cur = nxt
        rows.append(cur)
    for r, row in enumerate(rows[-5:]):
        c.alpha_composite(text_img(row, 'type', 19, col), (50, 1900 - 30 * (len(rows[-5:]) - r)))
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
    ts = [float(x) for x in sys.argv[1:]] or [2, 7, 12, 18, 24, 30, 34, 40, 45, 50, 55, 60, 64, 70]
    ims = [Image.fromarray(render(x)).resize((270, 480)) for x in ts]
    sheet = Image.new('RGB', (270 * 7, 480 * ((len(ims) + 6) // 7)), (0, 0, 0))
    for k, im in enumerate(ims): sheet.paste(im, ((k % 7) * 270, (k // 7) * 480))
    sheet.save('/tmp/claude-0/-home-claude/32ef0837-6367-50a7-8b18-d49a84afef86/scratchpad/race_sheet.jpg', quality=88)
    print('DUR', round(DUR, 2), [round(s, 2) for s in STARTS], [round(r, 1) for r in REVEAL])
