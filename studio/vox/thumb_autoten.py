from PIL import Image, ImageDraw
from lib import *
import hook as HK
import autoten as M
c=HK.rays_bg('navy')
place(c,HK.fit_text('10 AUTO STOCKS',150,CREAM),540,390)
place(c,HK.band('RECORD SALES. STOCKS DOWN?',84),540,570)
aw,ah=900,560
art=Image.new('RGBA',(aw,ah),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,aw-1,ah-1),28,fill=(253,251,246),outline=INK,width=8)
rows=[M.D[k] for k in (1,0,3,5,9)]
for r,row in enumerate(rows):
    nm,ch=row[0],row[6]; y=40+r*100
    art.alpha_composite(text_img(nm,'osw5',44,INK),(40,y))
    v=text_img(f'{ch:+.0f}%','anton',60,M.GRN if ch>0 else M.RED); art.alpha_composite(v,(860-v.size[0],y-8))
HK.art_glow(c,art,540,960,1.0,-1.5)
place(c,HK.tag('CARS DOWN, BIKES UP',INK,YEL,96,-5,sub='TOP SELLERS · EXPORT MARKETS'),540,1440)
place(c,HK.pill('MARUTI · TATA · TVS · HERO +6',YEL,INK,58,maxw=900),540,1660)
HK.finish(c,'../out/autoten_thumbnail.jpg')
