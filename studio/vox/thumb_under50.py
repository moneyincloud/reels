from PIL import Image
from lib import *
import hook as HK
import under50 as M
c=HK.rays_bg('navy')
place(c,HK.fit_text('UNDER ₹50 STOCKS',150,CREAM),540,470)
place(c,HK.band('I TESTED 10 · ONLY 5 PASSED',92),540,630)
art=Image.new('RGBA',(980,640),(0,0,0,0))
from PIL import ImageDraw
ImageDraw.Draw(art).rounded_rectangle((0,0,979,639),30,fill=(253,251,246),outline=INK,width=8)
for k,(nm,col,ok) in enumerate([('SUZLON',M.TEAL,1),('YES BANK',M.BLUE,0),('IOB',M.NAVY,1),('IRB',M.ORG,0),('SYNCOM',M.PURP,1),('JP POWER',M.GOLD,0)]):
    lb=M.label(nm,col); x=40+(k%2)*480; y=50+(k//2)*200
    art.alpha_composite(lb,(x,y))
    st=M.stamp_c('PASSED' if ok else 'FAILED',GRN if ok else RED,52,-6,40+k)
    art.alpha_composite(st,(x+lb.size[0]+10,y-10))
HK.art_glow(c,art,540,960,0.92,0)
place(c,HK.tag('STRONG OR TRAP?',RED,CREAM,104,-5,sub='5 RULES · REAL DATA · 28 OCT 2026'),540,1420)
place(c,HK.pill("DON'T BUY CHEAP BEFORE YOU SEE THIS",YEL,INK,46,maxw=960),540,1620)
HK.finish(c,'../out/under50_thumbnail.jpg')
Image.open('../out/under50_thumbnail.jpg').resize((540,960)).save('../frames/th.jpg')
