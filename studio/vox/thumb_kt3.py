from PIL import Image
from lib import *
import hook as HK
_th='navy'; c=HK.rays_bg(_th, cy=950)
place(c,HK.fit_text('ALL THE GOLD',150,HK.title_ink(_th)),540,420)
place(c,HK.fit_text('ON ONE SHIP?',120,HK.title_ink(_th)),540,560)
place(c,HK.band("KING'S TREASURY · EP 3",80),540,690)
art=Image.open('../kt3/art.png').convert('RGBA')
HK.art_glow(c,art,540,1000,0.5,-1)
place(c,HK.tag('ONE STORM: −99%',(232,96,76),CREAM,76,-4,sub='A REAL STOCK DID THIS'),540,1420)
place(c,HK.follow_sticker(size=34),540,1740)
HK.finish(c,'../out/kt3_thumbnail.jpg')
