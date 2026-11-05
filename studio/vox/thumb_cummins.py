from PIL import Image, ImageDraw
from lib import *
import hook as HK
import listx as LX
_th=HK.theme_for('cummins crash results'); c=HK.rays_bg(_th,cy=1050)
place(c,HK.fit_text("SALES GREW.",170,HK.title_ink(_th)),540,250)
place(c,HK.band('STOCK CRASHED 14%',112,txt=INK,bg=(255,200,61)),540,445)
art=Image.new('RGBA',(960,520),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rectangle((0,0,959,519),fill=(36,24,46)); d.rectangle((10,10,949,509),fill=(255,255,255))
for i,(n,v,up) in enumerate([('SALES','+4%',True),('PROFIT','-27%',False),('MARGIN','22% TO 15%',False)]):
    y=40+i*155; col=(31,157,85) if up else (229,72,77); bg=(221,246,230) if up else (255,225,225)
    d.rectangle((40,y,920,y+130),fill=col); d.rectangle((48,y+8,912,y+122),fill=bg)
    art.alpha_composite(text_img(n,'pop',60,INK),(84,y+26))
    t=text_img(v,'pop',76,col); art.alpha_composite(t,(880-t.size[0],y+16))
HK.art_glow(c,art,540,850,1.0,0)
place(c,HK.tag('₹18,000 CR GONE',(36,24,46),CREAM,80,-5,sub='CUMMINS INDIA · 5 NOV'),420,1300)
place(c,HK.follow_sticker(size=54),300,1700)
place(c,LX.pose_img(LX.POSE['shock'][1],470),840,1700)
HK.finish(c,'../out/cummins_thumbnail.jpg')
print(_th)
