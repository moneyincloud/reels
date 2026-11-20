"""Carousel: know tomorrow's gold rate before 9 AM (1080x1350, 9 slides)"""
import math
from PIL import Image, ImageDraw
from lib import *
from scenes import bgs, stamp_c, warn_icon
import saveshare as SS
from goldpredict import tag, inr, gold_stack, clock, moon, sun

W2, H2 = 1080, 1350
GREY = (120, 112, 104); BLUE = (40, 100, 200); ORG = (230, 120, 30); TEAL = (20, 140, 130); GOLD = (214, 160, 40); NAVY = (36, 44, 78)
OUT = '../../autopost/media/gold-rate-tomorrow-formula-carousel-slide{}.jpg'
N = 9


def base(k, dark=False):
    p, d = bgs(); src = d if dark else p
    c = src.crop((0, 285, W2, 285 + H2)).copy()
    col = CREAM if dark else INK
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, col, 1), (56, H2 - 78))
    n = text_img(f'{k}/{N}', 'anton', 40, RED); c.alpha_composite(n, (W2 - 56 - n.size[0], H2 - 86))
    return c


def title(c, s, col=INK, y=150, size=100):
    place(c, text_img(s, 'anton', size, col), 540, y)


def lines(c, rows, y0, gap, fn='osw5', size=44, col=INK, x=None):
    for k, s in enumerate(rows):
        im = text_img(s, fn, size, col)
        if x is None: place(c, im, 540, y0 + k * gap)
        else: c.alpha_composite(im, (x, int(y0 + k * gap - im.size[1] / 2)))


def save(c, k):
    c.convert('RGB').save(OUT.format(k), quality=92)


# 1 cover
c = base(1)
place(c, text_img("TOMORROW'S", 'anton', 120, INK), 540, 250)
place(c, text_img('GOLD RATE', 'anton', 170, GOLD), 540, 400)
place(c, tag('KNOW IT BEFORE 9 AM', RED, 70), 540, 570, 1.0, -2)
place(c, SS._card(760, 300), 540, 820, 1.0, -1)
for i, (s, col) in enumerate([('COMEX $', BLUE), ('x RUPEE', ORG), ('x 1.15', RED)]):
    place(c, text_img(s, 'anton', 76, col), 540, 720 + i * 95)
place(c, text_img('One formula. 4 numbers. 30 seconds.', 'osw5', 46, INK), 540, 1060)
place(c, text_img('Swipe →'.replace('→', '>>'), 'anton', 56, RED), 540, 1160)
save(c, 1)

# 2 the stake
c = base(2, dark=True)
title(c, 'YOUR GOLD PRICE', CREAM, 170, 96)
title(c, 'IS SET IN NEW YORK', YEL, 280, 96)
moon(c, 300, 560, 70, (30, 29, 28)); clock(c, 300, 760, 150, 22, 30, (60, 70, 110), CREAM)
sun(c, 790, 560, 55, 0); clock(c, 790, 760, 150, 9, 0, CREAM, INK)
place(c, text_img('NIGHT IN INDIA', 'anton', 50, CREAM), 300, 970); place(c, text_img('Comex trades', 'osw5', 38, YEL), 300, 1025)
place(c, text_img('9:00 AM', 'anton', 50, CREAM), 790, 970); place(c, text_img('MCX opens', 'osw5', 38, YEL), 790, 1025)
place(c, text_img('By morning, the move is already done.', 'osw5', 44, CREAM), 540, 1150)
save(c, 2)

# 3 step 1
c = base(3)
place(c, tag('STEP 1', BLUE, 64), 540, 150)
title(c, 'CHECK COMEX GOLD', INK, 290, 96)
place(c, SS._card(860, 380), 540, 620, 1.0, -1)
place(c, text_img('US gold price', 'osw5', 48, GREY), 540, 500)
place(c, text_img('$ per ounce', 'anton', 110, BLUE), 540, 620)
place(c, text_img('search: "gold price" or "XAU USD"', 'osw5', 40, INK), 540, 740)
lines(c, ['Comex = US gold futures market, New York.', 'It trades almost all day and night.'], 960, 64, size=42)
place(c, text_img('Example (18 Nov 2026, 9:07 AM): $3,797', 'anton', 50, BLUE), 540, 1130)
save(c, 3)

# 4 step 2
c = base(4)
place(c, tag('STEP 2', ORG, 64), 540, 150)
title(c, 'CHECK THE RUPEE', INK, 290, 96)
place(c, SS._card(860, 380), 540, 620, 1.0, 1)
place(c, text_img('how many rupees for 1 dollar', 'osw5', 46, GREY), 540, 500)
place(c, text_img('₹ per $', 'anton', 120, ORG), 540, 620)
place(c, text_img('search: "USD INR"', 'osw5', 40, INK), 540, 740)
lines(c, ['Weaker rupee = costlier gold,', 'even if Comex does not move.'], 960, 64, size=42)
place(c, text_img('Example (18 Nov 2026 close): ₹93.44', 'anton', 50, ORG), 540, 1130)
save(c, 4)

# 5 step 3 formula
c = base(5)
place(c, tag('STEP 3', RED, 64), 540, 150)
title(c, 'THE FORMULA', INK, 290, 110)
place(c, SS._card(900, 660), 540, 720, 1.0, -0.5)
rows = [('COMEX $ / oz', BLUE), ('x  ₹ per $', ORG), ('÷  3.11', INK), ('x  1.15', RED)]
for i, (s, col) in enumerate(rows):
    place(c, text_img(s, 'anton', 84, col), 540, 470 + i * 105)
d = ImageDraw.Draw(c); d.line((180, 900, 900, 900), fill=INK, width=6)
place(c, text_img('= ₹ per 10 g', 'anton', 80, GRN), 540, 965)
lines(c, ['÷ 3.11: 1 ounce = 31.1 g, so this gives 10 g', 'x 1.15: 15% import duty (from 13 May 2026)', 'Then +3% GST when you buy'], 1130, 52, size=36, col=GREY)
save(c, 5)

# 6 real check
c = base(6)
title(c, 'REAL CHECK · 18 NOV', INK, 150, 96)
place(c, SS._card(900, 520), 540, 520, 1.0, 0.5)
rows = [('Comex (spot)', '$3,797', BLUE), ('x Rupee', '93.44', ORG), ('÷ 10 g', '3.11035', INK), ('x Duty', '1.15', RED)]
for i, (a, b, col) in enumerate(rows):
    c.alpha_composite(text_img(a, 'osw5', 50, GREY), (150, 300 + i * 105))
    v = text_img(b, 'anton', 70, col); c.alpha_composite(v, (930 - v.size[0], 290 + i * 105))
place(c, text_img('FORMULA ₹1,31,178', 'anton', 90, INK), 540, 880)
place(c, text_img('MCX OPENED ₹1,31,624', 'anton', 90, GRN), 540, 990)
place(c, stamp_c('ONLY 0.3% APART', RED, 72, -4, 4), 540, 1115)
c.alpha_composite(text_img('Spot 9:07 AM: Ascendants · rupee close: PTI · MCX: INDmoney', 'type', 24, GREY, 1), (110, 1220))
save(c, 6)

# 7 limits
c = base(7, dark=True)
place(c, warn_icon(YEL), 230, 160, 1.2)
place(c, text_img('NOT A PREDICTION', 'anton', 92, YEL), 600, 160)
cards = [('NEXT MORNING', 'you can see it early', (120, 200, 140)),
         ('NEXT MONTH', 'nobody knows', RED),
         ('DUTY CAN CHANGE', 'May 2026: 6% to 15% overnight', ORG),
         ('YOUR BILL', '+3% GST + making charges', TEAL)]
for i, (a, b, col) in enumerate(cards):
    y = 340 + i * 200
    place(c, cutout(Image.new('RGBA', (900, 160), (40, 38, 36, 255)), border=6, shadow=0.4, bcol=col), 540, y)
    c.alpha_composite(text_img(a, 'anton', 62, CREAM), (130, y - 60))
    c.alpha_composite(text_img(b, 'osw5', 40, col), (132, y + 10))
place(c, text_img('Fed, dollar, wars, central banks move Comex every night.', 'osw5', 36, CREAM), 540, 1160)
save(c, 7)

# 8 recap (screenshot slide)
c = base(8)
place(c, SS._card(960, 1060), 540, 640, 1.0, -0.3)
place(c, text_img('GOLD RATE · CHEAT SHEET', 'anton', 66, INK), 540, 190)
d = ImageDraw.Draw(c); d.line((90, 240, 990, 240), fill=INK, width=5)
rows = [('1', 'Comex gold', '$ per ounce', BLUE), ('2', 'x Rupee', '₹ per $', ORG), ('3', '÷ 3.11', 'ounce to 10 grams', INK),
        ('4', 'x 1.15', '15% import duty', RED), ('5', '+ 3% GST', 'when you buy', TEAL), ('6', '+ Making', 'jewellery only', GREY)]
for i, (n, a, b, col) in enumerate(rows):
    y = 320 + i * 120
    d.ellipse((100, y - 36, 172, y + 36), fill=col, outline=INK, width=4)
    nn = text_img(n, 'anton', 50, CREAM); c.alpha_composite(nn, (136 - nn.size[0] // 2, y - nn.size[1] // 2))
    c.alpha_composite(text_img(a, 'anton', 62, col), (200, y - 42))
    v = text_img(b, 'osw5', 42, INK); c.alpha_composite(v, (980 - v.size[0], y - 28))
place(c, text_img('Check before 9 AM on market days', 'anton', 54, GRN), 540, 1060)
save(c, 8)

# 9 CTA
c = base(9)
place(c, SS.bookmark_icon(140), 230, 330, 1.0, -8)
place(c, text_img('SAVE THIS', 'anton', 150, INK), 620, 330)
place(c, text_img('Try it Monday, before 9 AM.', 'osw5', 56, INK), 540, 520)
place(c, text_img('Comment GOLD with your answer:', 'osw5', 50, GREY), 540, 640)
place(c, text_img('how close was it to the MCX open?', 'anton', 66, RED), 540, 730)
from fridge import follow_btn
place(c, follow_btn(), 540, 900)
lines(c, ['Formula is an approximation; dealer premiums vary.', 'Not a buy/sell call. Education only.'], 1090, 50, fn='type', size=30, col=GREY)
save(c, 9)
print('ok')
