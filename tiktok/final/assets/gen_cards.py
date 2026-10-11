#!/usr/bin/env python3
"""Generate branded 1080x1920 text cards for STV TikToks."""
import os, math, random
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
BURGUNDY = (69, 20, 37)
GOLD = (201, 169, 110)
CREAM = (247, 231, 206)
DARKGOLD = (160, 130, 80)
WHITE = (255, 255, 255)

FD = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(FD, "fonts")
CARD_DIR = os.path.join(FD, "cards")
os.makedirs(CARD_DIR, exist_ok=True)

def script(size): return ImageFont.truetype(os.path.join(FONTS, "Parisienne-Regular.ttf"), size)
def mont(size, weight="Regular"):
    f = ImageFont.truetype(os.path.join(FONTS, "Montserrat-VF.ttf"), size)
    try: f.set_variation_by_name(weight.encode())
    except: pass
    return f
def playfair(size, weight="Bold"):
    f = ImageFont.truetype(os.path.join(FONTS, "PlayfairDisplay-VF.ttf"), size)
    try: f.set_variation_by_name(weight.encode())
    except: pass
    return f

def draw_sparkle(d, cx, cy, r, color, alpha=255):
    """4-point star sparkle."""
    pts = []
    for i in range(8):
        ang = math.pi * i / 4 - math.pi / 2
        rr = r if i % 2 == 0 else r * 0.35
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=color + (alpha,) if len(color) == 3 else color)

def scatter_sparkles(d, n, color, rmin=6, rmax=18, seed=0, y_range=(0, H)):
    rnd = random.Random(seed)
    for _ in range(n):
        x = rnd.randint(40, W - 40)
        y = rnd.randint(y_range[0], y_range[1])
        draw_sparkle(d, x, y, rnd.randint(rmin, rmax), color, rnd.randint(120, 255))

def gold_frame(d, inset=36, width=3):
    d.rounded_rectangle([inset, inset, W - inset, H - inset], radius=28, outline=GOLD, width=width)

def divider(d, y, width=340):
    cx = W // 2
    d.line([cx - width//2, y, cx + width//2, y], fill=GOLD, width=3)
    draw_sparkle(d, cx, y, 16, GOLD)

def flourish(d, y, color=GOLD):
    """Thin elegant curved flourish line under text."""
    cx = W // 2
    pts = []
    for t in range(0, 201):
        x = cx - 220 + t * 2.2
        yy = y + 14 * math.sin(t * math.pi / 200)
        pts.append((x, yy))
    d.line(pts, fill=color, width=3, joint="curve")

def centered_text(d, y, text, font, fill, stroke_w=0, stroke_fill=None, spacing=4):
    """Draw centered text, returns bottom y. Supports \n."""
    lines = text.split("\n")
    # measure
    line_h = []
    total_h = 0
    widths = []
    for ln in lines:
        bbox = d.textbbox((0, 0), ln, font=font, stroke_width=stroke_w)
        w_ = bbox[2] - bbox[0]; h_ = bbox[3] - bbox[1]
        widths.append(w_); line_h.append(h_)
        total_h += h_ + spacing
    total_h -= spacing
    yy = y
    for i, ln in enumerate(lines):
        x = (W - widths[i]) / 2
        # adjust for bbox offset
        bbox = d.textbbox((0, 0), ln, font=font, stroke_width=stroke_w)
        d.text((x - bbox[0], yy - bbox[1]), ln, font=font, fill=fill,
               stroke_width=stroke_w, stroke_fill=stroke_fill)
        yy += line_h[i] + spacing
    return yy

def bg_burgundy():
    img = Image.new("RGB", (W, H), BURGUNDY)
    d = ImageDraw.Draw(img, "RGBA")
    # subtle radial glow top
    for r in range(600, 0, -20):
        a = int(18 * (1 - r / 600))
        d.ellipse([W//2 - r, -200 - r//2, W//2 + r, -200 + r//2 + r], fill=(201, 169, 110, a))
    return img, d

def bg_cream():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img, "RGBA")
    for r in range(600, 0, -20):
        a = int(14 * (1 - r / 600))
        d.ellipse([W//2 - r, H + 200 - r//2, W//2 + r, H + 200 + r//2], fill=(201, 169, 110, a))
    return img, d

def bg_gradient():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        c = tuple(int(BURGUNDY[i] * (1 - t * 0.35)) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    d = ImageDraw.Draw(img, "RGBA")
    return img, d

def save(img, name):
    p = os.path.join(CARD_DIR, name)
    img.save(p)
    print("saved", name)

# ============ VIDEO 1: MANIFESTO ============
def v1():
    # 1. HOOK
    img, d = bg_burgundy()
    scatter_sparkles(d, 22, GOLD, seed=11)
    gold_frame(d)
    centered_text(d, 330, "STOP\nSCROLLING", playfair(150), GOLD, stroke_w=2, stroke_fill=(40, 10, 20))
    divider(d, 830)
    centered_text(d, 900, "3 words changed my life", script(92), CREAM)
    centered_text(d, 1620, "@shes.the.vibe.co", mont(44, "SemiBold"), GOLD)
    save(img, "v1_hook.png")

    # 2. PRACTICAL
    img, d = bg_cream()
    scatter_sparkles(d, 16, DARKGOLD, seed=21)
    gold_frame(d)
    centered_text(d, 560, "PRACTICAL", playfair(140), BURGUNDY)
    flourish(d, 800)
    centered_text(d, 900, "pretty is pointless\nif it doesn't work", mont(58), BURGUNDY)
    centered_text(d, 1620, "@shes.the.vibe.co", mont(44, "SemiBold"), DARKGOLD)
    save(img, "v1_practical.png")

    # 3. PRETTY
    img, d = bg_burgundy()
    scatter_sparkles(d, 22, GOLD, seed=31)
    gold_frame(d)
    centered_text(d, 560, "PRETTY", playfair(150), GOLD, stroke_w=2, stroke_fill=(40, 10, 20))
    flourish(d, 800)
    centered_text(d, 900, "beautiful things\nget USED", mont(58), CREAM)
    centered_text(d, 1620, "@shes.the.vibe.co", mont(44, "SemiBold"), GOLD)
    save(img, "v1_pretty.png")

    # 4. YOU
    img, d = bg_cream()
    scatter_sparkles(d, 16, DARKGOLD, seed=41)
    gold_frame(d)
    centered_text(d, 560, "YOU", playfair(170), BURGUNDY)
    flourish(d, 820)
    centered_text(d, 920, "never about\nfitting a box", mont(58), BURGUNDY)
    centered_text(d, 1620, "@shes.the.vibe.co", mont(44, "SemiBold"), DARKGOLD)
    save(img, "v1_you.png")

    # 5. BRAND (illustration placeholder area - composited in ffmpeg)
    img, d = bg_gradient()
    scatter_sparkles(d, 26, GOLD, seed=51)
    gold_frame(d)
    centered_text(d, 240, "She's The Vibe", script(120), GOLD)
    # circle placeholder guide (illustration overlaid in ffmpeg)
    d.ellipse([W//2 - 260, 560, W//2 + 260, 1080], outline=GOLD, width=5)
    centered_text(d, 580, "", mont(40), CREAM)
    centered_text(d, 1180, "@shes.the.vibe.co", mont(56, "SemiBold"), CREAM)
    centered_text(d, 1300, "Practical. Pretty. You.", script(72), GOLD)
    save(img, "v1_brand.png")

    # 6. PILLARS
    img, d = bg_burgundy()
    scatter_sparkles(d, 22, GOLD, seed=61)
    gold_frame(d)
    centered_text(d, 420, "what we make", script(88), GOLD)
    divider(d, 640)
    centered_text(d, 720, "PLANNERS", playfair(104), CREAM)
    draw_sparkle(d, W//2, 900, 20, GOLD)
    centered_text(d, 960, "JOURNALS", playfair(104), CREAM)
    draw_sparkle(d, W//2, 1140, 20, GOLD)
    centered_text(d, 1200, "JEWELRY", playfair(104), CREAM)
    centered_text(d, 1620, "@shes.the.vibe.co", mont(44, "SemiBold"), GOLD)
    save(img, "v1_pillars.png")

    # 7. CTA
    img, d = bg_cream()
    scatter_sparkles(d, 26, DARKGOLD, seed=71)
    gold_frame(d, width=5)
    centered_text(d, 480, "FOLLOW FOR\nTHE VIBE", playfair(130), BURGUNDY)
    flourish(d, 900, DARKGOLD)
    centered_text(d, 1000, "new drops every week", script(84), DARKGOLD)
    centered_text(d, 1250, "shesthevibe.co", mont(64, "Bold"), BURGUNDY)
    draw_sparkle(d, W//2 - 260, 1280, 22, DARKGOLD)
    draw_sparkle(d, W//2 + 260, 1280, 22, DARKGOLD)
    save(img, "v1_cta.png")

# ============ VIDEO 2: JOURNAL PROMPTS ============
def v2():
    # 1. HOOK
    img, d = bg_burgundy()
    scatter_sparkles(d, 22, GOLD, seed=111)
    gold_frame(d)
    centered_text(d, 380, "FEELING\nSTUCK?", playfair(150), GOLD, stroke_w=2, stroke_fill=(40, 10, 20))
    divider(d, 900)
    centered_text(d, 970, "write this down", script(100), CREAM)
    centered_text(d, 1620, "@shes.the.vibe.co", mont(44, "SemiBold"), GOLD)
    save(img, "v2_hook.png")

    prompts = [
        ("v2_p1.png", "prompt no. 1", "What am I\npretending\nnot to know?", 112),
        ("v2_p2.png", "prompt no. 2", "What would I do\nif I trusted\nmyself?", 212),
        ("v2_p3.png", "prompt no. 3", "Who am I\nbecoming?", 312),
    ]
    for name, kicker, text, seed in prompts:
        img, d = bg_cream()
        scatter_sparkles(d, 18, DARKGOLD, seed=seed)
        gold_frame(d)
        centered_text(d, 380, kicker, script(80), DARKGOLD)
        divider(d, 560, width=260)
        centered_text(d, 640, text, playfair(108), BURGUNDY, spacing=10)
        # journal lines decoration
        for i, yy in enumerate([1150, 1210, 1270]):
            d.line([240, yy, 840, yy], fill=(160, 130, 80, 90), width=2)
        centered_text(d, 1620, "@shes.the.vibe.co", mont(44, "SemiBold"), DARKGOLD)
        save(img, name)

    # 5. PRODUCT
    img, d = bg_burgundy()
    scatter_sparkles(d, 24, GOLD, seed=411)
    gold_frame(d)
    centered_text(d, 380, "the", script(84), GOLD)
    centered_text(d, 480, "HEALING VIBE\nJOURNAL", playfair(110), CREAM)
    flourish(d, 860)
    centered_text(d, 950, "50 more prompts\ninside", mont(60), GOLD)
    centered_text(d, 1250, "SAVE THIS POST", mont(56, "Bold"), CREAM)
    draw_sparkle(d, W//2 - 300, 1278, 20, GOLD)
    draw_sparkle(d, W//2 + 300, 1278, 20, GOLD)
    save(img, "v2_product.png")

    # 6. CTA
    img, d = bg_cream()
    scatter_sparkles(d, 26, DARKGOLD, seed=511)
    gold_frame(d, width=5)
    centered_text(d, 520, "SAVE THIS", playfair(140), BURGUNDY)
    centered_text(d, 780, "your future self says thanks", script(76), DARKGOLD)
    divider(d, 1000, width=300)
    centered_text(d, 1080, "follow", mont(48), DARKGOLD)
    centered_text(d, 1160, "@shes.the.vibe.co", mont(64, "Bold"), BURGUNDY)
    save(img, "v2_cta.png")

# ============ VIDEO 3: DASHBOARD ============
def v3():
    # 1. HOOK
    img, d = bg_burgundy()
    scatter_sparkles(d, 22, GOLD, seed=611)
    gold_frame(d)
    centered_text(d, 380, "POV:", mont(72, "Bold"), GOLD)
    centered_text(d, 500, "YOUR WHOLE LIFE", playfair(84), CREAM)
    centered_text(d, 680, "on ONE", script(96), GOLD)
    centered_text(d, 840, "spreadsheet", playfair(120), CREAM)
    centered_text(d, 1620, "@shes.the.vibe.co", mont(44, "SemiBold"), GOLD)
    save(img, "v3_hook.png")

    flashes = [("BUDGET", 712), ("HABITS", 722), ("GOALS", 732), ("BILLS", 742)]
    for word, seed in flashes:
        img, d = bg_cream()
        scatter_sparkles(d, 14, DARKGOLD, seed=seed)
        gold_frame(d, width=5)
        centered_text(d, 700, word, playfair(170), BURGUNDY)
        # big check
        chk = mont(200, "Bold")
        centered_text(d, 980, "\u2713", chk, DARKGOLD)
        save(img, f"v3_{word.lower()}.png")

    # 6. PRODUCT
    img, d = bg_burgundy()
    scatter_sparkles(d, 24, GOLD, seed=811)
    gold_frame(d)
    centered_text(d, 360, "the spreadsheet that", script(80), GOLD)
    centered_text(d, 480, "runs my life", script(110), CREAM)
    divider(d, 760)
    centered_text(d, 830, "THE VIBE\nDASHBOARD", playfair(120), GOLD, stroke_w=2, stroke_fill=(40, 10, 20))
    centered_text(d, 1200, "budgets \u00b7 habits \u00b7 goals \u00b7 bills", mont(52), CREAM)
    centered_text(d, 1330, "$37", playfair(120), GOLD)
    save(img, "v3_product.png")

    # 7. CTA
    img, d = bg_cream()
    scatter_sparkles(d, 26, DARKGOLD, seed=911)
    gold_frame(d, width=5)
    centered_text(d, 500, "LINK IN BIO", playfair(140), BURGUNDY)
    flourish(d, 780, DARKGOLD)
    centered_text(d, 880, "get your life together, cutely", script(76), DARKGOLD)
    centered_text(d, 1120, "@shes.the.vibe.co", mont(64, "Bold"), BURGUNDY)
    centered_text(d, 1260, "shesthevibe.co", mont(52, "SemiBold"), DARKGOLD)
    save(img, "v3_cta.png")

if __name__ == "__main__":
    v1(); v2(); v3()
    print("ALL CARDS DONE")
