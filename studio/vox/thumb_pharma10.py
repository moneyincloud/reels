from PIL import Image, ImageDraw
from lib import *
import hook as HK
import pharma10 as M
c=HK.rays_bg('blue', cy=1000)
place(c,HK.fit_text('10 MID CAP',160,HK.title_ink('blue')),540,230)
place(c,HK.fit_text('PHARMA STOCKS',140,YEL),540,390)
for k,(ic,x,y,r) in enumerate((('pill',820,640,-12),('inhaler',930,860,10),('syringe',800,1060,-8),('tube',960,1180,12))):
    place(c,M.med_icon(ic,220),x,y,1,r)
place(c,M.pose(34,760),330,920,1,-2)
place(c,HK.tag('WHAT THEY MAKE',INK,YEL,96,-4,sub='INHALERS · INSULIN · ANTIBIOTICS · INJECTABLES'),540,1430)
place(c,HK.follow_sticker(size=52),540,1720)
HK.finish(c,'../out/pharma10_thumbnail.jpg')
