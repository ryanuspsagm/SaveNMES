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
b1 = a1.bar(yrs, d, color=RED, width=0.52)
a1.set_title("Operating result before transfers  ($M)")
a1.axhline(0, color="#444444", linewidth=0.8)
for r, v in zip(b1, d):
    a1.text(r.get_x() + r.get_width()/2, v - 0.18, f"{v:+.2f}", ha="center", va="top",
            fontsize=9, color=RED, fontweight="bold")
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
for r, v in zip(bars, pp[::-1]):
    ax.text(v - 400, r.get_y() + r.get_height()/2, f"${v:,.0f}", ha="right", va="center",
            fontsize=9, color="white", fontweight="bold")
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
ax.text(2007.0, 51.6, "Kentucky median (approx. 50)", fontsize=7.8, color=GRAY)
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
        fontsize=9, color=RED, fontweight="bold")
sa = [2.1100, 2.5188, 2.5814]
b2 = a2.bar(yrs, sa, color=BLUE, width=0.52)
a2.set_title("School administration expense  ($M)")
for r, v in zip(b2, sa):
    a2.text(r.get_x() + r.get_width()/2, v + 0.08, f"{v:.2f}", ha="center",
            fontsize=9, color=DBLUE, fontweight="bold")
a2.set_ylim(0, 3.25); clean(a2)
a2.text(0.03, 0.93, "+22.3% in two years", transform=a2.transAxes,
        fontsize=9, color=RED, fontweight="bold")
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

# ---- I: tax rates ---------------------------------------------------------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.7, 3.0), gridspec_kw={"width_ratios": [1, 1.3]})
tyrs = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
trates = [61.3, 60.6, 55.9, 54.2, 49.2, 52.4, 52.4, 52.4]
a1.plot(tyrs, trates, color=NAVY, marker="o", markersize=4.5, linewidth=2)
for x, v in zip(tyrs, trates):
    a1.text(x, v + 0.9, f"{v}", ha="center", fontsize=7.8, color=NAVY, fontweight="bold")
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
            fontsize=8.2, color="#333333", fontweight="bold")
a2.axvline(65.1, color=GRAY, linewidth=1.0, linestyle="--")
a2.text(65.8, 0.05, "KY school avg 65.1", fontsize=7.6, color=GRAY)
a2.set_title("2024-25 levied rate, area districts")
a2.set_xlim(0, 90)
a2.tick_params(axis="y", labelsize=8.2)
clean(a2, ygrid=False, xgrid=True)
fig.tight_layout(w_pad=2.2)
save(fig, "chart_tax.png")

print("charts done")
