#!/usr/bin/env python3
"""Refresh website reading copies from the current editable publication delivery."""
from pathlib import Path
import json,re,shutil,hashlib,subprocess,sys
import fitz
from PIL import Image,ImageOps,ImageDraw

ROOT=Path(__file__).resolve().parent
SOURCE=Path('/home/ayobami/Documents/Approved-Portfolio/06-Client-Ready-Portfolio')
projects=json.loads((SOURCE/'PROJECT-INDEX.json').read_text())
records=json.loads((ROOT/'dist/projects.json').read_text())
def key(t):return re.sub('[^a-z0-9]','',t.lower())
lookup={key(x['project']):x for x in projects}
def choose(project,pages):
 candidates=[]
 for p in Path(project['directory']).rglob('*.pdf'):
  low=str(p).lower()
  if any('/'+x+'/' in low for x in ['mockups','presentation','current-presentation','qa','current-qa','links','assets','form-resources','references']):continue
  if any(x in p.name.lower() for x in ['detail','proof','template','test','anatomy','contact']):continue
  try:
   d=fitz.open(p)
   if len(d)!=pages:continue
   score=20*('screen' in p.name.lower())+15*('digital' in p.name.lower())+10*('fillable' in p.name.lower())-15*('print' in p.name.lower())-15*('pdfx' in p.name.lower())
   candidates.append((score,-len(p.parts),p))
  except Exception:continue
 if not candidates:raise RuntimeError('No reading PDF for '+project['project'])
 return max(candidates,key=lambda x:x[:2])[2]
def render(page,width):
 pix=page.get_pixmap(matrix=fitz.Matrix(width/page.rect.width,width/page.rect.width),alpha=False)
 return Image.frombytes('RGB',(pix.width,pix.height),pix.samples)

written=[]
for n,b in enumerate(records,1):
 project=lookup[key(b['title'])];pdf=choose(project,int(b['pages']));dest=ROOT/'dist/assets'/b['slug'];dest.mkdir(exist_ok=True)
 target=dest/'publication.pdf';changed=not target.exists() or hashlib.sha256(target.read_bytes()).digest()!=hashlib.sha256(pdf.read_bytes()).digest()
 if changed:
  shutil.copy2(pdf,target);d=fitz.open(target)
  for i,page in enumerate(d,1):
   image=render(page,2000 if b['slug'] in ['halvorsen-quill','calloway','silence-quarterly','quarterly-index','clearpath-coaching','orlathread'] else 1680)
   image.save(dest/f'page-{i:02}.webp',quality=89,method=4)
   ImageOps.contain(image,(460,620)).save(dest/f'thumb-{i:02}.webp',quality=82,method=4)
  # Keep the existing cover/interior composition format while refreshing its actual pages.
  canvas=Image.new('RGB',(1200,760),'#e5e3de')
  positions=[(85,90,395,560),(535,35,280,480),(820,210,295,440)]
  for i,(x,y,w,h) in enumerate(positions[:min(3,len(d))],1):
   im=ImageOps.contain(Image.open(dest/f'page-{i:02}.webp').convert('RGB'),(w,h));ImageDraw.Draw(canvas).rectangle((x+12,y+13,x+im.width+12,y+im.height+13),fill='#c8c6c2');canvas.paste(im,(x,y))
  for name in ['card.webp','presentation.webp']:canvas.save(dest/name,quality=90,method=4)
 written.append({'project':b['title'],'source':str(pdf),'changed':changed,'pages':b['pages']})
 print('PUBLICATION',n,'/',len(records),b['title'],'updated' if changed else 'checked',flush=True)

# The selected-publications download is rebuilt from the cleaned reading copies.
out=fitz.open();font='/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
def title_page(title,subtitle):
 page=out.new_page(width=595.276,height=841.89);page.insert_font(fontname='body',fontfile=font)
 page.insert_text((56,70),'AYOBAMI / PUBLICATION DESIGN',fontname='body',fontsize=10)
 page.insert_textbox(fitz.Rect(56,235,540,390),title,fontname='body',fontsize=33,color=(.1,.12,.1))
 page.insert_textbox(fitz.Rect(56,410,530,490),subtitle,fontname='body',fontsize=13,color=(.2,.22,.2))
title_page('Selected publications','Reports, editorial publications, guides and brochures. Design and production by Ayobami.')
for slug in ['halvorsen-quill','silence-quarterly','quarterly-index','clearpath-coaching','orlathread','calloway']:
 d=fitz.open(ROOT/'dist/assets'/slug/'publication.pdf')
 for pi in sorted(set([0,min(1,len(d)-1),min(2,len(d)-1)])):out.insert_pdf(d,from_page=pi,to_page=pi)
title_page('Start with the content.','Publication design by Ayobami. For enquiries, use the contact details on the portfolio website.')
download=ROOT/'dist/downloads/ayobami-selected-publications-2026.pdf';out.save(download,garbage=4,deflate=True)

# Recompose image assets while retaining the current website styles and behaviour.
protected={name:(ROOT/name).read_bytes() for name in ['dist/site.css','dist/site.js']}
for name in ['editorial-plates-v4.py','polish-homepage-v5.py','clean-presentation-copy.py']:
 subprocess.run([sys.executable,str(ROOT/name)],cwd=ROOT,check=True)
for name,content in protected.items():(ROOT/name).write_bytes(content)
(ROOT/'publication-refresh.json').write_text(json.dumps(written,indent=2))
print('SYNCHRONISED',len(written),'publications',flush=True)
