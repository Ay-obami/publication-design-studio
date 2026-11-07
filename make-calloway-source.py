from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from pathlib import Path
import json, random

root=Path(__file__).resolve().parent
src=Path('/home/ayobami/Documents/Approved-Portfolio/01-Approved-Native-Projects/Complete-20-Project-Collection/18-calloway/CONTENT/publication.json')
data=json.loads(src.read_text())
m=data['model']
out=root/'process-assets'/'calloway'
out.mkdir(parents=True,exist_ok=True)

d=Document()
sec=d.sections[0]
sec.top_margin=Inches(.65); sec.bottom_margin=Inches(.65); sec.left_margin=Inches(.7); sec.right_margin=Inches(.7)

p=d.add_paragraph()
r=p.add_run('CALLOWAY HOLDINGS')
r.bold=True; r.font.name='Arial'; r.font.size=Pt(22); r.font.color.rgb=RGBColor(31,52,75)
p.alignment=WD_ALIGN_PARAGRAPH.LEFT

p=d.add_paragraph()
r=p.add_run('ANNUAL REPORT 2026 – WORKING DRAFT')
r.bold=True; r.font.name='Calibri'; r.font.size=Pt(17)

p=d.add_paragraph()
r=p.add_run('WORKING SOURCE DOCUMENT')
r.bold=True; r.font.name='Arial'; r.font.size=Pt(10); r.font.color.rgb=RGBColor(180,65,45)
p.add_run('\nManagement commentary, divisional information and financial tables prepared for publication design.')

p=d.add_paragraph('NOTES FOR DESIGNER: please make this feel professional / annual report. Need something modern but serious. Some charts can be pulled from the numbers below. Images supplied separately. Page count approx 45–50.')
p.runs[0].font.name='Calibri'; p.runs[0].font.size=Pt(11)

p=d.add_paragraph()
r=p.add_run('CONTENTS / ROUGH ORDER')
r.bold=True; r.font.name='Times New Roman'; r.font.size=Pt(14)
for text in ['Overview and key performance','Chair and CEO letters','Strategy / business model','Three divisions: Logistics, Energy, Services','People + sustainability','Governance','Financial statements and notes','Shareholder information / contacts']:
    q=d.add_paragraph(text, style='List Bullet')
    q.paragraph_format.left_indent=Inches(.25)

def heading(text,level=1,variant=0):
    p=d.add_paragraph()
    r=p.add_run(text)
    r.bold=True
    if variant%3==0:
        r.font.name='Arial'; r.font.size=Pt(15 if level==1 else 12); r.font.color.rgb=RGBColor(31,52,75)
    elif variant%3==1:
        r.font.name='Calibri'; r.font.size=Pt(16 if level==1 else 11); r.font.color.rgb=RGBColor(0,0,0)
    else:
        r.font.name='Times New Roman'; r.font.size=Pt(14 if level==1 else 12); r.font.color.rgb=RGBColor(58,96,92)
    return p

def body(text,variant=0):
    p=d.add_paragraph(text)
    p.paragraph_format.space_after=Pt([0,5,9][variant%3])
    for r in p.runs:
        r.font.name=['Calibri','Arial','Times New Roman'][variant%3]
        r.font.size=Pt([10.5,11,10][variant%3])
    return p

heading('1. YEAR IN FOCUS',1,0)
body(f"Revenue increased from £{m['revenue'][0]}m to £{m['revenue'][1]:,}m, while operating profit increased from £{m['operating_profit'][0]}m to £{m['operating_profit'][1]}m. The margin therefore moved from 20.4% to 19.6%. Closing cash was £{m['cash'][1]}m and capital expenditure increased to £{m['capex'][1]}m.",0)
body('Designer note: could this be a bold opening spread? Maybe revenue / profit / cash as three numbers. Need to avoid making growth look automatically positive because margin is down.',1)
t=d.add_table(rows=1, cols=3); t.alignment=WD_TABLE_ALIGNMENT.LEFT
t.rows[0].cells[0].text='Measure'; t.rows[0].cells[1].text='2025'; t.rows[0].cells[2].text='2026'
for label,key in [('Revenue £m','revenue'),('Operating profit £m','operating_profit'),('Cash £m','cash'),('Capex £m','capex'),('Employees','employees')]:
    c=t.add_row().cells; c[0].text=label; c[1].text=str(m[key][0]); c[2].text=str(m[key][1])

heading('CHAIR LETTER',1,1)
body('Mara Calloway / Chair',2)
body("Dear shareholders, The central decision in this illustrative year was how to grow without losing control of the balance sheet. We increased capital spending while maintaining a clear view of operating cash and borrowing. Revenue growth gives the group more room to invest, but the margin comparison reminds us that scale alone is not enough.",0)
body("The board's role is to test the reasons behind each investment, ask how the business will measure its progress and make sure someone is responsible for the next review. Logistics has a mature operating base, Energy carries a larger share of the investment programme, and Services provides the people and systems that help customers run their operations.",2)
body('Pull quote maybe: “Accountability stays visible.”',1)

heading('CEO LETTER / draft',1,2)
body('Jon Bell – Chief Executive',0)
body(f"The group entered the year with three priorities: protect the reliability of existing work, invest where capacity is constrained and improve the information available to managers. Group revenue was £{m['revenue'][1]:,}m and operating profit £{m['operating_profit'][1]}m.",1)
body('Need chart? maybe show division totals beside this text.',2)

heading('STRATEGY',1,0)
body('ONE FRAMEWORK / THREE OPERATING BUSINESSES',0)
for x in ['Understand customer requirement','Identify capability needed','Allocate resources','Inspect outcome']:
    d.add_paragraph(x, style='List Number')
body('The framework does not turn every project into a growth project. Maintenance, workforce capability and reporting controls also compete for resources.',2)

heading('BUSINESS MODEL',1,1)
body('[DIAGRAM PLACEHOLDER — customer need > division > assets/people/suppliers > delivery > reporting review]',1)

heading('CAPITAL ALLOCATION',1,2)
t=d.add_table(rows=1,cols=3)
t.style='Table Grid'
t.rows[0].cells[0].text='Division'; t.rows[0].cells[1].text='2025'; t.rows[0].cells[2].text='2026'
for div in m['divisions']:
    c=t.add_row().cells;c[0].text=div['name'];c[1].text=str(div['capex'][0]);c[2].text=str(div['capex'][1])
body('Group capital expenditure increased from £140m to £180m. Energy receives the largest increase in the current-year model.',0)

for idx,div in enumerate(m['divisions']):
    heading(div['name'].upper()+' DIVISION',1,idx)
    body(f"Revenue: £{div['revenue'][0]}m → £{div['revenue'][1]}m | Operating profit: £{div['profit'][0]}m → £{div['profit'][1]}m | Capex: £{div['capex'][0]}m → £{div['capex'][1]}m",idx)
    body(['Sequence of handoffs creates the operating result. Keep exceptions visible.','Build capacity with a review point. Growth and investment belong together.','Make delivery repeatable. Scope, deliver and review.'][idx],(idx+1)%3)
    if idx==1: body('[INSERT WIND FARM IMAGE HERE — supplied separately]',1)
    if idx==2: body('[INSERT GLASS / ARCHITECTURE IMAGE HERE — supplied separately]',1)

heading('PEOPLE + SUSTAINABILITY',1,0)
body(f"Employees increased from {m['employees'][0]:,} to {m['employees'][1]:,}. Training reached {m['training_hours'][1]:,} hours in the current-year model. Energy consumption increased from {m['energy_mwh'][0]:,} MWh to {m['energy_mwh'][1]:,} MWh.",0)
body('Please show denominators / methodology clearly. Do not make intensity look like an absolute outcome.',2)

heading('GOVERNANCE / BOARD',1,1)
body('Governance should connect decisions to evidence. Suggested structure: Board oversight → Executive coordination → Divisional delivery.',1)
body('Board profiles can be compact cards. No photography required.',0)

heading('FINANCIAL STATEMENTS',1,2)
body('Need this section to feel more reference-like than the narrative pages. Tables must be easy to scan. Keep year columns aligned.',2)

def fin_table(title, rows):
    heading(title,2,0)
    t=d.add_table(rows=1,cols=3); t.style='Table Grid'
    for i,x in enumerate(['£m','2025','2026']): t.rows[0].cells[i].text=x
    for label,key in rows:
        c=t.add_row().cells;c[0].text=label;c[1].text=str(m[key][0]);c[2].text=str(m[key][1])

fin_table('INCOME STATEMENT',[('Revenue','revenue'),('Operating cost','operating_cost'),('Operating profit','operating_profit'),('Finance cost','finance_cost'),('Profit before tax','pretax'),('Tax','tax'),('Profit','profit')])
fin_table('FINANCIAL POSITION',[('Tangible assets','ppe'),('Intangibles','intangibles'),('Inventory','inventory'),('Receivables','receivables'),('Cash','cash'),('Total assets','assets'),('Total liabilities','liabilities'),('Equity','equity')])
fin_table('CASH / FUNDING',[('Opening cash','opening_cash'),('Operating cash','operating_cash'),('Capex','capex'),('Bank debt','bank_debt'),('Other debt','other_debt'),('Closing cash','cash')])

heading('NOTES / GLOSSARY / SHAREHOLDER INFO',1,0)
body('Need basis, segments, asset roll-forward, funding, definitions and publication contact information. Keep note numbers easy to follow from statements.',0)
body('Definitions: EBITDA = operating profit plus non-cash asset charges. Net debt = gross borrowing less cash. Intensity = measure divided by stated activity denominator.',2)

p=d.add_paragraph()
p.add_run('END OF WORKING DRAFT — CONTENT STILL NEEDS DESIGN SYSTEM / PAGE ARCHITECTURE / FINAL QA').bold=True
p.runs[0].font.color.rgb=RGBColor(180,65,45)

path=out/'Calloway-Working-Source.docx'
d.save(path)
print(path)
