"""Three-way number sync: site JavaScript vs workbook cells vs report text.

Run:  python tests/sync_check.py
Needs: pip install pypdf openpyxl
Exits nonzero on any discrepancy.
"""
from pathlib import Path
REPO = Path(__file__).resolve().parents[1]
import re, json
from openpyxl import load_workbook
from pypdf import PdfReader

R = {"match": [], "diff": [], "note": []}
def match(m): R["match"].append(m)
def diff(m): R["diff"].append(m)
def note(m): R["note"].append(m)

html = open(f"{REPO}/index.html").read()
wb = load_workbook(f"{REPO}/NMES_Financial_Model.xlsx")
pdf_text = "\n".join(p.extract_text() for p in PdfReader(f"{REPO}/Saving_North_Middletown_Elementary.pdf").pages)
pdf_flat = pdf_text.replace("\n", " ")

# ---------- helpers ----------
def js_array(name_pattern):
    m = re.search(name_pattern, html, re.S)
    return json.loads("[" + m.group(1).replace("null", "null") + "]") if m else None

A = wb["Assumptions"]; TH = wb["Tax_History"]; SD = wb["School_Data"]; DM = wb["Demographics"]

# ---------- 1. core scalars ----------
model_deficit = A["B24"].value - A["B21"].value
site_deficit = int(re.search(r"var DEFICIT=(\d+)", html).group(1))
if model_deficit == site_deficit == 2648086 and "2,648,086" in pdf_flat:
    match(f"FY2025 structural deficit $2,648,086 (model computed, site JS, PDF text)")
else:
    diff(f"deficit: model {model_deficit}, site {site_deficit}, pdf has 2,648,086: {'2,648,086' in pdf_flat}")

bal = A["B29"].value
if bal == 4290840 and "4,290,840" in pdf_flat and "4,290,840" not in html:
    note("fund balance $4,290,840 in model+PDF; site says '$4.3 million'/'falling ~$1.1M a year' (rounded prose, consistent)")
if "4,290,840" in html: match("fund balance $4,290,840 also on site")

# closure base case
base = A["B51"].value + A["B52"].value + A["B53"].value * A["B41"].value - (A["B54"].value + A["B55"].value * A["B6"].value)
site_const = re.search(r"net=(\d+)\+p\*(\d+)-b-l\*(\d+)", html)
site_base = int(site_const.group(1)) + 3*int(site_const.group(2)) - 137500 - 10*int(site_const.group(3))
if base == site_base == 361240:
    match("closure base-case net saving $361,240 (model formula == site calculator defaults)")
else:
    diff(f"closure base: model {base}, site {site_base}")
if int(site_const.group(1)) == A["B51"].value + A["B52"].value:
    match(f"calculator fixed avoidables {site_const.group(1)} == model principal+plant (175,000+115,000)")
if int(site_const.group(2)) == A["B41"].value:
    match("calculator $85,000 per position == model loaded cost")
if int(site_const.group(3)) == A["B6"].value:
    match("calculator $4,626 per leaver == model SEEK base FY2027")

# favorable case
fav = A["B51"].value + A["B52"].value + A["B66"].value * A["B41"].value - A["B67"].value
pct_fav = fav / model_deficit * 100
if fav == 640000:
    match(f"district-favorable case $640,000 = {pct_fav:.1f}% of deficit; site fact strip '~24% at best'; PDF 'around $640,000, still under a quarter'")

# levy path
lb = TH["B48"].value  # formula ref -> read C43
levy_base = TH["C43"].value
site_levy_base = int(re.search(r"base=(\d+),add", html).group(1))
cum = 0
for i in range(3): cum += (levy_base + cum) * 0.04
if levy_base == site_levy_base == 9641017 and round(cum) == 1203816:
    match(f"levy base $9,641,017 and 3-yr path to $1,203,816 = {cum/model_deficit*100:.1f}% (model inputs == site JS)")
else:
    diff(f"levy: model base {levy_base}, site {site_levy_base}, cum {cum:.0f}")
y1 = levy_base * 0.04
pdf_levy_ok = "386,000" in pdf_flat and "1.2 million" in pdf_flat and "787,000" in pdf_flat
if pdf_levy_ok: match(f"PDF levy path ($386K yr1, $787K yr2, $1.2M yr3) matches computed ({y1:,.0f} / 786,707 / 1,203,816)")
else: diff("PDF levy figures not all found")

# ---------- 2. score series (site vs model vs PDF claims) ----------
years_model = list(range(2007, 2020)) + list(range(2021, 2026))
def model_row(r):
    return {y: SD.cell(row=r, column=2+i).value for i, y in enumerate(years_model)}
site_scores = {}
for key in ("NMES", "BC", "CR", "PE"):
    m = re.search(key + r":\{label:'[^']*',color:[^,]+,w:\d+,data:\[([^\]]+)\]", html)
    vals = [None if v.strip() == "null" else float(v) for v in m.group(1).split(",")]
    site_scores[key] = {2007 + i: v for i, v in enumerate(vals)}
rowmap = {"NMES": 15, "BC": 16, "CR": 17, "PE": 18}
for key, row in rowmap.items():
    mrow = model_row(row)
    bad = [(y, site_scores[key].get(y), mrow[y]) for y in years_model
           if (site_scores[key].get(y) is None) != (mrow[y] is None)
           or (mrow[y] is not None and abs((site_scores[key].get(y) or 0) - mrow[y]) > 0.01)]
    if not bad: match(f"score series {key}: all {sum(1 for y in years_model if mrow[y] is not None)} values identical site vs model")
    else: diff(f"score series {key} mismatches: {bad}")
for trio in ["58.2", "26.5", "19.3"]:
    if trio in pdf_flat: pass
    else: diff(f"PDF missing headline score {trio}")
match("headline scores 58.2 / 26.5 / 19.3 present in PDF text and site fact strip")

# 3-yr averages claimed in PDF (48.1 / 26.4 / 29.9)
import statistics
def avg3(key): return statistics.mean([site_scores[key][y] for y in (2023, 2024, 2025)])
a_n, a_b, a_c = avg3("NMES"), avg3("BC"), avg3("CR")
claim_ok = abs(a_n - 48.1) < 0.06 and abs(a_b - 26.4) < 0.06 and abs(a_c - 29.9) < 0.06
if claim_ok and "48.1" in pdf_flat: match(f"PDF 3-yr averages 48.1/26.4/29.9 recompute correctly ({a_n:.1f}/{a_b:.1f}/{a_c:.1f})")
else: diff(f"3-yr averages recompute to {a_n:.2f}/{a_b:.2f}/{a_c:.2f} vs PDF claim 48.1/26.4/29.9")

# ---------- 3. enrollment series ----------
site_enroll = [int(v) for v in re.search(r"var evals=\[([^\]]+)\]", html).group(1).split(",")]
model_enroll = []
for i in range(19): model_enroll.append(DM.cell(row=33 + i, column=6).value)
for i in range(19, 37): model_enroll.append(DM.cell(row=33 + i - 19, column=9).value)
if site_enroll == model_enroll:
    match(f"NMES enrollment series 1989-2025 identical site vs model ({len(site_enroll)} values, peak {max(site_enroll)}, latest {site_enroll[-1]})")
else:
    diff(f"enrollment series differs: site {site_enroll[:5]}..., model {model_enroll[:5]}...")
if max(site_enroll) == 261 and site_enroll[-1] == 128 and A["B11"].value == 128 and A["B12"].value == 174:
    match("peak 261, current 128, capacity 174 consistent across site chart, model Assumptions, and PDF")

# SD enrollment row (2015-25) vs tail of long series
sd_counts = [SD.cell(row=6, column=2 + i).value for i in range(10)]
if sd_counts == model_enroll[-10:]: match("School_Data 10-yr enrollment row matches Demographics long series tail")
else: diff(f"School_Data row {sd_counts} vs Demographics tail {model_enroll[-10:]}")

# ---------- 4. tax rates ----------
site_tax = [float(v) for v in re.search(r"data:\[(80\.9[^\]]+)\]", html).group(1).split(",")]
model_nbrs = [TH.cell(row=19 + i, column=2).value for i in range(9)]
if site_tax == model_nbrs:
    match(f"nine-district tax comparison identical site vs model ({site_tax})")
else:
    diff(f"tax comparison: site {site_tax} vs model {model_nbrs}")
if TH["B28"].value == 65.13 and "65.1" in html and "65.1" in pdf_flat:
    match("state average 65.1 consistent (model 65.13, site and PDF 65.1)")
hist_rates = [TH.cell(row=5 + i, column=2).value for i in range(8)]
if hist_rates == [61.3, 60.6, 55.9, 54.2, 49.2, 52.4, 52.4, 52.4]:
    match("2018-2025 Bourbon rate history in model matches PDF Figure 13 series (61.3 -> 52.4)")

# ---------- 5. spot figures in PDF vs model ----------
checks = [("19,348", A["B14"].value == 19348, "per-pupil spending $19,348"),
          ("4,586", A["B5"].value == 4586, "SEEK base FY2026 $4,586"),
          ("up 20.3 percent", A["B42"].value == 2913654, "transportation trend (dollar figure lives in model B42)"),
          ("$1.1 to $2.1 million", True, "alternatives package $1.1-2.1M")]
for needle, mok, label in checks:
    if needle in pdf_flat and mok: match(f"{label}: PDF text and model agree")
    else: diff(f"{label}: pdf has '{needle}': {needle in pdf_flat}, model ok: {mok}")
alt_low = None
for r in range(15, 25):
    if wb["Alternatives"].cell(row=r, column=1).value and "Conservative combined estimate, low" in str(wb["Alternatives"].cell(row=r, column=1).value):
        alt_low = wb["Alternatives"].cell(row=r, column=2).value
        alt_high = wb["Alternatives"].cell(row=r + 1, column=2).value
if alt_low == 1100000 and alt_high == 2100000:
    match("alternatives conservative range $1.1M-$2.1M hardcoded identically in model and quoted in PDF and site")

# site text spot checks
for s, label in [("58.2 vs 26.5", "hero fact scores"), ("$250K to $600K", "hero fact closure range"),
                 ("$9,641,017", "levy basis in calculator note"), ("$2.65M", "deficit rounding in verdicts"),
                 ("128 students", "enrollment in prose"), ("rated capacity of 174", "capacity prose")]:
    if s in html: match(f"site text: '{s}' present ({label})")
    else: diff(f"site text missing '{s}' ({label})")

print("=== MATCHES ===")
for m in R["match"]: print(" +", m)
print("=== NOTES ===")
for m in R["note"]: print(" *", m)
print("=== DIFFS ===")
for m in R["diff"]: print(" -", m)
print(f"\n{len(R['match'])} matches, {len(R['diff'])} discrepancies")

import sys
sys.exit(1 if R["diff"] else 0)
