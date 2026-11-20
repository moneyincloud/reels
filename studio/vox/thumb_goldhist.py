from PIL import Image, ImageDraw
from lib import *
import hook as HK
import goldhist as M
c=HK.rays_bg('navy')
place(c,HK.fit_text('GOLD 1990-2026',150,CREAM),540,400)
place(c,HK.band('WHY IT FELL. WHY IT ROSE.',86),540,590)
aw,ah=900,620
art=Image.new('RGBA',(aw,ah),(0,0,0,0))
M.bars(art,0,35,(0,35),M.GOLD,ox=0,oy=0,w=900,h=620,labels=True)
HK.art_glow(c,art,540,990,1.0,-1.5)
place(c,HK.tag('₹3,452 TO ₹1,18,421',INK,YEL,92,-5,sub='EVERY CRASH & EVERY JUMP · RBI DATA'),540,1480)
place(c,HK.pill("1991 · 1999 · 2008 · 2013 · 2020 · 2026",YEL,INK,50,maxw=980),540,1690)
HK.finish(c,'../out/goldhist_thumbnail.jpg')
