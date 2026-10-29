from PIL import Image, ImageDraw
from lib import *
import hook as HK
import itstocks as M
c=HK.rays_bg('navy')
place(c,HK.fit_text('40 IT STOCKS',170,CREAM),540,450)
place(c,HK.band('ONLY 7 PASSED',110),540,640)
art=Image.new('RGBA',(820,560),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,819,559),26,fill=(253,251,246),outline=INK,width=8)
pas={3,9,14,20,26,31,37}
for k in range(40):
    r,cc=divmod(k,8); x=80+cc*94; y=75+r*102
    ok=k in pas; d.ellipse((x-36,y-36,x+36,y+36),fill=GRN if ok else (225,70,60),outline=INK,width=4)
    if ok: d.line((x-17,y+2,x-4,y+15,x+19,y-13),fill=CREAM,width=8,joint='curve')
    else: d.line((x-15,y-15,x+15,y+15),fill=CREAM,width=7); d.line((x-15,y+15,x+15,y-15),fill=CREAM,width=7)
HK.art_glow(c,art,540,990,0.94,0)
place(c,HK.tag('PROFIT +20%/YR · ~ZERO DEBT',RED,CREAM,74,-4,sub='FUNDAMENTALS · BUSINESS · COUNTRIES'),540,1450)
place(c,HK.pill('NPST · ZENSAR · PERSISTENT +4',YEL,INK,52,maxw=940),540,1650)
HK.finish(c,'../out/itstocks_thumbnail.jpg')
Image.open('../out/itstocks_thumbnail.jpg').resize((540,960)).save('/tmp/claude-0/-home-claude/32ef0837-6367-50a7-8b18-d49a84afef86/scratchpad/th.jpg')
