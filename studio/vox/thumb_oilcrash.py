from PIL import Image, ImageDraw
from lib import *
import hook as HK
import listx as LX
_th=HK.theme_for('oil crude crash'); c=HK.rays_bg(_th,cy=1050)
place(c,HK.fit_text("OIL CRASHED 11%",170,HK.title_ink(_th)),540,260)
place(c,HK.band('WHO WINS? WHO LOSES?',112,txt=(255,255,255),bg=(229,72,77)),540,455)
art=Image.new('RGBA',(960,560),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,959,559),34,fill=(255,255,255),outline=(36,50,77),width=10)
rows=[('IndiGo','+5.2%',True),('Asian Paints','+4.0%',True),('ONGC','-2.1%',False)]
for i,(n,v,up) in enumerate(rows):
    y=50+i*160; col=(22,163,74) if up else (229,72,77); bg=(231,247,236) if up else (253,236,236)
    d.rounded_rectangle((40,y,920,y+130),24,fill=bg,outline=col,width=5)
    art.alpha_composite(text_img(n,'pop',58,INK),(80,y+28))
    t=text_img(v,'pop',72,col); art.alpha_composite(t,(880-t.size[0],y+22))
HK.art_glow(c,art,540,880,1.0,-1.2)
place(c,HK.tag('SENSEX +1,487',(22,163,74),CREAM,84,-5,sub='5 NOV 2026'),380,1400)
place(c,LX.pose_img(LX.POSE['shock'][1],470),840,1700)
place(c,HK.follow_sticker(size=54),300 if 'oilcrash'=='oilcrash' else 300,1760)
HK.finish(c,'../out/oilcrash_thumbnail.jpg')
