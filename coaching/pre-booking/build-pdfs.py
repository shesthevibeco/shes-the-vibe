#!/usr/bin/env python3
"""Convert She's The Vibe coaching markdown docs to branded PDFs."""
import sys
sys.path.insert(0, "/home/hatch/.local/lib/python3.12/site-packages")
import markdown
from weasyprint import HTML

BRAND_CSS = """
@page {
    size: Letter;
    margin: 2.2cm 2cm 2.5cm 2cm;
    @bottom-center {
        content: "She's The Vibe Co  ·  Practical. Pretty. You.  ·  shesthevibe.co";
        font-size: 8pt;
        color: #C9A96E;
        font-family: Georgia, serif;
    }
    @bottom-right {
        content: counter(page);
        font-size: 8pt;
        color: #999;
        font-family: Georgia, serif;
    }
}
body {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 11pt;
    line-height: 1.65;
    color: #2c2c2c;
}
h1 {
    color: #6B1D2A;
    font-size: 22pt;
    text-align: center;
    margin-top: 0.5cm;
    margin-bottom: 0.2cm;
    letter-spacing: 1px;
}
h1 + p {
    text-align: center;
    color: #C9A96E;
    font-size: 13pt;
    font-style: italic;
    margin-bottom: 1cm;
}
h2 {
    color: #6B1D2A;
    font-size: 14pt;
    border-bottom: 2px solid #C9A96E;
    padding-bottom: 4px;
    margin-top: 1.2cm;
}
h3 {
    color: #6B1D2A;
    font-size: 12pt;
    margin-top: 0.8cm;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin: 0.6cm 0;
    font-size: 10pt;
}
th {
    background-color: #6B1D2A;
    color: #FDF8F0;
    padding: 8px 10px;
    text-align: left;
    font-weight: bold;
}
td {
    padding: 7px 10px;
    border-bottom: 1px solid #e8ddd0;
}
tr:nth-child(even) td {
    background-color: #FDF8F0;
}
blockquote {
    border-left: 4px solid #C9A96E;
    margin: 0.6cm 0;
    padding: 0.4cm 0.8cm;
    background: #FDF8F0;
    color: #5a4a3a;
    font-style: italic;
}
hr {
    border: none;
    border-top: 1px solid #C9A96E;
    margin: 1cm 0;
}
strong { color: #6B1D2A; }
a { color: #6B1D2A; }
ul, ol { padding-left: 1.2cm; }
li { margin-bottom: 0.25cm; }
.cover-accent {
    text-align: center;
    color: #C9A96E;
    font-size: 18pt;
    letter-spacing: 8px;
    margin: 0.3cm 0 0.8cm 0;
}
"""

def md_to_pdf(md_path, pdf_path, title):
    with open(md_path) as f:
        md_text = f.read()
    html_body = markdown.markdown(md_text, extensions=["tables", "fenced_code"])
    # Add decorative accent after the first h1 block
    html_body = html_body.replace("</h1>", "</h1>\n<div class='cover-accent'>&#10022; &#10022; &#10022;</div>", 1)
    full_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{title}</title>
<style>{BRAND_CSS}</style></head>
<body>{html_body}</body></html>"""
    HTML(string=full_html).write_pdf(pdf_path)
    print(f"Created: {pdf_path}")

if __name__ == "__main__":
    base = "/home/hatch/workspace/shes-the-vibe/coaching/pre-booking/"
    md_to_pdf(base + "pre-booking-packet.md", base + "pre-booking-packet.pdf",
              "She's The Vibe — Coaching Pre-Booking Packet")
    md_to_pdf(base + "intake-form-fillable.md", base + "intake-form-fillable.pdf",
              "She's The Vibe — Coaching Intake Form")
