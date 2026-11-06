import sys,math;sys.path.insert(0,'../vox')
from PIL import Image,ImageDraw
from lib import font,text_img,place,INK
W,H=1080,1920;OR=(255,138,61);OR2=(214,96,24)
im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
for y in range(H):
    t=y/H;d.line((0,y,W,y),fill=(int(255-8*t),int(244-20*t),int(230-30*t)))
# floor line
d.polygon([(0,1500),(W,1240),(W,1330),(0,1590)],fill=(240,214,186))
def domino(n,lines,col,hi=False):
    w,h,dep=168,380,22
    dm=Image.new('RGBA',(w+dep+14,h+dep+14));dd=ImageDraw.Draw(dm)
    dd.rounded_rectangle((dep+10,10,w+dep+9,h+9),28,fill=INK)
    dd.rounded_rectangle((dep,dep*0+0,w+dep-1,h-1),28,fill=OR2,outline=INK,width=6)
    dd.rounded_rectangle((0,dep,w-1,h+dep-1),28,fill=(255,250,242) if not hi else OR,outline=INK,width=6)
    dd.line((24,dep+h/2,w-24,dep+h/2),fill=INK,width=5)
    nt=text_img(str(n),'anton',110,OR if not hi else (255,255,255));dm.alpha_composite(nt,(w//2-nt.size[0]//2,dep+40))
    y=dep+h/2+20
    for ln in lines:
        t=text_img(ln,'anton',38,INK if not hi else (255,255,255));s=min(1,(w-30)/t.size[0])
        if s<1:t=t.resize((int(t.size[0]*s),int(t.size[1]*s)))
        dm.alpha_composite(t,(w//2-t.size[0]//2,int(y)));y+=t.size[1]+6
    return dm
items=[(['RBI HIKES','REPO'],-14),(['BANK LOAN','RATES UP'],0),(['YOUR EMI','GOES UP'],0),(['LESS','SPENDING'],0),(['SALES','SLOW'],0)]
for k,(lb,rot) in reversed(list(enumerate(items))):
    x=150+k*195;y=1150-k*60
    if rot:x-=10;y+=6
    place(im,domino(k+1,lb,OR,hi=(k==2)),x,y,1.0,rot)
# motion lines
for k in range(3):
    d=ImageDraw.Draw(im);x0=120+k*30;d.arc((x0-90,880+k*20,x0+90,1060+k*20),200,300,fill=INK,width=5)
place(im,text_img('ONE RBI DECISION','anton',120,INK),540,200)
place(im,text_img('HITS YOUR WALLET','anton',120,OR2),540,340)
place(im,text_img('Repo 5.25% to 5.50% · 7 Oct 2026','pop',38,INK),540,460)
card=Image.new('RGBA',(940,250));cd=ImageDraw.Draw(card)
cd.rounded_rectangle((10,10,939,249),30,fill=INK);cd.rounded_rectangle((0,0,929,239),30,fill='white',outline=INK,width=6)
t1=text_img('₹50 LAKH HOME LOAN, 20 YEARS','anton',50,INK);card.alpha_composite(t1,(465-t1.size[0]//2,26))
t2=text_img('EMI +₹768 A MONTH','anton',74,OR2);card.alpha_composite(t2,(465-t2.size[0]//2,88))
t3=text_img('= about ₹1.84 lakh more over the loan*','pop',32,INK);card.alpha_composite(t3,(465-t3.size[0]//2,184))
place(im,card,540,1640)
place(im,text_img('*if your rate rises 7.50% to 7.75% (a 0.25% hike passed on)','osw5',26,(90,92,104)),540,1800)
im.convert('RGB').save('domino_sample.png')
