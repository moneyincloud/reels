from PIL import Image, ImageDraw
from lib import *
import hook as HK
import listx as LX
c=HK.rays_bg('cream',cy=1050)
place(c,HK.fit_text("TASMAC STRIKE",160,INK),540,260)
place(c,HK.band('BUT ₹16,800 BONUS?',110,txt=(255,255,255),bg=(229,72,77)),540,450)
art=Image.new('RGBA',(960,560),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,959,559),34,fill=(255,255,255),outline=(36,50,77),width=10)
d.rounded_rectangle((470,60,920,500),30,fill=(255,255,255),outline=(227,220,205),width=4)
d.rounded_rectangle((470,60,920,140),30,fill=(22,163,74)); d.rectangle((470,110,920,140),fill=(22,163,74))
t=text_img('BANK ALERT','osw5',36,(255,255,255)); art.alpha_composite(t,(695-t.size[0]//2,78))
t=text_img('CREDITED','osw5',34,(140,134,118)); art.alpha_composite(t,(695-t.size[0]//2,170))
t=text_img('₹16,800','pop',96,(22,163,74)); art.alpha_composite(t,(695-t.size[0]//2,230))
t=text_img('Deepavali bonus','pop',36,INK); art.alpha_composite(t,(695-t.size[0]//2,380))
sign=Image.new('RGBA',(360,420),(0,0,0,0)); sd=ImageDraw.Draw(sign)
sd.rectangle((165,150,195,420),fill=(139,90,43)); sd.rounded_rectangle((10,20,350,200),18,fill=(229,72,77))
t=text_img('STRIKE','pop',78,(255,255,255)); sign.alpha_composite(t,(180-t.size[0]//2,62))
art.alpha_composite(sign.rotate(8,expand=False,resample=Image.BICUBIC),(50,80))
HK.art_glow(c,art,540,880,1.0,-1.2)
place(c,HK.tag('245 SUSPENDED',(229,72,77),CREAM,84,-5,sub='SO WHY THE BONUS?'),380,1400)
place(c,LX.pose_img(LX.POSE['money_rain'][0],470),840,1700)
HK.finish(c,'../out/tasmac_thumbnail.jpg')
