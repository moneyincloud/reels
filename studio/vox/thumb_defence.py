from PIL import Image, ImageDraw
from lib import *
import hook as HK
import defence as M
c=HK.rays_bg('navy')
place(c,HK.fit_text('10 DEFENCE STOCKS',150,CREAM),540,470)
place(c,HK.band('SOLD IN 80+ COUNTRIES',96),540,630)
art=Image.new('RGBA',(M.MW+40,M.MH+40),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,M.MW+39,M.MH+39),26,fill=(253,251,246),outline=INK,width=8)
M.draw_map(art,99,20,20,0,0,labels=False,lit_t=0)
HK.art_glow(c,art,540,950,0.98,0)
place(c,HK.tag('5 NEAR 52-WEEK LOWS',RED,CREAM,96,-5,sub='PRODUCTS · PRICES · P/E · EXPORTS'),540,1330)
place(c,HK.pill("DON'T BUY BEFORE YOU SEE THIS",YEL,INK,52,maxw=940),540,1560)
HK.finish(c,'../out/defence_thumbnail.jpg')
Image.open('../out/defence_thumbnail.jpg').resize((540,960)).save('../frames/th.jpg')
