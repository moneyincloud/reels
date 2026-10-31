"""devops: timing only. The visuals live in canvas/devops.js; this module feeds devops_audio.py."""
import os as _os; ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))) + '/'
import json
import listx as LX

SH = ROOT + 'devops/'
SCRIPT = json.load(open(SH + 'script.json'))
DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO, DUR = LX.timing(SCRIPT, DURS)
WORDS = LX.word_times(SCRIPT, DURS, VO)
SWITCH = [STARTS[k] for k in (3, 5, 7, 9, 11)]
FILL = [VO[1 + 2 * k] + 0.5 for k in range(5)]


def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase)
    assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off
