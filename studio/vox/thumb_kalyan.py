from PIL import Image, ImageDraw
from lib import *
import hook as HK
import kalyan as M
from scenes import stamp_c
_th=HK.theme_for('kalyan jewellery gold'); c=HK.rays_bg(_th)
place(c,HK.fit_text('KALYAN JEWELLERS',150,HK.title_ink(_th)),540,330)
place(c,HK.band('1 SHOP TO 546 SHOWROOMS',96),540,500)
aw,ah=900,600
art=Image.new('RGBA',(aw,ah),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,aw-1,ah-1),28,fill=(253,251,246),outline=INK,width=8)
vals=[9771,8573,14071,25045,35743]; labs=['FY19','FY21','FY23','FY25','FY26']; cols=[M.GREY,M.GREY,M.BLUE,M.BLUE,GRN]
for k,v in enumerate(vals):
    x=130+k*160; hg=int(v/35743*380); d.rounded_rectangle((x-58,500-hg,x+58,500),12,fill=cols[k],outline=INK,width=5)
    t=text_img(labs[k],'osw5',30,INK); art.alpha_composite(t,(x-t.size[0]//2,512))
t=text_img('SALES (₹ CR)','type',30,M.GREY,2); art.alpha_composite(t,(40,40))
st=stamp_c('3.7X SALES',GRN,64,-6,3); art.alpha_composite(st,(60,110))
HK.art_glow(c,art,540,920,1.0,-1.5)
place(c,HK.tag('₹87 IPO TO ₹560',INK,YEL,100,-5,sub='MULTIBAGGER OR TRAP? · PART 1'),540,1390)
place(c,HK.follow_sticker(size=54),540,1680,)
HK.finish(c,'../out/kalyan_thumbnail.jpg'); print(_th)
