import cv2,sys,time
sr=cv2.dnn_superres.DnnSuperResImpl_create();sr.readModel('/home/claude/models/sr/EDSR_x4.pb');sr.setModel('edsr',4)
for n in sys.argv[1:]:
    t=time.time();img=cv2.imread(f'panels/p{n}.png');out=sr.upsample(img);cv2.imwrite(f'up/p{n}.png',out);print(n,out.shape,round(time.time()-t,1),flush=True)
