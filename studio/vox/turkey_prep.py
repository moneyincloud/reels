"""Prep data.js for the Animal Friday 'Turkey Problem' chalkboard reel (Yes Bank)."""
import json, subprocess, numpy as np, sys, os
sys.path.insert(0, '.')
import listx as LX
SH = '../turkey/'
SCRIPT = json.load(open(SH + 'script.json')); SPK = ['H'] * len(SCRIPT)
DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO, DUR = LX.timing(SCRIPT, DURS, lead=0.15, tail=0.3)
def at(i, ph, off=0.0):
    s = SCRIPT[i]; k = s.find(ph); assert k >= 0, (i, ph)
    return VO[i] + DURS[i] * k / len(s) + off
P = lambda tag, k=0: LX.POSE[tag][k]
CUES = sorted([
 (0, P('stop')), (at(0, 'then lost', -0.1), P('shock', 1)), (VO[1], P('calm')), (at(1, 'Humans', -0.1), P('smug')),
 (VO[2], P('confident')), (at(2, 'Its confidence', -0.1), P('proud')), (VO[3], P('nervous')), (VO[4], P('point')),
 (VO[5], P('bull')), (at(5, 'Its value', -0.1), P('rich_phone')), (VO[6], P('hodl')), (VO[7], P('think')),
 (at(7, 'Stay till', -0.1), P('secret')), (VO[8], P('alert')), (at(8, 'The stock', -0.1), P('gap_down')),
 (VO[9], P('panic_sell')), (at(9, 'The stock', -0.1), P('liquidated')), (VO[10], P('bagholder')), (VO[11], P('facepalm')),
 (at(11, 'Here are', -0.1), P('idea')), (VO[12], P('inspect')), (at(12, 'Two.', -0.1), P('analysis')), (at(12, 'Three.', -0.1), P('alert')),
 (VO[13], P('zen_guru')), (at(13, 'Save', -0.1), P('point')), (at(13, 'Or are', -0.1), P('laugh'))])
used = sorted({p for _, p in CUES})
os.makedirs(SH + 'web/poses', exist_ok=True)
for p in used:
    LX.pose_img(p, 330).save(SH + f'web/poses/p{p:02d}.png')
PG = [
 (0, "Don't", "*Don't be the turkey.*"), (0, 'It was', 'Fed for *1,000 days,* then lost *everything.*'),
 (1, 'Every day', 'Every day, a farmer *feeds the turkey.*'), (1, 'And every', 'Every day it grows *more sure:*'), (1, 'Humans', '"Humans *love me.*"'),
 (2, 'Day one hundred', 'Day *100.* Day *500.* Day *1,000.*'), (2, 'Its confidence', 'Confidence at an *all-time high.*'),
 (3, 'Then comes', 'Then comes *the day before the festival.*'), (3, 'The day', 'The day it *never saw coming.*'),
 (4, 'Investors', 'Investors do *the same* with stocks.'), (4, 'Let me', 'Here\'s *a real one.*'),
 (5, 'Yes Bank', '*Yes Bank.* For years, it kept *rising.*'), (5, 'and in August', 'Aug 2018: about *₹400* a share.'), (5, 'Its value', 'Value crossed *₹1 lakh crore.*'),
 (6, 'Every month', 'Every rising month felt *safer.*'), (6, 'Just like', 'Just like *the turkey.*'),
 (7, 'So what', 'So what was the *turkey\'s mistake?*'), (7, 'Stay till', 'Stay: *3 warning signs* you can check in *any stock.*'),
 (8, 'September', '*Sep 2018:* RBI cut the *CEO\'s term short.*'), (8, 'The stock', 'The stock *nearly halved* in a month.'),
 (9, 'March', '*Mar 2020:* RBI took over the *board.*'), (9, 'and capped', 'Withdrawals capped at *₹50,000.*'), (9, 'The stock', 'Stock crashed *~85% in a day.*'),
 (10, 'Today', 'Today, *6 years later:* about *₹16.*'), (10, 'Still', 'Still *~96% below* the peak.'),
 (11, "The turkey's", "The turkey's mistake?"), (11, 'Thinking', 'Thinking a long *calm streak* means *safety.*'), (11, 'Here are', 'The *3 warning signs:*'),
 (12, 'One.', '*1.* Loans growing *too fast* to *stressed* companies.'), (12, 'Two.', '*2.* Promoter *pledged* his *entire stake.*'), (12, 'Three.', '*3.* The *regulator* raised a *red flag.*'),
 (13, 'A long', 'A rising chart is *not proof of safety.*'), (13, 'Save', '*Save this.* Follow *@moneyincloud*'), (13, 'Or are', 'Or are you *still the turkey?*'),
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
  'turkey': (0, 'turkey'), 'lost': (0, 'then lost'), 'feed': (1, 'feeds'), 'love': (1, 'Humans'),
  'd100': (2, 'Day one hundred'), 'd500': (2, 'Day five'), 'd1000': (2, 'Day one thousand'), 'conf': (2, 'all-time'),
  'fest': (3, 'festival'), 'never': (3, 'never'), 'inv': (4, 'Investors'), 'real': (4, 'real one'),
  'yes': (5, 'Yes Bank'), 'aug': (5, 'August'), 'r400': (5, 'four hundred'), 'lakh': (5, 'one lakh'),
  'safer': (6, 'safer'), 'just': (6, 'Just like'), 'mist': (7, 'mistake'), 'three': (7, 'three warning'),
  'sep': (8, 'September'), 'ceo': (8, 'CEO'), 'halved': (8, 'halved'),
  'mar': (9, 'March'), 'board': (9, 'board'), 'cap': (9, 'fifty thousand'), 'crash': (9, 'crashed'),
  'today': (10, 'Today'), 'r16': (10, 'sixteen'), 'p96': (10, 'ninety six'),
  'calm': (11, 'calm streak'), 'signs': (11, 'three warning'),
  'w1': (12, 'One.'), 'w2': (12, 'Two.'), 'w3': (12, 'Three.'),
  'proof': (13, 'not proof'), 'save': (13, 'Save'), 'follow': (13, 'follow'), 'still': (13, 'Or are')}.items()}
open(SH + 'web/data.js', 'w').write('window.D=' + json.dumps({'dur': DUR, 'starts': STARTS, 'vo': VO, 'durs': DURS, 'spk': SPK,
  'cues': CUES, 'pages': PAGES, 'amp': amp.round(3).tolist(), 'marks': marks}) + ';')
json.dump({'dur': DUR, 'starts': STARTS, 'vo': VO, 'marks': marks, 'spk': SPK}, open(SH + 'web/data.json', 'w'))
print('DUR', round(DUR, 2), 'answer at', round(VO[11] / DUR, 2), [round(x, 1) for x in STARTS])
