"""copper audio: owner's Tamil VO (copper/vo/0.wav ..) + music bed + SFX. Without a recording it writes a music+SFX preview."""
import numpy as np, wave, subprocess, sys
sys.path.insert(0, '.')
import os
import copper as F
from sfx_lib import whoosh, pop, tick, hit, lp
SR = 48000; N = int(F.DUR * SR)
def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(float) / 32768
vo = np.zeros(N)
for i, t in enumerate(F.VO):
    if not os.path.exists(f'{F.SH}vo/{i}.wav'): continue
    x = load(f'{F.SH}vo/{i}.wav'); a = int(t * SR); vo[a:a + len(x)] += x[:N - a]
if np.abs(vo).max() > 0: vo = vo / np.abs(vo).max() * 0.88
# music: minor pad Am - F - C - E, pulse bass, kick on 1 and 3, hats; switches to brighter after the reveal
bpm = 100; beat = 60 / bpm; bar = 4 * beat; f = lambda m: 440 * 2 ** ((m - 69) / 12)
dark = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [52, 56, 59]]; bright = [[57, 61, 64], [54, 57, 61], [50, 54, 57], [52, 56, 59]]
mus = np.zeros(N); rng = np.random.default_rng(3)
reveal = F.at(3, 'உண்மையான')
for b in range(int(F.DUR / bar) + 1):
    a = int(b * bar * SR); n = min(int(bar * SR), N - a)
    if n <= 0: break
    tt = np.arange(n) / SR; ch = (bright if b * bar > reveal else dark)[b % 4]
    env = np.minimum(1, tt / 0.4) * np.exp(-tt * 0.3)
    for m in ch: mus[a:a + n] += 0.04 * env * (np.sin(2 * np.pi * f(m) * tt) + 0.25 * np.sin(2 * np.pi * f(m + 12) * tt))
    for k in range(8):
        s = int((b * bar + k * beat / 2) * SR); m = min(int(beat / 2 * SR * 0.9), N - s)
        if m > 0: u = np.arange(m) / SR; mus[s:s + m] += 0.08 * np.sin(2 * np.pi * f(ch[0] - 24) * u) * np.exp(-u * 6)
for k in range(int(F.DUR / beat)):
    s = int(k * beat * SR)
    if k % 2 == 0:
        m = int(0.3 * SR); u = np.arange(m) / SR
        if s + m < N: mus[s:s + m] += 0.28 * np.sin(2 * np.pi * (45 + 90 * np.exp(-u * 35)) * u) * np.exp(-u * 10)
    for h in (0.5,):
        s2 = int((k + h) * beat * SR); m = int(0.04 * SR)
        if s2 + m < N: z = np.diff(np.concatenate([[0], rng.normal(0, 1, m)])); mus[s2:s2 + m] += 0.03 * z * np.exp(-np.arange(m) / SR * 90)
envv = np.convolve(np.abs(vo), np.ones(2400) / 2400, 'same'); duck = 1 - 0.7 * np.clip(envv / 0.05, 0, 1)
mus *= np.convolve(duck, np.ones(4800) / 4800, 'same') * 0.6
fl = int(1.0 * SR); mus[-fl:] *= np.linspace(1, 0, fl)
fx = np.zeros(N + 2 * SR)
def put(sig, tm, g=1.0):
    a = int(max(0, tm) * SR); fx[a:a + len(sig)] += sig * g
def boom(d=1.2):
    n = int(d * SR); u = np.arange(n) / SR
    return (np.sin(2 * np.pi * (38 + 60 * np.exp(-u * 8)) * u) * np.exp(-u * 3.5) + 0.3 * lp(rng.normal(0, 1, n), np.full(n, 0.02)) * np.exp(-u * 6)) * 0.9
def riser(d=1.0):
    n = int(d * SR); u = np.arange(n) / SR; y = lp(rng.normal(0, 1, n), np.linspace(0.01, 0.3, n)); y /= np.abs(y).max()
    return y * (u / d) ** 2 * 0.55
def glitch(d=0.3):
    n = int(d * SR); y = np.sign(np.sin(2 * np.pi * np.cumsum(rng.choice([180, 420, 900, 1600], n)) / SR)); return y * np.exp(-np.arange(n) / SR * 8) * 0.18
def ding(fq=1568):
    n = int(1.0 * SR); u = np.arange(n) / SR; return (np.sin(2 * np.pi * fq * u) * np.exp(-u * 3) + 0.4 * np.sin(2 * np.pi * fq * 2.76 * u) * np.exp(-u * 7)) * 0.3
def down(d=0.6):
    n = int(d * SR); u = np.arange(n) / SR; return np.sin(2 * np.pi * np.cumsum(900 * np.exp(-u * 3)) / SR) * np.exp(-u * 3) * 0.2
at = F.at
put(riser(0.8), at(0, 'profit', -0.6), 0.5); put(boom(), at(0, 'profit', 0.2), 0.8); put(glitch(), at(0, 'profit', 0.2), 0.7)
put(hit(), at(0, 'ஏன்'), 0.6); put(pop(900), at(0, 'ஏறிருக்கு'), 0.5)
put(whoosh(), F.VO[1], 0.5); put(hit(), at(1, 'சுரங்கம்', -0.3), 0.5)
put(pop(800), F.VO[2], 0.4); put(riser(0.8), at(2, 'Revenue', -0.8), 0.35); put(ding(1318), at(2, 'Revenue', 1.0), 0.45)
put(riser(0.8), at(2, 'Profit', -0.8), 0.4); put(ding(1760), at(2, 'Profit', 1.0), 0.55)
put(rumble := boom(1.4), at(3, 'உண்மையான'), 0.6); put(glitch(), at(3, 'உண்மையான'), 0.5)
put(hit(), F.VO[4], 0.6); put(ding(2093), at(4, 'record'), 0.5)
put(down(), at(5, 'ஒண்ணு'), 0.6); put(hit(), at(5, 'ஒண்ணு'), 0.4); put(riser(0.6), at(5, 'ரெண்டு', -0.6), 0.4); put(ding(1568), at(5, 'ரெண்டு'), 0.45)
put(hit(), F.VO[6], 0.5); put(ding(1760), at(6, 'லாபம்'), 0.5)
put(glitch(), F.VO[7], 0.5); put(down(0.9), at(7, 'ஜனவரில'), 0.4); put(boom(), at(7, 'நாப்பது'), 0.8); put(hit(), at(7, 'இறங்குனா'), 0.6)
put(whoosh(), at(8, 'அனுப்புங்க', -0.2), 0.6); put(pop(1100), at(8, 'Save'), 0.6)
for s in F.SWITCH: put(whoosh(0.3), s - 0.1, 0.45)
mix = vo + mus + fx[:N] * 0.8
mix = np.tanh(mix * 1.15) / np.tanh(1.15)
w = wave.open(f'{F.SH}mix.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes()); w.close(); print('mix ok', round(F.DUR, 1))
