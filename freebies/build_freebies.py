#!/usr/bin/env python3
"""Build the 3 She's The Vibe lead-magnet PDFs."""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "freebies")
os.makedirs(OUT, exist_ok=True)

W, H = LETTER
BURGUNDY = HexColor("#451425")
GOLD = HexColor("#C9A96E")
CREAM = HexColor("#F7E7CE")
DARK = HexColor("#2b0d18")
SOFTGOLD = HexColor("#e8d5ae")

TITLE_FONT = "Helvetica-Bold"
BODY_FONT = "Helvetica"
ITALIC = "Helvetica-Oblique"

# ---------- shared drawing helpers ----------

def cover_page(c, title, subtitle, tagline):
    """Full-burgundy branded cover."""
    c.setFillColor(BURGUNDY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # thin gold frame
    c.setStrokeColor(GOLD); c.setLineWidth(2.5)
    c.roundRect(0.6*inch, 0.6*inch, W-1.2*inch, H-1.2*inch, 14, fill=0, stroke=1)
    # sparkles (small 4-point stars)
    def star(cx, cy, r):
        c.setFillColor(GOLD)
        p = c.beginPath()
        for i in range(8):
            import math
            ang = math.pi*i/4 - math.pi/2
            rr = r if i % 2 == 0 else r*0.35
            x, y = cx + rr*math.cos(ang), cy + rr*math.sin(ang)
            if i == 0: p.moveTo(x, y)
            else: p.lineTo(x, y)
        p.close(); c.drawPath(p, fill=1, stroke=0)
    import math
    star(1.6*inch, H-2.2*inch, 14); star(W-1.6*inch, H-2.6*inch, 10)
    star(1.9*inch, 2.4*inch, 10); star(W-1.9*inch, 2.1*inch, 14)
    star(W/2, H-1.55*inch, 8)
    # crown-ish flourish: "SHE'S THE VIBE"
    c.setFillColor(GOLD); c.setFont(TITLE_FONT, 13)
    c.drawCentredString(W/2, H-3.4*inch, "S H E ' S   T H E   V I B E")
    # main title
    c.setFillColor(CREAM)
    title_style = ParagraphStyle("t", fontName=TITLE_FONT, fontSize=34,
                                 leading=40, textColor=CREAM, alignment=TA_CENTER)
    p = Paragraph(title, title_style)
    pw, ph = p.wrap(W-2.4*inch, 3*inch)
    p.drawOn(c, (W-pw)/2, H-5.6*inch)
    # gold divider
    c.setStrokeColor(GOLD); c.setLineWidth(1.5)
    cy = H-6.1*inch
    c.line(W/2-1.6*inch, cy, W/2+1.6*inch, cy)
    star(W/2, cy, 9)
    # subtitle
    c.setFillColor(SOFTGOLD); c.setFont(ITALIC, 13)
    c.drawCentredString(W/2, H-6.6*inch, subtitle)
    # tagline at bottom
    c.setFillColor(CREAM); c.setFont(BODY_FONT, 10)
    c.drawCentredString(W/2, 1.35*inch, tagline)
    c.setFillColor(GOLD); c.setFont(BODY_FONT, 9)
    c.drawCentredString(W/2, 1.05*inch, "shesthevibe.co")
    c.showPage()

def page_header(c, section_label):
    c.setFillColor(BURGUNDY)
    c.rect(0, H-0.85*inch, W, 0.85*inch, fill=1, stroke=0)
    c.setFillColor(GOLD); c.setFont(TITLE_FONT, 10)
    c.drawCentredString(W/2, H-0.52*inch, section_label.upper())
    c.setFont(BODY_FONT, 8); c.setFillColor(CREAM)
    c.drawRightString(W-0.6*inch, 0.45*inch, "She's The Vibe  |  shesthevibe.co")
    return H-1.35*inch

def gold_divider(c, y):
    c.setStrokeColor(GOLD); c.setLineWidth(1)
    c.line(1.2*inch, y, W-1.2*inch, y)

def prompt_style(size=11, color=DARK, bold=False, italic=False, center=False):
    fn = TITLE_FONT if bold else (ITALIC if italic else BODY_FONT)
    return ParagraphStyle("s", fontName=fn, fontSize=size, leading=size+5,
                          textColor=color, alignment=TA_CENTER if center else TA_LEFT)

def draw_lines(c, x, y, width, n, gap=0.32*inch):
    c.setStrokeColor(HexColor("#d9c9a8")); c.setLineWidth(0.7)
    for i in range(n):
        c.line(x, y - i*gap, x+width, y - i*gap)

# ============================================================
# PDF 1: 50 JOURNAL PROMPTS
# ============================================================
SECTIONS = [
    ("Self-Discovery", [
        "What did you love doing as a kid before anyone told you what was 'appropriate'?",
        "Describe yourself in 10 words — then circle the ones that actually feel like YOU.",
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
        "Who do you need to forgive — including yourself?",
        "What kind of friend/partner/mother are you becoming? Is she who you want to be?",
        "Write a love letter to someone who deserves to hear it — maybe it's you.",
    ]),
    ("Breaking Cycles", [
        "What did you learn about love growing up that you're actively unlearning?",
        "What cycle ends with you? Name it out loud on this page.",
        "What would you do differently than the generation before you?",
        "Write about a moment you chose differently than your mother would have.",
        "What story about yourself are you done telling?",
        "Who told you you couldn't? What did you do anyway?",
        "What's one belief you inherited that was never actually yours?",
        "How has surviving hard things made you stronger — not bitter?",
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
        "Write your own 'I made it' moment — where are you, who's there, how does it feel?",
        "What does success look like for YOU — not Instagram, not your mama, you?",
        "What's one bold move you could make this month?",
        "Finish this sentence 10 times: 'I am becoming a woman who...'",
    ]),
]

def build_prompts():
    c = canvas.Canvas(os.path.join(OUT, "50-journal-prompts.pdf"), pagesize=LETTER)
    c.setTitle("50 Journal Prompts for When You're Stuck — She's The Vibe")
    c.setAuthor("She's The Vibe")
    cover_page(c, "50 Journal Prompts<br/>for When You're Stuck",
               "Practical. Pretty. You.",
               "Your words are the way back to yourself.")
    # intro
    y = page_header(c, "She's The Vibe  •  Free Download")
    intro = prompt_style(11.5, DARK)
    p = Paragraph("Hey love — these prompts are for the days your brain won't shut up, "
                  "the mornings you don't know where to start, and the nights you need "
                  "to get it OUT of your head and onto paper. There's no right way to use "
                  "them. Pick one. Write messy. Skip around. Come back when you need to. "
                  "Your journal doesn't judge — that's the whole point.", intro)
    pw, ph = p.wrap(W-2*inch, 4*inch)
    p.drawOn(c, inch, y-ph); y -= ph + 0.25*inch
    gold_divider(c, y); y -= 0.35*inch
    p2 = Paragraph("<b>How to use this:</b> one prompt a day, or binge ten at 2am — "
                   "your call. Give yourself at least 5 honest minutes per prompt. "
                   "Write the first thing that comes up, even if it's ugly. "
                   "Especially if it's ugly.", prompt_style(10.5, DARK))
    pw, ph = p2.wrap(W-2*inch, 3*inch)
    p2.drawOn(c, inch, y-ph); y -= ph + 0.3*inch
    c.showPage()
    # sections: 5 prompts per page with writing lines
    for si, (sec, prompts) in enumerate(SECTIONS):
        for chunk_start in range(0, 10, 5):
            y = page_header(c, f"Part {si+1}: {sec}")
            c.setFillColor(BURGUNDY); c.setFont(TITLE_FONT, 15)
            c.drawString(inch, y, f"{sec}")
            y -= 0.12*inch
            c.setStrokeColor(GOLD); c.setLineWidth(1.5)
            c.line(inch, y, inch+2.2*inch, y)
            y -= 0.3*inch
            for pi in range(chunk_start, min(chunk_start+5, 10)):
                num = si*10 + pi + 1
                c.setFillColor(GOLD); c.setFont(TITLE_FONT, 11)
                c.drawString(inch, y, f"{num}.")
                pr = Paragraph(prompts[pi], prompt_style(11, DARK))
                pw, ph = pr.wrap(W-2.6*inch, 2*inch)
                pr.drawOn(c, inch+0.35*inch, y-ph+4)
                y -= ph + 0.18*inch
                draw_lines(c, inch, y, W-2*inch, 4)
                y -= 4*0.32*inch + 0.28*inch
            c.showPage()
    # closing page
    y = page_header(c, "Keep Going")
    c.setFillColor(BURGUNDY); c.setFont(TITLE_FONT, 18)
    c.drawCentredString(W/2, y, "You showed up. That counts.")
    y -= 0.5*inch
    p = Paragraph("Fifty prompts down — or fifty to go, whenever you're ready. "
                  "If these helped you hear yourself a little clearer, imagine what "
                  "a whole guided journal could do. Check out the full She's The Vibe "
                  "journal collection, or book a free 20-minute Vibe Session and let's "
                  "talk about where you're headed.", prompt_style(11.5, DARK, center=True))
    pw, ph = p.wrap(W-2.4*inch, 4*inch)
    p.drawOn(c, (W-pw)/2, y-ph); y -= ph + 0.4*inch
    gold_divider(c, y); y -= 0.4*inch
    c.setFillColor(BURGUNDY); c.setFont(TITLE_FONT, 12)
    c.drawCentredString(W/2, y, "shesthevibe.co")
    y -= 0.3*inch
    c.setFont(BODY_FONT, 10); c.setFillColor(DARK)
    c.drawCentredString(W/2, y, "Practical. Pretty. You.")
    c.showPage()
    c.save()

# ============================================================
# PDF 2: 5-MINUTE MORNING RESET
# ============================================================
RESET_STEPS = [
    ("MINUTE 1 — BREATHE",
     "Close your eyes. Inhale for 4 counts, hold for 4, exhale for 6. "
     "Do it 3 times. You're not behind. You're right here.",
     "How does your breath feel right now? (tight / shallow / easy):"),
    ("MINUTE 2 — INTENTION",
     "Set ONE intention for today. Not a to-do list — a way of being. "
     "\"Today I will move slowly.\" \"Today I choose peace over proving.\"",
     "My intention for today:"),
    ("MINUTE 3 — GRATITUDE",
     "Name 3 things you're grateful for. Small counts. Coffee counts. "
     "Breathing counts. Let yourself actually feel one of them.",
     "1.                                          2.                                          3."),
    ("MINUTE 4 — BODY CHECK",
     "Scan from head to toe. Where are you holding tension? Shoulders? Jaw? "
     "Stomach? Breathe into that spot. Soften it just 10%.",
     "What I noticed in my body:"),
    ("MINUTE 5 — TODAY'S VIBE",
     "Pick your vibe for the day. One word. Write it big. Let it guide "
     "your choices — the music, the outfit, the energy you bring.",
     "Today's vibe (one word):"),
]

def build_reset():
    c = canvas.Canvas(os.path.join(OUT, "5-minute-morning-reset.pdf"), pagesize=LETTER)
    c.setTitle("The 5-Minute Morning Reset — She's The Vibe")
    c.setAuthor("She's The Vibe")
    cover_page(c, "The 5-Minute<br/>Morning Reset",
               "Start grounded. Stay you.",
               "Five minutes. Five steps. A whole different day.")
    y = page_header(c, "She's The Vibe  •  Free Download")
    p = Paragraph("Mornings set the tone — but nobody has an hour. This reset takes "
                  "five minutes and meets you where you are: half-awake, coffee in hand, "
                  "already thinking about everything. Print it, keep it by your bed, "
                  "and give yourself five minutes before the world gets a vote.",
                  prompt_style(11, DARK))
    pw, ph = p.wrap(W-2*inch, 3*inch)
    p.drawOn(c, inch, y-ph); y -= ph + 0.35*inch
    for i, (title, desc, write) in enumerate(RESET_STEPS):
        if y < 2.2*inch:
            c.showPage(); y = page_header(c, "The 5-Minute Morning Reset (cont.)")
        # step card
        card_h = 1.55*inch
        c.setFillColor(CREAM); c.setStrokeColor(GOLD); c.setLineWidth(1)
        c.roundRect(inch, y-card_h, W-2*inch, card_h, 10, fill=1, stroke=1)
        c.setFillColor(BURGUNDY); c.setFont(TITLE_FONT, 12)
        c.drawString(inch+0.2*inch, y-0.32*inch, title)
        pr = Paragraph(desc, prompt_style(10, DARK))
        pw, ph = pr.wrap(W-2.5*inch, 2*inch)
        pr.drawOn(c, inch+0.2*inch, y-0.42*inch-ph)
        c.setFillColor(HexColor("#8a6d3b")); c.setFont(ITALIC, 9.5)
        c.drawString(inch+0.2*inch, y-card_h+0.28*inch, write)
        c.setStrokeColor(HexColor("#d9c9a8")); c.setLineWidth(0.7)
        if i == 2:
            pass  # numbered blanks already in text
        else:
            c.line(inch+0.2*inch, y-card_h+0.14*inch, W-inch-0.2*inch, y-card_h+0.14*inch)
        y -= card_h + 0.22*inch
    if y < 1.6*inch:
        c.showPage(); y = page_header(c, "You Did It")
    else:
        y -= 0.1*inch
    gold_divider(c, y); y -= 0.35*inch
    p = Paragraph("Five minutes. You chose yourself first today — that's the whole "
                  "vibe. Tape this to your mirror, screenshot it, make it your lock "
                  "screen. And when you're ready for deeper work, the She's The Vibe "
                  "journals and a free 20-minute Vibe Session are waiting at "
                  "shesthevibe.co.", prompt_style(10.5, DARK, center=True))
    pw, ph = p.wrap(W-2.4*inch, 3*inch)
    p.drawOn(c, (W-pw)/2, y-ph)
    c.showPage(); c.save()

# ============================================================
# PDF 3: BOUNDARY SCRIPTS
# ============================================================
SCRIPT_SECTIONS = [
    ("Saying No", "The word is a full sentence. Here's how to say it kindly.",
     [
         ("The simple no", "\"I can't do that, but thank you for thinking of me.\""),
         ("No with a door closed", "\"That doesn't work for me. I hope you find what you need.\""),
         ("No to the guilt trip", "\"I understand you're disappointed, and my answer is still no.\""),
         ("The delay (buy yourself time)", "\"Let me check and get back to you.\" <i>(Then decide on YOUR terms.)</i>"),
     ]),
    ("With Family", "Love them. Still hold the line.",
     [
         ("The topic shutdown", "\"I'm not discussing that anymore. Let's talk about something else.\""),
         ("The visit boundary", "\"We'd love to see you Saturday from 2 to 4. We'll need to wrap up then.\""),
         ("The advice deflector", "\"I appreciate you caring. I've got this handled.\""),
         ("When they bring up the past", "\"I've moved past that, and I'd like our conversations to reflect that.\""),
     ]),
    ("At Work", "Professional doesn't mean doormat.",
     [
         ("The workload pushback", "\"I can take this on if we push back the X deadline — which should I prioritize?\""),
         ("The after-hours text", "\"I'll look at this first thing in the morning.\" <i>(Then put the phone down.)</i>"),
         ("The credit claim", "\"Thanks — actually, that was my work on that project. Happy to walk you through it.\""),
         ("The meeting overload", "\"I won't be able to make that one — please send me the notes.\""),
     ]),
    ("With Friends", "Real friends respect the line.",
     [
         ("The plan decline", "\"I need a quiet night in, but have so much fun! Let's catch up next week.\""),
         ("The venting limit", "\"I love you and I only have about 10 minutes of advice-brain left today.\""),
         ("The money ask", "\"I'm not able to lend money, but I can help you brainstorm other options.\""),
         ("The last-minute favor", "\"I can't swing that today. I need more notice for favors like that.\""),
     ]),
    ("When They Push Back", "They will test it. Hold it anyway.",
     [
         ("The repeat", "\"I hear you. My answer hasn't changed.\" <i>(Say it the same way, every time.)</i>"),
         ("The guilt", "\"I'm not responsible for managing your disappointment about my boundary.\""),
         ("The escalation", "\"If you keep pushing, I'm going to end this conversation.\" <i>(Then do it.)</i>"),
         ("The aftermath pep talk", "\"Holding that boundary was hard AND it was right. I'm proud of me.\""),
     ]),
]

def build_scripts():
    c = canvas.Canvas(os.path.join(OUT, "boundary-scripts.pdf"), pagesize=LETTER)
    c.setTitle("Boundary Scripts: What to Say When... — She's The Vibe")
    c.setAuthor("She's The Vibe")
    cover_page(c, "Boundary Scripts<br/><font size=20>What to Say When...</font>",
               "Your cheat sheet for holding the line.",
               "Because 'no' is a full sentence — but sometimes you need the words.")
    y = page_header(c, "She's The Vibe  •  Free Download")
    p = Paragraph("Boundaries aren't about being mean — they're about being clear. "
                  "The hardest part is finding the words in the moment, so here they are, "
                  "ready to go. Practice saying them out loud. Save the ones you need most. "
                  "And remember: a boundary without enforcement is just a suggestion.",
                  prompt_style(11, DARK))
    pw, ph = p.wrap(W-2*inch, 3*inch)
    p.drawOn(c, inch, y-ph); y -= ph + 0.35*inch
    for sec, sub, scripts in SCRIPT_SECTIONS:
        # estimate space: header 0.55 + 4 scripts * ~0.75
        need = 0.55*inch + len(scripts)*0.8*inch + 0.2*inch
        if y - need < 0.9*inch:
            c.showPage(); y = page_header(c, "Boundary Scripts (cont.)")
        c.setFillColor(BURGUNDY); c.setFont(TITLE_FONT, 14)
        c.drawString(inch, y, sec)
        y -= 0.2*inch
        c.setFont(ITALIC, 10); c.setFillColor(HexColor("#8a6d3b"))
        c.drawString(inch, y, sub)
        y -= 0.14*inch
        c.setStrokeColor(GOLD); c.setLineWidth(1.2)
        c.line(inch, y, inch+1.8*inch, y)
        y -= 0.28*inch
        for label, script in scripts:
            pr = Paragraph(f"<b>{label}:</b> {script}", prompt_style(10.5, DARK))
            pw, ph = pr.wrap(W-2.5*inch, 2*inch)
            if y - ph < 0.9*inch:
                c.showPage(); y = page_header(c, "Boundary Scripts (cont.)")
                c.setFillColor(BURGUNDY); c.setFont(TITLE_FONT, 14)
                c.drawString(inch, y, sec + " (cont.)"); y -= 0.35*inch
            # left gold bar
            c.setFillColor(GOLD)
            c.rect(inch, y-ph-2, 3, ph+4, fill=1, stroke=0)
            pr.drawOn(c, inch+0.18*inch, y-ph)
            y -= ph + 0.22*inch
        y -= 0.25*inch
    if y < 1.8*inch:
        c.showPage(); y = page_header(c, "You Said It")
    gold_divider(c, y); y -= 0.35*inch
    p = Paragraph("Every boundary you hold is a vote for the woman you're becoming. "
                  "If this cheat sheet helped, the <b>Healing Vibe Journal</b> goes deeper — "
                  "and a free 20-minute Vibe Session with Christina is the fastest way "
                  "to get personalized support. shesthevibe.co",
                  prompt_style(11, DARK, center=True))
    pw, ph = p.wrap(W-2.4*inch, 3*inch)
    p.drawOn(c, (W-pw)/2, y-ph)
    c.showPage(); c.save()

if __name__ == "__main__":
    build_prompts(); print("built 50-journal-prompts.pdf")
    build_reset(); print("built 5-minute-morning-reset.pdf")
    build_scripts(); print("built boundary-scripts.pdf")
