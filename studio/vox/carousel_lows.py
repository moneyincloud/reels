from PIL import Image, ImageDraw
import lows2 as L
from lib import *
from lows2 import NAVY, GREY, ORG, SOFT, BLUE, TEAL
from scenes import stamp_c, bgs
W2, H2 = 1080, 1350
def base(dark=False, n=None):
    pbg, dbg = bgs(); c = (dbg if dark else pbg).crop((0, 0, W2, H2)).copy()
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 50))
    if n: b = text_img(f'{n}/7', 'type', 30, RED, 1); c.alpha_composite(b, (W2 - 52 - b.size[0], 50))
    ImageDraw.Draw(c).line((60, 100, W2 - 60, 100), fill=col, width=2)
    return c
def save(c, k): c.convert('RGB').save(f'../out/carousel/52week_lows_{k}.jpg', quality=92)
# 1 cover
c = base(n=1)
place(c, text_img('5 GIANTS AT', 'anton', 120, INK), 540, 230)
place(c, text_img('52-WEEK LOWS', 'anton', 140, RED), 540, 370)
for k, nm in enumerate(L.ORDER):
    x = (240, 540, 840, 380, 700)[k]; y = (560, 560, 560, 780, 780)[k]
    place(c, L.icon(nm), x, y - 70, 0.6); place(c, L.label(nm, L.STK[nm][5]), x, y + 20, 1.1, (-4, 3, -2, 4, -3)[k])
place(c, L.label('BARGAIN?', GRN), 300, 1010, 1.4, -5); place(c, L.label('WARNING?', RED), 780, 1010, 1.4, 5)
place(c, text_img('swipe to see why each one fell >>', 'mark', 54, NAVY), 540, 1170, 1, -2)
place(c, text_img('NSE close, 23 Oct 2026', 'type', 28, GREY), 540, 1270)
save(c, 1)
R = {'HUL': ['PROFIT SLIPPED', 'INPUT COSTS UP', 'DETERGENT PRICES RAISED'], 'MARUTI': ['SEPT SALES UP', 'MARGINS IN FOCUS', 'Q2 RESULTS: 27 OCT'],
     'DMART': ['REVENUE +18%', 'MARGINS NARROWED', 'TARGETS CUT'], 'SWIGGY': ['-17% IN ONE DAY', 'INSTAMART LOSSES WIDER'],
     'NTPC': ['NUCLEAR + GREEN PLANS', 'COAL SUPPLY WORRIES', 'BIG SPENDING AHEAD']}
RC = [RED, ORG, NAVY]
for s, key in enumerate(L.ORDER):
    nm, sub, hi, lo, pct, col = L.STK[key]
    c = base(n=s + 2)
    place(c, text_img(nm, 'anton', 100 if len(nm) < 14 else 84, INK), 540, 200)
    place(c, text_img(sub, 'osw5', 42, col), 540, 290)
    place(c, L.card_box(900, 520, SOFT), 540, 610, 1, -0.6)
    pts, v = L.chart_pts(key, 170, 910, 430, 720)
    d = ImageDraw.Draw(c)
    for gy in (430, 575, 720): d.line((170, gy, 910, gy), fill=(225, 220, 210), width=2)
    L.spark(c, pts, 1, RED, 9)
    kh = v.index(max(v)); hx, hy = pts[kh]
    d.ellipse((hx - 11, hy - 11, hx + 11, hy + 11), fill=YEL, outline=INK, width=3)
    place(c, text_img('52W HIGH ' + L.rs(hi), 'osw5', 36, GREY), min(max(hx, 300), 780), hy - 38 if hy > 470 else 395)
    tx, ty = pts[-1]; d.ellipse((tx - 14, ty - 14, tx + 14, ty + 14), fill=RED, outline=INK, width=3)
    place(c, text_img('NOW ' + L.rs(lo), 'anton', 62, RED), 700, 800); place(c, L.icon(key), 250, 800, 0.75, -5)
    place(c, text_img('weekly close · last 12 months', 'type', 22, GREY), 540, 850)
    place(c, stamp_c(pct, RED, 130, -7, 900 + s), 540, 990)
    for k, r in enumerate(R[key]): place(c, L.label(r, RC[k % 3] if not r.startswith(('SEPT', 'REVENUE', 'NUCLEAR')) else GRN), 540, 1110 + k * 82, 1.0, (-2, 2, -1)[k])
    save(c, s + 2)
# 7 questions + disclaimer
c = base(n=7)
place(c, text_img('A 52-WEEK LOW IS', 'anton', 96, INK), 540, 200)
place(c, text_img('NOT A DISCOUNT', 'anton', 120, RED), 540, 320)
place(c, text_img('ask these 3 questions first', 'mark', 56, NAVY), 540, 440, 1, -2)
for k, q in enumerate(['1  WHY DID IT FALL?', '2  ARE PROFITS STILL GROWING?', '3  IS THE DEBT UNDER CONTROL?']):
    y = 580 + k * 160; place(c, L.card_box(900, 130, SOFT), 540, y, 1, (-1, 1, -0.5)[k]); place(c, text_img(q, 'anton', 56, INK), 540, y)
place(c, text_img('Cheap can get cheaper.', 'anton', 70, INK), 540, 1060)
for k, ln in enumerate(['Prices & charts: NSE via INDmoney, weekly closes to 23 Oct 2026.', 'Reasons: company filings & news reports, Oct 2026.', 'No buy/sell recommendation. I may hold some of these stocks.', 'Education only. Not investment advice.']):
    place(c, text_img(ln, 'type', 25, GREY), 540, 1160 + k * 38)
save(c, 7)
ims = [Image.open(f'../out/carousel/52week_lows_{k}.jpg').resize((270, 338)) for k in range(1, 8)]
sh = Image.new('RGB', (270 * 7, 338), 'white')
for k, m in enumerate(ims): sh.paste(m, (k * 270, 0))
sh.save('../frames/carousel.jpg')
