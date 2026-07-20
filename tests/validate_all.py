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
