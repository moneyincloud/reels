"""Timing for the 18 Nov 2026 IPO listing report reel (motion/ipo1118)."""
import json
SH = '/home/claude/reels/studio/ipo1118/'
SCRIPT = json.load(open(SH + 'script.json'))
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
        lost=at(0, 'This IPO'),
        four=at(1, 'Four'),
        myth=at(2, 'Most people'), board=at(2, 'So here'), iss=at(2, 'Issue price'), lday=at(2, 'listing day'), tday=at(2, 'and today'),
        wait=at(3, 'But wait'), least=at(3, 'least'), sixty=at(3, 'sixty four'),
        bls=at(4, 'B L S'), b241=at(4, 'Two hundred'), b79=at(4, 'Up seventy'), b84=at(4, 'eighty four'),
        sfc=at(5, 'S F C'), s9=at(5, 'Only nine'), suc=at(5, 'upper circuit'), s31=at(5, 'Now up'),
        bc=at(6, 'Bombay'), bc64=at(6, 'Sixty four'), bc16=at(6, 'up sixteen'), lc=at(6, 'Then three'), bc17=at(6, 'Now just'),
        mk=at(6, 'And M K'), mk5=at(6, 'Five times'), mkflat=at(6, 'flat'), mk16=at(6, 'now up sixteen'),
        ans=at(7, "So here's"), subs=at(7, 'Subscription'), chap=at(7, 'Listing day'),
        send=at(8, 'Send'), save=at(8, 'Save'), follow=at(8, 'follow'), edu=at(8, 'Education'), loop=at(8, 'Sixty four'))
