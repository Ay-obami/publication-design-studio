# Ayobami — Publication Design Studio

Publication design portfolio with complete PDF readers, selected project presentations and a searchable collection.

Production source: Approved-Portfolio/06-Client-Ready-Portfolio on the workstation. Editable InDesign and IDML documents, linked assets and font licences are maintained with each project. The public website serves the prepared dist directory through Vercel.

## Presentation updates
Run clean-presentation-copy.py after the website build. It keeps titles, descriptions and footer copy focused on the work and its deliverables. Asset credits and licence records remain with the publication files.

The publication PDF is the reading surface; thumbnails and editorial boards are previews. Preserve the PDF reader, keyboard navigation, category filters and mobile layouts when editing.

## Local preview
python3 -m http.server 8080 --directory dist
