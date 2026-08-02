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

A(Paragraph("PART ONE", kick))
A(Paragraph("The case against closing NMES: five answers from the district's own documents", h1))
A(Paragraph(
  "<b>Performance.</b> North Middletown leads the county in every state-tested subject and is a 2011 National "
  "Blue Ribbon School, one of five Kentucky public schools honored that year. <b>Cost.</b> The "
  "district's own Cost of Delivery of Services table, May 21, 2026, prices the school at $19,080 per student "
  "against a state average of $19,020 on the same table, and within 110 percent of its cheapest same-grade "
  "peer against the 150 percent standard in the state facilities manual. <b>What closure frees.</b> The "
  "district's own response prices it: $107,039 of building-bound lines plus $20,000 of insurance, with all "
  "staff retained in year one by its own appendix; across 5,832 scenarios built on the district's own "
  "figures and its own $54,479.40 staffing price, the median outcome LOSES $20,007 a year and 55 percent of "
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
  "The children in the building carry about $5.6 million of remaining state funding through grade 12, and "
  "roughly one in seven students at the middle and high school came through North Middletown. A family lost "
  "at kindergarten is lost for thirteen years.", body))

A(Paragraph("PART TWO", kick))
A(Paragraph("The district needs growth, not closures: three levers the board already owns", h1))
A(Paragraph(
  "<b>The problem is not one school.</b> Elementary enrollment is down 16.5 percent from its 2016 peak, "
  "while the county's child count has stayed flat for twenty-five years. Kindergarten intake hit 149 last "
  "fall, the lowest on the federal record. The General Fund burns through about $1.1 million of reserves a "
  "year, and the 205 missing elementary students explain most of it: about $948,000 a year of state money. "
  "The tax side is just as clear. The county's tax base grew 107.5 percent since 2012, second fastest of "
  "eight area counties. The school levy fell 5.4 percent, the only drop among nine districts. Holding the "
  "2012 rate would bring in about $613,000 more per year today", body))
A(Paragraph(
  "<b>Lever one, enrollment.</b> Each returning student brings the $4,626 state base against roughly $400 "
  "of real new cost. The pool is measured: 259 registered homeschoolers, roughly 450 to 550 county children "
  "outside the public schools, and 131 nonresident students already choosing this district. Eminence "
  "Independent proved the model an hour away: it grew 37 percent in the decade Bourbon shrank 13. The tools "
  "are options to weigh: a themed academy (arts, technology, or agriculture and outdoor sciences) or a "
  "donor-funded promise scholarship that pays every NMES graduate toward college, trade school, or any "
  "certification. The growth model prices the push with no free passes: one classroom teacher per full new "
  "class past the 25 seats already open at the district's own class caps. It pays in every one of 19,683 "
  "priced scenarios, with a middle case of +$141,780 a year. <b>Lever two, fixed costs.</b> Inspect every "
  "non-teaching position district-wide and trim by attrition: $340,000 to $425,000 a year. Consider "
  "restructuring the administration: $224,000 to $450,000. Smarter bus routes: $146,000 to $291,000 on a "
  "$2.7 million line no routing study has ever tested. Energy contracts: $50,000 to $150,000. "
  "<b>Lever three, revenue.</b> The rate is simply lower while the tax base more than doubled. Restoring "
  "the board's own 2018 rate brings in about $1.7 million a year. In the last ten years, across the eight "
  "neighboring districts, voters turned down exactly one school tax, a building nickel in Bath County. "
  "<b>Together, the plan is transformative.</b> At its low ends with the full rate restore it clears the "
  "whole gap. At its top ends it funds a 5 percent raise for every certified teacher and about $37 million "
  "of building capacity, anchored on the $32 million the district's own financial advisor presented in June "
  "2026. Every school stays open. A suggestion to run the plan: three committees, enrollment, fixed costs, and revenue; NMES volunteers stand at the ready to help", body))

A(Paragraph("THE CHOICE", kick))
A(Paragraph("Two roads, and four asks that cost nothing", h1))
A(Paragraph(
  "Shrink to fit, or grow and thrive. On North Middletown, four asks that cost nothing. <b>One,</b> keep "
  "the school Permanent in the facility plan; a plan commits no money, and only Permanent keeps every door "
  "open. <b>Two,</b> give the school the four years to the next plan, with public enrollment targets, "
  "judged on results. <b>Three,</b> let the community fund the building with grants, private money, and "
  "donated labor. <b>Four,</b> say publicly that the district will grow this school; uncertainty is its own "
  "enrollment killer. There is no pot of "
  "money these asks would squander: if staff are reassigned, closure frees only the $58,774 utilities line. "
  "A closed school cannot be recalled by the children it displaces. A growth plan can be measured, every "
  "year, by everyone", body))
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
