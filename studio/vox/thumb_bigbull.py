from PIL import Image, ImageDraw
from lib import *
import hook as HK
import bigbull as M
from scenes import stamp_c
c=HK.rays_bg('green')
place(c,HK.fit_text('THE BIG BULL',150,CREAM),540,400)
place(c,HK.band('₹5,000 TO ₹46,000 CR',100),540,580)
aw,ah=900,560
art=Image.new('RGBA',(aw,ah),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,aw-1,ah-1),28,fill=(253,251,246),outline=INK,width=8)
for k,(v,lab,col) in enumerate(((8431,'2020',M.GREY),(30652,'2022',GRN))):
    x=250+k*400; hg=int(v/30652*380); d.rounded_rectangle((x-90,470-hg,x+90,470),12,fill=col,outline=INK,width=5)
    t=text_img(lab,'osw5',34,INK); art.alpha_composite(t,(x-t.size[0]//2,482))
    t=text_img(f'₹{v:,} CR','anton',44,INK); art.alpha_composite(t,(x-t.size[0]//2,470-hg-62))
t=text_img('HIS PORTFOLIO','type',30,M.GREY,2); art.alpha_composite(t,(40,36))
HK.art_glow(c,art,540,980,1.0,-1.5)
place(c,HK.tag('MOST CAME AFTER 55',INK,YEL,96,-5,sub='HIS PORTFOLIO 3.6X IN 2.5 YEARS'),540,1440)
place(c,HK.pill('TITAN · 20 YEARS',YEL,INK,64,maxw=900),540,1660)
HK.finish(c,'../out/bigbull_thumbnail.jpg')
