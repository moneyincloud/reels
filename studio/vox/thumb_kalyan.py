from PIL import Image, ImageDraw
from lib import *
import hook as HK
import kalyan as M
from scenes import stamp_c
_th=HK.theme_for('kalyan jewellery gold'); c=HK.rays_bg(_th, cy=900)
place(c, M.logo_card(150), 540, 190, 1.0, -2)
place(c,HK.fit_text('KALYAN JEWELLERS',140,HK.title_ink(_th)),540,400)
place(c,HK.band('1 SHOP TO 546 SHOWROOMS',90),540,555)
place(c, M.photo('showroom.jpg', 640, 0.3, 0.1, (0, -0.02), 18), 470, 940, 1.0, -3)
place(c, M.photo('jewel.jpg', 300, 0.4, 0.1, (0, 0.04), 14), 850, 1080, 1.0, 6)
M.tape(c, 470, 690, -4); M.tape(c, 850, 860, 7)
place(c,HK.tag('₹87 IPO TO ₹560',INK,YEL,96,-4,sub='MULTIBAGGER OR TRAP? · PART 1'),540,1430)
place(c,HK.follow_sticker(size=52),540,1700)
HK.finish(c,'../out/kalyan_thumbnail.jpg'); print(_th)
