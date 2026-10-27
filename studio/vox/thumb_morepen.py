from PIL import Image, ImageDraw
from lib import *
import hook as HK
import morepen as M
c=HK.rays_bg('navy')
place(c,HK.fit_text('MOREPEN: 4X IN 7 MONTHS',140,CREAM),540,480)
place(c,HK.band('PROFIT DOUBLED TODAY',100),540,640)
art=Image.new('RGBA',(960,560),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((10,10,950,550),30,fill=(253,251,246),outline=INK,width=8)
v=M.CLOSES; lo,hi=33.05,max(v)
pts=[(300+620*k/(len(v)-1),480-400*(p-lo)/(hi-lo)) for k,p in enumerate(v)]
stroke(art,pts,14,GRN)
art.alpha_composite(M.meter_icon(),(40,150))
HK.art_glow(c,art,540,960,0.95,0)
place(c,HK.tag('MULTIBAGGER OR TRAP?',RED,CREAM,96,-5,sub='Q2 RESULTS · 27 OCT 2026'),540,1360)
place(c,HK.pill("DON'T BUY BEFORE YOU SEE THIS",YEL,INK,50,maxw=940),540,1580)
HK.finish(c,'../out/morepen_thumbnail.jpg')
Image.open('../out/morepen_thumbnail.jpg').resize((540,960)).save('../frames/th.jpg')
