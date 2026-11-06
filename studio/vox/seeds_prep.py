"""Prep data.js for the King's Treasury Ep 2 'The Golden Seeds' flat-vector reel."""
import json, subprocess, numpy as np, sys, os
sys.path.insert(0, '.')
import listx as LX
SH = '../seeds/'
SCRIPT = json.load(open(SH + 'script.json')); SPK = ['H'] * len(SCRIPT)
DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO, DUR = LX.timing(SCRIPT, DURS, lead=0.15, tail=0.3)
def at(i, ph, off=0.0):
    s = SCRIPT[i]; k = s.find(ph); assert k >= 0, (i, ph)
    return VO[i] + DURS[i] * k / len(s) + off
P = lambda tag, k=0: LX.POSE[tag][k]
CUES = sorted([
 (0, P('stop')), (at(0, "This prince", -0.1), P('facepalm')), (VO[1], P('wave')), (at(1, 'both princes', -0.1), P('point')),
 (VO[2], P('wholesome_win')), (at(2, 'dividend', -0.1), P('idea')), (VO[3], P('laugh')), (VO[4], P('zen_guru')),
 (VO[5], P('smug')), (at(5, "What's the", -0.1), P('shrug')), (VO[6], P('secret')), (VO[7], P('math')),
 (at(7, 'The younger', -0.1), P('shock', 1)), (at(7, 'The seeds', -0.1), P('eureka_up')), (VO[8], P('confident')),
 (at(8, 'but about', -0.1), P('bull')), (VO[9], P('point')), (at(9, 'never dig', -0.1), P('alert')), (VO[10], P('wave')),
 (at(10, 'And remember', -0.1), P('laugh'))])
used = sorted({p for _, p in CUES})
os.makedirs(SH + 'web/poses', exist_ok=True)
for p in used:
    LX.pose_img(p, 330).save(SH + f'web/poses/p{p:02d}.png')
PG = [
 (0, 'Stop', '*Stop spending* your golden fruit.'), (0, 'This prince', "This prince's mistake cost him *a forest.*"),
 (1, 'Welcome', "*King's Treasury,* episode 2."), (1, 'In episode', 'Both princes bought a share of *the sweet shop,*'), (1, 'with a thousand', 'with *1,000 gold* each.'),
 (2, 'Every year', 'Every year, the shop paid them *golden fruit:*'), (2, 'A small', 'a small share of its *profit.*'), (2, 'In the market', 'In the market, we call it a *dividend.*'),
 (3, 'The elder', 'The elder prince *ate* his fruit.'), (3, 'Sweet', 'Sweet, easy, *gone.*'),
 (4, 'The younger', 'The younger prince *planted every seed* back.'), (4, 'Year after', 'Year after year.'),
 (5, 'After five', 'After *5 years,* the elder prince laughed:'), (5, 'My thousand', '"Mine is *1,690.* Yours is only *1,790.*'), (5, "What's the", "What's *the difference?*\""),
 (6, 'Stay', 'Stay: *year 15* is where the story *flips.*'),
 (7, 'By year', 'Year 20: elder prince *~8,200 gold.*'), (7, 'The younger', 'Younger prince: *over 10,400.*'), (7, 'The seeds', 'The seeds grew *their own seeds.*'),
 (8, "That's", "That's *compounding,* and it's real."), (8, 'Over twenty', 'Nifty 50, 20 years: *~11%* a year on price alone,'), (8, 'but about', 'but *~12.5%* with dividends *reinvested.*'),
 (9, 'Three rules', '*3 rules* of the golden seeds:'), (9, 'Reinvest', '*Reinvest.* Give it *time.*'), (9, 'And never', 'And never *dig up the roots.*'),
 (10, 'Save', '*Save this.* Follow *@moneyincloud* for episode 3.'), (10, 'And remember', 'And remember: *stop spending* your golden fruit.'),
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
  'stop': (0, 'Stop'), 'forest0': (0, 'forest'), 'ep': (1, 'Welcome'), 'shop': (1, 'sweet shop'), 'gold': (1, 'thousand gold'),
  'fruit': (2, 'golden fruit'), 'profit': (2, 'profit'), 'div': (2, 'dividend'), 'ate': (3, 'ate'), 'gone': (3, 'gone'),
  'plant': (4, 'planted'), 'yay': (4, 'Year after'), 'five': (5, 'five years'), 'mine': (5, 'sixteen'), 'yours': (5, 'seventeen'), 'diff': (5, "What's the"),
  'flip': (6, 'year fifteen'), 'y20': (7, 'By year'), 'e8200': (7, 'eight thousand'), 'y10400': (7, 'ten thousand'), 'seeds': (7, 'The seeds'),
  'comp': (8, 'compounding'), 'pr': (8, 'eleven percent'), 'tr': (8, 'twelve and a half'),
  'r1': (9, 'Reinvest'), 'r2': (9, 'Give it time'), 'r3': (9, 'never dig'), 'save': (10, 'Save'), 'follow': (10, 'follow'), 'rem': (10, 'And remember')}.items()}
open(SH + 'web/data.js', 'w').write('window.D=' + json.dumps({'dur': DUR, 'starts': STARTS, 'vo': VO, 'durs': DURS, 'spk': SPK,
  'cues': CUES, 'pages': PAGES, 'amp': amp.round(3).tolist(), 'marks': marks}) + ';')
json.dump({'dur': DUR, 'starts': STARTS, 'vo': VO, 'marks': marks, 'spk': SPK}, open(SH + 'web/data.json', 'w'))
print('DUR', round(DUR, 2), 'answer at', round(VO[8] / DUR, 2), [round(x, 1) for x in STARTS])
