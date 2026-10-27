"""Ingest the owner's voice recordings: python3 ingest_vo.py <slug> file1 file2 ... (in line order).
Converts to 24 kHz mono wav, trims silence, normalises loudness, writes <slug>/vo/<i>.wav + durs.json."""
import sys, os, json, subprocess, numpy as np, soundfile as sf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
slug, files = sys.argv[1], sys.argv[2:]
d = ROOT + slug + '/vo/'; os.makedirs(d, exist_ok=True); durs = []
for i, f in enumerate(files):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-af', 'highpass=f=80,afftdn=nf=-25,loudnorm=I=-16:TP=-1.5', '-ac', '1', '-ar', '24000', '-f', 's16le', '-'], capture_output=True).stdout
    a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    nz = np.where(np.abs(a) > 0.02)[0]; a = a[max(0, nz[0] - 2400): nz[-1] + 4800]
    sf.write(f'{d}{i}.wav', a, 24000); durs.append(len(a) / 24000)
json.dump(durs, open(d + 'durs.json', 'w')); print([round(x, 2) for x in durs], round(sum(durs), 1))
