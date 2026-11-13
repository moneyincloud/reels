"""Timing module for the earntax doodle reel (HyperFrames build in motion/earntax). Audio only."""
import json
ROOT = '/home/claude/reels/studio/'
SH = ROOT + 'earntax/'
LINES = json.load(open(SH + 'lines.json'))
SCRIPT = [l['text'] for l in LINES]
DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO = [], []
_t = 0.0
for i, d in enumerate(DURS):
    STARTS.append(_t); VO.append(_t + (0.15 if i == 0 else 0.2)); _t = VO[-1] + d + 0.22
DUR = _t + 1.3
B = STARTS[1:]


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off
