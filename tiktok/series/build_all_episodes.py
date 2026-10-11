#!/usr/bin/env python3
"""Build INSTITUTIONALIZED episodes 2-6 + prequel (episode 0).
Data-driven framework: cards + overlays + segment lists, shared assembly machinery.
Escalation vs ep1: per-episode grade moods (warm ep4, cold ep5), varied card layouts
(giant rotated word card, voice-in-script cards, fading-sequence card), motif reuse
for continuity (same photograph, same room, same hallway, same red marker).
"""
import os, subprocess, glob, math, random
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
CARDS = os.path.join(BASE, "cards")
OV = os.path.join(BASE, "overlays")
ASSETS = os.path.join(BASE, "assets")
FONTS = "/home/hatch/workspace/shes-the-vibe/tiktok/final/assets/fonts"
FPS, W, H, TRANS = 30, 1080, 1920, 0.8

# ---------- palette ----------
BG = (26, 8, 13); BG2 = (42, 10, 18)
GOLD = (201, 169, 110); DIMGOLD = (150, 120, 75)
CREAM = (247, 231, 206); MUTED = (190, 170, 150)
RED = (178, 52, 58)
COLORS = {"GOLD": GOLD, "CREAM": CREAM, "MUTED": MUTED, "DIMGOLD": DIMGOLD, "RED": RED}

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

def font_for(b):
    f, s, w = b.get("f", "playfair"), b.get("s", 64), b.get("w", "Bold")
    return {"playfair": lambda: playfair(s, w), "script": lambda: script(s),
            "mont": lambda: mont(s, w)}[f]()

# ---------- card machinery ----------
def base_card():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    for y in range(0, H, 8):
        t = y / H
        c = tuple(int(BG[i] + (BG2[i] - BG[i]) * (1 - abs(t - 0.45) * 2) * 0.6) for i in range(3))
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
        dim_sparkle(d, rnd.randint(60, W - 60), rnd.randint(120, H - 120),
                    rnd.randint(5, 12), rnd.randint(40, 100))

def thin_frame(d, inset=40):
    d.rounded_rectangle([inset, inset, W - inset, H - inset], radius=24, outline=DIMGOLD, width=2)

def divider_block(d, y):
    cx = W // 2
    d.line([cx - 130, y, cx + 130, y], fill=DIMGOLD, width=2)
    dim_sparkle(d, cx, y, 12, 120)

def film_grain(img, amt=6):
    import numpy as np
    arr = np.asarray(img).astype(int)
    noise = np.random.randint(-amt, amt + 1, arr.shape)
    return Image.fromarray(np.clip(arr + noise, 0, 255).astype("uint8"))

def draw_card(name, defn):
    if defn.get("word"):
        w = defn["word"]
        img = base_card(); d = ImageDraw.Draw(img, "RGBA")
        thin_frame(d); scatter_dim(d, 12, seed=abs(hash(name)) % 9999)
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
        f = playfair(w["size"], "Black" if False else "Bold")
        try: f = playfair(w["size"], "ExtraBold")
        except: pass
        bb = ld.textbbox((0, 0), w["text"], font=f)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        ld.text(((W - tw) / 2 - bb[0], (H - th) / 2 - bb[1]), w["text"], font=f, fill=COLORS[w["c"]])
        layer = layer.rotate(w.get("rotate", -4), resample=Image.BICUBIC, center=(W / 2, H / 2))
        img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
        img = film_grain(img)
        img.save(os.path.join(CARDS, name)); print("card:", name); return
    img = base_card(); d = ImageDraw.Draw(img, "RGBA")
    thin_frame(d); scatter_dim(d, 14, seed=abs(hash(name)) % 9999)
    blocks = defn["blocks"]
    items, total = [], 0
    for b in blocks:
        if b.get("type") == "divider":
            items.append((b, None, [], [], [], 46)); total += 46 + b.get("gap", 26); continue
        f = font_for(b); lines = b["text"].split("\n")
        ws, hs = [], []
        for ln in lines:
            bb = d.textbbox((0, 0), ln, font=f)
            ws.append(bb[2] - bb[0]); hs.append(bb[3] - bb[1])
        h = sum(hs) + b.get("spacing", 10) * (len(lines) - 1)
        items.append((b, f, lines, ws, hs, h)); total += h + b.get("gap", 26)
    total -= blocks[-1].get("gap", 26) if blocks else 0
    y = defn.get("cy", 960) - total / 2
    for (b, f, lines, ws, hs, h) in items:
        if b.get("type") == "divider":
            divider_block(d, y + 23); y += 46 + b.get("gap", 26); continue
        yy = y
        for i, ln in enumerate(lines):
            d.text(((W - ws[i]) / 2, yy), ln, font=f, fill=COLORS[b.get("c", "CREAM")])
            yy += hs[i] + b.get("spacing", 10)
        y += h + b.get("gap", 26)
    img = film_grain(img)
    img.save(os.path.join(CARDS, name)); print("card:", name)

# ---------- overlay machinery ----------
def draw_overlay(name, defn):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img, "RGBA")
    y0, y1, alpha = defn["shade"]
    for y in range(y0, y1):
        t = abs(y - (y0 + y1) / 2) / ((y1 - y0) / 2)
        d.rectangle([(0, y), (W, y + 1)], fill=(0, 0, 0, int(alpha * (1 - t * 0.85))))
    blocks = defn["blocks"]
    items, total = [], 0
    for b in blocks:
        f = font_for(b); lines = b["text"].split("\n")
        ws, hs = [], []
        for ln in lines:
            bb = d.textbbox((0, 0), ln, font=f)
            ws.append(bb[2] - bb[0]); hs.append(bb[3] - bb[1])
        h = sum(hs) + b.get("spacing", 10) * (len(lines) - 1)
        items.append((b, f, lines, ws, hs, h)); total += h + b.get("gap", 22)
    total -= blocks[-1].get("gap", 22) if blocks else 0
    y = defn.get("cy", (y0 + y1) / 2) - total / 2
    for (b, f, lines, ws, hs, h) in items:
        yy = y
        for i, ln in enumerate(lines):
            d.text(((W - ws[i]) / 2, yy), ln, font=f, fill=COLORS[b.get("c", "CREAM")] + (255,))
            yy += hs[i] + b.get("spacing", 10)
        y += h + b.get("gap", 22)
    img.save(os.path.join(OV, name)); print("overlay:", name)

# ================= CARD DEFINITIONS =================
CARDS_DEF = {
# ---- EPISODE 2: "BULLSHIT" ----
"ep2_hook.png": {"blocks": [
    {"text": "In the picture, Mom was smiling.", "f": "playfair", "s": 68, "c": "GOLD"},
    {"text": "The girl was the problem.", "f": "playfair", "s": 76, "c": "CREAM"}]},
"ep2_salad.png": {"blocks": [
    {"text": "Her mother had been furious\nbecause the restaurant served her\nbagged salad.", "f": "mont", "s": 50, "w": "Medium", "c": "CREAM"},
    {"type": "divider"},
    {"text": "Everyone spent the afternoon\naccommodating her mood.", "f": "mont", "s": 44, "c": "MUTED"}]},
"ep2_notshown.png": {"blocks": [
    {"text": "But that wasn't what\nthe picture showed.", "f": "playfair", "s": 84, "c": "GOLD"}]},
"ep2_bullshit.png": {"word": {"text": "BULLSHIT.", "size": 170, "c": "RED", "rotate": -4}},
"ep2_part2.png": {"blocks": [
    {"text": "PART 2", "f": "mont", "s": 60, "w": "Bold", "c": "GOLD"},
    {"text": "BULLSHIT", "f": "script", "s": 110, "c": "CREAM"},
    {"type": "divider"},
    {"text": "FOLLOW FOR PART 3", "f": "playfair", "s": 60, "c": "GOLD"},
    {"text": "@shes.the.vibe.co", "f": "mont", "s": 42, "c": "MUTED"},
    {"text": "full story \u2014 link in bio", "f": "script", "s": 52, "c": "DIMGOLD"}]},
# ---- EPISODE 3: "The File Speaks" ----
"ep3_hook.png": {"blocks": [
    {"text": "Destruction of property.\nVulgar language.\nEmotional dysregulation.", "f": "mont", "s": 54, "w": "Medium", "c": "CREAM"}]},
"ep3_no.png": {"blocks": [
    {"text": "No San Antonio. No bagged salad.", "f": "playfair", "s": 62, "c": "GOLD"},
    {"text": "No photograph.\nNo question why.", "f": "playfair", "s": 72, "c": "CREAM"}]},
"ep3_voice1.png": {"blocks": [
    {"text": "\u201cI know your full legal name,\nyour date of birth, every address.\u201d", "f": "script", "s": 62, "c": "CREAM"},
    {"type": "divider"},
    {"text": "\u201cI probably know you better\nthan you know yourself.\u201d", "f": "script", "s": 62, "c": "GOLD"}]},
"ep3_voice2.png": {"blocks": [
    {"text": "\u201cI don't cry. I don't yell.\nI don't change my story.\u201d", "f": "script", "s": 64, "c": "CREAM"},
    {"type": "divider"},
    {"text": "\u201cI'm just ink on paper. Right?\u201d", "f": "script", "s": 72, "c": "GOLD"}]},
"ep3_ready.png": {"blocks": [
    {"text": "\u201cReady?\u201d", "f": "playfair", "s": 150, "c": "GOLD"}]},
"ep3_part3.png": {"blocks": [
    {"text": "PART 3", "f": "mont", "s": 60, "w": "Bold", "c": "GOLD"},
    {"text": "The File Speaks", "f": "script", "s": 100, "c": "CREAM"},
    {"type": "divider"},
    {"text": "FOLLOW FOR PART 4", "f": "playfair", "s": 60, "c": "GOLD"},
    {"text": "@shes.the.vibe.co", "f": "mont", "s": 42, "c": "MUTED"}]},
# ---- EPISODE 4: "The Notebook" (warmer) ----
"ep4_hook.png": {"blocks": [
    {"text": "She started writing. Everything.", "f": "playfair", "s": 72, "c": "GOLD"},
    {"text": "Not for them. For herself.", "f": "script", "s": 66, "c": "CREAM"}]},
"ep4_truth.png": {"blocks": [
    {"text": "\u201cMom was mad. Not me.\nI did not throw the chair.\u201d", "f": "playfair", "s": 64, "c": "GOLD"},
    {"type": "divider"},
    {"text": "She hid the pages\nwhere they wouldn't search.", "f": "mont", "s": 44, "c": "MUTED"}]},
"ep4_smile.png": {"blocks": [
    {"text": "For the first time since arriving,\nshe smiled.", "f": "script", "s": 70, "c": "GOLD"},
    {"text": "Small. Almost suspicious.\nBut real.", "f": "playfair", "s": 60, "c": "CREAM"}]},
"ep4_clinician.png": {"blocks": [
    {"text": "\u201cI haven't had the chance\nto review your file yet.\u201d", "f": "playfair", "s": 60, "c": "CREAM"},
    {"text": "\u201cTell me about yourself.\u201d", "f": "playfair", "s": 72, "c": "GOLD"}]},
"ep4_part4.png": {"blocks": [
    {"text": "PART 4", "f": "mont", "s": 60, "w": "Bold", "c": "GOLD"},
    {"text": "The Notebook", "f": "script", "s": 110, "c": "CREAM"},
    {"type": "divider"},
    {"text": "FOLLOW FOR PART 5", "f": "playfair", "s": 60, "c": "GOLD"},
    {"text": "@shes.the.vibe.co", "f": "mont", "s": 42, "c": "MUTED"}]},
}

# ================= OVERLAY DEFINITIONS =================
OV_DEF = {
# ---- EP 2 ----
"ov_ep2_photo.png": {"shade": (1150, 1580, 110), "blocks": [
    {"text": "San Antonio. The River Walk.", "f": "playfair", "s": 64, "c": "GOLD"},
    {"text": "She knew the picture immediately.", "f": "mont", "s": 46, "c": "CREAM"}]},
"ov_ep2_marker.png": {"shade": (1150, 1580, 110), "blocks": [
    {"text": "She grabbed the red marker\nand uncapped it.", "f": "playfair", "s": 62, "c": "CREAM"}]},
"ov_ep2_gone.png": {"shade": (1100, 1620, 115), "blocks": [
    {"text": "The photograph was gone\nthe next morning.", "f": "playfair", "s": 66, "c": "GOLD"},
    {"text": "So were her red markers.", "f": "playfair", "s": 66, "c": "CREAM"}]},
# ---- EP 3 ----
"ov_ep3_file.png": {"shade": (1150, 1580, 110), "blocks": [
    {"text": "Her name sat at the top.", "f": "playfair", "s": 66, "c": "GOLD"},
    {"text": "Three neat lines.", "f": "playfair", "s": 66, "c": "CREAM"}]},
"ov_ep3_door.png": {"shade": (1150, 1560, 110), "blocks": [
    {"text": "The office door opened.", "f": "playfair", "s": 72, "c": "CREAM"}]},
# ---- EP 4 ----
"ov_ep4_writing.png": {"shade": (1150, 1600, 105), "blocks": [
    {"text": "She wrote what people said\nbefore they could rewrite it.", "f": "playfair", "s": 60, "c": "CREAM"}]},
"ov_ep4_shift.png": {"shade": (1150, 1600, 110), "blocks": [
    {"text": "One morning, the photograph shifted.", "f": "playfair", "s": 58, "c": "GOLD"},
    {"text": "Her mother's smile was gone.", "f": "playfair", "s": 58, "c": "CREAM"}]},
"ov_ep4_pillow.png": {"shade": (1180, 1580, 110), "blocks": [
    {"text": "The red marker appeared\nunderneath her pillow.", "f": "playfair", "s": 62, "c": "CREAM"}]},
}

CARDS_DEF.update({
# ---- EPISODE 5: "Easier Lately" (colder) ----
"ep5_hook.png": {"blocks": [
    {"text": "The clinician's hair was\nballroom-dancer slick.", "f": "playfair", "s": 68, "c": "CREAM"},
    {"text": "Not a strand out of place.", "f": "mont", "s": 46, "c": "MUTED"}]},
"ep5_account.png": {"blocks": [
    {"text": "\u201cYour file indicates\ndifficulty accepting accountability.\u201d", "f": "playfair", "s": 66, "c": "GOLD"}]},
"ep5_lines.png": {"blocks": [
    {"text": "Fixation on perceived mistreatment.\nDifficulty accepting accountability.\nOppositional behavior.", "f": "mont", "s": 46, "w": "Medium", "c": "CREAM"}]},
"ep5_fade.png": {"blocks": [
    {"text": "That isn't what happened.", "f": "playfair", "s": 58, "c": "CREAM"},
    {"text": "I remember.", "f": "playfair", "s": 48, "c": "MUTED"},
    {"text": "I know.", "f": "playfair", "s": 40, "c": "DIMGOLD"}]},
"ep5_easier.png": {"blocks": [
    {"text": "\u201cYou've been much easier lately.\u201d", "f": "script", "s": 74, "c": "GOLD"}]},
"ep5_years.png": {"blocks": [
    {"text": "Years passed.", "f": "playfair", "s": 88, "c": "CREAM"},
    {"text": "The file called it progress.", "f": "mont", "s": 44, "c": "MUTED"}]},
"ep5_part5.png": {"blocks": [
    {"text": "PART 5", "f": "mont", "s": 60, "w": "Bold", "c": "GOLD"},
    {"text": "Easier Lately", "f": "script", "s": 105, "c": "CREAM"},
    {"type": "divider"},
    {"text": "FOLLOW FOR THE FINALE", "f": "playfair", "s": 58, "c": "GOLD"},
    {"text": "@shes.the.vibe.co", "f": "mont", "s": 42, "c": "MUTED"}]},
# ---- EPISODE 6: "The Red Marker" (finale) ----
"ep6_hook.png": {"blocks": [
    {"text": "Years later,", "f": "playfair", "s": 72, "c": "GOLD"},
    {"text": "another girl sat\nin another vinyl chair.", "f": "playfair", "s": 72, "c": "CREAM"}]},
"ep6_old.png": {"blocks": [
    {"text": "A pink bed. A red marker.\nA phone that never rang.\nA voice made of paper.", "f": "script", "s": 60, "c": "CREAM"}]},
"ep6_writes.png": {"blocks": [
    {"text": "Then she wrote.", "f": "playfair", "s": 96, "c": "GOLD"}]},
"ep6_end.png": {"cy": 900, "blocks": [
    {"text": "Her words mattered.", "f": "script", "s": 88, "c": "GOLD"},
    {"type": "divider"},
    {"text": "Read the full story \u2014 link in bio", "f": "playfair", "s": 54, "c": "CREAM"},
    {"text": "@shes.the.vibe.co", "f": "mont", "s": 44, "c": "MUTED"},
    {"text": "INSTITUTIONALIZED \u2014 the end", "f": "mont", "s": 36, "c": "DIMGOLD"}]},
# ---- PREQUEL: "The Pink Beds" ----
"ep0_hook.png": {"blocks": [
    {"text": "Before the file.\nBefore the pink bed.", "f": "playfair", "s": 72, "c": "GOLD"},
    {"text": "There was Casa.", "f": "script", "s": 76, "c": "CREAM"}]},
"ep0_twelve.png": {"blocks": [
    {"text": "She was twelve.", "f": "playfair", "s": 88, "c": "GOLD"},
    {"text": "Already certain\nshe had been forgotten.", "f": "playfair", "s": 62, "c": "CREAM"}]},
"ep0_depression.png": {"blocks": [
    {"text": "\u201cA pretty pink bed to match\nthe ugly, crippling depression\nI've got going on inside.\u201d", "f": "playfair", "s": 56, "c": "CREAM"}]},
"ep0_watch.png": {"blocks": [
    {"text": "Watch the series:", "f": "mont", "s": 48, "c": "MUTED"},
    {"text": "INSTITUTIONALIZED", "f": "playfair", "s": 68, "c": "GOLD"},
    {"type": "divider"},
    {"text": "6 parts \u2014 @shes.the.vibe.co", "f": "mont", "s": 44, "c": "CREAM"},
    {"text": "full story \u2014 link in bio", "f": "script", "s": 52, "c": "DIMGOLD"}]},
})

OV_DEF.update({
# ---- EP 5 ----
"ov_ep5_room.png": {"shade": (1100, 1620, 115), "blocks": [
    {"text": "The room was wrong. Off.", "f": "playfair", "s": 66, "c": "CREAM"},
    {"text": "Someone had stolen every bit of color.", "f": "playfair", "s": 56, "c": "MUTED"}]},
"ov_ep5_grows.png": {"shade": (1180, 1580, 110), "blocks": [
    {"text": "By morning,\nthe file was thicker.", "f": "playfair", "s": 64, "c": "CREAM"}]},
"ov_ep5_phone.png": {"shade": (1150, 1600, 110), "blocks": [
    {"text": "The phone still rang in the hallway.", "f": "playfair", "s": 58, "c": "CREAM"},
    {"text": "Once, she had looked up every time.", "f": "mont", "s": 44, "c": "MUTED"}]},
# ---- EP 6 ----
"ov_ep6_girl.png": {"shade": (1150, 1560, 110), "blocks": [
    {"text": "\u201cThat's not what happened.\u201d", "f": "playfair", "s": 68, "c": "GOLD"}]},
"ov_ep6_hand.png": {"shade": (1100, 1640, 112), "blocks": [
    {"text": "Her hand hovered over the paper.", "f": "playfair", "s": 60, "c": "CREAM"},
    {"text": "For one breath,\nshe considered putting the pen down.", "f": "playfair", "s": 56, "c": "MUTED"}]},
"ov_ep6_ping.png": {"shade": (700, 1080, 110), "blocks": [
    {"text": "Ping.", "f": "script", "s": 150, "c": "GOLD"},
    {"text": "Neither of them looked up.", "f": "mont", "s": 44, "c": "CREAM"}]},
"ov_ep6_night.png": {"shade": (1150, 1600, 110), "blocks": [
    {"text": "The white coat hung on the chair.", "f": "playfair", "s": 58, "c": "CREAM"},
    {"text": "The bedding was still pink.", "f": "playfair", "s": 58, "c": "GOLD"}]},
"ov_ep6_marker.png": {"shade": (1150, 1580, 110), "blocks": [
    {"text": "Her eyes opened.", "f": "playfair", "s": 68, "c": "CREAM"},
    {"text": "On the desk sat a red marker.", "f": "playfair", "s": 68, "c": "GOLD"}]},
# ---- PREQUEL ----
"ov_ep0_shelter.png": {"shade": (1150, 1580, 105), "blocks": [
    {"text": "The shelter sat in an industrial\npart of town.", "f": "playfair", "s": 62, "c": "CREAM"}]},
"ov_ep0_pink.png": {"shade": (1100, 1640, 105), "blocks": [
    {"text": "Every girl's bed was dressed\nin bright pink.", "f": "playfair", "s": 60, "c": "GOLD"},
    {"text": "Every boy's in blue.", "f": "playfair", "s": 60, "c": "CREAM"}]},
"ov_ep0_thread.png": {"shade": (1180, 1580, 105), "blocks": [
    {"text": "The pink bed is where\nthe story begins.", "f": "script", "s": 72, "c": "GOLD"}]},
})

# ================= ASSEMBLY =================
def asset(name):
    matches = glob.glob(os.path.join(ASSETS, f"*{name}*.mp4"))
    if not matches:
        raise SystemExit(f"asset not found: {name}")
    return matches[0]

GRADES = {
    "light": "eq=brightness=-0.06:saturation=0.85,noise=alls=5:allf=t",
    "warm": "eq=brightness=-0.02:saturation=1.08,noise=alls=5:allf=t",
    "cold": "eq=brightness=-0.09:saturation=0.55,noise=alls=6:allf=t",
}

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-2500:])
        raise SystemExit("ffmpeg failed: " + " ".join(cmd[:4]))
    return r

def seg_card(card, dur, out, zoom_in):
    frames = int(dur * FPS); zf = 0.06
    z = (f"zoompan=z='1+{zf}*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={FPS}"
         if zoom_in else
         f"zoompan=z='1+{zf}-{zf}*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={FPS}")
    run(["ffmpeg", "-y", "-loop", "1", "-i", os.path.join(CARDS, card),
         "-vf", f"scale=2160:3840,{z}",
         "-t", str(dur), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS), out])

def seg_clip(clip, start, dur, overlay_png, grade, out):
    ov = os.path.join(OV, overlay_png)
    vf = (f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,"
          f"fps={FPS},{grade},format=yuv420p[bg];"
          f"movie={ov},scale=1080:1920,format=yuva420p[fg];"
          f"[bg][fg]overlay=0:0:format=yuv420")
    run(["ffmpeg", "-y", "-ss", str(start), "-t", str(dur), "-i", clip,
         "-vf", vf, "-t", str(dur),
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS), out])

def xfade_chain(segs, out):
    n = len(segs)
    inputs = []
    for s in segs: inputs += ["-i", s]
    durs = []
    for s in segs:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "default=noprint_wrappers=1:nokey=1", s],
                           capture_output=True, text=True)
        durs.append(float(r.stdout.strip()))
    fc, offset, last = [], 0.0, "[0:v]"
    for i in range(n - 1):
        offset += durs[i] - TRANS
        nxt = f"[x{i}]"
        fc.append(f"{last}[{i+1}:v]xfade=transition=fade:duration={TRANS}:offset={offset:.3f}{nxt}")
        last = nxt
    total = sum(durs) - TRANS * (n - 1)
    run(["ffmpeg", "-y"] + inputs + ["-filter_complex", ";".join(fc),
         "-map", last, "-t", f"{total:.3f}",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS), out])
    return total

# Segment tuple: ("card", name, dur) or ("clip", asset_stem, start, dur, overlay, grade)
EPISODES = {
"episode-02.mp4": [
    ("card", "ep2_hook.png", 3.0),
    ("clip", "series-ep1-photo", 2.0, 4.0, "ov_ep2_photo.png", "light"),
    ("card", "ep2_salad.png", 3.5),
    ("card", "ep2_notshown.png", 3.0),
    ("clip", "series-ep2-red-marker", 0, 4.5, "ov_ep2_marker.png", "light"),
    ("card", "ep2_bullshit.png", 3.5),
    ("clip", "series-ep1-room", 1.0, 3.5, "ov_ep2_gone.png", "light"),
    ("card", "ep2_part2.png", 4.5)],
"episode-03.mp4": [
    ("card", "ep3_hook.png", 3.0),
    ("clip", "series-ep3-file-desk", 0, 4.5, "ov_ep3_file.png", "light"),
    ("card", "ep3_no.png", 3.5),
    ("card", "ep3_voice1.png", 4.0),
    ("card", "ep3_voice2.png", 4.0),
    ("clip", "series-ep1-hallway", 1.0, 4.0, "ov_ep3_door.png", "light"),
    ("card", "ep3_ready.png", 3.0),
    ("card", "ep3_part3.png", 4.5)],
"episode-04.mp4": [
    ("card", "ep4_hook.png", 3.0),
    ("clip", "series-ep4-notebook", 0, 5.0, "ov_ep4_writing.png", "warm"),
    ("card", "ep4_truth.png", 3.5),
    ("clip", "series-ep1-photo", 6.0, 4.0, "ov_ep4_shift.png", "warm"),
    ("clip", "series-ep2-red-marker", 3.0, 3.5, "ov_ep4_pillow.png", "warm"),
    ("card", "ep4_smile.png", 4.0),
    ("card", "ep4_clinician.png", 3.5),
    ("card", "ep4_part4.png", 4.5)],
"episode-05.mp4": [
    ("card", "ep5_hook.png", 3.0),
    ("clip", "series-ep5-cold-room", 0, 4.5, "ov_ep5_room.png", "cold"),
    ("card", "ep5_account.png", 3.5),
    ("clip", "series-ep3-file-desk", 3.0, 4.0, "ov_ep5_grows.png", "cold"),
    ("card", "ep5_lines.png", 4.0),
    ("card", "ep5_fade.png", 4.5),
    ("card", "ep5_easier.png", 3.5),
    ("clip", "series-ep1-hallway", 4.0, 3.5, "ov_ep5_phone.png", "cold"),
    ("card", "ep5_years.png", 3.0),
    ("card", "ep5_part5.png", 4.5)],
"episode-06.mp4": [
    ("card", "ep6_hook.png", 3.0),
    ("clip", "series-ep6-vinyl-chair", 0, 4.5, "ov_ep6_girl.png", "light"),
    ("card", "ep6_old.png", 3.5),
    ("clip", "series-ep3-file-desk", 5.0, 4.0, "ov_ep6_hand.png", "light"),
    ("card", "ep6_writes.png", 3.0),
    ("clip", "series-ep1-photo", 7.0, 3.0, "ov_ep6_ping.png", "light"),
    ("clip", "series-ep1-room", 2.0, 4.0, "ov_ep6_night.png", "light"),
    ("clip", "series-ep2-red-marker", 4.0, 4.0, "ov_ep6_marker.png", "light"),
    ("card", "ep6_end.png", 5.5)],
"episode-00-prequel.mp4": [
    ("card", "ep0_hook.png", 3.0),
    ("clip", "series-ep0-pink-beds", 0, 5.0, "ov_ep0_shelter.png", "warm"),
    ("card", "ep0_twelve.png", 3.5),
    ("clip", "series-ep1-girl-ceiling", 1.0, 4.0, "ov_ep0_pink.png", "warm"),
    ("card", "ep0_depression.png", 4.0),
    ("clip", "series-ep0-pink-beds", 5.0, 4.0, "ov_ep0_thread.png", "warm"),
    ("card", "ep0_watch.png", 4.5)],
}

def build_episode(outfile, segments):
    segs, counter = [], [0]
    def nxt(kind, *a):
        p = os.path.join(BASE, f"_seg_{outfile.replace('.mp4','')}_{counter[0]}.mp4")
        counter[0] += 1
        if kind == "card":
            seg_card(a[0], a[1], p, zoom_in=(counter[0] % 2 == 1))
        else:
            seg_clip(asset(a[0]), a[1], a[2], a[3], GRADES[a[4]], p)
        segs.append(p)
    for s in segments:
        nxt(s[0], *s[1:])
    out = os.path.join(BASE, outfile)
    total = xfade_chain(segs, out)
    for f in segs: os.remove(f)
    print(f"{outfile}: {total:.1f}s DONE")
    return total

if __name__ == "__main__":
    import sys
    only = sys.argv[1:] or list(EPISODES.keys())
    for name, card in CARDS_DEF.items():
        if not os.path.exists(os.path.join(CARDS, name)):
            draw_card(name, card)
    for name, ov in OV_DEF.items():
        if not os.path.exists(os.path.join(OV, name)):
            draw_overlay(name, ov)
    for outfile in only:
        build_episode(outfile, EPISODES[outfile])
    print("ALL DONE")
