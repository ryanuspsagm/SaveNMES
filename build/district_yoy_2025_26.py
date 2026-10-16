#!/usr/bin/env python3
"""Year-over-year change, 2024-25 to 2025-26, for every Kentucky district by level.

Reads the district rows of KDE's two accountability profile files and writes:
  build/kde_district_yoy_2025_26.csv    one row per district, level and measure
  build/district_yoy_2025_26.md         the distributions and Bourbon County's place in them
  build/district_yoy_2025_26_chart.png  small multiples of the distributions

Usage:
  python3 -I build/district_yoy_2025_26.py <KYRC25_ACCT_Profile.csv> <Accountable_Profile_2026.CSV>

The 2024-25 file (KYRC25_ACCT_Profile.csv, KDE historical datasets) carries each
district's totals as rows named "All Schools" with a blank School Type. The
2025-26 file (Accountable_Profile_2026.CSV, released October 14, 2026) carries
them as rows with a blank School Name. The two are matched on the district
number. The education cooperatives (codes 901 to 909) and the state row (999)
are excluded from the distributions; the state row is reported separately.
"""
import csv
import math
import os
import statistics
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
BOURBON = "041"

LEVELS = [("ES", "Elementary School", "Elementary"),
          ("MS", "Middle School", "Middle"),
          ("HS", "High School", "High")]

# key, label, 2024-25 column, 2025-26 column, 2025-26 change column (if KDE publishes one)
MEASURES = [
    ("overall", "Overall score (status plus change)",
     "OVERALL COMBINED INDICATOR RATE", "Overall Combined Indicator Rate", None),
    ("rm_status", "Reading and mathematics status",
     "READING_MATH STATUS", "Reading_Mathematics Status", "Reading_Mathematics Change"),
    ("ssw_status", "Science, social studies and writing status",
     "SCIENCE_SOCIAL STUDIES_COMBINED WRITING STATUS",
     "Science_Social Studies_Combined Writing Status",
     "Science_Social Studies_Combined Writing Change"),
    ("qscs_status", "Climate and safety survey status",
     "QUALITY OF SCHOOL CLIMATE AND SAFETY STATUS",
     "Quality Of School Climate and Safety Status",
     "Quality Of School Climate and Safety Change"),
    ("ps_status", "Postsecondary readiness status (high school only)",
     "POSTSECONDARY STATUS", "Postsecondary Status", "Postsecondary Change"),
    ("grad_status", "Graduation status (high school only)",
     "GRADUATION STATUS", "Graduation Status", "Graduation Change"),
]


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
    """Linear-interpolated percentile of a sorted list, p in 0..100."""
    if not sorted_vals:
        return None
    k = (len(sorted_vals) - 1) * p / 100.0
    f = math.floor(k)
    c = math.ceil(k)
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


def main(path25, path26):
    d25, d26 = load(path25, path26)
    records = []      # long-format rows for the CSV
    dist = {}         # (level, measure) -> list of (code, name, v25, v26, delta)
    state = {}        # (level, measure) -> delta for the state row
    mismatches = []   # KDE change column vs our difference

    for code, lname, _ in LEVELS:
        for key, label, c25, c26, cchg in MEASURES:
            rows = []
            for (dn, lv), r in d26.items():
                if lv != code:
                    continue
                r_old = d25.get((dn, lname))
                if r_old is None:
                    continue
                v26 = num(r.get(c26))
                v25 = num(r_old.get(c25))
                if v26 is None or v25 is None:
                    continue
                delta = round(v26 - v25, 1)
                if cchg:
                    kde = num(r.get(cchg))
                    if kde is not None and abs(kde - (v26 - v25)) > 0.15:
                        mismatches.append((dn, r["District Name"], code, key, kde, delta))
                if dn == "999":
                    state[(code, key)] = (v25, v26, delta)
                    continue
                if int(dn) >= 900:
                    continue
                rows.append((dn, r["District Name"], v25, v26, delta))
            rows.sort(key=lambda t: (t[4], t[1]))
            dist[(code, key)] = rows
            n = len(rows)
            deltas = [t[4] for t in rows]
            for i, (dn, name, v25, v26, delta) in enumerate(rows):
                below = sum(1 for x in deltas if x < delta)
                equal = sum(1 for x in deltas if x == delta)
                percentile = 100.0 * (below + 0.5 * equal) / n if n else None
                records.append({
                    "district_number": dn, "district": name, "level": code, "measure": key,
                    "value_2024_25": v25, "value_2025_26": v26, "change": delta,
                    "rank_from_bottom": i + 1, "districts": n,
                    "percentile": round(percentile, 1) if percentile is not None else "",
                })

    # ---------- did last year's gains revert? (reading and mathematics status) ----------
    revert = {}
    for code, lname, short in LEVELS:
        pairs = []
        for (dn, lv), r in d26.items():
            if lv != code or int(dn) >= 900:
                continue
            o = d25.get((dn, lname))
            if o is None:
                continue
            c25 = num(o.get("READING_MATH CHANGE"))
            c26 = num(r.get("Reading_Mathematics Change"))
            if c25 is None or c26 is None:
                continue
            pairs.append((dn, r["District Name"], c25, c26))
        xs = [p[2] for p in pairs]
        ys = [p[3] for p in pairs]
        rho = statistics.correlation(xs, ys) if len(pairs) > 2 else float("nan")
        big = sorted([p for p in pairs if p[2] >= 8.0], key=lambda p: -p[2])
        b = next((p for p in pairs if p[0] == BOURBON), None)
        revert[code] = {
            "n": len(pairs), "rho": rho, "big": big, "bourbon": b,
            "gain_rank": (sorted(xs, reverse=True).index(b[2]) + 1) if b else None,
            "fall_rank": (sorted(ys).index(b[3]) + 1) if b else None,
        }

    # ---------- CSV ----------
    out_csv = os.path.join(HERE, "kde_district_yoy_2025_26.csv")
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(records[0].keys()))
        w.writeheader()
        w.writerows(records)

    # ---------- summary ----------
    def stats(rows):
        d = sorted(t[4] for t in rows)
        n = len(d)
        return {
            "n": n, "min": d[0], "p10": pct(d, 10), "p25": pct(d, 25), "median": pct(d, 50),
            "p75": pct(d, 75), "p90": pct(d, 90), "max": d[-1], "mean": sum(d) / n,
            "fell": sum(1 for x in d if x < 0), "fell_share": 100.0 * sum(1 for x in d if x < 0) / n,
        }

    def bourbon(rows):
        for i, t in enumerate(rows):
            if t[0] == BOURBON:
                deltas = [x[4] for x in rows]
                below = sum(1 for x in deltas if x < t[4])
                equal = sum(1 for x in deltas if x == t[4])
                return t, i + 1, 100.0 * (below + 0.5 * equal) / len(rows)
        return None, None, None

    L = []
    L.append("# District year-over-year change, 2024-25 to 2025-26, by level\n")
    L.append("Every Kentucky district's accountability result at the elementary, middle and high school "
             "level, 2024-25 against 2025-26, from the district rows of KDE's two accountability profile "
             "files (KYRC25_ACCT_Profile.csv, KDE historical datasets; Accountable_Profile_2026.CSV, "
             "released October 14, 2026). Districts are matched on the district number. The education "
             "cooperatives and the state row are excluded from the distributions; the state's own "
             "change is shown for reference. Status is the year's own result on an indicator; the "
             "overall score is the state's published figure, which adds its change component to status. "
             "Rank 1 is the largest fall. The percentile is the share of districts at or below the "
             "district's change, so a low percentile means one of the larger falls.\n")
    if mismatches:
        L.append(f"Data check: {len(mismatches)} district rows where KDE's published change differs from "
                 "the difference of the two years' status by more than 0.15. They are listed at the end.\n")
    else:
        L.append("Data check: for every district and level, KDE's published change column equals the "
                 "difference between the two years' status to within rounding. The 2025-26 file's own "
                 "change figures and this file's differences are the same numbers.\n")

    L.append("## Bourbon County, both years\n")
    L.append("| Level | Measure | 2024-25 | 2025-26 | Change | Rank (1 = largest fall) | Percentile |")
    L.append("|---|---|---|---|---|---|---|")
    for code, lname, short in LEVELS:
        for key, label, *_ in MEASURES:
            rows = dist.get((code, key)) or []
            t, rank, pr = bourbon(rows)
            if t is None:
                continue
            L.append(f"| {short} | {label} | {t[2]:.1f} | {t[3]:.1f} | {t[4]:+.1f} | {rank} of {len(rows)} | {pr:.0f} |")
    L.append("")

    L.append("## Did 2024-25 gains revert in 2025-26? Reading and mathematics status\n")
    L.append("KDE's change figure is this year's status minus last year's. Comparing each district's "
             "2024-25 change with its 2025-26 change shows how much of a one-year gain tends to hold.\n")
    L.append("| Level | Districts | Correlation of the two years' changes | Districts gaining 8 or more in 2024-25 | Of those, fell in 2025-26 | Their median 2025-26 change | Bourbon 2024-25 change (rank among gains) | Bourbon 2025-26 change (rank among falls) |")
    L.append("|---|---|---|---|---|---|---|---|")
    for code, lname, short in LEVELS:
        v = revert[code]
        big = v["big"]
        fell = sum(1 for p in big if p[3] < 0)
        med = statistics.median([p[3] for p in big]) if big else float("nan")
        b = v["bourbon"]
        L.append(f"| {short} | {v['n']} | {v['rho']:+.2f} | {len(big)} | {fell} | {med:+.1f} | "
                 f"{b[2]:+.1f} ({v['gain_rank']} of {v['n']}) | {b[3]:+.1f} ({v['fall_rank']} of {v['n']}) |")
    L.append("")
    hs = revert["HS"]["big"]
    L.append("High school districts whose reading and mathematics status rose 8 or more points in 2024-25, "
             "and what happened in 2025-26:\n")
    for dn, name, c25, c26 in hs:
        mark = " (Bourbon County)" if dn == BOURBON else ""
        L.append(f"- {name}: {c25:+.1f} then {c26:+.1f}{mark}")
    L.append("")

    for code, lname, short in LEVELS:
        L.append(f"## {short} school level: distribution of the change across districts\n")
        L.append("| Measure | Districts | Fell | 10th pct | 25th pct | Median | 75th pct | 90th pct | State row | Bourbon | Bourbon rank | Bourbon pct |")
        L.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
        for key, label, *_ in MEASURES:
            rows = dist.get((code, key)) or []
            if not rows:
                continue
            s = stats(rows)
            t, rank, pr = bourbon(rows)
            st = state.get((code, key))
            st_s = f"{st[2]:+.1f}" if st else "n/a"
            b_s = f"{t[4]:+.1f}" if t else "n/a"
            r_s = f"{rank} of {s['n']}" if t else "n/a"
            p_s = f"{pr:.0f}" if t else "n/a"
            L.append(f"| {label} | {s['n']} | {s['fell']} ({s['fell_share']:.0f}%) | {s['p10']:+.1f} | {s['p25']:+.1f} | "
                     f"{s['median']:+.1f} | {s['p75']:+.1f} | {s['p90']:+.1f} | {st_s} | {b_s} | {r_s} | {p_s} |")
        L.append("")
        for key in ("overall", "rm_status"):
            rows = dist.get((code, key)) or []
            label = next(m[1] for m in MEASURES if m[0] == key)
            L.append(f"Largest falls, {label.lower()}, {short.lower()} level:\n")
            for dn, name, v25, v26, delta in rows[:12]:
                mark = " (Bourbon County)" if dn == BOURBON else ""
                L.append(f"- {name}: {v25:.1f} to {v26:.1f} ({delta:+.1f}){mark}")
            L.append("")

    if mismatches:
        L.append("## Rows where KDE's change column and the two-year difference disagree\n")
        for dn, name, code, key, kde, delta in mismatches:
            L.append(f"- {name} ({dn}), {code}, {key}: KDE change {kde:+.1f}, difference {delta:+.1f}")
        L.append("")

    out_md = os.path.join(HERE, "district_yoy_2025_26.md")
    open(out_md, "w", encoding="utf-8").write("\n".join(L))

    # ---------- chart ----------
    NAVY, SLATE, GRAY, INK, MUTED = "#1F3864", "#3A4356", "#8A93A6", "#1C2230", "#6B7486"
    BAR, LINE = "#B8C2D0", "#E3E8F0"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5})
    cols = [("overall", "Change in the overall score"),
            ("rm_status", "Change in reading and mathematics status")]
    fig, axes = plt.subplots(3, 2, figsize=(11.5, 9.4), sharex="col")
    for j, (key, ctitle) in enumerate(cols):
        allv = [t[4] for code, _, _ in LEVELS for t in dist[(code, key)]]
        lo = math.floor(min(allv) / 2.0) * 2 - 2
        hi = math.ceil(max(allv) / 2.0) * 2 + 2
        bins = list(range(int(lo), int(hi) + 2, 2))
        for i, (code, lname, short) in enumerate(LEVELS):
            ax = axes[i][j]
            rows = dist[(code, key)]
            vals = [t[4] for t in rows]
            s = stats(rows)
            counts, _, _ = ax.hist(vals, bins=bins, color=BAR, edgecolor="white", linewidth=1.0, zorder=2)
            ymax = max(counts) * 1.28
            ax.set_ylim(0, ymax)
            ax.set_xlim(lo, hi)
            ax.axvline(0, color=GRAY, lw=0.8, zorder=3)
            ax.axvline(s["median"], color=GRAY, lw=1.4, ls=(0, (4, 3)), zorder=4)
            t, rank, pr = bourbon(rows)
            med_right = not (t and t[4] > s["median"])
            ax.text(s["median"], ymax * 0.62, f" median {s['median']:+.1f} " , color=MUTED, fontsize=8.5,
                    ha="left" if med_right else "right", va="center", zorder=6)
            if t:
                b = t[4]
                ax.axvline(b, color=NAVY, lw=2.2, zorder=5)
                if b < 0:
                    what = f"{ordinal(rank)} largest fall of {s['n']} districts"
                else:
                    what = f"{ordinal(s['n'] - rank + 1)} largest gain of {s['n']} districts"
                label = f"Bourbon County {b:+.1f}\n{what}"
                left_side = b < (lo + hi) / 2.0
                ax.annotate(label, xy=(b, ymax * 0.80),
                            xytext=(0.985, 0.95) if left_side else (0.015, 0.95),
                            textcoords="axes fraction", ha="right" if left_side else "left", va="top",
                            color=NAVY, fontsize=9, fontweight="bold", zorder=7,
                            arrowprops=dict(arrowstyle="-", color=NAVY, lw=0.9, shrinkA=0, shrinkB=2))
            ax.text(0.015 if (t and t[4] < (lo + hi) / 2.0) else 0.985, 0.95,
                    f"{s['fell_share']:.0f}% of districts fell", transform=ax.transAxes,
                    ha="left" if (t and t[4] < (lo + hi) / 2.0) else "right", va="top",
                    color=MUTED, fontsize=8.5, zorder=6)
            for sp in ("top", "right"):
                ax.spines[sp].set_visible(False)
            for sp in ("left", "bottom"):
                ax.spines[sp].set_color(LINE)
            ax.tick_params(colors=MUTED, labelsize=8.5, length=0)
            ax.yaxis.grid(True, color=LINE, lw=0.8, zorder=0)
            ax.set_axisbelow(True)
            if j == 0:
                ax.set_ylabel(f"{short} level\n{s['n']} districts", color=INK, fontsize=10, labelpad=10)
            if i == 0:
                ax.set_title(ctitle, color=INK, fontsize=11, loc="left", pad=8)
            if i == 2:
                ax.set_xlabel("Points, 2025-26 minus 2024-25", color=MUTED, fontsize=9)
            ax.set_xticks(range(int(math.ceil(lo / 10.0)) * 10, int(hi) + 1, 10))
    fig.suptitle("Year over year, 2024-25 to 2025-26: every Kentucky district's change by level, Bourbon County marked",
                 x=0.045, ha="left", fontsize=12.5, color=INK, fontweight="bold", y=0.985)
    fig.text(0.045, 0.012,
             "Source: KDE accountability profiles, district rows (KYRC25_ACCT_Profile.csv; Accountable_Profile_2026.CSV, "
             "October 14, 2026). Status is the year's own result; the overall score adds the state's change component. "
             "Bars count districts in two-point bins; the cooperatives and the state row are excluded.",
             fontsize=7.8, color=MUTED, ha="left", va="bottom", wrap=True)
    fig.subplots_adjust(left=0.085, right=0.985, top=0.915, bottom=0.095, hspace=0.32, wspace=0.14)
    out_png = os.path.join(HERE, "district_yoy_2025_26_chart.png")
    fig.savefig(out_png, dpi=200)
    print("wrote", out_csv, out_md, out_png, f"({len(records)} rows; {len(mismatches)} change mismatches)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
