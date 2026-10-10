#!/usr/bin/env python3
"""Assemble TikTok videos from slide PNGs: Ken Burns zoom + crossfade transitions."""
import subprocess, os

S = os.path.expanduser("~/workspace/shes-the-vibe/tiktok/slides")
OUT = os.path.expanduser("~/workspace/shes-the-vibe/tiktok")
FPS = 30
FADE = 0.6

def build(name, slides):
    """slides: list of (filename, duration_sec)."""
    inputs, filters = [], []
    for i, (fn, dur) in enumerate(slides):
        inputs += ["-loop", "1", "-t", str(dur), "-i", os.path.join(S, fn)]
        frames = int(dur * FPS)
        filters.append(
            f"[{i}:v]scale=1350:2400,"
            f"zoompan=z='1+0.07*on/{frames}':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps={FPS},"
            f"format=yuv420p[v{i}]"
        )
    # xfade chain
    chain, acc, total = "[v0]", 0.0, 0.0
    for i in range(1, len(slides)):
        total += slides[i - 1][1]
        offset = total - i * FADE
        out = f"[x{i}]" if i < len(slides) - 1 else "[vout]"
        filters.append(f"{chain}[v{i}]xfade=transition=fade:duration={FADE}:offset={offset:.3f}{out}")
        chain = out
    # gentle fade in from black at start, fade out at end
    dur_total = total + slides[-1][1] - (len(slides) - 1) * FADE
    filters.append(f"[vout]fade=t=in:st=0:d=0.5,fade=t=out:st={dur_total-0.8:.2f}:d=0.8,format=yuv420p[vfinal]")
    out_path = os.path.join(OUT, name)
    cmd = (["ffmpeg", "-y"] + inputs +
           ["-filter_complex", ";".join(filters),
            "-map", "[vfinal]", "-c:v", "libx264", "-preset", "veryfast",
            "-crf", "22", "-movflags", "+faststart", out_path])
    print("building", name)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:])
        raise SystemExit(f"ffmpeg failed for {name}")
    print("done", out_path, f"({dur_total:.1f}s)")

# Video 2: 3 Journal Prompts for When You Feel Stuck (~35s)
build("tiktok-3-journal-prompts.mp4", [
    ("v2_hook.png", 4),
    ("v2_p1.png", 7),
    ("v2_p2.png", 7),
    ("v2_p3.png", 7),
    ("v2_final.png", 9),
])

# Video 7: What 'Practical. Pretty. You.' Actually Means (~35s)
build("tiktok-brand-manifesto.mp4", [
    ("v7_hook.png", 4),
    ("v7_practical.png", 7),
    ("v7_pretty.png", 7),
    ("v7_you.png", 7),
    ("v7_final.png", 9),
])

# Priority 2: Vibe Dashboard teaser (~24s)
build("tiktok-dashboard-teaser.mp4", [
    ("vd_hook.png", 5),
    ("vd_features.png", 6),
    ("vd_product.png", 6),
    ("vd_cta.png", 7),
])

print("ALL VIDEOS DONE")
