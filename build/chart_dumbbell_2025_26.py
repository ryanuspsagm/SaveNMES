#!/usr/bin/env python3
"""Before-and-after chart: each district elementary's KDE content index by subject,
2024-25 (hollow) to 2025-26 (solid), with the Kentucky average marked.

    python build/chart_dumbbell_2025_26.py build build/ksa_2025_26_change_chart.png
"""
import json, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

BUILD, OUT = sys.argv[1], sys.argv[2]
k26 = json.load(open(f"{BUILD}/kde_ksa_2025_26.json")); k25 = json.load(open(f"{BUILD}/kde_ksa_2024_25.json"))
SUBJ = ["Reading", "Mathematics", "Science", "Social Studies", "Combined Writing"]
SHOW = {"Combined Writing": "Writing"}
SCH = [("North Middletown Elementary School", "North Middletown", "#1F3864"),
       ("Bourbon Central Elementary School", "Bourbon Central", "#2E75B6"),
       ("Cane Ridge Elementary School", "Cane Ridge", "#8A93A6")]
NAVY, SLATE, MIST, LINE = "#1F3864", "#3A4356", "#8A93A6", "#E3E8F0"
ci = lambda k, name, s: float(k["schools"][name][s]["CI"])
ky = lambda s: float(k26["state_elementary"][s]["CI"])

fig = plt.figure(figsize=(10, 8.4), dpi=160, facecolor="white")
ax = fig.add_axes([0.19, 0.16, 0.77, 0.62]); ax.set_facecolor("white")
n = len(SCH); rh = 0.26; group = 1.0
for gi, s in enumerate(SUBJ):
    base = -gi * group
    for si, (name, lab, col) in enumerate(SCH):
        y = base + (n - 1) / 2 * rh - si * rh
        a, b = ci(k25, name, s), ci(k26, name, s)
        ax.plot([a, b], [y, y], color=col, lw=2.2, solid_capstyle="round", zorder=2, alpha=0.9)
        ax.plot([a], [y], marker="o", ms=7.5, mfc="white", mec=col, mew=1.8, ls="none", zorder=3)
        ax.plot([b], [y], marker="o", ms=8.5, mfc=col, mec="white", mew=1.4, ls="none", zorder=4)
        d = b - a
        txt = f"{b:.1f}  ({d:+.1f})"
        lx = max(a, b) + 2.2
        width = 1.05 * len(txt)          # roughly one index unit per character at this size
        kv = ky(s)
        if lx - 1.5 <= kv <= lx + width + 1.0:
            lx = kv + 2.0                 # step past the Kentucky tick instead of printing through it
        ax.text(lx, y, txt, va="center", ha="left", fontsize=9, color=SLATE, zorder=5,
                weight="bold" if abs(d) >= 15 else "normal")
    v = ky(s)
    top = base + (n - 1) / 2 * rh + rh / 2; bot = base - (n - 1) / 2 * rh - rh / 2
    ax.plot([v, v], [bot, top], color=SLATE, lw=2.2, zorder=1)
ax.set_xlim(0, 125); ax.set_ylim(-(len(SUBJ) - 1) * group - 0.55, 0.55)
ax.set_yticks([-gi * group for gi in range(len(SUBJ))])
ax.set_yticklabels([f"{SHOW.get(s, s)}\nKY avg {ky(s):.1f}" for s in SUBJ], fontsize=11, color=SLATE)
for lbl in ax.get_yticklabels(): lbl.set_linespacing(1.4)
ax.set_xticks([0, 25, 50, 75, 100, 125]); ax.tick_params(axis="x", labelsize=9.5, colors=MIST, length=0); ax.tick_params(axis="y", length=0)
ax.grid(axis="x", color=LINE, lw=1, zorder=0); ax.set_axisbelow(True)
for sp in ["top", "right", "left"]: ax.spines[sp].set_visible(False)
ax.spines["bottom"].set_color(LINE)
ax.set_xlabel("KDE content index: novice 0, apprentice 50, proficient 100, distinguished 125", fontsize=9.5, color=MIST, labelpad=8)
# callout on the two largest drops
ax.annotate("The two largest drops anywhere in the county,\nboth in subjects tested in a single grade (5th)",
            xy=(ci(k26, SCH[0][0], "Combined Writing"), -4 + rh), xytext=(74, -3.40),
            fontsize=9, color=NAVY, ha="left", va="center")
fig.text(0.04, 0.955, "Bourbon County elementary schools: last year to this year, subject by subject", fontsize=16, color=NAVY, weight="bold", ha="left", va="top")
fig.text(0.04, 0.905, "KDE content index, the status score the state's ratings are built from. Hollow dot: 2024-25. Solid dot: 2025-26.\n"
         "The label is this year's score and the change from last year. No change penalty is included: this is where each\nschool stands, and how far it moved.", fontsize=10, color=SLATE, ha="left", va="top", linespacing=1.45)
handles = [Line2D([0], [0], marker="o", ms=8, mfc=c, mec="white", ls="none", label=l) for _, l, c in SCH]
handles += [Line2D([0], [0], marker="o", ms=7.5, mfc="white", mec=SLATE, mew=1.6, ls="none", label="2024-25"),
            Line2D([0], [0], marker="o", ms=8, mfc=SLATE, mec="white", ls="none", label="2025-26"),
            Line2D([0], [0], color=SLATE, lw=2.2, label="Kentucky elementary average, 2025-26")]
fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.035, 0.825), ncol=6, frameon=False, fontsize=9.3, handletextpad=0.4, columnspacing=1.2, labelcolor=SLATE)
fig.text(0.04, 0.022, "Source: Kentucky Department of Education, Assessment and Accountability Data 2024-25 and 2025-26 (released Oct. 14, 2026), all students,\n"
         "elementary level. KDE withheld NMES's proficiency percentages in science, social studies and writing this year (small classes) but publishes\n"
         "the index for every subject.  savenmes.org",
         fontsize=8.2, color=MIST, ha="left", va="bottom", linespacing=1.45)
fig.savefig(OUT, dpi=160, facecolor="white"); print("wrote", OUT)
