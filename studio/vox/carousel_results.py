"""Carousel 2 Nov 2026: How to read quarterly results (5 checks) — real Q2 FY27 examples. 8 slides, 1080x1350."""
import os
from PIL import Image, ImageDraw
import twomoves as L
from lib import *
from twomoves import NAVY, GREY, ORG, SOFT, BLUE, TEAL
from scenes import stamp_c, bgs
W2, H2 = 1080, 1350
N = 8
os.makedirs('../out/carousel', exist_ok=True)


def base(dark=False, n=None):
    pbg, dbg = bgs(); c = (dbg if dark else pbg).crop((0, 0, W2, H2)).copy()
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (52, 50))
    if n: b = text_img(f'{n}/{N}', 'type', 30, RED, 1); c.alpha_composite(b, (W2 - 52 - b.size[0], 50))
    ImageDraw.Draw(c).line((60, 100, W2 - 60, 100), fill=col, width=2)
    return c


def save(c, k): c.convert('RGB').save(f'../out/carousel/results5_{k}.jpg', quality=92)


def src(c, txt, y=1290):
    sz = 26
    while sz > 16 and text_w(txt, 'type', sz, 1) > 980: sz -= 1
    place(c, text_img(txt, 'type', sz, GREY, 1), 540, y)


def hbar(c, y, name, val, vmax, col, txt=None, x0=400, wmax=460):
    d = ImageDraw.Draw(c); w = max(12, int(wmax * val / vmax))
    place(c, text_img(name, 'osw5', 46, INK), 230, y)
    d.rounded_rectangle((x0, y - 34, x0 + w, y + 34), 12, fill=col, outline=INK, width=4)
    c.alpha_composite(text_img(txt or f'+{val:g}%', 'anton', 60, col), (x0 + w + 16, int(y - 38)))


def check_slide(n, k, title, sub):
    c = base(n=n)
    place(c, L.label(f'CHECK {k}/5', NAVY), 180, 175, 1.1, -4)
    place(c, text_img(title, 'anton', 100 if len(title) < 16 else 84, INK), 540, 290)
    place(c, text_img(sub, 'mark', 50, NAVY), 540, 400, 1, -2)
    return c


# 1 cover
c = base(n=1)
place(c, text_img('SALES UP', 'anton', 150, GRN), 540, 250)
place(c, text_img('STOCK DOWN 16%?', 'anton', 120, RED), 540, 400)
place(c, L.icon('LAURUS'), 300, 600, 1.1, -4); place(c, L.icon('INTELLECT'), 780, 600, 1.1, 4)
place(c, L.label('LAURUS +7%', GRN), 300, 740, 1.2, -4); place(c, L.label('INTELLECT -16%', RED), 780, 740, 1.2, 4)
place(c, text_img('Read results in 5 checks', 'anton', 84, INK), 540, 920)
place(c, text_img('swipe >>  the last slide is a cheat sheet', 'mark', 50, NAVY), 540, 1050, 1, -2)
src(c, 'Stock moves: NSE close 30 Oct 2026, via INDmoney', 1260)
save(c, 1)

# 2 check 1: revenue
c = check_slide(2, 1, 'SALES GROWTH', 'did the business actually grow?')
place(c, L.card_box(920, 420, SOFT), 540, 690, 1, -0.5)
place(c, text_img('Q2 FY27 revenue / income, vs last year', 'osw5', 38, GREY), 540, 540)
hbar(c, 640, 'LAURUS', 33, 40, GRN); hbar(c, 740, 'TRENT', 22, 40, GRN); hbar(c, 840, 'INTELLECT', 11, 40, GRN)
place(c, text_img('All three grew.', 'anton', 80, INK), 540, 1010)
place(c, text_img("So sales alone can't explain the moves.", 'osw5', 46, RED), 540, 1110)
src(c, 'Sources: company Q2 FY27 results, 29-30 Oct 2026 (NSE filings via HDFC Sky, INDmoney news, Free Press Journal)')
save(c, 2)

# 3 check 2: profit vs sales
c = check_slide(3, 2, 'PROFIT GROWTH', 'is profit growing faster than sales?')
place(c, L.card_box(920, 520, SOFT), 540, 740, 1, 0.5)
place(c, text_img('LAURUS LABS · Q2 FY27 vs Q2 FY26', 'osw5', 38, GREY), 540, 540)
hbar(c, 650, 'REVENUE', 33, 126, GRN, x0=380, wmax=360); hbar(c, 770, 'PROFIT', 126, 126, GRN, x0=380, wmax=360)
place(c, text_img('net profit ₹441 Cr', 'anton', 70, GRN), 540, 900)
place(c, text_img('profit grew ~4x faster than sales', 'mark', 52, NAVY), 540, 1080, 1, -2)
place(c, text_img('Trent: profit +25% (₹468 Cr) on sales +22%', 'osw5', 42, INK), 540, 1170)
src(c, 'Sources: Laurus Labs results 29 Oct 2026 (NSE filing via HDFC Sky); Trent: INDmoney news 29 Oct 2026')
save(c, 3)

# 4 check 3: margins
c = check_slide(4, 3, 'MARGINS', 'how much of each ₹100 of sales is kept?')
place(c, L.card_box(920, 420, SOFT), 540, 700, 1, -0.5)
place(c, text_img('LAURUS · EBITDA MARGIN', 'osw5', 42, GREY), 540, 560)
place(c, text_img('26%', 'anton', 130, GREY), 205, 720)
marker_line(c, [(360, 720), (500, 720)], 1, GRN, 12, head=True, head_size=34)
place(c, text_img('34.5%', 'anton', 130, GRN), 750, 720)
place(c, text_img('a year ago  ->  Q2 FY27', 'type', 30, GREY), 540, 840)
place(c, text_img('Rising margins = profit grows faster', 'anton', 64, INK), 540, 1010)
place(c, text_img('Falling margins can sink a stock even when sales grow.', 'osw5', 40, RED), 540, 1100)
src(c, 'Source: Laurus Labs Q2 FY27 results, 29 Oct 2026 (NSE filing via HDFC Sky)')
save(c, 4)

# 5 check 4: expectations
c = check_slide(5, 4, 'EXPECTATIONS', 'beat or miss what the market expected?')
place(c, L.card_box(920, 460, SOFT), 540, 720, 1, 0.5)
place(c, L.icon('INTELLECT'), 220, 600, 0.8, -4)
c.alpha_composite(text_img('INTELLECT DESIGN', 'anton', 64, INK), (320, 560))
place(c, text_img('income +11% · profit ₹104 Cr vs ₹102 Cr last quarter', 'osw5', 36, INK), 540, 670)
place(c, stamp_c('REVENUE MISSED', RED, 80, -4, 991), 540, 820)
place(c, text_img('-16% in one day', 'anton', 100, RED), 540, 1040)
place(c, text_img('now 59% below its 52-week high of ₹1,245', 'osw5', 42, INK), 540, 1140)
src(c, 'Sources: company results 30 Oct 2026 (Free Press Journal, INDmoney news); price NSE 30 Oct 2026')
save(c, 5)

# 6 check 5: already priced in? (risk next to upside)
c = check_slide(6, 5, 'ALREADY PRICED IN?', 'what did the stock do before results?')
place(c, L.card_box(920, 460, SOFT), 540, 710, 1, -0.5)
c.alpha_composite(text_img('LAURUS · WEEKLY CLOSE, 12 MONTHS', 'osw5', 36, GREY), (120, 500))
pts, v = L.chart_pts('LAURUS', 140, 900, 580, 880)
d = ImageDraw.Draw(c)
for gy in (580, 730, 880): d.line((140, gy, 900, gy), fill=(225, 220, 210), width=2)
L.spark(c, pts, 1, GRN, 9)
tx, ty = pts[-1]; d.ellipse((tx - 14, ty - 14, tx + 14, ty + 14), fill=GRN, outline=INK, width=3)
place(c, L.label('₹2,406 record', GRN), 700, 610); place(c, text_img('₹982', 'anton', 44, GREY), 220, 805)
place(c, stamp_c('~2.5x IN A YEAR', GRN, 62, -4, 992), 540, 1030)
place(c, stamp_c('KOTAK: SELL RATING', RED, 56, 3, 993), 540, 1180)
src(c, 'NSE weekly closes 3 Nov 2025 - 30 Oct 2026 via INDmoney · Kotak rating: INDmoney news 28 Oct 2026', 1275)
save(c, 6)

# 7 what happened
c = base(n=7)
place(c, text_img('WHAT HAPPENED', 'anton', 110, INK), 540, 220)
place(c, text_img('stock move on 30 Oct 2026 (NSE close)', 'osw5', 42, GREY), 540, 320)
rows = [('LAURUS LABS', 'profit +126%, margins up', '+7.2%', GRN), ('TRENT', 'profit +25%, sales +22%', '+5.4%', GRN), ('INTELLECT', 'profit flat, revenue missed', '-16.3%', RED)]
for k, (nm, why, mv, col) in enumerate(rows):
    y = 500 + k * 220
    place(c, L.card_box(920, 180, SOFT), 540, y, 1, (-0.6, 0.5, -0.4)[k])
    c.alpha_composite(text_img(nm, 'anton', 62, INK), (120, int(y - 70)))
    c.alpha_composite(text_img(why, 'osw5', 38, GREY), (122, int(y + 10)))
    mt = text_img(mv, 'anton', 96, col); c.alpha_composite(mt, (960 - mt.size[0], int(y - 55)))
place(c, text_img('Stocks move on surprise, not on "good" or "bad".', 'anton', 52, NAVY), 540, 1180)
src(c, 'Prices: NSE via INDmoney. Results: company filings & news, 29-30 Oct 2026.', 1280)
save(c, 7)

# 8 cheat sheet
c = base(n=8)
place(c, text_img('RESULTS DAY', 'anton', 100, INK), 540, 200)
place(c, text_img('CHEAT SHEET', 'anton', 130, RED), 540, 320)
items = ['1  SALES: did they grow?', '2  PROFIT: faster than sales?', '3  MARGINS: up or down?', '4  EXPECTATIONS: beat or miss?', '5  PRICE: already priced in?']
for k, q in enumerate(items):
    y = 480 + k * 118; place(c, L.card_box(920, 100, SOFT), 540, y, 1, (-0.6, 0.5, -0.4, 0.6, -0.5)[k])
    c.alpha_composite(text_img(q, 'anton', 52, INK), (120, int(y - 34)))
    dd = ImageDraw.Draw(c); dd.rounded_rectangle((880, y - 28, 936, y + 28), 8, outline=GRN, width=6); dd.line((890, y, 904, y + 18, 928, y - 22), fill=GRN, width=8)
place(c, SS_b := __import__('saveshare').bookmark_icon(90), 330, 1090, 1, -8)
place(c, text_img('SAVE THIS', 'anton', 90, INK), 590, 1090)
for k, ln in enumerate(['No buy/sell recommendation. I may hold some of these stocks.', 'Education only. Not investment advice.']):
    place(c, text_img(ln, 'type', 25, GREY), 540, 1220 + k * 38)
save(c, 8)
ims = [Image.open(f'../out/carousel/results5_{k}.jpg').resize((270, 338)) for k in range(1, N + 1)]
sh = Image.new('RGB', (270 * 4, 338 * 2), 'white')
for k, m in enumerate(ims): sh.paste(m, ((k % 4) * 270, (k // 4) * 338))
sh.save('../frames/carousel.jpg')
print('carousel ok')
