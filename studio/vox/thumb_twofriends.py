from PIL import Image, ImageDraw
from lib import *
import hook as HK
import twofriends as M
c=HK.rays_bg('green')
place(c,HK.fit_text('SAME SALARY.',150,CREAM),540,380)
place(c,HK.band('₹5.5 CR vs ₹47 LAKH',104),540,560)
aw,ah=900,560
art=Image.new('RGBA',(aw,ah),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,aw-1,ah-1),28,fill=(253,251,246),outline=INK,width=8)
for k,(nm,col,sh,v,vc) in enumerate((('ARUN',M.GRN,(90,150,110),'started at 25',M.GRN),('KARTHIK',M.ORG,(210,140,80),'started at 45',M.RED))):
    p=M.person(nm,col,sh); p=p.resize((int(p.size[0]*0.8),int(p.size[1]*0.8))); x=int(225+k*450-p.size[0]/2); art.alpha_composite(p,(x,30))
    t=text_img(v,'osw5',40,vc); art.alpha_composite(t,(int(225+k*450-t.size[0]/2),460))
HK.art_glow(c,art,540,960,1.0,-1.5)
place(c,HK.tag('WHO ARE YOU?',INK,YEL,110,-5,sub='₹10,000 SIP · SAME FUND'),540,1440)
place(c,HK.pill('TAG YOUR KARTHIK',YEL,INK,64,maxw=900),540,1660)
HK.finish(c,'../out/twofriends_thumbnail.jpg')
