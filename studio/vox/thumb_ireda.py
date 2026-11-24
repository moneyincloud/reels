from PIL import Image, ImageDraw
from lib import *
import hook as HK
import ireda as M
c=HK.rays_bg('emerald')
place(c,HK.fit_text('IREDA',260,CREAM),540,400)
place(c,HK.band('MULTIBAGGER OR TRAP?',96),540,590)
aw,ah=900,620
art=Image.new('RGBA',(aw,ah),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,aw-1,ah-1),28,fill=(253,251,246),outline=INK,width=8)
for x in range(20,aw-20,30): d.line((x,20,x,ah-20),fill=(214,224,232),width=1)
for y in range(20,ah-20,30): d.line((20,y,aw-20,y),fill=(214,224,232),width=1)
pts=[(90,500),(200,490),(300,440),(400,300),(480,120),(560,220),(660,330),(760,360),(820,340)]
stroke(art,pts,14,INK)
for (x,y),lab,col,dy,dx in (((90,500),'₹32',INK,-70,40),((480,120),'₹310',GRN,0,-140),((820,340),'₹132',RED,-80,-20)):
    d.ellipse((x-16,y-16,x+16,y+16),fill=col,outline=INK,width=4)
    ti=text_img(lab,'anton',72,col); art.alpha_composite(ti,(int(x+dx-ti.size[0]/2),int(y+dy-ti.size[1]/2)))
for (x,lab) in ((90,'IPO 2023'),(480,'JUL 2024'),(800,'23 NOV 26')):
    ti=text_img(lab,'type',28,(90,85,80),1); art.alpha_composite(ti,(int(x-ti.size[0]/2),ah-60))
M.sun(art,690,130,0.55,0.2)
M.turbine(art,260,330,0.32,0.4,INK)
HK.art_glow(c,art,540,990,1.0,-1.5)
place(c,HK.tag('-57% FROM TOP',INK,YEL,104,-5,sub='NEW LOANS +31% · PROFIT +1% (Q2 FY27)'),540,1480)
place(c,HK.pill("NOBODY TELLS YOU THIS PART",YEL,INK,44,maxw=980),540,1690)
HK.finish(c,'../out/ireda_thumbnail.jpg')
