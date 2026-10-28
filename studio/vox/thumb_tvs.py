from PIL import Image, ImageDraw
from lib import *
import hook as HK
import tvs as M
c=HK.rays_bg('navy')
place(c,HK.fit_text('TVS PROFIT +52%',150,CREAM),540,470)
place(c,HK.band('1 IN 4 RUPEES COMES FROM ABROAD',84),540,630)
art=Image.new('RGBA',(M.MW+40,M.MH+40),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,M.MW+39,M.MH+39),26,fill=(253,251,246),outline=INK,width=8)
rt={'africa':0,'latam':0,'asia':0,'europe':0}
M.draw_map(art,99,20,20,tuple(rt),rt,labels=False)
HK.art_glow(c,art,540,950,0.98,0)
place(c,HK.tag('90+ COUNTRIES',RED,CREAM,110,-5,sub='Q2 RESULTS · LAST YEAR vs THIS YEAR'),540,1330)
place(c,HK.pill('WHERE TVS REALLY MAKES MONEY',YEL,INK,52,maxw=940),540,1560)
HK.finish(c,'../out/tvs_thumbnail.jpg')
Image.open('../out/tvs_thumbnail.jpg').resize((540,960)).save('../frames/th.jpg')
