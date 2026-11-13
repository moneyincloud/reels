const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:1});
await p.goto('file://'+process.cwd()+'/index.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);
const s=await p.$$('section');for(let i=0;i<s.length;i++){await s[i].screenshot({path:`slide${i+1}.png`});}
// overflow check
const o=await p.$$eval('section',ss=>ss.map((s,i)=>{const r=s.getBoundingClientRect();let bad=[];s.querySelectorAll('*').forEach(e=>{const q=e.getBoundingClientRect();if(e.classList.contains('host'))return;if(q.right>r.right-60||q.bottom>r.bottom-20)bad.push(e.className||e.tagName)});return i+1+':'+bad.join(',')}));console.log(o.join(' | '));await b.close();})();
