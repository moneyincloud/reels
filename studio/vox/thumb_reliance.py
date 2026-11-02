from PIL import Image, ImageDraw
from lib import *
import hook as HK
import listx as LX
c=HK.rays_bg('green',cy=1050)
place(c,HK.fit_text("RELIANCE +11.6%",160,CREAM),540,300)
place(c,HK.band('BEST DAY IN 6.5 YEARS',104),540,470)
art=Image.new('RGBA',(900,520),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,899,519),30,fill=(250,250,246),outline=INK,width=8)
rows=[('PROFIT','+41%',(34,170,110)),('OIL & CHEM','+68%',(34,170,110)),('JIO USERS','542 M',(40,110,200)),('RETAIL PROFIT','-24%',(225,80,70))]
for k,(a,b,col) in enumerate(rows):
    y=40+k*118; art.alpha_composite(text_img(a,'anton',64,INK),(40,y)); t=text_img(b,'anton',72,col); art.alpha_composite(t,(860-t.size[0],y-4))
    if k<3: d.line((40,y+104,860,y+104),fill=(220,220,214),width=3)
HK.art_glow(c,art,540,880,1.0,-1.5)
place(c,HK.tag('RALLY OR TRAP?',RED,CREAM,100,-5,sub='Q2 FY27 RESULTS'),420,1390)
place(c,LX.pose_img(LX.POSE['jackpot'][0],430),860,1720)
place(c,HK.pill('2 NOV 2026',YEL,INK,56,maxw=400),280,1700)
HK.finish(c,'../out/reliance_thumbnail.jpg')
