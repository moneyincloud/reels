from PIL import Image, ImageDraw
from lib import *
import hook as HK
import ccard as M
c=HK.rays_bg('purple', cy=1000)
place(c,HK.fit_text('NEVER PAY ONLY',150,HK.title_ink('purple')),540,240)
place(c,HK.fit_text('THE MINIMUM DUE',140,YEL),540,400)
place(c,M.cc_img(),720,780,1.05,-10)
a=M.person('arjun_shock',640); comp(c,a,-40,1560-a.size[1]+40)
place(c,HK.tag('₹2,100 IN 1 MONTH',INK,YEL,100,-4,sub='INTEREST + GST ON A ₹50,000 BILL'),540,1430)
place(c,HK.band('CREDIT CARD TRAP',76),760,1080)
place(c,HK.follow_sticker(size=52),540,1720)
HK.finish(c,'../out/ccard_thumbnail.jpg')
