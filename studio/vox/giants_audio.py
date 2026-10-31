"""giants audio: VO + tense music bed (darker, 100 BPM) + hard-hitting SFX on every slam. Writes giants/mix.wav."""
import numpy as np, wave, subprocess, sys
sys.path.insert(0, '.')
import giants as F
from sfx_lib import whoosh, pop, tick, hit, lp
SR = 48000; N = int(F.DUR * SR)
def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(float) / 32768
vo = np.zeros(N)
for i, t in enumerate(F.VO):
    x = load(f'{F.SH}vo/{i}.wav'); a = int(t * SR); vo[a:a + len(x)] += x[:N - a]
vo = vo / np.abs(vo).max() * 0.88
# music: minor pad Am - F - C - E, pulse bass, kick on 1 and 3, hats; switches to brighter after the reveal
bpm = 100; beat = 60 / bpm; bar = 4 * beat; f = lambda m: 440 * 2 ** ((m - 69) / 12)
dark = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [52, 56, 59]]; bright = [[57, 61, 64], [54, 57, 61], [50, 54, 57], [52, 56, 59]]
mus = np.zeros(N); rng = np.random.default_rng(3)
reveal = F.at(3, 'turned')
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
for ph in ('biggest', 'fell', 'twenty'): put(hit(), at(0, ph), 0.7); put(down(), at(0, ph, 0.1), 0.6)
put(riser(1.1), at(0, 'one hundred', -1.1), 0.5); put(boom(), at(0, 'one hundred'), 0.8); put(glitch(), at(0, 'one hundred'), 0.8)
for k in range(9): put(tick(), at(1, 'one lakh') + k * 0.08, 0.35)
for k in range(4): put(pop(700 + 80 * k), at(1, 'each', 0.15 + 0.12 * k), 0.45)
for ph in ('Reliance', 'HDFC', 'Infosys'): put(whoosh(), at(2, ph, -0.25), 0.55); put(down(0.9), at(2, ph, 0.2), 0.5)
put(riser(1.2), at(3, 'turned', -1.2), 0.6); put(boom(1.6), at(3, 'turned'), 0.9)
for k in range(20): put(tick(), at(3, 'turned') + k * 0.13, 0.25)
put(ding(2093), at(3, 'turned', 2.65), 0.6)
for k in range(11): put(tick(), at(4, 'Laurus', -0.1) + k * 0.045, 0.4)
put(hit(), at(4, 'No ads'), 0.6); put(whoosh(), at(4, 'brand'), 0.5)
put(riser(0.9), at(5, 'revenue', -0.9), 0.35); put(ding(1318), at(5, 'revenue', 1.0), 0.45); put(ding(1760), at(5, 'profit', 1.0), 0.5)
put(hit(), at(6, 'cut'), 0.6); put(down(), at(6, 'margins'), 0.5); put(pop(500), at(6, 'CEO'), 0.5)
put(hit(), at(7, 'big names', 0.5), 0.6); put(riser(1.0), at(7, 'growth', -1.0), 0.5); put(boom(), at(7, 'growth'), 0.8)
put(glitch(), at(7, 'Kotak'), 0.6); put(hit(), at(7, 'Kotak'), 0.5)
put(pop(1100), at(8, 'Save'), 0.6); put(whoosh(), at(8, 'Send', -0.2), 0.6)
for s in F.SWITCH: put(whoosh(0.3), s - 0.1, 0.45)
mix = vo + mus + fx[:N] * 0.8
mix = np.tanh(mix * 1.15) / np.tanh(1.15)
w = wave.open(f'{F.SH}mix.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes()); w.close(); print('mix ok', round(F.DUR, 1))
