from PIL import Image, ImageDraw
from lib import *
import hook as HK
import antipo as M
c=HK.rays_bg('navy')
place(c,HK.fit_text('ANTHROPIC IPO',170,CREAM),540,400)
place(c,HK.band('OPPORTUNITY OR BUBBLE?',90),540,590)
aw,ah=900,620
art=Image.new('RGBA',(aw,ah),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,aw-1,ah-1),28,fill=(253,251,246),outline=INK,width=8)
for x in range(20,aw-20,30): d.line((x,20,x,ah-20),fill=(214,224,232),width=1)
for y in range(20,ah-20,30): d.line((20,y,aw-20,y),fill=(214,224,232),width=1)
M.rocket(art,250,330,0.9,0.4)
M.bubble(art,640,300,170)
ti=text_img('?','anton',180,(80,140,210)); art.alpha_composite(ti,(640-ti.size[0]//2,300-ti.size[1]//2))
t1=text_img('NASDAQ: ANT','anton',56,INK); art.alpha_composite(t1,(aw-50-t1.size[0],ah-100))
t2=text_img('$70 – $78','anton',56,GRN); art.alpha_composite(t2,(50,ah-100))
HK.art_glow(c,art,540,990,1.0,-1.5)
place(c,HK.tag('$1.4 TRILLION?',INK,YEL,104,-5,sub='LISTS 19 NOV · 8 PM IST'),540,1480)
place(c,HK.pill("WATCH THIS BEFORE YOU INVEST",YEL,INK,50,maxw=980),540,1690)
HK.finish(c,'../out/antipo_thumbnail.jpg')
