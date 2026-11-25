"""Daily 'Gold Today' carousel (1080x1350, PCJ paper-collage look). python3 carousel_goldday.py ../goldday/<YYYY-MM-DD>.json
JSON: {"date":"2026-11-25","comex":3559.9,"comex_prev":3651.4,"comex_note":"Comex settle 24 Nov (GoldSeek)",
       "usdinr":92.84,"usdinr_note":"USD/INR 24 Nov (Trading Economics)","mcx_prev":122329,"mcx_note":"MCX Gold Dec fut close 24 Nov (INDmoney)",
       "check":{"date":"2026-11-24","est":123100,"mcx_open":122900}}   # check = yesterday's estimate vs MCX open (optional)
Writes ../../autopost/media/gold-today-<date>-slide{1..N}.jpg and prints the estimate."""
import sys, json, datetime
from PIL import Image, ImageDraw
from lib import *
from scenes import bgs, stamp_c, warn_icon
import saveshare as SS
from goldpredict import tag, gold_stack

J = json.load(open(sys.argv[1]))
W2, H2 = 1080, 1350
GREY = (120, 112, 104); BLUE = (40, 100, 200); ORG = (230, 120, 30); TEAL = (20, 140, 130); GOLD = (214, 160, 40)
DT = datetime.date.fromisoformat(J['date']); DS = DT.strftime('%d %b').upper().lstrip('0')
EST = J['comex'] * J['usdinr'] / 3.11035 * 1.15
DIFF = EST - J['mcx_prev']
SLIDES = []
def inr(v):
    s = f'{int(round(v)):d}'
    if len(s) > 3:
        h, t = s[:-3], s[-3:]; h = ','.join([h[max(0, i - 2):i] for i in range(len(h), 0, -2)][::-1]); s = h + ',' + t
    return '₹' + s
def base(dark=False):
    p, d = bgs(); c = (d if dark else p).crop((0, 285, W2, 285 + H2)).copy()
    c.alpha_composite(text_img('@moneyincloud', 'type', 30, CREAM if dark else INK, 1), (56, H2 - 78)); return c
def num(c, k, n):
    t = text_img(f'{k}/{n}', 'anton', 40, RED); c.alpha_composite(t, (W2 - 56 - t.size[0], H2 - 86))
def foot(c, s, col=GREY):
    c.alpha_composite(text_img(s, 'type', 24, col, 1), (70, 1205))

# 1 cover
c = base()
place(c, text_img('GOLD TODAY', 'anton', 150, INK), 540, 200)
place(c, tag(DS + ' · BEFORE 9 AM', RED, 64), 540, 340, 1.0, -2)
place(c, SS._card(900, 540), 540, 680, 1.0, -1)
place(c, text_img('Formula estimate · 24K · 10 g', 'osw5', 44, GREY), 540, 490)
place(c, text_img(inr(EST), 'anton', 170, GOLD), 540, 640)
up = DIFF >= 0
place(c, text_img(f'{"UP" if up else "DOWN"} {inr(abs(DIFF))} vs MCX close', 'anton', 60, GRN if up else RED), 540, 800)
place(c, text_img('before GST and making charges', 'osw5', 38, GREY), 540, 860)
place(c, text_img('Swipe for the maths >>', 'anton', 56, RED), 540, 1060)
SLIDES.append(c)
# 2 comex
c = base()
place(c, tag('STEP 1 · COMEX', BLUE, 64), 540, 160)
place(c, text_img('GOLD IN NEW YORK', 'anton', 96, INK), 540, 300)
place(c, SS._card(860, 420), 540, 640, 1.0, -1)
place(c, text_img('$ per ounce', 'osw5', 48, GREY), 540, 500)
place(c, text_img(f'${J["comex"]:,.1f}', 'anton', 150, BLUE), 540, 640)
if J.get('comex_prev'):
    ch = (J['comex'] / J['comex_prev'] - 1) * 100
    place(c, text_img(f'{"+" if ch >= 0 else ""}{ch:.2f}% vs previous', 'anton', 58, GRN if ch >= 0 else RED), 540, 780)
place(c, text_img('It traded all night while India slept.', 'osw5', 44, INK), 540, 960)
foot(c, 'Source: ' + J['comex_note'])
SLIDES.append(c)
# 3 rupee
c = base()
place(c, tag('STEP 2 · RUPEE', ORG, 64), 540, 160)
place(c, text_img('RUPEES PER DOLLAR', 'anton', 96, INK), 540, 300)
place(c, SS._card(860, 420), 540, 640, 1.0, 1)
place(c, text_img('₹ per $', 'osw5', 48, GREY), 540, 500)
place(c, text_img(f'₹{J["usdinr"]:.2f}', 'anton', 150, ORG), 540, 640)
place(c, text_img('Weaker rupee = costlier gold', 'anton', 54, INK), 540, 780)
foot(c, 'Source: ' + J['usdinr_note'])
SLIDES.append(c)
# 4 maths
c = base()
place(c, tag('STEP 3 · THE MATHS', RED, 64), 540, 150)
place(c, SS._card(920, 760), 540, 640, 1.0, -0.5)
rows = [('Comex $ / oz', f'{J["comex"]:,.1f}', BLUE), ('x Rupee', f'{J["usdinr"]:.2f}', ORG), ('÷ to 10 g', '3.11035', INK), ('x Duty 15%', '1.15', RED)]
for i, (a, b, col) in enumerate(rows):
    c.alpha_composite(text_img(a, 'osw5', 50, GREY), (140, 320 + i * 105))
    v = text_img(b, 'anton', 72, col); c.alpha_composite(v, (940 - v.size[0], 308 + i * 105))
d = ImageDraw.Draw(c); d.line((140, 760, 940, 760), fill=INK, width=6)
place(c, text_img('= ' + inr(EST) + ' / 10 g', 'anton', 92, GRN), 540, 830)
place(c, text_img(f'+3% GST = {inr(EST * 1.03)}  ·  22K ~ {inr(EST * 0.916 * 1.03 / 10)} / g', 'osw5', 40, INK), 540, 930)
foot(c, 'Duty 15% since 13 May 2026. Shops add making charges.')
SLIDES.append(c)
# 5 yesterday's check (track record)
if J.get('check'):
    k = J['check']; e, o = k['est'], k['mcx_open']; gap = abs(e / o - 1) * 100
    c = base()
    place(c, text_img("YESTERDAY'S CHECK", 'anton', 110, INK), 540, 180)
    place(c, SS._card(900, 520), 540, 560, 1.0, 0.5)
    kd = datetime.date.fromisoformat(k['date']).strftime('%d %b').lstrip('0')
    c.alpha_composite(text_img(f'Formula ({kd})', 'osw5', 50, GREY), (150, 380)); v = text_img(inr(e), 'anton', 76, INK); c.alpha_composite(v, (930 - v.size[0], 368))
    c.alpha_composite(text_img('MCX opened', 'osw5', 50, GREY), (150, 500)); v = text_img(inr(o), 'anton', 76, GRN); c.alpha_composite(v, (930 - v.size[0], 488))
    place(c, stamp_c(f'{gap:.1f}% APART', RED if gap > 1 else GRN, 84, -4, 4), 540, 700)
    place(c, text_img('We show the miss too. Every day.', 'anton', 56, INK), 540, 950)
    foot(c, 'MCX Gold front-month futures open, INDmoney')
    SLIDES.append(c)
# 6 CTA + limits
c = base(dark=True)
place(c, warn_icon(YEL), 220, 190, 1.1)
place(c, text_img('ESTIMATE, NOT A FORECAST', 'anton', 70, YEL), 610, 190)
for i, (a, col) in enumerate([('Comex can move before 9 AM', CREAM), ('Duty or GST changes move it overnight', CREAM), ('Jewellery adds making charges', CREAM)]):
    place(c, text_img('• ' + a, 'osw5', 46, col), 540, 380 + i * 80)
place(c, SS.bookmark_icon(120), 300, 720, 1.0, -8)
place(c, text_img('SAVE + FOLLOW', 'anton', 100, CREAM), 640, 720)
place(c, text_img('New gold card every market day, before 9 AM', 'osw5', 42, YEL), 540, 860)
place(c, text_img('Not a buy/sell call. Education only.', 'type', 32, CREAM, 1), 540, 1080)
SLIDES.append(c)
N = len(SLIDES); out = []
for k, c in enumerate(SLIDES, 1):
    num(c, k, N); p = f'../../autopost/media/gold-today-{J["date"]}-slide{k}.jpg'; c.convert('RGB').save(p, quality=92); out.append(p.split('/')[-1])
json.dump({'date': J['date'], 'est': round(EST), 'slides': out}, open(sys.argv[1].replace('.json', '.out.json'), 'w'))
print('estimate', round(EST), 'diff', round(DIFF), out)
