from PIL import Image, ImageDraw
from lib import *
import hook as HK
import suzlon as M
c=HK.rays_bg('teal')
place(c,HK.fit_text('SUZLON',250,CREAM),540,400)
place(c,HK.band('MULTIBAGGER OR TRAP?',96),540,590)
# art: paper card with drop chart + turbine
aw,ah=900,620
art=Image.new('RGBA',(aw,ah),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,aw-1,ah-1),28,fill=(253,251,246),outline=INK,width=8)
for x in range(20,aw-20,30): d.line((x,20,x,ah-20),fill=(214,224,232),width=1)
for y in range(20,ah-20,30): d.line((20,y,aw-20,y),fill=(214,224,232),width=1)
pts=[(90,110),(150,330),(230,470),(330,520),(450,535),(560,540),(640,500),(720,380),(790,450)]
stroke(art,pts,14,INK)
for (x,y),lab,col,dy,dx in (((90,110),'₹460',INK,-70,70),((560,540),'₹8',RED,-80,0),((790,450),'₹37',GRN,75,30)):
    d.ellipse((x-16,y-16,x+16,y+16),fill=col,outline=INK,width=4)
    ti=text_img(lab,'anton',72,col); art.alpha_composite(ti,(int(x+dx-ti.size[0]/2),int(y+dy-ti.size[1]/2)))
for (x,lab) in ((90,'2008'),(560,'2023'),(790,'TODAY')):
    ti=text_img(lab,'type',28,(90,85,80),1); art.alpha_composite(ti,(int(x-ti.size[0]/2),ah-60))
M.turbine(art,640,170,0.8,0.08,INK,0)
HK.art_glow(c,art,540,990,1.0,-1.5)
place(c,HK.tag('PROFIT -69%?',INK,YEL,104,-5,sub='Q2 RESULTS · 29 OCT 2026'),540,1480)
place(c,HK.pill("DON'T BUY MORE BEFORE YOU SEE THIS",YEL,INK,48,maxw=960),540,1690)
HK.finish(c,'../out/suzlon_thumbnail.jpg')
Image.open('../out/suzlon_thumbnail.jpg').resize((540,960)).save('/tmp/claude-0/-home-claude/32ef0837-6367-50a7-8b18-d49a84afef86/scratchpad/th2.jpg')
