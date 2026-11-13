"""Timing for the weekly movers leaderboard reels (HyperFrames build in motion/weekmov). Audio only."""
import json


def make(mode):
    SH = f'/home/claude/reels/studio/weekmov_{mode}/'
    L = json.load(open(SH + 'lines.json')); SCRIPT = [l['text'] for l in L]
    DURS = json.load(open(SH + 'vo/durs.json'))
    STARTS, VO = [], []; t = 0.0
    for i, d in enumerate(DURS):
        STARTS.append(t); VO.append(t + (0.15 if i == 0 else 0.25)); t = VO[-1] + d + 0.3
    DUR = t + 1.3

    def at(i, phrase, off=0.0):
        s = SCRIPT[i]; k = s.find(phrase)
        assert k >= 0, phrase
        return VO[i] + DURS[i] * (k / len(s)) + off
    return dict(SH=SH, SCRIPT=SCRIPT, DURS=DURS, STARTS=STARTS, VO=VO, DUR=DUR, B=STARTS[1:], at=at)
