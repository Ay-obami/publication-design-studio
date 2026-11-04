#!/usr/bin/env python3
"""Polish homepage presentation without altering any publication sources.
Art sources are original exported InDesign pages. Last pass after editorial-plates-v4.py.
"""
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parent
SITE=ROOT/"dist"
home=SITE/"index.html"
soup=BeautifulSoup(home.read_text(),"html.parser")

# Replace repeated Halvorsen hero with the multi-discipline, original-publication sequence.
hero=soup.select_one("a.hero-art, div.hero-gallery")
assert hero is not None
hero.name="div"
hero["class"]=["hero-art","hero-gallery"]
hero.attrs.pop("href",None)
hero.clear()
# No artwork is fabricated or AI-generated; page images are high-resolution InDesign exports.
items=[
    ("material",1,"editorial","Material magazine cover"),
    ("gridshift",3,"systems","Gridshift operational information page"),
    ("stillhouse",1,"identity","Stillhouse hospitality publication cover"),
    ("northline",1,"guides","Northline visitor guide cover")
]
for index,(slug,page,role,alt) in enumerate(items,1):
    figure=soup.new_tag("figure",attrs={"class":f"hero-gallery-panel hero-gallery-panel-{index} hero-gallery-{role}"})
    img=soup.new_tag("img",src=f"/assets/{slug}/page-{page:02d}.webp?v=highres2",alt=alt,loading="eager" if index<=2 else "lazy",decoding="async")
    figure.append(img)
    hero.append(figure)
label=soup.new_tag("span",attrs={"class":"hero-gallery-label"})
label.string="Selected publication disciplines."
hero.append(label)
caption=soup.select_one(".hero-caption")
assert caption is not None
caption.clear()
p=soup.new_tag("span");p.string="Editorial / Information / Identity / Guides";caption.append(p)
a=soup.new_tag("a",href="/work/")
a.string="Explore the complete portfolio ↗"
caption.append(a)
# Fix stale service filter URLs: archive filtering already supports ?category=...
for a in soup.select(".services-feature a.service-tile"):
    href=a.get("href","")
    if href.startswith("/?category="):
        a["href"]="/work/"+href[1:]
# Better client-facing descriptions; avoid multiple reiterations of 'not AI generated'.
services=soup.select_one("#services .section-head p")
if services:
    services.string="Find the right visual approach for your content, from information-rich reports to image-led editorial work."
proof=soup.select_one(".proof-band")
if proof:
    intro=proof.select_one("p")
    if intro:intro.string="Explore the complete document behind each design, not just a polished cover."
    cells=proof.select(".proof-items>div")
    if len(cells)==4:
        cells[0].select_one("strong").string="40 publications"
        cells[0].select_one("span").string="Across different formats and purposes"
        cells[1].select_one("strong").string="538 viewing pages"
        cells[1].select_one("span").string="Complete page sequences"
        cells[2].select_one("strong").string="Original documents"
        cells[2].select_one("span").string="Created using Adobe InDesign"
        cells[3].select_one("strong").string="Full-page readers"
        cells[3].select_one("span").string="Explore the layouts at your own pace"
# Refine selected section introductory copy.
selected=soup.select_one("#selected .section-head")
if selected:
    h=selected.select_one("h2")
    if h:h.string="Six projects. Six different ways of thinking."
    p=selected.select_one("p")
    if p:p.string="A closer look at architecture, editorial, reporting, learning and information design."
# Avoid repeated explanation in the archive invitation; make transition less bulky.
inv=soup.select_one(".archive-invitation")
if inv:
    head=inv.select_one("h2")
    if head:head.string="There's more to explore."
    body=inv.select_one("p")
    if body:body.string="Browse the full collection by format, or open any publication to see every page."
# Explicit local anchor semantics preserve browser keyboard navigation.
home.write_text(str(soup))

css_path=SITE/"site.css"
css=css_path.read_text()
marker="/* Final visual polish v5: multi-publication hero and page rhythm */"
if marker in css:css=css.split(marker)[0].rstrip()+"\n"
css+=r"""
/* Final visual polish v5: multi-publication hero and page rhythm */
.hero{padding-top:clamp(64px,6vw,88px);padding-bottom:34px}
.hero h1{margin-bottom:0}
.hero-gallery{height:clamp(380px,38vw,485px);display:grid;grid-template-columns:1fr 1.18fr 1fr 1.18fr;align-items:center;justify-items:center;gap:clamp(10px,2vw,29px);padding:clamp(40px,4vw,60px) clamp(30px,5vw,80px);background:#e7e4df;border:none;overflow:hidden;isolation:isolate}
.hero-gallery-panel{position:relative;margin:0;min-width:0;width:100%;display:flex;align-items:center;justify-content:center;max-height:100%;height:87%;box-shadow:0 13px 28px #0002;background:#fbfaf6;overflow:hidden}
.hero-gallery-panel img{height:100%;width:100%;max-width:100%;object-fit:contain;aspect-ratio:auto;display:block}
.hero-gallery-panel-1{height:83%;transform:translateY(12px)}
.hero-gallery-panel-2{height:91%;transform:translateY(-7px)}
.hero-gallery-panel-3{height:79%;transform:translateY(15px)}
.hero-gallery-panel-4{height:89%;transform:translateY(-8px)}
.hero-gallery-label{position:absolute;left:22px;bottom:14px;font-size:10px;text-transform:uppercase;letter-spacing:.14em;color:#424440}
.hero-caption{padding:13px 0 10px;border-bottom:1px solid var(--line);line-height:1.5}
.hero-caption a{text-decoration:underline;text-underline-offset:4px}
.services-feature{margin:6px 0 0}
.services-feature .section-head{margin-top:46px}
#selected .section-head{margin-top:88px}
#selected .featured{row-gap:clamp(34px,4vw,56px)}
#selected .card-info{padding-top:13px}
#selected .selected-project-descriptor{margin-top:5px}
#selected .plate-folio .plate-stage{height:490px}
#selected .plate-report .plate-stage{height:495px}
#selected .plate-fashion .plate-stage,#selected .plate-data .plate-stage{height:475px}
#selected .plate-workbook .plate-stage,#selected .plate-fold .plate-stage{height:445px}
.proof-band{margin-top:67px;padding:42px 46px}
.proof-band h2{font-size:38px}
.proof-band .proof-items{gap:20px}
.archive-invitation{margin:40px 0 70px;padding:32px 40px}
.archive-invitation h2{margin:9px 0}
.freelance-process .section-head{margin-top:70px}
.freelance-cta{margin-top:68px;margin-bottom:63px;padding-top:45px}
@media(min-width:1500px){
 #selected .plate-folio .plate-stage{height:540px}
 #selected .plate-report .plate-stage{height:535px}
}
@media(max-width:960px){
 .hero-gallery{height:375px;gap:13px;padding:45px 32px}
 #selected .plate-folio .plate-stage,#selected .plate-report .plate-stage{height:425px}
 #selected .plate-fashion .plate-stage,#selected .plate-data .plate-stage,#selected .plate-workbook .plate-stage,#selected .plate-fold .plate-stage{height:380px}
 .proof-band{padding:32px}
}
@media(max-width:700px){
 .hero{padding-top:46px}
 .hero-gallery{height:345px;grid-template-columns:1fr 1fr 1fr;gap:11px;padding:42px 16px 38px}
 .hero-gallery-panel{height:86%;transform:none}
 .hero-gallery-panel-1{height:80%}
 .hero-gallery-panel-2{height:94%}
 .hero-gallery-panel-3{display:none}
 .hero-gallery-panel-4{height:84%}
 .hero-gallery-label{font-size:8px;letter-spacing:.07em;bottom:10px;left:13px}
 .hero-caption{align-items:start;flex-direction:column;gap:5px}
 #selected .section-head{margin-top:60px}
 #selected .plate-folio .plate-stage,#selected .plate-report .plate-stage,#selected .plate-fashion .plate-stage,#selected .plate-data .plate-stage,#selected .plate-workbook .plate-stage,#selected .plate-fold .plate-stage{height:340px}
 .proof-band{margin-top:48px}
 .archive-invitation{padding:25px;margin:30px 0 55px}
 .freelance-process .section-head{margin-top:55px}
 .freelance-cta{margin-top:53px;margin-bottom:45px}
}
@media(max-width:360px){
 .hero-gallery{height:285px}
 #selected .plate-folio .plate-stage,#selected .plate-report .plate-stage,#selected .plate-fashion .plate-stage,#selected .plate-data .plate-stage,#selected .plate-workbook .plate-stage,#selected .plate-fold .plate-stage{height:300px}
}
"""
css_path.write_text(css)
print("POLISH_OK",len(hero.select("img")),"HERO_IMAGES",len(soup.select("#selected .editorial-plate")),"FEATURED",len(soup.select(".service-tile")),"SERVICES",flush=True)
