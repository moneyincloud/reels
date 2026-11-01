"""Prepare data.json (timing, words, cues, amplitude) + pose PNGs for the CSS/canvas midcap6 reel."""
import json, subprocess, numpy as np, sys
sys.path.insert(0, '.')
import listx as LX
SH = '../midcap6/'
SCRIPT = json.load(open(SH + 'script.json')); DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO, DUR = LX.timing(SCRIPT, DURS)
WORDS = LX.word_times(SCRIPT, DURS, VO)
def at(i, ph, off=0.0):
    s = SCRIPT[i]; k = s.find(ph); assert k >= 0, ph
    return VO[i] + DURS[i] * k / len(s) + off
P = lambda tag, k=0: LX.POSE[tag][k]
CUES = sorted([
 (0, P('stop')), (at(0, 'three numbers', -0.2), P('idea')),
 (VO[1], P('analysis')), (at(1, 'Most mid caps', -0.1), P('facepalm')), (at(1, 'These six', -0.1), P('celebrate', 1)),
 (VO[2], P('calm')), (at(2, 'Promoters own', -0.1), P('confident')),
 (VO[3], P('think')), (at(3, 'Indian funds', -0.1), P('whale')),
 (VO[4], P('algo')), (at(4, 'four percent', -0.2), P('wholesome_win')),
 (VO[5], P('laugh')), (at(5, 'The catch', -0.1), P('bored')),
 (VO[6], P('idea')), (at(6, 'Profit grew', -0.1), P('bull')), (at(6, 'government', -0.1), P('proud')),
 (VO[7], P('calm', 1)), (at(7, 'Indian funds', -0.1), P('proud', 1)),
 (VO[8], P('scam')), (at(8, 'twenty four', -0.2), P('math')),
 (VO[9], P('point')), (at(9, 'send', -0.1), P('wave'))])
used = sorted({p for _, p in CUES})
for p in used:
    LX.pose_img(p, 460).save(SH + f'web/poses/p{p:02d}.png')
# amplitude per frame (voice only)
SR = 24000; FPS = 30; N = int(DUR * SR); vo = np.zeros(N)
for i, t in enumerate(VO):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{SH}vo/{i}.wav', '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(float) / 32768; a = int(t * SR); vo[a:a + len(x)] += x[:N - a]
hop = SR // FPS; amp = []
for f in range(int(DUR * FPS) + 1):
    seg = vo[f * hop:(f + 1) * hop]; amp.append(float(np.sqrt((seg ** 2).mean())) if len(seg) else 0.0)
amp = np.array(amp); amp = np.clip(amp / (np.percentile(amp, 97) + 1e-9), 0, 1)
amp = np.convolve(amp, [0.25, 0.5, 0.25], 'same')
key = {}
for i in range(len(SCRIPT)):
    key[i] = {}
marks = {k: at(*v) for k, v in {
  'test1': (1, 'Return on'), 'test2': (1, 'Promoters'), 'test3': (1, 'low debt'), 'fail': (1, 'Most mid caps'), 'pass': (1, 'These six'),
  'ab_roe': (2, 'Return on'), 'ab_pro': (2, 'Promoters'),
  'na_roe': (3, 'Return on'), 'na_dii': (3, 'Indian funds'),
  'of_roe': (4, 'Thirty three'), 'of_debt': (4, 'almost no'), 'of_div': (4, 'four percent'),
  'co_roe': (5, 'Return on'), 'co_catch': (5, 'The catch'),
  'ma_prof': (6, 'Profit grew'), 'ma_gov': (6, 'government'),
  'cr_chn': (7, 'from Chennai'), 'cr_dii': (7, 'Indian funds'),
  'pe': (8, 'All six'), 'cta_num': (9, 'Comment'), 'cta_save': (9, 'Save'), 'cta_send': (9, 'send')}.items()}
json.dump({'dur': DUR, 'starts': STARTS, 'vo': VO, 'durs': DURS, 'words': WORDS, 'cues': CUES, 'amp': amp.round(3).tolist(), 'marks': marks},
          open(SH + 'web/data.json', 'w'))
print('DUR', round(DUR, 2), 'poses', used)
