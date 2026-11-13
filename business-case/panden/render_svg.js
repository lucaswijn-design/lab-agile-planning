// gebruik: node shot.js <svg|html> <png> [breedte]
const {chromium}=require('playwright');
(async()=>{const [src,out,w]=process.argv.slice(2);const b=await chromium.launch();
const p=await b.newPage({viewport:{width:+(w||1400),height:800}});
if(src.endsWith('.svg')){const fs=require('fs');await p.setContent('<html><body style="margin:0">'+fs.readFileSync(src,'utf8')+'</body></html>');}
else await p.goto('file://'+src);
await p.waitForTimeout(300);
const h=await p.evaluate(()=>document.body.scrollHeight);await p.setViewportSize({width:+(w||1400),height:h});
await p.screenshot({path:out});await b.close()})();
