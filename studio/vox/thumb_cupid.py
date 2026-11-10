from PIL import Image, ImageDraw
from lib import *
import hook as HK
import cupid as M
c=HK.rays_bg('pink', cy=1000)
place(c,HK.fit_text('CONDOM MAKER',150,HK.title_ink('pink')),540,230)
place(c,HK.fit_text('PLANS +123%',160,YEL),540,400)
place(c,M.pose(72,760),330,960,1,-2)
for ic,x,y,r in (('pack',820,640,-10),('pack2',950,860,8),('lube',800,1060,-6),('perfume',960,1180,10)):
    place(c,M.prod_icon(ic,210),x,y,1,r)
place(c,HK.tag('CUPID: TENDERS + FMCG',INK,YEL,84,-4,sub='FY26 ₹358 CR · FY27 GUIDANCE ₹800+ CR'),540,1430)
place(c,HK.follow_sticker(size=52),540,1720)
HK.finish(c,'../out/cupid_thumbnail.jpg')
