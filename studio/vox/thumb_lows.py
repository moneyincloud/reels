from PIL import Image, ImageDraw
from lib import *
import hook as HK
c=HK.rays_bg('navy')
place(c,HK.fit_text('GIANTS AT 52-WEEK LOWS',150,CREAM),540,510)
place(c,HK.band('BARGAIN OR TRAP?',120),540,665)
art=Image.new('RGBA',(900,560),(0,0,0,0)); d=ImageDraw.Draw(art)
pts=[(40,60),(170,30),(280,160),(400,110),(520,300),(640,250),(780,470)]
d.line(pts,fill=(226,58,44),width=46,joint='curve')
d.polygon([(860,540),(720,500),(830,400)],fill=(226,58,44))
for x,y in ((170,30),(400,110),(640,250)):
    d.ellipse((x-26,y-26,x+26,y+26),fill=(255,214,51),outline=(0,0,0),width=8)
HK.art_glow(c,art,540,910,0.62,0)
place(c,HK.tag('UP TO -59%',RED,CREAM,96,-6,sub='FROM 52-WEEK HIGH'),540,1225)
place(c,HK.pill('HUL · MARUTI · DMART · SWIGGY · NTPC',YEL,INK,46,maxw=940),540,1430)
HK.finish(c,'../out/52week_lows_thumbnail.jpg')
im=Image.open('../out/52week_lows_thumbnail.jpg')
sh=Image.new('RGB',(1080,640),(255,255,255)); sh.paste(im.resize((360,640)),(0,0)); sh.paste(im.crop((0,240,1080,1680)).resize((360,480)),(360,80)); sh.paste(im.crop((0,420,1080,1500)).resize((360,360)),(720,140)); sh.save('../frames/th.jpg')
