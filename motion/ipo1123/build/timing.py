"""VO layout + phrase anchors (char-proportional within each line). Writes t.json."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); D = H + '/../../../studio/ipo1123/'
L = json.load(open(D + 'script.json')); DU = json.load(open(D + 'vo/durs.json'))
GAP = 0.24; VO = []; t = 0.12
for d in DU: VO.append(t); t += d + GAP
DUR = t + 0.5
STARTS = [0.0] + [v - 0.22 for v in VO[1:]]
def at(i, ph, off=0.0):
    s = L[i]; k = s.find(ph); assert k >= 0, (i, ph)
    return VO[i] + DU[i] * k / len(s) + off
A = dict(mist=(0, 'Your mistake'), sell0=(0, 'Not knowing'),
         thu=(1, 'Thursday'), fri=(1, 'Integris'), nse=(1, 'Both on'),
         pb=(2, 'Price bands'), notout=(2, 'Not out'), biz=(2, 'So let'),
         twist=(3, 'But'), c15=(3, 'fifteen'), c65=(3, 'The other'), m65=(3, 'sixty five'),
         f1=(4, 'Number one'), fmum=(4, 'from Mumbai'), fcb=(4, 'China Bistro'), fib=(4, 'India Bistro'), fad=(4, 'Art of Dum'), fwed=(4, 'plus wedding'), f28=(4, 'Twenty eight'), fuae=(4, 'thirteen'),
         frev=(5, 'Last year'), fpat=(5, 'Profit'), fbut=(5, 'But April'), floss=(5, 'A sixteen'), fipo=(5, 'The IPO'), f192=(5, 'a one ninety'), fofs=(5, 'plus an offer'),
         i2=(6, 'Number two'), istent=(6, 'Heart stents'), imade=(6, 'made in India'), ideu=(6, 'Germany'), inld=(6, 'Netherlands'), irev=(6, 'Revenue'), i65=(6, 'Sixty five'), i600=(6, 'Six hundred'), iofs=(6, 'plus an offer'),
         cs=(7, 'So here'), lf=(7, 'Foodlink lists'), li=(7, 'Integris December'), plot=(7, 'Price band'), rhp=(7, 'Read the'),
         send=(8, 'Send this'), save=(8, 'Save this'), follow=(8, 'follow'), edu=(8, 'Education'), loop=(8, 'Now you know'))
T = dict(VO=VO, DURS=DU, STARTS=STARTS, DUR=DUR)
T.update({k: round(at(*v), 3) for k, v in A.items()})
json.dump(T, open(H + '/t.json', 'w'), indent=0)
print('DUR', round(DUR, 2), {k: T[k] for k in ('twist', 'cs', 'send')})
