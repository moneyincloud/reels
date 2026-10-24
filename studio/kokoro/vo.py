import os as _os; _D = _os.path.dirname(_os.path.abspath(__file__)) + '/'
import sys, json, soundfile as sf, numpy as np
from kokoro_onnx import Kokoro
d, voice = sys.argv[1], sys.argv[2]
k = Kokoro(_D + "kokoro-v1.0.onnx", _D + "voices-v1.0.bin")
L = json.load(open(d + '/script.json')); durs = []
for i, s in enumerate(L):
    a, sr = k.create(s, voice=voice, speed=float(sys.argv[3]) if len(sys.argv)>3 else 1.08, lang='en-us')
    # trim leading/trailing silence
    nz = np.where(np.abs(a) > 0.01)[0]; a = a[max(0, nz[0] - 1200): nz[-1] + 2400]
    sf.write(f'{d}/vo/{i}.wav', a, sr); durs.append(len(a) / sr)
json.dump(durs, open(d + '/vo/durs.json', 'w')); print(voice, [round(x, 2) for x in durs], round(sum(durs), 1))
