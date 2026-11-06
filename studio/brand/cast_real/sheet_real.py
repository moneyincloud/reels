from PIL import Image,ImageDraw,ImageFont,ImageFilter
F='../Poppins-Bold.ttf';M='../DejaVuSansMono-Bold.ttf'
def bg():
    im=Image.new('RGB',(1080,1920));d=ImageDraw.Draw(im)
    for y in range(1920):
        t=y/1919;d.line([(0,y),(1080,y)],fill=(int(142+(216-142)*t),int(210+(240-210)*t),int(246+(252-246)*t)))
    return im
def fit(img,w,h):
    s=min(w/img.width,h/img.height);return img.resize((int(img.width*s),int(img.height*s)),Image.LANCZOS)
def shadow(im,x,y,w):
    sh=Image.new('L',im.size,0);ImageDraw.Draw(sh).ellipse([x-w//2,y-14,x+w//2,y+14],fill=90)
    im.paste((40,60,90),(0,0),sh.filter(ImageFilter.GaussianBlur(10)))
CAST=[('appa','APPA · RAVI','40 · IT job'),('amma','AMMA · MEENA','38 · budget boss'),('arjun','ARJUN','19 · F&O dreams'),
      ('paati','PAATI','68 · gold & FD'),('thatha','THATHA','72 · retired clerk'),('kasi','KASI MAMA','"sure-shot tip"')]
# lineup
im=bg();d=ImageDraw.Draw(im)
d.rounded_rectangle([60,50,1020,210],40,fill='white',outline='#1B2440',width=6)
d.text((540,115),'THE CLOUD FAMILY',font=ImageFont.truetype(F,64),fill='#2B3F8C',anchor='mm')
d.text((540,172),'moneyincloud · realistic cast',font=ImageFont.truetype(M,26),fill='#5B6785',anchor='mm')
for i,(k,n,r) in enumerate(CAST):
    col,row=i%3,i//3;cx=190+col*350;fy=1000 if row==0 else 1760
    H={'appa':700,'amma':660,'arjun':690,'paati':600,'thatha':615,'kasi':630}[k];q=Image.open(f'cut/{k}_full.png');p=q.resize((int(q.width*H/q.height),H),Image.LANCZOS)
    shadow(im,cx,fy,220);im.paste(p,(cx-p.width//2,fy-p.height),p)
    d=ImageDraw.Draw(im)
    d.rounded_rectangle([cx-155,fy+12,cx+155,fy+110],26,fill='white',outline='#1B2440',width=4)
    d.text((cx,fy+45),n,font=ImageFont.truetype(F,30),fill='#2B3F8C',anchor='mm')
    d.text((cx,fy+85),r,font=ImageFont.truetype(M,21),fill='#3E4A66',anchor='mm')
im.save('realistic_cast_lineup.png')
# expressions board
EX=['happy','shock','worried','think','laugh','smug']
im=bg();d=ImageDraw.Draw(im)
d.rounded_rectangle([60,40,1020,170],40,fill='white',outline='#1B2440',width=6)
d.text((540,105),'EXPRESSIONS',font=ImageFont.truetype(F,60),fill='#2B3F8C',anchor='mm')
for j,e in enumerate(EX):d.text((175+j*150,225),e.upper(),font=ImageFont.truetype(M,22),fill='#2B3F8C',anchor='mm')
for i,(k,n,r) in enumerate(CAST):
    y=255+i*275
    d.text((40,y+130),n.split(' ·')[0],font=ImageFont.truetype(F,22),fill='#2B3F8C',anchor='lm') if False else None
    for j,e in enumerate(EX):
        x=105+j*150;t=Image.open(f'expr/{k}_{e}.png').convert('RGB')
        t=t.crop((0,0,t.width,int(t.width*1.3)));t=t.resize((140,182),Image.LANCZOS)
        im.paste(t,(x,y));ImageDraw.Draw(im).rectangle([x,y,x+139,y+181],outline='#1B2440',width=3)
    d=ImageDraw.Draw(im);d.text((540,y+205),n,font=ImageFont.truetype(F,24),fill='#2B3F8C',anchor='mm')
im.save('realistic_cast_expressions.png')
