const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
for(const f of ['gain_cover','gain_story','loss_cover','loss_story']){await p.goto('file://'+__dirname+'/'+f+'.html');await p.waitForTimeout(500);await p.screenshot({path:f+'.jpg',quality:92,type:'jpeg'});}
await b.close();})();
