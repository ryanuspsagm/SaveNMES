"""Builds the four-page Executive Summary (SaveNMES_Executive_Summary.pdf).
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
A(Paragraph("Executive Summary • The Case for Growth, the Case Against Closure, and the Choice", sub))
A(Paragraph("Version 4.2 • August 1, 2026 • Built from public records and Open Records Requests only • Every figure sourced in the full report and reproduced as live formulas in the companion workbook at SaveNMES.org", sub))
A(HRFlowable(width="100%", thickness=1.1, color=NAVY, spaceAfter=10))

A(Paragraph("THE CASE FOR GROWTH", kick))
A(Paragraph("A district-wide problem with district-wide levers", h1))
A(Paragraph(
  "<b>The problem is not one school.</b> Elementary enrollment is down 16.5 percent from its 2016 peak while "
  "the census shows the county's child population essentially flat for twenty-five years. Kindergarten intake "
  "hit 149 last fall, the lowest in the federal record, and fewer children have entered kindergarten than left "
  "fifth grade in seven of the last eight years. The General Fund draws down roughly $1.1 million of reserves "
  "a year, and the enrollment loss alone accounts for most of it: the 205 missing elementary students carry "
  "about $948,000 a year of state funding. The revenue posture is unique in the region: the Department of "
  "Revenue's certified values show Bourbon County's tax base grew 107.5 percent from 2012 to 2025, second "
  "fastest of the eight area counties, while the school levy fell 5.4 percent, the only decline among nine "
  "districts. Scott County rode the same boom, raised its rate 38.9 percent, and levies a 0.5 percent "
  "occupational tax besides; eight Kentucky districts levy that tax, Bourbon levies none. Merely holding the "
  "2012 rate would yield about $613,000 more per year today.", body))
A(Paragraph(
  "<b>Lever one, enrollment.</b> Each returning student brings the $4,626 SEEK base against roughly $400 of "
  "marginal cost. The recoverable pool is measured: 259 registered homeschoolers, roughly 450 to 550 county "
  "children outside the public schools, 131 nonresident students already choosing this district. The model is "
  "proven in-state: Eminence Independent grew 37 percent over the decade Bourbon shrank 13, on differentiation "
  "and open enrollment. A themed academy at North Middletown (arts, technology, or agriculture and outdoor sciences), a preschool-to-kindergarten pipeline, "
  "foundation-funded scholarship promises, and marketing against a measured pool are the plan; filling North "
  "Middletown's 46 open seats alone nets $56,000 to $116,000 a year, and today's 174 rating is not the ceiling: the 2013-approved plan rated the building at 198. <b>Lever two, fixed costs.</b> "
  "Transportation is $2.7 million coded to no school with no routing study ever produced; a ten percent "
  "optimization is about $270,000 a year. Kentucky's school energy program documented $225 million of "
  "statewide savings. An inspection of every non-teaching position district-wide, trimmed by attrition, is "
  "worth $340,000 to $425,000 a year. "
  "<b>Lever three, revenue.</b> The rate is simply lower while the tax base more than doubled. Restoring the "
  "board's own 2018 rate brings in about $1.7 million a year. In the last ten years, across the eight "
  "neighboring districts, voters have turned down exactly one school tax, a building nickel in Bath County; "
  "Bourbon's own voters never even petitioned either of this district's two recallable nickels.", body))

A(Paragraph("THE CASE AGAINST CLOSURE", kick))
A(Paragraph("Five answers from the district's own documents", h1))
A(Paragraph(
  "<b>Performance.</b> North Middletown leads the county in every state-tested subject. <b>Cost.</b> The "
  "district's own Cost of Delivery of Services table, May 21, 2026, prices the school at $19,080 per student "
  "against a state average of $19,020 on the same table, and within 110 percent of its cheapest same-grade "
  "peer against the 150 percent standard in the state facilities manual. <b>What closure frees.</b> The "
  "district's own response prices it: $107,039 of building-bound lines plus $20,000 of insurance, with all "
  "staff retained in year one by its own appendix; across 5,832 scenarios built on the district's own "
  "figures and its own $54,479.40 staffing price, the median outcome LOSES $21,971 a year and 55 percent of "
  "scenarios lose money. <b>The receiving schools.</b> The district's own table shows "
  "them at 97 and 98 percent of capacity, and the high school at 112 percent. <b>What closure risks.</b> "
  "Every exit is free and funded under today's rules: HB 563 makes a transfer to any neighboring district "
  "free to the family and funded for the district that wins the child, registered homeschooling in this "
  "county has climbed from 170 to 259 in five years, and the statewide virtual academy grew from 937 to "
  "2,412 students in its first two years. The losses step up with every ten percent of students who leave, "
  "and the first year is only the start: the missing children move up a grade each year and new kindergartners "
  "follow their older siblings out, so by the time every grade from kindergarten through twelve is short, the "
  "yearly loss is more than double the first hit (about $144,000 at ten percent, $420,000 at thirty), and the "
  "thirteen-year totals run $1.5 million to $4.6 million across those steps:", body))

step = Table(
    [[Paragraph(c, thead) for c in ["Share who leave", "Students (of 128)",
      "State funding lost, per year", "Lost through grade 12", "Against the best-case saving"]],
     [Paragraph(c, tcell) for c in ["10 percent", "13", "about $67,000", "about $650,000", "<b>14% of it, every year</b>"]],
     [Paragraph(c, tcell) for c in ["20 percent", "26", "about $133,000", "about $1.3 million", "<b>27%</b>"]],
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
  "The children in the building carry about $5.6 million of remaining state funding through grade 12, and "
  "roughly one in seven students at the middle and high school came through North Middletown. A family lost "
  "at kindergarten is lost for thirteen years.", body))

A(Paragraph("THE CHOICE", kick))
A(Paragraph("Two roads, and four asks that cost nothing", h1))
A(Paragraph(
  "Shrink to fit, or grow and thrive. On North Middletown specifically: <b>One,</b> keep the school Permanent "
  "in the facility plan with its capital needs at lower priority. A plan commits no money; the Transitional "
  "label saves nothing while foreclosing state facilities eligibility, major renovation, and replacement. "
  "<b>Two,</b> give the school and community the four years to the next facility plan for a measured "
  "enrollment push, against public targets, judged on results. <b>Three,</b> let the school and community "
  "raise grant-based and private funds, with donated services, for the building's critical needs. "
  "<b>Four,</b> state publicly that the district will work to grow this school; uncertainty is its own "
  "enrollment killer, and a sentence of commitment gives existing and future families the confidence to "
  "enroll. If staff are reassigned rather than cut, a closure frees the $58,774 utilities line, so there is "
  "no pot of money these asks would squander. A closed school cannot be recalled by the children it "
  "displaces; a growth plan can be measured, every year, by everyone.", body))
A(HRFlowable(width="100%", thickness=0.8, color=LINE, spaceBefore=6, spaceAfter=6))
A(Paragraph(
  "The full 57-page report, the financial model with every calculation as live formulas, all archived "
  "district documents, and every prior version with its corrections are free at SaveNMES.org and in the "
  "public repository.", ParagraphStyle("f", parent=body, fontSize=9.4, textColor=GRAY)))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE); canvas.setLineWidth(0.6)
    canvas.line(0.9*inch, 0.62*inch, 7.6*inch, 0.62*inch)
    canvas.setFont("Helvetica", 7.6); canvas.setFillColor(GRAY)
    canvas.drawString(0.9*inch, 0.47*inch,
        "Saving North Middletown Elementary School • Executive Summary • Version 4.2, August 1, 2026")
    canvas.drawRightString(7.6*inch, 0.47*inch, f"Page {doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate("SaveNMES_Executive_Summary.pdf", pagesize=letter,
                        leftMargin=0.9*inch, rightMargin=0.9*inch,
                        topMargin=0.8*inch, bottomMargin=0.9*inch,
                        title="Saving North Middletown Elementary: Executive Summary",
                        author="SaveNMES.org")
doc.build(S, onFirstPage=footer, onLaterPages=footer)
print("executive summary built")
