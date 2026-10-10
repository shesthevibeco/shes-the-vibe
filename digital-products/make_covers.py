#!/usr/bin/env python3
"""Overlay luxury typography on journal cover backgrounds and swap into PDFs."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = os.path.dirname(os.path.abspath(__file__))
COVERS = os.path.join(BASE, "covers")
W, H = 1224, 1584  # 2x US Letter

PLAYFAIR = "/tmp/PlayfairDisplay-Bold.ttf"
PINYON = "/tmp/PinyonScript.ttf"

CREAM = (250, 245, 234)
GOLD = (201, 162, 94)
GOLD_LIGHT = (233, 211, 160)

JOURNALS = [
    # (bg_key, title, subtitle, pdf_file)
    ("wellness", "The Whole Vibe", "MIND \u00b7 BODY \u00b7 SOUL WELLNESS JOURNAL",
     "The_Whole_Vibe_Mind_Body_Soul_Wellness_Journal_v1.pdf"),
    ("faith", "Faith Vibe", "LIFE & BIBLE COMPANION",
     "Faith_Vibe_Life_and_Bible_Companion_v1.pdf"),
    ("healing", "Healing Vibe", "INNER CHILD \u00b7 BOUNDARIES \u00b7 SELF-TRUST",
     "Healing_Vibe_Inner_Child_Boundaries_Self_Trust_Journal_v1.pdf"),
    ("reading", "Reading Vibe", "BOOK LOVERS LIBRARY JOURNAL",
     "Reading_Vibe_Book_Lovers_Library_Journal_v1.pdf"),
    ("tarot", "Read the Energy", "TAROT & ORACLE SPIRITUAL PRACTICE",
     "Read_the_Energy_Tarot_Oracle_Spiritual_Practice_Journal_v1.pdf"),
    ("dream", "Dream Vibe", "GUIDED DREAM JOURNAL",
     "Dream_Vibe_Guided_Dream_Journal_v1.pdf"),
    ("ancient", "Faith Vibe", "ETHIOPIAN & ANCIENT BOOKS",
     "Faith_Vibe_Ethiopian_and_Ancient_Books_Expansion_v1.pdf"),
    ("reflection", "Reading Vibe", "REUSABLE BOOK REFLECTION PACK",
     "Reading_Vibe_Reusable_Book_Reflection_Pack_v1.pdf"),
]


def tracked_text(draw, xy, text, font, fill, tracking=0, anchor="m"):
    """Draw text with letter tracking."""
    x, y = xy
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    if anchor == "m":
        x -= total / 2
    elif anchor == "r":
        x -= total
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill, anchor="lm")
        x += w + tracking
    return total


def make_cover(bg_key, title, subtitle):
    bg = Image.open(os.path.join(COVERS, f"cover-{bg_key}-bg.png")).convert("RGB")
    # center-crop to 1224:1584 then resize
    target_ratio = W / H
    bw, bh = bg.size
    if bw / bh > target_ratio:
        nw = int(bh * target_ratio); x0 = (bw - nw) // 2
        bg = bg.crop((x0, 0, x0 + nw, bh))
    else:
        nh = int(bw / target_ratio); y0 = (bh - nh) // 2
        bg = bg.crop((0, y0, bw, y0 + nh))
    bg = bg.resize((W, H), Image.LANCZOS)

    # soft dark scrim behind text (middle band)
    scrim = Image.new("L", (1, H), 0)
    sd = ImageDraw.Draw(scrim)
    for yy in range(H):
        # peak darkness around 38% height
        d = abs(yy / H - 0.38)
        alpha = max(0, int(150 * (1 - d / 0.35)))
        sd.point([(0, yy)], alpha)
    scrim = scrim.resize((W, H)).filter(ImageFilter.GaussianBlur(60))
    black = Image.new("RGB", (W, H), (10, 4, 8))
    bg = Image.composite(black, bg, scrim)

    d = ImageDraw.Draw(bg)
    f_brand = ImageFont.truetype(PLAYFAIR, 44)
    f_title = ImageFont.truetype(PLAYFAIR, 118)
    f_sub = ImageFont.truetype(PLAYFAIR, 40)

    cy = int(H * 0.38)
    # brand line
    tracked_text(d, (W / 2, int(H * 0.16)), "SHE'S THE VIBE", f_brand, GOLD, tracking=14)
    # thin gold rules flanking brand
    bw_brand = d.textlength("SHE'S THE VIBE", font=f_brand) + 14 * 12
    for sx in (-1, 1):
        x1 = W / 2 + sx * (bw_brand / 2 + 30)
        x2 = W / 2 + sx * (bw_brand / 2 + 150)
        d.line([(x1, int(H * 0.16)), (x2, int(H * 0.16))], fill=GOLD, width=2)

    # title (may need two lines if long)
    if d.textlength(title, font=f_title) > W - 160:
        f_title = ImageFont.truetype(PLAYFAIR, 92)
    d.text((W / 2, cy), title, font=f_title, fill=CREAM, anchor="mm",
           stroke_width=1, stroke_fill=(20, 8, 12))

    # gold rule under title
    tw = d.textlength(title, font=f_title)
    ry = cy + 95
    d.line([(W / 2 - tw / 2, ry), (W / 2 + tw / 2, ry)], fill=GOLD, width=3)

    # subtitle
    tracked_text(d, (W / 2, ry + 70), subtitle, f_sub, GOLD_LIGHT, tracking=8)

    # bottom mark
    f_pin = ImageFont.truetype(PINYON, 64)
    d.text((W / 2, int(H * 0.88)), "a guided journal", font=f_pin,
           fill=GOLD_LIGHT, anchor="mm")

    out = os.path.join(COVERS, f"cover-{bg_key}-final.png")
    bg.save(out)
    print("saved", out)
    return out


if __name__ == "__main__":
    for bg_key, title, subtitle, pdf in JOURNALS:
        make_cover(bg_key, title, subtitle)
