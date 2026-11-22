from PIL import Image, ImageDraw
from lib import *
import hook as HK
c=HK.rays_bg('gold')
place(c,HK.fit_text('₹1 LAKH IN 2021',150,CREAM),540,390)
place(c,HK.band('WHICH STOCK MADE CRORES?',84),540,580)
aw,ah=900,600
art=Image.new('RGBA',(aw,ah),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,aw-1,ah-1),28,fill=(8,20,30),outline=INK,width=8)
rows=[('CUPID','₹1.49 CR',(255,201,77)),('NURTURE WELL','₹1.28 CR',(255,201,77)),('SPECTRUM','₹89 L',(59,227,138)),('BSE','₹58 L',(59,227,138)),('PAYTM IPO','₹81 K',(255,77,94))]
for k,(n,v,col) in enumerate(rows):
    y=40+k*108
    art.alpha_composite(text_img(n,'anton',64,(233,244,247)),(50,y))
    t=text_img(v,'anton',70,col); art.alpha_composite(t,(aw-50-t.size[0],y-4))
HK.art_glow(c,art,540,980,1.0,-1.5)
place(c,HK.tag('ONLY 2 OUT OF 10',INK,YEL,100,-4,sub='REAL 2021 PRICES · NSE/BSE 20 NOV 2026'),540,1450)
place(c,HK.pill("ONE BIG IPO LOST MONEY",YEL,INK,52,maxw=980),540,1680)
HK.finish(c,'../out/crore21_thumbnail.jpg')
