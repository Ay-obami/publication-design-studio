# Ayobami — Publication Design Studio

Git-deployed static publication portfolio presenting **40 native Adobe InDesign studies** and **538 pages in the selected PDF viewing copies**. Real PDF page renders are used throughout; no AI-generated artwork is introduced into the website.

Source collection: `Approved-Portfolio/05-Design-Upgrade-In-Progress/DELIVERY/PACKAGE-MANIFEST.json`. The private native INDD/IDML packages, provenance records and current quality reviews remain outside the public website repository.

Build: `python3 build-40.py` on the authorised workstation with `pymupdf` and `Pillow`, and current source packages. This rebuilds 40 publication PDF page readers and then runs `refine-website.py` for the differentiated, freelancer-focused page design. To edit only the website layout without touching the PDFs, run `python3 refine-website.py`. Git tracks the complete `dist/` output so Vercel serves this exact snapshot without needing local source access.

Run: `python3 -m http.server 8080 --directory dist`.

This is independent, self-initiated portfolio work, not a record of paid client commissions. Quality upgrades are ongoing for some publications. Photography is credited in the individual source packages.

Visual design: category features use original exported publication covers and pages. All four presentations are authored HTML/CSS (no image generation) and vary in layout, color and typography. The original native InDesign source remains untouched.

Image-quality pipeline: `python3 render-quality.py` re-renders all page images from the canonical original PDF packages at 1680px or 2000px width (for selected projects), WebP 89, 460px thumbnails and 2400px portfolio compositions. It does not upscale the previous WebPs. This is also invoked at the end of `build-40.py`. The source packages and original PDFs remain unchanged.


### Portfolio editorial structure

The homepage is curated rather than displaying all 40 publications; the complete searchable archive is at `/work/`. Six selected projects contain three editorial boards composed from the original exported InDesign pages, followed by the existing full document reader and PDF. The 20-page vector PDF lookbook is `/downloads/ayobami-selected-publications-2026.pdf`.

Run `curate-portfolio.py` **after** `refine-website.py` and `render-quality.py` when rebuilding the website. It relies on Python BeautifulSoup4 and PyMuPDF and does not generate new illustration artwork. `build-40.py` orchestrates these steps in order. No AI-generated assets are used.
