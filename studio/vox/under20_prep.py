"""Prep data.js for the light-theme two-character 'loss math' reel (CSS/canvas)."""
import json, subprocess, numpy as np, sys
sys.path.insert(0, '.')
import listx as LX
SH = '../under20/'
SCRIPT = json.load(open(SH + 'script.json')); SPK = json.load(open(SH + 'speakers.json'))
DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO, DUR = LX.timing(SCRIPT, DURS, lead=0.12, tail=0.18)
def at(i, ph, off=0.0):
    s = SCRIPT[i]; k = s.find(ph); assert k >= 0, ph
    return VO[i] + DURS[i] * k / len(s) + off
P = lambda tag, k=0: LX.POSE[tag][k]
CUES = sorted([
 (0, P('alert')), (VO[1], P('analysis')), (VO[2], P('celebrate')), (VO[3], P('inspect')),
 (VO[4], P('wholesome_win')), (at(4, 'ROE', -0.1), P('confident')),
 (VO[5], P('watcher')), (VO[6], P('jackpot')), (VO[7], P('shock', 3)), (at(7, 'barred', -0.1), P('scam')),
 (VO[8], P('math')), (at(8, 'but it now', -0.1), P('nervous')),
 (VO[9], P('bull')), (at(9, 'yet the', -0.1), P('gap_down')),
 (VO[10], P('typing')), (at(10, 'but promoter', -0.1), P('think')),
 (VO[11], P('inspect')), (at(11, 'but the last', -0.1), P('shrug')),
 (VO[12], P('facepalm')), (VO[13], P('think')), (at(13, 'Sixteen', -0.1), P('shock')), (at(13, 'Only these', -0.1), P('idea')),
 (VO[14], P('zen_guru')), (VO[15], P('point')), (at(15, 'send it', -0.1), P('wave'))])
used = sorted({p for _, p in CUES})
import os; os.makedirs(SH + 'web/poses', exist_ok=True)
for p in used:
    LX.pose_img(p, 340).save(SH + f'web/poses/p{p:02d}.png')
# caption pages: (line, start phrase, display text with *accent* words)
PG = [
 (0, "Don't", "Don't buy these *₹20 stocks*"), (0, 'before', 'before you see this *one flag.*'),
 (1, 'Twenty', '*22 stocks under ₹20* passed this screen.'), (1, 'Ten year', '10-yr *ROE, ROCE, sales growth* all above *10%.*'),
 (2, 'Sounds', 'Sounds *strong!* Which ones?'),
 (3, "Here's", "Here's the *full list.*"), (3, "Let's", "Let's check the *6 biggest.*"),
 (4, 'Number', '*#1 Syncom Formulations*'), (4, 'Generic', '*Generic medicines,* 15+ countries.'),
 (4, 'ROE', 'ROE *17%,* almost *no debt,*'), (4, 'and promoters', 'promoters own *51%.*'),
 (5, 'Two', '*#2 Brightcom Group*'), (5, 'Digital', 'Digital *ad tech.*'), (5, 'P E', 'P/E just *1.6.*'),
 (6, 'Super', '*Super cheap!*'),
 (7, 'But in', 'But in 2025, *SEBI* found profits'), (7, 'inflated', '*inflated by ₹1,280 crore,*'), (7, 'and barred', 'and *barred 2 promoters* for 5 years.'),
 (8, 'Three', '*#3 A B Infrabuild*'), (8, 'It builds', '*Roads, railways* and *bridges.*'), (8, 'Profit', 'Profit grew *66% a year,*'), (8, 'but it now', 'but it now *waits longer* to get paid.'),
 (9, 'Four', '*#4 R M Drip & Sprinklers*'), (9, 'Drip irrigation', '*Drip irrigation* for farmers.'), (9, 'ROE', 'ROE *37%,* yet the stock is'), (9, 'seventy', '*77% below its high.*'),
 (10, 'Five', '*#5 Kellton Tech*'), (10, 'A I', '*AI, cloud* and *SAP* services.'), (10, 'P E', 'P/E *6.5,* but promoter holding'), (10, 'fell', 'fell *16 points* in 3 years.'),
 (11, 'Six', '*#6 Avonmore Capital*'), (11, 'Lending', '*Lending* and *investments.*'), (11, 'Ten year', '10-yr ROE *passes,* but the last'), (11, 'three years average', '3 years average just *5%.*'),
 (12, 'So the', 'So the screen is *wrong?*'),
 (13, 'Not wrong', 'Not wrong. It only reads *past numbers.*'), (13, "And here's", "And here's *the flag.*"),
 (13, 'Sixteen', '*16 of 22* are under *exchange surveillance.*'), (13, 'Only these', 'Only *these 6* aren\'t.'),
 (14, 'So before', 'Before you buy, check *who owns it,*'), (14, 'how it trades', '*how it trades,* and if the *numbers are clean.*'),
 (15, 'Save', '*Save this list,* and send it to the friend'), (15, 'who buys', 'who buys *anything under ₹20.*'),
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
  'flag': (0, 'one flag'), 'scr': (1, 'Ten year'), 'roce': (1, 'ROCE'), 'sales': (1, 'sales'), 'all': (1, 'all above'),
  'list': (3, 'full list'), 'six': (3, 'six biggest'),
  's1pro': (4, 'ROE'), 's1fl': (4, 'promoters'),
  's2pe': (5, 'P E'), 'sebi': (7, 'SEBI'), 'infl': (7, 'inflated'), 'bar': (7, 'barred'),
  's3pro': (8, 'Profit'), 's3fl': (8, 'but it now'), 's4pro': (9, 'ROE'), 's4fl': (9, 'yet the'),
  's5pro': (10, 'P E'), 's5fl': (10, 'but promoter'), 's6pro': (11, 'Ten year'), 's6fl': (11, 'but the last'),
  'flag2': (13, "And here's"), 'sixteen': (13, 'Sixteen'), 'only6': (13, 'Only these'),
  'c1': (14, 'who owns'), 'c2': (14, 'how it trades'), 'c3': (14, 'numbers are clean'),
  'save': (15, 'Save'), 'send': (15, 'send it')}.items()}
open(SH + 'web/data.js', 'w').write('window.D=' + json.dumps({'dur': DUR, 'starts': STARTS, 'vo': VO, 'durs': DURS, 'spk': SPK,
  'cues': CUES, 'pages': PAGES, 'amp': amp.round(3).tolist(), 'marks': marks}) + ';')
json.dump({'dur': DUR, 'starts': STARTS, 'vo': VO, 'marks': marks, 'spk': SPK}, open(SH + 'web/data.json', 'w'))
print('DUR', round(DUR, 2), 'poses', used)
