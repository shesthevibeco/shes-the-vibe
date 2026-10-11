#!/usr/bin/env python3
"""Generate dark cinematic 1080x1920 text cards for the INSTITUTIONALIZED series."""
import os, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
# Dark cinematic palette
BG = (26, 8, 13)          # near-black burgundy
BG2 = (42, 10, 18)        # slightly lifted for vignette feel
GOLD = (201, 169, 110)
DIMGOLD = (150, 120, 75)
CREAM = (247, 231, 206)
MUTED = (190, 170, 150)

FD = os.path.dirname(os.path.abspath(__file__))
FONTS = "/home/hatch/workspace/shes-the-vibe/tiktok/final/assets/fonts"
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

def base_card():
    img = Image.new("RGB", (W, H), BG)
    # subtle vertical gradient lift
    d = ImageDraw.Draw(img)
    for y in range(0, H, 8):
        t = y / H
        c = tuple(int(BG[i] + (BG2[i]-BG[i]) * (1-abs(t-0.45)*2) * 0.6) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    return img

def dim_sparkle(d, cx, cy, r, alpha=90):
    pts = []
    for i in range(8):
        ang = math.pi * i / 4 - math.pi / 2
        rr = r if i % 2 == 0 else r * 0.35
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=DIMGOLD + (alpha,))

def scatter_dim(d, n, seed=0):
    rnd = random.Random(seed)
    for _ in range(n):
        x = rnd.randint(60, W-60); y = rnd.randint(120, H-120)
        dim_sparkle(d, x, y, rnd.randint(5, 12), rnd.randint(40, 100))

def thin_frame(d, inset=40):
    d.rounded_rectangle([inset, inset, W-inset, H-inset], radius=24, outline=DIMGOLD, width=2)

def centered(d, y, text, font, fill, spacing=10, max_w=None):
    lines = text.split("\n")
    widths, heights, total = [], [], 0
    for ln in lines:
        b = d.textbbox((0,0), ln, font=font)
        w_, h_ = b[2]-b[0], b[3]-b[1]
        widths.append(w_); heights.append(h_); total += h_ + spacing
    total -= spacing
    yy = y
    for i, ln in enumerate(lines):
        x = (W - widths[i]) / 2
        d.text((x, yy), ln, font=font, fill=fill)
        yy += heights[i] + spacing
    return y + total

def divider(d, y, width=260):
    cx = W//2
    d.line([cx-width//2, y, cx+width//2, y], fill=DIMGOLD, width=2)
    dim_sparkle(d, cx, y, 12, 120)

def film_grain(img, amt=6):
    import numpy as np
    arr = np.asarray(img).astype(int)
    noise = np.random.randint(-amt, amt+1, arr.shape)
    arr = np.clip(arr + noise, 0, 255).astype("uint8")
    return Image.fromarray(arr)

def save(name, draw_fn):
    img = base_card()
    d = ImageDraw.Draw(img, "RGBA")
    thin_frame(d)
    scatter_dim(d, 14, seed=hash(name) % 9999)
    draw_fn(d)
    img = film_grain(img)
    img.save(os.path.join(CARD_DIR, name))
    print("card:", name)

def hook(d):
    centered(d, 700, "Once you went in,\nyou didn't come out.", playfair(92), GOLD)
    centered(d, 1080, "a story in six parts", script(64), MUTED)

def room(d):
    centered(d, 640, "White walls.\nInstitutional furniture.", playfair(72), CREAM)
    divider(d, 1080)
    centered(d, 1150, "A narrow bed\ndressed in pink.", playfair(88), GOLD)

def rules(d):
    centered(d, 700, "Laminated rules.\nA door that didn't lock.\nA black circle\nin the ceiling.", mont(56, "Medium"), CREAM)

def out(d):
    centered(d, 640, "Out of the building.", playfair(76), GOLD)
    centered(d, 800, "Out of her mother's\nversion of her.", playfair(76), CREAM)
    centered(d, 1120, "Out of the life everyone else\nchose before she could.", mont(44), MUTED)

def part1(d):
    centered(d, 560, "PART 1", mont(64, "Bold"), GOLD)
    centered(d, 700, "The Pink Bed", script(120), CREAM)
    divider(d, 1050)
    centered(d, 1140, "FOLLOW FOR PART 2", playfair(64), GOLD)
    centered(d, 1300, "@shes.the.vibe.co", mont(44), MUTED)
    centered(d, 1420, "full story — link in bio", script(56), DIMGOLD)

if __name__ == "__main__":
    save("s1_hook.png", hook)
    save("s1_room.png", room)
    save("s1_rules.png", rules)
    save("s1_out.png", out)
    save("s1_part1.png", part1)
    print("SERIES CARDS DONE")
