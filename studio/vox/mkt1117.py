"""Timing for the 17 Nov 2026 market reel (motion/mkt1117)."""
import json
SH = '/home/claude/reels/studio/mkt1117/'
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
        fell0=at(0, 'But more'), who=at(0, 'So who'),
        nifty=at(1, 'Nifty closed'), sensex=at(1, 'Sensex'),
        fell=at(2, 'two thousand one hundred'), rose=at(2, 'only two'), small=at(2, 'Smallcaps'),
        twist=at(3, 'twist'), never=at(3, 'never'),
        bank=at(4, 'Bank Nifty'), record=at(4, 'record'), psu=at(4, 'PSU'), axis=at(4, 'Axis'),
        crude=at(5, 'Crude'), fii=at(5, 'foreign'), wall=at(5, 'Wall Street'),
        it=at(6, 'IT stocks'), hcl=at(6, 'HCL'), infy=at(6, 'Infosys'),
        ans=at(7, 'A few'), index=at(7, 'The index'),
        save=at(8, 'Save'), follow=at(8, 'follow'), green=at(8, 'Because'))
