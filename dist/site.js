(()=>{'use strict';
const menu=document.querySelector('.menu-toggle'),nav=document.querySelector('header nav');
if(menu)menu.addEventListener('click',()=>{const on=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(on));nav.classList.toggle('open',on)});
const cards=[...document.querySelectorAll('.library .project-card')],search=document.querySelector('.search'),filters=[...document.querySelectorAll('.filter')],count=document.querySelector('#result-count'),empty=document.querySelector('.empty');
let category=new URLSearchParams(window.location.search).get('category')||'all';if(!['all','Reports','Editorial','Catalogs','Brochures'].includes(category))category='all';filters.forEach(f=>f.setAttribute('aria-pressed',String(f.dataset.filter===category)));
function filter(){const q=(search?.value||'').trim().toLowerCase();let n=0;cards.forEach(c=>{const show=(category==='all'||c.dataset.category===category)&&c.dataset.search.includes(q);c.hidden=!show;if(show)n++});if(count)count.textContent=n+' publication'+(n===1?'':'s');if(empty)empty.hidden=n!==0;}
filters.forEach(f=>f.addEventListener('click',()=>{category=f.dataset.filter;filters.forEach(x=>x.setAttribute('aria-pressed',String(x===f)));filter()}));if(search)search.addEventListener('input',filter);filter();filter();
const modal=document.querySelector('#page-reader');if(!modal)return;
const pages=[...document.querySelectorAll('.page-thumb')],im=modal.querySelector('img'),counter=modal.querySelector('[data-counter]'),prev=modal.querySelector('[data-prev]'),next=modal.querySelector('[data-next]'),zoom=modal.querySelector('[data-zoom]'),content=modal.querySelector('.reader-content');
let i=0,origin=null;
function show(n){i=Math.max(0,Math.min(pages.length-1,n));im.src=pages[i].dataset.full;im.alt=pages[i].dataset.alt;counter.textContent='Page '+(i+1)+' of '+pages.length;prev.disabled=i===0;next.disabled=i===pages.length-1;content.classList.remove('zoom');zoom.setAttribute('aria-pressed','false');zoom.textContent='Zoom';content.scrollTop=0;content.scrollLeft=0;}
pages.forEach((p,n)=>p.addEventListener('click',()=>{origin=p;show(n);modal.showModal();document.body.style.overflow='hidden'}));
prev.addEventListener('click',()=>show(i-1));next.addEventListener('click',()=>show(i+1));
zoom.addEventListener('click',()=>{const on=!content.classList.contains('zoom');content.classList.toggle('zoom',on);zoom.setAttribute('aria-pressed',String(on));zoom.textContent=on?'Fit page':'Zoom'});
modal.querySelector('[data-close]').addEventListener('click',()=>modal.close());
modal.addEventListener('close',()=>{document.body.style.overflow='';if(origin)origin.focus()});
modal.addEventListener('click',e=>{const r=modal.getBoundingClientRect();if(e.target===modal&&(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom))modal.close()});
document.addEventListener('keydown',e=>{if(!modal.open)return;if(e.key==='ArrowLeft'){e.preventDefault();show(i-1)}if(e.key==='ArrowRight'){e.preventDefault();show(i+1)}});
})();