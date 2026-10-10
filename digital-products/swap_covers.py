#!/usr/bin/env python3
"""Replace page 1 of each journal PDF with the new luxury cover, preserving form fields."""
import os
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject

BASE = os.path.dirname(os.path.abspath(__file__))
COVERS = os.path.join(BASE, "covers")

MAP = [
    ("wellness", "The_Whole_Vibe_Mind_Body_Soul_Wellness_Journal_v1.pdf"),
    ("faith", "Faith_Vibe_Life_and_Bible_Companion_v1.pdf"),
    ("healing", "Healing_Vibe_Inner_Child_Boundaries_Self_Trust_Journal_v1.pdf"),
    ("reading", "Reading_Vibe_Book_Lovers_Library_Journal_v1.pdf"),
    ("tarot", "Read_the_Energy_Tarot_Oracle_Spiritual_Practice_Journal_v1.pdf"),
    ("dream", "Dream_Vibe_Guided_Dream_Journal_v1.pdf"),
    ("ancient", "Faith_Vibe_Ethiopian_and_Ancient_Books_Expansion_v1.pdf"),
    ("reflection", "Reading_Vibe_Reusable_Book_Reflection_Pack_v1.pdf"),
]

for key, pdf_name in MAP:
    src = os.path.join(BASE, pdf_name)
    cover_png = os.path.join(COVERS, f"cover-{key}-final.png")

    # one-page PDF from the cover PNG at exactly 612x792pt
    from PIL import Image
    img = Image.open(cover_png).convert("RGB")
    img = img.resize((612, 792), Image.LANCZOS)
    cover_pdf_path = os.path.join(COVERS, f"cover-{key}-page.pdf")
    img.save(cover_pdf_path, "PDF", resolution=72.0)

    reader = PdfReader(src)
    cover_reader = PdfReader(cover_pdf_path)
    writer = PdfWriter()

    writer.add_page(cover_reader.pages[0])
    for p in reader.pages[1:]:
        writer.add_page(p)

    # preserve interactive form fields
    try:
        if "/AcroForm" in reader.trailer["/Root"]:
            writer._root_object[NameObject("/AcroForm")] = reader.trailer["/Root"]["/AcroForm"]
    except Exception as e:
        print(f"  [warn] acroform: {e}")

    out = os.path.join(BASE, pdf_name.replace("_v1.pdf", "_v2.pdf"))
    with open(out, "wb") as f:
        writer.write(f)

    # verify
    check = PdfReader(out)
    fields = 0
    try:
        fields = len(check.get_fields() or {})
    except Exception:
        pass
    print(f"{pdf_name}: {len(reader.pages)} -> {len(check.pages)} pages, {fields} form fields kept -> {os.path.basename(out)}")
