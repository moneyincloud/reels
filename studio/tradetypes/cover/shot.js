const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+__dirname+'/'+(process.argv[2]||'cover')+'.html');await p.waitForTimeout(600);await p.screenshot({path:(process.argv[2]||'cover')+'.jpg',type:'jpeg',quality:92});await b.close();})();
