"""Ingest the owner's voice recordings: python3 ingest_vo.py <slug> file1 file2 ... (in line order).
One file only: it is one take of the whole script, split at the longest pauses into one clip per script line.
Converts to 24 kHz mono wav, trims silence, normalises loudness, writes <slug>/vo/<i>.wav + durs.json."""
import sys, os, json, subprocess, numpy as np, soundfile as sf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
SR = 24000
slug, files = sys.argv[1], sys.argv[2:]
d = ROOT + slug + '/vo/'; os.makedirs(d, exist_ok=True)


def load(f):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-af', 'highpass=f=80,afftdn=nf=-25,loudnorm=I=-16:TP=-1.5', '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def trim(a):
    nz = np.where(np.abs(a) > 0.02)[0]; return a[max(0, nz[0] - 2400): nz[-1] + 4800]


def split(a, n):
    """cut one take into n clips at the n-1 longest pauses (20 ms frames below the speech level)"""
    fr = SR // 50; e = np.array([np.sqrt(np.mean(a[k:k + fr] ** 2)) for k in range(0, len(a) - fr, fr)])
    quiet = e < max(0.01, np.percentile(e, 30) * 1.5)
    runs, k = [], 0
    while k < len(quiet):
        if quiet[k]:
            j = k
            while j < len(quiet) and quiet[j]: j += 1
            if k > 0 and j < len(quiet): runs.append((j - k, (k + j) // 2 * fr))
            k = j
        else: k += 1
    cuts = sorted(c for _, c in sorted(runs, reverse=True)[:n - 1])
    if len(cuts) < n - 1: sys.exit(f'found only {len(cuts) + 1} parts, script has {n} lines: leave a 1-2 s pause between lines')
    return [a[s:e] for s, e in zip([0] + cuts, cuts + [len(a)])]


if len(files) == 1:
    n = len(json.load(open(ROOT + slug + '/script.json')))
    clips = split(trim(load(files[0])), n)
else:
    clips = [load(f) for f in files]
durs = []
for i, a in enumerate(clips):
    a = trim(a); sf.write(f'{d}{i}.wav', a, SR); durs.append(len(a) / SR)
json.dump(durs, open(d + 'durs.json', 'w')); print([round(x, 2) for x in durs], round(sum(durs), 1))
