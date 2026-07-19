# Save North Middletown Elementary

Community analysis opposing the closure of North Middletown Elementary School
(Bourbon County Schools, Kentucky). Written by Dr. Ryan Bradley, a former NMES
King, with the help of an AI research assistant. Every figure traces to a
public source cited in the report and on the site.

## What is here

- `index.html` - the interactive community website (single file, no build step;
  charts via Chart.js CDN). Edit text directly; sections are labeled.
- `Saving_North_Middletown_Elementary.pdf` - the 31-page report.
- `NMES_Financial_Model.xlsx` - the 13-tab financial model (166 formulas).
- `build/` - Python scripts that regenerate the PDF, model, and report charts.
  Requires: `pip install reportlab openpyxl matplotlib`. Run
  `python build/make_charts.py`, then `python build/build_pdf.py`,
  and `python build/build_model.py`.

## Live links wired into the site

- Petition: https://www.change.org/p/sos-save-our-school-north-middletown-elementary
- Report and model downloads are served from this repo via GitHub Pages.
- Board contacts: https://www.bourbon.kyschools.us/page/board-of-education

## Hosting

Any static host works. GitHub Pages: Settings -> Pages -> deploy from main,
and the site serves from `index.html` at the repo root.

Corrections welcome. This project criticizes decisions and asks for documents;
it attributes no motive and alleges no wrongdoing to anyone.
