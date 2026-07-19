from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                Image, Table, TableStyle, HRFlowable, KeepTogether)
from PIL import Image as PILImage

NAVY = colors.HexColor("#1F3864")
GOLD = colors.HexColor("#2E75B6")
GRAY = colors.HexColor("#555555")
LINE = colors.HexColor("#B9C2D0")
HEADBG = colors.HexColor("#E8EDF5")
ROWBG = colors.HexColor("#F5F7FA")

W = 6.7 * inch  # usable frame width

# ---------------- styles ----------------
body = ParagraphStyle("body", fontName="Times-Roman", fontSize=10.3, leading=14.2,
                      alignment=TA_JUSTIFY, spaceAfter=7, textColor=colors.HexColor("#1A1A1A"))
lede = ParagraphStyle("lede", parent=body, fontSize=10.8, leading=15.2)
bullet = ParagraphStyle("bullet", parent=body, leftIndent=16, bulletIndent=4, spaceAfter=5)
h1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=14.5, leading=17.5,
                    textColor=NAVY, spaceBefore=16, spaceAfter=7, keepWithNext=1)
h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=11.2, leading=14,
                    textColor=colors.HexColor("#2E5395"), spaceBefore=10, spaceAfter=5, keepWithNext=1)
cap = ParagraphStyle("cap", fontName="Helvetica-Oblique", fontSize=8.2, leading=10.5,
                     textColor=GRAY, spaceBefore=3, spaceAfter=12)
tcell = ParagraphStyle("tcell", fontName="Helvetica", fontSize=8.4, leading=10.6,
                       textColor=colors.HexColor("#1A1A1A"))
tcellb = ParagraphStyle("tcellb", parent=tcell, fontName="Helvetica-Bold")
thead = ParagraphStyle("thead", fontName="Helvetica-Bold", fontSize=8.6, leading=10.8,
                       textColor=NAVY)
qstyle = ParagraphStyle("q", parent=body, leftIndent=22, firstLineIndent=-22, spaceAfter=6.5)
note = ParagraphStyle("note", parent=body, fontSize=9.2, leading=12.6, textColor=GRAY)

story = []
A = story.append

def P(t, s=body):
    A(Paragraph(t, s))

def B(t):
    A(Paragraph(t, bullet, bulletText="\u2022"))

class HRK(HRFlowable):
    keepWithNext = 1
    def getKeepWithNext(self):
        return 1

def H(t):
    A(Paragraph(t, h1))
    A(HRK(width="100%", thickness=0.8, color=LINE, spaceAfter=8))

def H2(t):
    A(Paragraph(t, h2))

def fig(png, caption, width=W):
    im = PILImage.open(f"/home/claude/nmes/{png}")
    w, h = im.size
    height = width * h / w
    A(KeepTogether([Image(f"/home/claude/nmes/{png}", width=width, height=height),
                    Paragraph(caption, cap)]))

def tbl(header, rows, widths, caption=None, bold_first_col=False, align_right_from=None):
    data = [[Paragraph(c, thead) for c in header]]
    for r in rows:
        row = []
        for i, c in enumerate(r):
            st = tcellb if (bold_first_col and i == 0) else tcell
            row.append(Paragraph(c, st))
        data.append(row)
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), HEADBG),
        ("LINEBELOW", (0, 0), (-1, 0), 0.9, NAVY),
        ("LINEBELOW", (0, -1), (-1, -1), 0.6, LINE),
        ("LINEABOVE", (0, 0), (-1, 0), 0.6, LINE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ROWBG]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]
    t.setStyle(TableStyle(style))
    if caption and len(rows) <= 8:
        A(KeepTogether([t, Paragraph(caption, cap)]))
    elif caption:
        A(t)
        A(Paragraph(caption, cap))
    else:
        A(t)

# ================= COVER =================
A(Spacer(1, 1.35 * inch))
A(Paragraph("AN INDEPENDENT REVIEW OF PUBLIC RECORDS", ParagraphStyle(
    "kick", fontName="Helvetica-Bold", fontSize=9, textColor=GOLD, alignment=TA_CENTER, spaceAfter=18)))
A(Paragraph("Saving North Middletown<br/>Elementary School", ParagraphStyle(
    "title", fontName="Helvetica-Bold", fontSize=27, leading=32, textColor=NAVY,
    alignment=TA_CENTER, spaceAfter=10)))
A(Paragraph("A Deep Dive into Bourbon County Schools", ParagraphStyle(
    "sub", fontName="Times-Italic", fontSize=15.5, leading=19, textColor=colors.HexColor("#333333"),
    alignment=TA_CENTER, spaceAfter=22)))
A(HRFlowable(width=2.2 * inch, thickness=1.1, color=GOLD, hAlign="CENTER", spaceAfter=22))
A(Paragraph("Prepared for the North Middletown community and the members of the<br/>Bourbon County Board of Education",
            ParagraphStyle("pf", fontName="Times-Roman", fontSize=11.5, leading=15,
                           alignment=TA_CENTER, textColor=colors.HexColor("#1A1A1A"), spaceAfter=8)))
A(Paragraph("Paris and North Middletown, Kentucky &nbsp;\u2022&nbsp; July 2026",
            ParagraphStyle("pf2", fontName="Helvetica", fontSize=9.5, alignment=TA_CENTER,
                           textColor=GRAY, spaceAfter=6)))
A(Paragraph("Written by a former NMES King, with the help of an AI research assistant",
            ParagraphStyle("pf3", fontName="Helvetica-Oblique", fontSize=9, alignment=TA_CENTER,
                           textColor=GRAY, spaceAfter=0)))
A(Spacer(1, 2.2 * inch))
scope = ("This review draws exclusively on public records: the district's audited financial statements for the "
         "fiscal years ending June 30, 2024 and June 30, 2025; Kentucky Department of Education funding, facility, "
         "and school report card data; federal enrollment records; municipal bond disclosures; state regulations; and "
         "contemporaneous local reporting. Where a figure is an estimate rather than a published number, it is labeled "
         "as an estimate and its assumptions are stated. This document is not an audit, and it alleges no misconduct "
         "by any person; both years of the district's financial statements received clean opinions from its independent "
         "auditors. Its purpose is narrower and simpler: to lay out what the public record shows, and what it does not "
         "yet show, before an irreversible decision is made about a community's school. I am an alumnus of this school, "
         "and I wrote this report with the help of Fable 5, an AI research assistant from Anthropic; every figure "
         "should be re-verified against the cited primary sources before formal submission or republication.")
st = Table([[Paragraph(scope, ParagraphStyle("scope", fontName="Times-Roman", fontSize=9.3,
                                             leading=12.6, textColor=colors.HexColor("#333333")))]],
           colWidths=[W])
st.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F3F5F9")),
                        ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                        ("TOPPADDING", (0, 0), (-1, -1), 9),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
                        ("LEFTPADDING", (0, 0), (-1, -1), 11),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 11)]))
A(st)
A(PageBreak())

# ================= 1. EXECUTIVE SUMMARY =================
H("1. Executive Summary")
P("On July 15, 2026, the Local Planning Committee of Bourbon County Schools voted to reclassify North "
  "Middletown Elementary School from a \u201cpermanent\u201d to a \u201ctransitional\u201d facility in the district's draft "
  "four-year facility plan, the procedural first step toward closing the school. The committee's vote is advisory. "
  "The decision belongs to the elected Board of Education, and under state regulation it cannot take effect without "
  "further committee action, a public hearing, and approval by the Kentucky Board of Education. Superintendent Larry "
  "Begley has said publicly that \u201cthe decision is not final.\u201d", lede)
P("I wrote this report to examine the district's finances in depth, so the Board and the public can weigh that decision on "
  "the actual record. Three conclusions follow from it.")
P("<b>First, the district's budget problem is real.</b> The General Fund ran operating deficits before transfers of "
  "$2.54 million in fiscal 2024 and $2.65 million in fiscal 2025, and reserves have fallen from $6.58 million to "
  "$4.29 million in two years. The causes are identifiable: about $2.95 million in one-time federal pandemic aid "
  "expired; attendance-based state funding fell as roughly 248 students' worth of Average Daily Attendance "
  "disappeared after the pandemic hold-harmless ended; and several district-controlled costs grew quickly, led by "
  "central-office administration, up 44.8 percent in two years. Behind the attendance line sits a demographic "
  "fact I will not dodge: Bourbon County has hovered near twenty thousand residents for fifty years "
  "and is projected to shrink slightly by 2040.")
P("<b>Second, North Middletown Elementary did not cause the problem, and closing it will not fix it.</b> The school's "
  "costs are long-standing and stable. The \u201cover a million dollars\u201d figure cited for keeping it open is a gross "
  "site cost, not a savings estimate: the 128 students do not disappear, their teachers and their state funding move "
  "with them, and the district's fastest-growing expense, transportation, up 20.3 percent last year, would rise "
  "further with longer bus routes. Most building money in Kentucky school finance is legally restricted and cannot "
  "pay teachers in any case. A realistic net recurring saving, estimated in Section 4, is on the order of $250,000 to "
  "$600,000, a fraction of the deficit, and less than several alternatives that harm no one.")
P("<b>Third, the district has not yet shown its work.</b> No line-item net-savings analysis, transportation model, "
  "receiving-school capacity study, building condition assessment, or alternatives comparison has been published. "
  "Meanwhile the school proposed for closure is, on the state's own accountability composite, the district's "
  "highest-performing elementary, scoring 58.2 in 2024-25 against 26.5 and 19.3 at the two schools that would "
  "receive its students.")
P("The report closes with ten questions the administration should be required to answer in writing before any vote, "
  "a menu of revenue and cost measures worth an estimated $1.1 to $2.1 million a year without closing a school, and "
  "staged recommendations with clear decision thresholds. The district retains roughly $4.3 million in General Fund "
  "balance and is drawing it down at $1.1 to $1.2 million a year. There is a real problem here, and there is also "
  "time to solve it well. The ask is specific: pause any vote until the ten questions in this report are "
  "answered in writing.")

# ================= 2. WHERE THINGS STAND =================
H("2. Where Things Stand: The Decision and the Process")
tbl(["Date (2026)", "Event"],
    [["Early July",
      "As the district develops its four-year District Facility Plan, word spreads that closure of North Middletown "
      "Elementary is under discussion. North Middletown Mayor Jeff McFarland calls closure \u201cpossible and maybe even "
      "a probable outcome,\u201d and notes that \u201cthe past several years, North Middletown has been right at the top of "
      "the county\u201d on state testing."],
     ["July 9",
      "First Local Planning Committee public session; community concern grows."],
     ["July 15",
      "Second committee session and public forum at Bourbon County High School. Roughly 100 supporters attend; a "
      "30-minute forum runs about an hour and a half. Afterward the committee votes to classify the school as "
      "\u201ctransitional\u201d rather than \u201cpermanent,\u201d allowing a draft facility plan to be prepared without it. The "
      "committee can only recommend; it cannot close a school."],
     ["July 15-16",
      "Superintendent Larry Begley states the school serves about 100 students (federal records show 128), that "
      "keeping it open \u201ccost over a million dollars last school year,\u201d and that \u201cthe decision is not final.\u201d"],
     ["July 23 (scheduled)",
      "Community meeting set at the school for 6:30 p.m.; students and alumni invited to write letters of "
      "support."],
     ["July 29 (scheduled)",
      "Next Local Planning Committee public forum on the draft facility plan."]],
    [1.05 * inch, 5.65 * inch],
    caption="Figure 1. Timeline of the North Middletown Elementary decision, compiled from local reporting "
            "(WKYT; FOX 56; The Bourbon County Citizen), July 2026.",
    bold_first_col=True)
P("The remaining process is set by state regulation (702 KAR 4:180 and the Kentucky School Facilities Planning "
  "Manual). After the committee finishes its draft, the plan goes to the Kentucky Department of Education for review, "
  "returns to the committee for a vote, must be adopted by the local Board of Education, is subject to a formal "
  "public hearing, and finally requires approval by the Kentucky Board of Education. A \u201ctransitional\u201d label in a "
  "facility plan is a planning classification, not a closure: no school closes unless and until the elected local "
  "Board votes to close it. Each of those steps is a point at which Board members and the public can insist on the "
  "documentation this report describes, and at which written objections become part of the official record that "
  "goes to Frankfort.")

# ================= 3. FINANCES =================
H("3. The District's Finances: A Real Problem With Clear Causes")
P("I do not dispute that Bourbon County Schools faces genuine budget pressure. The district's own "
  "audited statements, prepared by Summers, McCrary and Sparks, PSC and posted by the Kentucky Department of "
  "Education, show it plainly.")
tbl(["General Fund (audited)", "FY2023", "FY2024", "FY2025"],
    [["Revenues, before transfers", "$27,668,655", "$24,952,644", "$26,449,318"],
     ["Expenditures, before transfers", "$27,905,775", "$27,487,732", "$29,097,404"],
     ["Operating result before transfers", "($237,120)", "($2,535,088)", "($2,648,086)"],
     ["Net transfers and other sources", "", "$1,469,431", "$1,422,621"],
     ["Change in fund balance", "", "($1,065,657)", "($1,225,465)"],
     ["Ending fund balance", "$6,582,802", "$5,516,305", "$4,290,840"],
     ["Unassigned portion", "", "$5,301,744", "$3,925,193"]],
    [2.55 * inch, 1.38 * inch, 1.38 * inch, 1.39 * inch],
    caption="Figure 2. Three-year General Fund summary, from the district's audited financial statements for the "
            "years ended June 30, 2024 and June 30, 2025. The fiscal 2023 revenue figure reflects a different "
            "presentation of state pension payments made on the district's behalf and is shown for context.",
    bold_first_col=True)
fig("chart_gf.png",
    "Figure 3. The operating gap and the drawdown. The district spends roughly $2.5 to $2.6 million more from its "
    "General Fund than it takes in before transfers, and reserves have fallen about $2.3 million in two years. "
    "Source: audited financial statements, FY2024 and FY2025.")
P("A reading note on the transfers line, because it softens the optics without changing the arithmetic: "
  "“net transfers and other sources” of roughly $1.4 million a year are moves between the district's own "
  "funds, indirect cost recoveries from grants and self-supporting operations and similar interfund items "
  "detailed in the audits' fund statements, not new money from outside. They cushion the General Fund's "
  "reported change in fund balance, which is why the honest measure of the structural problem is the "
  "operating result before transfers: the district spends about $2.6 million more than it takes in, and "
  "internal shuffling covers roughly half the gap while reserves absorb the rest.")
H2("Why it happened")
fig("chart_cliff.png",
    "Figure 4. The two revenue shocks. Federal revenue in the governmental funds fell $2.95 million from FY2023 to "
    "FY2025 as ESSER pandemic aid expired, and attendance-based state funding fell with roughly 248 fewer funded "
    "students. Sources: audited financial statements; SEEK attendance figures reported in the audits.")
P("Three forces converged. One-time federal pandemic relief, the ESSER programs, wound down, taking about "
  "$2.95 million a year with it while the staff and programs it paid for remained. Average Daily Attendance, the "
  "basis of Kentucky's SEEK funding formula, fell from a pandemic hold-harmless figure of 2,490 to 2,243, a "
  "recurring revenue loss on the order of $1.1 million a year at the current base guarantee of $4,586 per student. "
  "And the state's new two-year budget offers little relief: the SEEK base rises less than one percent in fiscal "
  "2027, and state school-bus funding is frozen roughly $90 million a year below what Kentucky statute calls for, "
  "statewide.")
P("At the same time, several costs the district controls grew quickly: a two-percent raise in fiscal 2024 with "
  "\u201csome employees receiving much more,\u201d in the words of the district's own audit narrative, step increases in "
  "fiscal 2025, transportation up 20.3 percent in a single year, and central-office administration up 44.8 percent "
  "in two years (Section 8). A $6.055 million bond issued in 2024 added roughly $430,000 a year of debt payments "
  "through 2044 (Section 6).")
P("Two facts round out the picture, and both cut in the community's favor. The district has already shown it can fix "
  "a money-losing operation without closing anything: between fiscal 2024 and 2025 it cut the day-care fund's loss "
  "from $722,828 to $79,010 and swung food service from a $610,606 loss to a $179,197 surplus, a combined "
  "improvement of about $1.4 million in one year. Even if part of that swing reflects one-time pricing and "
  "reimbursement changes, it shows that focused management can move seven figures without touching a school. "
  "And the district is not in collapse: both audits carry clean "
  "opinions, the fiscal 2026 budget holds a $1,411,076 contingency above the state's two-percent minimum, and at "
  "the current pace of drawdown the unassigned reserve lasts roughly three more budget cycles. The problem is real. "
  "So is the time to address it deliberately.")

# ================= 4. MILLION DOLLAR QUESTION =================
H("4. The Million-Dollar Question: What Closing the School Would Actually Save")
P("The case for closure rests on a single public statement: that keeping North Middletown Elementary open \u201ccost "
  "over a million dollars last school year.\u201d No supporting worksheet has been released. The state's own school "
  "spending data put that number in context.")
fig("chart_pp.png",
    "Figure 5. Per-student spending at the district's three elementary schools, 2023-24, as published in the "
    "Kentucky School Report Card's school-level expenditure data (total of state, local, and federal dollars).")
P("North Middletown's $19,348 per student is the highest of the three elementaries, and that is exactly what "
  "arithmetic predicts for a small school, because one principal, one office, one kitchen, and one heated building "
  "divide across 128 children instead of 450. Multiplied out, the school's total site spending is about $2.5 "
  "million, of which roughly $1.8 million is state and local money. But almost none of that total is what a closure "
  "would save, for a simple reason: <b>closing a school does not delete its students.</b>")
P("The 128 children would still need teachers, about eight to nine classrooms' worth at the district's average "
  "ratios, and Bourbon Central (459 students) and Cane Ridge (453 students) would each absorb roughly 64 more "
  "children across six grade levels, adding sections in several of them. The children's SEEK funding transfers with "
  "them. Food service, now a self-supporting operation, follows the meal counts. What is genuinely avoidable is the "
  "fixed layer: the principal and office staff, custodial time, utilities, and insurance, and only if the building "
  "is sold or fully repurposed rather than mothballed. Against those savings run the new costs: longer bus routes "
  "in the district's fastest-growing and worst-reimbursed budget line (families have warned of rides exceeding two "
  "hours a day), any staffing or space additions at the receiving schools, transition costs, and the quiet revenue "
  "risk that some families leave the district altogether, each departure taking at least $4,586 a year in base "
  "state funding with it, permanently.")
P("Put together, a defensible planning estimate of the net recurring General Fund saving is roughly <b>$250,000 to "
  "$600,000 a year</b>, an estimate, clearly labeled as such, that the district could replace tomorrow with a real "
  "worksheet. Even on assumptions generous to the district, five positions eliminated instead of three, busing "
  "at the low end, and not one family leaving, the arithmetic tops out in the low $600,000s, still under a "
  "quarter of the structural deficit (the companion workbook shows this case explicitly). The reason for "
  "skepticism about even that number is not theoretical. Districts across the country have run exactly this "
  "play, and the results are on the record. One more thing closure does not buy: borrowing room. Bonding "
  "capacity is built from restricted revenue streams that do not grow when a school closes (Section 6).")
H2("What happened when other districts tried this")
B("<b>Chicago, 2013.</b> The district closed about fifty schools projecting roughly $1 billion over a decade, "
  "including $43 million a year in operations. A 2023 Sun-Times and WBEZ analysis found actual labor savings of "
  "about $25 million a year, some $18 million short, while the district borrowed $329 million to prepare "
  "receiving schools, and a decade on more than half of the 46 emptied buildings still sat unused. The "
  "University of Chicago's own research consortium found displaced students' math scores depressed for up to "
  "four years.")
B("<b>Twelve districts, 2013.</b> The Pew Charitable Trusts studied a dozen districts that had closed schools and "
  "found 301 buildings still sitting unused, with those that did sell typically fetching $200,000 to $1 million, "
  "well below initial projections.")
B("<b>West Virginia, 1990-2002.</b> The state closed more than 300 schools and spent over $1 billion "
  "consolidating; the head of its own School Building Authority conceded in 2002 that the closings did not save "
  "taxpayers money. Local administrative staff grew 16 percent while enrollment fell 13 percent, and the state came "
  "to spend more of its education dollar on busing than any other.")
B("<b>Vermont, 2017-2020.</b> A 2024 Yale economics thesis by Grace Miller, studying 109 districts merged "
  "under Act 46, found no significant "
  "change in per-pupil spending or tax rates: administrative savings were absorbed almost entirely by higher "
  "salaries, benefits, and transportation.")
B("<b>California, 2026.</b> A Stanford analysis for the Getting Down to Facts project found that after "
  "closures amid enrollment decline, spending fell about $440 "
  "per pupil, and revenue fell by effectively the same amount, with no reduction in teachers or staff. Districts "
  "broke even. Earlier research puts typical closure savings below five percent of a district's budget.")
P("Student costs compound the fiscal ones: a 2024 national study following 470 Texas closures found displaced "
  "children, low-income children most of all, absent more often, disciplined more often, and earning less as "
  "adults. Roughly three-quarters or more of North Middletown's students qualify for free or reduced-price meals. "
  "If Bourbon County believes its closure would beat this record, the burden is on the administration to show the "
  "arithmetic.")
P("When the district's numbers are presented publicly, four framings deserve particular scrutiny, because "
  "each can make closure look better than it is: gross site cost presented as savings; restricted building "
  "dollars presented as operating relief; per-pupil cost cited without noting that state funding follows the "
  "student; and district-wide cost growth attributed to one small school. I have tried to avoid the "
  "mirror-image errors, and I flag my own judgment calls where they occur.")
P("Whatever the true net number proves to be, one comparison frames the decision: the district's structural deficit "
  "is about $2.6 million. Closing North Middletown Elementary addresses, at best, a small fraction of it, while "
  "the measures in Section 9 total more, harm no student, and close no town's school.")

# ================= 5. ACADEMICS =================
H("5. Academic Performance: The District Would Be Closing Its Best Elementary School")
fig("chart_district.png",
    "Figure 6. The full two-decade score history for every elementary school in the district, with Paris "
    "Independent's Paris Elementary for county context (reported from 2024). Values are SchoolDigger's normalized "
    "0-100 score computed from state test data, a consistent cross-year yardstick, not KDE's official rating. "
    "Dashed markers show where the underlying state assessment changed (2012 and 2021-22); no statewide tests were "
    "given in 2020, and North Middletown's 2021 result was not reported.")
fig("chart_compare.png",
    "Figure 7. The 2024-25 accountability composite for elementary schools across the region. Only Montgomery "
    "County's two elementaries outscore North Middletown; every elementary in Bourbon County, Clark County, and "
    "Paris Independent trails it.")
P("The pattern is hard to miss, and it runs in opposite directions. After a pandemic-era dip in 2023, North "
  "Middletown rebounded to 54.1 in 2024 and 58.2 in 2025, back above the state median, around the 60th "
  "percentile of Kentucky elementary schools, ranking 272nd of 685 statewide. Over the same stretch the receiving "
  "schools moved the other way: Bourbon Central has slid from 39.9 (2019) to 26.5, and Cane Ridge fell from 35.8 "
  "to 19.3 in a single year, both now in the bottom quarter of the state, alongside Paris Elementary at 12.2. "
  "Across the wider region (Figure 7), only Montgomery County's Northview and Mapleton outscore North Middletown; "
  "every elementary in Clark County and Paris Independent trails it. The two-decade record in Figure 6 "
  "deepens the contrast: around its Blue Ribbon years North Middletown scored 87.9 and 85.8, the top tier of "
  "the state, while Bourbon Central, the district's strongest elementary as recently as 2008 (81.9), has "
  "fallen by two-thirds.")
P("The profile beneath the composite has real texture. North Middletown students match the state average in "
  "reading (50 percent proficient or better) and mathematics (44 percent), and beat it decisively in writing (58 "
  "percent, twenty points above the state) and science (53 percent, sixteen above). Most striking for a school "
  "where about three-quarters of children qualify for free or reduced-price meals: its economically disadvantaged "
  "students scored 57.1, the 62nd percentile statewide, evidence that this environment lifts precisely the "
  "students the research says are hardest to lift.")
P("This is not a new story. In 2011 the U.S. Department of Education named North Middletown Elementary a "
  "<b>National Blue Ribbon School</b>, one of just five Kentucky public schools honored that year, an award "
  "reserved for schools performing in roughly the top ten percent of their state in reading and mathematics, and "
  "the state's education department separately gave it an inaugural Distinguished Winners Circle Award. In the "
  "years around that recognition the school ranked 36th of 683 Kentucky elementary schools (2010) and 51st of 688 "
  "(2011). The school the district proposes to close is not a school with a history of failure; it is a school "
  "with a history of excellence, now climbing back toward it.")
P("The record has always been built by people, and I will name the two who anchor it: Mrs. Beverly Craycraft "
  "and Mrs. Roxanne Mitchell. Every alumnus I talk to mentions them. For generations of North Middletown "
  "families, mine included, those two classrooms were where the standard for kindergarten through fifth grade "
  "was set. Mrs. Mitchell said it best herself, twenty years into her fifth grade room when the Blue Ribbon "
  "arrived, crediting the earlier grades with \u201cproviding the foundation my students need in basic geography "
  "skills\u201d and pointing to traditions that reached beyond the walls: \u201cIt has been customary for 3rd-grade "
  "students to tour stops along the Underground Railroad in northern Kentucky.\u201d The "
  "honors around them are documented: Alison Cloyd (2014) and Lydia Austin (2017) each received Campbellsville "
  "University's Excellence in Teaching Award, the statewide honor for which a district puts forward one teacher "
  "at a time, and the Blue Ribbon culture ran on programs the community itself powered, none more distinctive "
  "than \u201cArtBurst,\u201d which threaded the performing and creative arts through core academics with volunteers "
  "teaching art forms and students performing weekly. Those educators set a standard, and the school's history "
  "belongs to them. Its present belongs to a new set of educators proving equal to it: under principal Hannah "
  "Southall, the current staff has lifted the school from 32.1 to 54.1 to 58.2 in two years, keeps a "
  "gifted-and-talented program running, and draws the kind of testimony money cannot buy, a parent writing this "
  "month that her child \u201cfeels so loved and welcomed by each and every teacher.\u201d The people who set the "
  "standard have successors already making the climb. What that faculty needs is not consolidation. It is time, "
  "and a district willing to back them.")
P("Two honest caveats belong here. Small schools produce noisier year-to-year scores, 128 students is a small "
  "sample, and subgroup results vary widely: the school's girls (85.7, the 91st percentile) far outpace its boys "
  "(28.8), a gap the district should be helping the school close rather than closing the school. The same "
  "caution cuts both ways: no single year should define any school, which is why three-year averages matter, "
  "and they tell the same story. North Middletown averages 48.1 for 2023 through 2025, against 26.4 at Bourbon "
  "Central and 29.9 at Cane Ridge. Neither caveat "
  "changes the central fact: the consolidation "
  "on the table would move children from the district's strongest elementary environment into its weakest ones. If "
  "the administration believes those receiving schools can preserve these students' outcomes, that belief should be "
  "supported in writing, with a transition plan, before any vote, not assumed after one.")

# ================= 6. BONDS =================
H("6. Bonds, Buildings, and Two Different Pots of Money")
P("Kentucky school finance separates operating money from building money, and the distinction decides what a "
  "closure can and cannot accomplish. Districts do not borrow directly: a Finance Corporation, legally distinct "
  "but composed of the same people as the Board, issues bonds and leases the buildings back to the district. The "
  "state's School Facilities Construction Commission (SFCC) pays part of qualifying debt; the local share comes from "
  "restricted facility revenues, chiefly the \u201cnickel\u201d building tax (about $2.05 million in fiscal 2025) and the "
  "capital outlay allotment. <b>None of that money can lawfully pay teachers or plug the operating deficit.</b> "
  "\u201cWe spend a great deal on buildings\u201d and \u201cwe cannot afford to operate a school\u201d describe two different pots, "
  "and the public conversation should keep them separate.")
tbl(["Series", "Original amount", "Interest rate", "Final maturity", "Outstanding 6/30/25"],
    [["2013", "$2,255,000", "1.90-2.10%", "2026", "$348,000"],
     ["2013R (refunding)", "$468,000 *", "2.75-4.05%", "2033 *", "$585,000 *"],
     ["2016", "$5,700,000", "1.00-3.00%", "2029", "$3,145,000"],
     ["2018", "$1,850,000", "3.50%", "2038", "$1,560,000"],
     ["2020", "$3,620,000", "0.50-1.85%", "2031", "$3,405,000"],
     ["2023", "$810,000", "3.65-4.00%", "2034", "$755,000"],
     ["2024", "$6,055,000", "4.00-5.00%", "2044", "$5,945,290"],
     ["<b>Total</b>", "<b>$20,758,000</b>", "", "", "<b>$15,743,290</b>"]],
    [1.15 * inch, 1.45 * inch, 1.25 * inch, 1.2 * inch, 1.65 * inch],
    caption="Figure 8. Outstanding bonds of the Bourbon County School District Finance Corporation, from Note 4 of "
            "the FY2025 audited financial statements. The 2016 issue refinanced $5,315,000 of 2009 bonds (saving "
            "$314,834 in present value) and the 2020 issue refinanced $3,410,000 of 2011 bonds (saving $106,627). "
            "* The audit's figures for the 2013R issue are internally inconsistent: the outstanding balance exceeds "
            "the listed original amount, and the stated maturity contains an obvious typographical error. Both are details "
            "the finance office should correct on the record.",
    bold_first_col=True)
fig("chart_debt.png", "Figure 9. Annual bond payments are rising as the 2024 issue comes online. The state's SFCC "
    "pays $1,568,809 of the outstanding principal over the life of the bonds. Source: FY2024 and FY2025 audits.",
    width=4.6 * inch)
P("Three findings from the bond record deserve the Board's attention.")
B("<b>The 2024 borrowing funds an active project that has not been publicly tied to any school the district "
  "proposes to keep or close.</b> The $6.055 million issue flowed into the Construction Fund, and construction in "
  "progress grew from $3.65 million to $7.41 million during fiscal 2025, matching that fund's spending almost to "
  "the dollar. District planning documents describe an ambition to build a career-and-technical learning center, "
  "potentially in partnership with Bluegrass Community and Technical College; the bond's official statement and the "
  "state project application (the BG-1) would say definitively, and should be published alongside any closure "
  "discussion.")
B("<b>No bond issue on record names North Middletown Elementary.</b> The capital program has flowed elsewhere for "
  "years, which raises a fairness question the administration should answer directly: was the school passed over "
  "for investment before being described as too costly to keep?")
B("<b>The construction fund ran a negative $1.43 million restricted balance at June 30, 2024</b>, project spending "
  "ran ahead of the borrowing that later covered it. Not improper in itself, but it shows a capital program being "
  "prioritized and cash-flowed in the same years the operating budget went into deficit. The fiscal 2024 audit also "
  "notes the district held $23.5 million in unused bonding capacity, borrowing room for buildings that, again, "
  "cannot pay teachers either way.")
H2("What closing a school does, and does not do, to bonding capacity")
P("A district's ability to borrow for buildings is arithmetic set by statute and regulation, and it is worth "
  "walking through, because “bonding capacity” is likely to surface in the closure debate. Kentucky districts "
  "build capacity from two restricted streams: the capital outlay allotment of $100 per student in average daily "
  "attendance (KRS 157.420), of which regulation lets a district pledge 80 percent, the rest held back as a "
  "safety factor (702 KAR 4:160), and the restricted building-fund levy, the “nickel,” with its state FSPK "
  "equalization (KRS 157.440). Set existing debt payments against those streams and what remains is the room for "
  "new debt. On the fiscal 2025 numbers: roughly $224,000 a year of capital outlay, about $2.05 million of "
  "building-fund tax, and $1.58 million of district-paid debt service in fiscal 2026. The fiscal 2024 audit "
  "states the bottom line plainly: about $23.5 million of unused bonding capacity. The companion workbook lays "
  "the components side by side on the Debt_Service tab.")
P("Nothing in that arithmetic grows when a school closes. Closing North Middletown adds no assessment, no "
  "attendance, and no levy. What it changes is the plan, not the capacity: a “transitional” label removes the "
  "school's modest listed needs from the priority list and steers future SFCC offers of assistance (KRS "
  "157.622), and the district's own borrowing, toward other projects, such as the career-and-technical center "
  "ambition in the district's planning documents. That is a choice about priorities, and it deserves to be "
  "argued openly as one, with the bonding potential statement on the table. The arithmetic can also run against "
  "the district: every family that responds to closure by leaving takes $100 a year out of capital outlay and "
  "the SEEK base out of operations, permanently. Nor is an emptied building a windfall: the Pew study in "
  "Section 4 found districts typically realized $200,000 to $1 million on sales, one-time money that is itself "
  "restricted to capital use.")
P("As for where the 2024 borrowing went: the $6.055 million issue, at 4.00 to 5.00 percent interest through "
  "2044, flowed into the Construction Fund, where construction in progress grew from $3.65 million to $7.41 "
  "million during fiscal 2025, matching that fund's spending almost to the dollar, and it added roughly "
  "$430,000 a year of debt payments, which is why the district's share of debt service jumps from $1.15 "
  "million in fiscal 2025 to $1.58 million in fiscal 2026. The state's SFCC participates in the qualifying "
  "issues, paying $1,568,809 of principal over the life of the bonds. None of the seven outstanding issues "
  "names North Middletown Elementary. The two documents that would settle the 2024 bond's purpose beyond "
  "argument, the official statement and the BG-1 project application, are standard public records, and "
  "Question 7 asks for both.")

# ================= 7. THE BUILDING =================
H("7. The North Middletown Building Itself")
P("If the closure case rests on the building, the record so far does not support it. The school's sections date to "
  "1948, 1963, and 1964, an older plant, like much of the district. The state-approved District Facility Plan "
  "(adopted with Kentucky Board of Education approval in 2021) classifies North Middletown as a <b>permanent</b> "
  "kindergarten-through-five center with a capacity of 174, comfortably above its current 128 students. The "
  "improvements that plan lists for the school are modest and typical of buildings its age: life-safety upgrades "
  "(a sprinkler system, exit and emergency lighting), an accessibility ramp and elevator, and renovation of space "
  "for a vocal-music classroom. The plan's district-wide capital need of roughly $43.4 million is concentrated at "
  "the high school and middle school, not at North Middletown.")
P("The capacity number itself deserves scrutiny before anyone treats it as a wall. The 2021 plan rates North "
  "Middletown at 174 students; the same building, the same 1948, 1963, and 1964 sections, held 261 students "
  "at its 1988-89 peak, half again the current rating, and enrollment histories show it above 200 for most "
  "of the 1990s and 2000s. Nothing about the walls shrank. What changes a rated capacity under the state's "
  "facilities planning manual (702 KAR 4:180) is how rooms are counted: capacity is computed from the "
  "classrooms in regular homeroom use, at program class-size caps, discounted by a utilization factor, so "
  "every room reassigned over the years to preschool, intervention, special education services, or a "
  "computer lab quietly lowers the school's official capacity without a brick moving. Rated capacity, in "
  "other words, is a policy output the district itself controls, and it can be raised the same way it was "
  "lowered: by returning rooms to homeroom use as enrollment fills. Two records would settle the history, "
  "and Section 12 requests both: the pre-2021 facility plans, which carry the building's earlier rated "
  "capacities, and the room-by-room utilization worksheet behind the current 174. A closure case that "
  "leans on a capacity figure should first explain who set that figure, from what room assignments, and "
  "why the community should treat as fixed a number the administration can change with a room schedule.")
P("The 2026 planning cycle is supposed to rest on a fresh architect-and-engineer condition assessment of every "
  "building. If that assessment attaches a large renovation figure to North Middletown, the public has yet to see "
  "it, its author, or its assumptions, and it should be published before any \u201ctransitional\u201d designation is "
  "adopted. Two further points keep the building question in proportion. First, whatever renovation the school "
  "needs would be paid from the restricted facility funds described in Section 6, money that cannot close the "
  "operating deficit whether the school stays open or not. Second, the receiving schools carry their own listed "
  "expansion needs in the same plan; moving 128 children into them is not free of capital cost either. An empty "
  "building, finally, is not free: it must be secured, insured, minimally heated, and eventually disposed of, while "
  "the town loses its largest civic anchor, a community of about 610 people whose residents told the planning "
  "committee the school is \u201cthe heartbeat\u201d of the town.")

# ================= 8. ADMIN =================
H("8. Where the Money Is Actually Going: Administrative Growth")
fig("chart_admin.png",
    "Figure 10. Administration expense from the district's audited statements of activities. District (central "
    "office) administration grew from $999,727 in FY2023 to $1,447,164 in FY2025; school administration grew from "
    "$2,110,039 to $2,581,412 over the same two years.")
P("The single most striking controllable-cost trend in the audits is not at North Middletown. Central-office "
  "administration grew 44.8 percent in two years, an increase of $447,000 a year, comparable to or larger than "
  "any realistic net saving from closing the school, while enrollment and attendance fell. School-level "
  "administration grew 22.3 percent. Transportation grew 20.3 percent in fiscal 2025 alone, alongside bus purchases "
  "of roughly $888,000 and $691,000 in consecutive years. Single-year jumps can carry one-time costs, so the "
  "fair question is the multi-year trend and the routing, not any one invoice. Federal data most recently on "
  "file show the district "
  "reporting four central-office administrators and fifteen school administrators; reconciling that headcount "
  "against the dollar growth, position by position, is a reasonable ask before any classroom building closes.")
P("A caution belongs beside that number, offered here before anyone else raises it: functional expense lines "
  "in Kentucky school audits include allocated state pension payments made on the district's behalf, and "
  "reclassifications between categories can move money on paper without a single new hire. Some share of the "
  "44.8 percent may be accounting rather than administration. That possibility is not a defense of the trend; "
  "it is the reason I ask for a position-by-position accounting instead of assuming the worst. The "
  "growth is a question to be answered, not a verdict.")
P("I deliberately rely on the audited totals rather than individual salaries, because individual "
  "figures should come from official records: the Kentucky Department of Education's annual superintendent salary "
  "file and the district's own board-adopted administrator salary schedule, which sets pay by formula, a base "
  "teacher salary multiplied by a responsibility increment and an extended work year. Publishing those records, "
  "current and for the past five years, is part of the transparency the moment calls for, and appears among the "
  "questions in Section 10.")

# ================= 9. ALTERNATIVES =================
H("9. The Alternatives on the Table: Grow, Don't Close")
P("Every option below is available under current Kentucky law, and each comes with the question the administration "
  "should answer about it. Dollar values are planning estimates from the audited base figures, labeled as such; "
  "several overlap and cannot simply be summed. Even conservatively combined, they exceed both the realistic saving "
  "from closure and the district's annual reserve drawdown. One honesty note before the menu: the first "
  "revenue option is a tax adjustment, and I will not dress that up; the full rate analysis follows "
  "the menu, and it shows a district taxing near the bottom of its region. It asks the community to weigh "
  "a modest, no-recall increase against losing its school.")
H2("First among them: grow the Kings into the region's premier elementary school")
P("The strongest alternative is not defensive. Kentucky law already supplies the mechanism for growth: under House "
  "Bill 563 (2021), codified at KRS 157.350, a district that adopts a nonresident-student policy may, since July "
  "2022, enroll students from other counties and count them in its attendance for state SEEK funding, with no "
  "agreement from the child's home district required and tuition at the board's discretion. Every family North "
  "Middletown attracts brings at least the $4,586 base guarantee, plus applicable add-ons.")
P("North Middletown is built to compete for those families. It is a 2011 National Blue Ribbon school with a "
  "gifted-and-talented program, a 13.6-to-1 student-teacher ratio, and a 58.2 accountability composite that beats "
  "every elementary school in Bourbon County and every one in neighboring Clark County and Paris Independent "
  "(Conkwright 17.5, Strode Station 34.2, Justice 39.3, Shearer 42.3, Paris Elementary 12.2). Its state-approved "
  "capacity is 174 against 128 enrolled: forty-six open seats which, filled with transfer students at the base "
  "guarantee alone, represent roughly $211,000 a year in new recurring revenue at little marginal cost, before "
  "tuition, add-ons, or the further growth a themed program, a preschool satellite, and a serious marketing effort "
  "could generate along the U.S. 460 corridor, within a short drive of five surrounding counties. The question for "
  "the administration is why the district's only nationally honored school is slated for closure instead of "
  "expansion.")
P("Honesty requires naming the headwind first. Bourbon County has hovered near twenty thousand residents for "
  "more than fifty years, from 18,476 in 1970 to 20,252 in 2020, and the Kentucky State Data Center projects a "
  "decline of roughly four percent by 2040. The county is aging, its share of children is shrinking, and its "
  "celebrated horse-farm land base, the second largest stock of conserved farmland in Kentucky, structurally "
  "limits new subdivisions. The regional boom passed to the west: neighboring Scott County is projected to grow "
  "46 percent by 2050 and Fayette nearly ten, while Bourbon sits outside that corridor. The district's enrollment "
  "decline is real and structural, and I will not pretend otherwise. North Middletown Elementary itself "
  "tells the story: it held 261 children in 1988-89, about double today's 128 (Figure 11).")
P("But a school's enrollment does not have to wait on a county's birth rate, because the board controls two "
  "levers that demographics do not. The first is redistricting: attendance boundaries are the board's to draw, "
  "and with Bourbon Central at 459 students and Cane Ridge at 453 while the district's best elementary sits at "
  "128 of a rated 174, redrawing lines on the eastern side of the current zones, starting with families who "
  "already live closer to North Middletown than to their assigned school, would fill its open seats with "
  "children the district already educates, relieve the crowded Paris schools, and shorten those children's "
  "rides rather than lengthen them. The second is the county's edges: under House Bill 563, families just across the line in "
  "Clark, Nicholas, Bath, and Harrison counties can enroll at North Middletown and bring their state funding "
  "with them, and every nearby comparison school with a published score sits far below it, from Nicholas County Elementary near 16 "
  "and Conkwright at 17.5 to Strode Station at 34.2. The pitch is not that the region is growing. It is that the "
  "region's best small elementary has empty seats within a short drive of families across four counties whose current "
  "options score a third as high.")
P("Growth framed this way is reallocation and recruitment on quality, not a bet on a population rebound, and "
  "the near-term target is modest: returning to the 160 students the school enrolled as recently as 2019-20 "
  "takes just 32 children from a district of 2,600 and four neighboring counties.")
fig("chart_enroll.png",
    "Figure 11. NMES enrollment from 1989 through 2025 against its current state-rated capacity of 174. The "
    "school held 261 students at its 1988-89 peak, roughly double today's official count of 128. History "
    "compiled from federal school-level data. The long decline mirrors the county's flat population, which is "
    "exactly why this plan relies on boundary decisions and cross-county enrollment rather than demographics.",
    width=6.1 * inch)
H2("A worked example: rebalance the map, fill the school")
P("Here is one concrete scenario, arithmetic anyone can check, run in the workbook's Redistricting tab. Rezone "
  "30 students to North Middletown from the eastern edges of the two Paris-area attendance zones, drawing only "
  "from families who already live closer to North Middletown than to their assigned school, and recruit 16 "
  "cross-county transfers under House Bill 563. The school reaches exactly its rated 174. Bourbon Central eases "
  "from 459 to about 444 and Cane Ridge from 453 to about 438. No teacher is added at North Middletown: its "
  "nine classroom sections go from an average of about 14 students to about 19, still under the statutory caps "
  "of 24 in the primary grades (KRS 157.360). The 16 transfers bring roughly $74,000 a year of new SEEK "
  "revenue, supplies for all 46 added students cost about $18,000, and if the relief lets the receiving schools "
  "avoid or redeploy even one to two sections as the Paris side grows, the package is worth roughly <b>$140,000 "
  "to $225,000 a year, recurring</b>, while cutting North Middletown's much-cited cost per student from $19,348 "
  "to about $14,339, a 26 percent drop, purely by filling seats. Two assumptions are flagged in yellow in the "
  "workbook for the district to replace with real data: that rezoned students' bus routes shorten or hold even "
  "because they are chosen by proximity, and the receiving schools' grade-by-grade capacities, already a records "
  "ask in Question 3. This is what an unbiased boundary study looks like in miniature. The district holds the "
  "geocoded student counts and the routing data to run the full version, and it should, before any vote.")
fig("chart_balance.png",
    "Figure 12. One rebalancing scenario: North Middletown fills to its rated 174 while Bourbon Central and Cane "
    "Ridge each ease by about fifteen students. Enrollment counts as cited in Sections 4 and 9; the scenario "
    "levers (30 rezoned, 16 cross-county transfers) are adjustable in the companion workbook's Redistricting tab.", width=6.0 * inch)
H2("The transportation map, estimated from public geography")
P("The district has not published its zone map, its geocoded student counts, or its annual T-1 transportation "
  "report, so what follows is built from public geography and labeled accordingly; every input sits in yellow "
  "in the workbook's Transport_Geo tab for the district to replace. Bourbon County is about 290 square miles "
  "of land. Its people cluster west: Paris holds 10,171 of the county's 20,252 residents, against 747 in "
  "Millersburg and 610 in North Middletown. The district's own published attendance-zone view assigns the "
  "county's southeast, about 36 percent of its area, to North Middletown, with Millersburg in the northern "
  "zone, and the arithmetic follows: about 1.2 elementary students per square "
  "mile in the NMES zone, against roughly 4.9 in the two Paris-area zones and 3.6 district-wide. That density gap is "
  "not a detail; it is the exact variable state law funds on. KRS 157.370 sets transportation aid by "
  "transported pupils per square mile, paying more where density is low because low density costs more to "
  "serve. The funding history sharpens the point: the formula ran underfunded for two decades, the 2024-2026 "
  "state budget restored it to 90 and then 100 percent, computed on lagged fiscal 2023 costs, and the "
  "2026-2028 budget froze it again below the statute. A district that closes its one eastern school keeps "
  "every square mile of that coverage area and serves it with longer rides.")
tbl(["Zone", "Approx. area (sq mi)", "Elementary students", "Students per sq mi"],
    [["North Middletown zone (southeast)", "~105", "128", "~1.2"],
     ["Paris-area zones (north and southwest)", "~185", "912", "~4.9"],
     ["District overall", "290", "1,040", "3.6"]],
    [2.6 * inch, 1.35 * inch, 1.45 * inch, 1.3 * inch],
    caption="Zone areas traced from the district's published attendance-zone view onto the Census county outline; "
            "student counts as cited in Section 4. Approximate until the district releases its zone map and geocoded counts (Question 3).",
    bold_first_col=True)
fig("chart_map.png",
    "Figure 13. Where the students are: the three elementary attendance zones traced from the district's "
    "published zone view onto the U.S. Census county outline. Paris holds half the county's people and both "
    "receiving schools; Millersburg sits in the northern zone; the NMES zone runs about 1.2 students per "
    "square mile across roughly 105 square miles of the county's southeast.", width=5.2 * inch)
P("Now the closure arithmetic, bottom up. North Middletown sits about ten miles from the Paris schools on US "
  "460. Roughly 109 of the school's 128 students ride the bus on an estimated three rural routes. Extend "
  "those routes to Paris and each one adds about 40 bus-miles a day, out and back, morning and afternoon: "
  "about 20,400 added bus-miles a year. At a marginal cost of $2.50 to $4.50 per bus-mile that is $51,000 to "
  "$92,000 a year, and if the longer runs break the route tiering and force even one additional bus, add "
  "roughly $55,000 more. The bottom-up estimate therefore lands at about $51,000 to $147,000, squarely inside "
  "the $75,000 to $200,000 planning range this report has used from the start, and it validates the $137,500 "
  "midpoint in the closure model. It also prices the quieter cost: those are 15 to 20 added minutes each way "
  "for the county's easternmost children, on rides families already call long.")
P("Run the same arithmetic on the rebalancing scenario and the sign flips. Rezoned students already ride "
  "district buses today, ten miles west to the Paris schools; rezoning moves them to the school they live "
  "closest to, so the affected routes shorten, an estimated $10,000 to $18,000 a year saved. Rebalancing is "
  "transport-neutral at worst and modestly positive at best, while closure is a guaranteed transport "
  "increase. District-wide, the optimization lever in the menu below, routing software, tiered bells, and a "
  "right-sized fleet, remains worth 5 to 10 percent of the $2.9 million line, $145,000 to $290,000 a year, "
  "whichever way the boundary question is decided.")
P("The state-revenue side seals the comparison. Because the 2026-2028 appropriation is frozen at flat "
  "dollars computed on old costs, the marginal state reimbursement on any NEW busing mile is zero: every "
  "dollar of closure's added routes is district money. Rebalancing changes no transported-pupil count, so "
  "the district's KRS 157.370 allotment is untouched, and its SEEK revenue is untouched because the same "
  "students attend the same district. Cross-county transfer students add SEEK revenue while adding no "
  "required busing at all: under KRS 157.350 the receiving district sets its own transportation policy for "
  "nonresident students, and most Kentucky districts have families drive or meet routes at the county line. "
  "Redistricting, in short, does not raise transportation costs; on this arithmetic it trims them while the "
  "revenue side only gains.")
H2("How a real optimization would run, and who already runs them")
P("None of this requires inventing anything. The method is standard: geocode enrolled students from the "
  "student information system; aggregate to small planning zones; build a travel-time matrix from each zone "
  "to each school on the actual road network; then assign zones to schools to minimize total ride time, "
  "subject to building capacities, statutory class sizes, and keeping neighborhoods together, with bus "
  "routes re-optimized afterward. Kentucky districts already do versions of this. Fayette County convenes "
  "boundary working groups of parents, staff, and community members over GIS scenarios whenever it opens or "
  "rebalances schools, and publishes the maps. Jefferson County publishes its assignment boundary documents "
  "and has contracted route-optimization modeling for its bus system. Every district, Bourbon County "
  "included, already files the T-1 annual transportation report and keeps the address data the analysis "
  "needs. The tools are commodity software; the working group is a policy choice. A district facing a "
  "closure vote over money owes the public this study first, and the workbook's Transport_Geo and "
  "Redistricting tabs are built to receive its outputs.")
P("The savings from doing this well are documented, not hypothetical. Boston Public Schools ran the "
  "signature version in 2017: an MIT-built routing algorithm produced bus routes 20 percent more efficient "
  "than the hand-built ones, cut 50 buses, about 8 percent of the fleet, eliminated a million bus-miles in "
  "the first year, and saved roughly $5 million that the district returned to classrooms. Bourbon County's "
  "transportation line is $2.9 million; the 5 to 10 percent captured in the menu below is $145,000 to "
  "$290,000 a year, and Boston's 20 percent shows the ceiling sits higher than the menu assumes. One more "
  "check anyone can run without waiting on the district: the federal School Attendance Boundary Survey "
  "(NCES EDGE) published the district's actual attendance-zone boundaries as free GIS files in its 2015-16 "
  "collection, and NCES publishes geocoded school locations. Figure 13 should be tested against those "
  "files, and Appendix B lists them alongside the records only the district can produce.")
tbl(["Measure", "Estimated annual value", "How it works"],
    [["Take the annual 4% property-tax adjustment",
      "$350,000-$450,000, recurring",
      "State law (KRS 160.470) lets the Board collect up to 4% more revenue from existing property each year without "
      "a recall election. Assessments grew 7.4% last year; each year the adjustment is skipped is revenue foregone "
      "permanently."],
     ["Improve delinquent-tax recovery (partial)",
      "$60,000-$120,000",
      "FY2025 collections ran $239,126 (2.4 percent) below certified yield, an ordinary delinquency level; "
      "assumes one quarter to one half is recoverable through routine county channels."],
     ["Attendance recovery",
      "$100,000+ per 1% of ADA",
      "SEEK pays per day of attendance. A chronic-absenteeism campaign is the cheapest revenue in school finance."],
     ["Staffing alignment through attrition",
      "$300,000-$425,000",
      "Attendance is down roughly 250 students from the funded peak. Not replacing four to five positions "
      "district-wide as retirements occur spreads the adjustment fairly instead of extracting it from one town."],
     ["Administrative restraint",
      "$200,000-$450,000",
      "Return central-office spending toward its FY2023 level before any classroom building closes."],
     ["Transportation optimization",
      "$145,000-$290,000",
      "Routing software, tiered bell times, right-sized fleet, and a pause on bus purchases after $1.58 million in "
      "two years."],
     ["Medicaid billing, E-rate, and universal-meals eligibility",
      "$100,000-$250,000",
      "Federal reimbursements many districts under-collect: health services for students with special needs, "
      "technology discounts, and the Community Eligibility Provision for meals in high-poverty schools."],
     ["Energy performance contracting",
      "10-25% of utility spend",
      "State regulation (702 KAR 4:160) authorizes contracts in which guaranteed energy savings pay for the "
      "upgrades. No such contract is currently in place district-wide."],
     ["Nonresident student agreements",
      "$4,600+ per student",
      "State funding follows students who transfer in. Growth, not shrinkage, is the durable fix for a "
      "small-district budget."],
     ["Shared services with Paris Independent",
      "$100,000-$300,000",
      "Two school districts operate in one small county. Shared transportation, food service, and back-office "
      "functions deserve a serious, public study."],
     ["Fill North Middletown to capacity instead of closing it",
      "$140,000 to $225,000 net, recurring",
      "Rebalance eastern attendance boundaries and recruit cross-county transfers under House Bill 563 to fill "
      "all 46 open seats; the worked example above and the workbook's Redistricting tab show the arithmetic. "
      "Multi-age reorganization and a preschool or day-care satellite are additional levers on top."]],
    [1.75 * inch, 1.35 * inch, 3.6 * inch],
    caption="Figure 14. Revenue and cost measures available without closing a school. Values are estimates derived "
            "from the district's audited figures and state data; ranges overlap and are not additive to the penny. "
            "A conservative combination totals roughly $1.1 to $2.1 million a year, against an annual reserve "
            "drawdown of $1.1 to $1.2 million.",
    bold_first_col=True)

H2("The tax question, faced squarely")
P("The rate history strengthens rather than weakens the community's hand. Bourbon County Schools levies 52.4 "
  "cents per $100 on real estate, second lowest among nine area districts and roughly 13 cents below the "
  "statewide school average of 65.1. Fayette levies 80.9, Paris Independent, in this same county, 71.5, Clark "
  "66.8, Bath 63.4, Scott 62.9, and Harrison 57.7; only Nicholas County, at 43.1, sits lower, and Montgomery is "
  "essentially tied at 52.5 (Figure 15). The trend runs the same direction: the levied rate has fallen from 61.3 "
  "cents in 2018 to 52.4 today, a decline that largely reflects Kentucky's rollback mechanics, in which a rising "
  "assessment base pushes the cent rate down to hold revenue roughly level. The one year with a documented "
  "rate-type decision, 2019, shows the board taking the full four percent revenue option, and nothing in the "
  "record shows the board leaving levy authority on the table.")
P("Where the money lands is equally clear. Of the $9.9 million the property tax produced in fiscal 2025, $7.8 "
  "million went to the General Fund and $2.1 million to the building and debt funds; set against $29.1 million "
  "of General Fund spending, the local levy covers barely a quarter of operations, with state SEEK dollars "
  "carrying most of the rest. Two corrections belong on the record here. First, the rate confusion in the audits "
  "resolves cleanly: 52.4 cents is the levied real estate rate, the 54.2 in one audit note is a digit "
  "transposition of it, and 54.7 is the separate motor vehicle rate. Second, the collection shortfalls visible "
  "in the audits, $387,840 in fiscal 2024 and $239,126 in fiscal 2025, are ordinary "
  "delinquencies of roughly two to four percent of certified yield, the kind every Kentucky district carries, "
  "not revenue the board declined to levy. The menu above counts only a partial recovery of them for exactly "
  "that reason: honest numbers cut both ways, and I built this report to take the cut.")
P("What remains is the option the board controls every August. Under KRS 160.470 the board may set a rate "
  "producing four percent more revenue from existing property than the compensating rate, with no recall "
  "exposure attached. Taken on the current base, that is roughly $386,000 of new recurring revenue in year one, "
  "about $787,000 a year by year two, and about $1.2 million a year by year three, nearly half the structural "
  "deficit, from a district that would still tax below Harrison, Scott, Bath, Clark, Paris Independent, and "
  "Fayette. Section 12 carries the recommendation and the companion workbook carries the math. To be clear, the "
  "levy is one option, not the only one: the menu above lists other revenue and cost measures, and deeper "
  "spending reductions are always available to a board willing to make them. But the math is simple and it "
  "does not bend. Either spending comes down or revenue goes up, and a district drawing down a million "
  "dollars of reserves a year does not get to choose neither. The board and superintendent owe the public a "
  "chosen path, in writing, with the work shown. What they do not owe anyone is the closure of the district's "
  "best performing school dressed up as the only choice.")
fig("chart_tax.png",
    "Figure 15. Left: the Bourbon County Schools real estate rate by tax year, from Kentucky Department of "
    "Revenue rate books; years before 2018 could not be retrieved and are not interpolated. Right: current "
    "levied real estate rates across nine area districts against the statewide school average of 65.1 cents. "
    "Fayette and Clark are from local reporting of their board votes; all other rates are Department of Revenue "
    "rate book lines. Bath's bar is its 2025 rate (2024 was 60.7); Nicholas is shown at its real estate rate "
    "of 43.1 (its tangible rate is 43.7).")

# ================= 10. WHAT CAN'T BE QUANTIFIED =================
H("10. What Can't Be Quantified: A Town and Its Heartbeat")
moontext = ("<i>\u201cThe school is the heartbeat of our small, but vital community... Small, rural communities are "
            "often overlooked... they're ignored in favor of larger institutions in bigger cities and towns.\u201d</i>"
            "<br/><font size=8.6 color='#555555'>Rev. Dr. Stephanie Moon, North Middletown pastor, July 2026</font>")
mbox = Table([[Paragraph(moontext, ParagraphStyle(
    "moon", fontName="Times-Roman", fontSize=10.6, leading=14.6, textColor=colors.HexColor("#1A1A1A")))]],
    colWidths=[W])
mbox.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F3F5F9")),
    ("LINEBEFORE", (0, 0), (0, -1), 2.2, NAVY),
    ("TOPPADDING", (0, 0), (-1, -1), 9),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ("RIGHTPADDING", (0, 0), (-1, -1), 11),
]))
A(mbox)
A(Spacer(1, 10))
P("Everything to this point can be argued in dollars. This section cannot, and it belongs in the record anyway. "
  "North Middletown is a town of about 610 people. Its school has stood on College Street since 1948, educating "
  "grandparents, parents, and children in the same classrooms; this month those children were invited to write "
  "love letters to it. When a place that small loses its school, it loses its largest engine of civic life: the "
  "gym where the town gathers, the stage for every concert, the reason young families give for staying.")
P("The research on what follows a closure is unusually consistent. Cornell sociologist Thomas Lyson, studying 297 "
  "rural New York villages, found that in the smallest of them, 500 people or fewer, the presence of a school "
  "went with home values roughly a quarter higher ($59,508 versus $47,782), better water and sewer infrastructure, "
  "and more residents working in town; he warned that money saved through consolidation \u201ccould be forfeited in "
  "lost taxes.\u201d A North Dakota State University study that followed eight communities through consolidation found "
  "that in the towns that lost their schools, businesses, retail trade, and participation in community "
  "organizations all declined. A 2022 Brown University analysis of Arkansas's forced consolidations estimated that "
  "affected communities lost 13 to 15 percent of their population and roughly $1,300 in assessed value per "
  "property, "
  "with communities of color hit hardest. And a case study of Limerick, Saskatchewan documented the quieter losses "
  "after a school closed: volunteerism, community recreation, and the everyday ties between generations all "
  "frayed, felt even by residents with no children in school.")
P("There is a fiscal irony buried in that research: a district closing a school to protect its budget risks "
  "shrinking the very tax base the budget stands on. Property values, population, and local business activity are "
  "not sentimental line items. They are the assessment roll.")
P("The people closest to this school have already said what the studies measure. An alumna planning to enroll her "
  "own children told reporters that closing it \u201cjust makes no sense when the other schools are already so "
  "packed.\u201d Mayor Jeff McFarland calls closure \u201ca disservice to the community.\u201d None of this appears in a "
  "savings worksheet. All of it should appear in the Board's deliberation, because a decision that counts only "
  "what is easy to count is not a complete accounting.")
A(Spacer(1, 6))
H2("My own personal note")
ptext = ("I grew up in this school and in this town, and I cannot overstate what they made of me. Our academic "
         "team won a regional championship in that building. I played basketball as an NMES King and kickball on "
         "that playground. I learned from teachers like Mrs. Craycraft, Mrs. Johnson, and Mrs. Mitchell, the kind "
         "of teachers a child remembers for the rest of his life. Whatever I have become, the foundation was "
         "poured there, early, by people who knew my name. And the debt runs wider than one building: Bourbon County "
         "Schools carried me from elementary through high school, and I loved every year of it."
         "<br/><br/>I also remember that this fight is not new. When I was a student, the board of that era tried "
         "to attach this same transitional label to this school. My parents and their neighbors chose to fight, "
         "and North Middletown Elementary stayed permanent. It was the lifeblood of this town then. It is the "
         "lifeblood of this town now."
         "<br/><br/>Bourbon County is no longer my home, or my family's. But the grit and perseverance it and "
         "NMES gave me still remain. Some things are worth fighting for wherever life takes you, and this school "
         "is one of them."
         "<br/><font size=8.6 color='#555555'>A former NMES King</font>")
pbox = Table([[Paragraph(ptext, ParagraphStyle(
    "pnote", fontName="Times-Roman", fontSize=10.6, leading=14.6, textColor=colors.HexColor("#1A1A1A")))]],
    colWidths=[W])
pbox.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F3F5F9")),
    ("LINEBEFORE", (0, 0), (0, -1), 2.2, NAVY),
    ("TOPPADDING", (0, 0), (-1, -1), 9),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ("RIGHTPADDING", (0, 0), (-1, -1), 11),
]))
A(pbox)

# ================= 11. TEN QUESTIONS =================
H("11. Ten Questions the Board Should Require Answered, In Writing, Before Any Vote")
P("These are not rhetorical. Each has a document behind it that the administration either already holds or "
  "should be required to produce.")
qs = [
 "What is the line-item <b>net recurring General Fund saving</b> from closure: costs that truly disappear, minus "
 "added transportation, receiving-school costs, and the carrying or disposal cost of the building? Publish the "
 "worksheet.",
 "What exactly is inside the \u201cover a million dollars\u201d figure, and how does it reconcile with the state's "
 "published per-student spending data for the school? And which enrollment count is the administration using, "
 "federal data show 128 students, while public statements have ranged lower.",
 "Grade by grade, what is the real capacity at Bourbon Central and Cane Ridge, and what staff, sections, or space "
 "must be added to absorb 128 more children, at what cost, from which fund? And publish the geocoded student "
 "counts by attendance area that any honest boundary study, including the rebalancing scenario in Section 9, "
 "needs.",
 "What are the modeled bus routes, and what is the longest one-way ride a North Middletown kindergartner would "
 "face?",
 "What does the new architect-and-engineer condition assessment say about the North Middletown building, what "
 "renovation figure does it attach, and who prepared it?",
 "Which of the claimed savings are General Fund dollars that can pay teachers, and which are restricted facility "
 "dollars that cannot?",
 "What is the stated purpose of the 2024 $6.055 million bond issue? Publish the official statement and the "
 "BG-1, and state when North Middletown Elementary last received meaningful capital investment.",
 "Why did central-office administration grow 44.8 percent in two years while attendance fell, and what rollback "
 "is on the table before a school closes? Publish administrator compensation from the official state records.",
 "What is the written plan to protect the academic outcomes of students moved from a school scoring 58.2 into "
 "schools scoring 26.5 and 19.3, and what happens to the district's Title I allocations when they move?",
 "Which alternatives in Section 9 has the administration actually modeled, with what results, and if none, why "
 "is closure first on the list rather than last?"]
for i, q in enumerate(qs, 1):
    A(Paragraph(f"<b>{i}.</b>&nbsp;&nbsp;{q}", qstyle))

# ================= 12. RECOMMENDATIONS =================
H("12. Recommendations")
asktext = ("<b>The ask, plainly stated:</b> the community requests that the Board of Education pause any vote on "
           "the facility plan, or on the future of North Middletown Elementary, until the ten questions in Section "
           "11 are answered in writing and in public. A pause is fully within the Board's power: boards control "
           "their own agendas, a resolution deferring adoption of the plan requires only a majority, and if the "
           "four-year planning deadline presses, the governing regulation (702 KAR 4:180) allows a district to "
           "request a waiver or extension from the Kentucky Department of Education, relief the Department has "
           "granted other districts. Nothing in state law forces a rushed decision.")
askbox = Table([[Paragraph(asktext, ParagraphStyle(
    "ask", fontName="Times-Roman", fontSize=10.4, leading=14.4, textColor=colors.HexColor("#1A1A1A")))]],
    colWidths=[W])
askbox.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EAF1FA")),
    ("BOX", (0, 0), (-1, -1), 0.9, NAVY),
    ("TOPPADDING", (0, 0), (-1, -1), 9),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ("LEFTPADDING", (0, 0), (-1, -1), 11),
    ("RIGHTPADDING", (0, 0), (-1, -1), 11),
]))
A(askbox)
A(Spacer(1, 10))
H2("Before the July 29 forum and any Board action")
B("Adopt a formal Board position that closure is a last resort, to be considered only after the ten questions above "
  "are answered in writing and the alternatives in Section 9 have been costed.")
B("Decline to adopt any facility plan carrying a \u201ctransitional\u201d designation for North Middletown until the "
  "net-savings worksheet, the building condition assessment, the 2024 bond documents, and the school-level "
  "climate-and-safety survey results are public.")
B("A working threshold for the Board: if documented net recurring General Fund savings fall below roughly "
  "$400,000 to $500,000 a year, a range the four percent revenue option alone nearly matches in its first "
  "year, closure "
  "fails on its own financial terms.")
B("Request from the Kentucky Department of Education and the district's own archives the pre-2021 facility "
  "plan cycles and board minutes. They would settle the school's planning history, including whether an "
  "earlier transitional designation was proposed and reversed, and recover the building's earlier rated "
  "capacities.")
B("Face the levy each August with the numbers on the table: the four percent option adds roughly $386,000 of "
  "recurring revenue in year one and about $1.2 million a year by year three if taken three years running, "
  "while Bourbon would still tax below six of its eight neighbors. Take it or reject it, but decide on the "
  "record, alongside the spending decisions, because standing idle is the one answer I rule out.")
H2("Over the next twelve months")
B("Pursue the low-harm levers first: the collections-gap reconciliation, the 4-percent levy decision at the "
  "September tax setting, Medicaid and meals reimbursements, transportation routing, attrition-based staffing, and "
  "an administrative cost review, with quarterly public reporting against a target of cutting the operating "
  "deficit from $2.6 million to under $1.5 million by fiscal 2027 and under $800,000 by fiscal 2028.")
B("Charter a North Middletown sustainability committee, district, city, parents, and business, to design the "
  "multi-age model, community uses of the building, and a transfer-in program for the 2027-28 school year.")
B("Give that plan a real test: two years, a public target of at least 145 students at the fall 2028 count, "
  "and quarterly reporting against it. If the community's plan misses its own number, the conversation "
  "changes; if it hits, the question is settled. Either way, the decision will have been earned rather than "
  "assumed.")
H2("If consolidation is ever revisited")
B("Require an independent review of the savings estimate, a receiving-school capacity study, and a student "
  "transition plan, and cost grade reconfiguration (for example, a primary center at North Middletown) as the "
  "explicit alternative to outright closure.")
P("The district holds about $4.3 million in General Fund balance and is drawing it down at $1.1 to $1.2 million a "
  "year. That is a serious problem, and roughly three budget cycles in which to fix it properly. Closing the "
  "county's best elementary school, in the town that would lose the most, on the strength of an unpublished number, "
  "would be a permanent answer to a solvable problem. The community is not asking the Board to ignore the deficit. "
  "It is asking the administration to show its work. Revenue or reductions, the Board must choose one and own it; standing still simply spends the "
  "reserves and blames a school. Pause the vote. Answer the questions. Then decide with "
  "the whole record on the table.")

# ================= NOTES =================
H("Notes on the Data")
P("I built this report from public records, and I want it held to that standard. The audited figures come from "
  "the district's financial statements for the years ended June 30, 2024 and June 30, 2025, both of which carry "
  "clean opinions. Per-student spending is the state's published school-level data for 2023-24, the most recent "
  "full year posted, and should be refreshed when the next year appears. The multi-year score series in Figure 6 "
  "is SchoolDigger's normalized 0-100 rendering of Kentucky Department of Education test data, a consistent "
  "yardstick across years but not KDE's official rating; the underlying state assessments changed in 2012 and "
  "again in 2021-22. Demographic figures come from the U.S. Census Bureau, the Kentucky State Data Center's "
  "projections as reported in county planning documents, and the county's Envision 2040 plan. Enrollment counts "
  "from 1989 through 2014 are compiled from federal data by PublicSchoolReview; the 2015 through 2025 counts "
  "match the federal figures directly. Every dollar range labeled an estimate is mine, its assumptions are "
  "stated where it appears, and every one of them is adjustable in the companion workbook. The boundary "
  "rebalancing scenario in Section 9 is arithmetic on the cited enrollment counts, not a routing study; the "
  "geocoded student counts and routing data a full study needs are held by the district and requested in "
  "Question 3. The transportation estimates beside it use census geography, a highway distance, and labeled "
  "cost-per-mile bands; the district's annual T-1 transportation report and zone map would replace every one "
  "of those inputs, and the Transport_Geo tab is built to take them.", note)
P("A few items in the record need the district, not me, to resolve. The real-estate tax rate appears as 52.4 "
  "confusion is resolved in Section 9: 52.4 cents is the levied rate, 54.2 a transposition typo, 54.7 the "
  "motor vehicle rate; still open are the General Fund versus building fund cent split, the levied rate type "
  "by year, and the pre-2018 rate history, all in state files the district can produce. The 2013R bond "
  "figures are internally inconsistent as printed. The stated purpose of the 2023 and 2024 bond issues awaits "
  "the official statements. The school-level climate and safety survey results were not publicly retrievable. "
  "And the enrollment count itself: federal data show 128, public statements have said around 100, and a 118 "
  "figure appears in no official record I could find. Reported free and reduced-price meal shares for the school "
  "range from roughly 76 to 93 percent across federal and state sources. My recollection in Section 10 of an "
  "earlier transitional episode comes from personal discussions with my father, who served as mayor of North "
  "Middletown; it is offered as memory, and the pre-2021 planning records that would confirm it are requested "
  "in Section 12. One more for the record: the fiscal 2025 audit misprints the prior year's attendance as "
  "2,278.527; the correct figure, 2,278.537, comes from the fiscal 2024 audit itself.", note)
P("I prepared this report myself, with Fable 5, an AI research assistant from Anthropic, doing the digging "
  "alongside me, and I disclose that on purpose: check my work. Every figure traces to a source below, and every "
  "school and district named is the Kentucky one. Before release I stress-tested this report against its own bias, "
  "which is why the cautions on pension allocations inside expense lines, one-time swings, single-year score "
  "noise, and the tax cost of the levy option sit beside the numbers they qualify. The Kings mascot is confirmed "
  "by the school's spirit-wear listings, and the blue and white on these pages are the school's colors as this "
  "community knows them. Last: this report criticizes decisions and asks for documents. It attributes no motive "
  "and alleges no wrongdoing to the superintendent, the finance office, the Board, or any member of the planning "
  "committee, and nothing in it should be read otherwise.", note)

# ================= SOURCES =================
H("Sources")
srcs = [
 "Bourbon County School District, Audited Financial Statements, year ended June 30, 2024 (Summers, McCrary and "
 "Sparks, PSC), posted by the Kentucky Department of Education: education.ky.gov/districts/FinRept/Documents/"
 "FY2023-2024 FA Bourbon Co.pdf",
 "Bourbon County School District, Audited Financial Statements, year ended June 30, 2025, posted by the Kentucky "
 "Department of Education: education.ky.gov/districts/FinRept/Documents/FY2024-2025 FA Bourbon Co Rev.pdf",
 "Kentucky School Report Card, school-level per-pupil expenditure data (2023-24) and assessment and accountability "
 "datasets (2021-22 through 2024-25), Kentucky Department of Education: kyschoolreportcard.com; "
 "education.ky.gov/Open-House",
 "Bourbon County Schools District Facility Plan, approved by the Kentucky Board of Education, 2021: "
 "education.ky.gov/districts/fac/documents/bourbon co dfp.pdf",
 "702 KAR 4:180, Kentucky School Facilities Planning Manual; 702 KAR 4:160, Capital Construction Process: "
 "apps.legislature.ky.gov/law/kar/titles/702/004",
 "Kentucky Revised Statutes 160.470 and 132.017 (school property-tax rates); 157.350 (nonresident students); "
 "157.420 and 157.440 (capital outlay and building funds); 157.360 (class-size caps); 157.622 (SFCC offers "
 "of assistance)",
 "Kentucky Department of Education, SEEK funding files and Local District Tax Levies: education.ky.gov/districts/SEEK "
 "and education.ky.gov (Taxes)",
 "Kentucky Department of Revenue, 2025 Property Tax Rate Book",
 "School Facilities Construction Commission, bond participation and refunding policies: sfcc.ky.gov; Capital "
 "Projects and Bond Oversight Committee agenda, May 23, 2024, Kentucky Legislative Research Commission",
 "Municipal Securities Rulemaking Board, EMMA disclosure database (Bourbon County School District Finance "
 "Corporation): emma.msrb.org",
 "National Center for Education Statistics, Common Core of Data, Bourbon County district and school files "
 "(district 2100540; school 210054000096): nces.ed.gov/ccd",
 "Kentucky Center for Economic Policy, analyses of the 2026-2028 state budget and SEEK funding: kypolicy.org; "
 "Kentucky Lantern, \u201cSchools get increase but transportation funding still flat,\u201d February 25, 2026",
 "Research for Action, Revisiting Research on School Closings: Key Learnings for District and Community Leaders "
 "(2024)",
 "Howley, C., Johnson, J., and Petrie, J., Consolidation of Schools and Districts: What the Research Says and What "
 "It Means, National Education Policy Center (2011)",
 "Kim, J., The Long Shadow of School Closures, Annenberg Institute EdWorkingPaper 24-963 (2024); analysis of "
 "Vermont Act 46 consolidation outcomes (2024)",
 "WKYT-TV, \u201cResidents and alumni defend small town school from closure in Bourbon County,\u201d July 16, 2026, and "
 "\u201cCommunity meeting planned for Bourbon Co. elementary school in danger of closing,\u201d July 17, 2026",
 "FOX 56 News, coverage of the Bourbon County facility-planning meetings, July 2026; The Bourbon County Citizen, "
 "July 9 and July 16, 2026",
 "Bourbon County Schools, Comprehensive District Improvement Plan executive summary, 2024-25 (career-technical "
 "center and community-college partnership plans); district salary schedules as adopted by the Board of Education",
 "Kentucky Teacher (Kentucky Department of Education), \u201cBlue Ribbon school shares keys to success,\u201d November "
 "2011, North Middletown Elementary's 2011 National Blue Ribbon designation: kentuckyteacher.org",
 "Kentucky Department of Education, Non-Resident Student Policy guidance under House Bill 563 (2021) and KRS "
 "157.350: education.ky.gov/districts/enrol",
 "KRS 157.370 and 702 KAR 3:270 (SEEK transportation add-on, calculated on transported pupils per square "
 "mile); Kentucky Association of School Superintendents on the funding history: kysupts.org; 2024-2026 "
 "Kentucky budget (HB 6) restoring pupil transportation to 90 and then 100 percent of formula, as reported "
 "by LINK nky and Kentucky Public Radio, 2024",
 "Fayette County Public Schools, school rezoning working groups and boundary maps: fcps.net/zones; "
 "Jefferson County Public Schools, assignment boundary documents: jefferson.kyschools.us",
 "Boston Public Schools bus-route optimization (Bertsimas, Delarue, and Martin, MIT Operations Research "
 "Center, 2017): 20 percent route efficiency, 50 buses cut, about $5 million saved in year one; MIT Sloan, "
 "Route Fifty, The 74, and U.S. DOT ITS case documentation",
 "National Center for Education Statistics, School Attendance Boundary Survey 2015-16 (district "
 "attendance-zone GIS files) and EDGE geocoded school locations: nces.ed.gov/programs/edge",
 "U.S. Census Bureau, 2020 decennial counts and land area: Bourbon County (289.7 land square miles), Paris "
 "(10,171), Millersburg (747), North Middletown (610); U.S. Route 460 mileage, North Middletown to Paris",
 "Chicago Sun-Times and WBEZ, analysis of the 2013 Chicago school closings, June 2023; University of Chicago "
 "Consortium on School Research, School Closings in Chicago (2018)",
 "The Pew Charitable Trusts, Shuttered Public Schools: The Struggle to Bring Old Buildings New Life (2013)",
 "Charleston Gazette, \u201cClosing Costs\u201d series on West Virginia school consolidation (2002); West Virginia Public "
 "Broadcasting, \u201cSchool Consolidation Failed to Live Up to Its Promises\u201d (2015)",
 "Miller, G., Evaluating the Impact of School District Mergers in Vermont, Yale University (2024; "
 "undergraduate economics thesis)",
 "Pearman, F., The Fiscal Consequences of School Closures in California, Stanford University / Getting Down to "
 "Facts (2026), as summarized in Education Next and Education Week",
 "Prep Sportswear, North Middletown Elementary School Kings spirit-wear listing (school mascot): "
 "prepsportswear.com",
 "Lyson, T., \u201cWhat Does a School Mean to a Community?\u201d Journal of Research in Rural Education 17(3), 2002",
 "Sell, R., Leistritz, F., and Thompson, J., Socio-Economic Impacts of School Consolidation on Host and Vacated "
 "Communities, North Dakota State University, Agricultural Economics Report No. 347 (1996)",
 "Oncescu, J., and Giles, A., on the community impacts of a rural school closure (Limerick, Saskatchewan), "
 "Leisure/Loisir 36(2), 2012",
 "Smith and Zimmer, The Impacts of School District Consolidation on Rural Communities, Annenberg Institute at "
 "Brown University, EdWorkingPaper 22-530 (2022)",
 "Campbellsville University, Excellence in Teaching Award announcements (2014 and 2017 Bourbon County honorees); "
 "Bourbon County Schools staff directory (current NMES principal)",
 "NCES school-level enrollment history for North Middletown Elementary, 1988-89 through 2024-25 (as compiled by "
 "PublicSchoolReview); NCES CCD school detail, 2024-25 official count",
 "U.S. Census Bureau, decennial counts and population estimates for Bourbon County, Kentucky (via FRED series "
 "KYBOUR7POP)",
 "Kentucky State Data Center (University of Louisville), Kentucky Population and Household Projections "
 "2025-2050 (June 2026), as summarized by the Kentucky Association of Counties",
 "Bourbon County, Kentucky, Envision 2040 Comprehensive Plan (population projection and land-use analysis)",
 "Kentucky Department of Revenue, Kentucky Property Tax Rates books, 2024 and 2025 editions (school district "
 "lines, including Bourbon County 009007 and area districts); 2018-2022 rates from prior-year editions",
 "KRS 160.470 (school district tax rate limits, hearing, and the four percent revenue option); KRS 160.473",
 "Winchester Sun, Clark County Board of Education tax rate adoption (September 2024); Lexington "
 "Herald-Leader coverage of the Fayette County Public Schools 2024-25 rate",
 "Kentucky Department of Education, Local District Tax Levies files, SEEK Taxes page (rate type by year; "
 "cited as an open records item)",
]
for i, s in enumerate(srcs, 1):
    A(Paragraph(f"{i}. {s}", ParagraphStyle("src", parent=note, fontSize=8.4, leading=11.0, spaceAfter=3.2)))

# ================= GLOSSARY =================
A(PageBreak())
H("Appendix A: Plain-Language Glossary")
gl = [
 ["ADA (Average Daily Attendance)", "The average number of students actually present each day; the main driver of state funding."],
 ["BG-1", "The state form that authorizes a school construction project's scope and budget."],
 ["Bond / debt service", "Borrowing for buildings, and the annual principal-and-interest payments that repay it."],
 ["Bonding potential / capacity", "The new building debt a district's restricted revenues can support, as computed by KDE; built from the capital outlay and nickel streams, minus existing debt service. See Section 6."],
 ["Capital outlay", "A state allotment restricted to buildings and equipment; it cannot pay salaries."],
 ["Compensating rate", "The property-tax rate that produces the same revenue as the year before."],
 ["Contingency", "The required budget cushion; Kentucky law sets a two-percent minimum."],
 ["DFP (District Facility Plan)", "The state-approved four-year plan listing every building's status and capital priorities."],
 ["ESSER", "Federal pandemic relief for schools (Elementary and Secondary School Emergency Relief), now expired."],
 ["Finance Corporation", "The legal entity, with the same members as the Board, that issues a district's bonds."],
 ["4% rate (KRS 160.470)", "The state law allowing a board to collect up to four percent more property-tax revenue each year without a recall election."],
 ["FRPL", "Free and reduced-price lunch eligibility; a standard measure of student poverty."],
 ["FSPK / the \u201cnickel\u201d", "A restricted building tax (five cents per $100 of property value) that funds facilities and bond payments."],
 ["Fund balance / unassigned", "The district's accumulated reserves; the unassigned portion is not committed to any purpose."],
 ["General Fund", "The district's main operating account, salaries, utilities, and daily costs."],
 ["Hold-harmless", "A temporary rule that let districts keep pandemic-era funding based on older, higher attendance."],
 ["KDE / KBE", "The Kentucky Department of Education and the Kentucky Board of Education, which must approve facility plans."],
 ["KSA", "The Kentucky Summative Assessment, the state tests behind school accountability scores."],
 ["LPC (Local Planning Committee)", "The citizen-and-staff committee that drafts the facility plan; it recommends, but cannot close a school."],
 ["Official statement", "A bond's public prospectus describing its purpose, projects, and repayment terms."],
 ["On-behalf payments", "Pension and benefit costs the state pays directly for district employees, shown in the audit as both revenue and expense."],
 ["SEEK", "Support Education Excellence in Kentucky, the state's per-student funding formula ($4,586 base in fiscal 2026)."],
 ["SFCC", "The School Facilities Construction Commission, a state body that pays part of qualifying school-construction debt."],
 ["Tier I", "An optional layer of local tax effort that the state partially matches."],
 ["Title I", "Federal funding for schools serving many low-income students."],
 ["\u201cTransitional\u201d center", "A facility-plan label meaning a school is slated for possible consolidation; a classification, not a closure."],
 ["702 KAR 4:180", "The state regulation governing facility planning and the school-closure process."],
]
rows = [[Paragraph(f"<b>{a}</b>", tcell), Paragraph(b, tcell)] for a, b in gl]
gt = Table(rows, colWidths=[1.95 * inch, 4.75 * inch], hAlign="LEFT")
gt.setStyle(TableStyle([
    ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, ROWBG]),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 2.5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ("LINEBELOW", (0, -1), (-1, -1), 0.6, LINE),
    ("LINEABOVE", (0, 0), (-1, 0), 0.6, LINE),
]))
A(gt)

# ================= APPENDIX B: OPEN RECORDS =================
A(PageBreak())
H("Appendix B: The Open Records Checklist")
P("Kentucky's Open Records Act (KRS 61.870 to 61.884) entitles any resident to these documents on request "
  "to the district's records custodian, with a response due within five business days. Each request names "
  "the labeled estimate in this report or the companion workbook that it would replace. Nothing here seeks "
  "student-identifiable information, and I will publish, and correct against, whatever comes back.")
tbl(["Request", "What it settles"],
    [["<b>The money.</b> The net-savings worksheet behind the \u201cover a million dollars\u201d statement",
      "Replaces the $250,000 to $600,000 planning range (Sections 1, 4)"],
     ["Any alternatives modeling the administration has performed",
      "Whether closure was compared to anything (Section 9)"],
     ["Administrator salary schedule and five years of compensation, position by position",
      "How much of the 44.8 percent central-office growth is people versus accounting (Section 8)"],
     ["KDE levy files: rate type elected each year; General Fund versus building fund cent split",
      "The two open cells in the tax history (Section 9)"],
     ["<b>The buildings and bonds.</b> The 2024 bond's official statement and BG-1; the 2023 issue's purpose",
      "Where $6.9 million of recent borrowing went (Section 6)"],
     ["KDE's bonding potential statement for the district",
      "Real borrowing headroom beside the audit's $23.5 million (Section 6)"],
     ["The architect-and-engineer condition assessment for North Middletown, with author and assumptions",
      "The building case, if one exists (Section 7)"],
     ["The room-by-room worksheet behind the 174 capacity rating; the pre-2021 facility plans",
      "Whether capacity is a wall or a room schedule (Section 7)"],
     ["<b>The boundaries and buses.</b> The district's GIS attendance-zone map",
      "Replaces the traced zones in Figure 13"],
     ["Geocoded student counts by attendance area or planning zone",
      "Validates the density analysis; enables real boundary optimization (Section 9)"],
     ["The T-1 annual transportation report, route sheets, and cost per bus-mile",
      "Replaces every yellow busing input in the Transport_Geo tab"],
     ["Modeled post-closure routes and the longest one-way ride for the youngest riders",
      "Question 4's answer in minutes rather than adjectives"],
     ["<b>The students.</b> The written academic transition plan and Title I reallocation analysis",
      "What happens to the children academically (Section 5)"],
     ["Grade-by-grade capacity, sections, and space at Bourbon Central and Cane Ridge",
      "Absorption costs, and the rebalancing scenario's relief estimate (Sections 4, 9)"],
     ["School-level climate and safety survey results for all three elementaries",
      "The state's own measure of the school communities involved (Section 5)"]],
    [3.5 * inch, 3.2 * inch],
    caption="Fifteen requests in four groups. Each cites the section whose labeled estimate it replaces.",
    bold_first_col=False)
H2("Already public, no request needed")
B("School Attendance Boundary Survey (NCES EDGE, 2015-16): the district's attendance-zone GIS files, "
  "queryable at nces.ed.gov/opengis (SABS_1516 service, school 210054000096); geocoded school locations and "
  "enrollment files at nces.ed.gov/programs/edge.")
B("U.S. Census TIGER county boundaries and block-level population counts (census.gov/geographies); KDE SEEK "
  "transportation calculation files and district funding detail (education.ky.gov/districts/SEEK).")

# ---------------- build ----------------
def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.6)
    canvas.line(0.9 * inch, 0.66 * inch, 7.6 * inch, 0.66 * inch)
    canvas.setFont("Helvetica", 7.6)
    canvas.setFillColor(GRAY)
    canvas.drawString(0.9 * inch, 0.5 * inch,
                      "Saving North Middletown Elementary School  \u2022  A Deep Dive into Bourbon County Schools  \u2022  July 2026")
    canvas.drawRightString(7.6 * inch, 0.5 * inch, f"Page {doc.page - 1}")
    canvas.restoreState()

def cover(canvas, doc):
    pass

doc = SimpleDocTemplate("/home/claude/nmes/Saving_North_Middletown_Elementary.pdf",
                        pagesize=letter,
                        leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                        topMargin=0.85 * inch, bottomMargin=0.95 * inch,
                        title="Saving North Middletown Elementary School, a Deep Dive into Bourbon County Schools",
                        author="North Middletown Community Analysis")
doc.build(story, onFirstPage=cover, onLaterPages=footer)
print("pdf built")
