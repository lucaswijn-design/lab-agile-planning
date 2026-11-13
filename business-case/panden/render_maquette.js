// Maquettebeelden uit ontwerpen.html renderen (headless, swiftshader). three.js lokaal: zie make_render_pack.py.
// node maq.js <html> <three-pkg> <outdir> <json [{p,mode,view,l1,naam}]> [w] [h]
const {chromium}=require('playwright');
(async()=>{const [page,three,out,list,W,H]=process.argv.slice(2);const items=JSON.parse(list);
const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:+(W||1600),height:+(H||1200)},deviceScaleFactor:1});
await p.route('**/three.min.js',r=>r.fulfill({path:three+'/build/three.min.js',contentType:'application/javascript'}));
await p.route('**/OrbitControls.js',r=>r.fulfill({path:three+'/examples/js/controls/OrbitControls.js',contentType:'application/javascript'}));
const seen=new Set();p.on('pageerror',e=>{if(!seen.has(e.message)){seen.add(e.message);console.log('ERR',e.message)}});
await p.goto('file://'+page);await p.waitForFunction(()=>window.__m&&window.__m.ready,null,{timeout:60000});
await p.addStyleTag({content:'.wrap{max-width:none;padding:0}.wrap>*:not(.stage){display:none}.stage{grid-template-columns:1fr}.side,.hud,.cams{display:none!important}.view{aspect-ratio:auto;height:100vh;border:0}'});
let last=-1;
for(const it of items){
  if(it.p!==last){await p.evaluate(i=>window.__m.kies(i),it.p);last=it.p;}
  await p.evaluate(it=>{window.__m.setL1(it.l1!==false);window.__m.setMode(it.mode);window.__m.view(it.view);},it);
  await p.waitForTimeout(1500);
  await p.locator('#view canvas').screenshot({path:out+'/'+it.naam+'.png'});console.log('ok',it.naam);
}
await b.close();})();
