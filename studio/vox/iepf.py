"""Forgotten shares: ₹89,000 Cr unclaimed in IEPF and how families can check (paper collage, female VO)"""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import math, json, functools, random
import numpy as np
from PIL import Image, ImageDraw
from lib import *
from scenes import words_line, slam, stamp_c, bgs, typed, drop, warn_icon
from fridge import follow_btn
import saveshare as SS
import tea as TEA
import paperchars as PC

SH = ROOT + 'iepf/'
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
SOFT = (252, 250, 244); AGED = (238, 226, 196)
label = TEA.label


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def pp(t, t0, d=0.35, s=1.6): return eback(prog(t, t0, d), s)


def src(c, t, txt, t0, y=1740, col=GREY):
    if t > t0: place_text(c, txt, 'type', 24, col, 540, y, t, None, t0, 'fade', track=1)


# ---------------- props ----------------
@functools.lru_cache(None)
def certificate(sc=1.0):
    w, h = int(820 * sc), int(520 * sc)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, w - 1, h - 1), fill=AGED)
    for k, col in enumerate(((150, 110, 60), (190, 150, 90))):
        m = int((14 + k * 14) * sc); d.rectangle((m, m, w - m, h - m), outline=col, width=int(6 * sc))
    r = random.Random(3)
    for _ in range(int(60 * sc)):
        x, y = r.uniform(0, w), r.uniform(0, h); rr = r.uniform(2, 10) * sc
        d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(215, 195, 155))
    t = text_img('SHARE CERTIFICATE', 'pf', int(56 * sc), (90, 60, 30)); im.alpha_composite(t, (w // 2 - t.size[0] // 2, int(60 * sc)))
    t2 = text_img('100 EQUITY SHARES OF ₹10 EACH', 'type', int(26 * sc), (90, 60, 30), 2); im.alpha_composite(t2, (w // 2 - t2.size[0] // 2, int(150 * sc)))
    t3 = text_img('issued 1994 · folio no. ______', 'type', int(24 * sc), (120, 90, 60), 1); im.alpha_composite(t3, (w // 2 - t3.size[0] // 2, int(200 * sc)))
    for k in range(4):
        y = int((260 + k * 34) * sc); d.line((int(90 * sc), y, w - int(90 * sc), y), fill=(200, 175, 135), width=int(5 * sc))
    cx, cy = int(w - 150 * sc), int(h - 110 * sc); rr = int(62 * sc)
    d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=(190, 50, 40), outline=(140, 30, 25), width=int(5 * sc))
    sl = text_img('SEAL', 'anton', int(34 * sc), AGED); im.alpha_composite(sl, (cx - sl.size[0] // 2, cy - sl.size[1] // 2 - 4))
    return cutout(im, border=0, shadow=0.4, blur=10)


@functools.lru_cache(None)
def doc(title, lines, col=SOFT, w=520, h=320, ttl_col=INK):
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 12, fill=col)
    t = text_img(title, 'anton', 46, ttl_col); im.alpha_composite(t, (30, 22))
    for k, ln in enumerate(lines):
        li = text_img(ln, 'type', 26, GREY, 1); im.alpha_composite(li, (32, 100 + k * 44))
    return cutout(im, border=8, shadow=0.38)


@functools.lru_cache(None)
def vault():
    w, h = 420, 420
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 10, w - 10, h - 10), 30, fill=(80, 88, 100), outline=INK, width=8)
    d.ellipse((90, 90, w - 90, h - 90), fill=(130, 140, 152), outline=INK, width=8)
    for k in range(8):
        a = k * math.pi / 4; d.line((w / 2, h / 2, w / 2 + math.cos(a) * 110, h / 2 + math.sin(a) * 110), fill=INK, width=8)
    d.ellipse((w / 2 - 34, h / 2 - 34, w / 2 + 34, h / 2 + 34), fill=GOLD, outline=INK, width=6)
    t = text_img('IEPF', 'anton', 64, CREAM); im.alpha_composite(t, (w // 2 - t.size[0] // 2, 22))
    return cutout(im, border=8, shadow=0.4)


@functools.lru_cache(None)
def phone():
    w, h = 560, 900
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 60, fill=INK)
    d.rounded_rectangle((22, 22, w - 23, h - 23), 44, fill=(250, 250, 248))
    d.rounded_rectangle((w // 2 - 60, 36, w // 2 + 60, 60), 12, fill=INK)
    d.rounded_rectangle((50, 90, w - 50, 150), 30, fill=(232, 234, 238))
    u = text_img('iepf.gov.in', 'osw5', 32, INK); im.alpha_composite(u, (80, 100))
    d.rectangle((22, 175, w - 23, 255), fill=NAVY)
    hdr = text_img('UNCLAIMED AMOUNTS', 'anton', 40, CREAM); im.alpha_composite(hdr, (w // 2 - hdr.size[0] // 2, 192))
    lb = text_img('Investor name', 'type', 24, GREY); im.alpha_composite(lb, (60, 285))
    d.rounded_rectangle((50, 320, w - 50, 390), 14, fill=SOFT, outline=(150, 150, 160), width=3)
    d.rounded_rectangle((50, 420, w - 50, 490), 34, fill=GRN)
    s = text_img('SEARCH', 'anton', 40, CREAM); im.alpha_composite(s, (w // 2 - s.size[0] // 2, 430))
    return im


@functools.lru_cache(16)
def fam(kind):
    if kind == 'dad': return PC.person('man', 'calm', 'down', 'b', shirt=(235, 235, 225), pants=(80, 80, 90), mustache=True, old=True, scale=0.55)
    if kind == 'mum': return PC.person('woman', 'happy', 'down', 'a', shirt=(150, 80, 160), saree=True, old=True, scale=0.55)
    if kind == 'kid': return PC.person('man', 'wow', 'up', 'c', shirt=(110, 190, 230), pants=(60, 60, 80), scale=0.55)
    return PC.person('woman', 'wow', 'down', 'a', shirt=(235, 90, 120), saree=True, scale=0.55)


# ---------------- scenes ----------------
def s1(c, t):
    i = 0
    words_line(c, t, [("YOUR", INK, 0.1), ("PARENTS'", INK, 0.25)], 'anton', 130, 280, key='h1')
    words_line(c, t, [("LOST", RED, 0.45), ("SHARES", INK, 0.6)], 'anton', 130, 420, key='h2')
    dy, a = drop(t, 0.7, 360)
    if a > 0:
        jx, jy, jr = jit('cert', t, 2, 0.5)
        place(c, certificate(), 540 + jx, 800 + dy + jy, 1.0, -4 + jr + (1 - a) * 8, a)
    tn = at(i, 'not gone', -0.2)
    if t > tn:
        sc, a2 = slam(t, tn); place(c, stamp_c('NOT GONE', GRN, 110, -10, 7), 380, 1000, sc, 0, a2)
    te = at(i, 'eighty nine', -0.4)
    if t > te:
        v = int(89000 * eo(prog(t, te, 1.2)))
        fw = text_w('₹89,000 CR', 'anton', 150)
        highlight(c, 540 - fw / 2 - 20, 1200, 540 + fw / 2 + 20, 1330, prog(t, te + 1.2, 0.4), seed=2)
        place(c, text_img(f'₹{v:,} CR', 'anton', 150, INK), 540, 1260)
        place_text(c, 'of shares, unclaimed', 'mark', 56, RED, 540, 1410, t, 'unc', te + 0.6, 'slide', rot=-3)
    src(c, t, '~₹89,004 Cr (Nov 2025) · 1 Finance via Business Today', 1.2, 1700)


def s2(c, t):
    i = 1; T0 = STARTS[i]
    tc = at(i, 'old share', -0.3)
    if t > tc:
        p = prog(t, tc, 0.45); jx, jy, jr = jit('c2', t, 1.6, 0.4)
        place(c, certificate(0.6), 300 + jx, 380 + jy - (1 - eo(p)) * 300, 1, -6 + jr, clamp(p * 3))
        place_text(c, 'in a cupboard', 'mark', 44, RED, 300, 590, t, 'cb', tc + 0.4, 'slide', rot=-4)
    td = at(i, 'dividend', -0.3)
    if t > td:
        p = prog(t, td, 0.45)
        place(c, doc('DIVIDEND WARRANT', ('Pay: ₹1,250', 'not encashed'), (236, 244, 236), 460, 240, GRN), 790, 400 - (1 - eo(p)) * 300, 1, 5, clamp(p * 3))
    ts = at(i, 'seven years', -0.4)
    if t > ts:
        d = ImageDraw.Draw(c)
        for k in range(7):
            tk = ts + 0.12 * k
            if t < tk: continue
            x = 160 + k * 127; q = pp(t, tk)
            place(c, label(f'YR {k + 1}', RED if k == 6 else GREY), x, 800, 0.62 * q, (-3, 2, -2, 3, -1, 2, -3)[k])
        place_text(c, '7 years unclaimed', 'pfi', 64, INK, 540, 920, t, 's7', ts + 0.9, 'pop')
    tm = at(i, 'moves', -0.3)
    if t > tm:
        marker_line(c, curve((540, 990), (520, 1060), (540, 1130)), prog(t, tm, 0.4), RED, 9, head=True)
        dy, a = drop(t, tm + 0.3, 300)
        if a > 0: place(c, vault(), 540, 1360 + dy, 0.95, -2, a)
    tf = at(i, 'IEPF', -0.3)
    if t > tf: place(c, label('INVESTOR EDUCATION & PROTECTION FUND', NAVY), 540, 1610, 0.75 * pp(t, tf), -1)


def s3(c, t):
    i = 2; T0 = STARTS[i]
    place_text(c, 'INSIDE IEPF', 'anton', 120, INK, 540, 270, t, 'ii', T0 + 0.05, 'pop')
    te = at(i, 'eighty nine', -0.4)
    if t > te:
        v = int(89004 * eo(prog(t, te, 1.2)))
        place(c, text_img(f'₹{v:,} CR', 'anton', 140, GRN), 540, 440)
        place_text(c, 'Nov 2025', 'type', 32, GREY, 540, 530, t, 'nv', te + 0.3, 'fade')
    tc = at(i, 'sixteen hundred', -0.3)
    if t > tc:
        sc, a = slam(t, tc); place(c, stamp_c('1,671 COMPANIES', RED, 76, -5, 31), 540, 650, sc, 0, a)
    tr = at(i, 'Reliance', -0.4)
    if t > tr:
        cx, cy, r = 540, 1110, 300
        d = ImageDraw.Draw(c)
        slices = [('RELIANCE', 15.6, RED), ('HDFC BANK', 2.4, BLUE), ('L&T', 2.3, TEAL), ('HUL', 2.2, ORG), ('JSW STEEL', 2.2, GOLD), ('OTHERS', 75.3, (210, 204, 190))]
        q = eo(prog(t, tr, 1.2)); a0 = -90
        for nm, v, col in slices:
            sweep = 360 * v / 100 * q
            off = 26 if nm == 'RELIANCE' else 0; mid = math.radians(a0 + sweep / 2)
            ox, oy = math.cos(mid) * off, math.sin(mid) * off
            d.pieslice((cx - r + ox, cy - r + oy, cx + r + ox, cy + r + oy), a0, a0 + sweep, fill=col, outline=INK, width=4)
            a0 += sweep
        if q > 0.95:
            place(c, label('RELIANCE 15.6%', RED), 820, 830, pp(t, tr + 1.2), 4)
            place(c, text_img('HDFC Bank 2.4% · L&T 2.3% · HUL 2.2% · JSW Steel 2.2%', 'osw5', 32, INK), 540, 1460, pp(t, tr + 1.4))
    src(c, t, 'Share of IEPF value · 1 Finance via Business Today, Apr 2026', T0 + 1.0, 1700)


def s4(c, t):
    i = 3; T0 = STARTS[i]
    words_line(c, t, [("MAYBE", INK, T0 + 0.1), ("YOURS", RED, T0 + 0.3)], 'anton', 150, 300, key='my')
    for k, (kind, x) in enumerate((('dad', 230), ('mum', 450), ('kid', 670), ('sis', 880))):
        tk = T0 + 0.4 + 0.15 * k
        if t < tk: continue
        p = prog(t, tk, 0.45); jx, jy, jr = jit(('f', k), t, 1.4, 0.3)
        place(c, fam(kind), x + jx, 700 + jy + (1 - eo(p)) * 500, 0.85, jr, clamp(p * 3))
    td = at(i, 'dividends', -0.3)
    if t > td:
        place(c, label('+ DIVIDENDS ON THOSE SHARES', GRN), 540, 1060, pp(t, td), -2)
    th = at(i, 'how do you check', -0.3)
    if t > th:
        place_text(c, 'so how do you check?', 'pfi', 80, INK, 540, 1260, t, 'hc', th, 'pop')
        marker_line(c, [(220, 1320), (540, 1312), (860, 1304)], prog(t, th + 0.3, 0.4), RED, 8)


def s5(c, t):
    i = 4; T0 = STARTS[i]
    place(c, label('STEP 1', RED), 540, 230, pp(t, T0 + 0.05), -2)
    p = prog(t, T0 + 0.2, 0.45)
    place(c, phone(), 540, 900 + (1 - eo(p)) * 900, 1, 0, clamp(p * 3))
    if p > 0.8:
        ts = at(i, 'Search', -0.2)
        nm = 'S. RAMASAMY'
        n = int(len(nm) * clamp((t - ts) / 1.2)) if t > ts else 0
        tx = text_img(nm[:n] + ('|' if int(t * 3) % 2 else ''), 'osw5', 34, INK)
        c.alpha_composite(tx, (540 - 280 + 70, 900 - 450 + 331))
        if t > ts + 1.5:
            q = pp(t, ts + 1.5)
            place(c, doc('1 RESULT FOUND', ('Company: ABC Textiles Ltd', 'Shares: 100 · in IEPF'), (236, 244, 236), 470, 220, GRN), 540, 1130, q, -1)
            place_text(c, 'example name', 'mark', 40, RED, 800, 1400, t, 'ex', ts + 1.8, 'slide', rot=-4)
    src(c, t, 'iepf.gov.in → search unclaimed amounts (Business Standard guide)', T0 + 1.0, 1740)


def s6(c, t):
    i = 5; T0 = STARTS[i]
    place(c, label('STEP 2', RED), 540, 230, pp(t, T0 + 0.05), -2)
    place_text(c, 'FIND THE PROOF', 'anton', 110, INK, 540, 360, t, 'fp', T0 + 0.2, 'pop')
    items = [('certificates', lambda: certificate(0.55), 300, 640, -6), ('dividend letters', lambda: doc('DIVIDEND LETTER', ('Folio: ____', 'Year: 1999'), SOFT, 440, 240), 780, 620, 5),
             ('passbooks', lambda: doc('BANK PASSBOOK', ('A/c: ______', 'Dividend credit'), (225, 232, 245), 440, 240, NAVY), 540, 940, -2)]
    for k, (ph, f, x, y, r) in enumerate(items):
        tk = at(i, ph, -0.3)
        if t < tk: continue
        p = prog(t, tk, 0.45); jx, jy, jr = jit(('p6', k), t, 1.4, 0.3)
        place(c, f(), x + jx, y + jy - (1 - eo(p)) * 400, 1, r + jr, clamp(p * 3))
    ta = at(i, 'Ask relatives', -0.3)
    if t > ta:
        place(c, fam('dad'), 300, 1340, 0.75)
        place(c, fam('kid'), 760, 1340, 0.75)
        place_text(c, 'ask relatives!', 'mark', 56, RED, 540, 1150, t, 'ar', ta, 'slide', rot=-3)


def s7(c, t):
    i = 6; T0 = STARTS[i]
    place(c, label('STEP 3', RED), 540, 230, pp(t, T0 + 0.05), -2)
    tf = at(i, 'form', -0.3)
    if t > tf:
        p = prog(t, tf, 0.45)
        place(c, cutout(Image.new('RGBA', (820, 900), SOFT + (255,)), border=0, shadow=0.35), 540, 820 + (1 - eo(p)) * 700, 1, -1, clamp(p * 3))
        if p > 0.8:
            place(c, text_img('FORM IEPF-5', 'anton', 90, INK), 540, 460)
            c.alpha_composite(text_img('claim refund of shares & dividends', 'type', 28, GREY, 1), (190, 520))
            for k, (txt, ph) in enumerate((('PAN card', 'PAN'), ('ID proof', 'ID proof'), ('Bank details', 'bank details'))):
                tk = at(i, ph, -0.3); y = 660 + k * 150
                d = ImageDraw.Draw(c); d.rounded_rectangle((200, y - 40, 280, y + 40), 10, outline=INK, width=6)
                c.alpha_composite(text_img(txt, 'anton', 64, INK), (320, y - 44))
                if t > tk: d.line((212, y, 236, y + 26, 276, y - 30), fill=GRN, width=12, joint='curve')
            c.alpha_composite(text_img('file online, then send docs to the company', 'type', 26, GREY, 1), (190, 1140))
    th = at(i, 'Legal heirs', -0.3)
    if t > th:
        sc, a = slam(t, th); place(c, stamp_c('LEGAL HEIRS CAN CLAIM', GRN, 70, -5, 41), 540, 1400, sc, 0, a)
    src(c, t, 'Form IEPF-5 · iepf.gov.in · Business Standard, Oct 2025', T0 + 1.0, 1740)


def s8(c, t):
    i = 7; T0 = STARTS[i]
    if t > T0 + 0.1:
        p = prog(t, T0 + 0.1, 0.3)
        place(c, text_img("IT'S SLOW, BUT IT WORKS", 'osw', 54, YEL, 2), 540, 270, 0.6 + 0.4 * eback(p), 0, clamp(p * 3))
    tc = at(i, 'seventy five', -0.4)
    if t > tc:
        v = int(75417 * eo(prog(t, tc, 1.2)))
        place(c, text_img(f'{v:,}', 'anton', 190, GRN), 540, 520)
        place_text(c, 'claims approved in 2 years', 'osw5', 44, CREAM, 540, 650, t, 'ca', tc + 0.3, 'fade')
    ts = at(i, 'four crore', -0.4)
    if t > ts:
        v = 4.36 * eo(prog(t, ts, 1.2))
        place(c, text_img(f'{v:.2f} CR', 'anton', 190, YEL), 540, 880)
        place_text(c, 'shares returned to families', 'osw5', 44, CREAM, 540, 1010, t, 'sr', ts + 0.3, 'fade')
    tf = at(i, 'families', -0.2)
    if t > tf:
        for k, (kind, x) in enumerate((('dad', 300), ('mum', 540), ('kid', 780))):
            place(c, fam(kind), x, 1340 + math.sin(t * 4 + k) * 6, 0.7 * pp(t, tf + 0.12 * k))
    src(c, t, 'Govt reply in Lok Sabha, 27 Jul 2026 (via Outlook Money)', T0 + 1.0, 1740, (200, 194, 182))


def s9(c, t):
    i = 8; T0 = STARTS[i]
    q = pp(t, T0, 0.45, 1.2)
    place(c, SS._card(960, 720), 540, 520, q, -0.4)
    if q > 0.6:
        place(c, text_img('LOST SHARES · 3 STEPS', 'anton', 56, INK), 540, 220)
        d = ImageDraw.Draw(c); d.line((90, 262, 990, 262), fill=INK, width=4)
        rows = [('1', 'Search name on iepf.gov.in'), ('2', 'Find certificates, letters, passbooks'), ('3', 'File IEPF-5 with PAN, ID, bank details')]
        for k, (n, txt) in enumerate(rows):
            tk = T0 + 0.3 + 0.12 * k
            if t < tk: continue
            y = 310 + k * 150
            c.alpha_composite(text_img(n, 'anton', 90, RED), (110, y - 10))
            c.alpha_composite(text_img(txt, 'osw5', 40, INK), (200, y + 20))
        c.alpha_composite(text_img('Legal heirs can claim too', 'mark', 44, GRN), (200, 760))
    SS.send_frame(c, t, at(i, 'Send this', -0.3), 'your parents, tonight', y=1050)
    SS.save_pulse(c, t, at(i, 'Save this', -0.3), 540, 1290, 'SAVE THIS')
    tf = at(i, 'Follow', -0.2)
    if t > tf:
        q2 = prog(t, tf, 0.35); place(c, follow_btn(), 540, 1480, 0.5 + 0.5 * eback(q2), 0, clamp(q2 * 3))
    for k, ln in enumerate(['Data: 1 Finance study (Business Today, Apr 2026) · Lok Sabha reply, Jul 2026', 'Claim only through iepf.gov.in and the company/RTA', 'Education only. Not investment advice.']):
        place_text(c, ln, 'type', 22, GREY, 540, 1640 + k * 34, t, None, T0 + 0.3, 'fade', track=1)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
DARK_SCENES = {7}


def slam_times():
    return [at(0, 'not gone', -0.2), at(2, 'sixteen hundred', -0.3), at(6, 'Legal heirs', -0.3)] + [STARTS[k] + 0.05 for k in range(1, 8)]


def header(c, dark, t=0):
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 64))
    b = text_img('FORGOTTEN SHARES', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
    ImageDraw.Draw(c).line((60, 118, W - 60, 118), fill=col, width=2)
    ImageDraw.Draw(c).line((60, 118, 60 + (W - 120) * clamp(t / DUR), 118), fill=RED if not dark else YEL, width=8)


def transition(c, t):
    cols = [(GOLD, INK), (NAVY, CREAM), (RED, YEL), (GRN, CREAM), (YEL, INK), (BLUE, CREAM), (INK, YEL), (YEL, RED)]
    for bi, b in enumerate(B):
        d = 0.55
        if abs(t - b) > d / 2 + 0.12: continue
        for layer, delay in ((0, -0.07), (1, 0.0)):
            p = (t - (b - d / 2) - delay) / d
            if p <= 0 or p >= 1: continue
            p = eio(p); SWd, skew = 2050, 320
            xl = (W + 60) + p * (-(SWd + skew) - (W + 60) - 40)
            r = random.Random(bi * 10 + layer + 444)
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
    z = 1.0 + 0.035 * clamp((t - st) / (en - st))
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
