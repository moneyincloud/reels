from PIL import Image, ImageDraw
from lib import *
import hook as HK
import friends as M
c=HK.rays_bg('purple')
place(c,HK.fit_text('3 FRIENDS · ₹1 LAKH',150,CREAM),540,380)
place(c,HK.band('ONLY ONE GOT RICH',110),540,560)
aw,ah=920,700
art=Image.new('RGBA',(aw,ah),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,aw-1,ah-1),28,fill=(253,251,246),outline=INK,width=8)
base=410
for k,who in enumerate('RKM'):
    x=170+k*290
    hg=(110,150,0)[k]
    if hg: d.rounded_rectangle((x-80,base-hg,x+80,base),14,fill=M.COL[who],outline=INK,width=6)
    q=text_img('?','anton',150,M.COL[who]); art.alpha_composite(q,(int(x-q.size[0]/2),int(base-(hg or 0)-200)))
    f=M.friend(who,'wow','down',0.3); art.alpha_composite(f,(int(x-f.size[0]/2),base+10))
d.line((50,base,aw-50,base),fill=INK,width=6)
for k,lab in enumerate(('FD','NIFTY','GOLD')):
    t=text_img(lab,'anton',40,INK); art.alpha_composite(t,(int(170+k*290-t.size[0]/2),24))
HK.art_glow(c,art,540,1000,1.0,-1.2)
place(c,HK.tag('2006 TO 2026',RED,CREAM,96,-5,sub='FD vs NIFTY vs GOLD · REAL DATA'),540,1520)
place(c,HK.pill('GUESS WHO WON?',YEL,INK,64,maxw=900),540,1720)
HK.finish(c,'../out/friends_thumbnail.jpg')
Image.open('../out/friends_thumbnail.jpg').resize((540,960)).save('/tmp/claude-0/-home-claude/32ef0837-6367-50a7-8b18-d49a84afef86/scratchpad/th3.jpg')
