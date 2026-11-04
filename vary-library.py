#!/usr/bin/env python3
"""Give each of 40 real publication previews a distinctive editorial arrangement.
This only composes already-exported PDF pages using HTML/CSS.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import json
ROOT=Path(__file__).resolve().parent
D=ROOT/"dist"
books=json.loads((D/"projects.json").read_text())
doc=BeautifulSoup((D/"index.html").read_text(),"html.parser")
cards=doc.select("#library .project-card")
assert len(cards)==40, f"Expected 40 publications; got {len(cards)}"

palettes=[
    ("#eee9e0","#272922"),("#dce4e9","#203545"),("#ecdcc9","#573b30"),
    ("#e1e7db","#2d493b"),("#e9e1e7","#413046"),("#e4e4de","#262626"),
    ("#d6e5e6","#163a49"),("#e8dacd","#633e30"),("#e1dfeb","#3b365b"),
    ("#e7e5dc","#493f31")
]
# Alternating layouts intentionally vary proportions, crops, spatial rhythm and typography.
variants=["solo","spread","overlap","folio","strip","centerpiece","split","tall","gallery","offset"]
for i,(card,b) in enumerate(zip(cards,books)):
    slug=b["slug"]; pages=int(b["pages"])
    palette=palettes[(i*3+i//4)%len(palettes)]
    v=variants[(i*7+i//5)%len(variants)]
    card["class"]=[c for c in card.get("class",[]) if not c.startswith("library-art-") and c!="library-feature"]+["library-art-"+v]+(["library-feature"] if i in (4,9,24,35) else [])
    old=card.select_one(".project-art")
    art=doc.new_tag("div",attrs={"class":"project-art portfolio-preview","style":f"--preview-bg:{palette[0]};--preview-ink:{palette[1]};"})
    page_nums=[1, max(2,min(pages,(pages//2)+1)), max(1,min(pages,pages))]
    def img(n,style):
        el=doc.new_tag("img",src=f"/assets/{slug}/page-{n:02d}.webp",alt=f"Actual page {n} of {b['title']} publication",loading="lazy")
        el["class"]=f"preview-page {style}"
        el["decoding"]="async"
        return el
    stack=doc.new_tag("div",attrs={"class":"preview-stage"})
    if v in ("solo","centerpiece","tall"):
        stack.append(img(page_nums[0],"preview-front"))
        if v=="centerpiece" and pages>=2: stack.append(img(page_nums[1],"preview-behind"))
    elif v=="spread":
        stack.append(img(page_nums[0],"preview-left"))
        stack.append(img(page_nums[1],"preview-right"))
    elif v=="strip":
        for n in page_nums[:3]:stack.append(img(n,"preview-panel"))
    elif v=="gallery":
        for n in page_nums[:3]:stack.append(img(n,"preview-gallery-page"))
    elif v=="folio":
        stack.append(img(page_nums[0],"preview-front"))
        stack.append(img(page_nums[1],"preview-inset"))
    elif v=="offset":
        stack.append(img(page_nums[0],"preview-front"))
        stack.append(img(page_nums[1],"preview-offset"))
    elif v=="split":
        stack.append(img(page_nums[0],"preview-left"))
        stack.append(img(page_nums[1],"preview-right"))
    else:
        stack.append(img(page_nums[0],"preview-front"))
        stack.append(img(page_nums[1],"preview-behind"))
    art.append(stack)
    mark=doc.new_tag("span",attrs={"class":"preview-index"})
    mark.string=f"{i+1:02d} / 40"
    art.append(mark)
    old.replace_with(art)
(D/"index.html").write_text(str(doc))
css=r"""
/* Varied library presentation — composed only from actual InDesign PDF pages */
.library .portfolio-preview{height:260px;background:var(--preview-bg);color:var(--preview-ink);position:relative;border:0;overflow:hidden;isolation:isolate}
.library .preview-stage{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
.library .preview-page{position:absolute;max-width:none;object-fit:contain;height:auto;width:auto;max-height:90%;max-width:80%;filter:drop-shadow(5px 9px 9px #0002);transition:transform .3s ease}
.library .project-card a:hover .preview-page{transform:none}
.library .preview-index{position:absolute;z-index:4;right:12px;bottom:9px;font-size:9px;letter-spacing:1.2px;font-family:monospace;font-weight:700;opacity:.8}
.library-art-solo .preview-front{height:87%;max-width:75%;transform:rotate(-2deg)}
.library-art-solo a:hover .preview-front{transform:rotate(-2deg) translateY(-5px)}
.library-art-spread .preview-left{height:71%;max-width:45%;left:9%;transform:rotate(-7deg)}
.library-art-spread .preview-right{height:78%;max-width:48%;right:8%;transform:rotate(6deg)}
.library-art-overlap .preview-front{height:78%;max-width:54%;left:11%;z-index:2;transform:rotate(-6deg)}
.library-art-overlap .preview-behind{height:72%;max-width:54%;right:7%;transform:rotate(7deg)}
.library-art-folio .preview-front{height:87%;max-width:70%;left:8%;transform:rotate(0deg)}
.library-art-folio .preview-inset{height:51%;max-width:46%;right:7%;bottom:7%;z-index:2;transform:rotate(5deg)}
.library-art-strip .preview-panel{height:63%;max-width:34%;position:relative;margin:0 -1.5%;transform:rotate(-3deg)}
.library-art-strip .preview-panel:nth-child(2){height:77%;z-index:2;transform:rotate(2deg)}
.library-art-strip .preview-panel:nth-child(3){transform:rotate(6deg)}
.library-art-centerpiece .preview-front{height:78%;max-width:64%;left:14%;z-index:2;transform:rotate(-3deg)}
.library-art-centerpiece .preview-behind{height:66%;max-width:46%;right:3%;top:9%;opacity:.85;transform:rotate(9deg)}
.library-art-split .preview-left{height:85%;max-width:44%;left:5%;transform:rotate(0deg)}
.library-art-split .preview-right{height:76%;max-width:44%;right:5%;transform:rotate(0deg)}
.library-art-tall .preview-front{height:91%;max-width:64%;left:21%;transform:rotate(3deg)}
.library-art-gallery .preview-gallery-page{height:62%;max-width:31%;position:relative;margin:0 1%;transform:translateY(-10px)}
.library-art-gallery .preview-gallery-page:nth-child(2){transform:translateY(24px)}
.library-art-gallery .preview-gallery-page:nth-child(3){transform:translateY(-16px)}
.library-art-offset .preview-front{height:77%;max-width:56%;left:8%;top:8%;z-index:2;transform:rotate(-5deg)}
.library-art-offset .preview-offset{height:73%;max-width:52%;right:7%;bottom:5%;transform:rotate(8deg)}
.library .project-card .card-info{padding-top:11px}
.library .project-card .card-info h3{font-size:18px;font-weight:500}
.library .project-card .card-info p{font-size:11px}
.library .project-card.library-feature{grid-column:span 2}
.library .project-card.library-feature .portfolio-preview{height:340px}
.library .project-card.library-feature .preview-page{max-height:92%}
.library .project-card.library-feature .card-info h3{font-size:23px}
@media(max-width:1050px){.library .portfolio-preview{height:225px}.library .project-card.library-feature .portfolio-preview{height:300px}}
@media(max-width:700px){.library .portfolio-preview{height:200px}.library .project-card.library-feature .portfolio-preview{height:255px}.library .project-card .card-info h3{font-size:15px}}
@media(max-width:420px){.library .portfolio-preview{height:175px}.library .project-card .card-info h3{font-size:14px}}
@media(prefers-reduced-motion:reduce){.library .preview-page{transition:none}}
"""
p=D/"site.css"
old=p.read_text()
if "/* Varied library presentation" in old:old=old.split("/* Varied library presentation")[0].rstrip()+"\n"
p.write_text(old+css)
print(f"Applied {len(cards)} distinct project showcases across {len(set(variants))} layout families")
