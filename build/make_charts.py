import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

NAVY = "#1F3864"; BLUE = "#2E75B6"; DBLUE = "#1F4E79"; RED = "#9C3D3D"
GRAY = "#8A8F98"; LGRAY = "#C9CDD4"; MBLUE = "#8FAEDC"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": "#444444",
    "axes.labelcolor": "#333333", "text.color": "#333333", "xtick.color": "#444444",
    "ytick.color": "#444444", "axes.titlesize": 10, "axes.titleweight": "bold",
    "axes.titlepad": 10, "figure.facecolor": "white", "savefig.facecolor": "white",
})

def clean(ax, ygrid=True, xgrid=False):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    if ygrid:
        ax.yaxis.grid(True, color="#E4E6EA", linewidth=0.8); ax.set_axisbelow(True)
    if xgrid:
        ax.xaxis.grid(True, color="#E4E6EA", linewidth=0.8); ax.set_axisbelow(True)

def save(fig, name):
    fig.savefig(f"/home/claude/nmes/{name}", dpi=200, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)

yrs = ["FY2023", "FY2024", "FY2025"]

# ---- A: General Fund (deficit + balance) ----------------------------------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.7, 2.7))
d = [-0.237, -2.535, -2.648]
b1 = a1.bar(yrs, d, color="#9DC3E6", width=0.52)
a1.set_title("Operating result before transfers  ($M)")
a1.axhline(0, color="#444444", linewidth=0.8)
for r, v in zip(b1, d):
    a1.text(r.get_x() + r.get_width()/2, v - 0.18, f"{v:+.2f}", ha="center", va="top",
            fontsize=9, color=NAVY, fontweight="bold")
a1.set_ylim(-3.7, 0.45); clean(a1)
fb = [6.583, 5.516, 4.291]
b2 = a2.bar(yrs, fb, color=NAVY, width=0.52)
a2.set_title("General Fund balance at year end  ($M)")
for r, v in zip(b2, fb):
    a2.text(r.get_x() + r.get_width()/2, v + 0.18, f"{v:.2f}", ha="center",
            fontsize=9, color=NAVY, fontweight="bold")
a2.set_ylim(0, 7.9); clean(a2)
fig.tight_layout(w_pad=2.6)
save(fig, "chart_gf.png")

# ---- B: ESSER cliff + ADA -------------------------------------------------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.7, 2.7))
fed = [7.46, 6.00, 4.51]
b1 = a1.bar(yrs, fed, color=BLUE, width=0.52)
a1.set_title("Federal revenue, governmental funds  ($M)")
for r, v in zip(b1, fed):
    a1.text(r.get_x() + r.get_width()/2, v + 0.2, f"{v:.2f}", ha="center",
            fontsize=9, color=DBLUE, fontweight="bold")
a1.set_ylim(0, 9.4); clean(a1)
a1.annotate("down $2.95M as federal\npandemic aid expired",
            xy=(2, 4.9), xytext=(1.02, 8.15), fontsize=8.2, color=DBLUE,
            arrowprops=dict(arrowstyle="->", color=DBLUE, lw=0.9))
ada = [2490.4, 2278.5, 2242.5]
a2.plot(yrs, ada, color=NAVY, marker="o", markersize=5.5, linewidth=2)
a2.set_title("Average Daily Attendance (SEEK basis)")
for x, v in zip(yrs, ada):
    a2.text(x, v + 26, f"{v:,.0f}", ha="center", fontsize=9, color=NAVY, fontweight="bold")
a2.set_ylim(2130, 2610); clean(a2)
a2.text(0.02, 0.05, "about 248 fewer funded students since the\npandemic hold-harmless ended",
        transform=a2.transAxes, fontsize=8, color=GRAY)
fig.tight_layout(w_pad=2.6)
save(fig, "chart_cliff.png")

# ---- C: per-pupil spending ------------------------------------------------
fig, ax = plt.subplots(figsize=(6.7, 2.3))
schools = ["North Middletown\nElementary", "Cane Ridge\nElementary", "Bourbon Central\nElementary"]
pp = [19348, 18670, 18131]
colors = [NAVY, LGRAY, LGRAY]
bars = ax.barh(schools[::-1], pp[::-1], color=colors[::-1], height=0.52)
ax.set_title("Spending per student, 2023-24  (Kentucky School Report Card)")
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f"${v:,.0f}"))
for r, v, c in zip(bars, pp[::-1], colors[::-1]):
    ax.text(v - 400, r.get_y() + r.get_height()/2, f"${v:,.0f}", ha="right", va="center",
            fontsize=9, color="white" if c == NAVY else "#333333", fontweight="bold")
ax.set_xlim(0, 21200)
clean(ax, ygrid=False, xgrid=True)
fig.tight_layout()
save(fig, "chart_pp.png")

# ---- D: district elementary full history ---------------------------------
fig, ax = plt.subplots(figsize=(6.7, 3.3))
yrs_all = list(range(2007, 2026))
nan = float("nan")
series = [
    ("North Middletown", [56.5, 63.9, 68.6, 87.9, 85.8, 72.5, 67.6, 56.6, 56.9, 48.7, 49.3, 40.0, 50.4, nan, nan, 47.7, 32.1, 54.1, 58.2], NAVY, "-", "o", 2.3),
    ("Bourbon Central", [77.5, 81.9, 72.6, 69.6, 63.0, 74.7, 67.6, 51.8, 52.1, 30.0, 34.0, 32.8, 39.9, nan, 20.0, 29.9, 29.0, 23.8, 26.5], BLUE, "--", "s", 1.6),
    ("Cane Ridge", [35.2, 50.9, 56.2, 65.5, 34.5, 34.0, 49.6, 51.0, 51.1, 57.5, 50.4, 41.4, 38.8, nan, 23.8, 38.7, 34.6, 35.8, 19.3], GRAY, "-", "^", 1.6),
    ("Paris Elementary", [nan]*17 + [16.8, 12.2], "#AEB4BE", "-.", "D", 1.6),
]
for name, ys, col, ls, mk, lw in series:
    ax.plot(yrs_all, ys, color=col, linestyle=ls, marker=mk, markersize=3.8,
            linewidth=lw, label=name)
    last = [v for v in ys if v == v][-1]
    ax.text(2025.3, last, f"{last}", color=col, fontsize=8.8, fontweight="bold", va="center")
for xv in (2011.5, 2020):
    ax.axvline(xv, color="#D5D9E0", linewidth=1.1, linestyle="--", zorder=0)
ax.axhline(50, color=GRAY, linewidth=0.9, linestyle=":")
ax.text(2007.0, 51.6, "Kentucky median (approx. 50)", fontsize=7.8, color=GRAY,
        bbox=dict(facecolor="white", alpha=0.85, edgecolor="none", pad=0.8))
ax.text(2007.1, 92.6, "Blue Ribbon era: 2010 and 2011", fontsize=7.8, color=NAVY, fontweight="bold")
ax.set_title("Elementary school scores by year, 2007-2025")
ax.set_xticks(list(range(2007, 2026, 2)))
ax.set_xlim(2006.5, 2027.0)
ax.set_ylim(4, 97)
ax.legend(loc="upper right", frameon=False, fontsize=8.2, ncol=2)
ax.tick_params(axis="x", labelsize=8.4)
clean(ax)
fig.tight_layout()
save(fig, "chart_district.png")

# ---- E: regional 2024-25 comparison --------------------------------------
fig, ax = plt.subplots(figsize=(6.7, 3.5))
names = ["Northview  (Montgomery Co.)", "Mapleton  (Montgomery Co.)",
         "North Middletown  (Bourbon Co.)", "Shearer  (Clark Co.)",
         "Justice  (Clark Co.)", "Strode Station  (Clark Co.)",
         "Bourbon Central  (Bourbon Co.)", "Cane Ridge  (Bourbon Co.)",
         "Conkwright  (Clark Co.)", "Paris Elementary  (Paris Indep.)"]
vals = [68.9, 65.1, 58.2, 42.3, 39.3, 34.2, 26.5, 19.3, 17.5, 12.2]
cols = [LGRAY, LGRAY, NAVY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY, LGRAY]
bars = ax.barh(names[::-1], vals[::-1], color=cols[::-1], height=0.58)
for r, v in zip(bars, vals[::-1]):
    ax.text(v + 0.9, r.get_y() + r.get_height()/2, f"{v}", va="center",
            fontsize=8.8, color="#333333", fontweight="bold")
ax.axvline(50, color=GRAY, linewidth=1.0, linestyle="--")
ax.text(50.7, 0.15, "KY median", fontsize=8, color=GRAY)
ax.set_title("2024-25 accountability composite: elementary schools across the region")
ax.set_xlim(0, 79)
ax.tick_params(axis="y", labelsize=8.6)
clean(ax, ygrid=False, xgrid=True)
fig.tight_layout()
save(fig, "chart_compare.png")

# ---- F: administration growth --------------------------------------------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.7, 2.7))
da = [0.9997, 1.2321, 1.4472]
b1 = a1.bar(yrs, da, color=NAVY, width=0.52)
a1.set_title("District administration expense  ($M)")
for r, v in zip(b1, da):
    a1.text(r.get_x() + r.get_width()/2, v + 0.05, f"{v:.2f}", ha="center",
            fontsize=9, color=NAVY, fontweight="bold")
a1.set_ylim(0, 1.85); clean(a1)
a1.text(0.03, 0.93, "+44.8% in two years", transform=a1.transAxes,
        fontsize=9, color=BLUE, fontweight="bold")
sa = [2.1100, 2.5188, 2.5814]
b2 = a2.bar(yrs, sa, color=BLUE, width=0.52)
a2.set_title("School administration expense  ($M)")
for r, v in zip(b2, sa):
    a2.text(r.get_x() + r.get_width()/2, v + 0.08, f"{v:.2f}", ha="center",
            fontsize=9, color=DBLUE, fontweight="bold")
a2.set_ylim(0, 3.25); clean(a2)
a2.text(0.03, 0.93, "+22.3% in two years", transform=a2.transAxes,
        fontsize=9, color=BLUE, fontweight="bold")
fig.tight_layout(w_pad=2.6)
save(fig, "chart_admin.png")

# ---- G: debt service ------------------------------------------------------
fig, ax = plt.subplots(figsize=(4.8, 2.4))
labels = ["FY2025\ndistrict share", "FY2026\ndistrict share", "FY2026 total\n(incl. state SFCC)"]
vals = [1.150, 1.579, 1.846]
cols = [LGRAY, NAVY, BLUE]
bars = ax.bar(labels, vals, color=cols, width=0.52)
for r, v in zip(bars, vals):
    ax.text(r.get_x() + r.get_width()/2, v + 0.05, f"${v:.2f}M", ha="center",
            fontsize=8.8, fontweight="bold", color="#333333")
ax.set_title("Annual bond payments (debt service)")
ax.set_ylim(0, 2.25)
clean(ax)
fig.tight_layout()
save(fig, "chart_debt.png")

# ---- H: enrollment 1989-2025 vs capacity ---------------------------------
fig, ax = plt.subplots(figsize=(6.7, 2.8))
eyrs = list(range(1989, 2026))
evals = [261, 255, 234, 225, 202, 203, 182, 196, 208, 198, 205, 195, 195, 203,
         196, 206, 204, 199, 211, 224, 217, 177, 165, 167, 154, 154, 155, 154,
         131, 131, 160, 160, 148, 153, 145, 135, 128]
ax.plot(eyrs, evals, color=NAVY, linewidth=2.0, marker="o", markersize=2.8)
ax.axhline(174, color=BLUE, linewidth=1.2, linestyle="--")
ax.text(1996.5, 179, "Current rated capacity: 174", fontsize=8.2, color=BLUE, fontweight="bold")
ax.annotate("Peak: 261 students (1988-89)", xy=(1989, 261), xytext=(1992.2, 267),
            fontsize=8.2, color=NAVY, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=NAVY, lw=0.9))
ax.text(2025.5, 128, "128", color=NAVY, fontsize=9, fontweight="bold", va="center")
ax.set_title("NMES enrollment, 1989 to 2025")
ax.set_xticks([1989, 1993, 1997, 2001, 2005, 2009, 2013, 2017, 2021, 2025])
ax.set_xlim(1988, 2027.4)
ax.set_ylim(0, 292)
ax.tick_params(axis="x", labelsize=8.4)
clean(ax)
fig.tight_layout()
save(fig, "chart_enroll.png")

# ---- J: elementary rebalancing scenario -----------------------------------
fig, ax = plt.subplots(figsize=(6.7, 2.8))
import numpy as np
schools_b = ["North Middletown", "Bourbon Central", "Cane Ridge"]
today = [128, 459, 453]
after = [174, 444, 438]
x = np.arange(3); w = 0.36
b1 = ax.bar(x - w/2, today, w, color=LGRAY, label="Today")
b2 = ax.bar(x + w/2, after, w, color=NAVY, label="Rebalanced (30 rezoned + 16 transfers)")
for r, v in list(zip(b1, today)) + list(zip(b2, after)):
    ax.text(r.get_x() + r.get_width()/2, v + 8, f"{v}", ha="center", fontsize=8.6,
            fontweight="bold", color="#333333")
caps = [174, 549, 422]
for xi, cv in zip(x, caps):
    ax.plot([xi - w, xi + w], [cv, cv], color=BLUE, linewidth=1.4, linestyle="--")
ax.text(x[0] + w + 0.05, 174, "174", fontsize=8, color=BLUE, va="center")
ax.text(x[1] + w + 0.05, 549, "549", fontsize=8, color=BLUE, va="center")
ax.text(x[2] + w + 0.05, 422, "422", fontsize=8, color=BLUE, va="center")
ax.plot([], [], color=BLUE, linewidth=1.4, linestyle="--",
        label="Rated capacity (2021 facility plan)")
ax.set_xticks(x); ax.set_xticklabels(schools_b)
ax.set_title("One rebalancing scenario: fill NMES, relieve the Paris-area schools")
ax.set_ylim(0, 790)
ax.legend(loc="upper left", frameon=False, fontsize=8.2)
clean(ax)
fig.tight_layout()
save(fig, "chart_balance.png")

# ---- K: density map on the real county outline, traced zones --------------
fig, ax = plt.subplots(figsize=(6.7, 4.4))
from matplotlib.patches import Polygon as MplPolygon
COUNTY = [(-84.4438,38.2831),(-84.3792,38.2779),(-84.2787,38.3148),(-84.1926,38.3715),(-84.1674,38.3552),(-84.0957,38.2590),(-84.0562,38.2564),(-84.0634,38.2350),(-84.0275,38.2143),(-83.9880,38.2186),(-83.9772,38.1920),(-84.0813,38.1155),(-84.2859,38.0674),(-84.3792,38.1138),(-84.3541,38.1783),(-84.3720,38.2083),(-84.4007,38.2075),(-84.4438,38.2831)]
NORTH = [(-84.4438,38.2831),(-84.3792,38.2779),(-84.2787,38.3148),(-84.1926,38.3715),(-84.1674,38.3552),(-84.0957,38.259),(-84.0562,38.2564),(-84.0634,38.235),(-84.0323,38.2171),(-84.1,38.245),(-84.245,38.212),(-84.3,38.235),(-84.4204,38.2421),(-84.4438,38.2831)]
SW = [(-84.2428,38.0775),(-84.2859,38.0674),(-84.3792,38.1138),(-84.3541,38.1783),(-84.372,38.2083),(-84.4007,38.2075),(-84.4204,38.2421),(-84.3,38.235),(-84.245,38.212),(-84.235,38.14),(-84.2428,38.0775)]
EAST = [(-84.0323,38.2171),(-84.0275,38.2143),(-84.026,38.2145),(-84.02,38.212),(-83.9823,38.2045),(-83.9772,38.192),(-84.0813,38.1155),(-84.2428,38.0775),(-84.235,38.14),(-84.245,38.212),(-84.1,38.245),(-84.0323,38.2171)]
import os as _os, json as _json
_sabs_path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "sabs_zones.json")
SABS = _json.load(open(_sabs_path)) if _os.path.exists(_sabs_path) else None
def _zone_color(nm):
    n = nm.lower()
    if "middletown" in n: return "#E8EDF5"
    if "cane" in n: return "#C5D7EC"
    return "#8FAEDC"
if SABS:
    for _sch in SABS["schools"]:
        for _ring in _sch["rings"]:
            ax.add_patch(MplPolygon([tuple(p) for p in _ring], closed=True,
                         facecolor=_zone_color(_sch["name"]), edgecolor="#1F3864", linewidth=1.1))
else:
    ax.add_patch(MplPolygon(NORTH, closed=True, facecolor="#8FAEDC", edgecolor="#FFFFFF", linewidth=1.0))
    ax.add_patch(MplPolygon(SW, closed=True, facecolor="#C5D7EC", edgecolor="#FFFFFF", linewidth=1.0))
    ax.add_patch(MplPolygon(EAST, closed=True, facecolor="#E8EDF5", edgecolor="#FFFFFF", linewidth=1.0))
if not SABS:
    ax.add_patch(MplPolygon(COUNTY, closed=True, facecolor="none", edgecolor="#1F3864", linewidth=1.6))
paris = (-84.2529, 38.2098); nmid = (-84.1122, 38.1446); mills = (-84.1467, 38.3022)
ax.plot(*paris, "o", color=NAVY, markersize=9, zorder=5)
ax.text(-84.610, 38.252, "Paris (10,171)", fontsize=8.8, fontweight="bold",
        color="#1F3864", ha="left", va="top")
ax.text(-84.610, 38.233, "Bourbon Central 459\nCane Ridge 453", fontsize=7.4,
        color="#1F3864", ha="left", va="top")
ax.plot([-84.468, paris[0] - 0.010], [38.231, paris[1] + 0.005],
        color=GRAY, linewidth=0.8, linestyle=":", zorder=3)
ax.plot(*mills, "o", color=NAVY, markersize=5, zorder=5)
ax.text(mills[0] - 0.018, mills[1] - 0.004, "Millersburg (747)", fontsize=7.4, color="#1F3864",
        ha="right", va="center")
ax.plot(nmid[0], nmid[1], "*", color="#1F3864", markersize=16, zorder=5)
ax.text(nmid[0] + 0.005, nmid[1] - 0.022, "North Middletown (610)\nNMES: 128 of 174 seats",
        fontsize=8.2, fontweight="bold", color="#1F3864", ha="center", va="top",
        bbox=dict(facecolor="white", alpha=0.88, edgecolor="none", pad=1.6), zorder=6)
ax.plot([paris[0], nmid[0]], [paris[1], nmid[1]], color=GRAY, linewidth=1.1, linestyle=":", zorder=4)
if SABS:
    _nm = next(x for x in SABS["schools"] if "North Middletown" in x["name"])
    _north_lbl, _sw_lbl = "Cane Ridge zone", "Bourbon Central\nzone"
    _tot = sum(x["area_sq_mi"] for x in SABS["schools"])
    _nm_stats = "NMES zone\n%.0f sq mi\n%.0f%% of county\n128 students\n~%.1f per sq mi" % (
        _nm["area_sq_mi"], 100 * _nm["area_sq_mi"] / _tot, 128/_nm["area_sq_mi"])
else:
    _north_lbl, _sw_lbl = "North zone", "Southwest\nzone"
    _nm_stats = "NMES zone\n~105 sq mi\n128 students\n~1.2 per sq mi"
ax.text(-84.350, 38.262, _north_lbl, fontsize=7.8, color="#1F3864", fontweight="bold", ha="center")
ax.text(-84.302, 38.128, _sw_lbl, fontsize=7.6, color="#1F3864", fontweight="bold",
        ha="center", va="top")
ax.text(-83.906, 38.29, _nm_stats,
        fontsize=8.7, color="#1F3864", fontweight="bold", ha="right", va="top",
        bbox=dict(facecolor="white", alpha=0.88, edgecolor="none", pad=1.6), zorder=6)
ax.set_title("Bourbon County elementary zones: where the students are", fontsize=11.5, pad=14)
_sub = ("Official attendance boundaries: NCES School Attendance\nBoundary Survey, 2015-16 collection" if SABS
        else "Traced from the district's published attendance-zone view\non the U.S. Census county outline")
ax.text(-84.610, 38.398, _sub, fontsize=7.6, color="#555555", ha="left", va="top")
sb_y = 38.022; sb_x0 = -84.600; sb_x1 = sb_x0 + 0.1832
ax.plot([sb_x0, sb_x1], [sb_y, sb_y], color="#1F3864", linewidth=2.2, solid_capstyle="butt")
for xx in (sb_x0, sb_x1):
    ax.plot([xx, xx], [sb_y - 0.004, sb_y + 0.004], color="#1F3864", linewidth=1.6)
ax.text((sb_x0 + sb_x1) / 2, sb_y + 0.008, "10 miles", fontsize=7.4, color="#1F3864", ha="center")
ax.annotate("N", xy=(-83.925, 38.385), fontsize=10, fontweight="bold", color="#1F3864", ha="center")
ax.annotate("", xy=(-83.925, 38.383), xytext=(-83.925, 38.355),
            arrowprops=dict(arrowstyle="-|>", color="#1F3864", lw=1.4))
import numpy as np
ax.set_aspect(1 / np.cos(np.radians(38.2)))
ax.set_xlim(-84.615, -83.90); ax.set_ylim(38.005, 38.425)
ax.axis("off")
fig.tight_layout()
save(fig, "chart_map.png")

# ---- I: tax rates ---------------------------------------------------------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.7, 3.0), gridspec_kw={"width_ratios": [1, 1.3]})
tyrs = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
trates = [61.3, 60.6, 55.9, 54.2, 49.2, 52.4, 52.4, 52.4]
a1.plot(tyrs, trates, color=NAVY, marker="o", markersize=4.5, linewidth=2)
for x, v in [(2018, 61.3), (2022, 49.2), (2025, 52.4)]:
    a1.text(x, v + 1.1 if v != 49.2 else v - 2.4, f"{v}", ha="center", fontsize=8.2,
            color=NAVY, fontweight="bold")
a1.set_title("Bourbon Co. Schools rate by tax year\n(real estate, cents per $100)")
a1.set_ylim(43, 67)
a1.set_xticks(tyrs)
a1.tick_params(axis="x", labelsize=7.8, rotation=45)
clean(a1)
dnames = ["Fayette", "Paris Independent", "Clark", "Bath", "Scott", "Harrison",
          "Montgomery", "Bourbon County", "Nicholas"]
dvals = [80.9, 71.5, 66.8, 63.4, 62.9, 57.7, 52.5, 52.4, 43.1]
dcols = [LGRAY] * 9
dcols[7] = NAVY
bars = a2.barh(dnames[::-1], dvals[::-1], color=dcols[::-1], height=0.58)
for r, v in zip(bars, dvals[::-1]):
    a2.text(v + 1.0, r.get_y() + r.get_height() / 2, f"{v}", va="center",
            fontsize=8.2, color="#333333", fontweight="bold",
            bbox=dict(facecolor="white", alpha=0.85, edgecolor="none", pad=0.8))
a2.axvline(65.1, color=GRAY, linewidth=1.0, linestyle="--", zorder=0)
a2.text(66.0, 0.1, "KY school avg 65.1", fontsize=7.6, color=GRAY)
a2.set_title("2024-25 levied rate, area districts")
a2.set_xlim(0, 90)
a2.tick_params(axis="y", labelsize=8.2)
clean(a2, ygrid=False, xgrid=True)
fig.tight_layout(w_pad=2.2)
save(fig, "chart_tax.png")

print("charts done")
