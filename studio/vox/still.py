import sys, time
from PIL import Image
import importlib,os; render=importlib.import_module(os.environ.get("MOD","scenes")).render
ts=[float(x) for x in sys.argv[1:]]
ims=[]
for t in ts:
    a=time.time(); ims.append(Image.fromarray(render(t))); print(t, round(time.time()-a,2))
w=360;h=640
sheet=Image.new('RGB',(w*len(ims),h))
for i,im in enumerate(ims): sheet.paste(im.resize((w,h)),(i*w,0))
sheet.save('../frames/still.jpg',quality=88)
