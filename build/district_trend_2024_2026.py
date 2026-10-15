#!/usr/bin/env python3
"""Three-year trend for Bourbon County Middle School and Bourbon County High
School (with Paris and the state for comparison), from the archived KDE rows:
subject results and the accountability profile, 2023-24 to 2025-26.

    python build/district_trend_2024_2026.py   -> build/district_trend_2024_2026.md
"""
import csv, os
B = os.path.dirname(os.path.abspath(__file__))
SCH = {'041120': 'BCMS', '041110': 'BCHS', '478030': 'PMS', '478020': 'PHS', '041010': 'BCES', '041030': 'CRES', '041090': 'NMES', '999000': 'State', '999': 'State'}
LABEL = {'BCMS': 'Bourbon County Middle', 'BCHS': 'Bourbon County High', 'PMS': 'Paris Middle', 'PHS': 'Paris High', 'State': 'Kentucky'}
LEVEL = {'Middle School': 'MS', 'High School': 'HS', 'Elementary School': 'ES', 'MS': 'MS', 'HS': 'HS', 'ES': 'ES'}
SUBJ = {'Reading': 'Reading', 'Mathematics': 'Math', 'Science': 'Science', 'Social Studies': 'Social Studies', 'Combined Writing': 'Writing'}
def f(x):
    try: return float(x)
    except (TypeError, ValueError): return None
def norm(d):  # case-insensitive column access
    return {k.strip().lower(): v for k, v in d.items()}

def load_ksa(fn):
    out = {}
    with open(os.path.join(B, fn), newline='', encoding='utf-8-sig') as fh:
        for d in csv.DictReader(fh):
            n = norm(d)
            code = n['school code']; lvl = LEVEL.get(n['level']); s = SUBJ.get(n['subject'])
            if code not in SCH or lvl is None or s is None or n['demographic'] != 'All Students': continue
            sup = n['suppressed'] in ('Y', 'Yes')
            pd = n.get('proficient / distinguished', n.get('proficient/distinguished'))
            out[(SCH[code], lvl, s)] = {'pd': None if sup else f(pd), 'nov': None if sup else f(n['novice']), 'ci': f(n['content index'])}
    return out
K = {2024: load_ksa('kde_kyrc24_ksa_school_bourbon.csv'), 2025: load_ksa('kde_kyrc25_ksa_school_bourbon.csv'), 2026: load_ksa('kde_acct_2026_assessment_performance_bourbon.csv')}

def load_profile(fn):
    out = {}
    with open(os.path.join(B, fn), newline='', encoding='utf-8-sig') as fh:
        for d in csv.DictReader(fh):
            n = norm(d); code = n['school code']; lvl = LEVEL.get(n['level'])
            if code not in SCH or lvl is None: continue
            g = lambda *keys: next((n[k] for k in keys if k in n and n[k] != ''), '')
            out[(SCH[code], lvl)] = {
                'overall': g('overall combined indicator rate'), 'rating': g('overall indicator rating'),
                'fed': g('federal classification'), 'reason': g('reason for federal classification', 'reason for federal classifcation'),
                'rm': g('reading_math status', 'reading_mathematics status'), 'rm_rating': g('reading_math status rating', 'reading_mathematics statue rating'),
                'sw': g('science_social studies_combined writing status'), 'sw_rating': g('science_social studies_combined writing status rating', 'science_social studies_combined writing statue rating'),
                'q': g('quality of school climate and safety status'), 'ps': g('postsecondary status'), 'ps_rating': g('postsecondary status rating', 'postsecondary statue rating'),
                'gr': g('graduation status'), 'gr_rating': g('graduation status rating', 'graduation statue rating'),
                'rm_change': g('reading_math change', 'reading_mathematics change'), 'sw_change': g('science_social studies_combined writing change')}
    return out
P = {2024: load_profile('kde_kyrc24_profile_bourbon.csv'), 2025: load_profile('kde_kyrc25_profile_bourbon.csv'), 2026: load_profile('kde_acct_2026_profile_bourbon.csv')}
COLOR = {'1': 'red', '2': 'orange', '3': 'yellow', '4': 'green', '5': 'blue'}
LV = {'1': 'very low', '2': 'low', '3': 'medium', '4': 'high', '5': 'very high'}

L = ["# Bourbon County Middle and High School on the state tests, 2023-24 to 2025-26\n",
     "Working note. Sources archived under `build/`: KDE School Report Card files for 2023-24 (KYRC24) and 2024-25 (KYRC25) and the October 14, 2026 release; Bourbon County, Paris Independent and state rows. All students. Cells read percent proficient or distinguished (percent novice) and, in the second table, KDE's content index. Regenerate with `python build/district_trend_2024_2026.py`.\n"]
for lvl, schools in [('MS', ['BCMS', 'PMS', 'State']), ('HS', ['BCHS', 'PHS', 'State'])]:
    L.append(f"## {'Middle school' if lvl == 'MS' else 'High school'}: percent proficient or distinguished (novice)\n")
    L.append("| Subject | " + " | ".join(f"{LABEL[s]} 2024 | 2025 | 2026" for s in schools) + " |")
    L.append("|---|" + "---|" * (3 * len(schools)))
    for s in SUBJ.values():
        row = []
        for sch in schools:
            for y in (2024, 2025, 2026):
                e = K[y].get((sch, lvl, s))
                row.append('n/a' if e is None else ('*' if e['pd'] is None else f"{e['pd']:.0f} ({e['nov']:.0f})"))
        L.append(f"| {s} | " + " | ".join(row) + " |")
    L.append("")
    L.append(f"## {'Middle school' if lvl == 'MS' else 'High school'}: content index (status by subject)\n")
    L.append("| Subject | " + " | ".join(f"{LABEL[s]} 2024 | 2025 | 2026 | change" for s in schools) + " |")
    L.append("|---|" + "---|" * (4 * len(schools)))
    for s in SUBJ.values():
        row = []
        for sch in schools:
            vals = [K[y].get((sch, lvl, s), {}).get('ci') for y in (2024, 2025, 2026)]
            row += ['n/a' if v is None else f"{v:.1f}" for v in vals]
            row.append('n/a' if vals[0] is None or vals[2] is None else f"{vals[2] - vals[0]:+.1f}")
        L.append(f"| {s} | " + " | ".join(row) + " |")
    L.append("")
    L.append(f"## {'Middle school' if lvl == 'MS' else 'High school'}: accountability profile\n")
    L.append("| Measure | " + " | ".join(f"{LABEL[s]} 2024 | 2025 | 2026" for s in schools) + " |")
    L.append("|---|" + "---|" * (3 * len(schools)))
    rows = [('Official overall score (color)', lambda p: f"{p['overall']} ({COLOR.get(p['rating'], '')})"),
            ('Reading and math status (level)', lambda p: f"{p['rm']} ({LV.get(p['rm_rating'], '')})"),
            ('Science, social studies, writing status (level)', lambda p: f"{p['sw']} ({LV.get(p['sw_rating'], '')})"),
            ('Climate and safety survey status', lambda p: p['q'])]
    if lvl == 'HS':
        rows += [('Postsecondary readiness status (level)', lambda p: f"{p['ps']} ({LV.get(p['ps_rating'], '')})"),
                 ('Graduation rate status (level)', lambda p: f"{p['gr']} ({LV.get(p['gr_rating'], '')})")]
    rows.append(('Federal classification', lambda p: (p['fed'] + (' (' + p['reason'] + ')' if p['reason'] else '')) or 'none'))
    for label, fn in rows:
        row = []
        for sch in schools:
            for y in (2024, 2025, 2026):
                p = P[y].get((sch, lvl)); row.append('n/a' if p is None else fn(p))
        L.append(f"| {label} | " + " | ".join(row) + " |")
    L.append("")
open(os.path.join(B, 'district_trend_2024_2026.md'), 'w').write("\n".join(L))
print("wrote", os.path.join(B, 'district_trend_2024_2026.md'))
