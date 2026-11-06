import sys,os
from rembg import remove,new_session
from PIL import Image,ImageFilter
import numpy as np,cv2
s=new_session('isnet-general-use');os.makedirs('layers',exist_ok=True)
for n in sys.argv[1:]:
    if os.path.exists(f'layers/fg{n}.png'): continue
    im=Image.open(f'up/p{n}.png').convert('RGB')
    w,h=im.size;bx=int(w*0.075);by=int(h*0.045)
    im=im.crop((bx,by,w-bx,h-by)).resize((1080,int((h-2*by)*1080/(w-2*bx))),Image.LANCZOS)
    im.save(f'layers/bg{n}_full.png')
    cut=remove(im,session=s);a=np.asarray(cut)[...,3]
    m=(a>40).astype(np.uint8)*255;m=cv2.dilate(m,np.ones((25,25),np.uint8))
    bg=cv2.inpaint(np.asarray(im)[...,::-1].copy(),m,9,cv2.INPAINT_TELEA)[...,::-1]
    Image.fromarray(bg).filter(ImageFilter.GaussianBlur(3)).save(f'layers/bg{n}.png');cut.save(f'layers/fg{n}.png');print(n,flush=True)
