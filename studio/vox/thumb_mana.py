from PIL import Image, ImageDraw
from lib import *
import hook as HK
import mana as M
c=HK.rays_bg('gold', cy=1000)
place(c,HK.fit_text('₹12,000 PROFIT',150,HK.title_ink('gold')),540,230)
place(c,HK.fit_text('PER BRANCH, PER DAY?',120,YEL if HK.title_ink('gold')!=YEL else INK),540,390)
place(c,M.pose(50,760),330,960,1,-2)
place(c,M.chain(380),820,800,1,8)
for k in range(12): place(c,M.shop(70),640+(k%4)*90,1050+(k//4)*85)
place(c,HK.tag('MANAPPURAM: 5,328 BRANCHES',INK,YEL,76,-4,sub='₹585 CR PROFIT IN 3 MONTHS'),540,1430)
place(c,HK.follow_sticker(size=52),540,1720)
HK.finish(c,'../out/mana_thumbnail.jpg')
