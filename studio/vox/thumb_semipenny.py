from PIL import Image, ImageDraw
from lib import *
import hook as HK
c=HK.rays_bg('navy')
place(c,HK.fit_text('CHIP PENNY STOCKS',150,CREAM),540,400)
place(c,HK.band('MULTIBAGGER OR TRAP?',92),540,590)
art=Image.open('/home/claude/reels/motion/semipenny/assets/img/u5.jpg').convert('RGBA')
w=860; h=int(w*0.72); art=art.crop((0,int(art.size[1]*0.18),art.size[0],int(art.size[1]*0.18)+int(art.size[0]*0.72))).resize((w,h))
m=Image.new('L',(w,h),0); ImageDraw.Draw(m).rounded_rectangle((0,0,w-1,h-1),28,fill=255); art.putalpha(m)
d=ImageDraw.Draw(art); d.rounded_rectangle((0,0,w-1,h-1),28,outline=(255,181,71),width=8)
t=text_img('illustration','osw5',28,(200,210,215)); art.alpha_composite(t,(w-t.size[0]-18,h-t.size[1]-12))
HK.art_glow(c,art,540,1000,1.0,-1.5)
place(c,HK.tag('FACTORY SHUT. ₹358 CR VALUE.',INK,YEL,80,-4,sub='SPEL SEMICONDUCTOR · FY26 LOSS ₹23.84 CR'),540,1440)
place(c,HK.pill("5 CHIP STOCKS · REAL DATA",YEL,INK,52,maxw=980),540,1680)
HK.finish(c,'../out/semipenny_thumbnail.jpg')
