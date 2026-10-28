"""Generate the HyperFrames composition for the recharge reel (Data Storytelling look: cream sheet, pencil, notes).
Writes ../hf/recharge/index.html with timings from recharge_t.py. Audio: ../recharge/mix.wav -> assets/mix.wav"""
import json, shutil, os
import recharge_t as R

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, '..', 'hf', 'recharge')
T = R.times()
if os.path.exists(R.SH + 'mix.wav'): shutil.copy(R.SH + 'mix.wav', P + '/assets/mix.wav')

HTML = r'''<!doctype html>
<html lang="en" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="assets/gsap.min.js"></script>
<style>
@font-face{font-family:"Rupee";src:url(assets/fonts/Poppins-Bold.ttf);unicode-range:U+20B9;}
@font-face{font-family:"Caveat";src:url(assets/fonts/caveat-latin-700-normal.woff2) format("woff2");font-weight:700;}
@font-face{font-family:"Newsreader";src:url(assets/fonts/newsreader-latin-600-normal.woff2) format("woff2");font-weight:600;}
@font-face{font-family:"NewsreaderI";src:url(assets/fonts/newsreader-latin-400-italic.woff2) format("woff2");}
@font-face{font-family:"Plex";src:url(assets/fonts/ibm-plex-mono-latin-500-normal.woff2) format("woff2");}
@font-face{font-family:"Anton";src:url(assets/fonts/anton-latin-400-normal.woff2) format("woff2");}
:root{--paper:#f3ecdc;--ink:#2b2622;--grey:#9a9184;--red:#c8372d;--blue:#2f5d9e;--jio:#0f3cc9;--airtel:#e40000;--vi:#f2c200;}
*{margin:0;padding:0;box-sizing:border-box;}
html,body{width:1080px;height:1920px;overflow:hidden;background:var(--paper);}
#root{width:100%;height:100%;position:relative;overflow:hidden;background:var(--paper);}
#cam{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:540px 960px;}
#world{position:absolute;left:0;top:0;width:1080px;height:18000px;
  background-color:var(--paper);
  background-image:radial-gradient(rgba(43,38,34,.13) 1.6px,transparent 1.8px);background-size:36px 36px;}
.sec{position:absolute;left:0;width:1080px;height:1920px;}
.h{position:absolute;left:70px;right:70px;font-family:"Rupee","Newsreader",serif;font-weight:600;color:var(--ink);line-height:1.04;letter-spacing:-.01em;}
.hand{position:absolute;font-family:"Rupee","Caveat",cursive;font-weight:700;white-space:nowrap;line-height:1;}
.mono{position:absolute;font-family:"Plex",monospace;color:var(--grey);letter-spacing:.06em;white-space:nowrap;}
.num{position:absolute;font-family:"Rupee","Newsreader",serif;font-weight:600;color:var(--ink);white-space:nowrap;line-height:1;}
.chip{position:absolute;font-family:"Anton",sans-serif;font-size:56px;padding:8px 26px;border-radius:14px;border:4px solid var(--ink);white-space:nowrap;line-height:1.1;}
.card{position:absolute;background:#fbf7ee;border:3px solid var(--ink);border-radius:18px;box-shadow:8px 10px 0 rgba(43,38,34,.18);}
.slip{position:absolute;background:#fffaf0;border:2px solid rgba(43,38,34,.5);padding:20px 30px;box-shadow:6px 8px 0 rgba(43,38,34,.12);}
svg{position:absolute;left:0;top:0;overflow:visible;}
#hdr{position:absolute;left:0;top:0;width:1080px;height:150px;background:linear-gradient(var(--paper) 70%,rgba(243,236,220,0));}
#prog{position:absolute;left:60px;top:112px;height:6px;width:960px;background:var(--red);transform-origin:0 50%;}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="__DUR__" data-width="1080" data-height="1920">
  <div id="cam"><div id="world"></div></div>
  <div id="hdr">
    <div class="mono" style="left:52px;top:58px;font-size:30px;color:var(--ink)">@moneyincloud</div>
    <div class="mono" style="right:52px;top:58px;font-size:30px;color:var(--red)">RECHARGE CHECK</div>
    <div style="position:absolute;left:60px;top:114px;width:960px;height:2px;background:rgba(43,38,34,.5)"></div>
    <div id="prog"></div>
  </div>
  <audio id="mix" src="assets/mix.wav" data-start="0" data-duration="__DUR__" data-track-index="1" data-volume="1"></audio>
</div>
<script>
const T = __T__;
const SEC = 2000, W = document.getElementById('world');
const NS = 'http://www.w3.org/2000/svg';
const tl = gsap.timeline({paused:true});
let uid = 0;
function sec(k){ const d=document.createElement('div'); d.className='sec'; d.style.top=(k*SEC)+'px'; W.appendChild(d); return d; }
function div(p, cls, css, html){ const d=document.createElement('div'); d.className=cls; d.id='e'+(uid++); Object.assign(d.style, css||{}); if(html!==undefined) d.innerHTML=html; p.appendChild(d); return d; }
function svg(p){ const s=document.createElementNS(NS,'svg'); s.setAttribute('width','1080'); s.setAttribute('height','1920'); p.appendChild(s); return s; }
function path(s, d, col, w, extra){ const e=document.createElementNS(NS,'path'); e.setAttribute('d',d); e.setAttribute('fill', (extra&&extra.fill)||'none'); e.setAttribute('stroke',col); e.setAttribute('stroke-width',w); e.setAttribute('stroke-linecap','round'); e.setAttribute('stroke-linejoin','round'); s.appendChild(e); return e; }
// draw a stroke on
function draw(e, t, dur){ const L=e.getTotalLength(); e.style.strokeDasharray=L; tl.fromTo(e,{strokeDashoffset:L},{strokeDashoffset:0,duration:dur||0.6,ease:'power1.inOut'},t); }
// handwriting / reveal left->right
function write(e, t, dur){ tl.fromTo(e,{clipPath:'inset(-20% 100% -20% 0%)'},{clipPath:'inset(-20% 0% -20% 0%)',duration:dur||0.7,ease:'none'},t); }
function pop(e, t, rot){ tl.fromTo(e,{scale:0.2,opacity:0,rotation:(rot||0)-8},{scale:1,opacity:1,rotation:rot||0,duration:0.45,ease:'back.out(2.2)'},t); }
function fade(e, t){ tl.fromTo(e,{opacity:0,y:20},{opacity:1,y:0,duration:0.4,ease:'power2.out'},t); }
function count(e, t, a, b, fmt, dur){ const o={v:a}; e.textContent=fmt(a); tl.to(o,{v:b,duration:dur||1.0,ease:'power2.out',onUpdate:()=>{e.textContent=fmt(o.v);}},t); }
const inr = v => '₹'+Math.round(v).toLocaleString('en-IN');
// un-closed pencil ring around a point
function ring(s, cx, cy, rx, ry, col, t){ const a0=-0.6, a1=a0+Math.PI*2*0.93; let d=''; for(let i=0;i<=40;i++){const a=a0+(a1-a0)*i/40; const wob=1+0.04*Math.sin(i*1.7); d+=(i?'L':'M')+(cx+rx*wob*Math.cos(a)).toFixed(1)+' '+(cy+ry*wob*Math.sin(a)).toFixed(1);} const e=path(s,d,col,7); draw(e,t,0.45); return e; }
function strike(s, x0, y0, x1, y1, col, t){ const e=path(s,`M${x0} ${y0} Q ${(x0+x1)/2} ${(y0+y1)/2-14} ${x1} ${y1}`,col,10); draw(e,t,0.3); return e; }
function check(s, x, y, col, t){ const e=path(s,`M${x-22} ${y} L${x-6} ${y+20} L${x+26} ${y-26}`,col,10); draw(e,t,0.25); return e; }

// ---------- pencil (lives in world) ----------
const pen = document.createElement('div'); pen.id='pen'; pen.style.cssText='position:absolute;left:0;top:0;width:60px;height:420px;transform-origin:0 0;'; W.appendChild(pen);
pen.innerHTML = `<svg width="80" height="440" style="left:-14px;top:-6px"><g transform="rotate(-28 0 0)">
<polygon points="0,0 -11,46 11,46" fill="#e8c9a0" stroke="#2b2622" stroke-width="3"/><polygon points="0,0 -4,16 4,16" fill="#2b2622"/>
<rect x="-12" y="46" width="24" height="190" fill="#2f5d9e" stroke="#2b2622" stroke-width="3"/>
<rect x="-12" y="236" width="24" height="190" fill="#c8372d" stroke="#2b2622" stroke-width="3"/></g></svg>`;
let penAt = {x: 980, y: 1500};
gsap.set(pen,{x:penAt.x,y:penAt.y});
function penTo(x, y, t, dur){ tl.to(pen,{x:x, y:y, duration:dur||0.35, ease:'power2.inOut'}, t); tl.to(pen,{y:y-18,duration:0.08,ease:'power1.out'},t+(dur||0.35)); tl.to(pen,{y:y,duration:0.1,ease:'power1.in'},t+(dur||0.35)+0.08); }

// ---------- camera ----------
const cam = document.getElementById('cam');
const starts = [T.s0,T.s1,T.s2,T.s3,T.s4,T.s5,T.s6,T.s7,T.s8];
gsap.set(W,{y:0}); gsap.set(cam,{scale:1});
for(let k=1;k<9;k++){ const b=starts[k]-0.35;
  tl.to(W,{y:-k*SEC,duration:0.75,ease:'power3.inOut'},b);
  tl.to(cam,{scale:0.78,duration:0.36,ease:'power2.out'},b); tl.to(cam,{scale:1,duration:0.42,ease:'power2.inOut'},b+0.36); }
// slow push-in within each scene
for(let k=0;k<9;k++){ const a=starts[k]+0.45, e=(k<8?starts[k+1]:T.dur)-0.4; if(e>a) tl.to(cam,{rotation:(k%2?0.6:-0.6),duration:e-a,ease:'sine.inOut'},a); }
tl.fromTo('#prog',{scaleX:0},{scaleX:1,duration:T.dur,ease:'none'},0);
const S = k => k*SEC;  // y offset of section k in world, for the pencil

// ================= S0 HOOK =================
{ const p=sec(0), s=svg(p);
  const h=div(p,'h',{top:'190px',fontSize:'92px'},'<span style="display:block">Your recharge may</span><span style="display:block">cost 15% more soon.</span>'); write(h,0.0,0.9);
  const ph=path(s,'M300 560 Q300 520 340 520 L740 520 Q780 520 780 560 L780 1420 Q780 1460 740 1460 L340 1460 Q300 1460 300 1420 Z','#2b2622',9); draw(ph,0.15,1.0);
  path(s,'M490 548 L590 548','#2b2622',8); const cam1=path(s,'M490 548 L590 548','#2b2622',8); draw(cam1,0.8,0.2);
  const lab=div(p,'mono',{left:'0',width:'1080px',textAlign:'center',top:'640px',fontSize:'32px',color:'#2b2622'},'RECHARGE · 28 DAYS'); fade(lab,0.7);
  const pr=div(p,'num',{left:'0',width:'1080px',textAlign:'center',top:'800px',fontSize:'190px'},'₹189'); pop(pr,0.9);
  const sub=div(p,'mono',{left:'0',width:'1080px',textAlign:'center',top:'1040px',fontSize:'28px'},'Jio · cheapest 28-day plan (Jul 2026)'); fade(sub,1.1);
  const t1=T['0:fifteen percent']-0.1; count(pr,t1,189,217,inr,0.9);
  tl.to(pr,{color:'#c8372d',duration:0.2},t1);
  tl.fromTo(p,{x:0},{x:0,keyframes:[{x:-10,duration:.05},{x:9,duration:.05},{x:-6,duration:.05},{x:0,duration:.05}]},t1+0.9);
  ring(s,540,905,300,130,'#c8372d',t1+0.2);
  const n1=div(p,'hand',{left:'760px',top:'690px',fontSize:'96px',color:'#c8372d',transform:'rotate(-8deg)'},'+15%?'); write(n1,t1+0.5,0.5);
  penTo(800,S(0)+760,t1+0.4,0.3);
  const n2=div(p,'hand',{left:'130px',top:'1560px',fontSize:'86px',color:'#2f5d9e'},'do this before it does ↓'); write(n2,T['0:Do this'],1.0);
  penTo(160,S(0)+1600,T['0:Do this']-0.2,0.3); penTo(900,S(0)+1600,T['0:Do this']+0.2,0.9);
}
// ================= S1 12? WRONG =================
{ const p=sec(1), s=svg(p), t0=T.s1;
  const h=div(p,'h',{top:'190px',fontSize:'90px'},'<span style="display:block">How many recharges</span><span style="display:block">in a year?</span>'); write(h,t0+0.3,0.9);
  const M=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'];
  const tb=T['1:How many']+0.3;
  M.forEach((m,i)=>{ const x=110+(i%4)*220, y=560+Math.floor(i/4)*190;
    const b=path(s,`M${x} ${y} L${x+190} ${y} L${x+190} ${y+160} L${x} ${y+160} Z`,'#2b2622',5); draw(b,tb+i*0.07,0.35);
    const l=div(p,'mono',{left:(x+18)+'px',top:(y+16)+'px',fontSize:'30px',color:'#2b2622'},m); fade(l,tb+i*0.07+0.2);
    check(s,x+120,y+105,'#2f5d9e',tb+0.9+i*0.09); });
  penTo(230,S(1)+660,tb+0.8,0.25); penTo(890,S(1)+1040,tb+1.8,1.0);
  const tw=T['1:Twelve']-0.15; const q=div(p,'hand',{left:'360px',top:'1180px',fontSize:'240px',color:'#2f5d9e'},'12?'); write(q,tw,0.4);
  const tr=T['1:Wrong']-0.1; strike(s,330,1330,700,1270,'#c8372d',tr);
  const wr=div(p,'hand',{left:'250px',top:'1500px',fontSize:'170px',color:'#c8372d',transform:'rotate(-6deg)'},'WRONG'); pop(wr,tr+0.15,-6);
  tl.fromTo(p,{x:0},{x:0,keyframes:[{x:-14,duration:.05},{x:12,duration:.05},{x:-7,duration:.05},{x:0,duration:.05}]},tr+0.15);
}
// ================= S2 13 RECHARGES =================
{ const p=sec(2), s=svg(p), t0=T.s2;
  const h=div(p,'h',{top:'190px',fontSize:'88px'},'<span style="display:block">One year = 365 days.</span><span style="display:block">One plan = 28 days.</span>'); write(h,t0+0.3,1.0);
  const ax=path(s,'M90 900 L990 900','#2b2622',5); draw(ax,t0+0.5,0.7);
  const X = d => 90 + 900*d/365;
  for(let d=0; d<=364; d+=28){ const tk=path(s,`M${X(d)} 880 L${X(d)} 920`,'#9a9184',4); draw(tk,t0+0.6+d/365*0.6,0.1);
    if(d%56===0){ const l=div(p,'mono',{left:(X(d)-30)+'px',top:'935px',fontSize:'24px',width:'60px',textAlign:'center'},String(d)); fade(l,t0+0.7+d/365*0.6);} }
  const dl=div(p,'mono',{left:'880px',top:'975px',fontSize:'24px'},'days →'); fade(dl,t0+1.2);
  const ta=T['2:runs out'], tb=T['2:is thirteen'];
  const cnt=div(p,'num',{left:'0',width:'1080px',textAlign:'center',top:'1070px',fontSize:'200px'},'0');
  for(let k=1;k<=13;k++){ const d=Math.min(28*k,364), tk=ta+(tb-ta)*(k-1)/12;
    const c=div(p,'',{position:'absolute',left:(X(d)-22)+'px',top:'800px',width:'44px',height:'58px',background:k===13?'#c8372d':'#fbf7ee',border:'4px solid #2b2622',borderRadius:'8px'});
    tl.fromTo(c,{y:-160,opacity:0},{y:0,opacity:1,duration:0.3,ease:'bounce.out'},tk);
  }
  fade(cnt,ta); count(cnt,ta+0.15,0,13,v=>String(Math.round(v)),tb-ta);
  const eq=div(p,'mono',{left:'0',width:'1080px',textAlign:'center',top:'1320px',fontSize:'40px',color:'#2b2622'},'365 ÷ 28 = 13.04'); write(eq,T['2:Three sixty five'],0.8);
  ring(s,X(364),830,58,72,'#c8372d',tb+0.1);
  const n=div(p,'hand',{left:'640px',top:'620px',fontSize:'74px',color:'#c8372d',transform:'rotate(-5deg)'},'13th recharge!'); write(n,tb+0.3,0.6);
  tl.to(cnt,{color:'#c8372d',duration:0.2},tb+0.2);
  const yp=div(p,'hand',{left:'110px',top:'1470px',fontSize:'92px',color:'#2f5d9e'},'you pay for 13 months'); write(yp,T['2:You pay'],0.9);
  const yp2=div(p,'hand',{left:'250px',top:'1590px',fontSize:'92px',color:'#2f5d9e'},'every single year'); write(yp2,T['2:You pay']+1.0,0.8);
  penTo(X(28),S(2)+840,ta-0.2,0.3); penTo(X(364),S(2)+840,tb,(tb-ta)); penTo(150,S(2)+1500,T['2:You pay']-0.2,0.4); penTo(900,S(2)+1640,T['2:You pay']+1.0,1.0);
}
// ================= S3 WHY NOW =================
{ const p=sec(3), s=svg(p), t0=T.s3;
  const h=div(p,'h',{top:'190px',fontSize:'92px'},'Jio listed today.'); write(h,t0+0.3,0.7);
  const tj=T['3:Jio listed'];
  const ax=path(s,'M150 980 L930 980','#2b2622',4); draw(ax,tj-0.2,0.4);
  const Y = v => 980 - (v-1000)/400*560;
  const ln=path(s,`M260 ${Y(1119)} L820 ${Y(1358)}`,'#0f3cc9',10); draw(ln,tj+0.2,0.8);
  const d1=div(p,'',{position:'absolute',left:'238px',top:(Y(1119)-22)+'px',width:'44px',height:'44px',borderRadius:'50%',background:'#fbf7ee',border:'5px solid #2b2622'}); pop(d1,tj+0.1);
  const d2=div(p,'',{position:'absolute',left:'798px',top:(Y(1358)-22)+'px',width:'44px',height:'44px',borderRadius:'50%',background:'#0f3cc9',border:'5px solid #2b2622'}); pop(d2,tj+0.9);
  const l1=div(p,'num',{left:'150px',top:(Y(1119)+40)+'px',fontSize:'64px'},'₹1,119'); fade(l1,tj+0.2);
  const l1b=div(p,'mono',{left:'150px',top:(Y(1119)+115)+'px',fontSize:'26px'},'IPO PRICE'); fade(l1b,tj+0.3);
  const l2=div(p,'num',{left:'700px',top:(Y(1358)-120)+'px',fontSize:'64px',color:'#0f3cc9'},'₹1,358'); fade(l2,tj+1.0);
  const l2b=div(p,'mono',{left:'700px',top:(Y(1358)-150)+'px',fontSize:'26px'},'OPENED 28 OCT'); fade(l2b,tj+1.0);
  const t21=T['3:twenty one percent']; ring(s,820,Y(1358),70,70,'#c8372d',t21);
  const n=div(p,'hand',{left:'440px',top:'500px',fontSize:'110px',color:'#c8372d',transform:'rotate(-6deg)'},'+21%'); write(n,t21+0.2,0.5);
  const tbk=T['3:Brokers'];
  const c1=div(p,'slip',{left:'90px',top:'1080px',transform:'rotate(-2deg)'},'<div class="hand" style="position:static;font-size:58px;color:#2b2622">Elara: 12–15% hike</div><div class="mono" style="position:static;font-size:26px;margin-top:6px">expected in H2 FY27</div>'); pop(c1,tbk,-2);
  const c2=div(p,'slip',{left:'560px',top:'1120px',transform:'rotate(2deg)'},'<div class="hand" style="position:static;font-size:58px;color:#2b2622">Nomura: steady hikes</div><div class="mono" style="position:static;font-size:26px;margin-top:6px">peers likely to follow</div>'); pop(c2,tbk+0.6,2);
  const chips=[['JIO','#0f3cc9','#fff'],['AIRTEL','#e40000','#fff'],['Vi','#f2c200','#2b2622']];
  chips.forEach((c,i)=>{ const e=div(p,'chip',{left:(120+i*300)+'px',top:'1420px',background:c[1],color:c[2]},c[0]); pop(e,T['3:twelve to fifteen']-0.3+i*0.15,(i-1)*3); });
  const big=div(p,'hand',{left:'230px',top:'1560px',fontSize:'130px',color:'#c8372d'},'12–15% next?'); write(big,T['3:twelve to fifteen']+0.5,0.7);
  const src=div(p,'mono',{left:'0',width:'1080px',textAlign:'center',top:'1760px',fontSize:'22px'},'Mint/TradingView, 28 Oct 2026 · broker estimates, not announced'); fade(src,tj+1.2);
  penTo(820,S(3)+Y(1358),tj+0.2,0.8); penTo(600,S(3)+620,t21+0.1,0.3); penTo(300,S(3)+1640,T['3:twelve to fifteen']+0.4,0.3); penTo(940,S(3)+1640,T['3:twelve to fifteen']+0.8,0.7);
}
// ================= S4 HOW MUCH? =================
{ const p=sec(4), s=svg(p), t0=T.s4;
  const a1=path(s,'M150 400 L150 1400 L950 1400','#2b2622',5); draw(a1,t0+0.1,0.6);
  const q=div(p,'hand',{left:'190px',top:'520px',fontSize:'104px',color:'#2f5d9e'},'how much will it'); write(q,T['4:how much'],0.7);
  const q2=div(p,'hand',{left:'190px',top:'650px',fontSize:'104px',color:'#2f5d9e'},'cost you?'); write(q2,T['4:how much']+0.6,0.5);
  const slot=path(s,'M470 1390 L470 900 L700 900 L700 1390','#9a9184',5); slot.setAttribute('stroke-dasharray','18 14'); fade(slot,t0+0.4);
  const qm=div(p,'num',{left:'540px',top:'1050px',fontSize:'150px',color:'#9a9184'},'?'); pop(qm,t0+0.6);
  penTo(640,S(4)+1000,t0+0.3,0.4); tl.to(pen,{y:S(4)+960,duration:0.6,ease:'sine.inOut',yoyo:true,repeat:3},t0+0.8);
}
// ================= S5 MATH =================
{ const p=sec(5), s=svg(p), t0=T.s5;
  const h=div(p,'h',{top:'190px',fontSize:'84px'},'The math, one phone'); write(h,t0+0.2,0.7);
  const hk=div(p,'mono',{left:'72px',top:'300px',fontSize:'28px'},'₹189 PLAN × 13 RECHARGES A YEAR'); fade(hk,T['5:one eighty nine']);
  const base=1400, k=0.25;
  const ax=path(s,`M110 ${base} L970 ${base}`,'#2b2622',5); draw(ax,t0+0.2,0.5);
  const mk = (x, v, col, t, lab) => { const hgt=v*k;
    const b=div(p,'',{position:'absolute',left:x+'px',top:(base-hgt)+'px',width:'230px',height:hgt+'px',background:col,border:'5px solid #2b2622',borderBottom:'none',transformOrigin:'50% 100%'});
    tl.fromTo(b,{scaleY:0},{scaleY:1,duration:0.9,ease:'power3.out'},t);
    const n=div(p,'num',{left:(x-30)+'px',width:'290px',textAlign:'center',top:(base-hgt-110)+'px',fontSize:'78px'},inr(0)); count(n,t,0,v,inr,0.9); fade(n,t);
    const l=div(p,'mono',{left:(x-20)+'px',width:'270px',textAlign:'center',top:(base+20)+'px',fontSize:'28px',color:'#2b2622'},lab); fade(l,t); return b; };
  mk(200,2457,'repeating-linear-gradient(45deg,#2b2622 0 6px,#fbf7ee 6px 18px)',T['5:is two thousand']-0.2,'TODAY');
  mk(620,2826,'repeating-linear-gradient(45deg,#c8372d 0 8px,#fbf7ee 8px 18px)',T['5:After a fifteen']+0.6,'AFTER +15%');
  const t3=T["5:That's three"]; const br=path(s,`M880 ${base-2826*k} L940 ${base-2826*k} L940 ${base-2457*k} L880 ${base-2457*k}`,'#c8372d',7); draw(br,t3,0.4);
  const n=div(p,'hand',{left:'560px',top:'420px',fontSize:'100px',color:'#c8372d',transform:'rotate(-4deg)'},'+₹369 a year'); write(n,t3+0.3,0.7);
  const tf=T['5:A family'];
  for(let i=0;i<4;i++){ const ph=div(p,'',{position:'absolute',left:(150+i*120)+'px',top:'1520px',width:'80px',height:'140px',border:'6px solid #2b2622',borderRadius:'16px',background:'#fbf7ee'}); pop(ph,tf+i*0.12,(i-1.5)*4); }
  const f=div(p,'hand',{left:'640px',top:'1510px',fontSize:'86px',color:'#2f5d9e'},'≈ ₹1,476'); write(f,tf+0.7,0.6);
  const f2=div(p,'mono',{left:'645px',top:'1620px',fontSize:'24px',color:'#2b2622'},'EXTRA/YEAR · FAMILY OF 4'); fade(f2,tf+1.0);
  const src=div(p,'mono',{left:'0',width:'1080px',textAlign:'center',top:'1760px',fontSize:'22px'},'my calculation · plan price: Jio ₹189 / 28 days'); fade(src,t0+1.0);
  penTo(330,S(5)+base-2457*k-40,T['5:is two thousand'],0.4); penTo(750,S(5)+base-2826*k-40,T['5:After a fifteen']+0.6,0.4); penTo(940,S(5)+base-2700*k,t3,0.3); penTo(650,S(5)+480,t3+0.3,0.3); penTo(1000,S(5)+480,t3+0.6,0.7); penTo(700,S(5)+1560,tf+0.6,0.3); penTo(990,S(5)+1580,tf+0.9,0.6);
}
// ================= S6 LOCK THE PRICE =================
{ const p=sec(6), s=svg(p), t0=T.s6;
  const h=div(p,'h',{top:'190px',fontSize:'90px'},'Lock today’s price.'); write(h,t0+0.2,0.7);
  const n=div(p,'hand',{left:'80px',top:'330px',fontSize:'68px',color:'#2f5d9e'},'recharge a longer plan before the hike'); write(n,T['6:before the hike']-0.2,1.3);
  const tlk=T['6:locked']-0.2;
  const body=path(s,'M470 640 L610 640 L610 760 L470 760 Z','#2b2622',8,{fill:'#fbf7ee'}); draw(body,tlk,0.4);
  const sh=document.createElementNS(NS,'path'); sh.setAttribute('d','M495 640 L495 590 Q495 545 540 545 Q585 545 585 590 L585 640'); sh.setAttribute('fill','none'); sh.setAttribute('stroke','#2b2622'); sh.setAttribute('stroke-width','8'); s.appendChild(sh);
  tl.fromTo(sh,{y:-40},{y:0,duration:0.25,ease:'back.in(3)'},tlk+0.5);
  const lk=div(p,'mono',{left:'650px',top:'665px',fontSize:'30px',color:'#2b2622'},'<span style="display:block">PRICE LOCKED</span><span style="display:block">WHEN YOU PAY</span>'); fade(lk,tlk+0.7);
  const ta=T['6:annual plan']-0.2;
  const C=[['JIO','#0f3cc9','#fff','2.5GB/day'],['AIRTEL','#e40000','#fff','2GB/day'],['Vi','#f2c200','#2b2622','2GB/day']];
  C.forEach((c,i)=>{ const x=70+i*320;
    const cd=div(p,'card',{left:x+'px',top:'860px',width:'300px',height:'300px'}); pop(cd,ta+i*0.15,(i-1)*2);
    const ch=div(cd,'chip',{left:'20px',top:'20px',fontSize:'40px',background:c[1],color:c[2],padding:'4px 18px'},c[0]);
    div(cd,'num',{left:'20px',top:'120px',fontSize:'70px'},'₹3,599');
    div(cd,'mono',{left:'22px',top:'205px',fontSize:'22px',color:'#2b2622'},'365 DAYS');
    div(cd,'mono',{left:'22px',top:'240px',fontSize:'22px',color:'#2b2622'},c[3]); });
  const td=T['6:After a fifteen']; const X = v => 140 + (v-3400)/900*800;
  const ax=path(s,`M120 1380 L960 1380`,'#9a9184',4); draw(ax,td-0.3,0.4);
  const seg=path(s,`M${X(3599)} 1380 L${X(4139)} 1380`,'#c8372d',14); draw(seg,td+0.4,0.8);
  const a=div(p,'',{position:'absolute',left:(X(3599)-26)+'px',top:'1354px',width:'52px',height:'52px',borderRadius:'50%',background:'#2f5d9e',border:'5px solid #2b2622'}); pop(a,td);
  const b=div(p,'',{position:'absolute',left:(X(4139)-26)+'px',top:'1354px',width:'52px',height:'52px',borderRadius:'50%',background:'#c8372d',border:'5px solid #2b2622'}); pop(b,td+1.1);
  const la=div(p,'num',{left:(X(3599)-110)+'px',top:'1250px',fontSize:'60px',color:'#2f5d9e'},'₹3,599'); fade(la,td);
  const lam=div(p,'mono',{left:(X(3599)-110)+'px',top:'1430px',fontSize:'24px'},'TODAY'); fade(lam,td);
  const lb=div(p,'num',{left:(X(4139)-150)+'px',top:'1250px',fontSize:'60px',color:'#c8372d'},'₹4,139'); fade(lb,td+1.1);
  const lbm=div(p,'mono',{left:(X(4139)-150)+'px',top:'1430px',fontSize:'24px'},'IF +15% (MY CALC)'); fade(lbm,td+1.1);
  const t5=T["6:That's five"]; const sv=div(p,'hand',{left:'300px',top:'1520px',fontSize:'150px',color:'#2f5d9e',transform:'rotate(-4deg)'},'save ₹540'); write(sv,t5,0.7);
  ring(s,540,1610,330,110,'#2f5d9e',t5+0.7);
  penTo(120,S(6)+380,T['6:before the hike']-0.3,0.3); penTo(1000,S(6)+400,T['6:before the hike'],1.2); penTo(X(4139),S(6)+1380,td+0.4,0.8); penTo(340,S(6)+1600,t5-0.1,0.3); penTo(900,S(6)+1620,t5+0.1,0.7);
}
// ================= S7 FAIR WARNING =================
{ const p=sec(7), s=svg(p), t0=T.s7;
  const h=div(p,'h',{top:'190px',fontSize:'92px'},'Only if…'); write(h,t0+0.2,0.5);
  const items=[['you really use the data',T['7:really use']-0.2,'#2f5d9e',true],['same SIM all year',T['7:really use']+0.6,'#2f5d9e',true],['hike date: not official yet',T['7:no hike date']-0.1,'#c8372d',false]];
  items.forEach((it,i)=>{ const y=560+i*340;
    const bx=path(s,`M110 ${y} L190 ${y} L190 ${y+80} L110 ${y+80} Z`,'#2b2622',6); draw(bx,it[1]-0.2,0.3);
    const tx=div(p,'hand',{left:'230px',top:(y-6)+'px',fontSize:'90px',color:it[2]},it[0]); write(tx,it[1],0.8);
    if(it[3]) check(s,152,y+40,'#2f5d9e',it[1]+0.4); else { strike(s,122,y+12,178,y+70,'#c8372d',it[1]+0.4); strike(s,178,y+12,122,y+70,'#c8372d',it[1]+0.55); }
    penTo(240,S(7)+y+40,it[1]-0.15,0.2); });
  const nt=div(p,'mono',{left:'0',width:'1080px',textAlign:'center',top:'1620px',fontSize:'26px'},'No hike date announced by Jio, Airtel or Vi as of 28 Oct 2026'); fade(nt,T['7:no hike date']);
}
// ================= S8 CHEAT SHEET + SEND + FOLLOW =================
{ const p=sec(8), s=svg(p), t0=T.s8;
  const cd=div(p,'card',{left:'70px',top:'250px',width:'940px',height:'760px'}); pop(cd,t0+0.05,-0.5);
  div(cd,'h',{left:'40px',right:'40px',top:'30px',fontSize:'64px'},'Recharge cheat sheet');
  const rows=[['28-day plan','13 recharges / year','#2b2622'],['Expected hike','12–15% (brokers)','#c8372d'],['Smart move','lock a longer plan','#2f5d9e'],['Check first','no date official yet','#c8372d']];
  rows.forEach((r,i)=>{ const y=150+i*140; const l=div(cd,'mono',{left:'40px',top:(y+20)+'px',fontSize:'32px',color:'#2b2622'},r[0].toUpperCase());
    const v=div(cd,'hand',{right:'40px',top:(y)+'px',fontSize:'70px',color:r[2]},r[1]); write(v,t0+0.4+i*0.25,0.5);
    if(i<3){ const ln=div(cd,'',{position:'absolute',left:'40px',right:'40px',top:(y+110)+'px',height:'2px',background:'rgba(43,38,34,.2)'}); } });
  const sv=div(p,'hand',{left:'120px',top:'1045px',fontSize:'80px',color:'#2f5d9e'},'⤓ save this'); write(sv,T['8:Save this'],0.5);
  const sd=div(p,'card',{left:'110px',top:'1190px',width:'860px',height:'230px',background:'#f2c200'}); pop(sd,T['8:send it'],-1.5);
  div(sd,'h',{left:'40px',right:'40px',top:'30px',fontSize:'58px',textAlign:'center'},'Send this to');
  div(sd,'hand',{left:'0',width:'860px',textAlign:'center',top:'115px',fontSize:'74px',color:'#2b2622'},'whoever pays the family recharge');
  const fb=div(p,'chip',{left:'230px',top:'1490px',fontSize:'60px',background:'#2b2622',color:'#f3ecdc',borderColor:'#2b2622'},'Follow @moneyincloud'); pop(fb,T['8:Follow']);
  const srcs=['Sources: Mint/TradingView (Jio listing, Elara & Nomura, 28 Oct 2026),','DesiDime (Centrum, Jul 2026), Business Today (annual plans, 7 Sep 2026),','Cashify (Jul 2026). Hike math = my calculation. Education only.'];
  srcs.forEach((l,i)=>{ const e=div(p,'mono',{left:'0',width:'1080px',textAlign:'center',top:(1660+i*40)+'px',fontSize:'22px'},l); fade(e,t0+0.6); });
  penTo(900,S(8)+1020,T['8:Save this']-0.2,0.3); penTo(1000,S(8)+1500,T['8:Follow'],0.5);
}
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body>
</html>
'''
html = HTML.replace('__T__', json.dumps(T)).replace('__DUR__', str(T['dur']))
open(P + '/index.html', 'w').write(html)
print('wrote', P + '/index.html', T['dur'])
