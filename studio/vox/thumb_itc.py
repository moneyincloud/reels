from PIL import Image, ImageDraw
from lib import *
import hook as HK
import itc as M
c=HK.rays_bg('sky', cy=1000)
place(c,HK.fit_text('YOU USE ITC',170,HK.title_ink('sky')),540,230)
place(c,HK.fit_text('EVERY DAY. BUT…',120,HK.title_ink('sky')),540,400)
place(c,M.logo_card(180),540,640,1,-3)
for n,x,y,r in [('aashirvaad.png',190,960,-7),('darkfantasy.png',540,990,3),('yippee.png',890,960,7)]:
    place(c,M.print_card(n,300),x,y,1,r)
place(c,HK.tag('74% OF PROFIT',INK,YEL,120,-4,sub='STILL FROM CIGARETTES · Q2 FY27'),540,1420)
place(c,HK.follow_sticker(size=52),540,1720)
HK.finish(c,'../out/itc_thumbnail.jpg')
