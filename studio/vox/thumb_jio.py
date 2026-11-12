from PIL import Image, ImageDraw
from lib import *
import hook as HK
import jio as M
c=HK.rays_bg('blue', cy=1000)
place(c,HK.fit_text('JIO: BUY NOW',140,HK.title_ink('blue')),540,220)
place(c,HK.fit_text('OR WAIT?',150,YEL),540,390)
place(c,M.card_pro('IPO  ₹1,119','issue price · Oct 2026',M.JB,820,170),540,580,1,-2)
place(c,M.card_pro('NOW  ₹1,414','+26% · 2 weeks later',(40,170,100),820,170),540,770,1,1.5)
place(c,M.pose(14,440),540,1210,1,-2)
place(c,HK.tag('P/E 41. TOO HOT?',INK,YEL,90,-4,sub='THE MATH AFTER LISTING'),540,1480)
place(c,HK.follow_sticker(size=48),540,1740)
HK.finish(c,'../out/jio_thumbnail.jpg')
