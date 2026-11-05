from PIL import Image, ImageDraw
from lib import *
import hook as HK
import listx as LX
_th=HK.theme_for('parag milk dairy'); c=HK.rays_bg(_th,cy=1050)
place(c,HK.fit_text("PROFIT FELL 8%",170,HK.title_ink(_th)),540,260)
place(c,HK.band('STOCK JUMPED 17%',116,txt=(255,255,255),bg=(22,163,74)),540,455)
art=Image.new('RGBA',(960,560),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,959,559),34,fill=(255,255,255),outline=(36,50,77),width=10)
for x0,col,lc,lab,val,up in ((50,(253,236,236),(229,72,77),'PROFIT','−8%',False),(500,(231,247,236),(22,163,74),'STOCK','+17%',True)):
    d.rounded_rectangle((x0,50,x0+410,510),28,fill=col,outline=lc,width=6)
    t=text_img(lab,'osw5',40,lc); art.alpha_composite(t,(x0+205-t.size[0]//2,70))
    cx=x0+205; y=230
    pts=[(cx,y-90),(cx+70,y),(cx+28,y),(cx+28,y+90),(cx-28,y+90),(cx-28,y),(cx-70,y)] if up else [(cx,y+90),(cx+70,y),(cx+28,y),(cx+28,y-90),(cx-28,y-90),(cx-28,y),(cx-70,y)]
    d.polygon(pts,fill=lc)
    t=text_img(val,'pop',110,lc); art.alpha_composite(t,(cx-t.size[0]//2,340))
HK.art_glow(c,art,540,880,1.0,-1.2)
place(c,HK.tag('PARAG MILK FOODS',(232,123,0),CREAM,76,-5,sub='3 HIDDEN REASONS'),380,1400)
place(c,LX.pose_img(LX.POSE['gap_up'][0],470),840,1700)
place(c,HK.follow_sticker(size=54),300,1760)
HK.finish(c,'../out/paragmilk_thumbnail.jpg')
