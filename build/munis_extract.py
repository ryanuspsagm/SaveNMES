#!/usr/bin/env python3
"""Extract North Middletown's FY2026 General Fund actuals from the district's
own MUNIS ledger (build/munis_cost_by_org_fy2026.pdf, the 203-page Cost by ORG
transaction detail produced July 2026 in response to an open records request).

Every parsed transaction carries the full MUNIS account string
FUND-ORG-FUNCTION-...-OBJECT plus a signed amount. The parse is validated
against the report's own first-page summary: the six school orgs sum to
$21,482,444.56 and org 090 (NMES) to $1,285,310.36, both reproduced to the
penny before anything downstream is written.

Outputs build/munis_nmes_fy2026.json: NMES fund 1 (General Fund) totals by
function and by function+object, the derived program table used on the site,
and the fixed-position base used by the closure grid.

Run:  python build/munis_extract.py
"""
import collections
import json
import os
import re

from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
ACCT = re.compile(r"(\d{1,2})\s+-(\d{3})-(\d{4})-(\d{3,4})-(\d{2})-(\d{4})")
AMT = re.compile(r"(-?[\d,]+\.\d{2})\s+[YN]\b")

rows = []
for page in PdfReader(os.path.join(HERE, "munis_cost_by_org_fy2026.pdf")).pages:
    for line in (page.extract_text() or "").split("\n"):
        if "TOTAL" in line.upper():
            continue
        m = ACCT.search(line)
        if not m:
            continue
        a = AMT.search(line[m.end():])
        if not a:
            continue
        fund, org, func, _prog, _x, obj = m.groups()
        rows.append((fund, org, func, obj, float(a.group(1).replace(",", ""))))

by_org = collections.defaultdict(float)
for _f, o, _fn, _ob, v in rows:
    by_org[o] += v
assert round(sum(by_org.values()), 2) == 21_482_444.56, sum(by_org.values())
assert round(by_org["090"], 2) == 1_285_310.36, by_org["090"]

nmes_gf = [(fn, ob, v) for f, o, fn, ob, v in rows if o == "090" and f == "1"]
func = collections.defaultdict(float)
func_obj = collections.defaultdict(float)
for fn, ob, v in nmes_gf:
    func[fn] += v
    func_obj[fn + "-" + ob] += v
total = sum(v for _, _, v in nmes_gf)
assert round(total, 2) == 933_537.06, total

# custodial block inside plant O&M (2610): its payroll and payroll-driven
# benefit objects; everything else in 2610 is the building itself
CUST_OBJS = {"0130", "0221", "0222", "0232"}
custodial = sum(v for fn, ob, v in nmes_gf if fn == "2610" and ob in CUST_OBJS)
building = func["2610"] - custodial
admin = func["2410"] + func.get("2420", 0.0)
library = func["2222"]
fixed_positions = admin + custodial + library
assert round(custodial, 2) == 49_655.38, custodial
assert round(building, 2) == 79_211.17, building
assert round(admin, 2) == 115_397.25, admin
assert round(library, 2) == 49_051.77, library
assert round(fixed_positions, 2) == 214_104.40, fixed_positions

out = {
    "source": "District MUNIS ledger, Cost by ORG transaction detail, FY2026 "
              "(produced July 2026; archived as build/munis_cost_by_org_fy2026.pdf). "
              "Parse validated to the penny against the report's own org summary: "
              "six school orgs $21,482,444.56; org 090 (NMES) $1,285,310.36.",
    "scope": "Org 090, fund 1 (General Fund) only: $933,537.06. Excludes fund 2 "
             "federal/grant money ($231,623), fund 51 food service ($418,529) and "
             "fund 21 activity ($21,150), and carries no on-behalf objects, the "
             "same scope as the FY2026 working-budget table it replaces ($938,690, "
             "a 0.55 percent difference).",
    "nmes_gf_total": round(total, 2),
    "by_function": {fn: round(v, 2) for fn, v in sorted(func.items())},
    "by_function_object": {k: round(v, 2) for k, v in sorted(func_obj.items())
                           if abs(v) > 0.005},
    "derived": {
        "school_administration_2410_2420": round(admin, 2),
        "custodial_within_2610": round(custodial, 2),
        "building_within_2610": round(building, 2),
        "library_2222": round(library, 2),
        "fixed_positions_base": round(fixed_positions, 2),
    },
    "retrieved": "2026-08-02",
}
with open(os.path.join(HERE, "munis_nmes_fy2026.json"), "w") as f:
    json.dump(out, f, indent=1)
print(f"NMES GF total {total:,.2f} | fixed positions {fixed_positions:,.2f} "
      f"| building {building:,.2f}")
