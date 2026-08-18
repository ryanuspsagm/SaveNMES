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
A(Paragraph("Version 5.0 • August 17, 2026 • Built from public records and Open Records Requests only • Every figure sourced in the full report and reproduced as live formulas in the companion workbook at SaveNMES.org", sub))
A(HRFlowable(width="100%", thickness=1.1, color=NAVY, spaceAfter=10))

A(Paragraph("WHAT HAPPENED", kick))
A(Paragraph(
  "On July 15, 2026, a planning committee voted to label North Middletown Elementary “transitional.” "
  "That is step one toward closing the school. The vote is advisory; the elected Board decides. "
  "We checked the public records so the Board can see the whole picture first. Every number below is "
  "sourced in the full report and runs as a live formula in the workbook. Where the record forces an "
  "assumption, we make it, state it, and publish it openly so it can "
  "be challenged: the calculators at SaveNMES.org let anyone swap in their own.", body))

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
B("<b>Fact three: closing it frees very little.</b> The district spent $1,285,310 on the school last "
  "year, by its own ledger. Almost all of it moves with the children or pays for itself. Only the "
  "building's own costs stop: $79,211 a year if staff keep their jobs, up to $127,039 if the building is "
  "sold. The superintendent's written response says all staff would be retained, priced at its own "
  "$54,479.40 loaded cost. The district's $661,139 figure includes $493,407 of staffing savings that, by "
  "that same response, arrive only by attrition. In year one, only $127,039 remains. We priced 972 "
  "closure scenarios on the district's own figures, with family departures measured by the signed survey "
  "instead of guessed. The middle case LOSES $447,573 a year. 971 of the 972 lose money; the one winner nets $1,678 a year, $13 per displaced student.")
B("<b>Fact four: closing it risks a lot, every year.</b> Under HB 563, state money follows each child to "
  "whichever district wins the family. Homeschooling here grew from 170 to 259 in five years. The "
  "statewide virtual academy grew from 937 to 2,412 students in two, on its host district's counts. Each "
  "leaving family takes about $5,100 a year of state money. In August 2026 the survey measured the "
  "departures directly: 38 households answered for 85 children; cleaned, 31 households with 70 children "
  "say they would leave.")

step = Table(
    [[Paragraph(c, thead) for c in ["Estimate", "Basis",
      "Students missing each year", "SEEK lost each year"]],
     [Paragraph(c, tcell) for c in ["Today's students", "42 to 61 percent of the 128 enrolled now", "54 to 79", "$277,344 to $405,744"]],
     [Paragraph(c, tcell) for c in ["Steady state", "the same share of the whole feeder stream, middle half", "114 to 167", "<b>$585,504 to $857,712</b>"]],
     [Paragraph(c, tcell) for c in ["Steady-state median", "the middle of the band", "140", "$719,040"]]],
    colWidths=[0.85*inch, 1.9*inch, 1.55*inch, 2.0*inch], hAlign="LEFT")
step.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), HEADBG), ("LINEBELOW", (0, 0), (-1, 0), 0.9, NAVY),
    ("LINEBELOW", (0, -1), (-1, -1), 0.6, LINE), ("TOPPADDING", (0, 0), (-1, -1), 3.5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5), ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ("RIGHTPADDING", (0, 0), (-1, -1), 5)]))
A(step)
A(Spacer(1, 6))
A(Paragraph(
  "The survey is read as a share of the school, corrected for response bias, and the state's own files "
  "corroborate it: this year's kindergarten enrolled 12 children against a ten-year average of 22. A child who "
  "leaves is missing for every remaining grade, 12.62 effective years on the district's own records, and "
  "losses build until every grade is short. The children in the building carry about $6.2 to $6.9 million "
  "of state funding through grade 12. About one in eight middle and high schoolers came through North "
  "Middletown. A family lost at kindergarten is lost for thirteen years.", body))
A(Paragraph(
  "<b>The bottom line, from the two priced models:</b> grow the school and the middle case GAINS $142,080 "
  "a year, with not one losing scenario in 19,683 (every scenario prices students who actually arrive). Close "
  "it and the middle case LOSES $447,573 a year.", body))

A(Paragraph("PART TWO", kick))
A(Paragraph("The district needs growth, not closures: three levers the board already owns", h1))
A(Paragraph(
  "<b>The money problem is real, and it is district-wide.</b> The General Fund ran a $2.65 million "
  "deficit in fiscal 2025. Fiscal 2026 closed about $374,000 down, but only after a lawful $1.32 million "
  "transfer of restricted building money into operations. On operations alone the year trends about "
  "$1.74 million in the red. The causes are plain: pandemic aid ended, funded attendance fell about 247, "
  "and the 2026-27 forecast drops it again. Bourbon still holds a real cushion, 14.7 cents of reserve per "
  "dollar spent. But strip out the sweep and the district ran 9.1 cents in the red; measured that way the "
  "cushion is about a year and a half. Same-year comparison: an independent audit puts Fayette County's "
  "fiscal 2025 reserve near 1 percent of spending, below the 2 percent state law requires, borrowing up "
  "to $95 million to reach fall collections. Its seventy-plus fixes cover budgets and forecasting; none "
  "is a school closure. And Bourbon's revenue posture is unique: the tax base grew 107.5 percent since "
  "2012, second fastest of eight area counties, while the school levy fell 5.4 percent, the only drop "
  "among nine districts. Every neighbor's base grew too. Their boards raised rates anyway.", body))
B("<b>Lever one, enrollment.</b> Each recovered student brings about $4,236 of state money after supplies. "
  "The pool is measured: 236 students sit in Bourbon's own homeschool files, and 450 to 550 Bourbon County "
  "Schools kids are homeschooled, in private school, or enrolled in another district, worth $2.1 to $2.5 "
  "million a year at the full $4,636 SEEK base. "
  "Eminence Independent proved the model an hour away: it grew 35 "
  "percent in the decade Bourbon Schools shrank 10. Growth pays in every one of 19,683 priced scenarios, with a "
  "middle case of +$142,080 a year.")
B("<b>Lever two, fixed costs.</b> Trim every non-teaching position by attrition: $340,000 to $425,000 a "
  "year. Weigh an administrative restructuring: $224,000 to $450,000. Smarter bus routes: $146,000 to "
  "$291,000 on a $2.9 million line no routing study has ever tested. Energy contracts: $50,000 to "
  "$150,000. Counted once, the package is $760,000 to $1.3 million a year.")
B("<b>Lever three, revenue.</b> The rate is simply lower while the tax base more than doubled. Restoring "
  "the board's own 2018 rate brings in about $1.5 million a year on the certified real estate roll, and the "
  "rate menu beyond it reaches $0.9 to $2.2 million. The portion above four percent revenue growth is "
  "recallable by petition, the same democratic check every neighboring increase carried.")
A(Paragraph(
  "<b>Together, the plan is transformative.</b> Costs at the low end plus the full restore clear the "
  "trending gap with about $500,000 a year to spare, within $7,000 of a 5 percent raise for every "
  "certified teacher, on the $32 million of bonding capacity the district's own advisor presented, before "
  "one leaked student comes back; two recovered students close the difference. Half the pool: about $1.7 "
  "million a year and $47 million of capacity. The full pool: about $3.4 million and about $69 million. "
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
  "The full report, the financial model with every calculation as a live formula, all archived district "
  "documents, and every prior version with its corrections are free at SaveNMES.org and in the public "
  "repository.", ParagraphStyle("f", parent=body, fontSize=9.4, textColor=GRAY)))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE); canvas.setLineWidth(0.6)
    canvas.line(0.9*inch, 0.62*inch, 7.6*inch, 0.62*inch)
    canvas.setFont("Helvetica", 7.6); canvas.setFillColor(GRAY)
    canvas.drawString(0.9*inch, 0.47*inch,
        "Saving North Middletown Elementary School • Executive Summary • Version 5.0, August 17, 2026")
    canvas.drawRightString(7.6*inch, 0.47*inch, f"Page {doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate("SaveNMES_Executive_Summary.pdf", pagesize=letter,
                        leftMargin=0.9*inch, rightMargin=0.9*inch,
                        topMargin=0.8*inch, bottomMargin=0.9*inch,
                        title="Saving North Middletown Elementary: Executive Summary",
                        author="SaveNMES.org")
doc.build(S, onFirstPage=footer, onLaterPages=footer)
print("executive summary built")
