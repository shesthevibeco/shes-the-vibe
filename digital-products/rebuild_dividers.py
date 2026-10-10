#!/usr/bin/env python3
"""Rebuild all 50 tab-divider pages with STV luxury styling, preserving everything else."""
import os, re
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject

BASE = os.path.dirname(os.path.abspath(__file__))
COVERS = os.path.join(BASE, "covers")
W, H = 1224, 1584
PLAYFAIR = "/tmp/PlayfairDisplay-Bold.ttf"
CREAM = (250, 245, 234)
GOLD = (201, 162, 94)
GOLD_LIGHT = (233, 211, 160)

# (template, pdf, [(page, kicker, title)])
DIVIDERS = [
    ("wellness", "The_Whole_Vibe_Mind_Body_Soul_Wellness_Journal_v2.pdf", [
        (9, "JOURNAL 1", "Vision + Intentions"),
        (31, "JOURNAL 3", "Mindful Moments"),
        (41, "JOURNAL 4", "Body Vibe"),
        (53, "JOURNAL 5", "Move Your Vibe"),
        (67, "JOURNAL 6", "Nourished, Not Perfect"),
        (79, "JOURNAL 7", "Soul Care"),
        (97, "JOURNAL 9", "Gentle Goals"),
        (105, "JOURNAL 10", "Reset + Reflect"),
    ]),
    ("healing", "Healing_Vibe_Inner_Child_Boundaries_Self_Trust_Journal_v2.pdf", [
        (12, "PART ONE", "Before I Learned\nto Survive"),
        (24, "PART TWO", "The Patterns That\nKept Trying"),
        (36, "PART THREE", "Meeting Your\nYounger Selves"),
        (48, "PART FOUR", "What Was Lost.\nWhat Was Unfair."),
        (60, "PART FIVE", "Protection\nWithout Apology"),
        (73, "PART SIX", "Come Back to\nYour Own Signal"),
        (88, "PART SEVEN", "Love With Room\nto Breathe"),
        (111, "PART NINE", "The Life I\nChoose Now"),
    ]),
    ("reading", "Reading_Vibe_Book_Lovers_Library_Journal_v2.pdf", [
        (11, "PART ONE", "My Personal Library"),
        (21, "PART TWO", "TBR Headquarters"),
        (32, "PART THREE", "The Reading Log"),
        (49, "PART FOUR", "Reviews That Sound\nLike You"),
        (58, "PART FIVE", "Challenges\nWithout Pressure"),
        (66, "PART SIX", "Book Club"),
        (75, "PART SEVEN", "Joy, Taste +\nBookish Chaos"),
    ]),
    ("dream", "Dream_Vibe_Guided_Dream_Journal_v2.pdf", [
        (2, "DREAM CHAPTER 1", "Begin Here"),
        (11, "DREAM CHAPTER 2", "Capture"),
        (18, "DREAM CHAPTER 3", "Special Dreams"),
        (25, "DREAM CHAPTER 4", "Patterns"),
        (34, "DREAM CHAPTER 5", "Deeper Reflection"),
    ]),
    ("tarot", "Read_the_Energy_Tarot_Oracle_Spiritual_Practice_Journal_v2.pdf", [
        (2, "PRACTICE 1", "Foundations"),
        (11, "PRACTICE 2", "Everyday Magic"),
        (18, "PRACTICE 3", "Cleansing +\nGrounding"),
        (25, "PRACTICE 4", "Crystals +\nDivination"),
        (46, "PRACTICE 5", "Ritual + Rhythm"),
    ]),
    ("faith", "Faith_Vibe_Life_and_Bible_Companion_v2.pdf", [
        (9, "COMPANION 1", "Meet the Bible"),
        (17, "COMPANION 2", "Maps + Places"),
        (24, "COMPANION 3", "Family + People"),
        (30, "COMPANION 4", "66-Book Guide"),
        (64, "COMPANION 5", "Bible in a Year"),
        (79, "COMPANION 6", "Study the Word"),
        (90, "COMPANION 7", "Scripture for Life"),
        (99, "COMPANION 8", "Prayer + Presence"),
        (109, "COMPANION 9", "Faith in Real Life"),
        (118, "COMPANION 10", "Reset + Continue"),
    ]),
    ("ancient", "Faith_Vibe_Ethiopian_and_Ancient_Books_Expansion_v2.pdf", [
        (7, "COMPANION 1", "Canon + Context"),
        (13, "COMPANION 2", "History +\nRestoration"),
        (21, "COMPANION 3", "Wisdom +\nBiblical Additions"),
        (30, "COMPANION 4", "Ancient +\nEthiopian Texts"),
        (38, "COMPANION 5", "Read + Connect"),
        (48, "COMPANION 6", "Study + Reflect"),
        (55, "COMPANION 7", "Continue With\nHumility"),
    ]),
]


def tracked_text(draw, xy, text, font, fill, tracking=0):
    x, y = xy
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x -= total / 2
    for ch, wch in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill, anchor="lm")
        x += wch + tracking


def make_divider(template, kicker, title, out_path):
    bg = Image.open(os.path.join(COVERS, f"divider-{template}-bg.png")).convert("RGB")
    tr = W / H
    bw, bh = bg.size
    if bw / bh > tr:
        nw = int(bh * tr); x0 = (bw - nw) // 2
        bg = bg.crop((x0, 0, x0 + nw, bh))
    else:
        nh = int(bw / tr); y0 = (bh - nh) // 2
        bg = bg.crop((0, y0, bw, y0 + nh))
    bg = bg.resize((W, H), Image.LANCZOS)

    # center scrim
    scrim = Image.new("L", (1, H), 0)
    sd = ImageDraw.Draw(scrim)
    for yy in range(H):
        d = abs(yy / H - 0.5)
        sd.point([(0, yy)], max(0, int(140 * (1 - d / 0.4))))
    scrim = scrim.resize((W, H)).filter(ImageFilter.GaussianBlur(70))
    bg = Image.composite(Image.new("RGB", (W, H), (10, 4, 8)), bg, scrim)

    d = ImageDraw.Draw(bg)
    f_kick = ImageFont.truetype(PLAYFAIR, 46)
    cy = H // 2
    tracked_text(d, (W / 2, cy - 150), kicker, f_kick, GOLD, tracking=12)

    lines = title.split("\n")
    f_title = ImageFont.truetype(PLAYFAIR, 110)
    # shrink if too wide
    while any(d.textlength(l, font=f_title) > W - 180 for l in lines):
        f_title = ImageFont.truetype(PLAYFAIR, f_title.size - 6)
    lh = int(f_title.size * 1.25)
    y0 = cy - 40 - (len(lines) - 1) * lh / 2
    for i, line in enumerate(lines):
        d.text((W / 2, y0 + i * lh), line, font=f_title, fill=CREAM,
               anchor="mm", stroke_width=1, stroke_fill=(20, 8, 12))
    # gold rule
    maxw = max(d.textlength(l, font=f_title) for l in lines)
    ry = y0 + (len(lines) - 1) * lh + 85
    d.line([(W / 2 - maxw / 2, ry), (W / 2 + maxw / 2, ry)], fill=GOLD, width=3)

    bg.save(out_path)


def main():
    os.makedirs(os.path.join(COVERS, "dividers"), exist_ok=True)
    by_pdf = {}
    for template, pdf, pages in DIVIDERS:
        repl = {}
        for pnum, kicker, title in pages:
            slug = re.sub(r"[^a-z0-9]+", "-", f"{template}-{pnum}-{kicker}".lower()).strip("-")
            out = os.path.join(COVERS, "dividers", f"{slug}.png")
            make_divider(template, kicker, title, out)
            # one-page pdf
            img = Image.open(out).convert("RGB").resize((612, 792), Image.LANCZOS)
            pdf_one = out.replace(".png", ".pdf")
            img.save(pdf_one, "PDF", resolution=72.0)
            repl[pnum] = pdf_one
            print("  divider", pnum, kicker, "-", title.replace(chr(10), " / "))
        by_pdf[pdf] = repl

    for pdf, repl in by_pdf.items():
        src = os.path.join(BASE, pdf)
        reader = PdfReader(src)
        writer = PdfWriter()
        for i, page in enumerate(reader.pages, start=1):
            if i in repl:
                writer.add_page(PdfReader(repl[i]).pages[0])
            else:
                writer.add_page(page)
        try:
            if "/AcroForm" in reader.trailer["/Root"]:
                writer._root_object[NameObject("/AcroForm")] = reader.trailer["/Root"]["/AcroForm"]
        except Exception as e:
            print("  [warn] acroform", e)
        out = os.path.join(BASE, pdf.replace("_v2.pdf", "_v3.pdf"))
        with open(out, "wb") as f:
            writer.write(out)
        chk = PdfReader(out)
        nf = len(chk.get_fields() or {})
        print(f"{pdf}: {len(reader.pages)}->{len(chk.pages)} pages, {nf} fields, {len(repl)} dividers swapped")


if __name__ == "__main__":
    main()
