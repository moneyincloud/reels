from PIL import Image, ImageDraw
from lib import *
import hook as HK
import irfc as M
c=HK.rays_bg('navy')
place(c,HK.fit_text('IRFC',260,CREAM),540,400)
place(c,HK.band('MULTIBAGGER OR TRAP?',96),540,590)
aw,ah=900,620
art=Image.new('RGBA',(aw,ah),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,aw-1,ah-1),28,fill=(253,251,246),outline=INK,width=8)
for x in range(20,aw-20,30): d.line((x,20,x,ah-20),fill=(214,224,232),width=1)
for y in range(20,ah-20,30): d.line((20,y,aw-20,y),fill=(214,224,232),width=1)
pts=[(90,500),(200,520),(300,470),(400,330),(480,120),(560,200),(660,330),(760,400),(820,390)]
stroke(art,pts,14,INK)
for (x,y),lab,col,dy,dx in (((90,500),'₹26',INK,-70,40),((480,120),'₹229',GRN,0,-130),((820,390),'₹81',RED,-80,-10)):
    d.ellipse((x-16,y-16,x+16,y+16),fill=col,outline=INK,width=4)
    ti=text_img(lab,'anton',72,col); art.alpha_composite(ti,(int(x+dx-ti.size[0]/2),int(y+dy-ti.size[1]/2)))
for (x,lab) in ((90,'2021'),(480,'2024'),(820,'TODAY')):
    ti=text_img(lab,'type',28,(90,85,80),1); art.alpha_composite(ti,(int(x-ti.size[0]/2),ah-60))
M.rails(art,520,40,aw-40)
M.train(art,560,520,0.42,2,M.NAVY,INK,0)
HK.art_glow(c,art,540,990,1.0,-1.5)
place(c,HK.tag('-65% FROM TOP?',INK,YEL,104,-5,sub='Q2 PROFIT +10% · 15 OCT 2026'),540,1480)
place(c,HK.pill("DON'T AVERAGE DOWN BEFORE YOU SEE THIS",YEL,INK,44,maxw=980),540,1690)
HK.finish(c,'../out/irfc_thumbnail.jpg')
