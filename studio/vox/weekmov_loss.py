from weekmov_common import make
import json
_F = make('loss')
SH = _F['SH']; SCRIPT = _F['SCRIPT']; DURS = _F['DURS']; STARTS = _F['STARTS']; VO = _F['VO']; DUR = _F['DUR']; B = _F['B']; at = _F['at']
D = json.load(open('/home/claude/reels/motion/weekmov/build/loss.json'))
SAY = json.load(open('/home/claude/reels/motion/weekmov/build/say.json')) if __import__('os').path.exists('/home/claude/reels/motion/weekmov/build/say.json') else {}


def hot():
    out = []
    for gi, g in enumerate(D['groups']):
        out.append([at(gi + 1, SAY.get(r['spk'], r['spk'])) for r in g['rows'][:3]])
    return out


def timing():
    s0 = SCRIPT[0]; kp = 'jumped' if 'jumped' in s0 else 'fell'
    return dict(VO=VO, DURS=DURS, STARTS=STARTS, DUR=DUR, toppct=at(0, kp, 0.4), hook2=VO[0] + DURS[0] * 0.5,
                hot=hot(), ctxline=at(4, 'Nifty', 0.3), comment=at(5, 'Comment'), follow=at(5, 'follow'))
