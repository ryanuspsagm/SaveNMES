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
    a2.text(x, v + 26, f"{int(v + 0.5):,}", ha="center", fontsize=9, color=NAVY, fontweight="bold")
a2.set_ylim(2130, 2610); clean(a2)
a2.text(0.02, 0.05, "funded attendance down about 247 since the\npandemic hold-harmless ended",
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

# ---- D: district elementary full history (official record + third-party index) ----
fig, (axo, axs) = plt.subplots(2, 1, figsize=(6.7, 5.6), height_ratios=[1.15, 1])
yrs_all = list(range(2007, 2026))
nan = float("nan")
comp = [
    ("North Middletown", {2012:62.6,2013:68.8,2014:71.4,2015:72.1,2016:79.1,2022:51.9,2023:62.2,2024:74.5,2025:54.0}, NAVY, "-", "o", 2.4),
    ("Bourbon Central", {2012:63.2,2013:63.0,2014:69.8,2015:67.8,2016:56.8,2022:52.8,2023:56.7,2024:50.3,2025:55.4}, BLUE, "--", "s", 1.5),
    ("Cane Ridge", {2012:53.3,2013:58.9,2014:69.2,2015:68.5,2016:65.5,2022:54.3,2023:51.8,2024:60.7,2025:47.8}, GRAY, "-", "^", 1.5),
    ("Paris Elementary", {2012:48.0,2013:49.9,2014:59.4,2015:54.8,2016:69.6,2022:46.1,2023:45.9,2024:40.7,2025:41.9}, "#AEB4BE", "-.", "D", 1.3),
]
for name, m, col, ls, mk, lw in comp:
    ys = [m.get(y, nan) for y in yrs_all]
    axo.plot(yrs_all, ys, color=col, linestyle=ls, marker=mk, markersize=3.6, linewidth=lw, label=name)
axo.axvspan(2006.5, 2011.5, color="#F3F5F9")
axo.axvspan(2019.5, 2021.5, color="#E7EBF3")
axo.text(2009.0, 88, "CATS era: school files\navailable from KDE\nby data request", ha="center", fontsize=7.2, color="#777777")
axo.text(2018.4, 55, "no composite issued\n2017-2021", ha="center", fontsize=7.2, color="#777777",
         bbox=dict(facecolor="white", edgecolor="none", pad=1.2))
axo.text(2020.5, 42, "COVID", ha="center", fontsize=7.4, color="#777777", fontweight="bold")
axo.annotate('79.1 "Distinguished"', xy=(2016, 79.1), xytext=(2013.1, 92.5), fontsize=7.6, color=NAVY,
             fontweight="bold", arrowprops=dict(arrowstyle="->", color=NAVY, lw=0.8))
axo.annotate("74.5, first by 14 pts", xy=(2024, 74.5), xytext=(2021.2, 92.5), fontsize=7.6, color=NAVY,
             fontweight="bold", arrowprops=dict(arrowstyle="->", color=NAVY, lw=0.8))
axo.set_title("Official state composite: Unbridled Learning overall score (2012-16), KSA overall indicator rate (2022-25)")
axo.set_xticks(list(range(2007, 2026, 2)))
axo.set_xlim(2006.5, 2026.0)
axo.set_ylim(35, 101)
axo.legend(loc="lower left", frameon=False, fontsize=7.4, ncol=2)
clean(axo)
series = [
    ("North Middletown", [56.5, 63.9, 68.6, 87.9, 85.8, 72.5, 67.6, 56.6, 56.9, 48.7, 49.3, 40.0, 50.4, nan, nan, 47.7, 32.1, 54.1, 58.2], NAVY, "-", "o", 2.0),
    ("Bourbon Central", [77.5, 81.9, 72.6, 69.6, 63.0, 74.7, 67.6, 51.8, 52.1, 30.0, 34.0, 32.8, 39.9, nan, 20.0, 29.9, 29.0, 23.8, 26.5], BLUE, "--", "s", 1.4),
    ("Cane Ridge", [35.2, 50.9, 56.2, 65.5, 34.5, 34.0, 49.6, 51.0, 51.1, 57.5, 50.4, 41.4, 38.8, nan, 23.8, 38.7, 34.6, 35.8, 19.3], GRAY, "-", "^", 1.4),
    ("Paris Elementary", [nan]*17 + [16.8, 12.2], "#AEB4BE", "-.", "D", 1.4),
]
for name, ys, col, ls, mk, lw in series:
    axs.plot(yrs_all, ys, color=col, linestyle=ls, marker=mk, markersize=3.2, linewidth=lw)
axs.axvspan(2019.5, 2021.5, color="#E7EBF3")
axs.set_title("Third-party SchoolDigger index of the same tests (kept for context; official record governs)")
axs.set_xticks(list(range(2007, 2026, 2)))
axs.set_xlim(2006.5, 2026.0)
axs.set_ylim(4, 97)
axs.text(2007.0, 10, "validated against the official files: tracks larger schools closely (r near 0.9);\nunreliable year to year for a school NMES's size (r near 0.4)", fontsize=7.0, color="#777777")
clean(axs)
fig.tight_layout(h_pad=1.6)
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
ax.set_title("2024-25 school index across the region (SchoolDigger 0-100, from state test data)")
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
caps = [174, 521, 422]
for xi, cv in zip(x, caps):
    ax.plot([xi - w, xi + w], [cv, cv], color=BLUE, linewidth=1.4, linestyle="--")
ax.text(x[0] + w + 0.05, 174, "174", fontsize=8, color=BLUE, va="center")
ax.text(x[1] + w + 0.05, 521, "521", fontsize=8, color=BLUE, va="center")
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

# ---- V3.6: fourteen years of school levies, nine districts ----
import json as _json, os as _os
_lv_path=_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),"levy_series.json")
_lv=_json.load(open(_lv_path))
fig,(l1,l2)=plt.subplots(2,1,figsize=(6.9,7.0),height_ratios=[1.25,1])
_yrs=sorted(_lv["Bourbon Co"]); _x=[int(y[:4]) for y in _yrs]
_sty={"Fayette":("#AEB4BE","-"),"Paris Ind":(BLUE,"--"),"Clark":("#8FAEDC","-"),"Bath":("#C0625E","-"),
      "Scott":(GRAY,"-"),"Harrison":("#9BB0A5","-"),"Montgomery":(LGRAY,"-"),"Nicholas":(LGRAY,"--")}
for _lab,(_c,_ls) in _sty.items():
    l1.plot(_x,[_lv[_lab][y] for y in _yrs],color=_c,linestyle=_ls,lw=1.5,marker="o",ms=2.4,label=_lab)
l1.plot(_x,[_lv["Bourbon Co"][y] for y in _yrs],color=NAVY,lw=3.0,marker="o",ms=4.2,label="Bourbon County",zorder=5)
l1.annotate("Bourbon's levied rate fell 12 cents\n2018 to 2022, then the recallable\nnickel restored 5.7 in 2023",xy=(2022,49.2),
            xytext=(2016.6,42.2),fontsize=7.2,color=NAVY,fontweight="bold",
            arrowprops=dict(arrowstyle="->",color=NAVY,lw=0.9))
l1.set_title("School real estate levy, total levied (general fund plus facilities), cents per \$100:\nnine area districts, tax years 2012 to 2025")
l1.set_ylim(33,88); l1.legend(fontsize=6.8,ncol=3,frameon=False,loc="upper left")
clean(l1)
_labs=["Bath","Scott","Harrison","Clark","Fayette","Paris Ind","Nicholas","Montgomery","Bourbon Co"]
_pch=[( _lv[l]["2025-26"]/_lv[l]["2012-13"]-1)*100 for l in _labs]
_cols=[NAVY if l=="Bourbon Co" else ("#C0625E" if p>20 else "#9DC3E6") for l,p in zip(_labs,_pch)]
_bars=l2.bar(range(len(_labs)),_pch,color=_cols,width=0.62)
for _b,_p in zip(_bars,_pch):
    l2.text(_b.get_x()+_b.get_width()/2,_p+(1.2 if _p>=0 else -3.4),f"{_p:+.1f}%",ha="center",fontsize=8.2,
            fontweight="bold",color=NAVY if _p<0 else "#333333")
l2.axhline(0,color="#444444",lw=0.9)
l2.set_xticks(range(len(_labs))); l2.set_xticklabels(_labs,fontsize=7.8)
l2.set_ylabel("change in levied rate, percent")
l2.set_ylim(-14,82)
l2.set_title("Change over fourteen years: every neighboring district's levied rate rose.\nBourbon County's is the only one lower today than in 2012.",fontsize=9.5)
clean(l2)
fig.tight_layout(h_pad=2.0)
save(fig,"chart_levy_history.png")
print("levy history chart done")

print("charts done")

# ---- P2: every school filled to its rated capacity, seven capacity scenarios ----
import math as _math
def _sections(N):
    per = N/6
    return 4*_math.ceil(per/24) + _math.ceil(per/28) + _math.ceil(per/29)
def _pp(total, n_now, n_t, sect_now, V=400, T=85000):
    return (total + (n_t-n_now)*V + (_sections(n_t)-sect_now)*T) / n_t
_S = {'NMES': (128, 2476544, 9), 'BCES': (491, 8902321, _sections(491)), 'CRES': (461, 8606870, _sections(461))}
_scen = [
 ("Actual today\n(2023-24 filing)", None),
 ("2013 plan\n(state approved)\n198/564/500", {'NMES':198,'BCES':564,'CRES':500}),
 ("2017 plan\n(state approved)\n152/611/550", {'NMES':152,'BCES':611,'CRES':550}),
 ("2021 plan\n(state approved,\nin force) 174/521/422", {'NMES':174,'BCES':521,'CRES':422}),
 ("Peak enrollment,\npast 20 years\n224/620/495", {'NMES':224,'BCES':620,'CRES':495}),
 ("2026 architect\n(KFICS slides)\n154/499/397", {'NMES':154,'BCES':499,'CRES':397}),
 ("2026 draft plan\ntable (unapproved)\n154/640/547", {'NMES':154,'BCES':640,'CRES':547}),
]
_vals = {s: [] for s in _S}
for _name, _caps in _scen:
    for s, (n, tot, sec) in _S.items():
        _vals[s].append(tot/n if _caps is None else _pp(tot, n, _caps[s], sec))
import numpy as _np
fig, ax = plt.subplots(figsize=(7.2, 4.5))
x = _np.arange(len(_scen)); w = 0.27
bsets = [(_vals['NMES'], -w, NAVY, "North Middletown"), (_vals['BCES'], 0, BLUE, "Bourbon Central"),
         (_vals['CRES'], w, GRAY, "Cane Ridge")]
for vv, off, col, lab in bsets:
    bars = ax.bar(x + off, vv, w, color=col, label=lab)
    for b in bars:
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 200,
                f"{b.get_height()/1000:.1f}", ha="center", fontsize=6.4, fontweight="bold", color="#333333")
for gi in range(len(_scen)):
    trio = [_vals['NMES'][gi], _vals['BCES'][gi], _vals['CRES'][gi]]
    idx = trio.index(min(trio))
    ax.text(gi + (-w, 0, w)[idx], min(trio) - 1500, "low", ha="center", fontsize=6.6,
            color="white", fontweight="bold")
ax.set_ylabel("Per student, filled to the scenario's rating ($K)")
ax.set_ylim(0, 24800)
ax.yaxis.set_major_formatter(lambda v, p: f"{v/1000:,.0f}")
ax.set_xticks(x); ax.set_xticklabels([s[0] for s in _scen], fontsize=6.4)
ax.legend(fontsize=7.4, loc="upper left", frameon=False, ncol=3)
ax.set_title("Every school filled to its rated capacity: the answer depends on\nwhich of the district's own capacity tables you use")
clean(ax)
fig.tight_layout()
save(fig, "chart_capacity_scenarios.png")
print("capacity scenarios done")

# ---- V3: two-tailed closure spectrum + tornado (v5.0 grid, six levers) ----
fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.9, 5.8), height_ratios=[1, 1.5])
a1.axvspan(-846, 0, color="#F3E4E0", zorder=0)

a1.axvspan(-518, -339, color="#C9D6EA", zorder=1, alpha=0.9)
a1.plot([-846, -10], [0.5, 0.5], color="#666666", lw=1.2, zorder=2)
for v, lab in [(-846, "worst case\n\$846K lost"), (-10, "best case\n\$10K still lost")]:
    a1.plot([v], [0.5], marker="|", markersize=16, color="#444444", zorder=3)
    a1.annotate(lab, xy=(v, 0.5), xytext=(v, 0.16), ha="center", fontsize=7.8)
a1.plot([-427], [0.5], marker="D", markersize=9, color=NAVY, zorder=4)
a1.annotate("median: \$427K LOST", xy=(-427, 0.5), xytext=(-427, 0.68), ha="center", fontsize=8.2, fontweight="bold", color=NAVY)
a1.annotate("middle half:\n\$518K to \$339K lost", xy=(-427, 0.5), xytext=(-429, 0.06), ha="center", fontsize=7.4, color="#39506e")
a1.annotate("the plan needs \$800K to \$1M\nfrom the closure", xy=(700, 0.5), xytext=(620, 0.78), ha="center",
            fontsize=7.8, color="#8a4a2b", fontweight="bold",
            arrowprops=dict(arrowstyle="->", color="#8a4a2b", lw=0.9))
a1.plot([700, 900], [0.5, 0.5], color="#8a4a2b", lw=3, solid_capstyle="butt")
a1.text(-880, 0.86, "every one of the 972\nscenarios loses money", ha="center", fontsize=7.8, color="#7a3b2e", fontweight="bold")
a1.set_xlim(-1180, 1000); a1.set_ylim(0, 1)
a1.axvline(0, color="#888888", lw=0.9, linestyle=(0, (3, 2)))
a1.set_yticks([])
a1.set_xticks([-1200, -800, -400, 0, 400, 800])
a1.set_xticklabels(["-\$1,200K", "-\$800K", "-\$400K", "\$0", "+\$400K", "+\$800K"], fontsize=7.8)
a1.set_title("Net yearly effect of closing NMES: all 972 combinations, on the district's own figures\nand the signed school-choice survey")
for sp in ("top", "right", "left"): a1.spines[sp].set_visible(False)
levers3 = [("Fixed positions\n(all kept vs all cut over time)", -516.5, -302.4),
           ("Students missing at steady state\n(117 up to 154, survey-anchored)", -494.5, -319.7),
           ("Teachers cut (0 up to 3,\nat their \$54,479.40 each)", -518.4, -355.0),
           ("Add-ons per leaver (\$1,000 down to \$0)", -477.4, -341.4),
           ("Added busing (\$95K down to \$20K)", -441.4, -366.4),
           ("Building costs stopped (50 to 100%)", -436.2, -362.7)][::-1]
yy = np.arange(len(levers3))
for i, (lab, lo, hi) in enumerate(levers3):
    a2.barh(i, hi - lo, left=lo, height=0.55, color="#9DC3E6", edgecolor=BLUE, linewidth=0.8)
    a2.text(lo - 8, i, f"{lo:.0f}", ha="right", va="center", fontsize=7)
    a2.text(hi + 8, i, f"{hi:.0f}", ha="left", va="center", fontsize=7)
a2.axvline(-409.4, color=NAVY, lw=1.4, linestyle=(0, (4, 2)))
a2.text(-404, len(levers3) - 0.45, "central case LOSES \$409K", fontsize=7.6, color=NAVY, fontweight="bold")
a2.axvline(0, color="#888888", lw=0.9, linestyle=(0, (3, 2)))
a2.set_yticks(yy); a2.set_yticklabels([l[0] for l in levers3], fontsize=7.2)
a2.set_xlabel("Net yearly effect (\$K), central case, moving one lever at a time")
a2.set_xlim(-840, 140)
a2.xaxis.grid(True, color="#E4E6EA", linewidth=0.8); a2.set_axisbelow(True)
for sp in ("top", "right"): a2.spines[sp].set_visible(False)
a2.set_title("What moves the number most", fontsize=9.5)
fig.tight_layout()
save(fig, "chart_closure_spectrum.png")

# ---- V3.1: KFICS building condition index, every state report published ----
fig, ax = plt.subplots(figsize=(6.9, 3.7))
ci_x = [0, 1, 2]
ci_labels = ["October 2023\nofficial report\n(2020-21 inspections)",
             "October 2025\nofficial report\n(same inspections,\ncosts updated)",
             "July 2026\nupdated report\n(new April 2026\ninspections)"]
ci_series = [
    ("Bourbon Central (1988)", [0.888, 0.819, 0.823], BLUE, "--", "s", 1.6),
    ("Cane Ridge (1992)", [0.812, 0.812, 0.728], GRAY, "-", "^", 1.6),
    ("North Middletown (1948/64)", [0.694, 0.702, 0.773], NAVY, "-", "o", 2.4),
]
for nm, vv, col, ls, mk, lw in ci_series:
    ax.plot(ci_x, vv, color=col, linestyle=ls, marker=mk, markersize=6, linewidth=lw, label=nm)
    for xi, v in zip(ci_x, vv):
        dy = 0.013 if nm.startswith("North") else (0.013 if v >= 0.81 else -0.026)
        if nm.startswith("Cane") and xi < 2: dy = -0.026
        ax.text(xi, v + dy, f"{v:.3f}", ha="center", fontsize=7.6, color=col, fontweight="bold")
ax.annotate("the only school in the district whose\ncondition improved between inspections",
            xy=(2, 0.773), xytext=(1.30, 0.640), fontsize=7.6, color=NAVY, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=NAVY, lw=0.9))
ax.text(0.02, 0.045, "Condition Index = 1 minus (repairs due within 4 years / building replacement value). Higher is better.\n"
        "NMES four-year repair bill in the July 2026 report: \\$3.1M, the smallest of the district's five schools.",
        transform=ax.transAxes, fontsize=7.0, color="#666666")
ax.set_xticks(ci_x); ax.set_xticklabels(ci_labels, fontsize=7.6)
ax.set_xlim(-0.35, 2.55)
ax.set_ylim(0.55, 0.95)
ax.set_ylabel("KFICS Condition Index")
ax.legend(fontsize=7.6, loc="upper right", frameon=False)
clean(ax)
ax.set_title("Building condition as reported to the state: every KFICS State Report published")
fig.tight_layout()
save(fig, "chart_condition.png")

# ---- V3.4: the Kentucky record, full distribution + rural elementary cases ----
fig, (axA, axB) = plt.subplots(2, 1, figsize=(6.9, 7.2), height_ratios=[1, 1.05])
# Panel A: all 163 events, per displaced student, clipped at +/-16K
bins = [16,2,0,0,1,0,3,3,1,1,2,3,1,6,15,11,14,6,9,11,7,5,3,3,4,3,0,0,4,0,0,3,26]
edges = list(range(-16,17))
cols = []
for b in edges:
    if b < -13 or b >= 13: cols.append("#DDD3CB")
    else: cols.append(MBLUE if b >= 0 else "#C9CDD4")
axA.bar([e+0.5 for e in edges], bins, width=0.92, color=cols)
axA.axvspan(6.957, 8.696, color="#F3E4E0", zorder=0)
axA.axvline(1.102, color=NAVY, lw=1.6, linestyle=(0,(4,2)))
axA.text(1.35, 27.4, "median: \\$1,102 per\ndisplaced student", fontsize=7.4, color=NAVY, fontweight="bold")
axA.axvline(0, color="#555555", lw=1.0)
axA.text(-15.6, 27.4, "40% of districts spent\nMORE than trend\nafter closing", fontsize=7.2, color="#7a3b2e", fontweight="bold")
axA.text(7.83, 21.5, "the plan:\n\\$6,957\nto \\$8,696", ha="center", fontsize=7.2, color="#8a4a2b", fontweight="bold")
axA.text(14.5, 21.5, "beyond \\$13K:\nmore than a school\neven costs per\nstudent; budget\nnoise, both tails", ha="center", fontsize=6.4, color="#77706a")
axA.set_xlim(-16.6, 17.6); axA.set_ylim(0, 30)
axA.set_xticks(range(-16, 17, 4))
axA.set_xticklabels([("\u2264-16" if v==-16 else ("\u2265+16" if v==16 else f"{v:+d}")) for v in range(-16,17,4)], fontsize=7.6)
axA.set_xlabel("District budget gap vs state trend per displaced student ($K per year), whole gap credited to the closure", fontsize=7.8)
axA.set_ylabel("closure events")
axA.set_title("All 163 measurable Kentucky rural closures, 1995-2020: the whole record, nothing hidden", fontsize=9.6)
clean(axA)
# Panel B: rural ELEMENTARY closures only, the district's strongest cases
kb = [
    ("Metcalfe 2013 (built 2 new centers;\nscores fell 10.5 vs state)", 0, 2050, MBLUE, False),
    ("Webster 2012 (Slaughters El; NOTHING\nbuilt: the one clean comparable)", 0, 3525, "#5B6B7E", False),
    ("Perry 2017 (3 towns; built NEW\nWest Perry Elementary)", 0, 3643, MBLUE, False),
    ("Adair 2006 (3 schools; built NEW Adair Co\nElementary; spending spike reverting)", 0, 6935, MBLUE, False),
    ("THE PLAN: no new school,\n\\$800K to \\$1M required", 6957, 8696, "#C0625E", False),
]
yy = np.arange(len(kb))
for i, (lab, lo, hi, col, isrange) in enumerate(kb):
    axB.barh(i, hi-lo, left=lo, height=0.58, color=col, edgecolor="#666666" if i==len(kb)-1 else "none", linewidth=0.8)
    axB.text(hi+90, i, (f"\\${lo:,} to \\${hi:,}" if lo>0 else f"\\${hi:,}"), va="center", fontsize=7.2, fontweight="bold", color="#333333")
axB.set_yticks(yy); axB.set_yticklabels([k[0] for k in kb], fontsize=7.0)
axB.invert_yaxis()
axB.set_xlim(0, 10600)
axB.text(150, len(kb) - 0.92, "Our own model runs the other way: the median\nscenario LOSES \\$3,714 per displaced student a\nyear, and even its best case loses \\$86.",
         fontsize=7.0, color=NAVY, fontweight="bold", va="top")
axB.xaxis.set_major_formatter(lambda v, p: f"\\${v:,.0f}")
axB.set_xlabel("Per displaced student, per year. Rural ELEMENTARY closures only; city and county-seat grade\nreshuffles (Somerset 1999, Montgomery 2018, which opened a new elementary the same year)\nappear in the record above but are not comparisons for closing a rural town's school.", fontsize=7.2)
axB.set_title("The rural elementary cases: the strongest precedents fall short of the plan's number", fontsize=9.6)
clean(axB, ygrid=False, xgrid=True)
fig.tight_layout(h_pad=2.2)
save(fig, "chart_ky_record.png")

# ---- V3: Millersburg timeline ----
fig, ax = plt.subplots(figsize=(6.9, 3.9))
myrs = [1980, 1990, 2000, 2010, 2020]
mb = [987, 937, 842, 792, 747]
county5 = [19405, 19236, 19360, 19985, 20252]
mb_i = [v / 842 * 100 for v in mb]
co_i = [v / 19360 * 100 for v in county5]
ax.plot(myrs, mb_i, color=NAVY, marker="o", markersize=5, lw=2.4, label="Millersburg (2000 = 100)")
ax.plot(myrs, co_i, color=GRAY, marker="s", markersize=4, lw=1.8, linestyle="--", label="Bourbon County (2000 = 100)")
ax.axvline(2006, color="#B9C4D4", lw=1.0, linestyle=(0, (4, 2)))
ax.axvline(2006.45, color="#C0625E", lw=1.5, linestyle=(0, (4, 2)))
ax.axvline(2013, color="#B9C4D4", lw=1.0, linestyle=(0, (4, 2)))
ax.text(2005.6, 120.5, "private military institute\ncloses July 2006", fontsize=6.8, color="#666666", ha="right")
ax.text(2006.9, 78.2, "PUBLIC ELEMENTARY CLOSES 2006\n(federal CCD record; 119 students;\nNMES today: 128)", fontsize=6.8, color="#7a3b2e", fontweight="bold")
ax.text(2013.4, 114.5, "Joy Global closes 2013:\n197 jobs, half the\ntown's budget", fontsize=6.9, color="#666666")
ax.text(2020.5, mb_i[-1], "747\n(down 11%\nsince 2000)", fontsize=7.4, color=NAVY, fontweight="bold", va="center")
ax.text(2020.5, co_i[-1] + 1.2, "20,252 (+4.6%)", fontsize=7.4, color="#555555", va="center")
ax.set_xlim(1979, 2027.5)
ax.set_ylim(74, 126)
ax.set_ylabel("Population, indexed to 2000 = 100")
ax.legend(fontsize=7.6, loc="lower left", frameon=False)
clean(ax)
ax.set_title("Bourbon County has closed a small school before. The county grew; the town did not.")
fig.tight_layout()
save(fig, "chart_millersburg.png")
print("v3 charts done")
