from PIL import Image, ImageDraw
from lib import *
import hook as HK
import hypecheck as M
c=HK.rays_bg('red')
place(c,HK.fit_text('"MULTIBAGGER" LIST',140,CREAM),540,390)
place(c,HK.band('10 OUT OF 10 FELL',110),540,570)
aw,ah=900,560
art=Image.new('RGBA',(aw,ah),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,aw-1,ah-1),28,fill=(253,251,246),outline=INK,width=8)
for k,(nm,a,b) in enumerate(M.STK[:6]):
    y=36+k*74
    art.alpha_composite(text_img(nm,'osw5',40,INK),(40,y))
    v=text_img(f'{100*(b/a-1):+.0f}%','anton',52,M.RED); art.alpha_composite(v,(860-v.size[0],y-6))
t=text_img('...and 4 more','type',30,M.GREY,1); art.alpha_composite(t,(40,y+86))
HK.art_glow(c,art,540,960,1.0,-1.5)
place(c,HK.tag('₹1 LAKH TO ₹63,810',INK,YEL,96,-5,sub='HYPE vs REALITY'),540,1440)
place(c,HK.pill('PENNY STOCKS · CHECK FIRST',YEL,INK,60,maxw=900),540,1660)
HK.finish(c,'../out/hypecheck_thumbnail.jpg')
