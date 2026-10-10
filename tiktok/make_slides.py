#!/usr/bin/env python3
"""Render TikTok text cards for She's The Vibe. 1080x1920 slides with PIL.

V2 design: TikTok-native pacing. Hooks hit in 1-2s, big bold high-contrast
text, rapid-fire cards. No gentle intros.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
ASSETS = os.path.expanduser("~/workspace/shes-the-vibe/tiktok/assets")
OUT = os.path.expanduser("~/workspace/shes-the-vibe/tiktok/slides")
os.makedirs(OUT, exist_ok=True)

GOLD = (201, 169, 110)
CREAM = (247, 231, 206)
WHITE = (255, 255, 255)
BURGUNDY = (69, 20, 37)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"  # no italic; book reads as italic-ish at slant
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def load_bg(name):
    for f in os.listdir(ASSETS):
        if f.startswith(name) and f.endswith((".webp", ".png", ".jpg")):
            img = Image.open(os.path.join(ASSETS, f)).convert("RGB")
            r = max(W / img.width, H / img.height)
            img = img.resize((int(img.width * r) + 1, int(img.height * r) + 1), Image.LANCZOS)
            x = (img.width - W) // 2
            y = (img.height - H) // 2
            return img.crop((x, y, x + W, y + H))
    raise FileNotFoundError(name)

def dim(img, amount=0.55):
    overlay = Image.new("RGB", img.size, (0, 0, 0))
    return Image.blend(img, overlay, amount)

def vignette(img):
    mask = Image.new("L", img.size, 0)
    d = ImageDraw.Draw(mask)
    d.ellipse((-W * 0.35, -H * 0.25, W * 1.35, H * 1.25), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(220))
    black = Image.new("RGB", img.size, (10, 2, 6))
    return Image.composite(img, black, mask)

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def draw_centered_block(draw, cx, y, blocks):
    """blocks: list of (text, font, color, spacing_after, max_width, letter_pad). Returns end y."""
    for text, fnt, color, after, max_w, lpad in blocks:
        lines = wrap(draw, text, fnt, max_w or W - 120)
        lh = fnt.size + int(fnt.size * 0.32)
        for line in lines:
            if lpad:
                tw = sum(draw.textlength(ch, font=fnt) + lpad for ch in line) - lpad
                x = cx - tw / 2
                for ch in line:
                    draw.text((x, y), ch, font=fnt, fill=color,
                              stroke_width=3, stroke_fill=(0, 0, 0))
                    x += draw.textlength(ch, font=fnt) + lpad
            else:
                tw = draw.textlength(line, font=fnt)
                draw.text((cx - tw / 2, y), line, font=fnt, fill=color,
                          stroke_width=3, stroke_fill=(0, 0, 0))
            y += lh
        y += after
    return y

def divider(draw, cx, y, color=GOLD):
    f = font(SERIF_B, 40)
    t = "\u25c6   \u25c6   \u25c6"
    tw = draw.textlength(t, font=f)
    draw.text((cx - tw / 2, y), t, font=f, fill=color,
              stroke_width=1, stroke_fill=(0, 0, 0))
    return y + 80

def save(img, name):
    p = os.path.join(OUT, name)
    img.save(p, "PNG")
    print("wrote", p)
    return p

def punch_slide(bg, blocks, name, div=True):
    """Centered bold slide with optional top divider."""
    img = bg.copy(); d = ImageDraw.Draw(img)
    total = 80 if div else 0
    for text, fnt, color, after, max_w, lpad in blocks:
        ls = wrap(d, text, fnt, max_w or W - 120)
        total += len(ls) * (fnt.size + int(fnt.size * 0.32)) + after
    y = (H - total) / 2
    if div:
        y = divider(d, W / 2, y)
    draw_centered_block(d, W / 2, y, blocks)
    save(img, name)

f_bold = lambda s: font(SERIF_B, s)
f_it = lambda s: font(SERIF_I, s)
f_sans = lambda s: font(SANS, s)
f_sansb = lambda s: font(SANS_B, s)

flourish = load_bg("media-generation-bg-gold-flourish")          # already dark
silk = vignette(dim(load_bg("media-generation-bg-burgundy-silk"), 0.45))
flat = vignette(dim(load_bg("media-generation-bg-planner-flatlay"), 0.55))
flat_dark = vignette(dim(load_bg("media-generation-bg-planner-flatlay"), 0.65))

# ============================================================
# VIDEO 1: Brand Manifesto (~16.5s) — STOP SCROLLING energy
# ============================================================
punch_slide(flourish, [
    ("STOP SCROLLING", f_sansb(148), GOLD, 25, None, 6),
    ("3 words changed my life", f_it(78), CREAM, 20, None, 0),
], "v7_hook.png")

punch_slide(flourish, [
    ("PRACTICAL", f_sansb(150), GOLD, 25, None, 8),
    ("pretty is pointless if it doesn't work", f_it(70), WHITE, 20, None, 0),
], "v7_practical.png")

punch_slide(flourish, [
    ("PRETTY", f_sansb(150), GOLD, 25, None, 8),
    ("beautiful things get USED", f_it(70), WHITE, 20, None, 0),
], "v7_pretty.png")

punch_slide(flourish, [
    ("YOU", f_sansb(150), GOLD, 25, None, 8),
    ("never about fitting a box", f_it(70), WHITE, 20, None, 0),
], "v7_you.png")

# Brand card
brand = Image.open(os.path.expanduser(
    "~/workspace/shes-the-vibe/brand-illustration.png")).convert("RGB")
img = flourish.copy()
bw, bh = 640, int(640 * brand.height / brand.width)
brand = brand.resize((bw, bh), Image.LANCZOS)
img.paste(brand, ((W - bw) // 2, 400))
d = ImageDraw.Draw(img)
y = 400 + bh + 60
draw_centered_block(d, W / 2, y, [
    ("She's The Vibe", f_bold(92), GOLD, 15, None, 0),
    ("@shes.the.vibe.co", f_sans(56), CREAM, 20, None, 0),
])
save(img, "v7_final.png")

punch_slide(silk, [
    ("FOLLOW FOR", f_sansb(110), CREAM, 15, None, 6),
    ("THE VIBE", f_sansb(150), GOLD, 30, None, 8),
    ("new drops every week", f_it(66), WHITE, 20, None, 0),
], "v7_cta.png")

# ============================================================
# VIDEO 2: 3 Journal Prompts (~17.5s) — fast value hits
# ============================================================
punch_slide(silk, [
    ("FEELING STUCK?", f_sansb(132), GOLD, 25, None, 4),
    ("write this down.", f_it(88), CREAM, 20, None, 0),
], "v2_hook.png")

punch_slide(flourish, [
    ("PROMPT 1", f_sansb(52), GOLD, 30, None, 10),
    ("What am I pretending not to know?", f_bold(92), WHITE, 20, None, 0),
], "v2_p1.png")

punch_slide(flourish, [
    ("PROMPT 2", f_sansb(52), GOLD, 30, None, 10),
    ("What would I do if I trusted myself?", f_bold(88), WHITE, 20, None, 0),
], "v2_p2.png")

punch_slide(flourish, [
    ("PROMPT 3", f_sansb(52), GOLD, 30, None, 10),
    ("Who am I becoming?", f_bold(96), WHITE, 20, None, 0),
], "v2_p3.png")

# Final card with healing journal cover
heal = Image.open(os.path.expanduser(
    "~/workspace/shes-the-vibe/digital-products/covers/cover-healing-final.png")).convert("RGB")
img = flourish.copy()
cw, ch = 520, int(520 * heal.height / heal.width)
heal = heal.resize((cw, ch), Image.LANCZOS)
img.paste(heal, ((W - cw) // 2, 360))
d = ImageDraw.Draw(img)
y = 360 + ch + 55
y = draw_centered_block(d, W / 2, y, [
    ("50 more inside the", f_it(62), CREAM, 10, None, 0),
    ("Healing Vibe Journal", f_bold(74), GOLD, 35, None, 0),
])
divider(d, W / 2, y)
f = font(SANS_B, 52); t = "SAVE THIS POST"
tw = d.textlength(t, font=f)
d.text((W/2 - tw/2, H - 300), t, font=f, fill=GOLD, stroke_width=3, stroke_fill=(0,0,0))
save(img, "v2_final.png")

punch_slide(silk, [
    ("SAVE THIS", f_sansb(140), GOLD, 20, None, 8),
    ("follow @shes.the.vibe.co", f_sans(60), CREAM, 20, None, 0),
], "v2_cta.png")

# ============================================================
# VIDEO 3: Dashboard teaser (~14.5s) — rapid-fire features
# ============================================================
punch_slide(flat, [
    ("POV:", f_sansb(72), CREAM, 20, None, 10),
    ("YOUR WHOLE LIFE", f_sansb(112), GOLD, 15, None, 4),
    ("on ONE spreadsheet", f_it(78), WHITE, 20, None, 0),
], "vd_hook.png")

for i, word in enumerate(["BUDGET", "HABITS", "GOALS", "BILLS"]):
    bg = flat_dark if i % 2 else flat
    punch_slide(bg, [
        (word + " \u2713", f_sansb(150), GOLD, 20, None, 8),
    ], f"vd_f{i+1}.png", div=False)

punch_slide(flat, [
    ("The Vibe Dashboard", f_bold(92), GOLD, 20, None, 0),
    ("the spreadsheet that runs my life", f_it(64), WHITE, 20, None, 0),
], "vd_product.png")

punch_slide(silk, [
    ("LINK IN BIO", f_sansb(140), GOLD, 25, None, 8),
    ("@shes.the.vibe.co", f_sans(60), CREAM, 20, None, 0),
], "vd_cta.png")

print("ALL SLIDES DONE")
