from PIL import Image, ImageDraw
from lib import *
import hook as HK
import cupidq2 as M
c=HK.rays_bg('pink', cy=1000)
place(c,HK.fit_text('CUPID +7.6% TODAY',130,HK.title_ink('pink')),540,220)
place(c,HK.fit_text('WHY? READ THIS FIRST',110,YEL),540,370)
place(c,M.card_pro('REVENUE +122%','Q2 FY27 · ₹188 cr',M.PK,820,170),540,560,1,-2)
place(c,M.card_pro('PROFIT +133%','but margin fell to 29%',(230,70,70),820,170),540,750,1,1.5)
place(c,M.pose(2,440),540,1200,1,-2)
place(c,HK.tag('P/E 300+. TOO HOT?',INK,YEL,90,-4,sub='THE CATCH IN THE RESULTS'),540,1480)
place(c,HK.follow_sticker(size=48),540,1740)
HK.finish(c,'../out/cupidq2_thumbnail.jpg')
