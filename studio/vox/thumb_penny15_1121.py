from PIL import Image, ImageDraw
from lib import *
import hook as HK
th = 'blue'
c = HK.rays_bg(th, cy=1000)
g = Image.open('../penny15_1121/grid.png').convert('RGBA').crop((20, 345, 1060, 1215))
card = Image.new('RGBA', (g.size[0] + 40, g.size[1] + 40), (27, 27, 31, 255)); card.alpha_composite(g, (20, 20))
place(c, HK.fit_text('15 PENNY STOCKS', 150, HK.title_ink(th)), 540, 420)
place(c, HK.band('16–20 NOV 2026', 90), 540, 575)
place(c, card, 540, 975, 0.66, -2)
place(c, HK.tag('ONLY 4 ROSE. ALL BANKS', (30, 158, 90), (255, 255, 255), 76, -4, sub='LOW PRICE IS NOT CHEAP'), 540, 1370)
place(c, HK.follow_pill(size=40), 540, 1545)
HK.finish(c, '../out/penny15_1121_thumbnail.jpg')
print('ok')
