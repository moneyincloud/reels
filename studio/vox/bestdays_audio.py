import numpy as np, wave, subprocess, sys
sys.path.insert(0,'.')
import importlib
F = importlib.import_module(sys.argv[1] if len(sys.argv) > 1 else "bestdays")
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
S=F.STARTS; STARTS=F.STARTS; at=F.at
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
put(drum(3),0.05,0.8)
for k in range(5): put(pop(700+k*120),0.05+k*0.16,0.5)
put(hit(),1.0,0.9)
put(clunk(),at(0,'decided',-0.25),0.7); put(clunk(),at(0,'decided',0.0),0.6)
# s2 chart counter
T=STARTS[1]+0.05; put(pop(900),T,0.5)
tc=min(at(1,'Today',-1.6),T+1.0)
for k in range(30): put(beep(1300-k*12),tc+k*0.105,0.3)
put(rumble(0.9),at(1,'Down seven',-0.3),0.7); put(hit(),at(1,'Down seven',-0.3),0.5)
# s3 grid + countdown
for k in range(10): put(tick(),STARTS[2]+0.25+k*0.12,0.4)
for k in range(5): put(ding(1200+k*90),at(2,'five best',-0.3)+k*0.1,0.35)
for k in range(5): put(clunk(),at(2,'Five, out',0.0)+k*0.1,0.35)
T=at(2,'How much',-0.3); put(pop(1000),T,0.6)
for k in range(3): put(beep(1000),T+0.2+k,0.6)
# s4 tear reveal + rehook
T=STARTS[3]+0.05; put(whoosh(),T,0.8); put(hit(),T+0.15,0.7)
for k in range(8): put(beep(1200-k*50),at(3,'A seven',-0.1)+k*0.1,0.35)
put(riser(0.8),at(3,'But here',-0.9),0.6); put(drum(2),at(3,'But here',-0.3),0.7)
# s5 quiz
put(pop(800),at(4,'calm',-0.4),0.5); put(pop(1000),at(4,'right after',-0.4),0.5)
T=at(4,'Three',-0.2)
for k in range(3): put(beep(1000 if k<2 else 1400),T+k,0.6)
# s6 answer
T=STARTS[5]+0.05; put(ding(1568),T,0.6); put(hit(),T,0.5)
for k in range(20): put(beep(900+k*25),T+0.6+k*0.13,0.3)
put(kaching(),at(5,'almost four',-0.3)+0.8,0.55)
# s7 timeline
T=at(6,'ten worst',-1.2)
for k in range(10): put(tick(),T+0.06*k,0.45)
T=at(6,'Four of',-0.3)
for k in range(5): put(ding(1300+k*100),T+0.1*k,0.35)
put(riser(0.6),at(6,'within two',-0.8),0.5); put(drum(2),at(6,'within two',-0.2),0.6)
# s8 answer + cheat sheet
put(drum(2),at(7,"You can't",-0.3),0.7)
T=at(7,'without missing',-0.3)
for k in range(5): put(ding(1320+k*120),T+0.35+0.12*k,0.4)
put(pop(1200),T+0.6+0.12*5,0.6)
put(clunk(),at(7,'Past data',-0.3),0.6)
# s9 CTA
T=at(8,'Send this',-0.3); put(whoosh(),T+0.3,0.8)
put(pop(1200),at(8,'Save this',-0.3),0.7); put(pop(900),at(8,'follow',-0.2),0.6)
put(hit(),at(8,'Five days',-0.2),0.5)
mix=vo+mus+fx[:N]*0.8
mix=np.tanh(mix*1.1)/np.tanh(1.1)
w=wave.open(f'{F.SH}mix.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.clip(mix,-1,1)*32767).astype(np.int16).tobytes()); w.close(); print('mix ok', round(F.DUR,1))
