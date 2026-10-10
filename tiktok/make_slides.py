#!/usr/bin/env python3
"""Render TikTok text cards for She's The Vibe. 1080x1920 slides with PIL."""
import os, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
ASSETS = os.path.expanduser("~/workspace/shes-the-vibe/tiktok/assets")
OUT = os.path.expanduser("~/workspace/shes-the-vibe/tiktok/slides")
os.makedirs(OUT, exist_ok=True)

GOLD = (212, 175, 106)
GOLD_DEEP = (176, 141, 79)
CREAM = (247, 231, 206)
WHITE = (255, 255, 255)
BURGUNDY = (69, 20, 37)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"  # no italic available; use book
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def load_bg(name):
    for f in os.listdir(ASSETS):
        if f.startswith(name) and f.endswith((".webp", ".png", ".jpg")):
            img = Image.open(os.path.join(ASSETS, f)).convert("RGB")
            # cover-crop to 1080x1920
            r = max(W / img.width, H / img.height)
            img = img.resize((int(img.width * r) + 1, int(img.height * r) + 1), Image.LANCZOS)
            x = (img.width - W) // 2
            y = (img.height - H) // 2
            return img.crop((x, y, x + W, y + H))
    raise FileNotFoundError(name)

def dim(img, amount=0.45):
    """Darken image for text readability."""
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
        lines = wrap(draw, text, fnt, max_w or W - 160)
        lh = fnt.size + int(fnt.size * 0.35)
        for line in lines:
            if lpad:  # manual letter spacing
                tw = sum(draw.textlength(ch, font=fnt) + lpad for ch in line) - lpad
                x = cx - tw / 2
                for ch in line:
                    draw.text((x, y), ch, font=fnt, fill=color,
                              stroke_width=2, stroke_fill=(0, 0, 0))
                    x += draw.textlength(ch, font=fnt) + lpad
            else:
                tw = draw.textlength(line, font=fnt)
                draw.text((cx - tw / 2, y), line, font=fnt, fill=color,
                          stroke_width=2, stroke_fill=(0, 0, 0))
            y += lh
        y += after
    return y

def divider(draw, cx, y, color=GOLD):
    f = font(SERIF, 44)
    t = "\u25c6   \u25c6   \u25c6"
    tw = draw.textlength(t, font=f)
    draw.text((cx - tw / 2, y), t, font=f, fill=color,
              stroke_width=1, stroke_fill=(0, 0, 0))
    return y + 90

def save(img, name):
    p = os.path.join(OUT, name)
    img.save(p, "PNG")
    print("wrote", p)
    return p

# ============ VIDEO 2: 3 Journal Prompts ============
silk = vignette(dim(load_bg("media-generation-bg-burgundy-silk"), 0.35))
flourish = load_bg("media-generation-bg-gold-flourish")  # already dark

def slide2(lines_blocks, bg, name):
    img = bg.copy(); d = ImageDraw.Draw(img)
    total = 0
    for text, fnt, color, after, max_w, lpad in lines_blocks:
        ls = wrap(d, text, fnt, max_w or W - 160)
        total += len(ls) * (fnt.size + int(fnt.size * 0.35)) + after
    total += 90  # divider
    y = (H - total) / 2
    y = divider(d, W / 2, y)
    draw_centered_block(d, W / 2, y, lines_blocks)
    save(img, name)

f_big = lambda s: font(SERIF_B, s)
f_it = lambda s: font(SERIF_I, s)
f_sans = lambda s: font(SANS, s)

# Hook
slide2([
    ("Feeling stuck?", f_it(110), CREAM, 20, None, 0),
    ("Write this down.", f_big(96), GOLD, 30, None, 0),
], silk, "v2_hook.png")

# Prompt 1
slide2([
    ("prompt one", f_sans(44), GOLD, 30, None, 8),
    ("What am I pretending not to know?", f_big(88), WHITE, 20, None, 0),
], flourish, "v2_p1.png")

# Prompt 2
slide2([
    ("prompt two", f_sans(44), GOLD, 30, None, 8),
    ("What would I do if I trusted myself completely?", f_big(84), WHITE, 20, None, 0),
], flourish, "v2_p2.png")

# Prompt 3
slide2([
    ("prompt three", f_sans(44), GOLD, 30, None, 8),
    ("Who am I becoming \u2014 and what\u2019s in her way?", f_big(84), WHITE, 20, None, 0),
], flourish, "v2_p3.png")

# Final card with healing journal cover
heal = Image.open(os.path.expanduser(
    "~/workspace/shes-the-vibe/digital-products/covers/cover-healing-final.png")).convert("RGB")
img = flourish.copy()
cw, ch = 560, int(560 * heal.height / heal.width)
heal = heal.resize((cw, ch), Image.LANCZOS)
img.paste(heal, ((W - cw) // 2, 380))
d = ImageDraw.Draw(img)
y = 380 + ch + 60
y = draw_centered_block(d, W / 2, y, [
    ("50 more inside the", f_it(64), CREAM, 10, None, 0),
    ("Healing Vibe Journal", f_big(76), GOLD, 40, None, 0),
])
divider(d, W / 2, y)
d2 = ImageDraw.Draw(img)
f = font(SANS_B, 44); t = "Save this for later"
tw = d2.textlength(t, font=f)
d2.text((W/2 - tw/2, H - 320), t, font=f, fill=WHITE, stroke_width=2, stroke_fill=(0,0,0))
save(img, "v2_final.png")

# ============ VIDEO 7: Brand Manifesto ============
def slide7(lines_blocks, name):
    img = flourish.copy(); d = ImageDraw.Draw(img)
    total = 90
    for text, fnt, color, after, max_w, lpad in lines_blocks:
        ls = wrap(d, text, fnt, max_w or W - 160)
        total += len(ls) * (fnt.size + int(fnt.size * 0.35)) + after
    y = (H - total) / 2
    y = divider(d, W / 2, y)
    draw_centered_block(d, W / 2, y, lines_blocks)
    save(img, name)

slide7([
    ("Practical. Pretty. You.", f_big(92), GOLD, 25, None, 0),
    ("here\u2019s what that means", f_it(72), CREAM, 20, None, 0),
], "v7_hook.png")

slide7([
    ("PRACTICAL.", f_big(120), GOLD, 30, None, 10),
    ("Tools that actually organize your life.", f_it(68), WHITE, 20, None, 0),
], "v7_practical.png")

slide7([
    ("PRETTY.", f_big(120), GOLD, 30, None, 10),
    ("Because beautiful things get used.", f_it(68), WHITE, 20, None, 0),
], "v7_pretty.png")

slide7([
    ("YOU.", f_big(120), GOLD, 30, None, 10),
    ("Made for the woman becoming herself.", f_it(68), WHITE, 20, None, 0),
], "v7_you.png")

# Brand card
brand = Image.open(os.path.expanduser(
    "~/workspace/shes-the-vibe/brand-illustration.png")).convert("RGB")
img = flourish.copy()
bw, bh = 700, int(700 * brand.height / brand.width)
brand = brand.resize((bw, bh), Image.LANCZOS)
img.paste(brand, ((W - bw) // 2, 420))
d = ImageDraw.Draw(img)
y = 420 + bh + 70
draw_centered_block(d, W / 2, y, [
    ("She\u2019s The Vibe", f_big(96), GOLD, 15, None, 0),
    ("Practical. Pretty. You.", f_it(60), CREAM, 20, None, 0),
])
save(img, "v7_final.png")

# ============ PRIORITY 2: Dashboard teaser ============
flat = vignette(dim(load_bg("media-generation-bg-planner-flatlay"), 0.45))

def slideD(lines_blocks, name):
    img = flat.copy(); d = ImageDraw.Draw(img)
    total = 90
    for text, fnt, color, after, max_w, lpad in lines_blocks:
        ls = wrap(d, text, fnt, max_w or W - 160)
        total += len(ls) * (fnt.size + int(fnt.size * 0.35)) + after
    y = (H - total) / 2
    y = divider(d, W / 2, y)
    draw_centered_block(d, W / 2, y, lines_blocks)
    save(img, name)

slideD([
    ("POV: your whole life", f_it(84), CREAM, 10, None, 0),
    ("fits on ONE spreadsheet", f_big(88), GOLD, 20, None, 0),
], "vd_hook.png")

slideD([
    ("Budget  \u2022  Habits  \u2022  Goals  \u2022  Bills", f_sans(52), GOLD, 30, None, 0),
    ("all in one place", f_it(76), WHITE, 20, None, 0),
], "vd_features.png")

slideD([
    ("The Vibe Dashboard", f_big(96), GOLD, 25, None, 0),
    ("the spreadsheet that runs my life", f_it(64), WHITE, 20, None, 0),
], "vd_product.png")

slideD([
    ("Link in bio", f_big(100), GOLD, 25, None, 0),
    ("She\u2019s The Vibe", f_it(68), CREAM, 20, None, 0),
], "vd_cta.png")

print("ALL SLIDES DONE")
