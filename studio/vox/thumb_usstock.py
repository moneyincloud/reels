from PIL import Image, ImageDraw
from lib import *
import hook as HK
import listx as LX
import usstock as M
c=HK.rays_bg('navy',cy=1150)
place(c,HK.fit_text("BUYING US STOCKS?",150,CREAM),540,320)
place(c,HK.band('KNOW THESE 5 FIRST',112),540,490)
# 10 company chips
names=['Google','Apple','Microsoft','Amazon','Meta','Netflix','Nvidia','Visa','Coca-Cola',"McDonald's"]
chips=Image.new('RGBA',(980,330),(0,0,0,0)); d=ImageDraw.Draw(chips)
rows=[[]]; x=0
for n in names:
    t=text_img(n,'pop',40,INK); w=t.size[0]+44
    if x+w>980: rows.append([]); x=0
    rows[-1].append((t,w)); x+=w+14
for r,row in enumerate(rows):
    tot=sum(w for _,w in row)+14*(len(row)-1); x=(980-tot)//2; y=r*82
    for t,w in row:
        d.rounded_rectangle((x,y,x+w,y+66),33,fill=(252,252,250),outline=INK,width=5)
        chips.alpha_composite(t,(x+22,y+6)); x+=w+14
HK.art_glow(c,chips,540,790,1.0,0)
place(c,LX.host_img(940),540,1430)
place(c,HK.tag('TAX · FX COST · HOW TO BUY',YEL,INK,64,-4),540,1730)
HK.finish(c,'../out/usstock_thumbnail.jpg')
