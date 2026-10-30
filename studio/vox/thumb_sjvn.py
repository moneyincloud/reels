from PIL import Image, ImageDraw
from lib import *
import hook as HK
import sjvn as M
c=HK.rays_bg('navy')
place(c,HK.fit_text('SJVN',250,CREAM),540,390)
place(c,HK.band('MULTIBAGGER OR TRAP?',96),540,590)
aw,ah=900,560
art=Image.new('RGBA',(aw,ah),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,aw-1,ah-1),28,fill=(253,251,246),outline=INK,width=8)
for k,(lab,val,col,arrow) in enumerate((('PROFIT','+114%',GRN,'up'),('STOCK','-41%',RED,'down'))):
    x=230+k*440
    t=text_img(lab,'anton',64,INK); art.alpha_composite(t,(x-t.size[0]//2,40))
    v=text_img(val,'anton',130,col); art.alpha_composite(v,(x-v.size[0]//2,150))
    if arrow=='up': d.polygon([(x,360),(x-70,460),(x+70,460)],fill=col,outline=INK)
    else: d.polygon([(x,470),(x-70,370),(x+70,370)],fill=col,outline=INK)
d.line((aw//2,40,aw//2,ah-40),fill=(210,204,192),width=5)
HK.art_glow(c,art,540,1000,1.0,-1.5)
place(c,HK.tag('READ THE FINE PRINT',RED,CREAM,96,-5,sub='Q2 RESULTS · 30 OCT 2026'),540,1460)
place(c,HK.pill("DON'T DECIDE BEFORE YOU SEE THIS",YEL,INK,50,maxw=960),540,1680)
HK.finish(c,'../out/sjvn_thumbnail.jpg')
