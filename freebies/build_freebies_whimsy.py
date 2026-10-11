#!/usr/bin/env python3
"""Build the 3 She's The Vibe lead-magnet PDFs — MAXIMUM WHIMSY edition."""
import os
import math
import random
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------- fonts ----------
FONT_DIR = "/home/hatch/workspace/shes-the-vibe/tiktok/final/assets/fonts"
pdfmetrics.registerFont(TTFont('Parisienne', os.path.join(FONT_DIR, 'Parisienne-Regular.ttf')))
pdfmetrics.registerFont(TTFont('Playfair', os.path.join(FONT_DIR, 'PlayfairDisplay-VF.ttf')))
pdfmetrics.registerFont(TTFont('Montserrat', os.path.join(FONT_DIR, 'Montserrat-VF.ttf')))

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "freebies")
os.makedirs(OUT, exist_ok=True)

W, H = LETTER
BURGUNDY = HexColor("#451425")
GOLD = HexColor("#C9A96E")
CREAM = HexColor("#F7E7CE")
DARK = HexColor("#2b0d18")
SOFTGOLD = HexColor("#e8d5ae")
SOFTPINK = HexColor("#F4A7B9")
BLUSH = HexColor("#F9D5D3")
DEEPGOLD = HexColor("#a8842f")
MUTEDROSE = HexColor("#c98a8e")

TITLE_FONT = "Helvetica-Bold"
BODY_FONT = "Helvetica"
ITALIC = "Helvetica-Oblique"
SCRIPT = "Parisienne"
SERIF = "Playfair"
SANS = "Montserrat"

# ============================================================
# WHIMSY DRAWING HELPERS
# ============================================================

def star4(c, cx, cy, r, color=GOLD):
    """4-point sparkle star."""
    c.setFillColor(color)
    p = c.beginPath()
    for i in range(8):
        ang = math.pi * i / 4 - math.pi / 2
        rr = r if i % 2 == 0 else r * 0.35
        x, y = cx + rr * math.cos(ang), cy + rr * math.sin(ang)
        if i == 0:
            p.moveTo(x, y)
        else:
            p.lineTo(x, y)
    p.close()
    c.drawPath(p, fill=1, stroke=0)

def scatter_sparkles(c, n, seed=0, y_range=None, colors=None):
    """Scatter n sparkles randomly on the page."""
    rnd = random.Random(seed)
    colors = colors or [GOLD, GOLD, SOFTGOLD, SOFTPINK]
    ylo, yhi = y_range or (0.5 * inch, H - 0.5 * inch)
    for _ in range(n):
        x = rnd.uniform(0.4 * inch, W - 0.4 * inch)
        y = rnd.uniform(ylo, yhi)
        r = rnd.uniform(4, 14)
        star4(c, x, y, r, rnd.choice(colors))

def doodle_heart(c, cx, cy, size, color=SOFTPINK, filled=True):
    """Cute doodle heart."""
    s = size
    c.setStrokeColor(color)
    c.setLineWidth(1.5)
    p = c.beginPath()
    p.moveTo(cx, cy - s * 0.7)
    p.curveTo(cx - s * 1.3, cy + s * 0.1, cx - s * 0.6, cy + s * 0.8, cx, cy + s * 0.25)
    p.curveTo(cx + s * 0.6, cy + s * 0.8, cx + s * 1.3, cy + s * 0.1, cx, cy - s * 0.7)
    p.close()
    if filled:
        c.setFillColor(color)
        c.drawPath(p, fill=1, stroke=0)
    else:
        c.drawPath(p, fill=0, stroke=1)

def doodle_flower(c, cx, cy, r, petal_color=SOFTPINK, center_color=GOLD):
    """Simple 6-petal doodle flower."""
    c.setFillColor(petal_color)
    for i in range(6):
        ang = math.pi * i / 3
        px = cx + r * 0.7 * math.cos(ang)
        py = cy + r * 0.7 * math.sin(ang)
        c.ellipse(px - r * 0.45, py - r * 0.45, px + r * 0.45, py + r * 0.45, fill=1, stroke=0)
    c.setFillColor(center_color)
    c.circle(cx, cy, r * 0.35, fill=1, stroke=0)

def swirl_divider(c, y, width=3.2 * inch, color=GOLD):
    """Wavy swirl divider with a heart in the center."""
    cx = W / 2
    c.setStrokeColor(color)
    c.setLineWidth(1.5)
    # left swirl
    p = c.beginPath()
    steps = 60
    for i in range(steps + 1):
        t = i / steps
        x = cx - width / 2 + t * (width / 2 - 0.35 * inch)
        yy = y + 6 * math.sin(t * math.pi * 2.5)
        if i == 0:
            p.moveTo(x, yy)
        else:
            p.lineTo(x, yy)
    c.drawPath(p, fill=0, stroke=1)
    # right swirl
    p = c.beginPath()
    for i in range(steps + 1):
        t = i / steps
        x = cx + 0.35 * inch + t * (width / 2 - 0.35 * inch)
        yy = y + 6 * math.sin(t * math.pi * 2.5 + math.pi)
        if i == 0:
            p.moveTo(x, yy)
        else:
            p.lineTo(x, yy)
    c.drawPath(p, fill=0, stroke=1)
    # center heart + sparkles
    doodle_heart(c, cx, y, 10, SOFTPINK)
    star4(c, cx - 0.55 * inch, y + 4, 6)
    star4(c, cx + 0.55 * inch, y - 3, 5)

def corner_flourish(c, color=GOLD):
    """Decorative corners on a page."""
    m = 0.45 * inch
    c.setStrokeColor(color)
    c.setLineWidth(1.5)
    for (x0, y0, dx, dy) in [(m, m, 1, 1), (W - m, m, -1, 1),
                             (m, H - m, 1, -1), (W - m, H - m, -1, -1)]:
        p = c.beginPath()
        p.moveTo(x0, y0 + dy * 0.35 * inch)
        p.curveTo(x0, y0 + dy * 0.12 * inch, x0 + dx * 0.12 * inch, y0, x0 + dx * 0.35 * inch, y0)
        c.drawPath(p, fill=0, stroke=1)
        star4(c, x0 + dx * 0.42 * inch, y0 + dy * 0.42 * inch, 5, color)

def sticker_badge(c, cx, cy, r, number, bg=SOFTPINK, fg=BURGUNDY):
    """Circular sticker-style number badge."""
    c.setFillColor(bg)
    c.circle(cx, cy, r, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.circle(cx, cy, r - 2.5, fill=0, stroke=1)
    c.setFillColor(fg)
    c.setFont(TITLE_FONT, int(r * 0.85))
    c.drawCentredString(cx, cy - r * 0.32, str(number))

def script_header(c, text, y, size=26, color=BURGUNDY):
    """Playful script section header with pink swirl underline."""
    c.setFillColor(color)
    c.setFont(SCRIPT, size)
    c.drawCentredString(W / 2, y, text)
    # pink swirl underline
    c.setStrokeColor(SOFTPINK)
    c.setLineWidth(2)
    p = c.beginPath()
    cx = W / 2
    wpx = min(3.5 * inch, len(text) * size * 0.32)
    for i in range(41):
        t = i / 40
        x = cx - wpx / 2 + t * wpx
        yy = y - 10 + 4 * math.sin(t * math.pi * 3)
        if i == 0:
            p.moveTo(x, yy)
        else:
            p.lineTo(x, yy)
    c.drawPath(p, fill=0, stroke=1)
    return y - 28

def gold_divider(c, y):
    swirl_divider(c, y)

def prompt_style(size=11, color=DARK, bold=False, italic=False, center=False, font=None):
    if font:
        fn = font
    else:
        fn = TITLE_FONT if bold else (ITALIC if italic else BODY_FONT)
    return ParagraphStyle("s", fontName=fn, fontSize=size, leading=size + 5,
                          textColor=color, alignment=TA_CENTER if center else TA_LEFT)

def draw_lines(c, x, y, width, n, gap=0.32 * inch):
    c.setStrokeColor(HexColor("#d9c9a8"))
    c.setLineWidth(0.7)
    for i in range(n):
        c.line(x, y - i * gap, x + width, y - i * gap)
    # tiny heart at start of first line
    doodle_heart(c, x - 12, y + 2, 5, BLUSH)

# ---------- whimsical cover ----------

def cover_page(c, title, subtitle, tagline, seed=1):
    """Full-burgundy branded cover — whimsy edition."""
    c.setFillColor(BURGUNDY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # scattered sparkles across the whole cover
    scatter_sparkles(c, 28, seed=seed)
    # double gold frame with pink inner line
    c.setStrokeColor(GOLD)
    c.setLineWidth(2.5)
    c.roundRect(0.6 * inch, 0.6 * inch, W - 1.2 * inch, H - 1.2 * inch, 14, fill=0, stroke=1)
    c.setStrokeColor(SOFTPINK)
    c.setLineWidth(1)
    c.roundRect(0.72 * inch, 0.72 * inch, W - 1.44 * inch, H - 1.44 * inch, 10, fill=0, stroke=1)
    # corner doodles
    for (fx, fy) in [(1.15 * inch, H - 1.15 * inch), (W - 1.15 * inch, H - 1.15 * inch),
                     (1.15 * inch, 1.15 * inch), (W - 1.15 * inch, 1.15 * inch)]:
        doodle_flower(c, fx, fy, 12, BLUSH, GOLD)
    # brand line
    c.setFillColor(GOLD)
    c.setFont(TITLE_FONT, 13)
    c.drawCentredString(W / 2, H - 3.2 * inch, "S H E ' S   T H E   V I B E")
    star4(c, W / 2 - 2.4 * inch, H - 3.2 * inch + 4, 7)
    star4(c, W / 2 + 2.4 * inch, H - 3.2 * inch + 4, 7)
    # main title in script!
    c.setFillColor(CREAM)
    title_style = ParagraphStyle("t", fontName=SCRIPT, fontSize=44,
                                 leading=50, textColor=CREAM, alignment=TA_CENTER)
    p = Paragraph(title, title_style)
    pw, ph = p.wrap(W - 2.6 * inch, 3.5 * inch)
    p.drawOn(c, (W - pw) / 2, H - 5.9 * inch)
    # swirl divider
    swirl_divider(c, H - 6.35 * inch)
    # subtitle in italic serif
    c.setFillColor(SOFTGOLD)
    c.setFont(ITALIC, 14)
    c.drawCentredString(W / 2, H - 6.85 * inch, subtitle)
    # tagline + doodle hearts at bottom
    doodle_heart(c, W / 2 - 1.8 * inch, 1.6 * inch, 8, SOFTPINK)
    doodle_heart(c, W / 2 + 1.8 * inch, 1.6 * inch, 8, SOFTPINK)
    c.setFillColor(CREAM)
    c.setFont(BODY_FONT, 10)
    c.drawCentredString(W / 2, 1.35 * inch, tagline)
    c.setFillColor(GOLD)
    c.setFont(SCRIPT, 16)
    c.drawCentredString(W / 2, 1.0 * inch, "shesthevibe.co")
    c.showPage()

def page_header(c, section_label, seed=0):
    """Burgundy header bar with sparkles + script label."""
    c.setFillColor(BURGUNDY)
    c.rect(0, H - 0.85 * inch, W, 0.85 * inch, fill=1, stroke=0)
    # sparkles in header
    rnd = random.Random(seed)
    for _ in range(6):
        star4(c, rnd.uniform(0.3 * inch, W - 0.3 * inch),
              rnd.uniform(H - 0.8 * inch, H - 0.1 * inch),
              rnd.uniform(3, 7), GOLD if rnd.random() > 0.4 else SOFTPINK)
    c.setFillColor(GOLD)
    c.setFont(SCRIPT, 20)
    c.drawCentredString(W / 2, H - 0.58 * inch, section_label)
    # footer
    c.setFont(SCRIPT, 13)
    c.setFillColor(MUTEDROSE)
    c.drawRightString(W - 0.6 * inch, 0.45 * inch, "She's The Vibe")
    doodle_heart(c, W - 1.85 * inch, 0.5 * inch, 5, BLUSH)
    corner_flourish(c, GOLD)
    return H - 1.35 * inch

# ============================================================
# CONTENT (unchanged from original)
# ============================================================
SECTIONS = [
    ("Self-Discovery", [
        "What did you love doing as a kid before anyone told you what was 'appropriate'?",
        "Describe yourself in 10 words \u2014 then circle the ones that actually feel like YOU.",
        "What are you pretending not to know about yourself right now?",
        "If nobody would judge you, how would you spend your Saturdays?",
        "What part of yourself have you been dimming to keep someone else comfortable?",
        "Write about a moment you felt most like yourself. What were you doing?",
        "What do you want people to feel when they meet you?",
        "What's something you're good at that you never give yourself credit for?",
        "If your life had a theme song right now, what would it be and why?",
        "What would you do this week if you trusted yourself completely?",
    ]),
    ("When You're Overwhelmed", [
        "Dump it all out: everything on your mind, no filter, no organizing. Go.",
        "What's the ONE thing actually bothering you underneath all the noise?",
        "What can you put down today that was never yours to carry?",
        "Write a permission slip to yourself for something you need right now.",
        "What does your body need that you've been ignoring?",
        "List 5 things that are actually in your control today.",
        "What would 'good enough' look like today instead of perfect?",
        "Who or what is draining you most right now? Be honest.",
        "What would you tell your best friend if she were in your exact situation?",
        "What's one tiny thing that would make today 10% better?",
    ]),
    ("Relationships", [
        "Who makes you feel most like yourself? What do they do differently?",
        "What pattern keeps showing up in your relationships that you're tired of?",
        "Write the conversation you've been avoiding. Say the unsaid thing.",
        "What do you need from the people closest to you that you've never asked for?",
        "Describe a relationship that taught you something painful but valuable.",
        "Where are you over-giving? Where are you under-receiving?",
        "What does a healthy 'no' feel like in your body?",
        "Who do you need to forgive \u2014 including yourself?",
        "What kind of friend/partner/mother are you becoming? Is she who you want to be?",
        "Write a love letter to someone who deserves to hear it \u2014 maybe it's you.",
    ]),
    ("Breaking Cycles", [
        "What did you learn about love growing up that you're actively unlearning?",
        "What cycle ends with you? Name it out loud on this page.",
        "What would you do differently than the generation before you?",
        "Write about a moment you chose differently than your mother would have.",
        "What story about yourself are you done telling?",
        "Who told you you couldn't? What did you do anyway?",
        "What's one belief you inherited that was never actually yours?",
        "How has surviving hard things made you stronger \u2014 not bitter?",
        "What are you teaching the next generation just by how you live?",
        "Write to the younger you who needed someone in her corner. Be that someone.",
    ]),
    ("Dreaming Bigger", [
        "If money and fear weren't factors, what would your life look like in 3 years?",
        "What's the dream you've been calling 'silly' that won't leave you alone?",
        "Describe your ideal morning, in detail. Now: what's one step toward it?",
        "What would you create if you knew people would love it?",
        "Who do you admire and what specific quality of theirs do you want to embody?",
        "What's something you've always wanted to learn? Why not now?",
        "Write your own 'I made it' moment \u2014 where are you, who's there, how does it feel?",
        "What does success look like for YOU \u2014 not Instagram, not your mama, you?",
        "What's one bold move you could make this month?",
        "Finish this sentence 10 times: 'I am becoming a woman who...'",
    ]),
]

SECTION_TAGLINES = {
    "Self-Discovery": "get to know the real you",
    "When You're Overwhelmed": "for the days your brain won't shut up",
    "Relationships": "the people stuff, let's untangle it",
    "Breaking Cycles": "the cycle ends with you, babe",
    "Dreaming Bigger": "go ahead, want the big things",
}

def build_prompts():
    c = canvas.Canvas(os.path.join(OUT, "50-journal-prompts.pdf"), pagesize=LETTER)
    c.setTitle("50 Journal Prompts for When You're Stuck \u2014 She's The Vibe")
    c.setAuthor("She's The Vibe")
    cover_page(c, "50 Journal Prompts<br/>for When You're Stuck",
               "Practical. Pretty. You.",
               "Your words are the way back to yourself.", seed=11)
    # intro page with whimsy
    y = page_header(c, "hey love, let's do this", seed=21)
    scatter_sparkles(c, 10, seed=22, y_range=(1 * inch, H - 1.5 * inch))
    y = script_header(c, "How This Works", y - 10, size=28)
    intro = prompt_style(11.5, DARK)
    p = Paragraph("These prompts are for the days your brain won't shut up, "
                  "the mornings you don't know where to start, and the nights you need "
                  "to get it OUT of your head and onto paper. There's no right way to use "
                  "them. Pick one. Write messy. Skip around. Come back when you need to. "
                  "Your journal doesn't judge \u2014 that's the whole point.", intro)
    pw, ph = p.wrap(W - 2 * inch, 4 * inch)
    p.drawOn(c, inch, y - ph)
    y -= ph + 0.3 * inch
    swirl_divider(c, y)
    y -= 0.45 * inch
    y = script_header(c, "The Only Rules", y, size=24)
    rules = [
        "One prompt a day, or binge ten at 2am \u2014 your call",
        "Give yourself at least 5 honest minutes per prompt",
        "Write the first thing that comes up, even if it's ugly",
        "Especially if it's ugly",
    ]
    for i, rule in enumerate(rules):
        doodle_heart(c, inch + 0.15 * inch, y - 4, 7, SOFTPINK if i % 2 == 0 else GOLD)
        pr = Paragraph(rule, prompt_style(11, DARK))
        pw, ph = pr.wrap(W - 2.8 * inch, 2 * inch)
        pr.drawOn(c, inch + 0.5 * inch, y - ph + 4)
        y -= ph + 0.18 * inch
    y -= 0.2 * inch
    swirl_divider(c, y)
    c.showPage()
    # sections: 5 prompts per page with writing lines
    for si, (sec, prompts) in enumerate(SECTIONS):
        for chunk_start in range(0, 10, 5):
            y = page_header(c, f"part {si + 1} of 5", seed=30 + si * 10 + chunk_start)
            scatter_sparkles(c, 6, seed=40 + si * 10 + chunk_start,
                             y_range=(1 * inch, H - 1.6 * inch))
            # script section title + tagline
            y = script_header(c, sec, y - 5, size=26)
            c.setFillColor(MUTEDROSE)
            c.setFont(ITALIC, 11)
            c.drawCentredString(W / 2, y + 6, SECTION_TAGLINES.get(sec, ""))
            y -= 0.28 * inch
            for pi in range(chunk_start, min(chunk_start + 5, 10)):
                num = si * 10 + pi + 1
                sticker_badge(c, inch + 0.22 * inch, y - 2, 13, num,
                              SOFTPINK if num % 2 == 1 else BLUSH)
                pr = Paragraph(prompts[pi], prompt_style(11, DARK))
                pw, ph = pr.wrap(W - 2.9 * inch, 2 * inch)
                pr.drawOn(c, inch + 0.55 * inch, y - ph + 6)
                y -= ph + 0.2 * inch
                draw_lines(c, inch + 0.3 * inch, y, W - 2.6 * inch, 4)
                y -= 4 * 0.32 * inch + 0.3 * inch
            c.showPage()
    # closing page
    y = page_header(c, "you did it, babe", seed=99)
    scatter_sparkles(c, 12, seed=100, y_range=(1.5 * inch, H - 1.5 * inch))
    y = script_header(c, "You Showed Up. That Counts.", y - 10, size=28)
    p = Paragraph("Fifty prompts down \u2014 or fifty to go, whenever you're ready. "
                  "If these helped you hear yourself a little clearer, imagine what "
                  "a whole guided journal could do. Check out the full She's The Vibe "
                  "journal collection, or book a free 20-minute Vibe Session and let's "
                  "talk about where you're headed.", prompt_style(11.5, DARK, center=True))
    pw, ph = p.wrap(W - 2.4 * inch, 4 * inch)
    p.drawOn(c, (W - pw) / 2, y - ph)
    y -= ph + 0.45 * inch
    swirl_divider(c, y)
    y -= 0.45 * inch
    doodle_flower(c, W / 2 - 1.1 * inch, y, 14)
    doodle_flower(c, W / 2 + 1.1 * inch, y, 14)
    c.setFillColor(BURGUNDY)
    c.setFont(SCRIPT, 22)
    c.drawCentredString(W / 2, y - 0.35 * inch, "shesthevibe.co")
    c.setFont(BODY_FONT, 10)
    c.setFillColor(DARK)
    c.drawCentredString(W / 2, y - 0.62 * inch, "Practical. Pretty. You.")
    c.showPage()
    c.save()

# ============================================================
# PDF 2: 5-MINUTE MORNING RESET (magical ritual card)
# ============================================================
RESET_STEPS = [
    ("breathe", "Minute One",
     "Close your eyes. Inhale for 4 counts, hold for 4, exhale for 6. "
     "Do it 3 times. You're not behind. You're right here.",
     "How does your breath feel right now? (tight / shallow / easy):"),
    ("intention", "Minute Two",
     "Set ONE intention for today. Not a to-do list \u2014 a way of being. "
     "\"Today I will move slowly.\" \"Today I choose peace over proving.\"",
     "My intention for today:"),
    ("gratitude", "Minute Three",
     "Name 3 things you're grateful for. Small counts. Coffee counts. "
     "Breathing counts. Let yourself actually feel one of them.",
     "1.                                          2.                                          3."),
    ("body check", "Minute Four",
     "Scan from head to toe. Where are you holding tension? Shoulders? Jaw? "
     "Stomach? Breathe into that spot. Soften it just 10%.",
     "What I noticed in my body:"),
    ("today's vibe", "Minute Five",
     "Pick your vibe for the day. One word. Write it big. Let it guide "
     "your choices \u2014 the music, the outfit, the energy you bring.",
     "Today's vibe (one word):"),
]

STEP_ICONS = ["breathe", "intention", "gratitude", "body", "vibe"]

def build_reset():
    c = canvas.Canvas(os.path.join(OUT, "5-minute-morning-reset.pdf"), pagesize=LETTER)
    c.setTitle("The 5-Minute Morning Reset \u2014 She's The Vibe")
    c.setAuthor("She's The Vibe")
    cover_page(c, "The 5-Minute<br/>Morning Reset",
               "Start grounded. Stay you.",
               "Five minutes. Five steps. A whole different day.", seed=55)
    y = page_header(c, "your magical morning ritual", seed=61)
    scatter_sparkles(c, 8, seed=62, y_range=(1 * inch, H - 1.6 * inch))
    y = script_header(c, "Before the World Gets a Vote", y - 5, size=26)
    p = Paragraph("Mornings set the tone \u2014 but nobody has an hour. This reset takes "
                  "five minutes and meets you where you are: half-awake, coffee in hand, "
                  "already thinking about everything. Print it, keep it by your bed, "
                  "and give yourself five minutes before the world gets a vote.",
                  prompt_style(11, DARK, center=True))
    pw, ph = p.wrap(W - 2.2 * inch, 3 * inch)
    p.drawOn(c, (W - pw) / 2, y - ph)
    y -= ph + 0.4 * inch
    for i, (word, minute, desc, write) in enumerate(RESET_STEPS):
        if y < 2.4 * inch:
            c.showPage()
            y = page_header(c, "keep going, you're glowing", seed=70 + i)
            scatter_sparkles(c, 6, seed=80 + i, y_range=(1 * inch, H - 1.6 * inch))
        card_h = 1.7 * inch
        # blush card with gold border
        c.setFillColor(BLUSH if i % 2 == 0 else CREAM)
        c.setStrokeColor(GOLD)
        c.setLineWidth(1.2)
        c.roundRect(inch, y - card_h, W - 2 * inch, card_h, 12, fill=1, stroke=1)
        # corner sparkles on card
        star4(c, inch + 0.25 * inch, y - 0.22 * inch, 6, GOLD)
        star4(c, W - inch - 0.25 * inch, y - card_h + 0.25 * inch, 5, SOFTPINK)
        # sticker number
        sticker_badge(c, inch + 0.42 * inch, y - 0.42 * inch, 15, i + 1,
                      SOFTPINK if i % 2 == 0 else GOLD,
                      BURGUNDY if i % 2 == 0 else CREAM)
        # minute label in script
        c.setFillColor(BURGUNDY)
        c.setFont(SCRIPT, 22)
        c.drawString(inch + 0.75 * inch, y - 0.5 * inch, minute)
        # keyword in small caps
        c.setFillColor(DEEPGOLD)
        c.setFont(TITLE_FONT, 9)
        c.drawString(inch + 0.75 * inch, y - 0.68 * inch, word.upper())
        pr = Paragraph(desc, prompt_style(10, DARK))
        pw, ph = pr.wrap(W - 2.7 * inch, 2 * inch)
        pr.drawOn(c, inch + 0.25 * inch, y - 0.85 * inch - ph)
        c.setFillColor(HexColor("#8a6d3b"))
        c.setFont(ITALIC, 9.5)
        c.drawString(inch + 0.25 * inch, y - card_h + 0.32 * inch, write)
        c.setStrokeColor(HexColor("#d9c9a8"))
        c.setLineWidth(0.7)
        if i != 2:
            c.line(inch + 0.25 * inch, y - card_h + 0.16 * inch,
                   W - inch - 0.25 * inch, y - card_h + 0.16 * inch)
        # tiny heart on card
        doodle_heart(c, W - inch - 0.35 * inch, y - 0.35 * inch, 6, SOFTPINK)
        y -= card_h + 0.24 * inch
    if y < 1.8 * inch:
        c.showPage()
        y = page_header(c, "you did it", seed=90)
        scatter_sparkles(c, 8, seed=91, y_range=(1.5 * inch, H - 1.5 * inch))
    else:
        y -= 0.05 * inch
    swirl_divider(c, y)
    y -= 0.4 * inch
    y = script_header(c, "You Chose Yourself First", y, size=24)
    p = Paragraph("Five minutes. That's the whole vibe. Tape this to your mirror, "
                  "screenshot it, make it your lock screen. And when you're ready for "
                  "deeper work, the She's The Vibe journals and a free 20-minute Vibe "
                  "Session are waiting at shesthevibe.co.",
                  prompt_style(10.5, DARK, center=True))
    pw, ph = p.wrap(W - 2.4 * inch, 3 * inch)
    p.drawOn(c, (W - pw) / 2, y - ph)
    c.showPage()
    c.save()

# ============================================================
# PDF 3: BOUNDARY SCRIPTS (cute + empowering)
# ============================================================
SCRIPT_SECTIONS = [
    ("Saying No", "the word is a full sentence",
     [
         ("The simple no", "\"I can't do that, but thank you for thinking of me.\""),
         ("No with a door closed", "\"That doesn't work for me. I hope you find what you need.\""),
         ("No to the guilt trip", "\"I understand you're disappointed, and my answer is still no.\""),
         ("The delay (buy yourself time)", "\"Let me check and get back to you.\" <i>(Then decide on YOUR terms.)</i>"),
     ]),
    ("With Family", "love them. still hold the line.",
     [
         ("The topic shutdown", "\"I'm not discussing that anymore. Let's talk about something else.\""),
         ("The visit boundary", "\"We'd love to see you Saturday from 2 to 4. We'll need to wrap up then.\""),
         ("The advice deflector", "\"I appreciate you caring. I've got this handled.\""),
         ("When they bring up the past", "\"I've moved past that, and I'd like our conversations to reflect that.\""),
     ]),
    ("At Work", "professional doesn't mean doormat",
     [
         ("The workload pushback", "\"I can take this on if we push back the X deadline \u2014 which should I prioritize?\""),
         ("The after-hours text", "\"I'll look at this first thing in the morning.\" <i>(Then put the phone down.)</i>"),
         ("The credit claim", "\"Thanks \u2014 actually, that was my work on that project. Happy to walk you through it.\""),
         ("The meeting overload", "\"I won't be able to make that one \u2014 please send me the notes.\""),
     ]),
    ("With Friends", "real friends respect the line",
     [
         ("The plan decline", "\"I need a quiet night in, but have so much fun! Let's catch up next week.\""),
         ("The venting limit", "\"I love you and I only have about 10 minutes of advice-brain left today.\""),
         ("The money ask", "\"I'm not able to lend money, but I can help you brainstorm other options.\""),
         ("The last-minute favor", "\"I can't swing that today. I need more notice for favors like that.\""),
     ]),
    ("When They Push Back", "they will test it. hold it anyway.",
     [
         ("The repeat", "\"I hear you. My answer hasn't changed.\" <i>(Say it the same way, every time.)</i>"),
         ("The guilt", "\"I'm not responsible for managing your disappointment about my boundary.\""),
         ("The escalation", "\"If you keep pushing, I'm going to end this conversation.\" <i>(Then do it.)</i>"),
         ("The aftermath pep talk", "\"Holding that boundary was hard AND it was right. I'm proud of me.\""),
     ]),
]

def build_scripts():
    c = canvas.Canvas(os.path.join(OUT, "boundary-scripts.pdf"), pagesize=LETTER)
    c.setTitle("Boundary Scripts: What to Say When... \u2014 She's The Vibe")
    c.setAuthor("She's The Vibe")
    cover_page(c, "Boundary Scripts<br/><font size=28>what to say when...</font>",
               "Your cheat sheet for holding the line.",
               "Because 'no' is a full sentence \u2014 but sometimes you need the words.",
               seed=78)
    y = page_header(c, "your pocket power phrases", seed=81)
    scatter_sparkles(c, 8, seed=82, y_range=(1 * inch, H - 1.6 * inch))
    y = script_header(c, "Boundaries, But Make It Cute", y - 5, size=26)
    p = Paragraph("Boundaries aren't about being mean \u2014 they're about being clear. "
                  "The hardest part is finding the words in the moment, so here they are, "
                  "ready to go. Practice saying them out loud. Save the ones you need most. "
                  "And remember: a boundary without enforcement is just a suggestion.",
                  prompt_style(11, DARK, center=True))
    pw, ph = p.wrap(W - 2.2 * inch, 3 * inch)
    p.drawOn(c, (W - pw) / 2, y - ph)
    y -= ph + 0.4 * inch
    swirl_divider(c, y)
    y -= 0.45 * inch
    for si, (sec, sub, scripts) in enumerate(SCRIPT_SECTIONS):
        need = 0.75 * inch + len(scripts) * 0.85 * inch + 0.25 * inch
        if y - need < 0.9 * inch:
            c.showPage()
            y = page_header(c, "more power phrases", seed=90 + si)
            scatter_sparkles(c, 6, seed=95 + si, y_range=(1 * inch, H - 1.6 * inch))
        # script section title
        y = script_header(c, sec, y, size=24)
        c.setFillColor(MUTEDROSE)
        c.setFont(ITALIC, 10.5)
        c.drawCentredString(W / 2, y + 8, sub)
        y -= 0.3 * inch
        for li, (label, script) in enumerate(scripts):
            pr = Paragraph(f"<b>{label}:</b> {script}", prompt_style(10.5, DARK))
            pw, ph = pr.wrap(W - 2.9 * inch, 2 * inch)
            card_h = ph + 0.3 * inch
            if y - card_h < 0.9 * inch:
                c.showPage()
                y = page_header(c, sec.lower() + " (cont.)", seed=100 + si * 10 + li)
                scatter_sparkles(c, 5, seed=105 + si * 10 + li,
                                 y_range=(1 * inch, H - 1.6 * inch))
            # cute card: blush/cream alternating with pink left bar
            c.setFillColor(BLUSH if (si + li) % 2 == 0 else CREAM)
            c.setStrokeColor(SOFTPINK)
            c.setLineWidth(1)
            c.roundRect(inch, y - card_h, W - 2 * inch, card_h, 8, fill=1, stroke=1)
            # pink accent bar
            c.setFillColor(SOFTPINK)
            c.roundRect(inch, y - card_h, 0.12 * inch, card_h, 4, fill=1, stroke=0)
            # tiny heart on card
            doodle_heart(c, W - inch - 0.3 * inch, y - 0.22 * inch, 5,
                         SOFTPINK if (si + li) % 2 == 0 else GOLD)
            pr.drawOn(c, inch + 0.3 * inch, y - card_h + 0.15 * inch)
            y -= card_h + 0.18 * inch
        y -= 0.2 * inch
        if y > 1.2 * inch:
            # mini divider between sections
            c.setStrokeColor(BLUSH)
            c.setLineWidth(1)
            c.line(W / 2 - 1 * inch, y, W / 2 + 1 * inch, y)
            doodle_heart(c, W / 2, y, 6, BLUSH)
            y -= 0.3 * inch
    if y < 2.0 * inch:
        c.showPage()
        y = page_header(c, "say it with your chest", seed=120)
        scatter_sparkles(c, 8, seed=121, y_range=(1.5 * inch, H - 1.5 * inch))
    swirl_divider(c, y)
    y -= 0.4 * inch
    y = script_header(c, "Every Boundary Is a Vote", y, size=24)
    p = Paragraph("Every boundary you hold is a vote for the woman you're becoming. "
                  "If this cheat sheet helped, the <b>Healing Vibe Journal</b> goes deeper \u2014 "
                  "and a free 20-minute Vibe Session with Christina is the fastest way "
                  "to get personalized support. shesthevibe.co",
                  prompt_style(11, DARK, center=True))
    pw, ph = p.wrap(W - 2.4 * inch, 3 * inch)
    p.drawOn(c, (W - pw) / 2, y - ph)
    y -= ph + 0.3 * inch
    doodle_heart(c, W / 2 - 0.5 * inch, y, 8, SOFTPINK)
    doodle_heart(c, W / 2 + 0.5 * inch, y, 8, SOFTPINK)
    star4(c, W / 2, y, 7, GOLD)
    c.showPage()
    c.save()

if __name__ == "__main__":
    build_prompts()
    print("built 50-journal-prompts.pdf")
    build_reset()
    print("built 5-minute-morning-reset.pdf")
    build_scripts()
    print("built boundary-scripts.pdf")
