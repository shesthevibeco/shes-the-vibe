#!/usr/bin/env python3
"""Transparent text overlays (1080x1920) for series episode 1 clip segments."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
GOLD = (201, 169, 110)
CREAM = (247, 231, 206)

FD = os.path.dirname(os.path.abspath(__file__))
FONTS = "/home/hatch/workspace/shes-the-vibe/tiktok/final/assets/fonts"
OV_DIR = os.path.join(FD, "overlays")
os.makedirs(OV_DIR, exist_ok=True)

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

def shade(d, y0, y1, alpha=110):
    """Soft dark band for readability."""
    for y in range(y0, y1):
        t = abs(y - (y0+y1)/2) / ((y1-y0)/2)
        a = int(alpha * (1 - t*0.85))
        d.rectangle([(0, y), (W, y+1)], fill=(0, 0, 0, a))

def centered(d, y, text, font, fill, spacing=10):
    lines = text.split("\n")
    widths, heights, total = [], [], 0
    for ln in lines:
        b = d.textbbox((0,0), ln, font=font)
        w_, h_ = b[2]-b[0], b[3]-b[1]
        widths.append(w_); heights.append(h_); total += h_ + spacing
    total -= spacing
    yy = y
    for i, ln in enumerate(lines):
        d.text(((W-widths[i])/2, yy), ln, font=font, fill=fill+(255,))
        yy += heights[i] + spacing
    return y + total

def save(name, fn):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img, "RGBA")
    fn(d)
    img.save(os.path.join(OV_DIR, name))
    print("overlay:", name)

def ov_bang(d):
    shade(d, 420, 900)
    centered(d, 500, "Bang.", script(170), GOLD)
    centered(d, 760, "She shoved the bedroom\ndoor closed.", mont(52, "Medium"), CREAM)

def ov_therapy(d):
    shade(d, 1180, 1560)
    centered(d, 1260, "Family therapy had gone\nexactly how it always did.", playfair(66), CREAM)

def ov_teeth(d):
    shade(d, 1150, 1600)
    centered(d, 1230, "Nobody asked what she was\nholding so tightly\nbehind her teeth.", playfair(62), CREAM)

def ov_ping(d):
    shade(d, 700, 1050)
    centered(d, 770, "Ping.", script(170), GOLD)
    centered(d, 990, "The sound was so faint\nshe almost imagined it.", mont(46), CREAM)

def ov_photo(d):
    shade(d, 1120, 1620)
    centered(d, 1200, "There was a photograph\non the wall.", playfair(72), GOLD)
    centered(d, 1420, "That had not been\nthere before.", playfair(72), CREAM)

if __name__ == "__main__":
    save("ov_bang.png", ov_bang)
    save("ov_therapy.png", ov_therapy)
    save("ov_teeth.png", ov_teeth)
    save("ov_ping.png", ov_ping)
    save("ov_photo.png", ov_photo)
    print("OVERLAYS DONE")
