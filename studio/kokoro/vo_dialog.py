"""Two-voice dialogue TTS. usage: python3 vo_dialog.py <dir> <voiceH> <speedH> <voiceF> <speedF>
<dir>/script.json = list of lines, <dir>/speakers.json = list of 'H'/'F' per line."""
import os as _os; _D = _os.path.dirname(_os.path.abspath(__file__)) + '/'
import sys, json, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro
d = sys.argv[1]; V = {'H': (sys.argv[2], float(sys.argv[3])), 'F': (sys.argv[4], float(sys.argv[5]))}
k = Kokoro(_D + "kokoro-v1.0.onnx", _D + "voices-v1.0.bin")
L = json.load(open(d + '/script.json')); S = json.load(open(d + '/speakers.json')); durs = []
for i, (s, sp) in enumerate(zip(L, S)):
    a, sr = k.create(s, voice=V[sp][0], speed=V[sp][1], lang='en-us')
    nz = np.where(np.abs(a) > 0.01)[0]; a = a[max(0, nz[0] - 1200): nz[-1] + 2400]
    sf.write(f'{d}/vo/{i}.wav', a, sr); durs.append(len(a) / sr)
json.dump(durs, open(d + '/vo/durs.json', 'w')); print([round(x, 2) for x in durs], round(sum(durs), 1))
