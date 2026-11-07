#!/usr/bin/env python3
"""Apply the freelance-focused design layer to the real 40-publication website.
Artwork references are existing exported Adobe InDesign pages; no images are generated.
Run after build-40.py or to refresh the checked-in dist snapshot.
"""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parent
D=ROOT/"dist"
if not (D/"index.html").exists(): raise SystemExit("Run from a source checkout with dist/index.html")
home=(D/"index.html").read_text()
def actual(title,slug,category,modifier,pages,promise,detail):
    return f'''<a class="service-tile service-{modifier}" href="/?category={category}#library" aria-label="Explore {title} projects">
      <div class="service-art">
        <div class="service-art-type"><span class="service-small">DESIGNED TO BE READ</span><strong>{title}</strong></div>
        <div class="service-publication service-publication-primary"><img src="/assets/{slug}/page-01.webp" alt="Real InDesign cover from {pages}" loading="lazy"></div>
        <div class="service-publication service-publication-secondary"><img src="/assets/{slug}/page-02.webp" alt="Real interior page from {pages}" loading="lazy"></div>
        <span class="service-art-mark">0{['reports','editorial','catalogs','workbooks'].index(modifier)+1}</span>
      </div>
      <div class="service-tile-info"><div><h3>{title}</h3><p>{promise}</p><small>{detail}</small></div><span aria-hidden="true">↗</span></div>
    </a>'''
tiles=[
    actual("Reports &amp; company profiles","quarterly-index","Reports","reports","Quarterly Index","Structured, readable, and built for complex information.","Annual reports · Business reports · Company profiles"),
    actual("Magazines &amp; editorial","material","Editorial","editorial","Material","Editorial rhythm, strong typography, and stories that flow.","Magazines · Journals · Newsletters"),
    actual("Catalogs &amp; brochures","fernloop","Catalogs","catalogs","Fernloop","Clear product information with a distinct visual identity.","Catalogs · Lookbooks · Brochures"),
    actual("Books &amp; workbooks","clearpath-coaching","Brochures","workbooks","Clearpath Coaching","Long-form reading, learning materials, and usable page layouts.","Guides · Workbooks · Interactive PDFs")
]
categories='''<section class="services-feature" id="services"><div class="section-head"><h2>What I can design for you</h2><p>Choose the type of publication you need. Each example uses real pages from my InDesign portfolio, not generated mockups.</p></div><div class="service-gallery">'''+''.join(tiles)+'''</div><p class="service-disclosure">Publication design and production by Ayobami.</p></section>'''
# Remove any previous inserted categories and process sections to make reruns idempotent.
home=re.sub(r'<section class="services-feature" id="services">.*?</section>','',home,flags=re.S)
home=re.sub(r'<section class="freelance-process" id="process">.*?</section>','',home,flags=re.S)
home=re.sub(r'<section class="freelance-cta" id="contact">.*?</section>','',home,flags=re.S)
home=home.replace('<section id="selected">',categories+'<section id="selected">',1)
home=home.replace('Clear pages.<br><em>Distinct character.</em>','Publication design<br><em>that works for you.</em>')
home=home.replace('Publications built around the way their content deserves to be read.','I design magazines, catalogs, reports, brochures and workbooks in Adobe InDesign. See real page layouts, inspect complete publications, and find an approach that fits your content.')
home=home.replace('Explore selected work ↘','See what I design ↘')
home=home.replace('href="#selected">See what I design','href="#services">See what I design')
home=home.replace('A range of editorial, print and information design.','Selected publication studies. Open any project for the full PDF and every page.')
process='''<section class="freelance-process" id="process"><div class="section-head"><h2>How I work with you</h2><p>A straightforward process with clear deliverables and review points.</p></div><div class="freelance-steps">
<article><span>01 / BRIEF</span><h3>Tell me what you're making</h3><p>We define the publication, audience, content, page count, format and final use.</p></article>
<article><span>02 / DIRECTION</span><h3>Agree on a visual style</h3><p>We review a cover and representative spread before the full layout is developed.</p></article>
<article><span>03 / LAYOUT</span><h3>Build the full document</h3><p>I apply the agreed type, grid, imagery and information hierarchy across your pages.</p></article>
<article><span>04 / HANDOVER</span><h3>Review and receive your files</h3><p>We complete agreed revisions and prepare the relevant PDF, INDD and IDML deliverables.</p></article></div></section>'''
cta='''<section class="freelance-cta" id="contact"><div><span class="eyebrow">HAVE A PUBLICATION IN MIND?</span><h2>Let's make it<br><em>easy to read.</em></h2><p>Send me a short description of your project, approximate page count, and when you need it. I'll help you work out the right layout and deliverables.</p></div><a class="button" href="mailto:oyebisiayobami26@gmail.com?subject=Publication%20design%20enquiry">Email me about your publication ↗</a></section>'''
home=home.replace('</main>',process+cta+'</main>',1)
(D/"index.html").write_text(home)
# Update information architecture for commercial clients.
for page in ["index.html","about/index.html","credits/index.html"]:
 p=D/page
 html=p.read_text()
 if '<a href="/#services">Services</a>' not in html:
  html=html.replace('<a href="/#selected">Selected work</a>','<a href="/#services">Services</a><a href="/#selected">Selected work</a>')
 html=html.replace('<a href="/#library">All publications</a>','<a href="/#library">All publications</a>')
 if page=="index.html":
  html=html.replace('Publication design / InDesign','Freelance publication designer / Adobe InDesign')
 p.write_text(html)
# Project pages also lead clients to service context.
for p in (D/"work").glob("*/index.html"):
 txt=p.read_text()
 if '<a href="/#services">Services</a>' not in txt:
  txt=txt.replace('<a href="/#selected">Selected work</a>','<a href="/#services">Services</a><a href="/#selected">Selected work</a>')
 p.write_text(txt)

css='''

/* 2026 client-first portfolio: four independent presentation directions made from
   actual exported pages. No AI imagery or manufactured page artwork. */
:root{--ink:#20201d;--accent:#b85335;--wash:#f4f2ee}
.hero{grid-template-columns:1.45fr 1fr}.hero h1{font-size:clamp(50px,6.5vw,103px);letter-spacing:-4px;max-width:1000px}
.hero-intro{max-width:450px;color:#4d4d4a}
.services-feature{margin:25px 0 75px}
.services-feature .section-head{margin-top:48px}
.service-gallery{display:grid;grid-template-columns:1fr 1fr;gap:30px 24px}
.service-tile{display:block;color:var(--ink);text-decoration:none}
.service-tile:hover{text-decoration:none}
.service-art{height:365px;position:relative;overflow:hidden;border-radius:4px;isolation:isolate}
.service-art-type{position:absolute;z-index:3;left:28px;top:26px;max-width:48%;line-height:1}
.service-art-type strong{display:block;font-size:clamp(23px,2.6vw,41px);line-height:1.08;letter-spacing:-1.7px;font-weight:500}
.service-small{display:block;font-size:9px;font-weight:700;letter-spacing:1.6px;margin-bottom:13px}
.service-art-mark{position:absolute;right:25px;bottom:17px;font-size:14px;z-index:4;letter-spacing:2px;font-weight:700}
.service-publication{position:absolute;overflow:hidden;box-shadow:9px 12px 28px #0003;background:white;z-index:2}
.service-publication img{height:100%;width:100%;object-fit:contain;display:block}
.service-publication-primary{width:31%;height:72%;left:48%;top:13%;transform:rotate(-9deg)}
.service-publication-secondary{width:27%;height:64%;left:67%;top:26%;transform:rotate(9deg)}
.service-reports .service-art{background:#dce1e5;color:#172e45}
.service-reports .service-art-type{left:30px;top:40px}
.service-reports .service-publication-primary{width:31%;height:82%;left:47%;top:10%;transform:rotate(0deg)}
.service-reports .service-publication-secondary{width:28%;height:72%;left:66%;top:21%;transform:rotate(0deg)}
.service-editorial .service-art{background:#35292e;color:#fff}
.service-editorial .service-art-type{left:28px;top:auto;bottom:26px;max-width:38%}
.service-editorial .service-art-type strong{font-family:Georgia,serif;font-size:clamp(26px,3.1vw,47px);font-style:italic;letter-spacing:-2px}
.service-editorial .service-publication-primary{width:31%;height:85%;left:44%;top:6%;transform:rotate(-7deg)}
.service-editorial .service-publication-secondary{width:31%;height:81%;left:65%;top:10%;transform:rotate(7deg)}
.service-catalogs .service-art{background:#e8dabf;color:#3e382e}
.service-catalogs .service-art-type{left:30px;top:34px}
.service-catalogs .service-art-type strong{font-family:Arial,sans-serif;font-size:clamp(25px,2.9vw,45px);font-weight:800;letter-spacing:-2.4px;text-transform:uppercase}
.service-catalogs .service-publication-primary{width:32%;height:81%;left:41%;top:10%;transform:rotate(-11deg)}
.service-catalogs .service-publication-secondary{width:31%;height:68%;left:66%;top:25%;transform:rotate(11deg)}
.service-workbooks .service-art{background:#dce9df;color:#1e4b43}
.service-workbooks .service-art-type{left:30px;top:32px}
.service-workbooks .service-art-type strong{font-family:Georgia,serif;font-size:clamp(25px,2.9vw,43px);font-weight:400;letter-spacing:-1.4px}
.service-workbooks .service-publication-primary{width:29%;height:78%;left:49%;top:11%;transform:rotate(-3deg)}
.service-workbooks .service-publication-secondary{width:30%;height:68%;left:69%;top:24%;transform:rotate(4deg)}
.service-tile-info{display:flex;justify-content:space-between;gap:20px;padding:16px 3px 0}
.service-tile-info h3{font-size:22px;font-weight:500;letter-spacing:-.5px;margin:0 0 3px}
.service-tile-info p{font-size:14px;line-height:1.4;margin:0;color:#565650}
.service-tile-info small{display:block;font-size:11px;margin-top:10px;color:#797871}
.service-tile-info>span{font-size:22px}
.service-disclosure{font-size:12px;color:var(--muted);margin:25px 0 0}
.freelance-steps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px}
.freelance-steps article{border-top:1px solid #999;padding-top:15px}
.freelance-steps span{font-size:10px;letter-spacing:1.5px;color:var(--accent);font-weight:700}
.freelance-steps h3{font-size:20px;line-height:1.2;letter-spacing:-.6px;font-weight:500;margin:22px 0 10px}
.freelance-steps p{font-size:14px;color:var(--muted)}
.freelance-cta{margin:90px 0 80px;border-top:1px solid var(--line);padding:55px 0 0;display:flex;align-items:end;justify-content:space-between;gap:30px}
.freelance-cta h2{font-family:Georgia,serif;font-size:clamp(44px,5vw,76px);font-weight:400;letter-spacing:-2.7px;line-height:1.05;margin:22px 0 12px}
.freelance-cta em{color:var(--accent)}
.freelance-cta p{font-size:15px;color:var(--muted);max-width:540px}
.freelance-cta .button{white-space:nowrap}
@media(max-width:900px){.service-art{height:300px}.service-art-type strong{font-size:25px}.freelance-steps{grid-template-columns:1fr 1fr}}
@media(max-width:700px){.hero h1{font-size:clamp(46px,10vw,65px);letter-spacing:-2.5px}.service-gallery{grid-template-columns:1fr;gap:30px}.service-art{height:285px}.service-art-type strong{font-size:30px}.service-editorial .service-art-type strong{font-size:32px}.service-catalogs .service-art-type strong{font-size:30px}.service-tile-info h3{font-size:20px}.freelance-steps{grid-template-columns:1fr 1fr;gap:15px}.freelance-steps h3{font-size:17px}.freelance-cta{flex-direction:column;align-items:start;margin:60px 0 55px}.freelance-cta .button{width:100%;text-align:center}}
@media(max-width:380px){.service-art{height:252px}.service-art-type strong{font-size:24px}.freelance-steps{grid-template-columns:1fr}}
'''
p=D/"site.css"
existing=p.read_text()
if '/* 2026 client-first portfolio:' in existing:existing=existing.split('/* 2026 client-first portfolio:')[0].rstrip()+"\n"
p.write_text(existing+css)
# First load honours category link params, and points directly to real projects.
p=D/"site.js";js=p.read_text()
js=js.replace("let category='all';","let category=new URLSearchParams(window.location.search).get('category')||'all';if(!['all','Reports','Editorial','Catalogs','Brochures'].includes(category))category='all';filters.forEach(f=>f.setAttribute('aria-pressed',String(f.dataset.filter===category)));")
js=js.replace("if(search)search.addEventListener('input',filter);","if(search)search.addEventListener('input',filter);filter();")
p.write_text(js)
print("Client-first portfolio applied; all visual previews use real exported PDF page images.")

# Final layout pass: prevent type/artwork collisions and vary all 40 library visuals.
p=D/"site.css"
fix=r"""
/* Reserve separate visual zones for category typography and actual page previews. */
.service-art-type{max-width:40%;width:40%;left:25px;z-index:5;overflow-wrap:normal;}
.service-art-type strong{font-size:clamp(22px,2.2vw,33px);line-height:1.09;letter-spacing:-1.2px;overflow-wrap:break-word;}
.service-art .service-publication-primary{left:52%;width:25%;max-height:77%;} 
.service-art .service-publication-secondary{left:74%;right:2%;width:23%;max-height:70%;}
.service-reports .service-art-type{left:28px;top:35px;max-width:38%;width:38%;}
.service-reports .service-art-type strong{font-size:clamp(22px,2.2vw,32px);}
.service-reports .service-publication-primary{left:51%;width:27%;top:12%;}
.service-reports .service-publication-secondary{left:75%;width:23%;top:22%;}
.service-editorial .service-art-type{left:27px;bottom:30px;max-width:37%;width:37%;}
.service-editorial .service-art-type strong{font-size:clamp(23px,2.7vw,38px);}
.service-editorial .service-publication-primary{left:51%;width:27%;}
.service-editorial .service-publication-secondary{left:74%;width:24%;}
.service-catalogs .service-art-type{left:26px;max-width:39%;width:39%;}
.service-catalogs .service-art-type strong{font-size:clamp(20px,2.3vw,32px);letter-spacing:-1.1px;overflow-wrap:anywhere;}
.service-catalogs .service-publication-primary{left:50%;width:27%;}
.service-catalogs .service-publication-secondary{left:75%;width:24%;}
.service-workbooks .service-art-type{left:26px;max-width:39%;width:39%;}
.service-workbooks .service-art-type strong{font-size:clamp(21px,2.3vw,31px);}
.service-workbooks .service-publication-primary{left:52%;width:26%;}
.service-workbooks .service-publication-secondary{left:75%;width:23%;}
@media(max-width:1000px){.service-art-type strong{font-size:23px!important}.service-small{font-size:8px;letter-spacing:1px}.service-art .service-publication-primary{left:52%;width:26%}.service-art .service-publication-secondary{left:75%;width:23%}}
@media(max-width:1000px){.service-art .service-publication-primary{left:60%!important;width:20%!important}.service-art .service-publication-secondary{left:81%!important;right:0!important;width:18%!important}}\n@media(max-width:700px){.service-art-type{left:16px!important;max-width:42%!important;width:42%!important}.service-art-type strong{font-size:clamp(20px,5.2vw,27px)!important;letter-spacing:-.7px!important}.service-art .service-publication-primary{left:51%;width:26%;}.service-art .service-publication-secondary{left:75%;width:23%;}.service-art-mark{right:10px;bottom:8px}.service-small{font-size:7px;letter-spacing:.7px}}
"""
s=p.read_text()
if "/* Reserve separate visual zones" in s:s=s.split("/* Reserve separate visual zones")[0].rstrip()+"\n"
p.write_text(s+fix)
import runpy
runpy.run_path(str(ROOT/"vary-library.py"),run_name="__main__")
runpy.run_path(str(ROOT/"vary-selected.py"),run_name="__main__")
