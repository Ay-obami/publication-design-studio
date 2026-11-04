const puppeteer=require('/home/ayobami/.npm/_npx/4b4c857f6efdfb61/node_modules/puppeteer');
const fs=require('fs');
(async()=>{
let b=await puppeteer.launch({headless:true,executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});let checks=[];
for(const width of [1440,1024,768,390,320]){
 let p=await b.newPage();await p.setViewport({width,height:900,deviceScaleFactor:1});
 const errors=[];p.on('pageerror',e=>errors.push(e.message));
 await p.goto('http://127.0.0.1:8765/',{waitUntil:'networkidle0'});
 await p.evaluate(async()=>{for(const el of [...document.querySelectorAll('#selected .plate-stage')]){el.scrollIntoView({behavior:'instant',block:'center'});await new Promise(r=>setTimeout(r,100))}await document.fonts.ready});
 await p.evaluate(()=>document.querySelector('#selected').scrollIntoView({behavior:'instant',block:'start'}));
 await new Promise(r=>setTimeout(r,500));
 let stats=await p.evaluate(()=>{
  const cards=[...document.querySelectorAll('#selected .editorial-plate')];
  const boxes=cards.map(card=>{
    const stage=card.querySelector('.plate-stage');const labels=stage.querySelectorAll('.plate-overline,.plate-index');
    const images=[...stage.querySelectorAll('.plate-page')].map(div=>{let r=div.getBoundingClientRect(),im=div.querySelector('img');return {width:r.width,height:r.height,naturalWidth:im.naturalWidth,complete:im.complete,visible:getComputedStyle(div).display!=='none',rect:[r.left,r.top,r.right,r.bottom]}});
    return {name:card.className,stageWidth:stage.clientWidth,stageHeight:stage.clientHeight,images,labels:[...labels].map(x=>({text:x.textContent,scroll:x.scrollWidth,width:x.clientWidth}))};
  });
  return {overflow:document.documentElement.scrollWidth>innerWidth,features:cards.length,boxes};
 });
 console.log('WIDTH',width,'overflow',stats.overflow,'features',stats.features,'artwork_loaded',stats.boxes.map(x=>x.images.filter(i=>i.visible&&i.naturalWidth>0).length).join(','),'stage_sizes',stats.boxes.map(x=>Math.round(x.stageWidth)).join(','),'errors',errors.length);
 if(width===1440||width===390){
   const s=await p.$('#selected');await s.screenshot({path:'/tmp/plates-v4-'+width+'.png',captureBeyondViewport:true});
 }
 checks.push({width,...stats,errors});await p.close();
}
await b.close();
fs.writeFileSync('/tmp/plates-v4-qa.json',JSON.stringify({checks},null,2));
if(checks.some(x=>x.overflow||x.errors.length||x.features!==6||x.boxes.some(b=>b.images.some(i=>i.visible&&!i.naturalWidth))))process.exit(1);
})().catch(e=>{console.error(e);process.exit(1)});
