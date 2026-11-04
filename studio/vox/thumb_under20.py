from PIL import Image, ImageDraw
from lib import *
import hook as HK
import listx as LX
c=HK.rays_bg('cream',cy=1050)
place(c,HK.fit_text("STOCKS UNDER ₹20",150,INK),540,270)
place(c,HK.band('16 OF 22 ON EXCHANGE WATCH',96,txt=(255,255,255),bg=(229,72,77)),540,450)
art=Image.new('RGBA',(960,560),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,959,559),34,fill=(255,255,255),outline=(36,50,77),width=10)
rows=[('Syncom Formulations','NOT ON WATCH'),('R M Drip & Sprinklers','NOT ON WATCH'),('Osia Hyper Retail','ON WATCH'),('Zeal Aqua','ON WATCH'),('Bridge Securities','ON WATCH'),('Moksh Ornaments','ON WATCH')]
for i,(n,tg) in enumerate(rows):
    y=36+i*84; ok=tg=='NOT ON WATCH'
    d.rounded_rectangle((36,y,924,y+70),16,fill=(231,247,236) if ok else (253,236,236),outline=(22,163,74) if ok else (229,72,77),width=3)
    art.alpha_composite(text_img(n,'pop',38,INK),(60,y+12))
    d.rounded_rectangle((660,y+12,904,y+58),12,fill=(22,163,74) if ok else (229,72,77))
    t=text_img(tg,'osw5',30,(255,255,255)); art.alpha_composite(t,(782-t.size[0]//2,y+16))
HK.art_glow(c,art,540,880,1.0,-1.2)
place(c,HK.tag('TOP 6 EXPLAINED',(232,123,0),CREAM,84,-5,sub='BUSINESS + FUNDAMENTALS'),380,1400)
place(c,LX.pose_img(LX.POSE['shock'][3],470),840,1700)
HK.finish(c,'../out/under20_thumbnail.jpg')
