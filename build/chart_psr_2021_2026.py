#!/usr/bin/env python3
"""Postsecondary readiness, Bourbon County High against Kentucky, 2021-22 to 2025-26.

Reads KDE's postsecondary readiness files for the five years of the current system
(district and state rows, all students) and writes a two-panel chart and a note:
the share of seniors meeting a readiness measure, and the indicator status the
state scores, which counts a senior holding an industry credential in a high-demand
sector as 1.25 instead of 1 (703 KAR 5:270, Section 4). Ranks are among Kentucky
districts, 1 = highest.

Usage (five readiness files, then the five accountability profile files for the same years, which
supply the official status used for the ranks):
  python3 -I build/chart_psr_2021_2026.py postsecondary_readiness_2022.csv postsecondary_readiness_2023.csv \
      KYRC24_ACCT_Postsecondary_Readiness.csv KYRC25_ACCT_Postsecondary_Readiness.csv Postsecondary_Readiness_2026.CSV \
      accountability_profile_2022.csv accountability_profile_2023.csv KYRC24_ACCT_Profile.csv KYRC25_ACCT_Profile.csv \
      Accountable_Profile_2026.CSV
Writes: build/psr_2021_2026_chart.png, build/psr_2021_2026.md, build/kde_psr_2021_2026.csv
"""
import csv
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
YEARS = ["2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]
BOURBON, STATE = "041", "999"


def up(r):
    return {k.strip().upper(): v for k, v in r.items() if k}


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


def read(path):
    """-> {district_number: (rate, rate_with_bonus)} for district and state totals, all students."""
    out = {}
    with open(path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            r = up(r)
            if (r.get("DEMOGRAPHIC") or "").strip() != "All Students":
                continue
            if "SCHOOL CODE" in r and "DISTRICT NUMBER" not in r:          # 2025-26 layout
                if r["SCHOOL NAME"].strip() != "":
                    continue
                dn = r["SCHOOL CODE"].strip()
            else:
                sn = r["SCHOOL NAME"].strip()
                if sn not in ("---District Total---", "---State Total---", "All Schools"):
                    continue
                if sn == "All Schools" and r.get("SCHOOL TYPE", "").strip() != "":
                    continue
                dn = r["DISTRICT NUMBER"].strip()
            rate, bonus = num(r.get("POSTSECONDARY RATE")), num(r.get("POSTSECONDARY RATE WITH BONUS"))
            if rate is None and bonus is None:
                continue
            out[dn] = (rate, bonus)
    return out


def read_profile_status(path):
    """-> {district_number: postsecondary status} for high school district rows in a profile file."""
    out = {}
    with open(path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            r = up(r)
            if "SCHOOL CODE" in r and "DISTRICT NUMBER" not in r:
                if r["SCHOOL NAME"].strip() != "" or r["LEVEL"].strip() != "HS":
                    continue
                dn = r["SCHOOL CODE"].strip()
            else:
                sn = r["SCHOOL NAME"].strip()
                if sn not in ("---District Total---", "---State Total---", "All Schools"):
                    continue
                if sn == "All Schools" and r.get("SCHOOL TYPE", "").strip() != "":
                    continue
                if r["LEVEL"].strip() not in ("HS", "High School"):
                    continue
                dn = r["DISTRICT NUMBER"].strip()
            col = next((c for c in r if c.startswith("POSTSECONDARY") and ("STATUS" in c or "INDICATOR RATE" in c)
                        and "RATING" not in c and "CHANGE" not in c and "COMBINED" not in c), None)
            v = num(r.get(col)) if col else None
            if v is not None:
                out[dn] = v
    return out


def main(paths):
    series = {}
    recs = []
    profiles = paths[5:10]
    for year, p, pp in zip(YEARS, paths[:5], profiles):
        d = read(p)
        official = read_profile_status(pp)

        def place(pairs, dn):
            """pairs: list of (value, district). -> rank from the top, n, percentile (share at or below)."""
            pairs = [(v, k) for v, k in pairs if v is not None]
            mine = next((v for v, k in pairs if k == dn), None)
            n = len(pairs)
            if mine is None or n == 0:
                return None, n, None
            vals = [v for v, _ in pairs]
            below = sum(1 for x in vals if x < mine)
            equal = sum(1 for x in vals if x == mine)
            return sorted(vals, reverse=True).index(mine) + 1, n, 100.0 * (below + 0.5 * equal) / n

        districts = [(v, dn) for dn, v in official.items() if dn.isdigit() and int(dn) < 900]
        rank, n, pct = place(districts, BOURBON)
        rate_pairs = [(v[0], dn) for dn, v in d.items() if dn.isdigit() and int(dn) < 900]
        rate_rank, rate_n, rate_pct = place(rate_pairs, BOURBON)
        vals = sorted(v for v, _ in districts)
        median = vals[n // 2] if n % 2 else (vals[n // 2 - 1] + vals[n // 2]) / 2
        b, s = d.get(BOURBON, (None, None)), d.get(STATE, (None, None))
        series[year] = {"b_rate": b[0], "b_bonus": b[1], "s_rate": s[0], "s_bonus": s[1],
                        "rank": rank, "n": n, "pct": pct, "rate_rank": rate_rank, "rate_n": rate_n,
                        "rate_pct": rate_pct, "median": median}
        for who, dn, t in (("Bourbon County", BOURBON, b), ("Kentucky", STATE, s)):
            mine = dn == BOURBON
            recs.append({"year": year, "district": who, "postsecondary_rate": t[0], "rate_with_bonus": t[1],
                         "status_rank_from_top": rank if mine else "", "status_districts": n if mine else "",
                         "status_percentile": round(pct, 1) if mine and pct is not None else "",
                         "rate_rank_from_top": rate_rank if mine else "", "rate_districts": rate_n if mine else "",
                         "rate_percentile": round(rate_pct, 1) if mine and rate_pct is not None else "",
                         "district_median_with_bonus": round(median, 1)})

    out_csv = os.path.join(HERE, "kde_psr_2021_2026.csv")
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(recs[0].keys()))
        w.writeheader()
        w.writerows(recs)

    L = ["# Postsecondary readiness, Bourbon County High against Kentucky, 2021-22 to 2025-26\n",
         "From KDE's postsecondary readiness files, district and state rows, all students. The postsecondary "
         "rate is the share of seniors (graduates and grade 12 non-graduates) who met at least one academic or "
         "career readiness measure. The rate with bonus is the indicator status the state scores: a senior who "
         "holds an industry certification, licensure or credential in a state or regional high-demand sector counts "
         "as 1.25 points instead of 1 (703 KAR 5:270, Section 4), so the status can exceed 100. Bourbon County "
         "has one high school, so its district row is Bourbon County High School. Rank is among Kentucky "
         "districts with a high school result, 1 = highest.\n",
         "| Year | Bourbon rate | Rate rank (percentile) | Bourbon status (with bonus) | Status rank (percentile) | District median status | Kentucky rate | Kentucky status |",
         "|---|---|---|---|---|---|---|---|"]
    for y in YEARS:
        v = series[y]
        L.append(f"| {y} | {v['b_rate']:.1f} | {v['rate_rank']} of {v['rate_n']} ({ordinal(int(round(v['rate_pct'])))} pct) | {v['b_bonus']:.1f} | "
                 f"{v['rank']} of {v['n']} ({ordinal(int(round(v['pct'])))} pct) | {v['median']:.1f} | {v['s_rate']:.1f} | {v['s_bonus']:.1f} |")
    L.append("")
    L.append("Implied share of seniors holding a high-demand industry credential, a quarter point each "
             "(status minus rate, times four): "
             + "; ".join(f"{y} Bourbon {4 * (series[y]['b_bonus'] - series[y]['b_rate']):.0f} percent, Kentucky "
                         f"{4 * (series[y]['s_bonus'] - series[y]['s_rate']):.0f} percent" for y in YEARS) + ".\n")
    open(os.path.join(HERE, "psr_2021_2026.md"), "w", encoding="utf-8").write("\n".join(L))

    # chart
    NAVY, GRAY, INK, MUTED, LINE = "#1F3864", "#8A93A6", "#1C2230", "#6B7486", "#E3E8F0"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5})
    box = dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85)
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.9), sharey=True)
    panels = [("rate", "Share of seniors meeting at least one readiness measure"),
              ("bonus", "Readiness status as scored, with the high-demand credential bonus")]
    xs = list(range(len(YEARS)))
    for ax, (key, title) in zip(axes, panels):
        for who, pref, color, ls, mk, z in (("Kentucky", "s_", GRAY, (0, (4, 3)), "s", 2),
                                             ("Bourbon County", "b_", NAVY, "-", "o", 3)):
            ys = [series[y][pref + key] for y in YEARS]
            ax.plot(xs, ys, color=color, lw=2.2, ls=ls, marker=mk, ms=7, markeredgecolor="white",
                    markeredgewidth=1.2, zorder=z, label=who)
            for x, v in zip(xs, ys):
                other = series[YEARS[x]][("s_" if pref == "b_" else "b_") + key]
                dy = 1.8 if v >= other else -1.8
                xt, ha = (x - 0.25, "left") if x == 0 else (x, "center")
                ax.text(xt, v + dy, f"{v:.1f}", ha=ha, va="bottom" if dy > 0 else "top",
                        color=NAVY if who == "Bourbon County" else MUTED, fontsize=8.4,
                        fontweight="bold" if who == "Bourbon County" else "normal", zorder=6, bbox=box)
        rk_key, n_key, pct_key = ("rank", "n", "pct") if key == "bonus" else ("rate_rank", "rate_n", "rate_pct")
        for x, y in enumerate(YEARS):
            v = series[y]
            if v[rk_key]:
                ax.text(x, 52.5, f"{ordinal(v[rk_key])} of {v[n_key]}\n{ordinal(int(round(v[pct_key])))} pct", ha="center",
                        va="bottom", color=MUTED, fontsize=7.4, linespacing=1.3, zorder=6)
        ax.set_xlim(-0.45, len(YEARS) - 1 + 0.6)
        ax.set_ylim(51, 102)
        ax.set_xticks(xs)
        ax.set_xticklabels(YEARS, fontsize=8.6)
        ax.set_title(title, color=INK, fontsize=10.5, loc="left", pad=8)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        for sp in ("left", "bottom"):
            ax.spines[sp].set_color(LINE)
        ax.tick_params(colors=MUTED, labelsize=8.6, length=0)
        ax.yaxis.grid(True, color=LINE, lw=0.8)
        ax.set_axisbelow(True)
    axes[0].set_ylabel("Percent of seniors (status can exceed 100)", color=INK, fontsize=9.5, labelpad=8)
    h, lab = axes[0].get_legend_handles_labels()
    order = [lab.index("Bourbon County"), lab.index("Kentucky")]
    fig.legend([h[k] for k in order], [lab[k] for k in order], loc="upper right", bbox_to_anchor=(0.985, 0.925),
               ncol=2, frameon=False, fontsize=9.5)
    fig.suptitle("Postsecondary readiness, Bourbon County High against Kentucky, 2021-22 to 2025-26",
                 x=0.04, ha="left", fontsize=12.2, color=INK, fontweight="bold", y=0.985)
    fig.text(0.04, 0.015,
             "Source: KDE postsecondary readiness files, district and state rows, all students (postsecondary_readiness_2022 and 2023; "
             "KYRC24 and KYRC25; Postsecondary_Readiness_2026, October 14, 2026). Seniors count as ready by meeting one academic measure "
             "(CPE exam benchmark, dual credit, AP, IB or Cambridge) or one career measure (industry certification, CTE end-of-program "
             "assessment, CTE dual credit, apprenticeship, co-op or internship); a credential in a high-demand sector counts 1.25. The gray "
             "row under each panel is Bourbon's rank among Kentucky districts that year and its percentile, the share of districts at or below it.",
             fontsize=7.3, color=MUTED, ha="left", va="bottom", wrap=True)
    fig.subplots_adjust(left=0.06, right=0.985, top=0.80, bottom=0.2, wspace=0.12)
    out_png = os.path.join(HERE, "psr_2021_2026_chart.png")
    fig.savefig(out_png, dpi=200)
    print("wrote", out_png)
    for y in YEARS:
        print(y, series[y])


if __name__ == "__main__":
    if len(sys.argv) != 11:
        sys.exit(__doc__)
    main(sys.argv[1:])
