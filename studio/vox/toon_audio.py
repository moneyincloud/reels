"""Chennai Toon audio: voice + bouncy original music bed (synthesised, ducked) + cartoon SFX.
usage: python3 toon_audio.py <studio_voice_dir> <motion_project_dir>
Reads <project>/build/t.json (VO starts, scene starts, SFX cues) and <voice_dir>/vo/<i>.wav; writes <project>/assets/vo_mix.wav"""
import sys, json, subprocess, numpy as np, wave
sys.path.insert(0, '/home/claude/reels/studio/vox')
from sfx_lib import whoosh, pop, tick, hit, lp
vdir, proj = sys.argv[1], sys.argv[2]
T = json.load(open(proj + '/build/t.json'))
SR = 48000; DUR = T['DUR']; N = int(DUR * SR)
rg = np.random.default_rng(11)


def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(float) / 32768


vo = np.zeros(N)
for i, t in enumerate(T['VO']):
    x = load(f'{vdir}/vo/{i}.wav'); a = int(t * SR); vo[a:a + len(x)] += x[:max(0, N - a)]
vo = vo / np.abs(vo).max() * 0.85

# ---- music bed: 112 BPM, I-V-vi-IV in D major, plucky marimba + bass + kick/clap/shaker
bpm = 112; beat = 60 / bpm; bar = 4 * beat
f = lambda m: 440 * 2 ** ((m - 69) / 12)
prog = [[62, 66, 69], [69, 73, 76], [71, 74, 78], [67, 71, 74]]
mus = np.zeros(N + SR)
def note(m, t0, d, g, kind='pluck'):
    a = int(t0 * SR); n = int(d * SR)
    if a >= N: return
    tt = np.arange(n) / SR
    if kind == 'pluck':
        y = (np.sin(2 * np.pi * f(m) * tt) + 0.35 * np.sin(2 * np.pi * f(m) * 4 * tt) * np.exp(-tt * 30)) * np.exp(-tt * 9)
    else:
        y = np.sin(2 * np.pi * f(m) * tt) * np.minimum(1, tt / 0.01) * np.exp(-tt * 4)
    mus[a:a + n] += g * y[:len(mus) - a]
patt = [0, 2, 1, 2, 0, 1, 2, 1]   # arpeggio index per 8th
for b in range(int(DUR / bar) + 1):
    ch = prog[b % 4]
    for e in range(8):
        note(ch[patt[e]] + (12 if e in (3, 7) else 0), b * bar + e * beat / 2, 0.35, 0.09)
    note(ch[0] - 24, b * bar, beat * 1.5, 0.22, 'bass'); note(ch[0] - 24, b * bar + 2.5 * beat, beat, 0.16, 'bass')
for k in range(int(DUR / beat)):
    s = int(k * beat * SR)
    if k % 2 == 0:   # kick
        m = int(0.22 * SR); u = np.arange(m) / SR
        if s + m < N: mus[s:s + m] += 0.3 * np.sin(2 * np.pi * (48 + 80 * np.exp(-u * 32)) * u) * np.exp(-u * 13)
    else:            # clap
        m = int(0.12 * SR)
        if s + m < N:
            z = rg.normal(0, 1, m); z = np.diff(np.concatenate([[0], z]))
            mus[s:s + m] += 0.07 * z * np.exp(-np.arange(m) / SR * 30)
    for h in (0.5,):  # off-beat shaker
        s2 = int((k + h) * beat * SR); m = int(0.04 * SR)
        if s2 + m < N:
            z = np.diff(np.concatenate([[0], rg.normal(0, 1, m)])); mus[s2:s2 + m] += 0.035 * z * np.exp(-np.arange(m) / SR * 90)
mus = mus[:N]
envv = np.convolve(np.abs(vo), np.ones(2400) / 2400, 'same'); duck = 1 - 0.6 * np.clip(envv / 0.05, 0, 1)
duck = np.convolve(duck, np.ones(4800) / 4800, 'same'); mus *= duck * 0.55
fl = int(1.0 * SR); mus[-fl:] *= np.linspace(1, 0, fl)
fi = int(0.4 * SR); mus[:fi] *= np.linspace(0, 1, fi)

# ---- sfx
fx = np.zeros(N + 2 * SR)
def put(sig, tm, g=1.0):
    a = int(max(0, tm) * SR); fx[a:a + len(sig)] += sig[:len(fx) - a] * g
def ding(fr=1320):
    n = int(1.0 * SR); t = np.arange(n) / SR
    y = np.sin(2 * np.pi * fr * t) * np.exp(-t * 3) + 0.4 * np.sin(2 * np.pi * fr * 2.76 * t) * np.exp(-t * 6)
    return y / np.abs(y).max() * 0.35
def kaching():
    n = int(1.1 * SR); y = np.zeros(n); m = int(0.05 * SR)
    y[:m] += rg.normal(0, 1, m) * np.exp(-np.arange(m) / SR * 80) * 0.5
    d1 = ding(2093); y[:len(d1)] += d1 * 1.2; d2 = ding(2637); a = int(0.08 * SR); y[a:a + len(d2)] += d2[:n - a]
    return y * 0.7
def coin():
    n = int(0.35 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1975 * t) * (t < 0.07) + np.sin(2 * np.pi * 2637 * t) * (t >= 0.07)) * np.exp(-t * 9) * 0.3
def riser(d=0.9):
    n = int(d * SR); tt = np.arange(n) / SR; y = lp(rg.normal(0, 1, n), np.linspace(0.01, 0.25, n)); y /= np.abs(y).max()
    return y * (tt / d) ** 2 * 0.5
def boing():
    n = int(0.4 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * (180 + 260 * np.sin(t * 22) * np.exp(-t * 6)) * t) * np.exp(-t * 7) * 0.35
KIND = dict(pop=lambda: pop(900), hit=hit, ding=ding, kaching=kaching, coin=coin, riser=riser, tick=tick, boing=boing, whoosh=whoosh)
GAIN = dict(pop=0.55, hit=0.6, ding=0.35, kaching=0.5, coin=0.5, riser=0.35, tick=0.25, boing=0.5, whoosh=0.5)
for i, s in enumerate(T['STARTS'][1:], 1):
    put(whoosh(), s + 0.2 - 0.38, 0.7)
for k, t in T['SFX']:
    put(KIND[k](), t, GAIN[k])
# soft caption ticks on each chunk's first word
for sc in T['W']:
    for ph in sc:
        put(tick(), ph[0], 0.12)
mix = vo + mus * 0.75 + fx[:N] * 0.8
mix = np.tanh(mix * 1.1) / np.tanh(1.1); mix = mix / np.max(np.abs(mix)) * 0.89
fo = int(SR * 0.5); mix[-fo:] *= np.linspace(1, 0, fo)
w = wave.open(proj + '/assets/vo_mix.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes()); w.close(); print('mix ok', round(DUR, 1))
