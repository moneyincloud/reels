from PIL import Image, ImageDraw
from lib import *
import hook as HK
import isobank as M
c=HK.rays_bg('emerald', cy=1000)
place(c,HK.fit_text('YOUR BANK EARNS',140,HK.title_ink('emerald')),540,230)
place(c,HK.fit_text('3X ON YOUR MONEY',150,HK.title_ink('emerald')),540,400)
M.Cam.S,M.Cam.CX,M.Cam.CY=52,540,1000
t=30.0
town=Image.new('RGBA',(1080,1920),(0,0,0,0));M.draw_town(town,t);c.alpha_composite(town)
place(c,M.tag_img('YOU GET','2.5% on savings',(230,90,70)),230,640,1.25,-4)
place(c,M.tag_img('BANK GETS','7.5%+ on loans',(43,63,140)),850,640,1.25,4)
place(c,HK.tag('STOP KEEPING BIG MONEY IN SAVINGS?',INK,YEL,70,-3,sub='SBI SAVINGS 2.5% vs HOME LOANS 7.50%+'),540,1440)
place(c,HK.follow_sticker(size=52),540,1720)
HK.finish(c,'../out/isobank_thumbnail.jpg')
