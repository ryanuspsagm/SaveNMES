# Save North Middletown Elementary

Community analysis opposing the closure of North Middletown Elementary School
(Bourbon County Schools, Kentucky). Written by Dr. Ryan Bradley, a former NMES
King, with the help of an AI research assistant. Every figure traces to a
public source cited in the report and on the site.

## What is here

- `index.html` - the interactive community website (single file, no build step;
  charts via Chart.js CDN). Edit text directly; sections are labeled.
- `Saving_North_Middletown_Elementary.pdf` - the 28-page report.
- `NMES_Financial_Model.xlsx` - the 13-tab financial model (169 formulas).
- `build/` - Python scripts that regenerate the PDF, model, and report charts.
  Requires: `pip install reportlab openpyxl matplotlib`. Run
  `python build/make_charts.py`, then `python build/build_pdf.py`,
  and `python build/build_model.py`. `python build/fetch_sabs.py` pulls the
  official 2015-16 federal attendance boundaries (NCES SABS) into
  `build/sabs_zones.json`, already committed here; the map figure redraws from
  them automatically; `python build/zone_distances.py` then computes the
  actual zone distances the busing math uses. `python build/fetch_dfp.py` (run it on a machine with
  normal internet access) downloads the district's current District Facility
  Plan from KDE plus every distinct historical version held by the Wayback
  Machine, the documents that set each school's rated capacity and
  classification; commit the resulting `dfp_*.pdf` files and the capacity
  analysis picks them up. The SABS fetch script uses a saved
  `sabs_zones_raw.json` if present, then tries the NCES REST endpoint, and falls
  back to the EDGE bulk download (`SABS_1516_SchoolLevels.zip` in `~/Downloads`,
  or set `SABS_ZIP`), so it works without a reachable NCES server - which
  matters, because that endpoint is currently returning HTTP 500.

## Tests

`python tests/run_all.py` runs the whole suite:

- `tests/validate_all.py` - cross-file consistency: page, tab, and formula
  counts; figure numbering; meeting details; board roster; local assets;
  the no-dash rule; pagination quality; headline claims.
- `tests/sync_check.py` - every shared number checked three ways: site
  JavaScript vs workbook cells vs report text.
- `tests/test_site.py` - browser tests for the calculators, charts,
  toggles, anchors, and mobile layout (needs `pip install playwright`
  and a Chromium; Chart.js is vendored so no internet is needed).

Run the suite after any edit and before any push.

## Live links wired into the site

- Petition: https://www.change.org/p/sos-save-our-school-north-middletown-elementary
- Report and model downloads are served from this repo via GitHub Pages.
- Board contacts: https://www.bourbon.kyschools.us/page/board-of-education

## Hosting

Any static host works. GitHub Pages: Settings -> Pages -> deploy from main,
and the site serves from `index.html` at the repo root.

Corrections welcome. This project criticizes decisions and asks for documents;
it attributes no motive and alleges no wrongdoing to anyone.
