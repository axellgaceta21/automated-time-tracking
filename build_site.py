"""One-time site assembly and lossless source asset copying. Run with Python + Pillow."""
from pathlib import Path
from PIL import Image
import shutil, html

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'public'
for folder in ['assets/images/originals', 'assets/images/previews', 'assets/css', 'assets/js']:
    (OUT / folder).mkdir(parents=True, exist_ok=True)
files = {
 'workflow': 'n8n Workflow - Messy Data to Self-Tracking Tracker.png',
 'drive': 'Google Drive Trigger - upload xlsx here.png',
 'raw': 'raw-xlsx-file.png', 'clean': 'CLEANED_DATA.png',
 'log': 'VALIDATION_LOG.png', 'source': 'RAW-DATA.png',
 'dashboard': 'DASHBOARD.png', 'architecture': 'Time Report Workflow Architecture.png',
 'gmail': 'New Report Generated Gmail.png'
}
titles = {'workflow':'The complete n8n workflow', 'drive':'Google Drive export folder', 'raw':'Original Excel timesheet export', 'clean':'CLEANED_DATA · Standardized records and review statuses', 'log':'VALIDATION_LOG · Detected issues and review actions', 'source':'RAW_DATA · Original employee time records', 'dashboard':'DASHBOARD · Sample-run data quality', 'architecture':'Simplified business-process overview', 'gmail':'New Report Generated Gmail notification'}
for key, filename in files.items():
    shutil.copy2(ROOT / filename, OUT / 'assets/images/originals' / filename)
    im = Image.open(ROOT / filename)
    im.thumbnail((1400, 1300))
    im.save(OUT / f'assets/images/previews/{key}.webp', quality=88)
shutil.copy2(ROOT / 'logo.png', OUT / 'assets/images/logo.png')

def figure(key, eager=False, cls=''):
    w,h=Image.open(ROOT/files[key]).size
    return f'''<figure class="screenshot {cls}"><button class="image-trigger" data-image="assets/images/originals/{html.escape(files[key], quote=True)}" data-title="{titles[key]}" aria-label="Enlarge {titles[key]}"><img src="assets/images/previews/{key}.webp" width="{w}" height="{h}" alt="{titles[key]}" loading="{'eager' if eager else 'lazy'}" {'fetchpriority="high"' if eager else ''}><span class="enlarge">↗ <span>Explore full image</span></span></button><figcaption>{titles[key]} <span>Click to inspect ↗</span></figcaption></figure>'''

def head(num, label, title, sub=''):
    return f'<div class="section-heading"><p class="eyebrow">{num} / {label}</p><h2>{title}</h2>{f"<p>{sub}</p>" if sub else ""}</div>'

def step(num,title,tools,copy,visual,extra=''):
    return f'<article class="step"><div class="step-copy"><span class="step-number">{num}</span><p class="eyebrow">{tools}</p><h3>{title}</h3>{copy}{extra}</div><div class="step-visual">{visual}</div></article>'

# Native SVG: each actual n8n node is represented once, with explicit routing.
svg=['<svg class="architecture-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1360 660" role="img" aria-labelledby="arch-title arch-desc"><title id="arch-title">Complete n8n time-report workflow architecture</title><desc id="arch-desc">Stage one watches and filters files, checks for an existing report, and either emails and stops or continues. Stage two downloads, extracts, validates, and prepares metadata. Stage three creates and moves a report, prepares and writes all four tabs in parallel, and waits for all tabs. Stage four retrieves metadata, formats, and emails the new report.</desc><defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0L7 3.5L0 7" fill="#66899d"/></marker></defs>']
def line(points,label='',kind=''):
    svg.append(f'<path d="{points}" class="connector {kind}" marker-end="url(#arrow)"/>')
    if label: svg.append(f'<text x="{label[0]}" y="{label[1]}" class="route-label">{label[2]}</text>')
def node(x,y,w,id,label,kind=''):
    svg.append(f'<g class="diagram-node {kind}"><rect x="{x}" y="{y}" width="{w}" height="46" rx="6"/><text x="{x+11}" y="{y+17}" class="node-id">{id}</text><text x="{x+11}" y="{y+34}">{html.escape(label)}</text></g>')
def group(x,y,w,h,index,title):
    svg.append(f'<rect class="stage-frame" x="{x}" y="{y}" width="{w}" height="{h}" rx="9"/><text x="{x+14}" y="{y+21}" class="stage-label">{index} / {html.escape(title)}</text>')

# Four compact stage frames retain every source node while avoiding a tall reading column.
group(8,8,440,195,'01','DETECT & ROUTE')
node(24,40,180,'01','Watch Time Exports'); node(224,40,205,'02','Filter RAW Files')
node(24,100,180,'02A','Check Existing Report'); node(224,100,205,'02B','Report Already Exists?','decision')
node(111,154,225,'02C','Email Existing Report','terminal')
line('M204 63 H224');line('M326 86 V93 H114 V100');line('M204 123 H224');line('M326 146 V154')
line('M429 123 H452 V105 H472', (432,97,'NO'))
svg.append('<text x="340" y="150" class="route-label">YES · STOP</text>')

group(462,8,890,195,'02','EXTRACT & VALIDATE')
for i,(id,label) in enumerate([('03','Download Excel Export'),('04','Extract Time Entries'),('05','Validate & Normalize Data'),('06','Prepare Report Metadata')]):
    x=476+i*216
    node(x,80,200,id,label,'decision' if id=='05' else '')
    if i<3: line(f'M{x+200} 103 H{x+212}')

group(8,215,1344,315,'03','BUILD THE FOUR-TAB REPORT')
node(24,264,218,'07','Create Google Sheets Report');node(258,264,205,'08','Move Report to Folder')
line('M1224 126 V252 H133 V264',(1100,247,'NEW REPORT'))
line('M242 287 H258');line('M360 310 V330 H1248')
for i,(key,start) in enumerate([('RAW_DATA',9),('CLEANED_DATA',11),('VALIDATION_LOG',13),('DASHBOARD',15)]):
    x=356+i*242
    svg.append(f'<path d="M{x+105} 330 V343" class="connector" marker-end="url(#arrow)"/>')
    node(x,343,210,f'{start:02}',f'Prepare {key}')
    line(f'M{x+105} 389 V411')
    node(x,411,210,f'{start+1:02}',f'Write {key}')
    svg.append(f'<path d="M{x+105} 457 V472" class="connector"/>')
svg.append('<path d="M461 472 H1188 M676 472 V479" class="connector" marker-end="url(#arrow)"/>')
node(558,479,236,'17','Wait for All Report Tabs','decision')

group(8,540,1344,120,'04','FORMAT & NOTIFY')
stage4=[('18','Get Spreadsheet Metadata'),('19','Prepare Formatting Requests'),('20','Apply Spreadsheet Formatting'),('21','Prepare Advanced Formatting'),('22','Apply Advanced Formatting'),('23','Email New Report Generated')]
width=205
for i,(id,label) in enumerate(stage4):
    x=24+i*220
    node(x,585,width,id,label,'finish' if id=='23' else '')
    if i<5: line(f'M{x+width} 608 H{x+215}')
line('M676 525 V572 H126 V585')
svg.append('</svg>')

tabs=''; panels=''
descriptions={'source':'Preserves original employee time records for reference, comparison, and auditing.', 'clean':'Standardized records, calculated information, and validation statuses in one reviewable dataset.', 'log':'Detected issues, affected records, and recommended actions make the review process traceable.', 'dashboard':'A concise overview of processing results and the quality of the sample dataset.'}
for i,(key,label) in enumerate([('source','RAW_DATA'),('clean','CLEANED_DATA'),('log','VALIDATION_LOG'),('dashboard','DASHBOARD')]):
    tabs+=f'<button role="tab" id="tab-{key}" aria-controls="panel-{key}" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}">{label}</button>'
    panels+=f'<div role="tabpanel" id="panel-{key}" aria-labelledby="tab-{key}" tabindex="0" {"hidden" if i else ""}><p>{descriptions[key]}</p>{figure(key,cls="report-image")}</div>'

steps=step('01','Monitor new time exports','Google Drive / n8n','<p>A file-created trigger watches a designated Google Drive folder. The RAW-file filter allows only relevant exports to continue.</p><p class="outcome">A controlled entry point for incoming timesheets.</p>',figure('drive'))
steps+=step('02','Prevent duplicate reports','Google Drive / n8n / Gmail','<p>The workflow searches for a corresponding report before processing the export.</p><p>If a report exists, Gmail sends the existing-report notification and that branch stops. Otherwise, the file continues to extraction.</p><p class="outcome">One decision. Two distinct execution paths.</p>',figure('workflow'))
steps+=step('03','Download and extract Excel data','Google Drive / n8n','<p>The export is downloaded and its time entries are extracted: employee names, work dates, clock-in and clock-out times, reported hours, assignments, and notes.</p><p class="outcome">Source information stays available for comparison and auditing.</p>',figure('raw'))
steps+=step('04','Validate and normalize data','JavaScript / n8n','<p>JavaScript standardizes supported formats and evaluates records for inconsistencies. Uncertain information is flagged for verification.</p><ul class="validation-list"><li>Inconsistent date formats</li><li>Duplicate entries</li><li>Overlapping shifts</li><li>Missing or invalid values</li><li>Reported vs. calculated hours</li><li>Conflicting information</li></ul><div class="status-note"><code class="ready">✓ READY</code><p>No unresolved issues requiring manual review.</p><code class="pending">! PENDING_REVIEW</code><p>Missing, conflicting, or questionable information needs human verification.</p></div>',figure('clean')+figure('log'))
steps+=f'<article class="report-stage"><div class="step-copy"><span class="step-number">05</span><p class="eyebrow">Google Sheets / Google Drive / n8n</p><h3>One report. Four perspectives.</h3><p>The automation creates a Google Sheets report and writes four structured datasets in separate branches. Explore the actual output from the sample run.</p></div><div class="report-showcase"><div role="tablist" aria-label="Generated report tabs">{tabs}</div>{panels}</div></article>'
steps+=step('06','Synchronize and format reports','n8n / Google Sheets API','<p>Node 17 waits for all four report-writing branches. Spreadsheet metadata is then retrieved and formatting requests are prepared.</p><p>Standard formatting is applied first, followed by advanced formatting through the Google Sheets API.</p><p class="outcome">Formatting begins after all required report tabs have been written.</p>',figure('workflow'))
steps+=step('07','Send the report notification','Gmail / n8n','<p>After report generation and formatting, Gmail sends the new-report notification with report information and access to the generated tracker.</p><p>This is the final success notification, separate from the earlier existing-report branch.</p>',figure('gmail',cls='gmail-screenshot'))

techs=[('n8n','n8n','Automation & orchestration','Coordinates detection, filtering, conditional routing, processing, four reporting branches, synchronization, and notifications.'),('{ }','JavaScript','Data processing','Handles record normalization, validation logic, calculations, and dataset preparation.'),('△','Google Drive','File management','Monitors the folder, searches for existing reports, downloads exports, and organizes generated reports.'),('▦','Google Sheets','Spreadsheet reporting','Stores original records, cleaned records, validation issues, and the summary dashboard.'),('API','Google Sheets API','Spreadsheet formatting','Retrieves spreadsheet metadata and applies standard and advanced formatting operations.'),('M','Gmail','Notifications','Sends separate notifications for an existing report and a newly generated report.')]
technology=''.join(f'<article class="tech"><span class="tech-icon" aria-hidden="true">{icon}</span><div><p class="eyebrow">{role}</p><h3>{name}</h3><p>{desc}</p></div></article>' for icon,name,role,desc in techs)

document=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#0B1220"><title>Automated Time Tracking &amp; Data Validation System | Axell Gaceta</title><meta name="description" content="An automation engineering case study showcasing how n8n, JavaScript, and Google Workspace transform Excel timesheet exports into validated, self-checking Google Sheets reports."><meta property="og:title" content="Automated Time Tracking &amp; Data Validation System | Axell Gaceta"><meta property="og:description" content="From messy timesheets to self-checking reports. Explore an n8n, JavaScript, and Google Workspace automation case study."><meta property="og:type" content="website"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;450;500;550;600;650;700;750;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"><link rel="stylesheet" href="assets/css/style.css"><script src="assets/js/main.js" defer></script><script src="assets/js/image-viewer.js" defer></script></head>
<body><a class="skip-link" href="#main">Skip to content</a><header class="site-header"><div class="nav-wrap"><a class="brand" href="#hero" aria-label="Timeflow case study home"><svg viewBox="0 0 32 32" width="30" height="30" fill="none" aria-hidden="true"><rect x="2" y="2" width="28" height="28" rx="8" stroke="currentColor"/><path d="M9 10h14M16 10v13M11 19l5 5 5-5" stroke="currentColor" stroke-width="2"/></svg><span>AXELL<span class="brand-divider">/</span><span class="brand-light">CASE STUDY</span></span></a><nav aria-label="Main navigation"><a href="#overview">Overview</a><a href="#problem">Problem &amp; solution</a><a href="#architecture">Architecture</a><a href="#workflow">Workflow</a><a href="#demo">Demo</a><a href="#technologies">Stack</a><a href="#footer">About</a></nav><a class="portfolio-link" href="https://axell-builds.lovable.app/" target="_blank" rel="noopener noreferrer">Portfolio ↗</a></div></header>
<main id="main">
<section id="hero" class="hero container"><div class="hero-meta"><p class="eyebrow"><span class="live-dot"></span> Automation engineering / Case study</p><span class="project-type">n8n × Google Workspace</span></div><div class="hero-intro"><div><h1>Automated Time Tracking &amp; Data Validation System</h1><p class="hero-subtitle">From messy timesheets to self-checking reports.</p></div><div class="hero-description"><p>A repeatable n8n and JavaScript workflow that turns raw Excel timesheet exports into structured, validated Google Sheets reports.</p><div class="hero-actions"><a href="#architecture" class="button primary">Explore the workflow <span>↓</span></a><a href="#demo" class="text-link">Watch walkthrough ↗</a></div></div></div><ul class="tech-tags" aria-label="Project technologies">{''.join(f'<li>{x}</li>' for x in ['n8n','JavaScript','Google Drive','Google Sheets','Google Sheets API','Gmail'])}</ul><div class="hero-frame"><div class="frame-bar"><span><i></i><i></i><i></i></span><span>TIME EXPORT → VALIDATED REPORT</span><span class="frame-status">● n8n workflow</span></div>{figure('workflow',True)}<div class="frame-bottom"><span>Complete automation · 23 nodes · 4 report branches</span><span>Click to inspect ↗</span></div></div></section>
<section id="overview" class="section container">{head('01','THE PROJECT','Project Overview')}<div class="overview-grid"><div class="overview-copy"><p class="lead">A repeatable workflow that transforms raw Excel timesheet exports into structured, validated Google Sheets reports.</p><p>The automation detects new files in Google Drive, prevents duplicate report generation, extracts employee time entries, normalizes supported formats, flags questionable records, and sends a report-ready notification.</p></div><ul class="capabilities">{''.join(f'<li><span aria-hidden="true">✓</span>{x}</li>' for x in ['Automated file detection','Duplicate-report prevention','Excel data extraction','Data normalization & validation','Four-tab Sheets reporting','Automated spreadsheet formatting','Gmail notifications','Human-review safeguards'])}</ul></div><div class="sample-heading"><span class="eyebrow">Sample processing run</span><p>Observed output · not ongoing production metrics</p></div><div class="metrics"><div><strong>28</strong><span>Records processed</span></div><div><strong class="success">17</strong><span>Clean records</span></div><div><strong class="warning">11</strong><span>Requiring review</span></div><div><strong>60.71<span>%</span></strong><span>Clean data rate</span></div></div><div class="support-metrics"><span><b>13</b> Validation issues</span><span><b>31</b> Automatic normalizations</span><span><b>1</b> Duplicate record</span><a href="#workflow" data-open-dashboard>Inspect dashboard ↗</a></div></section>
<section id="problem" class="section container">{head('02','WHY IT EXISTS','The Problem &amp; The Solution','Less repetitive cleaning. More clarity about what needs attention.')}<div class="comparison"><article><p class="eyebrow warning">BEFORE / MANUAL REVIEW</p><h3>Messy inputs. Hidden inconsistencies.</h3><p>Timesheet exports can contain mixed formats, missing information, duplicates, overlapping shifts, and discrepancies between reported and calculated hours.</p><p>Manual cleaning is repetitive, and questionable records can be missed or demand extensive investigation.</p>{figure('raw')}</article><article><p class="eyebrow accent">AFTER / STRUCTURED VALIDATION</p><h3>Organized outputs. Visible exceptions.</h3><p>Supported formats are standardized. Records without unresolved issues become <code>READY</code>; questionable records become <code>PENDING_REVIEW</code>.</p><p>Original records remain available, and detected issues are documented for human verification.</p>{figure('clean')}</article></div><p class="integrity-note"><span aria-hidden="true">↳</span> Automation handles supported normalization. People resolve uncertain or conflicting records.</p></section>
<section id="architecture" class="section container">{head('03','SYSTEM DESIGN','Workflow Architecture','The complete execution path, from file detection to report notification.')}<div class="architecture-header"><span><i class="legend-dot"></i> Execution path <i class="legend-dot decision-dot"></i> Decision &amp; synchronization</span><span>Swipe or scroll horizontally on smaller screens ↔</span></div><div class="diagram-scroll" tabindex="0" role="region" aria-label="Scrollable workflow architecture diagram">{''.join(svg)}</div><p class="diagram-caption">The duplicate-report path stops after its notification. New reports pass through four parallel tab-writing branches before formatting.</p><details class="reference"><summary>View simplified business-process reference <span>+</span></summary><p>This supporting infographic summarizes the business process; the native diagram above represents the detailed n8n implementation.</p>{figure('architecture',cls='portrait')}</details></section>
<section id="workflow" class="section container">{head('04','INSIDE THE AUTOMATION','Step-by-Step Workflow','Seven stages. A traceable journey from source file to final notification.')}<div class="steps">{steps}</div></section>
<section id="demo" class="section container">{head('05','THE WALKTHROUGH','Watch the Workflow','A walkthrough of the workflow structure, data-processing stages, and reporting outputs.')}<div class="video"><iframe src="https://www.loom.com/embed/a8a529c2c6ef4d51b417c1a500f993bd" loading="lazy" title="Automated Time Tracking and Data Validation System walkthrough by Axell Gaceta" allow="fullscreen; picture-in-picture" allowfullscreen></iframe></div><div class="video-caption"><span>Workflow → validation → four-tab report</span><a class="text-link" href="https://www.loom.com/share/a8a529c2c6ef4d51b417c1a500f993bd" target="_blank" rel="noopener noreferrer">Open walkthrough on Loom ↗</a></div></section>
<section id="technologies" class="section container">{head('06','THE TOOLKIT','Technologies Used','Purpose-built responsibilities. One connected workflow.')}<div class="tech-grid">{technology}</div></section>
</main><footer id="footer"><div class="container"><div class="footer-top"><div><p class="eyebrow">THE BUILDER</p><h2>Built &amp; documented<br>by <span>Axell Gaceta.</span></h2><p>AI Automation Specialist &amp; Web Developer focused on building practical automation systems, intelligent workflows, and business tools.</p></div><a class="button primary" href="https://axell-builds.lovable.app/" target="_blank" rel="noopener noreferrer">Back to main portfolio ↗</a></div><div class="footer-bottom"><span>Automation with a clear audit trail.</span><div><a href="https://github.com/axellgaceta21" target="_blank" rel="noopener noreferrer">GitHub ↗</a><a href="https://www.linkedin.com/in/axellgaceta21/" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a><a href="https://drive.google.com/file/d/1KCkvbanLu4UV6E7QBP6FY8yVaKPkto5I/view?usp=sharing" target="_blank" rel="noopener noreferrer">Resume ↗</a><a href="#hero">Back to top ↑</a></div></div></div></footer>
<dialog id="image-viewer" aria-labelledby="viewer-title"><div class="viewer-header"><div><h2 id="viewer-title">Screenshot viewer</h2><p>Scroll to inspect · Drag to pan · + / − zoom · 0 actual size · F fit · Esc close</p></div><button id="viewer-close" aria-label="Close image viewer">✕</button></div><div class="viewer-toolbar" role="group" aria-label="Image controls"><button data-action="out" aria-label="Zoom out">−</button><output id="zoom-level" aria-live="polite">100%</output><button data-action="in" aria-label="Zoom in">+</button><button data-action="actual">100% / Reset</button><button data-action="fit">Fit to screen</button></div><div class="viewer-viewport" tabindex="0" role="region" aria-label="Scrollable full-resolution image"><div class="viewer-canvas"><img id="viewer-image" alt="" draggable="false"></div></div></dialog></body></html>'''
start = document.index('<section id="hero"')
end = document.index('<section id="overview"', start)
hero_html = f'''<section id="hero" class="hero container"><div class="hero-meta"><p class="eyebrow"><span class="live-dot"></span> Automation engineering / Case study</p><span class="project-type">n8n × Google Workspace</span></div><div class="hero-intro"><div><h1>Automated Time Tracking &amp; Data Validation System</h1><p class="hero-subtitle">From messy timesheets to self-checking reports.</p></div><div class="hero-description"><p>A repeatable n8n and JavaScript workflow that turns raw Excel timesheet exports into structured, validated Google Sheets reports.</p><div class="hero-actions"><a href="#architecture" class="button primary">Explore the workflow <span>↓</span></a><a href="#demo" class="text-link">Watch walkthrough ↗</a></div></div></div><ul class="tech-tags" aria-label="Project technologies">{''.join(f'<li>{x}</li>' for x in ['n8n','JavaScript','Google Drive','Google Sheets','Google Sheets API','Gmail'])}</ul><div class="hero-frame"><div class="frame-bar"><span><i></i><i></i><i></i></span><span>TIME EXPORT → VALIDATED REPORT</span><span class="frame-status">● n8n workflow</span></div>{figure('workflow',True)}<div class="frame-bottom"><span>Complete automation · 26 workflow nodes · 4 report branches</span><span>Click to inspect ↗</span></div></div></section>'''
document = document[:start] + hero_html + document[end:]
start = document.index('<footer id="footer">')
end = document.index('</footer>', start) + len('</footer>')
footer_html = '''<footer id="footer"><div class="container footer-center"><a class="footer-logo" href="#hero" aria-label="Back to case study top"><img src="assets/images/logo.png" width="251" height="230" alt="Axell Gaceta logo"></a><p class="eyebrow">BUILT &amp; DOCUMENTED BY</p><h2>Axell Gaceta</h2><p class="footer-role">AI Automation Specialist · Web Developer</p><nav class="footer-links" aria-label="Professional links"><a href="https://github.com/axellgaceta21" target="_blank" rel="noopener noreferrer">GitHub <span>↗</span></a><a class="footer-primary" href="https://axell-builds.lovable.app/" target="_blank" rel="noopener noreferrer">Portfolio <span>↗</span></a><a href="https://drive.google.com/file/d/1KCkvbanLu4UV6E7QBP6FY8yVaKPkto5I/view?usp=sharing" target="_blank" rel="noopener noreferrer">Resume <span>↗</span></a><a href="https://www.linkedin.com/in/axellgaceta21/" target="_blank" rel="noopener noreferrer">LinkedIn <span>↗</span></a></nav><div class="footer-divider"></div><p class="copyright">© 2026 Axell Gaceta. All rights reserved.</p></div></footer>'''
document = document[:start] + footer_html + document[end:]
document = document.replace('<link rel="stylesheet" href="assets/css/style.css">', '<link rel="icon" type="image/png" href="assets/images/logo.png"><link rel="stylesheet" href="assets/css/style.css">')
(OUT / 'index.html').write_text(document, encoding='utf-8')
print('Built public/index.html and copied 9 original/preview screenshot pairs, including the approved Gmail image.')
