#!/usr/bin/env python3
"""Build a Git-hostable portfolio from the current 40-package publication manifest.
Uses only exported publication PDFs from the non-AI collection; does not regenerate artwork.
"""
from pathlib import Path
import json, zipfile, re, html, shutil, io, hashlib, sys
from PIL import Image, ImageOps, ImageDraw
import pymupdf

ROOT=Path(__file__).resolve().parent
SOURCE=Path.home()/"Documents/Approved-Portfolio/05-Design-Upgrade-In-Progress/DELIVERY"
MANIFEST=SOURCE/"PACKAGE-MANIFEST.json"
OUT=ROOT/"dist-40"
ASSETS=OUT/"assets"
ASSETS.mkdir(parents=True,exist_ok=True)
records=json.loads(MANIFEST.read_text())
status=json.loads((SOURCE/"40-Approved-Editable-Packages/CURRENT-QUALITY-STATUS.json").read_text())
assert len(records)==40 and status["projects"]==40, "Expected the 40-project approved collection"

def slug(s): return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")
def esc(s): return html.escape(str(s),quote=True)
def choose_pdf(z, expected):
    candidates=[]
    for name in z.namelist():
        low=name.lower()
        if not low.endswith(".pdf") or any(k in low for k in ("presentation/","mockups/","/links/","/current-qa/","form-resources/","worked-example","template","test.pdf","proof.pdf")):
            continue
        priority=0
        if "screen.pdf" in low or "digital.pdf" in low: priority+=9
        if "review.pdf" in low: priority+=8
        if "fill" in low: priority+=7
        if "print" in low or "pdfx" in low: priority-=3
        candidates.append((priority,name))
    matches=[]
    for priority,name in candidates:
        try:
            data=z.read(name)
            doc=pymupdf.open(stream=data,filetype="pdf")
            pages=len(doc)
            doc.close()
            if pages==expected: matches.append((priority,len(data),name,data))
        except Exception: continue
    if not matches:
        raise RuntimeError("No publication PDF with expected "+str(expected)+" pages; candidates="+str([(p,n) for p,n in candidates]))
    matches.sort(key=lambda x:(x[0],-x[1]),reverse=True)
    return matches[0][2], matches[0][3]

def image_from_page(page,max_width):
    rect=page.rect
    scale=min(max_width/rect.width, 1.6)
    pix=page.get_pixmap(matrix=pymupdf.Matrix(scale,scale),alpha=False,colorspace=pymupdf.csRGB)
    return Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
def make_card(pages,folder):
    ims=[Image.open(folder/("page-%02d.webp"%i)).convert("RGB") for i in range(1,min(3,pages)+1)]
    canvas=Image.new("RGB",(1200,760),"#e5e3de")
    positions=[(85,90,395,560),(535,35,280,480),(820,210,295,440)]
    for i,im in enumerate(ims):
        x,y,w,h=positions[i]
        small=ImageOps.contain(im,(w,h))
        ImageDraw.Draw(canvas).rectangle((x+12,y+13,x+small.width+12,y+small.height+13),fill="#c8c6c2")
        canvas.paste(small,(x,y))
    canvas.save(folder/"card.webp",quality=83,method=5)
    canvas.save(folder/"presentation.webp",quality=84,method=5)

books=[]
for index,item in enumerate(records,1):
    title=item["project"]
    key=slug(title)
    expected=int(item["pages"])
    archive=SOURCE/item["package"]
    if not archive.is_file(): raise FileNotFoundError(archive)
    with zipfile.ZipFile(archive) as z: pdf_name,data=choose_pdf(z,expected)
    folder=ASSETS/key
    folder.mkdir(exist_ok=True)
    (folder/"publication.pdf").write_bytes(data)
    doc=pymupdf.open(stream=data,filetype="pdf")
    for n,page in enumerate(doc,1):
        file=folder/("page-%02d.webp"%n)
        im=image_from_page(page,980)
        im.save(file,"WEBP",quality=76,method=4)
        ImageOps.contain(im,(290,395)).save(folder/("thumb-%02d.webp"%n),"WEBP",quality=65,method=4)
    doc.close()
    make_card(expected,folder)
    # Categories describe publishing formats, not undisclosed customer relationships.
    lower=title.lower()
    if any(t in lower for t in ("report","index","quarterly","civic","datum","distributed","clearwater","harbor","hearthwell")): category="Reports"
    elif any(t in lower for t in ("journal","magazine","silence","material","neighbour","structure","fieldnote","slowroad")): category="Editorial"
    elif any(t in lower for t in ("catalog","pattern","thread","daily","signal","gridshift","fernloop")): category="Catalogs"
    else: category="Brochures"
    books.append(dict(title=title,slug=key,pages=expected,category=category,pdf_name=pdf_name))
    print("BUILT",index,"/40",title,expected,flush=True)

shutil.copy2(ROOT/"site.js",OUT/"site.js")
shutil.copy2(ROOT/"site.css",OUT/"site.css")
(OUT/"favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#171717"/><text x="13" y="47" fill="white" font-family="Arial" font-size="44">A</text></svg>')
def shell(page_title,desc,body):
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>'+esc(page_title)+' | Ayobami — Publication Design</title><meta name="description" content="'+esc(desc)+'"><link rel="icon" href="/favicon.svg"><link rel="stylesheet" href="/site.css"><script src="/site.js" defer></script></head><body><a class="skip" href="#main">Skip to content</a><header><a class="brand" href="/">Ayobami.<small>Publication design</small></a><button class="menu-toggle" aria-controls="main-nav" aria-expanded="false">Menu</button><nav id="main-nav" aria-label="Main navigation"><a href="/#selected">Selected work</a><a href="/#library">All publications</a><a href="/about/">About</a><a class="nav-contact" href="https://www.fiverr.com/ay_obam1" target="_blank" rel="noopener">Start a project ↗</a></nav></header>'+body+'<footer><p>40 self-initiated native publication studies. Images displayed here are rendered from actual exported InDesign publications, not AI-generated imagery. Fictional examples are not presented as client commissions.</p><a href="/credits/">Credits & production notes ↗</a><span>© 2026 Ayobami</span></footer></body></html>'

def card(b,n):
    return '<article class="project-card" data-category="'+b["category"]+'" data-search="'+esc((b["title"]+" "+b["category"]).lower())+'"><a href="/work/'+b["slug"]+'/"><div class="project-art"><img src="/assets/'+b["slug"]+'/card.webp" alt="'+esc(b["title"])+' publication page composition" width="1200" height="760" loading="lazy"></div><div class="card-info"><div><h3>'+esc(b["title"])+'</h3><p>'+b["category"]+' · '+str(b["pages"])+' pages</p></div><span class="card-num">'+str(n).zfill(2)+' ↗</span></div></a></article>'
selected_names=["Halvorsen-Quill","Silence-Quarterly","Quarterly-Index","Clearpath-Coaching","Orlathread","Calloway"]
selected=[next((x for x in books if x["title"]==v),None) for v in selected_names]
selected=[x for x in selected if x is not None]
if not selected: selected=books[:6]
shutil.copy2(ASSETS/selected[0]["slug"]/"presentation.webp",ASSETS/"hero.webp")
total=sum(x["pages"] for x in books)
home='<main id="main" class="container"><section class="hero"><div><span class="eyebrow">Independent publication design / InDesign</span><h1>Clear pages.<br><em>Distinct character.</em></h1></div><div class="hero-intro"><p>Forty publication studies, each built around the way its content deserves to be read.</p><a class="arrow-link" href="#selected">Explore selected work ↘</a></div></section>'
home+='<a class="hero-art" href="/work/'+selected[0]["slug"]+'/"><img src="/assets/hero.webp" width="1200" height="760" alt="Actual pages from '+esc(selected[0]["title"])+'"></a><div class="hero-caption"><span>'+esc(selected[0]["title"])+' / Native InDesign publication</span><span>View complete publications, not just covers.</span></div>'
home+='<section id="selected"><div class="section-head"><h2>Selected work</h2><p>A range of editorial, print and information design.</p></div><div class="featured">'+''.join(card(b,n) for n,b in enumerate(selected,1))+'</div></section>'
home+='<section class="proof-band"><div><span class="eyebrow">The page is the proof</span><h2>Beyond the<br>cover.</h2><p>Open a publication to inspect the full sequence, page by page.</p></div><div class="proof-items"><div><strong>40 publications</strong><span>Individual visual identity</span></div><div><strong>'+str(total)+' source pages</strong><span>Complete viewing copies</span></div><div><strong>Native layouts</strong><span>Created in Adobe InDesign</span></div><div><strong>Real page renders</strong><span>No AI-generated illustrations on this site</span></div></div></section>'
home+='<section id="library"><div class="section-head"><h2>Publication library</h2><p>'+str(len(books))+' publications. Browse by format or search by title.</p></div><div class="library-controls"><div class="filters">'+''.join('<button class="filter" data-filter="'+c+'" aria-pressed="'+('true' if c=="all" else 'false')+'">'+('All work' if c=="all" else c)+'</button>' for c in ["all","Catalogs","Editorial","Brochures","Reports"])+'</div><label class="search-label">Search <input class="search" type="search" placeholder="Find a publication" aria-label="Search publications"></label></div><p id="result-count" class="small-note" aria-live="polite">40 publications</p><p class="empty" hidden>No matching publications.</p><div class="library">'+''.join(card(b,n) for n,b in enumerate(books,1))+'</div></section></main>'
(OUT/"index.html").write_text(shell("Publication Design Studio","Forty original publication design studies created in Adobe InDesign.",home))
for b in books:
    t=b["title"];s=b["slug"]
    thumbs=''.join('<button class="page-thumb" data-full="/assets/'+s+'/page-%02d.webp'%n+'" data-alt="'+esc(t)+' page '+str(n)+'" aria-label="Read page '+str(n)+'"><img src="/assets/'+s+'/thumb-%02d.webp'%n+'" alt="'+esc(t)+' page '+str(n)+' thumbnail" loading="lazy"><span>Page '+str(n).zfill(2)+' / Click to read</span></button>' for n in range(1,b["pages"]+1))
    body='<main id="main" class="container"><section class="project-heading"><div class="breadcrumbs"><a href="/#library">← All publications</a> / '+b["category"]+'</div><span class="eyebrow">Native Adobe InDesign study</span><h1>'+esc(t)+'</h1><p class="deck">'+str(b["pages"])+' pages · '+b["category"]+' · Self-initiated publication study</p><a class="button" href="/assets/'+s+'/publication.pdf" target="_blank" rel="noopener">Read complete PDF ↗</a> <a class="button secondary" href="#pages">Explore every page ↓</a></section><div class="project-art"><img src="/assets/'+s+'/presentation.webp" alt="'+esc(t)+' original cover and interior pages"></div><section id="pages"><div class="section-head"><h2>Inside the publication</h2><p>All '+str(b["pages"])+' source pages.</p></div><p class="gallery-help">Select a page to read it; use the arrows or keyboard to navigate.</p><div class="page-grid">'+thumbs+'</div></section></main><dialog class="reader" id="page-reader" aria-label="'+esc(t)+' page reader"><div class="reader-bar"><strong>'+esc(t)+'</strong><div class="reader-nav"><button data-prev aria-label="Previous page">←</button><span data-counter aria-live="polite"></span><button data-next aria-label="Next page">→</button><button data-zoom aria-pressed="false">Zoom</button><button data-close aria-label="Close">Close ✕</button></div></div><div class="reader-content"><img alt=""></div></dialog>'
    target=OUT/"work"/s;target.mkdir(parents=True,exist_ok=True)
    (target/"index.html").write_text(shell(t,t+" publication design portfolio, complete InDesign document.",body))
for name,body in {"about":'<main id="main" class="container"><section class="project-heading"><h1>Publication design, built to be read.</h1><p class="deck">I design catalogs, reports, magazines, guides and brochures in Adobe InDesign. These forty studies are self-initiated examples of layout, typography, editorial sequence and production craft, not claims of paid-client engagements.</p><a class="button" href="/#library">Explore all work ↗</a></section></main>',"credits":'<main id="main" class="container"><section class="project-heading"><h1>Credits & production notes</h1><p>Images on this site are rendered from the published PDF layouts in the separate non-AI collection. Photography and other third-party content, where used, retain the credits and licences documented inside the individual editable packages. Sample data and fictional businesses should not be mistaken for measured outcomes or completed commercial work. Some projects remain in internal quality refinement.</p><p>Source INDD, IDML and rights/production registers are maintained separately from the public website.</p></section></main>'}.items():
    p=OUT/name;p.mkdir(exist_ok=True)
    (p/"index.html").write_text(shell(name.title(),name.title()+" for the publication design portfolio",body))
(OUT/"404.html").write_text(shell("Page not found","Page not found",'<main id="main" class="container"><h1>Page not found</h1><a href="/">Back to the library</a></main>'))
(OUT/"projects.json").write_text(json.dumps(books,indent=2))
host="https://ayobami-publication-studio.vercel.app"
urls=["/","/about/","/credits/"]+["/work/"+b["slug"]+"/" for b in books]
(OUT/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join("<url><loc>"+host+x+"</loc></url>" for x in urls)+"</urlset>")
(OUT/"robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: "+host+"/sitemap.xml\n")
print("COMPLETE",len(books),total,flush=True)
# Refresh the deployable snapshot only after all 40 builds finish successfully.
shutil.rmtree(ROOT/"dist",ignore_errors=True)
shutil.copytree(OUT,ROOT/"dist")
import runpy
runpy.run_path(str(ROOT/"refine-website.py"),run_name="__main__")
# Restore high-fidelity website imagery from the canonical PDFs, not prior web assets.
runpy.run_path(str(ROOT/"render-quality.py"),run_name="__main__")
# Build the client-first editorial case studies, separate archive, and portfolio PDF.
runpy.run_path(str(ROOT/"curate-portfolio.py"),run_name="__main__")
# Restore the visual archive and make original pages legible at readable size.
runpy.run_path(str(ROOT/"fix-reading-layout.py"),run_name="__main__")
print("CLIENT-FOCUSED DIST READY",flush=True)
