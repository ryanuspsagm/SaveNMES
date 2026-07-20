from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

CUR = '$#,##0;($#,##0);"-"'
PCT = '0.0%'
NUM = '#,##0;(#,##0);"-"'
BLUE = Font(name="Arial", size=10, color="0000FF")
BLK = Font(name="Arial", size=10)
GRN = Font(name="Arial", size=10, color="008000")
BOLD = Font(name="Arial", size=10, bold=True)
BOLDW = Font(name="Arial", size=11, bold=True, color="FFFFFF")
TITLE = Font(name="Arial", size=13, bold=True, color="1F3864")
SEC = Font(name="Arial", size=10, bold=True, color="1F3864")
NOTE = Font(name="Arial", size=9, italic=True, color="555555")
YEL = PatternFill("solid", fgColor="FFFF00")
HDR = PatternFill("solid", fgColor="1F3864")
LT = PatternFill("solid", fgColor="E8EDF5")
TOPLINE = Border(top=Side(style="thin", color="1F3864"))

wb = Workbook()

def sheet(name, widths):
    ws = wb.create_sheet(name)
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    return ws

def put(ws, cell, val, font=BLK, fmt=None, fill=None, bold=False, wrap=False):
    c = ws[cell]
    c.value = val
    c.font = BOLD if bold else font
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
    if wrap: c.alignment = Alignment(wrap_text=True, vertical="top")
    return c

# ================= README =================
rm = sheet("ReadMe", [110])
put(rm, "A1", "Saving North Middletown Elementary School — Financial Model", TITLE)
put(rm, "A2", "Companion workbook to the July 2026 report 'A Deep Dive into Bourbon County Schools' (Bourbon County, Kentucky)", NOTE)
rows = [
 "",
 "PURPOSE",
 "This workbook backs up every calculation in the PDF report: the district's three-year General Fund picture, the net-savings test of the",
 "closure proposal, the 'grow the Kings' nonresident-enrollment model, the alternatives menu, the bond schedule, and a reserve-runway",
 "projection. Every output is a live formula; change the blue inputs or yellow judgment cells and the model recalculates.",
 "",
 "HOW TO READ THE CELLS",
 "  Blue text  = a hardcoded input you can edit (audited figures, state data, or scenario levers; source noted alongside).",
 "  Black text = a formula. Do not overwrite.",
 "  Green text = a value pulled from another sheet in this workbook.",
 "  Yellow fill = a key judgment call or estimate the district should replace with actual data. Review these first.",
 "",
 "SOURCES (full citations in the PDF report)",
 "  Audited figures: Bourbon County School District audited financial statements, FY2023-24 and FY2024-25 (posted by KDE).",
 "  Per-pupil spending: Kentucky School Report Card school-level (ESSA) expenditure data, 2023-24.",
 "  SEEK base amounts: Kentucky 2024-2026 and 2026-2028 state budgets. Enrollment/capacity: NCES; 2021 KBE-approved facility plan.",
 "  Multi-year school scores and NMES enrollment history: School_Data tab (backs report Figures 6, 7, and 11).",
 "  County demographics and the full 1989-2025 NMES enrollment series: Demographics tab (backs Section 9 and Figure 11).",
 "  Tax rates, fund split, delinquency check, and the 4% three-year path: Tax_History tab (backs Figure 15).",
 "  Boundary rebalancing and fill-to-capacity scenario: Redistricting tab (backs the Section 9 worked example and Figure 12).",
 "  Bonding capacity components and what closure can and cannot change: Debt_Service tab (backs Section 6).",
 "  Student density, route-mile math, and busing cost scenarios: Transport_Geo tab (backs Section 9).",
 "",
 "CAVEAT",
 "Prepared by a former NMES King working alongside Fable 5, an AI research assistant from Anthropic. Estimates are labeled; every figure",
 "should be re-verified against the cited primary sources before formal use. Nothing here alleges misconduct by any official.",
]
r = 3
for t in rows:
    if t in ("PURPOSE", "HOW TO READ THE CELLS", "SOURCES (full citations in the PDF report)", "CAVEAT"):
        put(rm, f"A{r}", t, SEC)
    elif t.startswith("  Blue"):
        put(rm, f"A{r}", t, BLUE)
    elif t.startswith("  Green"):
        put(rm, f"A{r}", t, GRN)
    elif t.startswith("  Yellow"):
        put(rm, f"A{r}", t, BLK, fill=YEL)
    else:
        put(rm, f"A{r}", t, BLK if not t.startswith("  ") else NOTE)
    r += 1

# ================= ASSUMPTIONS =================
a = sheet("Assumptions", [52, 16, 60])
put(a, "A1", "Assumptions & Inputs", TITLE)
put(a, "A2", "Edit blue cells. Yellow cells are judgment calls/estimates — the district should replace them with actuals.", NOTE)

def arow(rr, label, val, fmt=CUR, src="", font=BLUE, fill=None, formula=False):
    put(a, f"A{rr}", label)
    put(a, f"B{rr}", val, font=BLK if formula else font, fmt=fmt, fill=fill)
    if src: put(a, f"C{rr}", src, NOTE)

put(a, "A4", "STATE FUNDING (SEEK base guarantee per pupil)", SEC)
arow(5,  "SEEK base, FY2026", 4586, CUR, "2024-2026 KY budget (HB 6); KDE SEEK files")
arow(6,  "SEEK base, FY2027", 4626, CUR, "2026-2028 KY budget (HB 500)")
arow(7,  "SEEK base, FY2028", 4792, CUR, "2026-2028 KY budget (HB 500)")
arow(8,  "SEEK base, FY2029 (held flat at FY2028)", "=B7", CUR, "Assumption", formula=True)

put(a, "A10", "NORTH MIDDLETOWN ELEMENTARY", SEC)
arow(11, "Enrollment, 2024-25", 128, NUM, "NCES CCD official count. Supt. has said 'around 100'; a '118' figure could not be verified in any official record")
arow(12, "Rated capacity", 174, NUM, "2021 KBE-approved District Facility Plan. A policy output, not a physical constant: the same building held 261 students in 1988-89. See report Section 7")
arow(13, "Open seats", "=B12-B11", NUM, "", formula=True)
arow(14, "Per-pupil spending, total (2023-24)", 19348, CUR, "KY School Report Card, ESSA school-level data")
arow(15, "Per-pupil spending, state/local share", 14173, CUR, "KY School Report Card, ESSA school-level data")
arow(16, "Classroom teachers (FTE)", 9.41, '0.00', "NCES")

put(a, "A18", "DISTRICT GENERAL FUND (audited)", SEC)
arow(19, "Revenues before transfers, FY2023", 27668655, CUR, "FY2024 audit (comparative)")
arow(20, "Revenues before transfers, FY2024", 24952644, CUR, "FY2024 audit")
arow(21, "Revenues before transfers, FY2025", 26449318, CUR, "FY2025 audit")
arow(22, "Expenditures before transfers, FY2023", 27905775, CUR, "FY2024 audit (comparative)")
arow(23, "Expenditures before transfers, FY2024", 27487732, CUR, "FY2024 audit")
arow(24, "Expenditures before transfers, FY2025", 29097404, CUR, "FY2025 audit")
arow(25, "Net transfers & other sources, FY2024", 1469431, CUR, "FY2024 audit")
arow(26, "Net transfers & other sources, FY2025", 1422621, CUR, "FY2025 audit")
arow(27, "Ending fund balance, FY2023", 6582802, CUR, "FY2024 audit")
arow(28, "Ending fund balance, FY2024", 5516305, CUR, "FY2024 audit")
arow(29, "Ending fund balance, FY2025", 4290840, CUR, "FY2025 audit")
arow(30, "Unassigned fund balance, FY2025", 3925193, CUR, "FY2025 audit")
arow(31, "Required contingency (share of spending)", 0.02, PCT, "Kentucky 2% statutory minimum")

put(a, "A33", "LOCAL REVENUE", SEC)
arow(34, "Property assessment, FY2025", 1843569625, CUR, "FY2025 audit MD&A")
arow(35, "GF property tax collected, FY2025", 7829060, CUR, "FY2025 audit")
arow(36, "Annual levy adjustment (KRS 160.470)", 0.04, PCT, "Board lever; up to 4% without recall")
arow(37, "Uncollected (delinquent) property tax, FY2024", 387840, CUR, "Calc yield $10,556,809 vs actual $10,168,969; ~3.7% delinquency, not foregone levy authority")
arow(38, "Uncollected (delinquent) property tax, FY2025", 239126, CUR, "Calc yield $9,880,143 vs actual $9,641,017; ~2.4% delinquency, not foregone levy authority")

put(a, "A40", "COST STRUCTURE", SEC)
arow(41, "Loaded cost per certified position (est.)", 85000, CUR, "Estimate — replace with district payroll data", fill=YEL)
arow(42, "Transportation expense, FY2025", 2913654, CUR, "FY2025 audit")
arow(43, "Transport optimization, low", 0.05, PCT, "Estimate", fill=YEL)
arow(44, "Transport optimization, high", 0.10, PCT, "Estimate", fill=YEL)
arow(45, "District administration expense, FY2023", 999727, CUR, "FY2024 audit")
arow(46, "District administration expense, FY2025", 1447164, CUR, "FY2025 audit")
arow(47, "Administrative rollback share of 2-yr growth", 0.5, PCT, "Judgment call", fill=YEL)
arow(48, "Attrition positions, district-wide", 4, NUM, "Judgment call", fill=YEL)

put(a, "A50", "CLOSURE SCENARIO JUDGMENTS (estimates — district must replace with actuals)", SEC)
arow(51, "Principal & office costs avoided", 175000, CUR, "Estimate", fill=YEL)
arow(52, "Plant/utilities/insurance avoided, net of carrying cost", 115000, CUR, "Estimate — assumes building sold or repurposed", fill=YEL)
arow(53, "Teaching positions truly eliminated", 3, NUM, "Estimate — via attrition only", fill=YEL)
arow(54, "Added busing cost per year", 137500, CUR, "Estimate — midpoint of $75K-$200K", fill=YEL)
arow(55, "Students leaving the district on closure", 10, NUM, "Judgment call — see sensitivity table", fill=YEL)
arow(56, "One-time transition cost", 100000, CUR, "Estimate", fill=YEL)

put(a, "A58", "GROWTH SCENARIO (nonresident enrollment under HB 563 / KRS 157.350)", SEC)
arow(59, "Transfer students, Year 1 (FY2027)", 15, NUM, "Scenario lever")
arow(60, "Transfer students, Year 2 (FY2028)", 30, NUM, "Scenario lever")
arow(61, "Transfer students, Year 3 (FY2029)", 46, NUM, "Scenario lever — capped at open seats in model")
arow(62, "Variable cost per transfer student", 400, CUR, "Estimate — supplies/materials", fill=YEL)
arow(63, "Added teacher once transfers exceed", 30, NUM, "Judgment call", fill=YEL)

put(a, "A65", "DISTRICT-FAVORABLE CLOSURE CASE (red-team upper bound)", SEC)
arow(66, "Positions eliminated, favorable case", 5, NUM, "Upper bound tested in Closure_Model", fill=YEL)
arow(67, "Added busing, favorable (low) case", 75000, CUR, "Low end of the $75K-$200K range", fill=YEL)

# ================= GF_SUMMARY =================
g = sheet("GF_Summary", [46, 15, 15, 15])
put(g, "A1", "General Fund, Three-Year Summary (audited)", TITLE)
for col, yr in zip("BCD", ["FY2023", "FY2024", "FY2025"]):
    put(g, f"{col}3", yr, BOLDW, fill=HDR)
put(g, "A3", "", BOLDW, fill=HDR)
lines = [
 ("Revenues before transfers", ["=Assumptions!B19", "=Assumptions!B20", "=Assumptions!B21"], GRN),
 ("Expenditures before transfers", ["=Assumptions!B22", "=Assumptions!B23", "=Assumptions!B24"], GRN),
 ("Operating result before transfers", ["=B4-B5", "=C4-C5", "=D4-D5"], BLK),
 ("Net transfers & other sources", [None, "=Assumptions!B25", "=Assumptions!B26"], GRN),
 ("Change in fund balance", [None, "=C6+C7", "=D6+D7"], BLK),
 ("Ending fund balance", ["=Assumptions!B27", "=Assumptions!B28", "=Assumptions!B29"], GRN),
 ("Check vs audited balances (small residual = other audited items)", [None, "=C9-B9-C8", "=D9-C9-D8"], BLK),
]
r = 4
for label, vals, f in lines:
    put(g, f"A{r}", label)
    for col, v in zip("BCD", vals):
        if v is not None:
            put(g, f"{col}{r}", v, font=f, fmt=CUR)
    r += 1
put(g, "A12", "METRICS", SEC)
put(g, "A13", "Fund balance as % of expenditures, FY2025"); put(g, "D13", "=D9/D5", BLK, PCT)
put(g, "A14", "2% contingency floor (FY2025 spending)"); put(g, "D14", "=Assumptions!B31*D5", BLK, CUR)
put(g, "A15", "Unassigned balance above the floor"); put(g, "D15", "=Assumptions!B30-D14", BLK, CUR)
put(g, "A16", "Average annual drawdown (FY2024-25)"); put(g, "D16", "=-AVERAGE(C8:D8)", BLK, CUR)
put(g, "A17", "Years of runway at current pace"); put(g, "D17", "=IFERROR(D15/D16,0)", BLK, '0.0')
put(g, "A19", "Source: FY2023-24 and FY2024-25 audited financial statements. FY2023 shown as reported in the FY2024 audit's comparative statement.", NOTE)
put(g, "A20", "What the transfers are: moves between the district's own funds (indirect cost recoveries from grants and self-supporting operations, fund closeouts, and similar interfund items detailed in the audits' fund statements). They cushion the General Fund's bottom line but are not new district revenue, which is why the operating result BEFORE transfers is the honest measure of the structural deficit.", NOTE, wrap=True)

# ================= CLOSURE_MODEL =================
c = sheet("Closure_Model", [54, 16, 46])
put(c, "A1", "Closure of NMES: Net-Savings Test", TITLE)
put(c, "A2", "Gross site cost is not net saving — students, teachers, and their SEEK funding move to receiving schools.", NOTE)
put(c, "A4", "THE CLAIM AND THE OFFICIAL DATA", SEC)
put(c, "A5", "Superintendent's stated gross cost (public statement, not yet documented)")
put(c, "B5", 1000000, BLUE, CUR); put(c, "C5", "WKYT, July 2026 — treated as a claim to verify", NOTE)
put(c, "A6", "Total site spending (state ESSA basis)"); put(c, "B6", "=Assumptions!B14*Assumptions!B11", GRN, CUR)
put(c, "A7", "State/local share of site spending"); put(c, "B7", "=Assumptions!B15*Assumptions!B11", GRN, CUR)
put(c, "A9", "RECURRING SAVINGS (costs that truly disappear)", SEC)
put(c, "A10", "Principal & office"); put(c, "B10", "=Assumptions!B51", GRN, CUR)
put(c, "A11", "Plant, utilities, insurance (net of carrying cost)"); put(c, "B11", "=Assumptions!B52", GRN, CUR)
put(c, "A12", "Teaching positions eliminated (via attrition)"); put(c, "B12", "=Assumptions!B53*Assumptions!B41", GRN, CUR)
put(c, "A13", "Gross avoidable cost", bold=True); put(c, "B13", "=SUM(B10:B12)", BLK, CUR, bold=True)
put(c, "A15", "RECURRING OFFSETS (new costs and lost revenue)", SEC)
put(c, "A16", "Added busing"); put(c, "B16", "=Assumptions!B54", GRN, CUR)
put(c, "A17", "SEEK revenue lost to departing students (FY2027 base)"); put(c, "B17", "=Assumptions!B55*Assumptions!B6", GRN, CUR)
put(c, "A18", "Total offsets", bold=True); put(c, "B18", "=SUM(B16:B17)", BLK, CUR, bold=True)
put(c, "A20", "NET RECURRING GENERAL FUND SAVING", bold=True)
nc = put(c, "B20", "=B13-B18", BLK, CUR, bold=True); nc.border = TOPLINE
put(c, "A21", "As a share of the FY2025 structural deficit"); put(c, "B21", "=B20/(Assumptions!B24-Assumptions!B21)", BLK, PCT)
put(c, "A22", "One-time transition cost (year one)"); put(c, "B22", "=Assumptions!B56", GRN, CUR)
put(c, "A24", "SENSITIVITY: STUDENTS LEAVING THE DISTRICT", SEC)
put(c, "A25", "Students leaving", bold=True); put(c, "B25", "Net recurring saving", bold=True)
for i, n in enumerate([0, 10, 20, 30]):
    rr = 26 + i
    put(c, f"A{rr}", n, BLUE, NUM)
    put(c, f"B{rr}", f"=$B$13-Assumptions!$B$54-A{rr}*Assumptions!$B$6", BLK, CUR)
put(c, "A31", "Each departing student removes at least the SEEK base guarantee, every year, permanently.", NOTE)
put(c, "A33", "DISTRICT-FAVORABLE CASE (red-team): 5 positions cut, low busing, no departures", SEC)
put(c, "A34", "Net recurring saving, favorable case")
put(c, "B34", "=Assumptions!B51+Assumptions!B52+Assumptions!B66*Assumptions!B41-Assumptions!B67", GRN, CUR)
put(c, "A35", "As a share of the FY2025 structural deficit")
put(c, "B35", "=B34/(Assumptions!B24-Assumptions!B21)", BLK, PCT)

# ================= GROWTH_MODEL =================
gr = sheet("Growth_Model", [50, 14, 14, 14])
put(gr, "A1", "Grow the Kings: Nonresident Enrollment Model (HB 563 / KRS 157.350)", TITLE)
put(gr, "A2", "SEEK funding follows nonresident students since July 2022; no agreement from the home district is required.", NOTE)
for col, yr in zip("BCD", ["FY2027", "FY2028", "FY2029"]):
    put(gr, f"{col}4", yr, BOLDW, fill=HDR)
put(gr, "A4", "", BOLDW, fill=HDR)
put(gr, "A5", "Transfer students (scenario)"); 
put(gr, "B5", "=Assumptions!B59", GRN, NUM); put(gr, "C5", "=Assumptions!B60", GRN, NUM); put(gr, "D5", "=Assumptions!B61", GRN, NUM)
put(gr, "A6", "Enrolled (capped at open seats)")
for col in "BCD":
    put(gr, f"{col}6", f"=MIN({col}5,Assumptions!$B$13)", BLK, NUM)
put(gr, "A7", "SEEK base per pupil")
put(gr, "B7", "=Assumptions!B6", GRN, CUR); put(gr, "C7", "=Assumptions!B7", GRN, CUR); put(gr, "D7", "=Assumptions!B8", GRN, CUR)
put(gr, "A8", "New SEEK revenue (base only)")
for col in "BCD":
    put(gr, f"{col}8", f"={col}6*{col}7", BLK, CUR)
put(gr, "A9", "Variable cost of added students")
for col in "BCD":
    put(gr, f"{col}9", f"={col}6*Assumptions!$B$62", BLK, CUR)
put(gr, "A10", "Added teacher (once threshold passed)")
for col in "BCD":
    put(gr, f"{col}10", f"=IF({col}6>Assumptions!$B$63,Assumptions!$B$41,0)", BLK, CUR)
put(gr, "A11", "Net new recurring revenue", bold=True)
for col in "BCD":
    cc = put(gr, f"{col}11", f"={col}8-{col}9-{col}10", BLK, CUR, bold=True); cc.border = TOPLINE
put(gr, "A12", "Cumulative")
put(gr, "B12", "=B11", BLK, CUR); put(gr, "C12", "=B12+C11", BLK, CUR); put(gr, "D12", "=C12+D11", BLK, CUR)
put(gr, "A14", "Upside excluded from this model: tuition, SEEK add-on weights, preschool and day-care expansion, and in-county boundary redistricting, which fills seats with students the district already serves.", NOTE, wrap=True)
put(gr, "A15", "Context: NMES enrolled 160 students as recently as 2019-20 (see School_Data) - the growth targets restore recent history, they do not exceed it.", NOTE, wrap=True)

# ================= REDISTRICTING =================
rd = sheet("Redistricting", [56, 15, 58])
put(rd, "A1", "Fill the Kings' Seats: Boundary Rebalancing and Cross-County Scenario", TITLE)
put(rd, "A2", "A planning scenario, not a routing study. The district holds the geocoded student counts and routing data a true optimization needs; releasing them is a records ask in the report.", NOTE, wrap=True)

put(rd, "A4", "CURRENT ELEMENTARY MAP (2024-25 counts as cited in report Sections 4 and 9)", SEC)
put(rd, "A5", "NMES enrollment"); put(rd, "B5", "=Assumptions!B11", GRN, NUM)
put(rd, "A6", "NMES rated capacity"); put(rd, "B6", "=Assumptions!B12", GRN, NUM)
put(rd, "A7", "NMES open seats"); put(rd, "B7", "=B6-B5", BLK, NUM)
put(rd, "A8", "Bourbon Central enrollment"); put(rd, "B8", 459, BLUE, NUM); put(rd, "C8", "Report Section 4; confirm against current-year infinite campus counts", NOTE)
put(rd, "A9", "Cane Ridge enrollment"); put(rd, "B9", 453, BLUE, NUM); put(rd, "C9", "Report Section 4", NOTE)

put(rd, "A11", "SCENARIO LEVERS (yellow = judgment calls the district's data should replace)", SEC)
put(rd, "A12", "Students rezoned to NMES from the eastern edges of the Paris-area zones", )
put(rd, "B12", 30, BLUE, NUM, fill=YEL); put(rd, "C12", "Chosen from families already living closer to NMES than to their assigned school; requires the geocoded counts", NOTE, wrap=True)
put(rd, "A13", "Cross-county transfers under HB 563 (KRS 157.350)")
put(rd, "B13", 16, BLUE, NUM, fill=YEL); put(rd, "C13", "SEEK funding follows each transfer; no home-district agreement required since July 2022", NOTE, wrap=True)
put(rd, "A14", "NMES enrollment after"); put(rd, "B14", "=B5+B12+B13", BLK, NUM)
put(rd, "A15", "Fill check vs capacity"); put(rd, "B15", "=B6-B14", BLK, NUM); put(rd, "C15", "Zero = exactly full", NOTE)
put(rd, "A16", "Bourbon Central after (half the rezone)"); put(rd, "B16", "=B8-B12/2", BLK, NUM)
put(rd, "A17", "Cane Ridge after (half the rezone)"); put(rd, "B17", "=B9-B12/2", BLK, NUM)

put(rd, "A19", "CLASSROOMS", SEC)
put(rd, "A20", "NMES classroom sections"); put(rd, "B20", 9, BLUE, NUM); put(rd, "C20", "9.41 classroom FTE, NCES; K-5 across nine homerooms", NOTE)
put(rd, "A21", "Average class size today"); put(rd, "B21", "=B5/B20", BLK, '0.0')
put(rd, "A22", "Average class size at capacity"); put(rd, "B22", "=B14/B20", BLK, '0.0')
put(rd, "A23", "Statutory caps (KRS 157.360): 24 in K-3, 28 in grade 4, 29 in grades 5-6. The scenario adds no NMES teachers.", NOTE)

put(rd, "A25", "RECURRING DOLLARS", SEC)
put(rd, "A26", "New SEEK revenue from cross-county transfers (FY2027 base)"); put(rd, "B26", "=B13*Assumptions!B6", GRN, CUR)
put(rd, "A27", "Variable cost of all added students"); put(rd, "B27", "=(B12+B13)*Assumptions!B62", GRN, CUR)
put(rd, "A28", "Sections avoided or redeployed at receiving schools, low (count)"); put(rd, "B28", 1, BLUE, NUM, fill=YEL)
put(rd, "A29", "Sections avoided or redeployed at receiving schools, high (count)"); put(rd, "B29", 2, BLUE, NUM, fill=YEL)
put(rd, "A30", "Net recurring benefit, low", bold=True); b30 = put(rd, "B30", "=B26-B27+B28*Assumptions!B41", BLK, CUR, bold=True); b30.border = TOPLINE
put(rd, "A31", "Net recurring benefit, high", bold=True); put(rd, "B31", "=B26-B27+B29*Assumptions!B41", BLK, CUR, bold=True)

put(rd, "A33", "PER-STUDENT ARITHMETIC (the number the closure argument leans on)", SEC)
put(rd, "A34", "NMES site spending today"); put(rd, "B34", "=Assumptions!B14*Assumptions!B11", GRN, CUR)
put(rd, "A35", "Per student today"); put(rd, "B35", "=Assumptions!B14", GRN, CUR)
put(rd, "A36", "Per student at capacity (site cost plus variable cost, over 174)")
put(rd, "B36", "=(B34+(B12+B13)*Assumptions!B62)/B14", BLK, CUR)
put(rd, "A37", "Change"); put(rd, "B37", "=B36/B35-1", BLK, PCT)
put(rd, "A39", "ASSUMPTIONS THE DISTRICT'S DATA SHOULD REPLACE", SEC)
put(rd, "A40", "Rezoned students are drawn only from homes closer to NMES than to their assigned school, so bus routes shorten or hold even; the district's routing data would settle it.", NOTE, wrap=True)
put(rd, "A41", "Receiving-school relief is booked only as one to two avoided or redeployed sections; grade-by-grade capacities at Bourbon Central and Cane Ridge are a records ask (report Question 3).", NOTE, wrap=True)
put(rd, "A42", "SEEK for rezoned in-county students is unchanged (same district); only cross-county transfers add revenue.", NOTE, wrap=True)

# ================= TRANSPORT_GEO =================
tg = sheet("Transport_Geo", [58, 15, 58])
put(tg, "A1", "Transportation and Geography: Density, Route Miles, and What Closure Adds", TITLE)
put(tg, "A2", "Zone geometry is official: NCES School Attendance Boundary Survey, 2015-16 collection (build/sabs_zones.json in the repository). Cost inputs remain labeled estimates; the district's annual T-1 transportation report and geocoded counts replace them.", NOTE, wrap=True)

put(tg, "A4", "GEOGRAPHY AND STUDENT DENSITY", SEC)
put(tg, "A5", "Bourbon County land area (square miles)"); put(tg, "B5", 290, BLUE, NUM); put(tg, "C5", "U.S. Census: 289.7 land square miles", NOTE)
put(tg, "A6", "Paris city population, 2020"); put(tg, "B6", 10171, BLUE, NUM); put(tg, "C6", "2020 Census", NOTE)
put(tg, "A7", "Millersburg population, 2020"); put(tg, "B7", 747, BLUE, NUM); put(tg, "C7", "2020 Census", NOTE)
put(tg, "A8", "North Middletown population, 2020"); put(tg, "B8", "=Demographics!B29", GRN, NUM); put(tg, "C8", "Demographics tab", NOTE)
put(tg, "A9", "NMES zone share of county area"); put(tg, "B9", 0.38, BLUE, PCT); put(tg, "C9", "Official: NCES SABS 2015-16, NMES zone 110.3 sq mi of the 289.1 sq mi zone total", NOTE)
put(tg, "A10", "NMES zone area (sq mi)"); put(tg, "B10", "=B5*B9", BLK, '0')
put(tg, "A11", "Paris-area zones (sq mi)"); put(tg, "B11", "=B5-B10", BLK, '0')
put(tg, "A12", "NMES elementary students"); put(tg, "B12", "=Assumptions!B11", GRN, NUM)
put(tg, "A13", "Paris-area elementary students"); put(tg, "B13", "=Redistricting!B8+Redistricting!B9", GRN, NUM)
put(tg, "A14", "Students per square mile, NMES zone"); put(tg, "B14", "=B12/B10", BLK, '0.0')
put(tg, "A15", "Students per square mile, Paris-area zones"); put(tg, "B15", "=B13/B11", BLK, '0.0')
put(tg, "A16", "Students per square mile, district elementary overall"); put(tg, "B16", "=(B12+B13)/B5", BLK, '0.0')
put(tg, "A17", "State law (KRS 157.370) funds transportation on transported pupils per square mile: low density earns a higher per-pupil allotment because it costs more to serve. Funding history: below the formula for two decades, restored to 90 then 100 percent (on lagged FY2023 costs) in the 2024-2026 budget, then frozen again below formula in the 2026-2028 budget.", NOTE, wrap=True)
put(tg, "A18", "STATE REVENUE EFFECT: with the appropriation frozen at flat dollars computed on lagged costs, the marginal state reimbursement on NEW busing miles is zero, so closure's added routes are district money. Rebalancing changes no transported-pupil count, so the add-on is unchanged; and the district is not required to transport nonresident transfer students at all (board policy decides).", NOTE, wrap=True)

put(tg, "A19", "WHAT CLOSURE ADDS: ROUTE-MILE ARITHMETIC (yellow = replace with district T-1 data)", SEC)
put(tg, "A20", "Share of NMES students riding the bus"); put(tg, "B20", 0.85, BLUE, PCT, fill=YEL)
put(tg, "A21", "Riders"); put(tg, "B21", "=ROUND(B20*B12,0)", BLK, NUM)
put(tg, "A22", "Rural routes serving NMES today"); put(tg, "B22", 3, BLUE, NUM, fill=YEL)
put(tg, "A23", "Added distance to the Paris schools, one way (miles)"); put(tg, "B23", 10, BLUE, NUM); put(tg, "C23", "US 460, North Middletown to Paris", NOTE)
put(tg, "A24", "Added bus-miles per route per day (out and back, AM and PM)"); put(tg, "B24", "=B23*4", BLK, NUM)
put(tg, "A25", "School days per year"); put(tg, "B25", 170, BLUE, NUM, fill=YEL)
put(tg, "A26", "Added bus-miles per year"); put(tg, "B26", "=B22*B24*B25", BLK, NUM)
put(tg, "A27", "Marginal cost per bus-mile, low"); put(tg, "B27", 2.50, BLUE, '0.00', fill=YEL); put(tg, "C27", "Fuel, maintenance, driver time; replace with district cost data", NOTE)
put(tg, "A28", "Marginal cost per bus-mile, high"); put(tg, "B28", 4.50, BLUE, '0.00', fill=YEL)
put(tg, "A29", "Added cost, mileage basis, low"); put(tg, "B29", "=B26*B27", BLK, CUR)
put(tg, "A30", "Added cost, mileage basis, high"); put(tg, "B30", "=B26*B28", BLK, CUR)
put(tg, "A31", "Additional buses if route tiers break (high case)"); put(tg, "B31", 1, BLUE, NUM, fill=YEL)
put(tg, "A32", "All-in cost per additional bus-year"); put(tg, "B32", 55000, BLUE, CUR, fill=YEL)
put(tg, "A33", "Bottom-up added busing cost, low", bold=True); c33 = put(tg, "B33", "=B29", BLK, CUR, bold=True); c33.border = TOPLINE
put(tg, "A34", "Bottom-up added busing cost, high", bold=True); put(tg, "B34", "=B30+B31*B32", BLK, CUR, bold=True)
put(tg, "A35", "Report's planning range (Closure_Model offset basis)"); put(tg, "B35", "Between $75,000 and $200,000", NOTE)
put(tg, "A36", "The bottom-up estimate lands inside the planning range; the $137,500 midpoint used in the Closure_Model stands. Note what closure does not remove: every square mile of the eastern county stays in the coverage area, with longer rides on it, roughly 15 to 20 added minutes each way on US 460.", NOTE, wrap=True)

put(tg, "A38", "WHAT REBALANCING CHANGES (Redistricting tab scenario)", SEC)
put(tg, "A39", "Students rezoned to NMES"); put(tg, "B39", "=Redistricting!B12", GRN, NUM)
put(tg, "A40", "Stem miles saved per affected route, one way"); put(tg, "B40", 3, BLUE, NUM, fill=YEL); put(tg, "C40", "Rezoned families live closer to NMES than to their assigned school", NOTE)
put(tg, "A41", "Affected routes"); put(tg, "B41", 2, BLUE, NUM, fill=YEL)
put(tg, "A42", "Bus-miles saved per year"); put(tg, "B42", "=B41*B40*4*B25", BLK, NUM)
put(tg, "A43", "Transport saving, low"); put(tg, "B43", "=B42*B27", BLK, CUR)
put(tg, "A44", "Transport saving, high"); put(tg, "B44", "=B42*B28", BLK, CUR)
put(tg, "A45", "Rebalancing is transport-neutral to modestly positive, the opposite sign of closure.", NOTE)

put(tg, "A47", "DISTRICT-WIDE CONTEXT", SEC)
put(tg, "A48", "Transportation expense, FY2025"); put(tg, "B48", "=Assumptions!B42", GRN, CUR)
put(tg, "A49", "Average Daily Attendance, FY2025"); put(tg, "B49", 2242.5, BLUE, '0.0'); put(tg, "C49", "FY2025 audit", NOTE)
put(tg, "A50", "Transportation cost per student in attendance"); put(tg, "B50", "=B48/B49", BLK, CUR)
put(tg, "A51", "Optimization potential at 5 to 10 percent (Alternatives menu)"); put(tg, "B51", "=Assumptions!B42*Assumptions!B43", GRN, CUR)
put(tg, "A52", ""); put(tg, "B52", "=Assumptions!B42*Assumptions!B44", GRN, CUR)

# ================= ALTERNATIVES =================
al = sheet("Alternatives", [46, 14, 14, 52])
put(al, "A1", "Revenue and Cost Alternatives (no school closed)", TITLE)
hdrs = ["Measure", "Low ($/yr)", "High ($/yr)", "Basis"]
for i, h in enumerate(hdrs):
    put(al, f"{get_column_letter(i+1)}3", h, BOLDW, fill=HDR)
alts = [
 ("4% property-tax adjustment (KRS 160.470)", "=Assumptions!B35*Assumptions!B36", 450000, "Low = 4% of FY2025 GF property tax; high allows base growth", GRN, BLUE),
 ("Improve delinquent-tax recovery (partial)", 60000, 120000, "25-50% of FY2025 delinquency of $239,126 (2.4% of certified yield)", BLUE, BLUE),
 ("Attendance recovery (+1-2% ADA)", 100000, 200000, "Approx. SEEK value per 1% of ADA", BLUE, BLUE),
 ("Attrition-based staffing alignment", "=Assumptions!B48*Assumptions!B41", 425000, "Low = positions x loaded cost", GRN, BLUE),
 ("Administrative restraint", "=Assumptions!B47*(Assumptions!B46-Assumptions!B45)", 450000, "Low = rollback share of 2-yr district-admin growth", GRN, BLUE),
 ("Transportation optimization", "=Assumptions!B42*Assumptions!B43", "=Assumptions!B42*Assumptions!B44", "5-10% of FY2025 transport expense", GRN, GRN),
 ("Medicaid billing, E-rate, meal reimbursements", 100000, 250000, "Typical under-collected federal reimbursements", BLUE, BLUE),
 ("Energy performance contracting", 50000, 150000, "10-25% of utilities; authorized by 702 KAR 4:160", BLUE, BLUE),
 ("Shared services with Paris Independent", 100000, 300000, "Transport, food service, back office", BLUE, BLUE),
 ("Fill NMES to capacity (rebalance + transfers, net)", "=Redistricting!B30", "=Redistricting!B31", "Boundary rebalancing and cross-county scenario, Redistricting tab", GRN, GRN),
 ("NMES multi-age reorganization", 170000, 255000, "Six or seven sections instead of nine, via attrition", BLUE, BLUE),
]
r = 4
for label, lo, hi, basis, flo, fhi in alts:
    put(al, f"A{r}", label)
    put(al, f"B{r}", lo, flo, CUR)
    put(al, f"C{r}", hi, fhi, CUR)
    put(al, f"D{r}", basis, NOTE)
    r += 1
put(al, f"A{r}", "Total identified (ranges overlap; not additive to the penny)", bold=True)
b = put(al, f"B{r}", f"=SUM(B4:B{r-1})", BLK, CUR, bold=True); b.border = TOPLINE
cc = put(al, f"C{r}", f"=SUM(C4:C{r-1})", BLK, CUR, bold=True); cc.border = TOPLINE
tot = r
put(al, f"A{tot+2}", "COMPARISON", SEC)
put(al, f"A{tot+3}", "Package midpoint (raw sum of ranges)"); put(al, f"B{tot+3}", f"=(B{tot}+C{tot})/2", BLK, CUR)
put(al, f"A{tot+4}", "Conservative combined estimate, low (haircut for overlap)"); put(al, f"B{tot+4}", 1100000, BLUE, CUR, fill=YEL)
put(al, f"A{tot+5}", "Conservative combined estimate, high"); put(al, f"B{tot+5}", 2100000, BLUE, CUR, fill=YEL)
put(al, f"A{tot+6}", "Conservative midpoint (used in Runway sheet)"); put(al, f"B{tot+6}", f"=(B{tot+4}+B{tot+5})/2", BLK, CUR)
put(al, f"A{tot+7}", "Average annual GF drawdown (FY2024-25)"); put(al, f"B{tot+7}", "=GF_Summary!D16", GRN, CUR)
put(al, f"A{tot+8}", "Closure net saving (base case)"); put(al, f"B{tot+8}", "=Closure_Model!B20", GRN, CUR)

# ================= DEBT_SERVICE =================
d = sheet("Debt_Service", [16, 16, 14, 12, 18, 44])
put(d, "A1", "Outstanding Bonds — Bourbon County School District Finance Corporation", TITLE)
put(d, "A2", "Source: FY2025 audited financial statements, Note 4. Facility funds and debt are restricted; they cannot pay operating costs.", NOTE)
for i, h in enumerate(["Series", "Original", "Rate", "Maturity", "Outstanding 6/30/25", "Note"]):
    put(d, f"{get_column_letter(i+1)}4", h, BOLDW, fill=HDR)
bonds = [
 ("2013", 2255000, "1.90-2.10%", "2026", 348000, ""),
 ("2013R", 468000, "2.75-4.05%", "2033", 585000, "Audit figures internally inconsistent; maturity typo in audit — district to correct"),
 ("2016", 5700000, "1.00-3.00%", "2029", 3145000, "Refunded $5,315,000 of 2009 bonds; NPV savings $314,834"),
 ("2018", 1850000, "3.50%", "2038", 1560000, ""),
 ("2020", 3620000, "0.50-1.85%", "2031", 3405000, "Refunded $3,410,000 of 2011 bonds; NPV savings $106,627"),
 ("2023", 810000, "3.65-4.00%", "2034", 755000, "Purpose to be confirmed from official statement"),
 ("2024", 6055000, "4.00-5.00%", "2044", 5945290, "Funds active construction program; purpose to be published"),
]
r = 5
for s, orig, rate, mat, out, nn in bonds:
    put(d, f"A{r}", s)
    put(d, f"B{r}", orig, BLUE, CUR)
    put(d, f"C{r}", rate)
    put(d, f"D{r}", mat)
    put(d, f"E{r}", out, BLUE, CUR)
    put(d, f"F{r}", nn, NOTE, wrap=True)
    r += 1
put(d, f"A{r}", "Total", bold=True)
bb = put(d, f"B{r}", f"=SUM(B5:B{r-1})", BLK, CUR, bold=True); bb.border = TOPLINE
ee = put(d, f"E{r}", f"=SUM(E5:E{r-1})", BLK, CUR, bold=True); ee.border = TOPLINE
r += 2
put(d, f"A{r}", "ANNUAL DEBT SERVICE", SEC); r += 1
put(d, f"A{r}", "District-paid, FY2025"); put(d, f"B{r}", 1150216, BLUE, CUR); r += 1
put(d, f"A{r}", "District-paid, FY2026"); put(d, f"B{r}", 1578700, BLUE, CUR); r += 1
put(d, f"A{r}", "Increase, FY2025 to FY2026"); put(d, f"B{r}", f"=B{r-1}-B{r-2}", BLK, CUR); r += 1
put(d, f"A{r}", "FY2026 total including state (SFCC) share"); put(d, f"B{r}", 1846159, BLUE, CUR); r += 1
put(d, f"A{r}", "SFCC-paid principal over life of bonds"); put(d, f"B{r}", 1568809, BLUE, CUR)
r += 2
put(d, f"A{r}", "BONDING CAPACITY: WHAT CLOSURE CAN AND CANNOT CHANGE", SEC); r += 1
put(d, f"A{r}", "Average Daily Attendance, FY2025 (SEEK basis)"); put(d, f"B{r}", 2242.5, BLUE, '0.0'); put(d, f"F{r}", "FY2025 audit", NOTE); ada_r = r; r += 1
put(d, f"A{r}", "Capital outlay allotment per year (KRS 157.420, $100 per ADA)"); put(d, f"B{r}", f"=100*B{ada_r}", BLK, CUR); co_r = r; r += 1
put(d, f"A{r}", "Bondable share of capital outlay (702 KAR 4:160 safety factor)"); put(d, f"B{r}", 0.8, BLUE, PCT); sh_r = r; r += 1
put(d, f"A{r}", "Building-fund and debt-fund property tax, FY2025 (the 'nickel' stream)"); put(d, f"B{r}", "=Tax_History!B33", GRN, CUR); bf_r = r; r += 1
put(d, f"A{r}", "District-paid debt service, FY2026"); put(d, f"B{r}", 1578700, BLUE, CUR); ds_r = r; r += 1
put(d, f"A{r}", "Annual restricted margin available for new debt (illustrative)")
mm = put(d, f"B{r}", f"=B{co_r}*B{sh_r}+B{bf_r}-B{ds_r}", BLK, CUR); mm.border = TOPLINE
put(d, f"F{r}", "Simplified: KDE's official bonding potential statement is the authority and should be published", NOTE, wrap=True); r += 1
put(d, f"A{r}", "Unused bonding capacity stated in the FY2024 audit"); put(d, f"B{r}", 23500000, BLUE, CUR); put(d, f"F{r}", "FY2024 audit note", NOTE); r += 2
put(d, f"A{r}", "Why closing NMES does not create bonding capacity: capacity is built from the streams above, none of which", NOTE); r += 1
put(d, f"A{r}", "grows when a school closes. Each student who leaves the district subtracts $100 per year from capital outlay", NOTE); r += 1
put(d, f"A{r}", "and the SEEK base from operations. Sale proceeds are one-time and restricted to capital use. What a closure", NOTE); r += 1
put(d, f"A{r}", "changes is the facility plan's priority list, which steers SFCC offers (KRS 157.622) toward other projects.", NOTE); r += 1
put(d, f"A{r}", "That is a choice about priorities, not a gain in capacity, and it should be argued openly with the BG-1,", NOTE); r += 1
put(d, f"A{r}", "the official statement, and the bonding potential statement all public.", NOTE)

# ================= RUNWAY =================
rw = sheet("Runway", [52, 14, 14, 14, 14])
put(rw, "A1", "Reserve Runway: Where the Fund Balance Goes Under Each Path", TITLE)
put(rw, "A2", "Simplified straight-line projection from the FY2025 ending balance; excludes raises, inflation, and one-time items.", NOTE)
for col, yr in zip("BCDE", ["FY2026", "FY2027", "FY2028", "FY2029"]):
    put(rw, f"{col}4", yr, BOLDW, fill=HDR)
put(rw, "A4", "Projected ending General Fund balance", BOLDW, fill=HDR)
put(rw, "A5", "Status quo (current drawdown continues)")
put(rw, "B5", "=GF_Summary!D9-GF_Summary!$D$16", BLK, CUR)
for col, prev in zip("CDE", "BCD"):
    put(rw, f"{col}5", f"={prev}5-GF_Summary!$D$16", BLK, CUR)
put(rw, "A6", "With alternatives package (conservative midpoint; half effect FY2027, full after)")
put(rw, "B6", "=GF_Summary!D9-GF_Summary!$D$16", BLK, CUR)
put(rw, "C6", "=B6-GF_Summary!$D$16+0.5*Alternatives!$B$21", BLK, CUR)
put(rw, "D6", "=C6-GF_Summary!$D$16+Alternatives!$B$21", BLK, CUR)
put(rw, "E6", "=D6-GF_Summary!$D$16+Alternatives!$B$21", BLK, CUR)
put(rw, "A7", "Closure only (base-case net saving from FY2027)")
put(rw, "B7", "=GF_Summary!D9-GF_Summary!$D$16", BLK, CUR)
for col, prev in zip("CDE", "BCD"):
    put(rw, f"{col}7", f"={prev}7-GF_Summary!$D$16+Closure_Model!$B$20", BLK, CUR)
put(rw, "A8", "2% contingency floor (approx., FY2025 basis)")
for col in "BCDE":
    put(rw, f"{col}8", "=GF_Summary!$D$14", GRN, CUR)
put(rw, "A10", "Reading: the alternatives package restores balance faster than closure, keeps every school open, and adds enrollment revenue rather than risking it.", NOTE, wrap=True)




# ================= TAX_HISTORY =================
th = sheet("Tax_History", [36, 13, 13, 13, 6, 13, 48])
put(th, "A1", "Property Tax Rates, Fund Split, Delinquency, and the 4% Option", TITLE)
put(th, "A2", "Backs Section 9 and Figure 15 of the report. Rates in cents per $100. DOR rate books primary for 2023-2025; 2018-2022 verified secondary; 2005-2017 not retrieved and not interpolated.", NOTE)

put(th, "A4", "BOURBON COUNTY SCHOOLS, REAL ESTATE RATE BY TAX YEAR", SEC)
trates = [("2018", 61.3), ("2019", 60.6), ("2020", 55.9), ("2021", 54.2),
          ("2022", 49.2), ("2023", 52.4), ("2024", 52.4), ("2025", 52.4)]
r = 5
for yr, v in trates:
    put(th, f"A{r}", yr); put(th, f"B{r}", v, BLUE, "0.0"); r += 1
put(th, "G5", "2019 documented as the board taking the 4% option (Bourbon County Citizen, 9/4/2019); other years' rate type undetermined pending KDE levy files", NOTE, wrap=True)
put(th, "A14", "Tangible/personal rate (recent)"); put(th, "B14", 64.5, BLUE, "0.0")
put(th, "A15", "Motor vehicle rate"); put(th, "B15", 54.7, BLUE, "0.0")
put(th, "A16", "Utility gross receipts"); put(th, "B16", 0.03, BLUE, PCT)

put(th, "A18", "AREA DISTRICTS, LEVIED REAL ESTATE RATE 2024-25", SEC)
nbrs = [("Fayette County", 80.9), ("Paris Independent", 71.5), ("Clark County", 66.8),
        ("Bath County", 63.4), ("Scott County", 62.9), ("Harrison County", 57.7),
        ("Montgomery County", 52.5), ("Bourbon County", 52.4), ("Nicholas County", 43.1)]
r = 19
for name, v in nbrs:
    put(th, f"A{r}", name); put(th, f"B{r}", v, BLUE, "0.0"); r += 1
put(th, "A28", "Statewide school average (DOR Table II, 2025)"); put(th, "B28", 65.13, BLUE, "0.0")
put(th, "G19", "Fayette and Clark from local reporting of board votes; others from DOR rate books. Bourbon ranks second lowest of the nine. Nicholas shown at its real estate rate of 43.1 (tangible 43.7). Bath 63.4 is the 2025 rate (2024: 60.7).", NOTE, wrap=True)

put(th, "A31", "FY2025 PROPERTY TAX BY FUND (audited)", SEC)
put(th, "A32", "General Fund"); put(th, "B32", 7829060, BLUE, CUR)
put(th, "A33", "Building (FSPK) and debt service funds"); put(th, "B33", 2052786, BLUE, CUR)
put(th, "A34", "Total property tax, FY2025"); put(th, "B34", "=B32+B33", BLK, CUR)
put(th, "A35", "General Fund property tax, FY2024"); put(th, "B35", 7150498, BLUE, CUR)
put(th, "A36", "General Fund revenue, FY2025"); put(th, "B36", 26449318, BLUE, CUR)
put(th, "A37", "General Fund deficit before transfers, FY2025"); put(th, "B37", 2648086, BLUE, CUR)
put(th, "A38", "General Fund expenditures, FY2025"); put(th, "B38", "=B36+B37", BLK, CUR)
put(th, "A39", "Local levy share of General Fund spending"); put(th, "B39", "=B32/B38", BLK, PCT)
put(th, "G32", "GF vs building-fund CENT split unverified; dollar split is audited. Cent split is a records request in the report.", NOTE, wrap=True)

put(th, "A41", "DELINQUENCY CHECK (collections vs certified yield)", SEC)
put(th, "B41", "FY2024", BOLD); put(th, "C41", "FY2025", BOLD)
put(th, "A42", "Calculated yield at levied rates"); put(th, "B42", 10556809, BLUE, CUR); put(th, "C42", 9880143, BLUE, CUR)
put(th, "A43", "Actual collections"); put(th, "B43", 10168969, BLUE, CUR); put(th, "C43", 9641017, BLUE, CUR)
put(th, "A44", "Gap (ordinary delinquency)"); put(th, "B44", "=B42-B43", BLK, CUR); put(th, "C44", "=C42-C43", BLK, CUR)
put(th, "A45", "Gap as share of yield"); put(th, "B45", "=B44/B42", BLK, PCT); put(th, "C45", "=C44/C42", BLK, PCT)

put(th, "A47", "FOUR PERCENT OPTION, THREE-YEAR PATH (KRS 160.470)", SEC)
put(th, "A48", "Base: FY2025 actual real + personal collections"); put(th, "B48", "=C43", GRN, CUR)
put(th, "A49", "Annual revenue option"); put(th, "B49", 0.04, BLUE, PCT)
put(th, "A50", "Year 1 added recurring revenue"); put(th, "B50", "=B48*B49", BLK, CUR)
put(th, "A51", "Year 2 added recurring revenue"); put(th, "B51", "=(B48+B50)*B49", BLK, CUR)
put(th, "A52", "Year 3 added recurring revenue"); put(th, "B52", "=(B48+B50+B51)*B49", BLK, CUR)
put(th, "A53", "Cumulative added annual revenue by Year 3"); put(th, "B53", "=B50+B51+B52", BLK, CUR)
put(th, "A54", "As a share of the FY2025 structural deficit"); put(th, "B54", "=B53/(Assumptions!B24-Assumptions!B21)", BLK, PCT)
put(th, "G48", "Basis: 4% more revenue from EXISTING real + personal property than the compensating rate; new property excluded (upside); motor vehicle separate; recall applies only above 4%.", NOTE, wrap=True)

# ================= DEMOGRAPHICS =================
dm = sheet("Demographics", [30, 12, 30, 6, 8, 8, 6, 8, 8, 44])
put(dm, "A1", "County Demographics and NMES Long-Run Enrollment", TITLE)
put(dm, "A2", "An honest picture: the county is flat to declining, so the growth plan relies on redistricting and cross-county enrollment, not a population rebound.", NOTE)

put(dm, "A4", "BOURBON COUNTY POPULATION (U.S. Census / FRED; KSDC projection)", SEC)
pop = [("1970", 18476), ("1980", 19405), ("1990", 19247), ("2000", 19352),
       ("2010", 19985), ("2020", 20252), ("2024 est.", 20337), ("2040 projection (KSDC)", 19352)]
r = 5
for yr, v in pop:
    put(dm, f"A{r}", yr)
    put(dm, f"B{r}", v, BLUE, NUM)
    r += 1
put(dm, "A13", "Change, 1970 to 2020"); put(dm, "B13", "=B10-B5", BLK, NUM)
put(dm, "A14", "Change as a share of 1970"); put(dm, "B14", "=B13/B5", BLK, PCT)
put(dm, "J5", "Sources: FRED series KYBOUR7POP; Envision 2040 plan citing the Kentucky State Data Center", NOTE, wrap=True)

put(dm, "A16", "ADJACENT COUNTIES: 2020 CENSUS AND OUTLOOK", SEC)
adj = [("Scott (Georgetown)", 57155, "+46.1% projected to 2050"),
       ("Fayette (Lexington)", 322570, "+9.8% projected to 2050"),
       ("Clark (Winchester)", 36972, "Slow growth"),
       ("Montgomery (Mt. Sterling)", 28000, "Slow growth"),
       ("Harrison (Cynthiana)", 18692, "Roughly flat"),
       ("Bath", 12500, "Flat to declining"),
       ("Nicholas (Carlisle)", 7537, "Flat to declining"),
       ("Bourbon", 20252, "About -4% by 2040 (KSDC)")]
r = 17
for name, v, note_t in adj:
    put(dm, f"A{r}", name)
    put(dm, f"B{r}", v, BLUE, NUM)
    put(dm, f"C{r}", note_t, NOTE)
    r += 1

put(dm, "A26", "NORTH MIDDLETOWN CITY POPULATION", SEC)
town = [("2000", 562), ("2010 (approx.)", 521), ("2020", 610), ("2024 est.", 679)]
r = 27
for yr, v in town:
    put(dm, f"A{r}", yr)
    put(dm, f"B{r}", v, BLUE, NUM)
    r += 1

put(dm, "A32", "NMES ENROLLMENT, 1989-2025 (spring of school year; backs Figure 11)", SEC)
hist = [261, 255, 234, 225, 202, 203, 182, 196, 208, 198, 205, 195, 195, 203,
        196, 206, 204, 199, 211, 224, 217, 177, 165, 167, 154, 154, 155, 154,
        131, 131, 160, 160, 148, 153, 145, 135, 128]
years = list(range(1989, 2026))
r = 33
for i in range(19):
    put(dm, f"E{r+i}", str(years[i]), BOLD)
    put(dm, f"F{r+i}", hist[i], BLUE, NUM)
for i in range(19, 37):
    put(dm, f"H{r+i-19}", str(years[i]), BOLD)
    put(dm, f"I{r+i-19}", hist[i], BLUE, NUM)
put(dm, "A33", "Peak enrollment (1988-89)")
put(dm, "B33", "=MAX(F33:F51,I33:I50)", BLK, NUM)
put(dm, "A34", "Latest official count (2024-25)")
put(dm, "B34", "=I50", BLK, NUM)
put(dm, "A35", "Decline from peak")
put(dm, "B35", "=B33-B34", BLK, NUM)
put(dm, "A36", "Decline as a share of peak")
put(dm, "B36", "=B35/B33", BLK, PCT)
put(dm, "A37", "Current rated capacity")
put(dm, "B37", "=Assumptions!B12", GRN, NUM)
put(dm, "J33", "1989-2014 compiled by PublicSchoolReview from federal data; 2015-2025 match NCES directly", NOTE, wrap=True)

put(dm, "A54", "HONEST BOTTOM LINE", SEC)
put(dm, "A55", "Bourbon County faces a real demographic headwind: flat for fifty years, aging, land-constrained, projected down about 4% by 2040, and outside the Scott and Fayette growth corridor. Organic enrollment growth at NMES is unlikely. The growth case therefore rests on redistricting within the district and cross-county enrollment on quality under House Bill 563, plus the school's academic record and community-anchor value.", NOTE, wrap=True)

# ================= SCHOOL_DATA =================
sd = sheet("School_Data", [30] + [7.2] * 18 + [44])
put(sd, "A1", "School Data Backing the Report Figures", TITLE)
put(sd, "A2", "Inputs (blue) transcribed from public sources. Scores are SchoolDigger's normalized 0-100 'Average Standard Score' from KDE test data - not KDE's official rating. Confirm vs KDE Open House datasets before formal submission.", NOTE)

put(sd, "A4", "NMES ENROLLMENT BY SCHOOL YEAR (backs Figure 11)", SEC)
eyears = ["'15-16", "'16-17", "'17-18", "'18-19", "'19-20", "'20-21", "'21-22", "'22-23", "'23-24", "'24-25"]
ecounts = [154, 131, 131, 160, 160, 148, 153, 145, 135, 128]
put(sd, "A5", "School year", bold=True)
put(sd, "A6", "Students")
for i, (y, v) in enumerate(zip(eyears, ecounts)):
    col = get_column_letter(2 + i)
    put(sd, f"{col}5", y, BOLD)
    put(sd, f"{col}6", v, BLUE, NUM)
put(sd, "T6", "NCES school-level data (as compiled by PublicSchoolReview); 2024-25 = NCES CCD official count", NOTE, wrap=True)
put(sd, "A8", "Rated capacity (2021 facility plan)"); put(sd, "B8", 174, BLUE, NUM)
put(sd, "A9", "Open seats, 2024-25"); put(sd, "B9", "=B8-K6", BLK, NUM)
put(sd, "A11", "Note: the superintendent has publicly said 'around 100'; a '118' figure could not be verified in any official record.", NOTE)

put(sd, "A13", "ELEMENTARY SCORES BY YEAR, 2007-2025 (backs Figures 6 and 7)", SEC)
syrs = [str(y) for y in range(2007, 2020)] + [str(y) for y in range(2021, 2026)]
put(sd, "A14", "School (district)", bold=True)
for i, y in enumerate(syrs):
    put(sd, f"{get_column_letter(2 + i)}14", y, BOLD)
put(sd, "T14", "SchoolDigger rendering of KDE test data. No statewide tests in 2020; NMES 2021 not reported. Assessment systems: CATS/KCCT 2007-11, K-PREP 2012-19, KSA 2021-25.", NOTE, wrap=True)
NAv = None
scores = [
 ("North Middletown (Bourbon Co.)", [56.5, 63.9, 68.6, 87.9, 85.8, 72.5, 67.6, 56.6, 56.9, 48.7, 49.3, 40.0, 50.4, NAv, 47.7, 32.1, 54.1, 58.2]),
 ("Bourbon Central (Bourbon Co.)", [77.5, 81.9, 72.6, 69.6, 63.0, 74.7, 67.6, 51.8, 52.1, 30.0, 34.0, 32.8, 39.9, 20.0, 29.9, 29.0, 23.8, 26.5]),
 ("Cane Ridge (Bourbon Co.)", [35.2, 50.9, 56.2, 65.5, 34.5, 34.0, 49.6, 51.0, 51.1, 57.5, 50.4, 41.4, 38.8, 23.8, 38.7, 34.6, 35.8, 19.3]),
 ("Paris Elementary (Paris Indep.)", [NAv]*16 + [16.8, 12.2]),
 ("Shearer (Clark Co.)", [NAv]*16 + [30.7, 42.3]),
 ("Justice (Clark Co.)", [NAv]*16 + [43.2, 39.3]),
 ("Strode Station (Clark Co.)", [NAv]*16 + [43.2, 34.2]),
 ("Conkwright (Clark Co.)", [NAv]*16 + [15.6, 17.5]),
 ("Northview (Montgomery Co.)", [NAv]*16 + [67.4, 68.9]),
 ("Mapleton (Montgomery Co.)", [NAv]*16 + [65.9, 65.1]),
 ("Nicholas County Elementary (Nicholas Co.)", [NAv]*16 + [15.9, NAv]),
]
rr = 15
for name, vals in scores:
    put(sd, f"A{rr}", name)
    for i, v in enumerate(vals):
        if v is not None:
            put(sd, f"{get_column_letter(2 + i)}{rr}", v, BLUE, "0.0")
    rr += 1

put(sd, "T25", "Nicholas County: 2024 value; 2025 not retrieved", NOTE)
put(sd, "A26", "Three-year average, 2023-2025: NMES / Bourbon Central / Cane Ridge")
put(sd, "B26", "=AVERAGE(Q15:S15)", BLK, "0.0")
put(sd, "C26", "=AVERAGE(Q16:S16)", BLK, "0.0")
put(sd, "D26", "=AVERAGE(Q17:S17)", BLK, "0.0")

put(sd, "A28", "NMES DETAIL, 2024-25 (backs Section 5)", SEC)
put(sd, "B29", "NMES", BOLD); put(sd, "C29", "Kentucky", BOLD)
detail = [
 ("Reading, proficient or better", 0.50, 0.50, PCT),
 ("Mathematics, proficient or better", 0.44, 0.44, PCT),
 ("Writing, proficient or better", 0.58, 0.38, PCT),
 ("Science, proficient or better", 0.53, 0.37, PCT),
 ("Composite: economically disadvantaged students", 57.1, None, "0.0"),
 ("Composite: female students", 85.7, None, "0.0"),
 ("Composite: male students", 28.8, None, "0.0"),
]
rr = 30
for label, nm, ky, fmt in detail:
    put(sd, f"A{rr}", label)
    put(sd, f"B{rr}", nm, BLUE, fmt)
    if ky is not None:
        put(sd, f"C{rr}", ky, BLUE, fmt)
    rr += 1
put(sd, "T30", "SchoolDigger/KDE; economically disadvantaged composite = 62nd percentile statewide; female = 91st", NOTE, wrap=True)

# ---- finish ----
del wb["Sheet"]
for ws in wb.worksheets:
    ws.sheet_view.showGridLines = True
wb.save("/home/claude/nmes/NMES_Financial_Model.xlsx")
print("model written")
