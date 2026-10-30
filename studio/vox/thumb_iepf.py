from PIL import Image, ImageDraw
from lib import *
import hook as HK
import iepf as M
c=HK.rays_bg('green')
place(c,HK.fit_text("PARENTS' LOST SHARES?",140,CREAM),540,380)
place(c,HK.band('₹89,000 CR UNCLAIMED',104),540,560)
cert=M.certificate(1.0)
HK.art_glow(c,cert,540,960,1.0,-4)
place(c,HK.tag('CHECK YOUR FAMILY NAME',RED,CREAM,84,-5,sub='3 STEPS · IEPF · FREE TO SEARCH'),540,1420)
place(c,HK.pill('SEND THIS TO YOUR PARENTS',YEL,INK,60,maxw=960),540,1660)
HK.finish(c,'../out/iepf_thumbnail.jpg')
Image.open('../out/iepf_thumbnail.jpg').resize((540,960)).save('/tmp/claude-0/-home-claude/32ef0837-6367-50a7-8b18-d49a84afef86/scratchpad/th_iepf.jpg')
