"""Multi-voice cast TTS. usage: python3 vo_cast.py <dir>
<dir>/lines.json = [{"who":"kasi","text":"..."}...]; voices from CAST below (override in <dir>/voices.json)."""
import os,sys,json,soundfile as sf,numpy as np
from kokoro_onnx import Kokoro
D=os.path.dirname(os.path.abspath(__file__))+'/'
CAST={'narrator':('af_heart',1.08),'appa':('am_michael',1.08),'amma':('hf_alpha',1.05),'arjun':('am_puck',1.15),
      'paati':('hf_beta',0.98),'thatha':('am_santa',0.95),'kasi':('hm_omega',1.05)}
d=sys.argv[1];os.makedirs(d+'/vo',exist_ok=True)
if os.path.exists(d+'/voices.json'):CAST.update({k:tuple(v) for k,v in json.load(open(d+'/voices.json')).items()})
k=Kokoro(D+'kokoro-v1.0.onnx',D+'voices-v1.0.bin')
L=json.load(open(d+'/lines.json'));durs=[]
for i,l in enumerate(L):
    v,s=CAST[l['who']];a,sr=k.create(l['text'],voice=v,speed=s,lang='en-us')
    nz=np.where(np.abs(a)>0.01)[0];a=a[max(0,nz[0]-1200):nz[-1]+2400]
    sf.write(f'{d}/vo/{i}.wav',a,sr);durs.append(len(a)/sr)
json.dump(durs,open(d+'/vo/durs.json','w'));print([round(x,2) for x in durs],round(sum(durs),1))
