"""Timing for the FirstCry business reel (motion/firstcry)."""
import json
SH = '/home/claude/reels/studio/firstcry/'
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
        jump=at(0,'jumped'), vol=at(0,'on about'), ipo0=at(0,'Yet'), why=at(0,'Why'),
        meet=at(1,'Meet'), pune=at(1,'Pune'), y10=at(1,'Founded'), y24=at(1,'listed'),
        items=at(2,'Diapers'), skus=at(2,'About two'), brands=at(2,'from over'), stores=at(2,'online and'),
        label=at(3,'hiding'),
        own=at(4,'Its own'), marg=at(4,'When'),
        four=at(5,'It runs'), b1=at(5,'The India'), b2=at(5,'Online'), b3=at(5,'GlobalBees'), b4=at(5,'And Intellitots'),
        prof=at(6,'Now'), rev=at(6,'revenue grew'), loss=at(6,'And the loss'),
        exc=at(7,"That's"), indp=at(7,'The India'), still=at(7,'But the company'), ipo=at(7,'and the share'),
        q=at(8,'Would'), cmt=at(8,'Tell me'), fol=at(8,'follow'))
