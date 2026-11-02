"""Prepare data.json (timing, words, cues, amplitude) + pose PNGs for the CSS/canvas midcap6 reel."""
import json, subprocess, numpy as np, sys
sys.path.insert(0, '.')
import listx as LX
SH = '../muhurat/'
SCRIPT = json.load(open(SH + 'script.json')); DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO, DUR = LX.timing(SCRIPT, DURS)
WORDS = LX.word_times(SCRIPT, DURS, VO)
def at(i, ph, off=0.0):
    s = SCRIPT[i]; k = s.find(ph); assert k >= 0, ph
    return VO[i] + DURS[i] * k / len(s) + off
P = lambda tag, k=0: LX.POSE[tag][k]
CUES = sorted([
 (0, P('alert')), (at(0, 'these timings', -0.2), P('idea')),
 (VO[1], P('sleepless')), (at(1, 'seventy minutes', -0.1), P('shock', 3)), (at(1, 'Pre-open', -0.1), P('alert')),
 (VO[2], P('calm')), (at(2, 'Samvat', -0.1), P('wholesome_win')), (at(2, 'B S E', -0.1), P('inspect')),
 (VO[3], P('typing')), (at(3, 'This year', -0.1), P('eureka_up')),
 (VO[4], P('think')),
 (VO[5], P('analysis')), (at(5, 'biggest jump', -0.1), P('celebrate')), (at(5, 'But nineteen', -0.1), P('shrug')),
 (VO[6], P('bull')), (at(6, 'best year', -0.1), P('jackpot')), (at(6, 'two red', -0.1), P('calm', 1)),
 (VO[7], P('zen_guru')), (at(7, 'many families', -0.1), P('wholesome_win')),
 (VO[8], P('point')), (at(8, 'happy Diwali', -0.2), P('celebrate', 1))])
used = sorted({p for _, p in CUES})
for p in used:
    LX.pose_img(p, 460).save(SH + f'web/poses/p{p:02d}.png')
# amplitude per frame (voice only)
SR = 24000; FPS = 30; N = int(DUR * SR); vo = np.zeros(N)
for i, t in enumerate(VO):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{SH}vo/{i}.wav', '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(float) / 32768; a = int(t * SR); vo[a:a + len(x)] += x[:N - a]
hop = SR // FPS; amp = []
for f in range(int(DUR * FPS) + 1):
    seg = vo[f * hop:(f + 1) * hop]; amp.append(float(np.sqrt((seg ** 2).mean())) if len(seg) else 0.0)
amp = np.array(amp); amp = np.clip(amp / (np.percentile(amp, 97) + 1e-9), 0, 1)
amp = np.convolve(amp, [0.25, 0.5, 0.25], 'same')
key = {}
for i in range(len(SCRIPT)):
    key[i] = {}
marks = {k: at(*v) for k, v in {
  'date': (1, 'November'), 'seventy': (1, 'seventy minutes'), 'time': (1, 'Two twenty'), 'pre': (1, 'Pre-open'),
  'samvat': (2, 'Samvat'), 'bse': (2, 'B S E'), 'nse': (2, 'N S E'),
  'real': (3, 'real trades'), 'settle': (3, 'settles'), 'cas': (3, 'closing auction'),
  'rose': (5, 'Nifty rose'), 'big08': (5, 'biggest jump'), 'small': (5, 'But nineteen'),
  'full': (6, 'Nifty ended'), 'avg': (6, 'averaging'), 'best': (6, 'best year'), 'red': (6, 'two red'),
  'trad': (7, 'tradition'), 'token': (7, 'token quantity'),
  'save': (8, 'Save'), 'send': (8, 'Send'), 'diwali': (8, 'happy Diwali')}.items()}
bursts = sorted([0.15] + [STARTS[k] + 0.05 for k in range(1, len(STARTS))] + [marks['big08'], marks['best'], marks['diwali'], marks['diwali'] + 0.5, marks['diwali'] + 1.0])
json.dump({'dur': DUR, 'starts': STARTS, 'vo': VO, 'durs': DURS, 'words': WORDS, 'cues': CUES, 'amp': amp.round(3).tolist(), 'marks': marks, 'bursts': bursts},
          open(SH + 'web/data.json', 'w'))
print('DUR', round(DUR, 2), 'poses', used)
