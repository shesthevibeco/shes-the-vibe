#!/usr/bin/env python3
"""Assemble INSTITUTIONALIZED series Episode 1: dark cinematic storytelling."""
import os, subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
CARDS = os.path.join(BASE, "cards")
OV = os.path.join(BASE, "overlays")
ASSETS = os.path.join(BASE, "assets")
ANIM = "/home/hatch/workspace/shes-the-vibe/tiktok/animated"
FPS = 30
W, H = 1080, 1920
TRANS = 0.8  # slow cinematic fades

ROOM = os.path.join(ASSETS, "media-generation-series-ep1-room-0-f20b8202-c0ca-4be4-bda7-c6a759189249.mp4")
PHOTO = os.path.join(ASSETS, "media-generation-series-ep1-photo-0-7b4968ae-0f3d-4ab0-b32c-a456d27edb72.mp4")
JOURNAL = os.path.join(ANIM, "media-generation-stv-girl-journal-0-8769ffa2-4d0a-4bcd-a40e-fc8f12592359.mp4")
INTRO = os.path.join(ANIM, "media-generation-stv-girl-intro-0-178159df-4f71-4fb2-be6d-fd68c791a985.mp4")

GRADE_LIGHT = "eq=brightness=-0.06:saturation=0.85,noise=alls=5:allf=t"
GRADE_HEAVY = "eq=brightness=-0.30:saturation=0.50,noise=alls=6:allf=t"

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-2500:])
        raise SystemExit("ffmpeg failed: " + " ".join(cmd[:4]))
    return r

def seg_card(card, dur, out, zoom_in=True):
    frames = int(dur * FPS)
    zf = 0.06
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
    for s in segs:
        inputs += ["-i", s]
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

if __name__ == "__main__":
    segs = []
    def add(path): segs.append(path); return path
    counter = [0]
    def nxt(kind, *a):
        p = os.path.join(BASE, f"_seg_ep1_{counter[0]}.mp4"); counter[0] += 1
        if kind == "card": seg_card(*a, p, zoom_in=(counter[0] % 2 == 1))
        else: seg_clip(*a, p)
        return add(p)

    nxt("card", "s1_hook.png", 3.0)
    nxt("clip", ROOM, 0, 5.0, "ov_bang.png", GRADE_LIGHT)
    nxt("card", "s1_room.png", 3.5)
    nxt("card", "s1_rules.png", 3.5)
    nxt("clip", JOURNAL, 0, 4.0, "ov_therapy.png", GRADE_HEAVY)
    nxt("card", "s1_out.png", 3.5)
    nxt("clip", INTRO, 0, 4.0, "ov_teeth.png", GRADE_HEAVY)
    nxt("clip", PHOTO, 0, 3.5, "ov_ping.png", GRADE_LIGHT)
    nxt("clip", PHOTO, 4.0, 5.0, "ov_photo.png", GRADE_LIGHT)
    nxt("card", "s1_part1.png", 4.5)

    total = xfade_chain(segs, os.path.join(BASE, "episode-01.mp4"))
    for f in segs: os.remove(f)
    print(f"episode-01.mp4: {total:.1f}s DONE")
