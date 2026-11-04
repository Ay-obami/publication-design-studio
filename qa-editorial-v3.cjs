const puppeteer=require('/home/ayobami/.npm/_npx/4b4c857f6efdfb61/node_modules/puppeteer');
const fs=require('fs');
(async()=>{
const browser=await puppeteer.launch({headless:true,executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
const result={tested:new Date().toISOString(),widths:[],projects:[],errors:[],missing:[]};
const base='http://127.0.0.1:8765';
for(const w of [1440,1024,768,390,320]){
 const p=await browser.newPage();await p.setViewport({width:w,height:900,deviceScaleFactor:1});const errors=[];
 p.on('pageerror',e=>errors.push('JS '+e.message));
 await p.goto(base+'/',{waitUntil:'networkidle0'});
 const home=await p.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,selected:document.querySelectorAll('#selected .project-card').length,serviceCards:document.querySelectorAll('.service-tile').length,selectedNames:[...document.querySelectorAll('#selected .card-info h3')].map(el=>el.textContent.trim()),unloaded:[...document.querySelectorAll('#selected .selected-stage img')].filter(i=>!i.complete && i.loading!=='lazy').length}));
 await p.goto(base+'/work/',{waitUntil:'networkidle0'});
 const archive=await p.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,cards:document.querySelectorAll('#library .project-card').length,featureCards:document.querySelectorAll('#library .library-feature').length,variantCount:new Set([...document.querySelectorAll('#library .project-card')].map(x=>[...x.classList].find(c=>c.startsWith('library-art-')))).size,collections:document.querySelectorAll('.editorial-collection-grid [data-collection]').length}));
 await p.click('[data-collection="Reports"]');
 archive.filtered=await p.evaluate(()=>({count:document.querySelectorAll('#library .project-card:not([hidden])').length,pressed:document.querySelector('.filter[data-filter="Reports"]').getAttribute('aria-pressed')}));
 await p.type('.search','quarterly');
 archive.search=await p.evaluate(()=>document.querySelector('#result-count')?.textContent);
 await p.goto(base+'/work/calloway/',{waitUntil:'networkidle0'});
 let detail=await p.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,boards:document.querySelectorAll('.editorial-board').length,pages:[...document.querySelectorAll('.editorial-page img')].map(x=>x.getAttribute('src')),description:document.querySelector('.case-brief').textContent.length,viewerThumbs:document.querySelectorAll('.page-thumb').length}));
 await p.click('.editorial-page .inspect-source');
 detail.reader=await p.evaluate(()=>({open:document.querySelector('#page-reader').open,fit:!document.querySelector('.reader-content').classList.contains('zoom'),zoomText:document.querySelector('[data-zoom]').textContent}));
 await p.keyboard.press('Escape');
 if(w===1440||w===390){
  await p.goto(base+'/work/orlathread/',{waitUntil:'domcontentloaded'});
  await p.screenshot({path:'/tmp/editorial-v3-orlathread-'+w+'.png',fullPage:false});
  await p.goto(base+'/',{waitUntil:'domcontentloaded'});
  await p.evaluate(()=>document.querySelector('#selected').scrollIntoView());
  await p.screenshot({path:'/tmp/editorial-v3-home-selected-'+w+'.png',fullPage:false});
  await p.goto(base+'/work/',{waitUntil:'domcontentloaded'});
  await p.evaluate(()=>document.querySelector('.editorial-collections').scrollIntoView());
  await p.screenshot({path:'/tmp/editorial-v3-collections-'+w+'.png',fullPage:false});
 }
 result.widths.push({width:w,home,archive,detail,errors});
 if(home.overflow||archive.overflow||detail.overflow||!detail.reader.fit||archive.cards!==40||archive.collections!==4||archive.filtered.pressed!=='true'||errors.length) result.errors.push(w);
 await p.close();
}
for(const slug of ['halvorsen-quill','silence-quarterly','quarterly-index','clearpath-coaching','orlathread','calloway']){
 const p=await browser.newPage();await p.goto(base+'/work/'+slug+'/',{waitUntil:'domcontentloaded'});
 const q=await p.evaluate(()=>({boards:document.querySelectorAll('.editorial-board').length,pages:[...document.querySelectorAll('.editorial-page img')].map(x=>x.getAttribute('src').split('?')[0]),images:[...document.querySelectorAll('.editorial-page img')].map(x=>x.getAttribute('src'))}));
 const missing=[];for(const url of q.images){const response=await p.goto(base+url,{waitUntil:'domcontentloaded'});if(response.status()!==200)missing.push(url);}
 if(new Set(q.pages).size!==q.pages.length||missing.length)result.missing.push({slug,missing,duplicates:q.pages});
 result.projects.push({slug,boards:q.boards,pageCount:q.pages.length,unique:new Set(q.pages).size});
 await p.close();
}
await browser.close();
fs.writeFileSync('/tmp/editorial-v3-qa.json',JSON.stringify(result,null,2));
console.log('QA_SUMMARY',JSON.stringify({widths:result.widths.map(x=>({width:x.width,home:x.home.selected,archive:x.archive.cards,variants:x.archive.variantCount,collections:x.archive.collections,filter:x.archive.filtered,overflow:[x.home.overflow,x.archive.overflow,x.detail.overflow],reader:x.detail.reader,jsErrors:x.errors})),projects:result.projects,errors:result.errors,missing:result.missing},null,2));
if(result.errors.length||result.missing.length)process.exit(1);
})().catch(e=>{console.error(e);process.exit(1)});
