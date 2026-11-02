from PIL import Image, ImageDraw
from lib import *
import hook as HK
import listx as LX
c=HK.rays_bg('maroon',cy=1000)
place(c,HK.fit_text("MUHURAT TRADING",150,CREAM),540,300)
place(c,HK.band('SUN 8 NOV · 2:20 PM',110),540,470)
art=Image.new('RGBA',(900,520),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,899,519),30,fill=(255,248,230),outline=INK,width=8)
rows=[('PRE-OPEN','2:05 PM'),('TRADING','2:20 – 3:30'),('AUCTION','3:20 – 3:30'),('SAMVAT','2083')]
for k,(a,b) in enumerate(rows):
    y=40+k*118; art.alpha_composite(text_img(a,'anton',64,INK),(40,y)); t=text_img(b,'anton',72,(200,90,20)); art.alpha_composite(t,(860-t.size[0],y-4))
    if k<3: d.line((40,y+104,860,y+104),fill=(230,210,170),width=3)
HK.art_glow(c,art,540,880,1.0,-1.5)
place(c,HK.tag('NOT EVENING!',RED,CREAM,100,-5,sub='DIWALI 2026'),400,1390)
place(c,LX.pose_img(LX.POSE['wholesome_win'][0],430),860,1720)
place(c,HK.pill('SAVE THE TIME',YEL,INK,56,maxw=440),300,1700)
HK.finish(c,'../out/muhurat_thumbnail.jpg')
