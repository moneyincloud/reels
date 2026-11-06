import numpy as np,sys
from PIL import Image,ImageFilter
from scipy import ndimage as nd
def fix(n,thr=16):
    im=np.asarray(Image.open(f'expr/{n}.png').convert('RGB')).astype(float)
    h,w,_=im.shape
    bgc=np.median(np.concatenate([im[:15].reshape(-1,3),im[:,:10].reshape(-1,3),im[:,-10:].reshape(-1,3)]),axis=0)
    dist=np.sqrt(((im-bgc)**2).sum(-1))
    near=dist<thr
    lab,_=nd.label(near)
    border=set(np.unique(np.concatenate([lab[0],lab[:,0],lab[:,-1]])))-{0}
    bg=np.isin(lab,list(border))
    bg=nd.binary_opening(bg,iterations=2)
    fg=~bg; fg=nd.binary_fill_holes(np.pad(fg,((0,2),(0,0)),constant_values=True))[:-2]
    al=Image.fromarray((fg*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    out=Image.open(f'expr/{n}.png').convert('RGBA');out.putalpha(al);out=out.crop(out.getbbox());out.save(f'cut/{n}.png')
for n in sys.argv[1:]: fix(n)
