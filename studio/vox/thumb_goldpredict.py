from PIL import Image, ImageDraw
from lib import *
import hook as HK
import goldpredict as M
c=HK.rays_bg('gold')
place(c,HK.fit_text('GOLD RATE',170,INK),540,400)
place(c,HK.band('CAN YOU PREDICT IT?',96),540,590)
aw,ah=900,620
art=Image.new('RGBA',(aw,ah),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,aw-1,ah-1),28,fill=(253,251,246),outline=INK,width=8)
for x in range(20,aw-20,30): d.line((x,20,x,ah-20),fill=(214,224,232),width=1)
for y in range(20,ah-20,30): d.line((20,y,aw-20,y),fill=(214,224,232),width=1)
for k,(a,col) in enumerate([('COMEX $',(40,100,200)),('x RUPEE',(230,120,30)),('x 1.15 DUTY',RED)]):
    ti=text_img(a,'anton',92,col); art.alpha_composite(ti,(aw//2-ti.size[0]//2,60+k*130))
d.line((120,470,aw-120,470),fill=INK,width=6)
ti=text_img("= NEXT MORNING'S RATE",'anton',80,GRN); art.alpha_composite(ti,(aw//2-ti.size[0]//2,495))
HK.art_glow(c,art,540,990,1.0,-1.5)
place(c,HK.tag('-₹19,621 IN 9 DAYS',INK,YEL,96,-5,sub='MCX GOLD · 9 NOV TO 20 NOV 2026'),540,1480)
place(c,HK.pill("SEE IT BEFORE 9 AM",YEL,INK,52,maxw=980),540,1690)
HK.finish(c,'../out/goldpredict_thumbnail.jpg')
