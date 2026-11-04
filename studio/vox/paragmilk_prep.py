"""Prep data.js for the light-theme two-character 'loss math' reel (CSS/canvas)."""
import json, subprocess, numpy as np, sys
sys.path.insert(0, '.')
import listx as LX
SH = '../paragmilk/'
SCRIPT = json.load(open(SH + 'script.json')); SPK = ['H'] * len(SCRIPT)
DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO, DUR = LX.timing(SCRIPT, DURS, lead=0.15, tail=0.25)
def at(i, ph, off=0.0):
    s = SCRIPT[i]; k = s.find(ph); assert k >= 0, ph
    return VO[i] + DURS[i] * k / len(s) + off
P = lambda tag, k=0: LX.POSE[tag][k]
CUES = sorted([
 (0, P('shock', 2)), (at(0, 'still jumped', -0.1), P('gap_up')),
 (VO[1], P('wave')), (VO[2], P('gap_down')), (at(2, 'raw material', -0.1), P('stress')),
 (VO[3], P('think')), (VO[4], P('bull')), (at(4, 'Volumes', -0.1), P('confident')),
 (VO[5], P('secret')), (at(5, 'Remove it', -0.1), P('eureka_up')),
 (VO[6], P('idea')), (at(6, 'paneer', -0.1), P('analysis')),
 (VO[7], P('jackpot')), (VO[8], P('zen_guru')), (VO[9], P('stop')), (at(9, 'fifty two', -0.1), P('inspect')),
 (VO[10], P('point')), (at(10, 'follow', -0.1), P('wave'))])
used = sorted({p for _, p in CUES})
import os; os.makedirs(SH + 'web/poses', exist_ok=True)
for p in used:
    LX.pose_img(p, 330).save(SH + f'web/poses/p{p:02d}.png')
# caption pages: (line, start phrase, display text with *accent* words)
PG = [
 (0, 'Your', "Your stock's *profit fell?*"), (0, "This one's", "This one's profit fell *8%,*"), (0, 'and the stock', 'and the stock still *jumped 17%* today.'),
 (1, "It's", "It's *Parag Milk Foods,*"), (1, 'the company', 'maker of *Gowardhan ghee, Go cheese, Avvatar.*'),
 (2, 'On the', 'Q2 profit fell to *₹42 crore*'), (2, 'from', 'from *₹45.6 crore* a year ago,'), (2, 'as raw', 'as *raw material costs* went up.'),
 (3, 'So why', 'So why did buyers *rush in?*'), (3, 'Three', '*3 reasons.*'),
 (4, 'One', '*1.* Record revenue: *₹1,241 crore,* up *23%.*'), (4, 'Volumes', 'Volumes grew *12%.*'),
 (5, 'Two', "*2.* Last year's profit had a *one-off boost.*"), (5, 'Remove', 'Remove it: profit grew *42%.*'), (5, 'Margins', 'Margins improved to *8.1%.*'),
 (6, 'Three', '*3.* New-age brands grew *71%.*'), (6, 'And paneer', 'Paneer capacity: *20 → 80 tonnes/day*'), (6, 'by June', 'by *June 2027.*'),
 (7, 'The stock', 'Closed at *₹292,* up *17%.*'),
 (8, 'So the', 'The lesson?'), (8, 'The market', 'The market reads *what\'s behind the profit,*'), (8, 'not just', 'not just the *headline number.*'),
 (9, 'But careful', '*Careful.* One good day ≠ *a trend.*'), (9, "It's still", 'Still *~23% below* its 52-week high of *₹377.*'),
 (10, 'Save', '*Save this* before the next results day,'), (10, 'and follow', 'and follow *@moneyincloud.*'),
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
  'pf': (0, 'profit fell eight'), 'jump': (0, 'still jumped'),
  'brands': (1, 'Gowardhan'), 'go': (1, 'Go cheese'), 'av': (1, 'Avvatar'),
  'p42': (2, 'forty two'), 'p45': (2, 'from forty'), 'raw': (2, 'raw material'),
  'three': (3, 'Three reasons'), 'rev': (4, 'Revenue'), 'vol': (4, 'Volumes'),
  'oneoff': (5, 'one off'), 'adj': (5, 'Remove it'), 'mar': (5, 'Margins'),
  'new': (6, 'new age'), 'pan': (6, 'paneer'), 'june': (6, 'June'),
  'close': (7, 'closed'), 'lesson': (8, 'The market'), 'care': (9, 'One good day'), 'high': (9, 'fifty two'),
  'save': (10, 'Save'), 'follow': (10, 'follow')}.items()}
open(SH + 'web/data.js', 'w').write('window.D=' + json.dumps({'dur': DUR, 'starts': STARTS, 'vo': VO, 'durs': DURS, 'spk': SPK,
  'cues': CUES, 'pages': PAGES, 'amp': amp.round(3).tolist(), 'marks': marks}) + ';')
json.dump({'dur': DUR, 'starts': STARTS, 'vo': VO, 'marks': marks, 'spk': SPK}, open(SH + 'web/data.json', 'w'))
print('DUR', round(DUR, 2), 'poses', used)
