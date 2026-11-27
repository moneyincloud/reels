from PIL import Image, ImageDraw
from lib import *
import hook as HK
import qual15 as M
c=HK.rays_bg('green')
place(c,HK.fit_text('15 SMALL CAPS',150,CREAM),540,390)
place(c,HK.band("PASSED NSE'S QUALITY TEST",88),540,570)
aw,ah=900,560
art=Image.new('RGBA',(aw,ah),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,aw-1,ah-1),28,fill=(253,251,246),outline=INK,width=8)
for k,r in enumerate([M.Q[j] for j in (11,1,7,5,14)]):
    y=36+k*100
    art.alpha_composite(text_img(r[0],'osw5',44,INK),(40,y))
    v=text_img(f'ROCE {r[4]:.0f}%','anton',48,M.GRN); art.alpha_composite(v,(860-v.size[0],y-4))
HK.art_glow(c,art,540,960,1.0,-1.5)
place(c,HK.tag('HIGH ROE · LOW DEBT',INK,YEL,100,-5,sub='WHAT EACH ONE DOES'),540,1440)
place(c,HK.pill('BUT QUALITY ≠ CHEAP'.replace('≠','IS NOT'),YEL,INK,58,maxw=900),540,1660)
HK.finish(c,'../out/qual15_thumbnail.jpg')
