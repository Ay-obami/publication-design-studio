#!/usr/bin/env python3
"""Six individually art-directed selected-work features.
Renders ONLY real publication pages from the already-built InDesign PDF exports.
No generated images, no mutations to source PDFs or native documents.
"""
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parent
D=ROOT/"dist"
p=D/"index.html"
soup=BeautifulSoup(p.read_text(),"html.parser")
selected=soup.select("#selected .project-card")
assert len(selected)==6, len(selected)

directions=[
    ("halvorsen-quill","folio","HALVORSEN / QUILL","ARCHITECTURE & CORPORATE PROFILE","A confident, structured profile. Editorial pacing and considered use of space.","01","Architecture profile"),
    ("silence-quarterly","fashion","SILENCE","FASHION & EDITORIAL","An expressive, image-led issue built around texture, gesture and restraint.","02","Fashion editorial"),
    ("quarterly-index","data","QUARTERLY INDEX","REPORT & DATA STORYTELLING","A detailed report that gives complex operational data a readable rhythm.","03","Business report"),
    ("clearpath-coaching","workbook","CLEARPATH","INTERACTIVE WORKBOOK","A guided workbook designed for practical reading and writing.","04","Guided workbook"),
    ("orlathread","fold","ORLATHREAD","FOLDED INFORMATION DESIGN","Compact information architecture, built for a tactile folding format.","05","Fold-out brochure"),
    ("calloway","industrial","CALLOWAY","LONG-FORM COMPANY REPORT","A comprehensive publication with a distinct industrial visual system.","06","Company report")
]
for card, (slug,style,name,discipline,summary,number,kind) in zip(selected,directions):
    old=card.select_one(".project-art")
    assert old is not None and (old.select_one("img").get("src")==f"/assets/{slug}/card.webp" or "selected-stage" in old.get("class",[])), (slug,old.get("class",[]))
    pages=sorted((D/"assets"/slug).glob("page-*.webp"))
    assert len(pages)>=2, (slug,len(pages))
    n=len(pages)
    indices=([1, min(5,n),min(12,n)] if n>5 else [1,2,min(3,n)])
    art=soup.new_tag("div",attrs={"class":f"project-art selected-stage selected-{style}"})
    kicker=soup.new_tag("div",attrs={"class":"selected-stage-heading"})
    over=soup.new_tag("span",attrs={"class":"selected-overline"})
    over.string=discipline
    kicker.append(over)
    h=soup.new_tag("strong",attrs={"class":"selected-display-title"})
    h.string=name
    kicker.append(h)
    art.append(kicker)
    gallery=soup.new_tag("div",attrs={"class":"selected-papers"})
    for i,idx in enumerate(indices):
        fig=soup.new_tag("div",attrs={"class":f"selected-sheet selected-sheet-{i+1}"})
        im=soup.new_tag("img",src=f"/assets/{slug}/page-{idx:02d}.webp",
          alt=f"Original page {idx} from {name} InDesign publication",
          loading="lazy",decoding="async")
        fig.append(im);gallery.append(fig)
    art.append(gallery)
    counter=soup.new_tag("span",attrs={"class":"selected-stage-index"})
    counter.string=number+" / 06"
    art.append(counter)
    old.replace_with(art)
    info=card.select_one(".card-info")
    desc=info.select_one("p")
    desc.string=kind+" · "+str(n)+" pages"
    extra=soup.new_tag("p",attrs={"class":"selected-project-descriptor"})
    extra.string=summary
    for previous in card.select(".selected-project-descriptor"): previous.decompose()
    info.insert_after(extra)
    card["class"]=[x for x in card.get("class",[]) if not x.startswith("selected-")]+["project-card",f"selected-feature-{style}"] if "project-card" not in card.get("class",[]) else [x for x in card["class"] if not x.startswith("selected-feature-")]+[f"selected-feature-{style}"]
p.write_text(str(soup))

css=r"""
/* Selected projects: six bespoke editorial compositions from actual InDesign page exports. */
#selected .featured{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:36px 22px}
#selected .featured>.project-card{grid-column:span 6;min-width:0}
#selected .featured>.project-card:nth-child(1),
#selected .featured>.project-card:nth-child(4){grid-column:span 7}
#selected .featured>.project-card:nth-child(2),
#selected .featured>.project-card:nth-child(3){grid-column:span 5}
#selected .featured>.project-card:nth-child(5){grid-column:span 5}
#selected .featured>.project-card:nth-child(6){grid-column:span 7}
#selected .selected-stage{position:relative;overflow:hidden;height:390px;border:0;isolation:isolate}
#selected .selected-stage-heading{position:absolute;left:24px;top:23px;z-index:4;max-width:39%;line-height:1.12}
#selected .selected-overline{display:block;font-size:9px;letter-spacing:1.5px;font-weight:800;line-height:1.35;margin-bottom:14px}
#selected .selected-display-title{display:block;font-size:clamp(23px,2.4vw,43px);font-weight:500;line-height:1.04;letter-spacing:-1.4px;overflow-wrap:break-word}
#selected .selected-stage-index{position:absolute;right:17px;bottom:14px;z-index:4;font-size:10px;letter-spacing:1.6px;font-weight:700}
#selected .selected-papers{position:absolute;inset:0}
#selected .selected-sheet{position:absolute;box-shadow:8px 12px 24px #0003;background:#fff;overflow:hidden;display:flex;align-items:center;justify-content:center}
#selected .selected-sheet img{display:block;object-fit:contain;width:100%;height:100%;max-width:100%;max-height:100%;aspect-ratio:auto;transition:none}
#selected .project-card a:hover img{transform:none}
#selected .selected-project-descriptor{font-size:13px;color:var(--muted);line-height:1.5;margin:8px 0 0;max-width:580px}
#selected .card-info{padding-top:16px}
#selected .card-info h3{font-size:25px;font-weight:500}
#selected .selected-folio{background:#d8d3cd;color:#242522}
#selected .selected-folio .selected-display-title{font-family:Georgia,serif;font-size:clamp(22px,2.5vw,43px);font-weight:400}
#selected .selected-folio .selected-sheet-1{left:46%;top:9%;width:30%;height:78%;transform:rotate(-3deg)}
#selected .selected-folio .selected-sheet-2{left:68%;top:22%;width:27%;height:66%;transform:rotate(3deg)}
#selected .selected-folio .selected-sheet-3{left:35%;top:38%;width:20%;height:48%;transform:rotate(-8deg)}
#selected .selected-fashion{background:#2b2527;color:#f7e9e2}
#selected .selected-fashion .selected-stage-heading{left:24px;top:auto;bottom:32px}
#selected .selected-fashion .selected-display-title{font-family:Georgia,serif;font-size:clamp(27px,3.8vw,58px);font-weight:400;font-style:italic;letter-spacing:-2px}
#selected .selected-fashion .selected-sheet-1{left:39%;top:6%;width:39%;height:81%;transform:rotate(-8deg)}
#selected .selected-fashion .selected-sheet-2{left:69%;top:14%;width:26%;height:69%;transform:rotate(8deg)}
#selected .selected-fashion .selected-sheet-3{display:none}
#selected .selected-data{background:#dbe6ec;color:#162f3b}
#selected .selected-data .selected-stage-heading{max-width:44%}
#selected .selected-data .selected-display-title{font-family:Arial,Helvetica,sans-serif;font-weight:800;font-size:clamp(22px,2.7vw,42px);text-transform:uppercase;letter-spacing:-1.5px}
#selected .selected-data .selected-sheet-1{left:53%;top:12%;width:32%;height:78%;transform:none}
#selected .selected-data .selected-sheet-2{left:76%;top:25%;width:21%;height:57%;transform:none}
#selected .selected-data .selected-sheet-3{display:none}
#selected .selected-workbook{background:#e4e9dd;color:#254c3b}
#selected .selected-workbook .selected-display-title{font-family:Georgia,serif;font-size:clamp(26px,3vw,48px);font-weight:400}
#selected .selected-workbook .selected-sheet-1{left:46%;top:9%;width:31%;height:78%;transform:rotate(-1deg)}
#selected .selected-workbook .selected-sheet-2{left:68%;top:18%;width:26%;height:70%;transform:rotate(5deg)}
#selected .selected-workbook .selected-sheet-3{left:35%;top:49%;width:20%;height:40%;transform:rotate(-7deg)}
#selected .selected-fold{background:#e9d4c3;color:#633b30}
#selected .selected-fold .selected-stage-heading{max-width:39%}
#selected .selected-fold .selected-display-title{font-size:clamp(22px,2.9vw,42px);font-weight:800;letter-spacing:-2px}
#selected .selected-fold .selected-sheet-1{left:43%;top:13%;width:27%;height:68%;transform:rotate(-10deg)}
#selected .selected-fold .selected-sheet-2{left:66%;top:22%;width:29%;height:61%;transform:rotate(8deg)}
#selected .selected-fold .selected-sheet-3{display:none}
#selected .selected-industrial{background:#243740;color:#edf3f1}
#selected .selected-industrial .selected-display-title{font-size:clamp(27px,3.3vw,55px);letter-spacing:-2px;font-weight:800}
#selected .selected-industrial .selected-sheet-1{left:44%;top:12%;width:32%;height:72%;transform:rotate(-6deg)}
#selected .selected-industrial .selected-sheet-2{left:68%;top:16%;width:27%;height:71%;transform:rotate(6deg)}
#selected .selected-industrial .selected-sheet-3{left:35%;top:47%;width:20%;height:40%;transform:rotate(-10deg)}
@media(max-width:1050px){
 #selected .selected-stage{height:320px}
 #selected .selected-stage-heading{max-width:42%;left:18px;top:20px}
 #selected .selected-display-title{font-size:clamp(18px,2.4vw,30px)!important}
 #selected .selected-fashion .selected-stage-heading{top:auto;bottom:20px}
 #selected .selected-overline{font-size:8px;letter-spacing:.8px}
}
@media(max-width:700px){
 #selected .featured>.project-card{grid-column:1/-1!important}
 #selected .selected-stage{height:300px}
 #selected .selected-stage-heading{max-width:42%;left:15px}
 #selected .selected-display-title{font-size:clamp(22px,5.3vw,34px)!important}
 #selected .selected-overline{font-size:7px;letter-spacing:.7px}
 #selected .card-info h3{font-size:21px}
 #selected .selected-project-descriptor{font-size:12px}
}
@media(max-width:380px){
 #selected .selected-stage{height:240px}
 #selected .selected-display-title{font-size:21px!important}
 #selected .selected-stage-heading{max-width:42%;left:12px;top:16px}
 #selected .selected-fashion .selected-stage-heading{top:auto;bottom:16px}
}
"""
p=D/"site.css";old=p.read_text()
if "/* Selected projects: six bespoke" in old:old=old.split("/* Selected projects: six bespoke")[0].rstrip()+"\n"
css += r"""
/* Collision-proof art direction: title on left, real page imagery on right. */
#selected .selected-stage-heading{left:22px;top:22px;bottom:auto;max-width:38%;width:38%;}
#selected .selected-fashion .selected-stage-heading{left:22px;top:25px;bottom:auto;}
#selected .selected-sheet-1{left:53%;width:24%;max-width:24%;top:10%;height:78%;}
#selected .selected-sheet-2{left:75%;width:22%;max-width:22%;top:21%;height:66%;}
#selected .selected-sheet-3{display:none;}
#selected .selected-fashion .selected-sheet-1,#selected .selected-folio .selected-sheet-1,#selected .selected-workbook .selected-sheet-1,#selected .selected-industrial .selected-sheet-1,#selected .selected-data .selected-sheet-1,#selected .selected-fold .selected-sheet-1{left:54%;width:23%;top:10%;height:78%;}
#selected .selected-fashion .selected-sheet-2,#selected .selected-folio .selected-sheet-2,#selected .selected-workbook .selected-sheet-2,#selected .selected-industrial .selected-sheet-2,#selected .selected-data .selected-sheet-2,#selected .selected-fold .selected-sheet-2{left:76%;width:21%;top:20%;height:68%;}
#selected .selected-stage-heading .selected-display-title{overflow-wrap:anywhere;hyphens:auto;font-size:clamp(20px,2.1vw,34px);}
@media(max-width:1050px){#selected .selected-stage-heading{left:14px;max-width:38%;width:38%}#selected .selected-fashion .selected-stage-heading{left:14px;top:20px;bottom:auto}#selected .selected-display-title{font-size:clamp(17px,2.2vw,27px)!important}}
@media(max-width:700px){#selected .selected-stage-heading{left:12px;top:17px;max-width:39%;width:39%}#selected .selected-fashion .selected-stage-heading{left:12px;top:17px;bottom:auto}#selected .selected-display-title{font-size:clamp(18px,4.1vw,28px)!important}#selected .selected-sheet-1,#selected .selected-sheet-2{max-width:none}}
@media(max-width:380px){#selected .selected-display-title{font-size:17px!important}}
"""
css += r"""\n/* Different rhythms: print folio, fashion issue, data dashboard, workbook, foldout, company report. */
#selected .selected-folio{height:430px;background:linear-gradient(115deg,#d8d3cd 45%,#e9e6e0 45%)}
#selected .selected-folio .selected-sheet-1{transform:rotate(-6deg);height:80%;top:8%}
#selected .selected-folio .selected-sheet-2{transform:rotate(5deg);top:17%}
#selected .selected-fashion{height:350px;background:#33252c}
#selected .selected-fashion .selected-display-title{font-family:Georgia,serif;font-style:italic;font-size:clamp(25px,2.8vw,44px)}
#selected .selected-fashion .selected-sheet-1{transform:rotate(-9deg);height:87%;top:7%}
#selected .selected-fashion .selected-sheet-2{transform:rotate(7deg);height:72%;top:17%}
#selected .selected-data{height:350px;background:#d5e0e9}
#selected .selected-data .selected-display-title{font-family:Arial,sans-serif;text-transform:uppercase;letter-spacing:-1.3px;font-weight:800}
#selected .selected-data .selected-sheet-1{transform:none;height:82%;top:9%}
#selected .selected-data .selected-sheet-2{transform:none;height:62%;top:21%}
#selected .selected-workbook{height:440px;background:#e1ebe1}
#selected .selected-workbook .selected-sheet-1{transform:rotate(-3deg);height:83%;top:10%}
#selected .selected-workbook .selected-sheet-2{transform:rotate(4deg);height:73%;top:18%}
#selected .selected-fold{height:300px;background:#efdbbe}
#selected .selected-fold .selected-display-title{font-family:Arial,sans-serif;font-weight:800;letter-spacing:-1.5px}
#selected .selected-fold .selected-sheet-1{transform:rotate(-8deg);height:72%;top:14%}
#selected .selected-fold .selected-sheet-2{transform:rotate(10deg);height:67%;top:18%}
#selected .selected-industrial{height:435px;background:#26383d}
#selected .selected-industrial .selected-display-title{font-size:clamp(24px,3vw,45px);font-weight:800;text-transform:uppercase}
#selected .selected-industrial .selected-sheet-1{transform:rotate(-5deg);height:80%;top:9%}
#selected .selected-industrial .selected-sheet-2{transform:rotate(6deg);height:76%;top:16%}
@media(max-width:1000px){#selected .selected-stage{height:300px}#selected .selected-folio,#selected .selected-workbook,#selected .selected-industrial{height:340px}}
@media(max-width:700px){#selected .selected-stage{height:285px!important}}
@media(max-width:380px){#selected .selected-stage{height:235px!important}}
"""
p.write_text(old+css)
print("Selected section rebuilt with six independently composed editorial layouts and real project pages.")
