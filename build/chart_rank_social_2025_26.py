#!/usr/bin/env python3
"""Social media figure: where Bourbon County ranks among Kentucky's districts, 2025-26, by level.

Reads build/kde_district_status_2025_26.csv (written by build/district_status_2025_26.py)
and draws one square image with three rank tracks: elementary, middle and high school
reading and mathematics status, the year's own result before the state's change formula.

Usage: python3 build/chart_rank_social_2025_26.py
Writes: build/bourbon_rank_social_2025_26.png (1200 x 1200)
"""
import csv
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "kde_district_status_2025_26.csv")
OUT = os.path.join(HERE, "bourbon_rank_social_2025_26.png")

NAVY, ROYAL, INK, MUTED, TRACK, LINE = "#1F3864", "#2E75B6", "#1C2230", "#6B7486", "#D9DFE8", "#E3E8F0"
LEVELS = [("ES", "Elementary"), ("MS", "Middle school"), ("HS", "High school")]


def ordinal(n):
    if 10 <= n % 100 <= 20:
        suf = "th"
    else:
        suf = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suf}"


def main():
    rows = {}
    with open(SRC, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["district_number"] == "041" and r["measure"] == "rm" and r["year"] == "2025-26":
                rows[r["level"]] = r
    assert all(code in rows for code, _ in LEVELS), "Bourbon County rows missing"

    plt.rcParams.update({"font.family": "DejaVu Sans"})
    fig = plt.figure(figsize=(6, 6), dpi=200)
    fig.patch.set_facecolor("white")
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Title block
    ax.text(5, 94.5, "Where Bourbon County Schools rank", fontsize=16.5, fontweight="bold", color=NAVY, va="top")
    ax.text(5, 88.5, "among Kentucky's school districts", fontsize=16.5, fontweight="bold", color=NAVY, va="top")
    ax.text(5, 81.5, "2025-26 state tests, reading and mathematics. Status is the year's own result,\n"
                     "before the state's change formula. All students, every district in Kentucky.",
            fontsize=8.2, color=MUTED, va="top", linespacing=1.45)

    # Tracks
    x0, x1 = 24.0, 56.0
    ys = [66.0, 52.0, 38.0]
    for (code, label), y in zip(LEVELS, ys):
        r = rows[code]
        rank, n, pr = int(r["rank_from_top"]), int(r["districts"]), float(r["percentile"])
        x = x0 + (x1 - x0) * pr / 100.0
        ax.plot([x0, x1], [y, y], color=TRACK, lw=7, solid_capstyle="round", zorder=1)
        ax.plot([(x0 + x1) / 2] * 2, [y - 2.2, y + 2.2], color=MUTED, lw=0.9, zorder=2)
        ax.scatter([x], [y], s=240, color=NAVY, edgecolor="white", linewidth=2, zorder=3)
        ax.text(x0 - 2.5, y, label, fontsize=11.5, color=INK, ha="right", va="center")
        ax.text(x1 + 3.0, y + 2.0, f"{ordinal(rank)} of {n} districts", fontsize=12, fontweight="bold",
                color=NAVY, ha="left", va="center")
        ax.text(x1 + 3.0, y - 2.4, f"bottom {pr:.0f} percent; state rating \"{r['state_rating']}\"",
                fontsize=7.4, color=MUTED, ha="left", va="center")
    ax.text(x0, ys[-1] - 5.2, "lowest", fontsize=7.2, color=MUTED, ha="left", va="top")
    ax.text((x0 + x1) / 2, ys[-1] - 5.2, "state median", fontsize=7.2, color=MUTED, ha="center", va="top")
    ax.text(x1, ys[-1] - 5.2, "highest", fontsize=7.2, color=MUTED, ha="right", va="top")

    # Takeaway
    ax.plot([5, 95], [26.0, 26.0], color=LINE, lw=0.8)
    ax.text(5, 23.0, "This is not one school's bad year.", fontsize=11, fontweight="bold", color=INK, va="top")
    ax.text(5, 18.3, "Elementary and middle school were already in the bottom 15 percent of districts\n"
                     "last year. The high school stood at the 42nd percentile last year and fell to the 9th.\n"
                     "Every level is rated \"low\" by the state on its own scale.",
            fontsize=8.2, color=INK, va="top", linespacing=1.5)
    ax.text(5, 2.6, "Source: Kentucky Department of Education, Accountable Profile 2025-2026 (released Oct. 14, 2026),\n"
                    "district rows, all students; the prior year from the 2024-25 School Report Card profile.\n"
                    "Rank 1 is the highest status in the state. Full tables and code: SaveNMES.org",
            fontsize=6.3, color=MUTED, va="bottom", linespacing=1.45)
    fig.savefig(OUT, dpi=200, facecolor="white")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
