from PIL import Image, ImageDraw
from lib import *
import hook as HK
import animals as A
c=HK.rays_bg('green')
place(c,HK.fit_text('MORE MONEY, STILL LOST?',150,CREAM),540,510)
place(c,HK.band('TORTOISE vs HARE',120),540,665)
art=Image.new('RGBA',(1100,600),(0,0,0,0))
h=A.hare('cry','head'); h=h.resize((int(h.size[0]*0.6),int(h.size[1]*0.6)))
tt=A.tortoise('happy',0,1.0,True)
art.alpha_composite(h,(80,0)); art.alpha_composite(tt,(420,170))
HK.art_glow(c,art,540,950,0.75,0)
place(c,HK.tag('-₹37 LAKH',RED,CREAM,104,-6,sub='WHY THE HARE LOST'),540,1285)
place(c,HK.pill('ANIMAL FRIDAY · TIME vs MONEY',YEL,INK,50,maxw=940),540,1460)
HK.finish(c,'../out/tortoise_thumbnail.jpg')
im=Image.open('../out/tortoise_thumbnail.jpg')
sh=Image.new('RGB',(1080,640),(255,255,255)); sh.paste(im.resize((360,640)),(0,0)); sh.paste(im.crop((0,240,1080,1680)).resize((360,480)),(360,80)); sh.paste(im.crop((0,420,1080,1500)).resize((360,360)),(720,140)); sh.save('../frames/th.jpg')
