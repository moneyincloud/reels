"""ITC factory film score + foley + voice mix (all synthesised). python3 build/audio.py <studio_voice_dir>"""
import sys, os, json, subprocess, numpy as np, wave
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = sys.argv[1]
T = json.load(open(P + '/build/t.json'))
SR = 48000; DUR = T['DUR']; N = int(DUR * SR) + SR
rg = np.random.default_rng(7)
f = lambda m: 440 * 2 ** ((m - 69) / 12)
def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(float) / 32768
def lp(x, a):
    y = np.zeros_like(x); s = 0.0
    for i in range(len(x)): s += a * (x[i] - s); y[i] = s
    return y
def env(n, a=0.005, d=0.2):
    t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t / d)
def put(buf, sig, t, g=1.0):
    a = int(max(0, t) * SR); b = min(len(buf), a + len(sig)); buf[a:b] += sig[:b - a] * g

vo = np.zeros(N)
for i, t in enumerate(T['VO']):
    x = load(f'{V}/vo/{i}.wav'); put(vo, x, t)
vo = vo / np.abs(vo).max() * 0.9

# ---- march, 120 BPM, D minor-ish factory figure; stops dead at the excise gate
bpm = 120; beat = 0.5
gate = T['P'][3][1]; gate_end = gate + 1.6
def band_on(t): return (t < gate or t >= gate_end) and t > 0.2
mus = np.zeros(N)
bass_seq = [50, 50, 57, 50, 53, 53, 57, 55]          # bassoon line
clar_seq = [62, 65, 69, 65, 62, 64, 65, 67, 69, 67, 65, 64, 62, 60, 62, 0]
def bassoon(m, d):
    n = int(d * SR); t = np.arange(n) / SR; ph = (f(m) * t) % 1
    x = (2 * ph - 1); x = lp(x, 0.08); return x * env(n, 0.01, d * 0.7) * 0.5
def clar(m, d):
    n = int(d * SR); t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f(m) * k * t) / k for k in (1, 3, 5, 7))
    return x * np.minimum(1, t / 0.02) * np.exp(-t / (d * 1.4)) * 0.25
def wood():
    n = int(0.08 * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * 1700 * t) * np.exp(-t * 60) * 0.5
def kick():
    n = int(0.3 * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * (45 + 90 * np.exp(-t * 30)) * t) * np.exp(-t * 9) * 0.9
def glock(m):
    n = int(1.4 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f(m) * t) + 0.4 * np.sin(2 * np.pi * f(m) * 2.76 * t) * np.exp(-t * 4)) * np.exp(-t * 2.5) * 0.35
k = 0; t = 0.0
while t < DUR - 1.0:
    if band_on(t):
        put(mus, bassoon(bass_seq[k % 8], beat * 0.95), t, 0.8)
        if k % 2 == 0: put(mus, kick(), t, 0.5)
        else: put(mus, wood(), t, 0.5)
        m = clar_seq[(2 * k) % 16]
        if m and t > T['STARTS'][1]: put(mus, clar(m, beat * 0.48), t, 0.55)
        m2 = clar_seq[(2 * k + 1) % 16]
        if m2 and t > T['STARTS'][2]: put(mus, clar(m2, beat * 0.48), t + beat / 2, 0.45)
    k += 1; t += beat
# glockenspiel on each station lighting up (S[k]+0.6)
for i, s in enumerate(T['STARTS'][2:9]):
    put(mus, glock(74 + [0, 3, 5, 7, 10, 12, 15][i]), s + 0.6, 0.9)
# the final pull-back: a lit chord
for m in (62, 65, 69, 74): put(mus, glock(m), T['STARTS'][9] + 2.6, 0.7)
fo = int(1.5 * SR); mus[N - SR - fo:N - SR] *= np.linspace(1, 0, fo); mus[N - SR:] = 0

# ---- foley
fx = np.zeros(N)
def noise(n): return rg.normal(0, 1, n)
def thump():
    n = int(0.25 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 70 * t) * np.exp(-t * 18) + lp(noise(n), 0.05) * np.exp(-t * 25) * 2) * 0.6
def whoosh(d=0.6):
    n = int(d * SR); t = np.arange(n) / SR; x = lp(noise(n), 0.12); return x / np.abs(x).max() * np.sin(np.pi * t / d) ** 2 * 0.5
def clank():
    n = int(0.5 * SR); t = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * fr * t) * np.exp(-t * dd) for fr, dd in ((420, 9), (1130, 14), (2210, 22))) * 0.3
def chain(d=1.8):
    n = int(d * SR); x = np.zeros(n)
    for j in range(int(d * 14)):
        a = int(j / 14 * SR); m = int(0.03 * SR); x[a:a + m] += np.sin(2 * np.pi * 2600 * np.arange(m) / SR) * np.exp(-np.arange(m) / SR * 120) * 0.4
    return x
def coins():
    out = np.zeros(int(1.0 * SR))
    for j in range(7):
        a = int(rg.uniform(0, 0.7) * SR); m = int(0.25 * SR); tt = np.arange(m) / SR
        out[a:a + m] += np.sin(2 * np.pi * rg.uniform(2400, 3600) * tt) * np.exp(-tt * 18) * 0.3
    return out
def rattle(d):
    n = int(d * SR); x = lp(noise(n), 0.3) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 9 * np.arange(n) / SR))) * 0.06; return x
def hum(d, fr=90):
    n = int(d * SR); t = np.arange(n) / SR; return (np.sin(2 * np.pi * fr * t) + 0.3 * np.sin(2 * np.pi * 2 * fr * t)) * 0.05 * np.minimum(1, t / 0.3) * np.minimum(1, (d - t) / 0.3)
S = T['STARTS']
put(fx, whoosh(0.9), S[1] - 0.7, 0.8)                     # through the porthole
put(fx, rattle(S[2] - S[1] + 0.5), S[1], 1.0)             # belt
put(fx, clank(), S[1] + 0.5, 0.6)                         # gantry sign bounce
put(fx, whoosh(0.7), S[2] - 0.6, 0.6); put(fx, thump(), S[2] + 0.25, 0.5)   # crate falls into hopper
for s in T['STAMPS']: put(fx, thump(), s, 0.9)            # the press
put(fx, clank(), T['P'][3][1], 1.0)                       # EXCISE gate slams (band stops)
put(fx, rattle(S[5] - S[4] + 0.5), S[4], 1.2)             # packing belt
for j in range(int((S[6] - S[5]) / 0.24)): put(fx, lp(noise(int(0.08 * SR)), 0.4) * 0.08, S[5] + j * 0.24, 1.0)   # sieve
put(fx, hum(S[7] - S[6] + 0.5, 85), S[6], 1.0)            # rollers
put(fx, chain(1.8), S[7] + 0.2, 0.8); put(fx, chain(1.8), S[7] + 1.4, 0.6)    # crane
put(fx, clank(), S[8] + 0.4, 1.0); put(fx, thump(), S[8] + 1.6, 0.7)          # vault wheel
put(fx, coins(), S[8] + 3.0, 1.0)
put(fx, whoosh(1.2), S[9] + 1.6, 0.6)                     # great pull-back

# ---- mix: duck music under the voice, carve 300 Hz-4 kHz roughly by lowering music when voice is active
envv = np.convolve(np.abs(vo), np.ones(2400) / 2400, 'same'); duck = 1 - 0.55 * np.clip(envv / 0.04, 0, 1)
duck = np.convolve(duck, np.ones(6000) / 6000, 'same')
mix = vo + mus * duck * 0.42 + fx * 0.8
mix = np.tanh(mix * 1.2) / np.tanh(1.2)
mix = mix[:int(DUR * SR)]; mix = mix / np.max(np.abs(mix)) * 0.89
fo = int(0.5 * SR); mix[-fo:] *= np.linspace(1, 0, fo)
w = wave.open(P + '/assets/mix.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes()); w.close(); print('mix ok', DUR)
