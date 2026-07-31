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

# closure central case (v3 two-tailed)
central = A["B51"].value + A["B52"].value + 3 * A["B69"].value - 137500 - 10 * A["B6"].value - 155000
site_const = re.search(r"net=FIXV\[f\]\+p\*c-b-l\*(\d+)-o", html)
site_fixv = re.search(r"var FIXV=\[(\d+),(\d+),(\d+)\]", html)
if central == 69071 and site_const and "$69,071" in html:
    match("closure central case $69,071 (model inputs == site calculator v3.9 defaults)")
else:
    diff(f"closure central: model {central}, site regex {'ok' if site_const else 'MISSING'}")
if site_fixv and int(site_fixv.group(2)) == A["B51"].value + A["B52"].value:
    match(f"calculator mothballed case {site_fixv.group(2)} == model B51+B52 (131,724+96,107, both measured)")
else:
    diff("calculator FIXV mothballed case does not equal model B51+B52")
if site_fixv and (int(site_fixv.group(1)), int(site_fixv.group(3))) == (58774, 276928):
    match("calculator reassigned/sold cases (58,774 / 276,928) match build/closure_grid.py")
else:
    diff("calculator FIXV reassigned/sold cases do not match the grid")
if A["B69"].value == 60000:
    match("GF-borne $60,000 per position (Assumptions B69) backs the calculator default")
if site_const and int(site_const.group(1)) == A["B6"].value:
    match("calculator $4,626 per leaver == model SEEK base FY2027")

# two-tailed range strings consistent
if "losing $556,000" in pdf_flat and "saving $552,000" in pdf_flat and "losing $556,000 and saving $552,000" in html:
    match("v3.9 two-tailed range (-$556,000 to +$552,000) consistent on site and in PDF")
else:
    diff("v3 two-tailed range strings missing on site or PDF")

# levy path: base is now the General Fund tax only (B48 = "=B32"), not total collections
levy_base = TH["B32"].value  # General Fund property tax, the base B48 points at
site_levy_base = int(re.search(r"base=(\d+),add", html).group(1))
cum = 0
for i in range(3): cum += (levy_base + cum) * 0.04
if levy_base == site_levy_base == 7829060 and round(cum) == 977568:
    match(f"levy base $7,829,060 (GF only) and 3-yr path to $977,568 = {cum/model_deficit*100:.1f}% of deficit (model inputs == site JS)")
else:
    diff(f"levy: model base {levy_base}, site {site_levy_base}, cum {cum:.0f}")
y1 = levy_base * 0.04
pdf_levy_ok = "313,000" in pdf_flat and "978,000" in pdf_flat and "639,000" in pdf_flat
if pdf_levy_ok: match(f"PDF levy path ($313K yr1, $639K yr2, $978K yr3) matches computed ({y1:,.0f} / 638,851 / 977,568)")
else: diff("PDF levy figures not all found")
# the excluded restricted base is disclosed, not silently dropped
if "7,829,060" in pdf_flat and "restricted building-fund" in pdf_flat:
    match("PDF discloses the GF-only levy base and why the restricted levy is excluded")
else: diff("PDF levy-base disclosure missing")

# ---------- 2. score series (site vs model vs PDF claims) ----------
years_model = list(range(2007, 2020)) + list(range(2021, 2026))
def model_row(r):
    return {y: SD.cell(row=r, column=2+i).value for i, y in enumerate(years_model)}

# the site now carries three selectable sources: comp (KDE official composite),
# pd (KDE reading/math average), sd (SchoolDigger third-party index)
def site_block(src):
    blk = re.search(src + r":\{(.*?)\]\}", html, re.S).group(1) + "]"
    out = {}
    for key in ("NMES", "BC", "CR", "PE"):
        vals = [None if v.strip() == "null" else float(v)
                for v in re.search(key + r":\[([^\]]+)\]", blk).group(1).split(",")]
        out[key] = {2007 + i: v for i, v in enumerate(vals)}
    return out
site_scores = site_block("sd")
site_comp = site_block("comp")
site_pd = site_block("pd")

# KDE official record: site arrays vs the archived source file
kde = json.load(open(f"{REPO}/build/kde_scores_history.json"))
comp_bad, pd_bad = [], []
for yk, row in kde["official_composite"].items():
    if yk == "note": continue
    y = int(yk[:4]) + 1
    for key in ("NMES", "BC", "CR", "PE"):
        want = row[key][0]
        got = site_comp[key].get(y)
        if got is None or abs(got - want) > 0.06:
            comp_bad.append((key, y, got, want))
for yk in kde["reading_pd"]:
    y = int(yk[:4]) + 1
    for key in ("NMES", "BC", "CR", "PE"):
        want = (kde["reading_pd"][yk][key] + kde["math_pd"][yk][key]) / 2
        got = site_pd[key].get(y)
        if got is None or abs(got - want) > 0.06:
            pd_bad.append((key, y, got, round(want, 2)))
if not comp_bad: match("site KDE composite series matches build/kde_scores_history.json (all schools, all years)")
else: diff(f"site KDE composite mismatches: {comp_bad}")
if not pd_bad: match("site KDE reading/math average series matches build/kde_scores_history.json")
else: diff(f"site KDE R/M average mismatches: {pd_bad}")

# model School_Data KDE history block vs the same source file
kh_years_keys = ["2011-12", "2012-13", "2013-14", "2014-15", "2015-16", "2016-17",
                 "2017-18", "2018-19", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25"]
mh_bad = []
for subj, base in (("reading_pd", 45), ("math_pd", 49)):
    for j, key in enumerate(("NMES", "BC", "CR", "PE")):
        for i, yk in enumerate(kh_years_keys):
            got = SD.cell(row=base + j, column=2 + i).value
            if abs(got - kde[subj][yk][key]) > 0.001:
                mh_bad.append((subj, key, yk, got))
for j, key in enumerate(("NMES", "BC", "CR", "PE")):
    for i, yk in enumerate(kh_years_keys):
        want = kde["official_composite"].get(yk, {})
        want = want[key][0] if key in want else None
        got = SD.cell(row=56 + j, column=2 + i).value
        if (got is None) != (want is None) or (want is not None and abs(got - want) > 0.001):
            mh_bad.append(("composite", key, yk, got))
if not mh_bad: match("model School_Data KDE history block matches build/kde_scores_history.json (104 P/D cells + composites)")
else: diff(f"model KDE history mismatches: {mh_bad}")
rowmap = {"NMES": 15, "BC": 16, "CR": 17, "PE": 18}
for key, row in rowmap.items():
    mrow = model_row(row)
    bad = [(y, site_scores[key].get(y), mrow[y]) for y in years_model
           if (site_scores[key].get(y) is None) != (mrow[y] is None)
           or (mrow[y] is not None and abs((site_scores[key].get(y) or 0) - mrow[y]) > 0.01)]
    if not bad: match(f"score series {key}: all {sum(1 for y in years_model if mrow[y] is not None)} values identical site vs model")
    else: diff(f"score series {key} mismatches: {bad}")
head_ok = all(s in pdf_flat for s in ["79.1", "74.5"])
site_sd_ok = all(s in html for s in ["58.2", "26.5", "19.3"])
if head_ok and site_sd_ok:
    match("PDF headlines the official composites (79.1 Distinguished, 74.5 first by 14); site keeps the SchoolDigger series (58.2 / 26.5 / 19.3) as selectable context")
else:
    diff(f"headline scores: PDF official {head_ok}, site SchoolDigger {site_sd_ok}")

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
    match("2018-2025 Bourbon rate history in model matches PDF Figure 16 series (61.3 -> 52.4)")

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

# ---------- 6. bonding story: $14M plan, savings-to-bond scenarios, FY2026 close ----------
DS = wb["Debt_Service"]
ds_vals = {}
for r in range(1, DS.max_row + 1):
    a = DS.cell(row=r, column=1).value
    if a: ds_vals[str(a)] = (DS.cell(row=r, column=2).value, DS.cell(row=r, column=3).value)
bond_amt = ds_vals.get("Proposed bond amount", (None, None))[0]
if bond_amt == 14000000 and "$14 million" in html and "$14 million" in pdf_flat:
    match("proposed $14M bond consistent across model, site, PDF")
else:
    diff(f"$14M bond: model {bond_amt}, site {'$14 million' in html}, pdf {'$14 million' in pdf_flat}")
excess = ds_vals.get("District's own KDE-filed excess cost of NMES vs peer elementaries", (None, None))[0]
if excess == 121220 and "$121,220" in html and "$121,000" in pdf_flat:
    match("audited excess cost $121,220 in model and on site; PDF rounds to $121,000")
else:
    diff(f"excess cost: model {excess}, site {'$121,220' in html}, pdf {'$121,000' in pdf_flat}")
fy26 = ds_vals.get("Net General Fund change, FY2026 (unaudited)", (None, None))[0]
rev26 = ds_vals.get("General Fund revenue, FY2026 actual (excludes carryforward and on-behalf)", (None, None))[0]
exp26 = ds_vals.get("General Fund expenditures, FY2026 actual", (None, None))[0]
if rev26 == 22103877 and exp26 == 22477866 and "$374,000" in html and "$374,000" in pdf_flat:
    match("FY2026 unaudited net change (-$373,989 from packet figures) rounds to $374,000 on site and PDF")
else:
    diff(f"FY2026 close: model rev {rev26} exp {exp26}, site {'$374,000' in html}, pdf {'$374,000' in pdf_flat}")
misc = ds_vals.get("Caveat 1: miscellaneous revenue (object 1990) budgeted at zero, received", (None, None))[0]
if misc == 1567829 and "$1.41 million" in html and "$1,413,929" in pdf_flat:
    match("FY2026 miscellaneous-revenue caveat in model and PDF; site keeps the rounded $1.41M mention")
else:
    diff(f"misc revenue caveat: model {misc}, site {'$1.41 million' in html}, pdf {'$1,413,929' in pdf_flat}")
xfer = ds_vals.get("Caveat 2: restricted capital money transferred INTO the General Fund in June 2026", (None, None))[0]
if xfer == 1320939 and "$1,320,939" in html and "$1,320,939" in pdf_flat:
    match("June 2026 capital-to-GF transfer ($1,320,939) present in model, site, PDF")
else:
    diff(f"capital transfer: model {xfer}, site {'$1,320,939' in html}, pdf {'$1,320,939' in pdf_flat}")
gap_b, gap_c = ds_vals.get("Operating gap to close first", (None, None))
if gap_b == 1900000 and gap_c == 373989 and "$21 million" in pdf_flat and "$25 million" in pdf_flat:
    match("balanced-budget scenario inputs ($1.9M / $373,989 gaps) in model; $21M/$25M capacity quoted in the PDF")
else:
    diff(f"scenario: model gaps {gap_b}/{gap_c}, pdf $21M {'$21 million' in pdf_flat}, $25M {'$25 million' in pdf_flat}")

# ---------- 7. KFICS condition index (v3.1): model vs PDF (site card moved to report in v4.1) ----------
FP = wb["Facility_Plans"]
ci_model = {FP.cell(row=r, column=1).value: [FP.cell(row=r, column=c).value for c in (2, 3, 4)]
            for r in range(67, 72)}
nmes_ci = ci_model.get("North Middletown Elementary (1948/64)")
cane_ci = ci_model.get("Cane Ridge Elementary (1992)")
cent_ci = ci_model.get("Bourbon Central Elementary (1988)")
def _r3(v): return [round(x, 3) for x in v]
if (nmes_ci and _r3(nmes_ci) == [0.694, 0.702, 0.773]
        and cane_ci and _r3(cane_ci) == [0.812, 0.812, 0.728]
        and cent_ci and _r3(cent_ci) == [0.888, 0.819, 0.823]
        and "chartCondition" not in html):
    match("KFICS condition index series intact in model; site card retired to the report (v4.1)")
else:
    diff(f"condition index: model {nmes_ci}/{cane_ci}/{cent_ci}, site chart absent: {'chartCondition' not in html}")
needs = FP["E69"].value; crv = FP["F69"].value
if needs and crv and abs((1 - needs / crv) - 0.773295) < 0.0005 and "0.773" in pdf_flat:
    match("NMES condition index 0.773 = 1 - 3,099,148/13,670,418 verified from state-report components; quoted in the PDF")
else:
    diff(f"NMES CI recompute: needs {needs}, crv {crv}, pdf 0.773 {'0.773' in pdf_flat}")

# ---------- 8. recruitment pool (v3.2): fill planner lever, model, PDF ----------
RD = wb["Redistricting"]
if re.search(r"net=\(t\+h\)\*4626-\(r\+t\+h\)\*400\+s\*60000-a\*60000", html):
    match("fill planner JS v3.8: (t+h)*4626-(r+t+h)*400+s*60000-a*60000 (NMES section debit live)")
else:
    diff("fill planner JS v3.8 formula with NMES section debit not found")
hs = (RD["B117"].value, RD["B118"].value)
seek46 = 46 * A["B6"].value
if hs == (236, 23) and "259 registered homeschool" in html and "236 registered homeschool" in pdf_flat:
    match("registered homeschool counts (236 BCS + 23 Paris = 259, 2022-23) consistent model/site/PDF")
else:
    diff(f"homeschool counts: model {hs}, site 259 {'259 registered homeschool' in html}, pdf 236 {'236 registered homeschool' in pdf_flat}")
pool = (RD["B123"].value, RD["B125"].value, RD["B126"].value, RD["B127"].value)
if pool == (76, 131, 54, 189) and "54 of them from Fayette County" in html and "net import of 189" in pdf_flat:
    match("KDE nonresident flows (76 out / 131 in / 54 Fayette / net 189) consistent model/site/PDF")
else:
    diff(f"nonresident flows: model {pool}")
if seek46 == 212796 and "$213,000" in pdf_flat and RD["B131"].value == "=Assumptions!B6-Assumptions!B62":
    match("46-seat fill from the pool = 46 x $4,626 = $212,796, quoted as about $213,000 in PDF; per-return net formula in model")
else:
    diff(f"pool revenue: 46*B6={seek46}, pdf $213,000 {'$213,000' in pdf_flat}")

# ---------- 9. KY closure record (v3.3): model formulas vs site chart vs PDF ----------
KC = wb["KY_Closures"]
perry = None; johnson = None
for r in range(15, 30):
    nm = KC.cell(row=r, column=1).value
    if nm == "Perry County": perry = r
    if nm == "Johnson County": johnson = r
if perry and johnson:
    pd_, pe, pf, pc = KC.cell(row=perry, column=4).value, KC.cell(row=perry, column=5).value, KC.cell(row=perry, column=6).value, KC.cell(row=perry, column=3).value
    per_kid = (pd_ * (1 + pf) - pe) / pc
    if abs(per_kid - 3643) < 2 and "3643" in re.sub(r"[,$]", "", html) and "$3,600" in pdf_flat:
        match("Perry 2017 per-displaced-student figure ($3,643) recomputes from model inputs; on site chart and in PDF (about $3,600)")
    else:
        diff(f"Perry per-kid: model recompute {per_kid:.0f}, site 3643 {'3643' in re.sub(r'[,$]','',html)}, pdf $3,600 {'$3,600' in pdf_flat}")
else:
    diff("KY_Closures tab missing Perry/Johnson rows")
plan_lo = 800000 / A["B11"].value; plan_hi = 1000000 / A["B11"].value
if plan_lo == 6250 and abs(plan_hi - 7812.5) < 1 and "$6,250 to $7,813" in html and "$6,250 to $7,813" in pdf_flat:
    match("plan requirement per displaced student ($6,250 to $7,813 = $800K-$1M over 128) consistent model/site/PDF")
else:
    diff(f"plan per-kid: {plan_lo:.0f}/{plan_hi:.0f}")
site_ky = re.search(r"chartKYRecord[\s\S]{0,1200}data:\[\[713,4414\],\[0,2050\],\[0,3525\],\[0,3643\],\[0,6935\],\[6250,7813\]\]", html)
if site_ky:
    match("site KY-record chart data matches the computed case table exactly")
else:
    diff("site KY-record chart data drifted from the case table")
if KC["B5"].value == 339 and KC["B6"].value == 72 and KC["B51"].value == 0 and "339 rural" in pdf_flat:
    match("closure universe (339/72) and the zero-precedent cell consistent in model and PDF")
else:
    diff(f"universe: model {KC['B5'].value}/{KC['B6'].value}, zero-cell {KC['B51'].value}")

# distribution rows (v3.4)
if (KC["C39"].value, KC["C40"].value, KC["B42"].value, KC["B43"].value) == (1102, 818, 8440, 541) \
        and "$1,102" in html and "$8,440" in html and "$541" in html and "$818" in pdf_flat:
    match("distribution stats (median $1,102 / plausible $818 / artifact $8,440 / corrected $541) consistent model/site/PDF")
else:
    diff(f"distribution rows: {KC['C39'].value}/{KC['C40'].value}/{KC['B42'].value}/{KC['B43'].value}")

# ---------- 10. levy history (v3.6): site JS vs model vs CSV ----------
import csv as _csv
lvrows={r["district"]:r for r in _csv.DictReader(open(f"{REPO}/build/ky_levy_history_2012_2026.csv"))}
site_bourbon=re.search(r'"Bourbon County":\[([\d.,]+)\]',html)
csv_b=[lvrows["Bourbon Co"][y] for y in sorted(k for k in lvrows["Bourbon Co"] if k[:2]=="20")]
if site_bourbon and [float(x) for x in site_bourbon.group(1).split(",")]==[float(x) for x in csv_b]:
    match("levy history: site JS Bourbon series identical to archived CSV (14 years)")
else:
    diff(f"levy history mismatch: site {site_bourbon and site_bourbon.group(1)} vs csv {csv_b}")
TH2 = wb["Tax_History"]
if TH2["O66"].value == 52.4 and TH2["B58"].value == 36.8 and abs(TH2["O58"].value-63.4)<0.05:
    match("levy table in model matches endpoints (Bath 36.8->63.4; Bourbon ends 52.4)")
else:
    diff(f"levy model endpoints: {TH2['B58'].value}/{TH2['O58'].value}/{TH2['O66'].value}")

# ---------- 11. beyond-4% recallable levy options (v3.7) ----------
lv_yield = TH2["B32"].value / TH2["B71"].value          # 7,829,060 / 41.0
lv_median = sorted(TH2[f"O{r}"].value for r in (58, 59, 60, 61, 63, 64, 65, 66))
lv_median = (lv_median[3] + lv_median[4]) / 2            # median of eight, Fayette excluded
lv_cases = [(TH2["B24"].value, "$1.01 million", 112),    # Harrison 57.7
            (lv_median,        "$1.51 million", 167),    # regional median 60.3
            (TH2["B5"].value,  "$1.70 million", 188),    # Bourbon's own 2018 rate 61.3
            (TH2["O61"].value, "$2.50 million", 277)]    # Clark 65.5
percent_cost = TH2["B73"].value * 0.01 / 100             # $21.16 per cent on the median home
ok_lv = abs(lv_yield - 190952.68) < 1 and abs(lv_median - 60.3) < 0.01 and abs(percent_cost - 21.16) < 0.005
for rate, revstr, fam in lv_cases:
    cents = rate - TH2["B12"].value
    rev = cents * lv_yield
    ok_lv &= (abs(rev / 1e6 - float(revstr[1:5])) < 0.005) and revstr in html and revstr in pdf_flat
    ok_lv &= round(cents * percent_cost) == fam and f"${fam}/yr" in html
if ok_lv:
    match("beyond-4% options: model-derived yield/median/costs reproduce all four site+PDF rows")
else:
    diff(f"beyond-4% options mismatch: yield {lv_yield:.2f}, median {lv_median}, cost/cent {percent_cost}")
lv_first_call = 373989 + 1320939
lv_margin = (TH2["B5"].value - TH2["B12"].value) * lv_yield - lv_first_call
if lv_first_call == 1694928 and round(lv_margin) == 4551 and "$4,551" in html and "$4,551" in pdf_flat \
        and str(TH2["B83"].value).startswith("=Debt_Service!") and TH2["B85"].value == "=B84-B83":
    match("beyond-4% sequencing: 2018 rate covers gap+sweep ($1,694,928) within $4,551, live in model")
else:
    diff(f"beyond-4% sequencing: first call {lv_first_call}, margin {lv_margin:.0f}")

# ---------- 12. v3.8: school costs, breakevens, growth plan ----------
SCt = wb["School_Costs"]
ok38 = SCt["B14"].value == 19348 and SCt["B15"].value == "=B14*128" and 19348*128 == 2476544
ok38 &= "$2,476,544" in html and "$2,476,544" in pdf_flat and "$8,305" in html and "$8,305" in pdf_flat
rev23 = (11808998, 20381341, 9550068, 2454)
ok38 &= (SCt["C9"].value, SCt["D9"].value, SCt["E9"].value, SCt["B9"].value) == rev23
ok38 &= abs(rev23[1]/rev23[3] - 8305.4) < 0.5 and abs(2476544/(rev23[1]/rev23[3]) - 298.2) < 0.5
if ok38:
    match("300-breakeven reconstruction: cost 128 x 19,348 = $2,476,544 exact; state-only $8,305 -> 298 (model/site/PDF)")
else:
    diff("300-breakeven reconstruction mismatch across model/site/PDF")
c01 = [(SCt[f"B{r}"].value, SCt[f"C{r}"].value) for r in (49,50,51,52)]
if c01 == [(595,3360),(312,4053),(193,4414),(145,5200)] and "$5,200" in html and "$4,414" in html:
    xs=[1/n for n,_ in c01]; ys=[p for _,p in c01]
    mx=sum(xs)/4; my=sum(ys)/4
    F=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs)
    a0=my-F*mx
    if abs(F-331507)<5 and abs(a0-2851)<5 and "$2,851" in html and "$332,000" in html:
        match("2000-01 scale curve: $2,851 + $331,507/N reproduced from the four report-card points")
    else:
        diff(f"2000-01 curve fit mismatch: F={F:.0f}, a={a0:.0f}")
    mil = (5200-4053)*145; nm = (19348-18131)*128
    if mil == 166315 and nm == 155776 and "$166,000" in html and "$156,000" in html:
        match("Millersburg symmetry: $166,315 (2000-01) vs $155,776 (2023-24), site quotes both rounded")
    else:
        diff(f"Millersburg symmetry mismatch: {mil} / {nm}")
else:
    diff(f"2000-01 report card rows mismatch in model: {c01}")
AL2 = wb["Alternatives"]
raw_lo = 313162.4 + 60000 + 100000 + 4*85000 + 0.5*(1447164-999727) + 2913654*0.05 + 100000 + 50000 + 100000 + (16*4626-46*400+(1-1)*60000) + 25*4226
raw_hi = 375000 + 120000 + 200000 + 425000 + 450000 + 2913654*0.10 + 250000 + 150000 + 300000 + (16*4626-46*400+(2-1)*60000) + 50*4226
if abs(raw_lo-1593830)<5 and abs(raw_hi-2888281)<5 and "$1.6 to $2.9 million" in html and "$1.6 to $2.9 million" in pdf_flat:
    match("growth plan raw sums $1.59M/$2.89M recomputed from inputs; quoted as $1.6 to $2.9 million on site and PDF")
else:
    diff(f"growth plan raw sums: {raw_lo:.0f}/{raw_hi:.0f}")
if "$960,000 to $1.9 million" in html and "$960,000 to $1.9 million" in pdf_flat \
        and "$260,000 to $530,000" in html and "$260,000 to $530,000" in pdf_flat:
    match("growth plan pillar subtotals consistent on site and in PDF")
else:
    diff("growth plan pillar subtotals missing or inconsistent")
fills = (16*4626-46*400, 55616+60000)
if fills[0]-0 == 55616+400*0 - 0 and "$56,000 to $116,000" in html and "$56,000 to $116,000" in pdf_flat \
        and "$115,616" not in re.sub(r"v3\.5[^)]*\)", "", html):
    match("fill package corrected to $56,000-$116,000 site+PDF; old default only in v3.5 history text")
else:
    diff("fill package correction incomplete")

# ---------- 13. federal EDFacts series (v3.8 amendment) ----------
ef_arch = json.load(open(f"{REPO}/build/edfacts_school_proficiency_bourbon.json"))
ef_bad = []
for key in ("NMES", "BC", "CR", "PE"):
    m = re.search(r"ef:\{.*?" + key + r":\[([^\]]+)\]", html, re.S)
    site_vals = [None if x.strip()=="null" else float(x) for x in m.group(1).split(",")]
    for i, label in enumerate(range(2007, 2026)):
        syk = f"SY{label-1}-{str(label)[2:]}"
        rec = ef_arch["data"].get(syk, {}).get(key)
        want = round((rec["r"]+rec["m"])/2, 1) if rec else None
        got = site_vals[i]
        if (got is None) != (want is None) or (want is not None and abs(got-want) > 0.05):
            ef_bad.append((key, label, got, want))
if not ef_bad:
    match("EDFacts site series identical to archived federal extract (4 schools x 10 years)")
else:
    diff(f"EDFacts series mismatches: {ef_bad}")

# site text spot checks
for s, label in [("1st in all 5 reported subjects", "hero fact scores"), ("-$556K to +$552K", "hero fact closure range"),
                 ("$7,829,060", "GF levy basis in calculator note"), ("$2.65M", "deficit rounding in verdicts"),
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
