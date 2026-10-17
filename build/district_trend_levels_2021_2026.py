#!/usr/bin/env python3
"""Bourbon County against Kentucky by level, every year of the current accountability system.

Kentucky's current system started in 2021-22, so the overall score exists for five years:
2021-22 (status only, no change component yet), 2022-23, 2023-24, 2024-25 and 2025-26.
Nothing comparable exists for 2016-17 through 2020-21: the state issued no overall score
in 2016-17, 2017-18, 2019-20 or 2020-21, and only a star rating in 2018-19. The earlier
Unbridled Learning scores (2011-12 to 2015-16) are a different scale and are not online.

This script reads the district rows of KDE's accountability profile files for the five
years and the assessment files for six (2020-21 has test results but no accountability),
and writes:
  build/district_trend_levels_2021_2026.md
  build/kde_district_trend_levels_2021_2026.csv
  build/district_trend_levels_2021_2026_overall_chart.png   overall score, five years, by level
  build/district_trend_levels_2021_2026_overall_percentile_chart.png   the same years as a percentile among districts
  build/district_trend_levels_2021_2026_pd_chart.png        reading and math percent proficient, six years

Usage (all paths are KDE files, downloaded with a browser user agent):
  python3 -I build/district_trend_levels_2021_2026.py \
      --p22 accountability_profile_2022.csv --p23 accountability_profile_2023.csv \
      --p24 KYRC24_ACCT_Profile.csv --p25 KYRC25_ACCT_Profile.csv --p26 Accountable_Profile_2026.CSV \
      --a21 asmt_performance_by_grade_2021.csv \
      --a22 accountable_assessment_performance_2022.csv --a23 accountable_assessment_performance_2023.csv \
      --a24 KYRC24_ACCT_Kentucky_Summative_Assessment.csv --a25 KYRC25_ACCT_Kentucky_Summative_Assessment.csv \
      --a26 Accountable_Assessment_Performance_2026.CSV
"""
import argparse
import csv
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
BOURBON, STATE = "041", "999"
YEARS = ["2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]
PD_YEARS = ["2020-21"] + YEARS
LEVELS = [("ES", "Elementary"), ("MS", "Middle"), ("HS", "High")]
COLOR = {1: "red", 2: "orange", 3: "yellow", 4: "green", 5: "blue"}
LEVEL_NAME = {1: "very low", 2: "low", 3: "medium", 4: "high", 5: "very high"}
LEVEL_CODE = {"Elementary School": "ES", "Middle School": "MS", "High School": "HS", "ES": "ES", "MS": "MS", "HS": "HS"}
SUBJ_CODE = {"RD": "Reading", "MA": "Mathematics", "SC": "Science", "SS": "Social Studies", "WR": "Combined Writing",
             "Reading": "Reading", "Mathematics": "Mathematics", "Science": "Science",
             "Social Studies": "Social Studies", "Combined Writing": "Combined Writing"}

# profile column names by file family
FAM = {
    "2022": {"overall": "OVERALL INDICATOR RATE", "overall_rt": "OVERALL INDICATOR RATING",
             "rm": "READING_MATH INDICATOR RATE", "rm_rt": "READING_MATH INDICATOR RATING",
             "ssw": "SCIENCE_SOCIAL STUDIES_COMBINED WRITING INDICATOR RATE"},
    "2023": {"overall": "OVERALL COMBINED INDICATOR RATE", "overall_rt": "OVERALL INDICATOR RATING",
             "rm": "READING_MATH STATUS", "rm_rt": "READING_MATH STATUS RATING",
             "ssw": "SCIENCE_SOCIAL STUDIES_COMBINED WRITING STATUS"},
    "2026": {"overall": "OVERALL COMBINED INDICATOR RATE", "overall_rt": "OVERALL INDICATOR RATING",
             "rm": "READING_MATHEMATICS STATUS", "rm_rt": "READING_MATHEMATICS STATUE RATING",
             "ssw": "SCIENCE_SOCIAL STUDIES_COMBINED WRITING STATUS"},
}


def up(row):
    """Upper-case the column names: KDE's files change case from year to year."""
    return {k.strip().upper(): v for k, v in row.items() if k is not None}


def num(s):
    s = (s or "").strip()
    if s in ("", "*", "N/A", "."):
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


def is_district(dn):
    try:
        return int(dn) < 900
    except ValueError:
        return False


def read_profile(path, fam):
    """-> {(district_number, level): row} for district and state totals."""
    out = {}
    with open(path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            r = up(r)
            if fam == "2026":
                if r["SCHOOL NAME"].strip() != "":
                    continue
                dn, lv = r["SCHOOL CODE"].strip(), r["LEVEL"].strip()
            else:
                sn = r["SCHOOL NAME"].strip()
                if sn not in ("---District Total---", "---State Total---", "All Schools"):
                    continue
                if sn == "All Schools" and r.get("SCHOOL TYPE", "").strip() != "":
                    continue
                dn, lv = r["DISTRICT NUMBER"].strip(), LEVEL_CODE.get(r["LEVEL"].strip())
            if lv:
                out[(dn, lv)] = r
    return out


def read_assessment(path, fam):
    """-> {(district_number, level, subject): (pd, index)} for all students, district and state totals."""
    out = {}
    with open(path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            r = up(r)
            if (r.get("DEMOGRAPHIC") or "").strip() != "All Students":
                continue
            if fam == "2026":
                if r["SCHOOL NAME"].strip() != "":
                    continue
                dn, lv, subj = r["SCHOOL CODE"].strip(), r["LEVEL"].strip(), r["SUBJECT"].strip()
                pd_, ci = num(r.get("PROFICIENT/DISTINGUISHED")), num(r.get("CONTENT INDEX"))
            else:
                sn = r["SCHOOL NAME"].strip()
                if sn not in ("---District Total---", "---State Total---", "All Schools"):
                    continue
                if sn == "All Schools" and r.get("SCHOOL TYPE", "").strip() != "":
                    continue
                dn, lv, subj = r["DISTRICT NUMBER"].strip(), LEVEL_CODE.get(r["LEVEL"].strip()), r["SUBJECT"].strip()
                pd_ = num(r.get("PROFICIENT/DISTINGUISHED") or r.get("PROFICIENT / DISTINGUISHED"))
                ci = num(r.get("CONTENT INDEX"))
            subj = SUBJ_CODE.get(subj)
            if lv and subj:
                out[(dn, lv, subj)] = (pd_, ci)
    return out


def read_by_grade_2021(path):
    """2020-21 has only grade rows: weight each grade's percent by its tested population."""
    acc = {}
    with open(path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if r["DEMOGRAPHIC"].strip() != "All Students":
                continue
            if r["SCHOOL NAME"].strip() not in ("---District Total---", "---State Total---"):
                continue
            dn, lv, subj = r["DISTRICT NUMBER"].strip(), r["LEVEL"].strip(), SUBJ_CODE.get(r["SUBJECT"].strip())
            pd_, n = num(r.get("PROFICIENT/DISTINGUISHED")), num(r.get("NAPD POPULATION"))
            if not subj or pd_ is None or not n:
                continue
            a = acc.setdefault((dn, lv, subj), [0.0, 0.0])
            a[0] += pd_ * n
            a[1] += n
    return {k: (round(v[0] / v[1], 1), None) for k, v in acc.items() if v[1]}


def rank_of(rows, col, dn, lv):
    vals, mine = [], None
    for (d, l), r in rows.items():
        if l != lv or not is_district(d):
            continue
        v = num(r.get(col))
        if v is None:
            continue
        vals.append(v)
        if d == dn:
            mine = v
    if mine is None:
        return None, len(vals), None
    n = len(vals)
    below = sum(1 for x in vals if x < mine)
    equal = sum(1 for x in vals if x == mine)
    pct = 100.0 * (below + 0.5 * equal) / n
    vals.sort(reverse=True)
    return vals.index(mine) + 1, n, pct


def main(a):
    prof = {"2021-22": (read_profile(a.p22, "2022"), FAM["2022"]),
            "2022-23": (read_profile(a.p23, "2023"), FAM["2023"]),
            "2023-24": (read_profile(a.p24, "2023"), FAM["2023"]),
            "2024-25": (read_profile(a.p25, "2023"), FAM["2023"]),
            "2025-26": (read_profile(a.p26, "2026"), FAM["2026"])}
    asmt = {"2020-21": read_by_grade_2021(a.a21),
            "2021-22": read_assessment(a.a22, "2022"),
            "2022-23": read_assessment(a.a23, "2023"),
            "2023-24": read_assessment(a.a24, "2023"),
            "2024-25": read_assessment(a.a25, "2023"),
            "2025-26": read_assessment(a.a26, "2026")}

    data, recs = {}, []
    for year in YEARS:
        rows, cols = prof[year]
        for lv, short in LEVELS:
            for who, dn in (("Bourbon County", BOURBON), ("Kentucky", STATE)):
                r = rows.get((dn, lv))
                if r is None:
                    continue
                for key in ("overall", "rm", "ssw"):
                    v = num(r.get(cols[key]))
                    data[(year, lv, who, key)] = v
                    rt = num(r.get(cols.get(key + "_rt", "")))
                    lab = ""
                    if rt is not None:
                        lab = COLOR.get(int(rt), "") if key == "overall" else LEVEL_NAME.get(int(rt), "")
                        data[(year, lv, who, key + "_rating")] = lab
                    rank, n, pct = (rank_of(rows, cols[key], dn, lv) if dn == BOURBON else (None, None, None))
                    if dn == BOURBON:
                        data[(year, lv, who, key + "_rank")] = (rank, n, pct)
                    recs.append({"year": year, "level": lv, "district": who, "measure": key, "value": v,
                                 "rating": lab, "rank_from_top": rank or "", "districts": n or "",
                                 "percentile": round(pct, 1) if pct is not None else ""})
    for year in PD_YEARS:
        for lv, short in LEVELS:
            for who, dn in (("Bourbon County", BOURBON), ("Kentucky", STATE)):
                for subj in ("Reading", "Mathematics"):
                    t = asmt[year].get((dn, lv, subj))
                    if t is None:
                        continue
                    data[(year, lv, who, "pd:" + subj)] = t[0]
                    recs.append({"year": year, "level": lv, "district": who, "measure": "pd:" + subj,
                                 "value": t[0], "rating": "", "rank_from_top": "", "districts": "", "percentile": ""})

    out_csv = os.path.join(HERE, "kde_district_trend_levels_2021_2026.csv")
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(recs[0].keys()))
        w.writeheader()
        w.writerows(recs)

    # ---------- markdown ----------
    def fmt(v):
        return "n/a" if v is None else f"{v:.1f}"

    L = ["# Bourbon County by level, every year of the current accountability system\n",
         "Kentucky's current accountability system began in 2021-22, so the overall score exists for five "
         "years. The state issued no overall score in 2016-17, 2017-18, 2019-20 or 2020-21, and only a star "
         "rating in 2018-19; the Unbridled Learning scores of 2011-12 to 2015-16 are on a different scale and "
         "KDE no longer posts those files. District rows, all students, from KDE's accountability profile "
         "files (accountability_profile_2022 and 2023, KYRC24 and KYRC25, Accountable_Profile_2026). In "
         "2021-22 the system scored status only, so that year's overall score has no change component. "
         "Ranks are among Kentucky districts with a result at that level, 1 = highest. The last table adds "
         "2020-21, a year with test results but no accountability; its level figures are the grade results "
         "weighted by tested students.\n"]
    for lv, short in LEVELS:
        L.append(f"## {short} school level\n")
        L.append("| Measure | " + " | ".join(YEARS) + " |")
        L.append("|---|" + "---|" * len(YEARS))
        for who in ("Bourbon County", "Kentucky"):
            cells = []
            for y in YEARS:
                v = data.get((y, lv, who, "overall"))
                rt = data.get((y, lv, who, "overall_rating"), "")
                cells.append(fmt(v) + (f" ({rt})" if rt else ""))
            L.append(f"| Overall score, {who} | " + " | ".join(cells) + " |")
        cells = []
        for y in YEARS:
            rk = data.get((y, lv, "Bourbon County", "overall_rank"))
            cells.append(f"{rk[0]} of {rk[1]} ({ordinal(int(round(rk[2])))} pct)" if rk and rk[0] else "n/a")
        L.append("| Bourbon rank and percentile, overall score | " + " | ".join(cells) + " |")
        for who in ("Bourbon County", "Kentucky"):
            cells = []
            for y in YEARS:
                v = data.get((y, lv, who, "rm"))
                rt = data.get((y, lv, who, "rm_rating"), "")
                cells.append(fmt(v) + (f" ({rt})" if rt else ""))
            L.append(f"| Reading and mathematics status, {who} | " + " | ".join(cells) + " |")
        cells = []
        for y in YEARS:
            rk = data.get((y, lv, "Bourbon County", "rm_rank"))
            cells.append(f"{rk[0]} of {rk[1]} ({ordinal(int(round(rk[2])))} pct)" if rk and rk[0] else "n/a")
        L.append("| Bourbon rank and percentile, reading and mathematics status | " + " | ".join(cells) + " |")
        for who in ("Bourbon County", "Kentucky"):
            cells = [fmt(data.get((y, lv, who, "ssw"))) for y in YEARS]
            L.append(f"| Science, social studies and writing status, {who} | " + " | ".join(cells) + " |")
        L.append("")
        L.append("| Percent proficient or distinguished | " + " | ".join(PD_YEARS) + " |")
        L.append("|---|" + "---|" * len(PD_YEARS))
        for subj in ("Reading", "Mathematics"):
            for who in ("Bourbon County", "Kentucky"):
                cells = []
                for y in PD_YEARS:
                    v = data.get((y, lv, who, "pd:" + subj))
                    cells.append("n/a" if v is None else f"{v:.0f}")
                L.append(f"| {subj}, {who} | " + " | ".join(cells) + " |")
        L.append("")
    out_md = os.path.join(HERE, "district_trend_levels_2021_2026.md")
    open(out_md, "w", encoding="utf-8").write("\n".join(L))

    # ---------- charts ----------
    NAVY, GRAY, INK, MUTED, LINE = "#1F3864", "#8A93A6", "#1C2230", "#6B7486", "#E3E8F0"
    FILL = {"red": "#C0392B", "orange": "#E67E22", "yellow": "#F1C40F", "green": "#27AE60", "blue": "#2E75B6"}
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5})
    box = dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85)

    def draw_panel(ax, years, series, key, lv, value_fmt, show_rating, rank_key, ylim=None):
        xs = list(range(len(years)))
        if ylim:
            ax.set_ylim(*ylim)
        for who, color, ls, mk, z in (("Kentucky", GRAY, (0, (4, 3)), "s", 2), ("Bourbon County", NAVY, "-", "o", 3)):
            ys = [data.get((y, lv, who, key)) for y in years]
            ax.plot(xs, ys, color=color, lw=2.0, ls=ls, zorder=z, label=who)
            for x, v in zip(xs, ys):
                if v is None:
                    continue
                rating = data.get((years[x], lv, who, key + "_rating"), "") if show_rating else ""
                fill = FILL.get(rating, color) if show_rating else color
                ax.scatter([x], [v], s=70 if who == "Bourbon County" else 46, marker=mk, color=fill,
                           edgecolor=color, linewidth=1.5, zorder=z + 2)
                other = data.get((years[x], lv, "Kentucky" if who == "Bourbon County" else "Bourbon County", key))
                label = value_fmt(v) + (f" {rating}" if (show_rating and who == "Bourbon County" and rating) else "")
                style = dict(color=NAVY if who == "Bourbon County" else MUTED, fontsize=8.2,
                             fontweight="bold" if who == "Bourbon County" else "normal", zorder=6, bbox=box)
                nbrs = [ys[k] for k in (x - 1, x + 1) if 0 <= k < len(ys) and ys[k] is not None]
                peak_under = (who == "Bourbon County" and len(nbrs) == 2 and all(v > n for n in nbrs)
                              and other is not None and other > v)
                if peak_under:
                    ax.text(x + 0.08, v + 0.4, label, ha="left", va="bottom", **style)
                else:
                    dy = 2.0 if (other is None or v >= other) else -2.0
                    # keep the first point's label inside the axes
                    xt, ha = (x - 0.28, "left") if x == 0 else (x, "center")
                    ax.text(xt, v + dy, label, ha=ha, va="bottom" if dy > 0 else "top", **style)
            if who == "Bourbon County" and rank_key and ylim:
                ybot = ylim[0] + (ylim[1] - ylim[0]) * 0.02
                for x, y in enumerate(years):
                    rk = data.get((y, lv, "Bourbon County", rank_key))
                    if rk and rk[0]:
                        ax.text(x, ybot, f"{ordinal(rk[0])}/{rk[1]}\n{ordinal(int(round(rk[2])))} pct", ha="center",
                                va="bottom", color=MUTED, fontsize=7.3, linespacing=1.3, zorder=6)
                import math as _m
                ax.set_yticks(list(range(int(_m.ceil((ylim[0] + 9) / 10.0)) * 10, int(ylim[1]) + 1, 10)))
        ax.set_xlim(-0.45, len(years) - 1 + 0.78)
        ax.set_xticks(xs)
        ax.set_xticklabels(years, fontsize=8.4)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        for sp in ("left", "bottom"):
            ax.spines[sp].set_color(LINE)
        ax.tick_params(colors=MUTED, labelsize=8.6, length=0)
        ax.yaxis.grid(True, color=LINE, lw=0.8)
        ax.set_axisbelow(True)

    # chart 1: overall score, five years
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 5.0), sharey=True)
    allv = [data.get((y, lv, w, "overall")) for y in YEARS for lv, _ in LEVELS for w in ("Bourbon County", "Kentucky")]
    allv = [v for v in allv if v is not None]
    for i, (lv, short) in enumerate(LEVELS):
        ax = axes[i]
        draw_panel(ax, YEARS, None, "overall", lv, lambda v: f"{v:.1f}", True, "overall_rank",
                   ylim=(min(allv) - 12, max(allv) + 7))
        ax.set_title(f"{short} school level", color=INK, fontsize=11, loc="left", pad=8)
        if i == 0:
            ax.set_ylabel("Overall score", color=INK, fontsize=10, labelpad=8)
    h, lab = axes[0].get_legend_handles_labels()
    order = [lab.index("Bourbon County"), lab.index("Kentucky")]
    fig.legend([h[k] for k in order], [lab[k] for k in order], loc="upper right", bbox_to_anchor=(0.985, 0.925),
               ncol=2, frameon=False, fontsize=9.5)
    fig.suptitle("Bourbon County against Kentucky, every year of the current accountability system: overall index by level",
                 x=0.04, ha="left", fontsize=12.2, color=INK, fontweight="bold", y=0.985)
    fig.text(0.04, 0.015,
             "Source: KDE accountability profiles, district rows, all students (accountability_profile_2022 and 2023; KYRC24 and "
             "KYRC25 School Report Card files; Accountable_Profile_2026, October 14, 2026). The overall score is the state's published "
             "figure; 2021-22 was scored on status alone, later years add the change component. Marker fill is the state's color. "
             "The gray row under each panel is Bourbon's rank among Kentucky districts that year (rank/districts) and its percentile, "
             "the share of districts at or below it. No overall score was issued from 2016-17 through 2020-21 (star ratings only in 2018-19).",
             fontsize=7.4, color=MUTED, ha="left", va="bottom", wrap=True)
    fig.subplots_adjust(left=0.06, right=0.985, top=0.80, bottom=0.19, wspace=0.14)
    out_png = os.path.join(HERE, "district_trend_levels_2021_2026_overall_chart.png")
    fig.savefig(out_png, dpi=200)

    # chart 1b: the same five years as a percentile among Kentucky districts
    def percentile_panel(ax, years, rank_tuples, ratings, title, first_label=True):
        """rank_tuples: list of (rank, n, pct) per year; ratings: color word per year or None."""
        xs = list(range(len(years)))
        ax.axhspan(0, 25, color="#F3F5F8", zorder=0)
        ax.axhline(50, color=GRAY, lw=1.2, ls=(0, (4, 3)), zorder=1)
        ys = [rk[2] if rk and rk[0] else None for rk in rank_tuples]
        ax.plot(xs, ys, color=NAVY, lw=2.2, zorder=3)
        for x, (rk, rating) in enumerate(zip(rank_tuples, ratings)):
            if not rk or not rk[0]:
                continue
            fill = FILL.get(rating or "", NAVY)
            ax.scatter([x], [rk[2]], s=80, color=fill, edgecolor=NAVY, linewidth=1.6, zorder=4)
            ax.text(x, rk[2] + 3.2, f"{ordinal(int(round(rk[2])))} pct", ha="center", va="bottom", color=NAVY,
                    fontsize=8.6, fontweight="bold", zorder=6, bbox=box)
            # the rank goes under the point unless the point is too low for it to clear the axis
            ry, rva = (rk[2] - 3.2, "top") if rk[2] >= 14 else (rk[2] + 11.0, "bottom")
            ax.text(x, ry, f"{ordinal(rk[0])} of {rk[1]}", ha="center", va=rva, color=MUTED,
                    fontsize=7.6, zorder=6, bbox=box)
        ax.text(len(years) - 1 + 0.62, 50, "median\ndistrict", color=MUTED, fontsize=7.4, ha="left", va="center")
        ax.text(len(years) - 1 + 0.62, 12.5, "bottom\nquarter", color=MUTED, fontsize=7.4, ha="left", va="center")
        ax.set_ylim(0, 100)
        ax.set_yticks([0, 25, 50, 75, 100])
        ax.set_xlim(-0.45, len(years) - 1 + 1.2)
        ax.set_xticks(xs)
        ax.set_xticklabels(years, fontsize=8.4)
        ax.set_title(title, color=INK, fontsize=11, loc="left", pad=8)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        for sp in ("left", "bottom"):
            ax.spines[sp].set_color(LINE)
        ax.tick_params(colors=MUTED, labelsize=8.6, length=0)
        ax.yaxis.grid(True, color=LINE, lw=0.8)
        ax.set_axisbelow(True)

    fig3, axes3 = plt.subplots(1, 3, figsize=(12.5, 5.0), sharey=True)
    for i, (lv, short) in enumerate(LEVELS):
        percentile_panel(axes3[i], YEARS,
                         [data.get((y, lv, "Bourbon County", "overall_rank")) for y in YEARS],
                         [data.get((y, lv, "Bourbon County", "overall_rating")) for y in YEARS],
                         f"{short} school level")
    axes3[0].set_ylabel("Percentile among Kentucky districts", color=INK, fontsize=10, labelpad=8)
    fig3.suptitle("Where Bourbon County's overall index ranks among Kentucky districts, by level, 2021-22 to 2025-26",
                  x=0.04, ha="left", fontsize=12.2, color=INK, fontweight="bold", y=0.985)
    fig3.text(0.04, 0.015,
              "Source: KDE accountability profiles, district rows, all students (accountability_profile_2022 and 2023; KYRC24 and KYRC25; "
              "Accountable_Profile_2026, October 14, 2026). Percentile is the share of Kentucky districts scoring at or below Bourbon County "
              "on the overall score that year; the label under each point is the rank, 1 = highest. Marker fill is the state's color for "
              "Bourbon's score that year.",
              fontsize=7.4, color=MUTED, ha="left", va="bottom", wrap=True)
    fig3.subplots_adjust(left=0.06, right=0.985, top=0.86, bottom=0.19, wspace=0.14)
    out_png3 = os.path.join(HERE, "district_trend_levels_2021_2026_overall_percentile_chart.png")
    fig3.savefig(out_png3, dpi=200)

    # chart 2: percent proficient or distinguished, reading and math, six years
    fig2, axes2 = plt.subplots(3, 2, figsize=(12.5, 9.4), sharex=True)
    for j, subj in enumerate(("Reading", "Mathematics")):
        allv = [data.get((y, lv, w, "pd:" + subj)) for y in PD_YEARS for lv, _ in LEVELS for w in ("Bourbon County", "Kentucky")]
        allv = [v for v in allv if v is not None]
        for i, (lv, short) in enumerate(LEVELS):
            ax = axes2[i][j]
            draw_panel(ax, PD_YEARS, None, "pd:" + subj, lv, lambda v: f"{v:.0f}", False, None)
            ax.set_ylim(min(allv) - 6, max(allv) + 6)
            if i == 0:
                ax.set_title(f"{subj}: percent proficient or distinguished", color=INK, fontsize=11, loc="left", pad=8)
            if j == 0:
                ax.set_ylabel(f"{short} level", color=INK, fontsize=10.5, labelpad=10)
    h, lab = axes2[0][0].get_legend_handles_labels()
    order = [lab.index("Bourbon County"), lab.index("Kentucky")]
    fig2.legend([h[k] for k in order], [lab[k] for k in order], loc="upper right", bbox_to_anchor=(0.985, 0.955),
                ncol=2, frameon=False, fontsize=9.5)
    fig2.suptitle("Bourbon County against Kentucky, 2020-21 to 2025-26: Kentucky Summative Assessment results by level",
                  x=0.04, ha="left", fontsize=12.2, color=INK, fontweight="bold", y=0.985)
    fig2.text(0.04, 0.012,
              "Source: KDE assessment files, district rows, all students. 2020-21 was a limited COVID-year administration with no "
              "accountability; its level figures are the grade results weighted by tested students. The Kentucky Summative Assessment "
              "replaced K-PREP in 2020-21, so earlier years are not on this scale.",
              fontsize=7.4, color=MUTED, ha="left", va="bottom", wrap=True)
    fig2.subplots_adjust(left=0.065, right=0.985, top=0.905, bottom=0.075, hspace=0.28, wspace=0.14)
    out_png2 = os.path.join(HERE, "district_trend_levels_2021_2026_pd_chart.png")
    fig2.savefig(out_png2, dpi=200)
    print("wrote", out_csv, out_md, out_png, out_png2, out_png3)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for k in ("p22", "p23", "p24", "p25", "p26", "a21", "a22", "a23", "a24", "a25", "a26"):
        ap.add_argument("--" + k, required=True)
    main(ap.parse_args())
