"""Chart-story sound: tense minimal beat + data ticks + impact on the crash + riser into the bounce."""
import sys, os, json, subprocess, numpy as np, wave
sys.path.insert(0, '/home/claude/reels/studio/vox')
from sfx_lib import whoosh, pop, tick, hit, lp
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); V = sys.argv[1]
T = json.load(open(P + '/build/t.json')); SR = 48000; DUR = T['DUR']; N = int(DUR * SR)
rg = np.random.default_rng(3); f = lambda m: 440 * 2 ** ((m - 69) / 12)
def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(float) / 32768
def put(b, s, t, g=1.0):
    a = int(max(0, t) * SR); e = min(len(b), a + len(s)); b[a:e] += s[:e - a] * g
vo = np.zeros(N)
for i, t in enumerate(T['VO']): put(vo, load(f'{V}/vo/{i}.wav'), t)
vo = vo / np.abs(vo).max() * 0.9
mus = np.zeros(N); beat = 60 / 100
S = T['STARTS']; up = S[3]
for k in range(int(DUR / beat)):
    t = k * beat
    if t > DUR - 1.2: break
    m = int(0.25 * SR); u = np.arange(m) / SR
    if k % 4 in (0, 2): put(mus, np.sin(2 * np.pi * (42 + 70 * np.exp(-u * 30)) * u) * np.exp(-u * 10), t, 0.55)   # kick
    h = int(0.05 * SR); z = np.diff(np.concatenate([[0], rg.normal(0, 1, h)])) * np.exp(-np.arange(h) / SR * 70)
    put(mus, z, t + beat / 2, 0.05)                                                                                  # hat
    root = 38 if t < up else 45                                                                                      # D minor pulse, lifts to A at the bounce
    n_ = int(beat * SR); uu = np.arange(n_) / SR
    put(mus, lp(np.sign(np.sin(2 * np.pi * f(root) * uu)), np.full(len(uu), 0.03)) * np.exp(-uu * 3) * 0.35, t, 0.8)
    if t >= up:   # brighter pluck on the bounce
        put(mus, np.sin(2 * np.pi * f(root + 24 + [0, 7, 12, 7][k % 4]) * uu) * np.exp(-uu * 8) * 0.18, t, 1.0)
mus[-int(1.2 * SR):] *= np.linspace(1, 0, int(1.2 * SR))
fx = np.zeros(N + SR)
for t in T['CANDLES']: put(fx, tick(), t, 0.12)                     # candles printing
put(fx, hit(), T['PH'][0][0] + 0.9, 0.5)                            # -26% slam
for s in S[1:]: put(fx, whoosh(), s - 0.35, 0.6)                    # camera moves
put(fx, hit(), T['PH'][1][2] + 0.2, 1.0)                            # the crash day
put(fx, pop(900), T['PH'][1][1], 0.5); put(fx, pop(900), T['PH'][2][2], 0.5); put(fx, pop(1100), T['PH'][3][2], 0.5)
n_ = int(0.9 * SR); uu = np.arange(n_) / SR; ris = lp(rg.normal(0, 1, n_), np.linspace(0.01, 0.3, n_)); ris = ris / np.abs(ris).max() * (uu / 0.9) ** 2
put(fx, ris, T['PH'][3][1] - 0.9, 0.4)
ch = sum(np.sin(2 * np.pi * f(m) * uu) * np.exp(-uu * 3) for m in (81, 85, 88)) / 3
put(fx, ch, T['PH'][3][1], 0.5); put(fx, pop(700), T['PH'][4][0] + 0.2, 0.6)
envv = np.convolve(np.abs(vo), np.ones(2400) / 2400, 'same'); duck = np.convolve(1 - 0.55 * np.clip(envv / 0.04, 0, 1), np.ones(6000) / 6000, 'same')
mix = vo + mus * duck * 0.5 + fx[:N] * 0.8
mix = np.tanh(mix * 1.15) / np.tanh(1.15); mix = mix / np.abs(mix).max() * 0.89
mix[-int(0.4 * SR):] *= np.linspace(1, 0, int(0.4 * SR))
w = wave.open(P + '/assets/mix.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes()); w.close(); print('mix ok')
