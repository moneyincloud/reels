from PIL import Image, ImageDraw
from lib import *
import hook as HK
import storyreel as M
c=HK.rays_bg('gold', cy=1000)
place(c,HK.fit_text('NEVER SPEND',170,HK.title_ink('gold')),540,240)
place(c,HK.fit_text('YOUR NEXT RAISE',140,HK.title_ink('gold')),540,410)
k=Image.open(M.LAY+'fg08.png').convert('RGBA');k=k.crop(k.getchannel('A').point(lambda v:255 if v>120 else 0).getbbox());k=k.resize((900,int(k.size[1]*900/k.size[0])));comp(c,k,90,560)
place(c,M.tag('+₹15,000 HIKE',M.GRN,size=60),250,640,1,-6)
place(c,M.stamp_c('₹0 SAVED',M.RED,90,-8,3),820,700)
place(c,HK.tag('₹34 LAKH MISSED',INK,YEL,110,-4,sub='THE RAISE THAT DISAPPEARED · EP 1'),540,1430)
place(c,HK.follow_sticker(size=52),540,1720)
HK.finish(c,'../out/storyreel_thumbnail.jpg')
