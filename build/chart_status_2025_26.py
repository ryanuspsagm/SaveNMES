#!/usr/bin/env python3
"""Draw the 2025-26 status chart (content index by subject) as a PNG for social media."""
import json, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.lines import Line2D

BUILD, OUT = sys.argv[1], sys.argv[2]
k = json.load(open(f"{BUILD}/kde_ksa_2025_26.json"))
SUBJ = ["Reading", "Mathematics", "Science", "Social Studies", "Combined Writing"]
LABEL = {"Combined Writing": "Writing"}
SCH = [("North Middletown Elementary School", "North Middletown", "#1F3864"),
       ("Bourbon Central Elementary School", "Bourbon Central", "#2E75B6"),
       ("Cane Ridge Elementary School", "Cane Ridge", "#8A93A6")]
NAVY, SLATE, MIST, LINE = "#1F3864", "#3A4356", "#8A93A6", "#E3E8F0"
ci = lambda name, s: float(k["schools"][name][s]["CI"])
ky = lambda s: float(k["state_elementary"][s]["CI"])
sup = lambda name, s: k["schools"][name][s]["suppressed"] == "Y"

fig = plt.figure(figsize=(10, 7.5), dpi=160, facecolor="white")
ax = fig.add_axes([0.20, 0.17, 0.76, 0.62])
ax.set_facecolor("white")
n = len(SCH); bh = 0.2; gap = 0.03; group = 1.0
ys = []
for gi, s in enumerate(SUBJ):
    base = -gi * group
    for si, (name, lab, col) in enumerate(SCH):
        y = base + (n - 1) / 2 * (bh + gap) - si * (bh + gap)
        w = ci(name, s); kv = ky(s)
        ax.add_patch(Rectangle((0, y - bh / 2), w, bh, color=col, lw=0))
        lx = w + 1.2 if not (w - 1 <= kv <= w + 7.5) else kv + 1.6
        ax.text(lx, y, f"{w:.1f}", va="center", ha="left", fontsize=9.5, color=SLATE)
        if gi == 0: ys.append(y)
    # Kentucky elementary average: a solid tick across the group
    v = ky(s)
    top = base + (n - 1) / 2 * (bh + gap) + bh / 2 + 0.02
    bot = base - (n - 1) / 2 * (bh + gap) - bh / 2 - 0.02
    ax.plot([v, v], [bot, top], color=SLATE, lw=2.2, solid_capstyle="butt", zorder=5)
ax.set_xlim(0, 125); ax.set_ylim(-(len(SUBJ) - 1) * group - 0.5, 0.5)
ax.set_yticks([-gi * group for gi in range(len(SUBJ))])
ax.set_yticklabels([f"{LABEL.get(s, s)}\n" + r"$\mathrm{KY\ avg\ }$" + f"{ky(s):.1f}" for s in SUBJ], fontsize=11, color=SLATE)
for lbl in ax.get_yticklabels(): lbl.set_linespacing(1.4)
ax.set_xticks([0, 25, 50, 75, 100, 125]); ax.tick_params(axis="x", labelsize=9.5, colors=MIST, length=0)
ax.tick_params(axis="y", length=0)
ax.grid(axis="x", color=LINE, lw=1, zorder=0); ax.set_axisbelow(True)
for sp in ["top", "right", "left"]: ax.spines[sp].set_visible(False)
ax.spines["bottom"].set_color(LINE)
ax.set_xlabel("KDE content index (novice 0, apprentice 50, proficient 100, distinguished 125)", fontsize=9.5, color=MIST, labelpad=8)
# rounded data-ends: redraw the end caps as rounded patches in pixel-true aspect
fig.canvas.draw()
px = ax.transData.transform
xpx = px((1, 0))[0] - px((0, 0))[0]; ypx = px((0, 1))[1] - px((0, 0))[1]
r_x = 4 / xpx; r_y = 4 / ypx
for gi, s in enumerate(SUBJ):
    base = -gi * group
    for si, (name, lab, col) in enumerate(SCH):
        y = base + (n - 1) / 2 * (bh + gap) - si * (bh + gap); w = ci(name, s)
        ax.add_patch(Rectangle((w - 2 * r_x, y - bh / 2), 2 * r_x, bh, color="white", lw=0, zorder=3))
        ax.add_patch(FancyBboxPatch((w - 2 * r_x, y - bh / 2), 2 * r_x, bh, boxstyle=f"round,pad=0,rounding_size={r_x}", mutation_aspect=r_y / r_x, color=col, lw=0, zorder=4))
        ax.add_patch(Rectangle((w - 2 * r_x, y - bh / 2), r_x, bh, color=col, lw=0, zorder=4))
# titles, legend, source
fig.text(0.04, 0.945, "Bourbon County elementary schools, 2025-26 state tests", fontsize=17, color=NAVY, weight="bold", ha="left", va="top")
fig.text(0.04, 0.895, "This year's status by subject: KDE's content index, the score the state's ratings are built from.\nNo change penalty is included. Higher is better.", fontsize=11, color=SLATE, ha="left", va="top", linespacing=1.45)
handles = [Line2D([0], [0], marker="s", ms=11, mec="none", mfc=c, ls="none", label=l) for _, l, c in SCH]
handles.append(Line2D([0], [0], color=SLATE, lw=2.2, label="Kentucky elementary average"))
fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.035, 0.835), ncol=4, frameon=False, fontsize=10, handletextpad=0.5, columnspacing=1.4, labelcolor=SLATE)
fig.text(0.04, 0.025, "Source: Kentucky Department of Education, Assessment and Accountability Data 2025-2026 (released Oct. 14, 2026), all students, elementary level.\n"
         "KDE withheld NMES's proficiency percentages in science, social studies and writing (small classes) but publishes the index for every subject.  savenmes.org",
         fontsize=8.3, color=MIST, ha="left", va="bottom", linespacing=1.45)
fig.savefig(OUT, dpi=160, facecolor="white")
print("wrote", OUT)
