from PIL import Image, ImageDraw
from lib import *
import hook as HK
c=HK.rays_bg('purple')
place(c,HK.fit_text('3 MONEY QUESTIONS',150,CREAM),540,510)
place(c,HK.band('MOST PEOPLE GET #3 WRONG',100),540,665)
art=Image.new('RGBA',(960,560),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((10,10,950,550),30,fill=(253,251,246),outline=INK,width=8)
t1=text_img('YOUR MONEY FALLS 50%.','anton',78,INK); art.alpha_composite(t1,(480-t1.size[0]//2,40))
t2=text_img('RISE NEEDED TO GET BACK?','anton',70,RED); art.alpha_composite(t2,(480-t2.size[0]//2,140))
for k,(L,s) in enumerate((('A','+50%'),('B','+75%'),('C','+100%'))):
    x=60+300*k; d.rounded_rectangle((x,290,x+260,500),24,fill=(240,236,255),outline=INK,width=6)
    a=text_img(L,'anton',60,(30,60,120)); art.alpha_composite(a,(x+130-a.size[0]//2,300))
    b=text_img(s,'anton',80,INK); art.alpha_composite(b,(x+130-b.size[0]//2,380))
HK.art_glow(c,art,540,900,0.66,0)
place(c,HK.tag('3 SECONDS. GO.',RED,CREAM,84,-5,sub='ANSWER INSIDE'),540,1270)
place(c,HK.pill('MONEY QUIZ · CAN YOU GET 3/3?',YEL,INK,52,maxw=940),540,1460)
HK.finish(c,'../out/quiz3_thumbnail.jpg')
im=Image.open('../out/quiz3_thumbnail.jpg')
sh=Image.new('RGB',(1080,640),(255,255,255)); sh.paste(im.resize((360,640)),(0,0)); sh.paste(im.crop((0,240,1080,1680)).resize((360,480)),(360,80)); sh.paste(im.crop((0,420,1080,1500)).resize((360,360)),(720,140)); sh.save('../frames/th.jpg')
