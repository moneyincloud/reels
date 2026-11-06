from PIL import Image, ImageDraw
from lib import *
import hook as HK
import rbidomino as M
c=HK.rays_bg('orange', cy=1000)
place(c,HK.fit_text('RBI JUST RAISED',150,HK.title_ink('orange')),540,240)
place(c,HK.fit_text('YOUR EMI',190,HK.title_ink('orange')),540,420)
for k in range(5):
    place(c,M.dom_img(k,k<3),150+k*190,960-k*40,0.82,(-14 if k==0 else 0))
a=M.person('appa_shock',520); comp(c,a,590,1560-a.size[1]+60)
place(c,HK.tag('+₹768 A MONTH',INK,YEL,120,-4,sub='₹50 LAKH LOAN · REPO 5.25% TO 5.50%'),520,1420)
place(c,HK.follow_sticker(size=52),540,1720)
HK.finish(c,'../out/rbidomino_thumbnail.jpg')
