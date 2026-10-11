#!/usr/bin/env python3
"""Assemble STV TikTok videos: cards + animated girl overlays + xfade transitions."""
import os, subprocess, math

BASE = os.path.dirname(os.path.abspath(__file__))
CARDS = os.path.join(BASE, "assets", "cards")
ANIM = "/home/hatch/workspace/shes-the-vibe/tiktok/animated"
BRAND = "/home/hatch/workspace/shes-the-vibe/tiktok/final/assets/brand-circle.png"
OUT = BASE
FPS = 30
W, H = 1080, 1920
TRANS = 0.4  # transition duration

def run(cmd, **kw):
    print(" ".join(cmd[:6]), "...")
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        print(r.stderr[-2000:])
        raise SystemExit("ffmpeg failed")
    return r

def seg_from_card(card, dur, out, zoom_dir=1):
    """Card -> segment mp4 with subtle zoompan motion."""
    frames = int(dur * FPS)
    # zoompan needs larger input; scale up first
    if zoom_dir > 0:
        z = f"zoompan=z='1+0.12*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={FPS}"
    else:
        z = f"zoompan=z='1.12-0.12*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={FPS}"
    run(["ffmpeg", "-y", "-loop", "1", "-i", card,
         "-vf", f"scale=2160:3840,{z}",
         "-t", str(dur), "-c:v", "libx264", "-pix_fmt", "yuv420p",
         "-r", str(FPS), out])

def seg_with_girl(card, girl_mp4, dur, out, gx=160, gy=1080, gw=700):
    """Card + animated girl clip overlay in gold frame."""
    base = out + ".base.mp4"
    seg_from_card(card, dur, base)
    # preprocess girl: scale (even dims), trim, fps
    girl = out + ".girl.mp4"
    run(["ffmpeg", "-y", "-i", girl_mp4,
         "-vf", f"scale={gw}:-2,fps={FPS},format=yuv420p",
         "-t", str(dur), "-c:v", "libx264", "-pix_fmt", "yuv420p",
         "-r", str(FPS), girl])
    # probe actual girl height for drawbox
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "stream=height", "-of", "default=noprint_wrappers=1:nokey=1", girl],
                       capture_output=True, text=True)
    gh = int(r.stdout.strip())
    run(["ffmpeg", "-y", "-i", base, "-i", girl,
         "-filter_complex",
         f"[0:v][1:v]overlay={gx}:{gy},drawbox=x={gx}:y={gy}:w={gw}:h={gh}:color=0xC9A96E:t=6[vid]",
         "-map", "[vid]", "-t", str(dur), "-c:v", "libx264", "-pix_fmt", "yuv420p",
         "-r", str(FPS), out])
    os.remove(base); os.remove(girl)

def seg_with_brand_illustration(card, dur, out):
    """Brand card + circular brand illustration overlay."""
    base = out + ".base.mp4"
    seg_from_card(card, dur, base)
    # illustration: 520x520 centered at (540, 820) -> x=280, y=560
    run(["ffmpeg", "-y", "-i", base, "-i", BRAND,
         "-filter_complex",
         "[1:v]scale=520:520,fps=30,format=yuva420p[ill];"
         "[0:v]format=yuv420p[bg];"
         "[bg][ill]overlay=280:560:format=yuv420[vid]",
         "-map", "[vid]", "-t", str(dur), "-c:v", "libx264", "-pix_fmt", "yuv420p",
         "-r", str(FPS), out])
    os.remove(base)

def xfade_chain(segs, transitions, out):
    """Chain segments with xfade. transitions[i] between segs[i] and segs[i+1]."""
    n = len(segs)
    assert len(transitions) == n - 1
    inputs = []
    for s in segs:
        inputs += ["-i", s]
    # compute durations via ffprobe
    durs = []
    for s in segs:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                            "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", s],
                           capture_output=True, text=True)
        durs.append(float(r.stdout.strip()))
    fc = []
    offset = 0
    last = "[0:v]"
    for i in range(n - 1):
        offset += durs[i] - TRANS
        nxt = f"[x{i}]"
        fc.append(f"{last}[{i+1}:v]xfade=transition={transitions[i]}:duration={TRANS}:offset={offset:.3f}{nxt}")
        last = nxt
    total = sum(durs) - TRANS * (n - 1)
    run(["ffmpeg", "-y"] + inputs +
        ["-filter_complex", ";".join(fc),
         "-map", last, "-t", f"{total:.3f}",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS), out])
    return total

def build(name, segments, transitions, outname):
    """segments: list of (kind, args). kind in card/girl/brand."""
    seg_files = []
    for i, s in enumerate(segments):
        kind = s[0]
        out = os.path.join(OUT, f"_seg_{name}_{i}.mp4")
        if kind == "card":
            _, card, dur = s
            seg_from_card(os.path.join(CARDS, card), dur, out, zoom_dir=1 if i % 2 == 0 else -1)
        elif kind == "girl":
            _, card, girlfile, dur = s
            seg_with_girl(os.path.join(CARDS, card),
                          os.path.join(ANIM, girlfile), dur, out)
        elif kind == "brand":
            _, card, dur = s
            seg_with_brand_illustration(os.path.join(CARDS, card), dur, out)
        seg_files.append(out)
    total = xfade_chain(seg_files, transitions, os.path.join(OUT, outname))
    for f in seg_files:
        os.remove(f)
    print(f"{outname}: {total:.1f}s DONE")

INTRO = "media-generation-stv-girl-intro-0-178159df-4f71-4fb2-be6d-fd68c791a985.mp4"
JOURNAL = "media-generation-stv-girl-journal-0-8769ffa2-4d0a-4bcd-a40e-fc8f12592359.mp4"
PLANNER = "media-generation-stv-girl-planner-0-8495536b-817e-4acf-9fd4-65b191ea1672.mp4"

if __name__ == "__main__":
    import sys
    which = sys.argv[1] if len(sys.argv) > 1 else "all"

    if which in ("all", "v1"):
        build("v1", [
            ("girl", "v1_hook.png", INTRO, 2.5),
            ("card", "v1_practical.png", 2.5),
            ("card", "v1_pretty.png", 2.5),
            ("card", "v1_you.png", 2.5),
            ("brand", "v1_brand.png", 3.0),
            ("card", "v1_pillars.png", 2.5),
            ("card", "v1_cta.png", 2.5),
        ], ["slideleft", "circleopen", "slideright", "radial", "circleopen", "smoothup"],
        "tiktok-manifesto-final.mp4")

    if which in ("all", "v2"):
        build("v2", [
            ("girl", "v2_hook.png", JOURNAL, 2.5),
            ("card", "v2_p1.png", 3.5),
            ("card", "v2_p2.png", 3.5),
            ("card", "v2_p3.png", 3.5),
            ("card", "v2_product.png", 2.5),
            ("card", "v2_cta.png", 2.5),
        ], ["slideleft", "circleopen", "slideright", "radial", "smoothup"],
        "tiktok-journal-prompts-final.mp4")

    if which in ("all", "v3"):
        build("v3", [
            ("girl", "v3_hook.png", PLANNER, 2.5),
            ("card", "v3_budget.png", 1.5),
            ("card", "v3_habits.png", 1.5),
            ("card", "v3_goals.png", 1.5),
            ("card", "v3_bills.png", 1.5),
            ("card", "v3_product.png", 3.5),
            ("card", "v3_cta.png", 3.0),
        ], ["slideleft", "circleopen", "circleopen", "circleopen", "radial", "smoothup"],
        "tiktok-dashboard-final.mp4")
    print("ALL VIDEOS DONE")
