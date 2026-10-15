#!/usr/bin/env python3
"""Full historical trend of the official KDE scores for the four county elementaries, 2012 to 2026."""
import json, math, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

BUILD, OUT = sys.argv[1], sys.argv[2]
hist = json.load(open(f"{BUILD}/kde_scores_history.json"))
subj = json.load(open(f"{BUILD}/kde_subjects_history.json"))
k26 = json.load(open(f"{BUILD}/kde_ksa_2025_26.json"))
NAME = {"NMES": "North Middletown Elementary School", "BC": "Bourbon Central Elementary School",
        "CR": "Cane Ridge Elementary School", "PE": "Paris Elementary School"}
SER = [("NMES", "North Middletown", "#1F3864", 3.0, "-"), ("BC", "Bourbon Central", "#2E75B6", 2.0, "-"),
       ("CR", "Cane Ridge", "#8A93A6", 2.0, "-"), ("PE", "Paris Elementary", "#AEB4BE", 1.8, (0, (5, 3)))]
NAVY, SLATE, MIST, LINE = "#1F3864", "#3A4356", "#8A93A6", "#E3E8F0"
years = list(range(2012, 2027))
key = lambda y: f"{y-1}-{str(y)[2:]}"
def f(x):
    try: return float(x)
    except (TypeError, ValueError): return None
nan = float("nan")

def series_rm(k):
    out = []
    for y in years:
        if y == 2026:
            r, m = f(k26["schools"][NAME[k]]["Reading"]["PD"]), f(k26["schools"][NAME[k]]["Mathematics"]["PD"])
            out.append((r + m) / 2 if r is not None and m is not None else nan); continue
        r = hist["reading_pd"].get(key(y), {}).get(k); m = hist["math_pd"].get(key(y), {}).get(k)
        out.append((r + m) / 2 if r is not None and m is not None else nan)
    return out
def series_oth(k):
    out = []
    for y in years:
        if y == 2026:
            vals = [f(k26["schools"][NAME[k]][s]["PD"]) for s in ("Science", "Social Studies", "Combined Writing")]
            vals = [v for v in vals if v is not None]
            out.append(sum(vals) / len(vals) if vals else nan); continue
        v = subj["avg"].get(key(y), {}).get(k)
        out.append(v if v is not None else nan)
    return out
def series_comp(k):
    out = []
    for y in years:
        if y == 2026:
            out.append(f(k26["profile"][NAME[k]]["overall_combined_indicator_rate"])); continue
        v = hist["official_composite"].get(key(y), {}).get(k)
        out.append(v[0] if v else nan)
    return out

PANELS = [
    ("Reading and mathematics", "Percent proficient or distinguished, the two subjects averaged. All tested grades, all students.", series_rm, (0, 85)),
    ("Science, social studies and writing", "Percent proficient or distinguished, averaged over the subjects the state published for that school and year.\nNo NMES point for 2026: all three subjects were suppressed. The state began publishing these for every school in 2018.", series_oth, (0, 85)),
    ("The state's official overall score", "Two systems: Unbridled Learning (2012 to 2016) and the current score (2022 to 2026), which adds a change-from-last-year piece to the year's status.\nShaded bands are the current elementary rating cut scores: red below 38, orange to 54.9, yellow to 69.9, green to 82.9, blue above. 2017 issued no score by design.", series_comp, (0, 100)),
]
fig = plt.figure(figsize=(10, 12.4), dpi=160, facecolor="white")
fig.text(0.05, 0.975, "Bourbon County elementary schools on the state tests, 2012 to 2026", fontsize=17, color=NAVY, weight="bold", va="top")
fig.text(0.05, 0.950, "Kentucky Department of Education files, archived in the SaveNMES repository. Years are the spring of the school year (2026 is 2025-26).\nNo state tests were given in 2020; 2021 was a limited COVID administration.", fontsize=10, color=SLATE, va="top", linespacing=1.45)
tops = [0.862, 0.580, 0.298]; h = 0.200
for (title, sub, fn, ylim), top in zip(PANELS, tops):
    ax = fig.add_axes([0.07, top - h, 0.80, h])
    fig.text(0.07, top + 0.036, title, fontsize=12.5, color=NAVY, weight="bold", va="bottom")
    fig.text(0.07, top + 0.031, sub, fontsize=8.4, color=MIST, va="top", linespacing=1.4)
    ax.axvspan(2019.5, 2020.5, color=LINE, alpha=0.6, lw=0, zorder=0)
    ax.text(2020, ylim[1] * 0.97, "no tests\n2020", ha="center", va="top", fontsize=8, color=MIST, linespacing=1.2)
    if fn is series_comp:
        for lo, hi, col, lab in [(0, 38, "#C2452D", "red"), (38, 55, "#E8A33D", "orange"), (55, 70, "#E9D24C", "yellow"), (70, 83, "#1E9B7B", "green"), (83, 100, "#3D5FC4", "blue")]:
            ax.axhspan(lo, hi, xmin=(2021.5 - 2011.3) / (2026.9 - 2011.3), xmax=1, color=col, alpha=0.09, lw=0, zorder=0)
    ends = []
    for k, lab, col, lw, ls in SER:
        ys = fn(k)
        ax.plot(years, ys, color=col, lw=lw, ls=ls, solid_joinstyle="round", solid_capstyle="round", zorder=3)
        ax.plot(years, ys, ls="none", marker="o", ms=5.2, mfc=col, mec="white", mew=1.4, zorder=4)
        last = max((i for i, v in enumerate(ys) if not math.isnan(v)), default=None)
        if last is not None:
            ends.append([years[last], ys[last], lab, col, ys[last]])
    # direct end labels, nudged apart
    ends.sort(key=lambda e: e[1])
    minsep = (ylim[1] - ylim[0]) * 0.065
    for i in range(1, len(ends)):
        if ends[i][4] - ends[i - 1][4] < minsep:
            ends[i][4] = ends[i - 1][4] + minsep
    for x, y, lab, col, ly in ends:
        xt = 2026.25 if x == 2026 else x + 0.25
        ax.annotate(f"{lab} {y:.1f}", xy=(x, y), xytext=(xt, ly), fontsize=8.6, color=SLATE, va="center", ha="left",
                    arrowprops=dict(arrowstyle="-", color=LINE, lw=0.8, shrinkA=0, shrinkB=3) if abs(ly - y) > 0.01 else None, zorder=5)
    ax.set_xlim(2011.3, 2026.9); ax.set_ylim(*ylim)
    ax.set_xticks(years); ax.set_xticklabels([str(y) for y in years], fontsize=8.5, color=MIST)
    ax.tick_params(axis="y", labelsize=8.5, colors=MIST, length=0); ax.tick_params(axis="x", length=0)
    ax.grid(axis="y", color=LINE, lw=1, zorder=0); ax.set_axisbelow(True)
    for sp in ["top", "right", "left"]: ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(LINE)
handles = [Line2D([0], [0], color=c, lw=lw, ls=ls, label=l) for _, l, c, lw, ls in SER]
fig.legend(handles=handles, loc="lower left", bbox_to_anchor=(0.05, 0.030), ncol=4, frameon=False, fontsize=9.5, handlelength=2.6, columnspacing=1.6, labelcolor=SLATE)
fig.text(0.05, 0.008, "Sources: KDE ACCOUNTABILITY_PROFILE and ACHIEVEMENT_LEVEL files 2012 to 2017, ACCOUNTABILITY_PROFICIENCY_LEVEL 2018 to 2019 (Wayback Machine), assessment files 2021 to 2025, and the October 14, 2026 release for 2025-26. 2017 issued no overall score by design. savenmes.org",
         fontsize=7.6, color=MIST, va="bottom", wrap=True)
fig.savefig(OUT, dpi=160, facecolor="white"); print("wrote", OUT)
