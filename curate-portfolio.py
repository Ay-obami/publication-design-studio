#!/usr/bin/env python3
"""Curated publication portfolio release: editorial case-study boards, separate work index,
and a vector PDF lookbook. Art and imagery come from the user's own InDesign PDF exports.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import json,re,textwrap
import pymupdf

ROOT=Path(__file__).resolve().parent
SITE=ROOT/"dist"
DATA=json.loads((SITE/"projects.json").read_text())
BY_SLUG={x["slug"]:x for x in DATA}
FEATURES=[
 dict(slug="halvorsen-quill",eyebrow="Architecture & profiles",headline="Designing clarity for a professional practice",problem="A complex practice needs a calm visual hierarchy and readable story.",solution="A restrained typographic system, strong section changes, and thoughtful interior pacing.",pages=(1,5,12),tone="folio"),
 dict(slug="silence-quarterly",eyebrow="Magazine & editorial",headline="An issue driven by imagery and editorial rhythm",problem="The subject needs visual personality without overwhelming the story.",solution="Large image moments and confident changes of pace make each section distinct.",pages=(1,8,17),tone="editorial"),
 dict(slug="quarterly-index",eyebrow="Annual reports & data",headline="Making detailed information easier to follow",problem="Information-rich reports can become dense and visually exhausting.",solution="Consistent grid, purposeful typographic levels, and breathing space between data.",pages=(1,9,18),tone="report"),
 dict(slug="clearpath-coaching",eyebrow="Guides & workbooks",headline="A workbook designed to be used, not just read",problem="Learning content needs room for action, reflection, and practical steps.",solution="Friendly hierarchy, deliberate whitespace, and a consistent reading sequence.",pages=(1,8,16),tone="workbook"),
 dict(slug="orlathread",eyebrow="Information design",headline="A compact publication with a clear message",problem="Small-format print has to communicate quickly without feeling cramped.",solution="Economical layout, a focused visual language, and careful use of each side.",pages=(1,2,2),tone="foldout"),
 dict(slug="calloway",eyebrow="Long-form corporate reports",headline="A complete report with a consistent design system",problem="Long reports need enough structure for readers to navigate multiple topics.",solution="Reusable grids and a clear section hierarchy across a substantial document.",pages=(1,14,31),tone="corporate"),
]
def html(s):return BeautifulSoup(s,"html.parser")
def get_art(page,index,slug,label):
    im=page.new_tag("img",src=f"/assets/{slug}/page-{index:02d}.webp?v=highres2",loading="lazy",decoding="async",alt=f"Original InDesign artwork, {slug.replace('-',' ')} page {index}")
    im["width"]="1200"
    return im

# Shared web headers: navigation directs users to the dedicated archive.
def update_nav(soup):
 for a in soup.select('header nav a, footer a, .breadcrumbs a'):
    href=a.get("href","")
    if href=="/#library":a["href"]="/work/"
    if href=="/#selected":a["href"]="/#selected"
 for a in soup.select('header nav a'):
    if a.get("href")=="/work/":a.string="All work"
 return soup

home_p=SITE/"index.html"
home=update_nav(html(home_p.read_text()))
library_section=home.select_one("#library")
archive_p=SITE/"work"/"index.html"
archive_p.parent.mkdir(parents=True,exist_ok=True)
if library_section:
    archive_library=str(library_section)
    library_section.decompose()
else:
    if not archive_p.exists():raise RuntimeError("Source library missing")
    archived=html(archive_p.read_text()).select_one("#library")
    if archived is None:raise RuntimeError("Archive missing section")
    archive_library=str(archived)

# New work archive: preserve thumbnails, category filters, counts, and search.
archive=html(home_p.read_text())
archive=update_nav(archive)
main=archive.select_one("main")
main.clear()
lead=html('''<section class="archive-intro"><span class="eyebrow">The complete collection / 2026</span>
<h1>Every publication,<br><em>in one place.</em></h1>
<p>Forty self-initiated Adobe InDesign studies. Browse the collection by format, search by name, or open any publication to inspect the complete page sequence.</p>
<div class="archive-meta"><span>40 publications</span><span>538 viewing-copy pages</span><a href="/downloads/ayobami-selected-publications-2026.pdf" download>Download selected portfolio PDF ↓</a></div>
</section>''')
main.append(lead)
library=html(archive_library).select_one("#library")
library["class"]=["archive-library"]
library.select_one(".section-head h2").string="Project index"
library.select_one(".section-head p").string="Search the complete archive; every entry opens a full publication."
main.append(library)
archive.title.string="All Publication Projects | Ayobami — Publication Design"
archive_p.write_text(str(archive))

# Homepage: keep featured projects, replace 40-card gallery with one simple archive invitation.
features_section=home.select_one("#selected")
selected_count=len(features_section.select(".project-card"))
assert selected_count==6,selected_count
home_cta=html('''<section class="archive-invitation"><div><span class="eyebrow">40 complete publication studies</span><h2>The rest of the collection.</h2>
<p>Browse every format and find a relevant example. The full archive has filters, search, and access to every page.</p></div>
<div class="archive-actions"><a class="button" href="/work/">Explore all 40 publications ↗</a><a class="text-link" href="/downloads/ayobami-selected-publications-2026.pdf" download>Download a curated PDF ↓</a></div></section>''')
proof=home.select_one(".proof-band")
if proof:proof.insert_after(home_cta)
else:features_section.insert_after(home_cta)
# Correct wording: source pages (542 per audit) differ from viewing PDF pages (538).
for x in home.select(".proof-items span"):
 if "Complete viewing copies" in x.text:
  prev=x.find_previous_sibling("strong")
  if prev:prev.string="538 viewing pages"
home_p.write_text(str(home))

# Individual selected-work case studies: 3 curated boards first, full pages later.
for f in FEATURES:
 slug=f["slug"]
 page_p=SITE/"work"/slug/"index.html"
 soup=update_nav(html(page_p.read_text()))
 first=soup.select_one(".project-heading")
 assert first is not None
 # Place case study directly after heading, before existing generic montage.
 old=soup.select_one(".curated-case-study")
 if old:old.decompose()
 n=BY_SLUG[slug]["pages"]
 picks=[min(max(1,i),n) for i in f["pages"]]
 case=soup.new_tag("section",attrs={"class":f"curated-case-study case-{f['tone']}","id":"case-study"})
 intro=soup.new_tag("div",attrs={"class":"case-intro"})
 intro.append(html(f'<span class="eyebrow">Art-directed case study / {f["eyebrow"]}</span><h2>{f["headline"]}</h2><div class="case-brief"><p><strong>The design challenge</strong><br>{f["problem"]}</p><p><strong>The approach</strong><br>{f["solution"]}</p></div>').select_one("span"))
 # separate nodes to avoid parser one-root restriction
 for markup in [f"<h2>{f['headline']}</h2>",f'<div class="case-brief"><p><strong>Design challenge</strong><br>{f["problem"]}</p><p><strong>Design approach</strong><br>{f["solution"]}</p></div>']:
  intro.append(next(iter(html(markup).contents)))
 case.append(intro)
 board_specs=[
  ("01","Cover & identity","The visual voice of the publication.",[picks[0]]),
  ("02","Editorial sequence","An edited look at the rhythm of the interior.",[picks[1],picks[2]]),
  ("03","Detail & structure","Typography, spacing, and content hierarchy.",[picks[2],picks[0]])
 ]
 for seq,title,caption,indices in board_specs:
  board=soup.new_tag("figure",attrs={"class":f"case-board case-board-{seq} board-{f['tone']}"})
  stage=soup.new_tag("div",attrs={"class":"case-board-stage"})
  for ix in indices:stage.append(get_art(soup,ix,slug,title))
  board.append(stage)
  cap=soup.new_tag("figcaption")
  cap.append(next(iter(html(f'<span>{seq} / 03</span><strong>{title}</strong><p>{caption}</p>').contents)))
  strong=soup.new_tag("strong");strong.string=title;cap.append(strong)
  para=soup.new_tag("p");para.string=caption;cap.append(para)
  board.append(cap)
  case.append(board)
 first.insert_after(case)
 generic=soup.select_one(".project-heading + .project-art")
 if generic:generic.decompose()
 # Existing per-page reader remains accessible and fully functional.
 for crumb in soup.select(".breadcrumbs a"):
  if crumb.get("href")=="/#library":crumb["href"]="/work/"
 page_p.write_text(str(soup))

# Add direct PDF download in top nav and page title update, preserving other content.
for p in [home_p,archive_p]:
 soup=html(p.read_text())
 nav=soup.select_one("header nav")
 if nav and not nav.select_one('a[href^="/downloads/"]'):
  a=soup.new_tag("a",href="/downloads/ayobami-selected-publications-2026.pdf")
  a.string="Portfolio PDF"
  nav.append(a)
 p.write_text(str(soup))
# Existing page links elsewhere
for p in (SITE/"work").glob("*/index.html"):
 s=p.read_text().replace('href="/#library"','href="/work/"')
 p.write_text(s)

CSS=r"""
/* Curated portfolio release: fewer home items, better evidence, separate full archive */
.archive-invitation{background:#f0eee8;margin:60px 0 95px;padding:40px 48px;display:flex;align-items:center;justify-content:space-between;gap:40px}
.archive-invitation h2{font-family:Georgia,serif;font-size:clamp(31px,4vw,55px);font-weight:400;line-height:1.1;letter-spacing:-1.7px;margin:14px 0}
.archive-invitation p{color:var(--muted);font-size:15px;max-width:600px}
.archive-actions{display:flex;align-items:start;gap:18px;flex-direction:column;flex-shrink:0}
.text-link{font-size:13px;border-bottom:1px solid currentColor;padding-bottom:6px}
.archive-intro{padding:70px 0 48px}
.archive-intro h1{font-family:Georgia,serif;font-size:clamp(46px,7vw,94px);font-weight:400;line-height:1.04;letter-spacing:-3px;margin:20px 0}
.archive-intro h1 em{color:var(--accent)}
.archive-intro p{max-width:670px;color:var(--muted);font-size:18px}
.archive-meta{display:flex;gap:25px;flex-wrap:wrap;font-size:13px;margin-top:34px;padding:17px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.archive-meta a{text-decoration:underline;text-underline-offset:4px}
.archive-library .section-head{margin:30px 0}
.archive-library .library{grid-template-columns:repeat(2,minmax(0,1fr));gap:0 30px}
.archive-library .library .project-card{grid-column:auto!important;padding:14px 0;border-bottom:1px solid var(--line)}
.archive-library .library .project-card a{display:grid;grid-template-columns:142px 1fr;gap:18px;align-items:center}
.archive-library .library .portfolio-preview,.archive-library .library .project-card.library-feature .portfolio-preview{height:105px;width:142px}
.archive-library .library .card-info{padding:0;align-items:center}
.archive-library .library .card-info h3,.archive-library .library .project-card.library-feature .card-info h3{font-size:17px}
.archive-library .library .card-info p{font-size:11px}
.archive-library .library .preview-index{font-size:7px}
.archive-library .library .card-num{display:inline;font-size:12px}
.curated-case-study{margin:25px 0 60px}
.case-intro{border-top:1px solid var(--line);padding:35px 0;display:grid;grid-template-columns:1.2fr 1fr;gap:20px}
.case-intro>.eyebrow{grid-column:1/-1}
.case-intro h2{font-family:Georgia,serif;font-size:clamp(33px,4vw,55px);font-weight:400;line-height:1.12;letter-spacing:-1.7px;max-width:650px;margin:0}
.case-brief{display:grid;gap:10px}
.case-brief p{font-size:14px;line-height:1.55;color:var(--muted);margin:0}
.case-brief strong{color:var(--ink)}
.case-board{margin:0 0 40px}
.case-board-stage{height:520px;display:flex;align-items:center;justify-content:center;gap:28px;overflow:hidden;padding:38px 10%;background:#e5e2dc}
.case-board-stage img{height:100%;width:auto;max-width:47%;min-width:0;object-fit:contain;filter:drop-shadow(7px 9px 9px #0002)}
.case-board-01 .case-board-stage img{max-width:68%}
.case-board-03 .case-board-stage{height:390px}
.case-board-03 .case-board-stage img{height:92%}
.case-board figcaption{display:flex;align-items:baseline;gap:22px;padding:14px 0 0;border-top:1px solid var(--line);margin-top:12px}
.case-board figcaption span{font-size:11px;letter-spacing:1px;color:var(--muted)}
.case-board figcaption strong{font-size:17px;font-weight:500}
.case-board figcaption p{font-size:13px;color:var(--muted);margin:0}
.case-editorial .case-board-stage{background:#33252b}
.case-report .case-board-stage{background:#dce5ec}
.case-workbook .case-board-stage{background:#e0eadf}
.case-foldout .case-board-stage{background:#e9d5be}
.case-corporate .case-board-stage{background:#293c43}
.case-folio .case-board-stage{background:#ddd6cf}
.case-board-01 .case-board-stage{height:610px}
.case-board-02 .case-board-stage{height:470px}
@media(max-width:800px){
 .archive-invitation{padding:28px;flex-direction:column;align-items:start;gap:18px}
 .case-intro{grid-template-columns:1fr}
 .case-board-stage,.case-board-01 .case-board-stage{height:430px;padding:24px 5%}
 .case-board-03 .case-board-stage{height:310px}
 .case-board figcaption{display:block}
 .case-board figcaption>*{display:block;margin:4px 0!important}
}
@media(max-width:700px){
 .archive-library .library{grid-template-columns:1fr;gap:0}
 .archive-library .library .project-card a{grid-template-columns:108px 1fr;gap:12px}
 .archive-library .library .portfolio-preview,.archive-library .library .project-card.library-feature .portfolio-preview{width:108px;height:90px}
 .archive-library .library .card-info h3{font-size:16px}
 .archive-intro{padding:40px 0 15px}
 .archive-meta{gap:14px}
 .case-board-stage,.case-board-01 .case-board-stage{height:315px}
 .case-board-02 .case-board-stage{height:300px}
 .case-board-03 .case-board-stage{height:260px}
 .case-board-stage img{max-width:45%}
}
"""
styles=SITE/"site.css"
old=styles.read_text()
if "/* Curated portfolio release:" in old:old=old.split("/* Curated portfolio release:")[0]
styles.write_text(old+CSS)

# SEO + sitemap
sitemap=SITE/"sitemap.xml"
source=sitemap.read_text()
if "<loc>https://ayobami-publication-studio.vercel.app/work/</loc>" not in source:
 source=source.replace("</urlset>","<url><loc>https://ayobami-publication-studio.vercel.app/work/</loc></url></urlset>")
 sitemap.write_text(source)

# PDF lookbook: 20-page vector PDF, live graphics taken from the original PDF files.
downloads=SITE/"downloads"
downloads.mkdir(exist_ok=True)
pdf_path=downloads/"ayobami-selected-publications-2026.pdf"
pdf=pymupdf.open()
W,H=842,595  # A4 landscape in PDF points
INK=(0.16,0.17,0.17);MID=(0.43,0.45,0.45);ACCENT=(0.68,0.31,0.23)
BG=(0.976,0.973,0.963)
def start_page(fill=BG):
 pg=pdf.new_page(width=W,height=H)
 pg.draw_rect(pymupdf.Rect(0,0,W,H),color=None,fill=fill)
 return pg
def txt(pg,pos,string,size=15,font="helv",color=INK):
 pg.insert_text(pos,string,fontsize=size,fontname=font,color=color)
def fit_source(pg,src,i,rect):
 original=src[i].rect
 pg.show_pdf_page(pymupdf.Rect(*rect),src,i,keep_proportion=True,overlay=True)
def footer(pg,num):
 txt(pg,(54,568),"AYOBAMI  /  INDEPENDENT PUBLICATION DESIGN",9,color=MID)
 txt(pg,(743,568),f"{num:02d} / 20",9,color=MID)
base=start_page()
txt(base,(56,78),"AYOBAMI    /    SELECTED PUBLICATION WORK",12,color=ACCENT)
txt(base,(56,205),"Publication design",49,font="hebo")
txt(base,(56,264),"that works for you.",41,font="hebo")
txt(base,(56,333),"Reports  /  Magazines  /  Brochures  /  Workbooks",17,color=MID)
txt(base,(56,386),"Six selected, self-initiated Adobe InDesign studies.",14)
txt(base,(56,410),"Every page shown originates in the original publication PDFs.",11,color=MID)
txt(base,(56,490),"2026  /  40 publications in the complete online portfolio",13)
footer(base,1)
npage=1
for no,f in enumerate(FEATURES,1):
 slug=f["slug"];b=BY_SLUG[slug];loc=SITE/"assets"/slug/"publication.pdf"
 src=pymupdf.open(loc)
 picks=[min(max(1,i),len(src))-1 for i in f["pages"]]
 # Intro page: cover art large on right.
 pg=start_page()
 txt(pg,(48,62),f"{no:02d}  /  {f['eyebrow'].upper()}",11,color=ACCENT)
 txt(pg,(48,120),b["title"].replace("-"," "),30,font="hebo")
 y=169
 for line in textwrap.wrap(f["headline"],49)[:2]:
  txt(pg,(48,y),line,17);y+=23
 txt(pg,(48,255),"THE DESIGN CHALLENGE",10,color=ACCENT)
 for i,line in enumerate(textwrap.wrap(f["problem"],68)[:2]):
  txt(pg,(48,278+i*21),line,11)
 txt(pg,(48,356),"THE APPROACH",10,color=ACCENT)
 for i,line in enumerate(textwrap.wrap(f["solution"],68)[:2]):
  txt(pg,(48,379+i*21),line,11)
 fit_source(pg,src,picks[0],(520,65,786,515));npage+=1;footer(pg,npage)
 # Interior spread: original vector PDF pages, side by side.
 pg=start_page()
 txt(pg,(48,58),f"{b['title'].replace('-',' ')}  /  EDITORIAL SEQUENCE",12,color=ACCENT)
 fit_source(pg,src,picks[1],(65,83,405,524))
 fit_source(pg,src,picks[2],(437,83,777,524))
 npage+=1;footer(pg,npage)
 # Detail board: focus on actual second section, generous scale, white area.
 pg=start_page(fill=(0.925,0.925,0.91))
 txt(pg,(48,55),f"{b['title'].replace('-',' ')}  /  TYPOGRAPHY & COMPOSITION",12,color=INK)
 fit_source(pg,src,picks[0],(64,84,382,518))
 fit_source(pg,src,picks[1],(459,111,763,493))
 npage+=1;footer(pg,npage)
 src.close()
last=start_page()
txt(last,(56,118),"Let's design a publication",37,font="hebo")
txt(last,(56,170),"that deserves to be read.",35,font="hebo")
txt(last,(56,259),"Services",14,color=ACCENT)
txt(last,(56,291),"Reports, magazines, catalogs, brochures, books and workbooks.",16)
txt(last,(56,363),"Portfolio: ayobami-publication-studio.vercel.app",14)
txt(last,(56,393),"Email: oyebisiayobami26@gmail.com",14)
txt(last,(56,471),"Portfolio samples are self-initiated exercises; not paid-client commissions.",10,color=MID)
npage+=1;footer(last,npage)
assert npage==20,npage
pdf.set_metadata({"title":"Ayobami — Selected Publication Design 2026","author":"Ayobami","subject":"Self-initiated InDesign publication-design portfolio"})
pdf.save(pdf_path,garbage=4,deflate=True)
pdf.close()
print("RELEASE_PREPARED",len(FEATURES),"CASE_STUDIES",len(DATA),"ARCHIVE_PROJECTS","PDF",pdf_path,pdf_path.stat().st_size,flush=True)
