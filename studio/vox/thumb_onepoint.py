from PIL import Image, ImageDraw
from lib import *
import hook as HK
import listx as LX
c=HK.rays_bg('teal',cy=1050)
place(c,HK.fit_text("₹72 STOCK",170,CREAM),540,300)
place(c,HK.band('MAY ANSWER YOUR BANK CALLS',92),540,470)
art=Image.new('RGBA',(900,560),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,899,559),30,fill=(250,250,246),outline=INK,width=8)
vals=[('FY21',102),('FY22',132),('FY23',140),('FY24',170),('FY25',256),('FY26',313)]
for k,(y,v) in enumerate(vals):
    x=70+k*130; h=int(v/313*330)
    d.rounded_rectangle((x,450-h,x+90,450),12,fill=(34,170,110) if k==5 else (180,214,198),outline=INK,width=5)
    t=text_img(y,'osw5',30,INK); art.alpha_composite(t,(x+45-t.size[0]//2,462))
t=text_img('SALES ₹ CR','type',28,(120,120,120),2); art.alpha_composite(t,(40,30))
t=text_img('JUNE QTR +129%','pop',44,(34,170,110)); art.alpha_composite(t,(470,34))
HK.art_glow(c,art,540,900,1.0,-1.5)
place(c,HK.tag('MULTIBAGGER OR TRAP?',RED,CREAM,84,-5,sub='ONE POINT ONE SOLUTIONS'),450,1390)
place(c,LX.pose_img(LX.POSE['speculator'][0],420),860,1725)
place(c,HK.pill('DEBT 4.7X?',YEL,INK,60,maxw=420),300,1700)
HK.finish(c,'../out/onepoint_thumbnail.jpg')
