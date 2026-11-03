from PIL import Image, ImageDraw
from lib import *
import hook as HK
import listx as LX
c=HK.rays_bg('cream',cy=1050)
place(c,HK.fit_text("LOST 50%?",190,INK),540,280)
place(c,HK.band('+50% WON\'T SAVE YOU',104,txt=(255,255,255),bg=(229,72,77)),540,470)
art=Image.new('RGBA',(960,520),(0,0,0,0)); d=ImageDraw.Draw(art)
d.rounded_rectangle((0,0,959,519),34,fill=(255,255,255),outline=(36,50,77),width=10)
def tile(x,txt,sub,fg,bg):
    d.rounded_rectangle((x,110,x+260,370),28,fill=bg,outline=fg,width=6)
    t=text_img(txt,'pop',84,fg); art.alpha_composite(t,(x+130-t.size[0]//2,165))
    s=text_img(sub,'osw5',34,fg); art.alpha_composite(s,(x+130-s.size[0]//2,290))
tile(40,'−50%','FALL',(229,72,77),(253,236,236)); tile(350,'+50%','RISE',(22,163,74),(231,247,236)); tile(660,'−25%','STILL DOWN',(229,72,77),(253,236,236))
d.polygon([(312,220),(342,240),(312,260)],fill=(140,134,118))
d.rectangle((622,222,644,232),fill=(140,134,118)); d.rectangle((622,248,644,258),fill=(140,134,118))
t=text_img('₹100 FALLS TO ₹50, RISES TO ONLY ₹75','osw5',38,(36,50,77)); art.alpha_composite(t,(480-t.size[0]//2,410))
HK.art_glow(c,art,540,900,1.0,-1.2)
place(c,HK.tag('NEEDS +100%',(232,123,0),CREAM,96,-5,sub='TO GET BACK'),360,1420)
place(c,LX.pose_img(LX.POSE['shock'][2],470),840,1700)
HK.finish(c,'../out/lossmath_thumbnail.jpg')
