"""Office agent explainer: chatbot vs agent, goal -> plan -> tools -> check -> you approve, 3 rules, comment AGENT (collage, male VO)"""
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

SH = ROOT + 'offagent/'
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
@functools.lru_cache(None)
def card(w, h, fill=(253, 251, 246)):
    return cutout(Image.new('RGBA', (w, h), fill + (255,)), border=5, shadow=0.35)


def tickbox(c, x, y, on, s=46):
    d = ImageDraw.Draw(c)
    d.rounded_rectangle((x - s / 2, y - s / 2, x + s / 2, y + s / 2), 8, fill=(253, 251, 246), outline=INK, width=5)
    if on > 0:
        k = min(1, on)
        pts = [(x - 14, y + 2), (x - 3, y + 14), (x + 18, y - 16)]
        d.line([pts[0], pts[1]] if k < 0.5 else pts, fill=GRN, width=9, joint='curve')


def s1(c, t):
    i = 0
    dy, a = drop(t, 0.1, 360)
    if a > 0: place(c, SZ.clipping(1.0, 'THE OFFICE AGENT', 'AI AT WORK', 'YOUR NEW DIGITAL COLLEAGUE'), 540, 420 + dy, 0.95, -3, a)
    tb = at(i, 'boring', -0.2)
    if t > tb:
        place(c, card(760, 300), 540, 820, pp(t, tb), 2)
        if t > tb + 0.2:
            place(c, text_img('DAILY SALES REPORT', 'anton', 66, INK), 540, 770)
            place(c, text_img('copy · paste · format · repeat', 'type', 32, GREY, 1), 540, 860)
    tc = at(i, 'coffee', -0.4)
    if t > tc:
        sc, a2 = slam(t, tc); place(c, stamp_c('DONE BY 9:00 AM', GRN, 90, -6, 3), 540, 1150, sc, 0, a2)
        place_text(c, 'while you sip your coffee', 'mark', 50, INK, 540, 1310, t, 'cf', tc + 0.4, 'slide', rot=-2)


def s2(c, t):
    i = 1; T0 = STARTS[i]
    place_text(c, 'CHATBOT vs AGENT', 'anton', 110, INK, 540, 260, t, 'cv', T0 + 0.05, 'pop')
    tc = at(i, 'chatbot answers', -0.2) if 'chatbot answers' in SCRIPT[i] else at(i, 'A chatbot', -0.2)
    if t > tc:
        place(c, card(440, 560), 290, 760, pp(t, tc), -3)
        if t > tc + 0.2:
            place(c, text_img('CHATBOT', 'anton', 64, GREY), 290, 560)
            place(c, label('ANSWERS', NAVY), 290, 700)
            place(c, text_img('you still do', 'type', 30, GREY, 1), 290, 830)
            place(c, text_img('the work', 'type', 30, GREY, 1), 290, 870)
    ta = at(i, 'An agent', -0.2)
    if t > ta:
        place(c, card(440, 560), 790, 760, pp(t, ta), 3)
        if t > ta + 0.2:
            place(c, text_img('AGENT', 'anton', 64, INK), 790, 560)
            place(c, label('DOES THE WORK', GRN), 790, 700)
            place(c, text_img('plans · acts', 'type', 30, GREY, 1), 790, 830)
            place(c, text_img('checks · asks you', 'type', 30, GREY, 1), 790, 870)
    tw = at(i, 'the work', 0.0)
    if t > tw:
        sc, a = slam(t, tw); place(c, stamp_c('ACTION, NOT CHAT', RED, 84, -5, 9), 540, 1200, sc, 0, a)


def s3(c, t):
    i = 2; T0 = STARTS[i]
    place_text(c, 'STEP 1: ONE GOAL', 'anton', 110, INK, 540, 260, t, 'g1', T0 + 0.05, 'pop')
    p = pp(t, T0 + 0.2, 0.4)
    place(c, cutout(Image.new('RGBA', (820, 520), (255, 236, 140, 255)), border=0, shadow=0.4), 540, 760, p, -2)
    typed(c, 'Every morning:', 'mark', 56, INK, 620, t, at(i, 'Every morning', -0.2), at(i, 'Every morning', 0.5))
    typed(c, "yesterday's sales emails", 'mark', 52, INK, 720, t, at(i, 'yesterday', -0.2), at(i, 'into', 0))
    typed(c, '-> ONE table', 'mark', 60, RED, 830, t, at(i, 'one table', -0.2), at(i, 'one table', 0.4))
    src(c, t, 'Example task. Start with one small, repeating job.', T0 + 1.0, 1720)


def s4(c, t):
    i = 3; T0 = STARTS[i]
    place_text(c, 'STEP 2: IT PLANS', 'anton', 110, INK, 540, 260, t, 'g2', T0 + 0.05, 'pop')
    place(c, card(880, 820), 540, 820, pp(t, T0 + 0.15), -1)
    steps = [('Open the inbox', 'Open the inbox'), ('Read the Sales folder', 'Read the sales'), ('Pull: customer', 'customer'), ('Pull: request', 'request'), ('Pull: deadline', 'deadline')]
    for k, (txt, ph) in enumerate(steps):
        tk = at(i, ph, -0.2)
        if t < tk: continue
        y = 520 + k * 140
        tickbox(c, 190, y, prog(t, tk + 0.3, 0.3) * 2)
        c.alpha_composite(text_img(txt, 'osw5', 52, INK), (250, int(y - 34)))


def s5(c, t):
    i = 4; T0 = STARTS[i]
    place_text(c, 'STEP 3: TOOLS', 'anton', 110, INK, 540, 260, t, 'g3', T0 + 0.05, 'pop')
    for k, (nm, col, ph) in enumerate((('EMAIL', NAVY, 'Email'), ('SHEETS', GRN, 'sheets'), ('FILES', ORG, 'files'))):
        tk = at(i, ph, -0.2)
        if t < tk: continue
        x = 220 + k * 320
        place(c, card(260, 260), x, 620, pp(t, tk), (-4, 2, 5)[k])
        place(c, label(nm, col), x, 620, pp(t, tk + 0.1))
    tc = at(i, 'checks', -0.3)
    if t > tc:
        place(c, card(840, 330), 540, 1050, pp(t, tc), 1)
        if t > tc + 0.2:
            d = ImageDraw.Draw(c)
            for r in range(4):
                y = 930 + r * 62
                d.line((170, y + 30, 910, y + 30), fill=GREY, width=2)
                for cx in (300, 560, 800):
                    c.alpha_composite(text_img(('CUSTOMER', 'REQUEST', 'DEADLINE')[(cx - 300) // 250] if r == 0 else '········', 'osw5', 30, INK if r == 0 else GREY), (cx - 90, y - 6))
        sc, a = slam(t, tc + 0.5); place(c, stamp_c('SELF-CHECKED', GRN, 80, -6, 21), 700, 1300, sc, 0, a)


def s6(c, t):
    i = 5; T0 = STARTS[i]
    place_text(c, 'STEP 4: IT ASKS YOU', 'anton', 100, INK, 540, 260, t, 'g4', T0 + 0.05, 'pop')
    ta = at(i, 'asks you', -0.3)
    if t > ta:
        place(c, card(800, 360), 540, 640, pp(t, ta), -1)
        if t > ta + 0.2:
            place(c, text_img('Report ready. Send to team?', 'osw5', 46, INK), 540, 560)
            d = ImageDraw.Draw(c)
            d.rounded_rectangle((330, 640, 750, 740), 26, fill=GRN, outline=INK, width=6)
            place(c, text_img('SEND', 'anton', 64, CREAM), 540, 690)
    tp = at(i, 'You press', -0.3)
    if t > tp:
        place_text(c, 'YOU press send', 'pfi', 96, INK, 540, 960, t, 'yp', tp, 'pop')
    tn = at(i, 'Not the agent', -0.3)
    if t > tn:
        sc, a = slam(t, tn); place(c, stamp_c('YOUR APPROVAL', RED, 92, 5, 27), 540, 1170, sc, 0, a)


def s7(c, t):
    i = 6; T0 = STARTS[i]
    if t > T0 + 0.1:
        p = prog(t, T0 + 0.1, 0.3); lw = text_w('3 SAFETY RULES', 'osw', 54, 2); x0 = 540 - (lw + 70) / 2
        place(c, warn_icon(YEL), x0 + 28, 262, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
        place(c, text_img('3 SAFETY RULES', 'osw', 54, YEL, 2), x0 + 70 + lw / 2, 260, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
    for k, (h1, ph, col) in enumerate((('1  START READ-ONLY', 'read only', YEL), ('2  APPROVE EVERY SEND', 'Approve', YEL), ('3  NO PASSWORDS / BANK', 'passwords', RED))):
        tk = at(i, ph, -0.3)
        if t < tk: continue
        y = 520 + k * 260; q = pp(t, tk, 0.35, 1.3)
        place(c, cutout(Image.new('RGBA', (920, 200), (40, 38, 36, 255)), border=6, shadow=0.4, bcol=col), 540, y, q, (-0.8, 0.8, -0.5)[k])
        if q > 0.6: place(c, text_img(h1, 'anton', 70, col), 540, y)


def s8(c, t):
    i = 7; T0 = STARTS[i]
    tg = at(i, 'free setup', -0.3)
    if t > tg:
        place(c, card(900, 520), 540, 560, pp(t, tg), -1)
        if t > tg + 0.2:
            place(c, text_img('FREE SETUP GUIDE', 'anton', 80, INK), 540, 420)
            for k, ln in enumerate(['5 steps for your first agent', '3 safety rules', 'one-page checklist']):
                place(c, text_img('• ' + ln, 'osw5', 44, INK), 540, 520 + k * 80, pp(t, tg + 0.3 + 0.15 * k))
    tc = at(i, 'Comment', -0.3)
    if t > tc:
        sc, a = slam(t, tc); place(c, stamp_c('COMMENT "AGENT"', RED, 110, -4, 33), 540, 980, sc, 0, a)
        place_text(c, "I'll DM it to you", 'mark', 56, INK, 540, 1140, t, 'dm', tc + 0.6, 'slide', rot=-2)
    tf = at(i, 'Follow', -0.2)
    if t > tf:
        q2 = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1380, 0.5 + 0.5 * eback(q2), 0, clamp(q2 * 3))
    place_text(c, 'Education only. Check your office IT policy before using any AI tool.', 'type', 22, GREY, 540, 1700, t, None, T0 + 0.3, 'fade', track=1)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
DARK_SCENES = {6}


def slam_times():
    return [at(0, 'coffee', -0.4), at(1, 'the work', 0), at(5, 'Not the agent', -0.3), at(7, 'Comment', -0.3)] + [STARTS[k] + 0.05 for k in range(1, 7)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('AI AT WORK', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
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
