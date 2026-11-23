"""Why Nifty fell on 23 Nov 2026: Chennai Toon. Closes from INDmoney (NSE, 23 Nov 2026 15:45 IST)."""
TITLE = 'Why Nifty fell 450 points today (23 Nov 2026): 5 reasons'
SUB = 'MARKET RECAP · 23 NOV 2026'
DISC = 'Not a buy/sell call. Education only. I may hold some stocks named.'
A, K = 90, 556
CHARS = [('arjun', A, False), ('kavya', K, True)]
EXTRA_CSS = '''
.bw { position:absolute; bottom:60px; width:96px; height:400px; }
.bar { position:absolute; bottom:0; left:0; right:0; border:5px solid #2a1810; border-radius:10px 10px 0 0; transform-origin:50% 100%; }
.bl { position:absolute; bottom:-52px; left:-10px; right:-10px; text-align:center; font-family:"Oswald",sans-serif; font-size:28px; color:#6b5a4c; }
.wl { position:absolute; right:20px; font-family:"Oswald",sans-serif; font-size:30px; color:#e63946; letter-spacing:2px; }
.dn { color:#e63946; }
.num { font-size:120px; line-height:1; }
'''
SCENES = [
 dict(land='central', chars=CHARS, talker='arjun',
  ui='''<div class="card" id="n0a" style="left:110px;top:390px;width:860px;text-align:center"><h3>NIFTY 50 · CLOSE · 23 NOV 2026</h3>
<div class="num">25,349.65</div><div class="big dn" style="font-size:64px">−450.95 (−1.75%)</div>
<div class="src">Source: NSE via INDmoney, 23 Nov 2026</div></div>
<div class="stamp" id="n0s" style="left:230px;top:800px;transform:rotate(-6deg)">−643 FROM HIGH</div>''',
  js='''pop("#n0a", W[0][2]-0.2); cam.shake("#sc0", W[0][2], {amp:12}); T.pose("kavya0", W[0][2], {R:[-40,-120], L:[40,120]});
pop("#n0s", W[1][0], -6); T.point("arjun0", W[1][0]); T.pointUp("arjun0", P[2]); T.rest("kavya0", P[2]);'''),
 dict(land='itpark', chars=CHARS, talker='arjun',
  ui='''<div class="pill" id="n1p" style="left:250px;top:390px;font-size:56px">1 · PROFIT BOOKING</div>
<div class="card" id="n1c" style="left:110px;top:510px;width:860px;height:470px;padding:0"><div style="position:absolute;left:24px;top:14px"><h3>NIFTY CLOSE · LAST 6 SESSIONS</h3></div><div class="bw" style="left:30px"><div class="bar" id="nb0" style="height:90px;background:#2a9d8f"></div><div class="bl">16 Nov</div></div><div class="bw" style="left:160px"><div class="bar" id="nb1" style="height:120px;background:#2a9d8f"></div><div class="bl">17 Nov</div></div><div class="bw" style="left:290px"><div class="bar" id="nb2" style="height:70px;background:#2a9d8f"></div><div class="bl">18 Nov</div></div><div class="bw" style="left:420px"><div class="bar" id="nb3" style="height:159px;background:#2a9d8f"></div><div class="bl">19 Nov</div></div><div class="bw" style="left:550px"><div class="bar" id="nb4" style="height:247px;background:#2a9d8f"></div><div class="bl">20 Nov</div></div><div class="bw" style="left:680px"><div class="bar" id="nb5" style="height:108px;background:#e63946"></div><div class="bl">23 Nov</div></div><div id="wall" style="position:absolute;left:10px;right:10px;bottom:369px;border-top:6px dashed #e63946"></div><div class="wl" style="bottom:379px">26,000 WALL</div></div>''',
  js='''pop("#n1p", P[0]); T.pointUp("arjun1", P[0]); pop("#n1c", P[1]);
for (let i=0;i<6;i++) tl.fromTo("#nb"+i,{scaleY:0},{scaleY:1,duration:0.45,ease:"back.out(1.6)"},P[1]+0.3+i*0.12);
tl.fromTo("#wall",{scaleX:0,transformOrigin:"0 50%"},{scaleX:1,duration:0.5,ease:"power2.out"},W[2][4]-0.2);
cam.crashZoom("#cam1", W[2][1], {to:1.12, hold:0.6}); T.think("kavya1", P[2]); T.shrug("arjun1", P[3]); T.rest("kavya1", P[3]);'''),
 dict(land='ripon', chars=CHARS, talker='arjun',
  ui='''<div class="pill" id="n2p" style="left:330px;top:390px;font-size:56px">2 · BANKS</div>
<div class="card" id="n2c" style="left:110px;top:520px;width:860px"><h3>23 NOV 2026 · CLOSE</h3>
<div class="row" id="n2r1" style="opacity:0"><span>Bank Nifty 62,585</span><b>−3.17%</b></div>
<div class="row" id="n2r2" style="opacity:0"><span>HDFC Bank ₹817.80</span><b>−3.33%</b></div>
<div class="src">Source: NSE via INDmoney · Bank Nifty hit a record on 20 Nov</div></div>''',
  js='''pop("#n2p", P[0]); pop("#n2c", P[1]-0.1); T.point("arjun2", P[1]);
tl.fromTo("#n2r1",{opacity:0,x:-40},{opacity:1,x:0,duration:0.35,ease:"back.out(2)"},W[1][2]);
tl.fromTo("#n2r2",{opacity:0,x:-40},{opacity:1,x:0,duration:0.35,ease:"back.out(2)"},W[2][2]); T.pose("kavya2", W[2][2], {R:[-40,-120], L:[40,120]});'''),
 dict(land='mylapore', chars=CHARS, talker='arjun',
  ui='''<div class="card" id="n3a" style="left:110px;top:390px;width:860px"><h3>TATA STEEL · 23 NOV 2026</h3>
<div class="big"><span>₹163</span> <span class="dn">−8.43%</span></div><div class="src">52-week low ₹160.06 · NSE via INDmoney</div></div>
<div class="card" id="n3b" style="left:110px;top:660px;width:860px"><h3>THE APL APOLLO DEAL</h3>
<div class="row"><span>26.6% promoter stake</span><b>₹15,510 Cr</b></div><div class="row" id="n3r" style="opacity:0"><span>Open offer, 26% more</span><b>₹16,756 Cr</b></div>
<div class="src">Source: Tata Steel announcement via SMM / CNBC, 23 Nov 2026</div></div>''',
  js='''pop("#n3a", W[0][3]-0.2); cam.shake("#sc3", W[0][3], {amp:10}); T.cheer("kavya3", W[0][3]); T.rest("kavya3", P[1]);
pop("#n3b", W[1][1]); T.point("arjun3", P[1]);
tl.fromTo("#n3r",{opacity:0,x:-40},{opacity:1,x:0,duration:0.35,ease:"back.out(2)"},P[2]); T.shrug("kavya3", P[3]);'''),
 dict(land='napier', chars=CHARS, talker='arjun',
  ui='''<div class="pill" id="n4p" style="left:300px;top:390px;font-size:56px">4 · US FED</div>
<div class="card" id="n4c" style="left:160px;top:520px;width:760px;text-align:center"><h3>DECEMBER FED RATE HIKE ODDS</h3>
<div class="num dn">93%</div><div class="src">CME FedWatch, via IIFL, 23 Nov 2026</div></div>''',
  js='''pop("#n4p", P[0]); T.pointUp("arjun4", P[0]); T.think("kavya4", P[1]);
pop("#n4c", W[2][0]-0.1); cam.crashZoom("#cam4", W[2][0], {to:1.15, hold:0.6, oy:"40%"}); T.rest("kavya4", P[3]); T.point("arjun4", P[3]);'''),
 dict(land='tnagar', chars=CHARS, talker='arjun',
  ui='''<div class="pill" id="n5p" style="left:320px;top:390px;font-size:56px">5 · RUPEE</div>
<div class="card" id="n5c" style="left:160px;top:520px;width:760px;text-align:center"><h3>RUPEE PER US DOLLAR</h3>
<div class="big">₹92.67 <span style="font-size:44px">Fri</span></div><div class="big dn" id="n5d" style="opacity:0">~₹93 <span style="font-size:44px">today</span></div>
<div class="src">Source: IIFL market report, 23 Nov 2026</div></div>''',
  js='''pop("#n5p", P[0]); pop("#n5c", W[1][0]-0.1); T.point("arjun5", P[1]);
tl.fromTo("#n5d",{opacity:0,y:30},{opacity:1,y:0,duration:0.35,ease:"back.out(2)"},W[1][4]); T.shrug("kavya5", P[2]);'''),
 dict(land='valluvar', chars=CHARS, talker='arjun', cam='pull',
  ui='''<div class="card" id="n6a" style="left:110px;top:390px;width:860px"><h3>NIFTY 50</h3>
<div class="row"><span>Record high</span><span>26,373.20</span></div><div class="row"><span>Close 23 Nov</span><span>25,349.65</span></div></div>
<div class="stamp" id="n6s" style="left:170px;top:730px;transform:rotate(-5deg);color:#2a9d8f;border-color:#2a9d8f">ONLY −3.9%</div>''',
  js='''T.think("kavya6", P[0]); pop("#n6a", P[1]); T.point("arjun6", P[1]);
pop("#n6s", W[2][2], -5); T.cheer("arjun6", P[3]); T.rest("kavya6", P[3]); T.nod("kavya6", P[3]+0.3);'''),
 dict(land='marina', chars=CHARS, talker='arjun',
  ui='''<div class="pill" id="n7a" style="left:250px;top:430px;font-size:64px">SAVE THIS</div>
<div class="pill" id="n7b" style="left:170px;top:600px;font-size:52px;background:#fff">FOLLOW @moneyincloud</div>''',
  js='''pop("#n7a", P[0], -3); T.wave("arjun7", P[0], 3); pop("#n7b", P[0]+1.2, 2); T.wave("kavya7", P[0]+1.0, 3, "L");'''),
]
SFX = [('hit', 0, 0, 2, 0), ('pop', 0, 1, 0, 0), ('pop', 1, 0, 0, 0), ('tick', 1, 1, 0, 0.3), ('tick', 1, 1, 0, 0.45), ('tick', 1, 1, 0, 0.6),
       ('tick', 1, 1, 0, 0.75), ('tick', 1, 1, 0, 0.9), ('boing', 1, 1, 0, 1.0), ('hit', 1, 2, 1, 0),
       ('pop', 2, 0, 0, 0), ('pop', 2, 1, 2, 0), ('pop', 2, 2, 2, 0), ('hit', 3, 0, 3, 0), ('pop', 3, 1, 1, 0), ('pop', 3, 2, 0, 0),
       ('pop', 4, 0, 0, 0), ('riser', 4, 2, 0, -0.9), ('hit', 4, 2, 0, 0), ('pop', 5, 0, 0, 0), ('pop', 5, 1, 0, 0), ('boing', 5, 1, 4, 0),
       ('pop', 6, 1, 0, 0), ('ding', 6, 2, 2, 0), ('pop', 7, 0, 0, 0), ('pop', 7, 0, 0, 1.2)]
