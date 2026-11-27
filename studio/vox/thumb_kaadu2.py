from PIL import Image
from lib import *
import hook as HK
import kaadu_cast as K
_th = 'red'; c = HK.rays_bg(_th, cy=900)
place(c, HK.fit_text("KAADU BANK · EP 2", 140, HK.title_ink(_th)), 540, 470)
place(c, HK.band("NEVER TRUST A FREE TIP", 80, txt=INK, bg=(255, 200, 61)), 540, 650)
HK.art_glow(c, K.kili('wow', True, True, 0.6), 470, 960, 0.85, 0)
place(c, K.aandhai('calm', True), 850, 1010, 0.5, 6)
place(c, HK.tag('~50,000 GOT THE SAME TIP', INK, CREAM, 58, -4, sub='ANIMAL FRIDAY'), 560, 1290)
place(c, HK.follow_sticker(size=50), 330, 1500)
HK.finish(c, '../out/kaadu2_thumbnail.jpg'); print(_th)
