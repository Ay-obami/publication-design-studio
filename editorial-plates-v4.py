#!/usr/bin/env python3
"""Six editorial plates, composed from source publication pages (no generated art).
Website-only layer applied after editorial-website-v3.py.
"""
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parent
DIST=ROOT/"dist"
path=DIST/"index.html"
soup=BeautifulSoup(path.read_text(),"html.parser")
projects=[
("halvorsen-quill","folio",[(1,"cover"),(6,"feature"),(11,"feature")],"Architecture / studio profile","A practice introduced through scale, space, and a quieter visual rhythm."),
("silence-quarterly","fashion",[(1,"cover"),(8,"detail")],"Fashion / editorial","Cloth, image, and pause shape the rhythm of the issue."),
("quarterly-index","data",[(1,"cover"),(8,"analysis"),(14,"analysis")],"Operations / information design","A report that makes comparison as important as the numbers themselves."),
("clearpath-coaching","workbook",[(6,"exercise"),(11,"exercise")],"Learning / workbook","Open working pages give the reader room to think and act."),
("orlathread","fold",[(1,"front"),(2,"back")],"Fold-out / information design","Two sides, one continuous information route."),
("calloway","report",[(1,"cover"),(3,"inside"),(29,"inside")],"Annual report / corporate","A full-length report, from cover story to accountability in the details.")
]
for idx,(slug,kind,imgs,genre,copy) in enumerate(projects,1):
 card=soup.select_one(f'#selected .project-card a[href="/work/{slug}/"]')
 assert card is not None,slug
 article=card.find_parent("article")
 article["class"]=["project-card","editorial-plate","plate-"+kind]
 old=card.select_one(".selected-stage, .plate-stage")
 assert old
 stage=soup.new_tag("div",attrs={"class":"plate-stage plate-stage-"+kind})
 # The artwork's display order and relative scale are the actual editorial design.
 group=soup.new_tag("div",attrs={"class":"plate-artworks"})
 for num,role in imgs:
  sheet=soup.new_tag("div",attrs={"class":f"plate-page plate-page-{role}"})
  image=soup.new_tag("img",src=f"/assets/{slug}/page-{num:02d}.webp?v=highres2",
     alt=f"{slug.replace('-', ' ')} — original Adobe InDesign publication page {num}",loading="lazy",decoding="async")
  sheet.append(image)
  group.append(sheet)
 stage.append(group)
 over=soup.new_tag("span",attrs={"class":"plate-overline"})
 over.string=genre
 stage.append(over)
 num=soup.new_tag("span",attrs={"class":"plate-index"})
 num.string=f"{idx:02d} / 06"
 stage.append(num)
 old.replace_with(stage)
 info=card.select_one(".card-info")
 num_el=info.select_one(".card-num")
 if num_el:num_el.decompose()
 info.select_one("h3").string=slug.replace("-"," ").title().replace("Quill","Quill").replace("Clearpath Coaching","Clearpath Coaching").replace("Quarterly Index","Quarterly Index").replace("Silence Quarterly","Silence Quarterly")
 descriptor=card.select_one(".selected-project-descriptor")
 if descriptor:descriptor.string=copy
 # card title stays outside artwork; no overlaid giant words or broken wrapping.
path.write_text(str(soup))
csspath=DIST/"site.css";css=csspath.read_text()
marker="/* Editorial Plates v4: six art-directed compositions */"
if marker in css:css=css.split(marker)[0]
css+=r"""
/* Editorial Plates v4: six art-directed compositions */
#selected .featured{
 display:grid;
 grid-template-columns:repeat(12,minmax(0,1fr));
 column-gap:clamp(16px,2vw,32px);
 row-gap:clamp(52px,5.5vw,84px)
}
#selected .featured>.editorial-plate{grid-column:span 6;min-width:0}
/* Match the specificity of the older nth-child rules instead of fighting them. */
#selected .featured>.project-card:nth-child(1),
#selected .featured>.project-card:nth-child(6){grid-column:1/-1}
#selected .featured>.project-card:nth-child(2),
#selected .featured>.project-card:nth-child(5){grid-column:span 5}
#selected .featured>.project-card:nth-child(3),
#selected .featured>.project-card:nth-child(4){grid-column:span 7}
#selected .editorial-plate>a{display:block;text-decoration:none}
#selected .plate-stage{
 position:relative;isolation:isolate;overflow:hidden;
 height:clamp(370px,36vw,510px);
 border:0;border-radius:0
}
#selected .plate-overline{
 position:absolute;z-index:5;left:24px;top:20px;
 font-family:var(--body);font-size:10px;
 font-weight:700;letter-spacing:.14em;text-transform:uppercase;
 color:inherit;line-height:1.4
}
#selected .plate-index{
 position:absolute;z-index:5;right:20px;bottom:16px;
 font-size:11px;letter-spacing:.14em;font-weight:700;color:inherit
}
#selected .plate-artworks{position:absolute;inset:0;z-index:1;display:flex;align-items:center;justify-content:center;gap:18px;padding:50px 42px 42px}
#selected .plate-page{min-width:0;max-height:100%;overflow:hidden;box-shadow:0 12px 30px #0002;background:#fff;display:flex;align-items:center;justify-content:center}
#selected .plate-page img{display:block;object-fit:contain;width:100%;height:100%;max-height:100%;aspect-ratio:auto;transform:none!important;transition:none}
#selected .card-info{padding:20px 0 0}
#selected .card-info h3{font-size:clamp(25px,2.5vw,37px);font-family:var(--display);font-weight:400;letter-spacing:-.045em;margin:0}
#selected .card-info p{font-size:12px;margin:6px 0 0;letter-spacing:.025em}
#selected .selected-project-descriptor{max-width:660px;line-height:1.6;font-size:14px;margin-top:10px;color:var(--muted)}
/* Plate 1: wide architectural triptych with a quiet asymmetric rhythm. */
#selected .plate-folio .plate-stage{height:520px;background:#dedbd4;color:#403f3a}
#selected .plate-folio .plate-artworks{padding:54px 8% 39px;gap:clamp(20px,3vw,50px)}
#selected .plate-folio .plate-page-cover{height:91%;width:29%;flex:none}
#selected .plate-folio .plate-page-feature{height:77%;width:24%;flex:none}
#selected .plate-folio .plate-page-feature:last-child{height:88%;width:25%}
#selected .plate-folio .plate-page img{object-fit:contain}
/* Plate 2: dark fashion field, immersive dominant cover and narrow detail. */
#selected .plate-fashion .plate-stage{height:545px;background:#221d22;color:#f6eee9}
#selected .plate-fashion .plate-artworks{padding:48px 34px 30px 34px;gap:9px;align-items:stretch}
#selected .plate-fashion .plate-page-cover{width:67%;height:100%;box-shadow:none;background:#221d22}
#selected .plate-fashion .plate-page-detail{width:30%;height:74%;align-self:center;box-shadow:none;background:#221d22}
#selected .plate-fashion .plate-overline{color:#fff}
/* Plate 3: the operational system becomes a visual spread, not a mini cover. */
#selected .plate-data .plate-stage{height:545px;background:#dfe8ea;color:#24444c}
#selected .plate-data .plate-artworks{padding:55px 6% 40px;gap:12px;align-items:center}
#selected .plate-data .plate-page-cover{width:22%;height:65%;flex:none}
#selected .plate-data .plate-page-analysis{width:34%;height:90%;flex:none}
/* Plate 4: two working pages are the entire composition. */
#selected .plate-workbook .plate-stage{height:495px;background:#e7e9df;color:#405247}
#selected .plate-workbook .plate-artworks{padding:52px 8% 42px;gap:3px}
#selected .plate-workbook .plate-page-exercise{height:97%;width:44%;box-shadow:0 4px 19px #0001}
#selected .plate-workbook .plate-page-exercise:first-child{transform:rotate(-1deg)}
#selected .plate-workbook .plate-page-exercise:last-child{transform:rotate(1deg)}
/* Plate 5: fold-out form, both actual sides shown in landscape without fake folds. */
#selected .plate-fold .plate-stage{height:495px;background:#dbcabc;color:#50443d}
#selected .plate-fold .plate-artworks{padding:64px 28px 40px;gap:25px;flex-direction:column}
#selected .plate-fold .plate-page{width:90%;height:42%;max-width:610px;box-shadow:0 6px 20px #0002}
#selected .plate-fold .plate-overline{max-width:80%}
/* Plate 6: a closing report with three evidence-led documents. */
#selected .plate-report .plate-stage{height:530px;background:#263e4a;color:#eff0eb}
#selected .plate-report .plate-artworks{padding:55px 10% 42px;gap:clamp(12px,2.4vw,42px)}
#selected .plate-report .plate-page-cover{width:30%;height:92%}
#selected .plate-report .plate-page-inside{width:28%;height:80%;box-shadow:0 10px 26px #0004}
#selected .plate-report .plate-page-inside:last-child{height:75%}
@media(min-width:1500px){
 #selected .plate-folio .plate-stage,#selected .plate-report .plate-stage{height:570px}
}
@media(max-width:960px){
 #selected .featured>.project-card:nth-child(1),#selected .featured>.project-card:nth-child(6){grid-column:1/-1}
 #selected .featured>.project-card:nth-child(2),#selected .featured>.project-card:nth-child(3),#selected .featured>.project-card:nth-child(4),#selected .featured>.project-card:nth-child(5){grid-column:span 6}
 #selected .plate-stage,#selected .plate-fashion .plate-stage,#selected .plate-data .plate-stage,#selected .plate-workbook .plate-stage,#selected .plate-fold .plate-stage{height:425px}
 #selected .plate-folio .plate-stage,#selected .plate-report .plate-stage{height:450px}
 #selected .plate-artworks{padding:48px 24px 32px}
 #selected .plate-overline{left:17px;top:15px}
}
@media(max-width:700px){
 #selected .featured{grid-template-columns:minmax(0,1fr);row-gap:42px}
 #selected .featured>.project-card{grid-column:1/-1}
 #selected .plate-stage,#selected .plate-fashion .plate-stage,#selected .plate-data .plate-stage,#selected .plate-workbook .plate-stage,#selected .plate-fold .plate-stage,#selected .plate-folio .plate-stage,#selected .plate-report .plate-stage{height:365px}
 #selected .plate-folio .plate-artworks{padding:49px 7% 33px;gap:12px}
 #selected .plate-folio .plate-page-cover{width:43%;height:88%}
 #selected .plate-folio .plate-page-feature{width:40%;height:74%}
 #selected .plate-folio .plate-page-feature:last-child{display:none}
 #selected .plate-fashion .plate-artworks{padding:50px 19px 25px;gap:8px}
 #selected .plate-data .plate-artworks{padding:52px 22px 33px;gap:9px}
 #selected .plate-data .plate-page-cover{display:none}
 #selected .plate-data .plate-page-analysis{width:47%;height:87%}
 #selected .plate-workbook .plate-artworks{padding:56px 20px 35px}
 #selected .plate-workbook .plate-page-exercise{width:47%;height:90%}
 #selected .plate-fold .plate-artworks{padding:50px 19px 29px;gap:17px}
 #selected .plate-fold .plate-page{width:95%;height:43%}
 #selected .plate-report .plate-artworks{padding:47px 18px 28px;gap:12px}
 #selected .plate-report .plate-page-cover{width:49%;height:90%}
 #selected .plate-report .plate-page-inside{width:44%;height:76%}
 #selected .plate-report .plate-page-inside:last-child{display:none}
 #selected .card-info h3{font-size:28px}
 #selected .plate-overline{font-size:9px}
}
@media(max-width:360px){
 #selected .plate-stage,#selected .plate-fashion .plate-stage,#selected .plate-data .plate-stage,#selected .plate-workbook .plate-stage,#selected .plate-fold .plate-stage,#selected .plate-folio .plate-stage,#selected .plate-report .plate-stage{height:310px}
 #selected .plate-overline{max-width:84%}
}
"""
csspath.write_text(css)
print("PLATES_BUILT",len(projects),flush=True)
