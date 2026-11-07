#!/usr/bin/env python3
"""Keep publication-facing copy focused on the work and its deliverables."""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parent
REPLACEMENTS={'The work shown is independent portfolio work. Fictional brands or data are used only to demonstrate design decisions; no client results are implied.': 'Explore complete publications, page systems and editable production deliverables.', 'This portfolio presents independent publication studies created to demonstrate layout, typography, information hierarchy and long-document design. Fictional organisations, names or sample data are demonstration content and are not presented as paid-client work or measured commercial results.': 'Publication design by Ayobami, spanning layout, typography, information hierarchy and long-document production.', '<span class="eyebrow">Transparency</span>': '<span class="eyebrow">Credits</span>'}
REPLACEMENTS.update({
 'Portfolio projects are self-initiated design studies, not commissioned client work. Covers and interiors shown are taken from the actual publication files.':'Publication design and production by Ayobami.',
 '40 self-initiated native publication studies. Images displayed here are rendered from actual exported InDesign publications, not AI-generated imagery. Fictional examples are not presented as client commissions.':'Publication design and production by Ayobami.',
 'I design catalogs, reports, magazines, guides and brochures in Adobe InDesign. These forty studies are self-initiated examples of layout, typography, editorial sequence and production craft, not claims of paid-client engagements.':'I design catalogs, reports, magazines, guides and brochures, combining clear typography, coherent page systems and careful production.',
 'Forty self-initiated Adobe InDesign studies. Browse the collection by format, search by name, or open any publication to inspect the complete page sequence.':'Browse the publication collection by format, search by name, or open a project to explore the complete page sequence.',
 ' · Self-initiated publication study':'',
 'Native Adobe InDesign study':'Publication design',
 'Production process case study / independent Adobe InDesign study':'Annual report production',
 'This is an independent production study for the fictional Calloway Holdings. The company and financial data are synthetic. The reconstructed Word file below was created from the same content model to demonstrate the kind of unstructured source material a publication designer has to turn into a dependable document system.':'The Calloway report brings management commentary, divisional comparisons and a reconciled financial model into a consistent publication system. The working Word document shows the content structure before page design.',
 'The reconstructed Word draft deliberately mixes rough hierarchy, notes to the designer, tables, image placeholders and inconsistent direct formatting. It is not claimed as a historical client file; it is a transparent demonstration of the source-to-layout problem.':'The working Word document combines headings, production notes, tables and image references. The design resolves these elements into a readable hierarchy, reusable styles and a dependable page sequence.',
 'Images on this site are rendered from the published PDF layouts in the separate non-AI collection. Photography and other third-party content, where used, retain the credits and licences documented inside the individual editable packages. Sample data and fictional businesses should not be mistaken for measured outcomes or completed commercial work. Some projects remain in internal quality refinement.':'Photography, typefaces and other third-party assets retain the credits and licences supplied with the individual publication packages.',
 'Independent publication design / InDesign':'Publication design / InDesign',
 'Forty publication studies, each built around the way its content deserves to be read.':'Publications built around the way their content deserves to be read.',
 'Forty original publication design studies created in Adobe InDesign.':'Publication design by Ayobami: reports, magazines, catalogs, guides and brochures.',
 'No AI-generated illustrations on this site':'Covers, interiors and complete publications',
 'No AI-generated imagery':'Original publication layouts',
})

REPLACEMENTS.update({'Browse the study archive': 'Browse all publications', 'Study archive / Adobe InDesign': 'Publication collection / Adobe InDesign', 'Additional publication,<br><em>studies.</em>': 'The complete<br><em>publication collection.</em>', 'A searchable archive of independent publication studies. Start with the selected case studies on the homepage, or use this index when you want a closer match by format.': 'Explore the complete publication collection. Filter by format, search by name, or open a project to inspect its full page sequence.', '40 publication designs. The varied visual presentation is back, with ten original layouts and four larger features. Filter or search to find a relevant example.': 'Explore 40 publications across reports, editorial design, catalogs, brochures and workbooks. Filter or search to find a relevant format.'})

REPLACEMENTS.update({'Reconstructed Calloway Word source document': 'Calloway working Word document', 'Three pages from the reconstructed Calloway Word source document': 'Three pages from the Calloway working Word document', 'Download the reconstructed Word source': 'Download the working Word document', 'Reconstructed source document / 4 Word pages / same synthetic content model': 'Working source document / 4 Word pages', 'reconstructed Word draft': 'working Word draft'})

def clean(s):
 for old,new in REPLACEMENTS.items():s=s.replace(old,new)
 return s

if __name__=='__main__':
 changed=[]
 for p in (ROOT/'dist').rglob('*'):
  if p.is_file() and p.suffix in ['.html','.json','.js']:
   old=p.read_text();new=clean(old)
   if new!=old:p.write_text(new);changed.append(str(p.relative_to(ROOT)))
 # Clean the generators as well as their output so a rebuild cannot restore old labels.
 for p in ROOT.glob('*.py'):
  if p.name==Path(__file__).name:continue
  old=p.read_text();new=clean(old)
  if new!=old:p.write_text(new);changed.append(p.name)
 print('Updated',len(changed),'website files')
