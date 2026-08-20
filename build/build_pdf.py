from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                CondPageBreak, Image, Table, TableStyle, HRFlowable,
                                KeepTogether)
from PIL import Image as PILImage
import os as _nmes_os
OUT = _nmes_os.environ.get("NMES_OUT", "/home/claude/nmes")

NAVY = colors.HexColor("#1F3864")
GOLD = colors.HexColor("#2E75B6")
GRAY = colors.HexColor("#555555")
LINE = colors.HexColor("#B9C2D0")
HEADBG = colors.HexColor("#E8EDF5")
ROWBG = colors.HexColor("#F5F7FA")

W = 6.7 * inch  # usable frame width

# ---------------- styles ----------------
body = ParagraphStyle("body", fontName="Times-Roman", fontSize=10.3, leading=13.8,
                      alignment=TA_JUSTIFY, spaceAfter=5.5, textColor=colors.HexColor("#1A1A1A"))
lede = ParagraphStyle("lede", parent=body, fontSize=10.8, leading=14.8)
bullet = ParagraphStyle("bullet", parent=body, leftIndent=16, bulletIndent=4, spaceAfter=4)
h1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=14.5, leading=17.5,
                    textColor=NAVY, spaceBefore=12, spaceAfter=6, keepWithNext=1)
h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=11.2, leading=14,
                    textColor=colors.HexColor("#2E5395"), spaceBefore=8, spaceAfter=4, keepWithNext=1)
cap = ParagraphStyle("cap", fontName="Helvetica-Oblique", fontSize=8.2, leading=10.3,
                     textColor=GRAY, spaceBefore=3, spaceAfter=8)
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
    im = PILImage.open(f"{OUT}/{png}")
    w, h = im.size
    height = width * h / w
    A(KeepTogether([Image(f"{OUT}/{png}", width=width, height=height),
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
    if caption and len(rows) <= 5:
        A(KeepTogether([t, Paragraph(caption, cap)]))
    elif caption:
        A(t)
        A(Paragraph(caption, cap))
    else:
        A(t)

# ================= COVER =================
A(Spacer(1, 1.35 * inch))
A(Paragraph("A COMMUNITY REVIEW OF PUBLIC RECORDS", ParagraphStyle(
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
A(Paragraph("Written by a group of volunteers from the NMES community (past and present), including Dr. Ryan Bradley, a former NMES King and Bourbon County Colonel; the analysis and report writing were accelerated with the use of an AI research assistant.<br/>Built from public records and Open Records Requests only.",
            ParagraphStyle("pf3", fontName="Helvetica-Oblique", fontSize=9, alignment=TA_CENTER,
                           textColor=GRAY, spaceAfter=5)))
A(Paragraph("Version 5.0 &nbsp;\u2022&nbsp; August 17, 2026",
            ParagraphStyle("pf4", fontName="Helvetica", fontSize=9, alignment=TA_CENTER,
                           textColor=GRAY, spaceAfter=0)))
A(Spacer(1, 1.6 * inch))
scope = ("This review is built from public records and Open Records Requests only: the district's audited financial "
         "statements for the fiscal years ending June 30, 2024 and June 30, 2025; documents produced under KRS 61.870; "
         "Kentucky Department of Education funding, facility, and school report card data; federal enrollment records; "
         "municipal bond disclosures; state regulations; and local reporting. Where a figure is an estimate, we label "
         "it and state its assumptions. This is not an audit. It alleges no misconduct by any person; both years of "
         "the district's financial statements received clean opinions from its independent auditors. Its purpose is "
         "simple: lay out what the public record shows, and what it does not yet show, before an irreversible decision "
         "is made about a community's school. We write as volunteers from the NMES community, past and present. The "
         "analysis and report writing were accelerated with the use of Claude, an AI research assistant from Anthropic. "
         "Re-verify every figure against the cited primary sources before formal submission or republication.")
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

# ================= CONTENTS =================
H("Contents")
toc_style = ParagraphStyle("toc", fontName="Times-Roman", fontSize=10.6, leading=15.5,
                           textColor=colors.HexColor("#1A1A1A"), leftIndent=14)
toc_part = ParagraphStyle("tocp", fontName="Helvetica-Bold", fontSize=10.2, leading=15,
                          textColor=NAVY, spaceBefore=9, spaceAfter=2)
for part, items in [
    ("Opening", ["1. Executive Summary: The Case, the Plan, and the Choice"]),
    ("Part One: The Case Against Closing NMES",
     ["2. Academic Performance: The District Would Be Closing Its Best Elementary School",
      "3. The School Is Not Expensive: The Cost Record",
      "4. The Million-Dollar Question: What Closing the School Would Actually Save",
      "5. What Closure Risks: The Record Where It Has Been Tried",
      "6. What Can't Be Quantified: A Town and Its Heartbeat"]),
    ("Part Two: The District Needs Growth, Not Closures",
     ["7. The District's Finances: A Real Problem With Clear Causes",
      "8. Bonds, Buildings, and Two Different Pots of Money",
      "9. Where the Money Is Actually Going: Administrative Growth",
      "10. The Alternatives on the Table: Grow, Don't Close"]),
    ("The Decision",
     ["11. The Decision, and the Four Asks"]),
    ("Supporting Data and Appendices",
     ["Notes on the Data", "Sources", "Appendix A: Plain-Language Glossary",
      "Appendix B: Other Supporting Data"])]:
    A(Paragraph(part, toc_part))
    for it in items:
        A(Paragraph(it, toc_style))
A(Spacer(1, 10))
P("The order follows SaveNMES.org section for section: the case against closing, the priced models, the "
  "district-wide growth plan, and the choice. Figures run in one numbered sequence; supporting tables sit "
  "unnumbered beside their text. Every figure traces to an archived source document and runs as a live "
  "formula in the companion workbook.", note)
A(Spacer(1, 14))

# ================= 1. EXECUTIVE SUMMARY =================
H("1. Executive Summary: The Case, the Plan, and the Choice")
P("On July 15, 2026, the Local Planning Committee of Bourbon County Schools voted to label North Middletown "
  "Elementary “transitional” in the district's draft four-year facility plan. That is the first step toward "
  "closing the school. The vote is advisory. The elected Board of Education decides, and nothing takes "
  "effect without further committee action, a public hearing, and approval by the Kentucky Board of "
  "Education. Superintendent Larry Begley has said publicly that “the decision is not final.” We checked "
  "the public records so the Board and the public can see the whole picture before any vote. This opening "
  "mirrors the executive summary published at SaveNMES.org. Every figure below is sourced in the numbered "
  "sections and runs as a live formula in the companion workbook. Where the record forces an assumption, "
  "we make one, state it where it is used, and publish it openly so it can be challenged, as a live input "
  "in the workbook and calculators. Corrections are made publicly.", lede)

H2("Part One. The case against closing NMES: four facts from the district's own documents")
B("<b>Fact one: it is the county's best elementary school.</b> On the state's 2024-25 tests, North "
  "Middletown ranks first among the county's four elementary schools in every state-reported subject. It "
  "beats the state average in science and writing. It was a National Blue Ribbon School in 2011, one of "
  "five in Kentucky that year (Section 2).")
B("<b>Fact two: it is not expensive.</b> On the newest state spending file (2024-25), NMES costs $17,903 "
  "per student. The average Kentucky elementary school costs $19,299, so NMES runs 7 percent below the "
  "state average. The district's own cost table, dated May 21, 2026, agrees: $19,080 per student against "
  "a state average of $19,020 on the same table, a gap of three tenths of one percent (Section 3).")
B("<b>Fact three: closing it frees very little.</b> Start from everything the district spent on the school "
  "last year: $1,285,310, from its own ledger. Almost all of it moves with the children or pays for itself. "
  "Only the building's own costs stop: $79,211 a year if staff keep their jobs, up to $127,039 if the "
  "building is sold. The superintendent's written response retains all staff, priced at its own "
  "$54,479.40 loaded cost. The district's $661,139 figure includes $493,407 of staffing savings that, by "
  "the response's own terms, arrive only as staff leave by attrition. In year one, with staff retained "
  "and supplies moving with the kids, only $127,039 remains. We priced 972 closure scenarios on the "
  "district's own figures, with departures measured by the signed school-choice survey instead of "
  "guessed. The range runs from losing $846,285 a year to still losing $9,860. The median LOSES "
  "$427,087. Every one loses money (Section 4).")
B("<b>Fact four: closing it risks a lot, every year.</b> Under HB 563, state money follows each child to "
  "whichever district wins the family. Registered homeschooling in this county grew from 170 to 259 in five "
  "years. The statewide virtual academy grew from 937 to 2,412 students in two years, on the enrollment "
  "counts of Cloverport Independent, its host district. Every child who leaves takes about $5,100 a year "
  "of state money along. The loss grows as the missing kids reach every grade (Section 5):")
tbl(["Estimate", "Basis", "Students missing each year", "SEEK lost each year"],
    [["Today's students", "43 to 57 percent of the 115 enrolled now", "49 to 65", "$251,174 to $333,190"],
     ["Steady state", "the same share of the whole feeder stream, middle half", "117 to 154", "<b>$599,742 to $789,404</b>"],
     ["Steady-state median", "the middle of the band", "136", "$697,136"]],
    [0.9 * inch, 2.2 * inch, 1.5 * inch, 1.8 * inch],
    caption="What leaving families cost, measured by the August 2026 school-choice survey (Section 5), "
            "priced at $5,126 per student-year: the enacted FY2027 SEEK base of $4,626 plus $500 of typical "
            "add-ons. A child who leaves is missing for every remaining grade through 12th, discounted by "
            "the district's own grade-to-grade survival (12.62 effective years). Losses build from six "
            "grade cohorts in year one to all thirteen by year eight, then hold.")
P("Read the signed evidence first: thirty-one households put their names on paper for seventy children. "
  "The statistical rows read the survey the honest way, as a share of the current student population, "
  "corrected for response bias. The middle half takes 49 to 65 of the 115 students enrolled today. "
  "Carried across the whole feeder stream, that keeps 117 to 154 students a year off the district's "
  "rolls, $599,742 to $789,404 a year. "
  "The children in the building carry about $6.2 to $6.9 million of remaining state funding through grade "
  "12 (1,339 student-years on the official 2024-25 roster of 128, priced at the $4,626 base to $5,126 with add-ons). About one in eight middle "
  "and high schoolers came through North Middletown, its elementary-seat share carried up the grades. A "
  "family lost at kindergarten is lost for thirteen years. "
  "<b>The bottom line, from the two priced models:</b> grow the school and the middle case GAINS $141,780 "
  "a year, with not one losing scenario in 19,683 (every scenario prices students who actually arrive). "
  "Close it and the middle case LOSES $427,087 a year.")

H2("Part Two. The district needs growth, not closures: three levers the board already owns")
P("<b>The money problem is real, and it is district-wide.</b> The General Fund ran a $2.65 million deficit "
  "in fiscal 2025. The district's own June 2026 ledger trends fiscal 2026 about $1.74 million in the red: "
  "better, still red. The causes are plain. Pandemic aid ended. Funded attendance fell by about 247 once "
  "the pandemic hold-harmless ended, and the state's 2026-27 forecast puts it at 2,174, down again. The "
  "district also sweeps $1.32 million a year of restricted building money into operations, draining the "
  "fund that should pay for buildings. And the revenue posture stands alone in the region: the county's "
  "tax base grew 107.5 percent since 2012, second fastest of eight area counties, while the school levy "
  "fell 5.4 percent, the only drop among nine districts. Every neighbor's base grew too. Their boards "
  "raised rates anyway (Sections 7 and 10).")
B("<b>Lever one, enrollment.</b> Each recovered student brings about $4,226 of state money after supplies. "
  "The pool is measured: 236 students sit in Bourbon's own homeschool files, and 450 to 550 Bourbon County "
  "Schools kids are homeschooled, in private school, or enrolled in another district, worth $2.1 to $2.5 "
  "million a year at the full $4,626 SEEK base. Eminence Independent proved "
  "the model an hour away: it grew 35 percent in the decade Bourbon Schools shrank 10. Growth pays in every one of "
  "19,683 priced scenarios, with a middle case of +$141,780 a year.")
B("<b>Lever two, fixed costs.</b> Trim every non-teaching position by attrition: $340,000 to $425,000 a "
  "year. Weigh an administrative restructuring: $224,000 to $450,000. Smarter bus routes: $146,000 to "
  "$291,000 on a $2.9 million line no routing study has ever tested. Energy contracts: $50,000 to "
  "$150,000. Counted once, the package is $760,000 to $1.3 million a year.")
B("<b>Lever three, revenue.</b> The rate is simply lower while the tax base more than doubled. Restoring "
  "the board's own 2018 rate brings in about $1.5 million a year on the certified real estate roll, and the "
  "rate menu beyond it reaches $0.9 to $2.2 million. The portion above four percent revenue growth is "
  "recallable by petition, the same democratic check every neighboring increase carried.")
P("<b>Together, the plan is transformative.</b> With costs at the low end and the full restore, it "
  "clears the trending gap with about $500,000 a year to spare, before a single leaked student comes "
  "back. That is within $7,000 of funding a 5 percent raise for every certified teacher; clearing the gap "
  "also unlocks the $32 million of bonding capacity the district's own advisor presented in June 2026. Two recovered "
  "students close the difference. Recover "
  "half the pool and the surplus reaches about $1.7 million a year and about $47 million of capacity; the "
  "full pool reaches about $3.4 million and about $69 million. Every school stays open. To run it, the "
  "board should create three standing committees, one per lever, each reporting publicly: enrollment "
  "growth, fixed costs, and revenue (Section 10).")

H2("The choice: two roads, and four asks that commit no new money")
P("Shrink to fit, or grow and thrive. On North Middletown, four asks that commit no new money:")
B("<b>One:</b> keep the school listed as Permanent in the facility plan; a plan commits no money, and only "
  "Permanent keeps every door open.")
B("<b>Two:</b> give it the four years to the next plan, with public enrollment targets and the tools to "
  "hit them, judged on results.")
B("<b>Three:</b> let the community fund the building's needs with grants, private money, and donated "
  "labor.")
B("<b>Four:</b> say publicly that the district will work to grow this school; uncertainty is its own "
  "enrollment killer.")
P("These asks put no money at risk: if staff keep their jobs, closing frees only $79,211 of building costs "
  "on the district's own ledger. A closed school cannot be recalled by the children it displaces; a growth "
  "plan can be measured by everyone, every year. The timing ask: pause any vote until the closure "
  "worksheet is published with both sides of the ledger and the four asks are answered in public "
  "(Section 11).")

# ================= PART ONE =================
H("Part One: The Case Against Closing NMES")
P("Four facts, in the website's order: the school outperforms, it is not expensive, closing it frees "
  "very little, and the risks land on the revenue side. Every figure is sourced and lives in the "
  "workbook.")

# ================= 5. ACADEMICS =================
H("2. Academic Performance: The District Would Be Closing Its Best Elementary School")
H2("The state's own numbers, first")
P("Before any index or ranking, here is the primary record: KDE's school-level file for the 2024-25 "
  "Kentucky Summative Assessments, archived at build/kde_ksa_2024_25.json so anyone can check it. On "
  "the state's own tests, North Middletown is first among all four elementary schools in Bourbon "
  "County, county district and Paris Independent alike, in every tested subject. It beats the "
  "<b>statewide</b> elementary average in science and writing.")
tbl(["Subject (percent proficient or distinguished)", "NMES", "Bourbon Central", "Cane Ridge", "Paris Elem.", "KY average"],
    [["Reading", "41", "38", "37", "25", "49"],
     ["Mathematics", "31", "28", "27", "29", "43"],
     ["Science", "53", "26", "*", "*", "37"],
     ["Social Studies", "36", "31", "27", "22", "38"],
     ["Combined Writing", "56", "40", "27", "4", "43"]],
    [2.35 * inch, 0.85 * inch, 1.15 * inch, 0.95 * inch, 0.85 * inch, 0.9 * inch],
    caption="Kentucky Summative Assessment results, 2024-25, all students, percent scoring proficient or "
            "distinguished. Source: KDE School Report Card assessment dataset, archived in this repository. "
            "Asterisks are cells the state suppresses (KDE's written rule withholds a row when any "
            "achievement level holds fewer than three students); the Kentucky average is the statewide "
            "elementary level.",
    bold_first_col=True)
P("Here is the full arc, straight from the state's own files (Figure 1, top panel). Through the Unbridled "
  "Learning era North Middletown's official overall score rose every single year: 62.6 to 68.8 to 71.4 to "
  "72.1 to <b>79.1</b>, closing 2015-16 with a formal <b>Distinguished</b> classification, the county's "
  "best score by nearly ten points. The same files show the school <b>first in the county in elementary "
  "mathematics in every pre-COVID administration on record</b>, 2011-12 through 2018-19, eight straight. "
  "The pandemic cratered every school in the county. The recovery is where they separate: North "
  "Middletown's overall indicator rate climbed 51.9 to 62.2 to <b>74.5</b> in 2023-24, first in the county "
  "by fourteen points, with reading and math both at 45 percent proficient or better. In 2024-25 a tested "
  "cohort of roughly sixty children slipped to 41 and 31 while statewide averages ticked up: a real "
  "single-year decline worth watching. The school still finished first among all four county elementaries "
  "in every subject where the state publishes comparable results (two schools' science scores are "
  "state-suppressed under KDE's fewer-than-three rule). Small schools swing hard in single years, in both "
  "directions; one soft year argues for attention, not for closure. One reading note, because the "
  "official index line crosses in 2024-25: Kentucky's index blends each year's level with the change from "
  "the year before. On every 2024-25 status measure the state computed, North Middletown led Bourbon "
  "Central; the index crosses only because the change formula subtracts North Middletown's own 2023-24 "
  "spike and credits Bourbon Central's climb off its 50.3. A school is not worse for having been "
  "excellent the year before.")
P("The repository also archives the federal EDFacts series, an independent cross-check that reaches back "
  "to the era of the 2011 Blue Ribbon, where North Middletown prints 89.5 and 94.8 on the old KCCT scale. "
  "Kentucky replaced its test in 2011-12, so federal values before and after that line are different "
  "scales, and the file reports small-school values as range midpoints.")
P("We keep the SchoolDigger index in Figure 1's lower panel and in Figure 2 only as outside context, "
  "with its limits printed. It tracks the county's larger schools closely but is unreliable year to "
  "year for a school this size, and it named the wrong county leader in three of the ten years both "
  "sources cover. Wherever the index and the official record disagree, the official record governs.")
P("In 2023-24 North Middletown matched the statewide elementary average in reading (45 percent proficient "
  "or better against 47) and beat it in mathematics (45 against 42). In 2024-25 it beat the state "
  "decisively in writing (56 against 43) and science (53 against 37). Most striking for a school where "
  "about three-quarters of children qualify for free or reduced-price meals: on the third-party index, its "
  "economically disadvantaged students alone rank in the 62nd percentile of all Kentucky schools. This "
  "environment lifts precisely the students the research says are hardest to lift.")
P("This is not a new story. In 2011 the U.S. Department of Education named North Middletown Elementary a "
  "<b>National Blue Ribbon School</b>, one of just five Kentucky public schools honored that year, an "
  "award for schools in roughly the top ten percent of their state in reading and mathematics. The state "
  "separately gave it an inaugural Distinguished Winners Circle Award. Around then the school ranked 36th "
  "of 683 Kentucky elementary schools (2010) and 51st of 688 (2011). This is not a school with a history "
  "of failure. It is a school with a history of excellence, climbing back toward it.")
P("The record was built by people, and two anchor it: Mrs. Beverly Craycraft and Mrs. Roxanne Mitchell, "
  "whose classrooms set the kindergarten-through-fifth standard for generations. The honors around them "
  "are documented: Alison Cloyd (2014) and Lydia Austin (2017) each received Campbellsville University's "
  "Excellence in Teaching Award, and the Blue Ribbon culture ran on community-powered programs, notably "
  "“ArtBurst,” which threaded the arts through core academics. The present belongs to a new set of "
  "educators. Under principal Hannah Southall the staff took the school from its COVID-era trough back to "
  "the county's best official overall rate, 74.5 in 2023-24, and the county's top marks in every "
  "state-reported subject in 2024-25, and keeps a gifted-and-talented program running. That faculty does "
  "not need consolidation. It needs time, and a district willing to back them.")
P("Two honest caveats. Small schools produce noisier year-to-year scores, and subgroup results vary "
  "widely: the school's girls (85.7, the 91st percentile) far outpace its boys (28.8), a gap the "
  "district should be helping the school close rather than closing the school. And no single year should "
  "define any school. Three-year averages tell the same story: on the third-party index North Middletown "
  "averages 48.1 for 2023 through 2025, against 26.4 at Bourbon Central and 29.9 at Cane Ridge. Neither "
  "caveat changes the central fact: this consolidation would move children from the district's strongest "
  "elementary environment into its weakest ones. If the administration believes the receiving schools "
  "can preserve these outcomes, it should say so in writing, with a transition plan, before any vote.")


fig("chart_district.png",
    "Figure 1. Top: the official state record, Kentucky's overall accountability composite in its two "
    "comparable eras (Unbridled Learning overall score, 2012-2016; KSA overall indicator rate, 2022-2025). No "
    "composite was issued from 2017 through 2021 (system transition, star-rating years, then COVID), and "
    "CATS-era school files (2006-2011) are available from KDE by data request. Bottom: SchoolDigger's "
    "third-party 0-100 index of the same tests, retained for context; wherever the two disagree, the "
    "official record governs. Sources: KDE historical datasets, archived in this repository as "
    "build/kde_scores_history.json.")
fig("chart_compare.png",
    "Figure 2. SchoolDigger's normalized 0-100 index for 2024-25 across the region's elementary schools, computed from state test data (not KDE's official rating). Montgomery County operates four elementaries; the two with retrieved index values are shown, and Montgomery "
    "County's two elementaries outscore North Middletown; every elementary in Bourbon County, Clark County, and "
    "Paris Independent trails it.")

# ================= 3. NOT EXPENSIVE =================
H("3. The School Is Not Expensive: The Cost Record")
P("The headline belongs first, because it is the newest number in the record. On the state's newest "
  "school spending file, 2024-25, posted after the July committee citation, North Middletown costs "
  "<b>$17,903 per student</b> against a Kentucky elementary average of $19,299: <b>7 percent below the "
  "state average</b>, and below it in five of the eight modern-era years. The district's own "
  "cost-of-delivery table, dated May 21, 2026, lands in the same place: $19,080 per student against a "
  "$19,020 state average on the same sheet, a gap of three tenths of one percent. Read every older figure "
  "in this section, including the 2023-24 numbers the July citation used, with that newest file beside "
  "it.")

H2("What this school has cost, in every year the state has ever measured it")
P("The cost argument rests on one recent number, so we assembled every school-level cost figure in any "
  "state or federal record, through the newest 2024-25 file: three reporting systems reaching back a "
  "quarter century, each archived in the repository. The oldest are the 2000-01 state report cards, "
  "recovered from the Internet Archive. They show all four of the district's then-elementaries on a "
  "single scale curve: about $2,851 per student plus a fixed base of about $332,000 per building, spread "
  "over however many children the zone lines assign to it. That one formula predicts every school within "
  "4 percent: Bourbon Central $3,360 at 595 students, Cane Ridge $4,053 at 312, North Middletown $4,414 "
  "at 193, Millersburg $5,200 at 145. No school on that list was mismanaged; the ranking is enrollment. "
  "In every year measured, the cheapest school in the county has been its biggest.")
P("The middle years confirm it: KDE's report-card datasets for 2011-12 through 2016-17 show the premium "
  "widest exactly when the building was emptiest, and two federal collections that measured school-level "
  "salaries independently show the same pattern. The record even holds a controlled experiment. "
  "Millersburg's premium over its receiving school was about $166,000 a year on the 2000-01 report "
  "cards; the district closed it in 2006; the thirty-year record shows the budget did not measurably "
  "bend. North Middletown's premium today is $156,000: the same experiment at almost the same number, "
  "twenty-three years apart. Provenance: CATS-era cards may report prior-year spending, which does not "
  "affect within-year comparisons; the 2012-13 file prints $19,635 in a renovation year, a capital "
  "charge excluded from operating comparisons; and the three systems use different definitions, so every "
  "comparison is within one system in one year. The School_Costs tab carries it all live.")

# ================= 4. MILLION DOLLAR QUESTION =================
H("4. The Million-Dollar Question: What Closing the School Would Actually Save")
P("The case for closure rests on a single public statement: that keeping North Middletown Elementary open "
  "\u201ccost over a million dollars last school year.\u201d No worksheet for that figure has ever been "
  "released. The district's later 48-page response prices a different, smaller number, $661,138.94, which "
  "this section takes apart below. The state's own spending data put the million-dollar figure in "
  "context.")
P("North Middletown's $19,348 per student is the highest of the three elementaries. That is exactly "
  "what the math predicts for a small school: one principal, one office, one kitchen, and one heated "
  "building divide across 128 children instead of 450. Multiplied out, the federal report puts about "
  "$2.5 million against this school, roughly $1.8 million of it state and local money. That is an "
  "allocated figure, not a site ledger. On the same 2023-24 basis the report showed $2,611,980 for "
  "North Middletown, while the district's working budget coded $1,593,309 to the school that year, "
  "about $1.0 million less. (The report's $19,348 rate at the 135 students then reported; at today's "
  "128 the same rate gives the $2,476,544 the cost case rests on.) The difference is central office, "
  "district transportation and district instructional support that no closure removes. And almost none of that total is what a "
  "closure would save, for a simple reason: <b>closing a school does not delete its students.</b>")
fig("chart_pp.png",
    "Figure 3. Per-student spending at the district's three elementary schools, 2023-24, as published in "
    "the Kentucky School Report Card's school-level expenditure data (total of state, local, and federal "
    "dollars). The newer 2024-25 file puts North Middletown 7 percent below the Kentucky elementary "
    "average (Section 3).")
fig("chart_capacity_scenarios.png",
    "Figure 4. Every school filled to its rated capacity, priced with step variable costs ($400 of supplies per "
    "student added or removed, plus or minus an $85,000 loaded section wherever KRS 157.360 class caps require "
    "one), on the district's 2023-24 state filings. Seven capacity sets, all from the district's own documents "
    "or federal data: today's actual enrollments, the three state-approved plans (2013, 2017, 2021), each school's twenty-year peak "
    "enrollment, the district's own architect's 2026 KFICS capacities, and the unapproved 2026 draft table. "
    "North Middletown comes out cheapest under the 2013 plan, the 2021 plan in force, the twenty-year peaks, "
    "and the architect's own numbers; Bourbon Central comes out cheapest under today's actuals, the 2017 plan, "
    "and the draft table. The 2017 plan, recovered from the Internet Archive and corroborated by the June 7, "
    "2017 state board minutes, rated North Middletown at 152 seats with 154 enrolled: the school now described "
    "as half empty was listed OVER capacity nine years ago.")
P("Five years of the district's filings say the same thing in time series. North Middletown's total "
  "site spending grew the <b>least</b> of the three elementaries: up about 16 percent since 2019-20, "
  "against 35 to 37 percent at Bourbon Central and 46 to 47 percent at Cane Ridge, under either "
  "base-year count. Per student, the same filings put all three schools up 49 to 53 percent since "
  "2019-20, within four points of each other, North Middletown in the middle: a district-wide cost "
  "trend, not one building's. What grew at North Middletown is the empty space around each student as "
  "enrollment slid from 166 to 128. Divide a nearly flat cost by a shrinking class and the per-student "
  "figure climbs. That is division, not an expensive school. Fill the seats and the division runs in "
  "reverse: at 174 students the per-student cost drops to between $14,339 and $15,316 depending on "
  "staffing, about $14,827 at the one-added-section default this version prices, $3,300 to $3,800 under "
  "either receiving school. And the students who fill it come from the exact schools over or near their "
  "rated capacity today.")
P("The capacity ratings deserve scrutiny they have never gotten. The same three unchanged buildings have "
  "been rated wildly differently by four consecutive plans: North Middletown 198, then 152, then 174, "
  "then the draft's 154; Bourbon Central 564, 611, 521, 640; Cane Ridge 500, 550, 422, 547. No major "
  "construction happened at any of the three after 2009. Ratings that swing by up to 128 seats between "
  "cycles are policy choices, not walls. The cost conclusion is validated against actuals two ways. At bare supplies "
  "($400), the filled school runs $14,339 at the approved 174 rating and $16,149 at the draft's 154; "
  "with class-cap staffing, $15,316 and $16,701. All four land below both receiving schools. The bound "
  "that matters: North Middletown stops being cheaper than Bourbon Central only if each added student "
  "costs more than $14,745 at 174, or more than $12,140 at 154. Priced the way we price everything else, "
  "an added student costs about $2,250 to $4,100. This version withdraws the earlier third validation, a "
  "two-school cost slope whose sign depended on an unpublished membership pair. In the pandemic-aid "
  "years the filled school would have run within 1 to 3 percent of the others, a tie; in the current "
  "cost structure the result is not close.")
P("One symmetry we apply to ourselves: per-student numbers move wherever the students move. Send "
  "students out of Bourbon Central and Cane Ridge and their per-student costs rise for the same "
  "denominator reason. A pure shuffle leaves total district spending nearly unchanged either way. Cost "
  "per student is a utilization measure, not a verdict on a building, and after the move a filled North "
  "Middletown is still the cheapest of the three. Run the other way, closing North Middletown would "
  "improve the receiving schools' per-student optics while saving almost nothing in total.")
P("The 115 children would still need teachers, about six homerooms' worth (eight to nine certified "
  "position-equivalents priced by ledger dollars), and Bourbon Central (459 students) and Cane Ridge "
  "(453) would each absorb roughly 57 more children across six grades. Their SEEK funding transfers "
  "with them; food service, self-supporting, follows the meal counts. What is genuinely avoidable is "
  "the fixed cost of running the building, and only if it is sold or fully repurposed rather than "
  "mothballed. Against those savings run the new costs: longer bus routes in the district's "
  "fastest-growing and worst-reimbursed budget line (families have warned of rides over two hours a "
  "day), staffing or space additions at the receiving schools, transition costs, and the quiet risk "
  "that some families leave the district altogether. Each departure takes at least $4,626 a year in "
  "base state funding, permanently (the fiscal 2027 base, the first year a closure could take effect; "
  "we use the fiscal 2027 figure for anything after a closure).")
P("First, the staffing price, stated plainly. $85,000 is the right all-in figure for comparing "
  "spending filings, but the wrong figure for the General Fund. Kentucky pays teacher retirement and "
  "health insurance on behalf of districts, so the General Fund keeps only salary plus roughly five "
  "percent when a position goes away: <b>$50,000 to $75,000 per position, not $85,000</b>. We go further and "
  "retire even that band. Every staffing lever is priced at the district's own fully loaded figure, "
  "<b>$54,479.40 per position</b>, from Appendix A.1 of its written response. Their number, their "
  "basis.")
P("The grid is built on the district's 48-page response and the community's survey. Six levers, each "
  "sourced. One: how much of the district's own $107,039 of building-bound expense lines actually stops "
  "(50 to 100 percent, plus its $20,000 insurance figure at the full stop). Two: how many of the four "
  "whole fixed positions are cut over time rather than retained (its appendix retains all staff in year "
  "one; the school council allocation lists 5.5; the three half-time lines stay uncut). Three: zero to "
  "three teachers at its own $54,479.40 price (its savings sheet says two, its own classroom-capacity "
  "count supports three). Four: the students missing from the rolls each year, anchored to the signed "
  "school-choice survey at steady state (117 to 154, Section 5; the signed floor of 74 (the 70 signed children spread over their twelve class cohorts, 5.83 per class, carried 12.62 effective years), the 31 "
  "households alone, sits below every priced leg as hard evidence, not a scenario). Five: each missing "
  "student "
  "costs the enacted FY2027 SEEK base of $4,626 plus up to $1,000 of add-ons, minus the $400 of "
  "supplies that stop, the same figure the growth model charges each recruit. One mechanic, stated "
  "plainly: SEEK pays on the prior year's average daily attendance, about 91 percent of end-of-year "
  "enrollment here, so the base alone prices a leaver near $4,200; the formula's at-risk, "
  "exceptional-child, language, and transportation weights, mostly uncounted in our $500 add-on, are "
  "worth roughly $1,000 to $2,200 more per student on the district's own KDE file, so our per-child "
  "price leans low; teacher savings appear "
  "ONLY on the teachers-cut lever, so staffing is never counted twice. Six: the added busing a "
  "110-square-mile zone requires, its high leg capped at half the route-split bottom-up maximum of $190,000. A property-value "
  "lever from an interim draft is removed while the PVA records request is pending; the property "
  "research stays in Section 6. build/closure_grid.py enumerates every combination, 972 in all, lever "
  "by lever in the workbook. Each lever carries a distribution: where the record pins a central setting "
  "(the derived $63,000 busing figure, the ~$500 of add-ons, the middle reads of the building and "
  "staffing-path levers), that setting counts double, a triangular 1-2-1 weight; teachers cut stays "
  "uniform; the leaver lever is triangular on the band's quartiles. The result is Figure 5. The net "
  "yearly effect falls between <b>losing $846,285 and still losing $9,860</b>. The middle half of "
  "weighted scenarios lands between a $518,405 and a $338,727 loss. The median outcome <b>LOSES "
  "$427,087 a year</b>, and every priced scenario loses money outright, before $100,000 to $300,000 of "
  "one-time transition costs in year one (unweighted, the median is a $425,053 loss; no conclusion "
  "changes). The plan's own requirement, the superintendent's stated need to free up $800,000 to "
  "$1,000,000 a year of operating money to bond a $14 million renovation, sits entirely outside the "
  "range. And closure buys no borrowing room: bonding capacity is built from restricted revenue streams "
  "that do not grow when a school closes (Section 8).")
P("<b>Year by year, not just steady state.</b> The exodus builds: six grade cohorts short in year "
  "one, all thirteen by year eight. Priced against the calculator's own generous default (building "
  "sold, three teachers cut, half the fixed positions cut, $63,000 of busing), the ledger runs:")
tbl(["Year", "Students missing (median path)", "Net yearly effect"],
    [["Year 1", "65", "+$27,339"],
     ["Year 2", "75", "-$19,921"],
     ["Year 3", "86", "-$71,907"],
     ["Year 4", "97", "-$123,893"],
     ["Year 5", "108", "-$175,879"],
     ["Year 6", "119", "-$227,865"],
     ["Year 7", "129", "-$275,125"],
     ["Year 8 on", "136", "-$308,207"]],
    [1.0*inch, 2.6*inch, 2.0*inch])
P("Closure is cash-positive exactly once, in year one, by $27,339, and the one-time transition cost "
  "of $100,000 to $300,000 erases that by itself. From year two the closure is under water and "
  "sinking; from year eight it loses $308,207 every year at the median, and the weighted grid median "
  "across all lever settings is worse, $427,087. The district's year-one framing prices the only year "
  "that ever looks close.")
fig("chart_closure_spectrum.png",
    "Figure 5. The honest range. Top: the net yearly effect of closure across all 972 combinations of "
    "the six sourced inputs, from losing $846,285 to still losing $9,860, the middle half of "
    "weighted scenarios between a $518,405 and a $338,727 loss, the median a $427,087 loss. The plan's "
    "own $800,000 to $1,000,000 requirement lies entirely outside the range. Bottom: how far each input "
    "moves the central case by itself. Inputs: the district's response worksheet and staffing appendix "
    "(Appendix A and A.1), its capacity appendix, its KDE filings, the federal attendance-zone map, and "
    "the exit routes under HB 563, homeschooling, and the statewide virtual academy; every lever and "
    "formula is in the Closure_Model tab.")
H2("What the families said: the school-choice survey")
P("In early August 2026 the community asked NMES families the question the district's plan never "
  "prices: if the school closes, what would your family actually do? Forty-two responses came in. "
  "Counting one further family with one child received after the form closed, <b>38 households "
  "answered for 85 children.</b> Duplicates were removed by hand, three households known to be staying "
  "were recoded, and one family that already left was set aside. The cleaned result: <b>31 households, "
  "with 70 children, say they would leave Bourbon County Schools</b>; 6 households (13 children) say "
  "they would stay. The 70 signed-out children are 82 percent of the 85 surveyed "
  "(surveyed children include current students, younger siblings, and children not yet in school). Where would they go? Montgomery County Schools 25, "
  "other or undecided 20, homeschool 16, private school 8, Clark County Schools 1. The "
  "other-or-undecided count includes seven children marked with a public school in this district; "
  "because their families say they would leave Bourbon County Schools, they are counted there, and the "
  "published data carries that coding. The anonymized data, every name and date removed, is published "
  "at build/survey_school_choice_2026_08_anonymized.csv; personal information is never published.")
P("Their named destinations are real and open today: Montgomery County, Clark County, homeschool, "
  "private school. The survey is read as a share of the school, not as per-class counts. The hand-coded "
  "kindergarten class years mark only which children are enrolled now, and no per-class math is "
  "published from them (a v5.0 method change, disclosed in the version history; earlier drafts derived "
  "a per-class floor). A child who leaves is missing for every remaining grade. The district's "
  "grade-to-grade records show 95 to 100 percent of county fifth graders enter its middle school and "
  "stay through 11th grade, senior-year survival 83 percent, so each lost child counts for 12.62 "
  "effective years rather than a flat 13.")
P("The statistical estimate corrects the survey for the obvious bias: families set on leaving answer a "
  "survey like this more readily than families staying put. Among surveyed children enrolled now or entering "
  "within the next three falls, the raw split is 62 leavers to 13 stayers, about two fifths of the "
  "eligible pool; the three-class window means a miscoded class year cannot move the sample. A "
  "response-propensity model discounts that split across leaver-to-stayer response ratios from 3.3x "
  "to about 9x, centered on 3.5x. "
  "The result: a true leave share with a median of 50 percent, middle half 43 to 57 percent. Applied to "
  "the 115 students enrolled today, that is <b>49 to 65 children in the building right now</b>. "
  "Extended to the entire NMES feeder stream, each entering class of about 22 (ten-year SAAR "
  "kindergarten average 22.2; recent per-grade range 19 to 24) carried for 12.62 effective years, it is "
  "<b>117 to 154 students missing from the rolls each year at steady state, $599,742 to $789,404 a "
  "year</b>, with a 95th-percentile bound near $912,000. Losses build from six grade cohorts in "
  "year one to all thirteen by year eight. build/exodus_model.py reproduces every number from the "
  "published data. The correction range is anchored to published measurements of exactly this bias, all "
  "in Sources. Groves, Presser, and Dipko (2004) measured interested groups answering 1.4 times more "
  "readily. Abraham, Helms, and Presser (2009) measured engaged people answering a follow-up survey "
  "1.35 times more readily. Pew's benchmark studies (2012, 2017) find civically engaged people "
  "over-represented at implied ratios of roughly 3 to 4. The model's 3.3x-to-9x span sits in the top half of that "
  "measured band, 1.4x to 4x, and runs far past it: it refuses every ratio below Pew's lower high-salience "
  "benchmark. The central 3.5x is pitched near the top of the published record on "
  "purpose: a small, emotionally charged pool answering a zero-effort form circulated by the campaign "
  "itself is exactly where this bias runs strongest. The model leans against its own survey.")
P("The state's own files corroborate the band from outside the survey. The SAAR school-level "
  "enrollment reports, archived here, show NMES ending 2023-24 with 141 students, 2024-25 with 128, "
  "and 2025-26 with 115. This year's kindergarten enrolled <b>12 children against a ten-year average of "
  "22</b>: the front-door defection the survey predicts, already visible in the district's own state "
  "filings before any closure vote. And if the skeptic's reading is right, that the entering class "
  "settles near 15 rather than 21.5, the priced pipeline shrinks but the conclusion holds: at a "
  "15-child class the median exodus is still 95 students, about $487,000 a year. One label is corrected in this release: the facility plan's '128', previously "
  "described as the district's 2023-24 SAAR figure, matches the state's 2024-25 SAAR end-of-year "
  "membership file exactly (as does Cane Ridge's 461). End-of-year enrollment is the planning manual's "
  "own basis; the state's 2023-24 file shows 141.")
P("Where inter-district choice is already open, the aftermath is on the record. Council Bluffs, Iowa "
  "closed rural Crescent Elementary in 2023: 127 school-age children lived in its zone, only 49 still "
  "attended, and after the closure the town's students scattered to homeschooling, neighboring "
  "districts, and a new charter school founded to replace it. Wisconsin's Palmyra-Eagle district lost "
  "up to 40 percent of its students to open enrollment and its board voted to dissolve the district (a state panel later kept it open). "
  "Iowa's Orient-Macksburg watched 53 percent of its certified enrollment open-enroll out and dissolved "
  "in June 2025. Wisconsin's River Valley closed two rural elementaries in 2017 and 2018 for projected "
  "savings; seven years later, still shrinking, it closed its third and last satellite campus and went "
  "to referendum to survive. In Nebraska, Scottsbluff administrators conceded in 2026 that closing "
  "their last country school was unlikely to save much money if a critical mass of its students "
  "transferred out. No Kentucky district has yet closed a rural elementary in the HB 563 "
  "open-enrollment era and published the aftermath; Bourbon County would be the experiment. Sources for "
  "every case are in the back matter.")
P("These cases also answer the objection that families say one thing and do another. They are measured "
  "behavior, not promises. Our corrected band, 43 to 57 percent with a median of 50, sits between the "
  "40 percent Palmyra-Eagle actually lost and the 53 percent Orient-Macksburg actually lost; 61 percent "
  "of Crescent's zone had stopped attending before the school closed. The survey, after our discount, "
  "predicts what comparable communities already did.")
P("<b>What would prove us wrong.</b> We publish the test in advance. If this fall's kindergarten "
  "returns to the ten-year average of 22 and end-of-year enrollment holds near 115 with the school "
  "open, the decline story weakens. If the school closes and fewer than 49 students, the band's low "
  "edge for today's enrollment, leave in the first year, the survey band overpredicted and this "
  "model's central conclusion fails. The SAAR files we cite will answer either way, and we will "
  "publish that answer whichever way it falls.")
P("Leaving is not pure loss, and the model credits the savings without double counting: the supplies "
  "credit scales with every child who goes, and teacher cuts are priced only on their own lever. Even "
  "with both credits at their friendliest, every priced scenario loses money. $400 of supplies and a "
  "few positions cannot outrun $5,126 walking out with every child.")
P("The research says this dynamic is structural, not local. Georgetown's Edunomics Lab documents "
  "per-pupil revenue leaving with each lost student while costs fall only in steps (Financial Impacts "
  "of Enrollment Decline, 2021); Bellwether's national data show the same squeeze. Georgetown's FutureEd "
  "finds kindergartners are the largest entry group in school-choice programs, over a third of annual "
  "participants: K-5 is where districts win or lose families, and this district's grade-to-grade "
  "records show families almost never leave once enrolled. Research for Action's 2024 review finds "
  "closures rarely save what districts project, with enrollment loss to other systems a recurring "
  "result. All four are in the Sources.")
H2("What the district's own ledger says this school costs")
P("In July 2026 the district answered an open records request and produced its books. What North "
  "Middletown costs moves by about a million dollars depending on which of its own documents you open.")
P("The 300-student breakeven, and every version of the cost case against this school, rests on "
  "$2,476,544, which comes from the federal per-student report and spreads district-wide costs across "
  "buildings. The district's own <b>Overall Cost by ORG</b> summary codes <b>$1,285,310</b> to North "
  "Middletown. Its FY2026 working budget codes <b>$1,706,493</b> to location 090, the school's own code, "
  "of which $406,333 is the state's on-behalf pension and health payments, not district cash. The two "
  "documents reconcile: $1,706,493 less on-behalf is $1,300,160, within 1.2 percent of the Cost by ORG "
  "figure. Like for like, same year and same all-in definition, the federal report put $2,611,980 "
  "against the school for 2023-24 while the working budget coded $1,593,309 to location 090 that year. "
  "The difference, $1,018,671, is central office, district transportation, the maintenance pool and "
  "district instructional support that no closure removes. One number puts the scale in view: of the "
  "$41.8 million of all-funds spending in the fiscal 2025 audit, the district codes $21,482,445 to any "
  "school at all.")
tbl(["School", "Coded by the district", "Enrolled", "Breakeven at $15,983", "Clears by"],
    [["North Middletown", "$1,285,310", "128", "80", "48"],
     ["Bourbon Central", "$4,033,689", "459", "252", "207"],
     ["Cane Ridge", "$4,326,733", "453", "271", "182"],
     ["Bourbon County Middle", "$3,868,106", "590", "242", "348"],
     ["Bourbon County High", "$5,515,105", "766", "345", "421"]],
    [W * 0.28, W * 0.22, W * 0.14, W * 0.22, W * 0.14],
    caption="The corrected average-cost test (all-in cost against the district's full $15,983 revenue per "
            "member), run on the cost the district's own ledger codes to each school rather than the cost "
            "the federal report allocates to it. Every school clears, and that is the finding: the answer "
            "swings from 300 to 80 students on the definitions of cost and revenue used, so the "
            "definitions should be chosen and published before any vote. Source: Overall Cost by ORG, "
            "produced July 2026; enrollment as elsewhere. Model, School_Costs tab.")
P("The working budget's location view cuts against this report in one place. Measured on all dollars "
  "coded to each school there, including the on-behalf entries this report strips elsewhere, North "
  "Middletown runs <b>$13,332</b> per student against $12,167 at Cane Ridge and $11,882 at Bourbon "
  "Central. Those are premiums of 9.6 and 12.2 percent, against 3.6 and 6.7 percent on the federal "
  "all-in basis. "
  "Equally allocated overhead narrows every gap, so the direct-coded comparison shows a wider one. The "
  "dollar premium is $149,000 to $186,000 a year, still smaller than this school's ledger-actual fixed "
  "base of $293,316. That is the scale argument in the district's own numbers: a fixed base spread over "
  "few students, not a school that overspends.")
P("Of the $1,706,493 coded to the school, on-behalf payments ($406,333) are not district cash, federal "
  "grants ($191,048) follow the child, and food service ($170,423) is self-supporting from meal "
  "reimbursement. That leaves the General Fund. The district's MUNIS ledger, the 203-page Cost by ORG "
  "detail archived here, shows what the school actually spent from it in fiscal 2026: <b>$933,537</b>, "
  "within 0.55 percent of the working budget's $938,690, most of it teacher salary payable again at "
  "the receiving school. By function: regular classroom instruction $474,956; other "
  "instructional programs $128,036; school administration $115,397; the building itself, utilities, "
  "disposal, telecom, supplies and repairs, $79,211; custodial pay and benefits $49,655; library and "
  "media $49,052; student health $33,664; transportation and other $2,893; and $673 of special "
  "education, because that staffing is carried at the district office. The district's worksheet reaches "
  "the same neighborhood by its own route, $107,039 of avoidable lines plus $20,000 of busing; the "
  "$27,828 gap from the ledger's $79,211 is insurance and lines the ledger books district-wide. So we "
  "use $79,211 for the staff-retained case and $127,039 when the building sells. The parse reproduces "
  "the ledger's own org totals to the penny; build/munis_extract.py reruns it. The same ledger makes "
  "the per-position estimate measured: on-behalf payments coded to the school total $406,333 against "
  "$1,497,576 of salary and benefits, a 27.1 percent load, putting the General Fund share of an all-in "
  "$85,000 position at about $66,860. The school's classroom payroll line of $324,550 over 4.9 to 5.8 "
  "teaching positions works out to $56,000 to $66,000 each. Three routes, one answer, at the middle of "
  "the $50,000 to $75,000 range this report already uses.")
H2("Where the superintendent's $661,139 comes from, and why it may never show up")
P("The district's response prices closure savings at “$661,138.94 MINIMUM.” Take it apart block by "
  "block. The claim is $493,407 of staffing priced with benefits, "
  "$40,693 of supplies, books and field trips, and $127,039 of building costs and insurance ($107,039 "
  "plus $20,000): $493,407 + $107,039 + $20,000 + $40,693 = $661,139. The same response states all "
  "current staff would be retained, so the staffing block saves $0 in year one. The supplies are spent "
  "wherever the children sit. The $127,039 that remains is the same building money the ledger walk above "
  "already counts. The response prices no added busing and not one leaving family. Those costs are "
  "real, so we price them: about $63,000 a year to bus the children to Paris, and one family in ten "
  "leaving (13 students at $5,126 each is $66,638 a year of state money). And the analysis behind the "
  "number? Asked for any cost-benefit analysis of closing the school, the district's July 2026 records "
  "response answered N/A: none exists.")
P("Two conclusions follow. First, the closure model estimated the school's avoidable fixed base at "
  "$230,000 mothballed and $290,000 sold. Measured, school administration plus custodial plus the "
  "building's own lines total <b>$244,263</b> on the MUNIS ledger's FY2026 actuals ($227,831 on the "
  "earlier working-budget program view). Every fixed line including the library totals <b>$293,316</b> "
  "on the ledger ($276,928 on the budget view). Both estimates land within seven percent of the "
  "measured record. Second, <b>$230,000 is the floor of the grid, not a floor case</b>: "
  "reaching it requires the principal, the secretary, the custodian and the utilities all to go, and "
  "districts frequently redeploy people rather than cut them. So version 3.9 rebuilt the grid on "
  "measured fixed lines, moving the median from $91,240 to $21,571. The district's written response "
  "then answered the open question directly: all current staff retained, savings only through "
  "attrition, avoidable expense lines of $107,039 plus $20,000 of insurance. Version 4.2 rebuilt the "
  "grid on the district's own figures, flipping the median negative. Version 4.5 added the lever "
  "weights above and re-based the fixed-position lever on the ledger's FY2026 actuals ($214,104 against "
  "the budget's $218,154); the published median was a $20,007 yearly loss, 55 percent of scenarios "
  "losing money. Version 5.0 replaces the leaver guess with the measured survey at steady state and "
  "embeds the supplies credit in the leaver term: 972 scenarios, median a $427,087 yearly loss, every one losing "
  "money.")
P("There is a limit to what any ledger can settle. The six levers that decide a closure's net effect "
  "span about $836,000. The district's books speak to two of them, worth about a third of that spread. "
  "The rest are decisions, not accounting: how many families leave, whether the building is sold or "
  "mothballed, whether the receiving schools need capacity work, how far the buses go, and whether staff "
  "are cut or moved. The range is wide because the decisions are open.")
P("The same records response contains a staffing document that answers the scale question from the other "
  "direction. The School Council Allocation for 2026-27 gives North Middletown <b>5.5 fixed "
  "positions</b>: a principal, a secretary, a custodian, one paraprofessional, and half a librarian, half "
  "a housekeeper and half a library aide. No assistant principal. No counselor. Bourbon Central receives "
  "12.25 fixed positions and Cane Ridge 11.5, each with an assistant principal, a counselor, three "
  "paraprofessionals and two secretaries. Per hundred students that is 4.3 fixed positions at North "
  "Middletown against 2.6 at the receiving schools. We print that ratio because it is the first thing a "
  "critic would compute. It is also the whole scale argument: a building needs one principal and one "
  "office whether it holds 128 children or 460, and the leanest-staffed school in the county is the one "
  "proposed for closure. (Its teacher column is enrollment divided by the KRS 157.360 statutory cap, a "
  "floor, not a roster; we do not use it as a staffing count.)")


# ================= 5. WHAT CLOSURE RISKS =================
H("5. What Closure Risks: The Record Where It Has Been Tried")

H2("Bourbon County has run this play before: Millersburg, 2006")
P("Millersburg Elementary, about nine road miles from Paris, closed in 2006 with a final enrollment of "
  "119 students, nearly the size of North Middletown today. Its students went to Cane Ridge, whose "
  "addition the facility plan dates to 2007. What happened next is on the census rolls, Figure 6: "
  "Millersburg fell from 842 people in 2000 to 792 in 2010 to 747 in 2020, down 11 percent, while the "
  "county grew 4.6 percent. No single closure did that alone: the private Millersburg Military "
  "Institute shut permanently the same July, and the Joy Global plant followed in 2013, taking 197 jobs "
  "and, by the town's own accounting, half its operating budget. The honest lesson is worse, not "
  "better: small towns lose their anchors in cascades, each loss making the next more likely. Twenty "
  "years later the district is over capacity at the school that absorbed Millersburg's children and "
  "proposes to solve it by closing another small school. North Middletown's attendance zone holds "
  "2,625 people. The records ask writes itself: produce the 2006 savings analysis and the savings "
  "actually realized, before the same projection is made again.")
fig("chart_millersburg.png",
    "Figure 6. Millersburg and Bourbon County population, indexed to 2000, with the town's three institutional "
    "losses marked. The elementary's 2006 date is its federal record: enrolled through 2005-06, status closed "
    "in the 2006-07 CCD universe file; the military institute is a separate, private school that closed "
    "permanently in July 2006. Decennial census counts: Millersburg 987, 937, 842, 792, 747; the county "
    "grew 4.6 percent from 2000 to 2020.")
H2("Has this ever worked in Kentucky? We checked all thirty years")
P("From the federal Common Core of Data, every Kentucky public school, every year, 1994 through 2023, "
  "we built the complete record. It holds <b>339 rural and small-town school closures since 1995</b>, "
  "after screening out renames, rebuilds under new federal IDs, and non-community programs, and <b>72 "
  "towns that lost their last public school entirely</b>. Millersburg 2006 is one of them, which "
  "independently validates the method. The full lists and inputs are archived here. Three findings "
  "follow.")
P("<b>First, the money.</b> For the 163 closure events with clean finance data, we compared each "
  "district's spending from the year before closure to three years after against the statewide trend, "
  "credited the ENTIRE gap to the closure, the most generous reading, and priced it per displaced "
  "student. The median closure produced <b>$1,102 per displaced student</b> ($818 among the physically "
  "plausible cases), and <b>40 percent of districts spent MORE than trend after closing</b>. Both "
  "tails hold events beyond $13,000 per child, more than any school costs to run: budget-wide noise, "
  "not closure effects. The raw median for the 27 closures most like this plan prints $8,440; the same "
  "artifact, and inside the plausible window that median is <b>$541</b>. The yardstick: this plan "
  "needs <b>$6,957 to $8,696 per displaced child</b>, at the record's 75th percentile and above. The one "
  "clean rural comparable with nothing built, Webster County's closure of Slaughters Elementary in "
  "2012, paid $3,525; the strongest rural-elementary case, Adair County in 2006 at $6,935, still falls "
  "short of the band, and it built a new school. The record's figure is an "
  "upper bound by construction. Our bottom-up model prices only the levers a closure moves, and its "
  "median is a $427,087 yearly LOSS, about $3,714 per displaced student below zero. The plan's "
  "requirement is six to eight times the record's median and unreachable by our own model, whose best case is "
  "itself an $86-per-displaced-student loss.")

P("<b>Second, the classrooms.</b> Test scores can only be compared within one accountability system, so "
  "we tested the 42 closure events measurable inside the 2012 to 2019 window on the uniform federal "
  "proficiency series. Eleven districts improved three or more points against the state, ten declined, "
  "twenty-one were flat: a wash, median half a point down. Inside the wash the pattern points one way: "
  "the more children displaced, the worse the trend. The improvers were overwhelmingly small closures "
  "inside eastern Kentucky's broad mid-decade testing rebound, gains far too large for schools that "
  "were one to eight percent of their districts to explain. Exactly <b>one</b> event shows both clear "
  "savings and clear gains: Leslie County 2013, which folded its middle school into an existing campus "
  "in the same community. No case shows a district closing a rural town's elementary school, clearly "
  "saving money, and clearly improving scores.")

P("<b>Third, the two best cases, disclosed by us so no one has to discover them.</b> Perry County "
  "closed three rural elementaries in 2017 and shows real, modest savings, about $3,600 per displaced "
  "student, with scores continuing an earlier climb; it built the new West Perry Elementary for the "
  "children it moved. Johnson County closed 178-student Meade Memorial Elementary in 2016 with nothing "
  "built; spending ran about six points under trend while scores stayed flat, in proportion to the "
  "school's five percent share of the district, our own model's median arriving on schedule. Neither "
  "resembles what this plan promises. Two honest limits: closures before 2012 and after 2016 cannot be "
  "score-tested across Kentucky's assessment-system changes, and small towns that kept their schools "
  "declined at nearly the same rate as towns that lost them, so we make no claim that closure causes "
  "population decline. What the record shows is narrower and harder: no measurable precedent for the "
  "savings this plan requires, and none for academic improvement from a closure like this. If the "
  "board believes this closure would be the first in thirty years to beat that record, the analysis "
  "showing how would make the board's case, and we would welcome being wrong.")
fig("chart_ky_record.png",
    "Figure 7. Top: all 163 measurable Kentucky rural closures, priced per displaced student with each "
    "district's entire budget gap against the state trend credited to its closure; the shaded tails "
    "beyond $13,000 per child exceed what any school costs to run per student and mark budget-wide "
    "noise, not closure effects. Bottom: the rural elementary cases only. City and county-seat grade "
    "reshuffles (Somerset 1999; Montgomery 2018, which opened a new elementary the same year) appear in "
    "the top panel but are not comparisons for a rural closure. Data: build/ky_closure_events_full.csv "
    "(every event, every input), build/ky_rural_closures_1995_2023.csv, and "
    "build/ky_closure_dollar_cases.csv.", width=6.0 * inch)

H2("What happened when other districts tried this")
B("<b>Chicago, 2013.</b> The district closed about fifty schools projecting roughly $1 billion over a "
  "decade, including $43 million a year in operations. A 2023 Sun-Times and WBEZ analysis found actual "
  "labor savings of about $25 million a year, $18 million short, while the district borrowed $329 "
  "million to prepare receiving schools; a decade on, more than half of the 46 emptied buildings still "
  "sat unused. The University of Chicago's research consortium found displaced students' math scores "
  "depressed for up to four years.")
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
P("The costs to children pile on top of the costs to the budget. A 2024 national study following 470 "
  "Texas closures found displaced children, low-income children most of all, absent more often, "
  "disciplined more often, and earning less as adults. Roughly three-quarters or more of North "
  "Middletown's students qualify for free or reduced-price meals. If Bourbon County believes its closure "
  "would beat this record, the burden is on the administration to show the math.")
P("When the numbers are shown in public, four distinctions will help everyone read them the same way. "
  "Each can quietly make closure look better than it is: gross site cost presented as savings; "
  "restricted building dollars presented as operating relief; per-pupil cost cited without noting that "
  "state funding follows the student; district-wide cost growth pinned on one small school. We flag "
  "our own judgment calls where they occur.")
P("Whatever the true net number, one comparison frames the decision on either honest yardstick. Against the $2.6 million structural deficit before transfers, closing North Middletown "
  "addresses at best a small fraction. Against the roughly $1.15 million the district actually draws "
  "from reserves each year, even the fullest documented claim, the $493,407 staffing block, reaches about forty percent. Either way it "
  "is a partial fix, while the measures in Section 10 total more, harm no student, and close no town's "
  "school.")

# ================= 10. WHAT CAN'T BE QUANTIFIED =================
H("6. What Can't Be Quantified: A Town and Its Heartbeat")
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
P("Everything to this point can be argued in dollars. This section cannot, and belongs in the record "
  "anyway. North Middletown is a town of about 610 people. Its school has stood on College Street since "
  "1948, educating grandparents, parents, and children in the same classrooms; this month those "
  "children were invited to write love letters to it. When a place that small loses its school, it "
  "loses its largest engine of civic life: the gym where the town gathers, the stage for every "
  "concert, the reason young families give for staying.")
P("The research on what follows a closure is unusually consistent. Cornell sociologist Thomas Lyson, "
  "studying 297 rural New York villages, found that in the smallest of them, 500 people or fewer, the "
  "presence of a school went with home values roughly a quarter higher ($59,508 versus $47,782), better "
  "water and sewer infrastructure, and more residents working in town. He warned that money saved "
  "through consolidation \u201ccould be forfeited in lost taxes.\u201d A North Dakota State University study "
  "followed eight communities through consolidation: in the towns that lost their schools, businesses, "
  "retail trade, and participation in community organizations all declined. A 2022 Brown University "
  "analysis of Arkansas's forced consolidations estimated that affected communities lost 13 to 15 "
  "percent of their population and roughly $1,300 in assessed value per property, with communities of "
  "color hit hardest. And a case study of Limerick, Saskatchewan documented the quieter losses after a "
  "school closed: volunteerism, recreation, and the everyday ties between generations all frayed, felt "
  "even by residents with no children in school.")
P("There is a fiscal irony buried in that research: a district closing a school to protect its budget risks "
  "shrinking the very tax base the budget stands on. Property values, population, and local business activity are "
  "not sentimental line items. They are the assessment roll.")
P("The people closest to this school have already said what the studies measure. An alumna planning to "
  "enroll her own children told reporters that closing it \u201cjust makes no sense when the other schools "
  "are already so packed.\u201d Mayor Jeff McFarland calls closure \u201ca disservice to the community.\u201d None of "
  "this appears in a savings worksheet. All of it should appear in the Board's deliberation. A decision "
  "that counts only what is easy to count is not a complete accounting.")
A(Spacer(1, 6))
H2("A personal note from Dr. Ryan Bradley")
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
         "<br/><font size=8.6 color='#555555'>Dr. Ryan Bradley, a former NMES King and Bourbon County Colonel</font>")
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


# ================= PART TWO =================
H("Part Two: The District Needs Growth, Not Closures")
P("The district has a real money problem. It is district-wide, North Middletown did not cause it, and "
  "closing the school does not dent it. These sections size the problem from the audited statements, "
  "then price the three levers the board already owns.")

# ================= 3. FINANCES =================
H("7. The District's Finances: A Real Problem With Clear Causes")
P("We do not dispute that Bourbon County Schools faces genuine budget pressure. The district's own "
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
    caption="Figure 8. Three-year General Fund summary, from the district's audited financial statements for the "
            "years ended June 30, 2024 and June 30, 2025. The fiscal 2023 revenue figure reflects a different "
            "presentation of state pension payments made on the district's behalf and is shown for context. The "
            "fiscal 2024 change line differs from the balance movement by $840, a residual carried in the audit "
            "and noted in the companion workbook.",
    bold_first_col=True)

P("A note on the transfers line: “net transfers and other sources” of roughly $1.4 million a year are "
  "moves between the district's own funds, not new money. They cushion the reported change in fund "
  "balance. So the honest measure is the operating result before transfers: the district spends about "
  "$2.6 million more than it takes in, transfers cover roughly half the gap, and reserves absorb the "
  "rest. Which transfers can be sustained is a question the finance office should answer in writing.")
fig("chart_gf.png",
    "Figure 9. The operating gap and the drawdown. The district spends roughly $2.5 to $2.6 million more from its "
    "General Fund than it takes in before transfers, and reserves have fallen about $2.3 million in two years. "
    "Source: audited financial statements, FY2024 and FY2025.")
H2("Why it happened", need=2.0)

P("Three forces converged. One-time federal pandemic relief, the ESSER programs, wound down, taking "
  "about $2.95 million a year with it while the staff and programs it paid for remained. Average Daily "
  "Attendance, the basis of Kentucky's SEEK formula, fell from a pandemic hold-harmless 2,490 to 2,243, "
  "a recurring revenue loss on the order of $1.1 million a year at the fiscal 2026 base guarantee of "
  "$4,586 per student. And the new two-year state budget offers little relief: the SEEK base rises less "
  "than one percent in fiscal 2027, and state school-bus funding is frozen roughly $90 million a year "
  "below what Kentucky statute calls for, statewide.")
fig("chart_cliff.png",
    "Figure 10. The two revenue shocks. Federal revenue in the governmental funds fell $2.95 million from FY2023 to "
    "FY2025 as ESSER pandemic aid expired, and attendance-based state funding fell as funded average daily "
    "attendance dropped by roughly 247 (attendance, not enrollment headcount). Sources: audited financial "
    "statements; SEEK attendance figures reported in the audits.")
P("At the same time, several costs the district controls grew quickly: a two-percent raise in fiscal "
  "2024 with \u201csome employees receiving much more,\u201d in the audit's own words, and step increases in "
  "fiscal 2025. Transportation rose 20.3 percent in a single year, and central-office administration "
  "44.8 percent in two years (Section 9). A $6.055 million bond issued in 2024 helped push "
  "debt-service payments up about $430,000 this year (Section 8).")
P("Two more facts cut in the community's favor. The district has already fixed a money-losing operation "
  "without closing anything. Between fiscal 2024 and 2025 it cut the day-care fund's loss from $722,828 "
  "to $79,010 and swung food service from a $610,606 loss to a $179,197 surplus: about $1.4 million of "
  "improvement in one year. Focused management can move seven figures without touching a school. And "
  "the district is not in collapse: both audits carry clean opinions, the fiscal 2026 budget holds a "
  "$1,489,853 contingency, well above the state's two-percent minimum, and at the current drawdown pace "
  "the unassigned reserve lasts roughly three more budget cycles. The problem is real. So is the time "
  "to fix it right.")
H2("A same-year yardstick: Fayette County, on both districts' audits")
P("Both districts' fiscal 2025 statements carry clean audit opinions. Hold them to the same fiscal "
  "year, 2025, on those statements and the same two measures, both audits archived here. The yearly "
  "gap, revenues less expenditures before transfers over General Fund spending: Bourbon ran <b>9.1 "
  "cents in the red per dollar spent</b> ($2,648,086 against $29,097,404), its third deficit in three "
  "years, against Fayette's <b>5.7 cents</b> ($38,907,376 against $685,348,803). The cushion, the "
  "ending General Fund balance over the same spending: Bourbon still holds <b>14.7 cents of reserve per "
  "dollar</b> ($4,290,840) against Fayette's <b>4.1 cents</b> ($28,361,786). Fayette's balance fell "
  "another $14.9 million, from $43.3 million to $28.4 million, in a year its budget book had planned to "
  "hold the fund flat.")
P("Fayette's figures moved after that audit. On August 3, 2026 its board received an independent audit "
  "of budget processes and expenditures by Weaver, L.L.P., archived here with the district's release. "
  "Weaver reports that after unaudited corrections the district made to its own fiscal 2025 ledger in "
  "June 2026, the year's ending General Fund balance was approximately <b>$6,902,403, about 1 "
  "percent</b> of $690,460,223 of General Fund spending. That is below the 2 percent minimum reserve "
  "KRS 160.470(6)(a) requires every Kentucky district to budget, and below Fayette's own 6 percent "
  "administrative threshold. That figure sits <b>$21.5 million below the $28,361,786 the audited "
  "statements report for the same June 30, 2025 date</b>. The two are not reconciled in the deck; "
  "Weaver does not reconcile them anywhere else either. Two readings are open: real corrections the "
  "audited statements did not carry, or a budget-basis waterfall run from the planned contingency "
  "rather than the audited opening balance. Weaver calls the residual both the ending General Fund "
  "balance and the contingency in the same finding. It traces the gap to unsupported and erroneous "
  "entries: a $3.5 million occupational tax receivable with no documentation, about $8 million of "
  "interdistrict receivables miscoded as revenue, on-behalf payments recorded so revenues and "
  "expenditures did not net to zero, and an unexplained $20.4 million salary overage. Weaver labels its "
  "figures unaudited and subject to change as the district addresses identified misstatements. We carry "
  "them the same way and do not net one basis against the other.")
P("How long each cushion lasts depends on the burn rate used. Bourbon's fund balance fell $1,225,465 "
  "last year, about <b>4.2 cents per dollar spent</b>, after $1,422,621 of net other financing came in, "
  "including the $1,320,939 sweep of restricted building money (audited budgetary comparison: operating "
  "transfers in $1,630,142, out $207,521). On operations alone the district ran <b>9.1 cents in the "
  "red</b>. Our plan ends the sweep, so the operating gap is the basis: at 9.1 cents a 14.7-cent "
  "cushion covers about <b>a year and a half</b>; at 4.2 cents, about three and a half years. Fayette "
  "ran 5.7 cents against a 4.1-cent cushion, under a year, nearer one cent on Weaver's unaudited view; "
  "it has approved borrowing up to $95 million to reach fall tax collections. Both districts' "
  "net-change figures are held down by transfers in, so both are restated on the operating basis and "
  "measured the same way. One more item belongs in the record: Weaver's "
  "report contains more than seventy recommendations and ten priority actions, and <b>none of them is "
  "a school closure</b>. Every one concerns budget amendment controls, segregation of duties, "
  "forecasting methodology, reconciliation, accurate reporting to the board and the public, and a "
  "board-approved plan to rebuild the reserve.")

# ================= 6. BONDS =================
H("8. Bonds, Buildings, and Two Different Pots of Money")
P("Kentucky school finance separates operating money from building money, and that split decides what "
  "closing a school can and cannot do. Districts do not borrow directly: a Finance Corporation, a "
  "separate body on paper but the same people as the Board, issues bonds and leases the buildings back. "
  "The state's School Facilities Construction Commission (SFCC) pays part of qualifying debt; the local "
  "share comes from restricted facility revenues, chiefly the \u201cnickel\u201d building tax (about $2.05 "
  "million in fiscal 2025) and the capital outlay allotment. <b>None of that money can lawfully pay "
  "teachers or plug the operating deficit.</b> \u201cWe spend a great deal on buildings\u201d and \u201cwe cannot "
  "afford to operate a school\u201d describe two different pots. The public conversation should keep them "
  "separate.")
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
    caption="Figure 11. Outstanding bonds of the Bourbon County School District Finance Corporation, from Note 4 of "
            "the FY2025 audited financial statements. The 2016 issue refinanced $5,315,000 of 2009 bonds (saving "
            "$314,834 in present value) and the 2020 issue refinanced $3,410,000 of 2011 bonds (saving $106,627). "
            "* The audit's figures for the 2013R issue are internally inconsistent: the outstanding balance exceeds "
            "the listed original amount, and the stated maturity contains an obvious typographical error. Both are details "
            "the finance office should correct on the record.",
    bold_first_col=True)
fig("chart_debt.png", "Figure 12. Annual bond payments are rising as the 2024 issue comes online. The state's SFCC "
    "pays $1,568,809 of the outstanding principal over the life of the bonds. Source: FY2024 and FY2025 audits.",
    width=4.6 * inch)
P("Three things in the bond record deserve the Board's attention.")
B("<b>The 2024 borrowing's stated purpose is on the public record, and it names the high school, not "
  "any elementary.</b> The SFCC Bond Payee Disclosure approved by the legislature's Capital Projects "
  "and Bond Oversight Committee on June 20, 2024 states the Series of 2024 purpose: various "
  "construction projects including roof replacement at Bourbon County High School and a districtwide "
  "audio system. The issue sold at $6.055 million, and the proceeds flowed into the Construction Fund, "
  "where construction in progress grew from $3.65 million to $7.41 million during fiscal 2025. The "
  "disclosure and minutes are archived here; the BG-1 project applications would complete the "
  "project-by-project accounting, and that records ask stands.")
B("<b>No bond issue on record names North Middletown Elementary.</b> The capital program has flowed "
  "elsewhere for years, and the 2021 facility plan shows where: its in-biennium priority was the $6.66 "
  "million high school Career and Technical Center, while North Middletown's $3.62 million renovation "
  "sat scheduled after the biennium. The fairness question: how much has been invested in this building "
  "against the district's other schools over the past decade? The records are a public-records request "
  "away, and we will publish whatever comes back.")
B("<b>The construction fund ran a negative $1.43 million restricted balance at June 30, 2024</b>: "
  "project spending ran ahead of the borrowing that later covered it, a capital program prioritized and "
  "paid out of cash flow in the same years the operating budget went into deficit.")
H2("The district's own June 2026 bonding numbers, from its own advisor")
P("In June 2026 the district's financial advisor, Robert W. Baird and Co., presented the bonding "
  "picture to the planning committee; the presentation, archived here, anchors this section. Bondable "
  "restricted revenues for fiscal 2027: $3,252,893, built from the two nickels ($1,200,105 each), their "
  "state equalization ($552,990), 80 percent of capital outlay ($173,944), and $126,250 a year of "
  "unexpired SFCC offers of assistance expiring between January 2028 and January 2034. (The components "
  "print $501 over the stated total, Baird's own rounding.) Current bonding capacity: <b>$32 "
  "million</b>. Two of Baird's sensitivities matter here. First, <b>a loss of 50 students drops "
  "capacity to $31 million</b>: about $20,000 of building capacity walks out with every student, "
  "pricing the enrollment risk of a closure in the advisor's own terms. (That $20,000 rides the "
  "restricted streams, not comparable to the General Fund bond multiplier used elsewhere.) Second, the "
  "presentation is built on the state's 2026-27 SEEK "
  "forecast of 2,174.3 in funded attendance (AADA plus growth, the attendance measure SEEK pays on, not "
  "enrollment headcount). The state's own SEEK files, archived beside it, verify the forecast line by "
  "line, with the same $2,400,209,505 assessment Baird prints, down from the 2,222.8 funded in fiscal "
  "2026: the slide the growth plan exists to reverse. None of this capacity pays a teacher or closes "
  "the operating gap, and all of it depends on the restricted stream actually paying for buildings "
  "rather than being swept into operations.")
H2("What closing a school does, and does not do, to bonding capacity")
P("A district's ability to borrow for buildings is simple math set by statute. Capacity is built from two "
  "restricted streams: the capital outlay allotment of $100 per student in average daily attendance (KRS "
  "157.420), of which regulation lets a district pledge 80 percent (702 KAR 4:160), and the restricted "
  "building-fund levy, the “nickel,” with its state FSPK equalization (KRS 157.440). Set existing debt "
  "payments against those streams and what remains is the room for new debt: on the fiscal 2025 numbers, "
  "roughly $224,000 a year of capital outlay, about $2.05 million of building-fund tax, and $1.58 million "
  "of district-paid debt service. The fiscal 2024 audit states the bottom line plainly: about $23.5 million "
  "of unused bonding capacity as of June 30, 2024, laid out component by component on the workbook's "
  "Debt_Service tab.")
P("Nothing in that math grows when a school closes: no assessment, no attendance, no levy. What changes "
  "is the plan, not the capacity. A “transitional” label removes the school's modest listed needs from "
  "the priority list and steers future SFCC offers of assistance (KRS 157.622), and the district's own "
  "borrowing, toward other projects. That is a choice about priorities, and it deserves to be argued "
  "openly as one. The math can also run against the district: every family that responds to closure by "
  "leaving takes $100 a year out of capital outlay and the SEEK base out of operations, permanently. "
  "Nor is an emptied building a windfall: the Pew sale prices in Section 5, typically $200,000 to $1 "
  "million, are one-time money, itself restricted to capital use.")
P("As the 2024 issue and the other series settle in, total debt service steps up about $430,000, from "
  "$1.15 million in fiscal 2025 to $1.58 million in fiscal 2026. That is the net change across all "
  "seven series, some rising and the 2013 issue maturing, not the 2024 bond's payment alone. The SFCC pays "
  "$1,568,809 of principal on the qualifying issues over the life of the bonds. None of the seven "
  "outstanding issues names North Middletown Elementary.")
H2("Where the general fund is actually trending: the unaudited FY2026 close")
P("The district's own KDE Budget Monitoring Tool, in the June 2026 packet on the board's July 16 agenda "
  "and archived here, shows fiscal 2026 closing down roughly $374,000, the best result in three years. "
  "The audited drawdowns were $1.07 million and $1.23 million in the two years before. "
  "The same packet shows how that headline was built. Two June entries account for nearly all of it: a "
  "$1,320,939 transfer of restricted capital money into the general fund, and a $1,413,929 receipt "
  "booked to miscellaneous revenue in period 12 against a budget of zero. The transfer is lawful, "
  "through a Capital Funds Request, and precisely the sweep the growth plan would end. The packet's "
  "variance row reconciles to the dollar. The genuine improvements are real but modest: SEEK revenue $402,000 over budget and "
  "payroll falling through ordinary attrition. Excluding the capital transfer, the year is down about "
  "$1.7 million; excluding the unidentified June receipt as well, about $3.1 million, the same range as "
  "the audited years. These figures are unaudited, the balance sheet shows no receivable behind the "
  "June receipt, and the packet does not identify its source. The district should identify it on the "
  "record before this close is cited to justify anything, in either direction.")

# ================= 8. ADMIN =================
H("9. Where the Money Is Actually Going: Administrative Growth", need=3.0)
fig("chart_admin.png",
    "Figure 13. Administration expense from the district's audited statements of activities. District (central "
    "office) administration grew from $999,727 in FY2023 to $1,447,164 in FY2025; school administration grew from "
    "$2,110,039 to $2,581,412 over the same two years.")
P("The biggest cost jump in the audits is not at North Middletown. Central-office administration grew "
  "44.8 percent in two years, an increase of $447,000 a year, as much as or more than any realistic net "
  "saving from closing the school, while enrollment and attendance fell. School-level administration "
  "grew 22.3 percent, and transportation grew 20.3 percent in fiscal 2025 alone, alongside bus purchases "
  "of roughly $888,000 and $691,000 in consecutive years. Federal data most recently on file show four "
  "central-office administrators and fifteen school administrators. Matching that headcount against the "
  "dollar growth, position by position, is a fair ask before any classroom building closes.")
P("A caution belongs beside that number: functional expense lines in Kentucky school audits include "
  "allocated state pension payments made on the district's behalf, and reclassifications can move money "
  "on paper without a single new hire. Some share of the 44.8 percent may be accounting rather than "
  "administration. That is why we ask for a position-by-position accounting rather than assuming the "
  "worst.")
H2("What the 44.8 percent is actually made of")
P("The district produced its FY2024, FY2025 and FY2026 working budgets in July 2026, and we read them "
  "line by line. The 44.8 percent is real and it cross-validates: district administration on the MUNIS "
  "ledger grows by a very similar amount on a different two-year window, two independent documents "
  "agreeing within about two and a half percent. What they contradict is the story told about it, "
  "including in earlier versions of this report.")
P("<b>Administrative salaries went down, not up.</b> Over the window the ledger covers, salaries in the "
  "district administration function fall about 8 percent. The growth sits in four non-salary lines. "
  "Insurance, meaning property, liability and general coverage, roughly doubled: a regional market cost, "
  "not a hiring decision. Tax collection fees under object 0311 are statutory: the sheriff and the "
  "county clerk are paid a percentage of what they collect, so the line rises when assessments rise. "
  "Accrued sick leave paid at retirement, object 0291, is a Kentucky benefit that converts unused sick "
  "leave to a lump sum; it is coded to central office because payroll clears there, and it is a "
  "retirement cost for staff across the district. Purchased "
  "professional and technical services covers legal, audit, architect and consulting work, including "
  "this facility planning cycle itself.")
P("The number that matters most runs against the way this increase is usually described. <b>Total district "
  "payroll fell</b>, from $30,410,725 to $30,201,047 across the two most recent years in the district's own "
  "payroll reports, down 0.7 percent. The district as a whole did not get bigger.")
P("What did grow is narrower, and every word of it is defensible. Board and central office payroll, "
  "location 001, rose 25.6 percent. That headline is misleading and we will not use it: $187,623 of the "
  "$248,611 increase is the sick-leave and on-behalf program above, which is not ongoing salary. Setting "
  "it aside, <b>central office payroll still grew about 6.3 percent in a year when total district "
  "payroll fell 0.7 percent.</b> That is the fair comparison. The remaining increase is $60,988, and it "
  "is two offices moving in opposite directions: the business office up $114,295, the superintendent's "
  "office down $53,307, netting to exactly $60,988. Every other central office program is flat in "
  "total.")
P("Three findings run against the assumption we started from. First, <b>the records do not show the "
  "district adding net administrative positions</b>: twenty-two months of board agendas contain two "
  "director-level structural actions and both are consolidations (Finance Officer combined with Food "
  "Service Director, December 2024; Pupil Personnel combined with Elementary Continuous Improvement, May "
  "2025). Second, <b>neither the salary schedules nor the payroll report can answer the question</b>: the "
  "published schedules name no senior certified administrator at all, and the payroll report carries "
  "dollars rather than headcount, so it cannot separate one more person from the same people paid more. "
  "Third, <b>the one real documented addition is below director level</b>: a Childcare Director line, a "
  "Migrant Advocate and Recruiter Coordinator line, and a widened assistant principal index that reaches "
  "schools of 400 to 500 pupils.")
P("So the ask changes shape. The right question is not who was hired. It is that <b>the cost growth cited as a "
  "reason to close a school is concentrated in insurance, statutory fees, retirement payouts and professional "
  "services, and the district has never published a position-by-position administrative roster with titles, FTE "
  "and salary that would let anyone check the rest.</b> Until it exists, nobody outside the central office can "
  "answer this question.")
P("We rely on the audited totals rather than individual salaries, on purpose. Individual figures should "
  "come from official records: the KDE superintendent salary file and the board-adopted administrator "
  "salary schedule, both produced in the district's July 2026 records response.")

# ================= 9. ALTERNATIVES =================
H("10. The Alternatives on the Table: Grow, Don't Close")
P("Every option below is available under current Kentucky law. Dollar values are planning estimates from the audited base "
  "figures, labeled as such; several overlap and cannot simply be summed. Even conservatively combined, "
  "they exceed both the realistic saving from closure and the district's annual reserve drawdown. The "
  "first revenue option is a tax adjustment; the full rate analysis follows in this section, and the "
  "itemized menu is Figure 21 in Appendix B. Together they show a district taxing near the bottom of its "
  "region.")
H2("First among them: grow the Kings into the region's premier elementary school")
P("The strongest alternative is not defensive. Kentucky law already gives the district a way to grow. "
  "Under House Bill 563 (2021), codified at KRS 157.350, a district that adopts a nonresident-student "
  "policy may, since July 2022, enroll students from other counties and count them in its attendance "
  "for SEEK funding. No agreement from the child's home district is required, and tuition is at the "
  "board's discretion. Every family North Middletown attracts brings approximately the $4,626 base, and more with the formula's weights, "
  "guarantee (fiscal 2027), plus applicable add-ons.")
P("North Middletown is built to compete for those families. It is a 2011 National Blue Ribbon school "
  "with a gifted-and-talented program and a 13.6-to-1 student-teacher ratio. Its state results lead "
  "every elementary school in Bourbon County in every state-reported subject, and a third-party index "
  "also tops every school in neighboring Clark County and Paris Independent (Conkwright 17.5, Strode "
  "Station 34.2, Justice 39.3, Shearer 42.3, Paris Elementary 12.2). Its state-approved capacity is 174 "
  "against 128 enrolled: forty-six open seats. Filled with transfer students at the base guarantee "
  "alone, they represent roughly $213,000 a year of new recurring revenue gross, about $194,000 after "
  "supplies and about $134,000 if they require the added section this version prices. On top sit "
  "tuition, add-ons, and the further growth a signature program, a preschool satellite, and serious "
  "marketing could pull along the U.S. 460 corridor, a short drive from five surrounding counties. The question "
  "for the administration: why is the district's only nationally honored school proposed for "
  "reclassification instead of expansion?")
P("Honesty requires naming the headwind first. Bourbon County has hovered near twenty thousand "
  "residents for more than fifty years, from 18,476 in 1970 to 20,252 in 2020, and the Kentucky State "
  "Data Center projects a decline of roughly four percent by 2040. The county is aging, its share of "
  "children is shrinking, and its horse-farm land base, the second largest stock of conserved farmland "
  "in Kentucky, structurally limits new subdivisions. The regional boom passed to the west: Scott County "
  "is projected to grow 46 percent by 2050 and Fayette nearly ten, while Bourbon sits outside that "
  "corridor. The district's enrollment decline is real and structural, and we will not pretend "
  "otherwise. North Middletown itself tells the story: it held 261 children in 1988-89, about double "
  "today's 128 (Figure 14).")
P("But a school's enrollment does not have to wait on a county's birth rate, because the board controls "
  "two levers that demographics do not. The first is redistricting. Attendance boundaries are the "
  "board's to draw. With Bourbon Central at 459 students and Cane Ridge at 453 while the district's "
  "best elementary sits at 128 of a rated 174, redrawing the eastern edges, closest families first, "
  "would fill open seats with children the district already educates, relieve the crowded Paris "
  "schools, and shorten rides. The second is the county's edges. Under House Bill 563, families just across the "
  "line in Clark, Nicholas, Montgomery, and Harrison counties can enroll at North Middletown and bring "
  "their state funding with them. On the third-party index the nearby comparison schools in three of "
  "those counties sit below North Middletown; Montgomery County's two elementaries outscore it there, "
  "and the recruiting case runs on distance and small classes rather than rank. The pitch is not that "
  "the region is growing. It is that a school with the county's top state-reported results has empty "
  "seats within a short drive of families in four counties.")
P("The seats deserve a destination, not just a headcount. One natural path: a program for advanced "
  "learners that families apply into from across the district and, under House Bill 563, from "
  "surrounding counties; Kentucky's larger districts have run magnet schools for decades because a "
  "distinctive program pulls enrollment to the building that hosts it. A preschool satellite, or simply "
  "growing the neighborhood school it has always been, serves the same end, and under any of them every "
  "child in the zone keeps their seat. Growth here means recruiting on the strength of a good school, "
  "not betting on a population rebound. The near-term target is modest: returning to the 160 students "
  "the school enrolled as recently as 2020-21 (166 in 2019-20) takes 45 children, measured from today's 115, in a district of "
  "2,600 and four neighboring counties.")
fig("chart_enroll.png",
    "Figure 14. NMES enrollment from 1989 through 2025 against its current state-rated capacity of 174. "
    "The school held 261 students at its 1988-89 peak, roughly double today's official count of 128. "
    "History compiled from federal school-level data.",
    width=6.1 * inch)
P("The decline itself deserves questions, not just measurement, because its milestones track the "
  "district's own planning documents: 261 at the 1988-89 peak, 169 in the 2013 facility plan, 161 in "
  "the 2021 plan, 128 today. The town did not empty out, and the zone's boundaries are unchanged in the "
  "federal record since at least 2015-16. Over the same years the district centralized preschool at the "
  "Paris center, so many zone families now start school in Paris. The renovation priced in 2013 "
  "reappears in the 2021 plan, priced higher. The rated capacity was written down from 198 to 174. No "
  "public recruitment or transfer program has marketed the county's highest-scoring elementary to "
  "anyone. Each of those is a district decision, not a demographic fact. A school 93 percent full "
  "against its rating in the 2021 plan did not become surplus in four years by itself.")
H2("The children never left the county")
P("The case for closing a school starts with a premise: there are fewer children. Checked against exact "
  "counts, the premise is false. The decennial census counts every child rather than sampling them, and "
  "children aged 5 to 17 in Bourbon County number <b>3,594 in 2000, 3,574 in 2010 and 3,548 in "
  "2020</b>, a change of 1.3 percent across twenty years. The Census Bureau's separate annual "
  "school-age estimates agree, moving from about 3,400 in 2014 to about 3,491 in 2023. There is no "
  "demographic decline story here.")
P("Enrollment is a different matter, and these are federal fall counts, not estimates. The two county "
  "districts together held <b>3,708 students in fall 2019 and 3,428 in fall 2022</b>. Bourbon County "
  "Schools alone went from 2,912 in 2014 to 2,616 in 2023, down 10.2 percent, while the Census Bureau's "
  "school-age estimates for the county actually rose about 2.7 percent. The elementary grades fell 16.5 "
  "percent from their 2016 peak, 1,245 to 1,040; kindergarten intake hit 149 last fall, the lowest in "
  "the federal record; and fewer children have entered kindergarten than left fifth grade in seven of "
  "the last eight years. The break is neither gradual nor a birth-rate story: it begins after 2019.")
P("Three cautions belong beside that finding. The Census counts homeschooling inside private school, so "
  "the category can never be labeled private alone. Bourbon does not stand alone, and we will not claim "
  "it does: the move away from public school after 2019 is regional, with registered homeschooling up "
  "139 percent in Harrison County and 112 percent in Fayette over comparable windows. And survey "
  "vintages from 2022 and 2023 carry pandemic weighting caveats. What is specific to Bourbon is the "
  "combination: a flat child population, a double-digit enrollment decline, and a district not yet "
  "organized to compete for the children still here, which is exactly the plan this report prices.")
P("Every one of those children is a Bourbon County child whose family already chose something else, and "
  "the state pays $4,626 for each one who returns. Filling North Middletown's 46 open seats takes about "
  "one in ten of them: 46 of the 483 documented.")
H2("Where the students come from: the pool is measured, and it is large")
P("The students are not hypothetical. The public record measures the pool three ways, all archived "
  "here. First, the districts' own records. Kentucky homeschool families must file a letter of intent "
  "with the local superintendent (KRS 159.160). The counts the districts reported, collected by the "
  "Washington Post's records project, show <b>236 registered homeschool students in the Bourbon County "
  "district and 23 in Paris Independent</b> in 2022-23, about 259 in all, up roughly half since "
  "2018-19. Compliance with the filing statute is incomplete, so that is a floor. Second, the Census. "
  "The American Community Survey counts private school and homeschooling as one combined answer, and "
  "shows that group roughly doubling since the 2014-2018 window. An earlier version put it at about one "
  "in three from the survey alone; too high, inflated by a small-sample weighting artifact in one age "
  "band. Reconciling the district "
  "rosters, the census counts and the state's non-resident file gives <b>about 450 to 550 Bourbon "
  "County Schools children</b> outside this district's classrooms: homeschooled, in private school, or "
  "enrolled in another district. County-wide, roughly 13 to 15 percent of school-age children sit "
  "outside public school entirely, against nearer one in eleven a decade ago. The county has two "
  "private schools: St. Mary in Paris, 96 students in the federal Private School Survey, and Bourbon "
  "Christian Academy in Millersburg, a K-12 school founded in 2002 that grew out of a homeschool group "
  "and skips that voluntary survey, so its students add to the pool uncounted. Third, the state. KDE's "
  "Non-Resident Student report for 2024-25 counts <b>247 Bourbon County Schools residents enrolled in "
  "another district</b>, 171 at Paris Independent and 76 out of county, ten of them at Cloverport "
  "Independent, 150 miles away, host of the statewide virtual academy. Those exports belong in the "
  "pool: the aim is to win them back, not net them against the 436 nonresident students who enroll "
  "here (131 from out of county, <b>including 54 from Fayette County</b>, proof the district can pull "
  "families when it competes). The two documented counts alone, 236 homeschool filings and 247 "
  "students enrolled elsewhere, reach 483 before any private-school student is counted, so the 450 to "
  "550 band is conservative.")
P("The revenue side is symmetric with the closure math in Section 4, on purpose, using the same $4,626 "
  "SEEK base cell in the workbook. A homeschool or private-school student generates no state funding for "
  "the district today, so each one who enrolls is entirely new money: $4,626 of SEEK a year, about "
  "$4,226 after supplies. At the full check, the 450 to 550 pool is $2.1 to $2.5 million a year the "
  "district is not collecting. Net of supplies, the 236 students in this district's own homeschool "
  "files alone carry about $1.0 million a year, and the full pool $1.9 to $2.3 million. Filling all 46 "
  "open seats at the rated 174 from this pool alone is worth about <b>$213,000 a year gross, roughly "
  "$134,000 to $194,000 net of supplies and the zero to one new section the v3.8 correction "
  "prices</b>. That takes fewer than one in five of the registered homeschoolers. The Redistricting tab carries "
  "a returning-student lever beside the rezone and transfer levers, capped together at the 70 seats "
  "between today's enrollment and the 198 rating approved in 2013 (today's 174 is not a ceiling). It "
  "sits at zero by default, so the separate rezone-and-transfer package, $56,000 to $116,000 in "
  "Appendix B, claims nothing from it. What would move these families is no mystery: the county's top "
  "test scores, the state's best-trending building, and small classes are exactly the product "
  "homeschool and private-school families shopped for when they left. Two records asks sharpen this: "
  "the letter-of-intent counts by year at both districts, and the school-level split of the 131 "
  "out-of-county students already here. Closing the school with the open seats forfeits the one asset "
  "this recruitment case runs on.")

H2("The growth path: the same menu as a district-wide recovery plan")
P("Bourbon County Schools has a structural funding problem: spending has outrun revenue at every "
  "building, salaries are hard to raise, capital projects wait, and the causes sit district-wide, not "
  "at North Middletown. It is not the reason salaries cannot increase: its excess cost is about "
  "$156,000 a year, $121,220 on the district's own KDE-filed comparison to the peer average, six tenths "
  "of one percent of the budget. It is not the reason capital projects cannot be funded: the district's "
  "own advisor presented $32 million of bonding capacity in June 2026 (Baird, archived here), while the "
  "capital-to-operations sweep consumes about $17 million of it, a General Fund problem every school "
  "shares. Organized as a plan, the Appendix B menu (Figure 21) is three moves. <b>Move one, inspect "
  "fixed costs</b>: every non-teaching position trimmed by attrition, administrative restructuring "
  "weighed on its merits (the recent growth was insurance, payouts and contracts, not new hires), and "
  "transportation and energy efficiency, worth $760,000 to $1.3 million a year. <b>Move two, grow "
  "enrollment instead of shrinking it</b>: fill North Middletown's 46 seats, recover attendance, and "
  "recruit district-wide from the measured pool of homeschool, private-school and nonresident "
  "families, worth $260,000 to $530,000 a year. <b>Move three, have the honest revenue "
  "conversation</b>: restore the board's own 2018 rate, worth about $1.5 million a year with Bourbon "
  "still taxing below five of its eight neighbors, the recallable rate menu beyond it reaching $0.9 to "
  "$2.2 million, and delinquency recovery adding $60,000 to $120,000. Together the counted-once cost "
  "package and the 2018 restore alone are worth about $2.2 to $2.8 million a year (Figure 21; "
  "confidence and overlap disclosed on the Alternatives tab). Any one move outweighs closure, whose "
  "median outcome loses $427,087 a year. Together they balance the budget, end the sweep, free the "
  "restricted stream to bond the renovation plan, and close nothing. The Alternatives tab prices each "
  "move live.")
P("And the surplus is transformative. The website's plan calculator prices the enrollment lever "
  "directly: recovered leakage students, zero to the full measured pool of 550, each at the same $4,226 "
  "net-of-supplies cell the closure model uses. The gap to close is the district's own most current "
  "number: its June 2026 year-end ledger trends the fiscal 2026 General Fund at <b>$1,738,653</b> in "
  "the red before transfers ($20,694,287 of revenue against $22,432,940 of spending). On-behalf entries "
  "cancel in the gap; the audit will refine it; the audited fiscal 2025 gap was $2,648,086. The "
  "sequencing discussion uses the related $1,694,928 close-plus-sweep requirement. One caution carries "
  "over from Section 8: the trend counts the unidentified $1.4 million June receipt. If that receipt "
  "does not recur the gap runs toward $3.1 million, which the plan's middle and top cases clear and its "
  "floor does not. With the cost package at its low end, the full 2018 restore, and not one student "
  "recovered, the plan clears the trending gap with about $500,000 a year to spare. That is within "
  "$7,000 of funding the full 5 percent raise for every certified teacher, about $507,000 a year on "
  "the district's own $10.0 million General Fund certified payroll. Two recovered students close the "
  "difference, and every dollar of the deeper cost package lands on top. The calculator opens at the "
  "central case, half the pool recovered: 275 of 550 students at the same $4,226 add $1,162,150 a year "
  "and the plan runs about $1.66 million ahead. After the raise, about $1.16 million services roughly "
  "$15.0 million of new bonds: about $47 million of capacity with the advisor's $32 million. At the sliders' top, the full 550-student pool with every lever "
  "high, the plan runs about $3.4 million ahead: the raise plus roughly $37 million of new bonds, about "
  "$69 million of capacity. Every 100 recovered students move the number by $422,600 a year in either "
  "direction. The capacity is the advisor's own $32 million rating, real only once the sweep ends, "
  "because the sweep spends the very stream it is built on. Together: teachers paid more, real building "
  "capacity, every school open. The earlier 10-percent-raise and $52 million top-end claims are "
  "withdrawn with the lever correction.")
P("A suggestion for running the plan: the board should create three standing committees, one per lever, "
  "each with a public charge and a progress report at every board meeting. An enrollment growth "
  "committee works to win families back: reach the 236 homeschool households in the district's own "
  "files, market the county's top-scoring elementary to the 450 to 550 Bourbon County Schools children "
  "now outside its classrooms, and own the public enrollment targets. A fixed-cost committee drives the "
  "$760,000 to $1.3 million package: commission the routing study the $2.9 million transportation line "
  "has never had, review every non-teaching vacancy before it is refilled, and put the energy contracts "
  "out to bid. A revenue committee lays the rate choices in front of the public: what each step on the "
  "menu funds, what it costs the median homeowner per month, and a path back to the board's own 2018 "
  "rate. Committees commit no new money and turn a plan on paper into work with names on it. Volunteers "
  "from the North Middletown community stand at the ready to serve on all three.")

H2("The growth model, priced like the closure model")
P("The growth side is priced with the same discipline as the closure grid, on the district's own "
  "standards. The anchor is its own Appendix B: 24 students per room in kindergarten through grade 3, "
  "28 in fourth, 29 in fifth. Applied to the school's actual grade counts, the six homerooms hold 153 "
  "students against 128 enrolled, so 25 seats sit open today. The architect slide in the same packet "
  "rates the building at 154, corroborating the count. The model fills those seats first, then hires "
  "one classroom teacher per full new class, at a selectable pace. Every setting is a real classroom "
  "count: 1 per 18 (smaller classes than today), 1 per 21 (today's actual class size), or 1 per 24 "
  "(the district's own K-3 cap). Support staff is priced on its own lever, none, 1 per 75, or 1 per 50 added "
  "students, at the school's own classified lines. New teachers are priced at the certified schedule's "
  "entry-to-midpoint rows, $41,718 to $56,583. Busing runs $0 to $1,000 per recruit, marginal costs "
  "$400 to $1,000 per student against a measured $331, and state add-ons run the same $0, $500, and "
  "$1,000 legs the closure grid prices for each leaver, so the two models treat add-ons and the $400 "
  "supplies figure symmetrically. No lever double-counts staffing: teacher changes are priced only on "
  "each grid's own teacher lever.")
P("The result: across all 19,683 priced scenarios, growth pays in every single one. Under the same "
  "lever weighting as the closure grid (triangular on every cost lever, whose middle legs are the "
  "documented central reads; uniform on the enrollment target, the board's choice, not a chance), the "
  "median gains $141,780 a year and the middle half runs from $94,520 to $182,654. Even "
  "the worst case, a class of 18 at the top salary with every cost at its maximum, still nets $3,331. "
  "The website's calculator opens at 30 added students, no new hires needed: $141,780 a year, the weighted "
  "median itself. (The target reads 140 on the slider's 110 base, the district's "
  "figure, whose SBDM allocation projects 111; the same 30 added to the official 128 count is a target of 158. The "
  "district's own Appendix B caps leave 25 open seats across the six grades; adding 30 leaves five "
  "over unless enrollment lands unevenly, and the calculator's hiring lever prices the section the "
  "caps would force.) The same stack drives the cost-per-student curve. At 160 students the school "
  "costs about $14,600 per student with no new hire yet needed. At the 198 seats the state approved in "
  "2013, with two new teachers paid for, about $12,500: cheaper than every school in the county today. "
  "One script, build/growth_grid.py, reproduces the whole grid.")
H2("The tax question, faced squarely")
P("The rate history strengthens the community's hand. Bourbon County Schools levies 52.4 cents per $100 "
  "on real estate, second lowest among nine area districts and roughly 13 cents below the statewide "
  "school average of 65.1. Fayette levies 80.9, Paris Independent, in this same county, 71.5, Clark "
  "65.5, Bath 63.4, Scott 62.9, and Harrison 57.7; only Nicholas County, at 43.1, sits lower, and "
  "Montgomery is essentially tied at 52.5 (Figure 15). The levied rate has fallen from 61.3 cents in "
  "2018 to 52.4 today, a decline that largely reflects Kentucky's rollback mechanics, in which a rising "
  "assessment base pushes the cent rate down to hold revenue roughly level. KDE's levied-type file, "
  "archived here, shows the board took the full four percent revenue option in five of the last twelve "
  "years and the compensating rate or less in the other seven, the exact years the rate slid. The "
  "regional contrast is stark: Scott County rode "
  "the same assessment boom, raised its rate 38.9 percent on top, and levies a 0.5 percent occupational "
  "tax besides; eight Kentucky districts levy that tax, Bourbon levies none, though its utility tax is "
  "already at the 3 percent maximum. Merely holding the 2012 rate, three cents higher, would yield "
  "about $499,000 more per year today at the district's own per-cent yield.")
P("Where the money lands is equally clear. Of the $9.9 million the property tax produced in fiscal "
  "2025, $7.8 million went to the General Fund and $2.1 million to the building and debt funds. Set "
  "against $29.1 million of General Fund spending, the local levy covers barely a quarter of "
  "operations, with state SEEK dollars carrying most of the rest. Two corrections belong on the record. "
  "First, the rate confusion in the audits resolves cleanly: 52.4 cents is the levied real estate rate, "
  "the 54.2 in one audit note is a digit transposition of it, and 54.7 is the separate motor vehicle "
  "rate. Second, the collection shortfalls in the audits, $387,840 in fiscal 2024 and $239,126 in "
  "fiscal 2025, are ordinary delinquencies of roughly two to four percent of certified yield, the kind "
  "every Kentucky district carries, not revenue the board declined to levy. The Figure 21 menu counts "
  "only a partial recovery of them for exactly that reason: honest numbers cut both ways, and we built "
  "this report to take the cut.")
P("What remains is the choice the board controls every August: the rate itself. The anchor of this "
  "report's revenue lever is the rate this board levied in 2018, 61.3 cents. Restoring it raises about "
  "$1.5 million a year on the certified real estate roll, the part that can actually pay teachers, with "
  "Bourbon still taxing below five of its eight neighbors: Fayette, Paris Independent, Clark, Bath, and "
  "Scott. The four percent revenue growth KRS 160.470 allows without recall exposure is a revenue cap, "
  "not a rate move, and it is not the ask here. For scale, it compounds to roughly $313,000 in its "
  "first year, about $639,000 in its second, and about $978,000 a year by its third: over four fifths "
  "of the annual reserve drawdown. The next subsection walks the mechanics. (The restricted "
  "building-fund levy, which cannot pay operating costs, is excluded from this base.) Section 11 "
  "carries the recommendation; the workbook carries the math. The levy is one option, not the only one; "
  "the Figure 21 menu lists others, and deeper spending cuts are always available. But the math does "
  "not bend. Either spending comes down or "
  "revenue goes up. A district drawing down a million dollars of reserves a year does not get to choose "
  "neither. The board and superintendent owe the public a chosen path, in writing, with the work shown. "
  "A full menu, both columns priced, is what this report puts in its hands.")
fig("chart_tax.png",
    "Figure 15. Left: the Bourbon County Schools real estate rate by tax year, from Kentucky Department of "
    "Revenue rate books; years before 2018 could not be retrieved and are not interpolated. Right: current "
    "levied real estate rates across nine area districts against the statewide school average of 65.1 cents. "
    "Fayette and Clark are from local reporting of their board votes; all other rates are Department of Revenue "
    "rate book lines. Bath's bar is its 2025 rate (2024 was 60.7); Nicholas is shown at its real estate rate "
    "of 43.1 (its tangible rate is 43.7).")
P("The fourteen-year record settles how unusual this county's levy path is. KDE publishes every "
  "district's levied rates back to tax year 2012, and Figure 16 plots all nine area districts on the "
  "same axis: every neighboring district's levied rate is higher today than fourteen years ago, most by "
  "double-digit percentages, Bath by 72 percent. Bourbon County's is <b>5.4 percent lower</b>, the only "
  "decline in the region, falling from third highest among the nine in 2012 to eighth today, the "
  "second lowest. Two honesty notes. First, these are levied RATES: under House Bill 44 a rate can "
  "drift down while collections hold, because the compensating rate falls as "
  "assessments grow. The chart measures the net of each board's levy choices against its assessment "
  "growth, and by that measure every other board in the region chose to keep or grow its rate while "
  "Bourbon's slid. Second, Bourbon did take the four percent revenue option in five of the last twelve "
  "years, by KDE's own levied-type file. The rate fell anyway because the other seven years took the "
  "compensating rate or less, including the twelve-cent slide from 2018 to 2022, the exact years the "
  "drawdowns began. The neighbors that rose took the four percent seven, eight, and nine times over "
  "the same window.")
fig("chart_levy_history.png",
    "Figure 16. Fourteen years of school levies, nine area districts, from KDE's Local District Tax Levies "
    "files (total real estate column: general fund plus all facilities levies), cross-checked against the "
    "Department of Revenue rate books for 2024 and 2025, where all nine districts reconcile exactly. Top: "
    "levied rates by tax year. Bottom: percentage change from 2012 to 2025. Rates are levied rates, not "
    "revenue effort; see the House Bill 44 note in the text. Data archived as build/ky_levy_history_"
    "2012_2026.csv.", width=5.7 * inch)

H2("The four percent is a limit on revenue, not on the rate")
P("That distinction decides an argument raised at every public meeting, so it belongs in the record "
  "plainly. The district states that it takes the four percent option. The published rate has not "
  "risen. <b>Both statements can be true at the same time, and ordinarily are.</b> Under KRS 160.470 "
  "the board's benchmark each August is not last year's rate. It is the <b>compensating rate</b>: the "
  "rate that raises the same dollars from existing property as the prior year. When assessments rise, "
  "that rate falls automatically, by the amount assessments rose. The four percent option is the "
  "compensating rate multiplied by 1.04. A board taking the full four percent every year, in a county "
  "whose property is appreciating, therefore publishes a falling rate while collecting more money. The "
  "table below works that math on this district's own figures: the fiscal 2025 certified assessment of "
  "$1,843,569,625 and the 41.0 General Fund cents in KDE's levied-rates file.")
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
P("Two consequences follow. First, <b>a flat or falling rate is not evidence either way</b>; arguing "
  "about the rate alone settles nothing. Second, <b>raising the rate four percent is a different act "
  "entirely from taking the four percent option</b>: last year's rate times 1.04, against five percent "
  "assessment growth, raises about 9.2 percent more revenue. Every dollar above the four percent "
  "ceiling is subject to a recall petition.")
P("What Figure 16 measures, then, is not property markets: every board sets its rate each August "
  "against its own compensating rate, so assessment growth is netted out before any of them votes. What "
  "remains is the choice each board made. Eight boards facing the same statute chose to finish with "
  "more resources to compete with, and one did not. <b>A single document closes the remaining "
  "uncertainty</b>, and it is an outstanding records ask: for each of the last five years, the "
  "certified compensating rate set against the rate the board actually levied.")
P("One movement in Figure 16 needs explaining. Bourbon's total levied rate rose 3.2 cents in tax year "
  "2023, from 49.2 to 52.4, and has held there since. <b>That increase was not operating money:</b> KDE "
  "dates this board's recallable facilities nickel to August 17, 2023 and puts it at 5.7 cents. A new "
  "5.7-cent restricted levy inside a 3.2-cent net increase means the remainder of the rate fell about "
  "2.5 cents the same year: roughly $415,000 a year of unrestricted revenue at the district's certified "
  "real-estate yield of about $166,000 per cent. KDE does not publish the year-by-year "
  "rate-type split, so the 2.5 cents is an inference, and the certified split by year is requested for "
  "exactly that reason. The direction is not in doubt: the "
  "levy that rose in 2023 was money that cannot lawfully pay a teacher, and it rose in the same year "
  "the operating levy appears to have fallen.")

H2("Beyond the four percent: the recallable levy options")
P("The four percent revenue growth is the most the board can collect without offering voters a veto. It "
  "is not the ceiling, and the rate is the real lever. Kentucky law (KRS 160.470) lets the board levy "
  "any rate, with the portion above four percent subject to a voter recall petition; that is exactly "
  "how every neighboring district in Figure 16 climbed past Bourbon. Each option below is priced at "
  "the certified real estate base in the fiscal 2025 audit. The $1,843,569,625 total valuation splits, "
  "on the audit's own calculated levy of $9,880,143 at 52.4 real and 64.5 tangible cents, into "
  "$1,661,885,191 of real estate and $181,684,434 of tangible property. One cent on real estate thus "
  "yields about $166,189 at full collection (collections ran about 98 percent of the calculated levy). "
  "Added cents are priced on real estate alone because the tangible rate, already 64.5 cents, sits "
  "above every option on the menu and would not move. The household cost is priced on the county's "
  "median owner-occupied home of $211,600 (Census ACS 2019-2023): each added cent costs that household "
  "$21.16 a year, about $1.76 a month. Vehicle rates are untouched; the homestead exemption shields "
  "about $46,000 of a senior homeowner's value, so most retirees pay less; farmland is assessed at "
  "agricultural value, not market; renters pay only what landlords pass through.")
tbl(["Option", "New rate", "Added cents", "Median-home cost", "New recurring revenue"],
    [["Match Harrison County", "57.7", "+5.3", "$112/yr ($9.35/mo)", "about $0.88 million"],
     ["Match the regional median (Fayette excluded)", "60.3", "+7.9", "$167/yr ($13.93/mo)", "about $1.31 million"],
     ["Restore Bourbon's own 2018 rate", "61.3", "+8.9", "$188/yr ($15.69/mo)", "about $1.48 million"],
     ["Match Clark County", "65.5", "+13.1", "$277/yr ($23.10/mo)", "about $2.18 million"]],
    [W * 0.30, W * 0.11, W * 0.13, W * 0.22, W * 0.24],
    caption="Recallable levy options at Bourbon's own per-cent yield. Rates are 2025-26 levied real estate "
            "rates; the regional median is the median of the eight area districts with Fayette excluded. "
            "Every formula is live in the model's Tax_History tab, rows 70 to 91.")
P("Restoring the rate this district itself levied in 2018 closes about two thirds of the structural gap "
  "on its own; matching Clark closes nearly all of it. The sequencing is where the plan's own goal "
  "comes within reach. The first call on any new recurring money is closing the operating gap ($373,989 "
  "on the FY2026 trend) and ending the $1,320,939 capital-to-General-Fund sweep, $1,694,928 in all, "
  "because ending the sweep frees the restricted building stream to carry bonds. Restoring the 2018 "
  "rate raises about $1,479,000 (8.9 cents on the certified real base), covering the operating close "
  "and most of the sweep. The remaining $216,000 a year is well inside the cost package's $760,000 "
  "floor. An earlier version priced the restore at $1,699,479 by dividing all-class property "
  "collections by the real-estate cent count; that blended figure overstated a real-only rate move and "
  "is corrected here and in the version history. Once the General Fund stands alone, the nickel "
  "residual carries the $14 million renovation, the restricted capacity becomes genuinely pledgeable, "
  "and the phasing-in nickel equalization adds about $3.6 million on top of the advisor's $32 million: "
  "roughly $35.6 million of construction capacity. The district's own advisor corroborated the base in "
  "June 2026, rating current capacity at $32 million on the same restricted stream. All of it for "
  "$15.69 a month on the median home, without pledging a cent of the new levy to a bond and without "
  "closing anything. Pledged straight to construction instead, the four options carry about $11.5, "
  "$17.1, $19.2, and $28.3 million at the model's 4.5 percent, 20-year assumption. The Harrison and "
  "median options are honest partial steps; they leave about $814,000 and $382,000 a year still to "
  "find from the alternatives menu before the sweep can end.")
P("None of this recommends a particular number, and none of it is counted in the alternatives package "
  "of Section 10. A menu of options exists between cut nothing and close a school, every one prices "
  "out larger than the most generous closure estimate, and every one carries a built-in democratic "
  "check. <b>A levy above four percent can be recalled by the "
  "voters it taxes. A closed school cannot be recalled by the children it displaces.</b> This community "
  "was offered that veto twice on the facilities nickels and twice declined to use it. It has never "
  "been offered the same vote on the operating levy that pays teachers. And the recall record next door "
  "is thin. Across the eight neighboring districts in the last ten years, voters have turned down "
  "exactly one school tax, Bath County's building nickel, in November 2024 and again in January 2025, "
  "and no neighbor has lost an operating rate to a recall in that decade. Statewide, Marion County "
  "voters upheld their board's nickel 54 to 46 in 2015.")

# ================= 12. RECOMMENDATIONS =================
H("11. The Decision, and the Four Asks")
P("The decision before the Board is often framed as closure versus no closure. That is the wrong frame. "
  "The deficit is a districtwide problem, and North Middletown, whose realistic closure saving covers "
  "under a quarter of the gap, did not cause it. The real question is which full operating plan gives "
  "the best five-year result, and there are at least three on the table. The comparison below is an "
  "illustration on our stated assumptions, not a forecast. The Scenarios tab carries the math, and "
  "one-time closure transition costs (unpublished) are not included. Two yardsticks run throughout: "
  "coverage percentages against the $2.65 million operating gap before transfers, balance projections "
  "against the roughly $1.15 million net drawdown after transfers.")
tbl(["Plan", "Recurring impact, year 3", "Projected FY2029 balance", "What it requires"],
    [["1. Districtwide status quo (change nothing)", "None", "Fully drawn down",
      "No decisions; the districtwide drawdown simply continues, with or without North Middletown"],
     ["2. Close NMES and consolidate", "-$846,285 to -$9,860 (median: LOSES $427,087)", "Median: gone much sooner than status quo",
      "Closure vote; the median scenario loses money; longer rides; enrollment-loss risk"],
     ["3. Districtwide recovery plan (menu plus 2018 restore)", "$2.2-$2.8 million a year", "About $4.3 million or better",
      "Revenue votes, administrative rollback, boundary action and HB 563 recruitment, implementation "
      "discipline; every school stays open"]],
    [1.85 * inch, 1.45 * inch, 1.35 * inch, 2.05 * inch],
    caption="Three complete plans, compared on the same assumptions. At the closure grid's median, Plan 2 "
            "drains reserves faster than doing nothing; even its best case loses $9,860 a year, and every "
            "priced scenario loses money outright. Plan 3 restores balance with every school open; "
            "rebalancing and growing North Middletown ($56,000 to $116,000 a year, Section 10) is one line "
            "inside its menu. Scenarios and Runway tabs of the companion workbook.",
    bold_first_col=True)
H2("The four asks, in full")
P("<b>One:</b> keep the school Permanent in the facility plan with its capital needs at lower priority; "
  "a plan commits no money, Priority 2 exists for exactly this, and the Transitional label saves "
  "nothing while foreclosing state facilities eligibility, major renovation, and replacement. "
  "<b>Two:</b> give the school and community the four years to the next facility plan for a measured "
  "enrollment push, against public targets set with the board, judged on results. The tools are options "
  "to weigh: a themed academy in arts, technology, or agriculture and outdoor sciences, or a "
  "donor-funded promise scholarship that pays every North Middletown graduate toward college, trade "
  "school, or any certification. <b>Three:</b> let the school and community raise grant-based and "
  "private funds, with donated services, for the building's critical needs, at no cost to the district. "
  "<b>Four:</b> state publicly that the district will work to grow this school; a sentence of "
  "commitment gives families the confidence to enroll. The honesty behind these asks is already in the "
  "district's books (the $79,211 building figure, Section 4), and the restricted renovation money is "
  "capped by enrollment regardless, a ceiling that rises with every recruited student.")
asktext = ("<b>The ask, plainly stated:</b> the community requests that the Board of Education pause any vote on "
           "the facility plan, or on the future of North Middletown Elementary, until the closure worksheet, "
           "with both sides of the ledger, is published and the four asks are answered in writing and in "
           "public. A pause is fully within the Board's power. Boards control their own agendas, and a "
           "resolution deferring adoption requires only a majority. If the four-year planning deadline "
           "presses, the Board can ask the Kentucky Department of Education in writing for more time under "
           "the facilities-planning framework (702 KAR 4:180 and its incorporated manual), a question that "
           "costs nothing to ask. Nothing in state law forces a rushed decision.")
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
H2("Before any Board action on the facility plan")
B("Adopt a formal Board position that closure is a last resort, to be considered only after the closure worksheet "
  "is published with its downside and the alternatives in Section 10 have been costed.")
B("Decline to adopt any facility plan carrying a \u201ctransitional\u201d designation for North Middletown "
  "until the net-savings worksheet, the complete KFICS assessment behind the July slides, the 2024 "
  "bond project applications (the BG-1s behind the high school roof and audio-system purpose), and the "
  "school-level climate-and-safety survey results are public.")
B("A working threshold for the Board: if documented net recurring General Fund savings fall below roughly "
  "$400,000 to $500,000 a year, about a third of the $1.48 million that restoring the 2018 rate raises "
  "without closing a school, closure "
  "fails on its own financial terms.")
B("Face the levy each August with the rate on the table, not just the revenue formula: restoring the "
  "board's own 2018 rate raises about $1.48 million a year, and Bourbon would still tax below five of its "
  "eight neighbors. Adopt it or reject it, but decide on the record, alongside the spending decisions, "
  "because standing still is the one path the numbers close off.")
H2("Over the next twelve months")
B("Pursue the low-harm levers first: the collections-gap reconciliation, the levy decision at the "
  "September tax setting with the 2018 restore priced on the table, transportation routing, "
  "attrition-based staffing, and an administrative cost review. Report quarterly, in public, against a "
  "target of cutting the operating deficit from $2.6 million to under $1.5 million by fiscal 2027 and "
  "under $800,000 by fiscal 2028.")
B("Set up a North Middletown sustainability committee, district, city, parents, and business, to "
  "design the signature program, community uses of the building, and a transfer-in program for the "
  "2027-28 school year.")
B("Give that plan a real test, with a published ladder of targets: 145 at the fall 2027 count, 160 by "
  "2028, 180 by 2029, 198 by 2030, and quarterly reporting against it. If the community's plan misses "
  "its own number, the conversation changes; if it hits, the question is settled. Either way, the "
  "decision will have been earned rather than assumed.")
H2("If consolidation is ever revisited")
B("Require an independent review of the savings estimate, a receiving-school capacity study, and a student "
  "transition plan, and cost grade reconfiguration (for example, a primary center at North Middletown) as the "
  "explicit alternative to outright closure.")
P("The district holds about $4.3 million in General Fund balance and is drawing it down at $1.1 to $1.2 "
  "million a year: a serious problem, and roughly three budget cycles to fix it properly. Closing the "
  "county's best elementary school, in the town that would lose the most, on the strength of an "
  "unpublished number, would be a permanent answer to a solvable problem. The record is settled by the "
  "district's own July 2026 records response: asked for any cost-benefit analysis, enrollment study, "
  "capacity study, feasibility study, transportation study, or document evaluating the future use of "
  "NMES, it answered N/A to every one. The analyses do not exist. Before any vote, the Board should "
  "require the administration to create them and compare closure against complete keep-open and "
  "districtwide recovery plans. Revenue or reductions, the Board must choose one and own it; standing "
  "still spends the reserves and settles nothing. Pause the vote. Create the analysis the records "
  "response says does not exist.")

# ================= NOTES =================
H("Notes on the Data")
P("We built this report from public records and Open Records Requests only, and we want it held to that "
  "standard. The audited figures come from the district's financial statements for the years ended June "
  "30, 2024 and June 30, 2025, both with clean opinions. The multi-year score series in Figure 1's lower "
  "panel is SchoolDigger's normalized 0-100 rendering of state test data, a consistent yardstick but "
  "not KDE's official rating. Where this report says first in every tested subject, that is the state's "
  "own 2024-25 assessment file, archived in the repository, and the underlying state assessments "
  "changed in 2012 and again in 2021-22. Demographic figures come from the U.S. Census Bureau, the Kentucky State "
  "Data Center, and the county's Envision 2040 plan. Enrollment counts from 1989 through 2014 are "
  "compiled from federal data by PublicSchoolReview; the 2015 through 2025 counts match the federal "
  "figures directly. Every dollar range labeled an estimate is ours, its assumptions are stated where "
  "it appears, and every one is adjustable in the workbook. The boundary rebalancing scenario in the "
  "appendix is simple math on the cited enrollment counts, not a routing study; the appendix states the "
  "transportation inputs beside it.", note)
P("A few items need the district, not us, to resolve. The real-estate tax rate appears three ways in "
  "public records, as 52.4, 54.2, and 54.7 cents; Section 10 resolves it: 52.4 is the levied rate, 54.2 "
  "a transposition typo, 54.7 the motor vehicle rate. The cent split (41.0 General Fund plus two 5.7 "
  "nickels) and the levied rate type by year are settled from KDE's own files, archived here; still "
  "open is the pre-2012 rate history, in state files the district can produce. The 2013R bond figures "
  "are internally inconsistent as printed. The 2024 bond's stated purpose is on the public record "
  "through the state's June 2024 bond disclosure (high school roof and a districtwide audio system); "
  "the 2023 issue's project detail and both years' BG-1 applications are still open. The school-level "
  "climate and safety survey results were not publicly retrievable. And the enrollment count itself: "
  "federal data show 128, public statements have said around 100, and a 118 figure appears in no "
  "official record we could find. Reported free and reduced-price meal shares for the school range from "
  "roughly 76 to 93 percent across federal and state sources. The recollection in Section 6 of an "
  "earlier transitional episode is Dr. Bradley's, from talks with his father, who served as mayor of "
  "North Middletown; it is offered as memory, and the pre-2021 planning records that would confirm it "
  "remain a public-records request away. One more for the record: the fiscal 2025 audit misprints the "
  "prior year's attendance as 2,278.527; the correct figure, 2,278.537, comes from the fiscal 2024 "
  "audit itself.", note)
P("We prepared this report ourselves, a group of volunteers from the NMES community, with Claude, an AI "
  "research assistant from Anthropic, doing the digging alongside us, and we disclose that on purpose: "
  "check our work. Every figure traces to a source below, and every school and district named is the "
  "Kentucky one. Cautions on pension allocations, one-time swings, single-year score noise, and the tax "
  "cost of the levy option sit beside the numbers they qualify. The Kings mascot and the blue and white "
  "of these pages are the school's own. This report criticizes decisions and asks for documents. It "
  "attributes no motive and alleges no wrongdoing to the superintendent, the finance office, the Board, "
  "or any member of the planning committee, and nothing in it should be read otherwise.", note)
P("<b>Version history.</b> Every version stays public at github.com/ryanuspsagm/SaveNMES, with the "
  "line-by-line record of every change to the report, model, and website. The changes in each release:", note)
P("<b>Version 5.0, August 17.</b> The school-choice survey results are published, anonymized, and the "
  "closure grid is rebuilt on them. The survey: 38 households answered for 85 children (one family with "
  "one child arrived after the form closed and is counted); cleaned by hand "
  "(duplicates removed, three households known to be staying recoded, one family already gone set aside), "
  "31 households with 70 children say they would leave. The grid's leaver lever moves from guessed shares "
  "of 128 (0 to 64 students) to survey-anchored students missing from the rolls at steady state (117 to "
  "154: the statistical band's 25th, 50th, and 75th percentiles, triangular; the floor of 74 (5.83 signed leavers per class cohort carried 12.62 effective years) from signed "
  "households alone is kept as hard evidence below every priced leg, not as a scenario). "
  "Each missing student is priced at the SEEK base plus add-ons minus the "
  "$400 of supplies that stop being spent (the same figure the growth model charges each recruit; the "
  "credit scales with students, and teacher savings appear only on the teachers-cut lever, so staffing is "
  "never counted twice; the busing high leg is capped at half its $190,000 route-split bottom-up maximum, at $95,000, and a "
  "property-value lever priced in an interim draft is removed while the PVA records request is pending). "
  "The grid moves from 5,832 to 972 scenarios; the median moves from a $20,007 to "
  "a $427,087 yearly loss, the middle half to a $518,405-to-$338,727 loss, every priced scenario loses "
  "money (the best case still loses $9,860), and the website default (the savings that scale with "
  "students granted, teachers included, half the fixed overhead cut, median leavers) opens at a $308,207 "
  "loss, the 82nd percentile. In the same release the exodus estimate is restated as a share of the "
  "current student population extended to the whole feeder stream (the hand-coded class years are not assumed accurate; the evidence window spans current "
  "enrollment plus the next three entering classes), open-enrollment case studies are added with sources, and the shrinking "
  "scenario count is the direct result of inputs the survey and records responses pinned down. The response-bias factor is recentered from 3x to 3.5x and floored at 3.3x, Pew's lower high-salience benchmark, chosen for a small, emotionally charged respondent pool, and every survey-derived figure is re-based. The current-enrollment baseline is restated on the 2025-26 end-of-year count of 115; capacity and cost comparisons keep the official 2024-25 filings at 128. The "
  "survey results are expressed as shares of current enrollment with a destination breakdown; leaving "
  "families who marked an in-district school are folded into the other-or-undecided row. Two "
  "value notes in the same release: the SEEK base is the enacted FY2027 figure of $4,626 (2026 Ky. Acts "
  "ch. 168, HB 500, p. 20, archived in build/); an interim draft of this release wrongly moved it to "
  "$4,636 on the false premise that $4,626 was only the House figure; that error is corrected here "
  "(both grids, the growth "
  "median moves to $141,780), and multi-year loss totals are retired in favor of per-year figures. The "
  "net closure range now leads the website. The research base is added to Sources: Edunomics Lab and "
  "Bellwether on enrollment-decline finances, FutureEd on kindergarten as the largest school-choice entry "
  "group, Research for Action's 2024 closure-research review, and the survey-methodology anchors for "
  "the response-bias correction (Groves 2004; Abraham, Helms, and Presser 2009; Pew 2012 and 2017). "
  "A new report section "
  "documents the method: 12.62 effective years per lost child from the district's own grade-to-grade "
  "survival, a six-to-thirteen cohort ramp, and a response-propensity correction of the raw survey, all "
  "reproduced by build/exodus_model.py from the published data. Two label corrections: the facility "
  "plan's 128, previously described as the district's 2023-24 SAAR figure, matches the state's 2024-25 "
  "SAAR end-of-year membership file exactly (the 2023-24 file shows 141), and is relabeled here and in "
  "the workbook; the score-suppression notes now state KDE's written rule, a row is withheld when any "
  "achievement level holds fewer than three students, in place of 'too few students'. Newly archived "
  "sources: the state SAAR school-level enrollment files (1999-2019 and 2022-23 through 2025-26), KDE's "
  "SAAR definitions, the HB6 suppression guidance, the SBDM allocation sheets, and the anonymized survey. "
  "The website's survey button is replaced by the published results, and both calculators and every "
  "dependent figure re-base to the new grid.", note)
P("<b>Version 4.6, August 3.</b> A five-track adversarial audit at the community's direction, across the website, executive summary, report, and model, with every published grid statistic independently recomputed (all reproduced exactly). The headline correction is the per-cent tax yield. Earlier versions divided the audit's $7,829,060 of General Fund property collections by the 41.0 real-estate cents to get $190,953 per cent; that blend includes tangible property taxed at 64.5 cents, a rate already above every option on the menu, so it overstated what a real-estate rate move raises. The audit's own certified valuation and calculated levy split the base into $1,661,885,191 of real estate and $181,684,434 of tangible: about $166,189 per real cent. The restore restates from $1,699,479 to about $1,479,000; the menu from $1.01/$1.51/$1.70/$2.50 million to $0.88/$1.31/$1.48/$2.18 million; the package-plus-restore band from $2.5-$3.0 to $2.2-$2.8 million; the hold-the-2012-rate figure from $573,000 to $499,000; the 2023 inference from $477,000 to $415,000; and the plan re-bases: floor surplus $721,000 to about $500,000 (now within $7,000 of the 5 percent raise rather than clearing it; two recovered students close the difference), central case $1.88 to $1.66 million, top $3.6 to $3.4 million, capacities accordingly. Other corrections the same round: a stale per-student saving from version 3.9 ($169) replaced with the current median loss; Bourbon ranks eighth of nine area districts, not seventh; the recruiting counties corrected to Clark, Nicholas, Montgomery, and Harrison (Bath does not adjoin), with Montgomery's higher-scoring elementaries disclosed; one in seven middle and high schoolers restated as about one in eight; the child-population comparison restated on the Census series it cites (up about 2.7 percent, which strengthens the point); the attendance decline restated 248 to 247; central-office ex-program growth 7.6 to about 6.3 percent; Millersburg standardized to its 2006 closure; NMES restated as the lowest-need school building in the KFICS assessment, not second lowest; the all-funds scale corrected from $44 to $41.8 million; the working-budget location view relabeled as including on-behalf dollars; the 2019-20 enrollment corrected to 166 (160 was 2020-21); and the fifth ask of v4.4 is recorded as folded back into ask two. Framing tightened in the same pass: the recall check on any levy above four percent revenue growth is now disclosed beside the restore everywhere; the $661,139 discussion states the year-one-versus-attrition timing point without characterizing anyone; the growth banner says what the grid conditions on (students who arrive); the asks read commit-no-new-money rather than cost-nothing; and the executive summary carries the same not-an-audit disclaimer as the report. Later the same day, Fayette County Public Schools published the independent audit of its budget processes that its board received on August 3, 2026, and the peer comparison in Section 7 was extended to carry it: after the district's own unaudited June 2026 corrections, Fayette's fiscal 2025 ending General Fund balance is about $6,902,403, roughly 1 percent of spending and below the 2 percent minimum reserve KRS 160.470(6)(a) requires every district to budget, a figure that sits $21.5 million below the balance the audited statements report for the same date. The comparison now publishes both districts' burn rates and years of runway, and the audit deck and its coverage are archived under build/. A same-day correction to that addition: the gap between Weaver's figure and the audited balance was first published as a $21.5 million restatement producing a $36.4 million drawdown. Weaver never uses the word restatement, its waterfall runs from the planned contingency rather than the audited opening balance, and its expenditure total differs from the audited one, so subtracting its closing figure from the audited opening mixed two bases. Both artifacts now state the $21.5 million difference as a difference, keep the runway comparison on the audited books of both districts, and carry Weaver's one percent as its own clearly labeled unaudited finding. No version number was incremented; it belongs to this release.", note)
P("<b>Version 4.5, August 2.</b> Both scenario grids now carry explicit lever distributions: triangular "
  "1-2-1 weights where the record pins a central setting, uniform where it does not (teachers cut, "
  "families leaving, the enrollment target). The published closure median moved from a $21,971 to a "
  "$17,982 yearly loss (54 percent losing money) and the growth median from $140,331 to $141,780; the "
  "ranges are unchanged and no conclusion moved. The middle half of each grid is now published beside "
  "its range. The Kentucky elementary average on the cost chart was extended back to 2012 from the same "
  "state files as the school lines. The kindergartner lifetime-funding range tightened to $67,000-$76,000 "
  "with add-ons counted at both ends. The district's $661,139 claim is now reconciled block by block "
  "against the school's General Fund budget. A review round the same day: both website "
  "calculators now state only the percentile their settings reflect, the growth calculator opens at the "
  "weighted median itself (30 added students, then $141,780), the decision panel shows the three default "
  "scenarios side by side, the leaving-cost escalation is charted year by year, and the website cost "
  "chart starts at 2014 because the 2013 file carries the one-time renovation charge. The growth plan "
  "itself became a calculator (levers, raise, bonds and building capacity, on the model's own bases), the "
  "closure calculator prices any loss in cents of tax rate and dollars a month for the median homeowner, "
  "and the scenario bars became percentile scales with a live marker tied to the calculators. A MUNIS pass "
  "followed: the district's own 203-page Cost by ORG transaction ledger, archived here, replaced the "
  "working-budget line items everywhere they appeared; the parse reproduces the ledger's own org totals to "
  "the penny, the school's General Fund actuals ($933,537) land within 0.55 percent of the budget "
  "($938,690), the fixed-position lever re-based to $214,104, and the closure median moved to a $20,007 "
  "yearly loss with the ceiling at $484,582. Two more changes the same day: FIRST, a correction. The plan's "
  "enrollment lever had been published at $1.1 to $3.3 million a year, unsupported by the model's own Move 2 "
  "rows ($260,000 to $530,000); the corrected band now governs, the low-end plan clears the gap only with "
  "the full restore (about $71,000 to spare on the basis then in use; the final basis and figures follow "
  "later in this note), the top ends fund the 5 percent raise and about $4.9 million "
  "of new bonds, and the earlier 10-percent-raise and $52 million claims are withdrawn. SECOND, the "
  "district's advisor's June 2026 bonding presentation was archived and now anchors the capacity claims: "
  "$32 million of capacity, $126,250 of expiring SFCC offers, and about $20,000 of capacity lost per "
  "departing student, by its own sensitivity. The Fayette comparison was aligned to the same fiscal year "
  "2025 on both sides, then moved from Fayette's budget book to its audited statements (a 5.7-cent gap "
  "per General Fund dollar against Bourbon's 9.1, both audited, same measure), and the state's own SEEK "
  "files were archived to verify the 2,174.3 forecast independently of the advisor. "
  "The district's July 2026 records response was then received and archived: it "
  "produced the ledger, budgets, salary schedules, bus routes, and planning records this report now cites, "
  "and answered N/A to any cost-benefit, enrollment, capacity, feasibility, or transportation analysis and "
  "any document evaluating the school's future; the report's publish-the-worksheet asks were rewritten as "
  "that finding, and the money section was rebuilt as a plain ledger walk from the $1,285,310 all-funds "
  "total. The report "
  "was then restructured to follow the website's flow end to end: Part One the case against closing, Part "
  "Two the growth plan, ending on the asks. The twelve-questions section and the Open Records appendix were "
  "removed (their requests live on in the asks and the named records gaps), and the process record, the "
  "building assessment, and the transportation and rebalancing analyses moved to an appendix of other "
  "supporting data. A later round re-based the plan calculator twice over: the enrollment lever now prices "
  "recovered leakage students directly, zero to 550 at $4,226 each, and the plan is measured against the "
  "trending fiscal 2026 gap, $1,738,653 on the district's own June 2026 year-end ledger, beside the audited "
  "fiscal 2025 gap of $2,648,086 it improves on. The same round added the family survey to the website, made "
  "the leakage picture district-specific (236 students in Bourbon's own homeschool files at $4,226 each, "
  "about $1.0 million a year; a net import of 189 on public-school transfers), re-derived the county leakage "
  "band at the symmetric $4,226 cell ($1.9 to $2.3 million, from $2.1 to $2.3 million), added the audited "
  "reserve comparison to the Fayette card (Bourbon 14.7 cents of fund balance per dollar spent, Fayette 4.1), "
  "and re-labeled every SEEK figure as funded attendance rather than students, since SEEK pays on attendance, "
  "not enrollment. On review, the plan calculator's default moved from zero recovery to the central case, "
  "half the measured pool (275 students, a $1,882,976 default surplus); the zero-recovery floor stays "
  "published beside it. On a further review the leakage pool was restated specific to Bourbon County "
  "Schools and now includes residents enrolled in other districts alongside homeschool and private school: "
  "the two documented counts alone, 236 homeschool filings and 247 students enrolled elsewhere, reach 483, "
  "so the 450 to 550 band and its $1.9 to $2.3 million pricing are unchanged and conservative, and the "
  "net-import framing was retired. An adversarial audit round then ran across all four artifacts and "
  "corrected five published figures: Eminence Independent's growth is 35 percent (733 to 991), not 37, "
  "and the matching decade decline at Bourbon County Schools is 10 percent, not 13; the bus-route trim "
  "of $146,000 to $291,000 is 5 to 10 percent of the audited $2.9 million fiscal 2025 transportation "
  "line, which the prose had understated as $2.7 million; the carried state funding of the school's 128 "
  "students is $6.2 to $6.9 million on their actual grade counts (1,339 student-years at $4,626 to "
  "$5,126), replacing an unreproducible $5.6 to $7.4 million band; the 30-percent-leaving loss is 87 "
  "percent of the best-case closure saving, not 86; and the site's escalation chart now uses the same "
  "whole-student convention as its table. The supplies asymmetry between the two grids is now disclosed "
  "with its sensitivity (leavers priced net of supplies move the closure median to a $5,305 loss; no "
  "conclusion changes), and the workbook was swept for stale prior-version figures. The same round "
  "corrected the report's per-hundred staffing ratio (4.3 fixed positions, not 5.0, on the school's own "
  "128 count), restated the measured fixed base on the MUNIS ledger ($244,263 and $293,316, beside the "
  "budget-view $227,831 and $276,928), replaced the stale one-documented-year rate-type sentence with "
  "KDE's own five-of-twelve levied-type record, re-derived the hold-the-2012-rate figure at $573,000, "
  "updated Clark County to its current 65.5 cents, corrected the General Fund share of an $85,000 "
  "position to about $66,860, disclosed the growth calculator's 110 base beside the official 128, and "
  "repaired cross-references left by the removed sections. Three deep-dive "
  "sections then came out at the community's direction, "
  "the 300-student-breakeven reconstruction, the $14 million plan walk, and the June 2026 "
  "capital-transfer decomposition, with their key facts kept in Sections 4 and 8 and the full math in the "
  "workbook, and the revenue ask was re-anchored on restoring the 2018 rate, still below five of the "
  "eight neighbors, rather than on the four percent revenue option. A condensation pass closed the release: the opening was rewritten to mirror the "
  "executive summary document, the back matter was retitled Supporting Data and Appendices, duplicated "
  "passages were removed, and the report was tightened from 60 to 50 pages with every figure and table "
  "retained. A reader correction after release: St. Mary in Paris had been called the county's sole "
  "private school; Bourbon Christian Academy in Millersburg (K-12, founded 2002, grown from a homeschool "
  "group) is the second, absent from the voluntary federal survey that sourced the claim, and its "
  "uncounted students only make the 450 to 550 pool more conservative. In the same review round, the "
  "pool's headline pricing moved to the undiscounted $4,626 SEEK base, $2.1 to $2.5 million a year the "
  "district is not collecting, since forgone revenue is the full check; the net-of-supplies $1.9 to "
  "$2.3 million stays published in Section 10, and the plan calculator still credits recovered students "
  "only at $4,226.", note)
P("<b>Version 4.4, August 1.</b> The growth model rebuilt on the district's own standards: the first 25 "
  "added students fill seats already open at its own Appendix B class caps, teachers are hired per full "
  "new class at a selectable pace (1 per 18, 21, or 24, each a real classroom count), support staff rides "
  "its own lever, and state add-ons run the same legs as the closure grid. Growth now pays in all 19,683 "
  "scenarios, median $140,331. The leaving-cost table added the full-effect and thirteen-year lifetime "
  "figures. The alternatives menu dropped Medicaid (v4.2) and shared services, and its band is published "
  "raw, $1.4 to $2.3 million, with no haircut. The asks grew to five, with a promise-scholarship option "
  "and the committee volunteers named. The 2011 National Blue Ribbon designation was added from the "
  "federal list. The transformative check was published: at the plan's low ends a 5 percent certified "
  "raise and about $23 million of building capacity; at the top ends a 10 percent raise and roughly $52 "
  "million.", note)
P("<b>Version 4.2, August 1.</b> The closure grid rebuilt on the district's own 48-page response: its own "
  "$107,039 worksheet and $20,000 insurance figure, its own $54,479.40 fully loaded staffing price, a "
  "teacher lever running to three positions on its own classroom-capacity appendix, and leakage priced to "
  "50 percent. The median outcome flipped to a $21,971 yearly LOSS across 5,832 scenarios, with 55 percent "
  "losing money. The prior published figures were this report's own estimates; the district's own paperwork "
  "replaced them.", note)
P("<b>Versions 4.0 and 4.1, July 31.</b> The report restructured around the two cases and the choice; the "
  "executive summary added; the Millersburg case study kept while the cohort-leakage claim was withdrawn; "
  "the four asks revised.", note)
P("<b>Version 3.9, July 29.</b> The district's ledger published and the grid rebuilt on measured fixed "
  "lines ($58,774 reassigned, $227,831 mothballed, $276,928 sold). Ten corrections ran in this release, "
  "five against this report's own case, including withdrawing an unsourced marginal-cost estimate, "
  "re-basing the breakeven range at 54 to 69 students, capping the out-of-system share at 13 to 15 "
  "percent, and narrowing the website calculator to the grid it cites. The published median fell from "
  "$91,240 to $21,571 and the negative share rose from 29 to 45 percent.", note)
P("<b>Versions 2.6 through 3.8, July 20 to 26.</b> The bonding story and transport geography (2.6); the "
  "June 2026 capital transfer decomposed (2.7); two-tailed closure economics (3.0); building condition "
  "from every KFICS report (3.1); the recruitment pool measured (3.2); thirty years of Kentucky rural "
  "closures tested (3.3) and the full 163-event distribution (3.4); a correction release from this "
  "report's own adversarial audit (3.5); fourteen years of levies across nine districts (3.6); the "
  "recallable levy options priced (3.7); and the fill package charged for new sections alongside the "
  "25-year cost record (3.8).", note)
P("Corrections policy: errors will be corrected publicly and promptly, and each corrected version "
  "carries a new version number and date. Every version, and the line-by-line history of every change "
  "to the report, model and website, is archived at github.com/ryanuspsagm/SaveNMES. Send corrections, "
  "with the source that supports them, to ryanuspsagm@gmail.com. The same standard is asked of the "
  "district: its July 2026 records response answered N/A to any closure analysis, so if our numbers are "
  "wrong, creating and publishing the analysis is the fastest way to show it.", note)

# ================= SOURCES =================
H("Sources")
srcs = [
 "School Choice Survey, August 2026, anonymized responses (38 households, 85 children; every name and "
 "submission date removed): build/survey_school_choice_2026_08_anonymized.csv, with the model that "
 "reproduces every published figure at build/exodus_model.py",
 "Kentucky Department of Education, Superintendent's Annual Attendance Report (SAAR), school-level "
 "enrollment summaries: 2022-23 through 2025-26 and the 1999-2019 combined workbook, with KDE's SAAR "
 "Definitions and Explanations: education.ky.gov/districts/enrol; archived in this repository under "
 "build/saar_enrollment_*.xls and build/saar_definitions_kde.pdf",
 "Kentucky Department of Education, House Bill 6 (2024) Requirement to Report Academic Performance on "
 "Websites, November 2025 (states the fewer-than-three suppression rule) and Suppressed Student Data "
 "and Improvement Planning Goal Setting, December 2022: education.ky.gov; archived as "
 "build/kde_hb6_suppression_rule_2025.pdf and build/kde_suppressed_data_guidance_2022.pdf",
 "Bourbon County Schools, SBDM school council allocations, 2026-27 (per-school staffing ratios and the "
 "111-student North Middletown projection): build/school_council_allocation_2026_27.pdf",
 "Bourbon County School District, Audited Financial Statements, year ended June 30, 2024 (Summers, McCrary and "
 "Sparks, PSC), posted by the Kentucky Department of Education: education.ky.gov/districts/FinRept/Documents/"
 "FY2023-2024 FA Bourbon Co.pdf",
 "Bourbon County School District, Audited Financial Statements, year ended June 30, 2025, posted by the Kentucky "
 "Department of Education: education.ky.gov/districts/FinRept/Documents/FY2024-2025 FA Bourbon Co Rev.pdf",
 "Kentucky School Report Card, school-level per-pupil expenditure data (2023-24) and assessment and accountability "
 "datasets (2021-22 through 2024-25), Kentucky Department of Education: kyschoolreportcard.com; "
 "education.ky.gov/Open-House",
 "SchoolDigger, normalized 0-100 school test-score histories and statewide rankings built from Kentucky "
 "Department of Education assessment data: schooldigger.com (used for Figures 1 and 2 and the statewide ranks; "
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
 "(2024): researchforaction.org",
 "Groves, R., Presser, S., and Dipko, S., The Role of Topic Interest in Survey Participation Decisions, "
 "Public Opinion Quarterly 68(1) (2004)",
 "Abraham, K., Helms, S., and Presser, S., How Social Processes Distort Measurement: The Impact of Survey "
 "Nonresponse on Estimates of Volunteer Work, American Journal of Sociology 114(4) (2009); archived as "
 "build/abraham_helms_presser_2009_nber_w14076.pdf",
 "Pew Research Center, Assessing the Representativeness of Public Opinion Surveys (2012) and What Low "
 "Response Rates Mean for Telephone Surveys (2017); archived in build/",
 "KMTV 3 News Now, Council Bluffs school board votes to close Crescent Elementary (2023) and Crescent "
 "community plans charter school to replace closed elementary (2026): 3newsnow.com",
 "Education Week, Open Enrollment Has Drained One District; It's Looking to Dissolve (Dec. 2019): "
 "edweek.org (Palmyra-Eagle, Wisconsin)",
 "Iowa Starting Line, Orient-Macksburg could be first Iowa school district to shutter since 2015 "
 "(May 2024): iowastartingline.com; Iowa Public Radio, Orient-Macksburg school district closed "
 "permanently (June 2025)",
 "Valley Sentinel, River Valley school board votes to close Early Learning Center, eyes $1M in savings "
 "(Jan. 2025): valleysentinelnews.com",
 "Flatwater Free Press, The last country school in Scottsbluff shuts its doors (June 2026): "
 "flatwaterfreepress.org",
 "Edunomics Lab, Georgetown University, Financial Impacts of Enrollment Decline (2021): edunomicslab.org "
 "(per-pupil revenue leaves with each lost student while costs fall only in steps)",
 "Bellwether, How Student Enrollment Declines Are Affecting Education Budgets, Explained in 10 Figures: "
 "bellwether.org",
 "FutureEd, Georgetown University, Directional Signals: A New Analysis of the Evolving Private School Choice "
 "Landscape: future-ed.org (kindergartners are the largest entry group in choice programs, over a third of "
 "annual participants)",
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
 "Fayette County Public Schools, Audit of Budget Processes and Expenditures, Weaver, L.L.P., presented to "
 "the Fayette County Board of Education August 3, 2026, published by the district and archived at "
 "build/fcps_weaver_audit_2026_08.pdf, with the district's release and contemporaneous coverage; "
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
 "table in Section 10",
 "Kentucky Department of Education, Nickel Levy Chart (March 2024), dating each district's facilities and "
 "recallable nickels, including Bourbon County's August 17, 2023 recallable levy; and KDE SEEK payment "
 "schedules FY2025 through FY2027 for the equalization phase-in on that nickel",
 "Bourbon County Schools, Annual Financial Report and audit, fiscal 2025 (certified real and personal "
 "property assessment of $1,843,569,625 and General Fund property tax collections of $7,829,060; General Fund "
 "revenues $26,449,318, expenditures $29,097,404, and an ending fund balance of $4,290,840), archived in this "
 "repository as build/bourbon_audit_fy2025.pdf",
 "Robert W. Baird and Co., Bonding Capacity Presentation to the Bourbon County Schools Local Planning Committee, June 2026 "
 "($32 million current capacity from $3,252,893 of FY2027 bondable restricted revenues; sensitivities and the outstanding "
 "debt schedule), archived in this repository as build/baird_lpc_june2026.pdf",
 "Fayette County School District, Financial Statements and Reports Required by the Single Audit Act, fiscal year ended "
 "June 30, 2025 (General Fund revenues $646,441,427, expenditures $685,348,803, a $38,907,376 gap before transfers; fund "
 "balance $43.3 million to $28.4 million), archived in this repository as build/fcps_audit_fy2025.pdf; its Tentative "
 "Budget 2025-26 (General Fund $715,685,019; beginning balances $91.6 million, "
 "$82.5 million, $42 million), archived as build/fcps_tentative_budget_2025_26.pdf",
 "Kentucky Department of Education, SEEK calculation files: FY2026-2027 SEEK Forecast Data (May 6, 2026; Bourbon County "
 "AADA plus growth 2,174.3, assessment $2,400,209,505) and FY2025-2026 SEEK Final Data (February 27, 2026; AADA plus "
 "growth 2,222.755), archived in this repository as build/seek_forecast_2026_27_data.xlsx and "
 "build/seek_final_2025_26_data.xlsx with the extract build/seek_aada_series.json",
 "Bourbon County Schools MUNIS general ledger, Cost by ORG transaction detail, fiscal 2026, archived in this repository as "
 "build/munis_cost_by_org_fy2026.pdf with the reproducible extractor build/munis_extract.py",
 "Kentucky school-level spending files behind the cost-history chart, 2013-14 through 2024-25, archived in this repository "
 "(SPENDING_PER_STUDENT and Kentucky Report Card financial transparency files; statewide elementary averages in "
 "build/ky_elem_spending_2012_2017.json), with the reproducible extractor build/cost_history.py",
 "Kentucky Department of Education assessment files behind the science, social studies and writing score series, 2017-18 "
 "through 2024-25, extracted with sources and suppression flags to build/kde_subjects_history.json",
 "Bourbon County Schools, index of records fulfilled in response to the July 2026 open records requests (received July 20-21, "
 "2026; N/A answers for any cost-benefit, enrollment, capacity, feasibility, or transportation analysis and any document "
 "evaluating the future use of NMES), archived in this repository as build/records_fulfilled_2026_07.pdf",
]
for i, s in enumerate(srcs, 1):
    A(Paragraph(f"{i}. {s}", ParagraphStyle("src", parent=note, fontSize=8.4, leading=10.4, spaceAfter=2.2)))

# ================= GLOSSARY =================
H("Appendix A: Plain-Language Glossary", need=2.2)
gl = [
 ["ADA (Average Daily Attendance)", "The average number of students actually present each day; the main driver of state funding."],
 ["BG-1", "The state form that authorizes a school construction project's scope and budget."],
 ["Bond / debt service", "Borrowing for buildings, and the annual principal-and-interest payments that repay it."],
 ["Bonding potential / capacity", "The new building debt a district's restricted revenues can support, as computed by KDE; built from the capital outlay and nickel streams, minus existing debt service. See Section 8."],
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
for chunk in (gl[:8], gl[8:]):
    rows = [[Paragraph(f"<b>{a}</b>", tcell), Paragraph(b, tcell)] for a, b in chunk]
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


# ================= APPENDIX B: OTHER SUPPORTING DATA =================
H("Appendix B: Other Supporting Data", need=2.2)
P("Analysis that supports Parts One and Two but sits outside the website's flow: the process record, the "
  "building itself, and the transportation and rebalancing work. Everything here is sourced the same way "
  "as the body and reproduced in the companion workbook.")

H2("Where things stand: the decision and the process", need=1.6)
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
      "Superintendent Larry Begley states the school serves about 100 students; the federal count is 128, and "
      "reconciling the two is one of the open records questions. He adds that "
      "keeping it open \u201ccost over a million dollars last school year,\u201d and that \u201cthe decision is not final.\u201d"],
     ["July 23",
      "Community meeting set for 6:30 p.m. at the North Middletown Community Center, next to the fire "
      "department on Church Street; students and alumni invited to write letters of support."],
     ["July 29",
      "Local Planning Committee public forum on the draft facility plan (outcome to be added when the "
      "minutes post)."]],
    [1.05 * inch, 5.65 * inch],
    caption="Figure 17. Timeline of the North Middletown Elementary decision, compiled from local reporting "
            "(WKYT; FOX 56; The Bourbon County Citizen), July 2026.",
    bold_first_col=True)
P("The remaining process is set by state regulation (702 KAR 4:180 and the Kentucky School Facilities "
  "Planning Manual). After the committee finishes its draft, the plan goes to the Kentucky Department "
  "of Education for review, returns to the committee for a vote, and must be adopted by the local "
  "Board of Education. It is then subject to a formal public hearing and finally requires approval by "
  "the Kentucky Board of Education. A \u201ctransitional\u201d label is a planning classification, not a closure: no school closes "
  "unless the elected local Board votes to close it. Each step is a point where Board members and the "
  "public can insist on the documentation this report describes, and where written objections become "
  "part of the official record that goes to Frankfort.")

# ================= 7. THE BUILDING =================
H2("The North Middletown building itself", need=1.2)
P("If the closure case rests on the building, the record does not support it. The school's sections "
  "date to 1948, 1963, and 1964, an older building, like much of the district. The state-approved "
  "District Facility Plan (KBE approval, 2021) classifies North Middletown as a <b>permanent</b> "
  "kindergarten-through-five center with a capacity of 174, comfortably above its current 128 students. "
  "That plan, archived here with its predecessor, prices the school's needs plainly: $317,660 of "
  "life-safety work, a $325,000 accessibility ramp and elevator, and a $3.62 million major renovation "
  "of the mechanical, electrical, and plumbing systems, about $4.26 million in all. The life-safety and "
  "accessibility items, $642,660 together, sit within the 2022-24 biennium schedule; the $3.62 million "
  "major renovation is scheduled <b>after</b> it. The biennium's headline priority was the $6.66 "
  "million high school Career and Technical Center. The district-wide capital need it assesses is "
  "roughly $43.4 million, concentrated at the high school and middle school, not at North Middletown.")
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
P("Three facts fall out of that table. First, North Middletown's rated capacity was written down from "
  "198 to 174 between the two plans, while the same 1948 and 1964 walls held 261 students at the 1988-89 "
  "peak; Cane Ridge fell from 500 to 422 and Bourbon Central from 564 to 521. What changes a rated "
  "capacity under the state's planning manual (702 KAR 4:180, unamended since 2008 and re-certified by "
  "the state as recently as March 2025) is how rooms are counted: standard classrooms times a cap set by "
  "room size, with no utilization discount. Every room relabeled from standard classroom to preschool, "
  "intervention, or computer lab lowers the official number without a brick moving, and the manual "
  "itself says twice that “Different use of the facility spaces shall not reduce the capacity of the "
  "facility” (sections 302.2.2 and 302.3.1). A fair question, not an accusation: under that provision, "
  "what changed at each building to move the ratings? Rated capacity is a number the district sets "
  "through room assignments, and the same pencil that makes space for 128 more children in Paris can "
  "raise North Middletown back toward the 198 it carried in 2013. Second, as recently as the "
  "2021 plan North Middletown stood at 161 students against its rating of 174: <b>93 percent full</b>. "
  "The “half-empty school” is four years old, not a generation old. Third, the 2013 and 2021 plans "
  "both classified North Middletown as permanent; the transitional label in the 2026 draft reverses two "
  "consecutive state-approved plans, which is exactly why the community is entitled to the analysis "
  "behind it.")
P("The 2026 planning cycle sharpens the point. The draft presented at the July 15 forum, an annotated "
  "attendee copy archived here, carries no KDE approval date yet and re-rates the same buildings again, "
  "on the KFICS basis. Cane Ridge rises from 422 to 547 and Bourbon Central to 640, while North "
  "Middletown falls again, from 174 to 154. The draft's own new-construction sections read <b>None</b>, "
  "so the 244 paper seats it adds in Paris come from no brick; ratings that move 125 seats in a single "
  "cycle are policy, not walls. Even at 154, North Middletown stands 83 percent full today. The draft "
  "as presented that day, before the committee's amendment, still listed the school as <b>permanent</b>, "
  "and its headline capital priority is an $18.6 million major renovation of the high school's 1968 and "
  "1981 sections.")
P("The investment record runs alongside. The 2013 plan priced a $1.92 million major renovation for "
  "North Middletown: a security vestibule, enlarged music and computer classrooms, media center and "
  "kitchen, gymnasium upgrades, new flooring, window and door replacement, electrical upgrades, and HVAC "
  "replacement. The 2021 plan prices much of the same scope again, higher, at $4.26 million all told, "
  "with the major renovation again scheduled after the biennium. Whether any of the 2013-priced work was "
  "ever completed is exactly what the district's maintenance and project records would show. The same "
  "needs priced in two consecutive plans, eight years apart, while the capital program built elsewhere "
  "both times, raise a forward-looking question: fund the work this cycle, or let the community fund it, "
  "before the building's condition is cited as a reason to close.")
P("The KFICS Facilities Assessment by RossTarrant Architects, presented in slides at the July meeting "
  "and produced in full in the July 2026 records response, is archived here. North Middletown's total "
  "need is <b>$8,530,093</b>, the <b>lowest</b> of the five school buildings the assessment prices. The "
  "two receiving schools need $23.2 million combined, $8,840,267 at Bourbon Central and $14,387,595 at "
  "Cane Ridge, a 1992 building needing two thirds more than the 1948 one proposed for closure. The "
  "high school needs $27.5 million, the middle school $22.4 million, and the districtwide total is "
  "<b>$98,441,294</b>, more than four times the unused bonding capacity in Section 8. Closing the "
  "least-needy building avoids $8.5 million of restricted-fund need, moves its children into "
  "buildings needing $23.2 million, and does nothing about a $98 million problem. Two points bound the "
  "question. Any renovation would be paid from the restricted facility funds of Section 8, which cannot "
  "close the operating deficit either way. And the receiving schools have little room. Approved "
  "ratings are 521 at Bourbon Central and 422 at Cane Ridge, so at today's 459 and 453 Cane Ridge sits "
  "31 <b>over</b> its rating and there is a net 31 uncommitted seats for 128 children. If ratings can "
  "move by room assignment, the same move raises North Middletown's capacity instead. An empty building is "
  "not free either: it must be secured, insured, minimally heated and eventually disposed of, in a town "
  "of about 610 people whose residents told the planning committee the school is the heartbeat of the "
  "town.")

H2("The state's own condition index: the district's best-trending building")
P("The architect's slides are one reading of the building. The state publishes its own, and it is "
  "stronger. Kentucky's facilities inventory system (KFICS) assigns every public school building a "
  "Condition Index: one minus the ratio of repairs coming due within four years to the cost of "
  "replacing the building outright, so a higher number means a healthier building. KDE has published "
  "exactly three statewide reports: October 2023, October 2025 (both resting on inspections from 2020 "
  "and early 2021, with costs updated between them), and a July 2, 2026 update. The update carries the "
  "first fresh inspections, completed in April 2026 by the district's own third-party architect and "
  "reviewed by KDE. Figure 18 plots every number the state has ever published for the three elementary "
  "schools.")

P("Three findings sit in that figure. First, in the newest KDE-reviewed data, North Middletown's "
  "condition index is <b>0.773</b>: better than Cane Ridge (0.728), within six points of Bourbon "
  "Central (0.823), and far ahead of the middle school (0.596), the district's other 1948 building. "
  "Second, North Middletown is the <b>only school in the district whose condition improved</b> between "
  "the 2020-21 and April 2026 inspection cycles, from 0.694 to 0.773, while every other school's index "
  "fell or held. Its repairs coming due within four years dropped from about $4.1 million to <b>$3.1 "
  "million, the smallest four-year repair bill of the district's five schools</b>; Cane Ridge, a 1992 "
  "building, moved the other way, 0.812 to 0.728, with a $4.8 million four-year bill. Third, the "
  "numbers reconcile with the architect's own $8.5 million total-need figure for NMES: that total "
  "includes longer-horizon work and $2.9 million of instructional-space items, while the condition "
  "index counts what is due within four years. Either way NMES sits near the bottom of the need list. "
  "One caveat favors caution rather than the closure case: NMES's Educational Suitability score, the "
  "separate survey of how well the 1948 layout matches modern program standards, prints 0.21725 in the "
  "July 2026 report, identical to five decimal places to the 2023 report. That half of the score "
  "appears carried forward, not re-surveyed in April 2026, even as the condition half was refreshed. "
  "Whether it was re-surveyed is for the district and its architect to answer on the record; the "
  "identical figure may have an innocent explanation, and the ask is simply to state it. On the "
  "state's newest data, the building proposed for closure is the only one whose condition improved, "
  "carries the smallest near-term repair bill of the five, and scores above a receiving school 44 "
  "years its junior.")
fig("chart_condition.png",
    "Figure 18. The KFICS Condition Index for Bourbon County's three elementary schools in every "
    "statewide report the state has published: October 2023 official, October 2025 official, and the "
    "July 2, 2026 update. Source: KDE, KFICS State Reports, archived under build/ in this repository; "
    "Bourbon County is district 041.", width=5.6 * inch)

H2("A worked example: rebalance the map, fill the school")
P("One scenario, run in the workbook's Redistricting tab. Rezone 30 students to North Middletown from "
  "the adjacent edges of the Cane Ridge and Bourbon Central zones, proximity first, and recruit 16 "
  "cross-county transfers under House Bill 563. The school reaches exactly its rated 174; Bourbon "
  "Central eases to "
  "about 444 and Cane Ridge to about 438. Priced honestly: the class caps (KRS 157.360) bind grade by "
  "grade, not on average. So 46 arrivals likely require one new section, possibly two if they lump in "
  "the wrong grades, possibly none if the rezone is drawn grade by grade; the Redistricting tab carries "
  "that lever at the same $60,000 General Fund rate we apply to eliminated positions. The 16 transfers "
  "bring roughly $74,000 a year of new SEEK revenue; supplies for all 46 added students cost about "
  "$18,000. With one added section against one to two avoided at the receiving schools, the package is "
  "worth roughly <b>$56,000 to $116,000 a year, recurring</b>, down from the $116,000 to $176,000 "
  "published before this correction. The move cuts the school's much-cited "
  "cost per student from $19,348 to about $14,827 with the added section, purely by filling seats. Two "
  "assumptions are flagged in yellow for the district to replace with real data: route shortening by "
  "proximity, and the receiving schools' grade-by-grade capacities. The July 2026 records response "
  "produced the current bus routes but answered N/A for GIS "
  "files, routing-software reports, and ride-time analyses. The district holds the data to run the full "
  "version, and it should, before any vote.")
fig("chart_balance.png",
    "Figure 19. One rebalancing scenario: North Middletown fills to its rated 174 while Bourbon Central and Cane "
    "Ridge each ease by about fifteen students. Dashed lines mark each school's rated capacity "
    "(174, 521, 422); Cane Ridge enrolls above its rating today and remains above it even "
    "rebalanced, which is the receiving-capacity problem closure would compound. The scenario levers (30 "
    "rezoned, 16 cross-county transfers) are adjustable in the companion workbook's Redistricting tab.", width=5.2 * inch)

H2("The transportation map, drawn from the official boundaries")
P("The zone geometry here is official: the federal School Attendance Boundary Survey (2015-16, the last "
  "national collection) published the district's actual attendance boundaries, and this report draws "
  "them directly. The district has still not published its geocoded student counts or its annual T-1 "
  "transportation report, so the cost inputs sit in yellow in the workbook's Transport_Geo tab. Bourbon "
  "County is about 290 square miles of land. Its people cluster west: Paris holds 10,171 of the county's "
  "20,252 residents, against 747 in Millersburg and 610 in North Middletown. The federal boundary file "
  "settles the map: North Middletown's zone covers 110 square miles, 38 percent of the county; Cane "
  "Ridge serves the north including Millersburg; Bourbon Central the southwest. The math follows: about "
  "1.2 elementary students per square mile in the NMES zone, against roughly 5.1 across the two "
  "Paris-based schools' zones and 3.6 district-wide. That density gap is the exact variable state law "
  "funds on: KRS 157.370 sets transportation aid by transported pupils per square mile, paying more "
  "where density is low. The funding history: the formula ran underfunded for two decades, the "
  "2024-2026 state budget restored it to 90 and then 100 percent, computed on lagged fiscal 2023 "
  "costs, and the 2026-2028 budget froze it again below the statute. A district that closes its one "
  "eastern school keeps every square mile of that coverage area and serves it with longer rides.")
tbl(["Zone", "Approx. area (sq mi)", "Elementary students", "Students per sq mi"],
    [["North Middletown zone (southeast)", "110", "128", "~1.2"],
     ["Cane Ridge zone (north)", "120", "453", "~3.8"],
     ["Bourbon Central zone (southwest)", "59", "459", "~7.8"],
     ["District overall", "289", "1,040", "3.6"]],
    [2.6 * inch, 1.35 * inch, 1.45 * inch, 1.3 * inch],
    caption="Official zone areas from the federal School Attendance Boundary Survey (2015-16 collection); "
            "students shown are each school's cited enrollment, the closest public proxy for zone residents. The July 2026 records response confirms it: current boundaries sit in board policy, and the district reports no newer maps, no GIS files, and no reassignment scenarios (all N/A).",
    bold_first_col=True)

P("Now the closure math, from the bottom up, with the distances measured on the official zone geometry "
  "(the workbook's Transport_Geo tab and build/zone_distances.py carry the computation). North Middletown "
  "sits ten road miles from the Paris schools on US 460, against 8.9 straight-line, a road factor of 1.13 "
  "on the one pair that can be measured exactly; a conservative 1.2 is applied everywhere else. Roughly 109 "
  "of the school's 128 students ride the bus on an estimated three rural routes. Extend those routes to "
  "Paris and each adds about 40 bus-miles a day: about 20,400 added bus-miles over a 170-day school year, "
  "$51,000 to $92,000 at "
  "$2.50 to $4.50 per mile, plus roughly $55,000 more if the longer runs force an additional bus. The "
  "bottom-up estimate lands at about $51,000 to $147,000, overlapping the $75,000 to $200,000 planning "
  "range this report has used from the start. The geometry also prices the quieter cost. Averaged over "
  "the zone, closure adds an estimated 4 road miles each way to a child's trip. At the far corner, a "
  "kindergartner who rides about 10 road miles today would ride about 18, roughly 15 to 20 added "
  "minutes each way. And 78 percent of the zone's area lies closer to North Middletown than to Paris, "
  "which is the whole map's point in a single number.")
fig("chart_map.png",
    "Figure 20. Where the students are: the district's official attendance zones from the federal School "
    "Attendance Boundary Survey (2015-16 collection), fetched by the repository's build/fetch_sabs.py. "
    "Paris holds half the county's people and both receiving schools; Millersburg sits in Cane Ridge's "
    "northern zone.", width=5.2 * inch)
P("Run the same math on the rebalancing scenario and the sign flips. Rezoned students already ride "
  "district buses today, ten miles west to the Paris schools. Rezoning moves them to the school they "
  "live closest to, so the affected routes shorten: an estimated $10,000 to $18,000 a year saved. "
  "(Each rezoned student cuts about 136 bus-miles a year at $2.50 to $4.50 a mile; the district's T-1 "
  "route data would replace the estimate.) On this geometry rebalancing is transport-neutral at worst and "
  "modestly positive at best, while closure adds miles. District-wide, the optimization lever in the "
  "menu below, routing software, tiered bells, and a right-sized fleet, remains worth 5 to 10 percent "
  "of the $2.9 million line, $146,000 to $291,000 a year, whichever way the boundary question is "
  "decided.")
P("The state-revenue side runs the same way. Because the 2026-2028 appropriation is frozen at flat "
  "dollars computed on old costs, the marginal state reimbursement on any NEW busing mile is zero: "
  "every dollar of closure's added routes is district money. Rebalancing changes no transported-pupil "
  "count, so the KRS 157.370 allotment and SEEK revenue are untouched, and cross-county transfers add "
  "SEEK revenue with no required busing: under KRS 157.350 the receiving district sets its own "
  "transportation policy for nonresidents. On this math redistricting does not raise transportation "
  "costs; it trims them, while the revenue side gains.")
H2("How a real optimization would run, and who already runs them")
P("None of this requires inventing anything. The method is standard: geocode enrolled students, build a "
  "travel-time matrix on the real road network, then assign zones to schools to minimize ride time, "
  "subject to capacities, statutory class sizes, and keeping neighborhoods together, with routes "
  "re-optimized afterward. Kentucky districts already do this: Fayette convenes boundary working groups "
  "over GIS scenarios and publishes the maps; Jefferson publishes its assignment documents and has "
  "contracted route-optimization modeling. Every district files the annual T-1 transportation report "
  "and keeps the address data this needs. A district facing a closure vote over money owes the public "
  "this study first, and the Transport_Geo and Redistricting tabs are built to receive its outputs.")
P("The savings from doing this well are documented. Boston Public Schools ran the signature version in "
  "2017: an MIT-built routing algorithm produced bus routes 20 percent more efficient, cut 50 buses, and "
  "saved roughly $5 million in the first year. Bourbon County's transportation line is $2.9 million; the "
  "5 to 10 percent captured in the menu below is $146,000 to $291,000 a year, and Boston's 20 percent "
  "shows the ceiling sits higher than the menu assumes. One more check anyone can run: Figure 20 is "
  "drawn straight from the free federal SABS GIS file, fetched by the repository's build/fetch_sabs.py, "
  "so anyone can reproduce it in one step.")
tbl(["Measure", "Estimated annual value", "How it works"],
    [["Restore the board's own 2018 rate (61.3 cents)",
      "about $1.48 million a year, recurring",
      "The rate this board itself levied in 2018, restored, still leaves Bourbon taxing below five of its "
      "eight neighbors. Under KRS 160.470 the portion above four percent revenue growth is subject to voter "
      "recall, a built-in democratic check; priced at the certified $166,189 per real-estate cent."],
     ["Improve delinquent-tax recovery (partial)",
      "$60,000-$120,000",
      "FY2025 collections ran $239,126 (2.4 percent) below certified yield, an ordinary delinquency level; "
      "assumes one quarter to one half is recoverable through routine county channels."],
     ["Attendance recovery",
      "$100,000+ per 1% of ADA",
      "SEEK pays per day of attendance. A chronic-absenteeism campaign is the cheapest revenue in school finance."],
     ["Staffing alignment through attrition",
      "$340,000-$425,000",
      "Funded attendance is down roughly 247 from the pandemic hold-harmless peak. Not replacing four to five positions "
      "district-wide as retirements occur spreads the adjustment fairly instead of extracting it from one town. "
      "Positions are priced at a loaded $85,000; where attrition falls on certified staff the General Fund keeps "
      "about $66,860, so the band's low end is the safer planning figure."],
     ["Administrative restraint",
      "$224,000-$450,000",
      "Return central-office spending toward its FY2023 level before any classroom building closes. Section 9 "
      "finds the recent growth concentrated in insurance, statutory fees and contracts, so the top of this band "
      "means renegotiating market costs; the counted-once package books only the $224,000 floor."],
     ["Transportation optimization",
      "$146,000-$291,000",
      "Routing software, tiered bell times, right-sized fleet, and a pause on bus purchases after $1.58 million in "
      "two years."],
     ["Energy performance contracting",
      "10-25% of utility spend",
      "Kentucky law authorizes guaranteed energy savings contracts (KRS 45A.345 to 45A.352) in which the "
      "savings pay for the upgrades. No such contract is currently in place district-wide."],
     ["District-wide recruitment beyond North Middletown's seats",
      "$106,000 to $211,000",
      "Priced in v3.8: 25 to 50 additional students at $4,226 net each. State funding follows students who "
      "transfer in; the measured pool (450 to 550 Bourbon County Schools children in homeschool, private "
      "school, or another district) is in Section 10, and 62 open seats exist at "
      "Bourbon Central's approved rating. Growth, not shrinkage, is the durable fix for a small-district "
      "budget."],
     ["Fill North Middletown to capacity instead of closing it",
      "$56,000 to $116,000 net, recurring",
      "Rebalance eastern attendance boundaries and recruit cross-county transfers under House Bill 563 to fill "
      "all 46 open seats; the worked example above and the workbook's Redistricting tab show the math. "
      "A preschool or day-care satellite is an additional lever on top."]],
    [1.75 * inch, 1.35 * inch, 3.6 * inch],
    caption="Figure 21. Measures available without closing a school. The menu mixes new recurring revenue "
            "and recurring cost reductions; the workbook's Alternatives tab labels each line by type with a "
            "confidence rating and what would firm it up. Values are estimates from the district's audited "
            "figures and state data; ranges overlap and are not additive to the penny. The 2018 restore "
            "plus the counted-once cost package alone is $2.2 to $2.8 million a year, against an annual "
            "reserve drawdown of $1.1 to $1.2 million; the remaining lines overlap the growth plan's "
            "enrollment lever, and the tab also prices the KRS 160.470 four percent revenue mechanics row "
            "by row.",
    bold_first_col=True)

H2("The closure analysis the district confirms does not exist")
P("The July 2026 records response settled the central question of our records asks: asked for any "
  "cost-benefit analysis of closing, consolidating, or repurposing the school, the district answered "
  "N/A. None exists. When that analysis is created, and it should exist in writing before any vote, it "
  "should run line by line. Count the net recurring General Fund saving, meaning costs that truly "
  "disappear, minus added transportation, receiving-school costs, and the carrying or disposal cost of "
  "the building, with the downside beside it. One-sided worksheets do not count. Two risks belong on that "
  "page, and neither appears in anything the district has produced. "
  "<b>First, children who leave the district rather than change schools.</b> Each one takes the SEEK "
  "base with them, $4,626 at the fiscal 2027 rate, every year, permanently; ten students is $46,260 a "
  "year and thirty is $138,780. Our grid prices that leakage rather than assuming zero, and the risk is "
  "live here: 236 families sit in this district's own homeschool files, 247 residents are already "
  "enrolled in another district, and roughly 450 to 550 Bourbon County Schools children in all sit "
  "outside its classrooms. The exits are open and in use. The district's published math carries no "
  "leakage line at all. <b>Second, assessment erosion.</b> What does losing the town's only school do "
  "to property values inside the North Middletown attendance area, and so to the assessment base that "
  "funds every school in the county? Our own evidence has limits: the thirty-year Kentucky corpus in "
  "Section 5 does not establish that closure causes decline, because small towns that kept their "
  "schools declined at nearly the same rate. So this is not a claim. It is a risk, it "
  "runs one direction only, and the revenue at stake is the district's own, which makes bounding it the "
  "district's job. Both risks are estimable; neither has been estimated. A worksheet that books every "
  "saving at its best case and every risk at zero is incomplete. The board should ask for the second "
  "column before relying on the first.")

# ---------------- build ----------------
def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.6)
    canvas.line(0.9 * inch, 0.66 * inch, 7.6 * inch, 0.66 * inch)
    canvas.setFont("Helvetica", 7.6)
    canvas.setFillColor(GRAY)
    canvas.drawString(0.9 * inch, 0.5 * inch,
                      "Saving North Middletown Elementary School  \u2022  A Close Look at Bourbon County Schools  \u2022  Version 5.0, August 17, 2026")
    canvas.drawRightString(7.6 * inch, 0.5 * inch, f"Page {doc.page - 1}")
    canvas.restoreState()

def cover(canvas, doc):
    pass

doc = SimpleDocTemplate(f"{OUT}/Saving_North_Middletown_Elementary.pdf",
                        pagesize=letter,
                        leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                        topMargin=0.78 * inch, bottomMargin=0.87 * inch,
                        title="Saving North Middletown Elementary School, a Close Look at Bourbon County Schools",
                        author="North Middletown Community Analysis")
doc.build(story, onFirstPage=cover, onLaterPages=footer)
print("pdf built")
