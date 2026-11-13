from PIL import Image, ImageDraw
from lib import *
import hook as HK
import divi6 as M
th='green'
c=HK.rays_bg(th, cy=1000)
place(c,HK.fit_text('₹1 LAKH = ₹6,600',140,HK.title_ink(th)),540,220)
place(c,HK.fit_text('EVERY YEAR?',140,YEL),540,380)
place(c,M.card_pro('6 DIVIDEND STOCKS','Coal India · Wipro · ONGC · IOC · BPCL · ITC',M.GN,860,170),540,580,1,-2)
place(c,M.pose(50,460),540,1120,1,-2)
place(c,HK.tag('SAVE THIS CHEAT SHEET',INK,YEL,84,-4,sub='+ THE TAX CATCH'),540,1470)
place(c,HK.follow_sticker(size=48),540,1740)
HK.finish(c,'../out/divi6_thumbnail.jpg')
