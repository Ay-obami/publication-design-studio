#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
import shutil

ROOT=Path(__file__).resolve().parent
SITE=ROOT/'dist'
PROC=ROOT/'process-assets'/'calloway'
ASSET=SITE/'assets'/'calloway'/'process'
DOWNLOADS=SITE/'downloads'
ASSET.mkdir(parents=True,exist_ok=True)
DOWNLOADS.mkdir(parents=True,exist_ok=True)

for name in ['raw-source-preview.webp','indesign-anatomy.jpg','all-48-pages.jpg']:
    shutil.copy2(PROC/name,ASSET/name)
shutil.copy2(PROC/'Calloway-Raw-Source-Demo.docx',DOWNLOADS/'calloway-raw-source-demo.docx')

def load(p): return BeautifulSoup(p.read_text(),'html.parser')
def save(p,s): p.write_text(str(s))

# Homepage: keep Halvorsen first visually and surface Calloway as the deeper process case.
hp=SITE/'index.html'
s=load(hp)
for href,desc in [
    ('/work/halvorsen-quill/','A quieter architecture profile built around scale, space and editorial restraint.'),
    ('/work/calloway/','Working draft to 48-page annual report, including system, QA and handoff.')
]:
    link=s.select_one(f'a[href="{href}"]')
    card=link.find_parent('article') if link else None
    if not card: continue
    for badge in card.select('.flagship-badge'):
        badge.decompose()
    card['class']=[c for c in card.get('class',[]) if c not in ('flagship-card','flagship-visual','flagship-process')]
    d=card.select_one('.selected-project-descriptor')
    if d: d.string=desc

selected=s.select_one('#selected')
if selected:
    h=selected.select_one('.section-head h2')
    p=selected.select_one('.section-head p')
    if h: h.string='Selected work & case studies'
    if p: p.string='Visual direction, editorial systems and one complete publication-production workflow.'
    old=s.select_one('.process-feature-home')
    if old: old.decompose()
    feature=BeautifulSoup('''<section class="process-feature-home">
<div class="process-feature-copy">
<span class="eyebrow">See how I work / Calloway</span>
<h2>From a working draft to a 48-page annual report.</h2>
<p>The finished pages are only the end of the job. This process study shows the source content, content audit, grid and hierarchy, representative approval pages, full document build, QA and editable handoff.</p>
<div class="process-feature-actions"><a class="button" href="/work/calloway/#process-case">See the full workflow ↗</a><a class="text-link" href="/downloads/calloway-raw-source-demo.docx">Inspect the source demo ↓</a></div>
</div>
<div class="process-feature-media">
<figure class="process-feature-before"><img src="/assets/calloway/process/raw-source-preview.webp" alt="Reconstructed Calloway Word source document before publication design" loading="lazy"><figcaption>01 / Source content</figcaption></figure>
<figure class="process-feature-after"><img src="/assets/calloway/page-37.webp?v=highres2" alt="Calloway finished annual report financial statement page" loading="lazy"><figcaption>05 / Finished publication</figcaption></figure>
</div>
</section>''','html.parser').select_one('section')
    selected.insert_after(feature)
save(hp,s)

# Calloway: full production-process case study.
cp=SITE/'work'/'calloway'/'index.html'
s=load(cp)
if s.title: s.title.string='Calloway Process Case Study | Ayobami — Publication Design'
meta=s.select_one('meta[name="description"]')
if meta: meta['content']='A complete publication-production case study: working Word source, content audit, InDesign system, 48-page annual report, QA and editable handoff.'
heading=s.select_one('.project-heading')
if heading:
    crumb=heading.select_one('.breadcrumbs')
    if crumb: crumb.clear(); crumb.append(BeautifulSoup('<a href="/work/">← All publications</a> / Reports','html.parser'))
    eye=heading.select_one('.eyebrow')
    if eye: eye.string='Production process case study / independent Adobe InDesign study'
    deck=heading.select_one('.deck')
    if deck: deck.string='48 pages · Annual report · Adobe InDesign · Full production workflow documented'
    if not heading.select_one('a[href="#process-case"]'):
        a=s.new_tag('a',href='#process-case',attrs={'class':'button secondary'})
        a.string='See the process ↓'
        heading.append(' ')
        heading.append(a)

old=s.select_one('#process-case')
if old: old.decompose()

process=BeautifulSoup('''<section class="process-case" id="process-case">
<div class="process-hero">
<div><span class="eyebrow">Publication production case study</span><h2>From working draft<br><em>to a 48-page report.</em></h2></div>
<div><p>This is an independent production study for the fictional Calloway Holdings. The company and financial data are synthetic. The reconstructed Word file below was created from the same content model to demonstrate the kind of unstructured source material a publication designer has to turn into a dependable document system.</p><div class="process-stats"><span><strong>48</strong> mapped pages</span><span><strong>12</strong> columns</span><span><strong>27</strong> financial reconciliations</span><span><strong>INDD + IDML</strong> handoff</span></div></div>
</div>

<article class="process-step process-source">
<div class="process-step-copy"><span class="process-kicker">01 / SOURCE</span><h3>Start with content, not a pretty spread.</h3><p>The reconstructed Word draft deliberately mixes rough hierarchy, notes to the designer, tables, image placeholders and inconsistent direct formatting. It is not claimed as a historical client file; it is a transparent demonstration of the source-to-layout problem.</p><a class="text-link" href="/downloads/calloway-raw-source-demo.docx">Download the reconstructed Word source ↓</a></div>
<figure class="process-step-media process-source-media"><img src="/assets/calloway/process/raw-source-preview.webp" alt="Three pages from the reconstructed Calloway Word source document" loading="lazy"><figcaption>Reconstructed source document / 4 Word pages / same synthetic content model</figcaption></figure>
</article>

<article class="process-step process-audit">
<div class="process-step-copy"><span class="process-kicker">02 / CONTENT AUDIT</span><h3>Turn the draft into a page architecture.</h3><p>The content was mapped before layout: letters, strategy, operating divisions, people and sustainability, governance, statements and notes each need different reading behaviours but one report system.</p></div>
<div class="process-audit-grid">
<div><strong>01</strong><span>Overview & performance</span><p>Headline measures, contents and the reading route.</p></div>
<div><strong>02</strong><span>Leadership narrative</span><p>Chair and CEO letters with sustained reading pages.</p></div>
<div><strong>03</strong><span>Strategy & divisions</span><p>Three operating businesses with charts, diagrams and decision points.</p></div>
<div><strong>04</strong><span>People & sustainability</span><p>Measures with explicit denominators and methodology.</p></div>
<div><strong>05</strong><span>Governance</span><p>Roles, review cycle and remuneration reference tables.</p></div>
<div><strong>06</strong><span>Financial reference</span><p>Statements plus five notes that reconcile back to the group model.</p></div>
</div>
</article>

<article class="process-step process-system">
<div class="process-step-copy"><span class="process-kicker">03 / DESIGN SYSTEM</span><h3>Approve the rules before scaling the pages.</h3><p>The report uses an A4, 12-column structure with 18 mm margins, 5 mm gutters and a baseline rhythm. The anatomy proof below is an actual InDesign export with the grid overlaid—not a recreation made for the website.</p><div class="process-system-specs"><span>A4</span><span>12 columns</span><span>18 mm margins</span><span>5 mm gutters</span><span>baseline rhythm</span><span>serif + sans hierarchy</span></div></div>
<figure class="process-step-media"><img src="/assets/calloway/process/indesign-anatomy.jpg" alt="Actual Calloway InDesign page with margin, column and baseline guides shown" loading="lazy"><figcaption>Actual InDesign anatomy export / grid, margins and baseline shown</figcaption></figure>
</article>

<article class="process-step process-approval">
<div class="process-step-copy"><span class="process-kicker">04 / REPRESENTATIVE APPROVAL</span><h3>Test different content types before building all 48 pages.</h3><p>A useful approval set should test the system, not three variations of the cover. These pages cover a performance page, a division section and a dense financial statement.</p></div>
<div class="approval-grid">
<figure><img src="/assets/calloway/page-03.webp?v=highres2" alt="Calloway performance page" loading="lazy"><figcaption>Performance / comparison</figcaption></figure>
<figure><img src="/assets/calloway/page-14.webp?v=highres2" alt="Calloway logistics division opener" loading="lazy"><figcaption>Division / narrative</figcaption></figure>
<figure><img src="/assets/calloway/page-37.webp?v=highres2" alt="Calloway income statement page" loading="lazy"><figcaption>Financial statement / reference</figcaption></figure>
</div>
</article>

<article class="process-step process-full">
<div class="process-step-copy"><span class="process-kicker">05 / FULL DOCUMENT</span><h3>The real test is whether the system survives page 48.</h3><p>The complete report moves through narrative, charts, tables, diagrams, governance and financial notes. The overview below is assembled from the actual exported pages.</p><div class="process-feature-actions"><a class="button secondary" href="/assets/calloway/publication.pdf" target="_blank" rel="noopener">Read the complete PDF ↗</a><a class="text-link" href="#pages">Inspect all 48 pages ↓</a></div></div>
<figure class="process-step-media process-all-pages"><img src="/assets/calloway/process/all-48-pages.jpg" alt="Overview of all 48 pages in the Calloway annual report" loading="lazy"><figcaption>All 48 exported report pages</figcaption></figure>
</article>

<article class="process-step process-handoff">
<div class="process-step-copy"><span class="process-kicker">06 / QA & HANDOFF</span><h3>Delivery is part of the design job.</h3><p>The native package contains the editable document, IDML fallback, linked assets, fonts and screen/print outputs. Automated checks recorded 27 financial reconciliations, eight bookmarks and 18 link destinations. The print PDF remains provisional until a physical proof and printer profile are approved.</p><div class="handoff-facts"><span>48-page native document</span><span>27 reconciliations passed</span><span>8 bookmarks</span><span>18 link destinations</span><span>screen PDF</span><span>provisional print PDF</span></div></div>
<div class="handoff-tree"><span class="tree-label">PACKAGE / CALLOWAY</span><code>Calloway.indd
Calloway.idml
EXPORT/
  Calloway-Screen.pdf
  Calloway-Print-Provisional.pdf
Links/
Document fonts/
QA/</code><p>Editable source + fallback + outputs + linked production assets.</p></div>
</article>

<div class="process-close"><span class="eyebrow">Have content that still looks like step 01?</span><h3>I can turn it into a publication system.</h3><a class="button" href="mailto:oyebisiayobami26@gmail.com?subject=Publication%20design%20enquiry">Email me about your publication ↗</a></div>
</section>''','html.parser').select_one('section')

case=s.select_one('.curated-case-study')
if case:
    case.insert_before(process)
    intro=case.select_one('.case-intro')
    if intro:
        e=intro.select_one('.eyebrow'); h=intro.select_one('h2')
        if e: e.string='Finished publication / selected pages'
        if h: h.string='The system after it scales to 48 pages'
save(cp,s)

cssp=SITE/'site.css'
css=cssp.read_text()
marker='/* Publication process case v7 */'
if marker in css: css=css.split(marker)[0]
css += r'''
/* Publication process case v7 */
.process-feature-home{display:grid;grid-template-columns:.8fr 1.2fr;gap:clamp(28px,5vw,70px);align-items:center;margin:62px 0 82px;padding:42px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}.process-feature-copy h2{font-family:var(--display);font-size:clamp(34px,4.8vw,64px);font-weight:400;line-height:1.04;letter-spacing:-.045em;margin:14px 0 18px}.process-feature-copy>p{font-size:15px;line-height:1.7;color:var(--muted)}.process-feature-actions{display:flex;gap:18px;align-items:center;flex-wrap:wrap;margin-top:24px}.process-feature-media{display:grid;grid-template-columns:1.3fr .7fr;gap:16px;align-items:end;background:#e8e5df;padding:24px}.process-feature-media figure{margin:0}.process-feature-media img{display:block;width:100%;height:auto}.process-feature-before{transform:rotate(-1deg)}.process-feature-after{transform:rotate(2deg)}.process-feature-media figcaption,.process-step-media figcaption,.approval-grid figcaption{font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-top:9px}
.process-case{margin:35px 0 80px}.process-hero{display:grid;grid-template-columns:1fr 1fr;gap:clamp(30px,6vw,85px);padding:48px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}.process-hero h2{font-family:var(--display);font-size:clamp(42px,6vw,78px);line-height:1.01;font-weight:400;letter-spacing:-.055em;margin:14px 0}.process-hero h2 em{color:var(--accent)}.process-hero p{font-size:16px;line-height:1.75;color:var(--muted)}.process-stats{display:grid;grid-template-columns:repeat(2,1fr);gap:0;border-top:1px solid var(--line);border-left:1px solid var(--line);margin-top:24px}.process-stats span{padding:15px;border-right:1px solid var(--line);border-bottom:1px solid var(--line);font-size:11px;color:var(--muted)}.process-stats strong{display:block;color:var(--ink);font-size:18px;margin-bottom:3px}
.process-step{padding:62px 0;border-bottom:1px solid var(--line)}.process-step-copy{max-width:790px;margin-bottom:28px}.process-kicker{font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:var(--accent);font-weight:700}.process-step h3,.process-close h3{font-family:var(--display);font-size:clamp(31px,4vw,50px);font-weight:400;line-height:1.08;letter-spacing:-.04em;margin:13px 0 16px}.process-step-copy>p{font-size:15px;line-height:1.75;color:var(--muted)}.process-step-media{margin:0}.process-step-media img{display:block;width:100%;height:auto;background:#e8e5df}.process-source-media{padding:22px;background:#e8e5df}.process-audit-grid{display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid var(--line);border-left:1px solid var(--line)}.process-audit-grid>div{padding:24px;border-right:1px solid var(--line);border-bottom:1px solid var(--line)}.process-audit-grid strong{font-size:10px;color:var(--accent);letter-spacing:.13em}.process-audit-grid span{display:block;font-size:16px;font-weight:600;margin:12px 0 8px}.process-audit-grid p{font-size:12px;line-height:1.55;color:var(--muted);margin:0}.process-system{display:grid;grid-template-columns:.7fr 1.3fr;gap:42px;align-items:start}.process-system .process-step-copy{margin:0}.process-system-specs,.handoff-facts{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}.process-system-specs span,.handoff-facts span{border:1px solid var(--line);padding:8px 10px;font-size:10px;text-transform:uppercase;letter-spacing:.07em}.approval-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;background:#e8e5df;padding:26px;align-items:end}.approval-grid figure{margin:0}.approval-grid img{display:block;width:100%;height:auto;filter:drop-shadow(4px 5px 7px #0002)}.process-all-pages img{border:1px solid var(--line)}.process-handoff{display:grid;grid-template-columns:1fr .85fr;gap:50px}.process-handoff .process-step-copy{margin:0}.handoff-tree{background:#171717;color:#f4f0e8;padding:28px 30px;align-self:start}.tree-label{display:block;color:#c7775e;font-size:10px;letter-spacing:.14em;margin-bottom:18px}.handoff-tree code{white-space:pre-wrap;display:block;font:13px/1.75 ui-monospace,SFMono-Regular,Menlo,monospace}.handoff-tree p{font-size:11px;color:#bcb8b0;margin:18px 0 0}.process-close{padding:58px 0 15px;max-width:820px}.process-close .button{margin-top:8px}
@media(max-width:850px){.process-feature-home,.process-hero,.process-system,.process-handoff{grid-template-columns:1fr}.process-feature-media{grid-template-columns:1.2fr .8fr}.process-audit-grid{grid-template-columns:repeat(2,1fr)}.approval-grid{gap:10px;padding:16px}}
@media(max-width:560px){.process-feature-media,.approval-grid,.process-audit-grid{grid-template-columns:1fr}.process-feature-after{max-width:70%;justify-self:end}.process-source-media{padding:10px}.process-step{padding:44px 0}.process-stats{grid-template-columns:1fr 1fr}}
'''
cssp.write_text(css)
print('FLAGSHIP_PROCESS_V7_READY')
