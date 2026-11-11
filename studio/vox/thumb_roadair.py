from PIL import Image, ImageDraw
from lib import *
import hook as HK
import roadair as M
c=HK.rays_bg('orange', cy=1000)
place(c,HK.fit_text('TOLL ROAD & AIRPORT',120,HK.title_ink('orange')),540,220)
place(c,HK.fit_text('STOCKS HAVE AN END DATE',110,YEL),540,370)
d=ImageDraw.Draw(c)
for k,(lab,yr,col) in enumerate((('MUMBAI-PUNE EW','2030',M.OR),('HYDERABAD ORR','2053',M.BL),('HYDERABAD AIRPORT','2068',(40,170,100)))):
    place(c,M.card_pro(f'{lab}  {yr}','concession ends',col,860,180),540,560+k*200,1,[-2,1.5,-1][k])
place(c,M.pose(14,440),540,1250,1,-2)
place(c,HK.tag('IRB vs GMR AIRPORTS',INK,YEL,90,-4,sub='PROJECTS · CONTRACT END YEARS · RISKS'),540,1480)
place(c,HK.follow_sticker(size=48),540,1740)
HK.finish(c,'../out/roadair_thumbnail.jpg')
