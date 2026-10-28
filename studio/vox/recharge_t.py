"""Timing for the recharge reel (HyperFrames build). Shared by audio + HTML generator."""
import os, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
SH = ROOT + 'recharge/'
SCRIPT = json.load(open(SH + 'script.json'))
DURS = json.load(open(SH + 'vo/durs.json'))
LEAD, TAIL = 0.15, 0.35
STARTS, VO = [], []
_t = 0.0
for i, d in enumerate(DURS):
    STARTS.append(_t); VO.append(_t + (0.1 if i == 0 else LEAD)); _t = VO[-1] + d + TAIL
DUR = round(_t + 1.8, 2)
B = STARTS[1:]
PH = {0: ['fifteen percent', 'Do this'], 1: ['How many', 'Twelve', 'Wrong'],
      2: ['runs out', 'Three sixty five', 'is thirteen', 'You pay'],
      3: ['Jio listed', 'twenty one percent', 'Brokers', 'twelve to fifteen'],
      4: ['how much', "Let's do"],
      5: ['one eighty nine', 'is two thousand', 'After a fifteen', "That's three", 'A family'],
      6: ['before the hike', 'locked', 'annual plan', 'After a fifteen', "That's five"],
      7: ['really use', 'no hike date'], 8: ['Save this', 'send it', 'Follow']}


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return round(VO[i] + DURS[i] * (k / len(s)) + off, 3)


def times():
    T = {f'{i}:{p}': at(i, p) for i, ps in PH.items() for p in ps}
    T.update({f's{i}': round(s, 3) for i, s in enumerate(STARTS)}); T['dur'] = DUR
    return T


def slam_times(): return []
