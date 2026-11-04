import json
from PIL import Image, ImageDraw
from lib import *
import hook as HK
c=HK.rays_bg('navy')
place(c,HK.fit_text('5 DAYS DECIDED THE YEAR',150,CREAM),540,510)
place(c,HK.band('NOBODY TELLS YOU',110),540,665)
# art: the real NIFTY 50 one-year line with the 5 best days marked green
D=json.load(open('../bestdays/closes.json')); v=D['closes']; lo,hi=min(v),max(v)
art=Image.new('RGBA',(900,560),(0,0,0,0)); d=ImageDraw.Draw(art)
pts=[(30+840*k/(len(v)-1),40+480*(hi-p)/(hi-lo)) for k,p in enumerate(v)]
d.line(pts,fill=(245,240,228),width=14,joint='curve')
for k in D['best5']:
    x,y=pts[k]; d.ellipse((x-26,y-26,x+26,y+26),fill=(46,160,90),outline=(255,214,51),width=8)
HK.art_glow(c,art,540,900,0.62,0)
place(c,HK.tag('-7% TO -17%',RED,CREAM,110,-5,sub='MISS JUST 5 DAYS'),540,1270)
place(c,HK.pill('NIFTY 50 · PAST 1 YEAR',YEL,INK,52,maxw=940),540,1460)
HK.finish(c,'../out/bestdays_thumbnail.jpg')
im=Image.open('../out/bestdays_thumbnail.jpg')
sh=Image.new('RGB',(1080,640),(255,255,255)); sh.paste(im.resize((360,640)),(0,0)); sh.paste(im.crop((0,240,1080,1680)).resize((360,480)),(360,80)); sh.paste(im.crop((0,420,1080,1500)).resize((360,360)),(720,140)); sh.save('../frames/th.jpg')
