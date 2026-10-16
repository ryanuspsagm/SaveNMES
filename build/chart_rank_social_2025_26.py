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

NAVY, INK, MUTED, TRACK = "#1F3864", "#1C2230", "#6B7486", "#D9DFE8"
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

    ax.text(5, 92.0, "Where Bourbon County Schools rank", fontsize=16.5, fontweight="bold", color=NAVY, va="top")
    ax.text(5, 86.0, "among Kentucky's school districts", fontsize=16.5, fontweight="bold", color=NAVY, va="top")
    ax.text(5, 78.5, "2025-26 state tests, reading and mathematics. All students, every district in Kentucky.",
            fontsize=8.4, color=MUTED, va="top")

    x0, x1 = 24.0, 56.0
    ys = [62.0, 45.0, 28.0]
    for (code, label), y in zip(LEVELS, ys):
        r = rows[code]
        rank, n, pr = int(r["rank_from_top"]), int(r["districts"]), float(r["percentile"])
        x = x0 + (x1 - x0) * pr / 100.0
        ax.plot([x0, x1], [y, y], color=TRACK, lw=8, solid_capstyle="round", zorder=1)
        ax.plot([(x0 + x1) / 2] * 2, [y - 2.4, y + 2.4], color=MUTED, lw=0.9, zorder=2)
        ax.scatter([x], [y], s=300, color=NAVY, edgecolor="white", linewidth=2, zorder=3)
        ax.text(x0 - 2.5, y, label, fontsize=12, color=INK, ha="right", va="center")
        ax.text(x1 + 3.0, y + 2.2, f"{ordinal(rank)} of {n} districts", fontsize=12.5, fontweight="bold",
                color=NAVY, ha="left", va="center")
        ax.text(x1 + 3.0, y - 2.6, f"bottom {pr:.0f} percent", fontsize=9, color=MUTED, ha="left", va="center")
    ax.text(x0, ys[-1] - 5.6, "lowest", fontsize=7.4, color=MUTED, ha="left", va="top")
    ax.text((x0 + x1) / 2, ys[-1] - 5.6, "state median", fontsize=7.4, color=MUTED, ha="center", va="top")
    ax.text(x1, ys[-1] - 5.6, "highest", fontsize=7.4, color=MUTED, ha="right", va="top")

    ax.text(5, 4.5, "Source: Kentucky Department of Education, Accountable Profile 2025-2026, district rows.  SaveNMES.org",
            fontsize=6.4, color=MUTED, va="bottom")
    fig.savefig(OUT, dpi=200, facecolor="white")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
