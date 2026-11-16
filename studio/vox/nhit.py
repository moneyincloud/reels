"""Timing for the NHIT ₹1 lakh reel (motion/nhit)."""
import json
SH = '/home/claude/reels/studio/nhit/'
SCRIPT = [l['text'] for l in json.load(open(SH + 'lines.json'))]
DURS = json.load(open(SH + 'vo/durs.json'))
STARTS, VO = [], []; t = 0.0
for i, d in enumerate(DURS):
    STARTS.append(t); VO.append(t + (0.15 if i == 0 else 0.3)); t = VO[-1] + d + 0.25
DUR = t + 1.3
def at(i, phrase, off=0.0):
    s = SCRIPT[i]; k = s.find(phrase); assert k >= 0, phrase
    return VO[i] + DURS[i] * (k / len(s)) + off
def timing():
    return dict(VO=VO, DURS=DURS, STARTS=STARTS, DUR=DUR,
        toll=at(0, 'toll roads'), catch0=at(0, 'But there'), owns=at(1, 'owns'), truck=at(1, 'Every time'), flows=at(1, 'cash flows'),
        units=at(2, 'five hundred'), jun=at(3, 'three rupees'), r1880=at(3, 'one thousand'), sep=at(4, 'two rupees'), r1495=at(4, 'About one thousand'),
        changes=at(4, 'So the payout'), tax=at(5, 'taxed'), catch=at(6, 'Now the catch'), priv=at(6, 'privately'), lot=at(6, 'twenty five thousand'),
        l42=at(6, 'forty two'), cant=at(7, 'cannot'), pub=at(7, 'Public'), one=at(7, 'one unit'), comment=at(8, 'Comment'), save=at(8, 'save'))
