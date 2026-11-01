from PIL import Image, ImageDraw
from lib import *
import hook as HK
import listx as LX
c=HK.rays_bg('navy',cy=1050)
place(c,HK.fit_text("6 STRONG MID CAPS",150,CREAM),540,300)
place(c,HK.band('THAT PASS 3 TESTS',110),540,470)
art=Image.new('RGBA',(940,560),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,939,559),30,fill=(250,250,246),outline=INK,width=8)
names=[('1','Abbott India','ROE 34%'),('2','Nippon AMC','ROE 34%'),('3','Oracle Fin.','ROE 33%'),('4','Colgate','ROE 83%'),('5','Mazagon Dock','ROE 29%'),('6','Coromandel','ROE 16%')]
for k,(n,nm,r) in enumerate(names):
    x=40+(k%2)*450; y=40+(k//2)*165
    d.rounded_rectangle((x,y,x+420,y+140),22,fill=(232,246,240),outline=INK,width=4)
    d.ellipse((x+18,y+34,x+90,y+106),fill=(34,170,110)); t=text_img(n,'anton',54,(252,252,250)); art.alpha_composite(t,(x+54-t.size[0]//2,y+38))
    art.alpha_composite(text_img(nm,'pop',38,INK),(x+108,y+22)); art.alpha_composite(text_img(r,'osw5',30,(34,140,100)),(x+110,y+82))
HK.art_glow(c,art,540,920,1.0,-1.2)
place(c,HK.tag('PROMOTERS > 50%',RED,CREAM,76,-5,sub='ROE > 15% · LOW DEBT'),400,1420)
place(c,LX.pose_img(LX.POSE['celebrate'][1],440),860,1720)
HK.finish(c,'../out/midcap6_thumbnail.jpg')
