#!/usr/bin/env python3
"""Where Bourbon County's status scores fall among Kentucky's districts, by level, 2025-26.

Status is the year's own result on each accountability indicator, before the state
adds its change component. This script reads the district rows of KDE's two
accountability profile files and, for every district at the elementary, middle and
high school level, places each status score (and the published overall score) in
the statewide distribution. It also builds a status-only overall from the state's
own indicator weights, after checking that those weights reproduce every published
overall score.

Writes:
  build/kde_district_status_2025_26.csv    one row per district, level, measure and year
  build/district_status_2025_26.md         the distributions and Bourbon County's place
  build/district_status_2025_26_chart.png  small multiples, Bourbon County marked

Usage:
  python3 -I build/district_status_2025_26.py <KYRC25_ACCT_Profile.csv> <Accountable_Profile_2026.CSV>
"""
import csv
import math
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.ticker  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
BOURBON = "041"
LEVELS = [("ES", "Elementary School", "Elementary"),
          ("MS", "Middle School", "Middle"),
          ("HS", "High School", "High")]
RATING = {1: "very low", 2: "low", 3: "medium", 4: "high", 5: "very high"}

# KDE's state indicator weights (Accountability System Overview, November 2025, p. 7)
WEIGHTS = {
    "ES": {"rm": 51, "ssw": 40, "el": 5, "qscs": 4},
    "MS": {"rm": 46, "ssw": 45, "el": 5, "qscs": 4},
    "HS": {"rm": 45, "ssw": 20, "el": 5, "qscs": 4, "ps": 20, "grad": 6},
}

# key, label, 2024-25 status column, 2025-26 status column, 2024-25 rating, 2025-26 rating, 2025-26 combined rate
IND = [
    ("rm", "Reading and mathematics status",
     "READING_MATH STATUS", "Reading_Mathematics Status",
     "READING_MATH STATUS RATING", "Reading_Mathematics Statue Rating",
     "Reading_Mathematics Combined Indicator Rate"),
    ("ssw", "Science, social studies and writing status",
     "SCIENCE_SOCIAL STUDIES_COMBINED WRITING STATUS", "Science_Social Studies_Combined Writing Status",
     "SCIENCE_SOCIAL STUDIES_COMBINED WRITING STATUS RATING", "Science_Social Studies_Combined Writing Statue Rating",
     "Science_Social Studies_Combined Writing Combined Indicator Rate"),
    ("el", "English learner progress status",
     "ENGLISH LEARNERS PROGRESS STATUS", "English Learners Progress Status",
     "ENGLISH LEARNERS PROGRESS STATUS RATING", "English Learners Progress Statue Rating",
     "English Learners Progress Combined Indicator Rate"),
    ("qscs", "Climate and safety survey status",
     "QUALITY OF SCHOOL CLIMATE AND SAFETY STATUS", "Quality Of School Climate and Safety Status",
     "QUALITY OF SCHOOL CLIMATE AND SAFETY STATUS RATING", "Quality Of School Climate and Safety Statue Rating",
     "Quality Of School Climate and Safety Combined Indicator Rate"),
    ("ps", "Postsecondary readiness status (high school)",
     "POSTSECONDARY STATUS", "Postsecondary Status",
     "POSTSECONDARY STATUS RATING", "Postsecondary Statue Rating",
     "Postsecondary Combined Indicator Rate"),
    ("grad", "Graduation rate status (high school)",
     "GRADUATION STATUS", "Graduation Status",
     "GRADUATION STATUS RATING", "Graduation Statue Rating",
     "Graduation Combined Indicator Rate"),
]
OVERALL25, OVERALL26 = "OVERALL COMBINED INDICATOR RATE", "Overall Combined Indicator Rate"
OVR_RATING25, OVR_RATING26 = "OVERALL INDICATOR RATING", "Overall Indicator Rating"
COLOR = {1: "red", 2: "orange", 3: "yellow", 4: "green", 5: "blue"}


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


def pct(sorted_vals, p):
    if not sorted_vals:
        return None
    k = (len(sorted_vals) - 1) * p / 100.0
    f, c = math.floor(k), math.ceil(k)
    if f == c:
        return sorted_vals[int(k)]
    return sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f)


def load(path25, path26):
    r25 = list(csv.DictReader(open(path25, encoding="utf-8-sig")))
    r26 = list(csv.DictReader(open(path26, encoding="utf-8-sig")))
    d25, d26 = {}, {}
    for r in r25:
        if r["School Type"].strip() == "" and r["School Name"].strip() == "All Schools":
            d25[(r["District Number"].strip(), r["Level"].strip())] = r
    for r in r26:
        if r["School Name"].strip() == "":
            d26[(r["School Code"].strip(), r["Level"].strip())] = r
    return d25, d26


def weighted(level, values):
    """Weighted mean on KDE's weights over the indicators present, weights redistributed proportionally."""
    w = WEIGHTS[level]
    num_, den = 0.0, 0.0
    for k, v in values.items():
        if v is None or k not in w:
            continue
        num_ += w[k] * v
        den += w[k]
    return num_ / den if den else None


def place(rows, dn):
    """rows: list of (dn, name, value). Returns (value, rank from top, percentile, n)."""
    vals = sorted((v for _, _, v in rows), reverse=True)
    n = len(vals)
    for d, name, v in rows:
        if d == dn:
            rank = vals.index(v) + 1
            below = sum(1 for x in vals if x < v)
            equal = sum(1 for x in vals if x == v)
            return v, rank, 100.0 * (below + 0.5 * equal) / n, n
    return None, None, None, n


def main(path25, path26):
    d25, d26 = load(path25, path26)
    MEASURES = [(k, lab) for k, lab, *_ in IND] + [
        ("status_only", "Status-only overall (KDE weights on status alone)"),
        ("overall", "Published overall score (status plus change)"),
    ]
    data = {}      # (level, measure, year) -> list of (dn, name, value)
    ratings = {}   # (level, measure, year, dn) -> rating label
    weight_check = {}

    for code, lname, short in LEVELS:
        maxdiff, nchk = 0.0, 0
        for year in ("2024-25", "2025-26"):
            for key, _ in MEASURES:
                data[(code, key, year)] = []
        for (dn, lv), r in d26.items():
            if lv != code or int(dn) >= 900 and dn != "999":
                continue
            o = d25.get((dn, lname))
            if o is None:
                continue
            name = r["District Name"]
            st25, st26, comb26 = {}, {}, {}
            for key, lab, c25, c26, rt25, rt26, cc26 in IND:
                st25[key] = num(o.get(c25))
                st26[key] = num(r.get(c26))
                comb26[key] = num(r.get(cc26))
                for year, val, rt in (("2024-25", st25[key], num(o.get(rt25))),
                                      ("2025-26", st26[key], num(r.get(rt26)))):
                    if val is not None:
                        data[(code, key, year)].append((dn, name, val))
                        if rt is not None:
                            ratings[(code, key, year, dn)] = RATING.get(int(rt), "")
            so25, so26 = weighted(code, st25), weighted(code, st26)
            if so25 is not None:
                data[(code, "status_only", "2024-25")].append((dn, name, round(so25, 1)))
            if so26 is not None:
                data[(code, "status_only", "2025-26")].append((dn, name, round(so26, 1)))
            ov25, ov26 = num(o.get(OVERALL25)), num(r.get(OVERALL26))
            if ov25 is not None:
                data[(code, "overall", "2024-25")].append((dn, name, ov25))
                rt = num(o.get(OVR_RATING25))
                if rt is not None:
                    ratings[(code, "overall", "2024-25", dn)] = COLOR.get(int(rt), "")
            if ov26 is not None:
                data[(code, "overall", "2025-26")].append((dn, name, ov26))
                rt = num(r.get(OVR_RATING26))
                if rt is not None:
                    ratings[(code, "overall", "2025-26", dn)] = COLOR.get(int(rt), "")
                rebuilt = weighted(code, comb26)
                if rebuilt is not None:
                    maxdiff = max(maxdiff, abs(rebuilt - ov26))
                    nchk += 1
        weight_check[code] = (nchk, maxdiff)

    # the state row (999) is reported separately and excluded from the distributions
    state = {}
    for k, rows in data.items():
        state[k] = next((v for dn, _, v in rows if dn == "999"), None)
        data[k] = [t for t in rows if t[0] != "999"]

    # ---------- CSV ----------
    out_csv = os.path.join(HERE, "kde_district_status_2025_26.csv")
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["district_number", "district", "level", "measure", "year", "value",
                    "rank_from_top", "districts", "percentile", "state_rating"])
        for (code, key, year), rows in sorted(data.items()):
            vals = sorted((v for _, _, v in rows), reverse=True)
            n = len(vals)
            for dn, name, v in sorted(rows, key=lambda t: (-t[2], t[1])):
                below = sum(1 for x in vals if x < v)
                equal = sum(1 for x in vals if x == v)
                w.writerow([dn, name, code, key, year, v, vals.index(v) + 1, n,
                            round(100.0 * (below + 0.5 * equal) / n, 1),
                            ratings.get((code, key, year, dn), "")])

    # ---------- summary ----------
    L = []
    L.append("# Bourbon County's status scores in the statewide distribution, by level\n")
    L.append("Status is the year's own result on each accountability indicator, before the state adds its "
             "change component. Every Kentucky district's status at the elementary, middle and high school "
             "level comes from the district rows of KDE's accountability profile files (KYRC25_ACCT_Profile.csv "
             "for 2024-25; Accountable_Profile_2026.CSV, released October 14, 2026, for 2025-26). Rank 1 is "
             "the highest status in the state; the percentile is the share of districts at or below Bourbon "
             "County, so a low percentile means most districts score higher. The state's level for each score "
             "(very low to very high) and the overall color are the ones printed in the state file. The "
             "education cooperatives are excluded; the state row is shown for reference.\n")
    L.append("The status-only overall applies KDE's published indicator weights (elementary 51/40/5/4, middle "
             "46/45/5/4, high 45/20/5/4/20/6 for reading and mathematics, science and social studies and writing, "
             "English learner progress, climate and safety, postsecondary readiness and graduation) to status "
             "alone, redistributing the weight of any missing indicator proportionally. Weight check: the same "
             "weights applied to KDE's combined indicator rates reproduce the published overall score for "
             + "; ".join(f"{short.lower()} {weight_check[code][0]} districts within {weight_check[code][1]:.2f}"
                         for code, _, short in LEVELS) + ".\n")

    L.append("## Bourbon County, both years, with its place among districts\n")
    L.append("| Level | Measure | 2024-25 | Rank | Pct | 2025-26 | Rank | Pct | State level 2025-26 |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for code, lname, short in LEVELS:
        for key, lab in MEASURES:
            v25, r25, p25, n25 = place(data[(code, key, "2024-25")], BOURBON)
            v26, r26, p26, n26 = place(data[(code, key, "2025-26")], BOURBON)
            if v26 is None and v25 is None:
                continue
            c25 = f"{v25:.1f} | {r25} of {n25} | {p25:.0f}" if v25 is not None else "n/a | n/a | n/a"
            c26 = f"{v26:.1f} | {r26} of {n26} | {p26:.0f}" if v26 is not None else "n/a | n/a | n/a"
            L.append(f"| {short} | {lab} | {c25} | {c26} | {ratings.get((code, key, '2025-26', BOURBON), '')} |")
    L.append("")

    for code, lname, short in LEVELS:
        L.append(f"## {short} school level, 2025-26: the statewide distribution of status\n")
        L.append("| Measure | Districts | 10th pct | 25th pct | Median | 75th pct | 90th pct | State row | Bourbon | Bourbon rank | Bourbon pct |")
        L.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for key, lab in MEASURES:
            rows = data[(code, key, "2025-26")]
            if not rows:
                continue
            d = sorted(v for _, _, v in rows)
            v, rk, pr, n = place(rows, BOURBON)
            st = state.get((code, key, "2025-26"))
            L.append(f"| {lab} | {n} | {pct(d, 10):.1f} | {pct(d, 25):.1f} | {pct(d, 50):.1f} | {pct(d, 75):.1f} | "
                     f"{pct(d, 90):.1f} | {st if st is not None else 'n/a'} | "
                     f"{v if v is not None else 'n/a'} | {f'{rk} of {n}' if rk else 'n/a'} | {f'{pr:.0f}' if pr is not None else 'n/a'} |")
        L.append("")
        for key in ("rm", "ssw"):
            rows = sorted(data[(code, key, "2025-26")], key=lambda t: t[2])
            lab = next(l for k, l in MEASURES if k == key)
            v, rk, pr, n = place(rows, BOURBON)
            L.append(f"Lowest {lab.lower()}, {short.lower()} level, 2025-26 (Bourbon County is {ordinal(n - rk + 1)} from the bottom):\n")
            for dn, name, val in rows[:12]:
                mark = " (Bourbon County)" if dn == BOURBON else ""
                L.append(f"- {name}: {val:.1f}{mark}")
            if rk and (n - rk + 1) > 12:
                L.append(f"- ... Bourbon County: {v:.1f}, {ordinal(n - rk + 1)} from the bottom")
            L.append("")

    out_md = os.path.join(HERE, "district_status_2025_26.md")
    open(out_md, "w", encoding="utf-8").write("\n".join(L))

    # ---------- chart ----------
    NAVY, GRAY, INK, MUTED = "#1F3864", "#8A93A6", "#1C2230", "#6B7486"
    BAR, LINE = "#B8C2D0", "#E3E8F0"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5})
    cols = [("rm", "Reading and mathematics status, 2025-26"),
            ("ssw", "Science, social studies and writing status, 2025-26")]
    fig, axes = plt.subplots(3, 2, figsize=(11.5, 9.4), sharex="col")
    for j, (key, ctitle) in enumerate(cols):
        allv = [v for code, _, _ in LEVELS for _, _, v in data[(code, key, "2025-26")]]
        lo = math.floor(min(allv) / 5.0) * 5 - 2
        hi = math.ceil(max(allv) / 5.0) * 5 + 2
        bins = list(range(int(lo), int(hi) + 2, 2))
        for i, (code, lname, short) in enumerate(LEVELS):
            ax = axes[i][j]
            rows = data[(code, key, "2025-26")]
            vals = [v for _, _, v in rows]
            d = sorted(vals)
            median = pct(d, 50)
            counts, _, _ = ax.hist(vals, bins=bins, color=BAR, edgecolor="white", linewidth=1.0, zorder=2)
            ymax = max(counts) * 1.32
            ax.set_ylim(0, ymax)
            ax.set_xlim(lo, hi)
            v, rk, pr, n = place(rows, BOURBON)
            v25, r25, p25, n25 = place(data[(code, key, "2024-25")], BOURBON)
            ax.axvline(median, color=GRAY, lw=1.4, ls=(0, (4, 3)), zorder=4)
            med_right = not (v is not None and v > median)
            ax.text(median, ymax * 0.60, f" median {median:.1f} ", color=MUTED, fontsize=8.5,
                    ha="left" if med_right else "right", va="center", zorder=6)
            if v is not None:
                ax.axvline(v, color=NAVY, lw=2.2, zorder=5)
                level = ratings.get((code, key, "2025-26", BOURBON), "")
                label = (f"Bourbon County {v:.1f} ({level})\n{ordinal(rk)} of {n} districts, "
                         f"{ordinal(int(round(pr)))} percentile")
                left_side = v < (lo + hi) / 2.0
                ax.annotate(label, xy=(v, ymax * 0.80),
                            xytext=(0.985, 0.95) if left_side else (0.015, 0.95),
                            textcoords="axes fraction", ha="right" if left_side else "left", va="top",
                            color=NAVY, fontsize=9, fontweight="bold", zorder=7,
                            arrowprops=dict(arrowstyle="-", color=NAVY, lw=0.9, shrinkA=0, shrinkB=2))
                if v25 is not None:
                    ax.axvline(v25, color=NAVY, lw=1.1, ls=(0, (1.5, 2.5)), zorder=4)
                    ax.text(v25, ymax * 0.30, f" 2024-25: {v25:.1f} ", color=NAVY, fontsize=8,
                            ha="left" if v25 >= v else "right", va="center", zorder=6)
            for sp in ("top", "right"):
                ax.spines[sp].set_visible(False)
            for sp in ("left", "bottom"):
                ax.spines[sp].set_color(LINE)
            ax.tick_params(colors=MUTED, labelsize=8.5, length=0)
            ax.yaxis.grid(True, color=LINE, lw=0.8, zorder=0)
            ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
            ax.set_axisbelow(True)
            if j == 0:
                ax.set_ylabel(f"{short} level\n{n} districts", color=INK, fontsize=10, labelpad=10)
            if i == 0:
                ax.set_title(ctitle, color=INK, fontsize=11, loc="left", pad=8)
            if i == 2:
                ax.set_xlabel("Status score (district, all students)", color=MUTED, fontsize=9)
            ax.set_xticks(range(int(math.ceil(lo / 10.0)) * 10, int(hi) + 1, 10))
    fig.suptitle("Status, not change: where Bourbon County's 2025-26 scores fall among Kentucky's districts, by level",
                 x=0.045, ha="left", fontsize=12.5, color=INK, fontweight="bold", y=0.985)
    fig.text(0.045, 0.012,
             "Source: KDE accountability profiles, district rows (Accountable_Profile_2026.CSV, October 14, 2026; "
             "KYRC25_ACCT_Profile.csv for the 2024-25 marker). Status is the year's own result on the indicator. "
             "Bars count districts in two-point bins; the level in parentheses is the state's own rating; "
             "the cooperatives and the state row are excluded.",
             fontsize=7.8, color=MUTED, ha="left", va="bottom", wrap=True)
    fig.subplots_adjust(left=0.085, right=0.985, top=0.915, bottom=0.095, hspace=0.32, wspace=0.14)
    out_png = os.path.join(HERE, "district_status_2025_26_chart.png")
    fig.savefig(out_png, dpi=200)
    print("wrote", out_csv, out_md, out_png)
    for code, _, short in LEVELS:
        print(f"weight check {short}: {weight_check[code][0]} districts, max diff {weight_check[code][1]:.3f}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
