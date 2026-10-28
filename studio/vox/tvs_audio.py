import numpy as np, wave, subprocess, sys
sys.path.insert(0,'.')
import importlib
F = importlib.import_module(sys.argv[1] if len(sys.argv) > 1 else "tvs")
from sfx_lib import whoosh, pop, tick, hit
SR=48000; N=int(F.DUR*SR)
def load(p):
    raw=subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar',str(SR),'-f','s16le','-'],capture_output=True).stdout
    return np.frombuffer(raw,np.int16).astype(float)/32768
vo=np.zeros(N)
for i,t in enumerate(F.VO):
    x=load(f'{F.SH}vo/{i}.wav'); a=int(t*SR); vo[a:a+len(x)]+=x[:N-a]
vo=vo/np.abs(vo).max()*0.85
# --- music bed, 95 BPM, Am7 Fmaj7 Cmaj7 G6 ---
bpm=95; beat=60/bpm; t=np.arange(N)/SR
chords=[[57,60,64,67],[53,57,60,64],[48,52,55,59],[55,59,62,64]]
mus=np.zeros(N); bar=4*beat
f=lambda m:440*2**((m-69)/12)
for b in range(int(F.DUR/bar)+1):
    a=int(b*bar*SR); n=min(int(bar*SR),N-a)
    if n<=0: break
    tt=np.arange(n)/SR; env=np.minimum(1,tt/0.6)*np.exp(-tt*0.25)
    for m in chords[b%4]:
        mus[a:a+n]+=0.05*env*(np.sin(2*np.pi*f(m)*tt)+0.3*np.sin(2*np.pi*f(m)*2*tt+0.4))
    root=chords[b%4][0]-12
    for k in range(4):  # soft bass on beats
        s=int((b*bar+k*beat)*SR); m=min(int(beat*SR*0.9),N-s)
        if m>0:
            u=np.arange(m)/SR; mus[s:s+m]+=0.09*np.sin(2*np.pi*f(root)*u)*np.exp(-u*3)
rng=np.random.default_rng(1)
for k in range(int(F.DUR/beat)):
    s=int(k*beat*SR)
    if k%2==0:  # kick
        m=int(0.25*SR); u=np.arange(m)/SR
        if s+m<N: mus[s:s+m]+=0.22*np.sin(2*np.pi*(50+70*np.exp(-u*30))*u)*np.exp(-u*12)
    for h in (0,0.5):  # shaker
        s2=int((k+h)*beat*SR); m=int(0.05*SR)
        if s2+m<N:
            z=rng.normal(0,1,m); z=np.diff(np.concatenate([[0],z]))
            mus[s2:s2+m]+=0.025*z*np.exp(-np.arange(m)/SR*80)
# sidechain duck under voice
envv=np.convolve(np.abs(vo),np.ones(2400)/2400,'same'); duck=1-0.72*np.clip(envv/0.05,0,1)
duck=np.convolve(duck,np.ones(4800)/4800,'same')
mus=mus*duck*0.55
fade=np.ones(N); fl=int(1.2*SR); fade[-fl:]=np.linspace(1,0,fl); mus*=fade
# --- sfx ---
fx=np.zeros(N+SR)
def put(sig,tm,g=1.0):
    a=int(max(0,tm)*SR); fx[a:a+len(sig)]+=sig*g
for b in F.B: put(whoosh(),b-0.3,0.9)
for ts in F.slam_times(): put(hit(),ts,0.8)
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
S=F.STARTS; at=F.at
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
STARTS=F.STARTS
put(drum(3),0.05,0.8)
for k in range(4): put(whoosh(),0.2+k*0.25,0.35); put(pop(600+k*90),0.6+k*0.25,0.4)
for k in range(6): put(clink(2400+k*150)[:int(0.2*SR)],1.4+k*0.35,0.5)
put(pop(900),at(0,'this map',-0.3),0.5)
put(riser(0.7),at(0,'Profit up',-1.0),0.6); put(kaching(),at(0,'Profit up',-0.2),0.6)
put(pop(800),STARTS[1]+0.05,0.5)
for k in range(14): put(beep(900+k*40),at(1,'stock jumped',0.1)+k*0.09,0.4)
put(ding(1568),at(1,'stock jumped',1.4),0.4)
for ph,ph2 in (('Revenue','seventeen'),('Profit','thirteen')):
    put(pop(700),at(2,ph,-0.3),0.5)
    for k in range(8): put(tick(),at(2,ph2,-0.2)+k*0.1,0.35)
    put(kaching(),at(2,ph2,0.6),0.45)
put(pop(600),at(2,'thirteen',0.8),0.4); put(pop(650),at(2,'thirteen',1.1),0.4)
put(riser(0.8),at(3,'surprise',-0.3),0.5); put(pop(900),at(3,'Electric',-0.3),0.5)
put(riser(0.9),at(3,'one lakh',-0.3),0.6); put(drum(2),at(3,'one lakh',0.7),0.8)
for ph in ('Apache','Jupiter','iQube','King','Norton'): put(pop(700),at(4,ph,-0.3),0.5); put(whoosh(),at(4,ph,-0.35),0.25)
put(horn(220,0.6),at(4,'Apache',-0.1),0.25)
put(whoosh(),STARTS[5]+0.3,0.4)
for k in range(10): put(tick(),STARTS[5]+0.5+k*0.12,0.3)
put(kaching(),at(5,'Exports',-0.2),0.5); put(drum(2),at(5,'one in every',-0.3),0.7)
for k in range(10): put(beep(800+k*60),at(6,'ninety',-0.3)+k*0.1,0.4)
for ph in ('Africa','Mexico','Nepal','Europe'):
    for k in range(4): put(whoosh(),at(6,ph,-0.3)+k*0.12,0.25); put(pop(700+k*80),at(6,ph,0.1)+k*0.12,0.35)
put(ding(1760),at(6,'Norton',-0.2),0.4)
put(drum(2),STARTS[7]+0.05,0.6); put(kaching(),at(7,'Growth is strong',-0.3),0.4)
for ph in ('high base','material costs','Norton'): put(horn(200,0.5),at(7,ph,-0.35),0.28); put(pop(600),at(7,ph,-0.35),0.4)
put(whoosh(),at(8,'send it',-0.3),0.5); put(pop(900),at(8,'Follow',-0.2),0.6)
put(whoosh(),F.DUR-0.6,0.6)
mix=vo+mus+fx[:N]*0.8
mix=np.tanh(mix*1.1)/np.tanh(1.1)
w=wave.open(f'{F.SH}mix.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.clip(mix,-1,1)*32767).astype(np.int16).tobytes()); w.close(); print('mix ok', round(F.DUR,1))
