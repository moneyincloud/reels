import numpy as np,sys
from PIL import Image
EX=['happy','shock','worried','think','laugh','smug']
def runs(mask):
    out=[];s=None
    for i,v in enumerate(mask):
        if v and s is None:s=i
        if not v and s is not None:
            if i-s>40: out.append((s,i))
            s=None
    if s is not None and len(mask)-s>40: out.append((s,len(mask)))
    return out
for who in ['appa','amma','arjun','paati','thatha','kasi']:
    im=Image.open(f'raw/{who}_expr.png').convert('RGB');a=np.asarray(im).astype(int)
    white=(a.min(axis=2)>245)
    cols=runs(white.mean(axis=0)<0.9); rows=runs(white.mean(axis=1)<0.9)
    print(who,cols,rows)
    k=0
    for (y0,y1) in rows[:2]:
        for (x0,x1) in cols[:3]:
            im.crop((x0+3,y0+3,x1-3,y1-3)).save(f'expr/{who}_{EX[k]}.png');k+=1
