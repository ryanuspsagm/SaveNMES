#!/usr/bin/env python3
"""Pull KDE's 2025-26 Assessment and Accountability datasets and extract the
Bourbon County Schools, Paris Independent and state rows.

    python build/fetch_kde_acct_2026.py [raw_dir]

raw_dir (default ~/Downloads/kde_acct_2026) receives the four KDE files, about
83 MB, downloaded with a browser User-Agent because education.ky.gov answers
plain clients with HTTP 403; files already present and non-empty are reused.
Outputs, all under build/: kde_acct_2026_*.csv (raw KDE rows for the two
districts and the state, every elementary school's overall and status columns,
plus the statewide CSI/TSI/ATSI lists),
kde_ksa_2025_26.json and kde_levels_2025_26.json (same shapes as the 2024-25
files), kde_acct_2026_manifest.json (URLs, sizes, MD5s) and
ksa_2025_26_comparison.md (the comparison note). Companion to
kde_ksa_2024_25.json; nothing on the site reads these files yet."""
import csv, json, os, sys, zipfile, hashlib, urllib.request, urllib.parse
import xml.etree.ElementTree as ET
from collections import Counter

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
RETRIEVED = "2026-10-15"
PAGE = "https://www.education.ky.gov/Open-House/data/Pages/Assessment_Accountability_Datasets_2025-2026.aspx"
BASE = "https://www.education.ky.gov/Open-House/data/OAA Temporary Datasets/"
FILES = {
    "profile": "Accountable_Profile_2026.CSV",
    "assessment": "Accountable_Assessment_Performance_2026.CSV",
    "by_grade": "Assessment_Performance_by_Grade_2026.CSV",
    "csi": "ACCT_CSI_TSI_ATSI_2026.xlsx",
}
SUBJECTS = ["Reading", "Mathematics", "Science", "Social Studies", "Combined Writing"]
ELEM = {"041010": "Bourbon Central Elementary School", "041030": "Cane Ridge Elementary School",
        "041090": "North Middletown Elementary School", "478010": "Paris Elementary School"}
SHORT = {"041010": "BCES", "041030": "CRES", "041090": "NMES", "478010": "PES", "041": "District", "999": "Kentucky"}
HIST = {"041010": "BC", "041030": "CR", "041090": "NMES", "478010": "PE"}
COLOR = {"1": "red", "2": "orange", "3": "yellow", "4": "green", "5": "blue"}

def download(raw):
    os.makedirs(raw, exist_ok=True)
    for name in FILES.values():
        path = os.path.join(raw, name)
        if os.path.exists(path) and os.path.getsize(path) > 0:
            print("have", name)
            continue
        url = urllib.parse.quote(BASE + name, safe=":/")
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
        with urllib.request.urlopen(req, timeout=600) as r, open(path, "wb") as f:
            while True:
                chunk = r.read(1 << 20)
                if not chunk:
                    break
                f.write(chunk)
        size = os.path.getsize(path)
        print("fetched", name, size, "bytes")
        if size == 0:
            sys.exit("KDE served %s as an empty file; try again later" % name)

def extract(DL, BUILD):
    def keep(code):
        return code.startswith("041") or code.startswith("478") or code == "999"

    def read_filtered(name, code_col):
        with open(os.path.join(DL, name), newline="", encoding="utf-8-sig") as f:
            r = csv.reader(f)
            hdr = next(r)
            rows = [row for row in r if len(row) > code_col and keep(row[code_col])]
        return hdr, rows

    def write_csv(path, hdr, rows):
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(hdr)
            w.writerows(rows)

    def md5(path):
        h = hashlib.md5()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest()

    # ---------- 1. raw extracts ----------
    p_hdr, p_rows = read_filtered(FILES["profile"], 1)
    a_hdr, a_rows = read_filtered(FILES["assessment"], 0)
    g_hdr, g_rows = read_filtered(FILES["by_grade"], 0)
    write_csv(os.path.join(BUILD, "kde_acct_2026_profile_bourbon.csv"), p_hdr, p_rows)
    # every elementary school in the state, overall and status columns only: backs the
    # bottom-5-percent cut and the statewide rank claims on the site (tests/verify_kde_2026.py)
    ES_COLS = ["School Code", "District Name", "School Name", "Federal Classification", "Reason for Federal Classifcation",
               "Overall Combined Indicator Rate", "Overall Indicator Rating", "Overall Combined Federal Rate",
               "Reading_Mathematics Status", "Science_Social Studies_Combined Writing Status",
               "English Learners Progress Status", "Quality Of School Climate and Safety Status"]
    with open(os.path.join(DL, FILES["profile"]), newline="", encoding="utf-8-sig") as fh:
        rd = csv.DictReader(fh)
        es_rows = [[d[c] for c in ES_COLS] for d in rd if d["Level"] == "ES" and d["School Name"]]
    write_csv(os.path.join(BUILD, "kde_acct_2026_profile_es_statewide.csv"), ES_COLS, es_rows)
    write_csv(os.path.join(BUILD, "kde_acct_2026_assessment_performance_bourbon.csv"), a_hdr, a_rows)
    write_csv(os.path.join(BUILD, "kde_acct_2026_by_grade_bourbon.csv"), g_hdr, g_rows)

    # CSI / TSI / ATSI workbook (statewide, small) flattened without openpyxl
    z = zipfile.ZipFile(os.path.join(DL, FILES["csi"]))
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    ss = []
    for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", ns):
        ss.append("".join(t.text or "" for t in si.iter("{%s}t" % ns["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    sheet_names = [s.get("name") for s in wb.find("m:sheets", ns)]
    OUT_COLS = ["List", "Code", "District", "School", "Type", "School Level", "Title 1",
                "Federal Classification", "Number of years identified", "Reason for Federal Classification"]
    csi_rows = []
    for i, sheet in enumerate(sorted(n for n in z.namelist() if n.startswith("xl/worksheets/sheet"))):
        root = ET.fromstring(z.read(sheet))
        rows = []
        for r in root.iter("{%s}row" % ns["m"]):
            vals = []
            for c in r.findall("m:c", ns):
                v = c.find("m:v", ns)
                if v is None:
                    vals.append("")
                else:
                    vals.append(ss[int(v.text)] if c.get("t") == "s" else v.text)
            rows.append([x.strip() for x in vals])
        hdr = rows[0]
        for row in rows[1:]:
            d = dict(zip(hdr, row))
            csi_rows.append([sheet_names[i]] + [d.get(c, "") for c in OUT_COLS[1:]])
    write_csv(os.path.join(BUILD, "kde_acct_2026_csi_tsi_atsi_statewide.csv"), OUT_COLS, csi_rows)
    csi_counts = {}
    for row in csi_rows:
        csi_counts[row[0]] = csi_counts.get(row[0], 0) + 1
    bourbon_lists = [row for row in csi_rows if row[2] in ("Bourbon County", "Paris Independent")]

    # ---------- 2. JSON in the repo's 2024-25 shapes ----------
    A = {}  # (code, level, demographic, subject) -> row dict
    for row in a_rows:
        d = dict(zip(a_hdr, row))
        A[(d["School Code"], d["Level"], d["Demographic"], d["Subject"])] = d

    def subj_entry(code, subject, level="ES"):
        d = A[(code, level, "All Students", subject)]
        sup = d["Suppressed"] == "Y"
        return {"P": "*" if sup else d["Proficient"], "D": "*" if sup else d["Distinguished"],
                "PD": "*" if sup else d["Proficient/Distinguished"],
                "CI": d["Content Index"] if d["Content Index"] else "*",
                "suppressed": "Y" if sup else "N"}

    P = {}
    for row in p_rows:
        d = dict(zip(p_hdr, row))
        P[(d["School Code"], d["Level"])] = d

    def profile_entry(code, level="ES"):
        d = P[(code, level)]
        g = lambda k: d.get(k, "")
        return {
            "federal_classification": g("Federal Classification"), "federal_reason": g("Reason for Federal Classifcation"),
            "overall_combined_indicator_rate": g("Overall Combined Indicator Rate"), "overall_indicator_rating": g("Overall Indicator Rating"),
            "overall_combined_federal_rate": g("Overall Combined Federal Rate"),
            "reading_math": {"status": g("Reading_Mathematics Status"), "status_rating": g("Reading_Mathematics Statue Rating"),
                              "change": g("Reading_Mathematics Change"), "change_rating": g("Reading_Mathematics Change Rating"),
                              "combined_rate": g("Reading_Mathematics Combined Indicator Rate"), "combined_rating": g("Reading_Mathematics Combined Indicator Rating")},
            "science_social_studies_writing": {"status": g("Science_Social Studies_Combined Writing Status"), "status_rating": g("Science_Social Studies_Combined Writing Statue Rating"),
                              "change": g("Science_Social Studies_Combined Writing Change"), "change_rating": g("Science_Social Studies_Combined Writing Change Rating"),
                              "combined_rate": g("Science_Social Studies_Combined Writing Combined Indicator Rate"), "combined_rating": g("Science_Social Studies_Combined Writing Combined Indicator Rating")},
            "english_learner_progress": {"status": g("English Learners Progress Status"), "change": g("English Learners Progress Change"),
                              "combined_rate": g("English Learners Progress Combined Indicator Rate"), "combined_rating": g("English Learners Progress Combined Indicator Rating")},
            "quality_of_school_climate_and_safety": {"status": g("Quality Of School Climate and Safety Status"), "status_rating": g("Quality Of School Climate and Safety Statue Rating"),
                              "change": g("Quality Of School Climate and Safety Change"), "change_rating": g("Quality Of School Climate and Safety Change Rating"),
                              "combined_rate": g("Quality Of School Climate and Safety Combined Indicator Rate"), "combined_rating": g("Quality Of School Climate and Safety Combined Indicator Rating")},
        }

    ksa = {
        "source": "Kentucky Department of Education, Assessment and Accountability Data 2025-2026 (page published 10/14/2026): Accountable_Assessment_Performance_2026.CSV (performance levels and content index, all students, elementary level) and Accountable_Profile_2026.CSV (indicator status, change, combined rates, ratings and federal classification). Downloaded " + RETRIEVED + " from " + PAGE + ". Percentages as published by KDE; suppressed cells marked *; KDE still publishes the content index for most suppressed cells.",
        "retrieved": RETRIEVED,
        "schools": {ELEM[c]: {s: subj_entry(c, s) for s in SUBJECTS} for c in ELEM},
        "district_elementary": {s: subj_entry("041", s) for s in SUBJECTS},
        "paris_independent_elementary": {s: subj_entry("478", s) for s in SUBJECTS},
        "state_elementary": {s: subj_entry("999", s) for s in SUBJECTS},
        "profile": {**{ELEM[c]: profile_entry(c) for c in ELEM}, "Bourbon County (district, ES)": profile_entry("041"),
                    "Paris Independent (district, ES)": profile_entry("478"), "Kentucky (ES)": profile_entry("999")},
        "rating_colors": {"1": "red (lowest)", "2": "orange", "3": "yellow", "4": "green", "5": "blue (highest)"},
    }
    json.dump(ksa, open(os.path.join(BUILD, "kde_ksa_2025_26.json"), "w"), indent=1)

    # by-grade levels
    GRADE = {"03": "3rd", "04": "4th", "05": "5th"}
    SUBJ_FIX = {"Editing and Mechanic": "Editing and Mechanics"}
    ORDER = ["Mathematics", "Reading", "Science", "Editing and Mechanics", "On Demand Writing", "Social Studies"]
    levels = {s: {} for s in ORDER}
    for row in g_rows:
        d = dict(zip(g_hdr, row))
        if d["Demographic"] != "All Students" or d["Grade"] not in GRADE or d["School Code"] not in SHORT:
            continue
        subj = SUBJ_FIX.get(d["Subject"], d["Subject"])
        if subj not in levels:
            continue
        grade = GRADE[d["Grade"]]
        levels[subj].setdefault(grade, {})
        if d["Suppressed"] == "Y" or d["Proficient/Distinguished"] == "":
            val = None
        else:
            val = [int(d[k]) for k in ("Novice", "Apprentice", "Proficient", "Distinguished", "Proficient/Distinguished")]
        levels[subj][grade][SHORT[d["School Code"]]] = val
    KEYS = ["BCES", "CRES", "NMES", "PES", "District", "Kentucky"]
    for s in levels:
        for g in levels[s]:
            levels[s][g] = {k: levels[s][g].get(k) for k in KEYS}
    lv = {
        "source": "Kentucky Department of Education, Assessment and Accountability Data 2025-2026: Assessment_Performance_by_Grade_2026.CSV (performance levels by grade, all students tested), downloaded " + RETRIEVED + " from " + PAGE + ". Rows trimmed to the three Bourbon County Schools elementaries, Paris Elementary (PES), the Bourbon County district and state totals. Values are percentages as published by KDE, including its own rounded Proficient/Distinguished column; nulls are state-suppressed cells. Grade-level tested counts are not in this release (they come with the School Report Card enrollment file later in the fall).",
        "retrieved": RETRIEVED,
        "levels": levels,
        "tested_by_grade": None,
    }
    json.dump(lv, open(os.path.join(BUILD, "kde_levels_2025_26.json"), "w"), indent=1)

    # manifest
    man = {"page": PAGE, "page_published": "10/14/2026 3:55 PM (as shown on the page)", "retrieved": RETRIEVED,
           "note": "Downloaded with a browser User-Agent; education.ky.gov answers plain curl with HTTP 403. Accountable_Summary_2026.CSV and All_Datasets_Archive.Zip were served with Content-Length 0 (origin last-modified 2026-10-15 04:42 UTC) on three attempts and are not archived.",
           "files": []}
    for k, name in FILES.items():
        path = os.path.join(DL, name)
        man["files"].append({"name": name, "url": BASE + name, "bytes": os.path.getsize(path), "md5": md5(path), "role": k})
    json.dump(man, open(os.path.join(BUILD, "kde_acct_2026_manifest.json"), "w"), indent=1)

    print("wrote extracts, json and manifest to", BUILD)

def note(BUILD, MD):
    ksa = json.load(open(os.path.join(BUILD, "kde_ksa_2025_26.json")))
    lv = json.load(open(os.path.join(BUILD, "kde_levels_2025_26.json")))
    man = json.load(open(os.path.join(BUILD, "kde_acct_2026_manifest.json")))
    prev = json.load(open(os.path.join(BUILD, "kde_ksa_2024_25.json")))
    prev_levels = json.load(open(os.path.join(BUILD, "kde_levels_2024_25.json")))
    hist = json.load(open(os.path.join(BUILD, "kde_scores_history.json")))
    csi = list(csv.DictReader(open(os.path.join(BUILD, "kde_acct_2026_csi_tsi_atsi_statewide.csv"))))
    prev_comp = hist["official_composite"]["2024-25"]
    SUBJECTS = ["Reading", "Mathematics", "Science", "Social Studies", "Combined Writing"]
    NAMES = {"BCES": "Bourbon Central Elementary School", "CRES": "Cane Ridge Elementary School",
             "NMES": "North Middletown Elementary School", "PES": "Paris Elementary School"}
    LABEL = {"BCES": "Bourbon Central", "CRES": "Cane Ridge", "NMES": "North Middletown", "PES": "Paris Elem. (Paris Ind.)"}
    COLOR = {"1": "red", "2": "orange", "3": "yellow", "4": "green", "5": "blue"}

    def num(x):
        try:
            return float(x)
        except (TypeError, ValueError):
            return None

    def cell(cur, old, dec=0):
        c, o = num(cur), num(old)
        if c is None:
            return "*" + (f" (24-25: {old})" if o is not None else "")
        if o is None:
            return f"{cur}" + (" (24-25: *)" if old == "*" else "")
        return f"{cur} ({c - o:+.{dec}f})"

    L = []
    L.append("# 2025-26 KDE accountability results: Bourbon County elementaries compared\n")
    L.append(f"Working note, not published on the site. Data: KDE Assessment and Accountability Data 2025-2026 (page published 10/14/2026), downloaded {man['retrieved']}; provenance in `build/kde_acct_2026_manifest.json`, extracted rows in `build/kde_acct_2026_*.csv`, and the same shapes as last year's files in `build/kde_ksa_2025_26.json` and `build/kde_levels_2025_26.json`. All-students rows, elementary level, as KDE published them. Figures in parentheses are the change from 2024-25 (`build/kde_ksa_2024_25.json`). Asterisks are KDE-suppressed cells. Regenerate everything with `python build/fetch_kde_acct_2026.py`.\n")

    L.append("## Headline\n")
    L.append("- North Middletown posted the lowest result of the four county elementaries in every subject, after being first in every subject in 2024-25. Reading fell from 41 to 21 percent proficient or distinguished (49 percent novice); math from 31 to 23. Science, social studies and writing are suppressed this year, but KDE still publishes their content indexes: 58.7, 22.2 and 25.0 against 75.0, 47.0 and 77.0 last year.")
    L.append("- NMES's overall indicator rate is 18.2, rating 1 (red), against 54.0 in 2024-25 and 74.5 in 2023-24. Both assessment indicators are red; climate and safety (a student survey) is yellow at 73.8.")
    L.append("- KDE has identified NMES for Comprehensive Support and Improvement (CSI), reason \"Bottom 5%\", first year identified. It is one of 53 CSI schools statewide, 19 of them newly identified this year and 38 of the 53 in Jefferson County; it is the only CSI school in Bourbon County.")
    L.append("- Bourbon Central: 54.1 (orange). Reading up 8 points to 46, math up 6 to 34, writing down 13 to 27. Its reading/math indicator is green; it is on the TSI list for students with disabilities.")
    L.append("- Cane Ridge: 55.9 (yellow), now the district's highest overall. Science, social studies and writing combined is green (social studies up 5 to 32); reading 40 (+3), math 25 (-2).")
    L.append("- Paris Elementary (Paris Independent): 52.6 (orange), up on the content index in four of five subjects (social studies the exception), and above NMES in every subject this year.")
    L.append("- Every county elementary, and the Bourbon County district as a whole, is below the Kentucky elementary average in every subject. Last year NMES beat the state in science and writing; no county school does now.\n")

    cols = ["BCES", "CRES", "NMES", "PES"]
    L.append("## 1. Percent proficient or distinguished, by subject\n")
    L.append("| Subject | " + " | ".join(LABEL[c] for c in cols) + " | BCS district | KY elementary |")
    L.append("|---|" + "---|" * (len(cols) + 2))
    for s in SUBJECTS:
        row = [s] + [cell(ksa["schools"][NAMES[c]][s]["PD"], prev["schools"][NAMES[c]][s]["PD"]) for c in cols]
        row.append(ksa["district_elementary"][s]["PD"])
        row.append(cell(ksa["state_elementary"][s]["PD"], prev["state_elementary"][s]["PD"]))
        L.append("| " + " | ".join(row) + " |")
    L.append("")
    L.append("## 2. Content index, by subject\n")
    L.append("The content index (0 to 125: novice 0, apprentice 0.5, proficient 1, distinguished 1.25) is what the accountability status is built from, and KDE publishes it even for most suppressed cells, so it is the only like-for-like measure for NMES's science, social studies and writing this year.\n")
    L.append("| Subject | " + " | ".join(LABEL[c] for c in cols) + " | BCS district | KY elementary |")
    L.append("|---|" + "---|" * (len(cols) + 2))
    for s in SUBJECTS:
        row = [s] + [cell(ksa["schools"][NAMES[c]][s]["CI"], prev["schools"][NAMES[c]][s]["CI"], 1) for c in cols]
        row.append(ksa["district_elementary"][s]["CI"])
        row.append(cell(ksa["state_elementary"][s]["CI"], prev["state_elementary"][s]["CI"], 1))
        L.append("| " + " | ".join(row) + " |")
    L.append("")

    L.append("## 3. Rank among the three Bourbon County Schools elementaries\n")
    L.append("Ranked on percent proficient or distinguished where all three are published, otherwise on the content index (marked CI). Paris Elementary is in a separate district and is left out of the ranking; it is above NMES on every row.\n")
    L.append("| Subject | Order (high to low) | basis |")
    L.append("|---|---|---|")
    for s in SUBJECTS:
        vals = [(num(ksa["schools"][NAMES[c]][s]["PD"]), LABEL[c]) for c in ("BCES", "CRES", "NMES")]
        basis = "P/D %"
        if any(v is None for v, _ in vals):
            vals = [(num(ksa["schools"][NAMES[c]][s]["CI"]), LABEL[c]) for c in ("BCES", "CRES", "NMES")]
            basis = "CI"
        vals.sort(key=lambda t: -t[0])
        parts, i = [], 0
        while i < len(vals):
            j = i
            while j + 1 < len(vals) and vals[j + 1][0] == vals[i][0]:
                j += 1
            group = vals[i:j + 1]
            parts.append((" = ".join(lab for _, lab in group)) + f" ({vals[i][0]:g})" + (" tied" if len(group) > 1 else ""))
            i = j + 1
        L.append(f"| {s} | " + " > ".join(parts) + f" | {basis} |")
    L.append("")

    L.append("## 4. Accountability profile (status, change, combined rate, rating)\n")
    L.append("Rating colors: 1 red, 2 orange, 3 yellow, 4 green, 5 blue. In KDE's file the combined indicator rate equals status plus change, and the reading/math status equals the mean of the two content indexes (science, social studies and writing: the mean of the three); both identities check against every row below.\n")
    L.append("| School | Overall rate (rating) | Overall 24-25 | R/M status | R/M change | R/M combined (rating) | Sci/SS/W status | Sci/SS/W change | Sci/SS/W combined (rating) | Climate & safety (rating) | Federal classification |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|")
    prof_rows = [(NAMES["BCES"], "Bourbon Central", prev_comp["BC"][0]), (NAMES["CRES"], "Cane Ridge", prev_comp["CR"][0]),
                 (NAMES["NMES"], "North Middletown", prev_comp["NMES"][0]), (NAMES["PES"], "Paris Elementary", prev_comp["PE"][0]),
                 ("Bourbon County (district, ES)", "BCS district (ES)", None), ("Kentucky (ES)", "Kentucky (ES)", None)]
    for key, lab, old in prof_rows:
        p = ksa["profile"][key]
        rm, sw, q = p["reading_math"], p["science_social_studies_writing"], p["quality_of_school_climate_and_safety"]
        fc = (p["federal_classification"] + (" (" + p["federal_reason"] + ")" if p["federal_reason"] else "")) or "none"
        L.append(f"| {lab} | {p['overall_combined_indicator_rate']} ({p['overall_indicator_rating']} {COLOR.get(p['overall_indicator_rating'], '')}) | {old if old is not None else 'n/a'} | {rm['status']} | {rm['change']} | {rm['combined_rate']} ({rm['combined_rating']}) | {sw['status']} | {sw['change']} | {sw['combined_rate']} ({sw['combined_rating']}) | {q['combined_rate']} ({q['combined_rating']}) | {fc} |")
    L.append("")

    L.append("## 5. Grade-level results, percent proficient or distinguished\n")
    L.append("Each cell is this year's grade with the same grade's 2024-25 figure in parentheses (a different cohort of children). Paris has no 2024-25 grade file in the repo.\n")
    L.append("| Grade / subject | Bourbon Central | Cane Ridge | North Middletown | Paris Elem. | BCS district | Kentucky |")
    L.append("|---|---|---|---|---|---|---|")
    KEYS = ["BCES", "CRES", "NMES", "PES", "District", "Kentucky"]
    pd_of = lambda v: "*" if v is None else str(v[4])
    for s in ["Reading", "Mathematics", "Science", "Social Studies", "On Demand Writing", "Editing and Mechanics"]:
        for g in ["3rd", "4th", "5th"]:
            if g not in lv["levels"][s]:
                continue
            row = [f"{g} {s}"]
            for k in KEYS:
                cur = lv["levels"][s][g].get(k)
                if k == "PES":
                    row.append(pd_of(cur))
                else:
                    old = (prev_levels["levels"].get(s, {}).get(g, {}) or {}).get(k)
                    row.append(f"{pd_of(cur)} ({pd_of(old)})")
            L.append("| " + " | ".join(row) + " |")
    L.append("")
    L.append("NMES novice shares where published: 3rd grade reading 64 percent, 3rd grade math 36, 4th grade math 52, 5th grade editing and mechanics 47. Statewide 3rd grade reading novice is 23 percent. NMES's published subgroup rows are economically disadvantaged only: reading 18 percent proficient or distinguished, math 27.\n")

    L.append("## 6. Federal classifications (ACCT_CSI_TSI_ATSI_2026.xlsx)\n")
    from collections import Counter
    cnt = Counter(r["List"] for r in csi)
    yrs = Counter(r["Number of years identified"] for r in csi if r["List"] == "CSI")
    L.append("Statewide: " + ", ".join(f"{k} {v}" for k, v in cnt.items()) + f". CSI years identified: " + ", ".join(f"{v} schools in year {k}" for k, v in sorted(yrs.items())) + ". The workbook does not give the identification rule; KDE's 2025 release described CSI as the bottom 5 percent of schools by level on the overall score, a graduation rate under 80 percent, or three years of ATSI, with new schools identified every year since House Bill 298 (2025).\n")
    L.append("| List | School | Level | Title I | Years identified | Reason |")
    L.append("|---|---|---|---|---|---|")
    for r in csi:
        if r["District"] in ("Bourbon County", "Paris Independent"):
            L.append(f"| {r['List']} | {r['School']} | {r['School Level']} | {r['Title 1']} | {r['Number of years identified'] or 'n/a'} | {r['Reason for Federal Classification']} |")
    L.append("")

    L.append("## 7. Reading the numbers\n")
    L.append("- Suppression. Science is tested in 4th grade only, social studies and writing in 5th only, so at NMES each rests on one class. KDE withheld the level percentages for all three (and most of NMES's grade rows) but published the content indexes, which is why the tables above lean on the index.")
    L.append("- Cohort size. KDE's 2024-25 enrollment file counted 26, 19 and 28 students in NMES's 3rd, 4th and 5th grades. This year's 5th grade is last year's 4th, so the social studies and writing results rest on roughly 19 to 20 children, about five points per child. The reading and math figures cover all three grades, about 70 children, where one child is about 1.4 points; a 20-point fall in reading is not sampling noise at that size.")
    L.append("- The rate counts a drop twice. KDE's combined rate is status plus change, so this year's low status (39.2 reading/math, 35.3 science/social studies/writing) is reduced again by the fall from last year (-14.4 and -31.0) to give 24.8 and 4.3. On status alone both indicators rate orange (2); the change component makes them red. The same arithmetic lifted NMES in 2023-24, when rising scores produced the 74.5 the site and report cite. The overall rate is a weighted blend of the indicator rates in which the two assessment indicators carry nearly all the weight.")
    L.append("- Second year of decline in reading and math. KDE's 2024-25 file already showed NMES's reading/math change negative for both subgroups it published (-9.6 economically disadvantaged, -10.9 white); the all-students status implied by this year's file was 53.6 in 2024-25 and is 39.2 now.")
    L.append("- What CSI brings. For the schools identified in 2025, KDE described the process (Kentucky Teacher, December 2025, https://www.kentuckyteacher.org/news/2025/12/kentucky-board-of-education-discusses-recent-assessment-and-accountability-results-focuses-on-student-achievement/): an education recovery support team works with the school, KDE and Cognia run a diagnostic review, a turnaround team of school and community leaders writes an improvement plan, and the school becomes eligible to apply for federal school improvement funds. The same article gives the identification rule (bottom 5 percent of schools by level, graduation rate under 80 percent, or three years of ATSI) and says identification is now annual under House Bill 298 (2025). Kentucky's exit rules are worth reading in KDE's CSI guidance before the site says anything. Note the tension: the district is weighing closure of a school the state has just placed in a required improvement process.")
    L.append("- Not yet available. KDE served the Accountable_Summary_2026.CSV (subgroup indicator rates) and the all-datasets zip as empty files on three tries (content-length 0, origin last-modified this morning); the School Report Card suite with grade enrollment counts comes later in the fall. Re-pull both before any publication.\n")

    L.append("## 8. Where the site carries 2025-26, and what still shows 2024-25\n")
    L.append("- `index.html`, Fact One: the lede, one two-year table (2024-25 and 2025-26 percent proficient or distinguished with the content index), the status table (status only, with the status-only overall from KDE's 51/40/5/4 weights), the status chart (`chartStatus`), the 2026 points on the two-decades chart, and a 2025-26 / 2024-25 toggle on the grade-level breakout. `tests/verify_kde_2026.py` ties each of those numbers to the archived rows.")
    L.append("- The report builder still carries the 2024-25 claim at `build/build_pdf.py` lines 319 to 326 and the model at `build/build_model.py` lines 1218, 1243 and 1262; the committed report (v5.0, August 17) predates the release and the site says so. A report revision is a separate job.")
    L.append("- `build/kde_scores_history.json` and `build/kde_subjects_history.json`, which feed the report's charts, were left at 2024-25 for the same reason; the entries to append are in section 9.\n")
    L.append("## 9. Series entries to append to the history files with the next report revision\n")
    L.append("```")
    L.append('kde_scores_history.json  reading_pd 2025-26: NMES 21, BC 46, CR 40, PE 31')
    L.append('                         math_pd    2025-26: NMES 23, BC 34, CR 25, PE 31')
    L.append('                         official_composite 2025-26: NMES 18.2, BC 54.1, CR 55.9, PE 52.6')
    L.append('                         state_elementary_pd 2025-26: Reading 50, Mathematics 43')
    L.append('kde_subjects_history.json per_subject 2025-26: BC Science 31 / Social Studies 30 / Writing 27;')
    L.append('                         CR 32 / 32 / 29; NMES null / null / null (suppressed; CI 58.7 / 22.2 / 25.0);')
    L.append('                         PE 23 / 18 / 12.  avg: BC 29.3, CR 31.0, NMES null, PE 17.7')
    L.append("```\n")

    L.append("## 10. Provenance\n")
    L.append(f"Page: {man['page']} (published {man['page_published']}). Retrieved {man['retrieved']}. {man['note']}\n")
    L.append("| File | Bytes | MD5 |")
    L.append("|---|---|---|")
    for f in man["files"]:
        L.append(f"| {f['name']} | {f['bytes']:,} | {f['md5']} |")
    L.append("")
    open(MD, "w").write("\n".join(L))
    print("wrote", MD)

if __name__ == "__main__":
    raw = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/Downloads/kde_acct_2026")
    build = os.path.dirname(os.path.abspath(__file__))
    download(raw)
    extract(raw, build)
    note(build, os.path.join(build, "ksa_2025_26_comparison.md"))
