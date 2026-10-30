from PIL import Image, ImageDraw
from lib import *
import hook as HK
import pcj2 as M
from scenes import stamp_c
c=HK.rays_bg('maroon')
place(c,HK.fit_text('PC JEWELLER · PART 2',140,CREAM),540,380)
place(c,HK.band('DEBT FREE. BUT -23%?',104),540,560)
aw,ah=900,600
art=Image.new('RGBA',(aw,ah),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,aw-1,ah-1),28,fill=(253,251,246),outline=INK,width=8)
vals=[4150,2151,1167,339]; labs=['MAR 24','MAR 25','MAR 26','SEP 26']; cols=[RED,M.ORG,M.GOLD,GRN]
for k,v in enumerate(vals):
    x=140+k*205; hg=int(v/4150*380); d.rounded_rectangle((x-70,500-hg,x+70,500),12,fill=cols[k],outline=INK,width=5)
    t=text_img(labs[k],'osw5',30,INK); art.alpha_composite(t,(x-t.size[0]//2,512))
t=text_img('BORROWINGS','type',30,M.GREY,2); art.alpha_composite(t,(aw-40-t.size[0],40))
st=stamp_c('14 BANKS REPAID',GRN,64,-6,3); art.alpha_composite(st,(aw-st.size[0]-30,100))
HK.art_glow(c,art,540,990,1.0,-1.5)
place(c,HK.tag("WHAT'S THE CATCH?",INK,YEL,104,-5,sub='PROFIT +58% · Q2 FY27'),540,1470)
place(c,HK.pill('MULTIBAGGER OR TRAP?',YEL,INK,64,maxw=900),540,1690)
HK.finish(c,'../out/pcj2_thumbnail.jpg')
