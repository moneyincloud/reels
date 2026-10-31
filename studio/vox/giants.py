"""giants: timing for the 'big names fell, quiet stock grew' reel. Visuals: canvas/giants.js (reads giants/timing.json)."""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import json

SH = ROOT + 'giants/'
SCRIPT = json.load(open(SH + 'script.json'))
DURS = json.load(open(SH + 'vo/durs.json'))
TAIL = [0.3, 0.2, 0.75, 0.3, 0.3, 0.3, 0.55, 0.35, 0.2]   # pause after each line: long before the reveal and the lesson
STARTS, VO = [], []
_t = 0.0
for _i, _d in enumerate(DURS):
    STARTS.append(_t); VO.append(_t + (0.1 if _i == 0 else 0.15)); _t = VO[-1] + _d + TAIL[_i]
DUR = _t + 1.2
WORDS = []
for _i, _s in enumerate(SCRIPT):
    _pos = 0; _ws = []
    for _w in _s.split(' '):
        _k = _s.find(_w, _pos); _pos = _k + len(_w); _ws.append((_w, VO[_i] + DURS[_i] * _k / len(_s)))
    WORDS.append(_ws)
SWITCH = STARTS[1:]


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off


if __name__ == '__main__':
    json.dump({'starts': STARTS, 'vo': VO, 'dur': DUR}, open(SH + 'timing.json', 'w'))
    print('DUR', round(DUR, 2), [round(s, 2) for s in STARTS])
