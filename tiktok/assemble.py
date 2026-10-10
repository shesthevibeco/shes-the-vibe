#!/usr/bin/env python3
"""Assemble TikTok videos from slide PNGs.

TikTok-native pacing: HARD CUTS (concat, no crossfades), subtle Ken Burns
push-in per clip for motion energy, quick fade in/out at the ends only.
"""
import subprocess, os

S = os.path.expanduser("~/workspace/shes-the-vibe/tiktok/slides")
OUT = os.path.expanduser("~/workspace/shes-the-vibe/tiktok")
FPS = 30

def build(name, slides):
    """slides: list of (filename, duration_sec)."""
    inputs, filters = [], []
    for i, (fn, dur) in enumerate(slides):
        frames = max(2, int(round(dur * FPS)))
        inputs += ["-loop", "1", "-t", str(dur), "-i", os.path.join(S, fn)]
        # upscale then gentle push-in zoom so every cut feels alive
        filters.append(
            f"[{i}:v]scale=1080:1920,"
            f"zoompan=z='1+0.10*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
            f":d={frames}:s=1080x1920:fps={FPS},format=yuv420p[v{i}]"
        )
    n = len(slides)
    vlabels = "".join(f"[v{i}]" for i in range(n))
    dur_total = sum(d for _, d in slides)
    filters.append(
        f"{vlabels}concat=n={n}:v=1:a=0,"
        f"fade=t=in:st=0:d=0.3,fade=t=out:st={dur_total-0.5:.2f}:d=0.5,"
        f"format=yuv420p[vout]"
    )
    out_path = os.path.join(OUT, name)
    cmd = (["ffmpeg", "-y"] + inputs +
           ["-filter_complex", ";".join(filters),
            "-map", "[vout]", "-c:v", "libx264", "-preset", "veryfast",
            "-crf", "22", "-movflags", "+faststart", out_path])
    print("building", name)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:])
        raise SystemExit(f"ffmpeg failed for {name}")
    print("done", out_path, f"({dur_total:.1f}s)")

# Video 1: Brand Manifesto (~16.5s) — STOP SCROLLING hook, rapid-fire cards
build("tiktok-brand-manifesto.mp4", [
    ("v7_hook.png", 3.0),
    ("v7_practical.png", 2.5),
    ("v7_pretty.png", 2.5),
    ("v7_you.png", 2.5),
    ("v7_final.png", 3.0),
    ("v7_cta.png", 3.0),
])

# Video 2: 3 Journal Prompts (~17.5s) — hook, 3 fast prompts, product, CTA
build("tiktok-3-journal-prompts.mp4", [
    ("v2_hook.png", 2.5),
    ("v2_p1.png", 3.0),
    ("v2_p2.png", 3.0),
    ("v2_p3.png", 3.0),
    ("v2_final.png", 3.5),
    ("v2_cta.png", 2.5),
])

# Video 3: Vibe Dashboard teaser (~14.5s) — POV hook, rapid feature flashes
build("tiktok-dashboard-teaser.mp4", [
    ("vd_hook.png", 2.5),
    ("vd_f1.png", 1.5),
    ("vd_f2.png", 1.5),
    ("vd_f3.png", 1.5),
    ("vd_f4.png", 1.5),
    ("vd_product.png", 3.0),
    ("vd_cta.png", 3.0),
])

print("ALL VIDEOS DONE")
