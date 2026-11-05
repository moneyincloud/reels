"""Prep data.js for the Cummins India pixel-art reel (5 Nov 2026)."""
import json, subprocess, numpy as np, sys, os
sys.path.insert(0, '.')
import listx as LX
from PIL import Image
SH = '../cummins/'
SCRIPT = json.load(open(SH + 'script.json')); SPK = ['H'] * len(SCRIPT)
DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO, DUR = LX.timing(SCRIPT, DURS, lead=0.15, tail=0.3)
def at(i, ph, off=0.0):
    s = SCRIPT[i]; k = s.find(ph); assert k >= 0, (i, ph)
    return VO[i] + DURS[i] * k / len(s) + off
P = lambda tag, k=0: LX.POSE[tag][k]
CUES = sorted([
 (0, P('stop')), (at(0, 'yet this', -0.1), P('shock', 1)), (VO[1], P('gap_down')), (at(1, 'more than', -0.1), P('alert')),
 (VO[2], P('point')), (at(2, 'Engines', -0.1), P('confident')), (VO[3], P('think')), (at(3, 'Revenue', -0.1), P('bull')),
 (VO[4], P('wholesome_win')), (VO[5], P('nervous')), (at(5, 'Stay with', -0.1), P('secret')), (VO[6], P('math')),
 (at(6, 'Down twenty', -0.1), P('bear')), (VO[7], P('inspect')), (at(7, "It's something", -0.1), P('idea')),
 (VO[8], P('eureka_up')), (VO[9], P('analysis')), (at(9, 'This quarter', -0.1), P('sad')), (VO[10], P('stress')),
 (at(10, 'But what', -0.1), P('facepalm')), (VO[11], P('bagholder')), (VO[12], P('point')), (at(12, 'Ask', -0.1), P('idea')),
 (VO[13], P('wave')), (at(13, 'Because', -0.1), P('shrug'))])
used = sorted({p for _, p in CUES})
os.makedirs(SH + 'web/poses', exist_ok=True)
for p in used:  # pixelate the avatar to match the pixel-art style
    im = LX.pose_img(p, 330).convert('RGBA'); w, h = im.size; f = 5
    sm = im.resize((w // f, h // f), Image.NEAREST)
    a = np.array(sm); a[..., 3] = np.where(a[..., 3] > 110, 255, 0); sm = Image.fromarray(a)
    sm.resize((w // f * f, h // f * f), Image.NEAREST).save(SH + f'web/poses/p{p:02d}.png')
PG = [
 (0, 'Stop', '*Stop.* Sales grew,'), (0, 'yet this', 'yet this stock lost *₹18,000 crore* in one day.'),
 (1, 'This is', 'This is *Cummins India.*'), (1, 'Today', 'Today it crashed *14%,*'), (1, 'on more', 'on *10x+* its usual volume.'),
 (2, 'You may', 'You may not know the name,'), (2, "but you've", "but you've *seen its machines.*"), (2, 'The giant', 'Giant *generators* behind hospitals, malls, *data centres.*'), (2, 'Engines', 'Engines for *trucks, trains, mines.*'),
 (3, 'So what', 'So what *went wrong?*'), (3, 'Not sales', '*Not sales.* Revenue *+4%,*'), (3, 'to three', 'to *₹3,300 crore.*'),
 (4, 'Domestic', 'Domestic *grew.* Exports *grew.*'), (4, 'Data', 'Data centres *kept ordering.*'),
 (5, 'So why', 'So why did *₹18,000 crore* disappear?'), (5, 'Stay', 'Stay. *One word* decides most results days.'),
 (6, 'Analysts', 'Analysts expected *~₹625 crore* profit.'), (6, 'Cummins made', 'Cummins made *₹467 crore.*'), (6, 'Down', '*−27%* from last year.'),
 (7, 'Was it', 'A *one-off* charge? A *tax* hit?'), (7, 'No.', '*No.* You can check it yourself,'), (7, 'in thirty', 'in *30 seconds.*'),
 (8, 'The word', 'The word is *MARGIN.*'),
 (9, 'Last year', 'Last year, from every *₹100* of sales,'), (9, 'Cummins kept', 'it kept *~₹22* as operating profit.'), (9, 'This quarter', 'This quarter: only *₹15.*'),
 (10, 'Metal', '*Metal and freight* costs went up,'), (10, 'and the product', 'and the *product mix* changed.'), (10, 'Sales grew', 'Sales *grew.* What it kept *shrank.*'),
 (11, 'And the', 'The stock is now *a third below*'), (11, 'its May', 'its May high of *₹6,100.*'),
 (12, 'So on', 'On results day, don\'t just ask,'), (12, 'did sales', '*did sales grow?*'), (12, 'Ask', 'Ask: of every *₹100,* how much did they *keep?*'),
 (13, 'Save', '*Save this* for the next results day.'), (13, 'and follow', 'Follow *@moneyincloud.*'), (13, 'Because', 'Because sometimes *sales grow,*'), (13, 'and the stock', 'and the stock *still falls.*'),
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
  'sales': (0, 'Sales grew'), 'lost': (0, 'lost'), 'name': (1, 'Cummins'), 'crash': (1, 'crashed'), 'vol': (1, 'more than'),
  'gen': (2, 'giant generators'), 'hosp': (2, 'hospitals'), 'dc': (2, 'data centres'), 'eng': (2, 'Engines'), 'truck': (2, 'trucks'),
  'notsales': (3, 'Not sales'), 'rev': (3, 'Revenue'), 'r3300': (3, 'three thousand'),
  'dom': (4, 'Domestic'), 'exp': (4, 'Exports'), 'dco': (4, 'Data centres'),
  'why': (5, 'So why'), 'word': (5, 'one word'),
  'est': (6, 'Analysts'), 'made': (6, 'Cummins made'), 'down': (6, 'Down twenty'),
  'oneoff': (7, 'one-off'), 'tax': (7, 'tax hit'), 'no': (7, 'No.'), 'sec30': (7, 'thirty'),
  'margin': (8, 'margin'),
  'h100': (9, 'every hundred'), 'k22': (9, 'twenty two'), 'k15': (9, 'only fifteen'),
  'metal': (10, 'Metal'), 'mix': (10, 'product mix'), 'kept': (10, 'But what'),
  'third': (11, 'a third'), 'may': (11, 'May high'),
  'q1': (12, 'did sales'), 'q2': (12, 'Ask, out'), 'keep': (12, 'how much'),
  'save': (13, 'Save'), 'follow': (13, 'follow'), 'loop': (13, 'Because')}.items()}
WK = [4283.2,4333.8,4479.3,4468.9,4600.2,4410.4,4346.4,4482.1,4116.7,4062,3930.4,4020.9,4368.4,4412.4,4733.9,4898.3,4800.7,4649.7,4615.3,4631.5,4646.5,5138.7,5140.9,5232,5266.4,5401,5392,5353,5881,5784,5621.5,5865,5642,5478,5621.5,5448,5600.5,5519,5426,5400,5107.5,5193,5035,5070,5099.5,4945,4860,4830,4608,4344.2,4452.6,4058.9]
VOL = [631136,224821,429821,274337,301745,294916,484045,554541,218940,448464,579384,464796,252610,583979,772374,549721,698364,478748,393224,358865,5850005]  # 7 Oct - 4 Nov daily, then 5 Nov
open(SH + 'web/data.js', 'w').write('window.D=' + json.dumps({'dur': DUR, 'starts': STARTS, 'vo': VO, 'durs': DURS, 'spk': SPK,
  'cues': CUES, 'pages': PAGES, 'amp': amp.round(3).tolist(), 'marks': marks, 'wk': WK, 'vol': VOL}) + ';')
json.dump({'dur': DUR, 'starts': STARTS, 'vo': VO, 'marks': marks, 'spk': SPK}, open(SH + 'web/data.json', 'w'))
print('DUR', round(DUR, 2), 'poses', used, 'margin at', marks['margin'], round(marks['margin'] / DUR, 2))
