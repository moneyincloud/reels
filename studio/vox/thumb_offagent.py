from PIL import Image, ImageDraw
from lib import *
import hook as HK
from scenes import stamp_c
c=HK.rays_bg('teal')
place(c,HK.fit_text('YOUR AI OFFICE AGENT',140,CREAM),540,400)
place(c,HK.band('DOES THE BORING WORK',100),540,575)
aw,ah=900,560
art=Image.new('RGBA',(aw,ah),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,aw-1,ah-1),28,fill=(253,251,246),outline=INK,width=8)
for k,txt in enumerate(['Open the inbox','Read the Sales folder','Make one table','Ask before sending']):
    y=90+k*110; d.rounded_rectangle((70,y-28,126,y+28),8,fill=(253,251,246),outline=INK,width=5)
    d.line([(82,y+2),(95,y+16),(118,y-18)],fill=GRN,width=9)
    t=text_img(txt,'osw5',50,INK); art.alpha_composite(t,(160,y-34))
HK.art_glow(c,art,540,960,1.0,-1.5)
place(c,HK.tag('COMMENT "AGENT"',INK,YEL,104,-5,sub='FREE SETUP GUIDE IN YOUR DMs'),540,1440)
place(c,HK.pill('5 STEPS · 3 SAFETY RULES',YEL,INK,60,maxw=900),540,1660)
HK.finish(c,'../out/offagent_thumbnail.jpg')
