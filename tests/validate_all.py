"""Cross-file consistency validation: report vs model vs site vs README.

Checks counts, figure numbering, meeting details, board roster, local
assets, forbidden dashes, pagination quality, SABS pipeline references,
and headline claims.

Run:  python tests/validate_all.py
Needs: pip install pypdf openpyxl  (pypdfium2 optional, for the
pagination scan; that check is skipped without it)
Exits nonzero if any check fails.
"""
import os
import re
import sys
from pathlib import Path

from openpyxl import load_workbook
from pypdf import PdfReader

REPO = Path(__file__).resolve().parents[1]

ok, bad = [], []
def chk(cond, label): (ok if cond else bad).append(label)


def main():
    html = (REPO / "index.html").read_text()
    readme = (REPO / "README.md").read_text()
    r = PdfReader(REPO / "Saving_North_Middletown_Elementary.pdf")
    t = " ".join(pg.extract_text() for pg in r.pages).replace("\n", " ")
    wb = load_workbook(REPO / "NMES_Financial_Model.xlsx")

    # wording
    chk("arithmetic" not in t.lower(), "no 'arithmetic' in the PDF")
    chk("arithmetic" not in html.lower(), "no 'arithmetic' on the site")

    # counts everywhere
    n = len(r.pages)
    nf = sum(1 for ws in wb.worksheets for row in ws.iter_rows()
             for c in row if isinstance(c.value, str) and c.value.startswith("="))
    chk(f"The {n}-page report" in html and f"the {n}-page report" in readme,
        f"page count {n} consistent across PDF, site, README")
    chk(f"{len(wb.sheetnames)}-tab" in readme and f"({nf} formulas)" in readme,
        f"{len(wb.sheetnames)} tabs / {nf} formulas consistent with README")

    # figure caption sequence
    seq = sorted(set(int(f) for f in re.findall(r"Figure (\d+)\.", t)))
    chk(seq == list(range(1, seq[-1] + 1)), f"figure captions sequential ({seq})")

    # meeting details
    chk("North Middletown Community Center" in html
        and "North Middletown Community Center" in t,
        "July 23 meeting at the Community Center in site and PDF")
    chk("meeting set at the school" not in t
        and "at the school</div>" not in html, "no stale meeting location")

    # board roster
    for name in ["Bradley Purcell", "Jonathan Ott", "Mandy Thornberry",
                 "Miranda Wyles", "Shane Buckler", "larry.begley"]:
        chk(name.lower() in html.lower(), f"board contact present: {name}")
    for old in ["Earlywine", "Talbot", "Kandice"]:
        chk(old not in html, f"stale board name absent: {old}")

    # local assets referenced by the site exist
    for asset in re.findall(r'(?:src|href)="([^"#][^":]*?)"', html):
        if not asset.startswith(("http", "mailto", "tel", "file:")):
            chk((REPO / asset).exists(), f"local asset exists: {asset}")

    # forbidden dashes
    chk(not re.search(r"[–—]", t) and not re.search(r"[–—]", html),
        "zero en/em dashes in PDF and site")
    cells = [c.value for ws in wb for row in ws.iter_rows() for c in row
             if isinstance(c.value, str)]
    chk(not any(re.search(r"[–—]", v) for v in cells),
        "zero en/em dashes in workbook cells")
    chk(not any("Fable" in v for v in cells) and "Fable" not in t,
        "no model identifier in workbook or PDF")
    chk("$4,626" in t and "fiscal 2027" in t,
        "PDF states the $4,626 FY2027 SEEK base")

    # facility-plan capacity analysis (DFP documents archived in build/)
    for f in ["dfp_current.pdf", "dfp_2013_excerpt.png", "dfp_2026_draft_excerpt.png",
              "dfp_manifest.json"]:
        chk((REPO / "build" / f).exists(), f"DFP archive present: build/{f}")
    fp = wb["Facility_Plans"]
    chk(fp["E7"].value == 521 and fp["E8"].value == 422 and fp["E9"].value == 174,
        "model Facility_Plans: 2021 capacities 521/422/174")
    chk(fp["C9"].value == 198,
        "model Facility_Plans: NMES 2013 capacity 198")
    chk("549 at Bourbon Central and 422 at Cane Ridge" in t and "net 59 uncommitted seats" in t,
        "PDF states receiving capacities 549/422 and the net 59 seats")
    chk("549" in html and "422" in html and "198" in html and "59" in html,
        "site shows capacities 549/422, the 198 history, and the net 59")
    chk("547" in t and "154" in t and "83 percent full" in t,
        "PDF carries the 2026 draft re-ratings and the 83 percent fill")
    chk("547" in html and "154" in html and "83 percent full" in html,
        "site carries the 2026 draft re-ratings and the 83 percent fill")

    # pagination quality (optional dependency)
    try:
        import numpy as np
        import pypdfium2 as pdfium
        pdf2 = pdfium.PdfDocument(str(REPO / "Saving_North_Middletown_Elementary.pdf"))
        worst = 1.0
        for i, page in enumerate(pdf2):
            a = np.array(page.render(scale=0.4).to_pil().convert("L"))
            H = a.shape[0]
            nz = np.where(((a[:int(H * 0.9)]) < 200).sum(axis=1) > 3)[0]
            if len(nz) and i > 0:
                worst = min(worst, nz.max() / H)
        chk(worst >= 0.25, f"no near-empty pages (worst body end {worst:.0%})")
    except ImportError:
        print("  (pypdfium2 not installed; pagination scan skipped)")

    # SABS data consistency
    import json
    sabs_path = REPO / "build" / "sabs_zones.json"
    if sabs_path.exists():
        sabs = json.load(open(sabs_path))
        areas = {s["name"]: s["area_sq_mi"] for s in sabs["schools"]}
        total = sum(areas.values())
        nm = next(v for k, v in areas.items() if "North Middletown" in k)
        chk(len(areas) == 3, "SABS file holds three school zones")
        chk(285 <= total <= 295, f"SABS zone areas sum to the county ({total:.1f} sq mi)")
        chk(any(s.get("ncessch") == "210054000096" for s in sabs["schools"]),
            "SABS includes NMES by its NCES id")
        chk(abs(nm - 110.3) < 1, f"NMES official zone area {nm} sq mi")
        chk("110 square miles, 38 percent" in t, "PDF cites the official 110 sq mi / 38 percent")
        chk("38 percent of the county" in html, "site cites the official 38 percent")
        chk("roughly 5.1 across" in t, "PDF cites the official 5.1 per sq mi Paris-area density")

    # actual-distance computation
    zd_path = REPO / "build" / "zone_distances.json"
    if zd_path.exists():
        zd = json.load(open(zd_path))
        chk(zd["pair_road_mi"] == 10.0 and zd["implied_road_factor"] == 1.13,
            "distance file: US 460 pair 10 road mi, factor 1.13")
        chk(3.5 <= zd["mean_added_road_mi"] <= 4.5,
            f"distance file: mean added road miles {zd['mean_added_road_mi']}")
        chk(zd["share_of_area_closer_to_nmes"] == 0.78, "distance file: 78 percent closer to NMES")
        chk("road factor of 1.13" in t and "78 percent of the zone" in t,
            "PDF cites the measured road factor and the 78 percent share")

    # SABS pipeline references
    chk((REPO / "build" / "fetch_sabs.py").exists() and "fetch_sabs.py" in t
        and "fetch_sabs.py" in readme and "fetch_sabs.py" in html,
        "SABS query script present and referenced in PDF, README, site")

    # headline claims
    for needle in ["$140,000 to $225,000", "2,648,086", "$23.5",
                   "Appendix B: The Open Records Checklist", "KRS 157.370",
                   "Boston Public Schools"]:
        chk(needle in t, f"PDF claim intact: {needle}")
    chk("$361,240" in html, "site claim intact: $361,240 calculator default")

    print(f"PASS {len(ok)}")
    print(f"FAIL {len(bad)}")
    for b in bad:
        print("  -", b)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
