"""52-week lows v2 — reference template (captions, real charts, counters, progress bar, loop, icons)"""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs
from fridge import follow_btn
import tea as TEA

import os
SH = ROOT + '' + os.environ.get('LDIR', 'indai') + '/'
CAP = os.environ.get('CAP', 'en')
CAPS_ON = os.environ.get('CAPS', '0') == '1'  # owner prefers NO on-screen subtitles
FONTS['ta'] = FD + 'noto-sans-tamil-tamil-800-normal.woff'
SCRIPT = json.load(open(SH + 'script.json'))
DURS = json.load(open(SH + 'vo/durs.json'))
LEAD, TAIL = 0.15, 0.3
STARTS, VO = [], []
_t = 0.0
for i, d in enumerate(DURS):
    STARTS.append(_t); VO.append(_t + (0.1 if i == 0 else LEAD)); _t = VO[-1] + d + TAIL
DUR = _t + 1.8
B = STARTS[1:]
SOFT = (253, 251, 246); NAVY = (30, 60, 120); BLUE = (40, 100, 200); GREY = (120, 116, 108); GOLD = (214, 160, 40)
PINK = (230, 90, 140); TEAL = (20, 140, 130); ORG = (230, 120, 30)
card_box = TEA.card_box; label = TEA.label; coin = TEA.coin

def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def inr(v):
    v = int(round(v)); s = str(abs(v))
    if len(s) > 3:
        h, t3 = s[:-3], s[-3:]; parts = []
        while len(h) > 2: parts.insert(0, h[-2:]); h = h[:-2]
        if h: parts.insert(0, h)
        s = ','.join(parts) + ',' + t3
    return ('-' if v < 0 else '') + '₹' + s


def short(v):
    if v >= 1e7: return f'₹{v / 1e7:.2f} Cr'
    if v >= 1e5: return f'₹{v / 1e5:.1f} L'
    return inr(v)



def biz_card(name, col, tags, w=900):
    h = 150 + 70 * len(tags)
    im = card_box(w, h, SOFT); comp(im, text_img(name, 'anton', 80, col), 40, 24)
    for k, t in enumerate(tags):
        comp(im, text_img('•  ' + t, 'osw', 44, INK), 50, 140 + k * 70)
    return im


def value_line(c, t, t0, v, y=1430, col=GRN, dur=1.2):
    if t < t0: return
    p = eo(prog(t, t0, dur)); vv = 100000 + (v - 100000) * p
    place(c, card_box(820, 200, SOFT), 540, y)
    place(c, text_img('₹1 lakh', 'osw', 56, GREY), 260, y)
    marker_line(c, [(370, y), (450, y)], 1, GREY, 8, head=True, head_size=22)
    place(c, text_img(inr(vv), 'anton', 96, col), 700, y)


def stock_header(c, t, i, n, key):
    nm, col, v, mult = STOCKS[key][:4]
    t0 = STARTS[i] + 0.05
    if t > t0:
        sc, a = slam(t, t0); place(c, stamp_c(f'#{n}', col, 110, -6, 950 + n), 160, 290, sc, 0, a)
    place_text(c, nm, 'anton', 104, INK, 620, 290, t, f'nm{i}', t0 + 0.1, 'pop')


def spark(c, pts, p, col, w=12):
    n = len(pts) - 1; f = p * n; k = int(f); out = pts[:k + 1]
    if k < n: a, b = pts[k], pts[k + 1]; fr = f - k; out = out + [(a[0] + (b[0] - a[0]) * fr, a[1] + (b[1] - a[1]) * fr)]
    if len(out) >= 2: stroke(c, out, w, col)




import textwrap
import saveshare as SS
PURPLE = (120, 70, 200)


@functools.lru_cache(maxsize=None)
def phone_img(w=260, h=470):
    im = Image.new('RGBA', (w + 12, h + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((12, 12, w + 11, h + 11), 40, fill=INK)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 40, fill=(40, 40, 46), outline=INK, width=6)
    d.rounded_rectangle((16, 40, w - 17, h - 40), 18, fill=(235, 245, 255))
    d.rounded_rectangle((w // 2 - 30, 16, w // 2 + 30, 26), 5, fill=(90, 90, 96))
    for k in range(4):  # little chart bars
        bh = (60, 110, 80, 140)[k]; x = 40 + k * 48
        d.rounded_rectangle((x, h - 70 - bh, x + 32, h - 70), 6, fill=(GRN, BLUE, ORG, PURPLE)[k], outline=INK, width=3)
    comp(im, text_img('₹ ••••••', 'anton', 52, INK), 40, 70)
    return im


@functools.lru_cache(maxsize=None)
def laptop_img(w=420, h=280):
    im = Image.new('RGBA', (w + 80, h + 70), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((40, 0, 40 + w, h), 18, fill=(40, 40, 46), outline=INK, width=6)
    d.rounded_rectangle((58, 18, 22 + w, h - 18), 10, fill=(255, 248, 235))
    d.polygon([(0, h + 8), (w + 80, h + 8), (w + 50, h + 60), (30, h + 60)], fill=(200, 196, 188), outline=INK)
    d.line([(0, h + 8), (w + 80, h + 8), (w + 50, h + 60), (30, h + 60), (0, h + 8)], fill=INK, width=5)
    # chat bubbles on screen
    d.rounded_rectangle((190, 40, 440, 90), 16, fill=YEL, outline=INK, width=3)
    d.rounded_rectangle((80, 110, 360, 190), 16, fill=CREAM, outline=INK, width=3)
    for k in range(3): d.line((100, 130 + k * 20, 330 - k * 40, 130 + k * 20), fill=GREY, width=6)
    return im


def bubble(text, me=True, w=820, size=46, blur=False):
    lines = textwrap.wrap(text, 30 if size >= 46 else 36)
    ims = [text_img(l, 'osw', size, INK) for l in lines]
    h = sum(m.size[1] for m in ims) + 12 * (len(ims) - 1) + 50
    ww = min(w, max(m.size[0] for m in ims) + 70)
    im = Image.new('RGBA', (ww + 8, h + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((8, 8, ww + 7, h + 7), 26, fill=INK)
    d.rounded_rectangle((0, 0, ww - 1, h - 1), 26, fill=YEL if me else SOFT, outline=INK, width=5)
    y = 25
    for m in ims: im.alpha_composite(m, (35, y)); y += m.size[1] + 12
    if blur:
        from PIL import ImageFilter
        box = (30, 20, ww - 30, h - 20); reg = im.crop(box).filter(ImageFilter.GaussianBlur(14)); im.paste(reg, box)
    return im


def typed(c, t, t0, text, x, y, me=True, dur=0.9, blur=False, anchor='c'):
    if t < t0: return
    n = max(1, int(len(text) * clamp((t - t0) / dur)))
    b = bubble(text[:n] if not blur else text, me, blur=blur)
    p = eback(prog(t, t0, 0.3), 1.4)
    place(c, b, x, y, p)


def x_mark(c, x, y, k=40, col=RED, w=14):
    d = ImageDraw.Draw(c); d.line((x - k, y - k, x + k, y + k), fill=col, width=w); d.line((x + k, y - k, x - k, y + k), fill=col, width=w)


def icon_card(c, t, t0, n, txt, col, y):
    if t < t0: return
    p = eback(prog(t, t0, 0.4), 1.3)
    place(c, SS._card(880, 150), 540, y, p, (-1, 1, -0.5, 0.8, -0.8)[n % 5])
    if p > 0.6:
        place(c, label(f'{n}/5', col), 190, y, 1.0, -4)
        place(c, text_img(txt, 'anton', 58, INK), 600, y)


def s1(c, t):
    i = 0; T0 = 0.05
    tc = at(i, 'stock portfolio', -0.6)
    q = eio(prog(t, T0, 0.8))
    place(c, phone_img(), 120 + 170 * q, 660, 0.95, -6)
    place(c, laptop_img(), 980 - 200 * q, 640, 0.9, 4)
    if t > T0 + 0.6:
        d = ImageDraw.Draw(c); pr = clamp((t - T0 - 0.6) / 0.5)
        x0, x1 = 420, 560 + 0 * pr; xm = 420 + (560 - 420) * pr
        d.line([(400, 700), (xm, 700)], fill=YEL, width=16); d.line([(400, 700), (xm, 700)], fill=INK, width=4)
        if pr >= 1:
            g = math.exp(-(t - T0 - 1.1) * 4)
            if g > 0.05: d.ellipse((520 - 60 * g, 700 - 60 * g, 520 + 60 * g, 700 + 60 * g), outline=YEL, width=8)
    place_text(c, 'I ASKED AI ABOUT', 'anton', 100, INK, 540, 250, t, 'h1', 0.15, 'pop')
    place_text(c, 'MY ENTIRE PORTFOLIO', 'anton', 96, RED, 540, 370, t, 'h2', 0.35, 'pop')
    t5 = at(i, 'five seconds', -0.3)
    if t > t5:
        s_, a = slam(t, t5); place(c, stamp_c('ANSWERED IN 5 SEC', RED, 92, -5, 501), 540, 1050, s_, 0, a)
    tn = at(i, 'never do', -0.4)
    if t > tn:
        place_text(c, '...and what it can NEVER do', 'mark', 56, NAVY, 540, 1250, t, 'nv', tn, 'slide', rot=-2)
        sh = math.sin(t * 40) * 6 * math.exp(-(t - tn) * 3)
        place(c, text_img('?', 'anton', 200, RED), 540 + sh, 1430, eback(prog(t, tn + 0.2, 0.4), 1.8), 8)


def s2(c, t):
    i = 1
    place_text(c, 'INDMONEY  +  CLAUDE', 'anton', 104, INK, 540, 280, t, 'ic', STARTS[1] + 0.05, 'pop')
    place_text(c, 'now officially connected', 'mark', 56, NAVY, 540, 390, t, 'oc', STARTS[1] + 0.3, 'slide', rot=-2)
    ts = at(i, 'spreadsheets', -0.3)
    if t > ts:
        p = eback(prog(t, ts, 0.4), 1.4); place(c, SS._card(380, 280, (225, 245, 230)), 300, 680, p, -3)
        if p > 0.6:
            d = ImageDraw.Draw(c)
            for r in range(4):
                for k in range(3): d.rectangle((150 + k * 100, 580 + r * 50, 240 + k * 100, 620 + r * 50), outline=GRN, width=3)
            if t > ts + 0.5: x_mark(c, 300, 680, 110)
    tt = at(i, 'ten open tabs', -0.3)
    if t > tt:
        p = eback(prog(t, tt, 0.4), 1.4); place(c, SS._card(380, 280, (225, 235, 255)), 780, 680, p, 3)
        if p > 0.6:
            d = ImageDraw.Draw(c)
            for k in range(5): d.rounded_rectangle((620 + k * 62, 590, 676 + k * 62, 630), 8, fill=(BLUE, ORG, GRN, PURPLE, RED)[k], outline=INK, width=3)
            d.rectangle((620, 630, 940, 780), fill=SOFT, outline=INK, width=4)
            if t > tt + 0.5: x_mark(c, 780, 680, 110)
    tj = at(i, 'You just ask', -0.3)
    typed(c, t, tj, 'Hey Claude, how is my portfolio today?', 540, 1080, True, 1.2)
    if t > tj + 0.8: place(c, label('PLAIN ENGLISH', GRN), 540, 1260, 1.2 * eback(prog(t, tj + 0.8, 0.35), 1.6), -3)


def s3(c, t):
    i = 2
    place_text(c, 'JUST ASK', 'anton', 120, INK, 540, 260, t, 'ja', STARTS[2] + 0.05, 'pop')
    qs = [('Which stock fell the most this month?', 'Which stock'), ('How much is in mutual funds?', 'mutual funds'), ('Is my SIP still running?', 'SIP')]
    for k, (q, ph) in enumerate(qs):
        typed(c, t, at(i, ph, -0.4), q, 600, 430 + k * 170, True, 0.8)
    ta = at(i, 'reads your account', -0.4)
    if t > ta:
        typed(c, t, ta, 'Top faller: ••••• (-•.•%). Mutual funds: ₹ ••,•••. SIP: active, next on ••/••', 470, 1050, False, 0.01, blur=True)
        place(c, label('YOUR DATA STAYS PRIVATE', NAVY), 540, 1280, 1.1 * eback(prog(t, ta + 0.4, 0.35), 1.6), 2)
        place(c, text_img('answers blurred · illustration', 'type', 26, GREY), 540, 1370)


def s4(c, t):
    i = 3
    place_text(c, 'BUT WAIT...', 'anton', 140, RED, 540, 300, t, 'bw', STARTS[3] + 0.05, 'pop')
    tq = at(i, 'trade it', -0.4)
    if t > tq:
        sh = math.sin(t * 40) * 8 * math.exp(-(t - tq) * 2)
        place(c, text_img('?', 'anton', 420, RED), 540 + sh, 780, eback(prog(t, tq, 0.4), 1.8), 6)
        place(c, label('TRADE MY STOCKS?', RED), 300, 1120, 1.2 * eback(prog(t, tq, 0.35), 1.6), -5)
    tm = at(i, 'move it out', -0.4)
    if t > tm: place(c, label('MOVE MY MONEY?', RED), 780, 1240, 1.2 * eback(prog(t, tm, 0.35), 1.6), 5)
    tsc = at(i, 'scary part', -0.4)
    if t > tsc: place_text(c, "that's the scary part", 'mark', 64, NAVY, 540, 1420, t, 'sp', tsc, 'slide', rot=-2)


def s5(c, t):
    i = 4
    place_text(c, 'WHAT IT CAN DO', 'anton', 116, INK, 540, 270, t, 'cd', STARTS[4] + 0.05, 'pop')
    icon_card(c, t, at(i, 'One', -0.3), 1, 'NET WORTH + ALLOCATION', GRN, 480)
    icon_card(c, t, at(i, 'Two', -0.3), 2, 'HOLDINGS + SIP CHECKS', BLUE, 680)
    icon_card(c, t, at(i, 'Three', -0.3), 3, 'LIVE PRICES + NEWS', ORG, 880)
    tl = at(i, 'live prices', 0.2)
    typed(c, t, tl, 'NIFTY 50: 22,745.65 (27 Oct, 9:59 am)', 540, 1150, False, 0.6)
    if t > tl + 0.6: place(c, text_img('real data · NSE via INDmoney', 'type', 26, GREY), 540, 1300)


def s6(c, t):
    i = 5
    place_text(c, 'AND MORE', 'anton', 116, INK, 540, 270, t, 'am', STARTS[5] + 0.05, 'pop')
    icon_card(c, t, at(i, 'Four', -0.3), 4, 'OPTION CHAIN + GREEKS', PURPLE, 520)
    icon_card(c, t, at(i, 'Five', -0.3), 5, 'COMPARE MUTUAL FUNDS', TEAL, 720)
    to = at(i, 'one chat', -0.4)
    if t > to:
        s_, a = slam(t, to); place(c, stamp_c('ALL IN ONE CHAT', RED, 100, -5, 606), 540, 1000, s_, 0, a)


def s7(c, t):
    i = 6
    place_text(c, 'SETUP: 2 MINUTES', 'anton', 106, INK, 540, 260, t, 'su', STARTS[6] + 0.05, 'pop')
    SS.checklist(c, t, [('1  SETTINGS > CONNECTORS', at(i, 'Connectors', 0.1)), ('2  ADD CUSTOM CONNECTOR', at(i, 'custom connector', 0.3)),
                        ('3  PASTE THE INDMONEY LINK', at(i, 'paste', 0.4)), ('4  LOG IN WITH OTP + APPROVE', at(i, 'approve', 0.2))], y0=470, gap=165)
    tp = at(i, 'paste', 0.0)
    if t > tp:
        p = eback(prog(t, tp, 0.4), 1.4); place(c, SS._card(760, 120, YEL), 540, 1220, p, -1)
        if p > 0.6: place(c, text_img('mcp.indmoney.com/mcp', 'anton', 66, INK), 540, 1215)


def s8(c, t):
    i = 7
    place_text(c, 'THE ANSWER:', 'anton', 100, INK, 540, 250, t, 'an', STARTS[7] + 0.05, 'pop')
    tr = at(i, 'read only', -0.4)
    if t > tr:
        d = ImageDraw.Draw(c); p = eback(prog(t, tr, 0.4), 1.6); s = 1.0 * p
        place(c, stamp_c('READ-ONLY', GRN, 150, -6, 707), 540, 470, p, 0, 1)
    for k, (txt, ph) in enumerate([('NO TRADES', 'place trades'), ('NO WITHDRAWALS', 'withdraw'), ('NO SETTING CHANGES', 'change settings')]):
        tk = at(i, ph, -0.3)
        if t > tk:
            p = eback(prog(t, tk, 0.35), 1.4); y = 720 + k * 150
            place(c, SS._card(760, 120), 540, y, p, (-1, 1, -0.5)[k])
            if p > 0.6: place(c, text_img(txt, 'anton', 62, INK), 580, y); x_mark(c, 230, y, 30, RED, 12)
    tv = at(i, 'revoke', -0.3)
    if t > tv: place(c, label('REVOKE ACCESS IN 2 CLICKS', NAVY), 540, 1220, 1.2 * eback(prog(t, tv, 0.35), 1.6), -2)
    if t > tv + 0.6: place(c, text_img("source: INDmoney's MCP page, Oct 2026", 'type', 26, GREY), 540, 1320)


def s9(c, t):
    i = 8; T0 = STARTS[8] + 0.05
    SS.cheat_sheet(c, t, T0, 'INDMONEY + CLAUDE: CHEAT SHEET', [('CONNECT', 'Claude > Connectors', INK), ('LINK', 'mcp.indmoney.com/mcp', BLUE),
                   ('LOGIN', 'OTP + approve', INK), ('ACCESS', 'read-only', GRN), ('COST', 'free for users', GRN)], y0=170)
    SS.send_frame(c, t, at(i, 'Send this', -0.2), 'the friend with 5 investing apps', 1170)
    tq = at(i, 'So, would you', -0.2)
    if t > tq: place_text(c, 'Would you let AI see your portfolio?', 'mark', 52, YEL, 540, 1390, t, 'wq', tq, 'slide', rot=-2)
    for k, ln in enumerate(['Referral code in caption: I may earn a reward if you join.', 'Info: indmoney.com/mcp, Oct 2026. Not a paid sponsorship.', 'Education only. Not investment advice.']):
        place_text(c, ln, 'type', 24, (210, 204, 192), 540, 1500 + k * 38, t, None, T0 + 0.3, 'fade', track=1)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]


def SLAMS():
    return [at(0, 'five seconds', -0.3), at(5, 'one chat', -0.4), at(7, 'read only', -0.4)] + [STARTS[k] + 0.05 for k in range(1, 8)]


# ---------- captions ----------
def text_ta(word, size, col):
    runs, cur, isT = [], '', None
    for ch in word:
        t_ = 0x0B80 <= ord(ch) <= 0x0BFF or ch in '\u200c\u200d'
        if isT is None or t_ == isT: cur += ch
        else: runs.append((cur, isT)); cur = ch
        isT = t_
    if cur: runs.append((cur, isT))
    ims = [text_img(r, 'ta' if tt else 'osw', size if tt else int(size * 1.05), col) for r, tt in runs]
    h = max(m.size[1] for m in ims); w = sum(m.size[0] for m in ims)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); x = 0
    for m in ims: im.alpha_composite(m, (x, h - m.size[1])); x += m.size[0]
    return im


@functools.lru_cache(maxsize=None)
def cap_chunks(i):
    txt = TA[i] if CAP == 'ta' else SCRIPT[i]
    fn, size = ('ta', 50) if CAP == 'ta' else ('anton', 66)
    words = txt.split(); pos = []; c0 = 0
    for w_ in words:
        k = txt.find(w_, c0); pos.append(k / len(txt)); c0 = k + len(w_)
    chunks, cur, cw = [], [], 0
    for j, w_ in enumerate(words):
        ww = font(fn, size).getlength(w_ + ' ')
        if cur and (cw + ww > 860 or len(cur) >= (3 if CAP == 'ta' else 4) or words[cur[-1]][-1] in '.?!,:'):
            chunks.append(cur); cur, cw = [], 0
        cur.append(j); cw += ww
    if cur: chunks.append(cur)
    return words, pos, chunks, fn, size


@functools.lru_cache(maxsize=512)
def cap_img(i, ci, hj):
    words, pos, chunks, fn, size = cap_chunks(i)
    ims = [(text_ta(words[j], size, CREAM) if CAP == 'ta' else text_img(words[j].upper(), fn, size, YEL if j == hj else CREAM)) for j in chunks[ci]]
    gap = 18; w = sum(m.size[0] for m in ims) + gap * (len(ims) - 1) + 56; h = max(m.size[1] for m in ims) + 30
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 22, fill=(20, 20, 22, 215))
    x = 28
    for m in ims: im.alpha_composite(m, (x, (h - m.size[1]) // 2)); x += m.size[0] + gap
    return im


def captions(c, t):
    i = scene_at(t)
    if t < VO[i] or t > VO[i] + DURS[i] + 0.25: return
    words, pos, chunks, fn, size = cap_chunks(i)
    f = (t - VO[i]) / DURS[i]; hj = 0
    for j, p in enumerate(pos):
        if f >= p: hj = j
    ci = next(k for k, ch in enumerate(chunks) if hj in ch)
    place(c, cap_img(i, ci, hj), 540, 1665)


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('INDMONEY x CLAUDE', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
    ImageDraw.Draw(c).line((60, 118, W - 60, 118), fill=col, width=2)
    ImageDraw.Draw(c).line((60, 118, 60 + (W - 120) * clamp(t / DUR), 118), fill=RED if not dark else YEL, width=8)


def transition(c, t):
    cols = [(TEAL, INK), (GOLD, INK), (ORG, CREAM), (RED, YEL), (PINK, CREAM), (YEL, INK), (BLUE, CREAM), (INK, RED), (YEL, NAVY)]
    for bi, b in enumerate(B):
        d = 0.5
        if abs(t - b) > d / 2 + 0.12: continue
        for layer, delay in ((0, -0.05), (1, 0.0)):
            p = (t - (b - d / 2) - delay) / d
            if p <= 0 or p >= 1: continue
            p = eio(p); SWd, skew = 2050, 320
            xl = (W + 60) + p * (-(SWd + skew) - (W + 60) - 40)
            r = random.Random(bi * 10 + layer + 7900)
            left = [(xl + r.uniform(-14, 14) - skew * (y / H), y) for y in range(0, H + 1, 40)]
            right = [(xl + SWd + r.uniform(-14, 14) - skew * (y / H), y) for y in range(H, -1, -40)]
            if layer == 0:
                left = [(x - 70, y) for x, y in left]; right = [(x + 70, y) for x, y in right]
            poly_fill(c, left + right, cols[bi % len(cols)][layer], 255, S=1)


def slam_times():
    return SLAMS()


def scene_at(t):
    k = 0
    for i, s in enumerate(STARTS):
        if t >= s: k = i
    return k


def render(t):
    LOOP = 0.6
    if t > DUR - LOOP:
        a = _render(t); b = _render(1.15, loop=True); q = eio((t - (DUR - LOOP)) / LOOP)
        return (a * (1 - q) + b * q).astype(np.uint8)
    return _render(t)


def _render(t, loop=False):
    pbg, dbg = bgs()
    i = scene_at(t); dark = (i == 8)
    c = (dbg if dark else pbg).copy()
    st = STARTS[i]; en = STARTS[i + 1] if i + 1 < len(STARTS) else DUR
    SCENES[i](c, t)
    z = 1.0 + 0.035 * clamp((t - st) / (en - st))
    sx = sy = 0
    for ts in slam_times():
        if 0 <= t - ts < 0.35:
            k = math.exp(-(t - ts) * 14) * 8
            sx += k * math.sin((t - ts) * 90); sy += k * math.cos((t - ts) * 77)
    cw, ch = W / z, H / z
    cx, cy = W / 2 + sx, max(ch / 2, H * 0.47) + sy
    c = c.transform((W, H), Image.EXTENT, (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2), Image.BICUBIC)
    if not loop and (CAPS_ON or CAP == 'ta'): captions(c, t)
    header(c, dark, t if not loop else 0); transition(c, t)
    arr = np.asarray(c.convert('RGB')).astype(np.float32)
    g = grain_frames()[int(t * FPS) % 6]
    fl = 1 + 0.012 * math.sin(t * 37) * math.sin(t * 13)
    return np.clip(arr * fl + g[..., None], 0, 255).astype(np.uint8)
