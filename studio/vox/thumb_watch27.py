from PIL import Image, ImageDraw
from lib import *
import hook as HK
import watch27 as M
c=HK.rays_bg('oil', cy=1000)
place(c,HK.fit_text('2027 WATCHLIST',170,HK.title_ink('oil')),540,240)
place(c,HK.fit_text('5 SECTORS HSBC NAMED',110,HK.title_ink('oil')),540,410)
atom=M._render(M.lit_t(4)+1.0).crop((0,520,1080,1420)).resize((980,817))
mask=Image.new('L',atom.size,0);ImageDraw.Draw(mask).ellipse((40,0,940,817),fill=255)
from PIL import ImageFilter
atom.putalpha(mask.filter(ImageFilter.GaussianBlur(30)));c.alpha_composite(atom,(50,520))
place(c,HK.tag('BANKS · INDUSTRIALS · REAL ESTATE…',INK,YEL,64,-3,sub='WATCHLIST, NOT A BUY LIST'),540,1440)
place(c,HK.follow_sticker(size=52),540,1720)
HK.finish(c,'../out/watch27_thumbnail.jpg')
