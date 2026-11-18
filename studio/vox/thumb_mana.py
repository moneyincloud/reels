from PIL import Image, ImageDraw
from lib import *
import hook as HK
import mana as M
c=HK.rays_bg('gold')
place(c,HK.fit_text('MANAPPURAM',190,CREAM),540,400)
place(c,HK.band('MULTIBAGGER OR TRAP?',96),540,590)
aw,ah=900,620
art=Image.new('RGBA',(aw,ah),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,aw-1,ah-1),28,fill=(253,251,246),outline=INK,width=8)
for x in range(20,aw-20,30): d.line((x,20,x,ah-20),fill=(214,224,232),width=1)
for y in range(20,ah-20,30): d.line((20,y,aw-20,y),fill=(214,224,232),width=1)
M.necklace(art,250,330,0.62,0.3,1.0)
base=540
for k,(lab,v,col) in enumerate((('Q2 FY26',217,(200,190,175)),('Q2 FY27',701,GRN))):
    hg=int(v/701*380); x=560+k*190
    d.rounded_rectangle((x-70,base-hg,x+70,base),12,fill=col,outline=INK,width=5)
    ti=text_img(f'₹{v} Cr','anton',48,INK); art.alpha_composite(ti,(int(x-ti.size[0]/2),base-hg-62))
    ti=text_img(lab,'type',26,(90,85,80),1); art.alpha_composite(ti,(int(x-ti.size[0]/2),base+14))
ti=text_img('PROFIT','type',30,(90,85,80),2); art.alpha_composite(ti,(aw-40-ti.size[0],34))
HK.art_glow(c,art,540,990,1.0,-1.5)
place(c,HK.tag('PROFIT +223%?',INK,YEL,104,-5,sub='Q2 RESULTS · 12 NOV 2026'),540,1480)
place(c,HK.pill("BUT THE STOCK FELL 4.6% ON 18 NOV",YEL,INK,50,maxw=980),540,1690)
HK.finish(c,'../out/mana_thumbnail.jpg')
