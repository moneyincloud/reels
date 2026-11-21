from PIL import Image, ImageDraw
from lib import *
import hook as HK
import antday1 as M
c = HK.rays_bg('navy')
place(c, HK.fit_text('ANTHROPIC LISTED', 150, CREAM), 540, 470)
place(c, HK.band('DAY 1 · +17%  |  DAY 2 · -8.5%', 80), 540, 640)
aw, ah = 900, 560
art = Image.new('RGBA', (aw, ah), (0, 0, 0, 0)); d = ImageDraw.Draw(art)
d.rounded_rectangle((0, 0, aw - 1, ah - 1), 28, fill=(253, 251, 246), outline=INK, width=8)
for x in range(20, aw - 20, 30): d.line((x, 20, x, ah - 20), fill=(214, 224, 232), width=1)
for y in range(20, ah - 20, 30): d.line((20, y, aw - 20, y), fill=(214, 224, 232), width=1)
def Y(v): return 500 - (v - 78) / (118 - 78) * 440
# IPO line
x = 40
while x < aw - 40: d.line((x, Y(83), x + 26, Y(83)), fill=M.PURPLE, width=7); x += 44
for cx, k in ((300, M.D1), (580, M.D2)):
    d.line((cx, Y(k['h']), cx, Y(k['l'])), fill=INK, width=9)
    y0, y1 = sorted((Y(k['o']), Y(k['c']))); d.rectangle((cx - 70, y0, cx + 70, y1), fill=RED, outline=INK, width=6)
t1 = text_img('IPO $83', 'anton', 50, M.PURPLE); art.alpha_composite(t1, (aw - 40 - t1.size[0], int(Y(83)) - 64))
t2 = text_img('OPEN $111.50', 'anton', 50, GRN); art.alpha_composite(t2, (400, 50))
t3 = text_img('NOW $88.91', 'anton', 50, INK); art.alpha_composite(t3, (660, int(Y(88.91)) - 80))
HK.art_glow(c, art, 540, 960, 0.92, -1.5)
place(c, HK.tag('OPENING BUYERS: -20%', INK, YEL, 90, -5, sub='ANT · NASDAQ · 19–20 NOV 2026'), 540, 1400)
place(c, HK.pill('MADE WITH CLAUDE · CHECK EVERY NUMBER', YEL, INK, 40, maxw=900), 540, 1570)
HK.finish(c, '../out/antday1_thumbnail.jpg')
