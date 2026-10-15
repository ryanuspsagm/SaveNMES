"""Verify the 2025-26 KDE scores against the archived state rows, three ways.

1. build/kde_ksa_2025_26.json and build/kde_levels_2025_26.json re-derive
   exactly from the raw KDE rows archived in build/kde_acct_2026_*.csv.
2. KDE's own arithmetic holds on every row the site uses: levels sum to 100,
   proficient plus distinguished equals the published P/D, the content index
   follows the 0/50/100/125 weights, each indicator status is the mean of its
   content indexes, combined rate equals status plus change, and the published
   overall reproduces from the state's 51/40/5/4 weights.
3. The site carries those numbers unchanged: the 2025-26 table, the status
   table (status only, with the status-only overall from the same weights), the
   status chart data, the 2026 points on the history chart, the grade-level
   breakout for both years, and the CSI sentences (53 schools, 19 new, 38 in
   Jefferson County, 33 elementary, NMES 35th lowest of 715 on status, second
   lowest on the official overall, cut between 37.6 and 38.2).

Run:  python tests/verify_kde_2026.py
Exits nonzero if any check fails.
"""
import csv
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
B = REPO / "build"
ok, bad = [], []
def chk(cond, label): (ok if cond else bad).append(label)
def f(x):
    try: return float(x)
    except (TypeError, ValueError): return None

prof = list(csv.DictReader(open(B / "kde_acct_2026_profile_bourbon.csv", encoding="utf-8")))
asm = list(csv.DictReader(open(B / "kde_acct_2026_assessment_performance_bourbon.csv", encoding="utf-8")))
grd = list(csv.DictReader(open(B / "kde_acct_2026_by_grade_bourbon.csv", encoding="utf-8")))
csi = list(csv.DictReader(open(B / "kde_acct_2026_csi_tsi_atsi_statewide.csv", encoding="utf-8")))
es_all = list(csv.DictReader(open(B / "kde_acct_2026_profile_es_statewide.csv", encoding="utf-8")))
ksa = json.load(open(B / "kde_ksa_2025_26.json"))
lv26 = json.load(open(B / "kde_levels_2025_26.json"))["levels"]
lv25 = json.load(open(B / "kde_levels_2024_25.json"))["levels"]
html = (REPO / "index.html").read_text()

CODES = {"041010": "Bourbon Central Elementary School", "041030": "Cane Ridge Elementary School",
         "041090": "North Middletown Elementary School", "478010": "Paris Elementary School"}
SUBJ = ["Reading", "Mathematics", "Science", "Social Studies", "Combined Writing"]
A = {(r["School Code"], r["Level"], r["Demographic"], r["Subject"]): r for r in asm}
PR = {(r["School Code"], r["Level"]): r for r in prof}

# ---------- 1. JSON re-derives from the raw rows
def same(e, r):
    sup = r["Suppressed"] == "Y"
    if e["suppressed"] != ("Y" if sup else "N") or e["CI"] != (r["Content Index"] or "*"):
        return False
    if sup:
        return e["P"] == "*" and e["D"] == "*" and e["PD"] == "*"
    return e["P"] == r["Proficient"] and e["D"] == r["Distinguished"] and e["PD"] == r["Proficient/Distinguished"]
for code, name in CODES.items():
    chk(all(same(ksa["schools"][name][s], A[(code, "ES", "All Students", s)]) for s in SUBJ),
        f"kde_ksa_2025_26.json matches the archived KDE rows: {name}")
chk(all(same(ksa["state_elementary"][s], A[("999", "ES", "All Students", s)]) for s in SUBJ),
    "kde_ksa_2025_26.json matches the archived KDE rows: Kentucky elementary")
chk(all(same(ksa["district_elementary"][s], A[("041", "ES", "All Students", s)]) for s in SUBJ),
    "kde_ksa_2025_26.json matches the archived KDE rows: Bourbon County district")
GR = {"03": "3rd", "04": "4th", "05": "5th"}
KEY = {"041010": "BCES", "041030": "CRES", "041090": "NMES", "478010": "PES", "041": "District", "999": "Kentucky"}
FIX = {"Editing and Mechanic": "Editing and Mechanics"}
rebuilt = {}
for r in grd:
    if r["Demographic"] != "All Students" or r["Grade"] not in GR or r["School Code"] not in KEY:
        continue
    subj = FIX.get(r["Subject"], r["Subject"])
    if subj not in lv26:
        continue
    val = None if r["Suppressed"] == "Y" else [int(r[c]) for c in ("Novice", "Apprentice", "Proficient", "Distinguished", "Proficient/Distinguished")]
    rebuilt.setdefault(subj, {}).setdefault(GR[r["Grade"]], {})[KEY[r["School Code"]]] = val
chk(all(lv26[s][g].get(k) == rebuilt[s][g].get(k) for s in lv26 for g in lv26[s] for k in lv26[s][g]),
    "kde_levels_2025_26.json matches the archived by-grade rows")

# ---------- 2. KDE's arithmetic holds
ROWS = [(c, "ES") for c in list(CODES) + ["041", "999"]]
for code, level in ROWS:
    for s in SUBJ:
        r = A[(code, level, "All Students", s)]
        if r["Suppressed"] == "Y":
            continue
        n, a, p, d, pd, ci = (int(r["Novice"]), int(r["Apprentice"]), int(r["Proficient"]), int(r["Distinguished"]),
                              int(r["Proficient/Distinguished"]), f(r["Content Index"]))
        chk(98 <= n + a + p + d <= 102 and abs(p + d - pd) <= 1, f"levels sum and P+D=PD: {code} {s}")
        chk(abs(0.5 * a + p + 1.25 * d - ci) <= 2.0, f"content index follows the 0/50/100/125 weights: {code} {s}")
W = [("Reading_Mathematics", 51), ("Science_Social Studies_Combined Writing", 40), ("English Learners Progress", 5), ("Quality Of School Climate and Safety", 4)]
def weighted(r, field):
    avail = [(f(r[f"{ind} {field}"]), w) for ind, w in W if f(r[f"{ind} {field}"]) is not None]
    return sum(v * w for v, w in avail) / sum(w for _, w in avail)
status_only = {}
for code, level in ROWS:
    r = PR[(code, level)]
    ci = lambda s: f(A[(code, level, "All Students", s)]["Content Index"])
    chk(abs(f(r["Reading_Mathematics Status"]) - (ci("Reading") + ci("Mathematics")) / 2) <= 0.06,
        f"reading/math status is the mean of the two content indexes: {code}")
    chk(abs(f(r["Science_Social Studies_Combined Writing Status"]) - (ci("Science") + ci("Social Studies") + ci("Combined Writing")) / 3) <= 0.06,
        f"science/social studies/writing status is the mean of the three content indexes: {code}")
    for ind, _ in W:
        if f(r[f"{ind} Status"]) is None:
            continue
        chk(abs(f(r[f"{ind} Combined Indicator Rate"]) - (f(r[f"{ind} Status"]) + f(r[f"{ind} Change"]))) <= 0.06,
            f"combined rate is status plus change: {code} {ind}")
    chk(abs(weighted(r, "Combined Indicator Rate") - f(r["Overall Combined Indicator Rate"])) <= 0.1,
        f"published overall reproduces from KDE's 51/40/5/4 weights: {code}")
    status_only[code] = round(weighted(r, "Status"), 1)
# statewide: the same weights reproduce every elementary overall; rank and cut claims
ES_W = [("Reading_Mathematics Status", 51), ("Science_Social Studies_Combined Writing Status", 40),
        ("English Learners Progress Status", 5), ("Quality Of School Climate and Safety Status", 4)]
def so(r):
    avail = [(f(r[c]), w) for c, w in ES_W if f(r[c]) is not None]
    return sum(v * w for v, w in avail) / sum(w for _, w in avail)
rated = [r for r in es_all if f(r["Overall Combined Indicator Rate"]) is not None]
chk(len(rated) == 715, f"715 rated elementary schools statewide (found {len(rated)})")
by_status = sorted(rated, key=so)
by_overall = sorted(rated, key=lambda r: f(r["Overall Combined Indicator Rate"]))
rank_status = 1 + [r["School Code"] for r in by_status].index("041090")
rank_overall = 1 + [r["School Code"] for r in by_overall].index("041090")
chk(rank_status == 35 and rank_overall == 2, f"NMES ranks 35th lowest on status-only and 2nd lowest on the official overall (found {rank_status}, {rank_overall})")
csi_es = [r for r in rated if r["Federal Classification"].strip() == "CSI" and f(r["Overall Combined Federal Rate"]) is not None]
non_es = [r for r in rated if r["Federal Classification"].strip() != "CSI" and f(r["Overall Combined Federal Rate"]) is not None]
hi, lo = max(f(r["Overall Combined Federal Rate"]) for r in csi_es), min(f(r["Overall Combined Federal Rate"]) for r in non_es)
chk(len(csi_es) == 33 and hi == 37.6 and lo == 38.2 and f(PR[("041090", "ES")]["Overall Combined Federal Rate"]) == 33.0,
    f"33 CSI elementary schools; the federal cut sits between {hi} and {lo}; NMES's federal rate is 33.0")
c_rows = [r for r in csi if r["List"] == "CSI"]
chk(len(c_rows) == 53 and sum(r["Number of years identified"] == "1" for r in c_rows) == 19
    and sum(r["District"] == "Jefferson County" for r in c_rows) == 38
    and [r for r in c_rows if r["District"] == "Bourbon County"] == [r for r in c_rows if r["School"] == "North Middletown Elementary School"]
    and any(r["School"] == "North Middletown Elementary School" and r["Title 1"] == "Y" and r["Reason for Federal Classification"] == "Bottom 5%" for r in c_rows),
    "CSI roster: 53 schools, 19 new, 38 in Jefferson County, NMES the only Bourbon County school, Title I, bottom 5 percent")

# ---------- 3. the site carries the numbers unchanged
SHOW = {"Combined Writing": "Writing"}
prev = json.load(open(B / "kde_ksa_2024_25.json"))
sec = html[html.index("The state's own numbers, 2024-25 and 2025-26"):html.index("Status, not change")]
for s in SUBJ:
    cells = []
    for c in ("041090", "041010", "041030"):
        cells += [prev["schools"][CODES[c]][s], ksa["schools"][CODES[c]][s]]
    cells += [prev["state_elementary"][s], ksa["state_elementary"][s]]
    want = "".join(f"<td>{e['PD']} ({e['CI']})</td>" for e in cells)
    chk(f"<tr><td>{SHOW.get(s, s)}</td>{want}</tr>" in sec, f"site combined table row matches both archives: {s}")
st = html[html.index("Status, not change"):html.index("Two decades of scores")]
order = ["041090", "041010", "041030", "478010", "999"]
def cells(getter):
    return "".join(f"<td>{getter(PR[(c, 'ES')])}</td>" for c in order)
for label, field in [("Reading and mathematics", "Reading_Mathematics Status"), ("Science, social studies and writing", "Science_Social Studies_Combined Writing Status"),
                     ("Climate and safety survey", "Quality Of School Climate and Safety Status")]:
    vals = [PR[(c, "ES")][field] for c in order]
    chk(all(f"<td>{v} (" in st for v in vals), f"site status table row carries KDE's published status: {label}")
chk(cells(lambda r: f"{status_only[r['School Code']]:.1f}") in st, "site status-only overall row equals the 51/40/5/4 weighting of KDE's statuses")
chk(all(f"<td>{PR[(c, 'ES')]['Overall Combined Indicator Rate']} (" in st for c in order), "site official overall row carries KDE's published overall")
m = re.search(r"var K26=(\{.*?\});\n", html)
K26 = json.loads(m.group(1)) if m else {}
chk(bool(m) and K26.get("NMES") == [f(ksa["schools"][CODES["041090"]][s]["CI"]) for s in SUBJ]
    and K26.get("BC") == [f(ksa["schools"][CODES["041010"]][s]["CI"]) for s in SUBJ]
    and K26.get("CR") == [f(ksa["schools"][CODES["041030"]][s]["CI"]) for s in SUBJ]
    and K26.get("KY") == [f(ksa["state_elementary"][s]["CI"]) for s in SUBJ],
    "status chart data (K26) equals the archived content indexes")
def last(series, key):
    block = re.search(r"\n" + series + r":\{\n(.*?\])\},", html, re.S).group(1)
    arr = re.search(r"(?m)^" + key + r":\[(.*?)\]", block).group(1).split(",")
    return None if arr[-1] == "null" else float(arr[-1]), len(arr)
pd = lambda c, s: f(ksa["schools"][CODES[c]][s]["PD"])
def oth(c):
    vals = [pd(c, s) for s in ("Science", "Social Studies", "Combined Writing") if pd(c, s) is not None]
    return round(sum(vals) / len(vals), 1) if vals else None
for key, c in [("NMES", "041090"), ("BC", "041010"), ("CR", "041030"), ("PE", "478010")]:
    chk(last("comp", key) == (f(PR[(c, "ES")]["Overall Combined Indicator Rate"]), 20), f"history chart 2026 composite point: {key}")
    chk(last("pd", key) == (round((pd(c, "Reading") + pd(c, "Mathematics")) / 2, 1), 20), f"history chart 2026 reading/math point: {key}")
    chk(last("oth", key) == (oth(c), 20), f"history chart 2026 science/social studies/writing point: {key}")
    chk(last("sd", key) == (None, 20), f"history chart 2026 SchoolDigger point empty: {key}")
chk("for(var y=2007;y<=2026;y++)" in html and "from 2007 to 2026" in html, "history chart runs to 2026")
m = re.search(r"var LVD=(\{.*?\});\n", html)
LVD = json.loads(m.group(1)) if m else {}
chk(LVD.get("2025-26") == lv26 and LVD.get("2024-25") == lv25, "grade-level breakout carries both years exactly as archived")
chk('name="lvYear" value="2025-26" checked' in html and "render('2025-26')" in html, "grade-level breakout defaults to 2025-26 with a year toggle")
for needle in ["one of 53 statewide", "35th lowest of Kentucky's 715 elementary schools", "ranks second lowest",
               "last in the county in every subject", 'id="chartStatus"', "status-only 39.1"]:
    chk(needle in html, f"site sentence present: {needle}")
nmes_ci = [f(ksa["schools"][CODES["041090"]][s]["CI"]) for s in SUBJ]
others = [[f(ksa["schools"][CODES[c]][s]["CI"]) for s in SUBJ] for c in ("041010", "041030", "478010")]
chk(all(nmes_ci[i] <= min(o[i] for o in others) for i in range(5)), "NMES's content index is lowest of the four county elementaries in every subject (backs 'last in the county')")
chk(status_only["041090"] == 39.1 and f(PR[("041090", "ES")]["Overall Combined Indicator Rate"]) == 18.2, "NMES status-only overall 39.1 against the official 18.2")

for needle in ["had the county's best test scores for a decade", "close the county's smallest school", "one bad year explained grade by grade"]:
    chk(needle in html, f"stale best-school claim replaced: {needle}")

print(f"PASS {len(ok)}")
print(f"FAIL {len(bad)}")
for b in bad:
    print("  -", b)
sys.exit(1 if bad else 0)
