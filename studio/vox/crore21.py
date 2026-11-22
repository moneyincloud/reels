"""Timing for the semiconductor penny stocks HyperFrames reel."""
import os, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
SH = ROOT + 'crore21/'
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


def timing():
    T = {k: at(i, p) for k, (i, p) in KEYS.items()}
    T.update(DUR=round(DUR, 3), STARTS=[round(x, 3) for x in STARTS], VO=[round(x, 3) for x in VO], DURS=DURS)
    return T
KEYS = {
 'one_lakh': (0, 'one lakh'), 'pick': (0, 'one stock'), 'crores': (0, 'crores'), 'lost': (0, 'lost'), 'ten': (0, 'ten real'),
 'hit': (1, 'Hitachi'), 'servo': (1, 'Servotech'), 'gev': (1, 'GE Vernova'), 'axis': (1, 'AXISCADES'),
 'kesar': (2, 'Kesar'), 'bse': (2, 'BSE'), 'spec': (2, 'Spectrum'), 'close': (2, 'So close'),
 'n2': (3, 'Number two'), 'biscuit': (3, 'biscuit'), 'paise': (3, 'fourteen'), 'today2': (3, 'Today'),
 'wait': (4, 'But wait'), 'april': (4, 'In April'), 'gone': (4, 'Half'),
 'n1': (5, 'Number one'), 'p245': (5, 'Two rupees'), 'p365': (5, 'Today'), 'became': (5, 'One lakh became'),
 'twist': (6, 'twist'), 'paytm': (6, 'Pay T M'), 'worth': (6, 'worth about'),
 'two': (7, 'only two'), 'crashed': (7, 'crashed'), 'winners': (7, 'winners'),
 'bet': (8, "Don't bet"), 'spread': (8, 'Spread'), 'check': (8, 'check the business'), 'patient': (8, 'patient'), 'save': (8, 'Save'), 'follow': (8, 'follow'),
}

def timing():
    T = {k: at(i, p) for k, (i, p) in KEYS.items()}
    T.update(DUR=round(DUR, 3), STARTS=[round(x, 3) for x in STARTS], VO=[round(x, 3) for x in VO], DURS=DURS)
    return T
