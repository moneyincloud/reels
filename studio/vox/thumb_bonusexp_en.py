from PIL import Image, ImageDraw
from lib import *
import hook as HK
import bonusexp_en as M
c=HK.rays_bg('sky', cy=1000)
place(c,HK.fit_text('WHERE IS YOUR',140,HK.title_ink('sky')),540,230)
place(c,HK.fit_text('DIWALI BONUS GOING?',120,HK.title_ink('sky')),540,390)
place(c,M.ticket_img('?', M.RED),540,690,1.0,-3)
layer=Image.new('RGBA',(W,H),(0,0,0,0));M.cloudy(layer,540,1090,2.2,0.5,'wow');c.alpha_composite(layer)
place(c,HK.tag('4 STOPS FOR YOUR BONUS',INK,YEL,84,-3,sub='EMERGENCY FUND · DEBT · SIP · 10% FUN'),540,1440)
place(c,HK.follow_sticker(size=52),540,1720)
HK.finish(c,'../out/bonusexp_en_thumbnail.jpg')
