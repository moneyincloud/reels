from PIL import Image, ImageDraw
from lib import *
import hook as HK
import listx as LX
c=HK.rays_bg('cream',cy=1050)
place(c,HK.fit_text("AI OFFICE",190,INK),540,260)
place(c,HK.band('IDEA TO LIVE APP, END TO END',92,txt=(255,255,255),bg=(124,92,252)),540,450)
art=Image.new('RGBA',(960,580),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,959,579),34,fill=(255,255,255),outline=(36,50,77),width=10)
R=[('CEO','/office-hours',(124,92,252)),('PRODUCT MGR','/spec',(47,111,237)),('ARCHITECT','/plan-eng-review',(19,161,150)),('DESIGNER','/plan-design-review',(224,85,155)),
   ('DEV TEAM','/review',(22,163,74)),('TESTER','/qa',(229,72,77)),('SECURITY','/cso',(71,85,105)),('RELEASE','/ship',(232,123,0))]
for i,(r,cmd,col) in enumerate(R):
    x=40+(i%2)*450; y=40+(i//2)*128
    d.rounded_rectangle((x,y,x+430,y+108),20,fill=(251,250,247),outline=col,width=5)
    art.alpha_composite(text_img(r,'osw5',40,col),(x+24,y+12))
    art.alpha_composite(text_img(cmd,'pop',30,INK),(x+24,y+60))
HK.art_glow(c,art,540,900,1.0,-1.2)
place(c,HK.tag('CHENNAI · 8 AI ROLES',(232,123,0),CREAM,70,-5,sub='HOW IT WORKS'),380,1430)
place(c,LX.pose_img(LX.POSE['celebrate'][0],470),840,1700)
HK.finish(c,'../out/aioffice_thumbnail.jpg')
