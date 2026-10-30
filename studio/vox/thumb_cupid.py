from PIL import Image, ImageDraw
from lib import *
import hook as HK
import cupid as M
c=HK.rays_bg('chai')
place(c,HK.fit_text('CUPID: 1 SHARE = 100',150,CREAM),540,380)
place(c,HK.band('7X IN 1 YEAR. HOW?',110),540,560)
aw,ah=920,620
art=Image.new('RGBA',(aw,ah),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,aw-1,ah-1),28,fill=(253,251,246),outline=INK,width=8)
d.rounded_rectangle((70,200,250,380),12,fill=M.GOLD,outline=INK,width=8)
t=text_img('1','anton',120,INK); art.alpha_composite(t,(160-t.size[0]//2,212))
ar=text_img('=','anton',150,INK); art.alpha_composite(ar,(300,190))
for k in range(100):
    r_,cc=divmod(k,10); x=430+cc*44; y=90+r_*44
    d.rounded_rectangle((x,y,x+36,y+36),6,fill=GRN,outline=INK,width=3)
t=text_img('SPLIT 1:10 + BONUS 1:1 + BONUS 4:1','osw5',34,INK); art.alpha_composite(t,(aw//2-t.size[0]//2,ah-70))
HK.art_glow(c,art,540,1000,1.0,-1.2)
place(c,HK.tag('125+ COUNTRIES · P/E 308',RED,CREAM,84,-5,sub='CONDOMS · TENDERS · FMCG · THE CATCH'),540,1480)
place(c,HK.pill("DON'T MISS THE RISK",YEL,INK,64,maxw=900),540,1700)
HK.finish(c,'../out/cupid_thumbnail.jpg')
Image.open('../out/cupid_thumbnail.jpg').resize((540,960)).save('/tmp/claude-0/-home-claude/32ef0837-6367-50a7-8b18-d49a84afef86/scratchpad/th_cupid.jpg')
