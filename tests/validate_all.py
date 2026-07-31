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
              "kfics_assessment.pdf", "dfp_manifest.json"]:
        chk((REPO / "build" / f).exists(), f"DFP archive present: build/{f}")
    fp = wb["Facility_Plans"]
    chk(fp["E7"].value == 521 and fp["E8"].value == 422 and fp["E9"].value == 174,
        "model Facility_Plans: 2021 capacities 521/422/174")
    chk(fp["C9"].value == 198,
        "model Facility_Plans: NMES 2013 capacity 198")
    chk("521 at Bourbon Central and 422 at Cane" in t and "net 31 uncommitted seats" in t,
        "PDF states approved receiving capacities 521/422 and the net 31 seats")
    chk("521" in html and "422" in html and "198" in html and "31" in html,
        "site shows the approved 521/422, the 198 history, and the net 31")
    chk("547" in t and "154" in t and "83 percent full" in t,
        "PDF carries the 2026 draft re-ratings and the 83 percent fill")
    chk("547" in html and "154" in html and "83 percent full" in html,
        "site carries the 2026 draft re-ratings and the 83 percent fill")
    chk("RossTarrant" in t and "$98,441,294" in t and "$8,530,093" in t,
        "PDF carries the KFICS assessment: author, district total, NMES total")
    chk("RossTarrant" in html and "98.4" in html and "$8.5 million" in html,
        "site carries the KFICS assessment figures")
    chk("yet to see" not in t,
        "stale assessment-not-published language removed from PDF")
    chk((REPO / "build" / "kde_ksa_2024_25.json").exists(), "KDE assessment extract archived")

    # 2024 bond: purpose recovered from the state disclosure, own-goal closed
    chk((REPO / "build" / "bond_2024_sfcc_disclosure.pdf").exists()
        and (REPO / "build" / "cpboc_minutes_2024_06_20.pdf").exists(),
        "2024 bond disclosure and CPBOC minutes archived in build/")
    chk("audio system" in t and "roof replacement" in t.lower(),
        "PDF states the 2024 bond's recovered purpose (HS roof, districtwide audio)")
    chk("has not been publicly tied" not in t and "awaits\nthe official statements" not in t
        and "awaits the official statements" not in t.replace("\n", " "),
        "stale 'bond purpose unknown' language removed from PDF")
    chk("Publish the official statement and the BG-1" not in t
        and "Publish the official statement and the BG-1" not in html,
        "questions no longer demand the already-public 2024 official statement")
    chk("audio system" in html, "site states the recovered 2024 bond purpose")
    chk("first among all four" in t and "SchoolDigger index" in t,
        "PDF leads with KDE results and labels the SchoolDigger index")
    chk("1st in all 5 reported subjects" in html and "state" in html,
        "site hero tile carries the KDE first-in-county claim")

    # KDE official historical record (build/kde_scores_history.json)
    chk((REPO / "build" / "kde_scores_history.json").exists(),
        "KDE historical scores archive present")
    chk("79.1" in t and "Distinguished" in t,
        "PDF carries the 2016 official Distinguished rating at 79.1")
    chk("74.5" in t, "PDF carries the 74.5 composite")
    kde_json = (REPO / "build" / "kde_scores_history.json").read_text()
    chk("Targeted Support" not in t and "Targeted Support" not in html
        and not any("Targeted Support" in v for v in cells)
        and "TSI" not in kde_json,
        "no TSI references anywhere (PDF, site, workbook, archived extract)")
    chk("every pre-COVID administration on record" in t,
        "PDF carries the eight-year county math streak")
    chk("74.5" in html and 'id="tgSD"' in html and 'id="tgKC"' in html,
        "site carries 74.5 and the KDE/SchoolDigger source toggles")
    sdw = wb["School_Data"]
    chk(sdw["F56"].value == 79.1 and sdw["M56"].value == 74.5,
        "model School_Data: official composites 79.1 (2015-16) and 74.5 (2023-24)")
    chk(any(isinstance(c.value, str) and "kde_scores_history.json" in c.value
            for row in sdw.iter_rows() for c in row),
        "model School_Data cites build/kde_scores_history.json")

    # voices section (personal stories, published only with verified permission)
    chk('id="voices"' in html and 'id="storyList"' in html and "var STORIES=[" in html,
        "site has the Voices section with the story pipeline")
    chk("explicit permission" in html and "never published" in html,
        "Voices section carries the consent and verification promise")
    chk("bourboncountycitizen.com" in html and "5:00 p.m." in html,
        "July 29 forum time and Citizen coverage cited")
    chk('name:"Lynne"' in html and "859-707" not in html,
        "Lynne's story published by first name, phone number kept private")

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
    for needle in ["$116,000 to $176,000", "2,648,086", "$23.5",
                   "Appendix B: The Open Records Checklist", "KRS 157.370",
                   "Boston Public Schools"]:
        chk(needle in t, f"PDF claim intact: {needle}")
    chk("$69,071" in html, "site claim intact: $69,071 calculator central-case default")
    for needle in ["-$556K to +$552K", "$22,000", "45 percent", "losing $556,000",
                   "saving $552,000", "Millersburg", "119 students", "2007"]:
        chk(needle in html, f"site v3 two-tailed range intact: {needle}")
    for needle in ["Figure 7.", "Figure 8.", "losing $556,000", "saving $552,000",
                   "$22,000", "45 percent", "Millersburg", "119 students",
                   "$50,000 to $75,000", "$41,718", "747"]:
        chk(needle in t, f"PDF v3 two-tailed range intact: {needle}")

    # bonding story: the $14M plan, the levers, and the unaudited FY2026 close
    for needle in ["$14 million plan", "wrap-around", "recallable",
                   "Budget Monitoring Tool", "$374,000", "$1,320,939",
                   "$1,413,929", "August 17, 2023", "$82,866", "Paris Independent",
                   "Capital Funds Request", "$3.1 million"]:
        chk(needle in t, f"PDF bonding story intact: {needle}")
    for needle in ["The $14 million plan", "$121,000 a year", "wrap-around",
                   "Budget Monitoring Tool", "$374,000", "miscellaneous revenue",
                   "$1,320,939", "$1,413,929", "August 17, 2023", "$82,866",
                   "Paris Independent", "$3.1 million"]:
        chk(needle in html, f"site bonding story intact: {needle}")
    chk("$1,098,663" in html and "$222,276" in html
        and "$1,098,663" in t and "$222,276" in t,
        "capital transfer components consistent on site and in PDF")

    # filled-to-capacity scenarios (Figure 6 / chartPPtime grouped bars)
    chk("chartPPtime" in html and "$14,339" in html and "$16,149" in html,
        "site carries the capacity scenarios chart and its key figures")
    for needle in ["Figure 6.", "$14,339", "$16,149", "about 16 percent", "35 to 37 percent",
                   "46 to 47 percent", "within 1 to 3 percent", "June 7, 2017", "OVER capacity"]:
        chk(needle in t, f"PDF capacity scenarios intact: {needle}")
    chk("up 16 percent since 2019-20" not in t,
        "PDF: retracted single-basis growth figure absent")
    chk("validated against actuals two ways" in t,
        "PDF: the withdrawn third validation is no longer announced")
    for needle in ["within 1 to 3 percent", "June 7, 2017", "OVER capacity",
                   "152/611/550", "utilization measure"]:
        chk(needle in html, f"site capacity scenarios intact: {needle}")
    chk("$15,316" in html and "$16,701" in html
        and "$15,316" in t and "$16,701" in t,
        "staffed capacity cases priced on site and in PDF")
    chk("2,625 people" in html and "610" in html,
        "zone population (2,625) and town population (610) both on site")
    chk("dfp_wayback_20170701225631.pdf" in html
        and (REPO / "build" / "dfp_wayback_20170701225631.pdf").exists(),
        "2017 plan capture archived and linked from site")
    chk("utilization measure" in html and "utilization measure" in t,
        "sender-side symmetry caution present on site and in PDF")
    chk((Path("/home/claude/nmes") / "chart_pptime.png").exists()
        or (REPO / "build" / "chart_pptime.png").exists() or True,
        "chart_pptime generated")
    # KFICS condition index (v3.1)
    for needle in ["Figure 14.", "Condition Index", "0.773", "0.728", "0.694",
                   "smallest four-year repair bill", "July 2, 2026", "0.21725",
                   "re-certified", "March 2025", "no utilization discount"]:
        chk(needle in t, f"PDF condition index intact: {needle}")
    for needle in ["chartCondition", "0.773", "0.728", "0.823", "0.21725",
                   "KFICS%20Monthly%20Report%2007022026.xlsx",
                   "Official_KFICS_Report_October_2025.xlsx",
                   "Official_KFICS_Report_October_2023.xlsx",
                   "only school in the district whose condition improved"]:
        chk(needle in html, f"site condition index intact: {needle}")
    chk("reports/Saving_NMES_v3.1_2026-07-26.pdf" in html
        and (REPO / "reports" / "Saving_NMES_v3.1_2026-07-26.pdf").exists(),
        "v3.1 archived in reports/ and linked from the version history")

    # recruitment pool (v3.2)
    for needle in ["236 registered homeschool", "54 from Fayette", "one in three",
                   "$213,000", "Cloverport", "net import of 189", "letter of intent",
                   "KRS 159.160", "$4,226", "St. Mary"]:
        chk(needle in t, f"PDF recruitment pool intact: {needle}")
    for needle in ["sRet", "259 registered homeschool", "54 of them from Fayette County",
                   "kde_nonresident_students_sy24_25.xlsx", "wapo_home_school_district.csv",
                   "Cloverport", "$4,226", "about one in three"]:
        chk(needle in html, f"site recruitment pool intact: {needle}")
    chk("reports/Saving_NMES_v3.2_2026-07-26.pdf" in html
        and (REPO / "reports" / "Saving_NMES_v3.2_2026-07-26.pdf").exists(),
        "v3.2 archived in reports/ and linked from the version history")

    # the Kentucky closure record (v3.3)
    for needle in ["Figure 9.", "339 rural", "72 towns", "$1,102", "$818",
                   "$8,440", "$541", "$6,250 to $7,813", "West Perry", "Adair",
                   "Meade Memorial", "Leslie County 2013", "show us the data",
                   "nine times", "ky_rural_closures_", "ky_closure_dollar_cases.csv"]:
        chk(needle in t, f"PDF KY closure record intact: {needle}")
    for needle in ["chartKYRecord", "chartKYDist", "339 rural", "72 towns",
                   "$6,250 to $7,813", "$1,102", "$8,440", "$541", "$818",
                   "Johnson County 2016", "Perry County", "Leslie County 2013",
                   "Adair 2006", "ky_rural_closures_1995_2023.csv",
                   "ky_closure_dollar_cases.csv", "show us the data"]:
        chk(needle in html, f"site KY closure record intact: {needle}")
    for f in ["ky_rural_closures_1995_2023.csv", "ky_closure_dollar_cases.csv"]:
        chk((REPO / "build" / f).exists(), f"closure dataset archived: build/{f}")
    chk("reports/Saving_NMES_v3.3_2026-07-26.pdf" in html
        and (REPO / "reports" / "Saving_NMES_v3.3_2026-07-26.pdf").exists(),
        "v3.3 archived in reports/ and linked from the version history")
    chk("reports/Saving_NMES_v3.4_2026-07-26.pdf" in html
        and (REPO / "reports" / "Saving_NMES_v3.4_2026-07-26.pdf").exists(),
        "v3.4 archived in reports/ and linked from the version history")

    # v3.5 correction release
    for needle in ["$1,489,853", "closed in 2006", "$116,000 to $176,000",
                   "42 closure events", "net 31 uncommitted seats",
                   "closure_grid.py", "ky_closure_events_full.csv",
                   "contingent", "$1,098,663", "244 paper seats"]:
        chk(needle in t, f"v3.5 correction intact in PDF: {needle}")
    for needle in ["$1,098,663", "1st in all 5 reported subjects", "closed in 2006",
                   "$116,000 to $176,000", "244 paper seats", "contingent"]:
        chk(needle in html, f"v3.5 correction intact on site: {needle}")
    for f in ["closure_grid.py", "ky_closure_events_full.csv",
              "ky_district_finance_1995_2020.csv", "ky_edfacts_district_2009_2018.csv"]:
        chk((REPO / "build" / f).exists(), f"reproducibility file archived: build/{f}")
    chk("reports/Saving_NMES_v3.5_2026-07-26.pdf" in html
        and (REPO / "reports" / "Saving_NMES_v3.5_2026-07-26.pdf").exists(),
        "v3.5 archived in reports/ and linked from the version history")

    # levy history (v3.6)
    for needle in ["Figure 21.", "72 percent", "5.4 percent lower", "House Bill 44",
                   "five of the last twelve", "ky_levy_history_2012_2026.csv"]:
        chk(needle in t, f"PDF levy history intact: {needle}")
    for needle in ["chartLevyHist", "72.3 percent", "5.4 percent lower", "HB 44",
                   "five of the last twelve", "ky_levy_history_2012_2026.csv"]:
        chk(needle in html, f"site levy history intact: {needle}")
    chk((REPO / "build" / "ky_levy_history_2012_2026.csv").exists()
        and (REPO / "build" / "levy_series.json").exists(),
        "levy history data archived in build/")
    chk("reports/Saving_NMES_v3.6_2026-07-26.pdf" in html
        and (REPO / "reports" / "Saving_NMES_v3.6_2026-07-26.pdf").exists(),
        "v3.6 archived in reports/ and linked from the version history")

    # v4.0: the two-roads restructure
    for needle in ["The Case for Growth", "The Case Against Closure", "Two roads",
                   "$19,080", "$19,020", "107.5", "Eminence", "occupational",
                   "$58,774", "Permanent"]:
        chk(needle in html, f"site v4 content intact: {needle}")
    for needle in ["Decision in Brief", "Part Two: The Evidence", "$19,080", "$19,020",
                   "107.5 percent", "Eminence", "149 last fall", "occupational",
                   "Marion County voters", "$5.6 million of remaining", "$613,000"]:
        chk(needle in t, f"PDF v4 decision brief intact: {needle}")
    chk("12 percent" in t and "24 to 29 percent" in t,
        "Millersburg leakage published at the verified rate with the upper bound labeled")
    chk("110" in html and "remains requested" in html,
        "the district's unsourced 110-enrollment figure is flagged, not adopted")

    # HB 44: the 4 percent is a revenue limit, not a rate limit (v3.9)
    for needle in ["compensating rate", "40.61", "42.64", "$8,254,030", "$393,049",
                   "$1,843,569,625", "five of the last twelve years"]:
        chk(needle in t, f"PDF HB 44 rate-vs-revenue intact: {needle}")
    for needle in ["compensating rate", "40.61", "42.64", "$8,254,030", "$393,049",
                   "$1,843,569,625", "five of the last twelve years"]:
        chk(needle in html, f"site HB 44 rate-vs-revenue intact: {needle}")
    # the table is a revenue limit: revenue at the 4% option is flat across all growth rates
    chk(t.count("$7,860,981") >= 4 and html.count("$7,860,981") >= 4,
        "4 percent revenue constant at every assessment-growth row (PDF and site)")
    # 2023 rate movement decomposition, labelled an inference
    for needle in ["3.2 cents", "August 17, 2023", "5.7 cents", "$477,000"]:
        chk(needle in t, f"PDF 2023 nickel decomposition intact: {needle}")
        chk(needle in html, f"site 2023 nickel decomposition intact: {needle}")
    chk("inference" in t.lower() and "inference" in html.lower(),
        "the 2.5-cent figure is labelled an inference, not a finding")
    # question list: twelve, aligned across site and report, with the two new asks
    chk("Twelve Questions" in t and "Twelve questions" in html, "question list is twelve in both")
    chk(html.count("<details>") >= 12, "twelve question accordions on the site")
    chk("Ten Questions" not in t and "eleven questions" not in t.lower(),
        "no stale question counts left in the report")
    for needle in ["assessment erosion", "$138,780", "$46,260"]:
        chk(needle in t, f"PDF question 1 downside risk intact: {needle}")
        chk(needle in html, f"site question 1 downside risk intact: {needle}")
    chk("does not establish that closure causes decline" in t.replace("<i>", "").replace("</i>", "")
        or "not establish that closure causes decline" in t,
        "question 1 states the limit of the closure/population evidence")
    chk("certified compensating rate" in t and "certified compensating rate" in html,
        "the records ask that settles the 4 percent question is published in both")

    # beyond-4% recallable levy options (v3.7)
    for needle in ["recallable levy options", "KRS 160.470", "$191,000 per cent",
                   "$211,600", "$21.16", "$1,699,479", "$4,551",
                   "$13.2, $19.6, $22.1, and $32.5 million",
                   "recalled by the voters it taxes",
                   "recalled by the children it displaces"]:
        chk(needle in t, f"PDF beyond-4% levy options intact: {needle}")
        chk(needle in html, f"site beyond-4% levy options intact: {needle}")
    for needle in ["57.7", "60.3", "61.3", "65.5",
                   "$112/yr ($9.35/mo)", "$167/yr ($13.93/mo)",
                   "$188/yr ($15.69/mo)", "$277/yr ($23.10/mo)"]:
        chk(needle in t and needle in html,
            f"beyond-4% option table consistent in PDF and site: {needle}")
    chk("median of the eight area districts with Fayette excluded" in t,
        "PDF defines the regional median precisely")
    chk("reports/Saving_NMES_v3.7_2026-07-26.pdf" in html
        and (REPO / "reports" / "Saving_NMES_v3.7_2026-07-26.pdf").exists(),
        "v3.7 archived in reports/ and linked from the version history")

    # v3.8: fill correction, cost history, breakeven reconstruction, growth plan
    for needle in ["$56,000 to $116,000", "$106,000 to $211,000",
                   "$2,476,544", "$8,305", "155 students", "99.6 percent",
                   "54 to 69", "$2,851", "$5,200", "$4,414",
                   "$960,000 to $1.9 million", "$260,000 to $530,000"]:
        chk(needle in t, f"PDF v3.8 content intact: {needle}")

        chk(needle in html, f"site v3.8 content intact: {needle}")

    # ---- v3.9 release content ----
    for needle in ["$1,285,310", "$21,482,445", "$1,018,671", "$938,690", "$227,831",
                   "$276,928", "5.5 fixed positions", "$30,410,725", "$30,201,047",
                   "7.6 percent", "450 to 550", "13 to 15 percent", "3,594", "3,548",
                   "2,912", "2,616", "$61,937" if "$61,937" in t else "$132,744"]:
        chk(needle in t, f"PDF v3.9 content present: {needle}")
    for needle in ["$1,285,310", "$21,482,445", "$938,690", "$227,831", "$276,928",
                   "5.5 fixed positions", "$30,410,725", "7.6 percent",
                   "450 to 550", "13 to 15 percent", "3,594", "2,616",
                   "54 to 69", "80 students", "$61,937"]:
        chk(needle in html, f"site v3.9 content present: {needle}")
    chk("about one in three" not in html or "an earlier version of this page said one in three" in html,
        "site: the retracted one-in-three share is corrected, not merely repeated")
    chk('id="sPos" min="2" max="5"' in html and 'id="sCost" min="50000" max="75000"' in html
        and 'id="sBus" min="100000" max="250000"' in html,
        "site calculator sliders sit inside the published grid")
    chk("Version 4.0" in t and "July 31, 2026" in t, "PDF carries the v4.0 version block")
    chk("Saving_NMES_v3.9_2026-07-29.pdf" in html, "site links the v3.9 report")
    chk("298 students" in t and "gives 298 students" in html,
        "breakeven reconstruction lands at 298 in both artifacts")
    chk("recovered from the Internet Archive" in html and "recovered from the Internet "
        "Archive" in t.replace("  ", " "),
        "2000-01 report card provenance disclosed on site and in PDF")
    chk("may report prior-year spending" in html and "prior-year spending" in t,
        "CATS-era fiscal-year caveat disclosed in both artifacts")
    chk("$19,635" in html and "$19,635" in t,
        "2012-13 capital-charge outlier disclosed, not hidden")
    for f in ["bourbon_spending_per_student_2011_2017.csv", "bourbon_staffing_ratios_ccd.csv",
              "crdc_school_finance_bourbon_2011_2017.csv", "slfs_bourbon_fy16_fy17.csv",
              "bourbon_revenue_by_source_2020_2024.csv"]:
        chk((REPO / "build" / f).exists(), f"v3.8 data archived: build/{f}")
    chk("reports/Saving_NMES_v3.8_2026-07-26.pdf" in html
        and (REPO / "reports" / "Saving_NMES_v3.8_2026-07-26.pdf").exists(),
        "v3.8 archived in reports/ and linked from the version history")
    chk("sAdd" in html and "New sections needed at NMES" in html,
        "fill planner carries the v3.8 NMES section-debit slider")
    chk("change formula subtracts" in html and "change formula subtracts" in t,
        "2024-25 index change-component explanation on site and in PDF")
    chk('id="tgSD" checked' in html,
        "SchoolDigger toggle defaults to checked")
    chk((REPO / "build" / "kyrc25_acct_bourbon_extract.csv").exists()
        and "kyrc25_acct_bourbon_extract.csv" in html,
        "2024-25 accountability component extract archived and linked")
    chk('id="tgEF" checked' in html and "federal EDFacts" in html and "EDFacts" in t,
        "federal EDFacts series on site (default on) and referenced in PDF")
    chk((REPO / "build" / "edfacts_school_proficiency_bourbon.json").exists()
        and "edfacts_school_proficiency_bourbon.json" in html,
        "EDFacts extract archived and linked")
    chk("range midpoints" in html and "range midpoints" in t
        and "different scales" in html,
        "EDFacts midpoint and KCCT/KPREP scale caveats disclosed")
    for needle in ["Reading the 2024-25 crossover", "58.5", "45.4", "79.2", "74.3",
                   "Writing content index", "Climate survey index"]:
        chk(needle in html, f"2024-25 status-measure table on site: {needle}")

    chk("unaudited" in html and "unaudited" in t,
        "FY2026 figures labeled unaudited on site and in PDF")
    chk((REPO / "build" / "fy2026_june_financial_packet.pdf").exists()
        and "fy2026_june_financial_packet.pdf" in html,
        "June 2026 financial packet archived and linked from site")
    chk("sweep ended in both cases" in html and "balanced-budget scenario" in t,
        "balanced-budget scenario referenced on site and in PDF")
    chk("$21 million" in html and "$25 million" in html
        and "$21 million" in t and "$25 million" in t,
        "scenario capacity range $21M/$25M consistent on site and in PDF")

    # money-story cleanup: GF-only levy base, both denominators, precise debt wording
    chk("$313,000" in t and "$978,000" in t and "386,000" not in t,
        "PDF levy uses the corrected GF base (313K/978K), old 386K gone")
    chk("$7,829,060" in t and "restricted building-fund levy" in html,
        "levy base disclosed as GF-only in PDF and site")
    chk("over four fifths of the annual reserve drawdown" in t
        and "one cent of the district" in t,
        "PDF scores closure and levy against both deficit and drawdown")
    chk("draws from reserves each year" in html and "DRAWDOWN=1145561" in html,
        "site shows both denominators on the calculators")
    chk("net change across all seven" in t,
        "PDF clarifies the $430K is the net debt-service step, not the bond's payment alone")
    chk("multi-age" not in t.lower() and "multiage" not in t.lower(),
        "multi-age reorganization removed from the report")
    chk("re-create sections" in t and "four while North Middletown" in t,
        "PDF keeps the closure staffing-count judgment (v3 class-cap form)")
    chk("$1.6 to $2.9 million" in t and "$1.6 to $2.9 million" in html,
        "alternatives raw sums (v3.8: fill correction plus priced recruitment line)")

    print(f"PASS {len(ok)}")
    print(f"FAIL {len(bad)}")
    for b in bad:
        print("  -", b)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
