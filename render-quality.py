#!/usr/bin/env python3
"""Render publication images at display/retina quality directly from canonical PDF packages.
Never upscale an existing webp. No AI assets. Original INDD and PDF packages unchanged.
Preserves existing HTML, CSS, video, and GitHub deploy configuration.
"""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import pymupdf, json, zipfile, subprocess, sys, io, re, os
ROOT=Path(__file__).resolve().parent
SOURCE=Path.home()/"Documents/Approved-Portfolio/05-Design-Upgrade-In-Progress/DELIVERY"
manifest=json.loads((SOURCE/"PACKAGE-MANIFEST.json").read_text())
OUT=ROOT/"dist/assets"
SELECTED={"halvorsen-quill","silence-quarterly","quarterly-index","clearpath-coaching","orlathread","calloway"}
assert len(manifest)==40
def slug(s):return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
def select_pdf(z,expected):
 choices=[]
 for name in z.namelist():
  low=name.lower()
  if not low.endswith('.pdf') or any(x in low for x in ('presentation/','mockups/','/links/','/current-qa/','form-resources/','worked-example','template','test.pdf','proof.pdf')): continue
  priority=(9 if 'screen.pdf' in low or 'digital.pdf' in low else 0)+(8 if 'review.pdf' in low else 0)+(7 if 'fill' in low else 0)-(3 if 'print' in low or 'pdfx' in low else 0)
  try:
   data=z.read(name)
   doc=pymupdf.open(stream=data,filetype='pdf')
   n=len(doc)
   doc.close()
   if n==expected:choices.append((priority,-len(data),name,data))
  except Exception:continue
 if not choices:raise ValueError('No suitable PDF '+str(expected))
 choices.sort(reverse=True)
 return choices[0][-1]
def render(page,width):
 scale=width/page.rect.width
 pix=page.get_pixmap(matrix=pymupdf.Matrix(scale,scale),colorspace=pymupdf.csRGB,alpha=False)
 return Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
def save_webp(im,dest,quality=89):
 temp=dest.with_suffix(".tmp.webp")
 im.save(temp,"WEBP",quality=quality,method=4)
 os.replace(temp,dest)
def compose(folder, pagecount,selected=False):
 # A higher-res arrangement built from real page artwork.
 candidates=[1,min(pagecount,2),min(pagecount,3)]
 images=[Image.open(folder/("page-%02d.webp"%n)).convert("RGB") for n in candidates]
 W,H=(2400,1520)
 canvas=Image.new("RGB",(W,H),"#e6e3df")
 rect=ImageDraw.Draw(canvas)
 positions=[(170,170,780,1150),(1020,90,555,1000),(1630,420,575,890)]
 for i,(im,(x,y,w,h)) in enumerate(zip(images,positions)):
  small=ImageOps.contain(im,(w,h),Image.Resampling.LANCZOS)
  rect.rectangle((x+20,y+25,x+small.width+20,y+small.height+25),fill="#c6c2bb")
  canvas.paste(small,(x,y))
 save_webp(canvas,folder/"presentation.webp",89)
 save_webp(ImageOps.contain(canvas,(1500,960),Image.Resampling.LANCZOS),folder/"card.webp",88)
 if selected and folder.name=="halvorsen-quill":
  save_webp(canvas,OUT/"hero.webp",89)

for index,x in enumerate(manifest,1):
 key=slug(x['project']); expected=int(x['pages'])
 package=SOURCE/x['package'];folder=OUT/key
 if not folder.is_dir():raise FileNotFoundError(folder)
 with zipfile.ZipFile(package) as z: data=select_pdf(z,expected)
 doc=pymupdf.open(stream=data,filetype="pdf")
 assert len(doc)==expected
 for j,page in enumerate(doc,1):
  # 1680-2000px raster widths sharpen both high-DPI previews and page reader.
  # Original source is vector PDF: direct renderer preserves type and linework.
  im=render(page,2000 if key in SELECTED and j<=3 else 1680)
  save_webp(im,folder/("page-%02d.webp"%j),89)
  thumb=ImageOps.contain(im,(460,650),Image.Resampling.LANCZOS)
  save_webp(thumb,folder/("thumb-%02d.webp"%j),84)
 doc.close()
 compose(folder,expected,key in SELECTED)
 print("QUALITY",index,"/40",x['project'],expected,flush=True)
print("ALL HIGH-RES RENDERS FINISHED",flush=True)
# Force a new browser/CDN URL for refreshed images, without changing page paths.
from bs4 import BeautifulSoup
for html_file in (ROOT/"dist").rglob("*.html"):
    text=html_file.read_text()
    # Asset requests only; avoid touching CSS or unrelated URLs.
    import re as _re
    text=_re.sub(r'(/assets/[^"\s]+?\.webp)(?!\?v=)',r'\1?v=highres2',text)
    html_file.write_text(text)
print("HIGH-RES ASSET URLS VERSIONED",flush=True)

