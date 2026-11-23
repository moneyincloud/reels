"""Phrase-level TTS with word timings for word-by-word captions (toon style).
usage: python3 vo_words.py <dir>
<dir>/script.json = [ {"scene": "tnagar", "who": "narrator", "phrases": [ {"say": "...", "cap": "..."} , ...]}, ... ]
  say = what the voice reads; cap = caption text (defaults to say). Mark keywords in cap with *word*.
<dir>/voices.json = {"narrator": ["am_michael", 1.1]} (optional)
Writes <dir>/vo/<scene>_<k>.wav per scene, <dir>/vo/words.json:
  [{"dur": d, "phrases": [{"t0","t1","cap","words":[{"w","t","key"}]}]}]  (times relative to scene audio start)"""
import os, sys, json, re, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro
D = os.path.dirname(os.path.abspath(__file__)) + '/'
CAST = {'narrator': ('am_michael', 1.1)}
d = sys.argv[1]; os.makedirs(d + '/vo', exist_ok=True)
if os.path.exists(d + '/voices.json'):
    CAST.update({k: tuple(v) for k, v in json.load(open(d + '/voices.json')).items()})
k = Kokoro(D + 'kokoro-v1.0.onnx', D + 'voices-v1.0.bin')
S = json.load(open(d + '/script.json'))
SR = 24000


def syl(w):
    w = w.lower().strip('*.,!?:;"\'')
    if re.fullmatch(r'[₹\d,.%]+', w):  # numbers are long when spoken
        return 2 + len(re.sub(r'\D', '', w)) * 1.2
    if len(w) <= 1:
        return 1
    return max(1, len(re.findall(r'[aeiouy]+', w)) - (1 if w.endswith('e') and len(w) > 3 else 0))


out = []
for si, sc in enumerate(S):
    v, sp = CAST[sc.get('who', 'narrator')]
    audio, ph = [], []
    t = 0.0
    for p in sc['phrases']:
        a, sr = k.create(p['say'], voice=v, speed=sp, lang='en-us')
        nz = np.where(np.abs(a) > 0.012)[0]
        a = a[max(0, nz[0] - 240):nz[-1] + 600]
        dur = len(a) / sr
        cap = p.get('cap', p['say'])
        toks = cap.split()
        wts = [syl(x) for x in toks]
        tot = sum(wts); acc = 0; words = []
        for x, wt in zip(toks, wts):
            words.append({'w': x.replace('*', ''), 'key': '*' in x,'t': round(t + 0.04 + dur * 0.92 * acc / tot, 3)})
            acc += wt
        ph.append({'t0': round(t, 3), 't1': round(t + dur, 3), 'cap': cap, 'words': words})
        audio.append(a)
        gap = 0.22 if p['say'].rstrip()[-1:] in '.?!' else 0.08
        audio.append(np.zeros(int(gap * sr)))
        t += dur + gap
    full = np.concatenate(audio)
    sf.write(f'{d}/vo/{si}.wav', full, SR)
    out.append({'scene': sc['scene'], 'dur': round(len(full) / SR, 3), 'phrases': ph})
json.dump(out, open(d + '/vo/words.json', 'w'), indent=1)
print([o['dur'] for o in out], round(sum(o['dur'] for o in out), 1))
