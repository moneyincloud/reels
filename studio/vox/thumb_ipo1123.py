from PIL import Image, ImageDraw
from lib import *
import hook as HK
c=HK.rays_bg('purple')
place(c,HK.fit_text('2 IPOs THIS WEEK',150,CREAM),540,390)
place(c,HK.band('WHAT DO THEY SELL?',96),540,580)
aw,ah=900,520
art=Image.new('RGBA',(aw,ah),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,aw-1,ah-1),28,fill=(253,251,246),outline=INK,width=8)
rows=[('FOODLINK','OPENS 26 NOV','weddings · restaurants · India + UAE'),('INTEGRIS','OPENS 27 NOV','medtech: heart stents · lab kits · 65+ markets')]
for k,(n,dt,sub) in enumerate(rows):
    y=50+k*250
    art.alpha_composite(text_img(n,'anton',76,INK),(50,y))
    t=text_img(dt,'anton',50,(107,63,212)); art.alpha_composite(t,(aw-50-t.size[0],y+16))
    art.alpha_composite(text_img(sub,'osw5',44,(85,85,106)),(50,y+108))
    if k==0: d.line((40,y+200,aw-40,y+200),fill=(220,212,196),width=4)
HK.art_glow(c,art,540,930,1.0,-1.5)
place(c,HK.tag('PRICE BAND: NOT OUT YET',INK,YEL,84,-4,sub='MAINBOARD · NSE + BSE · 23 NOV 2026'),540,1440)
place(c,HK.pill('BUSINESS FIRST. PRICE LATER.',YEL,INK,52,maxw=980),540,1660)
HK.finish(c,'../out/ipo1123_thumbnail.jpg')
