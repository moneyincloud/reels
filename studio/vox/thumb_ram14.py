from PIL import Image, ImageDraw
from lib import *
import hook as HK
import ram14 as M
th='gold' if 'gold' in HK.THEMES else 'orange'
c=HK.rays_bg(th, cy=1000)
place(c,HK.fit_text("RAMA'S 14 YEARS",140,HK.title_ink(th)),540,220)
place(c,HK.fit_text('₹1 LAKH → ₹26.7 LAKH'.replace('→','TO'),120,YEL),540,380)
place(c,M.card_pro('THANGAMAYIL  26x','Nov 2012 to Nov 2026',M.GD,820,170),540,580,1,-2)
place(c,M.pose(50,460),540,1150,1,-2)
place(c,HK.tag('COULD YOU HOLD 14 YEARS?',INK,YEL,84,-4,sub='EVEN THROUGH A −42% FALL'),540,1470)
place(c,HK.follow_sticker(size=48),540,1740)
HK.finish(c,'../out/ram14_thumbnail.jpg')
