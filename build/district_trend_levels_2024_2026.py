#!/usr/bin/env python3
"""Bourbon County against Kentucky by level, 2023-24 to 2025-26: the district's own rows.

Three years of district-level results at the elementary, middle and high school level,
from KDE's accountability profile and assessment files: the two test indicators (reading
and mathematics status; science, social studies and writing status), the published
overall score and color, Bourbon County's rank among districts on each, and the percent
proficient or distinguished with the content index for every tested subject.

Writes:
  build/district_trend_levels_2024_2026.md
  build/kde_district_trend_levels_2024_2026.csv
  build/district_trend_levels_2024_2026_chart.png

Usage:
  python3 -I build/district_trend_levels_2024_2026.py \
      KYRC24_ACCT_Profile.csv KYRC25_ACCT_Profile.csv Accountable_Profile_2026.CSV \
      KYRC24_ACCT_Kentucky_Summative_Assessment.csv KYRC25_ACCT_Kentucky_Summative_Assessment.csv \
      Accountable_Assessment_Performance_2026.CSV
"""
import csv
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
BOURBON, STATE = "041", "999"
YEARS = ["2023-24", "2024-25", "2025-26"]
LEVELS = [("ES", "Elementary School", "Elementary"),
          ("MS", "Middle School", "Middle"),
          ("HS", "High School", "High")]
SUBJECTS = ["Reading", "Mathematics", "Science", "Social Studies", "Combined Writing"]
COLOR = {1: "red", 2: "orange", 3: "yellow", 4: "green", 5: "blue"}
LEVEL_NAME = {1: "very low", 2: "low", 3: "medium", 4: "high", 5: "very high"}

# profile columns by file family (KYRC = 2023-24 and 2024-25 historical files; ACCT26 = the 2025-26 release)
PROF = {
    "KYRC": {"rm": "READING_MATH STATUS", "rm_rt": "READING_MATH STATUS RATING",
             "ssw": "SCIENCE_SOCIAL STUDIES_COMBINED WRITING STATUS",
             "ssw_rt": "SCIENCE_SOCIAL STUDIES_COMBINED WRITING STATUS RATING",
             "qscs": "QUALITY OF SCHOOL CLIMATE AND SAFETY STATUS",
             "overall": "OVERALL COMBINED INDICATOR RATE", "overall_rt": "OVERALL INDICATOR RATING"},
    "ACCT26": {"rm": "Reading_Mathematics Status", "rm_rt": "Reading_Mathematics Statue Rating",
               "ssw": "Science_Social Studies_Combined Writing Status",
               "ssw_rt": "Science_Social Studies_Combined Writing Statue Rating",
               "qscs": "Quality Of School Climate and Safety Status",
               "overall": "Overall Combined Indicator Rate", "overall_rt": "Overall Indicator Rating"},
}


def num(s):
    s = (s or "").strip()
    if s in ("", "*", "N/A"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def ordinal(n):
    if 10 <= n % 100 <= 20:
        suf = "th"
    else:
        suf = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suf}"


def district_rows_profile(path, family):
    """-> {(district_number, level_code): row}"""
    out = {}
    with open(path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if family == "KYRC":
                if r["School Type"].strip() == "" and r["School Name"].strip() == "All Schools":
                    code = {"Elementary School": "ES", "Middle School": "MS", "High School": "HS"}.get(r["Level"].strip())
                    if code:
                        out[(r["District Number"].strip(), code)] = r
            else:
                if r["School Name"].strip() == "":
                    out[(r["School Code"].strip(), r["Level"].strip())] = r
    return out


def district_rows_assessment(path, family):
    """-> {(district_number, level_code, subject): (pd, index)} for all students"""
    out = {}
    with open(path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if r.get("Demographic", "").strip() != "All Students":
                continue
            if family == "KYRC":
                if not (r["School Type"].strip() == "" and r["School Name"].strip() == "All Schools"):
                    continue
                dn = r["District Number"].strip()
                code = {"Elementary School": "ES", "Middle School": "MS", "High School": "HS"}.get(r["Level"].strip())
                pd_ = num(r.get("Proficient / Distinguished"))
            else:
                if r["School Name"].strip() != "":
                    continue
                dn = r["School Code"].strip()
                code = r["Level"].strip()
                pd_ = num(r.get("Proficient/Distinguished"))
            if code and r["Subject"].strip() in SUBJECTS:
                out[(dn, code, r["Subject"].strip())] = (pd_, num(r.get("Content Index")), r.get("Suppressed", "").strip())
    return out


def is_district(dn):
    try:
        return int(dn) < 900
    except ValueError:
        return False


def rank_of(rows, key, dn, lv):
    """rank from the top among districts at level lv on profile column key; -> (rank, n)"""
    vals = []
    mine = None
    for (d, l), r in rows.items():
        if l != lv or not is_district(d):
            continue
        v = num(r.get(key))
        if v is None:
            continue
        vals.append(v)
        if d == dn:
            mine = v
    if mine is None:
        return None, len(vals)
    vals.sort(reverse=True)
    return vals.index(mine) + 1, len(vals)


def main(p24, p25, p26, a24, a25, a26):
    prof = {"2023-24": (district_rows_profile(p24, "KYRC"), PROF["KYRC"]),
            "2024-25": (district_rows_profile(p25, "KYRC"), PROF["KYRC"]),
            "2025-26": (district_rows_profile(p26, "ACCT26"), PROF["ACCT26"])}
    asmt = {"2023-24": district_rows_assessment(a24, "KYRC"),
            "2024-25": district_rows_assessment(a25, "KYRC"),
            "2025-26": district_rows_assessment(a26, "ACCT26")}

    # ---------- gather ----------
    data = {}   # (year, level, who, measure) -> value
    recs = []
    for year in YEARS:
        rows, cols = prof[year]
        for code, lname, short in LEVELS:
            for who, dn in (("Bourbon County", BOURBON), ("Kentucky", STATE)):
                r = rows.get((dn, code))
                if r is None:
                    continue
                for key in ("rm", "ssw", "qscs", "overall"):
                    v = num(r.get(cols[key]))
                    data[(year, code, who, key)] = v
                    rt = num(r.get(cols.get(key + "_rt", "")))
                    if rt is not None:
                        lab = COLOR.get(int(rt)) if key == "overall" else LEVEL_NAME.get(int(rt))
                        data[(year, code, who, key + "_rating")] = lab
                    rank, n = (rank_of(rows, cols[key], dn, code) if dn == BOURBON else (None, None))
                    recs.append({"year": year, "level": code, "district": who, "measure": key, "value": v,
                                 "rating": data.get((year, code, who, key + "_rating"), ""),
                                 "rank_from_top": rank or "", "districts": n or ""})
                    if dn == BOURBON:
                        data[(year, code, who, key + "_rank")] = (rank, n)
                for subj in SUBJECTS:
                    t = asmt[year].get((dn, code, subj))
                    if t is None:
                        continue
                    data[(year, code, who, "pd:" + subj)] = t[0]
                    data[(year, code, who, "ci:" + subj)] = t[1]
                    data[(year, code, who, "sup:" + subj)] = t[2]
                    recs.append({"year": year, "level": code, "district": who, "measure": "pd:" + subj,
                                 "value": t[0], "rating": "", "rank_from_top": "", "districts": ""})
                    recs.append({"year": year, "level": code, "district": who, "measure": "ci:" + subj,
                                 "value": t[1], "rating": "", "rank_from_top": "", "districts": ""})

    out_csv = os.path.join(HERE, "kde_district_trend_levels_2024_2026.csv")
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(recs[0].keys()))
        w.writeheader()
        w.writerows(recs)

    # ---------- markdown ----------
    def fmt(v, nd=1):
        return "n/a" if v is None else (f"{v:.{nd}f}" if isinstance(v, float) else str(v))

    def cell_rank(year, code):
        rk = data.get((year, code, "Bourbon County", "rm_rank"))
        return f"{rk[0]} of {rk[1]}" if rk and rk[0] else "n/a"

    L = ["# Bourbon County by level, 2023-24 to 2025-26, against Kentucky\n",
         "District rows from KDE's accountability profile and assessment files for 2023-24 (KYRC24), 2024-25 "
         "(KYRC25) and 2025-26 (the October 14, 2026 release), all students. Status is the year's own result on "
         "the indicator; the overall score adds the state's change component. Ranks are among Kentucky districts "
         "with a result at that level, 1 = highest. Percent proficient or distinguished and the content index "
         "(novice 0, apprentice 50, proficient 100, distinguished 125) are for every tested subject; asterisks "
         "mark a suppressed percentage, for which the index is still published.\n"]
    for code, lname, short in LEVELS:
        L.append(f"## {short} school level\n")
        L.append("| Measure | Bourbon 2023-24 | 2024-25 | 2025-26 | Kentucky 2023-24 | 2024-25 | 2025-26 |")
        L.append("|---|---|---|---|---|---|---|")
        for key, label in (("rm", "Reading and mathematics status (state level)"),
                           ("ssw", "Science, social studies and writing status (state level)"),
                           ("qscs", "Climate and safety survey status"),
                           ("overall", "Overall score (color)")):
            cells = []
            for who in ("Bourbon County", "Kentucky"):
                for year in YEARS:
                    v = data.get((year, code, who, key))
                    rt = data.get((year, code, who, key + "_rating"))
                    cells.append(fmt(v) + (f" ({rt})" if rt and key != "qscs" else ""))
            L.append(f"| {label} | " + " | ".join(cells) + " |")
        for key, label in (("rm", "Bourbon rank, reading and mathematics status"),
                           ("ssw", "Bourbon rank, science, social studies and writing status"),
                           ("overall", "Bourbon rank, overall score")):
            cells = []
            for year in YEARS:
                rk = data.get((year, code, "Bourbon County", key + "_rank"))
                cells.append(f"{rk[0]} of {rk[1]}" if rk and rk[0] else "n/a")
            L.append(f"| {label} | " + " | ".join(cells) + " | | | |")
        for subj in SUBJECTS:
            cells = []
            for who in ("Bourbon County", "Kentucky"):
                for year in YEARS:
                    pd_ = data.get((year, code, who, "pd:" + subj))
                    ci = data.get((year, code, who, "ci:" + subj))
                    sup = data.get((year, code, who, "sup:" + subj))
                    pd_s = "*" if (pd_ is None or sup == "Y") else f"{pd_:.0f}"
                    cells.append(f"{pd_s} ({fmt(ci)})")
            L.append(f"| {subj}: percent proficient or distinguished (index) | " + " | ".join(cells) + " |")
        L.append("")
    out_md = os.path.join(HERE, "district_trend_levels_2024_2026.md")
    open(out_md, "w", encoding="utf-8").write("\n".join(L))

    # ---------- chart ----------
    NAVY, GRAY, INK, MUTED, LINE = "#1F3864", "#8A93A6", "#1C2230", "#6B7486", "#E3E8F0"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5})
    cols = [("rm", "Reading and mathematics status"), ("ssw", "Science, social studies and writing status")]
    fig, axes = plt.subplots(3, 2, figsize=(11.5, 9.2), sharex=True)
    xs = [0, 1, 2]
    for j, (key, ctitle) in enumerate(cols):
        allv = [data.get((y, c, w, key)) for y in YEARS for c, _, _ in LEVELS for w in ("Bourbon County", "Kentucky")]
        allv = [v for v in allv if v is not None]
        lo, hi = min(allv) - 6, max(allv) + 6
        for i, (code, lname, short) in enumerate(LEVELS):
            ax = axes[i][j]
            for who, color, ls, mk, z in (("Kentucky", GRAY, (0, (4, 3)), "s", 2), ("Bourbon County", NAVY, "-", "o", 3)):
                ys = [data.get((y, code, who, key)) for y in YEARS]
                ax.plot(xs, ys, color=color, lw=2.2, ls=ls, marker=mk, ms=7, markeredgecolor="white",
                        markeredgewidth=1.2, zorder=z, label=who)
                for x, v in zip(xs, ys):
                    if v is None:
                        continue
                    # labels go on the outside: the higher series above its point, the lower one below
                    other = data.get((YEARS[x], code, "Kentucky" if who == "Bourbon County" else "Bourbon County", key))
                    dy = 1.9 if (other is None or v >= other) else -1.9
                    ax.text(x, v + dy, f"{v:.1f}", color=color if who == "Bourbon County" else MUTED, fontsize=8.6,
                            ha="center", va="bottom" if dy > 0 else "top",
                            fontweight="bold" if who == "Bourbon County" else "normal", zorder=5)
                if who == "Bourbon County":
                    rk = data.get((YEARS[-1], code, "Bourbon County", key + "_rank"))
                    if rk and rk[0]:
                        ax.text(2.12, ys[-1], f"{ordinal(rk[0])}\nof {rk[1]}\ndistricts", color=NAVY, fontsize=7.8,
                                ha="left", va="center", zorder=5)
            ax.set_ylim(lo, hi)
            ax.set_xlim(-0.35, 2.55)
            ax.set_xticks(xs)
            ax.set_xticklabels(YEARS)
            for sp in ("top", "right"):
                ax.spines[sp].set_visible(False)
            for sp in ("left", "bottom"):
                ax.spines[sp].set_color(LINE)
            ax.tick_params(colors=MUTED, labelsize=8.8, length=0)
            ax.yaxis.grid(True, color=LINE, lw=0.8)
            ax.set_axisbelow(True)
            if j == 0:
                ax.set_ylabel(f"{short} level", color=INK, fontsize=10.5, labelpad=10)
            if i == 0:
                ax.set_title(ctitle, color=INK, fontsize=11, loc="left", pad=8)
    handles, labels = axes[0][0].get_legend_handles_labels()
    order = [labels.index("Bourbon County"), labels.index("Kentucky")]
    fig.legend([handles[k] for k in order], [labels[k] for k in order], loc="upper right",
               bbox_to_anchor=(0.985, 0.975), ncol=2, frameon=False, fontsize=9.5)
    fig.suptitle("Bourbon County against Kentucky, 2023-24 to 2025-26: the state's two test indicators by level",
                 x=0.045, ha="left", fontsize=12.5, color=INK, fontweight="bold", y=0.985)
    fig.text(0.045, 0.012,
             "Source: KDE accountability profiles, district rows (KYRC24 and KYRC25 School Report Card files; "
             "Accountable_Profile_2026.CSV, October 14, 2026). Status is the year's own result on the indicator, all "
             "students; the Kentucky line is the statewide level result. Rank is among Kentucky districts, 1 = highest.",
             fontsize=7.8, color=MUTED, ha="left", va="bottom", wrap=True)
    fig.subplots_adjust(left=0.075, right=0.985, top=0.905, bottom=0.085, hspace=0.3, wspace=0.16)
    out_png = os.path.join(HERE, "district_trend_levels_2024_2026_chart.png")
    fig.savefig(out_png, dpi=200)
    print("wrote", out_csv, out_md, out_png)


if __name__ == "__main__":
    if len(sys.argv) != 7:
        sys.exit(__doc__)
    main(*sys.argv[1:])
