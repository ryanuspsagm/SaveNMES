#!/usr/bin/env python3
"""Bourbon County's standing among Kentucky districts by school level, two eras on one page.

Top panel elementary, middle panel middle school, bottom panel high school. Each panel
plots the percentile of Bourbon County among Kentucky districts (100 = top) with the
rank under every point:

  2008 to 2011   Kentucky Core Content Tests (the CATS era): average percent proficient
                 or distinguished across the four subjects the LRC district profiles
                 report (reading, mathematics, science, writing), ranked among the 174
                 districts of the time (169 with a high school). Source:
                 build/benchmarks_oea_districts_2008_2011.csv (see
                 build/parse_oea_district_profiles.py).
  2022 to 2026   The state's overall accountability score for the level, ranked among
                 the 172 districts (168 with a high school). Source:
                 build/kde_district_trend_levels_2021_2026.csv.

The two measures are not the same scale, so the eras are drawn as separate lines with
a break between them; the percentile and rank are what carry across.

Usage: python3 build/standing_by_level_2008_2026.py
Writes build/standing_by_level_2008_2026_chart.png, build/standing_by_level_2008_2026.csv
and build/standing_by_level_2008_2026.md.
"""
import csv
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
NAVY, GRAY, INK, MUTED, LINE = "#1F3864", "#8A93A6", "#1C2230", "#6B7486", "#E3E8F0"
FILL = {"red": "#C0392B", "orange": "#E67E22", "yellow": "#F1C40F", "green": "#27AE60", "blue": "#2E75B6"}
BOX = dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.88)
LEVELS = [("ES", "Elementary school level"), ("MS", "Middle school level"), ("HS", "High school level")]
OLD_YEARS = [(2008, "2007-08"), (2009, "2008-09"), (2010, "2009-10"), (2011, "2010-11")]
NEW_YEARS = ["2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]
SUBJECTS = ("reading", "math", "science", "writing")


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


def standing(vals, mine):
    """(rank from the top, districts, percentile = share at or below, ties split)."""
    n = len(vals)
    above = sum(1 for v in vals if v > mine)
    below = sum(1 for v in vals if v < mine)
    equal = n - above - below
    return above + 1, n, 100.0 * (below + 0.5 * equal) / n


def old_era():
    """Per year and level: Bourbon's four-subject average, its standing, and the reading
    and mathematics only standing as a check."""
    rows = list(csv.DictReader(open(os.path.join(HERE, "benchmarks_oea_districts_2008_2011.csv"))))
    out = {}
    for year, _ in OLD_YEARS:
        for lv, _ in LEVELS:
            four, two, state = {}, {}, None
            for r in rows:
                if int(r["year"]) != year or r["level"] != lv:
                    continue
                v = [num(r[s]) for s in SUBJECTS]
                if any(x is None for x in v):
                    continue
                if r["district"] == "Kentucky":
                    state = sum(v) / 4
                    continue
                four[r["district"]] = sum(v) / 4
                two[r["district"]] = (v[0] + v[1]) / 2
            mine4, mine2 = four["Bourbon County"], two["Bourbon County"]
            out[(year, lv)] = dict(value=mine4, state=state, rank=standing(list(four.values()), mine4),
                                   rm_value=mine2, rm_rank=standing(list(two.values()), mine2))
    return out


def new_era():
    rows = list(csv.DictReader(open(os.path.join(HERE, "kde_district_trend_levels_2021_2026.csv"))))
    out = {}
    for r in rows:
        if r["measure"] != "overall":
            continue
        key = (r["year"], r["level"])
        if r["district"] == "Bourbon County":
            out.setdefault(key, {}).update(value=num(r["value"]), rating=r["rating"],
                                           rank=(int(r["rank_from_top"]), int(r["districts"]), num(r["percentile"])))
        elif r["district"] == "Kentucky":
            out.setdefault(key, {})["state"] = num(r["value"])
    return out


class Labeler:
    """Places point labels where they do not cross the plotted lines or other labels.

    Candidates are tried in order; the first whose box (measured with the figure's
    renderer) stays inside the axes and clear of the line segments and earlier labels
    wins. Falls back to the first candidate if none is clear.
    """

    def __init__(self, fig, ax, segments, fixed_texts=()):
        self.fig, self.ax, self.segments = fig, ax, segments
        self.renderer = fig.canvas.get_renderer()
        self.boxes = [self.bbox(t) for t in fixed_texts]

    def bbox(self, t):
        return t.get_window_extent(renderer=self.renderer).transformed(self.ax.transData.inverted())

    def clear(self, bb):
        x0, x1 = self.ax.get_xlim()
        if bb.y0 < 0.5 or bb.y1 > 100 or bb.x0 < x0 or bb.x1 > x1:
            return "outside"
        pad_x, pad_y = 0.04, 0.8
        for (xa, ya), (xb, yb) in self.segments:
            for k in range(26):
                f = k / 25
                px, py = xa + f * (xb - xa), ya + f * (yb - ya)
                if bb.x0 - pad_x <= px <= bb.x1 + pad_x and bb.y0 - pad_y <= py <= bb.y1 + pad_y:
                    return "line"
        for o in self.boxes:
            if bb.x0 < o.x1 + pad_x and bb.x1 > o.x0 - pad_x and bb.y0 < o.y1 + 0.6 and bb.y1 > o.y0 - 0.6:
                return "label"
        return ""

    def try_at(self, x, y, text, ha, va, style):
        t = self.ax.text(x, y, text, ha=ha, va=va, zorder=6, bbox=BOX, **style)
        bb = self.bbox(t)
        why = self.clear(bb)
        if os.environ.get("LABEL_DEBUG"):
            print(f"  {text!r} at ({x:.2f},{y:.1f}) {ha}/{va}: box x {bb.x0:.2f}-{bb.x1:.2f} "
                  f"y {bb.y0:.1f}-{bb.y1:.1f} -> {why or 'ok'}")
        if why:
            t.remove()
            return None, bb
        return t, bb

    def place(self, x, y, text, candidates, **style):
        for dx, dy, ha, va in candidates:
            t, bb = self.try_at(x + dx, y + dy, text, ha, va, style)
            if t:
                self.boxes.append(bb)
                return t
        return None

    def block(self, x, y, pct_text, rank_text, pct_style, rank_style):
        """Both labels stacked beside the point, for points too low to label above and below."""
        base = max(0.8, y - 5.2)
        for dx in (0.2, -0.2, 0.32, -0.32):
            ha = "left" if dx > 0 else "right"
            r, rb = self.try_at(x + dx, base, rank_text, ha, "bottom", rank_style)
            if not r:
                continue
            self.boxes.append(rb)
            pt, pb = self.try_at(x + dx, rb.y1 + 0.9, pct_text, ha, "bottom", pct_style)
            if pt:
                self.boxes.append(pb)
                return True
            r.remove()
            self.boxes.pop()
        return False

    def point(self, x, rank):
        rk, n, pct = rank
        pct_style = dict(color=NAVY, fontsize=8.4, fontweight="bold")
        rank_style = dict(color=MUTED, fontsize=7.4)
        above, below = (0, 3.0, "center", "bottom"), (0, -3.0, "center", "top")
        right, left = (0.17, 0, "left", "center"), (-0.17, 0, "right", "center")
        corners = [(0.14, 2.2, "left", "bottom"), (-0.14, 2.2, "right", "bottom"),
                   (0.14, -2.2, "left", "top"), (-0.14, -2.2, "right", "top")]
        stacked = [(0, 10.4, "center", "bottom"), (0, -10.4, "center", "top")]
        pct_text, rank_text = f"{ordinal(int(round(pct)))} pct", f"{ordinal(rk)} of {n}"
        t1 = self.place(x, pct, pct_text, [above, below, right, left] + corners, **pct_style)
        # the rank goes under the point when it can; otherwise beside it, on the flatter side first
        slopes = [abs(yb - ya) for (xa, ya), (xb, yb) in self.segments if xa == x or xb == x]
        side = [right, left]
        if len(slopes) == 2 and slopes[0] < slopes[1]:
            side = [left, right]
        t2 = self.place(x, pct, rank_text, [below] + side + corners[2:] + corners[:2] + stacked, **rank_style) \
            if t1 else None
        if t1 and t2:
            return
        # no clear pair of spots: stack both beside the point instead
        for t in (t1, t2):
            if t:
                bb = self.bbox(t)
                self.boxes = [b for b in self.boxes if not (b.x0 == bb.x0 and b.y0 == bb.y0 and b.x1 == bb.x1)]
                t.remove()
        if not self.block(x, pct, pct_text, rank_text, pct_style, rank_style):
            self.ax.text(x, pct + 3.0, pct_text, ha="center", va="bottom", zorder=6, bbox=BOX, **pct_style)
            self.ax.text(x, pct + 10.4, rank_text, ha="center", va="bottom", zorder=6, bbox=BOX, **rank_style)


def panel(fig, ax, lv, title, old, new, top):
    gap = 4
    xs_old = [0, 1, 2, 3]
    xs_new = [gap + 1 + i for i in range(len(NEW_YEARS))]
    ax.axhspan(0, 25, color="#F3F5F8", zorder=0)
    ax.axhline(50, color=GRAY, lw=1.1, ls=(0, (4, 3)), zorder=1)
    ax.axvline(gap, color=LINE, lw=1.0, zorder=1)
    ys_old = [old[(y, lv)]["rank"][2] for y, _ in OLD_YEARS]
    ys_new = [new[(y, lv)]["rank"][2] for y in NEW_YEARS]
    ax.plot(xs_old, ys_old, color=NAVY, lw=2.0, zorder=3)
    ax.plot(xs_new, ys_new, color=NAVY, lw=2.0, zorder=3)
    for x, (y, _) in zip(xs_old, OLD_YEARS):
        ax.scatter([x], [old[(y, lv)]["rank"][2]], s=70, color="white", edgecolor=NAVY, linewidth=1.8, zorder=4)
    for x, y in zip(xs_new, NEW_YEARS):
        ax.scatter([x], [new[(y, lv)]["rank"][2]], s=70, color=FILL.get(new[(y, lv)]["rating"], NAVY),
                   edgecolor=NAVY, linewidth=1.6, zorder=4)
    fixed = [
        ax.text(gap, 98, "systems changed:\nno comparable\nranking 2012 to 2021", ha="center", va="top",
                color=MUTED, fontsize=6.4, linespacing=1.22, zorder=6, bbox=BOX),
        ax.text(xs_new[-1] + 0.62, 50, "median\ndistrict", color=MUTED, fontsize=7.0, ha="left", va="center"),
        ax.text(xs_new[-1] + 0.62, 15.5, "bottom\nquarter", color=MUTED, fontsize=7.0, ha="left", va="center"),
    ]
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_xlim(-0.55, xs_new[-1] + 1.35)
    ax.set_xticks(xs_old + xs_new)
    ax.set_xticklabels([lab for _, lab in OLD_YEARS] + NEW_YEARS, fontsize=7.8)
    ax.set_title(title, color=INK, fontsize=11, loc="left", pad=6, fontweight="bold")
    if top:
        ax.text(1.5, 112, "CATS era: percent proficient or distinguished,\nfour tested subjects, 174 districts",
                ha="center", va="bottom", color=INK, fontsize=8.2, linespacing=1.2, clip_on=False)
        ax.text(gap + 3, 112, "Current system: state overall accountability score,\n172 districts",
                ha="center", va="bottom", color=INK, fontsize=8.2, linespacing=1.2, clip_on=False)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color(LINE)
    ax.tick_params(colors=MUTED, labelsize=8.4, length=0)
    ax.yaxis.grid(True, color=LINE, lw=0.8)
    ax.set_axisbelow(True)
    ax.set_ylabel("Percentile among Kentucky districts", color=INK, fontsize=8.8, labelpad=6)
    segments = list(zip(zip(xs_old, ys_old), zip(xs_old[1:], ys_old[1:])))
    segments += list(zip(zip(xs_new, ys_new), zip(xs_new[1:], ys_new[1:])))
    points = [(x, old[(y, lv)]["rank"]) for x, (y, _) in zip(xs_old, OLD_YEARS)]
    points += [(x, new[(y, lv)]["rank"]) for x, y in zip(xs_new, NEW_YEARS)]
    return segments, points, fixed


def main():
    old, new = old_era(), new_era()
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5})
    fig, axes = plt.subplots(3, 1, figsize=(8.5, 11.0))
    fig.subplots_adjust(left=0.085, right=0.955, top=0.868, bottom=0.08, hspace=0.40)
    pending = []
    for ax, (lv, title) in zip(axes, LEVELS):
        pending.append((ax, panel(fig, ax, lv, title, old, new, top=(lv == "ES"))))
    fig.canvas.draw()
    for ax, (segments, points, fixed) in pending:
        lab = Labeler(fig, ax, segments, fixed)
        for x, rank in points:
            lab.point(x, rank)
    fig.suptitle("Where Bourbon County ranks among Kentucky school districts, by level",
                 x=0.06, ha="left", fontsize=13.2, color=INK, fontweight="bold", y=0.985)
    fig.text(0.06, 0.962, "Percentile and rank among Kentucky districts each year (100th percentile = top district).\n"
             "2008 to 2011 on the Kentucky Core Content Tests; 2022 to 2026 on the state's overall score.",
             fontsize=8.8, color=MUTED, ha="left", va="top", linespacing=1.3)
    fig.text(0.06, 0.012,
             "Sources: Legislative Research Commission, Kentucky District Data Profiles (research reports 360, 368, 382, "
             "392), Kentucky Core Content Test results for every district, average of reading, mathematics, science and "
             "writing percent proficient or distinguished; KDE accountability profiles 2021-22 to 2025-26, district rows, "
             "overall score by level (Accountable_Profile_2026, October 14, 2026). Percentile is the share of districts "
             "scoring at or below Bourbon County that year; 169 of the 174 districts had a high school in 2008 to 2011, "
             "168 of 172 now. Marker fill in the current system is the state's color rating for that score; the CATS era "
             "had no color ratings.",
             fontsize=6.9, color=MUTED, ha="left", va="bottom", wrap=True)
    out_png = os.path.join(HERE, "standing_by_level_2008_2026_chart.png")
    fig.savefig(out_png, dpi=200)

    # data table
    out_csv = os.path.join(HERE, "standing_by_level_2008_2026.csv")
    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year", "level", "measure", "bourbon", "kentucky", "rank_from_top", "districts", "percentile",
                    "rating", "reading_math_only_rank", "reading_math_only_percentile"])
        for year, lab in OLD_YEARS:
            for lv, _ in LEVELS:
                d = old[(year, lv)]
                w.writerow([lab, lv, "kcct_four_subject_pd", f"{d['value']:.2f}", f"{d['state']:.2f}", d["rank"][0],
                            d["rank"][1], f"{d['rank'][2]:.1f}", "", d["rm_rank"][0], f"{d['rm_rank'][2]:.1f}"])
        for year in NEW_YEARS:
            for lv, _ in LEVELS:
                d = new[(year, lv)]
                w.writerow([year, lv, "overall_score", f"{d['value']:.1f}", f"{d['state']:.1f}", d["rank"][0],
                            d["rank"][1], f"{d['rank'][2]:.1f}", d["rating"], "", ""])

    # notes
    lines = ["# Bourbon County's standing by level, 2008 to 2011 and 2022 to 2026", "",
             "One page, three panels: elementary on top, middle school in the middle, high school at the bottom. "
             "Each panel plots Bourbon County's percentile among Kentucky districts (100 = top) with the rank under "
             "every point. Chart: `build/standing_by_level_2008_2026_chart.png`. Data: "
             "`build/standing_by_level_2008_2026.csv`.", "",
             "## What is ranked in each era", "",
             "- 2008 to 2011 (CATS era): the Kentucky Core Content Test percent proficient or distinguished, averaged "
             "across the four subjects the LRC district profiles report for every district at every level (reading, "
             "mathematics, science, writing). Ranked among the 174 districts of the time; 169 had a high school. "
             "The profiles were decoded for every district by `build/parse_oea_district_profiles.py`, with the state "
             "row checked on every page, and the 2009 and 2011 reports (whose text layer is a glyph substitution) "
             "checked against the readable 2010 report district by district.",
             "- 2022 to 2026 (current system): the state's overall accountability score for the level, ranked among "
             "the 172 districts (168 with a high school). The overall score blends reading and mathematics, science, "
             "social studies and writing, English learner progress, the school climate survey and, for high school, "
             "postsecondary readiness and graduation.",
             "- The CATS academic index itself is not online for this era, and the files for the systems in between "
             "(Unbridled Learning, 2012 to 2017, and the first years of the current law, 2018 to 2021) are no longer "
             "published, so no comparable by-level district ranking exists for 2012 to 2021. The chart leaves that "
             "gap open rather than bridging it.", "",
             "## Standing each year", "",
             "| School year | Level | Measure | Bourbon | Kentucky | Rank | Districts | Percentile | Reading and math only |",
             "|---|---|---|---|---|---|---|---|---|"]
    for year, lab in OLD_YEARS:
        for lv, _ in LEVELS:
            d = old[(year, lv)]
            lines.append(f"| {lab} | {lv} | KCCT four-subject average | {d['value']:.1f} | {d['state']:.1f} | "
                         f"{ordinal(d['rank'][0])} | {d['rank'][1]} | {ordinal(int(round(d['rank'][2])))} | "
                         f"{ordinal(d['rm_rank'][0])} of {d['rm_rank'][1]}, {ordinal(int(round(d['rm_rank'][2])))} pct |")
    for year in NEW_YEARS:
        for lv, _ in LEVELS:
            d = new[(year, lv)]
            lines.append(f"| {year} | {lv} | Overall score ({d['rating']}) | {d['value']:.1f} | {d['state']:.1f} | "
                         f"{ordinal(d['rank'][0])} | {d['rank'][1]} | {ordinal(int(round(d['rank'][2])))} | |")
    lines += ["", "## Reading the chart", ""]
    for lv, title in LEVELS:
        o = [old[(y, lv)]["rank"] for y, _ in OLD_YEARS]
        n = [new[(y, lv)]["rank"] for y in NEW_YEARS]
        lines.append(f"- {title}: {ordinal(int(round(o[0][2])))} percentile in 2007-08 ({ordinal(o[0][0])} of {o[0][1]}) "
                     f"and {ordinal(int(round(o[-1][2])))} in 2010-11 ({ordinal(o[-1][0])} of {o[-1][1]}); "
                     f"{ordinal(int(round(n[0][2])))} percentile in 2021-22 ({ordinal(n[0][0])} of {n[0][1]}) and "
                     f"{ordinal(int(round(n[-1][2])))} in 2025-26 ({ordinal(n[-1][0])} of {n[-1][1]}).")
    diffs = []
    for year, lab in OLD_YEARS:
        for lv, _ in LEVELS:
            d = old[(year, lv)]
            if abs(d["rank"][2] - d["rm_rank"][2]) >= 15:
                diffs.append(f"{lv} {lab} ({ordinal(int(round(d['rank'][2])))} percentile on four subjects, "
                             f"{ordinal(int(round(d['rm_rank'][2])))} on reading and math)")
    lines += ["", "Percentile is the share of Kentucky districts scoring at or below Bourbon County that year, ties "
              "split; rank 1 is the highest district. The reading and math only column repeats the CATS-era ranking "
              "on those two subjects alone, as a check on the four-subject average. The two agree within 15 "
              "percentile points everywhere except " + ("; ".join(diffs) if diffs else "nowhere") + ". Those "
              "high school gaps come from science and writing: Bourbon's high school science ran above the state "
              "in 2008 while its reading ran well below, and in 2011 its mathematics ran above the state while its "
              "writing ran far below. The four-subject average is the closer match to today's overall score, "
              "which also counts science and writing.", ""]
    out_md = os.path.join(HERE, "standing_by_level_2008_2026.md")
    with open(out_md, "w") as f:
        f.write("\n".join(lines))
    print("wrote", out_png, out_csv, out_md)


if __name__ == "__main__":
    main()
