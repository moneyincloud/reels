from rembg import remove,new_session
from PIL import Image
import glob,os
s=new_session('isnet-general-use')
files=sorted(glob.glob('raw/*_full.png'))+sorted(glob.glob('expr/*.png'))
for f in files:
    o='cut/'+os.path.basename(f)
    if os.path.exists(o): continue
    im=Image.open(f).convert('RGB');r=remove(im,session=s)
    r=r.crop(r.getbbox());r.save(o);print(o,flush=True)
