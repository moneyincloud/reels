import json,numpy as np,soundfile as sf
T=json.load(open('times.json')); C=json.load(open('../../motion/penny15/build/t.json'))
v,sr=sf.read('vo.wav'); DUR=T['DUR']; N=int(DUR*sr); out=np.zeros(N); out[:len(v)]+=v[:N]
t=np.arange(N)/sr; rng=np.random.default_rng(7)
# soft pad: Am-F-C-G, 2 s per chord
ch=[[220,261.6,329.6],[174.6,220,261.6],[261.6,329.6,392],[196,246.9,293.7]]
pad=np.zeros(N)
for i in range(int(DUR/2)+1):
    a=int(i*2*sr); b=min(N,int((i*2+2.2)*sr)); tt=np.arange(b-a)/sr
    env=np.minimum(1,tt/0.3)*np.minimum(1,(2.2-tt)/0.4).clip(0)
    for f in ch[(i//2)%4]: pad[a:b]+=np.sin(2*np.pi*f*tt)*env*0.5
pad+=0.3*np.sin(2*np.pi*55*t)*(0.5+0.5*np.sin(2*np.pi*t/2))
vo_env=np.convolve(np.abs(out),np.ones(4800)/4800,'same'); duck=1-0.55*np.clip(vo_env/0.05,0,1)
out+=pad/np.abs(pad).max()*0.06*duck
def put(x,at,g):
    a=int(at*sr); b=min(N,a+len(x)); out[a:b]+=x[:b-a]*g
def pop(): tt=np.arange(int(.08*sr))/sr; return np.sin(2*np.pi*(900-4000*tt)*tt)*np.exp(-tt*45)
def whoosh(d=.4): n=int(d*sr); w=rng.normal(0,1,n); w=np.convolve(w,np.ones(30)/30,'same'); return w*np.hanning(n)
def hit(): tt=np.arange(int(.5*sr))/sr; return np.sin(2*np.pi*60*tt)*np.exp(-tt*8)+0.3*rng.normal(0,1,len(tt))*np.exp(-tt*30)
def ding(): tt=np.arange(int(.6*sr))/sr; return (np.sin(2*np.pi*1320*tt)+.5*np.sin(2*np.pi*1980*tt))*np.exp(-tt*7)
for ts in C['CARD_T']: put(pop(),ts-0.1,0.25)
for a,b in C['SC'][1:]: put(whoosh(),a-0.2,0.12)
put(hit(),0.0,0.35); put(hit(),T['banks'][0]+0.1,0.3); put(hit(),T['twist'][0],0.35); put(hit(),T['f14'][0]+1.2,0.35)
for k in ['r1','r2','r3']: put(ding(),T[k][0]+0.2,0.15)
out[-int(.5*sr):]*=np.linspace(1,0,int(.5*sr))
out=out/max(1,np.abs(out).max()/0.95)
sf.write('mix.wav',out.astype('float32'),sr); print('mix ok',round(len(out)/sr,2))
