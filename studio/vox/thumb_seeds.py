from PIL import Image
from lib import *
import hook as HK
_th='green'; c=HK.rays_bg(_th, cy=950)
place(c,HK.fit_text('STOP EATING',150,HK.title_ink(_th)),540,250)
place(c,HK.fit_text('YOUR GOLDEN FRUIT',110,HK.title_ink(_th)),540,400)
place(c,HK.band("KING'S TREASURY · EP 2",88),540,540)
art=Image.open('/tmp/claude-0/-home-claude/32ef0837-6367-50a7-8b18-d49a84afef86/scratchpad/sart.png').convert('RGBA')
HK.art_glow(c,art,540,960,1.0,-1)
place(c,HK.tag('1 TREE vs A FOREST',(232,96,76),CREAM,90,-4,sub='20 YEARS · SAME START'),540,1390)
place(c,HK.follow_sticker(size=52),540,1690)
HK.finish(c,'../out/seeds_thumbnail.jpg')
