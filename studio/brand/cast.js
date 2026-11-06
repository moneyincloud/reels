// moneyincloud house cartoon style: "The Cloud Family"
// Bold outline cartoon · cloud blue + gold · subtle Tamil Nadu touches.
// Usage: CAST.draw(ctx, 'appa', x, y, scale, {expr:'happy', arm:'point'})  (x,y = feet centre)
(function(){
const OL='#1B2440';            // outline ink
const LW=7;                    // outline width at scale 1
const PAL={sky:'#7EC8F2',sky2:'#BFE6FB',cloud:'#FFFFFF',gold:'#FFC531',gold2:'#E09A00',ink:OL,cream:'#FFF7E6',
  red:'#F0524A',green:'#2DB36B',teal:'#14A3A3',purple:'#7D5BD6',orange:'#FF8A3D',pink:'#FF7FA8',navy:'#2B3F8C'};
const SKIN={a:'#C98B5E',b:'#B87A4E',c:'#D9A273',d:'#A86D44'};
function S(c,fill){c.fillStyle=fill;c.fill();c.strokeStyle=OL;c.lineWidth=LW;c.lineJoin='round';c.lineCap='round';c.stroke()}
function E(c,x,y,rx,ry,fill,rot=0){c.beginPath();c.ellipse(x,y,rx,ry,rot,0,Math.PI*2);S(c,fill)}
function R(c,x,y,w,h,r,fill){c.beginPath();c.roundRect(x,y,w,h,r);S(c,fill)}
function P(c,pts,fill,close=true){c.beginPath();c.moveTo(pts[0][0],pts[0][1]);for(let i=1;i<pts.length;i++){const p=pts[i];if(p.length===4)c.quadraticCurveTo(p[0],p[1],p[2],p[3]);else c.lineTo(p[0],p[1])}if(close)c.closePath();if(fill)S(c,fill);else{c.strokeStyle=OL;c.lineWidth=LW;c.lineCap='round';c.lineJoin='round';c.stroke()}}
function L(c,x1,y1,x2,y2,w=LW,col=OL){c.beginPath();c.moveTo(x1,y1);c.lineTo(x2,y2);c.strokeStyle=col;c.lineWidth=w;c.lineCap='round';c.stroke()}
// ---- face ----
function face(c,cx,cy,r,o){const ex=r*0.36,ey=-r*0.05,er=r*0.2;
 const shock=o.expr==='shock',sad=o.expr==='sad'||o.expr==='worried',laugh=o.expr==='laugh',think=o.expr==='think',smug=o.expr==='smug';
 for(const sx of [-1,1]){E(c,cx+sx*ex,cy+ey,er,er*(shock?1.25:1.1),'#FFFFFF');
  if(laugh){c.beginPath();c.arc(cx+sx*ex,cy+ey+er*0.2,er*0.7,Math.PI*1.1,Math.PI*1.9);c.strokeStyle=OL;c.lineWidth=LW;c.stroke();continue}
  const px=think?er*0.35:smug?sx*er*0.1:0,py=think?-er*0.35:0;c.beginPath();c.arc(cx+sx*ex+px,cy+ey+py,er*(shock?0.38:0.5),0,7);c.fillStyle=OL;c.fill();
  c.beginPath();c.arc(cx+sx*ex+px-er*0.15,cy+ey+py-er*0.18,er*0.16,0,7);c.fillStyle='#fff';c.fill();
  if(o.glasses){c.beginPath();c.arc(cx+sx*ex,cy+ey,er*1.35,0,7);c.strokeStyle=OL;c.lineWidth=LW*0.8;c.stroke()}
  // brows
  const by=cy+ey-er*1.6;c.beginPath();if(sad){c.moveTo(cx+sx*ex-er*0.9*sx,by-er*0.3);c.lineTo(cx+sx*ex+er*0.6*sx,by+er*0.2)}else if(o.expr==='angry'){c.moveTo(cx+sx*ex-er*0.9*sx,by+er*0.3);c.lineTo(cx+sx*ex+er*0.6*sx,by-er*0.1)}else{c.moveTo(cx+sx*ex-er*0.8,by);c.quadraticCurveTo(cx+sx*ex,by-er*(shock?0.7:0.35),cx+sx*ex+er*0.8,by)}
  c.strokeStyle=o.browCol||OL;c.lineWidth=LW*0.9;c.stroke()}
 if(o.glasses)L(c,cx-ex+er*1.35,cy+ey,cx+ex-er*1.35,cy+ey,LW*0.8);
 // nose
 c.beginPath();c.moveTo(cx,cy+r*0.08);c.quadraticCurveTo(cx+r*0.1,cy+r*0.22,cx-r*0.02,cy+r*0.26);c.strokeStyle=OL;c.lineWidth=LW*0.7;c.stroke();
 // mouth
 const my=cy+r*0.45;c.beginPath();
 if(shock){c.ellipse(cx,my+r*0.03,r*0.14,r*0.18,0,0,7);S(c,'#7A2230')}
 else if(laugh){c.moveTo(cx-r*0.3,my-r*0.05);c.quadraticCurveTo(cx,my+r*0.4,cx+r*0.3,my-r*0.05);c.closePath();S(c,'#7A2230');c.beginPath();c.moveTo(cx-r*0.22,my);c.lineTo(cx+r*0.22,my);c.strokeStyle='#fff';c.lineWidth=LW*0.6;c.stroke()}
 else if(sad){c.arc(cx,my+r*0.18,r*0.2,Math.PI*1.15,Math.PI*1.85);c.strokeStyle=OL;c.lineWidth=LW;c.stroke()}
 else if(think){c.moveTo(cx-r*0.12,my);c.lineTo(cx+r*0.18,my-r*0.04);c.strokeStyle=OL;c.lineWidth=LW;c.stroke()}
 else if(smug){c.moveTo(cx-r*0.2,my);c.quadraticCurveTo(cx+r*0.05,my+r*0.12,cx+r*0.28,my-r*0.08);c.strokeStyle=OL;c.lineWidth=LW;c.stroke()}
 else {c.arc(cx,my-r*0.08,r*0.24,Math.PI*0.15,Math.PI*0.85);c.strokeStyle=OL;c.lineWidth=LW;c.stroke()}
 if(o.mustache){c.beginPath();c.moveTo(cx-r*0.32,my-r*0.12);c.quadraticCurveTo(cx-r*0.15,my-r*0.26,cx,my-r*0.16);c.quadraticCurveTo(cx+r*0.15,my-r*0.26,cx+r*0.32,my-r*0.12);c.quadraticCurveTo(cx,my-r*0.06,cx-r*0.32,my-r*0.12);S(c,o.hairCol||OL)}
 if(o.bindi){c.beginPath();c.arc(cx,cy-r*0.42,r*0.07,0,7);c.fillStyle=PAL.red;c.fill()}
 if(o.vibhuti){for(let k=0;k<3;k++)L(c,cx-r*0.28,cy-r*0.5+k*r*0.08,cx+r*0.28,cy-r*0.5+k*r*0.08,LW*0.5,'#F4F1EA');c.beginPath();c.arc(cx,cy-r*0.42,r*0.06,0,7);c.fillStyle=PAL.red;c.fill()}
 // cheeks
 for(const sx of [-1,1]){c.beginPath();c.ellipse(cx+sx*r*0.55,cy+r*0.3,r*0.12,r*0.07,0,0,7);c.fillStyle='rgba(240,82,74,.28)';c.fill()}
}
function head(c,cx,cy,r,o){
 // back hair
 if(o.hair==='bun'||o.hair==='braid'){E(c,cx,cy-r*0.15,r*1.08,r*1.05,o.hairCol);if(o.hair==='bun')E(c,cx+r*0.85,cy-r*0.55,r*0.38,r*0.36,o.hairCol);
  if(o.jasmine){for(let k=0;k<7;k++){c.beginPath();c.arc(cx+r*0.6+Math.cos(k*0.7-1.2)*r*0.55,cy-r*0.55+Math.sin(k*0.7-1.2)*r*0.5,r*0.09,0,7);S(c,'#FFFFFF')}}}
 // ears
 for(const sx of [-1,1])E(c,cx+sx*r*0.98,cy+r*0.08,r*0.17,r*0.24,o.skin);
 if(o.earrings)for(const sx of [-1,1]){c.beginPath();c.arc(cx+sx*r*0.98,cy+r*0.38,r*0.09,0,7);S(c,PAL.gold)}
 E(c,cx,cy,r,r*1.02,o.skin);
 // front hair
 c.save();if(o.hair==='short'){P(c,[[cx-r*0.98,cy-r*0.05],[cx-r*0.95,cy-r*0.9,cx-r*0.1,cy-r*1.12],[cx+r*0.9,cy-r*1.05,cx+r*0.98,cy-r*0.15],[cx+r*0.7,cy-r*0.55,cx+r*0.1,cy-r*0.62],[cx-r*0.6,cy-r*0.6,cx-r*0.98,cy-r*0.05]],o.hairCol)}
 else if(o.hair==='spiky'){P(c,[[cx-r*1.0,cy-r*0.1],[cx-r*0.9,cy-r*1.0],[cx-r*0.55,cy-r*0.85],[cx-r*0.35,cy-r*1.3],[cx,cy-r*0.95],[cx+r*0.3,cy-r*1.35],[cx+r*0.5,cy-r*0.9],[cx+r*0.95,cy-r*1.1],[cx+r*1.0,cy-r*0.1],[cx+r*0.6,cy-r*0.55],[cx-r*0.5,cy-r*0.6]],o.hairCol)}
 else if(o.hair==='bun'||o.hair==='braid'){P(c,[[cx-r*1.0,cy+r*0.1],[cx-r*0.95,cy-r*0.95,cx,cy-r*1.05],[cx+r*0.95,cy-r*0.95,cx+r*1.0,cy+r*0.1],[cx+r*0.7,cy-r*0.45,cx,cy-r*0.62],[cx-r*0.7,cy-r*0.45,cx-r*1.0,cy+r*0.1]],o.hairCol);L(c,cx,cy-r*1.0,cx,cy-r*0.62,LW*0.6,'#F4F1EA')}
 else if(o.hair==='bald'){P(c,[[cx-r*1.0,cy+r*0.15],[cx-r*1.02,cy-r*0.3,cx-r*0.75,cy-r*0.45],[cx-r*0.7,cy-r*0.05,cx-r*1.0,cy+r*0.15]],o.hairCol);P(c,[[cx+r*1.0,cy+r*0.15],[cx+r*1.02,cy-r*0.3,cx+r*0.75,cy-r*0.45],[cx+r*0.7,cy-r*0.05,cx+r*1.0,cy+r*0.15]],o.hairCol)}
 c.restore();
 face(c,cx,cy+r*0.08,r,o)}
// ---- bodies ----
function arm(c,x,y,dx,dy,sleeve,skin,len){const ex=x+dx*len,ey=y+dy*len;c.beginPath();c.moveTo(x,y);c.lineTo(ex,ey);c.strokeStyle=OL;c.lineWidth=34;c.lineCap='round';c.stroke();c.strokeStyle=sleeve;c.lineWidth=34-LW*2;c.stroke();
 c.beginPath();c.arc(ex,ey,15,0,7);S(c,skin)}
function body(c,o,t){const sh=-290;// shoulders y (feet at 0)
 const top=o.outfit;
 // legs / lower
 if(top==='saree'){P(c,[[-80,sh+40],[-110,-10],[110,-10],[80,sh+40]],o.c1);P(c,[[-60,sh+60],[30,sh+30],[100,-10],[40,-10]],o.c2);
  R(c,-62,-16,50,22,10,'#6B4A2A');R(c,12,-16,50,22,10,'#6B4A2A')}
 else if(top==='veshti'){P(c,[[-70,sh+150],[-82,-10],[82,-10],[70,sh+150]],'#FFFFFF');L(c,-82,-24,82,-24,LW*1.2,PAL.gold);
  R(c,-64,-16,50,22,10,'#6B4A2A');R(c,14,-16,50,22,10,'#6B4A2A')}
 else {R(c,-62,sh+150,56,sh*-1-150-10,18,o.c2);R(c,6,sh+150,56,sh*-1-150-10,18,o.c2);R(c,-70,-18,62,24,12,'#2E2E3A');R(c,8,-18,62,24,12,'#2E2E3A')}
 // torso
 if(top==='saree'){P(c,[[-78,sh],[-90,sh+50,-80,sh+130],[80,sh+130],[90,sh+50,78,sh]],o.c1);P(c,[[-60,sh-4],[70,sh+110],[90,sh+60],[20,sh-6]],o.c2)}
 else if(top==='veshti'){P(c,[[-80,sh],[-92,sh+60,-74,sh+160],[74,sh+160],[92,sh+60,80,sh]],o.c1);P(c,[[-40,sh-4],[60,sh+150],[80,sh+120],[0,sh-6]],'#FFFFFF')}
 else if(top==='hoodie'){P(c,[[-80,sh],[-94,sh+70,-78,sh+170],[78,sh+170],[94,sh+70,80,sh]],o.c1);R(c,-46,sh+90,92,46,16,o.c3||PAL.navy);L(c,-14,sh+10,-18,sh+60,LW*0.7);L(c,14,sh+10,18,sh+60,LW*0.7)}
 else {P(c,[[-80,sh],[-94,sh+70,-78,sh+165],[78,sh+165],[94,sh+70,80,sh]],o.c1);P(c,[[-22,sh-2],[0,sh+30],[22,sh-2]],o.collar||'#FFFFFF');
  if(o.tag){R(c,-30,sh+60,40,56,8,'#FFFFFF');L(c,-10,sh+30,-10,sh+60,LW*0.5)}
  if(o.pocketPen){R(c,30,sh+40,34,30,6,o.c1);L(c,40,sh+30,40,sh+50,LW*0.7,PAL.navy)}}
 // arms
 const a=o.arm||'down',sk=o.skin,sl=(top==='saree')?o.skin:(top==='veshti'?o.c1:o.c1);
 const wave=Math.sin((t||0)*6)*0.25;
 const AR={down:[[-0.25,1],[0.25,1]],point:[[-0.25,1],[0.95,-0.45]],up:[[-0.7,-0.9+wave],[0.7,-0.9-wave]],hips:[[-0.75,0.45],[0.75,0.45]],hold:[[-0.25,1],[0.6,0.35]],think:[[-0.25,1],[0.15,-0.6]],shrug:[[-0.9,-0.2],[0.9,-0.2]]}[a];
 arm(c,-78,sh+28,AR[0][0],AR[0][1],sl,sk,120);arm(c,78,sh+28,AR[1][0],AR[1][1],sl,sk,120);
 return {handR:[78+AR[1][0]*120,sh+28+AR[1][1]*120],handL:[-78+AR[0][0]*120,sh+28+AR[0][1]*120],neck:sh}}
// ---- props ----
const PROP={
 coffee(c,x,y,s=1){c.save();c.translate(x,y);c.scale(s,s);P(c,[[-26,-50],[26,-50],[18,10],[-18,10]],'#D9DDE6');P(c,[[-40,10],[40,10],[30,34],[-30,34]],'#C3C9D6');for(let k=0;k<3;k++){c.beginPath();c.moveTo(-10+k*10,-60);c.quadraticCurveTo(-20+k*10,-80,-8+k*10,-96);c.strokeStyle='rgba(27,36,64,.45)';c.lineWidth=4;c.stroke()}c.restore()},
 coin(c,x,y,r=22){E(c,x,y,r,r,PAL.gold);c.beginPath();c.arc(x,y,r*0.62,0,7);c.strokeStyle=PAL.gold2;c.lineWidth=4;c.stroke();c.fillStyle=PAL.gold2;c.font=`bold ${r}px Pop, sans-serif`;c.textAlign='center';c.textBaseline='middle';c.fillText('₹',x,y+2)},
 phone(c,x,y,s=1){c.save();c.translate(x,y);c.scale(s,s);R(c,-24,-44,48,88,10,'#2A3350');R(c,-17,-34,34,62,4,'#7EC8F2');c.restore()},
 jar(c,x,y,s=1){c.save();c.translate(x,y);c.scale(s,s);R(c,-40,-70,80,90,18,'rgba(191,230,251,.9)');R(c,-30,-86,60,20,6,PAL.gold);for(let k=0;k<5;k++)E(c,-16+(k%3)*16,-10-Math.floor(k/3)*18,12,12,PAL.gold);c.restore()},
 auto(c,x,y,s=1){c.save();c.translate(x,y);c.scale(s,s);P(c,[[-150,-20],[-150,-130],[-60,-175],[120,-175],[150,-120],[150,-20]],PAL.gold);P(c,[[-150,-130],[-60,-175],[120,-175],[130,-150],[-140,-150]],'#2B8C4E');R(c,-110,-120,90,70,10,'#BFE6FB');R(c,0,-120,110,70,10,'#BFE6FB');for(const wx of [-100,100])E(c,wx,-14,34,34,'#2E2E3A');c.restore()},
 kolam(c,x,y,r=60){c.save();c.translate(x,y);for(let i=0;i<4;i++){c.rotate(Math.PI/2);c.beginPath();c.ellipse(0,-r*0.5,r*0.25,r*0.5,0,0,7);c.strokeStyle='#FFFFFF';c.lineWidth=5;c.stroke()}for(let i=0;i<8;i++){c.beginPath();c.arc(Math.cos(i*Math.PI/4)*r*0.95,Math.sin(i*Math.PI/4)*r*0.95,4,0,7);c.fillStyle='#FFFFFF';c.fill()}c.beginPath();c.arc(0,0,6,0,7);c.fillStyle='#FFFFFF';c.fill();c.restore()},
 cloud(c,x,y,s=1){c.save();c.translate(x,y);c.scale(s,s);c.beginPath();c.arc(-50,0,40,Math.PI*0.5,Math.PI*1.5);c.arc(-10,-30,46,Math.PI,Math.PI*1.9);c.arc(45,-8,38,Math.PI*1.3,Math.PI*0.5);c.closePath();S(c,'#FFFFFF');c.restore()},
 bubble(c,x,y,w,h,text,tail='left',fill='#FFFFFF',col=OL,fs=34){R(c,x-w/2,y-h/2,w,h,h/2.2,fill);const tx=tail==='left'?x-w*0.25:x+w*0.25;P(c,[[tx-18,y+h/2-6],[tx+(tail==='left'?-30:30),y+h/2+34],[tx+18,y+h/2-6]],fill,false);c.beginPath();c.moveTo(tx-16,y+h/2-LW*0.6);c.lineTo(tx+16,y+h/2-LW*0.6);c.strokeStyle=fill;c.lineWidth=LW*1.4;c.stroke();
  c.fillStyle=col;c.font=`${fs}px Pop, sans-serif`;c.textAlign='center';c.textBaseline='middle';c.fillText(text,x,y+2)}
};
// ---- the cast ----
const CAST={
 appa:{name:'APPA · RAVI',role:'40, IT job in Chennai · salaried, busy, means well',skin:SKIN.a,hair:'short',hairCol:'#20202A',outfit:'shirt',c1:'#5BA4E6',c2:'#3B4A6B',glasses:true,mustache:true,tag:true,r:74},
 amma:{name:'AMMA · MEENA',role:'38, runs the home budget · the family\'s smartest saver',skin:SKIN.c,hair:'bun',hairCol:'#1E1A22',outfit:'saree',c1:'#2DB36B',c2:'#FFC531',bindi:true,jasmine:true,earrings:true,r:72},
 arjun:{name:'ARJUN',role:'19, college · wants F&O, crypto, quick money',skin:SKIN.c,hair:'spiky',hairCol:'#20202A',outfit:'hoodie',c1:'#FF8A3D',c2:'#2B3F8C',c3:'#E9732A',r:70},
 paati:{name:'PAATI',role:'68, trusts gold and FD · sharp, funny, wise',skin:SKIN.d,hair:'bun',hairCol:'#D9D4CF',browCol:'#9A948E',outfit:'saree',c1:'#7D5BD6',c2:'#FFC531',bindi:true,earrings:true,glasses:true,r:70},
 thatha:{name:'THATHA',role:'72, retired govt clerk · loves stories about the old Sensex',skin:SKIN.b,hair:'bald',hairCol:'#E6E2DD',outfit:'veshti',c1:'#F4F1EA',vibhuti:true,mustache:true,r:70},
 kasi:{name:'KASI MAMA',role:'neighbour · always has a "sure-shot tip"',skin:SKIN.a,hair:'short',hairCol:'#20202A',outfit:'shirt',c1:'#F0524A',c2:'#2E2E3A',collar:'#FFC531',mustache:true,pocketPen:true,r:74}
};
function draw(c,who,x,y,s=1,o={}){const ch=Object.assign({},CAST[who],o);c.save();c.translate(x,y);c.scale(s,s);
 // ground shadow
 c.beginPath();c.ellipse(0,4,110,18,0,0,7);c.fillStyle='rgba(27,36,64,.18)';c.fill();
 const b=body(c,ch,o.t);head(c,0,b.neck-ch.r*0.92,ch.r,ch);
 if(o.hold&&PROP[o.hold])PROP[o.hold](c,b.handR[0]+10,b.handR[1]-10,0.8);
 c.restore();return ch}
window.CAST={draw,PAL,PROP,CAST,OL,LW,E,R,P,L,S};
})();
