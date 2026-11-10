from PIL import Image, ImageDraw
from lib import *
import hook as HK
import cipla as M
c=HK.rays_bg('green', cy=1000)
place(c,HK.fit_text('CIPLA SELLS IN',140,HK.title_ink('green')),540,230)
place(c,HK.fit_text('86 COUNTRIES',170,YEL),540,400)
place(c,M.pose(34,760),330,960,1,-2)
place(c,M.med_icon('globe',300),820,720,1,0)
for ic,x,y,r in (('inhaler',760,1000,-8),('heart',930,1000,8),('vial',860,1170,-6)):
    place(c,M.med_icon(ic,180),x,y,1,r)
place(c,HK.tag('WHERE ITS MONEY COMES FROM',INK,YEL,72,-4,sub='INDIA 48% · US 22% · AFRICA 16% · EM & EUROPE 13%'),540,1430)
place(c,HK.follow_sticker(size=52),540,1720)
HK.finish(c,'../out/cipla_thumbnail.jpg')
