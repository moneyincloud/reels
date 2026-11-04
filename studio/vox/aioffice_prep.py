"""Prep data.js for the light-theme two-character 'loss math' reel (CSS/canvas)."""
import json, subprocess, numpy as np, sys
sys.path.insert(0, '.')
import listx as LX
SH = '../aioffice/'
SCRIPT = json.load(open(SH + 'script.json')); SPK = ['H'] * len(SCRIPT)
DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO, DUR = LX.timing(SCRIPT, DURS, lead=0.15, tail=0.25)
def at(i, ph, off=0.0):
    s = SCRIPT[i]; k = s.find(ph); assert k >= 0, ph
    return VO[i] + DURS[i] * k / len(s) + off
P = lambda tag, k=0: LX.POSE[tag][k]
CUES = sorted([
 (0, P('wave')), (at(0, 'Meet', -0.1), P('point')), (VO[1], P('analysis')), (VO[2], P('alert')),
 (VO[3], P('think')), (VO[4], P('typing')), (VO[5], P('math')), (VO[6], P('inspect')), (VO[7], P('algo')),
 (VO[8], P('stress')), (at(8, 'Every bug', -0.1), P('confident')), (VO[9], P('stop')), (VO[10], P('moon_rocket')),
 (VO[11], P('celebrate')), (VO[12], P('point')), (at(12, 'Type', -0.1), P('wave'))])
used = sorted({p for _, p in CUES})
import os; os.makedirs(SH + 'web/poses', exist_ok=True)
for p in used:
    LX.pose_img(p, 330).save(SH + f'web/poses/p{p:02d}.png')
# caption pages: (line, start phrase, display text with *accent* words)
PG = [
 (0, 'What', 'What if your whole team was *AI?*'), (0, 'Meet', 'Meet *Marina Code Labs,* Chennai.'),
 (1, 'Eight', '*8 desks,* each with *one job.*'), (1, 'CEO', 'CEO, PM, architect, designer,'), (1, 'developers', 'developers, tester, security, release.'),
 (2, 'Monday', '*Monday, 9 AM.* A client walks in.'), (2, 'Kanchi', '*Kanchi Silks* wants an *online saree store.*'),
 (3, 'Step one', '*Step 1:* the *CEO* runs office hours.'), (3, 'Who', 'Who buys? Why online? *Smallest launch?*'),
 (4, 'Step two', '*Step 2:* the *PM* writes the spec.'), (4, 'Catalogue', 'Catalogue, cart, *UPI,* order tracking.'), (4, 'Loyalty', 'Loyalty points → *version 2.*'),
 (5, 'Step three', '*Step 3:* the *architect* plans the system.'), (5, 'A React', 'React app, API, *Postgres,* payment gateway.'),
 (6, 'Step four', '*Step 4:* the *designer* reviews every screen.'),
 (7, 'Step five', '*Step 5:* the *developers* build it.'), (7, 'Frontend', 'Frontend, backend, DevOps,'), (7, 'and every', 'and every change gets a *code review.*'),
 (8, 'Step six', '*Step 6:* the *tester* orders again and again.'), (8, 'Empty', 'Empty carts, slow networks, *failed payments.*'), (8, 'Every bug', 'Every bug: *logged and fixed.*'),
 (9, 'Step seven', '*Step 7:* *security* checks payments and data.'),
 (10, 'Step eight', '*Step 8:* the *release manager* ships it live.'),
 (11, 'Friday', '*Friday:* team *retro.*'), (11, 'What went', 'What went well? What to *improve?*'),
 (12, 'One idea', '*1 idea, 8 desks, a live store.*'), (12, 'You are', 'You are the *client.*'), (12, 'Type', '*Type the command.* Your AI office gets to work.'),
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
  'meet': (0, 'Meet'), 'walk': (2, 'A client'), 'kanchi': (2, 'Kanchi'),
  'q1': (3, 'Who'), 'q2': (3, 'Why online'), 'q3': (3, 'What is'),
  'f1': (4, 'Catalogue'), 'loy': (4, 'Loyalty'), 'a1': (5, 'React'), 'a2': (5, 'API'), 'a3': (5, 'Postgres'), 'a4': (5, 'payment'),
  'scr': (6, 'every screen'), 'fe': (7, 'Frontend'), 'rev': (7, 'code review'),
  'b1': (8, 'Empty'), 'b2': (8, 'slow'), 'b3': (8, 'failed'), 'fix': (8, 'Every bug'),
  'pay': (9, 'payment'), 'data': (9, 'customer'), 'test': (10, 'final tests'), 'live': (10, 'ships'),
  'well': (11, 'What went'), 'imp': (11, 'improve'), 'you': (12, 'You are'), 'cmd': (12, 'Type')}.items()}
open(SH + 'web/data.js', 'w').write('window.D=' + json.dumps({'dur': DUR, 'starts': STARTS, 'vo': VO, 'durs': DURS, 'spk': SPK,
  'cues': CUES, 'pages': PAGES, 'amp': amp.round(3).tolist(), 'marks': marks}) + ';')
json.dump({'dur': DUR, 'starts': STARTS, 'vo': VO, 'marks': marks, 'spk': SPK}, open(SH + 'web/data.json', 'w'))
print('DUR', round(DUR, 2), 'poses', used)
