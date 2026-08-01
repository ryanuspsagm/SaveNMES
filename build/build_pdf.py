from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                CondPageBreak, Image, Table, TableStyle, HRFlowable,
                                KeepTogether)
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

def H(t, need=0):
    if need:
        A(CondPageBreak(need * inch))
    A(Paragraph(t, h1))
    A(HRK(width="100%", thickness=0.8, color=LINE, spaceAfter=8))

def H2(t, need=0):
    if need:
        A(CondPageBreak(need * inch))
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
A(Paragraph("A Close Look at Bourbon County Schools", ParagraphStyle(
    "sub", fontName="Times-Italic", fontSize=15.5, leading=19, textColor=colors.HexColor("#333333"),
    alignment=TA_CENTER, spaceAfter=22)))
A(HRFlowable(width=2.2 * inch, thickness=1.1, color=GOLD, hAlign="CENTER", spaceAfter=22))
A(Paragraph("Prepared for the North Middletown community and the members of the<br/>Bourbon County Board of Education",
            ParagraphStyle("pf", fontName="Times-Roman", fontSize=11.5, leading=15,
                           alignment=TA_CENTER, textColor=colors.HexColor("#1A1A1A"), spaceAfter=8)))
A(Paragraph("Paris and North Middletown, Kentucky &nbsp;\u2022&nbsp; July 2026",
            ParagraphStyle("pf2", fontName="Helvetica", fontSize=9.5, alignment=TA_CENTER,
                           textColor=GRAY, spaceAfter=6)))
A(Paragraph("Written by a former NMES King; the analysis and report writing were accelerated with the use of an AI research assistant",
            ParagraphStyle("pf3", fontName="Helvetica-Oblique", fontSize=9, alignment=TA_CENTER,
                           textColor=GRAY, spaceAfter=5)))
A(Paragraph("Version 4.2 &nbsp;\u2022&nbsp; August 1, 2026",
            ParagraphStyle("pf4", fontName="Helvetica", fontSize=9, alignment=TA_CENTER,
                           textColor=GRAY, spaceAfter=0)))
A(Spacer(1, 1.6 * inch))
scope = ("This review relies only on public records: the district's audited financial statements for the "
         "fiscal years ending June 30, 2024 and June 30, 2025; Kentucky Department of Education funding, facility, "
         "and school report card data; federal enrollment records; municipal bond disclosures; state regulations; and "
         "contemporaneous local reporting. Where a figure is an estimate rather than a published number, it is labeled "
         "as an estimate and its assumptions are stated. This document is not an audit, and it alleges no misconduct "
         "by any person; both years of the district's financial statements received clean opinions from its independent "
         "auditors. Its purpose is narrower and simpler: to lay out what the public record shows, and what it does not "
         "yet show, before an irreversible decision is made about a community's school. I am an alumnus of this school. "
         "The analysis and report writing were accelerated with the use of Claude, an AI research assistant from Anthropic; every figure "
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
  "$4.29 million in two years. The causes are clear: about $2.95 million in one-time federal pandemic aid "
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
  "pay teachers in any case. The receiving schools' approved ratings are 521 at Bourbon Central and 422 at Cane "
  "Ridge; at today's enrollment that is a net 31 uncommitted seats for 128 children, with Cane Ridge already 31 "
  "students over its rating. Section 4 prices every defensible combination of the closure's costs and savings, "
  "with every staffing input now taken from the district's own written response at its own fully loaded prices: "
  "the net effect runs from losing $591,545 a year to saving $488,631, the median outcome LOSES $21,971 a year, "
  "and 55 percent of scenarios lose money outright. Every alternative in this report saves more than that.")
P("<b>Third, the district has not yet shown its work.</b> No line-item net-savings analysis, transportation model, "
  "receiving-school capacity study, or alternatives comparison has been published. The one technical document that "
  "has surfaced, the architect's KFICS condition assessment presented in July, strengthens the keep-open case: it "
  "prices North Middletown's needs at $8.5 million, second lowest of the district's schools, against $23.2 million "
  "at the two receiving schools combined and $98.4 million districtwide (Section 7). "
  "Meanwhile the school proposed for closure is, on the state's official 2024-25 assessments, the county's "
  "highest-performing elementary: first among all four elementary schools in Bourbon County in every tested "
  "subject, reading, mathematics, science, social studies, and writing, and above the statewide elementary "
  "average in science and writing. The state's historical files complete the arc: county math leader in "
  "every pre-COVID year on record and an official Distinguished rating in 2016 (Section 5).")
P("The report closes with twelve questions the administration should have to answer in writing before any vote, "
  "a list of revenue and cost measures worth an estimated $1.0 to $1.9 million a year without closing a school, and "
  "recommendations that come in stages, each with a clear number for when the Board should act. The district retains roughly $4.3 million in General Fund "
  "balance and is drawing it down at $1.1 to $1.2 million a year. There is a real problem here, and there is also "
  "time to solve it well. I am asking for one thing, and it is specific: pause any vote until the twelve questions in this report are "
  "answered in writing.")

# ================= 2. WHERE THINGS STAND =================
H("The Decision in Brief: Two Roads", need=3.0)
P("This report now leads with its conclusions, in the same order the full evidence appears. Part One here: the "
  "case for growth, then the case against closure, then the choice. Every figure is sourced in the numbered "
  "sections that follow and live in the companion workbook; nothing in these pages stands on its own "
  "authority.")

H2("The case for growth: a district-wide problem with district-wide levers")
P("<b>The problem is not one school.</b> Elementary enrollment is down 16.5 percent from its 2016 peak while "
  "the census shows the county's child population essentially flat for twenty-five years; kindergarten intake "
  "hit 149 last fall, the lowest in the federal record, and fewer children have entered kindergarten than left "
  "fifth grade in seven of the last eight years. The General Fund draws down roughly $1.1 million of reserves "
  "a year, and the enrollment loss alone accounts for most of it: the 205 missing elementary students carry "
  "about $948,000 a year of state funding. And the revenue posture is unique in the region: the Department of "
  "Revenue's certified values show Bourbon County's tax base grew <b>107.5 percent from 2012 to 2025, second "
  "fastest of the eight area counties</b>, while the school levy fell 5.4 percent, the only decline among "
  "nine districts. Scott County rode the same boom, raised its rate 38.9 percent on top, and levies a 0.5 "
  "percent occupational tax besides; eight Kentucky districts levy that tax, Bourbon levies none, though its "
  "utility tax is already at the 3 percent maximum. Merely holding the 2012 rate would yield about $613,000 "
  "more per year today.")
P("<b>The levers.</b> First, enrollment: each returning student brings the $4,626 SEEK base against roughly "
  "$400 of marginal cost, the recoverable pool is measured (259 registered homeschoolers, roughly 450 to 550 "
  "county children outside the public schools, 131 nonresident students already choosing this district), and "
  "the model is proven in-state: Eminence Independent grew from 733 to 1,006 students (up 37 percent) over "
  "the decade Bourbon shrank 13 percent, on differentiation and open enrollment. A themed academy at North "
  "Middletown (arts, technology, or agriculture and outdoor sciences), a preschool-to-kindergarten pipeline, foundation-funded scholarship promises (private dollars, "
  "lawfully), and modest marketing against a measured pool are the growth plan, and filling North Middletown's "
  "46 open seats alone nets $56,000 to $116,000 a year, with today's 174 rating not the ceiling: the state's "
  "2013-approved plan rated this building at 198. Second, fixed costs: transportation is $2.7 million "
  "coded to no school with no routing study ever produced (a ten percent optimization is about $270,000 a "
  "year); Kentucky's school energy program documented $225 million of statewide savings; and an inspection "
  "of every non-teaching position district-wide, trimmed by attrition rather than layoffs, is worth $340,000 "
  "to $425,000 a year at the district's own loaded costs. Third, revenue: the rate is simply "
  "lower, 52.4 cents against every neighbor but one, while the tax base more than doubled; restoring the "
  "board's own 2018 rate yields about $1.7 million a year, priced in Section 9. The recall record next door "
  "is thin: across the eight neighboring districts in the last ten years, voters have turned down exactly one "
  "school tax, Bath County's building nickel, in November 2024 and again in January 2025, and no neighbor has "
  "lost an operating rate to a recall in that decade. Statewide, Marion County voters upheld their board's "
  "nickel 54 to 46 in 2015, and Bourbon's own voters declined even to petition either of this district's two "
  "recallable nickels.")

H2("The case against closure: five answers from the district's own documents")
P("<b>Performance.</b> North Middletown leads the county in every state-tested subject. <b>Cost.</b> The "
  "district's own Cost of Delivery of Services table, dated May 21, 2026 and prepared for its planning "
  "committee, prices the school at $19,080 per student against a state average of $19,020 on the same table, "
  "three tenths of one percent apart, and within 110 percent of its cheapest same-grade peer against the 150 "
  "percent standard in the state facilities manual. <b>What closure frees.</b> The district's own response "
  "prices it: $107,039 of building-bound expense lines plus about $20,000 of insurance, with all staff "
  "retained in year one by its own statement; across 5,832 priced scenarios built on those figures the median "
  "outcome LOSES $21,971 a year and 55 percent of scenarios lose money. <b>What closure risks.</b> Read the "
  "risk as steps: every 10 percent of the school's students whose families leave the district rather than "
  "change schools takes about $67,000 a year in state funding at the base plus typical add-ons, and each "
  "further 10 percent stacks another $67,000 on top, about $133,000 a year at 20 percent and $195,000 at 30, "
  "against roughly $650,000, $1.3 million and $1.9 million respectively through grade 12. The children in the building carry $5.6 million of remaining state funding "
  "through grade 12, and the exits are wide open: HB 563 makes a transfer to any neighboring district free "
  "to the family and funded for the district that wins the child, registered homeschooling in this county "
  "has climbed from 170 to 259 in five years, and the statewide virtual academy grew from 937 to 2,412 "
  "students in its first two years. <b>The receiving schools.</b> The "
  "district's own May 2026 table shows them at 97 and 98 percent of capacity, with the middle school the only "
  "building with room and the high school at 112 percent.")

H2("The choice, and four asks that cost nothing")
P("Shrink to fit, or grow and thrive. On North Middletown specifically, the asks are modest. <b>One:</b> "
  "keep the school Permanent in the facility plan with its capital needs at lower priority; a plan commits no "
  "money, Priority 2 exists for exactly this, and the Transitional label saves nothing while foreclosing "
  "state facilities eligibility, major renovation, and replacement. <b>Two:</b> give the school and community "
  "the four years to the next facility plan for a measured enrollment push, against public targets set with "
  "the board, and judge it on results. <b>Three:</b> let the school and community raise grant-based and "
  "private funds, with donated services, for the building's critical needs, at no cost to the district. "
  "<b>Four:</b> state publicly that the district will work to grow this school, because uncertainty is its "
  "own enrollment killer and a sentence of commitment gives existing and future families the confidence to "
  "enroll. The honesty behind these asks is already in the district's books: if staff are reassigned rather "
  "than cut, a closure frees the $58,774 utilities line, and the restricted renovation money is capped by "
  "enrollment regardless, a ceiling that rises with every recruited student. A closed school cannot be "
  "recalled by the children it displaces; a growth plan can be measured, every year, by everyone.")
A(PageBreak())
H("Part Two: The Evidence")
P("The sections that follow are the complete analysis: every source, every method, every correction, "
  "in the order the questions arise. The companion workbook reproduces every calculation as live formulas.")

H("2. Where Things Stand: The Decision and the Process", need=1.6)
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
      "Community meeting set for 6:30 p.m. at the North Middletown Community Center, next to the fire "
      "department on Church Street; students and alumni invited to write letters of support."],
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
            "presentation of state pension payments made on the district's behalf and is shown for context. The "
            "fiscal 2024 change line differs from the balance movement by $840, a residual carried in the audit "
            "and noted in the companion workbook.",
    bold_first_col=True)
fig("chart_gf.png",
    "Figure 3. The operating gap and the drawdown. The district spends roughly $2.5 to $2.6 million more from its "
    "General Fund than it takes in before transfers, and reserves have fallen about $2.3 million in two years. "
    "Source: audited financial statements, FY2024 and FY2025.")
P("A note on the transfers line: “net transfers and other sources” of roughly $1.4 million a year are moves "
  "between the district's own funds, indirect cost recoveries from grants and self-supporting operations and "
  "similar interfund items detailed in the audits' fund statements, not new money from outside. They cushion the "
  "General Fund's reported change in fund balance, which is why the honest measure of the structural problem is "
  "the operating result before transfers: the district spends about $2.6 million more than it takes in, and "
  "interfund transfers, some of them recurring and legitimate resources, some of them not sustainable, cover "
  "roughly half the gap while reserves absorb the rest. Which transfers can be sustained is itself a question the "
  "district's finance office should answer in writing.")
H2("Why it happened", need=4.0)
fig("chart_cliff.png",
    "Figure 4. The two revenue shocks. Federal revenue in the governmental funds fell $2.95 million from FY2023 to "
    "FY2025 as ESSER pandemic aid expired, and attendance-based state funding fell with roughly 248 fewer funded "
    "students. Sources: audited financial statements; SEEK attendance figures reported in the audits.")
P("Three forces converged. One-time federal pandemic relief, the ESSER programs, wound down, taking about "
  "$2.95 million a year with it while the staff and programs it paid for remained. Average Daily Attendance, the "
  "basis of Kentucky's SEEK funding formula, fell from a pandemic hold-harmless figure of 2,490 to 2,243, a "
  "recurring revenue loss on the order of $1.1 million a year at the fiscal 2026 base guarantee of $4,586 per student. "
  "And the state's new two-year budget offers little relief: the SEEK base rises less than one percent in fiscal "
  "2027, and state school-bus funding is frozen roughly $90 million a year below what Kentucky statute calls for, "
  "statewide.")
P("At the same time, several costs the district controls grew quickly: a two-percent raise in fiscal 2024 with "
  "\u201csome employees receiving much more,\u201d in the words of the district's own audit narrative, step increases in "
  "fiscal 2025, transportation up 20.3 percent in a single year, and central-office administration up 44.8 percent "
  "in two years (Section 8). A $6.055 million bond issued in 2024 helped push the district's debt-service payments "
  "up by about $430,000 this year (Section 6).")
P("Two more facts fill in the rest of the picture, and both cut in the community's favor. The district has already shown it can fix "
  "a money-losing operation without closing anything: between fiscal 2024 and 2025 it cut the day-care fund's loss "
  "from $722,828 to $79,010 and swung food service from a $610,606 loss to a $179,197 surplus, a combined "
  "improvement of about $1.4 million in one year. Even if part of that swing reflects one-time pricing and "
  "reimbursement changes, it shows that focused management can move seven figures without touching a school. "
  "And the district is not in collapse: both audits carry clean "
  "opinions, the fiscal 2026 budget holds a $1,489,853 contingency, well above the state's two-percent minimum, and at "
  "the current pace of drawdown the unassigned reserve lasts roughly three more budget cycles. The problem is real. "
  "So is the time to fix it right.")

# ================= 4. MILLION DOLLAR QUESTION =================
H("4. The Million-Dollar Question: What Closing the School Would Actually Save")
P("The case for closure rests on a single public statement: that keeping North Middletown Elementary open \u201ccost "
  "over a million dollars last school year.\u201d No supporting worksheet has been released. The state's own school "
  "spending data put that number in context.")
fig("chart_pp.png",
    "Figure 5. Per-student spending at the district's three elementary schools, 2023-24, as published in the "
    "Kentucky School Report Card's school-level expenditure data (total of state, local, and federal dollars).")
P("North Middletown's $19,348 per student is the highest of the three elementaries, and that is exactly what "
  "the math predicts for a small school, because one principal, one office, one kitchen, and one heated building "
  "divide across 128 children instead of 450. Multiplied out, the federal report puts about $2.5 "
  "million against this school, of which roughly $1.8 million is state and local money. That is an allocated "
  "figure rather than a site ledger. On the same 2023-24 basis the report showed $2,611,980 for North "
  "Middletown, while the district's own working budget coded $1,593,309 to the school that year, about $1.0 "
  "million less, and the difference is central office, district transportation and district instructional "
  "support that the report spreads across buildings and that no closure removes. But almost none of that total "
  "is what a closure would save, for a simple reason: <b>closing a school does not delete its students.</b>")
fig("chart_capacity_scenarios.png",
    "Figure 6. Every school filled to its rated capacity, priced with step variable costs ($400 of supplies per "
    "student added or removed, plus or minus an $85,000 loaded section wherever KRS 157.360 class caps require "
    "one), on the district's 2023-24 state filings. Seven capacity sets, all from the district's own documents "
    "or federal data: the three state-approved plans (2013, 2017, 2021), each school's twenty-year peak "
    "enrollment, the district's own architect's 2026 KFICS capacities, and the unapproved 2026 draft table. "
    "North Middletown comes out cheapest under the 2013 plan, the 2021 plan in force, the twenty-year peaks, "
    "and the architect's own numbers; Bourbon Central comes out cheapest under today's actuals, the 2017 plan, "
    "and the draft table. The 2017 plan, recovered from the Internet Archive and corroborated by the June 7, "
    "2017 state board minutes, rated North Middletown at 152 seats with 154 enrolled: the school now described "
    "as half empty was listed OVER capacity nine years ago.")
P("Five years of the district's own filings say the same thing in time series: North Middletown's total site "
  "spending grew the <b>least</b> of the three elementaries, up about 16 percent since 2019-20, against 35 to 37 "
  "percent at Bourbon Central and 46 to 47 percent at Cane Ridge. Each figure is the state's published per- "
  "student cost multiplied by that school's reported enrollment, and the bands carry the two base-year counts the "
  "record offers, the enrollment printed in the district's own 2021 facility plan and the federal fall count for "
  "2019; North Middletown finishes lowest under either. The same filings priced per student say it more directly "
  "still: since 2019-20 Bourbon Central is up 49 percent ($12,159 to $18,131), Cane Ridge up 53 percent ($12,168 "
  "to $18,670) and North Middletown up 50 percent ($12,903 to $19,348). Weighted across the three, elementary "
  "cost per student went from $12,266 to $18,512, up 51 percent. Every elementary in the county costs about half "
  "again per student what it did five years ago, the three within four points of each other, and North Middletown "
  "sits in the middle. That is a district-wide cost trend, not one building's. What grew at North Middletown is "
  "the empty space around each student as enrollment slid from 166 to 128. Divide a nearly flat cost by a "
  "shrinking class and the per-student figure climbs; that is division, not an expensive school. Fill the seats "
  "and the same division runs in reverse: at 174 students the school's per-student cost drops to between $14,339 "
  "and $15,316 depending on staffing, about $14,827 at the one-added-section default this version prices, $3,300 "
  "to $3,800 under either receiving school, and the students who fill it come from the exact schools that are "
  "over or near their rated capacity today.")
P("The capacity ratings themselves deserve the scrutiny they have never gotten, because the same three "
  "unchanged buildings have been rated wildly differently by four consecutive plans: North Middletown 198, then "
  "152, then 174, then the draft's 154; Bourbon Central 564, 611, 521, 640; Cane Ridge 500, 550, 422, 547. No "
  "major construction happened at any of the three after 2009. Ratings that swing by up to 128 seats between "
  "cycles are policy choices, not walls, and whichever school the chosen table shortchanges will look expensive "
  "at capacity. The two 2026 documents disagree with each other by 141 and 150 seats on the receiving schools "
  "in the same planning cycle. The cost conclusion is validated against actuals two ways. At bare supplies "
  "($400), the filled school runs $14,339 at the approved 174 rating and $16,149 at the draft's 154; with "
  "class-cap staffing added, $15,316 and $16,701. All four land below both receiving schools ($18,131 and "
  "$18,670). The bound that matters is where the result would turn: North Middletown stops being cheaper than "
  "Bourbon Central only if each added student costs more than $14,745 at 174, or more than $12,140 at 154. "
  "Priced the way this report prices everything else, an added student costs between about $2,250 and $4,100. "
  "This version withdraws the earlier third validation, a two-school cost slope: its sign depended on a "
  "membership pair the district has not published, and on the two other pairs available it comes out negative. In the pandemic-aid "
  "years the filled school would have run within 1 to 3 percent of the others, a tie; in the district's "
  "current cost structure the result is not close.")
P("One symmetry this report applies to itself: per-student numbers move wherever the students move. Send students "
  "out of Bourbon Central and Cane Ridge and their per-student costs rise for the same denominator reason, to "
  "roughly $18,700 and $19,300 in the workbook's scenario, because a departing student takes only variable costs "
  "while the fixed costs stay. A pure shuffle leaves total district spending nearly unchanged in either "
  "direction. Cost per student is a utilization measure, not a verdict on a building; on the post-move comparison "
  "a filled North Middletown is still the cheapest of the three, by a wider margin than before. The cash case for "
  "filling the school is booked separately and conservatively in the workbook: one to two consolidated sections "
  "at the sending schools, new SEEK revenue from out-of-county transfers under HB 563, and capacity relief at "
  "Cane Ridge. And the same symmetry runs the other way: closing North Middletown would improve the receiving "
  "schools' per-student optics while saving almost nothing in total, which is this report's Section 4 finding "
  "restated in one sentence.")
P("The 128 children would still need teachers, about eight to nine classrooms' worth at the district's average "
  "ratios, and Bourbon Central (459 students) and Cane Ridge (453 students) would each absorb roughly 64 more "
  "children across six grade levels, adding sections in several of them. The children's SEEK funding transfers with "
  "them. Food service, now a self-supporting operation, follows the meal counts. What is genuinely avoidable is the "
  "fixed cost of running the building: the principal and office staff, custodial time, utilities, and insurance, and only if the building "
  "is sold or fully repurposed rather than mothballed. Against those savings run the new costs: longer bus routes "
  "in the district's fastest-growing and worst-reimbursed budget line (families have warned of rides exceeding two "
  "hours a day), any staffing or space additions at the receiving schools, transition costs, and the quiet revenue "
  "risk that some families leave the district altogether, each departure taking at least $4,626 a year in base "
  "state funding with it, permanently (the fiscal 2027 base, the first year a closure could take effect; this "
  "report uses the fiscal 2027 figure for anything that would happen after a closure).")
P("Before totaling it up, one correction this version makes to its own earlier math, and it ran in the "
  "district's favor: prior versions credited $85,000 for every eliminated position. That is the right all-in "
  "figure for comparing spending filings, but it is the wrong figure for the General Fund, because Kentucky "
  "pays teacher retirement and health insurance on behalf of districts; the district's own year-end packet "
  "books $6.94 million of such on-behalf payments, and its own published salary schedule runs from $41,718 "
  "for a new Rank III teacher to $71,447 at the top of Rank I. The General Fund itself keeps only salary plus "
  "roughly five percent when a position goes away: <b>$50,000 to $75,000 per position, not $85,000</b>. "
  "Version 4.2 goes one step further and retires even that band: every staffing lever is now priced at the "
  "district's own fully loaded figure, <b>$54,479.40 per position</b>, from Appendix A.1 of its written "
  "response. Their number, their basis.")
P("Version 4.2 rebuilds the grid on the district's own 48-page response. Seven levers, each sourced: "
  "how much of the district's own $107,039 of building-bound expense lines actually stops (50 to 100 "
  "percent, plus its $20,000 insurance figure at the full stop); how many of the four fixed positions are "
  "cut over time rather than retained (its own appendix says all staff are retained in year one); zero to "
  "three teachers at its own $54,479.40 price (its savings sheet says two, its own classroom-capacity "
  "count supports three); the families who leave, from none to half the school, each taking $4,626 "
  "plus up to $1,000 of add-ons; the zone property effect; and the added busing a 110-square-mile zone "
  "requires. Run every combination, 5,832 in all, enumerated by build/closure_grid.py in this repository "
  "and published lever by lever in the workbook, and the result is Figure 7: the net yearly effect falls "
  "between <b>losing $591,545 and saving $488,631</b>, the middle half of all scenarios lands between a "
  "$148,790 loss and a $102,067 saving, the median outcome <b>LOSES $21,971 a year</b>, and 55 percent of "
  "scenarios lose money outright, before $100,000 to $300,000 of one-time transition costs in the first "
  "year. The plan's own requirement, $800,000 to $1,000,000 a year, sits entirely outside the range. One "
  "more thing closure does not buy: borrowing room. Bonding capacity is built from restricted revenue "
  "streams that do not grow when a school closes (Section 6).")
fig("chart_closure_spectrum.png",
    "Figure 7. The honest range. Top: the net yearly effect of closure across all 5,832 combinations of the "
    "seven sourced inputs, from losing $591,545 to saving $488,631, with the middle half of scenarios between "
    "a $148,790 loss and a $102,067 saving and the median at a $21,971 loss. The plan's own $800,000 to "
    "$1,000,000 requirement lies entirely outside the defensible range. Bottom: how far each input moves the "
    "central case by itself. Inputs: the district's own response worksheet and staffing appendix (Appendix "
    "A and A.1), its capacity appendix, its KDE filings, the federal attendance-zone map, and the exit "
    "routes open under HB 563, homeschooling, and the statewide virtual academy; every lever and formula is "
    "in the workbook's Closure_Model tab.")
H2("What the district's own ledger says this school costs")
P("In July 2026 the district answered an open records request and produced its books. The answer to what North "
  "Middletown costs moves by about a million dollars depending on which of the district's own documents you open.")
P("The 300-student breakeven, and every version of the cost case against this school, rests on $2,476,544, "
  "which comes from the federal per-student report and spreads district-wide costs across buildings. The "
  "district's own <b>Overall Cost by ORG</b> summary codes <b>$1,285,310</b> to North Middletown. Its FY2026 "
  "working budget codes <b>$1,706,493</b> to location 090, the school's own code, of which $406,333 is the "
  "state's on-behalf pension and health payments, which are not district cash. The two documents reconcile: "
  "$1,706,493 less on-behalf is $1,300,160, within 1.2 percent of the Cost by ORG figure. On a like-for-like "
  "basis, same year and same all-in definition, the federal report put $2,611,980 against the school for "
  "2023-24 while the working budget coded $1,593,309 to location 090 that year, a difference of $1,018,671 "
  "in central office, district transportation, the maintenance pool and district instructional support that "
  "no closure removes. One number puts the scale in view: of a roughly $44 million all-funds budget, the "
  "district codes $21,482,445 to any school at all.")
tbl(["School", "Coded by the district", "Enrolled", "Breakeven at $15,983", "Clears by"],
    [["North Middletown", "$1,285,310", "128", "80", "48"],
     ["Bourbon Central", "$4,033,689", "459", "252", "207"],
     ["Cane Ridge", "$4,326,733", "453", "271", "182"],
     ["Bourbon County Middle", "$3,868,106", "590", "242", "348"],
     ["Bourbon County High", "$5,515,105", "766", "345", "421"]],
    [W * 0.28, W * 0.22, W * 0.14, W * 0.22, W * 0.14],
    caption="The same corrected test as the table above, run on the cost the district's own ledger codes to "
            "each school rather than the cost the federal report allocates to it. Every school clears, and "
            "that is the finding rather than a defense of this one: the answer to how many students a school "
            "needs swings from 300 to 80 on the definition of cost alone, and the district picks the "
            "definition. Source: Overall Cost by ORG, produced July 2026; enrollment as elsewhere in this "
            "report. Model, School_Costs tab.")
P("The same ledger cuts against this report in one place. Measured on dollars coded to each school, North "
  "Middletown runs <b>$13,332</b> per student against $12,167 at Cane Ridge and $11,882 at Bourbon Central, "
  "premiums of 9.6 and 12.2 percent, against 3.6 and 6.7 percent on the federal all-in basis. Equally allocated "
  "overhead narrows every gap, so the direct-coded comparison necessarily shows a wider one. The dollar premium "
  "is $149,000 to $186,000 a year, and it remains smaller than this school's measured fixed base of $277,948. "
  "That is the scale argument in the district's own numbers: a fixed base spread over few students, not a school "
  "that overspends.")
P("Of the $1,706,493 coded to the school, on-behalf payments ($406,333) are not district cash, federal grants "
  "($191,048) follow the child, and food service ($170,423) is self-supporting from meal reimbursement. That "
  "leaves <b>$938,690 of General Fund money</b>, and most of it is teacher salary payable again at the "
  "receiving school. Measured by program: regular classroom instruction $397,700; school administration, "
  "meaning principal, secretary and extended day, $131,724; special education $107,175; primary and other "
  "instruction $81,442; plant, utilities, sanitation and water $58,774; library and media $49,097; custodial "
  "$37,333; student support $33,676; technology, field trips and other $41,769. The same ledger converts this "
  "report's per-position estimate from reasoned to measured: on-behalf payments coded to the school total "
  "$406,333 against $1,497,576 of salary and benefits, a load of 27.1 percent, which puts the General Fund "
  "share of an $85,000 position at $61,937, and the school's own classroom payroll line of $324,550 over 4.9 "
  "to 5.8 teaching positions works out to $56,000 to $66,000 each. Three routes, one answer, and it sits at "
  "the middle of the $50,000 to $75,000 range this report already uses.")
P("Two conclusions follow. First, the closure model estimated this school's avoidable fixed base at $230,000 "
  "mothballed and $290,000 sold. Measured, school administration plus custodial plus plant is <b>$227,831</b>, "
  "within half a percent of the lower figure, and every fixed line at the school including the library totals "
  "<b>$276,928</b>, which is less than the $290,000 published as the high case. The estimate was good and "
  "slightly generous to the closure at the top. Second, <b>$230,000 is the floor of the grid, not a floor "
  "case.</b> Reaching it requires that the principal, the secretary, the custodian and the utilities all go. "
  "Districts frequently redeploy people rather than cut them, and if that happens here the closure avoids the "
  "utilities and nothing else, $58,774. The old grid contained no such scenario, which meant every figure this "
  "report published assumed the district would make the deepest cut available to it. <b>So version 3.9 rebuilt "
  "the grid</b> on three measured values: staff reassigned and utilities only, $58,774; mothballed with those "
  "positions cut, $227,831; sold, adding the library and media line, $276,928. That correction moved the "
  "median from $91,240 to $21,571. The district's written response then answered the open question directly: "
  "all current staff would be retained, savings arrive only through attrition, and its own appendix prices "
  "the avoidable expense lines at $107,039 plus $20,000 of insurance. Version 4.2 therefore rebuilds the grid "
  "once more, this time on the district's own figures throughout, and the median flips negative: a $21,971 "
  "yearly loss, with 55 percent of scenarios losing money.")
P("There is a limit to what any ledger can settle. The seven inputs that decide a closure's net effect span about "
  "$950,000. The district's books speak to two of them, worth about a third of that spread. The rest, how many "
  "families leave, whether the building is sold or mothballed, whether the receiving schools need capacity work, "
  "how far the buses go, and whether staff are cut or moved, are decisions rather than accounting. The range is "
  "wide because the decisions are open.")
P("The same records response contains a staffing document that answers the scale question from the other "
  "direction. The School Council Allocation for 2026-27 gives North Middletown <b>5.5 fixed positions</b>: a "
  "principal, a secretary, a custodian, one paraprofessional, and half a librarian, half a housekeeper and "
  "half a library aide. No assistant principal. No counselor. Bourbon Central receives 12.25 fixed positions "
  "and Cane Ridge 11.5, each with an assistant principal, a counselor, three paraprofessionals and two "
  "secretaries. Per hundred students that is 5.0 fixed positions at North Middletown against 2.6 at the "
  "receiving schools, and that ratio is printed here because it is the first thing a critic would compute. It "
  "is also the whole scale argument: a building needs one principal and one office whether it holds 128 "
  "children or 460, and the leanest-staffed school in the county is the one proposed for closure. A note on "
  "the same document's teacher column: it is enrollment divided by the KRS 157.360 statutory cap, cell by "
  "cell, on a sheet headed maximum class size staffing. It is a floor, not a roster, and this report does not "
  "use it as a staffing count.")

H2("Bourbon County has run this play before: Millersburg, 2006")
P("Millersburg Elementary, about nine road miles from Paris, closed in 2006 with a final enrollment of 119 students, "
  "nearly the size of North Middletown today. Its students went to Cane Ridge, whose addition the district's "
  "own facility plan dates to 2007. What happened next is on the census rolls, Figure 8: Millersburg fell "
  "from 842 people in 2000 to 792 in 2010 to 747 in 2020, down 11 percent, while the county grew 4.6 percent. "
  "No single closure did that alone, and this report is careful not to conflate the town's two lost schools: the private Millersburg Military Institute, after a temporary 2003 closure, shut permanently in July 2006, and the public elementary never opened that fall. The Joy Global plant followed "
  "in 2013, taking 197 jobs and, by the town's own accounting, half its operating budget. That is the honest "
  "lesson, and it is worse, not better: small towns lose their anchors in cascades, each loss making the next "
  "more likely. Twenty years later the district is over capacity at the school that absorbed Millersburg's "
  "children and proposes to solve it by closing another small school. North Middletown's attendance zone "
  "holds 2,625 people. The records ask writes itself: produce the savings analysis from the 2007 closure and "
  "the savings actually realized, so this community can compare projection to outcome before the same "
  "projection is made again.")
fig("chart_millersburg.png",
    "Figure 8. Millersburg and Bourbon County population, indexed to 2000, with the town's three institutional "
    "losses marked. The elementary's 2006 date is its federal record: enrolled through 2005-06, status closed "
    "in the 2006-07 CCD universe file; the military institute is a separate, private school that closed "
    "permanently in July 2006. Decennial census counts: Millersburg 987, 937, 842, 792, 747; the county grew 4.6 percent "
    "from 2000 to 2020. Millersburg Elementary's final enrollment was 119 students; North Middletown enrolls "
    "128 today.")
H2("Has this ever worked in Kentucky? We checked all thirty years")
P("From the federal Common Core of Data, every Kentucky public school, every year, 1994 through 2023, I built the "
  "complete record: <b>339 rural and small-town school closures since 1995</b>, after screening out renames, "
  "rebuilds under new federal IDs, and non-community programs, and <b>72 towns that lost their last public school "
  "entirely</b>. Millersburg 2006 is one of them, which independently validates the method. The full lists and "
  "inputs are archived in this repository. Three findings follow.")
P("<b>First, the money.</b> For the 163 closure events with clean finance data, I compared each district's "
  "spending from the year before closure to three years after against the statewide trend and against similar- "
  "sized districts, credited the ENTIRE gap to the closure, the most generous reading, and priced it per "
  "displaced student. Figure 9 shows the whole distribution. The median closure produced <b>$1,102 per displaced "
  "student</b> ($818 among the physically plausible cases), and <b>40 percent of districts spent MORE than trend "
  "after closing</b>. Both tails hold events beyond $13,000 per child, more than any school costs to run per "
  "student, which indicates budget-wide events rather than closures, and is why this report prices closure "
  "bottom-up from positions, busing and state funding. One figure anyone can compute from the archived "
  "spreadsheet: the raw median for the 27 closures most like this plan prints $8,440. It is an artifact, whole- "
  "district budget noise divided by 60-to-320-student denominators, with 11 of the 27 beyond the physical "
  "ceiling; inside the plausible window that median is <b>$541</b>. The yardstick: this plan needs <b>$6,250 to "
  "$7,813 per displaced child</b>, above the record's 75th percentile. Among rural elementary closures the one "
  "clean comparable with nothing built, Webster County's closure of Slaughters Elementary in 2012, paid $3,525; "
  "every case at or near the plan's number came with a new school (Perry 2017, Adair 2006, Metcalfe 2013) or was "
  "a city or county-seat grade reshuffle (Somerset 1999; Montgomery 2018, which opened a new elementary the same "
  "year). The two methods bracket rather than coincide, and the v3.9 grid rebuild moved this report's number and "
  "not the record's: thirty years of budget outcomes put the plausible median at $818 per displaced student, "
  "while this report's bottom-up model now reads $169, down from $713 before the fixed-cost lever was rebuilt on "
  "measured lines. They measure different things. The record's figure credits a district's entire budget change "
  "to its closure, an upper bound by construction; the bottom-up figure prices only the levers a closure moves. "
  "The plan's requirement is eight times the first and thirty-seven times the second.")
fig("chart_ky_record.png",
    "Figure 9. Top: all 163 measurable Kentucky rural closures, priced per displaced student with each "
    "district's entire budget gap against the state trend credited to its closure. The median is $1,102; 40 "
    "percent of districts spent more than trend after closing; the shaded tails beyond $13,000 per child "
    "exceed what any school costs to run per student and mark budget-wide noise, not closure effects. "
    "Bottom: the rural elementary cases only. The one clean no-construction comparable (Webster 2012) paid "
    "$3,525 per displaced student; Perry, Adair, and Metcalfe built new schools; the plan requires $6,250 to "
    "$7,813 while building nothing. City and county-seat grade reshuffles (Somerset 1999; Montgomery 2018, "
    "which opened a new elementary the same year) appear in the top panel but are not comparisons for a "
    "rural closure. Data: build/ky_closure_events_full.csv (every event, every input), build/ky_rural_closures_1995_2023.csv, and build/ky_closure_dollar_cases.csv.")
P("<b>Second, the classrooms.</b> Test scores can only be compared within one accountability system, so I tested "
  "the 42 closure events measurable inside the 2012 to 2019 window on the uniform federal proficiency series. "
  "Eleven districts improved three or more points against the state, ten declined, twenty-one were flat: a wash, "
  "median half a point down. And the pattern inside the wash points one way: the more children a closure "
  "displaced, the worse the trend. Events moving fifteen percent or more of a district's students ran a median "
  "two points down; the improvers were overwhelmingly small closures inside eastern Kentucky's broad mid-decade "
  "testing rebound, gains far too large for schools that were one to eight percent of their districts to explain. "
  "Exactly <b>one</b> event in the record shows both clear savings and clear gains: Leslie County 2013, which "
  "folded its middle school into an existing campus in the same community. No case in this record shows a "
  "district closing a rural town's elementary school, clearly saving money, and clearly improving scores.")
P("<b>Third, the two best cases, disclosed by us so no one has to discover them.</b> Perry County closed "
  "three rural elementaries in 2017 and shows real, modest savings, about $3,600 per displaced student, with "
  "scores continuing a climb that began years earlier; it did so by building the new West Perry Elementary "
  "for the children it moved. Johnson County closed 178-student Meade Memorial Elementary in 2016 with "
  "nothing built and spending ran about six points under the state trend afterward, while scores stayed "
  "flat: savings without improvement, in proportion to the school's five percent share of the district, "
  "which is our own model's median arriving on schedule. Those are the strongest cards the record deals a "
  "closure advocate, and neither resembles what this plan promises. Two honest limits belong here too: "
  "closures before 2012 and after 2016 cannot be score-tested across Kentucky's assessment-system changes, "
  "and small towns that kept their schools also declined in population at nearly the same rate as towns "
  "that lost them, so I make no claim that closure causes population decline. What the record does show is "
  "narrower and harder: no measurable precedent for the savings this plan requires, and none for academic "
  "improvement from a closure like this one. If the board believes it will be the first in thirty years, "
  "show us the data.")

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
P("The costs to children pile on top of the costs to the budget: a 2024 national study following 470 Texas closures found displaced "
  "children, low-income children most of all, absent more often, disciplined more often, and earning less as "
  "adults. Roughly three-quarters or more of North Middletown's students qualify for free or reduced-price meals. "
  "If Bourbon County believes its closure would beat this record, the burden is on the administration to show the "
  "math.")
P("When the district shows its numbers in public, watch four ways it can frame them, because each can make "
  "closure look better than it is: gross site cost presented as savings; restricted building dollars presented as "
  "operating relief; per-pupil cost cited without noting that state funding follows the student; and district- "
  "wide cost growth attributed to one small school. I flag my own judgment calls where they occur.")
P("Whatever the true net number proves to be, one comparison frames the decision, and it holds on either honest "
  "yardstick. Against the $2.6 million structural deficit before transfers, closing North Middletown addresses at "
  "best a small fraction; against the roughly $1.15 million the district actually draws from reserves each year, "
  "the favorable case reaches a bit over half, and the base case under a third. On either measure it is a partial "
  "fix, while the measures in Section 9 total more, harm no student, and close no town's school.")

H2("The 300-student breakeven, reconstructed from the state's own files")
P("At the July committee meeting a figure was cited: North Middletown needs about 300 students to break even. "
  "No worksheet has been published with it, so this version reconstructs it from the state's own files, and "
  "both sides of the fraction can now be named. The cost side is $2,476,544, which is 128 students "
  "times the $19,348 per-student total on the 2023-24 state report card, a figure that "
  "includes federal spending and the state's on-behalf pension payments, that pairs a 2023-24 rate with a "
  "later headcount (the same rate at that year's 135 students gives the $2,611,980 the school actually "
  "reported), and that the federal report allocates to the school rather than the district's own budget "
  "coding to it. The revenue side that yields 300 is "
  "state revenue alone: in 2022-23, state sources came to $8,305 per member, and $2,476,544 divided by $8,305 "
  "gives 298 students; per SEEK attendance instead of membership it gives 303, and the implied $8,255 sits "
  "between the two. One other route reaches about the same place, and it only became testable when the district "
  "produced its ledger in July 2026: $1,285,310, the cost the district's own Cost by ORG summary codes to this "
  "school, divided by the $4,626 SEEK base, gives 278. Both routes are the same construction, a whole-cost "
  "numerator over a single revenue stream; 298 fits the district's stated \"about 300\" within 0.7 percent and "
  "278 within 7.3 percent. The district collects three "
  "streams per student, not one: in 2023-24, $5,475 local, $7,128 state, and $3,380 federal, $15,983 in all. "
  "The 300 construction counts every dollar of cost from all three sources, then credits the school only the "
  "state share of what its students bring in; the local and federal revenue those same children generate, "
  "$8,855 per student, more than the state share, is counted on the cost side and skipped on the revenue "
  "side. Run the same fraction with matching definitions and the breakeven is 155 students, not 300.")
tbl(["School", "All-in cost per pupil", "Enrolled", "Corrected-test breakeven", "Short by"],
    [["North Middletown", "$19,348", "128", "155", "27"],
     ["Bourbon Central", "$18,131", "459", "521", "62"],
     ["Cane Ridge", "$18,670", "453", "529", "76"],
     ["Bourbon County Middle", "$16,673", "590", "615", "25"],
     ["Bourbon County High", "$17,404", "766", "834", "68"]],
    [W * 0.28, W * 0.20, W * 0.14, W * 0.24, W * 0.14],
    caption="The corrected average-cost test (all-in cost against the district's full $15,983 revenue per "
            "member) applied to every school the district owns. Every school fails, including both receiving "
            "schools; Cane Ridge falls short by 76 students and about $1.2 million a year, nearly three times "
            "North Middletown's shortfall. Statewide, 1,146 of the 1,151 Kentucky schools with reported data, 99.6 "
            "percent, spend more per student than the $8,255 bar the 300 implies; on the corrected test in "
            "this table, against the district's full $15,983 revenue per member, 786 of them, 68 percent, "
            "still fail. Nobody reads Cane Ridge's number as a closure argument, and rightly so: an "
            "average-cost breakeven in a drawdown year measures the district's budget, not any school. "
            "Model, School_Costs tab.")
P("The real breakeven question is the marginal one: at what enrollment do a school's students bring in more "
  "than closing it could actually save? Set each school's fixed site base, principal, office, and plant, "
  "against the state guarantee that is actually at risk when a family leaves the district rather than "
  "transferring inside it, and North Middletown clears its bar at 54 students on the district's own measured "
  "principal and office line of $132,744 plus its measured plant line of $96,107, 66 once the school's "
  "measured library and media line of $49,097 is counted with them, and 69 on the $290,000 this model "
  "estimated, while enrolling 128. This version drops the lower bar "
  "published in v3.8, which credited each child with $3,380 of federal money: the district's working budget "
  "shows federal grant spending at this school of $191,048, and Title I is a district allocation driven by "
  "resident poverty, so it follows the child to the receiving building and relieves the General Fund by "
  "nothing. The same test puts Cane Ridge's bar at 77 and Bourbon Central's at 86; every school clears "
  "comfortably, which is how school finance is supposed to work. The full grid version in this section, with position, busing, and leaver effects, "
  "brackets North Middletown between 20 and 122 students. Every construction of the question except one, "
  "all-source costs divided by state-only revenue, says this school brings in more than closing it could recover. One request follows: "
  "publish the worksheet behind the 300. If it differs from this reconstruction, the district's own records "
  "are the fastest way to show it.")

H2("What this school has cost, in every year the state has ever measured it")
P("The cost argument rests on one recent number, so this version assembles every school-level cost figure that "
  "exists in any state or federal record: three reporting systems reaching back a quarter century, each archived "
  "in the repository. The oldest are the 2000-01 state report cards, recovered from the Internet Archive, and "
  "they show all four of the district's then-elementaries on a single scale curve: about $2,851 per student plus "
  "a fixed base of about $332,000 per building spread over however many children the zone lines assign to it. "
  "That one formula predicts every school within 4 percent: Bourbon Central $3,360 reported at 595 students, Cane "
  "Ridge $4,053 at 312, North Middletown $4,414 at 193, Millersburg $5,200 at 145. No school on that list was "
  "mismanaged; the ranking is enrollment, and Cane Ridge itself cost 21 percent more than Bourbon Central for the "
  "same scale reason North Middletown cost 31 percent more. In every year measured, the cheapest school in the "
  "county has been its biggest.")
P("The middle years confirm it: KDE's own report-card datasets for 2011-12 through 2016-17 show North "
  "Middletown's premium widest exactly when the building was emptiest, 133 to 177 students, and two federal "
  "collections that measured school-level salaries independently, the Civil Rights Data Collection and the "
  "NCES school-level finance survey, show the same pattern. Federal staffing records (CCD, 1996 to 2019) "
  "show the school staffed at parity with both larger elementaries in its 200-student years, including its "
  "2007-09 peak. And the record contains a controlled experiment: Millersburg's premium over its receiving "
  "school was about $166,000 a year on the 2000-01 report cards; the district closed it in 2006; and the "
  "thirty-year record in this report shows the district's budget did not measurably bend. North Middletown's "
  "premium today is $156,000, the same experiment at almost the same number, twenty-three years apart. "
  "Provenance notes: the 2000-01 figures are as printed on the recovered report cards, with archived copies "
  "being added to the repository; CATS-era cards may report prior-year spending, which does not affect the "
  "within-year comparison; the 2012-13 file prints North Middletown at $19,635 in a renovation year, an "
  "obvious capital charge excluded from operating comparisons; and the three reporting systems use different "
  "definitions, so every comparison here is within one system in one year. The School_Costs tab carries all "
  "of it live.")

# ================= 5. ACADEMICS =================
H("5. Academic Performance: The District Would Be Closing Its Best Elementary School", need=5.3)
fig("chart_district.png",
    "Figure 10. Top: the official state record, Kentucky's overall accountability composite in its two "
    "comparable eras (Unbridled Learning overall score, 2012-2016; KSA overall indicator rate, 2022-2025). No "
    "composite was issued from 2017 through 2021 (system transition, star-rating years, then COVID), and "
    "CATS-era school files (2006-2011) are available from KDE by data request. Bottom: SchoolDigger's "
    "third-party 0-100 index of the same tests, retained for context and validated against the official "
    "record; wherever the two disagree, the official record governs. Sources: KDE historical datasets, "
    "archived in this repository as build/kde_scores_history.json.")
fig("chart_compare.png",
    "Figure 11. SchoolDigger's normalized 0-100 index for 2024-25 across the region's elementary schools, computed from state test data (not KDE's official rating). Montgomery County operates four elementaries; the two with retrieved index values are shown, and Montgomery "
    "County's two elementaries outscore North Middletown; every elementary in Bourbon County, Clark County, and "
    "Paris Independent trails it.")
H2("The state's own numbers, first")
P("Before any index or ranking, here is the primary record: the Kentucky Department of Education's school-level "
  "assessment file for the 2024-25 Kentucky Summative Assessments, archived in this repository "
  "(build/kde_ksa_2024_25.json) so anyone can check it. On the state's own tests, North Middletown is first "
  "among all four elementary schools in Bourbon County, county district and Paris Independent alike, in every "
  "tested subject, and it beats the <b>statewide</b> elementary average in science and writing.")
tbl(["Subject (percent proficient or distinguished)", "NMES", "Bourbon Central", "Cane Ridge", "Paris Elem.", "KY average"],
    [["Reading", "41", "38", "37", "25", "49"],
     ["Mathematics", "31", "28", "27", "29", "43"],
     ["Science", "53", "26", "*", "*", "37"],
     ["Social Studies", "36", "31", "27", "22", "38"],
     ["Combined Writing", "56", "40", "27", "4", "43"]],
    [2.35 * inch, 0.85 * inch, 1.15 * inch, 0.95 * inch, 0.85 * inch, 0.9 * inch],
    caption="Kentucky Summative Assessment results, 2024-25, all students, percent scoring proficient or "
            "distinguished. Source: KDE School Report Card assessment dataset, archived in this repository. "
            "Asterisks are cells the state suppresses for small groups; the Kentucky average is the statewide "
            "elementary level. North Middletown leads all four county schools in all five subjects.",
    bold_first_col=True)
P("Here is the full arc, straight from the state's own files (Figure 10, top panel). Through the Unbridled "
  "Learning era North Middletown's official overall score rose every single year, 62.6 to 68.8 to 71.4 to 72.1 "
  "to <b>79.1</b>, closing 2015-16 with a formal <b>Distinguished</b> classification, the county's best score "
  "by nearly ten points. The same files show the school <b>first in the county in elementary mathematics in "
  "every pre-COVID administration on record</b>, 2011-12 through 2018-19, eight straight. The pandemic "
  "cratered every school in the county; the recovery is where they separate. North Middletown's overall "
  "indicator rate climbed 51.9 to 62.2 to <b>74.5</b> in 2023-24, first in the county by fourteen points, with "
  "reading and math both at 45 percent proficient or better. In 2024-25 a tested cohort of roughly sixty "
  "children slipped to 41 and 31 while statewide averages ticked up, a real single-year decline worth "
  "watching, and the school still finished first among all four county elementaries in every subject where the state publishes comparable results (two schools' science scores are state-suppressed small groups). "
  "Small schools swing hard in single years, in both directions; the record above is why one soft year argues "
  "for attention, not for closure. One reading note, because the official index line crosses in 2024-25: "
  "Kentucky's overall index blends each year's level with the change from the year before. On every 2024-25 "
  "status measure the state computed, North Middletown led Bourbon Central: the weighted reading and math "
  "content indexes (58.5 and 48.7 against 55.5 and 45.4), every other subject, the climate survey (78.0 to "
  "76.5), and the safety survey (73.5 to 72.3). The index crosses only because the change formula subtracts "
  "North Middletown's own 2023-24 spike and credits Bourbon Central's climb off its 50.3. A school is not "
  "worse for having been excellent the year before; that is the change component working as designed on a "
  "small cohort, and the state's component file is archived in the repository.")
P("The site's score chart now also carries the federal EDFacts series, the U.S. Department of Education's "
  "own record of each school's reading and math proficiency, 2009-10 through 2018-19 plus the 2020-21 "
  "COVID administration (federal and state agree within two tenths for North Middletown that year): an independent "
  "federal cross-check of the state numbers that reaches two years further back, into the era of the 2011 "
  "Blue Ribbon, where North Middletown prints 89.5 and 94.8 on the old KCCT scale. Kentucky replaced its "
  "test in 2011-12, so federal values before and after that line are different scales, and the file reports "
  "small-school values as range midpoints; the extract is archived in the repository.")
P("I keep the SchoolDigger index in Figure 10's lower panel and in Figure 11 only as outside context, with "
  "its limits printed. Tested against the official record, it tracks the county's larger schools closely "
  "(correlation near 0.9) but is unreliable year to year for a school North Middletown's size (near 0.4), and "
  "it named the wrong county leader in three of the ten years both sources cover, twice against North "
  "Middletown, including the year the state rated the school Distinguished. It still adds one thing the "
  "official archive cannot yet show: the Blue Ribbon-era view, where North Middletown's index reached 87.9 "
  "and 85.8 around 2010 and 2011; the official CATS files for those years are on request with KDE. Wherever "
  "the index and the official record disagree, the official record governs in this report.")
P("In 2023-24 North Middletown matched the statewide elementary average in reading (45 percent proficient or "
  "better against 47) and beat it in mathematics (45 against 42); in 2024-25 it beat the state decisively in "
  "writing (56 against 43) and science (53 against 37). Most striking for a school where about three-quarters of "
  "children qualify for free or reduced-price meals: on the third-party index, its economically disadvantaged "
  "students alone rank in the 62nd percentile of all Kentucky schools, evidence that this environment lifts "
  "precisely the students the research says are hardest to lift.")
P("This is not a new story. In 2011 the U.S. Department of Education named North Middletown Elementary a "
  "<b>National Blue Ribbon School</b>, one of just five Kentucky public schools honored that year, an award "
  "reserved for schools performing in roughly the top ten percent of their state in reading and mathematics, and "
  "the state's education department separately gave it an inaugural Distinguished Winners Circle Award. In the "
  "years around that recognition the school ranked 36th of 683 Kentucky elementary schools (2010) and 51st of 688 "
  "(2011). The school the district proposes to close is not a school with a history of failure; it is a school "
  "with a history of excellence, now climbing back toward it.")
P("The record was built by people, and two anchor it: Mrs. Beverly Craycraft and Mrs. Roxanne Mitchell. For "
  "generations of North Middletown families those two classrooms set the standard for kindergarten through fifth "
  "grade. Mrs. Mitchell, twenty years into her fifth grade room when the Blue Ribbon arrived, credited the "
  "earlier grades with “providing the foundation my students need in basic geography skills” and pointed to "
  "traditions reaching beyond the walls: “It has been customary for 3rd-grade students to tour stops along the "
  "Underground Railroad in northern Kentucky.” The honors around them are documented: Alison Cloyd (2014) and "
  "Lydia Austin (2017) each received Campbellsville University's Excellence in Teaching Award, for which a "
  "district puts forward one teacher at a time, and the Blue Ribbon culture ran on community-powered programs, "
  "notably “ArtBurst,” which threaded the performing and creative arts through core academics. The present "
  "belongs to a new set of educators: under principal Hannah Southall the current staff took the school from its "
  "COVID-era trough back to the county's best official overall rate, 74.5 in 2023-24, and the county's top marks "
  "in every state-reported subject in 2024-25, and keeps a gifted-and-talented program running. What that faculty "
  "needs is not consolidation. It is time, and a district willing to back them.")
P("Two honest caveats belong here. Small schools produce noisier year-to-year scores, 128 students is a small "
  "sample, and subgroup results vary widely: the school's girls (85.7, the 91st percentile) far outpace its boys "
  "(28.8), a gap the district should be helping the school close rather than closing the school. The same "
  "caution cuts both ways: no single year should define any school, which is why three-year averages matter, "
  "and they tell the same story. On the SchoolDigger index, third-party and kept only for context, North Middletown averages 48.1 for 2023 through 2025, against 26.4 at Bourbon "
  "Central and 29.9 at Cane Ridge. Neither caveat "
  "changes the central fact: the consolidation "
  "on the table would move children from the district's strongest elementary environment into its weakest ones. If "
  "the administration believes those receiving schools can preserve these students' outcomes, that belief should be "
  "supported in writing, with a transition plan, before any vote, not assumed after one.")

# ================= 6. BONDS =================
H("6. Bonds, Buildings, and Two Different Pots of Money")
P("Kentucky school finance separates operating money from building money, and that split decides what "
  "closing a school can and cannot do. Districts do not borrow directly: a Finance Corporation, a separate body on paper "
  "but made up of the same people as the Board, issues bonds and leases the buildings back to the district. The "
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
    caption="Figure 12. Outstanding bonds of the Bourbon County School District Finance Corporation, from Note 4 of "
            "the FY2025 audited financial statements. The 2016 issue refinanced $5,315,000 of 2009 bonds (saving "
            "$314,834 in present value) and the 2020 issue refinanced $3,410,000 of 2011 bonds (saving $106,627). "
            "* The audit's figures for the 2013R issue are internally inconsistent: the outstanding balance exceeds "
            "the listed original amount, and the stated maturity contains an obvious typographical error. Both are details "
            "the finance office should correct on the record.",
    bold_first_col=True)
fig("chart_debt.png", "Figure 13. Annual bond payments are rising as the 2024 issue comes online. The state's SFCC "
    "pays $1,568,809 of the outstanding principal over the life of the bonds. Source: FY2024 and FY2025 audits.",
    width=4.6 * inch)
P("Three things in the bond record deserve the Board's attention.")
B("<b>The 2024 borrowing's stated purpose is on the public record, and it names the high school, not any "
  "elementary.</b> The SFCC Bond Payee Disclosure reviewed and approved by the legislature's Capital Projects and "
  "Bond Oversight Committee on June 20, 2024 states the purpose of the Series of 2024 bonds: various construction "
  "projects including roof replacement at Bourbon County High School and a districtwide audio system. The issue "
  "was presented at an estimated $10 million with an 18 percent SFCC share and sold at $6.055 million; the "
  "proceeds flowed into the Construction Fund, where construction in progress grew from $3.65 million to $7.41 "
  "million during fiscal 2025, matching that fund's spending almost to the dollar. The disclosure and the "
  "committee minutes are archived in this repository. The BG-1 project applications would complete the "
  "project-by-project accounting, and Question 7 asks for them.")
B("<b>No bond issue on record names North Middletown Elementary.</b> The capital program has flowed elsewhere for "
  "years, and the 2021 facility plan shows where: its in-biennium priority was the $6.66 million high school "
  "Career and Technical Center, while North Middletown's $3.62 million renovation sat scheduled after the "
  "biennium. That raises a fairness question the administration should answer directly: how much has been "
  "invested in this building compared with the district's other schools over the past decade? The records "
  "requested in Appendix B would answer it.")
B("<b>The construction fund ran a negative $1.43 million restricted balance at June 30, 2024</b>, project spending "
  "ran ahead of the borrowing that later covered it. Not improper in itself, but it shows a capital program being "
  "prioritized and paid for out of cash flow in the same years the operating budget went into deficit. The fiscal 2024 audit also "
  "notes the district held $23.5 million in unused bonding capacity as of June 30, 2024, borrowing room for buildings that, again, "
  "cannot pay teachers either way.")
H2("What closing a school does, and does not do, to bonding capacity")
P("A district's ability to borrow for buildings is simple math set by statute and regulation, and it is worth "
  "walking through, because “bonding capacity” is likely to surface in the closure debate. Kentucky districts "
  "build capacity from two restricted streams: the capital outlay allotment of $100 per student in average daily "
  "attendance (KRS 157.420), of which regulation lets a district pledge 80 percent, the rest held back as a "
  "safety factor (702 KAR 4:160), and the restricted building-fund levy, the “nickel,” with its state FSPK "
  "equalization (KRS 157.440). Set existing debt payments against those streams and what remains is the room for "
  "new debt. On the fiscal 2025 numbers: roughly $224,000 a year of capital outlay, about $2.05 million of "
  "building-fund tax, and $1.58 million of district-paid debt service in fiscal 2026. The fiscal 2024 audit "
  "states the bottom line plainly: about $23.5 million of unused bonding capacity as of June 30, 2024. The companion workbook lays "
  "the components side by side on the Debt_Service tab.")
P("Nothing in that math grows when a school closes: no assessment, no attendance, no levy. What it changes is the "
  "plan, not the capacity: a “transitional” label removes the school's modest listed needs from the priority list "
  "and steers future SFCC offers of assistance (KRS 157.622), and the district's own borrowing, toward other "
  "projects, such as the career-and-technical center ambition in the district's planning documents. That is a "
  "choice about priorities, and it deserves to be argued openly as one, with the bonding potential statement on "
  "the table. The math can also run against the district: every family that responds to closure by leaving takes "
  "$100 a year out of capital outlay and the SEEK base out of operations, permanently. Nor is an emptied building "
  "a windfall: the Pew study in Section 4 found districts typically realized $200,000 to $1 million on sales, "
  "one-time money that is itself restricted to capital use.")
P("As for where the 2024 borrowing went: the $6.055 million issue, at 4.00 to 5.00 percent interest through "
  "2044, flowed into the Construction Fund, where construction in progress grew from $3.65 million to $7.41 "
  "million during fiscal 2025, matching that fund's spending almost to the dollar. As it and the other series "
  "settle into their schedules, the district's total debt-service payment steps up by about $430,000, from $1.15 "
  "million in fiscal 2025 to $1.58 million in fiscal 2026 (that $430,000 is the net change across all seven "
  "series, some rising and the 2013 issue maturing, not the 2024 bond's payment alone). The state's SFCC participates in the qualifying "
  "issues, paying $1,568,809 of principal over the life of the bonds. None of the seven outstanding issues "
  "names North Middletown Elementary, and the 2024 issue's stated purpose on the state disclosure, roof "
  "replacement at the high school and a districtwide audio system, confirms the pattern: the active capital "
  "program serves other buildings. The BG-1 project applications would complete the accounting, and Question 7 "
  "asks for them.")
H2("The $14 million plan, and the levers not on the table")
P("At the July 15, 2026 planning committee meeting, the superintendent stated that the district must free up "
  "$800,000 to $1,000,000 a year in operating money to bond $14 million. That is a general-fund bond: the payment "
  "would come from the budget that pays teachers. Debt service on $14 million runs roughly $0.8 to $1.1 million a "
  "year depending on term, about the same size as the school's claimed operating cost, so money saved by a "
  "closure would go to debt service and the general fund deficit itself would not shrink. The published savings "
  "estimates also do not support a bond of that size: bond capacity is annual savings capitalized, and the "
  "district's own KDE-filed school-level spending puts North Middletown's full excess cost near $121,000 a year, "
  "which supports about $1.6 million of bonds. This report's two-tailed best case, $488,631, supports about $6.3 million, and its median, a $21,971 yearly loss, supports none. "
  "Of the available estimates, only the administration's own unpublished figure reaches $14 million. The "
  "workbook's Debt_Service tab runs every scenario.")
P("Three funding sources are available without a closure. First, the restricted capacity itself: the FY2024 "
  "audit's $23.5 million, less the local share of the 2024 issue, leaves roughly $18 million, and the district's "
  "debt schedule shows why it is usable now. District-paid payments hold near $1.58 million a year through 2030, "
  "fall to about $1.32 million in 2031 to 2035, and drop below $400,000 after 2035 as the 2013, 2016 and 2020 "
  "series retire; a standard wrap-around structure fills exactly that shape. Second, the nickel stream is "
  "stronger than this report first described, a correction that runs in the district's favor. KDE's SEEK payment "
  "schedules and Nickel Levy Chart show Bourbon already levies a recallable nickel alongside the original "
  "facilities nickel. The board levied it on August 17, 2023 and the recall window closed with no petition, so "
  "the community has accepted a facilities tax twice. KDE's levied-rates file decomposes the 52.4-cent rate as "
  "41.0 general fund plus 5.7 FSPK plus 5.7 recallable. State equalization on that nickel is phasing in, $82,866 "
  "on the FY2025 schedule and $276,246 a year at full value on the FY2027 schedule, new restricted revenue that "
  "expands bonding capacity with no board action. The same file puts Paris Independent at 71.5 cents with 17.4 "
  "cents of recallable building levies. Third, SFCC offers of assistance, the state participation already "
  "carrying $1.57 million of current principal. These raise amounts comparable to the plan's $14 million, so the "
  "decision is a choice among funding mechanisms and should be made with the fiscal agent's current bonding "
  "potential statement public. The workbook's Debt_Service tab combines them into a balanced-budget scenario: "
  "close the operating gap first from levy increments and cost reductions, then fund construction from the "
  "remainder plus the new nickel equalization, with the capital-to-operations sweep ended so the building-fund "
  "stream is free to pledge. It supports roughly $21 million of capacity in the conservative case, treating the "
  "FY2026 miscellaneous receipt as one-time, and about $25 million on the FY2026 trend. On the trend the budget "
  "balances with about $283,000 to spare; the conservative case remains about $1.24 million short.")
H2("The June 2026 capital transfer: what the year-end packet reveals")
P("The June 2026 year-end packet, archived in this repository, documents a transaction that decodes the plan. In "
  "June 2026 the district moved $1,320,939 of restricted capital money into the general fund: $1,098,663 from the "
  "Building Fund and $222,276 from Capital Outlay, which ended the year at exactly zero. The transfer is lawful, "
  "under a flexibility provision Kentucky's budget acts have carried since 2020, exercised through a Capital Funds "
  "Request to the state. The Building Fund piece sat in the district's own working budget from September 2025 at $1,120,203; the $222,276 Capital Outlay piece appears in no version of the FY2026 budget, and the packet's sending-fund page books the Building Fund transfer $30 below its own General Fund ledger, the figure used here. Its significance is "
  "simple. The Building Fund collects about $2.5 million a year from the two facilities nickels; debt service "
  "consumes about $1.38 million; the roughly $1.1 million residual is precisely the restricted stream that could "
  "service a $14 million bond. In fiscal 2026 that residual plugged the operating budget instead. So the plan, "
  "decoded from the district's own books: let the general fund stand on its own, stop the sweep, and pledge the "
  "nickel residual to the bond. Any recurring million dollars performs that function, the untaken 4 percent levy, "
  "the alternatives package, or reductions elsewhere in a $22 million budget. The closure is one candidate among "
  "several, and the smallest-yield one.")
H2("Where the general fund is actually trending: the unaudited FY2026 close")
P("The district's own KDE Budget Monitoring Tool, included in the June 2026 financial packet on the board's July "
  "16, 2026 agenda and archived in this repository, shows fiscal 2026 closing down roughly $374,000, the best "
  "result in three years, against audited drawdowns of $1.07 million in fiscal 2024 and $1.23 million in fiscal "
  "2025. The same packet shows how that headline was built. Two June entries account for nearly all of it: the "
  "$1,320,939 capital transfer described above, and a $1,413,929 receipt booked to miscellaneous revenue in "
  "period 12 against a budget of zero, in a line that produced about $154,000 across the other eleven months "
  "combined. June revenue totaled $3.92 million against $1.13 million in June of the prior year, and those two "
  "entries are 98 percent of the difference. The packet's variance row reconciles to the dollar: the projected "
  "$4.08 million fund balance equals the $1.49 million budgeted contingency, plus revenue $2.23 million over "
  "budget, of which the June miscellaneous entry is 63 percent, plus salaries $588,000 under budget and $224,000 "
  "below the prior year, less other expenses $224,000 over budget. The genuine improvements are real but modest: "
  "SEEK revenue $402,000 over budget and payroll falling through ordinary attrition. Excluding the capital "
  "transfer, the year is down about $1.7 million; excluding the unidentified June receipt as well, about $3.1 "
  "million, the same range as the audited years. These figures are unaudited, the general fund balance sheet "
  "shows no receivable behind the June receipt, and the packet does not identify its source. The district should "
  "identify it on the record before this close is cited to justify anything, in either direction, and a decision "
  "as permanent as a school closure should be evaluated against audited actuals as well as budgets.")

# ================= 7. THE BUILDING =================
H("7. The North Middletown Building Itself")
P("If the closure case rests on the building, the record so far does not support it. The school's sections date to "
  "1948, 1963, and 1964, an older building, like much of the district. The state-approved District Facility Plan "
  "(adopted with Kentucky Board of Education approval in 2021) classifies North Middletown as a <b>permanent</b> "
  "kindergarten-through-five center with a capacity of 174, comfortably above its current 128 students. That plan, "
  "archived in this repository alongside its predecessor, prices the school's needs plainly: $317,660 of "
  "life-safety work, a $325,000 accessibility ramp and elevator, and a $3.62 million major renovation of the "
  "building's mechanical, electrical, and plumbing systems, about $4.26 million in all. The life-safety and "
  "accessibility items, $642,660 together, sit within the 2022-24 biennium schedule; the $3.62 million major "
  "renovation is scheduled <b>after</b> it. The biennium's headline priority was the $6.66 million high school "
  "Career and Technical Center. The district-wide capital need it assesses is roughly $43.4 million, concentrated "
  "at the high school and middle school, not at North Middletown.")
H2("What the district's own facility plans show")
P("The prior facility plan, approved by the Kentucky Board of Education in June 2013 and recovered from the "
  "Internet Archive's captures of the state's own posting, settles what earlier versions of this report could "
  "only infer. Both plans are archived in this repository.")
tbl(["School", "2013 plan: enrolled / capacity", "2021 plan: enrolled / capacity", "Today"],
    [["North Middletown Elementary", "169 / 198", "161 / 174", "128 enrolled"],
     ["Cane Ridge Elementary", "461 / 500", "480 / 422", "453 enrolled, 31 over its rating"],
     ["Bourbon Central Elementary", "602 / 564", "535 / 521", "459 enrolled, 62 open at its approved 521"],
     ["Preschool/Head Start Center", "296 / 180", "272 / 200", "over capacity in both plans"]],
    [1.9 * inch, 1.7 * inch, 1.7 * inch, 1.4 * inch],
    caption="Enrollment and rated capacity in the district's two most recent state-approved facility plans "
            "(KBE June 2013 and KBE August 2021; both archived under build/ in this report's repository), with "
            "current 2024-25 enrollment. Bourbon Central's approved rating is 521; the plan's 549 is a contingent To-Become figure tied to an expansion never built, per its own "
            "2021 plan. The reading order, enrollment first, is confirmed by the 2021 plan's "
            "own preschool note (272 = 80 full-day plus 192 half-day students).",
    bold_first_col=True)
P("Three facts fall out of that table. First, the rated capacity of North Middletown was written down from 198 "
  "to 174 between the two plans, while the same 1948 and 1964 walls held 261 students at the 1988-89 peak. The "
  "write-down was not unique: Cane Ridge fell from 500 to 422 and Bourbon Central from 564 to 521. What changes "
  "a rated capacity under the state's facilities planning manual (702 KAR 4:180, unamended since 2008 and "
  "re-certified by the state as recently as March 2025) is how rooms are counted: elementary capacity is the "
  "number of standard classrooms in the district's own room inventory times a cap set by room size (25, 22, or "
  "20 students), with no utilization discount, so every room relabeled from standard classroom to preschool, "
  "intervention, special education services, or a "
  "computer lab lowers the official number without a brick moving. The manual itself says the quiet part "
  "aloud, twice: “Different use of the facility spaces shall not reduce the capacity of the facility” "
  "(sections 302.2.2 and 302.3.1). Rated capacity is a number the "
  "district sets through its own room assignments and planning submissions, and it can be raised the "
  "same way it was lowered. That cuts against the "
  "closure case: if room assignments can be re-rated to make space for 128 more children in Paris, the same "
  "pencil can raise North Middletown's rating back toward the 198 it carried in 2013, or toward the 261 the "
  "building has actually held, and every seat restored there can be filled with revenue-bearing students "
  "rather than vacated. The room-by-room worksheets behind "
  "each rating, and the intermediate 2017-cycle plan, remain requested in Appendix B. Second, as recently as the "
  "2021 plan North Middletown stood at 161 students against its rating of 174: <b>93 percent full</b>. The "
  "“half-empty school” is four years old, not a generation old, and its window coincides with the "
  "district-wide attendance decline after the pandemic. Third, the 2013 plan classified North Middletown as "
  "permanent, with a long-range plan to reorganize it as a grade-band center, and the 2021 plan classified it as "
  "permanent with no change proposed at all. The transitional label in the 2026 draft is a reversal of two "
  "consecutive state-approved plans, which is precisely why the community is entitled to the analysis behind it.")
P("The 2026 planning cycle sharpens the point to a fine edge. The draft plan presented at the July 15 forum, an "
  "annotated attendee copy of which is archived in this repository, carries no KDE approval date yet and re-rates "
  "the same buildings again, this time on the state facilities inventory (KFICS) basis: Cane Ridge rises from 422 "
  "to 547 and Bourbon Central to 640, while North Middletown falls again, from 174 to 154. The draft's own "
  "new-construction sections read <b>None</b>, so not one of those 216 new paper seats at the receiving schools "
  "comes from a brick. Ratings that can move 125 seats in a single planning cycle are policy, not walls. That "
  "has been the point all along. Two more details sit on the same page: even at its reduced 154 "
  "rating, North Middletown stands 83 percent full today, and the draft as presented that day, before the "
  "committee's amendment, still listed the school as <b>permanent</b>. Its headline capital priority is an $18.6 "
  "million major renovation of the high school's 1968 and 1981 sections, the same direction the two approved "
  "plans already show.")
P("The investment record runs alongside. The 2013 plan priced a $1.92 million major renovation for North "
  "Middletown: a security vestibule, enlarged music and computer classrooms, media center and kitchen, gymnasium "
  "upgrades, new flooring, window and door replacement, electrical upgrades, and HVAC replacement. The 2021 plan "
  "prices much of the same scope again, higher, at $4.26 million all told, with the major renovation again "
  "scheduled after the biennium. "
  "Whether any of the 2013-priced work was ever completed is exactly what the maintenance and project records "
  "requested in Appendix B would show. A fair question for the administration follows: when the same needs are "
  "priced in two consecutive plans, eight years apart, and the capital program builds elsewhere both times, at "
  "what point does deferred investment itself become the closure case?")
P("The KFICS Facilities Assessment prepared by RossTarrant Architects, presented in slides at the July meeting, "
  "is archived in this repository. North Middletown's total need is <b>$8,530,093</b>: $5,648,434 of building "
  "condition work (exterior walls, windows, electrical service, water distribution) plus $2,881,659 of "
  "instructional-space items. That is the <b>second lowest</b> of the district's schools. The two receiving "
  "schools need $23.2 million combined, $8,840,267 at Bourbon Central and $14,387,595 at Cane Ridge, a 1992 "
  "building needing two thirds more than the 1948 one proposed for closure. The high school needs $27.5 million, "
  "the middle school $22.4 million, and the districtwide total is <b>$98,441,294</b>, more than four times the "
  "unused bonding capacity in Section 6. Closing the second-least-needy building avoids $8.5 million of "
  "restricted-fund need, moves its children into buildings needing $23.2 million, and does nothing about a $98 "
  "million problem. The full report behind the slides remains unpublished and is requested in Appendix B. Two "
  "points bound the building question. Any renovation would be paid from the restricted facility funds described "
  "in Section 6, which cannot close the operating deficit either way. And the receiving schools have little room: "
  "approved ratings are 521 at Bourbon Central and 422 at Cane Ridge, so at today's 459 and 453 there are 90 "
  "seats open at Bourbon Central and Cane Ridge sits 31 <b>over</b> its rating, a net 31 uncommitted seats for "
  "128 children. If the answer is that ratings can be adjusted by room assignment, the same adjustment raises "
  "North Middletown's capacity instead. The 2026 draft adds 244 paper seats in Paris and subtracts 20 at North "
  "Middletown with no construction in it. The architect's slides print a third set, 499 and 397, at which the "
  "receiving schools have <b>negative</b> net room. Under every printed set: 31 uncommitted at the approved 521 "
  "and 422; 59 only under the 2021 plan's contingent 549, a To-Become rating tied to an expansion never built; "
  "minus 16 at the architect's 499 and 397. Only the draft's 640 and 547 produces room. An empty building is also "
  "not free: it must be secured, insured, minimally heated and eventually disposed of, in a town of about 610 "
  "people whose residents told the planning committee the school is the heartbeat of the town.")

H2("The state's own condition index: the district's best-trending building")
P("The architect's slides are one reading of the building. The state publishes its own, and it is stronger. "
  "Kentucky's facilities inventory system (KFICS) assigns every public school building a Condition Index, "
  "defined in the state reports as one minus the ratio of repairs coming due within four years to the cost of "
  "replacing the building outright, so a higher number means a healthier building. KDE has published exactly "
  "three statewide reports: the official October 2023 report, the official October 2025 report (both resting "
  "on inspections done in 2020 and early 2021, with costs updated between them), and an updated report "
  "generated July 2, 2026 that carries the first fresh inspections, completed in April 2026 by the district's "
  "own third-party architect and reviewed by KDE. Figure 14 plots every number the state has ever published "
  "for the three elementary schools.")
fig("chart_condition.png",
    "Figure 14. The KFICS Condition Index for Bourbon County's three elementary schools in every statewide "
    "report the state has published: October 2023 official, October 2025 official, and the July 2, 2026 "
    "update. The 2023 and 2025 reports rest on the same 2020-21 inspections; the July 2026 report is the "
    "first with fresh April 2026 inspections. Source: KDE, KFICS State Reports, downloadable from the "
    "department's facilities pages and archived under build/ in this repository; Bourbon County is "
    "district 041.")
P("Three findings sit in that figure. First, in the newest KDE-reviewed data, North Middletown's condition index "
  "is <b>0.773</b>: better than Cane Ridge (0.728), within six points of Bourbon Central (0.823), and far ahead "
  "of the middle school (0.596), the district's other 1948 building. Second, North Middletown is the <b>only "
  "school in the district whose condition improved</b> between the 2020-21 and April 2026 inspection cycles, from "
  "0.694 to 0.773, while every other school's index fell or held: the repairs coming due within four years at "
  "NMES dropped from about $4.1 million to <b>$3.1 million, the smallest four-year repair bill of the district's "
  "five schools</b>. Cane Ridge, a 1992 building, moved the other way, from 0.812 to 0.728 with a $4.8 million "
  "four-year bill. Third, the numbers reconcile with the architect's own $8.5 million total-need figure for NMES "
  "quoted above: that larger total includes longer-horizon work and $2.9 million of instructional-space items, "
  "while the condition index counts what is actually due within four years. On either reading NMES is near the "
  "bottom of the district's need list. One caveat belongs in the record, and it favors caution rather than the "
  "closure case: NMES's Educational Suitability score, the separate survey of how well the 1948 layout matches "
  "modern program standards, prints 0.21725 in the July 2026 report, identical to five decimal places to the 2023 "
  "report, so that half of the aggregate score appears to have been carried forward rather than re-surveyed in "
  "April 2026 even as the condition half was refreshed. On the state's newest published data the building the "
  "draft plan proposes to close is the only one in the district whose condition improved, carries the smallest "
  "near-term repair bill of the five, and scores above a receiving school 44 years its junior.")

# ================= 8. ADMIN =================
H("8. Where the Money Is Actually Going: Administrative Growth", need=4.3)
fig("chart_admin.png",
    "Figure 15. Administration expense from the district's audited statements of activities. District (central "
    "office) administration grew from $999,727 in FY2023 to $1,447,164 in FY2025; school administration grew from "
    "$2,110,039 to $2,581,412 over the same two years.")
P("The biggest cost jump in the audits, and one the district controls, is not at North Middletown. Central-office "
  "administration grew 44.8 percent in two years, an increase of $447,000 a year, as much as or more than"
  "any realistic net saving from closing the school, while enrollment and attendance fell. School-level "
  "administration grew 22.3 percent. Transportation grew 20.3 percent in fiscal 2025 alone, alongside bus purchases "
  "of roughly $888,000 and $691,000 in consecutive years. Single-year jumps can carry one-time costs, so the "
  "fair question is the multi-year trend and the routing, not any one invoice. Federal data most recently on "
  "file show the district "
  "reporting four central-office administrators and fifteen school administrators; matching that headcount "
  "against the dollar growth, position by position, is a fair thing to ask before any classroom building closes.")
P("A caution belongs beside that number: functional expense lines in Kentucky school audits include allocated "
  "state pension payments made on the district's behalf, and reclassifications between categories can move money "
  "on paper without a single new hire. Some share of the 44.8 percent may be accounting rather than "
  "administration. That is the reason for asking for a position-by-position accounting rather than assuming the "
  "worst.")
H2("What the 44.8 percent is actually made of")
P("The district produced its FY2024, FY2025 and FY2026 working budgets in July 2026, and this section is the "
  "result of reading them line by line. The 44.8 percent is real and it cross-validates: district administration "
  "on the MUNIS ledger grows by a very similar amount on a different two-year window, two independent documents "
  "agreeing within about two and a half percent. What they disagree with is the story told about it, including in "
  "earlier versions of this report.")
P("<b>Administrative salaries went down, not up.</b> Over the window the ledger covers, salaries in the "
  "district administration function fall about 8 percent. The growth sits in four non-salary lines. Insurance, "
  "meaning property, liability and general coverage, roughly doubled, which is a regional market cost rather "
  "than a hiring decision. Tax collection fees under object 0311 are statutory: the sheriff and the county "
  "clerk are paid a percentage of what they collect, so the line rises when assessments rise. Accrued sick "
  "leave paid at retirement, object 0291, is a Kentucky benefit that lets a retiring employee convert unused "
  "sick leave to a lump sum, and it is coded to central office because that is where payroll clears, not "
  "because central office grew; it is a retirement cost for staff across the district. Purchased professional "
  "and technical services covers legal, audit, architect and consulting work, including this facility planning "
  "cycle itself.")
P("The number that matters most runs against the way this increase is usually described. <b>Total district "
  "payroll fell</b>, from $30,410,725 to $30,201,047 across the two most recent years in the district's own "
  "payroll reports, down 0.7 percent. The district as a whole did not get bigger.")
P("What did grow is narrower, and every word of it is defensible. Board and central office payroll, location "
  "001, rose 25.6 percent. That headline is misleading and this report will not use it: $187,623 of the "
  "$248,611 increase is the sick-leave and on-behalf program described above, which is not ongoing salary. "
  "Setting that program aside, <b>central office payroll still grew 7.6 percent in a year when total district "
  "payroll fell 0.7 percent.</b> That is the fair comparison. The remaining increase is $60,988, and it is two "
  "offices moving in opposite directions: the business office up $114,295, the superintendent's office down "
  "$53,307, netting to exactly $60,988. Every other central office program is flat in total.")
P("Three findings run against the assumption this report started from. First, <b>the records do not show the "
  "district adding net administrative positions.</b> Twenty-two months of board agendas contain two director- "
  "level structural actions and both go the other way: on December 3, 2024 the board combined the Finance Officer "
  "and Food Service Director roles, and on May 15, 2025 it combined the Director of Pupil Personnel and the "
  "Director of Elementary Continuous Improvement into one position. Those are consolidations. Second, <b>neither "
  "the salary schedules nor the payroll report can answer the question.</b> In all three years the published "
  "schedules name no senior certified administrator at all: no line, no dollar figure, no day count for "
  "superintendent, assistant superintendent, or any director. Central office pay is a responsibility index times "
  "the teacher base over 185 days, and the payroll report carries dollars rather than headcount, so it cannot "
  "separate one more person from the same people paid more. Third, <b>there is one real documented addition and "
  "it is below director level</b>: the schedule added a Childcare Director line and a Migrant Advocate and "
  "Recruiter Coordinator line, and widened the assistant principal index so that schools of 400 to 500 pupils "
  "qualify for an indexed assistant principal where the FY2023-24 table started at 501; on July 16, 2026 the "
  "board added elementary assistant principals to the extended days table and noted they were not currently "
  "reflected on the schedule, which means people already hold those jobs.")
P("So the ask changes shape. The right question is not who was hired. It is that <b>the cost growth cited as a "
  "reason to close a school is concentrated in insurance, statutory fees, retirement payouts and professional "
  "services, and the district has never published a position-by-position administrative roster with titles, FTE "
  "and salary that would let anyone check the rest.</b> Until it exists, nobody outside the central office can "
  "answer this question.")
P("I deliberately rely on the audited totals rather than individual salaries, because individual figures should "
  "come from official records: the Kentucky Department of Education's annual superintendent salary file and the "
  "district's own board-adopted administrator salary schedule, which sets pay by formula, a base teacher salary "
  "multiplied by a responsibility increment and an extended work year. Those records, current and for the past "
  "five years, are requested in Section 10.")

# ================= 9. ALTERNATIVES =================
H("9. The Alternatives on the Table: Grow, Don't Close")
P("Every option below is available under current Kentucky law, and each comes with the question the "
  "administration should answer about it. Dollar values are planning estimates from the audited base figures, "
  "labeled as such; several overlap and cannot simply be summed. Even conservatively combined, they exceed both "
  "the realistic saving from closure and the district's annual reserve drawdown. The first revenue option is a "
  "tax adjustment; the full rate analysis follows the menu and shows a district taxing near the bottom of its "
  "region.")
H2("First among them: grow the Kings into the region's premier elementary school")
P("The strongest alternative is not defensive. Kentucky law already gives the district a way to grow: under House "
  "Bill 563 (2021), codified at KRS 157.350, a district that adopts a nonresident-student policy may, since July "
  "2022, enroll students from other counties and count them in its attendance for state SEEK funding, with no "
  "agreement from the child's home district required and tuition at the board's discretion. Every family North "
  "Middletown attracts brings at least the $4,626 base guarantee (fiscal 2027), plus applicable add-ons.")
P("North Middletown is built to compete for those families. It is a 2011 National Blue Ribbon school with a "
  "gifted-and-talented program, a 13.6-to-1 student-teacher ratio, state results that lead every elementary "
  "school in Bourbon County in every state-reported subject, and a third-party index that also tops every school in "
  "neighboring Clark County and Paris Independent "
  "(Conkwright 17.5, Strode Station 34.2, Justice 39.3, Shearer 42.3, Paris Elementary 12.2). Its state-approved "
  "capacity is 174 against 128 enrolled: forty-six open seats which, filled with transfer students at the base "
  "guarantee alone, represent roughly $213,000 a year of new recurring revenue gross, about $194,000 after supplies and about $134,000 if they require the added section this version prices, before "
  "tuition, add-ons, or the further growth a signature program (advanced learners is one natural fit), a preschool satellite, and a serious marketing effort "
  "could generate along the U.S. 460 corridor, within a short drive of five surrounding counties. The question for "
  "the administration is why the district's only nationally honored school is proposed for reclassification instead of "
  "expansion.")
P("Honesty requires naming the headwind first. Bourbon County has hovered near twenty thousand residents for "
  "more than fifty years, from 18,476 in 1970 to 20,252 in 2020, and the Kentucky State Data Center projects a "
  "decline of roughly four percent by 2040. The county is aging, its share of children is shrinking, and its "
  "celebrated horse-farm land base, the second largest stock of conserved farmland in Kentucky, structurally "
  "limits new subdivisions. The regional boom passed to the west: neighboring Scott County is projected to grow "
  "46 percent by 2050 and Fayette nearly ten, while Bourbon sits outside that corridor. The district's enrollment "
  "decline is real and structural, and I will not pretend otherwise. North Middletown Elementary itself "
  "tells the story: it held 261 children in 1988-89, about double today's 128 (Figure 16).")
P("But a school's enrollment does not have to wait on a county's birth rate, because the board controls two "
  "levers that demographics do not. The first is redistricting: attendance boundaries are the board's to draw, "
  "and with Bourbon Central at 459 students and Cane Ridge at 453 while the district's best elementary sits at "
  "128 of a rated 174, redrawing lines on the eastern side of the current zones, starting with families who "
  "already live closer to North Middletown than to their assigned school, would fill its open seats with children "
  "the district already educates, relieve the crowded Paris schools, and shorten those children's rides rather "
  "than lengthen them. The second is the county's edges: under House Bill 563, families just across the line in "
  "Clark, Nicholas, Bath, and Harrison counties can enroll at North Middletown and bring their state funding with "
  "them, and on the third-party index used for outside context every nearby comparison school with a published "
  "score sits below it, from Nicholas County Elementary near 16 and Conkwright at 17.5 to Strode Station at 34.2. "
  "The pitch is not that the region is growing. It is that a school with the county's top state-reported results "
  "has empty seats within a short drive of families in four counties.")
P("The seats deserve a destination, not just a headcount, and the school already holds the ingredients: a "
  "National Blue Ribbon history, the county's top results on the state's 2024-25 assessments, an existing gifted- "
  "and-talented program, and open seats no other school in the area can offer. Build on them and North Middletown "
  "becomes the region's premier elementary. One natural path, though not the only one, is a specialized program "
  "for advanced learners that families apply into from across the district and, under House Bill 563, from the "
  "surrounding counties; Kentucky's larger districts have run magnet and specialized-program schools for decades "
  "precisely because a distinctive program pulls enrollment to the building that hosts it. A preschool satellite, "
  "or simply growing the neighborhood school it has always been, would serve the same end. Under any of them, "
  "every child in the zone keeps their seat; the program adds students, it never displaces one. A district that "
  "needs students has reason to run a growth play at the school best credentialed to anchor it.")
P("Framed this way, growth means moving and recruiting students on the strength of a good school, not betting on a population rebound, and "
  "the near-term target is modest: returning to the 160 students the school enrolled as recently as 2019-20 "
  "takes just 32 children from a district of 2,600 and four neighboring counties.")
fig("chart_enroll.png",
    "Figure 16. NMES enrollment from 1989 through 2025 against its current state-rated capacity of 174. The "
    "school held 261 students at its 1988-89 peak, roughly double today's official count of 128. History "
    "compiled from federal school-level data. The long decline mirrors the county's flat population, which is "
    "exactly why this plan relies on boundary decisions and cross-county enrollment rather than demographics.",
    width=6.1 * inch)
P("The decline itself deserves questions, not just measurement, because its milestones track the district's "
  "own planning documents: 261 at the 1988-89 peak, 169 in the 2013 facility plan, 161 in the 2021 plan, 128 "
  "today. The town did not empty out; North Middletown holds about 610 people and the zone's boundaries are "
  "unchanged in the federal record since at least 2015-16. Over the same years the district centralized "
  "preschool at the Paris center, so many zone families now start their school lives in Paris; the renovation "
  "priced for the building in 2013 reappears in the 2021 plan, priced higher; the rated capacity was written "
  "down from 198 to 174; and no public recruitment or transfer program has marketed the county's highest-scoring "
  "elementary to anyone. Each of those is a district decision, not a demographic fact, and the records "
  "requested in Appendix B would show how much of the decline they explain. A school that stood 93 percent "
  "full against its rating in the 2021 plan did not become surplus in four years by itself.")
H2("A worked example: rebalance the map, fill the school")
P("One scenario, run in the workbook's Redistricting tab. Rezone 30 students to North Middletown from the "
  "adjacent edges of the Cane Ridge and Bourbon Central zones, drawing only from families who already live closer "
  "to North Middletown than to their assigned school, and recruit 16 cross-county transfers under House Bill 563. "
  "The school reaches exactly its rated 174; Bourbon Central eases from 459 to about 444 and Cane Ridge from 453 "
  "to about 438. A correction this report makes against its own case: earlier versions assumed no teacher is "
  "added at North Middletown, because nine sections average about 19 students at 174. The class caps (KRS "
  "157.360: 24 in primary through grade 3, 28 in grade 4, 29 in grade 5) bind grade by grade, not on average, so "
  "46 arrivals likely require one new section, possibly two if they lump in the wrong grades and possibly none if "
  "the rezone is drawn grade-by-grade. The planner carries that lever at the same $60,000 General Fund rate this "
  "report applies to eliminated positions. The 16 transfers bring roughly $74,000 a year of new SEEK revenue, "
  "supplies for all 46 added students cost about $18,000, and with one added section against one to two avoided "
  "at the receiving schools the package is worth roughly <b>$56,000 to $116,000 a year, recurring</b>, down from "
  "the $116,000 to $176,000 published before this correction; across the two section sliders it runs from minus "
  "$64,000 to $176,000. The move cuts North Middletown's much-cited cost per student from $19,348 to about "
  "$14,827 with the added section ($14,339 without, $15,316 with two), purely by filling seats. Two assumptions "
  "are flagged in yellow in the workbook for the district to replace with real data: that rezoned students' bus "
  "routes shorten or hold because they are chosen by proximity, and the receiving schools' grade-by-grade "
  "capacities, already a records ask in Question 3. The district holds the geocoded student counts and routing "
  "data to run the full version, and it should, before any vote.")
fig("chart_balance.png",
    "Figure 17. One rebalancing scenario: North Middletown fills to its rated 174 while Bourbon Central and Cane "
    "Ridge each ease by about fifteen students. Dashed lines mark each school's rated capacity "
    "(174, 521, 422); Cane Ridge enrolls above its rating today and remains above it even "
    "rebalanced, which is the receiving-capacity problem closure would compound. The scenario levers (30 "
    "rezoned, 16 cross-county transfers) are adjustable in the companion workbook's Redistricting tab.", width=6.0 * inch)

H2("The children never left the county")
P("The case for closing a school starts with a premise: there are fewer children. Checked against exact counts, "
  "the premise is false. The decennial census counts every child rather than sampling them, and children aged 5 "
  "to 17 in Bourbon County number <b>3,594 in 2000, 3,574 in 2010 and 3,548 in 2020</b>, a change of 1.3 percent "
  "across twenty-five years. The Census Bureau's separate annual school-age estimates agree, moving from about "
  "3,400 in 2014 to about 3,491 in 2023. There is no demographic decline story available here.")
P("The enrollment is a different matter, and these are federal fall counts rather than estimates. The two "
  "county districts together held <b>3,708 students in fall 2019 and 3,428 in fall 2022</b>. Bourbon County "
  "Schools alone went from 2,912 in 2014 to 2,616 in 2023, down 10.2 percent, while the county's children "
  "moved four tenths of one percent. The elementary grades fell 16.5 percent from their 2016 peak, 1,245 to "
  "1,040. The break is neither gradual nor a birth-rate story: it begins after 2019.")
P("Three cautions belong beside that finding. The Census counts homeschooling inside private school, because "
  "its questionnaire offers private school, private college or home school as a single answer, so the category "
  "can never be labeled private alone. Bourbon does not stand alone, and this report will not claim it does: "
  "the move away from public school after 2019 is regional, with registered homeschooling up 139 percent in "
  "Harrison County and 112 percent in Fayette over comparable windows and roughly 1,200 new private seats "
  "opened within a twenty-five minute drive, and measured as attendance against child population, Nicholas, "
  "Bath and Montgomery show gaps as large or larger. And survey vintages from 2022 and 2023 carry pandemic "
  "weighting caveats, so the year-to-year points move more than the underlying reality does. What is specific "
  "to Bourbon is the combination: a flat child population, a double-digit enrollment decline, and a district "
  "responding by removing a school rather than competing for the children who are still here.")
P("Every one of those children is a Bourbon County child whose family already chose something else, and the state "
  "pays $4,626 for each one who returns. Filling North Middletown's 46 open seats requires winning back fewer "
  "than one in ten of them.")
H2("Where the students come from: the pool is measured, and it is large")
P("The students are not hypothetical, and the public record measures the pool three ways, all archived here. "
  "First, the districts' own records: Kentucky homeschool families must file a letter of intent with the local "
  "superintendent (KRS 159.160), and the counts the districts reported, collected by the Washington Post's "
  "records project, show <b>236 registered homeschool students in the Bourbon County district and 23 in Paris "
  "Independent</b> in 2022-23, about 259 in all, up roughly half since 2018-19. Compliance with the filing "
  "statute is incomplete, so that is a floor. Second, the Census: the American Community Survey counts private "
  "school and homeschooling as one combined answer, and shows that group roughly doubling since the 2014-2018 "
  "window. An earlier version of this report put it at about one in three of the county's school-age children "
  "from the survey alone. That was too high. Reconciling the district rosters, the census counts and the state's "
  "non-resident file gives <b>about 450 to 550 children, roughly 13 to 15 percent</b>, in private school or "
  "homeschooling, against nearer one in eleven a decade ago. The survey figure is inflated by one age band: "
  "children 10 to 14 jump from 210 to 580 in a year and print 41 percent non-public against 11.6 percent for the "
  "pooled neighboring counties in the same band, while the 5 to 9 band barely moves. A real shift moves all three "
  "bands, so that is a small-sample weighting artifact. St. Mary in Paris, the county's only private school, "
  "enrolls 96 students in the federal Private School Survey, so most of the group is homeschooling or commuting "
  "outside the county. Third, the state: KDE's Non-Resident Student report for 2024-25 shows this district "
  "already <b>wins</b> the competition it is in, with 436 nonresident students enrolled here (305 Paris "
  "Independent residents plus 131 from out of county, <b>including 54 from Fayette County</b>) against 247 "
  "residents enrolled elsewhere, a net import of 189. Only 76 county-district residents attend an out-of-county "
  "public school, ten of them at Cloverport Independent, 150 miles away, which hosts the statewide virtual "
  "academy.")
P("The revenue side is symmetric with the closure math in Section 4, on purpose, using the same $4,626 SEEK "
  "base cell in the workbook. A homeschool or private-school student generates no state funding for the "
  "district today, so each one who enrolls is entirely new money: about $4,226 net of supplies. Filling all "
  "46 open seats at the rated 174 from this pool alone is worth about <b>$213,000 a year gross, roughly "
  "$134,000 to $194,000 net of supplies and the zero to one new section the v3.8 correction prices</b>, and "
  "requires fewer than one in five of the registered homeschoolers, or about one in twenty-five of the "
  "Census pool. The fill planner on the site and the Redistricting tab now carry a returning-student lever "
  "alongside the rezone and transfer levers, capped together at the 70 seats between today's enrollment and "
  "the 198 rating the state approved in 2013, and set to zero by "
  "default so the $56,000 to $116,000 package above claims nothing from it. What would move these families "
  "is not a mystery either: the county's top test scores, the state's best-trending building, and small "
  "classes are precisely the product homeschool and private-school families shopped for when they left. Two "
  "records asks sharpen this: the letter-of-intent counts by year at both districts, which are public "
  "records, and the school-level split of the 131 out-of-county students already here. Closing the school "
  "with the open seats forfeits the one asset this recruitment case runs on.")

H2("The transportation map, drawn from the official boundaries")
P("The zone geometry here is official: the federal School Attendance Boundary Survey (2015-16, the last "
  "national collection) published the district's actual attendance boundaries, and this report draws them "
  "directly. The district has still not published its geocoded student counts or its annual T-1 "
  "transportation report, so the cost inputs sit in yellow in the workbook's Transport_Geo tab. Bourbon County is about 290 square miles "
  "of land. Its people cluster west: Paris holds 10,171 of the county's 20,252 residents, against 747 in "
  "Millersburg and 610 in North Middletown. The federal boundary file settles the map: North Middletown's "
  "zone covers 110 square miles, 38 percent of the county, Cane Ridge serves the north including "
  "Millersburg, and Bourbon Central the southwest. The math follows: about 1.2 elementary students per square "
  "mile in the NMES zone, against roughly 5.1 across the two Paris-based schools' zones and 3.6 district-wide. That density gap is "
  "not a detail; it is the exact variable state law funds on. KRS 157.370 sets transportation aid by "
  "transported pupils per square mile, paying more where density is low because low density costs more to "
  "serve. The funding history sharpens the point: the formula ran underfunded for two decades, the 2024-2026 "
  "state budget restored it to 90 and then 100 percent, computed on lagged fiscal 2023 costs, and the "
  "2026-2028 budget froze it again below the statute. A district that closes its one eastern school keeps "
  "every square mile of that coverage area and serves it with longer rides.")
tbl(["Zone", "Approx. area (sq mi)", "Elementary students", "Students per sq mi"],
    [["North Middletown zone (southeast)", "110", "128", "~1.2"],
     ["Cane Ridge zone (north)", "120", "453", "~3.8"],
     ["Bourbon Central zone (southwest)", "59", "459", "~7.8"],
     ["District overall", "289", "1,040", "3.6"]],
    [2.6 * inch, 1.35 * inch, 1.45 * inch, 1.3 * inch],
    caption="Official zone areas from the federal School Attendance Boundary Survey (2015-16 collection); "
            "students shown are each school's cited enrollment, the closest public proxy for zone residents. The vintage is the caveat: the district should confirm nothing has moved since (Appendix B).",
    bold_first_col=True)
fig("chart_map.png",
    "Figure 18. Where the students are: the district's official attendance zones from the federal School "
    "Attendance Boundary Survey (2015-16 collection), fetched by the repository's build/fetch_sabs.py. Paris "
    "holds half the county's people and both receiving schools; Millersburg sits in Cane Ridge's northern "
    "zone; the NMES zone runs about 1.2 students per square mile across 110 square miles of the southeast.", width=5.2 * inch)
P("Now the closure math, from the bottom up, with the distances measured on the official zone geometry "
  "rather than assumed (the workbook's Transport_Geo tab and build/zone_distances.py carry the computation). "
  "North Middletown sits ten road miles from the Paris schools on US "
  "460, against 8.9 miles straight-line, a road factor of 1.13 on the one pair that can be measured exactly; "
  "a conservative 1.2 is applied everywhere else. Roughly 109 of the school's 128 students ride the bus on an estimated three rural routes. Extend "
  "those routes to Paris and each one adds about 40 bus-miles a day, out and back, morning and afternoon: "
  "about 20,400 added bus-miles a year. At a marginal cost of $2.50 to $4.50 per bus-mile that is $51,000 to "
  "$92,000 a year, and if the longer runs break the route tiering and force even one additional bus, add "
  "roughly $55,000 more. The bottom-up estimate therefore lands at about $51,000 to $147,000, squarely inside "
  "the $75,000 to $200,000 planning range this report has used from the start, and it validates the $137,500 "
  "midpoint in the closure model. The geometry also prices the quieter cost. Averaged over the zone's "
  "area, closure adds an estimated 4 road miles each way to a child's trip. At the far corner, near the Nicholas "
  "County line, a kindergartner who today rides about 10 road miles to North Middletown would ride about 18 "
  "to Paris, roughly 15 to 20 added minutes each way at rural bus speeds. And 78 percent of the zone's area "
  "lies closer to North Middletown than to Paris, which is the whole map's point in a single number.")
P("Run the same math on the rebalancing scenario and the sign flips. Rezoned students already ride district buses "
  "today, ten miles west to the Paris schools; rezoning moves them to the school they live closest to, so the "
  "affected routes shorten, an estimated $10,000 to $18,000 a year saved (each rezoned student cutting about 136 "
  "bus-miles a year at $2.50 to $4.50 a mile, an estimate the district's T-1 route data would replace). On this "
  "geometry rebalancing is transport-neutral at worst and modestly positive at best, while closure adds miles. "
  "District-wide, the optimization lever in the menu below, routing software, tiered bells, and a right-sized "
  "fleet, remains worth 5 to 10 percent of the $2.9 million line, $145,000 to $290,000 a year, whichever way the "
  "boundary question is decided.")
P("The state-revenue side runs the same way. Because the 2026-2028 appropriation is frozen at flat dollars "
  "computed on old costs, the marginal state reimbursement on any NEW busing mile is zero: every dollar of "
  "closure's added routes is district money. Rebalancing changes no transported-pupil count, so the district's "
  "KRS 157.370 allotment is untouched, and its SEEK revenue is untouched because the same students attend the "
  "same district. Cross-county transfer students add SEEK revenue while adding no required busing at all: under "
  "KRS 157.350 the receiving district sets its own transportation policy for nonresident students, and most "
  "Kentucky districts have families drive or meet routes at the county line. On this math redistricting does not "
  "raise transportation costs; it trims them, while the revenue side gains.")
H2("How a real optimization would run, and who already runs them")
P("None of this requires inventing anything. The method is standard: geocode enrolled students from the student "
  "information system; aggregate to small planning zones; build a travel-time matrix from each zone to each "
  "school on the actual road network; then assign zones to schools to minimize total ride time, subject to "
  "building capacities, statutory class sizes, and keeping neighborhoods together, with bus routes re-optimized "
  "afterward. Kentucky districts already do this. Fayette County convenes boundary working groups over GIS "
  "scenarios whenever it opens or rebalances schools, and publishes the maps; Jefferson County publishes its "
  "assignment boundary documents and has contracted route-optimization modeling. Every district, Bourbon County "
  "included, already files the T-1 annual transportation report and keeps the address data the analysis needs. "
  "The tools are commodity software; the working group is a policy choice. A district facing a closure vote over "
  "money owes the public this study first, and the workbook's Transport_Geo and Redistricting tabs are built to "
  "receive its outputs.")
P("The savings from doing this well are documented, not hypothetical. Boston Public Schools ran the "
  "signature version in 2017: an MIT-built routing algorithm produced bus routes 20 percent more efficient "
  "than the hand-built ones, cut 50 buses, about 8 percent of the fleet, eliminated a million bus-miles in "
  "the first year, and saved roughly $5 million that the district returned to classrooms. Bourbon County's "
  "transportation line is $2.9 million; the 5 to 10 percent captured in the menu below is $145,000 to "
  "$290,000 a year, and Boston's 20 percent shows the ceiling sits higher than the menu assumes. One more "
  "check anyone can run without waiting on the district: the federal School Attendance Boundary Survey "
  "(NCES EDGE) published the district's actual attendance-zone boundaries as free GIS files in its 2015-16 "
  "collection, and NCES publishes geocoded school locations. Figure 18 is drawn directly from that file, "
  "fetched by the repository's build/fetch_sabs.py, so anyone can reproduce it in one step. Appendix B lists the datasets alongside the records "
  "only the district can produce.")
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
     ["Energy performance contracting",
      "10-25% of utility spend",
      "State regulation (702 KAR 4:160) authorizes contracts in which guaranteed energy savings pay for the "
      "upgrades. No such contract is currently in place district-wide."],
     ["District-wide recruitment beyond North Middletown's seats",
      "$106,000 to $211,000",
      "Priced in v3.8: 25 to 50 additional students at $4,226 net each. State funding follows students who "
      "transfer in; the measured pool (259 registered homeschoolers, a Census pool near one in three county "
      "children, a nonresident market the district already wins) is in Section 9, and 62 open seats exist at "
      "Bourbon Central's approved rating. Growth, not shrinkage, is the durable fix for a small-district "
      "budget."],
     ["Shared services with Paris Independent",
      "$100,000-$300,000",
      "Two school districts operate in one small county. Shared transportation, food service, and back-office "
      "functions deserve a serious, public study."],
     ["Fill North Middletown to capacity instead of closing it",
      "$56,000 to $116,000 net, recurring",
      "Rebalance eastern attendance boundaries and recruit cross-county transfers under House Bill 563 to fill "
      "all 46 open seats; the worked example above and the workbook's Redistricting tab show the math. "
      "A preschool or day-care satellite is an additional lever on top."]],
    [1.75 * inch, 1.35 * inch, 3.6 * inch],
    caption="Figure 19. Measures available without closing a school. The menu deliberately mixes two kinds of lines, "
            "new recurring revenue and recurring cost reductions, and the workbook's Alternatives tab labels each one "
            "by type with a confidence rating and what would firm it up. Values are estimates derived from the "
            "district's audited figures and state data; ranges overlap and are not additive to the penny. The "
            "rows sum to roughly $1.5 to $2.6 million raw; the published $1.0 to $1.9 million a year applies "
            "a conservative haircut for overlap and implementation risk, against an annual reserve drawdown "
            "of $1.1 to $1.2 million.",
    bold_first_col=True)

H2("The growth path: the same menu as a district-wide recovery plan")
P("Bourbon County Schools has a structural funding problem: spending has outrun revenue at every building, "
  "salaries are hard to raise, capital projects wait, and North Middletown is being blamed for it. North "
  "Middletown is not the reason salaries cannot increase; its excess cost is about $156,000 a year against the "
  "cheaper receiving school ($121,220 on the district's own KDE-filed comparison to the peer average), six tenths "
  "of one percent of the budget. It is not the reason capital projects cannot be funded; roughly $17.6 million of "
  "restricted bonding capacity sits unused while the capital-to-operations sweep drains the building fund, and "
  "that sweep is a General Fund problem every school shares. Organized as a plan, the menu above prices out as "
  "three moves. <b>Move one, inspect fixed costs</b>: every non-teaching position district-wide trimmed by "
  "attrition, administrative restructuring considered on its own merits (the district's own audit table shows "
  "the recent growth was insurance, payouts and contracts, not new hires), transportation and energy "
  "efficiency, and shared services, worth $860,000 to $1.6 million a year. <b>Move two, grow enrollment instead of shrinking it</b>: "
  "fill North Middletown's 46 seats, recover attendance, and recruit district-wide from the measured pool of "
  "homeschool, private-school and nonresident families, worth $260,000 to $530,000 a year. <b>Move three, have "
  "the honest revenue conversation</b>: the four percent option and delinquency recovery bring $370,000 to "
  "$495,000 in year one and about $1.0 to $1.1 million by year three as the option compounds, and the recallable "
  "menu beyond four percent reaches $1.0 to $2.5 million. The three moves are the raw $1.5 to $2.6 million shown "
  "under Figure 19, cut to the published $1.0 to $1.9 million after overlap and implementation risk. Any one "
  "alone outweighs closure, whose median outcome now loses $21,971 a year. Together they balance the budget, end the sweep, free the "
  "restricted stream to bond the renovation plan, and close nothing. The Alternatives tab prices each move live.")

H2("The tax question, faced squarely")
P("The rate history strengthens rather than weakens the community's hand. Bourbon County Schools levies 52.4 "
  "cents per $100 on real estate, second lowest among nine area districts and roughly 13 cents below the "
  "statewide school average of 65.1. Fayette levies 80.9, Paris Independent, in this same county, 71.5, Clark "
  "66.8, Bath 63.4, Scott 62.9, and Harrison 57.7; only Nicholas County, at 43.1, sits lower, and Montgomery is "
  "essentially tied at 52.5 (Figure 20). The trend runs the same direction: the levied rate has fallen from 61.3 "
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
  "exposure attached. Taken on the General Fund levy of $7,829,060, the part that can actually pay teachers, that "
  "is roughly $313,000 of new recurring revenue in year one, about $639,000 a year by year two, and about $978,000 a year by "
  "year three, more than a third of the structural deficit and over four fifths of the annual reserve drawdown, "
  "from a district that would still tax below Harrison, Scott, Bath, Clark, Paris Independent, and "
  "Fayette. (The restricted building-fund levy, which cannot pay operating costs, is excluded from this base, the "
  "same restricted-funds rule this report applies to closure.) Section 12 carries the recommendation and the "
  "companion workbook carries the math. To be clear, the "
  "levy is one option, not the only one: the menu above lists other revenue and cost measures, and deeper "
  "spending reductions are always available to a board willing to make them. But the math is simple and it "
  "does not bend. Either spending comes down or revenue goes up, and a district drawing down a million "
  "dollars of reserves a year does not get to choose neither. The board and superintendent owe the public a "
  "chosen path, in writing, with the work shown. What they do not owe anyone is the closure of the district's "
  "best performing school presented as the only choice.")
fig("chart_tax.png",
    "Figure 20. Left: the Bourbon County Schools real estate rate by tax year, from Kentucky Department of "
    "Revenue rate books; years before 2018 could not be retrieved and are not interpolated. Right: current "
    "levied real estate rates across nine area districts against the statewide school average of 65.1 cents. "
    "Fayette and Clark are from local reporting of their board votes; all other rates are Department of Revenue "
    "rate book lines. Bath's bar is its 2025 rate (2024 was 60.7); Nicholas is shown at its real estate rate "
    "of 43.1 (its tangible rate is 43.7).")
P("The fourteen-year record settles how unusual this county's levy path is. KDE publishes every district's "
  "levied rates back to tax year 2012, and Figure 21 plots all nine area districts on the same axis: every "
  "neighboring district's levied rate is higher today than it was fourteen years ago, most by double-digit "
  "percentages, Bath by 72 percent. Bourbon County's is <b>5.4 percent lower</b>, the only decline in the "
  "region, falling from second highest among the nine in 2012 to seventh today. Two honesty notes belong in "
  "the reading. First, these are levied RATES: under House Bill 44 a rate can drift down while collections "
  "hold, because the compensating rate falls as assessments grow, so the chart measures the net of each "
  "board's levy choices against its assessment growth, and by that measure every other board in the region "
  "chose to keep or grow its rate while Bourbon's slid. Second, Bourbon did take the four percent revenue "
  "option in five of the last twelve years, by KDE's own levied-type file; the rate fell anyway because the "
  "other seven years took the compensating rate or less, including the twelve-cent slide from 2018 to 2022, "
  "the exact years the drawdowns began. The neighbors that rose took the four percent seven, eight, and nine "
  "times over the same window. The community that has twice declined to petition against a facilities nickel "
  "has never been asked to vote against the operating levy that pays teachers; the board simply has not "
  "levied it.")
fig("chart_levy_history.png",
    "Figure 21. Fourteen years of school levies, nine area districts, from KDE's Local District Tax Levies "
    "files (total real estate column: general fund plus all facilities levies), cross-checked against the "
    "Department of Revenue rate books for 2024 and 2025, where all nine districts reconcile exactly. Top: "
    "levied rates by tax year. Bottom: percentage change from 2012 to 2025. Bourbon County is the only "
    "district in the region whose levied rate is lower today than in 2012. Rates are levied rates, not "
    "revenue effort; see the House Bill 44 note in the text. Data archived as build/ky_levy_history_"
    "2012_2026.csv.")

H2("The four percent is a limit on revenue, not on the rate")
P("That distinction decides an argument raised at every public meeting on this proposal, so it belongs in the "
  "record plainly. The district states that it takes the four percent option. The published rate has not "
  "risen. <b>Both statements can be true at the same time, and ordinarily are.</b> Under KRS 160.470 the "
  "board's benchmark each August is not last year's rate. It is the <b>compensating rate</b>, defined as the "
  "rate that raises the same dollars from existing property as the prior year. When assessments rise, that "
  "rate falls automatically, by the amount assessments rose. The four percent option is the compensating rate "
  "multiplied by 1.04. A board taking the full four percent every year, in a county whose property is "
  "appreciating, therefore publishes a falling rate while collecting more money. The table below works that "
  "math on this district's own figures: the fiscal 2025 certified assessment of $1,843,569,625 and the "
  "41.0 General Fund cents in KDE's levied-rates file.")
tbl(["Assessment growth", "Compensating rate", "Four percent option", "Rate raised four percent",
     "Revenue, four percent option", "Revenue, rate raised four percent", "Recallable excess"],
    [["0 percent", "41.00", "42.64", "42.64", "$7,860,981", "$7,860,981", "none"],
     ["3 percent", "39.81", "41.40", "42.64", "$7,860,981", "$8,096,810", "$235,829"],
     ["5 percent", "39.05", "<b>40.61</b>", "42.64", "$7,860,981", "$8,254,030", "$393,049"],
     ["7 percent", "38.32", "39.85", "42.64", "$7,860,981", "$8,411,250", "$550,269"]],
    [0.90 * inch, 0.98 * inch, 0.84 * inch, 0.84 * inch, 0.98 * inch, 0.98 * inch, 0.88 * inch],
    caption="Rates in cents per $100 of assessed value, General Fund levy only, on the fiscal 2025 "
            "certified assessment of $1,843,569,625 at the 41.0-cent General Fund rate. Read the five percent "
            "row: the largest rate the board can levy without recall exposure is 40.61 cents, below the 41.0 "
            "it levies now, and it still collects four percent more revenue. Revenue from new construction "
            "sits outside the cap and is additional. A reading of KRS 160.470 and KRS 132.017, not legal "
            "advice.")
P("Two consequences follow, and they point in opposite directions. First, <b>a flat or falling rate is not "
  "evidence either way</b>, and arguing about the rate alone settles nothing. Second, <b>raising the rate four "
  "percent is a different act entirely from taking the four percent option.</b> Last year's rate multiplied "
  "by 1.04, against five percent assessment growth, raises about 9.2 percent more revenue, and every dollar "
  "above the four percent ceiling is subject to a recall petition. The naive rate overshoots the protected "
  "rate by exactly the assessment growth rate, in every case. Only when assessments are perfectly flat do the "
  "two converge.")
P("What Figure 21 measures, then, is not property markets. Every one of those nine boards sets its rate each "
  "August against its own compensating rate, computed from its own assessment growth, so assessment growth is "
  "netted out before any of them votes. What remains is the choice each board made. Eight of the nine levy a "
  "higher rate today than in 2012; Bourbon's is 5.4 percent lower, the only decline in the region, and it has "
  "fallen from second highest of the nine to seventh. The honest framing of the revenue question is therefore "
  "not that this county's assessments rose, since they rose across the region. It is that eight boards facing "
  "the same statutory mechanism finished with more resources to compete with, and one did not. <b>A single "
  "document closes the remaining uncertainty</b>, and it is on the outstanding records list in Appendix B: "
  "for each of the last five years, the certified compensating rate set against the rate the board actually "
  "levied. If the four percent was taken, the levied rate sits four percent above the compensating rate, every "
  "year, on the page.")
P("One movement in Figure 21 needs explaining, because it cuts in both directions. Bourbon's total levied rate "
  "rose 3.2 cents in tax year 2023, from 49.2 to 52.4, and has held at 52.4 for three years. <b>That increase "
  "was not operating money.</b> KDE's Nickel Levy Chart dates this board's recallable facilities nickel to "
  "August 17, 2023, and KDE's current levied-rates file puts that nickel at 5.7 cents. A new 5.7-cent "
  "restricted levy inside a 3.2-cent net increase means the remainder of the rate fell about 2.5 cents in the "
  "same year, roughly $477,000 a year of unrestricted revenue at this district's own $191,000 per cent. Two "
  "caveats belong with that figure: KDE does not publish the year-by-year rate-type split, so the 2.5 cents "
  "is an inference from the current file rather than a document, and a facilities nickel is an equivalent rate "
  "that is restated annually against the whole property base and drifts. The certified split by year is "
  "requested in Appendix B for precisely this reason. The direction, however, is not in doubt: the levy that "
  "rose in 2023 was money that cannot lawfully pay a teacher, and it rose in the same year the operating levy "
  "appears to have fallen.")

H2("Beyond the four percent: the recallable levy options")
P("The four percent option is the largest increase the board can take without offering voters a veto. It is "
  "not the ceiling. Kentucky law (KRS 160.470) lets the board levy any rate, with the portion above four "
  "percent subject to a voter recall petition, and that is exactly how every neighboring district in Figure "
  "21 climbed past Bourbon. Each option below is priced at Bourbon's own audited yield of about $191,000 per "
  "cent of rate: $7,829,060 of General Fund collections across the 41.0 General Fund cents in KDE's "
  "levied-rates file, real estate only, so the figures are conservative. The household cost is priced on the "
  "county's median owner-occupied home of $211,600 (Census ACS 2019-2023): each added cent costs that "
  "household $21.16 a year, about $1.76 a month. Vehicle rates are untouched; the homestead exemption "
  "shields about $46,000 of a senior homeowner's value, so most retirees pay less; farmland is assessed at "
  "agricultural value, not market; renters pay only what landlords pass through.")
tbl(["Option", "New rate", "Added cents", "Median-home cost", "New recurring revenue"],
    [["Match Harrison County", "57.7", "+5.3", "$112/yr ($9.35/mo)", "about $1.01 million"],
     ["Match the regional median (Fayette excluded)", "60.3", "+7.9", "$167/yr ($13.93/mo)", "about $1.51 million"],
     ["Restore Bourbon's own 2018 rate", "61.3", "+8.9", "$188/yr ($15.69/mo)", "about $1.70 million"],
     ["Match Clark County", "65.5", "+13.1", "$277/yr ($23.10/mo)", "about $2.50 million"]],
    [W * 0.30, W * 0.11, W * 0.13, W * 0.22, W * 0.24],
    caption="Recallable levy options at Bourbon's own per-cent yield. Rates are 2025-26 levied real estate "
            "rates; the regional median is the median of the eight area districts with Fayette excluded. "
            "Every formula is live in the model's Tax_History tab, rows 70 to 91.")
P("Restoring the rate this district itself levied in 2018 closes about two thirds of the structural gap on "
  "its own; matching Clark closes nearly all of it. And the sequencing is where the plan's own goal comes "
  "within reach. The first call on any new recurring money is closing the operating gap ($373,989 on the "
  "FY2026 trend) and ending the $1,320,939 capital-to-General-Fund sweep, $1,694,928 in all, because ending "
  "the sweep is what frees the restricted building stream to carry bonds. Restoring the 2018 rate raises "
  "$1,699,479, covering that requirement to within $4,551. The rate this board itself levied eight years ago "
  "is, almost to the dollar, the make-the-General-Fund-stand-alone rate. Once the General Fund stands alone, "
  "the nickel residual carries the $14 million renovation, the roughly $17.6 million of unused restricted "
  "capacity becomes genuinely pledgeable, and the phasing-in nickel equalization adds about $3.6 million "
  "more: roughly $35 million of construction capacity, for $15.69 a month on the median home, without "
  "pledging a cent of the new levy to a bond and without closing anything. Pledged straight to construction "
  "instead, the four options carry about $13.2, $19.6, $22.1, and $32.5 million at the model's 4.5 percent, "
  "20-year assumption. The Harrison and median options are honest partial steps; they leave about $680,000 "
  "and $190,000 a year still to find from the alternatives menu before the sweep can end.")
P("None of this is a recommendation of a particular number, and none of it is counted in the alternatives "
  "package of Section 9. The point is narrower: a menu of options exists between cut nothing and close a "
  "school, every one of them prices out larger than the most generous closure estimate, and every one of "
  "them carries a built-in democratic check. <b>A levy above four percent can be recalled by the voters it "
  "taxes. A closed school cannot be recalled by the children it displaces.</b> This community was offered "
  "that veto twice on the facilities nickels and twice declined to use it. It has never been offered the "
  "same vote on the operating levy that pays teachers.")

# ================= 10. WHAT CAN'T BE QUANTIFIED =================
H("10. What Can't Be Quantified: A Town and Its Heartbeat")
moontext = ("<i>\u201cThe school is the heartbeat of our small, but vital community.\u201d</i>"
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
P("Everything to this point can be argued in dollars. This section cannot, and belongs in the record anyway. "
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

# ================= 11. TWELVE QUESTIONS =================
H("11. Twelve Questions the Board Should Require Answered, In Writing, Before Any Vote")
P("These are not rhetorical. Each has a document behind it that the administration either already holds or "
  "should be required to produce.")
qs = [
 "<b>Publish the closure worksheet, including the downside.</b> Line by line: the net recurring General Fund "
 "saving, meaning costs that truly disappear, minus added transportation, receiving-school costs, and the "
 "carrying or disposal cost of the building. And publish the downside alongside it, because a worksheet "
 "carrying only one side of the ledger is not a worksheet. Two risks belong on that page and neither appears "
 "in anything the district has produced. <b>First, children who leave the district rather than change "
 "schools.</b> Each one takes the SEEK base with them, $4,626 at the fiscal 2027 rate, every year, "
 "permanently; ten students is $46,260 a year and thirty is $138,780. This report's grid prices that leakage "
 "at 0, 10 and 30 students rather than assuming zero, and the risk is live here specifically: 259 registered "
 "homeschool students and roughly 450 to 550 county children are already outside these schools, so the exits "
 "are open and in use. The district's published math carries no leakage line at all. <b>Second, assessment "
 "erosion.</b> What does the loss of the town's only school do to property values inside the North Middletown "
 "attendance area, and therefore to the assessment base that funds every school in the county? The limits of "
 "my own evidence belong in the question: the thirty-year Kentucky corpus in Section 5 does <i>not</i> "
 "establish that closure causes decline, because small towns that kept their schools declined at nearly the "
 "same rate. So this is not a claim. It is a risk, it runs in one direction only, and the revenue at stake is "
 "the district's own, which makes bounding it the district's job. Publish a range and the method behind it. "
 "Both risks are estimable; neither has been estimated. A worksheet that books every saving at its best case "
 "and every risk at zero is a sales document.",
 "<b>Assessments rose everywhere. Why is Bourbon's the only rate that fell?</b> This is not a gotcha, and "
 "\u201cwe take the four percent\u201d is not a responsive answer to it. Under House Bill 44 the four percent "
 "is a limit on <b>revenue, not on the rate</b>: the benchmark is the compensating rate, which falls "
 "automatically as assessments grow, so a board can take the full four percent every year and still publish a "
 "lower rate than the year before. Section 11 works that math on this district's own assessment. Which "
 "means a flat rate proves nothing on its own, in either direction, and it also means the nine-district "
 "comparison in Figure 21 has already netted assessment growth out, because every one of those boards sets "
 "its rate against its own compensating rate computed from its own assessment growth. On that comparison: "
 "eight of the nine levy more today than in 2012, Bourbon levies 5.4 percent less, the only decline in the "
 "region, falling from second highest of the nine to seventh, and KDE's levied-type file shows Bourbon took "
 "the four percent option in five of the last twelve years against seven, eight and nine times for the "
 "neighbors that rose. So, two things in writing. One: for each of the last five years, the certified "
 "compensating rate set against the rate the board actually levied, which settles the question in a single "
 "line. Two: if the option was not taken, name what was given up, and state what it means to run a school "
 "system against eight neighbors who chose to compete with more resources. A district that has declined "
 "revenue its neighbors accepted cannot present a school closure as the only remaining option without first "
 "showing the math on the option it declined.",
 "<b>Which enrollment number is the plan built on?</b> Two documents the district produced in the same month "
 "give different 2026-27 projections for the same three elementary schools: the School Council staffing "
 "allocation says 111, 463 and 445, while the Elementary Capacity Graphic says 115, 475 and 424, for totals "
 "of 1,019 and 1,014. Which set is the plan built on, and which set was used to decide that the receiving "
 "schools have room?",
 "What exactly is inside the \u201cover a million dollars\u201d figure, and how does it reconcile with the state's "
 "published per-student spending data for the school? And which enrollment count is the administration using, "
 "federal data show 128 students, while public statements have ranged lower.",
 "Grade by grade, what is the real capacity at Bourbon Central and Cane Ridge, and what staff, sections, or space "
 "must be added to absorb 128 more children, at what cost, from which fund? The district's own 2021 facility plan "
 "rates them at 521 and 422 (549 only if an expansion never built is granted); at today's 459 and 453 enrolled, that is a net 31 uncommitted seats. Reconcile the "
 "ratings while at it: the approved plans and the 2026 draft print three different capacities for the same "
 "unchanged buildings. And publish the "
 "geocoded student counts by attendance area that any honest boundary study, including the rebalancing scenario "
 "in Section 9, needs.",
 "What are the modeled bus routes, and what is the longest one-way ride a North Middletown kindergartner would "
 "face?",
 "Where is the full report behind the KFICS assessment slides? The presentation, prepared by RossTarrant "
 "Architects, attaches $8.5 million to North Middletown, second lowest of the district's schools, against $98.4 "
 "million districtwide; publish the complete assessment, its room-by-room data, and its assumptions.",
 "Which of the claimed savings are General Fund dollars that can pay teachers, and which are restricted facility "
 "dollars that cannot?",
 "The 2024 $6.055 million bond's stated purpose is now on the public record (high school roof and a districtwide "
 "audio system, per the state bond disclosure archived here). Publish the BG-1 project applications behind it, and "
 "state when North Middletown Elementary last received meaningful capital investment.",
 "Why did central-office administration grow 44.8 percent in two years while attendance fell, and what rollback "
 "is on the table before a school closes? Publish administrator compensation from the official state records.",
 "What is the written plan to protect the academic outcomes of students moved from the school that leads the "
 "county in every state-reported subject on the 2024-25 assessments into the two schools it outscores, and "
 "what happens to the district's Title I allocations when they move?",
 "Which alternatives in Section 9 has the administration actually modeled, with what results, and if none, why "
 "is closure first on the list rather than last?"]
for i, q in enumerate(qs, 1):
    A(Paragraph(f"<b>{i}.</b>&nbsp;&nbsp;{q}", qstyle))

# ================= 12. RECOMMENDATIONS =================
H("12. Recommendations")
P("The decision before the Board is often framed as closure versus no closure. That is the wrong frame. The "
  "deficit is a districtwide problem: every school stays on the same path under Plan 1, and North "
  "Middletown, whose realistic closure saving covers under a quarter of the gap, did not cause it. The "
  "real question is which full operating plan gives the best five-year result once you check it against real numbers, and there are at "
  "least three on the table. The comparison below is an illustration, not a forecast, built on this report's stated assumptions and "
  "a straight-line projection from the fiscal 2025 balance; the workbook's Scenarios tab carries the math, and "
  "the district should replace every assumption with actuals. One-time closure transition costs, which the "
  "district has not published, are not included and would reduce Plan 2's early-year figures. Two yardsticks "
  "are in play throughout this report, and they measure different things: coverage percentages run against the "
  "$2.65 million operating gap before transfers, while these balance projections run on the roughly $1.15 "
  "million net drawdown after transfers. A plan can restore the reported balance while covering only part of "
  "the before-transfers gap, which is why both numbers are always shown side by side.")
tbl(["Plan", "Recurring impact, year 3", "Projected FY2029 balance", "What it requires"],
    [["1. Districtwide status quo (change nothing)", "None", "Fully drawn down",
      "No decisions; the districtwide drawdown simply continues, with or without North Middletown"],
     ["2. Close NMES and consolidate", "-$591,545 to +$488,631 (median: LOSES $21,971)", "Median: gone sooner than status quo; best case $1.2M",
      "Closure vote; the median scenario loses money; longer rides; enrollment-loss risk"],
     ["3. Districtwide recovery plan (menu plus levy)", "$1.0-$1.9 million a year", "About $3.3 million",
      "Revenue votes, administrative rollback, boundary action and HB 563 recruitment, implementation "
      "discipline; every school stays open"]],
    [1.85 * inch, 1.45 * inch, 1.35 * inch, 2.05 * inch],
    caption="Three complete plans, compared on the same assumptions. At the v4.2 median, Plan 2 drains "
            "reserves faster than doing nothing; only its best case buys a meaningful cushion, and 55 percent "
            "of its scenarios lose money outright. Plan 3 restores balance while keeping every "
            "school open, and rebalancing and growing North Middletown ($56,000 to $116,000 a year, Section 9) "
            "is one line inside its menu. Scenarios and Runway tabs of the companion workbook.",
    bold_first_col=True)
asktext = ("<b>The ask, plainly stated:</b> the community requests that the Board of Education pause any vote on "
           "the facility plan, or on the future of North Middletown Elementary, until the twelve questions in Section "
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
B("Adopt a formal Board position that closure is a last resort, to be considered only after the twelve questions above "
  "are answered in writing and the alternatives in Section 9 have been costed.")
B("Decline to adopt any facility plan carrying a \u201ctransitional\u201d designation for North Middletown until the "
  "net-savings worksheet, the complete KFICS assessment behind the July slides, the 2024 bond project "
  "applications (the BG-1s behind the already-public high school roof and audio-system purpose), and the "
  "school-level climate-and-safety survey results are public.")
B("A working threshold for the Board: if documented net recurring General Fund savings fall below roughly "
  "$400,000 to $500,000 a year, a range the four percent revenue option alone reaches by its second year "
  "without closing a school, closure "
  "fails on its own financial terms.")
B("Face the levy each August with the numbers on the table: the four percent option adds roughly $313,000 of "
  "recurring revenue in year one and about $978,000 a year by year three if taken three years running, "
  "while Bourbon would still tax below six of its eight neighbors. Take it or reject it, but decide on the "
  "record, alongside the spending decisions, because standing idle is the one answer I rule out.")
H2("Over the next twelve months")
B("Pursue the low-harm levers first: the collections-gap reconciliation, the 4-percent levy decision at the "
  "September tax setting, transportation routing, attrition-based staffing, and "
  "an administrative cost review, with quarterly public reporting against a target of cutting the operating "
  "deficit from $2.6 million to under $1.5 million by fiscal 2027 and under $800,000 by fiscal 2028.")
B("Set up a North Middletown sustainability committee, district, city, parents, and business, to design the "
  "signature program, community uses of the building, and a transfer-in program for the 2027-28 school year.")
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
  "county's best elementary school, in the town that would lose the most, on the strength of an unpublished "
  "number, would be a permanent answer to a solvable problem. The community is not asking the Board to ignore the "
  "deficit. It is asking the administration to show its work. Before an irreversible decision, the district "
  "should publish the staffing, receiving-school capacity, transportation, building, enrollment-retention, tax, "
  "and interfund-transfer analyses needed to compare closure against complete keep-open and districtwide recovery "
  "plans. Revenue or reductions, the Board must choose one and own it; standing still simply spends the reserves "
  "and settles nothing. Pause the vote. Answer the questions.")

# ================= NOTES =================
H("Notes on the Data")
P("I built this report from public records, and I want it held to that standard. The audited figures come from "
  "the district's financial statements for the years ended June 30, 2024 and June 30, 2025, both of which carry "
  "clean opinions. Per-student spending is the state's published school-level data for 2023-24, the most recent "
  "full year posted, and should be refreshed when the next year appears. The multi-year score series in Figure 10 "
  "is SchoolDigger's normalized 0-100 rendering of Kentucky Department of Education test data, a consistent "
  "yardstick across years but not KDE's official rating. Where this report says first in every tested subject, "
  "that is the state's own 2024-25 assessment file, archived in the repository; third-party rankings built on "
  "older data or different weights may order schools differently, and the state's current file is the primary "
  "academic record here; the underlying state assessments changed in 2012 and "
  "again in 2021-22. Demographic figures come from the U.S. Census Bureau, the Kentucky State Data Center's "
  "projections as reported in county planning documents, and the county's Envision 2040 plan. Enrollment counts "
  "from 1989 through 2014 are compiled from federal data by PublicSchoolReview; the 2015 through 2025 counts "
  "match the federal figures directly. Every dollar range labeled an estimate is mine, its assumptions are "
  "stated where it appears, and every one of them is adjustable in the companion workbook. The boundary "
  "rebalancing scenario in Section 9 is simple math on the cited enrollment counts, not a routing study; the "
  "geocoded student counts and routing data a full study needs are held by the district and requested in "
  "Question 3. The transportation estimates beside it use the official federal zone boundaries (SABS, "
  "2015-16), a highway distance, and labeled cost-per-mile bands; the district's annual T-1 transportation "
  "report would replace the cost inputs, and the Transport_Geo tab is built to take them.", note)
P("A few items in the record need the district, not me, to resolve. The real-estate tax rate appears three "
  "ways in public records, as 52.4, 54.2, and 54.7 cents; that confusion is resolved in Section 9: 52.4 "
  "cents is the levied rate, 54.2 a transposition typo, 54.7 the "
  "motor vehicle rate; still open are the General Fund versus building fund cent split, the levied rate type "
  "by year, and the pre-2018 rate history, all in state files the district can produce. The 2013R bond "
  "figures are internally inconsistent as printed. The 2024 bond's stated purpose is now on the public record "
  "through the state's June 2024 bond disclosure (high school roof and a districtwide audio system); the 2023 "
  "issue's project detail and both years' BG-1 applications are still open. The school-level climate and safety "
  "survey results were not publicly retrievable. "
  "And the enrollment count itself: federal data show 128, public statements have said around 100, and a 118 "
  "figure appears in no official record I could find. Reported free and reduced-price meal shares for the school "
  "range from roughly 76 to 93 percent across federal and state sources. My recollection in Section 10 of an "
  "earlier transitional episode comes from personal discussions with my father, who served as mayor of North "
  "Middletown; it is offered as memory, and the pre-2021 planning records that would confirm it are requested "
  "in Section 12. One more for the record: the fiscal 2025 audit misprints the prior year's attendance as "
  "2,278.527; the correct figure, 2,278.537, comes from the fiscal 2024 audit itself.", note)
P("I prepared this report myself, with Claude, an AI research assistant from Anthropic, doing the digging "
  "alongside me, and I disclose that on purpose: check my work. Every figure traces to a source below, and every "
  "school and district named is the Kentucky one. Cautions on pension allocations inside expense lines, one-time "
  "swings, single-year score noise, and the tax cost of the levy option sit beside the numbers they qualify. The "
  "Kings mascot and the blue and white of these pages are the school's own. This report criticizes decisions and "
  "asks for documents. It attributes no motive and alleges no wrongdoing to the superintendent, the finance "
  "office, the Board, or any member of the planning committee, and nothing in it should be read otherwise.", note)
P("Corrections in version 3.9. Ten, five of them against this report's own case. <b>One.</b> The 99.6 percent "
  "statewide figure was attached to the corrected test; it belongs to the $8,255 bar the 300 implies. The "
  "corrected test fails 786 of 1,151 Kentucky schools, 68 percent. <b>Two.</b> The real breakeven was published "
  "as 38 to 69 students. The low end credited every child with federal money that in fact follows the child and "
  "relieves the General Fund by nothing. The lower bar is withdrawn; the range is 54 to 69, and the school "
  "enrolls 128. <b>Three.</b> A $9,848 empirical marginal cost, taken from two schools' cost gap over their "
  "enrollment gap, depends on a membership pair I cannot source and turns negative on the two I can. Withdrawn, "
  "and replaced with the break-even bound. <b>Four.</b> The five-year growth comparison, 16, 37 and 47 percent, "
  "did not name its enrollment counts: state membership for North Middletown but 2021 facility plan headcounts "
  "for the receiving schools. On federal fall 2019 counts it gives 16, 35 and 46 percent. Bands are now published "
  "with the counts named; North Middletown grew least under every count tested. <b>Five.</b> The federally "
  "reported $2.5 million was called total site spending. It is allocated to the school, not coded to it; the "
  "district's ledger codes about $1.0 million less. <b>Six.</b> The $2,476,544 was described as exact to the "
  "dollar. The exact step is my own multiplication, the fit to the district's stated about 300 is 298, and it "
  "pairs a 2023-24 rate with a later headcount. <b>Seven.</b> No other revenue definition was said to land near "
  "300; the district's coded cost over the SEEK base gives 278. <b>Eight.</b> About one in three of the county's "
  "school-age children were said to be in private school or homeschooling, from the Census survey alone. The "
  "rosters cap it lower: 450 to 550 children, 13 to 15 percent. <b>Nine.</b> The website closure calculator "
  "allowed combinations wider than the grid it cites, in every case flattering closure; its sliders now sit "
  "inside the grid.", note)
P("One further disclosure that is not a correction but belongs with them. The measured fixed base at this "
  "school, $227,831 for administration, custodial and plant, sits within half a percent of the $230,000 this "
  "report's closure grid uses as its low fixed-cost value. That is corroboration. But $230,000 is the grid's "
  "floor, and reaching it requires that the principal, the secretary, the custodian and the utilities all be "
  "eliminated rather than reassigned, and the v3.8 grid contained no redeployment scenario at all. Version "
  "3.9 rebuilt that lever on three measured values, $58,774 reassigned, $227,831 mothballed and $276,928 "
  "sold, taking the grid from 1,944 combinations to 2,916. The published median fell from $91,240 to "
  "$21,571, the negative share rose from 29 to 45 percent, and the range widened to minus $556,006 and plus "
  "$551,928. It was the tenth correction in that release and the one that cost this report's case the most.", note)
P("Changes in version 4.2, made after the district published its 48-page Response to the 10 Questions "
  "(archived in full in the repository). The closure grid was rebuilt on the district's own figures, and the "
  "changes cut in both directions. In closure's favor: the non-salary savings lever now uses the district's "
  "own worksheet ($107,039 of building-bound lines plus $20,000 of insurance) instead of this report's "
  "narrower measured cases; the teacher lever rises to a top leg of three positions, because the district's "
  "own classroom-capacity appendix supports three eliminated homerooms even though its savings sheet prices "
  "two; and every staffing position is priced at the district's own fully loaded $54,479.40 instead of a "
  "$50,000 to $75,000 band. Against closure: the leakage lever now runs to 50 percent of the school, priced "
  "at the SEEK base plus up to $1,000 of add-ons per leaver, and the capacity-debt-service lever is retired. "
  "The old two-tailed range, minus $556,000 to plus $552,000 with a $22,000 median saving across 2,916 "
  "scenarios, is replaced by the new grid: 5,832 scenarios, a range of minus $591,545 to plus $488,631, a "
  "median outcome that LOSES $21,971 a year, and 55 percent of scenarios losing money. The prior published "
  "figures were not errors; they were this report's own estimates, and the district's own paperwork has now "
  "replaced them.", note)
P("Corrections policy: errors identified in this report will be corrected publicly and promptly, and each "
  "corrected version will carry a new version number and date. Every version, and the line-by-line history of "
  "every change to the report, model and website, is archived at github.com/ryanuspsagm/SaveNMES. Send "
  "corrections, with the source that supports them, to ryanuspsagm@gmail.com. The same standard is asked of the "
  "district: publish the worksheet, and if this report's numbers are wrong, its own records are the fastest way "
  "to show it.", note)

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
 "SchoolDigger, normalized 0-100 school test-score histories and statewide rankings built from Kentucky "
 "Department of Education assessment data: schooldigger.com (used for Figures 10 and 11 and the statewide ranks; "
 "not KDE's official rating)",
 "Kentucky Department of Education, School Report Card assessment dataset, 2024-25 Kentucky Summative "
 "Assessments, school-level, all students: kyschoolreportcard.com datasets; the rows for the four Bourbon "
 "County elementary schools and the statewide elementary averages are archived in this repository as "
 "build/kde_ksa_2024_25.json",
 "Kentucky Department of Education, historical School Report Card datasets, 2011-12 through 2023-24: "
 "accountability achievement and profile files (education.ky.gov/Open-House/data/HistoricalDatasets) and, "
 "for 2017-18 and 2018-19, Wayback Machine captures of KDE's retired openhouse download endpoint; the "
 "multi-year extract for the four county elementary schools, with the SchoolDigger validation results, is "
 "archived in this repository as build/kde_scores_history.json",
 "Bourbon County Schools District Facility Plan, approved by the Kentucky Board of Education, August 2021: "
 "education.ky.gov/districts/fac/documents/bourbon co dfp.pdf (archived in this repository as build/dfp_current.pdf)",
 "Bourbon County Schools District Facilities Plan, approved by the Kentucky Board of Education, June 2013, "
 "recovered from the Internet Archive's Wayback Machine captures of the same KDE address (24 captures, 2015-2025): "
 "web.archive.org; excerpt archived in this repository as build/dfp_2013_excerpt.png with provenance in "
 "build/dfp_manifest.json",
 "Bourbon County Schools District Facility Plan, 2026 planning-cycle draft as presented at the July 15, 2026 "
 "Local Planning Committee forum, before the committee's amendment (KDE approval date listed TBD); annotated "
 "attendee copy archived in this repository as build/dfp_2026_draft_excerpt.png with provenance in "
 "build/dfp_manifest.json",
 "702 KAR 4:180, Kentucky School Facilities Planning Manual; 702 KAR 4:160, Capital Construction Process: "
 "apps.legislature.ky.gov/law/kar/titles/702/004",
 "Kentucky Revised Statutes 160.470 and 132.017 (school property-tax rates); 157.350 (nonresident students); "
 "157.420 and 157.440 (capital outlay and building funds); 157.360 (class-size caps); 157.622 (SFCC offers "
 "of assistance)",
 "Kentucky Department of Education, SEEK funding files and Local District Tax Levies: education.ky.gov/districts/SEEK "
 "and education.ky.gov (Taxes)",
 "Kentucky Department of Revenue, 2025 Property Tax Rate Book",
 "School Facilities Construction Commission, bond participation and refunding policies: sfcc.ky.gov; SFCC Bond "
 "Payee Disclosure for the Series of 2024 bonds and the Capital Projects and Bond Oversight Committee minutes of "
 "June 20, 2024, Kentucky Legislative Research Commission (both archived in this repository under build/)",
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
 "WKYT-TV and FOX 56 News, coverage of the Bath County nickel-tax votes, November 2024 and January 15, 2025 "
 "(the only school tax defeated by voters in any of the eight neighboring districts in the last ten years)",
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
 "KRS 132.010 (definition of the compensating rate) and KRS 132.017 (petition and recall of a tax rate "
 "producing more than four percent additional revenue), the two statutes behind the rate-versus-revenue "
 "table in Section 11",
 "Kentucky Department of Education, Nickel Levy Chart (March 2024), dating each district's facilities and "
 "recallable nickels, including Bourbon County's August 17, 2023 recallable levy; and KDE SEEK payment "
 "schedules FY2025 through FY2027 for the equalization phase-in on that nickel",
 "Bourbon County Schools, Annual Financial Report and audit, fiscal 2025 (certified real and personal "
 "property assessment of $1,843,569,625 and General Fund property tax collections of $7,829,060)",
]
for i, s in enumerate(srcs, 1):
    A(Paragraph(f"{i}. {s}", ParagraphStyle("src", parent=note, fontSize=8.4, leading=10.8, spaceAfter=2.7)))

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
 ["SEEK", "Support Education Excellence in Kentucky, the state's per-student funding formula ($4,586 base in fiscal 2026, rising to $4,626 in fiscal 2027)."],
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
P("Kentucky's Open Records Act (KRS 61.870 to 61.884; inspection rights and request procedures in KRS 61.872, "
  "agency response requirements in KRS 61.880) entitles any resident to these documents on request "
  "to the district's records custodian, with a response due within five business days. Each request names "
  "the labeled estimate in this report or the companion workbook that it would replace. Nothing here seeks "
  "student-identifiable information, and I will publish, and correct against, whatever comes back.")
tbl(["Request", "What it settles"],
    [["<b>The money.</b> The net-savings worksheet behind the \u201cover a million dollars\u201d statement",
      "Replaces the published two-tailed range, minus $591,545 to plus $488,631 (Sections 1, 4)"],
     ["Any alternatives modeling the administration has performed",
      "Whether closure was compared to anything (Section 9)"],
     ["Administrator salary schedule and five years of compensation, position by position",
      "How much of the 44.8 percent central-office growth is people versus accounting (Section 8)"],
     ["KDE levy files: rate type elected each year; General Fund versus building fund cent split",
      "The two open cells in the tax history (Section 9)"],
     ["<b>The certified compensating rate against the rate actually levied, each of the last five years</b>",
      "Settles in one line whether the four percent option was taken, which the levied rate alone cannot "
      "show (Section 11, Question 2)"],
     ["<b>The buildings and bonds.</b> The 2024 bond's official statement and BG-1; the 2023 issue's purpose",
      "Where $6.9 million of recent borrowing went (Section 6)"],
     ["KDE's bonding potential statement for the district",
      "Real borrowing headroom beside the audit's $23.5 million (Section 6)"],
     ["The complete KFICS assessment behind the RossTarrant slides, with room-by-room data and assumptions",
      "The slides are public (archived on this site); the full report is not (Section 7)"],
     ["The room-by-room worksheet behind the 174 capacity rating; the pre-2021 facility plans",
      "Whether capacity is a wall or a room schedule (Section 7)"],
     ["<b>The boundaries and buses.</b> The district's current GIS attendance-zone map",
      "Confirms the official 2015-16 federal boundaries in Figure 18 are still in force"],
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
B("School Attendance Boundary Survey (NCES EDGE, 2015-16): the district's attendance-zone GIS files, school "
  "locations, and enrollment files at nces.ed.gov/programs/edge, with the prepared query in this repository as "
  "build/fetch_sabs.py. Also public: U.S. Census TIGER county boundaries and block-level population counts "
  "(census.gov/geographies), and KDE SEEK transportation calculation files (education.ky.gov/districts/SEEK).")
B("Every levy figure in Section 11 can be checked without asking anyone for anything. KDE publishes its Local "
  "District Tax Levies files, which carry each district's levied rates and the general fund, FSPK and "
  "recallable components of the current year's rate, and its Nickel Levy Chart, which dates every district's "
  "facilities nickels. The Kentucky Department of Revenue publishes annual Property Tax Rates books covering "
  "all 120 counties and every school district line. This report's compiled fourteen-year, nine-district series "
  "is archived in the repository as build/ky_levy_history_2012_2026.csv, and it reconciles exactly against the "
  "Department of Revenue books for 2024 and 2025 in all nine districts. What is <b>not</b> published, and "
  "therefore is requested above, is the rate type each board elected in each prior year and the general fund "
  "versus building fund split for years before the current file. That single gap is the reason the 2.5-cent "
  "figure in Section 11 is labeled an inference rather than a finding.")

# ---------------- build ----------------
def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.6)
    canvas.line(0.9 * inch, 0.66 * inch, 7.6 * inch, 0.66 * inch)
    canvas.setFont("Helvetica", 7.6)
    canvas.setFillColor(GRAY)
    canvas.drawString(0.9 * inch, 0.5 * inch,
                      "Saving North Middletown Elementary School  \u2022  A Close Look at Bourbon County Schools  \u2022  Version 4.2, August 1, 2026")
    canvas.drawRightString(7.6 * inch, 0.5 * inch, f"Page {doc.page - 1}")
    canvas.restoreState()

def cover(canvas, doc):
    pass

doc = SimpleDocTemplate("/home/claude/nmes/Saving_North_Middletown_Elementary.pdf",
                        pagesize=letter,
                        leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                        topMargin=0.85 * inch, bottomMargin=0.95 * inch,
                        title="Saving North Middletown Elementary School, a Close Look at Bourbon County Schools",
                        author="North Middletown Community Analysis")
doc.build(story, onFirstPage=cover, onLaterPages=footer)
print("pdf built")
