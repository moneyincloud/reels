"""VO + ducked music bed + SFX -> assets/vo_mix.wav (48 kHz mono)."""
import numpy as np, json, os, sys, subprocess, soundfile as sf
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H + '/../../../studio/vox')
from sfx_lib import whoosh, pop, tick, hit
D = H + '/../../../studio/ipo1123/'
T = json.load(open(H + '/t.json')); SR = 48000; N = int(T['DUR'] * SR)
def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(float) / 32768
vo = np.zeros(N)
for i, t in enumerate(T['VO']):
    x = load(f'{D}vo/{i}.wav'); a = int(t * SR); vo[a:a + len(x)] += x[:N - a]
vo = vo / np.abs(vo).max() * 0.85
bpm = 100; beat = 60 / bpm; bar = 4 * beat
chords = [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 59], [55, 59, 62, 64]]
f = lambda m: 440 * 2 ** ((m - 69) / 12); mus = np.zeros(N)
for b in range(int(T['DUR'] / bar) + 1):
    a = int(b * bar * SR); n = min(int(bar * SR), N - a)
    if n <= 0: break
    tt = np.arange(n) / SR; e = np.minimum(1, tt / 0.5) * np.exp(-tt * 0.3)
    for m in chords[b % 4]: mus[a:a + n] += 0.05 * e * (np.sin(2 * np.pi * f(m) * tt) + 0.3 * np.sin(4 * np.pi * f(m) * tt))
    for k in range(4):
        s = int((b * bar + k * beat) * SR); m = min(int(beat * SR * 0.9), N - s)
        if m > 0: u = np.arange(m) / SR; mus[s:s + m] += 0.09 * np.sin(2 * np.pi * f(chords[b % 4][0] - 12) * u) * np.exp(-u * 3)
for k in range(int(T['DUR'] / beat)):
    s = int(k * beat * SR); m = int(0.25 * SR)
    if k % 2 == 0 and s + m < N: u = np.arange(m) / SR; mus[s:s + m] += 0.2 * np.sin(2 * np.pi * (50 + 70 * np.exp(-u * 30)) * u) * np.exp(-u * 12)
ev = np.convolve(np.abs(vo), np.ones(2400) / 2400, 'same'); duck = np.convolve(1 - 0.72 * np.clip(ev / 0.05, 0, 1), np.ones(4800) / 4800, 'same')
mus = mus * duck * 0.5; fl = int(1.0 * SR); mus[-fl:] *= np.linspace(1, 0, fl)
fx = np.zeros(N + SR)
def put(sig, tm, g=1.0):
    a = int(max(0, tm) * SR); fx[a:a + len(sig)] += sig * g
def ding(fr=1320):
    n = int(1.0 * SR); t = np.arange(n) / SR
    y = np.sin(2 * np.pi * fr * t) * np.exp(-t * 3) + 0.4 * np.sin(2 * np.pi * fr * 2.76 * t) * np.exp(-t * 6); return y / np.abs(y).max() * 0.35
def riser(d=1.2):
    n = int(d * SR); t = np.arange(n) / SR; fr = 200 + 900 * (t / d) ** 2
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * (t / d) ** 2 * 0.25
def kaching():
    return np.concatenate([ding(2100)[:int(0.12 * SR)], ding(2800)]) * 0.8
put(hit(), 0.0, 0.9); put(whoosh(), 0.3, 0.6)
for s in T['STARTS'][1:]: put(whoosh(), s - 0.3, 0.8)
put(hit(), T['mist'], 0.8); put(pop(), T['sell0'], 0.7); put(pop(), T['sell0'] + 0.25, 0.7)
put(pop(), T['thu'] + 0.1, 0.7); put(pop(), T['fri'] + 0.1, 0.7)
put(hit(), T['notout'], 0.9); put(riser(), T['twist'] - 1.3, 0.8)
for k in range(15): put(tick(), T['c15'] + k * 0.066, 0.5)
for k in range(20): put(tick(), T['c65'] + 0.1 + k * 0.07, 0.4)
for k in ('fcb', 'fib', 'fad', 'fwed'): put(pop(), T[k], 0.7)
put(kaching(), T['frev'] + 1.2, 0.6); put(riser(0.8), T['floss'] - 0.8, 0.6); put(hit(), T['floss'] + 0.4, 1.0)
for k in ('istent',): [put(pop(), T[k] + d, 0.6) for d in (-0.1, 0.6, 1.2, 1.7)]
for k in ('imade', 'ideu', 'inld'): put(ding(1500), T[k] + 0.1, 0.5)
put(whoosh(), T['irev'] - 0.5, 0.9); put(kaching(), T['irev'] + 1.3, 0.5)
for k in range(7): put(ding(1320 + 60 * k), T['STARTS'][7] + 0.3 + k * 0.25, 0.25)
put(hit(), T['rhp'], 0.7); put(pop(780), T['save'], 0.8); put(whoosh(0.8), T['send'] + 1.2, 0.8)
mix = vo + mus + fx[:N] * 0.55
mix = mix / max(1e-6, np.abs(mix).max()) * 0.92
sf.write(H + '/../assets/vo_mix.wav', mix.astype(np.float32), SR, subtype='PCM_16')
os.makedirs(D, exist_ok=True); sf.write(D + 'mix.wav', mix.astype(np.float32), SR, subtype='PCM_16')
print('mix ok', round(len(mix) / SR, 2))
