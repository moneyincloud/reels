from PIL import Image, ImageDraw
from lib import *
import hook as HK
c=HK.rays_bg('maroon')
place(c,HK.fit_text('SALES GREW. STOCK -16%',150,CREAM),540,510)
place(c,HK.band('WHY?',130),540,665)
art=Image.new('RGBA',(900,560),(0,0,0,0)); d=ImageDraw.Draw(art)
# left: green rising line (Laurus), right: red falling line (Intellect) - shapes follow the real 1y trends
g=[(30,470),(120,450),(200,420),(280,330),(360,250),(420,110)]
r=[(480,90),(560,200),(640,260),(720,250),(800,330),(860,470)]
d.line(g,fill=(46,160,90),width=40,joint='curve'); d.polygon([(400,40),(470,120),(380,140)],fill=(46,160,90))
d.line(r,fill=(226,58,44),width=40,joint='curve'); d.polygon([(890,540),(800,490),(880,420)],fill=(226,58,44))
d.line((450,20,450,540),fill=(255,214,51),width=10)
HK.art_glow(c,art,540,930,0.6,0)
place(c,HK.tag('+7% vs -16%',RED,CREAM,104,-6,sub='SAME DAY · 30 OCT'),540,1270)
place(c,HK.pill('LAURUS LABS · INTELLECT DESIGN',YEL,INK,50,maxw=940),540,1460)
HK.finish(c,'../out/twomoves_thumbnail.jpg')
im=Image.open('../out/twomoves_thumbnail.jpg')
sh=Image.new('RGB',(1080,640),(255,255,255)); sh.paste(im.resize((360,640)),(0,0)); sh.paste(im.crop((0,240,1080,1680)).resize((360,480)),(360,80)); sh.paste(im.crop((0,420,1080,1500)).resize((360,360)),(720,140)); sh.save('../frames/th.jpg')
