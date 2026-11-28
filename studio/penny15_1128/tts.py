import sys,json,numpy as np,soundfile as sf
sys.path.insert(0,'/home/claude/reels/studio/kokoro')
from kokoro_onnx import Kokoro
K='/home/claude/reels/studio/kokoro/'
k=Kokoro(K+'kokoro-v1.0.onnx',K+'voices-v1.0.bin')
S=json.load(open('segs.json')); voice,speed=sys.argv[1],float(sys.argv[2])
out=[];t=0.15;T={};sr=24000
out.append(np.zeros(int(0.15*sr),'float32'))
for sid,txt,gap in S:
    a,sr=k.create(txt,voice=voice,speed=speed,lang='en-us')
    nz=np.where(np.abs(a)>0.01)[0]; a=a[max(0,nz[0]-600):nz[-1]+1800]
    sf.write(f'vo/{sid}.wav',a,sr)
    T[sid]=[round(t,3),round(len(a)/sr,3)]; out.append(a); t+=len(a)/sr
    out.append(np.zeros(int(gap*sr),'float32')); t+=gap
v=np.concatenate(out); sf.write('vo.wav',v,sr)
T['DUR']=round(t+0.9,2); json.dump(T,open('times.json','w'),indent=0); print(T['DUR'])
