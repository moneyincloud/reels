"""Prep data.js for the King's Treasury Ep 3 'One Ship, All the Gold' storybook reel."""
import json, subprocess, numpy as np, sys, os
sys.path.insert(0, '.')
import listx as LX
SH = '../kt3/'
SCRIPT = json.load(open(SH + 'script.json')); SPK = ['H'] * len(SCRIPT)
DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO, DUR = LX.timing(SCRIPT, DURS, lead=0.15, tail=0.3)
def at(i, ph, off=0.0):
    s = SCRIPT[i]; k = s.find(ph); assert k >= 0, (i, ph)
    return VO[i] + DURS[i] * k / len(s) + off
P = lambda tag, k=0: LX.POSE[tag][k]
CUES = sorted([
 (0, P('yolo')), (at(0, "One storm", -0.1), P('shock')), (VO[1], P('wave')), (at(1, 'Today', -0.1), P('point')),
 (VO[2], P('idea')), (at(2, 'brave', -0.1), P('secret')), (VO[3], P('fomo')), (at(3, 'come back', -0.1), P('moon_point')),
 (VO[4], P('think')), (at(4, 'Mathi smiled', -0.1), P('zen_guru')), (VO[5], P('nervous')), (at(5, 'Stay', -0.1), P('alert')),
 (VO[6], P('cry')), (at(6, 'Arun lost', -0.1), P('wholesome_win')), (VO[7], P('analysis')), (at(7, 'Down', -0.1), P('panic_sell')),
 (VO[8], P('calm')), (VO[9], P('point')), (at(9, 'never sail', -0.1), P('scam')), (VO[10], P('wave')),
 (at(10, 'One ship', -0.1), P('laugh'))])
used = sorted({p for _, p in CUES})
os.makedirs(SH + 'web/poses', exist_ok=True)
for p in used:
    LX.pose_img(p, 330).save(SH + f'web/poses/p{p:02d}.png')
PG = [
 (0, 'General', '*All the gold.* One ship.'), (1, 'Welcome', "*King's Treasury,* episode 3."), (1, 'Today', "Enter: *the king's 3 friends*"),
 (2, 'Minister', '*Mathi* · the scroll'), (2, 'Merchant', '*Selvan* · the sweet shop'), (2, 'And brave', '*Veeran* · the hot tip'),
 (3, 'The fastest', 'A *hot tip*'), (3, "I'll load", '*1,000 gold* on one ship'),
 (4, 'The king', 'Ask the *minister*'), (4, 'Mathi smiled', '*10 ships,* 100 gold each'),
 (5, 'Then', 'The *storm*'), (5, 'Stay', 'This really *happened*'),
 (6, "Veeran's", 'Veeran: *14 gold* left'), (6, 'Arun lost', 'Arun: *9 ships home*'),
 (7, 'In August', 'Yes Bank: *₹404*'), (7, 'By March', '→ *₹5.55*'), (7, 'Down', '*−99%*'),
 (8, 'In the same', 'Nifty 50: *about −6%*'),
 (9, 'Three rules', '*3 rules* of the ships'),
 (10, 'Save', '*Save* · *send* · *follow*'), (10, 'One ship', 'One ship. *One storm.*'),
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
  'gen': (0, 'General'), 'storm0': (0, 'One storm'), 'ninety': (0, 'ninety'), 'ep': (1, 'Welcome'), 'arun': (1, 'Last time'), 'friends': (1, 'Today'),
  'mathi': (2, 'Minister'), 'selvan': (2, 'Merchant'), 'veeran': (2, 'And brave'), 'tip': (2, 'hot tip'),
  'fast': (3, 'The fastest'), 'load': (3, "I'll load"), 'rich': (3, 'come back'),
  'vel': (4, 'Prince Vel'), 'king': (4, 'The king'), 'split': (4, 'Mathi smiled'), 'hund': (4, 'A hundred'),
  'storm': (5, 'Then the storm'), 'stay': (5, 'Stay'), 'sank': (6, "Veeran's ship"), 'fourteen': (6, 'only fourteen'), 'nine': (6, 'Arun lost'),
  'aug': (7, 'In August'), 'p404': (7, 'four hundred'), 'mar': (7, 'By March'), 'p555': (7, 'five rupees'), 'down': (7, 'Down'),
  'nifty': (8, 'Nifty'), 'basket': (8, 'fifty big'), 'six': (8, 'about six'),
  'r1': (9, 'Never load'), 'r2': (9, 'Spread'), 'r3': (9, 'never sail'), 'save': (10, 'Save'), 'send': (10, 'send it'), 'follow': (10, 'follow'), 'rem': (10, 'One ship')}.items()}
open(SH + 'web/data.js', 'w').write('window.D=' + json.dumps({'dur': DUR, 'starts': STARTS, 'vo': VO, 'durs': DURS, 'spk': SPK,
  'cues': CUES, 'pages': PAGES, 'amp': amp.round(3).tolist(), 'marks': marks}) + ';')
json.dump({'dur': DUR, 'starts': STARTS, 'vo': VO, 'marks': marks, 'spk': SPK}, open(SH + 'web/data.json', 'w'))
print('DUR', round(DUR, 2), 'answer at', round(VO[8] / DUR, 2), [round(x, 1) for x in STARTS])
