#!/usr/bin/env python3
"""Restore visual archive, improve readable case-study layouts and page inspection.
Uses real exported InDesign imagery; no image generation.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import re
ROOT=Path(__file__).resolve().parent
DIST=ROOT/"dist"
archive=DIST/"work/index.html"
s=BeautifulSoup(archive.read_text(),"html.parser")
section=s.select_one("#library")
assert section and len(section.select(".project-card"))==40
section["class"]=["archive-visual-gallery"]
heading=section.select_one(".section-head")
heading.select_one("h2").string="The complete portfolio"
heading.select_one("p").string="Explore 40 publications across reports, editorial design, catalogs, brochures and workbooks. Filter or search to find a relevant format."
archive.write_text(str(s))

# Case boards: make selected page one-per-row readable and offer an obvious
# action to open source resolution without navigating away.
selected=["halvorsen-quill","silence-quarterly","quarterly-index","clearpath-coaching","orlathread","calloway"]
for slug in selected:
    path=DIST/"work"/slug/"index.html"
    page=BeautifulSoup(path.read_text(),"html.parser")
    boards=page.select(".case-board")
    assert len(boards)==3,(slug,len(boards))
    for board in boards:
        stage=board.select_one(".case-board-stage")
        # Give each source page its own reader-sized frame instead of squeezing
        # two A4 pages into a short horizontal montage.
        stage["class"]=["case-board-stage","readable-board"]
        for image in list(stage.select("img")):
            src=image.get("src","")
            match=re.search(r"/page-(\d+)\.webp",src)
            assert match,(slug,src)
            page_number=int(match.group(1))
            if image.parent.get("class") and "readable-sheet" in image.parent.get("class",[]):
                continue
            wrapper=page.new_tag("div",attrs={"class":"readable-sheet"})
            image.wrap(wrapper)
            action=page.new_tag("button",attrs={"type":"button","class":"inspect-source","data-open-page":str(page_number)})
            action.string=f"Read page {page_number} at full resolution ↗"
            wrapper.append(action)
        if board.get("class",[])[1]=="case-board-03":
            stage["class"].append("detail-board")
    # Make introductory CTA point to the visible case rather than raw all-pages grid
    for a in page.select('.project-heading a[href="#pages"]'):
        a.string="View all pages ↓"
    # Explain distinction between sample and full PDF
    case=page.select_one(".curated-case-study")
    note=page.new_tag("p",attrs={"class":"readability-note"})
    note.string="Pages are displayed large for reading. Select “Read page at full resolution” to inspect typography and details using the native high-resolution page reader, or use the original vector PDF."
    if not case.select_one(".readability-note"):
        case.select_one(".case-intro").append(note)
    path.write_text(str(page))
    
# For non-featured publications, show a substantial actual page at readable size too.
for folder in sorted((DIST/"work").iterdir()):
    if not folder.is_dir() or folder.name in selected:continue
    page_file=folder/"index.html"
    if not page_file.is_file():continue
    page=BeautifulSoup(page_file.read_text(),"html.parser")
    if page.select_one(".reading-highlight"):continue
    gallery=page.select_one("#pages")
    if not gallery:continue
    first=page.select_one(".page-thumb")
    if first is None:continue
    first_image=first.get("data-full")
    section=page.new_tag("section",attrs={"class":"reading-highlight"})
    header=page.new_tag("div",attrs={"class":"section-head"})
    title=page.new_tag("h2");title.string="A closer look";header.append(title)
    desc=page.new_tag("p");desc.string="Actual original InDesign artwork, displayed larger. Select Read page to inspect fine details.";header.append(desc)
    section.append(header)
    img=page.new_tag("img",src=first_image,alt=f"Full-resolution {folder.name.replace('-', ' ')} publication preview",loading="lazy")
    section.append(img)
    btn=page.new_tag("button",attrs={"class":"inspect-source","type":"button","data-open-page":"1"})
    btn.string="Read page 1 at full resolution ↗"
    section.append(btn)
    gallery.insert_before(section)
    page_file.write_text(str(page))

css_path=DIST/"site.css"
css=css_path.read_text()
marker="/* Visual 40-work archive & readable case-study upgrade */"
if marker in css:css=css.split(marker)[0].rstrip()+"\n"
css+=r"""
/* Visual 40-work archive & readable case-study upgrade */
/* Remove only the compact index overrides; retain the earlier 10 compositions and hero cards. */
.archive-visual-gallery .library{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:32px 20px}
.archive-visual-gallery .library .project-card{grid-column:span 1;min-width:0;border:0;padding:0}
.archive-visual-gallery .library .project-card.library-feature{grid-column:span 2}
.archive-visual-gallery .library .project-card a{display:block}
.archive-visual-gallery .library .portfolio-preview{width:100%;height:260px}
.archive-visual-gallery .library .project-card.library-feature .portfolio-preview{width:100%;height:340px}
.archive-visual-gallery .library .card-info{display:flex;justify-content:space-between;padding:15px 0 0;align-items:start}
.archive-visual-gallery .library .card-info h3{font-size:19px}
.archive-visual-gallery .library .project-card.library-feature .card-info h3{font-size:23px}
.archive-visual-gallery .library .card-info p{font-size:12px}
.archive-visual-gallery .library .card-num{display:block;font-size:11px}
.archive-visual-gallery .library .preview-index{font-size:9px}
.archive-visual-gallery .section-head{margin:35px 0 25px}

.reading-highlight{margin:50px 0 65px;text-align:center}
.reading-highlight .section-head{text-align:left}
.reading-highlight>img{width:auto;max-width:min(100%,820px);max-height:none;display:block;margin:0 auto 18px;box-shadow:0 7px 20px #0002}
.reading-highlight .inspect-source{background:#20201d;color:#fff;border:1px solid #20201d;padding:12px 22px;min-height:44px;font-size:14px}
.reading-highlight .inspect-source:hover{background:#444}
/* Each displayed source page receives its own generous viewing area. */
.curated-case-study .readability-note{grid-column:1/-1;font-size:13px;line-height:1.6;color:var(--muted);max-width:830px;margin:6px 0 0}
.curated-case-study .readable-board{height:auto!important;min-height:0!important;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,470px),1fr));align-items:start;justify-items:center;gap:32px;padding:42px clamp(15px,4vw,65px);overflow:visible}
.curated-case-study .readable-sheet{width:100%;display:flex;flex-direction:column;align-items:center;gap:16px;min-width:0}
.curated-case-study .readable-sheet img{display:block;width:auto!important;height:auto!important;max-height:none!important;max-width:min(100%,780px)!important;object-fit:contain!important;box-shadow:0 10px 25px #0002;filter:none}
.curated-case-study .readable-sheet button{font-size:13px;border:1px solid currentColor;padding:11px 18px;background:#fff;color:#242424;min-height:44px;max-width:100%;white-space:normal}
.curated-case-study .readable-sheet button:hover{background:#242424;color:#fff}
.curated-case-study .case-board-01 .readable-board{grid-template-columns:minmax(0,1fr);padding-inline:clamp(15px,8vw,125px)}
.curated-case-study .case-board-01 .readable-sheet{max-width:760px}
.curated-case-study .detail-board .readable-sheet{max-width:700px}
.curated-case-study .case-board figcaption{margin-top:14px}
/* Preserve genuinely legible detail rather than minifying complete spreads. */
.reader{width:min(1440px,98vw);max-width:98vw;height:96vh;max-height:96vh}
.reader-content{padding:20px;height:calc(100% - 72px)}
.reader-content.zoom{justify-content:flex-start}
.reader-content.zoom img{min-width:1400px;max-width:none;width:1400px;height:auto;max-height:none;object-fit:contain}
.reader-bar button{min-height:34px}
@media(max-width:1190px){
 .archive-visual-gallery .library{grid-template-columns:repeat(3,minmax(0,1fr))}
 .archive-visual-gallery .library .project-card.library-feature{grid-column:span 2}
 .archive-visual-gallery .library .portfolio-preview{height:230px}
 .archive-visual-gallery .library .project-card.library-feature .portfolio-preview{height:295px}
 .curated-case-study .readable-board{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media(max-width:750px){
 .archive-visual-gallery .library{grid-template-columns:repeat(2,minmax(0,1fr));gap:25px 14px}
 .archive-visual-gallery .library .project-card.library-feature{grid-column:span 2}
 .archive-visual-gallery .library .portfolio-preview{height:200px}
 .archive-visual-gallery .library .project-card.library-feature .portfolio-preview{height:260px}
 .archive-visual-gallery .library .card-info h3{font-size:16px}
 .archive-visual-gallery .library .project-card.library-feature .card-info h3{font-size:19px}
 .curated-case-study .readable-board{grid-template-columns:minmax(0,1fr);padding:20px 10px;gap:28px}
 .curated-case-study .readable-sheet{width:100%;max-width:600px}
 .curated-case-study .readable-sheet img{width:100%!important;height:auto!important;max-width:100%!important}
 .reader-content.zoom img{min-width:1100px;width:1100px}
}
@media(max-width:400px){
 .archive-visual-gallery .library .portfolio-preview{height:174px}
 .archive-visual-gallery .library .project-card.library-feature .portfolio-preview{height:220px}
 .archive-visual-gallery .library .card-info h3{font-size:14px}
 .archive-visual-gallery .library .card-info p{font-size:10px}
}
"""
css_path.write_text(css)

js_path=DIST/"site.js"
js=js_path.read_text()
# Wire the case-study inspection buttons into the existing full-resolution page reader.
needle="prev.addEventListener('click',()=>show(i-1));"
inject="""document.querySelectorAll('[data-open-page]').forEach(button=>button.addEventListener('click',()=>{
 const target=Math.max(0,Number(button.dataset.openPage)-1);
 if(!pages[target])return;
 origin=button;
 show(target);
 modal.showModal();
 document.body.style.overflow='hidden';
 content.classList.remove('zoom');
 zoom.setAttribute('aria-pressed','false');
 zoom.textContent='Zoom';
}));
"""
if inject not in js:js=js.replace(needle,inject+needle)
# Fit to page is the default. Zoom remains optional and user-controlled.
js=js.replace("content.classList.add('zoom');zoom.setAttribute('aria-pressed','true');zoom.textContent='Fit page';content.scrollTop=0", "content.classList.remove('zoom');zoom.setAttribute('aria-pressed','false');zoom.textContent='Zoom';content.scrollTop=0")
js_path.write_text(js)
print("40-work visual archive restored; six case studies upgraded for readable large pages and direct inspection.")
