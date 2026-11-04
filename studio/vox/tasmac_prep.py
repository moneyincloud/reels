"""Prep data.js for the light-theme two-character 'loss math' reel (CSS/canvas)."""
import json, subprocess, numpy as np, sys
sys.path.insert(0, '.')
import listx as LX
SH = '../tasmac/'
SCRIPT = json.load(open(SH + 'script.json')); SPK = ['H'] * len(SCRIPT)
DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO, DUR = LX.timing(SCRIPT, DURS, lead=0.15, tail=0.25)
def at(i, ph, off=0.0):
    s = SCRIPT[i]; k = s.find(ph); assert k >= 0, ph
    return VO[i] + DURS[i] * k / len(s) + off
P = lambda tag, k=0: LX.POSE[tag][k]
CUES = sorted([
 (0, P('alert')), (at(0, 'but staff', -0.1), P('money_rain')),
 (VO[1], P('shock', 2)), (at(1, 'Here', -0.1), P('point')),
 (VO[2], P('idea')), (at(2, 'Return', -0.1), P('wholesome_win')),
 (VO[3], P('inspect')), (at(3, 'cash', -0.1), P('stop')),
 (VO[4], P('stress', 1)), (VO[5], P('cross')), (at(5, 'Nearly', -0.1), P('market_closed')),
 (VO[6], P('alert')), (at(6, 'suspended', -0.1), P('shock', 1)),
 (VO[7], P('calm')), (VO[8], P('math')), (at(8, 'Twenty percent', -0.1), P('jackpot')),
 (VO[9], P('analysis')), (VO[10], P('rich_phone')),
 (VO[11], P('secret')), (at(11, 'Five days', -0.1), P('shock', 3)),
 (VO[12], P('confident')), (VO[13], P('point')), (at(13, 'share', -0.1), P('wave'))])
used = sorted({p for _, p in CUES})
import os; os.makedirs(SH + 'web/poses', exist_ok=True)
for p in used:
    LX.pose_img(p, 330).save(SH + f'web/poses/p{p:02d}.png')
# caption pages: (line, start phrase, display text with *accent* words)
PG = [
 (0, 'Strike', 'Strike shut your *TASMAC,*'), (0, 'but staff', 'but staff still get a *₹16,800 bonus.*'),
 (1, 'And', 'And *245* were *suspended.*'), (1, 'So,', 'So, is it a *strike reward?*'),
 (2, 'From', 'From *1 Nov,* every bottle carries *₹10 extra.*'), (2, 'Return', 'Return the empty, get *₹10 back.*'),
 (3, "It's", "It's a *Madras High Court* order."), (3, 'Staff scan', 'Staff *scan every bottle,* at sale and return.'), (3, 'And cash', 'Cash restricted *above ₹1,000.*'),
 (4, 'Workers', 'Workers said it\'s *too much.*'), (4, 'Extra', '*Extra workload,* not enough *scanners,*'), (4, 'no space', '*no space* for empties, *network failures.*'),
 (5, 'So on', 'So on 1 Nov, a *flash strike.*'), (5, 'Nearly', 'Nearly *1 in 10* of *4,048 shops* shut.'),
 (6, 'The government', 'The government *hit back.*'), (6, 'Two hundred', '*245 supervisors* suspended,'), (6, 'and over', 'and *1,700+ show-cause notices.*'),
 (7, 'By', 'By 3 Nov, *98%* of shops were *open again.*'),
 (8, 'Now', 'Now, *the bonus.*'), (8, 'For this', 'Salary capped at *₹7,000 a month.*'), (8, 'Twelve', '12 months = *₹84,000.*'), (8, 'Twenty percent', '20% = *₹16,800.*'),
 (9, 'Eight', '*8.33% bonus* + *11.67% ex gratia.*'), (9, 'Same', 'Same for *every category.*'),
 (10, 'Today', 'Today: *district managers* →'), (10, 'then', '*staff bank accounts.* No cash.'),
 (11, 'But', "But here's *the twist.*"), (11, 'On October', 'On *27 Oct,* CM Vijay announced'), (11, 'this twenty', 'this *20% Deepavali bonus*'), (11, 'Five days', '*5 days before* the strike.'),
 (12, 'TASMAC', 'TASMAC staff got *20% last year too.*'), (12, "So it's", "So it's *not a strike reward.*"), (12, 'And the', 'And the *bottle fight* isn\'t over.'),
 (13, 'Ten', '*₹10 bottle return.*'), (13, 'Smart', '*Smart idea,* or *extra burden?*'), (13, 'Comment', '*Comment below,* share with someone at TASMAC.'),
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
  'bonus': (0, 'but staff'), 'susp': (1, 'suspended'), 'reward': (1, 'strike reward'),
  'ten': (2, 'ten rupees extra'), 'ret': (2, 'Return'), 'back': (2, 'back'),
  'hc': (3, 'Madras'), 'scan': (3, 'scan'), 'cash': (3, 'cash'),
  'w1': (4, 'Extra'), 'w2': (4, 'not enough'), 'w3': (4, 'no space'), 'w4': (4, 'network'),
  'strike': (5, 'flash strike'), 'shut': (5, 'Nearly'),
  'hit': (6, 'hit back'), 'n245': (6, 'Two hundred'), 'n1700': (6, 'seventeen'),
  'open': (7, 'ninety eight'),
  'cap': (8, 'capped'), 'twelve': (8, 'Twelve'), 'pct': (8, 'Twenty percent'),
  'split': (9, 'Eight'), 'same': (9, 'Same'),
  'dm': (10, 'district'), 'bank': (10, 'bank'),
  'twist': (11, 'twist'), 'oct': (11, 'October'), 'five': (11, 'Five days'),
  'last': (12, 'last year'), 'notr': (12, 'not a strike'), 'fight': (12, 'bottle fight'),
  'poll': (13, 'Smart'), 'share': (13, 'share')}.items()}
open(SH + 'web/data.js', 'w').write('window.D=' + json.dumps({'dur': DUR, 'starts': STARTS, 'vo': VO, 'durs': DURS, 'spk': SPK,
  'cues': CUES, 'pages': PAGES, 'amp': amp.round(3).tolist(), 'marks': marks}) + ';')
json.dump({'dur': DUR, 'starts': STARTS, 'vo': VO, 'marks': marks, 'spk': SPK}, open(SH + 'web/data.json', 'w'))
print('DUR', round(DUR, 2), 'poses', used)
