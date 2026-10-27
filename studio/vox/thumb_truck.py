from PIL import Image, ImageDraw
from lib import *
import hook as HK
import paperchars as P
c=HK.rays_bg('navy')
place(c,HK.fit_text('15 YEARS AWAY FROM HOME',140,CREAM),540,500)
place(c,HK.band('BECAUSE OF ONE "DOUBLE IT" SCHEME',80),540,660)
art=Image.new('RGBA',(980,760),(0,0,0,0))
lr=P.lorry().resize((660,312)); art.alpha_composite(lr,(300,420))
dr=P.person(skin='c',mustache=True,shirt=(250,250,245),pants=(80,70,60),mood='sad').resize((300,600)); art.alpha_composite(dr,(20,140))
HK.art_glow(c,art,540,960,1.0,0)
place(c,HK.tag('A STORY FOR EVERY FAMILY',RED,CREAM,90,-5,sub='WATCH TILL THE END'),540,1420)
place(c,HK.pill('SEND THIS TO YOUR PARENTS',YEL,INK,52,maxw=940),540,1620)
HK.finish(c,'../out/truck_story_thumbnail.jpg')
