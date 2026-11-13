from PIL import Image
from lib import *
import hook as HK
import animals as A
_th = HK.theme_for('F&O options trading losses'); c = HK.rays_bg(_th, cy=900)
place(c, HK.fit_text("88% LOST MONEY", 150, HK.title_ink(_th)), 540, 470)
place(c, HK.band("DON'T TRADE LIKE THE MONKEY", 84, txt=INK, bg=(255, 200, 61)), 540, 650)
art = A.monkey('cry', 'head', 0, 1.0, False)
HK.art_glow(c, art, 540, 940, 0.95, 0)
place(c, A.fee_coin('₹'), 300, 900, 0.8, -15); place(c, A.fee_coin('FEE'), 790, 1050, 0.7, 12)
place(c, HK.tag('SEBI F&O STUDY · FY26', INK, CREAM, 64, -5, sub='ANIMAL FRIDAY'), 560, 1290)
place(c, HK.follow_sticker(size=50), 330, 1500)
HK.finish(c, '../out/monkey_thumbnail.jpg'); print(_th)
