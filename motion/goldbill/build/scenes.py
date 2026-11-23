"""Gold jewellery bill at T. Nagar: Chennai Toon pilot. Numbers: 22K Chennai 19 Nov 2026 = ₹11,980/g (MJDTA via YourStory Tamil);
8 g = ₹95,840; VA 12% (example within 3-25%) = ₹11,501; GST 3% on ₹1,07,341 = ₹3,220; total ₹1,10,561 (+₹14,721, +15.4%).
Hallmark fee ₹45 -> ₹75/article (BIS amendment, 14 Sep 2026)."""
TITLE = 'Gold bill vs board rate: where ₹15,000 goes (Chennai)'
SUB = 'ILLUSTRATION · EXAMPLE BILL'
DISC = 'Example bill · Not a buy/sell call. Education only.'
A, K = 90, 556   # character x
EXTRA_CSS = '''
.board { background:#1f1a14; color:#ffd23f; border-color:#2a1810; }
.board h3 { color:#e9d9a8; }
.bill h3 { color:#7a2e2e; }
.coin { position:absolute; width:120px; height:120px; border-radius:50%; background:radial-gradient(circle at 35% 30%,#fff3b0,#f2b21b 55%,#b9790c); border:6px solid #2a1810;
  font-size:40px; display:flex; align-items:center; justify-content:center; color:#7a4a00; }
.tick { display:inline-flex; width:56px; height:56px; border-radius:12px; border:5px solid #2a1810; background:#fff; margin-right:18px; align-items:center; justify-content:center;
  font-size:40px; color:#2a9d8f; vertical-align:middle; }
.tip { font-size:38px; padding:14px 0; display:flex; align-items:center; border-bottom:4px dashed #d8ccb8; }
.tip:last-of-type { border-bottom:none; }
.bar { position:relative; height:34px; border-radius:17px; border:5px solid #2a1810; background:linear-gradient(90deg,#9be7a0,#ffd23f,#ff8a5b); }
.mk { position:absolute; top:-26px; width:12px; height:76px; background:#2a1810; border-radius:6px; }
.huid { font-family:"Oswald",sans-serif; font-size:60px; letter-spacing:6px; }
'''
CHARS = [('arjun', A, False), ('kavya', K, True)]

SCENES = [
 dict(land='tnagar', chars=CHARS, talker='arjun', cam='push',
  ui='''<div class="card board" id="g0a" style="left:50px;top:400px;width:450px"><h3>BOARD RATE · 8 g</h3><div class="big">₹95,840</div></div>
<div class="card bill" id="g0b" style="left:580px;top:400px;width:450px"><h3>YOUR BILL</h3><div class="big" style="color:#e63946">₹1,10,561</div></div>
<div class="stamp" id="g0c" style="left:250px;top:700px;transform:rotate(-6deg)">+₹14,721 ?!</div>''',
  js='''pop("#g0a", W[0][3]-0.1, -3); T.point("arjun0", W[0][1]);
pop("#g0b", W[1][3]-0.1, 3); T.cheer("kavya0", W[1][3]); T.pose("kavya0", W[1][3]+0.6, {R:[-40,-120], L:[40,120]});
pop("#g0c", P[2]+0.2, -6); cam.shake("#sc0", P[2]+0.25, {amp:12}); T.shrug("arjun0", P[2]);'''),
 dict(land='mylapore', chars=CHARS, talker='arjun',
  ui='''<div class="card" id="g1a" style="left:150px;top:390px;width:780px"><h3>CHENNAI · 22K GOLD · 19 NOV 2026</h3>
<div class="big">₹11,980 <span style="font-size:48px">/ gram</span></div>
<div class="row" id="g1r" style="opacity:0"><span>× 8 g (1 sovereign)</span><b>₹95,840</b></div>
<div class="src">Source: MJDTA rate, via YourStory Tamil, 19 Nov 2026</div></div>
<div class="coin" id="g1c1" style="left:120px;top:800px">8g</div><div class="coin" id="g1c2" style="left:830px;top:800px">₹</div>''',
  js='''pop("#g1a", W[1][4]-0.2); T.pointUp("arjun1", W[1][0]);
tl.fromTo("#g1r",{opacity:0,x:-40},{opacity:1,x:0,duration:0.35,ease:"back.out(2)"},P[2]);
pop("#g1c1", P[2]+0.2); pop("#g1c2", P[2]+0.4); T.nod("kavya1", P[3]); T.rest("arjun1", P[3]);'''),
 dict(land='central', chars=CHARS, talker='arjun',
  ui='''<div class="pill" id="g2p" style="left:140px;top:390px">VA = wastage + making</div>
<div class="card" id="g2b" style="left:110px;top:520px;width:860px"><h3>TYPICAL VA RANGE</h3>
<div style="display:flex;justify-content:space-between;font-size:40px;margin:6px 0 30px"><span>3%</span><span>25%</span></div>
<div class="bar"><div class="mk" id="g2m" style="left:0"></div></div>
<div class="src">Range: IIFL / BlueStone guides 2026 · 12% is an example</div></div>
<div class="card bill" id="g2c" style="left:110px;top:520px;width:860px;opacity:0"><h3>YOUR BILL</h3>
<div class="row"><span>Gold 8 g</span><span>₹95,840</span></div><div class="row"><span>VA 12%</span><b>+ ₹11,501</b></div></div>''',
  js='''pop("#g2p", W[0][2]-0.1, -2); T.think("kavya2", P[1]);
pop("#g2b", P[2]); tl.fromTo("#g2m",{x:0},{x:300,duration:0.9,ease:"power2.out"},W[2][2]);
out("#g2b", P[3]-0.1); pop("#g2c", P[3]); T.point("arjun2", P[3]);'''),
 dict(land='ripon', chars=CHARS, talker='arjun',
  ui='''<div class="card" id="g3a" style="left:140px;top:390px;width:800px;text-align:center"><h3>HALLMARK ON EVERY PIECE</h3>
<div class="huid">BIS · 22K916 · <span style="color:#e63946">XY12AB</span></div><div class="src">6-digit HUID (sample) · verify in BIS Care app</div></div>
<div class="card" id="g3b" style="left:210px;top:660px;width:660px;text-align:center"><h3>FEE PER PIECE · SEP 2026</h3>
<div class="big"><s style="color:#9a8a7a">₹45</s> <span style="color:#e63946">₹75</span></div><div class="src">Source: BIS Hallmarking Amendment Regulations, 14 Sep 2026</div></div>''',
  js='''pop("#g3a", W[0][3]-0.2); T.pointUp("arjun3", P[0]);
pop("#g3b", W[1][2]); cam.crashZoom("#cam3", W[1][4], {to:1.18, hold:0.5, ox:"50%", oy:"40%"}); T.cheer("kavya3", W[1][4]);
T.rest("kavya3", P[2]); T.nod("arjun3", P[2]);'''),
 dict(land='napier', chars=CHARS, talker='arjun',
  ui='''<div class="pill" id="g4p" style="left:380px;top:390px;font-size:70px">GST 3%</div>
<div class="card bill" id="g4c" style="left:110px;top:540px;width:860px"><h3>YOUR BILL</h3>
<div class="row"><span>Gold + VA</span><span>₹1,07,341</span></div><div class="row" id="g4r" style="opacity:0"><span>GST 3%</span><b>+ ₹3,220</b></div>
<div class="src">GST on jewellery sale: 3% of the value (CBIC GST FAQ)</div></div>''',
  js='''pop("#g4p", P[0]+0.1, -3); pop("#g4c", P[1]); T.point("arjun4", P[1]);
tl.fromTo("#g4r",{opacity:0,x:-40},{opacity:1,x:0,duration:0.35,ease:"back.out(2)"},P[2]); T.shrug("kavya4", P[2]);'''),
 dict(land='valluvar', chars=CHARS, talker='arjun', cam='pull',
  ui='''<div class="card bill" id="g5a" style="left:110px;top:400px;width:860px;text-align:center"><h3>TOTAL BILL · 1 SOVEREIGN</h3>
<div class="big" style="font-size:130px;color:#e63946">₹1,10,561</div><div class="src">vs board rate ₹95,840</div></div>
<div class="stamp" id="g5s" style="left:320px;top:740px;transform:rotate(-7deg)">+15.4%</div>''',
  js='''pop("#g5a", P[1]); cam.shake("#sc5", P[1]+0.3, {amp:10}); T.cheer("arjun5", P[1]);
pop("#g5s", P[2]+0.1, -7); T.pose("kavya5", P[2], {R:[-40,-120], L:[40,120]}); T.rest("arjun5", P[2]+0.6);'''),
 dict(land='metro', chars=CHARS, talker='arjun',
  ui='''<div class="card" id="g6a" style="left:70px;top:390px;width:940px"><h3>3 TIPS BEFORE YOU BUY</h3>
<div class="tip" id="g6t1" style="opacity:0"><span class="tick">1</span>Ask the VA % first</div>
<div class="tip" id="g6t2" style="opacity:0"><span class="tick">2</span>Check HUID in BIS Care app</div>
<div class="tip" id="g6t3" style="opacity:0"><span class="tick">3</span>Investing? Gold ETF: no making/GST*</div>
<div class="src">*ETFs have a small yearly expense ratio · Source: Angel One GST guide, 2026</div></div>''',
  js='''pop("#g6a", P[0]); T.pointUp("arjun6", P[0]);
[1,2,4].forEach((k,i)=>{ tl.fromTo("#g6t"+(i+1),{opacity:0,x:-50},{opacity:1,x:0,duration:0.35,ease:"back.out(2)"},P[k]); });
T.nod("kavya6", P[1]); T.think("kavya6", P[3]); T.rest("kavya6", P[4]+0.8);'''),
 dict(land='marina', chars=CHARS, talker='arjun',
  ui='''<div class="pill" id="g7a" style="left:250px;top:430px;font-size:64px">SAVE THIS</div>
<div class="pill" id="g7b" style="left:170px;top:600px;font-size:52px;background:#fff">FOLLOW @moneyincloud</div>''',
  js='''pop("#g7a", P[0], -3); T.wave("arjun7", P[0], 3); pop("#g7b", P[1], 2); T.wave("kavya7", P[1]-0.2, 3, "L");'''),
]

# sound cues: (kind, scene, phrase, word, offset)
SFX = [('pop', 0, 0, 3, -0.1), ('pop', 0, 1, 3, -0.1), ('hit', 0, 2, 0, 0.2),
       ('pop', 1, 1, 4, -0.2), ('ding', 1, 2, 0, 0), ('coin', 1, 2, 0, 0.2), ('coin', 1, 2, 0, 0.4),
       ('pop', 2, 0, 2, -0.1), ('pop', 2, 2, 0, 0), ('tick', 2, 2, 2, 0), ('pop', 2, 3, 0, 0), ('kaching', 2, 3, 3, 0),
       ('pop', 3, 0, 3, -0.2), ('pop', 3, 1, 2, 0), ('hit', 3, 1, 4, 0),
       ('pop', 4, 0, 0, 0.1), ('pop', 4, 1, 0, 0), ('kaching', 4, 2, 0, 0),
       ('riser', 5, 1, 0, -0.9), ('hit', 5, 1, 0, 0), ('kaching', 5, 1, 0, 0.1), ('pop', 5, 2, 0, 0.1),
       ('pop', 6, 0, 0, 0), ('ding', 6, 1, 0, 0), ('ding', 6, 2, 0, 0), ('ding', 6, 4, 0, 0),
       ('pop', 7, 0, 0, 0), ('pop', 7, 1, 0, 0)]
