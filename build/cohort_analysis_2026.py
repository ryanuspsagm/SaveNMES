#!/usr/bin/env python3
"""Follow each NMES cohort through the state files, 2023-24 to 2025-26, and
separate three explanations for the 2025-26 fall: a weak cohort, a school-wide
slide, or children leaving.

Reads the Bourbon County extracts archived under build/ (KYRC24 and KYRC25
School Report Card files, the October 14, 2026 release, the SAAR enrollment
workbooks) and writes build/cohort_analysis_2025_26.md and
build/kde_grade_rows_2024_2026.json.

    python build/cohort_analysis_2026.py
"""
import csv, json, os
import xlrd

B = os.path.dirname(os.path.abspath(__file__))
SCH = {'041090': 'NMES', '041010': 'BCES', '041030': 'CRES', '478010': 'PES', '041000': 'District', '999000': 'State', '041': 'District', '999': 'State'}
LABEL = {'NMES': 'North Middletown', 'BCES': 'Bourbon Central', 'CRES': 'Cane Ridge', 'PES': 'Paris Elem.', 'District': 'BCS district', 'State': 'Kentucky'}
GR = {'Grade 3': '3', 'Grade 4': '4', 'Grade 5': '5', '3rd': '3', '4th': '4', '5th': '5', '03': '3', '04': '4', '05': '5', 'ES': 'all', 'Elementary School': 'all'}
SUBJ = {'Reading': 'Reading', 'Mathematics': 'Math', 'Science': 'Science', 'Social Studies': 'SS', 'On Demand Writing': 'ODW',
        'Editing and Mechanics': 'EM', 'Editing and Mechanic': 'EM', 'Combined Writing': 'CW'}

def num(v):
    try: return int(float(v))
    except (TypeError, ValueError): return None

def load(fn, grade_col, cols):
    out = {}
    with open(os.path.join(B, fn), newline='', encoding='utf-8-sig') as f:
        for d in csv.DictReader(f):
            if d['School Code'] not in SCH: continue
            g = GR.get(d[grade_col]); s = SUBJ.get(d['Subject'])
            if g is None or s is None: continue
            vals = [num(d[c]) for c in cols]
            out[(SCH[d['School Code']], g, s, d['Demographic'])] = None if d['Suppressed'] in ('Y', 'Yes') or any(v is None for v in vals) else vals
    return out
C24 = ['Novice', 'Apprentice', 'Proficient', 'Distinguished', 'Proficient / Distinguished']
C26 = ['Novice', 'Apprentice', 'Proficient', 'Distinguished', 'Proficient/Distinguished']
Y = {2024: {**load('kde_kyrc24_ksa_by_grade_bourbon.csv', 'Grade', C24), **load('kde_kyrc24_ksa_school_bourbon.csv', 'Level', C24)},
     2025: {**load('kde_kyrc25_ksa_by_grade_bourbon.csv', 'Grade', C24), **load('kde_kyrc25_ksa_school_bourbon.csv', 'Level', C24)},
     2026: {**load('kde_acct_2026_by_grade_bourbon.csv', 'Grade', C26), **load('kde_acct_2026_assessment_performance_bourbon.csv', 'Level', C26)}}
json.dump({str(y): {"|".join(k): v for k, v in Y[y].items() if k[3] == 'All Students'} for y in Y},
          open(os.path.join(B, 'kde_grade_rows_2024_2026.json'), 'w'), indent=0)
v = lambda y, sch, g, s, dm='All Students': Y[y].get((sch, g, s, dm))
cell = lambda x: '*' if x is None else f"{x[4]} ({x[0]})"

# SAAR enrollment by grade (end of year) for NMES, and KYRC October counts
def saar():
    out = {}
    for yr in ['2022_23', '2023_24', '2024_25', '2025_26']:
        sh = xlrd.open_workbook(os.path.join(B, f'saar_enrollment_{yr}.xls')).sheet_by_index(0)
        district = None
        for r in range(sh.nrows):
            name = str(sh.cell_value(r, 0))
            if name.endswith(' - Bourbon County') or name.endswith(' - Paris Independent'):
                district = name
            key = None
            if name.startswith('090 - North Mi'): key = 'NMES'
            elif name.startswith('010 - Bourbon C') and district and 'Bourbon' in district: key = 'BCES'
            elif name.startswith('030 - Cane Rid'): key = 'CRES'
            elif name.startswith('010 - Paris Ele') and district and 'Paris' in district: key = 'PES'
            if key:
                out.setdefault(yr.replace('_', '-'), {})[key] = [int(float(sh.cell_value(r, c) or 0)) for c in range(1, 7)] + [int(float(sh.cell_value(r, 15) or 0))]
    return out
S = saar()
def octo(fn):
    out = {}
    with open(os.path.join(B, fn), newline='', encoding='utf-8-sig') as f:
        for d in csv.DictReader(f):
            if d['School Code'] in SCH:
                out[(SCH[d['School Code']], d['Demographic'])] = [num(d[c].replace(',', '')) for c in ['K', 'Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'All Grades']]
    return out
O = {2024: octo('kde_kyrc24_enrollment_bourbon.csv'), 2025: octo('kde_kyrc25_enrollment_bourbon.csv')}

L = []
L.append("# Where the 2025-26 fall came from: NMES cohort by cohort\n")
L.append("Working note, not on the site. Sources, all archived under `build/`: KDE School Report Card files for 2023-24 (KYRC24) and 2024-25 (KYRC25), the October 14, 2026 release for 2025-26, and the SAAR enrollment workbooks (end-of-year counts by grade). Percentages are KDE's, all students unless stated; the first number in a cell is percent proficient or distinguished, the number in parentheses percent novice; asterisks are KDE-suppressed cells. Regenerate with `python build/cohort_analysis_2026.py`.\n")

L.append("## 1. Every grade, three years\n")
for s in ['Reading', 'Math']:
    L.append(f"**{s}**\n")
    L.append("| Grade | Year | " + " | ".join(LABEL[k] for k in ['NMES', 'BCES', 'CRES', 'PES', 'District', 'State']) + " |")
    L.append("|---|---|" + "---|" * 6)
    for g in ['3', '4', '5']:
        for y in [2024, 2025, 2026]:
            L.append(f"| {g} | {y} | " + " | ".join(cell(v(y, k, g, s)) for k in ['NMES', 'BCES', 'CRES', 'PES', 'District', 'State']) + " |")
    L.append("")
L.append("**Single-grade subjects** (science is a 4th-grade test; social studies, on-demand writing and editing and mechanics are 5th-grade tests)\n")
L.append("| Subject | Year | " + " | ".join(LABEL[k] for k in ['NMES', 'BCES', 'CRES', 'PES', 'District', 'State']) + " |")
L.append("|---|---|" + "---|" * 6)
for s, g, name in [('Science', '4', 'Science, grade 4'), ('SS', '5', 'Social studies, grade 5'), ('ODW', '5', 'On-demand writing, grade 5'), ('EM', '5', 'Editing and mechanics, grade 5')]:
    for y in [2024, 2025, 2026]:
        L.append(f"| {name} | {y} | " + " | ".join(cell(v(y, k, g, s)) for k in ['NMES', 'BCES', 'CRES', 'PES', 'District', 'State']) + " |")
L.append("")

L.append("## 2. The same children, year to year\n")
L.append("Cohorts are named by the spring they were in third grade. Reading the rows across follows one group of children; the comparison schools and the state show how much a cohort normally moves from one grade to the next.\n")
for s in ['Reading', 'Math']:
    L.append(f"**{s}**\n")
    L.append("| Cohort | Grade and year | " + " | ".join(LABEL[k] for k in ['NMES', 'BCES', 'CRES', 'PES', 'District', 'State']) + " |")
    L.append("|---|---|" + "---|" * 6)
    for c3, path in [(2023, [(2024, '4'), (2025, '5')]), (2024, [(2024, '3'), (2025, '4'), (2026, '5')]), (2025, [(2025, '3'), (2026, '4')]), (2026, [(2026, '3')])]:
        for (y, g) in path:
            L.append(f"| 3rd grade in {c3} | grade {g}, {y} | " + " | ".join(cell(v(y, k, g, s)) for k in ['NMES', 'BCES', 'CRES', 'PES', 'District', 'State']) + " |")
    L.append("")

# implied suppressed cells from school totals and SAAR grade sizes
def rng(p, n): return (max(0.0, (p - 0.5) / 100 * n), (p + 0.5) / 100 * n)
n25 = S['2024-25']['NMES'][3:6]; n26 = S['2025-26']['NMES'][3:6]
L.append("## 3. Filling in the suppressed cells from the school totals\n")
L.append(f"KDE suppresses a grade when a performance level holds fewer than three children, but it still publishes the whole-school figure, and the grade sizes are public (SAAR end-of-year counts: {n25[0]}, {n25[1]} and {n25[2]} in grades 3 to 5 in 2024-25; {n26[0]}, {n26[1]} and {n26[2]} in 2025-26). Subtracting the published grades from the school total brackets the suppressed one.\n")
L.append("| Quantity | Reading | Math |")
L.append("|---|---|---|")
rows = {}
for s, all25, g4_25, g5_25, all26, g3_26, g4_26 in [('Reading', 41, 47, 54, 21, 18, None), ('Math', 31, 41, 46, 23, 14, 26)]:
    t25 = rng(all25, sum(n25)); c4 = rng(g4_25, n25[1]); c5 = rng(g5_25, n25[2])
    g3lo, g3hi = max(0, t25[0] - c4[1] - c5[1]), t25[1] - c4[0] - c5[0]
    t26 = rng(all26, sum(n26)); c3 = rng(g3_26, n26[0])
    rlo, rhi = max(0, t26[0] - c3[1]), t26[1] - c3[0]
    rows.setdefault('2024-25 third grade, suppressed', []).append(f"{g3lo / n25[0]:.0%} to {g3hi / n25[0]:.0%} proficient")
    rows.setdefault('2025-26 grades 4 and 5 together', []).append(f"{rlo / (n26[1] + n26[2]):.0%} to {rhi / (n26[1] + n26[2]):.0%} proficient")
    if g4_26 is not None:
        c4n = rng(g4_26, n26[1]); g5lo, g5hi = max(0, rlo - c4n[1]), rhi - c4n[0]
        rows.setdefault('2025-26 fifth grade, suppressed', []).append(f"{g5lo / n26[2]:.0%} to {g5hi / n26[2]:.0%} proficient (same children: {g4_25}% in 4th grade)")
    else:
        rows.setdefault('2025-26 fifth grade, suppressed', []).append(f"not separable from 4th grade; the two together are {rlo / (n26[1] + n26[2]):.0%} to {rhi / (n26[1] + n26[2]):.0%} (same children: {g4_25}% and {g3lo / n25[0]:.0%} to {g3hi / n25[0]:.0%} a year earlier)")
    b_rate = ((g3lo + g3hi) / 2) / n25[0]
    cf = (c3[0] + c3[1]) / 2 + g4_25 / 100 * n26[2] + b_rate * n26[1]
    rows.setdefault('School figure if the continuing cohorts had held their 2024-25 rates', []).append(f"{cf / sum(n26):.0%} (actual {all26}%)")
    rows.setdefault('Share of the fall from swapping the departing 5th grade for the new 3rd grade', []).append(f"{all25 - round(cf / sum(n26) * 100)} of {all25 - all26} points")
    rows.setdefault('Share of the fall from the continuing cohorts themselves', []).append(f"{round(cf / sum(n26) * 100) - all26} of {all25 - all26} points")
for k, vals in rows.items():
    L.append(f"| {k} | " + " | ".join(vals) + " |")
L.append("")

L.append("## 4. Who was enrolled\n")
L.append("October counts from the School Report Card enrollment file, end-of-year counts from the SAAR. Grades 3 to 5 are the tested grades.\n")
L.append("| NMES | K | 1 | 2 | 3 | 4 | 5 | All |")
L.append("|---|---|---|---|---|---|---|---|")
for lab, arr in [('October 2023', O[2024][('NMES', 'All Students')]), ('End of 2023-24', S['2023-24']['NMES']), ('October 2024', O[2025][('NMES', 'All Students')]), ('End of 2024-25', S['2024-25']['NMES']), ('End of 2025-26', S['2025-26']['NMES'])]:
    L.append(f"| {lab} | " + " | ".join(str(x) for x in arr) + " |")
L.append("")
L.append("Within-year change, October to June, all grades: " + "; ".join(f"{LABEL[k]} 2023-24 {S['2023-24'][k][6] - O[2024][(k, 'All Students')][6]:+d} of {O[2024][(k, 'All Students')][6]}, 2024-25 {S['2024-25'][k][6] - O[2025][(k, 'All Students')][6]:+d} of {O[2025][(k, 'All Students')][6]}" for k in ['NMES', 'BCES', 'CRES', 'PES']) + ".\n")
L.append("| NMES, October counts | 2023-24 | 2024-25 |")
L.append("|---|---|---|")
for dm in ['Economically Disadvantaged', 'Students with Disabilities (IEP)', 'Homeless', 'English Learner', 'Hispanic or Latino', 'Male', 'Female', 'Gifted and Talented']:
    a, b = O[2024].get(('NMES', dm)), O[2025].get(('NMES', dm))
    f = lambda arr: f"{arr[6]} of {O[2024][('NMES','All Students')][6] if arr is a else O[2025][('NMES','All Students')][6]} ({arr[6] / (O[2024][('NMES','All Students')][6] if arr is a else O[2025][('NMES','All Students')][6]):.0%})" if arr and arr[6] is not None else 'n/a'
    L.append(f"| {dm} | {f(a)} | {f(b)} |")
L.append("")

L.append("## 5. Subgroups at the school level\n")
L.append("| NMES, reading | 2023-24 | 2024-25 | 2025-26 |")
L.append("|---|---|---|---|")
DM = [('All Students', 'All students'), ('Economically Disadvantaged', 'Economically disadvantaged'), ('Student without Disabilities (IEP)', 'Without an IEP'), ('Students without IEP', 'Without an IEP'), ('Male', 'Boys'), ('Female', 'Girls'), ('White (non-Hispanic)', 'White'), ('White (Non-Hispanic)', 'White')]
seen = set()
for s in ['Reading', 'Math']:
    if s == 'Math':
        L.append(""); L.append("| NMES, math | 2023-24 | 2024-25 | 2025-26 |"); L.append("|---|---|---|---|")
    seen = set()
    for key, lab in DM:
        if lab in seen: continue
        vals = []
        for y in [2024, 2025, 2026]:
            x = None
            for k2, l2 in DM:
                if l2 == lab and (('NMES', 'all', s, k2) in Y[y]):
                    x = Y[y][('NMES', 'all', s, k2)]; break
            vals.append(cell(x) if any(l2 == lab and ('NMES', 'all', s, k2) in Y[y] for k2, l2 in DM) else 'no row')
        seen.add(lab)
        L.append(f"| {lab} | " + " | ".join(vals) + " |")
L.append("")

L.append("## 6. Staff, attendance, participation\n")
def tt(fn):
    with open(os.path.join(B, fn), newline='', encoding='utf-8-sig') as f:
        return {SCH[d['School Code']]: (d['Teacher Count'], d['Teacher Turnover Count'], d['Turnover Percent']) for d in csv.DictReader(f) if d['School Code'] in SCH}
T = {2024: tt('kde_kyrc24_teacher_turnover_bourbon.csv'), 2025: tt('kde_kyrc25_teacher_turnover_bourbon.csv')}
def ca(fn):
    with open(os.path.join(B, fn), newline='', encoding='utf-8-sig') as f:
        return {(SCH[d['School Code']], d['Grade']): (d['Chronically Absent Students'], d['Chronic Absenteeism Rate']) for d in csv.DictReader(f) if d['School Code'] in SCH}
A = {2024: ca('kde_kyrc24_chronic_absenteeism_bourbon.csv'), 2025: ca('kde_kyrc25_chronic_absenteeism_bourbon.csv')}
L.append("| School | Teachers, 2024-25 | Turnover into 2023-24 | Turnover into 2024-25 | Chronic absenteeism 2023-24 | 2024-25 | Students taught by inexperienced teachers, 2024-25 |")
L.append("|---|---|---|---|---|---|---|")
with open(os.path.join(B, 'kde_kyrc25_inexperienced_teachers_bourbon.csv'), newline='', encoding='utf-8-sig') as f:
    IX = {SCH[d['School Code']]: d['All Students'] for d in csv.DictReader(f) if d['School Code'] in SCH}
for k in ['NMES', 'BCES', 'CRES', 'PES']:
    L.append(f"| {LABEL[k]} | {T[2025][k][0]} | {T[2024][k][2]}% ({T[2024][k][1]} of {T[2024][k][0]}) | {T[2025][k][2]}% ({T[2025][k][1]} of {T[2025][k][0]}) | {A[2024][(k, 'All Grades')][1]}% | {A[2025][(k, 'All Grades')][1]}% | {IX.get(k, 'n/a')}% |")
L.append("")
L.append(f"NMES chronic absenteeism by grade, 2024-25 (children absent 10 percent or more of enrolled days): K {A[2025][('NMES','K')][0]}, 1st {A[2025][('NMES','1st')][0]}, 2nd {A[2025][('NMES','2nd')][0]}, 3rd {A[2025][('NMES','3rd')][0]}, 4th {A[2025][('NMES','4th')][0]}, 5th {A[2025][('NMES','5th')][0]} of October counts of {', '.join(str(x) for x in O[2025][('NMES','All Students')][:6])}. KSA participation at NMES was 100 percent in reading and math in both 2023-24 and 2024-25 (KYRC participation files). Retention in grades 4 and up in 2024-25: none. KDE's turnover figure for a year is the share of the prior year's teachers who did not return; the figure that would show who left after 2024-25 is published with the 2025-26 report card later this fall.\n")

L.append("## 7. Reading\n")
L.append("- **Not one bad cohort, and not a school-wide slide either: it is two separate things at once.** Swapping the departing fifth grade (54 percent proficient in reading, 46 in math) for the incoming third grade (18 and 14) accounts for about 13 of the 20 reading points and for all of the math fall; in math the continuing cohorts actually improved on net. The rest of the reading fall sits in the fifth grade.")
L.append("- **The fifth grade of 2025-26 is the anomaly.** Those children scored 47 percent proficient in reading and 41 in math as fourth graders in 2025, with 53 percent proficient in science, the best fourth grade in the county. A year later the bracketing puts them near 25 to 31 percent in math and the fourth-and-fifth-grade pair at 21 to 23 percent in reading, while editing and mechanics fell to 16 percent against 50 and 52 for the two previous fifth grades, and the writing and social studies indexes fell from 77 and 47 to 25 and 22. Cohorts at the comparison schools moved by at most seven points between fourth and fifth grade. A drop of this size, in every subject, in one classroom-year, points at that classroom: a teacher change, a long-term substitute, or a disrupted year. The public record cannot yet say which; the 2025-26 turnover figure will.")
L.append("- **The fourth grade did well.** The same cohort that was suppressed as third graders in 2025 (bracketed at 3 to 8 percent proficient in math) reached 26 percent in math as fourth graders, a larger gain than any comparison school's cohort made. Whatever went wrong in 2025-26, it did not go wrong in every room.")
L.append("- **The entry grade is the slow problem.** NMES's third graders have come in weaker three years running, 29 percent proficient in reading in 2024 (a class of 15), about 20 percent in 2025, 18 percent in 2026 with 64 percent novice, while the district's third grade rose from 30 to 38. That is a kindergarten-through-second-grade question, of instruction or of who enrolls: the 2026 third graders were the first-grade class of 2023-24, which carried 8 homeless children of 27 and 8 chronically absent. It is the one systemic signal in the file, and it predates this year.")
L.append("- **Children leaving does not explain 2025-26.** NMES lost 17 children between October 2024 and June 2025 (12 percent, against 1 to 7 percent at the other three schools), mostly in kindergarten, first and third grade, before the strong spring 2025 tests. Between the two tests the tested cohorts held or grew: the children in grades 2, 3 and 4 in October 2024 numbered 20, 26 and 19, and those same cohorts numbered 19, 24 and 19 at the end of 2025-26. Net departures were small. What the public file cannot show is churn, leavers replaced by arrivals, which would matter most in the fifth-grade room; that is a records question.")
L.append("- **What else is ruled out.** Participation was 100 percent in both prior years. Every NMES teacher in 2024-25 was experienced. Turnover into 2024-25 was 2 of 9. Chronic absenteeism in the tested grades was moderate (6, 3 and 5 children). Retention was zero. The district's own grades were flat, so it is not the test.\n")
L.append("## 8. What would settle the fifth-grade question\n")
L.append("Records request, location 090: the certified staff roster for 2024-25 and 2025-26 by grade assignment with separation dates and any long-term substitute assignments; withdrawals and new enrollments by grade and month for 2025-26; chronic absenteeism by grade for 2025-26; and the district's fall, winter and spring benchmark results for the fifth grade. The 2025-26 School Report Card, due later this fall, will publish teacher turnover and absenteeism without a request.\n")
open(os.path.join(B, 'cohort_analysis_2025_26.md'), 'w').write("\n".join(L))
print("wrote", os.path.join(B, 'cohort_analysis_2025_26.md'))
