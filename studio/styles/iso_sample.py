import sys,math;sys.path.insert(0,'../vox')
from PIL import Image,ImageDraw,ImageFilter
from lib import font,text_img,place,INK
W,H=1080,1920;S=58;CX,CY=540,930
def P(x,y,z=0):return (CX+(x-y)*S*0.866,CY+(x+y)*S*0.5-z*S)
def shade(c,f):return tuple(max(0,min(255,int(v*f))) for v in c)
def box(d,x,y,w,dp,h,col,z=0,top=None):
    a,b,c_,e=P(x,y,z+h),P(x+w,y,z+h),P(x+w,y+dp,z+h),P(x,y+dp,z+h)
    fl=[P(x,y+dp,z),P(x+w,y+dp,z),P(x+w,y+dp,z+h),P(x,y+dp,z+h)]
    fr=[P(x+w,y,z),P(x+w,y+dp,z),P(x+w,y+dp,z+h),P(x+w,y,z+h)]
    d.polygon(fl,fill=shade(col,0.78),outline=INK);d.polygon(fr,fill=shade(col,0.62),outline=INK)
    d.polygon([a,b,c_,e],fill=top or shade(col,1.08),outline=INK)
def roof(d,x,y,w,dp,z,h,col):
    r1,r2=P(x+w/2,y,z+h),P(x+w/2,y+dp,z+h)
    d.polygon([P(x+w,y,z),P(x+w,y+dp,z),r2,r1],fill=shade(col,0.75),outline=INK)
    d.polygon([P(x,y+dp,z),P(x+w,y+dp,z),r2],fill=shade(col,0.95),outline=INK)
    d.polygon([P(x,y,z),P(x,y+dp,z),r2,r1],fill=col,outline=INK)
im=Image.new('RGB',(W,H));d=ImageDraw.Draw(im)
for y in range(H):
    t=y/H;d.line((0,y,W,y),fill=(int(214+30*t),int(240+10*t),int(250)))
d=ImageDraw.Draw(im,'RGBA')
# ground slab
box(d,-6,-6,12,12,0.5,(120,205,150),top=(150,222,170))
# roads
for k in range(-6,6):
    d.polygon([P(k,-0.6,0.5),P(k+1,-0.6,0.5),P(k+1,0.6,0.5),P(k,0.6,0.5)],fill=(90,96,110))
    d.polygon([P(-0.6,k,0.5),P(0.6,k,0.5),P(0.6,k+1,0.5),P(-0.6,k+1,0.5)],fill=(90,96,110))
for k in range(-6,6,2):d.line([P(k+0.3,0,0.51),P(k+0.9,0,0.51)],fill=(255,240,180),width=4);d.line([P(0,k+0.3,0.51),P(0,k+0.9,0.51)],fill=(255,240,180),width=4)
# your house (left)
box(d,-5,1.5,3,3,2,(255,210,120),0.5);roof(d,-5,1.5,3,3,2.5,1.4,(230,90,70))
# bank centre-back
box(d,1.5,-5.2,4,3.5,0.4,(235,235,240),0.5)
box(d,1.8,-4.9,3.4,2.9,2.8,(245,245,250),0.9)
for k in range(5):
    x=1.9+k*0.8;d.line([P(x,-2.0,0.9),P(x,-2.0,3.7)],fill=(180,184,196),width=10)
box(d,1.6,-5.1,3.8,3.3,0.35,(43,63,140),3.7);roof(d,1.6,-5.1,3.8,3.3,4.05,1.0,(43,63,140))
# home buyer (right)
box(d,2,2,3,3,2.4,(140,190,250),0.5);roof(d,2,2,3,3,2.9,1.3,(60,120,210))
# trees
for (tx,ty) in [(-4.5,-4.5),(-2.5,-3.8),(4.8,-0.7),(-4.6,5),(1.2,5.2)]:
    box(d,tx,ty,0.3,0.3,0.6,(120,80,40),0.5);x0,y0=P(tx+0.15,ty+0.15,1.5);d.ellipse((x0-34,y0-34,x0+34,y0+34),fill=(50,160,90),outline=INK,width=3)
# coins on road
def coin(x,y,z,lab=None,c=(255,197,49)):
    sx,sy=P(x,y,z);d.ellipse((sx-26,sy-15,sx+26,sy+15),fill=shade(c,0.8),outline=INK,width=3);d.ellipse((sx-26,sy-22,sx+26,sy+8),fill=c,outline=INK,width=3)
    d.text((sx,sy-7),'₹',font=font('pop',24),fill=INK,anchor='mm')
for k,(x,y) in enumerate([(-1.8,0),(-0.6,-0.9),(0,-1.9)]):coin(x,y,0.7)
for k,(x,y) in enumerate([(0,1.2),(0,2.3),(0,3.4)]):coin(x,y,0.7,c=(255,140,60))
def tag(s,sub,colr,x,y,z):
    sx,sy=P(x,y,z);t=text_img(s,'anton',54,(255,255,255));u=text_img(sub,'pop',30,INK)
    w=max(t.size[0],u.size[0])+50;h=t.size[1]+u.size[1]+34
    card=Image.new('RGBA',(w+10,h+10));cd=ImageDraw.Draw(card)
    cd.rounded_rectangle((10,10,w+9,h+9),22,fill=INK);cd.rounded_rectangle((0,0,w-1,h-1),22,fill='white',outline=INK,width=5)
    cd.rounded_rectangle((8,8,w-9,t.size[1]+20),16,fill=colr);card.alpha_composite(t,(int(w/2-t.size[0]/2),10));card.alpha_composite(u,(int(w/2-u.size[0]/2),t.size[1]+22))
    c=im.convert('RGBA');place(c,card,sx,sy-90);return c
im=tag('YOU','deposit ₹1 lakh',(230,90,70),-4.2,3.2,4.4)
d=ImageDraw.Draw(im,'RGBA')
im=tag('BANK','pays you 2.5%',(43,63,140),3.6,-3.6,5.0)
im=tag('HOME BUYER','pays bank 7.5%+',(60,120,210),4.6,4.6,-1.2)
place(im,text_img('HOW A BANK','anton',120,INK),540,170);place(im,text_img('MAKES MONEY','anton',140,(30,130,70)),540,300)
card=Image.new('RGBA',(900,200));cd=ImageDraw.Draw(card);cd.rounded_rectangle((10,10,899,199),30,fill=INK);cd.rounded_rectangle((0,0,889,189),30,fill='white',outline=INK,width=6)
cd.text((445,60),'₹2,500 to you  vs  ₹7,500 from loan',font=font('pop',40),fill=INK,anchor='mm');t2=text_img('ABOUT ₹5,000 KEPT A YEAR*','anton',58,(30,130,70));card.alpha_composite(t2,(445-t2.size[0]//2,95))
place(im,card,540,1640)
place(im,text_img('*simplified: SBI savings 2.5%, home loan from 7.50% (Oct 2026)','osw5',26,(90,92,104)),540,1780)
im.convert('RGB').save('isometric_sample.png')
