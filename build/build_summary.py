"""Builds the two-page Executive Summary (SaveNMES_Executive_Summary.pdf).
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

S = []
A = S.append

A(Paragraph("Saving North Middletown Elementary", title))
A(Paragraph("Executive Summary • The Case Against Closure, the Case for Growth, and the Choice", sub))
A(Paragraph("Version 4.5 • August 2, 2026 • Built from public records and Open Records Requests only • Every figure sourced in the full report and reproduced as live formulas in the companion workbook at SaveNMES.org", sub))
A(HRFlowable(width="100%", thickness=1.1, color=NAVY, spaceAfter=10))

A(Paragraph("WHAT HAPPENED", kick))
A(Paragraph(
  "On July 15, 2026, a planning committee voted to label North Middletown Elementary “transitional.” "
  "That is the first step toward closing the school. The vote is advisory. The elected Board of Education "
  "decides. We checked the public records so the Board and the public can see the whole picture before any "
  "vote. Every number below is sourced in the full report and runs as a live formula in the companion "
  "workbook.", body))

A(Paragraph("PART ONE", kick))
A(Paragraph("The case against closing NMES: four facts from the district's own documents", h1))
A(Paragraph(
  "<b>Fact one: it is the county's best elementary school.</b> On the state's 2024-25 tests, North "
  "Middletown ranks first among the county's four elementary schools in every tested subject. It was a "
  "National Blue Ribbon School in 2011, one of five in Kentucky that year. <b>Fact two: it is not "
  "expensive.</b> The district's own cost table, dated May 21, 2026, prices the school at $19,080 per "
  "student. The state average on the same table is $19,020. The gap is three tenths of one percent.", body))
A(Paragraph(
  "<b>Fact three: closing it frees very little.</b> Start from everything the district spent on the school "
  "last year: $1,285,310, from its own ledger. Almost all of it moves with the children or pays for itself. "
  "Only the building's own costs stop: $79,211 a year if staff keep their jobs, up to $127,039 if the "
  "building is sold. The superintendent's written response says all staff would be retained, and it prices "
  "those staff at its own $54,479.40 loaded cost. We priced 5,832 closure scenarios on the district's own "
  "figures. The middle case LOSES $20,007 a year, and 55 percent of the scenarios lose money.", body))
A(Paragraph(
  "<b>Fact four: closing it risks a lot, every year.</b> Under HB 563, state money follows each child to "
  "whichever district wins the family. Registered homeschooling in this county grew from 170 to 259 in five "
  "years. The state virtual academy grew from 937 to 2,412 students in two years. Every family that leaves "
  "takes about $5,100 a year of state money with it, and the loss grows as the missing kids reach every "
  "grade:", body))

step = Table(
    [[Paragraph(c, thead) for c in ["Share who leave", "Students (of 128)",
      "State funding lost, per year", "Lost through grade 12", "Against the best-case saving"]],
     [Paragraph(c, tcell) for c in ["10 percent", "13", "about $67,000", "about $650,000", "<b>14% of it, every year</b>"]],
     [Paragraph(c, tcell) for c in ["20 percent", "26", "about $133,000", "about $1.3 million", "<b>28%</b>"]],
     [Paragraph(c, tcell) for c in ["30 percent", "38", "about $195,000", "about $1.9 million", "<b>40%</b>"]]],
    colWidths=[1.05*inch, 1.05*inch, 1.45*inch, 1.35*inch, 1.7*inch], hAlign="LEFT")
step.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), HEADBG), ("LINEBELOW", (0, 0), (-1, 0), 0.9, NAVY),
    ("LINEBELOW", (0, -1), (-1, -1), 0.6, LINE), ("TOPPADDING", (0, 0), (-1, -1), 3.5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5), ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ("RIGHTPADDING", (0, 0), (-1, -1), 5)]))
A(step)
A(Spacer(1, 6))
A(Paragraph(
  "The children in the building carry about $5.6 million of state funding through grade 12. One in seven "
  "students at the middle and high school came through North Middletown. A family lost at kindergarten is "
  "lost for thirteen years.", body))
A(Paragraph(
  "<b>The bottom line, from the two priced models:</b> grow the school and the middle case GAINS $141,780 "
  "a year, with not one losing scenario in 19,683. Close it and the middle case LOSES $20,007 a year.", body))

A(Paragraph("PART TWO", kick))
A(Paragraph("The district needs growth, not closures: three levers the board already owns", h1))
A(Paragraph(
  "<b>The money problem is real, and it is district-wide.</b> The General Fund ran a $2.65 million deficit "
  "in fiscal 2025. The district's own June 2026 ledger trends fiscal 2026 about $1.74 million in the red: "
  "better, still red. The causes are plain. Pandemic aid ended. Funded attendance fell by about 248 once "
  "the pandemic hold-harmless ended. And the revenue posture is unique in the region: the county's tax "
  "base grew 107.5 percent since 2012, second fastest of eight area counties, while the school levy fell "
  "5.4 percent, the only drop among nine districts. Every neighbor's base grew too. Their boards raised "
  "rates anyway.", body))
A(Paragraph(
  "<b>Lever one, enrollment.</b> Each recovered student brings about $4,226 of state money after supplies. "
  "The pool is measured: 236 students sit in Bourbon's own homeschool files, and 450 to 550 county kids are "
  "outside the public schools altogether. Eminence Independent proved the model an hour away: it grew 37 "
  "percent in the decade Bourbon shrank 13. Growth pays in every one of 19,683 priced scenarios, with a "
  "middle case of +$141,780 a year. <b>Lever two, fixed costs.</b> Trim every non-teaching position by "
  "attrition: $340,000 to $425,000 a year. Weigh an administrative restructuring: $224,000 to $450,000. "
  "Smarter bus routes: $146,000 to $291,000 on a $2.7 million line no routing study has ever tested. Energy "
  "contracts: $50,000 to $150,000. <b>Lever three, revenue.</b> The rate is simply lower while the tax base "
  "more than doubled. Restoring the board's own 2018 rate brings in about $1.7 million a year, and the rate "
  "menu beyond it reaches $1.0 to $2.5 million. <b>Together, the plan is transformative.</b> With costs at "
  "the low end and the full restore, it clears the trending gap with about $721,000 a year to spare: a 5 "
  "percent raise for every certified teacher and about $35 million of building capacity, anchored on the "
  "$32 million the district's own advisor presented in June 2026, before a single leaked student comes "
  "back. Recover half the pool and the surplus reaches about $1.9 million a year. Every school stays open. "
  "Three committees can run it: enrollment, fixed costs, and revenue. NMES volunteers stand ready to help.", body))

A(Paragraph("THE CHOICE", kick))
A(Paragraph("Two roads, and four asks that cost nothing", h1))
A(Paragraph(
  "Shrink to fit, or grow and thrive. On North Middletown, four asks that cost nothing. <b>One,</b> keep "
  "the school Permanent in the facility plan; a plan commits no money, and only Permanent keeps every door "
  "open. <b>Two,</b> give the school the four years to the next plan, with public enrollment targets, "
  "judged on results. <b>Three,</b> let the community fund the building with grants, private money, and "
  "donated labor. <b>Four,</b> say publicly that the district will grow this school; uncertainty is its own "
  "enrollment killer. These asks put no money at risk: if staff keep their jobs, closing frees only "
  "$79,211 of building costs on the district's own ledger. "
  "A closed school cannot be recalled by the children it displaces. A growth plan can be measured, every "
  "year, by everyone.", body))
A(HRFlowable(width="100%", thickness=0.8, color=LINE, spaceBefore=6, spaceAfter=6))
A(Paragraph(
  "The full 58-page report, the financial model with every calculation as live formulas, all archived "
  "district documents, and every prior version with its corrections are free at SaveNMES.org and in the "
  "public repository.", ParagraphStyle("f", parent=body, fontSize=9.4, textColor=GRAY)))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE); canvas.setLineWidth(0.6)
    canvas.line(0.9*inch, 0.62*inch, 7.6*inch, 0.62*inch)
    canvas.setFont("Helvetica", 7.6); canvas.setFillColor(GRAY)
    canvas.drawString(0.9*inch, 0.47*inch,
        "Saving North Middletown Elementary School • Executive Summary • Version 4.5, August 2, 2026")
    canvas.drawRightString(7.6*inch, 0.47*inch, f"Page {doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate("SaveNMES_Executive_Summary.pdf", pagesize=letter,
                        leftMargin=0.9*inch, rightMargin=0.9*inch,
                        topMargin=0.8*inch, bottomMargin=0.9*inch,
                        title="Saving North Middletown Elementary: Executive Summary",
                        author="SaveNMES.org")
doc.build(S, onFirstPage=footer, onLaterPages=footer)
print("executive summary built")
