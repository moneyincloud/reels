from PIL import Image, ImageDraw
from lib import *
import hook as HK
import indai as M
c=HK.rays_bg('purple')
place(c,HK.fit_text('MY STOCK APP + AI',150,CREAM),540,510)
place(c,HK.band('IT ANSWERED IN 5 SECONDS',96),540,665)
art=Image.new('RGBA',(900,560),(0,0,0,0))
art.alpha_composite(M.phone_img().resize((230,416)),(80,60)); art.alpha_composite(M.laptop_img(),(360,130))
d=ImageDraw.Draw(art); d.line((320,300,410,300),fill=(255,214,51),width=18)
HK.art_glow(c,art,540,920,0.72,0)
place(c,HK.tag('READ-ONLY',(36,138,84),CREAM,100,-6,sub='CAN IT TRADE? NO'),540,1225)
place(c,HK.pill('INDMONEY x CLAUDE · HOW TO CONNECT',YEL,INK,48,maxw=940),540,1430)
HK.finish(c,'../out/indai_thumbnail.jpg')
im=Image.open('../out/indai_thumbnail.jpg')
sh=Image.new('RGB',(1080,640),(255,255,255)); sh.paste(im.resize((360,640)),(0,0)); sh.paste(im.crop((0,240,1080,1680)).resize((360,480)),(360,80)); sh.paste(im.crop((0,420,1080,1500)).resize((360,360)),(720,140)); sh.save('../frames/th.jpg')
