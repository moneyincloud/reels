from PIL import Image, ImageDraw
from lib import *
import hook as HK
bg = Image.open('/home/claude/reels/motion/penny15/snaps/frame-03-at-31.5s.png').convert('RGBA')
c = bg.copy(); d = ImageDraw.Draw(c)
d.rectangle((0, 1192, 1080, 1340), fill=(251, 248, 240, 255))  # hide caption / disclaimer strip
d.rectangle((0, 180, 1080, 395), fill=(251, 248, 240, 255))    # replace header
place(c, text_img('15 PENNY STOCKS UNDER ₹40', 'anton', 96, INK), 540, 290)
place(c, HK.tag('ALL 15 ARE DOWN 20–57%'.replace('–', ' TO '), (255, 255, 255), (217, 58, 43), 74, -3, sub='LOW PRICE IS NOT CHEAP'), 540, 1340)
place(c, HK.follow_sticker(size=46), 540, 1580)
c.convert('RGB').save('../out/penny-stocks-under-40-india-2026-cover.jpg', quality=92)
print('ok')
