import numpy as np, wave, subprocess, sys, json
sys.path.insert(0,'.')
import importlib
import types
_d=json.load(open("../muhurat/web/data.json"))
F=types.SimpleNamespace(DUR=_d["dur"],VO=_d["vo"],SH="../muhurat/",STARTS=_d["starts"],WORDS=_d["words"])
_m=_d["marks"]
from sfx_lib import whoosh, pop, tick, hit
SR=48000; N=int(F.DUR*SR)
def load(p):
    raw=subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar',str(SR),'-f','s16le','-'],capture_output=True).stdout
    return np.frombuffer(raw,np.int16).astype(float)/32768
vo=np.zeros(N)
for i,t in enumerate(F.VO):
    x=load(f'{F.SH}vo/{i}.wav'); a=int(t*SR); vo[a:a+len(x)]+=x[:N-a]
vo=vo/np.abs(vo).max()*0.85
# --- festive music bed: tanpura drone + sitar-like plucks (raga Yaman flavour) + tabla-like groove, 100 BPM ---
bpm=100; beat=60/bpm; t=np.arange(N)/SR
f=lambda m:440*2**((m-69)/12)
mus=np.zeros(N); rng=np.random.default_rng(3)
SA=50  # D3 as Sa
# tanpura: Pa-Sa-Sa-Sa(low) cycle, rich harmonics, long decay
cyc=[SA+7+12,SA+12,SA+12,SA]
step=beat*1.0; k=0
while k*step<F.DUR:
    s0=int(k*step*SR); m=min(int(step*2.2*SR),N-s0)
    if m<=0: break
    u=np.arange(m)/SR; fr=f(cyc[k%4]); env=np.minimum(1,u/0.04)*np.exp(-u*1.1)
    y=sum(np.sin(2*np.pi*fr*h*u+h)*(0.6/h)*(1+0.3*np.sin(2*np.pi*0.7*u*h)) for h in (1,2,3,4,5,6))
    mus[s0:s0+m]+=0.035*env*y; k+=1
# Karplus-Strong pluck
def pluck(fr,d=1.2,bright=0.996):
    n=int(d*SR); p=max(2,int(SR/fr)); buf=rng.uniform(-1,1,p); out=np.zeros(n)
    for i in range(n):
        out[i]=buf[i%p]; buf[i%p]=bright*0.5*(buf[i%p]+buf[(i+1)%p])
    return out*np.exp(-np.arange(n)/SR*1.8)
# Yaman scale: S R G M# P D N (0 2 4 6 7 9 11)
sc=[0,2,4,6,7,9,11,12,14,16]
phr=[[7,9,11,12],[11,9,7,6],[4,6,7,9],[7,6,4,2],[0,4,7,11],[12,11,9,7],[6,7,9,7],[4,2,0,-1]]
cache={}
bar=4*beat
for bi in range(int(F.DUR/bar)+1):
    notes=phr[bi%len(phr)]
    for j,nn in enumerate(notes):
        if (bi*4+j)%3==2: continue
        tm=bi*bar+j*beat+(0.5*beat if j%2 else 0)
        mid=SA+12+nn
        if mid not in cache: cache[mid]=pluck(f(mid))
        sig=cache[mid]; s0=int(tm*SR); m=min(len(sig),N-s0)
        if m>0: mus[s0:s0+m]+=0.07*sig[:m]
# tabla-like: 'dha' (bass+ring) on 1 & 3, 'na' ring on off-beats, 'ge' slide
def bayan(d=0.45):
    u=np.arange(int(d*SR))/SR; fr=90+40*np.exp(-u*8); return np.sin(2*np.pi*np.cumsum(fr)/SR)*np.exp(-u*7)
def dayan(fr=520,d=0.25):
    u=np.arange(int(d*SR))/SR; return (np.sin(2*np.pi*fr*u)+0.5*np.sin(2*np.pi*fr*2.7*u))*np.exp(-u*16)
B=bayan(); Dn=dayan(); Dh=dayan(780,0.18)
pat=[('B',0),('D',0.5),('d',1),('D',1.5),('B',2),('D',2.5),('d',3),('d',3.5)]
for bi in range(int(F.DUR/bar)+1):
    for kind,off in pat:
        s0=int((bi*bar+off*beat)*SR)
        sig={'B':B,'D':Dn,'d':Dh}[kind]; m=min(len(sig),N-s0)
        if m>0: mus[s0:s0+m]+={'B':0.16,'D':0.07,'d':0.05}[kind]*sig[:m]
# sidechain duck under voice
envv=np.convolve(np.abs(vo),np.ones(2400)/2400,'same'); duck=1-0.72*np.clip(envv/0.05,0,1)
duck=np.convolve(duck,np.ones(4800)/4800,'same')
mus=mus*duck*0.55
fade=np.ones(N); fl=int(1.2*SR); fade[-fl:]=np.linspace(1,0,fl); mus*=fade
# --- sfx ---
fx=np.zeros(N+SR)
def put(sig,tm,g=1.0):
    a=int(max(0,tm)*SR); fx[a:a+len(sig)]+=sig*g
for b in F.STARTS[1:]: put(whoosh(),b-0.25,0.55); put(pop(1100),b,0.3)
rg=np.random.default_rng(7)
def clink(f=2600):
    n=int(0.25*SR); t=np.arange(n)/SR
    y=sum(np.sin(2*np.pi*f*m*t+rg.uniform(0,6))*np.exp(-t*(18+8*m))/m for m in (1,1.51,2.27,3.1))
    return y/np.abs(y).max()*0.3
def rumble(d=1.8):
    n=int(d*SR); t=np.arange(n)/SR; x=rg.normal(0,1,n)
    from sfx_lib import lp
    y=lp(x,np.full(n,0.004)); y=y/np.abs(y).max()
    return (y+0.5*np.sin(2*np.pi*42*t))*np.minimum(1,t/0.15)*np.exp(-t*1.6)*0.9
def ding(f=1320):
    n=int(1.2*SR); t=np.arange(n)/SR
    y=np.sin(2*np.pi*f*t)*np.exp(-t*3)+0.4*np.sin(2*np.pi*f*2.76*t)*np.exp(-t*6)+0.25*np.sin(2*np.pi*f*5.4*t)*np.exp(-t*9)
    return y/np.abs(y).max()*0.35
def creak(d=0.6):
    n=int(d*SR); t=np.arange(n)/SR; fr=180+60*np.sin(t*9)
    y=np.sign(np.sin(2*np.pi*np.cumsum(fr)/SR))*(0.5+0.5*np.sin(t*70))
    from sfx_lib import lp
    y=lp(y,np.full(n,0.08)); return y/np.abs(y).max()*np.sin(np.pi*t/d)*0.18
def chains(d=1.2):
    out=np.zeros(int(d*SR))
    for k in range(40):
        c=clink(rg.uniform(1800,4200))[:int(0.08*SR)]*rg.uniform(0.2,0.6); a=int(rg.uniform(0,d-0.1)*SR); out[a:a+len(c)]+=c
    return out
def clunk():
    from sfx_lib import hit
    h=hit()*1.2; c=np.concatenate([np.zeros(int(0.02*SR)),clink(900)]); c=np.pad(c,(0,max(0,len(h)-len(c))))[:len(h)]
    return h+c*0.6
S=F.STARTS
def horn(f=220,d=1.6):
    n=int(d*SR); tt=np.arange(n)/SR; y=np.zeros(n)
    for m in (1,1.26,1.5,2):
        ph=2*np.pi*f*m*tt; y+=np.sign(np.sin(ph))*0.15+np.sin(ph)*0.5
    from sfx_lib import lp
    y=lp(y,np.full(n,0.06)); env=np.minimum(1,tt/0.15)*np.exp(-np.maximum(0,tt-0.6)*2.5)
    return y/np.abs(y).max()*env*0.5
def drum(n_hits=3,gap=0.18):
    from sfx_lib import hit
    h=hit(); out=np.zeros(int((n_hits*gap+0.4)*SR))
    for k in range(n_hits): a=int(k*gap*SR); out[a:a+len(h)]+=h[:len(out)-a]*(0.7+0.15*k)
    return out
def murmur(d=2.0):
    n=int(d*SR); x=rg.normal(0,1,n)
    from sfx_lib import lp
    y=lp(x,np.full(n,0.05)); y=y-lp(y,np.full(n,0.01)); y=y/np.abs(y).max()
    tt=np.arange(n)/SR; return y*(0.6+0.4*np.sin(tt*7))*np.minimum(1,tt/0.3)*np.minimum(1,(d-tt)/0.4)*0.25
def riser(d=0.7):
    n=int(d*SR); tt=np.arange(n)/SR; x=rg.normal(0,1,n)
    from sfx_lib import lp
    y=lp(x,np.linspace(0.01,0.25,n)); y=y/np.abs(y).max()
    return y*(tt/d)**2*0.5
def beep(f=1200,d=0.04):
    n=int(d*SR); tt=np.arange(n)/SR; return np.sin(2*np.pi*f*tt)*np.exp(-tt*60)*0.25
def kaching():
    n=int(0.9*SR); tt=np.arange(n)/SR; x=rg.normal(0,1,int(0.05*SR))*np.exp(-np.arange(int(0.05*SR))/SR*80)
    y=np.zeros(n); y[:len(x)]+=x*0.5
    y+=ding(2093)[:n]*1.2 if len(ding(2093))>=n else np.pad(ding(2093),(0,n-len(ding(2093))))*1.2
    y[int(0.08*SR):]+=(ding(2637)[:n-int(0.08*SR)])*1.0
    return y*0.7
# soft ticks on headline words (quiet, keyboard-like)
M=_m
def whistle(d=0.38):
    u=np.arange(int(d*SR))/SR; fr=900+2400*(u/d)**1.3; return np.sin(2*np.pi*np.cumsum(fr)/SR)*np.minimum(1,u/0.05)*0.25
def boom():
    u=np.arange(int(0.9*SR))/SR; x=np.random.default_rng(5).normal(0,1,len(u))
    from sfx_lib import lp
    y=lp(x,np.full(len(u),0.02)); y=y/np.abs(y).max(); return (y+0.6*np.sin(2*np.pi*55*u))*np.exp(-u*4.5)*0.8
def crackle(d=1.4,seed=0):
    r=np.random.default_rng(seed); out=np.zeros(int(d*SR))
    for k in range(60):
        a=int(r.uniform(0,d-0.03)*SR)*1; n=int(0.012*SR); out[a:a+n]+=r.normal(0,1,n)*np.exp(-np.arange(n)/SR*400)*r.uniform(0.2,0.7)*np.exp(-a/SR*1.5)
    return out*0.6
def bell(f0=660,d=2.5):
    u=np.arange(int(d*SR))/SR
    y=sum(a*np.sin(2*np.pi*f0*r*u)*np.exp(-u*dd) for r,a,dd in ((1,1,1.2),(2.76,0.5,2.2),(5.4,0.3,3.5),(8.9,0.15,5)))
    return y/np.abs(y).max()*0.45
def sparkle(seed=0,d=0.9):
    r=np.random.default_rng(seed); out=np.zeros(int(d*SR))
    for k in range(10):
        a=int(k*d/10*SR); fr=r.uniform(2500,5200); n=int(0.25*SR); u=np.arange(n)/SR; sig=np.sin(2*np.pi*fr*u)*np.exp(-u*18)*0.25
        out[a:a+n]+=sig[:len(out)-a]
    return out
def tick2(): 
    u=np.arange(int(0.03*SR))/SR; return np.sin(2*np.pi*3000*u)*np.exp(-u*200)*0.4
for i,b in enumerate(_d['bursts']):
    put(whistle(),b,0.6); put(boom(),b+0.35,0.55); put(crackle(1.4,i),b+0.45,0.5)
for s in F.STARTS[1:]: put(bell(660 if F.STARTS.index(s)%2 else 880),s,0.35)
put(sparkle(1),0.2,0.6); put(sparkle(2),1.4,0.5)
for k in range(int((M['time']-F.STARTS[1])/0.12)): put(tick2(),F.STARTS[1]+0.2+k*0.12,0.5)
for k in range(24): put(tick2(),M['time']+0.2+k*0.066,0.35)
put(ding(1568),M['seventy'],0.45); put(pop(800),M['pre'],0.4); put(pop(1000),M['pre']+0.6,0.4)
put(whoosh(),M['samvat']-0.1,0.5); put(bell(990,3),M['samvat']+0.3,0.4); put(clunk(),M['bse'],0.45); put(clunk(),M['nse'],0.45)
put(clunk(),M['real']+0.2,0.8); put(rumble(0.5),M['real']+0.2,0.3); put(pop(900),M['cas'],0.45)
for k in range(8): put(clink(2200+k*150),F.STARTS[4]+k*0.11,0.35)
for k in range(20): put(pop(600+k*25),M['rose']+0.1+k*0.07,0.22)
put(kaching(),M['big08'],0.5); put(rumble(0.6),M['small'],0.3)
for k in range(10): put(pop(700+k*40),M['full']+0.1+k*0.09,0.3)
put(riser(1.0),M['avg']-0.9,0.3); put(sparkle(3),M['best'],0.55); put(clunk(),M['red'],0.4)
put(bell(550,3),M['trad'],0.35)
for k in range(6): put(clink(1800+k*200),M['token']+k*0.2,0.4)
put(pop(900),M['save'],0.5); put(whoosh(),M['send']-0.2,0.5); put(sparkle(4,1.4),M['diwali'],0.7)
put(whoosh(),F.DUR-0.6,0.6)
mix=vo+mus+fx[:N]*0.8
mix=np.tanh(mix*1.1)/np.tanh(1.1)
w=wave.open(f'{F.SH}mix.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.clip(mix,-1,1)*32767).astype(np.int16).tobytes()); w.close(); print('mix ok', round(F.DUR,1))
