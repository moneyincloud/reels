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
SH = ROOT + '' + os.environ.get('LDIR', 'lows2') + '/'
CAP = os.environ.get('CAP', 'en')
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




CLOSES = json.load(open(ROOT + 'lows/closes.json'))
STK = {
    'HUL': ('HINDUSTAN UNILEVER', 'FMCG · ₹4.26 LAKH CR', 2667.2, 1814.7, '-32%', BLUE),
    'MARUTI': ('MARUTI SUZUKI', 'AUTO · ₹3.53 LAKH CR', 17370, 11230, '-35%', NAVY),
    'DMART': ('DMART', 'RETAIL · ₹2.06 LAKH CR', 4644, 3157.7, '-32%', GRN),
    'SWIGGY': ('SWIGGY', 'FOOD + QUICK COMMERCE', 434, 176, '-59%', ORG),
    'NTPC': ('NTPC', 'POWER · ₹2.89 LAKH CR', 414.4, 298, '-28%', TEAL),
}
ORDER = ['HUL', 'MARUTI', 'DMART', 'SWIGGY', 'NTPC']

TA = [
    "இந்தியாவின் பெரிய பிராண்டுகள் 52 வார குறைந்த விலையைத் தொட்டுள்ளன. இது வாய்ப்பா, எச்சரிக்கையா? ஏன் விழுந்தன என்று பார்ப்போம்.",
    "முதலில் சந்தை. நிஃப்டி அதன் உச்சத்திலிருந்து சுமார் 14% கீழே. ஆனால் இந்த ஜாம்பவான்கள் இன்னும் அதிகமாக விழுந்துள்ளன.",
    "ஹிந்துஸ்தான் யூனிலீவர். உச்சத்திலிருந்து 32% சரிவு. லாபம் குறைந்தது, மூலப்பொருள் செலவு உயர்கிறது, சோப்புத்தூள் விலை உயர்த்தப்பட்டது.",
    "மாருதி சுசுகி. 35% சரிவு, செப்டம்பர் விற்பனை உயர்ந்தும் கூட. சந்தை லாப வரம்பைக் கவனிக்கிறது. Q2 முடிவுகள் அக்டோபர் 27 அன்று.",
    "டிமார்ட். 32% சரிவு. வருவாய் 18% உயர்ந்தது, ஆனால் லாப வரம்பு குறைந்தது, தரகு நிறுவனங்கள் இலக்கைக் குறைத்தன.",
    "ஸ்விக்கி. உச்சத்திலிருந்து 59% சரிவு. இன்ஸ்டாமார்ட் இழப்பு அதிகரித்ததால் ஒரே நாளில் 17% விழுந்தது.",
    "என்டிபிசி. 28% சரிவு. அணு மற்றும் பசுமை மின்சாரத் திட்டங்கள் உள்ளன, ஆனால் நிலக்கரி விநியோகமும் பெரிய செலவுகளும் கவலை.",
    "நினைவில் கொள்ளுங்கள்: 52 வார குறைந்த விலை தள்ளுபடி ஸ்டிக்கர் அல்ல. மூன்று கேள்விகள்: ஏன் விழுந்தது? லாபம் வளர்கிறதா? கடன் கட்டுப்பாட்டில் உள்ளதா?",
    "மலிவானது இன்னும் மலிவாகலாம். இதைச் சேமித்து, moneyincloud-ஐப் பின்தொடருங்கள். கல்விக்காக மட்டும், முதலீட்டு ஆலோசனை அல்ல. அப்போ, வாய்ப்பா, எச்சரிக்கையா?",
]


def rs(v):
    return inr(v) if v >= 1000 else '₹' + (f'{v:.0f}' if v >= 100 else f'{v:.2f}')


@functools.lru_cache(maxsize=None)
def icon(key):
    im = Image.new('RGBA', (200, 160), (0, 0, 0, 0)); d = ImageDraw.Draw(im); O = INK; w = 6
    col = STK[key][5]
    if key == 'HUL':
        d.rounded_rectangle((60, 40, 130, 150), 18, fill=col, outline=O, width=w)
        d.rectangle((80, 14, 110, 42), fill=CREAM, outline=O, width=w)
        d.rounded_rectangle((72, 80, 118, 120), 8, fill=CREAM, outline=O, width=4)
        for x, y, r in ((155, 60, 18), (175, 105, 12), (150, 130, 9), (30, 70, 10)):
            d.ellipse((x - r, y - r, x + r, y + r), fill=(220, 236, 255), outline=O, width=4)
    elif key == 'MARUTI':
        d.polygon([(55, 70), (80, 35), (135, 35), (160, 70)], fill=CREAM, outline=O)
        d.line([(55, 70), (80, 35), (135, 35), (160, 70)], fill=O, width=w)
        d.rounded_rectangle((15, 68, 188, 120), 18, fill=col, outline=O, width=w)
        for x in (55, 150):
            d.ellipse((x - 22, 100, x + 22, 144), fill=O); d.ellipse((x - 9, 113, x + 9, 131), fill=GREY)
        d.ellipse((168, 80, 182, 92), fill=YEL)
    elif key == 'DMART':
        d.line([(10, 30), (40, 30), (65, 110), (165, 110)], fill=O, width=w)
        d.polygon([(45, 45), (185, 45), (165, 100), (62, 100)], fill=col, outline=O)
        d.line([(45, 45), (185, 45), (165, 100), (62, 100), (45, 45)], fill=O, width=w)
        for x in (80, 150): d.ellipse((x - 15, 118, x + 15, 148), fill=O)
        for x in (90, 120, 150): d.line([(x, 50), (x - 4, 96)], fill=O, width=3)
    elif key == 'SWIGGY':
        d.rounded_rectangle((30, 55, 140, 150), 12, fill=col, outline=O, width=w)
        d.arc((55, 20, 115, 80), 180, 360, fill=O, width=w)
        d.ellipse((140, 10, 190, 60), fill=RED, outline=O, width=w); d.polygon([(147, 48), (183, 48), (165, 90)], fill=RED)
        d.line([(147, 48), (165, 90), (183, 48)], fill=O, width=w); d.ellipse((158, 26, 172, 40), fill=CREAM)
    elif key == 'NTPC':
        d.ellipse((30, 10, 170, 150), fill=col, outline=O, width=w)
        bolt = [(108, 22), (62, 88), (95, 88), (82, 138), (138, 68), (104, 68), (118, 22)]
        d.polygon(bolt, fill=YEL); d.line(bolt + [bolt[0]], fill=O, width=5)
    return im


def chart_pts(key, x0=170, x1=910, yt=600, yb=900):
    v = CLOSES[key]; lo, hi = min(v), max(v)
    return [(x0 + (x1 - x0) * k / (len(v) - 1), yt + (yb - yt) * (hi - p) / (hi - lo)) for k, p in enumerate(v)], v


def low_card(c, t, i, key, t_pct, reasons):
    nm, sub, hi, lo, pct, col = STK[key]
    n = ORDER.index(key) + 1
    T0 = STARTS[i] + 0.05
    if t > T0:
        place(c, label(f'{n}/5', INK), 110, 195, 1.1 * eback(prog(t, T0, 0.3), 1.6), -4)
    place_text(c, nm, 'anton', 104 if len(nm) < 14 else 88, INK, 540, 290, t, f'n{i}', T0, 'pop')
    place_text(c, sub, 'osw5', 44, col, 540, 395, t, f's{i}', T0 + 0.2, 'slide')
    if t > T0 + 0.35:
        p = eback(prog(t, T0 + 0.35, 0.4), 1.3); place(c, card_box(900, 560, SOFT), 540, 770, p, -0.6)
    if t > T0 + 0.7:
        pts, v = chart_pts(key)
        d = ImageDraw.Draw(c)
        for gy in (600, 750, 900): d.line((170, gy, 910, gy), fill=(225, 220, 210), width=2)
        p = eio(prog(t, T0 + 0.7, 1.6)); spark(c, pts, p, RED, 9)
        kh = v.index(max(v)); hx, hy = pts[kh]
        if p * (len(pts) - 1) >= kh:
            d.ellipse((hx - 11, hy - 11, hx + 11, hy + 11), fill=YEL, outline=INK, width=3)
            place(c, text_img('52W HIGH ' + rs(hi), 'osw5', 36, GREY), min(max(hx, 300), 780), hy - 38 if hy > 640 else 555)
        f = p * (len(pts) - 1); k = min(int(f), len(pts) - 2); fr = f - k
        tx = pts[k][0] + (pts[k + 1][0] - pts[k][0]) * fr; ty = pts[k][1] + (pts[k + 1][1] - pts[k][1]) * fr
        val = v[k] + (v[k + 1] - v[k]) * fr
        if p < 1:
            d.ellipse((tx - 9, ty - 9, tx + 9, ty + 9), fill=RED, outline=INK, width=3)
            place(c, text_img(rs(val), 'anton', 44, INK), min(tx, 840), ty + 42 if ty < 860 else ty - 42)
        else:
            d.ellipse((tx - 14, ty - 14, tx + 14, ty + 14), fill=RED, outline=INK, width=3)
            place(c, text_img('NOW ' + rs(lo), 'anton', 66, RED), 700, 975)
        place(c, icon(key), 250, 975, 0.8 * eback(prog(t, T0 + 0.8, 0.4), 1.6), -5)
        if p > 0.05: place(c, text_img('weekly close · last 12 months', 'type', 22, GREY), 540, 1025)
    if t > t_pct:
        s_, a = slam(t, t_pct); place(c, stamp_c(pct, RED, 140, -7, 800 + i), 540, 1150, s_, 0, a)
        if t - t_pct < 0.25: c.alpha_composite(Image.new('RGBA', c.size, (226, 58, 44, int(80 * (1 - (t - t_pct) / 0.25)))))
    for k, (txt, ph, cl) in enumerate(reasons):
        tk = at(i, ph, -0.3)
        if t > tk: place(c, label(txt, cl), 540, 1300 + k * 92, 1.15 * eback(prog(t, tk, 0.35), 1.6), (-2, 2, -1)[k % 3])


def s1(c, t):
    i = 0
    words_line(c, t, [("52-WEEK", INK, 0.05), ("LOWS", RED, 0.25)], 'anton', 170, 300, key='h')
    tb = at(i, 'biggest brands', -0.2) if 'biggest brands' in SCRIPT[0] else 0.4
    tf = at(i, 'fifty two', 0)
    for k, nm in enumerate(ORDER):
        tk = tb + 0.12 * k
        if t > tk:
            x = (240, 540, 840, 380, 700)[k]; y = (560, 560, 560, 760, 760)[k]
            dy = 0 if t < tf else 40 * eio(prog(t, tf + k * 0.06, 0.6))
            place(c, icon(nm), x, y - 70 + dy, 0.55 * eback(prog(t, tk, 0.3), 1.6), (-4, 3, -2, 4, -3)[k])
            place(c, label('MARUTI' if nm == 'MARUTI' else nm, STK[nm][5]), x, y + 20 + dy, 1.1 * eback(prog(t, tk, 0.3), 1.6), (-4, 3, -2, 4, -3)[k])
            if dy > 5: ImageDraw.Draw(c).polygon([(x - 20, y + dy + 70), (x + 20, y + dy + 70), (x, y + dy + 98)], fill=RED)
    hb = 'thirty two' in SCRIPT[0]; yq = 1230 if hb else 1080
    if hb:
        t32 = at(i, 'thirty two', -0.3)
        if t > t32:
            s_, a = slam(t, t32); place(c, stamp_c('HUL -32%', RED, 120, -6, 777), 540, 1010, s_, 0, a)
    tq = at(i, 'Bargain' if 'Bargain' in SCRIPT[0] else 'bargain', -0.3)
    if t > tq: place(c, label('BARGAIN?', GRN), 300, yq, 1.4 * eback(prog(t, tq, 0.35), 1.6), -5)
    tw = at(i, 'warning', -0.3)
    if t > tw:
        sh = math.sin(t * 40) * 6 * math.exp(-(t - tw) * 3)
        place(c, label('WARNING?', RED), 780 + sh, yq, 1.4 * eback(prog(t, tw, 0.35), 1.6), 5)
    if 'why they fell' in SCRIPT[0]:
        tc = at(i, 'why they fell', -0.3)
        if t > tc: place_text(c, "let's check why they fell", 'mark', 66, NAVY, 540, 1270, t, 'wf', tc, 'slide', rot=-2)
    else:
        tc = tw + 0.5
    if t > tc + 0.3: place_text(c, 'prices: NSE close, 23 Oct 2026', 'type', 30, GREY, 540, 1390, t, None, tc + 0.3, 'fade', track=1)


def s2(c, t):
    i = 1
    place_text(c, 'THE MARKET', 'anton', 130, INK, 540, 300, t, 'm', STARTS[1] + 0.05, 'pop')
    tn = at(i, 'Nifty', -0.3)
    if t > tn:
        p = eback(prog(t, tn, 0.4), 1.3); place(c, card_box(880, 380, SOFT), 540, 640, p, -1)
        if p > 0.6:
            q = eo(prog(t, tn + 0.3, 1.0)); nv = 26373 + (22600 - 26373) * q
            place(c, text_img('NIFTY 50', 'osw5', 50, GREY), 540, 530)
            place(c, text_img('HIGH 26,373', 'anton', 70, GREY), 540, 620)
            place(c, text_img('NOW ' + f'{int(nv):,}', 'anton', 90, RED), 540, 730)
    tf = at(i, 'fourteen percent', -0.3)
    if t > tf: place(c, label('-14% FROM HIGH', RED), 540, 900, 1.3 * eback(prog(t, tf, 0.35), 1.6), 2)
    tg = at(i, 'giants', -0.3)
    if t > tg:
        place_text(c, 'fall from 52-week high', 'type', 30, GREY, 540, 990, t, None, tg, 'fade', track=1)
        ph = eo(prog(t, tg, 0.9))
        bars = [('NIFTY', 14, GREY), ('NTPC', 28, TEAL), ('HUL', 32, BLUE), ('DMART', 32, GRN), ('MARUTI', 35, NAVY), ('SWIGGY', 59, ORG)]
        d = ImageDraw.Draw(c)
        for k, (nm, v, cl) in enumerate(bars):
            y = 1055 + k * 84; w = int(9 * v * ph)
            place(c, text_img(nm, 'osw5', 38, INK), 170, y)
            d.rounded_rectangle((300, y - 28, 300 + w, y + 28), 10, fill=cl, outline=INK, width=3)
            if ph > 0.1: c.alpha_composite(text_img(f'-{int(round(v * ph))}%', 'anton', 48, RED), (320 + w, y - 30))


def s3(c, t): low_card(c, t, 2, 'HUL', at(2, 'thirty two', -0.3), [('PROFIT SLIPPED', 'Profits slipped', RED), ('INPUT COSTS UP', 'input costs', ORG), ('DETERGENT PRICES RAISED', 'detergent', NAVY)])
def s4(c, t): low_card(c, t, 3, 'MARUTI', at(3, 'thirty five', -0.3), [('SEPT SALES UP', 'September sales', GRN), ('MARGINS IN FOCUS', 'margins', ORG), ('Q2 RESULTS: 27 OCT', 'October twenty', NAVY)])
def s5(c, t): low_card(c, t, 4, 'DMART', at(4, 'thirty two', -0.3), [('REVENUE +18%', 'eighteen percent', GRN), ('MARGINS NARROWED', 'margins narrowed', RED), ('TARGETS CUT', 'brokerages', ORG)])
def s6(c, t): low_card(c, t, 5, 'SWIGGY', at(5, 'fifty nine', -0.3), [('-17% IN ONE DAY', 'seventeen percent', RED), ('INSTAMART LOSSES WIDER', 'Instamart', ORG)])
def s7(c, t): low_card(c, t, 6, 'NTPC', at(6, 'twenty eight', -0.3), [('NUCLEAR + GREEN PLANS', 'nuclear', GRN), ('COAL SUPPLY WORRIES', 'coal supply', ORG), ('BIG SPENDING AHEAD', 'big spending', NAVY)])


def s8(c, t):
    i = 7
    place_text(c, '52-WEEK LOW', 'anton', 120, INK, 540, 290, t, 'q', STARTS[7] + 0.05, 'pop')
    td = at(i, 'discount sticker', -0.4)
    if t > td:
        p = eback(prog(t, td, 0.4), 1.5)
        place(c, stamp_c('SALE 30% OFF', ORG, 110, -8, 977), 540, 520, p, 0, 1)
        tx = td + 0.6
        if t > tx:
            q = eo(prog(t, tx, 0.3)); d = ImageDraw.Draw(c)
            d.line((180, 420, 180 + 720 * q, 420 + 200 * q), fill=RED, width=22)
            d.line((900, 420, 900 - 720 * q, 420 + 200 * q), fill=RED, width=22)
            place_text(c, 'not a discount sticker', 'mark', 62, RED, 540, 700, t, 'nd', tx, 'slide', rot=-2)
    tq = at(i, 'three questions', -0.3)
    if t > tq: place_text(c, 'ASK 3 QUESTIONS', 'anton', 90, NAVY, 540, 860, t, 'aq', tq, 'pop')
    for k, (txt, ph) in enumerate([('1  WHY DID IT FALL?', 'Why did'), ('2  ARE PROFITS GROWING?', 'Are profits'), ('3  IS DEBT UNDER CONTROL?', 'debt')]):
        tk = at(i, ph, -0.3)
        if t > tk:
            p = eback(prog(t, tk, 0.4), 1.3); y = 1030 + k * 170
            place(c, card_box(860, 140, SOFT), 540, y, p, (-1, 1, -0.5)[k])
            if p > 0.6:
                place(c, text_img(txt, 'anton', 60, INK), 520, y)
                d = ImageDraw.Draw(c); d.rounded_rectangle((860, y - 30, 920, y + 30), 8, outline=GRN, width=6)
                if t > tk + 0.5: d.line((872, y, 886, y + 18, 912, y - 22), fill=GRN, width=8)


def s9(c, t):
    i = 8
    place_text(c, 'CHEAP CAN GET', 'anton', 120, CREAM, 540, 300, t, 'c1', STARTS[8] + 0.05, 'pop')
    place_text(c, 'CHEAPER', 'anton', 150, YEL, 540, 440, t, 'c2', STARTS[8] + 0.2, 'pop')
    ts = at(i, 'Save this', -0.3)
    if t > ts: place_text(c, 'save this before you buy any dip', 'mark', 56, CREAM, 540, 600, t, 'sv', ts, 'slide', rot=-2)
    tfo = at(i, 'follow', -0.2)
    if t > tfo:
        pp = prog(t, tfo, 0.35); place(c, follow_btn(), 540, 790, 0.5 + 0.5 * eback(pp), 0, clamp(pp * 3))
    for k, ln in enumerate(['Prices & charts: NSE via INDmoney, weekly closes to 23 Oct 2026.', 'Reasons: company filings & news reports, Oct 2026.', 'No buy/sell recommendation. I may hold some of these stocks.', 'Education only. Not investment advice.']):
        place_text(c, ln, 'type', 25, (210, 204, 192), 540, 960 + k * 40, t, None, STARTS[8] + 0.3, 'fade', track=1)
    tb = at(i, 'So, bargain', -0.2)
    if t > tb:
        place(c, label('BARGAIN?', GRN), 300, 1260, 1.3 * eback(prog(t, tb + 0.2, 0.35), 1.6), -5)
        place(c, label('WARNING?', RED), 780, 1260, 1.3 * eback(prog(t, tb + 0.6, 0.35), 1.6), 5)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]


def SLAMS():
    return [at(2, 'thirty two', -0.3), at(3, 'thirty five', -0.3), at(4, 'thirty two', -0.3), at(5, 'fifty nine', -0.3), at(6, 'twenty eight', -0.3)] + [STARTS[k] + 0.05 for k in range(1, 8)]


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
    b = text_img('52-WEEK LOW CHECK', 'type', 30, RED, 1); c.alpha_composite(b, (W - 52 - b.size[0], 64))
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
    if not loop: captions(c, t)
    header(c, dark, t if not loop else 0); transition(c, t)
    arr = np.asarray(c.convert('RGB')).astype(np.float32)
    g = grain_frames()[int(t * FPS) % 6]
    fl = 1 + 0.012 * math.sin(t * 37) * math.sin(t * 13)
    return np.clip(arr * fl + g[..., None], 0, 255).astype(np.uint8)
