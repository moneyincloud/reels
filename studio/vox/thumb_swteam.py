from PIL import Image, ImageDraw
from lib import *
import hook as HK
import swteam as M
c=HK.rays_bg('navy')
place(c,HK.fit_text('8 AI AGENTS. 1 HUMAN.',140,CREAM),540,400)
place(c,HK.band('ONE SOFTWARE COMPANY',100),540,575)
aw,ah=900,560
art=Image.new('RGBA',(aw,ah),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,aw-1,ah-1),28,fill=(253,251,246),outline=INK,width=8)
for k,(nm,col) in enumerate(M.ROLES):
    r_,cc=divmod(k,4); dk=M.desk(nm,col); x=int(120+cc*220-dk.size[0]/2); y=int(150+r_*250-dk.size[1]/2)
    art.alpha_composite(dk,(x,y))
HK.art_glow(c,art,540,960,1.0,-1.5)
place(c,HK.tag('DEVELOPER · TESTER · RELEASE',INK,YEL,80,-5,sub='ONE WEEK INSIDE'),540,1440)
place(c,HK.pill('YOU APPROVE EVERYTHING',YEL,INK,60,maxw=900),540,1660)
HK.finish(c,'../out/swteam_thumbnail.jpg')
