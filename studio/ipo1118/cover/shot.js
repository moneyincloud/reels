const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
for(const n of ['cover','story']){await p.goto('file://'+__dirname+'/'+n+'.html');await p.waitForTimeout(500);await p.screenshot({path:__dirname+'/'+n+'.jpg',type:'jpeg',quality:92});}
await b.close();})();
