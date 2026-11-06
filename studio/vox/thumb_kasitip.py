from PIL import Image, ImageDraw
from lib import *
import hook as HK
import kasitip as M
c=HK.rays_bg('red', cy=1000)
place(c,HK.fit_text('NEVER TRUST',170,HK.title_ink('red')),540,250)
place(c,HK.fit_text("THIS UNCLE'S TIP",130,HK.title_ink('red')),540,420)
k=M.person('kasi_smug',640); comp(c,k,-60,1560-k.size[1])
a=M.person('arjun_shock',560); comp(c,a,560,1560-a.size[1]+40)
place(c,HK.tag('91% LOST MONEY',INK,YEL,110,-4,sub='SEBI DATA · F&O TRADERS FY25'),540,1430)
place(c,HK.band('SURE-SHOT TIP?',84),300,640)
place(c,HK.follow_sticker(size=52),540,1720)
HK.finish(c,'../out/kasitip_thumbnail.jpg')
