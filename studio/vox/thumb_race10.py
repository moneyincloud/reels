from PIL import Image, ImageDraw
from lib import *
import hook as HK
import listx as LX
c=HK.rays_bg('night',cy=1050)
place(c,HK.fit_text("₹1 LAKH IN 2016",150,CREAM),540,300)
place(c,HK.band('4 CHOICES. 1 WINNER.',112),540,470)
art=Image.new('RGBA',(940,640),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,939,639),30,fill=(250,250,246),outline=INK,width=8)
rows=[('CASH',1.0,(150,150,150)),('FD',1.85,(90,140,210)),('NIFTY',2.96,(34,170,110)),('?',4.71,(232,176,40))]
for k,(n,v,col) in enumerate(rows):
    y=90+k*140; d.text((40,y-30),n,font=font('anton',64),fill=INK)
    x0=280; w=int(v/4.71*600)
    d.rounded_rectangle((x0,y-34,x0+w,y+34),18,fill=col,outline=INK,width=5)
    lab='₹?.??L' if n=='?' else f'₹{v:.2f}L'
    t=text_img(lab,'pop',40,INK); art.alpha_composite(t,(x0+w-t.size[0]-14 if n=='?' else x0+w+12,y-28))
HK.art_glow(c,art,540,960,1.0,-1.5)
place(c,HK.tag('YOURS LOST?',RED,CREAM,100,-5,sub='10 YEARS · REAL DATA'),400,1450)
place(c,HK.pill('WAIT FOR THE TWIST',YEL,INK,58,maxw=560),340,1740)
place(c,LX.pose_img(24,400),860,1735)
HK.finish(c,'../out/race10_thumbnail.jpg')
