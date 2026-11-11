from PIL import Image, ImageDraw
from lib import *
import hook as HK
import eqmf as M
c=HK.rays_bg('teal', cy=1000)
place(c,M.note((('STOCKS','anton',120,M.CORAL),('you pick 1 company','type',44,INK)),(255,250,238),470,5),290,420,1,-5)
place(c,M.note((('MUTUAL FUND','anton',96,M.TEALP),('a manager picks 50','type',44,INK)),(236,248,244),470,9),790,440,1,5)
place(c,text_img('vs','mark',130,YEL),540,640)
place(c,M.pose(14,640),540,960,1,-2)
place(c,HK.tag('SAME ₹10,000, 2 RIDES',INK,YEL,90,-4,sub='RISK · COSTS · TAX · WHO SHOULD PICK WHAT'),540,1400)
place(c,HK.follow_sticker(size=52),540,1700)
HK.finish(c,'../out/eqmf_thumbnail.jpg')
