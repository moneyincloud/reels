"""Timing module for the penny15 doodle reel (HyperFrames build in motion/penny15). Audio only."""
import json
ROOT = '/home/claude/reels/studio/'
SH = ROOT + 'penny15/'
LINES = json.load(open(SH + 'lines.json'))
SCRIPT = [l['text'] for l in LINES]
DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO = [], []
_t = 0.0
for i, d in enumerate(DURS):
    STARTS.append(_t); VO.append(_t + (0.15 if i == 0 else 0.2)); _t = VO[-1] + d + 0.22
DUR = _t + 1.3
B = STARTS[1:]
STOCKS = ['Vodafone Idea', 'Yes Bank', 'Suzlon', 'UCO', 'Punjab and Sind', 'Central Bank', 'Indian Overseas Bank',
          'I. R. B.', 'Reliance Power', 'J. P. Power', 'Alok', 'Trident', 'H. C. C.', 'RattanIndia Power', 'G. T. L. Infra']


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


def stock_times():
    out = []
    for nm in STOCKS:
        li = 2 if nm in SCRIPT[2] and STOCKS.index(nm) < 7 else 3
        out.append(at(li, nm))
    return out


def slam_times():
    return [at(0, 'one point four', -0.2), at(4, 'twenty to', -0.2)]
