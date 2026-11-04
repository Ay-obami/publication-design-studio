#!/usr/bin/env python3
"""Website-only art direction. No changes to INDD packages or source PDFs.
Run AFTER curate-portfolio.py and fix-reading-layout.py.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import json
ROOT=Path(__file__).resolve().parent;DIST=ROOT/"dist"
projects={p["slug"]:p for p in json.loads((DIST/"projects.json").read_text())}
def parse(p):return BeautifulSoup(p.read_text(),"html.parser")
def node(soup,markup):
    src=BeautifulSoup(markup,"html.parser")
    assert len(src.contents)==1,markup[:50]
    return src.contents[0]
CASES={
"halvorsen-quill":{
 "pages":[1,4,7,11,15],
 "summary":"A studio profile that needs to introduce a practice without losing the quiet confidence of its work. The design moves from an architectural cover to a consistent interior language.",
 "focus":"Restrained image use, deliberate scale changes, and a steady grid help the reader move between the practice, its thinking, and its work.",
 "caption":["A calm introduction","The profile moves from identity into substance","An editorial system that carries the long read"],
 "notes":["Scale and white space do the first work.","Interior pages need the same discipline as the cover.","A consistent system matters more than repeated effects."],
 "layout":"folio"},
"silence-quarterly":{
 "pages":[1,6,14,21,29],
 "summary":"A fashion editorial built around material, gesture, and the spaces between images. Its most important quality is the change of pace from one feature to the next.",
 "focus":"Emphasise the contrast between expressive photography and quieter reading pages instead of treating every spread as a cover.",
 "caption":["The issue establishes its visual voice","Image, pause, and editorial progression","The rhythm continues beyond the opening"],
 "notes":["An image-led opening sets the tone.","Contrasting pages keep the story moving.","The quieter pages give the imagery space."],
 "layout":"editorial"},
"quarterly-index":{
 "pages":[1,6,12,20,27],
 "summary":"A report about finding a clear argument in complex operational information. The design must make comparisons understandable before asking the reader to interpret results.",
 "focus":"A disciplined data hierarchy, comparisons placed together, and consistent editorial conventions give the numbers a readable sequence.",
 "caption":["A report, not a collection of charts","Comparisons before conclusions","Sustaining hierarchy across the document"],
 "notes":["Context gives a number its meaning.","Comparisons should be legible at a glance.","Information needs a consistent reading path."],
 "layout":"analytical"},
"clearpath-coaching":{
 "pages":[1,5,11,17,25],
 "summary":"A practical workbook where the design is part of the exercise. Readers need an inviting entry point, straightforward prompts, and enough room to write.",
 "focus":"Large working areas, small-step prompts, and a clear sequence prevent the layout from competing with the reader's own responses.",
 "caption":["An invitation to begin","Prompts become practical exercises","A sequence with room for reflection"],
 "notes":["Friendly structure makes an exercise approachable.","Writing space is a functional design decision.","The reader participates in the publication."],
 "layout":"workshop"},
"orlathread":{
 "pages":[1,2],
 "summary":"Two sides of a compact folded information piece. Its success depends on communicating the essential sequence without making either side feel crowded.",
 "focus":"The physical constraint is the design brief: a short information route, two carefully organised sides, and enough contrast to identify the next step.",
 "caption":["Side one — the opening route","Side two — the continuation"],
 "notes":["A small format requires ruthless hierarchy.","Both sides must work as one continuous sequence."],
 "layout":"folded"},
"calloway":{
 "pages":[1,3,14,29,43],
 "summary":"A substantial corporate report connecting headline performance to the chapters behind it. The design needs consistency without flattening the differences between financial information, narrative, and supporting detail.",
 "focus":"A restrained report architecture keeps long-form prose, sections, and data legible as readers move through the document.",
 "caption":["First impressions, with the numbers in view","Different sections, one report system","Details are the test of a long document"],
 "notes":["The cover provides an immediate reading direction.","Different information types need a shared grid.","The system has to endure throughout the publication."],
 "layout":"corporate"},
}
# Substantive case-study curation, no duplicated portfolio pages.
for slug,cfg in CASES.items():
    path=DIST/"work"/slug/"index.html";soup=parse(path)
    section=soup.select_one(".curated-case-study")
    assert section
    section["class"]=[v for v in section.get("class",[]) if not v.startswith("editorial-story-")]+["editorial-story-"+cfg["layout"]]
    intro=section.select_one(".case-intro")
    title=intro.select_one("h2")
    existing=intro.select_one(".editorial-context")
    if existing:existing.decompose()
    brief=intro.select_one(".case-brief")
    if brief:
        brief.clear()
        brief.append(node(soup,'<div><span class="case-brief-key">Project intention</span><p>'+cfg["summary"]+'</p></div>'))
        brief.append(node(soup,'<div><span class="case-brief-key">Design decisions</span><p>'+cfg["focus"]+'</p></div>'))
    old_note=intro.select_one(".readability-note")
    if old_note:old_note.decompose()
    intro.append(node(soup,'<p class="editorial-context">Selected pages below are from the complete publication. The original PDF and full page reader remain available for close inspection.</p>'))
    old_boards=section.select(".case-board")
    for x in old_boards:x.decompose()
    picks=cfg["pages"];n=projects[slug]["pages"]
    assert all(1<=i<=n for i in picks)
    combinations=[[picks[0]],picks[1:3],picks[3:5]] if len(picks)==5 else [[picks[0]],[picks[1]]]
    for ix,selection in enumerate(combinations):
        figure=soup.new_tag("figure",attrs={"class":f"case-board editorial-board editorial-board-{ix+1}","data-editorial-board":str(ix+1)})
        stage=soup.new_tag("div",attrs={"class":"editorial-board-stage"})
        for page_n in selection:
            image=soup.new_tag("img",src=f"/assets/{slug}/page-{page_n:02d}.webp?v=highres2",alt=f"{projects[slug]['title']}, original InDesign publication page {page_n}",loading="lazy",decoding="async")
            frame=soup.new_tag("div",attrs={"class":"editorial-page"})
            frame.append(image)
            action=soup.new_tag("button",attrs={"type":"button","class":"inspect-source","data-open-page":str(page_n)})
            action.string=f"Open page {page_n} in reader"
            frame.append(action)
            stage.append(frame)
        figure.append(stage)
        annotation=soup.new_tag("figcaption",attrs={"class":"editorial-board-caption"})
        lab=soup.new_tag("span",attrs={"class":"eyebrow"})
        lab.string=f"{ix+1:02d} / {len(combinations):02d}  —  {cfg['caption'][ix]}"
        annotation.append(lab)
        txt=soup.new_tag("p");txt.string=cfg["notes"][ix];annotation.append(txt)
        figure.append(annotation)
        section.append(figure)
    path.write_text(str(soup))
# Homepage selected work: intentional, content-specific micro-headlines.
home=DIST/"index.html";soup=parse(home)
for slug,cfg in CASES.items():
    card=soup.select_one(f'#selected .project-card a[href="/work/{slug}/"]')
    assert card
    card=card.find_parent(class_="project-card")
    card["class"]=[x for x in card.get("class",[]) if not x.startswith("editorial-feature-")]+["editorial-feature-"+cfg["layout"]]
    descriptor=card.select_one(".selected-project-descriptor")
    if descriptor:descriptor.string=cfg["summary"].split(".")[0]+"."
selected=soup.select_one("#selected .section-head")
if selected:
    heading=selected.select_one("h2")
    if heading:heading.string="Six publications. Six different design problems."
    desc=selected.select_one("p")
    if desc:desc.string="An edited starting point: from an architecture profile to a data-rich annual report. Every project opens to the actual pages."
home.write_text(str(soup))
# Archive collection introductions: orient visitors; original 40-card visual gallery untouched.
archive=DIST/"work/index.html";soup=parse(archive)
library=soup.select_one("#library");assert len(library.select(".project-card"))==40
if not soup.select_one(".editorial-collections"):
    group=node(soup,"""<section class="editorial-collections" aria-labelledby="collections-heading">
        <div class="editorial-collections-intro"><span class="eyebrow">Explore by publication type / 01–04</span><h2 id="collections-heading">Different content needs a different reading experience.</h2><p>Start with what you need to communicate. Each collection explores its own balance of structure, image, and information. All forty projects remain in the gallery below.</p></div>
        <div class="editorial-collection-grid">
          <button type="button" data-collection="Catalogs"><span class="collection-index">01 / Product-led</span><strong>Catalogs</strong><span>Comparisons, specifications, and clear product sequences.</span><span class="collection-arrow" aria-hidden="true">Explore →</span></button>
          <button type="button" data-collection="Editorial"><span class="collection-index">02 / Story-led</span><strong>Editorial</strong><span>Image, typography, and pacing across connected pages.</span><span class="collection-arrow" aria-hidden="true">Explore →</span></button>
          <button type="button" data-collection="Brochures"><span class="collection-index">03 / Purpose-led</span><strong>Brochures</strong><span>Profiles, guides, and concise communication with a clear route.</span><span class="collection-arrow" aria-hidden="true">Explore →</span></button>
          <button type="button" data-collection="Reports"><span class="collection-index">04 / Evidence-led</span><strong>Reports</strong><span>Data, narrative, and a hierarchy built for longer reading.</span><span class="collection-arrow" aria-hidden="true">Explore →</span></button>
        </div></section>""")
    library.insert_before(group)
archive.write_text(str(soup))
# A discreet route back to the work archive on all detail pages.
# Add script that uses the existing filter controls rather than duplicating their logic.
js=DIST/"site.js";code=js.read_text()
marker="/* editorial collection jump links */"
if marker not in code:
    code+="\n"+marker+"""
document.querySelectorAll('[data-collection]').forEach(link=>{
 link.addEventListener('click',()=>{
   const key=link.getAttribute('data-collection');
   const target=[...document.querySelectorAll('button[data-filter]')].find(el=>el.dataset.filter===key);
   if(target){target.click();document.querySelector('#library')?.scrollIntoView({behavior:'smooth',block:'start'});}
 });
});
"""
js.write_text(code)
css=DIST/"site.css";style=css.read_text();marker="/* Editorial studio release v3 - original design system */"
if marker in style:style=style.split(marker)[0].rstrip()+"\n"
style+=r"""
/* Editorial studio release v3 - original design system */
:root{
 --ink:#222321;--muted:#595b57;--paper:#faf9f6;--wash:#f0eee9;
 --line:#d8d4cc;--accent:#ad492c;--display:"Iowan Old Style","Baskerville","Palatino Linotype",Georgia,serif;
 --body:"Helvetica Neue","Arial",sans-serif
}
body{background:var(--paper);color:var(--ink);font-family:var(--body);line-height:1.63;-webkit-font-smoothing:antialiased}
header{height:88px}
.brand{font-size:23px;letter-spacing:-1.2px;font-weight:700}
.brand small{font-size:10px;letter-spacing:2.3px}
nav{gap:24px}
nav a:not(.nav-contact){border-bottom:1px solid transparent;padding-bottom:4px}
nav a:hover{border-bottom-color:var(--accent);text-decoration:none}
.eyebrow{font-size:10px;letter-spacing:2.1px}
.hero{padding-top:100px;padding-bottom:60px;gap:8%}
.hero h1,.archive-intro h1,.case-intro h2,.archive-invitation h2,.freelance-cta h2{font-family:var(--display);letter-spacing:-.048em}
.hero h1{font-size:clamp(56px,6.9vw,108px);line-height:.98}
.hero-intro{font-size:17px;line-height:1.7}
.section-head{margin-top:106px;border-top:1px solid var(--ink);padding-top:21px}
.section-head h2{font-family:var(--display);font-size:clamp(31px,3.3vw,49px);letter-spacing:-.035em;line-height:1.09}
.section-head p{max-width:490px;line-height:1.65}
.service-tile-info h3,.card-info h3{letter-spacing:-.035em}
#selected .featured{row-gap:64px}
#selected .card-info h3{font-family:var(--display);font-size:clamp(25px,2.25vw,34px);font-weight:400;line-height:1.1}
#selected .selected-project-descriptor{font-size:13px;line-height:1.65;max-width:440px}
#selected .selected-stage{border-radius:0;box-shadow:none}
#selected .selected-stage-heading{max-width:42%}
#selected .editorial-feature-folio .selected-stage{background:#dad1c4}
#selected .editorial-feature-folio .selected-papers .selected-sheet-1{left:52%;top:8%;width:40%;height:84%;transform:none}
#selected .editorial-feature-folio .selected-papers .selected-sheet-2{display:none}
#selected .editorial-feature-folio .selected-papers .selected-sheet-3{display:none}
#selected .editorial-feature-editorial .selected-stage{background:#272328}
#selected .editorial-feature-editorial .selected-papers .selected-sheet-1{left:39%;top:0;width:61%;height:100%;transform:none;box-shadow:none}
#selected .editorial-feature-editorial .selected-papers .selected-sheet-2{display:none}
#selected .editorial-feature-editorial .selected-stage-heading{bottom:30px;left:26px;top:auto;max-width:35%;color:#fff}
#selected .editorial-feature-analytical .selected-stage{background:#dfe9ea}
#selected .editorial-feature-analytical .selected-stage-heading{max-width:47%}
#selected .editorial-feature-analytical .selected-papers .selected-sheet-1{left:52%;top:10%;width:44%;height:82%;transform:none}
#selected .editorial-feature-analytical .selected-papers .selected-sheet-2{display:none}
#selected .editorial-feature-workshop .selected-stage{background:#e1e4d7}
#selected .editorial-feature-workshop .selected-papers .selected-sheet-1{left:45%;width:32%;top:10%;height:80%;transform:rotate(-2deg)}
#selected .editorial-feature-workshop .selected-papers .selected-sheet-2{left:71%;top:20%;width:23%;height:63%;transform:rotate(3deg)}
#selected .editorial-feature-workshop .selected-papers .selected-sheet-3{display:none}
#selected .editorial-feature-folded .selected-stage{background:#e7d0b7}
#selected .editorial-feature-folded .selected-papers .selected-sheet-1{left:40%;width:28%;top:14%;height:72%;transform:rotate(0deg)}
#selected .editorial-feature-folded .selected-papers .selected-sheet-2{left:66%;width:29%;top:14%;height:72%;transform:rotate(0deg)}
#selected .editorial-feature-corporate .selected-stage{background:#253c49}
#selected .editorial-feature-corporate .selected-stage-heading{left:27px;top:28px}
#selected .editorial-feature-corporate .selected-papers .selected-sheet-1{left:46%;width:35%;top:8%;height:85%;transform:rotate(0deg)}
#selected .editorial-feature-corporate .selected-papers .selected-sheet-2{left:75%;width:21%;top:21%;height:62%;transform:rotate(0deg)}
#selected .editorial-feature-corporate .selected-papers .selected-sheet-3{display:none}
.archive-intro{padding-top:100px}
.archive-intro h1{font-size:clamp(47px,6.9vw,92px);line-height:1}
.archive-intro p{font-size:17px;line-height:1.7}
.editorial-collections{padding:58px 0 45px;border-bottom:1px solid var(--line);margin-bottom:30px}
.editorial-collections-intro{max-width:800px}
.editorial-collections h2{font:400 clamp(30px,3.6vw,51px)/1.1 var(--display);letter-spacing:-.035em;margin:21px 0 15px}
.editorial-collections-intro>p{font-size:15px;line-height:1.7;color:var(--muted);max-width:600px}
.editorial-collection-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:40px}
.editorial-collection-grid button{text-align:left;background:#eeeae2;color:var(--ink);border:1px solid #e0ddd5;padding:23px 20px 19px;display:flex;flex-direction:column;align-items:start;gap:13px;min-width:0;min-height:220px;transition:background .2s,border-color .2s}
.editorial-collection-grid button:nth-child(2){background:#e1e1df}
.editorial-collection-grid button:nth-child(3){background:#e8dfd6}
.editorial-collection-grid button:nth-child(4){background:#dee4e4}
.editorial-collection-grid button:hover,.editorial-collection-grid button:focus-visible{background:#fff;border-color:var(--ink)}
.editorial-collection-grid .collection-index{font-size:10px;letter-spacing:1.15px;text-transform:uppercase;color:#555}
.editorial-collection-grid strong{font:400 clamp(24px,2.5vw,34px)/1.05 var(--display);letter-spacing:-.025em}
.editorial-collection-grid button>span:nth-child(3){font-size:12px;color:#555;line-height:1.5;max-width:210px}
.editorial-collection-grid .collection-arrow{margin-top:auto;font-size:13px;align-self:end}
.archive-visual-gallery .section-head{margin-top:15px}
.archive-visual-gallery .library .card-info h3{font-family:var(--display);font-weight:400;line-height:1.12}
.project-heading h1{font-family:var(--display)}
.case-intro{padding:48px 0 42px;column-gap:7%;grid-template-columns:1fr 1.06fr}
.case-intro h2{font-size:clamp(37px,4.6vw,67px);line-height:1.05}
.case-brief{align-self:center;gap:25px}
.case-brief-key{font-size:10px;letter-spacing:1.6px;text-transform:uppercase;color:var(--accent);font-weight:700}
.case-brief p{font-size:15px;line-height:1.7;margin:9px 0 0;color:#4b4b49}
.editorial-context{font-size:12px!important;line-height:1.6;color:var(--muted);grid-column:1/-1;border-top:1px solid var(--line);margin:14px 0 0;padding-top:15px}
.editorial-board{margin:0 0 72px}
.editorial-board-stage{display:flex;justify-content:center;align-items:center;gap:clamp(16px,2.5vw,36px);padding:clamp(30px,5vw,70px);background:#e7e3dc}
.editorial-page{display:flex;flex-direction:column;align-items:center;gap:20px;flex:1;min-width:0;max-width:700px}
.editorial-page img{width:auto;height:auto;max-width:100%;max-height:760px;box-shadow:0 9px 25px #0002;object-fit:contain}
.editorial-page button{background:transparent;border:0;border-bottom:1px solid currentColor;color:inherit;font-size:12px;padding:5px 0;min-height:38px}
.editorial-page button:hover{opacity:.65}
.editorial-board-1 .editorial-board-stage{min-height:600px}
.editorial-board-1 .editorial-page{max-width:650px}
.editorial-board-2 .editorial-board-stage{min-height:510px}
.editorial-board-3 .editorial-board-stage{min-height:510px}
.editorial-board-caption{display:grid;grid-template-columns:1.05fr 1fr;gap:28px;border-top:1px solid var(--line);padding:17px 0 0;align-items:baseline}
.editorial-board-caption p{font-size:15px;color:var(--muted);margin:0;line-height:1.5}
.editorial-board-caption .eyebrow{line-height:1.6;letter-spacing:1.25px}
.editorial-story-folio .editorial-board-stage{background:#dfd7cc}
.editorial-story-folio .editorial-board-3 .editorial-board-stage{background:#ede9e3}
.editorial-story-editorial .editorial-board-1 .editorial-board-stage{background:#2b2529}
.editorial-story-editorial .editorial-board-2 .editorial-board-stage{background:#ded8d3}
.editorial-story-editorial .editorial-board-3 .editorial-board-stage{background:#29272b}
.editorial-story-analytical .editorial-board-stage{background:#dce6e9}
.editorial-story-analytical .editorial-board-3 .editorial-board-stage{background:#ebf0f1}
.editorial-story-workshop .editorial-board-stage{background:#e1e8dd}
.editorial-story-workshop .editorial-board-2 .editorial-board-stage{background:#f0f1e9}
.editorial-story-folded .editorial-board-stage{background:#e6d6bf}
.editorial-story-folded .editorial-board-2 .editorial-board-stage{background:#f1e7d9}
.editorial-story-corporate .editorial-board-1 .editorial-board-stage{background:#273d48}
.editorial-story-corporate .editorial-board-2 .editorial-board-stage{background:#dce3e5}
.editorial-story-corporate .editorial-board-3 .editorial-board-stage{background:#213740}
.case-board figcaption.editorial-board-caption{display:grid;align-items:baseline;margin-top:0;border-top:1px solid var(--line);padding:17px 0 0}
@media(max-width:1020px){
 .editorial-collection-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
 .editorial-collection-grid button{min-height:190px}
 .case-intro{grid-template-columns:1fr}
 .case-brief{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media(max-width:700px){
 .hero{grid-template-columns:minmax(0,1fr)!important;gap:20px!important}
 .hero>*{min-width:0;max-width:100%;width:100%}
 .hero-intro{max-width:100%}
 header{height:78px}.hero{padding-top:56px}
 .section-head{margin-top:68px}
 #selected .featured{row-gap:38px}
 #selected .selected-stage-heading{max-width:39%}
 #selected .selected-display-title{font-size:clamp(21px,5vw,29px)}
 .archive-intro{padding-top:54px}
 .editorial-collections{padding-top:30px}
 .editorial-collections h2{font-size:33px}
 .editorial-collection-grid{gap:9px;margin-top:28px}
 .editorial-collection-grid button{padding:18px 13px 13px;min-height:211px}
 .editorial-collection-grid strong{font-size:23px}
 .editorial-collection-grid button>span:nth-child(3){font-size:11px}
 .case-brief{grid-template-columns:1fr}
 .editorial-board{margin-bottom:48px}
 .editorial-board-stage{display:flex;flex-direction:column;align-items:center;padding:20px 12px;gap:24px}
 .editorial-page{width:100%;max-width:560px}
 .editorial-page img{max-height:none;max-width:min(100%,560px)}
 .editorial-board-1 .editorial-board-stage,.editorial-board-2 .editorial-board-stage,.editorial-board-3 .editorial-board-stage{min-height:0}
 .editorial-board-caption{grid-template-columns:1fr;gap:8px}
 .case-board figcaption.editorial-board-caption{display:grid}
}
@media(max-width:375px){
 .editorial-collection-grid{grid-template-columns:1fr}
 .editorial-collection-grid button{min-height:155px}
}
@media(prefers-reduced-motion:reduce){.editorial-collection-grid button{transition:none}}
"""
css.write_text(style)
print("EDITORIAL_WEBSITE",len(CASES),"CURATED_CASES",len(library.select(".project-card")),"ARCHIVE_ITEMS",flush=True)
