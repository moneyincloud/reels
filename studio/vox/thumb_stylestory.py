from PIL import Image, ImageDraw
from lib import *
import hook as HK
import stylestory as M
c=HK.rays_bg('orange', cy=1000)
place(c,HK.fit_text('SAME ₹1 LAKH BONUS',130,HK.title_ink('orange')),540,230)
place(c,HK.fit_text('10 YEARS LATER',150,YEL),540,390)
place(c,M.kid('A','sad',330),290,820,1,-4); place(c,M.kid('B','happy',330),790,820,1,4)
place(c,HK.tag('LOST IT vs ₹3.1 LAKH',INK,YEL,88,-4,sub='ONE STORY · 9 ANIMATION STYLES'),540,1300)
place(c,HK.follow_sticker(size=52),540,1680)
HK.finish(c,'../out/stylestory_thumbnail.jpg')
