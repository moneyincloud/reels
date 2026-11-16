"""Timing for the intraday / swing / F&O explainer (motion/tradetypes)."""
import json
SH = '/home/claude/reels/studio/tradetypes/'
L = json.load(open(SH + 'lines.json')); SCRIPT = [l['text'] for l in L]
DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO = [], []; t = 0.0
for i, d in enumerate(DURS):
    STARTS.append(t); VO.append(t + (0.15 if i == 0 else 0.3)); t = VO[-1] + d + 0.25
DUR = t + 1.3
B = STARTS[1:]
def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase); assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off
def timing():
    return dict(VO=VO, DURS=DURS, STARTS=STARTS, DUR=DUR, SCRIPT=SCRIPT,
        open630=at(1, 'opened at'), high=at(1, 'six hundred and eighty nine'), close=at(2, 'By the closing'), c664=at(2, 'six hundred and sixty four'),
        sw592=at(3, 'From the Diwali'), sw711=at(3, 'seven hundred and eleven'), sw20=at(3, 'twenty percent'),
        night=at(4, 'You hold overnight'), o718=at(4, 'opened at'), d685=at(4, 'dropped'),
        fno=at(5, 'contracts'), lots=at(5, 'fixed lots'), lot65=at(5, 'sixty five units'), lakh=at(5, 'sixteen'),
        p179=at(6, 'one hundred and seventy nine'), r11=at(6, 'eleven thousand'), loss=at(6, 'the same loss'),
        sebi=at(7, 'SEBI'), nine=at(7, 'nine in ten'), comment=at(8, 'Comment'), save=at(8, 'save'))
