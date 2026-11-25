from PIL import Image, ImageDraw
from lib import *
import hook as HK
import ipo1125 as M
from scenes import stamp_c
c=HK.rays_bg('purple')
place(c,HK.fit_text('IPO REPORT',220,CREAM),540,400)
place(c,HK.band('₹8,981 CR IPO. RETAIL: 0.48x',84),540,580)
aw,ah=900,620
art=Image.new('RGBA',(aw,ah),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,aw-1,ah-1),28,fill=(253,251,246),outline=INK,width=8)
rows=[('MAHANADI',0.48,'RETAIL 0.48x',M.RED),('CRYSTAL CROP',9.71,'RETAIL 9.71x',GRN)]
y1=500-380*1/10
for k,(n,v,lab,col) in enumerate(rows):
    x=250+k*400; hg=int(max(14,min(v,10)/10*380)); d.rounded_rectangle((x-110,500-hg,x+110,500),14,fill=col,outline=INK,width=6)
    t=text_img(n,'osw5',40,INK); art.alpha_composite(t,(x-t.size[0]//2,515))
    t=text_img(lab,'anton',58,col); art.alpha_composite(t,(x-t.size[0]//2,int(500-hg-80 if k else y1-90)))
for xx in range(60,aw-60,34): d.line((xx,y1,xx+18,y1),fill=INK,width=5)
t=text_img('1x','anton',40,INK); art.alpha_composite(t,(30,int(y1-48)))
t=text_img('SUBSCRIPTION, FINAL DAY','type',28,M.GREY,2); art.alpha_composite(t,(aw//2-t.size[0]//2,40))
HK.art_glow(c,art,540,990,1.0,-1.5)
place(c,HK.tag('WHY?',INK,YEL,110,-5,sub='ALSO: EAAA 5.3x, OPENED +0.6%'),540,1450)
place(c,HK.pill('NEVER TRUST IPO HYPE',YEL,INK,60,maxw=900),540,1680)
HK.finish(c,'../out/ipo1125_thumbnail.jpg')
