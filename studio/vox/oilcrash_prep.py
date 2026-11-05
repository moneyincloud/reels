"""Prep data.js for the light-theme two-character 'loss math' reel (CSS/canvas)."""
import json, subprocess, numpy as np, sys
sys.path.insert(0, '.')
import listx as LX
SH = '../oilcrash/'
SCRIPT = json.load(open(SH + 'script.json')); SPK = ['H'] * len(SCRIPT)
DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO, DUR = LX.timing(SCRIPT, DURS, lead=0.15, tail=0.25)
def at(i, ph, off=0.0):
    s = SCRIPT[i]; k = s.find(ph); assert k >= 0, ph
    return VO[i] + DURS[i] * k / len(s) + off
P = lambda tag, k=0: LX.POSE[tag][k]
CUES = sorted([
 (0, P('shock', 1)), (at(0, 'Your stocks', -0.1), P('point')),
 (VO[1], P('gap_down')), (VO[2], P('think')), (at(2, 'markets now', -0.1), P('idea')),
 (VO[3], P('inspect')), (VO[4], P('bull')), (at(4, 'By eleven', -0.1), P('jackpot')),
 (VO[5], P('think')), (VO[6], P('moon_rocket')), (VO[7], P('wholesome_win')), (VO[8], P('bear')),
 (VO[9], P('stop')), (at(9, 'One headline', -0.1), P('nervous')), (VO[10], P('point')), (at(10, 'Follow', -0.1), P('wave'))])
used = sorted({p for _, p in CUES})
import os; os.makedirs(SH + 'web/poses', exist_ok=True)
for p in used:
    LX.pose_img(p, 330).save(SH + f'web/poses/p{p:02d}.png')
# caption pages: (line, start phrase, display text with *accent* words)
PG = [
 (0, 'Oil', '*Oil crashed 11%* today.'), (0, 'Your stocks', 'Your stocks could *win or lose.* Here\'s who.'),
 (1, 'This', 'Brent crude fell as low as *$93.50,*'), (1, 'from almost', 'from almost *$105* yesterday.'),
 (2, 'Why', 'Why? *US midterms* favoured the Democrats.'), (2, 'and markets', 'Markets hope the *West Asia conflict* ends sooner.'),
 (3, 'Why does', 'Why does *India* care?'), (3, 'Because', '*~9 of 10 barrels* we use are *imported.*'),
 (4, 'Cheaper', 'Cheaper oil = *smaller import bill.*'), (4, 'So Indian', 'So *Indian stocks rallied.*'), (4, 'By eleven', 'By 11:20, Sensex up *~1,500 points,*'), (4, 'and Nifty', 'Nifty *+1.8%.*'),
 (5, 'Now', 'Who *wins* when oil falls?'),
 (6, 'One', '*1. Airlines.* Fuel is a *huge cost.*'), (6, 'IndiGo', 'IndiGo *+5%.*'),
 (7, 'Two', '*2. Paint makers.* Raw materials from *crude.*'), (7, 'Asian', 'Asian Paints *+4%.*'),
 (8, 'And who', 'Who *loses?* Oil producers.'), (8, 'because', 'They earn *less per barrel.*'), (8, 'ONGC', 'ONGC *−2%.*'),
 (9, 'But careful', '*Careful.* Oil is still *+18% in 3 months.*'), (9, 'One headline', 'One headline can *flip it back.*'),
 (10, 'Save', '*Save this* for the next oil move.'), (10, 'Follow', 'Follow *@moneyincloud.*'),
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
  'crash': (0, 'crashed'), 'win': (0, 'win or lose'), 'low': (1, 'ninety three'), 'high': (1, 'one hundred five'),
  'mid': (2, 'midterm'), 'dem': (2, 'Democrats'), 'wa': (2, 'West Asia'), 'nine': (3, 'nine out'), 'imp': (3, 'imported'),
  'bill': (4, 'smaller'), 'sx': (4, 'Sensex'), 'nf': (4, 'Nifty'), 'who': (5, 'who wins'),
  'fuel': (6, 'Fuel'), 'indigo': (6, 'IndiGo'), 'raw': (7, 'raw'), 'asian': (7, 'Asian'),
  'prod': (8, 'Oil producers'), 'ongc': (8, 'ONGC'), 'up18': (9, 'eighteen'), 'flip': (9, 'One headline'),
  'save': (10, 'Save'), 'follow': (10, 'Follow')}.items()}
open(SH + 'web/data.js', 'w').write('window.D=' + json.dumps({'dur': DUR, 'starts': STARTS, 'vo': VO, 'durs': DURS, 'spk': SPK,
  'cues': CUES, 'pages': PAGES, 'amp': amp.round(3).tolist(), 'marks': marks}) + ';')
json.dump({'dur': DUR, 'starts': STARTS, 'vo': VO, 'marks': marks, 'spk': SPK}, open(SH + 'web/data.json', 'w'))
print('DUR', round(DUR, 2), 'poses', used)
