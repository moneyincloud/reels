from PIL import Image, ImageDraw
from lib import *
import hook as HK
import listx as LX
c=HK.rays_bg('green',cy=1150)
place(c,HK.fit_text("DON'T INVEST ₹1",150,CREAM),540,330)
place(c,HK.band('UNTIL YOU HAVE THESE 4',100),540,500)
# 4 icon tiles in a row
tiles=Image.new('RGBA',(960,250),(0,0,0,0)); d=ImageDraw.Draw(tiles)
for k,fn in enumerate(LX.ICONS if hasattr(LX,'ICONS') else [LX.ico_jar,LX.ico_umbrella,LX.ico_heart,LX.ico_plant]):
    x=k*240+10
    d.rounded_rectangle((x,10,x+220,240),26,fill=(252,252,250),outline=INK,width=7)
    d.ellipse((x+8,18,x+56,66),fill=INK); n=text_img(str(k+1),'pop',34,(252,252,250)); tiles.alpha_composite(n,(x+32-n.size[0]//2,20))
    fn(tiles,x+120,135+(10 if k==1 else 0),0.72 if k!=1 else 0.75)
HK.art_glow(c,tiles,540,760,1.0,0)
host=LX.host_img(980)
place(c,host,540,1420)
place(c,HK.pill('SAVE BEFORE YOUR 1ST SIP',YEL,INK,62,maxw=880),540,1770)
HK.finish(c,'../out/invest4_thumbnail.jpg')
