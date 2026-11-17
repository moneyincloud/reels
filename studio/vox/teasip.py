"""Timing for the tea money -> SIP reel (motion/teasip)."""
import json
SH = '/home/claude/reels/studio/teasip/'
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
        trad=at(0, 'not even'), rs25=at(0, 'twenty five'), tea30=at(1, 'nineteen thirties'), cups=at(1, 'free cups'),
        kanji=at(2, 'neeraagaaram'), early=at(2, 'early'), swap=at(3, 'Put'), work=at(3, 'working days'),
        wk=at(4, 'one hundred'), mo=at(4, 'about five'), yr=at(4, 'around six'), inv=at(5, 'one lakh'),
        nifty=at(6, 'Nifty'), twelve=at(6, 'twelve'), l49=at(6, 'four point nine'), past=at(7, 'past'), fall=at(7, 'Markets fall'),
        comment=at(8, 'Comment'), save=at(8, 'save'))
