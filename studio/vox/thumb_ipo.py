from PIL import Image, ImageDraw
from lib import *
import hook as HK
import ipo as M
c=HK.rays_bg('maroon')
place(c,HK.fit_text('IPO REGRET CLUB',150,CREAM),540,380)
place(c,HK.band('5 OF 9 STILL BELOW IPO PRICE',84),540,560)
aw,ah=920,640
art=Image.new('RGBA',(aw,ah),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,aw-1,ah-1),28,fill=(253,251,246),outline=INK,width=8)
rows=['ZOM','NYKAA','PAYTM','SWIGGY','OLA']
for k,key in enumerate(rows):
    y=60+k*112; pc=M.chg(key); up=pc>=0
    nm=text_img(M.D[key][0].split(' /')[0],'anton',62,INK); art.alpha_composite(nm,(50,y))
    v=text_img(f'{pc:+.0f}%','anton',74,GRN if up else RED); art.alpha_composite(v,(aw-50-v.size[0],y-6))
    d.line((40,y+100,aw-40,y+100),fill=(220,212,196),width=3)
HK.art_glow(c,art,540,1010,1.0,-1.5)
place(c,HK.tag('ONE IPO WENT 4X',INK,YEL,100,-5,sub='PAYTM · LIC · SWIGGY · ZOMATO · 9 IPOs'),540,1530)
place(c,HK.pill('TAG THE FRIEND WHO APPLIED',YEL,INK,56,maxw=960),540,1730)
HK.finish(c,'../out/ipo_thumbnail.jpg')
Image.open('../out/ipo_thumbnail.jpg').resize((540,960)).save('/tmp/claude-0/-home-claude/32ef0837-6367-50a7-8b18-d49a84afef86/scratchpad/th_ipo.jpg')
