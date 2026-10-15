#!/usr/bin/env python3
"""One shareable image: the 2025-26 NMES result, where the fall came from, and
what the CSI label means. Numbers come from build/kde_ksa_2025_26.json,
build/kde_ksa_2024_25.json and the decomposition in build/cohort_analysis_2026.py.

    python build/chart_overall_card.py build build/ksa_2025_26_overall_card.png
"""
import json, sys, textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

BUILD, OUT = sys.argv[1], sys.argv[2]
k26 = json.load(open(f"{BUILD}/kde_ksa_2025_26.json")); k25 = json.load(open(f"{BUILD}/kde_ksa_2024_25.json"))
N = "North Middletown Elementary School"
rd26, rd25 = int(k26["schools"][N]["Reading"]["PD"]), int(k25["schools"][N]["Reading"]["PD"])
ma26, ma25 = int(k26["schools"][N]["Mathematics"]["PD"]), int(k25["schools"][N]["Mathematics"]["PD"])
official = float(k26["profile"][N]["overall_combined_indicator_rate"])
STATUS_ONLY = 39.1       # KDE 51/40/5/4 weights on status; verified in tests/verify_kde_2026.py
SWAP, ROOM = 13, 7       # reading points: cohort swap vs continuing cohorts; build/cohort_analysis_2026.py
assert rd25 - rd26 == SWAP + ROOM
NAVY, ROYAL, GRAY, SLATE, MIST, LINE, CHALK, PAPER = "#1F3864", "#2E75B6", "#8A93A6", "#3A4356", "#8A93A6", "#E3E8F0", "#FFFFFF", "#FAFBFD"
ORANGE, RED = "#E8A33D", "#C2452D"
W = 1200; DPI = 160
px = lambda pt: pt * DPI / 72          # font size in pixels
lh = lambda pt, ls=1.33: px(pt) * ls   # line height in pixels, with margin over the drawn 1.25 spacing
cw = lambda pt: px(pt) * 0.50          # average character width (DejaVu Sans)
M = 50; PAD = 22; INNER = W - 2 * M - 2 * PAD

# ---- lay out first, draw second
items = []  # (kind, y, payload)
y = 0
# header
items.append(("rect", 0, (0, 0, W, 150, NAVY)))
items.append(("text", 38, (M, "North Middletown Elementary", 23, CHALK, "bold", "left", 1.0)))
items.append(("text", 104, (M, "The 2025-26 state scores, where the fall came from, and what the state's label means", 12.5, "#C9D4E8", "normal", "left", 1.0)))
y = 150 + 35
# tiles
tiles = [("Reading proficient", f"{rd26}%", f"was {rd25}% in 2024-25", RED),
         ("Math proficient", f"{ma26}%", f"was {ma25}% in 2024-25", RED),
         ("Status score (this year)", f"{STATUS_ONLY}", f"official score {official:.1f} after the\nstate's change penalty", ORANGE),
         ("State label", "CSI", "Comprehensive Support and\nImprovement, 1 of 53 schools", RED)]
tw, th, tg = (W - 2 * M - 3 * 17) / 4, 168, 17
for i, (lab, val, sub, col) in enumerate(tiles):
    x = M + i * (tw + tg)
    items.append(("card", y, (x, y, tw, th)))
    items.append(("rect", y, (x, y, 6, th, col)))
    items.append(("text", y + 16, (x + 20, lab, 9.4, MIST, "normal", "left", 1.0)))
    items.append(("text", y + 44, (x + 20, val, 30, NAVY, "bold", "left", 1.0)))
    items.append(("text", y + 112, (x + 20, sub, 8.8, SLATE, "normal", "left", 1.25)))
y += th + 30

# bridge chart
cy = y; label_w = 300
rows = [("2024-25 result", 0, rd25, NAVY, f"{rd25}%"),
        ("Strong 5th grade left (54%),\nweak 3rd grade arrived (18%)", rd25 - SWAP, rd25, GRAY, f"-{SWAP}"),
        ("Continuing children fell,\nnearly all of it in the 5th grade", rd26, rd25 - SWAP, GRAY, f"-{ROOM}"),
        ("2025-26 result", 0, rd26, NAVY, f"{rd26}%")]
bx0 = M + PAD + label_w; bx1 = W - M - PAD - 60; scale = (bx1 - bx0) / 50.0
xv = lambda v: bx0 + v * scale
rh, rgap = 28, 42
by0 = cy + 95; by1 = by0 + 4 * rh + 3 * rgap
foot = textwrap.fill("In math the swap explains the whole fall, and the continuing cohorts improved on net: the 4th grade rose from about 6 to 26 percent proficient.", int(INNER / cw(9.2)))
ch = (by1 + 40 + lh(9.2) * (foot.count("\n") + 1) + 18) - cy
items.append(("card", cy, (M, cy, W - 2 * M, ch)))
items.append(("text", cy + 16, (M + PAD, "Where the 20 reading points went", 15, NAVY, "bold", "left", 1.0)))
items.append(("text", cy + 54, (M + PAD, "Percent of NMES students proficient or distinguished in reading, 2024-25 to 2025-26, from the state's grade files", 9.2, MIST, "normal", "left", 1.0)))
for v in (0, 10, 20, 30, 40, 50):
    items.append(("line", by0, ((xv(v), xv(v)), (by0 - 8, by1 + 8), LINE, 1)))
    items.append(("text", by1 + 14, (xv(v), str(v), 8.5, MIST, "normal", "center", 1.0)))
for i, (lab, a, b, col, val) in enumerate(rows):
    ry = by0 + i * (rh + rgap)
    items.append(("rtext", ry + rh / 2, (bx0 - 12, lab, 9.4, SLATE, "normal", "right", 1.15)))
    items.append(("bar", ry, (xv(a), ry, xv(b) - xv(a), rh, col)))
    items.append(("ctext", ry + rh / 2, (xv(b) + 10, val, 11, NAVY if col == NAVY else SLATE, "bold", "left", 1.0)))
    if i in (1, 2):
        items.append(("line", ry, ((xv(b), xv(b)), (ry - rgap, ry), SLATE, 0.8)))
items.append(("text", by1 + 40, (M + PAD, foot, 9.2, SLATE, "normal", "left", 1.25)))
y = cy + ch + 28

# grade-by-grade findings
def bullets_card(title, entries, head_pt, body_pt, sq_col):
    global y
    cy = y; yy = cy + 52; blocks = []
    width_chars = int((INNER - 20) / cw(body_pt))
    for head, body in entries:
        wrapped = textwrap.fill(body, width_chars)
        blocks.append((yy, head, wrapped))
        yy += (lh(head_pt, 1.0) + 4 if head else 0) + lh(body_pt) * (wrapped.count("\n") + 1) + 12
    ch = yy - cy + 10
    items.append(("card", cy, (M, cy, W - 2 * M, ch)))
    items.append(("text", cy + 18, (M + PAD, title, 15, NAVY, "bold", "left", 1.0)))
    for by, head, wrapped in blocks:
        items.append(("rect", by + 6, (M + PAD, by + 6, 8, 8, sq_col)))
        if head:
            items.append(("text", by, (M + PAD + 20, head, head_pt, NAVY, "bold", "left", 1.0)))
            items.append(("text", by + lh(head_pt, 1.0) + 4, (M + PAD + 20, wrapped, body_pt, SLATE, "normal", "left", 1.25)))
        else:
            items.append(("text", by, (M + PAD + 20, wrapped, body_pt, SLATE, "normal", "left", 1.25)))
    y = cy + ch + 28
    return ch
bullets_card("What the grade-by-grade record shows", [
    ("The 5th grade is the anomaly.", "These children were the county's best 4th grade in 2025: 47% proficient in reading, 41% in math, 53% in science. A year later every 5th-grade subject fell; editing and mechanics went to 16% against 50% and 52% for the two previous 5th grades. One classroom-year, every subject: that points at the room, not the school."),
    ("The 4th grade improved.", "The cohort bracketed at 3 to 8 percent proficient in math as 3rd graders reached 26 percent as 4th graders, a larger gain than any cohort at the other county schools."),
    ("The entry grade is the slow problem.", "3rd graders have come in weaker three years running: 29, about 20, then 18 percent proficient in reading, while the district's 3rd grade rose from 30 to 38."),
    ("Children leaving does not explain it.", "The tested cohorts held between the two tests: 20, 26 and 19 children in October 2024, 19, 24 and 19 a year on. The 17 who left during 2024-25 were mostly in K, 1st and 3rd grade, before the strong 2025 tests."),
], 10.2, 8.9, ROYAL)
bullets_card("What the CSI label means, from KDE's own rules", [
    ("", "KDE audits the school and the district within 45 days, including whether the principal and the district can lead a turnaround."),
    ("", "A turnaround team writes a three-year plan, running by fall 2027. The school becomes eligible for federal school improvement money and on-site state support."),
    ("", "The school council's authority moves to the superintendent for the turnaround; an advisory team of teachers and parents takes its voice."),
    ("", "A school exits when it climbs out of the bottom five percent and its overall score improves. It is not a closure order: the law assumes the school stays open and gets help."),
    ("", "The district is now deciding whether to close a school the state has just placed on a three-year improvement track."),
], 10.2, 9.2, NAVY)
src = textwrap.fill("Sources: Kentucky Department of Education, Assessment and Accountability Data 2025-2026 (Oct. 14, 2026); School Report Card files 2023-24 and 2024-25; SAAR enrollment; KDE Comprehensive Support and Improvement Process (KRS 160.346, 703 KAR 5:280).", int((W - 2 * M) / cw(7.8)))
items.append(("text", y, (M, src, 7.8, MIST, "normal", "left", 1.35)))
y += lh(7.8, 1.35) * (src.count("\n") + 1) + 10
items.append(("text", y, (M, "Every figure and the state's own files: savenmes.org", 9.5, NAVY, "bold", "left", 1.0)))
H = int(y + lh(9.5) + 40)

# ---- draw
fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor=PAPER)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")
for kind, yy, p in items:
    if kind == "rect":
        x, y0, w, h, col = p; ax.add_patch(Rectangle((x, y0), w, h, fc=col, lw=0))
    elif kind == "card":
        x, y0, w, h = p; ax.add_patch(FancyBboxPatch((x, y0), w, h, boxstyle="round,pad=0,rounding_size=10", fc=CHALK, ec=LINE, lw=1.2))
    elif kind == "bar":
        x, y0, w, h, col = p; ax.add_patch(FancyBboxPatch((x, y0), w, h, boxstyle="round,pad=0,rounding_size=4", fc=col, lw=0))
    elif kind == "line":
        (x0, x1), (y0, y1), col, lw = p; ax.plot([x0, x1], [y0, y1], color=col, lw=lw, zorder=0)
    else:
        x, s, pt, col, wt, ha, ls = p
        va = "center" if kind in ("rtext", "ctext") else "top"
        ax.text(x, yy, s, fontsize=pt, color=col, weight=wt, ha=ha, va=va, linespacing=ls)
fig.savefig(OUT, dpi=DPI, facecolor=PAPER); print("wrote", OUT, W, "x", H)
