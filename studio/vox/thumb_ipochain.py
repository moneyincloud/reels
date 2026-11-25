from PIL import Image, ImageDraw
from lib import *
import hook as HK
import ipochain as M
c=HK.rays_bg('purple')
place(c,HK.fit_text('HOW AN IPO WORKS',150,CREAM),540,400)
place(c,HK.band('WHERE YOUR ₹ GOES',104),540,580)
aw,ah=900,560
art=Image.new('RGBA',(aw,ah),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,aw-1,ah-1),28,fill=(253,251,246),outline=INK,width=8)
t=text_img('LENSKART ₹7,278 CR IPO','anton',48,INK); art.alpha_composite(t,(aw//2-t.size[0]//2,40))
x0,x1=60,840; sp=x0+(x1-x0)*2150/7278
d.rounded_rectangle((x0,130,sp,300),14,fill=GRN,outline=INK,width=5); d.rounded_rectangle((sp,130,x1,300),14,fill=M.ORG,outline=INK,width=5)
for txt,cx,cy,sz in (('₹2,150',(x0+sp)/2,190,52),('COMPANY',(x0+sp)/2,255,32),('₹5,128',(sp+x1)/2,190,64),('OLD SHAREHOLDERS',(sp+x1)/2,255,32)):
    t=text_img(txt,'anton',sz,CREAM); art.alpha_composite(t,(int(cx-t.size[0]/2),int(cy-t.size[1]/2)))
for k,nm in enumerate(['BID','ALLOT','LIST','1 YEAR','TAX']):
    nd=M.node_img(nm,1 if k==3 else 2); x=110+k*170; art.alpha_composite(nd,(int(x-nd.size[0]/2),400))
d.line((110,420,790,420),fill=INK,width=3)
for k,nm in enumerate(['BID','ALLOT','LIST','1 YEAR','TAX']):
    nd=M.node_img(nm,1 if k==3 else 2); x=110+k*170; art.alpha_composite(nd,(int(x-nd.size[0]/2),400))
HK.art_glow(c,art,540,960,1.0,-1.5)
place(c,HK.tag('STT · GST · BROKERAGE · TAX',INK,YEL,80,-5,sub='THE FULL 1-YEAR CHAIN'),540,1440)
place(c,HK.pill('SAVE BEFORE YOUR NEXT IPO',YEL,INK,60,maxw=900),540,1660)
HK.finish(c,'../out/ipochain_thumbnail.jpg')
