"""Timing for the Kalyan Jewellers reel (motion/kalyan)."""
import json
SH = '/home/claude/reels/studio/kalyan/'
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
        profit=at(0,'four hundred'), months=at(0,'in just'), kerala=at(0,'And it all'),
        first=at(1,'opened'), thr=at(1,'in Thrishoor'), y93=at(1,'in nineteen'),
        five=at(2,'over five'), k365=at(2,'Three hundred'), c138=at(2,'one hundred thirty'),
        most=at(3,"But"), notjust=at(3,"Kalyan isn't"),
        me=at(4,'It has'), us=at(4,'Plus two'), uk=at(4,'and two in the UK'), total=at(4,"That's"),
        money=at(5,'Now'), rev=at(5,'revenue jumped'), prof=at(5,'Profit rose'), land=at(5,'though'),
        india=at(6,'Four hundred'), mideast=at(6,'and just'),
        trick=at(7,'The growth'), fr=at(7,'Franchise'), part=at(7,'Partners'), p59=at(7,'About fifty'), p84=at(7,'and eighty'),
        q=at(8,'So,'), cmt=at(8,'Tell me'), fol=at(8,'follow'))
