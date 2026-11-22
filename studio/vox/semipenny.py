"""Timing for the semiconductor penny stocks HyperFrames reel."""
import os, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
SH = ROOT + 'semipenny/'
SCRIPT = json.load(open(SH + 'script.json'))
DURS = json.load(open(SH + 'vo/durs.json'))
LEAD, TAIL = 0.15, 0.35
STARTS, VO = [], []
_t = 0.0
for i, d in enumerate(DURS):
    STARTS.append(_t); VO.append(_t + (0.1 if i == 0 else LEAD)); _t = VO[-1] + d + TAIL
DUR = _t + 1.6

def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return round(VO[i] + DURS[i] * (k / len(s)) + off, 3)

KEYS = {
 'multi': (0, 'multibagger'), 'traps': (0, 'traps'),
 'spel': (1, 'SPEL'), 'chennai': (1, 'Chennai'), 'packs': (1, 'packs'), 'first': (1, "India's first"), 'perfect': (1, 'perfect'),
 'catch': (2, 'catch'), 'shut': (2, 'shut'), 'sales': (2, 'sales'), 'loss': (2, 'loss'),
 'values': (3, 'values'), 'f51': (3, 'fifty one'),
 'mic': (4, 'M I C'), 'led': (4, 'LED'), 'weak': (4, 'weak'),
 'ae': (5, 'Artificial'), 'f79': (5, 'seventy nine'), 'surv': (5, 'surveillance'), 'flag': (5, 'red flag'),
 'real': (6, 'real chip'), 'rir': (6, 'R I R'), 'odisha': (6, 'Odisha'), 'p618': (6, 'six hundred'),
 'mos': (7, 'MosChip'), 'both': (7, 'Both are real'), 'f30': (7, 'thirty'),
 'c1': (8, 'factory running'), 'c2': (8, 'making a profit'), 'c3': (8, 'surveillance list'),
 'cheap': (9, 'cheap'), 'save': (9, 'Save'), 'follow': (9, 'follow'),
}

def timing():
    T = {k: at(i, p) for k, (i, p) in KEYS.items()}
    T.update(DUR=round(DUR, 3), STARTS=[round(x, 3) for x in STARTS], VO=[round(x, 3) for x in VO], DURS=DURS)
    return T
