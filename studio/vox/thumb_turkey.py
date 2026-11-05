from PIL import Image
from lib import *
import hook as HK
import listx as LX
_th=HK.theme_for('yes bank'); c=HK.rays_bg(_th,cy=900)
place(c,HK.fit_text("DON'T BE THE TURKEY",150,HK.title_ink(_th)),540,240)
place(c,HK.band('YES BANK: ₹404 TO ₹16',104,txt=INK,bg=(255,200,61)),540,430)
tk=Image.open('/tmp/claude-0/-home-claude/32ef0837-6367-50a7-8b18-d49a84afef86/scratchpad/turkey.png').convert('RGBA')
HK.art_glow(c,tk,540,860,1.05,0)
place(c,HK.tag('-96% FROM PEAK',(229,72,77),CREAM,76,-5,sub='ANIMAL FRIDAY'),560,1390)
place(c,HK.follow_sticker(size=54),300,1700)
place(c,LX.pose_img(LX.POSE['shock'][1],470),840,1700)
HK.finish(c,'../out/turkey_thumbnail.jpg'); print(_th)
