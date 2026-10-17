#!/usr/bin/env python3
"""Benchmarks from the 2008 to 2011 era for Bourbon County, set against the current system.

Kentucky's CATS accountability index of that era is not online (KDE serves it by data
request), so the benchmarks here come from three public sources that do survive:

  1. The Legislative Research Commission's Kentucky District Data Profiles for school
     years 2008, 2009, 2010 and 2011 (Office of Education Accountability research
     reports 360, 368, 382 and 392): Bourbon County's Kentucky Core Content Test
     results by level against the state, the 2008 academic index, ACT, AP and
     graduation figures. Transcribed into build/benchmarks_oea_2008_2011.csv and
     build/benchmarks_oea_other_2008_2011.csv.
  2. The federal EDFacts district proficiency series already archived in the
     repository (build/ky_edfacts_district_2009_2018.csv), which ranks Bourbon County
     among every Kentucky district from 2009 to 2018.
  3. KYSTATS High School Feedback Reports for Bourbon County High School, classes of
     2010 to 2015, 2021, 2023 and 2024 (build/benchmarks_hsfr_2010_2024.csv and
     build/benchmarks_hsfr_instate_series.csv): college-going, readiness and ACT.

Writes build/benchmarks_2008_2026.md and three charts:
  build/benchmark_standing_2009_2026_chart.png   district standing among Kentucky districts, two eras
  build/benchmark_gap_2008_2026_chart.png        district minus state, percent proficient, by level, two eras
  build/benchmark_postsecondary_2010_2024_chart.png  college-going and ACT, Bourbon County High against Kentucky

Usage: python3 build/benchmarks_2008_2026.py
"""
import csv
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import gridspec  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
NAVY, ROYAL, GRAY, INK, MUTED, LINE = "#1F3864", "#2E75B6", "#8A93A6", "#1C2230", "#6B7486", "#E3E8F0"
BOX = dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85)
LEVELS = [("ES", "Elementary"), ("MS", "Middle"), ("HS", "High")]
KSA_YEARS = ["2020-21", "2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]
KCCT_YEARS = ["2008", "2009", "2010", "2011"]


def num(s):
    s = (s or "").strip()
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


def read_csv(name):
    with open(os.path.join(HERE, name), encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def style(ax, xlabels=None, xs=None):
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color(LINE)
    ax.tick_params(colors=MUTED, labelsize=8.4, length=0)
    ax.yaxis.grid(True, color=LINE, lw=0.8)
    ax.set_axisbelow(True)
    if xs is not None:
        ax.set_xticks(xs)
        ax.set_xticklabels(xlabels, fontsize=8.2)


def main():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5})

    # ---------- EDFacts: Bourbon's percentile among districts, 2009 to 2018 ----------
    ed = read_csv("ky_edfacts_district_2009_2018.csv")
    ed_years = sorted({r["year"] for r in ed})
    ed_pct, ed_rank = {}, {}
    for y in ed_years:
        rows = [(r["district"], num(r["math_pct_prof_midpt"]), num(r["read_pct_prof_midpt"])) for r in ed if r["year"] == y]
        rows = [t for t in rows if t[1] is not None and t[2] is not None]
        for key, idx in (("math", 1), ("reading", 2)):
            vals = [t[idx] for t in rows]
            mine = next((t[idx] for t in rows if t[0] == "Bourbon County"), None)
            if mine is None:
                continue
            below = sum(1 for v in vals if v < mine)
            equal = sum(1 for v in vals if v == mine)
            ed_pct[(y, key)] = 100.0 * (below + 0.5 * equal) / len(vals)
            ed_rank[(y, key)] = (sorted(vals, reverse=True).index(mine) + 1, len(vals), mine)

    # ---------- current system: reading and math status percentile by level ----------
    cur = read_csv("kde_district_trend_levels_2021_2026.csv")
    rm_pct, rm_rank, pd_ = {}, {}, {}
    for r in cur:
        if r["measure"] == "rm" and r["district"] == "Bourbon County" and r.get("percentile"):
            rm_pct[(r["year"], r["level"])] = num(r["percentile"])
            rm_rank[(r["year"], r["level"])] = (int(r["rank_from_top"]), int(r["districts"]))
        if r["measure"].startswith("pd:"):
            pd_[(r["year"], r["level"], r["district"], r["measure"][3:])] = num(r["value"])

    # ---------- OEA profiles: KCCT percent proficient by level, 2008 to 2011 ----------
    oea = read_csv("benchmarks_oea_2008_2011.csv")
    kcct = {(r["year"], r["level"], r["subject"]): (num(r["district_pd"]), num(r["state_pd"])) for r in oea}
    other = read_csv("benchmarks_oea_other_2008_2011.csv")

    # ---------- KYSTATS feedback reports ----------
    hs = read_csv("benchmarks_hsfr_2010_2024.csv")
    inst = read_csv("benchmarks_hsfr_instate_series.csv")

    # ================= chart 1: standing among Kentucky districts, two eras =================
    fig = plt.figure(figsize=(12.5, 8.6))
    gs = gridspec.GridSpec(2, 3, figure=fig, height_ratios=[1.15, 1.0], hspace=0.5, wspace=0.16,
                           left=0.06, right=0.985, top=0.9, bottom=0.1)
    ax = fig.add_subplot(gs[0, :])
    xs = list(range(len(ed_years)))
    ax.axhspan(0, 25, color="#F3F5F8", zorder=0)
    ax.axhline(50, color=GRAY, lw=1.2, ls=(0, (4, 3)), zorder=1)
    for key, color, ls, mk, label in (("reading", NAVY, "-", "o", "Reading"), ("math", ROYAL, (0, (5, 3)), "s", "Mathematics")):
        ys = [ed_pct.get((y, key)) for y in ed_years]
        ax.plot(xs, ys, color=color, lw=2.2, ls=ls, marker=mk, ms=7, markeredgecolor="white", markeredgewidth=1.2,
                zorder=3, label=label)
        for x, y in zip(xs, ys):
            other_v = ed_pct.get((ed_years[x], "math" if key == "reading" else "reading"))
            dy = 3.0 if (other_v is None or y >= other_v) else -3.0
            rk = ed_rank[(ed_years[x], key)]
            ax.text(x, y + dy, f"{ordinal(int(round(y)))}\n{rk[0]} of {rk[1]}", ha="center",
                    va="bottom" if dy > 0 else "top", color=color, fontsize=7.4, linespacing=1.25, zorder=6, bbox=BOX)
    ax.text(len(ed_years) - 1 + 0.45, 50, "median\ndistrict", color=MUTED, fontsize=7.4, ha="left", va="center")
    ax.text(len(ed_years) - 1 + 0.45, 12.5, "bottom\nquarter", color=MUTED, fontsize=7.4, ha="left", va="center")
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_xlim(-0.5, len(ed_years) - 1 + 1.0)
    style(ax, ed_years, xs)
    ax.set_title("Federal EDFacts series, all grades: percent proficient in reading and mathematics, percentile among Kentucky districts",
                 color=INK, fontsize=10.5, loc="left", pad=8)
    ax.set_ylabel("Percentile", color=INK, fontsize=9.5)
    ax.legend(loc="upper right", bbox_to_anchor=(0.9, 1.0), ncol=2, frameon=False, fontsize=9)
    years5 = ["2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]
    for j, (lv, short) in enumerate(LEVELS):
        axb = fig.add_subplot(gs[1, j])
        xs5 = list(range(len(years5)))
        axb.axhspan(0, 25, color="#F3F5F8", zorder=0)
        axb.axhline(50, color=GRAY, lw=1.2, ls=(0, (4, 3)), zorder=1)
        ys = [rm_pct.get((y, lv)) for y in years5]
        axb.plot(xs5, ys, color=NAVY, lw=2.2, marker="o", ms=7, markeredgecolor="white", markeredgewidth=1.2, zorder=3)
        for x, y in zip(xs5, ys):
            if y is None:
                continue
            rk = rm_rank[(years5[x], lv)]
            ry, rva = (y - 3.2, "top") if y >= 16 else (y + 3.2, "bottom")
            axb.text(x, ry, f"{ordinal(int(round(y)))}\n{rk[0]} of {rk[1]}", ha="center", va=rva, color=NAVY,
                     fontsize=7.4, linespacing=1.25, zorder=6, bbox=BOX)
        axb.set_ylim(0, 100)
        axb.set_yticks([0, 25, 50, 75, 100])
        axb.set_xlim(-0.5, len(years5) - 1 + 0.5)
        style(axb, years5, xs5)
        axb.set_title(f"{short} level", color=INK, fontsize=10, loc="left", pad=6)
        if j == 0:
            axb.set_ylabel("Percentile", color=INK, fontsize=9.5)
    fig.suptitle("Where Bourbon County has stood among Kentucky's districts, 2009 to 2026",
                 x=0.04, ha="left", fontsize=12.5, color=INK, fontweight="bold", y=0.985)
    fig.text(0.06, 0.455, "State accountability system, 2021-22 to 2025-26: reading and mathematics status, percentile among Kentucky districts, by level",
             fontsize=10.5, color=INK, ha="left", va="bottom")
    fig.text(0.04, 0.012,
             "Sources: federal EDFacts district proficiency file archived in the repository (build/ky_edfacts_district_2009_2018.csv, "
             "all tested grades, range midpoints); KDE accountability profiles 2021-22 to 2025-26, district rows. The two eras use different "
             "tests and measures, so compare standing, not scores. Percentile is the share of districts at or below Bourbon County; "
             "the second line under each point is its rank, 1 = highest.",
             fontsize=7.3, color=MUTED, ha="left", va="bottom", wrap=True)
    fig.savefig(os.path.join(HERE, "benchmark_standing_2009_2026_chart.png"), dpi=200)

    # ================= chart 2: district minus state, percent proficient, by level, two eras =================
    fig2, axes2 = plt.subplots(1, 3, figsize=(12.5, 4.9), sharey=True)
    labels = KCCT_YEARS + [""] + KSA_YEARS
    xs_all = list(range(len(labels)))
    for i, (lv, short) in enumerate(LEVELS):
        ax = axes2[i]
        ax.axhline(0, color=GRAY, lw=1.2, zorder=1)
        ax.axvspan(3.5, 4.5, color="#F3F5F8", zorder=0)
        for subj, color, ls, mk in (("Reading", NAVY, "-", "o"), ("Mathematics", ROYAL, (0, (5, 3)), "s")):
            xs, ys = [], []
            for k, y in enumerate(KCCT_YEARS):
                d, s = kcct.get((y, lv, subj), (None, None))
                if d is not None and s is not None:
                    xs.append(k)
                    ys.append(d - s)
            ax.plot(xs, ys, color=color, lw=2.2, ls=ls, marker=mk, ms=6.5, markeredgecolor="white", markeredgewidth=1.2,
                    zorder=3, label=subj)
            xs2, ys2 = [], []
            for k, y in enumerate(KSA_YEARS):
                d = pd_.get((y, lv, "Bourbon County", subj))
                s = pd_.get((y, lv, "Kentucky", subj))
                if d is not None and s is not None:
                    xs2.append(len(KCCT_YEARS) + 1 + k)
                    ys2.append(d - s)
            ax.plot(xs2, ys2, color=color, lw=2.2, ls=ls, marker=mk, ms=6.5, markeredgecolor="white", markeredgewidth=1.2, zorder=3)
            for x, v in list(zip(xs, ys)) + list(zip(xs2, ys2)):
                # the higher of the two subjects takes the label above its point, the lower below
                if x < len(KCCT_YEARS):
                    o = kcct.get((KCCT_YEARS[x], lv, "Mathematics" if subj == "Reading" else "Reading"), (None, None))
                    other_gap = (o[0] - o[1]) if o[0] is not None and o[1] is not None else None
                else:
                    y = KSA_YEARS[x - len(KCCT_YEARS) - 1]
                    od = pd_.get((y, lv, "Bourbon County", "Mathematics" if subj == "Reading" else "Reading"))
                    os_ = pd_.get((y, lv, "Kentucky", "Mathematics" if subj == "Reading" else "Reading"))
                    other_gap = (od - os_) if od is not None and os_ is not None else None
                above = other_gap is None or v > other_gap or (v == other_gap and subj == "Reading")
                ax.text(x, v + (1.8 if above else -1.8), f"{v:+.0f}", ha="center", va="bottom" if above else "top",
                        color=color, fontsize=7.4, zorder=6, bbox=BOX)
        ax.text(1.5, 24.5, "Core Content Tests (CATS era)", ha="center", va="top", color=MUTED, fontsize=7.8)
        ax.text(7.5, 24.5, "Kentucky Summative Assessment", ha="center", va="top", color=MUTED, fontsize=7.8)
        ax.set_ylim(-26, 26)
        ax.set_xlim(-0.6, len(labels) - 0.4)
        style(ax, labels, xs_all)
        for t in ax.get_xticklabels():
            t.set_rotation(45)
            t.set_ha("right")
        ax.set_title(f"{short} school level", color=INK, fontsize=11, loc="left", pad=8)
        if i == 0:
            ax.set_ylabel("Bourbon County minus Kentucky, points", color=INK, fontsize=9.5)
            ax.text(-0.45, 19.5, "above the state", color=MUTED, fontsize=7.4, ha="left", va="top")
            ax.text(-0.45, -19.5, "below the state", color=MUTED, fontsize=7.4, ha="left", va="bottom")
    h, lab = axes2[0].get_legend_handles_labels()
    fig2.legend(h, lab, loc="upper right", bbox_to_anchor=(0.985, 0.93), ncol=2, frameon=False, fontsize=9.5)
    fig2.suptitle("Then and now: Bourbon County's percent proficient or distinguished minus Kentucky's, by level",
                  x=0.04, ha="left", fontsize=12.2, color=INK, fontweight="bold", y=0.985)
    fig2.text(0.04, 0.012,
              "Sources: Legislative Research Commission, Kentucky District Data Profiles for school years 2008 to 2011 (Core Content Tests, "
              "district and state percent proficient or distinguished by level); KDE assessment files 2020-21 to 2025-26, district and state "
              "rows. The two tests differ, so the chart compares the gap to the state, not the scores.",
              fontsize=7.3, color=MUTED, ha="left", va="bottom", wrap=True)
    fig2.subplots_adjust(left=0.06, right=0.985, top=0.8, bottom=0.2, wspace=0.1)
    fig2.savefig(os.path.join(HERE, "benchmark_gap_2008_2026_chart.png"), dpi=200)

    # ================= chart 3: postsecondary benchmarks =================
    fig3, axes3 = plt.subplots(1, 2, figsize=(12.5, 4.9))
    ax = axes3[0]
    yrs = [r["class_year"] for r in inst]
    xs = list(range(len(yrs)))
    # leave a visible gap where 2015-16 is missing
    gap_after = yrs.index("2014-15")
    xpos = [x if x <= gap_after else x + 1 for x in xs]
    for key, color, ls, mk, label in (("instate_college_going_state", GRAY, (0, (4, 3)), "s", "Kentucky"),
                                      ("instate_college_going", NAVY, "-", "o", "Bourbon County High")):
        ys = [num(r[key]) for r in inst]
        seg1 = [(xpos[k], ys[k]) for k in range(len(ys)) if k <= gap_after]
        seg2 = [(xpos[k], ys[k]) for k in range(len(ys)) if k > gap_after]
        for seg in (seg1, seg2):
            ax.plot([p[0] for p in seg], [p[1] for p in seg], color=color, lw=2.2, ls=ls, marker=mk, ms=6.5,
                    markeredgecolor="white", markeredgewidth=1.2, zorder=3 if key.endswith("state") else 4,
                    label=label if seg is seg1 else None)
        for k, v in enumerate(ys):
            other_v = num(inst[k]["instate_college_going" if key.endswith("state") else "instate_college_going_state"])
            dy = 1.5 if v >= other_v else -1.5
            ax.text(xpos[k], v + dy, f"{v:.0f}", ha="center", va="bottom" if dy > 0 else "top",
                    color=NAVY if key == "instate_college_going" else MUTED, fontsize=7.4,
                    fontweight="bold" if key == "instate_college_going" else "normal", zorder=6, bbox=BOX)
    ax.set_ylim(35, 72)
    ax.set_xlim(-0.6, max(xpos) + 0.6)
    ax.set_xticks(xpos)
    ax.set_xticklabels([y[2:] if False else y for y in yrs], fontsize=7.6, rotation=45, ha="right")
    style(ax)
    ax.set_title("Share of graduates enrolling in a Kentucky college the next fall (in-state college-going rate)",
                 color=INK, fontsize=9.6, loc="left", pad=8)
    ax.set_ylabel("Percent of graduates", color=INK, fontsize=9.5)
    ax.legend(loc="lower left", frameon=False, fontsize=8.8)
    ax = axes3[1]
    classes = [r["class_year"] for r in hs]
    xpos2 = []
    for c in classes:
        xpos2.append(int(c) - 2010)
    for key, color, ls, mk, label in (("act_composite_state", GRAY, (0, (4, 3)), "s", "Kentucky"),
                                      ("act_composite", NAVY, "-", "o", "Bourbon County High")):
        ys = [num(r[key]) for r in hs]
        # draw contiguous runs only
        runs, run = [], []
        for x, y in zip(xpos2, ys):
            if run and x != run[-1][0] + 1:
                runs.append(run)
                run = []
            run.append((x, y))
        runs.append(run)
        for n, seg in enumerate(runs):
            ax.plot([p[0] for p in seg], [p[1] for p in seg], color=color, lw=2.2, ls=ls, marker=mk, ms=6.5,
                    markeredgecolor="white", markeredgewidth=1.2, zorder=3 if key.endswith("state") else 4,
                    label=label if n == 0 else None)
        for x, v, r in zip(xpos2, ys, hs):
            other_v = num(r["act_composite" if key.endswith("state") else "act_composite_state"])
            dy = 0.22 if v >= other_v else -0.22
            ax.text(x, v + dy, f"{v:.1f}", ha="center", va="bottom" if dy > 0 else "top",
                    color=NAVY if key == "act_composite" else MUTED, fontsize=7.4,
                    fontweight="bold" if key == "act_composite" else "normal", zorder=6, bbox=BOX)
    ax.set_ylim(17, 21)
    ax.set_xlim(-0.6, 14.6)
    ax.set_xticks(list(range(0, 15)))
    ax.set_xticklabels([str(2010 + k) for k in range(15)], fontsize=7.6, rotation=45, ha="right")
    style(ax)
    ax.set_title("Average junior-year ACT composite of each graduating class", color=INK, fontsize=9.6, loc="left", pad=8)
    ax.set_ylabel("ACT composite", color=INK, fontsize=9.5)
    ax.legend(loc="upper left", frameon=False, fontsize=8.8)
    fig3.suptitle("Postsecondary benchmarks since 2010: Bourbon County High School against Kentucky (KYSTATS feedback reports)",
                  x=0.04, ha="left", fontsize=12, color=INK, fontweight="bold", y=0.985)
    fig3.text(0.04, 0.012,
              "Source: Kentucky High School Feedback Reports for Bourbon County High School (KYSTATS and its predecessor), classes of 2010 "
              "to 2015, 2021, 2023 and 2024; no report was found for the classes of 2016 to 2020 and 2022, and the 2015-16 college-going "
              "year is not covered by any report in hand. In-state rates are taken from the latest report covering each year so the "
              "definition is consistent. The ACT panel shows the classes with a report.",
              fontsize=7.2, color=MUTED, ha="left", va="bottom", wrap=True)
    fig3.subplots_adjust(left=0.06, right=0.985, top=0.84, bottom=0.26, wspace=0.16)
    fig3.savefig(os.path.join(HERE, "benchmark_postsecondary_2010_2024_chart.png"), dpi=200)

    # ================= note =================
    L = ["# Benchmarks from the 2008 to 2011 era, against the current system\n",
         "The Commonwealth Accountability Testing System (CATS) index that Kentucky published from 1999 to 2011 is "
         "no longer posted by KDE; the department supplies those school and district files by data request, and the "
         "Wayback Machine is not reachable from this environment. Three public sources that do survive give the "
         "district's standing in that era: the Legislative Research Commission's Kentucky District Data Profiles for "
         "school years 2008 to 2011 (Core Content Test results by level against the state, the 2008 academic index, "
         "ACT, AP and graduation), the federal EDFacts district proficiency series from 2009, and the KYSTATS High "
         "School Feedback Reports for Bourbon County High School from the class of 2010. Values from the profiles "
         "and feedback reports were transcribed by hand from the PDFs listed under Sources.\n"]

    L.append("## Core Content Tests, 2008 to 2011: percent proficient or distinguished, Bourbon County (Kentucky)\n")
    L.append("| Level | Subject | 2008 | 2009 | 2010 | 2011 |")
    L.append("|---|---|---|---|---|---|")
    for lv, short in LEVELS:
        for subj in ("Reading", "Mathematics", "Science", "Writing"):
            cells = []
            for y in KCCT_YEARS:
                d, s = kcct.get((y, lv, subj), (None, None))
                cells.append(f"{d:.0f} ({s:.0f})" if d is not None else "n/a")
            L.append(f"| {short} | {subj} | " + " | ".join(cells) + " |")
    L.append("")
    L.append("The 2008 profile also prints the CATS academic index by subject and level, district (state): "
             "reading elementary 100 (95), middle 87 (92), high 81 (88); mathematics 107 (97), 77 (86), 69 (69); "
             "science 110 (98), 80 (88), 80 (72); writing 95 (90), 65 (81), 75 (76). The index ran 0 to 140 with "
             "100 as the state's long-term goal.\n")

    L.append("## The same gap today: Kentucky Summative Assessment, percent proficient or distinguished, Bourbon County (Kentucky)\n")
    L.append("| Level | Subject | " + " | ".join(KSA_YEARS) + " |")
    L.append("|---|---|" + "---|" * len(KSA_YEARS))
    for lv, short in LEVELS:
        for subj in ("Reading", "Mathematics"):
            cells = []
            for y in KSA_YEARS:
                d = pd_.get((y, lv, "Bourbon County", subj))
                s = pd_.get((y, lv, "Kentucky", subj))
                cells.append(f"{d:.0f} ({s:.0f})" if d is not None and s is not None else "n/a")
            L.append(f"| {short} | {subj} | " + " | ".join(cells) + " |")
    L.append("")

    L.append("## Standing among Kentucky districts: federal EDFacts series, 2009 to 2018\n")
    L.append("Percent proficient in reading and mathematics, all tested grades, range midpoints as EDFacts reports them. "
             "Rank 1 is the highest district; the percentile is the share of districts at or below Bourbon County.\n")
    L.append("| Year | Reading | Rank | Percentile | Mathematics | Rank | Percentile |")
    L.append("|---|---|---|---|---|---|---|")
    for y in ed_years:
        rr, mr = ed_rank[(y, "reading")], ed_rank[(y, "math")]
        L.append(f"| {y} | {rr[2]:.0f} | {rr[0]} of {rr[1]} | {ordinal(int(round(ed_pct[(y, 'reading')])))} | "
                 f"{mr[2]:.0f} | {mr[0]} of {mr[1]} | {ordinal(int(round(ed_pct[(y, 'math')])))} |")
    L.append("")
    L.append("For comparison, on the state's reading and mathematics status in 2025-26 the district ranks "
             + ", ".join(f"{short.lower()} {rm_rank[('2025-26', lv)][0]} of {rm_rank[('2025-26', lv)][1]} ({ordinal(int(round(rm_pct[('2025-26', lv)])))} percentile)" for lv, short in LEVELS) + ".\n")

    L.append("## Other 2008 to 2011 district benchmarks from the profiles\n")
    L.append("| Year | Measure | Bourbon County | Comparison | Note |")
    L.append("|---|---|---|---|---|")
    for r in other:
        L.append(f"| {r['year']} | {r['measure']} | {r['district']} | {r['state_or_benchmark'] or ''} | {r['note']} |")
    L.append("")

    L.append("## Postsecondary benchmarks: KYSTATS High School Feedback Reports, Bourbon County High School\n")
    L.append("| Class | Graduates | Junior ACT composite (KY) | Free or reduced lunch (KY) | Overall college-going (KY) | In-state college-going (KY) | College and/or career ready (KY) | Graduation rate |")
    L.append("|---|---|---|---|---|---|---|---|")
    for r in hs:
        def pair(a, b):
            va, vb = num(r[a]), num(r[b])
            if va is None:
                return "n/a"
            return f"{va:.1f}" + (f" ({vb:.1f})" if vb is not None else "")
        L.append(f"| {r['class_year']} | {r['graduates']} | {pair('act_composite', 'act_composite_state')} | "
                 f"{pair('frl_pct', 'frl_pct_state')} | {pair('college_going_overall', 'college_going_overall_state')} | "
                 f"{pair('college_going_instate', 'college_going_instate_state')} | "
                 f"{pair('ready_college_or_career_kde', 'ready_college_or_career_kde_state')} | {r['grad_rate'] or 'n/a'} |")
    L.append("")
    L.append("The class of 2010 report also gives the share of graduates meeting the Council on Postsecondary Education "
             "benchmarks on the junior ACT: mathematics 33.8 percent, English 46.5 percent, reading 45.1 percent "
             "(class of 2011: 38.7, 51.0 and 46.5 percent). Readiness as the state defines it today, with its "
             "career routes, is in the 2012 and later reports; the 2021 report carries no readiness figure because "
             "of COVID-19.\n")
    L.append("In-state college-going rate, taken from the latest report that covers each class so the definition is consistent:\n")
    L.append("| Class | Bourbon County High | Kentucky |")
    L.append("|---|---|---|")
    for r in inst:
        L.append(f"| {r['class_year']} | {num(r['instate_college_going']):.1f} | {num(r['instate_college_going_state']):.1f} |")
    L.append("")

    L.append("## Sources\n")
    L.append("- Legislative Research Commission, Office of Education Accountability, Kentucky District Data Profiles: "
             "School Year 2007-2008 (Research Report 360, Bourbon County pages 50 and 51), School Year 2009 (Research Report 368, "
             "pages 50 and 51), School Year 2010 (Research Report 382, pages 50 and 51, ACT appendix pages 372 and 373), "
             "School Year 2011 (Research Report 392, pages 52 and 53). https://apps.legislature.ky.gov/lrc/publications/ResearchReports/RR360.pdf, "
             "RR368.pdf, RR382.pdf, RR392.pdf")
    L.append("- Federal EDFacts district achievement series archived as build/ky_edfacts_district_2009_2018.csv.")
    L.append("- KYSTATS, Kentucky High School Feedback Reports for Bourbon County High School (041_110): "
             "https://kystats.ky.gov/Content/Reports/HSFRCG_2010_041_110.pdf through HSFRCG_2015_041_110.pdf, "
             "HSFR_2021_041_110.pdf, HSFR_2023_041_110.pdf, HSFR_2024_041_110.pdf.")
    L.append("- KDE accountability profile and assessment files, 2020-21 to 2025-26, as used elsewhere in this repository.")
    open(os.path.join(HERE, "benchmarks_2008_2026.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("wrote charts and note")


if __name__ == "__main__":
    main()
