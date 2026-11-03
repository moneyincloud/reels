"""Prep data.js for the light-theme two-character 'loss math' reel (CSS/canvas)."""
import json, subprocess, numpy as np, sys
sys.path.insert(0, '.')
import listx as LX
SH = '../lossmath/'
SCRIPT = json.load(open(SH + 'script.json')); SPK = json.load(open(SH + 'speakers.json'))
DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO, DUR = LX.timing(SCRIPT, DURS, lead=0.12, tail=0.18)
def at(i, ph, off=0.0):
    s = SCRIPT[i]; k = s.find(ph); assert k >= 0, ph
    return VO[i] + DURS[i] * k / len(s) + off
P = lambda tag, k=0: LX.POSE[tag][k]
CUES = sorted([
 (0, P('alert')), (at(0, 'A fifty', -0.1), P('point')),
 (VO[1], P('smug')), (VO[2], P('stop')), (VO[3], P('idea')),
 (VO[4], P('math')), (at(4, 'falls', -0.1), P('gap_down')),
 (VO[5], P('analysis')), (at(5, 'So you reach', -0.1), P('shrug')),
 (VO[6], P('think')), (VO[7], P('eureka_up')), (VO[8], P('smug', 2)),
 (VO[9], P('math')), (at(9, 'Down eighty', -0.1), P('facepalm')),
 (VO[10], P('think')), (VO[11], P('bear')), (at(11, 'To get back', -0.1), P('analysis')), (at(11, 'It took', -0.1), P('sleepless')),
 (VO[12], P('calm')), (VO[13], P('zen_guru')), (at(13, 'A small loss', -0.1), P('point')), (at(13, 'A big one', -0.1), P('stress')),
 (VO[14], P('proud')), (VO[15], P('point')), (at(15, 'And send', -0.1), P('wave'))])
used = sorted({p for _, p in CUES})
import os; os.makedirs(SH + 'web/poses', exist_ok=True)
for p in used:
    LX.pose_img(p, 340).save(SH + f'web/poses/p{p:02d}.png')
# caption pages: (line, start phrase, display text with *accent* words)
PG = [
 (0, 'Lost', 'Lost *50%* on your stock?'), (0, 'A fifty', 'A *50% rise* is the *wrong fix.*'),
 (1, 'Wait', 'Wait, what? My stock fell *50.*'), (1, 'If it', 'If it goes up *50,* I\'m *back,* right?'),
 (2, 'Nope', 'Nope. You\'d still be *down 25%.*'),
 (3, 'How', '*How?*'),
 (4, 'Take', 'Take *₹100.* It falls *50%.*'), (4, "You're", 'You\'re left with *₹50.*'),
 (5, 'Now', 'Now it *rises 50%.*'), (5, 'But', 'But 50% of 50 is just *₹25.*'), (5, 'So you', 'So you reach *₹75.* Not *₹100.*'),
 (6, 'Then', 'Then what does it *really need?*'),
 (7, 'A hundred', '*100%.* It has to *double,*'), (7, 'just', 'just to *get back.*'),
 (8, 'Double', '*Double?* Only for *big falls?*'),
 (9, 'It gets', 'It gets *worse* as the fall gets *bigger.*'), (9, 'Down ten', 'Down 10, needs *11.* Down 20, needs *25.*'),
 (9, 'Down thirty', 'Down 30, needs *43.*'), (9, 'Down eighty', 'Down 80? *400%.*'),
 (10, 'Has', 'Has this happened to the *whole market?*'),
 (11, 'In March', 'March 2020: Nifty fell *about 40%,*'), (11, 'from', 'from *12,430* to *7,511.*'),
 (11, 'To get', 'To get back, it needed *65%.*'), (11, 'It took', 'It took until *November.*'),
 (12, 'So how', 'So how do I *protect myself?*'),
 (13, 'Keep', '*Keep losses small.*'), (13, 'Decide', 'Decide your *exit* before you buy,'),
 (13, 'and don', 'and don\'t put *too much in one stock.*'), (13, 'A small', 'A *small loss* is easy to recover.'),
 (13, 'A big', 'A *big one* can take *years.*'),
 (14, 'Got', 'Got it. *Small losses,* not big ones.'),
 (15, 'Save', '*Save this* before your next trade.'), (15, 'And send', 'Send it to the friend who says...'),
 (15, 'my stock', '"my stock fell *50%*"'),
]
PAGES = [(round(at(i, ph, -0.08), 3), txt) for i, ph, txt in PG]
SR = 24000; FPS = 30; N = int(DUR * SR); vo = np.zeros(N)
for i, t in enumerate(VO):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{SH}vo/{i}.wav', '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(float) / 32768; a = int(t * SR); vo[a:a + len(x)] += x[:N - a]
hop = SR // FPS; amp = []
for f in range(int(DUR * FPS) + 1):
    seg = vo[f * hop:(f + 1) * hop]; amp.append(float(np.sqrt((seg ** 2).mean())) if len(seg) else 0.0)
amp = np.array(amp); amp = np.clip(amp / (np.percentile(amp, 97) + 1e-9), 0, 1)
amp = np.convolve(amp, [0.25, 0.5, 0.25], 'same')
marks = {k: round(at(*v), 3) for k, v in {
  'm50a': (0, 'fifty percent'), 'm50b': (0, 'A fifty'), 'still': (2, 'still'),
  'r100': (4, 'hundred'), 'fall': (4, 'falls'), 'left': (4, 'left'), 'rise': (5, 'rises'), 'r25': (5, 'twenty five'),
  'r75': (5, 'seventy five'), 'not100': (5, 'Not a'), 'dbl': (7, 'double'), 'dbl0': (7, 'A hundred'),
  't10': (9, 'Down ten'), 't20': (9, 'Down twenty'), 't30': (9, 'Down thirty'), 't80': (9, 'Down eighty'), 't80b': (9, 'Four hundred'),
  'n0': (11, 'In March'), 'nfell': (11, 'Nifty fell'), 'nfrom': (11, 'from'), 'nback': (11, 'To get back'), 'nnov': (11, 'It took'),
  'k1': (13, 'Keep'), 'k2': (13, 'Decide'), 'k3': (13, "and don't"), 'ks': (13, 'A small'), 'kb': (13, 'A big'),
  'got': (14, 'Got'), 'save': (15, 'Save'), 'send': (15, 'And send')}.items()}
open(SH + 'web/data.js', 'w').write('window.D=' + json.dumps({'dur': DUR, 'starts': STARTS, 'vo': VO, 'durs': DURS, 'spk': SPK,
  'cues': CUES, 'pages': PAGES, 'amp': amp.round(3).tolist(), 'marks': marks}) + ';')
json.dump({'dur': DUR, 'starts': STARTS, 'vo': VO, 'marks': marks, 'spk': SPK}, open(SH + 'web/data.json', 'w'))
print('DUR', round(DUR, 2), 'poses', used)
