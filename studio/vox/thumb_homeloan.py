from PIL import Image, ImageDraw
from lib import *
import hook as HK
import homeloan as M
c=HK.rays_bg('red')
place(c,HK.fit_text('₹50 LAKH HOME LOAN?',140,CREAM),540,390)
place(c,HK.band('YOU PAY ₹50 L MORE IN INTEREST',76),540,570)
aw,ah=900,560
art=Image.new('RGBA',(aw,ah),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,aw-1,ah-1),28,fill=(253,251,246),outline=INK,width=8)
h=M.house(300); art.alpha_composite(h,(40,(ah-h.size[1])//2))
for k,(a,b) in enumerate((('13th EMI','-₹9 L'),('EMI +5%/yr','-₹17.7 L'),('₹1 L/yr prepay','-₹17 L'))):
    y=90+k*140; art.alpha_composite(text_img(a,'osw5',42,INK),(380,y)); v=text_img(b,'anton',56,M.GRN); art.alpha_composite(v,(870-v.size[0],y-8))
HK.art_glow(c,art,540,960,1.0,-1.5)
place(c,HK.tag('CUT IT BY ₹17 LAKH',INK,YEL,100,-5,sub='4 SIMPLE TRICKS'),540,1440)
place(c,HK.pill('REDUCE TENURE, NOT EMI',YEL,INK,60,maxw=900),540,1660)
HK.finish(c,'../out/homeloan_thumbnail.jpg')
