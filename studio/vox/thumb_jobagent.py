from PIL import Image, ImageDraw
from lib import *
import hook as HK
import jobagent as M
c=HK.rays_bg('teal', cy=1000)
place(c,HK.fit_text('200 APPLICATIONS',140,HK.title_ink('teal')),540,240)
place(c,HK.fit_text('0 CALLS?',170,YEL),540,410)
a=M.person('arjun_worried',660); comp(c,a,-60,1560-a.size[1]+40)
ph=M.app_frame('AI JOB AGENT').copy(); d=ImageDraw.Draw(ph)
for j,(x,y,s,col) in enumerate([('DevOps Engineer','match',' 92% ',M.GREEN),('Cloud Engineer','match',' 85% ',M.GREEN),('Data Analyst','skipped',' 31% ',M.RED)]):
    M.row(d,ph,190+j*165,x,y,s,col)
place(c,ph,770,860,0.62,6)
place(c,HK.tag('5 STEPS',INK,YEL,110,-4,sub='HOW AN AI JOB AGENT WORKS'),540,1430)
place(c,HK.follow_sticker(size=52),540,1720)
HK.finish(c,'../out/jobagent_thumbnail.jpg')
