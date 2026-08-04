"""Builds the three-page Executive Summary (SaveNMES_Executive_Summary.pdf).
Standalone companion to the full report; every figure is sourced there."""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable)

NAVY = colors.HexColor("#1F3864")
GOLD = colors.HexColor("#F5C242")
GRAY = colors.HexColor("#666666")
LINE = colors.HexColor("#C9D3E4")
HEADBG = colors.HexColor("#EAF0F8")

body = ParagraphStyle("body", fontName="Times-Roman", fontSize=10.6, leading=14.6,
                      spaceAfter=8, textColor=colors.HexColor("#1A1A1A"))
h1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=15.5, leading=19,
                    textColor=NAVY, spaceBefore=14, spaceAfter=6)
kick = ParagraphStyle("kick", fontName="Helvetica-Bold", fontSize=9, leading=12,
                      textColor=GRAY, spaceBefore=10)
title = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=23, leading=27,
                       textColor=NAVY, spaceAfter=4)
sub = ParagraphStyle("s", fontName="Times-Italic", fontSize=11.5, leading=15,
                     textColor=GRAY, spaceAfter=2)
thead = ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=8.6, leading=10.8, textColor=NAVY)
tcell = ParagraphStyle("tc", fontName="Times-Roman", fontSize=9.6, leading=12.4)
bull = ParagraphStyle("bull", parent=body, leftIndent=16, bulletIndent=4, spaceAfter=6)

S = []
A = S.append

def B(t):
    A(Paragraph(t, bull, bulletText="•"))

A(Paragraph("Saving North Middletown Elementary", title))
A(Paragraph("Executive Summary • The Case Against Closure, the Case for Growth, and the Choice", sub))
A(Paragraph("Version 4.6 • August 3, 2026 • Built from public records and Open Records Requests only • Every figure sourced in the full report and reproduced as live formulas in the companion workbook at SaveNMES.org", sub))
A(HRFlowable(width="100%", thickness=1.1, color=NAVY, spaceAfter=10))

A(Paragraph("WHAT HAPPENED", kick))
A(Paragraph(
  "On July 15, 2026, a planning committee voted to label North Middletown Elementary “transitional.” "
  "That is the first step toward closing the school. The vote is advisory. The elected Board of Education "
  "decides. We checked the public records so the Board and the public can see the whole picture before any "
  "vote. Every number below is sourced in the full report and runs as a live formula in the companion "
  "workbook. Where the record forces an assumption, we make it, state it, and publish it openly so it can "
  "be challenged: the calculators at SaveNMES.org let anyone replace our assumptions with their own.", body))

A(Paragraph("PART ONE", kick))
A(Paragraph("The case against closing NMES: four facts from the district's own documents", h1))
B("<b>Fact one: it is the county's best elementary school.</b> On the state's 2024-25 tests, North "
  "Middletown ranks first among the county's four elementary schools in every state-reported subject, and it beats "
  "the state average in science and writing. It was a "
  "National Blue Ribbon School in 2011, one of five in Kentucky that year.")
B("<b>Fact two: it is not expensive.</b> On the newest state spending file (2024-25), NMES costs $17,903 "
  "per student. The average Kentucky elementary school costs $19,299, so NMES runs 7 percent below the "
  "state average. The district's own cost table, dated May 21, 2026, agrees: it prices the school at "
  "$19,080 per student against a state average of $19,020 on the same table, a gap of three tenths of one "
  "percent.")
B("<b>Fact three: closing it frees very little.</b> Start from everything the district spent on the school "
  "last year: $1,285,310, from its own ledger. Almost all of it moves with the children or pays for itself. "
  "Only the building's own costs stop: $79,211 a year if staff keep their jobs, up to $127,039 if the "
  "building is sold. The superintendent's written response says all staff would be retained, and it prices "
  "those staff at its own $54,479.40 loaded cost. The district's $661,139 figure includes $493,407 of staffing "
  "savings that, by the same response's own terms, arrive only if and when staff leave by attrition; in year "
  "one, with staff retained and supplies moving with the kids, only "
  "$127,039 of it remains. We priced 5,832 closure scenarios on the district's own "
  "figures. The middle case LOSES $20,007 a year, and 55 percent of the scenarios lose money.")
B("<b>Fact four: closing it risks a lot, every year.</b> Under HB 563, state money follows each child to "
  "whichever district wins the family. Registered homeschooling in this county grew from 170 to 259 in five "
  "years. The statewide virtual academy grew from 937 to 2,412 students in two years, on the enrollment counts "
  "of Cloverport Independent, its host district. Every family that leaves "
  "takes about $5,100 a year of state money with it, and the loss grows as the missing kids reach every "
  "grade:")

step = Table(
    [[Paragraph(c, thead) for c in ["Share who leave", "Students (of 128)",
      "Year one", "Per year, full effect", "Total by grade 12"]],
     [Paragraph(c, tcell) for c in ["10 percent", "13", "$67,000", "$144,000", "<b>$1.5 million</b>"]],
     [Paragraph(c, tcell) for c in ["20 percent", "26", "$133,000", "$287,000", "<b>$3.1 million</b>"]],
     [Paragraph(c, tcell) for c in ["30 percent", "38", "$195,000", "$420,000", "<b>$4.6 million</b>"]],
     [Paragraph(c, tcell) for c in ["50 percent", "64", "$328,000", "$713,000", "<b>$7.7 million</b>"]]],
    colWidths=[1.15*inch, 1.15*inch, 1.15*inch, 1.5*inch, 1.65*inch], hAlign="LEFT")
step.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), HEADBG), ("LINEBELOW", (0, 0), (-1, 0), 0.9, NAVY),
    ("LINEBELOW", (0, -1), (-1, -1), 0.6, LINE), ("TOPPADDING", (0, 0), (-1, -1), 3.5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5), ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ("RIGHTPADDING", (0, 0), (-1, -1), 5)]))
A(step)
A(Spacer(1, 6))
A(Paragraph(
  "The first wave is only the start: the missing kids climb one grade a year, so by year eight every grade "
  "is short and the yearly loss is more than double the first hit. The children in the building carry "
  "about $6.2 to $6.9 million of remaining state funding through grade 12. About one in eight students at the "
  "middle and high school came through North Middletown, its share of the county's elementary seats carried "
  "up the grades. A family lost at kindergarten is lost for thirteen years.", body))
A(Paragraph(
  "<b>The bottom line, from the two priced models:</b> grow the school and the middle case GAINS $141,780 "
  "a year, with not one losing scenario in 19,683 (every scenario prices students who actually arrive). Close "
  "it and the middle case LOSES $20,007 a year.", body))

A(Paragraph("PART TWO", kick))
A(Paragraph("The district needs growth, not closures: three levers the board already owns", h1))
A(Paragraph(
  "<b>The money problem is real, and it is district-wide.</b> The General Fund ran a $2.65 million deficit "
  "in fiscal 2025. The district's own June 2026 ledger shows fiscal 2026 closing about $374,000 down, but "
  "only after a lawful $1.32 million transfer of restricted building money into operations through a state "
  "Capital Funds Request; on operations alone the year trends about $1.74 million in the red: better, still "
  "red. The causes are plain. Pandemic aid ended. Funded attendance fell by about 247 once "
  "the pandemic hold-harmless ended, and the state's 2026-27 forecast puts it at 2,174, down again. And the "
  "transfer spends the very stream that should pay for buildings. Bourbon still holds a real cushion, 14.7 cents of reserve per dollar spent. The balance fell only 4.2 cents last year, but only because the $1.32 million sweep flowed in; on operations alone the district ran 9.1 cents in the red, and this plan ends the sweep. Measured that way the cushion is about a year and a half. Fayette County shows what running out looks like. An independent audit presented to its board on August 3, 2026 puts its fiscal 2025 reserve at about 1 percent of spending after the district's own unaudited corrections, below the 2 percent Kentucky law requires every district to budget, and it is borrowing up to $95 million to reach fall tax collections. That audit's seventy-plus recommendations are about budget controls, forecasting and reporting; not one is to close a school. The revenue posture is also unique in the region: the county's tax "
  "base grew 107.5 percent since 2012, second fastest of eight area counties, while the school levy fell "
  "5.4 percent, the only drop among nine districts. Every neighbor's base grew too. Their boards raised "
  "rates anyway.", body))
B("<b>Lever one, enrollment.</b> Each recovered student brings about $4,226 of state money after supplies. "
  "The pool is measured: 236 students sit in Bourbon's own homeschool files, and 450 to 550 Bourbon County "
  "Schools kids are homeschooled, in private school, or enrolled in another district, worth $2.1 to $2.5 "
  "million a year at the full $4,626 SEEK base. "
  "Eminence Independent proved the model an hour away: it grew 35 "
  "percent in the decade Bourbon Schools shrank 10. Growth pays in every one of 19,683 priced scenarios, with a "
  "middle case of +$141,780 a year.")
B("<b>Lever two, fixed costs.</b> Trim every non-teaching position by attrition: $340,000 to $425,000 a "
  "year. Weigh an administrative restructuring: $224,000 to $450,000. Smarter bus routes: $146,000 to "
  "$291,000 on a $2.9 million line no routing study has ever tested. Energy contracts: $50,000 to "
  "$150,000. Counted once, the package is $760,000 to $1.3 million a year.")
B("<b>Lever three, revenue.</b> The rate is simply lower while the tax base more than doubled. Restoring "
  "the board's own 2018 rate brings in about $1.5 million a year on the certified real estate roll, and the "
  "rate menu beyond it reaches $0.9 to $2.2 million. The portion above four percent revenue growth is "
  "recallable by petition, the same democratic check every neighboring increase carried.")
A(Paragraph(
  "<b>Together, the plan is transformative.</b> With costs at the low end and the full restore, it clears "
  "the trending gap with about $500,000 a year to spare, within $7,000 of funding a 5 percent raise for every "
  "certified teacher on its own, on the $32 million of bonding capacity the district's "
  "own advisor presented in June 2026, before a single leaked student comes back; two recovered students close the difference. Recover half the pool and the surplus reaches "
  "about $1.7 million a year and about $47 million of capacity; the full pool reaches about $3.4 million and about $69 million. "
  "Every school stays open. To run it, the board should create three standing committees, one per lever, "
  "each reporting publicly: enrollment growth, fixed costs, and revenue. NMES volunteers stand ready to "
  "serve on all three.", body))

A(Paragraph("THE CHOICE", kick))
A(Paragraph("Two roads, and four asks that commit no new money", h1))
A(Paragraph(
  "Shrink to fit, or grow and thrive. On North Middletown, four asks that commit no new money:", body))
B("<b>One:</b> keep the school listed as Permanent in the facility plan; a plan commits no money, and only "
  "Permanent keeps every door open.")
B("<b>Two:</b> give it the four years to the next plan, with public enrollment targets and the tools to "
  "hit them, judged on results.")
B("<b>Three:</b> let the community fund the building's needs with grants, private money, and donated "
  "labor.")
B("<b>Four:</b> say publicly that the district will work to grow this school; uncertainty is its own "
  "enrollment killer.")
A(Paragraph(
  "These asks put no money at risk: if staff keep their jobs, closing frees only "
  "$79,211 of building costs on the district's own ledger. "
  "A closed school cannot be recalled by the children it displaces. A growth plan can be measured, every "
  "year, by everyone.", body))
A(HRFlowable(width="100%", thickness=0.8, color=LINE, spaceBefore=6, spaceAfter=6))
A(Paragraph(
  "Prepared by NMES community volunteers from public records and Open Records Requests, with analysis "
  "accelerated by an AI research assistant. This is not an audit; it attributes no motive and alleges no "
  "misconduct by anyone. Estimates are labeled, and every figure can be tested in the model at SaveNMES.org.",
  ParagraphStyle("d", parent=body, fontSize=9.4, textColor=GRAY)))
A(Paragraph(
  "The full 53-page report, the financial model with every calculation as live formulas, all archived "
  "district documents, and every prior version with its corrections are free at SaveNMES.org and in the "
  "public repository.", ParagraphStyle("f", parent=body, fontSize=9.4, textColor=GRAY)))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE); canvas.setLineWidth(0.6)
    canvas.line(0.9*inch, 0.62*inch, 7.6*inch, 0.62*inch)
    canvas.setFont("Helvetica", 7.6); canvas.setFillColor(GRAY)
    canvas.drawString(0.9*inch, 0.47*inch,
        "Saving North Middletown Elementary School • Executive Summary • Version 4.6, August 3, 2026")
    canvas.drawRightString(7.6*inch, 0.47*inch, f"Page {doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate("SaveNMES_Executive_Summary.pdf", pagesize=letter,
                        leftMargin=0.9*inch, rightMargin=0.9*inch,
                        topMargin=0.8*inch, bottomMargin=0.9*inch,
                        title="Saving North Middletown Elementary: Executive Summary",
                        author="SaveNMES.org")
doc.build(S, onFirstPage=footer, onLaterPages=footer)
print("executive summary built")
