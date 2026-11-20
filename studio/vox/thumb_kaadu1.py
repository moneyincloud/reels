from PIL import Image
from lib import *
import hook as HK
import kaadu_cast as K
_th = 'green'; c = HK.rays_bg(_th, cy=900)
place(c, HK.fit_text("KAADU BANK · EP 1", 140, HK.title_ink(_th)), 540, 470)
place(c, HK.band("NEVER LAUGH AT A SMALL SIP", 80, txt=INK, bg=(255, 200, 61)), 540, 650)
HK.art_glow(c, K.ammu('happy', 'carry'), 470, 960, 0.85, 0)
place(c, K.mani('wow', 'head', 0, 1.0, False), 800, 1010, 0.42, 6)
place(c, K.grain(40), 250, 1080, 0.9, -20)
place(c, HK.tag('~10 CRORE SIPs PAID · OCT 2026', INK, CREAM, 58, -4, sub='ANIMAL FRIDAY'), 560, 1290)
place(c, HK.follow_sticker(size=50), 330, 1500)
HK.finish(c, '../out/kaadu1_thumbnail.jpg'); print(_th)
