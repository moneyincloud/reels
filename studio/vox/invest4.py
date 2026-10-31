"""invest4: '4 things before you invest' - first reel in the LISTX listicle-explainer style."""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools
import numpy as np
from PIL import Image, ImageDraw
from lib import *
import listx as LX
LX.USE_HOST = True  # published with the avatar before the no-avatar rule
from listx import INKL, ACC, MUTE

SH = ROOT + 'invest4/'
SCRIPT = json.load(open(SH + 'script.json'))
DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO, DUR = LX.timing(SCRIPT, DURS)
WORDS = LX.word_times(SCRIPT, DURS, VO)
ALLW = [w for seg in WORDS for w in seg]

ACCENTS = ["these four.", "emergency fund.", "Six months", "Term insurance.", "ten to fifteen times",
           "Health insurance.", "eleven and a half percent", "index fund SIP.", "eleven percent", "Save this,"]
DARK = {3, 4, 7, 8}
SWITCH = [STARTS[k] for k in (3, 5, 7, 9)]
# item k (0-3) title segment = 1+2k; slot fills when the title is spoken
FILL = [VO[1 + 2 * k] + 0.5 for k in range(4)]
ICONS = [LX.ico_jar, LX.ico_umbrella, LX.ico_heart, LX.ico_plant]
NAMES = ['Emergency fund', 'Term insurance', 'Health insurance', 'Index fund SIP']
PILLS = ['6 MONTHS OF EXPENSES', '10-15x YEARLY INCOME', 'COSTS +11.5% A YEAR', 'NIFTY 50 · LOW COST']
SLUGS = ['emergency fund', 'term insurance', 'health insurance', 'index fund']
SRC = ['rule of thumb used by planners · not a fixed law',
       'rule of thumb used by planners · not a fixed law',
       'Aon Global Medical Trend Rates 2026 · India 11.5%',
       'Nifty 50 TRI 20-yr CAGR 11.2% · FundsIndia (Apr 2026) · past returns, not a promise']


def acc_idx(i):
    ph = ACCENTS[i].split(' '); ws = [w for w, _ in WORDS[i]]
    for k in range(len(ws) - len(ph) + 1):
        if ws[k:k + len(ph)] == ph: return set(range(k, k + len(ph)))
    return set()


ACC_IDX = [acc_idx(i) for i in range(len(SCRIPT))]


def seg_at(t):
    i = 0
    for k, s in enumerate(STARTS):
        if t >= s: i = k
    return i


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    return VO[i] + DURS[i] * (max(0, k) / len(s)) + off


def hsize(i):
    n = len(SCRIPT[i])
    return 70 if n < 40 else 62 if n < 80 else 56


# ---------------- visuals ----------------
def v_intro(c, t):
    i = 0
    p = eback(prog(t, VO[0] + 0.2, 0.4), 1.5)
    place(c, text_img('0/4', 'pop', 300, INKL), 620, 980, p)
    LX.sticker(c, t, at(0, "Don't"), "DON'T INVEST YET", 640, 800, -7, 44)
    LX.sticker(c, t, at(0, 'four'), 'SET UP 4 THINGS', 660, 1170, 5, 40)


def v_jar(c, t):
    t0 = VO[2]; f = eo(prog(t, at(2, 'Six'), 2.2))
    cx, cy = 720, 1020; s = 1.6
    LX.ico_jar(c, cx, cy, s, fill=f * 0.9)
    d = ImageDraw.Draw(c); ly = cy + 100 * s - 12 * s - (200 * s - 50 * s) * 0.9
    for x in range(int(cx - 170), int(cx + 170), 22): d.line((x, ly, x + 12, ly), fill=ACC, width=4)
    if t > at(2, 'Six'):
        m = 1 + int(f * 5.999)
        place(c, text_img(f'MONTH {m}', 'type', 34, INKL, 2), cx + 250, ly - 2)
    LX.sticker(c, t, at(2, 'job loss'), 'NO PANIC SELLING', 760, 1340, -4, 36)
    LX.sticker(c, t, at(2, 'Six', 0.6), 'rule of thumb', 930, 1220, 8, 30)


def family(c, cx, cy, s, col):
    d = ImageDraw.Draw(c); w = max(3, int(6 * s))
    for dx, h in ((-70, 1.0), (70, 0.95), (0, 0.6)):
        x = cx + dx * s; hh = 120 * s * h; top = cy - hh
        r = 22 * s * (0.8 + 0.2 * h)
        d.ellipse((x - r, top - 2 * r, x + r, top), fill=(250, 250, 248), outline=col, width=w)
        d.line((x, top, x, cy - 30 * s * h), fill=col, width=w)
        d.line((x - 26 * s * h, top + 30 * s * h, x + 26 * s * h, top + 30 * s * h), fill=col, width=w)
        d.line((x, cy - 30 * s * h, x - 20 * s * h, cy + 10 * s), fill=col, width=w)
        d.line((x, cy - 30 * s * h, x + 20 * s * h, cy + 10 * s), fill=col, width=w)


def v_umbrella(c, t):
    col = (235, 235, 235)
    p = eback(prog(t, VO[4] + 0.1, 0.45), 1.6)
    family(c, 720, 1250, 1.2, col)
    # rain
    d = ImageDraw.Draw(c)
    for k in range(26):
        x = 470 + (k * 97) % 520; y = 760 + ((k * 53 + t * 900) % 520)
        if abs(x - 720) < 190 * p and y > 900: continue
        d.line((x, y, x - 8, y + 26), fill=(120, 170, 150), width=4)
    if p > 0.02: place(c, umb_img(), 720, 980 - (1 - p) * 120, p)
    v = 10 + 5 * eo(prog(t, at(4, 'fifteen'), 0.6))
    if t > at(4, 'ten'):
        place(c, text_img(f'{int(round(v))}x', 'pop', 130, ACC), 260, 880)
        place(c, text_img('YEARLY INCOME', 'type', 26, (200, 200, 200), 2), 260, 965)
    LX.sticker(c, t, at(4, 'loans'), 'NO LOANS LEFT BEHIND', 720, 1420, -4, 34)
    LX.sticker(c, t, at(4, 'ten', 0.8), 'rule of thumb', 260, 1050, -8, 30)


@functools.lru_cache(2)
def umb_img():
    im = Image.new('RGBA', (560, 420), (0, 0, 0, 0)); LX.ico_umbrella(im, 280, 250, 2.3); return im


def v_bill(c, t):
    t0 = VO[6]; g = eo(prog(t, at(6, 'Medical'), 3.0))
    d = ImageDraw.Draw(c)
    x0, x1 = 520, 860; yb = 1340; h = 260 + 340 * g
    pts = [(x0, yb - h)]
    for k in range(9): pts.append((x0 + (x1 - x0) * (k + 0.5) / 9, yb - h + (14 if k % 2 == 0 else 0)))
    d.rectangle((x0, yb - h + 14, x1, yb), fill=(252, 252, 250), outline=INKL, width=6)
    d.polygon([(x0, yb - h + 14)] + [(x0 + (x1 - x0) * k / 10, yb - h + (0 if k % 2 else 14)) for k in range(11)], fill=(252, 252, 250))
    d.line([(x0 + (x1 - x0) * k / 10, yb - h + (0 if k % 2 else 14)) for k in range(11)], fill=INKL, width=6)
    hb = text_img('HOSPITAL BILL', 'pop', 30, INKL); c.alpha_composite(hb, (x0 + 30, int(yb - h + 40)))
    n = int((h - 120) / 46)
    for k in range(n):
        y = yb - h + 100 + k * 46
        d.line((x0 + 30, y, x0 + 200, y), fill=(170, 170, 170), width=5)
        d.text((x1 - 140, y - 16), f'{(k + 3) * 13:,}k'.replace('k', ',000'), font=font('type', 24), fill=INKL)
    d.rectangle((x0 + 20, yb - 70, x1 - 20, yb - 66), fill=INKL)
    # heart monitor line at top
    LX.ico_heart(c, 970, 1180, 0.6)
    if t > at(6, 'rising'):
        v = 11.5 * eo(prog(t, at(6, 'rising'), 1.0))
        place(c, text_img(f'+{v:.1f}%', 'pop', 110, ACC), 340, 900)
        place(c, text_img('A YEAR', 'type', 26, MUTE, 2), 340, 975)
    LX.sticker(c, t, at(6, 'One hospital'), '1 BILL = YEARS OF SAVINGS', 760, 1430, 4, 30)


def v_index(c, t):
    col = (235, 235, 235); d = ImageDraw.Draw(c)
    f = eo(prog(t, at(8, 'top fifty'), 1.6)); n = int(f * 50)
    gx, gy, cs = 470, 760, 52
    for k in range(50):
        r, q = divmod(k, 10)
        x = gx + q * cs; y = gy + r * cs
        d.rounded_rectangle((x, y, x + cs - 8, y + cs - 8), 8, fill=ACC if k < n else None, outline=(110, 110, 116), width=3)
    if t > at(8, 'top fifty'):
        place(c, text_img(f'{n} COMPANIES', 'type', 28, (200, 200, 200), 2), gx + 255, gy + 290)
    # rising line
    lp = prog(t, at(8, 'Over twenty'), 1.8)
    if lp > 0:
        ox, oy, w, h = 470, 1380, 520, 300
        d.line((ox, oy, ox + w, oy), fill=(120, 120, 126), width=3)
        pts = []
        for k in range(41):
            u = k / 40
            if u > lp: break
            val = 1.112 ** (u * 20); y = oy - (val - 1) / (1.112 ** 20 - 1) * h
            y += math.sin(k * 1.7) * 10 * (1 - u)
            pts.append((ox + u * w, y))
        if len(pts) > 1: d.line(pts, fill=ACC, width=8, joint='curve')
        d.text((ox, oy + 10), '20 YEARS', font=font('type', 22), fill=(170, 170, 170))
        v = 11.2 * eo(clamp(lp))
        place(c, text_img(f'{v:.1f}%', 'pop', 96, (245, 245, 245)), ox + 120, oy - 230)
        place(c, text_img('A YEAR, NIFTY 50 TRI', 'type', 22, (200, 200, 200), 2), ox + 150, oy - 170)
    LX.sticker(c, t, at(8, 'low cost'), 'LOW COST', 870, 1460, 6, 34)


def v_outro(c, t):
    p = eback(prog(t, VO[9], 0.4), 1.5)
    place(c, text_img('4/4', 'pop', 260, ACC), 680, 940, p)
    LX.sticker(c, t, at(9, 'ready'), 'NOW YOU CAN INVEST', 690, 1130, -5, 40)
    LX.sticker(c, t, at(9, 'Save'), 'SAVE', 900, 1300, 7, 52)
    LX.sticker(c, t, at(9, 'send'), 'SEND TO A FRIEND', 720, 1440, -6, 38)


VIS = {0: v_intro, 2: v_jar, 4: v_umbrella, 6: v_bill, 8: v_index, 9: v_outro}


# ---------------- frame ----------------
def _render(t, loop=False):
    i = seg_at(t); dark = i in DARK
    c = LX.bg_cached(dark)
    item = (i - 1) // 2 if 1 <= i <= 8 else None
    done = sum(1 for ft in FILL if t > ft)
    LX.hud(c, t, item + 2 if item is not None else (1 if i == 0 else 6), f'#{item + 1} · {SLUGS[item]}' if item is not None else ('the list' if i == 0 else 'ready'), done, 4, dark)
    LX.headline(c, t, WORDS[i], ACC_IDX[i], size=hsize(i), col=(240, 240, 240) if dark else INKL,
                hl=(30, 80, 58) if dark else LX.ACC_SOFT)
    if item is not None:
        LX.item_title(c, t, VO[1 + 2 * item], item + 1, NAMES[item], PILLS[item], ICONS[item], y=640, dark=dark)
        if i % 2 == 1:  # title segment: big icon reveal
            q = eback(prog(t, VO[i] + 0.2, 0.45), 1.6)
            if q > 0.02: place(c, big_icon(item), 720, 1050, q, math.sin(t * 2) * 3)
    if i in VIS: VIS[i](c, t)
    if item is not None and t > VO[1 + 2 * item]:
        c.alpha_composite(text_img(SRC[item], 'type', 22, (150, 150, 150) if dark else MUTE), (70, 1868))
    if i in (0, 9):
        c.alpha_composite(text_img('Education only. Not investment advice.', 'type', 22, MUTE), (70, 1868))
    LX.shelf(c, t, 560, 1690, 4, FILL, ICONS, w=470, dark=dark)
    LX.draw_host(c, t, ALLW, big=not dark)
    LX.flash(c, t, SWITCH)
    return np.asarray(c.convert('RGB'))


@functools.lru_cache(4)
def big_icon(k):
    im = Image.new('RGBA', (600, 600), (0, 0, 0, 0))
    ICONS[k](im, 300, 300, 2.1) if k != 1 else LX.ico_umbrella(im, 300, 330, 2.2)
    return im


def render(t):
    LOOP = 0.6
    if t > DUR - LOOP:
        a = _render(t).astype(np.float32); b = _render(0.35, True).astype(np.float32); q = eio((t - (DUR - LOOP)) / LOOP)
        return (a * (1 - q) + b * q).astype(np.uint8)
    return _render(t)


if __name__ == '__main__':
    import sys
    ts = [float(x) for x in sys.argv[1:]] or [0.8, 3.3, 6, 10, 12.5, 17, 20, 25, 30, 35, 42, 46]
    ims = [Image.fromarray(render(x)).resize((270, 480)) for x in ts]
    sheet = Image.new('RGB', (270 * 6, 480 * ((len(ims) + 5) // 6)), (0, 0, 0))
    for k, im in enumerate(ims): sheet.paste(im, ((k % 6) * 270, (k // 6) * 480))
    sheet.save('/tmp/claude-0/-home-claude/32ef0837-6367-50a7-8b18-d49a84afef86/scratchpad/invest4_sheet.jpg', quality=88)
    print('DUR', DUR, [round(s, 2) for s in STARTS])
