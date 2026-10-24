import numpy as np, wave, sys
SR=48000; DUR=56.4
rng=np.random.default_rng(3)
def env(n,a,r):
    e=np.ones(n); na=int(a*n); e[:na]=np.linspace(0,1,na)**1.5; e[na:]=np.linspace(1,0,n-na)**2; return e
def lp(x,k):  # one-pole lowpass with time-varying coef k (0..1)
    y=np.zeros_like(x); s=0.0
    for i in range(len(x)): s+= k[i]*(x[i]-s); y[i]=s
    return y
def whoosh(d=0.42):
    n=int(d*SR); x=rng.normal(0,1,n)
    k=np.linspace(0.35,0.03,n)          # closing low-pass = pitch sweeping down
    y=lp(x,k); y=y-lp(y,np.full(n,0.01))  # crude band-pass
    return y/np.abs(y).max()*env(n,0.55,0.45)*0.5
def pop(f=780,d=0.05):
    n=int(d*SR); t=np.arange(n)/SR; fr=f*np.exp(-t*30)
    return np.sin(2*np.pi*np.cumsum(fr)/SR)*np.exp(-t*70)*0.35
def tick(d=0.02):
    n=int(d*SR); x=rng.normal(0,1,n); x=x-lp(x,np.full(n,0.3))
    return x/np.abs(x).max()*np.exp(-np.arange(n)/SR*250)*0.12
def hit():
    n=int(0.32*SR); t=np.arange(n)/SR
    th=np.sin(2*np.pi*(55+40*np.exp(-t*25))*t)*np.exp(-t*14)
    tr=rng.normal(0,1,n)*np.exp(-t*90); tr=lp(tr,np.full(n,0.25))
    y=th*0.8+tr*0.5; return y/np.abs(y).max()*0.55
