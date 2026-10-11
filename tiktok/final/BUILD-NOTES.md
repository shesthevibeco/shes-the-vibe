# TikTok Final Videos — Build Notes (2026-10-10)

Rebuilt from scratch after Christina rejected the previous versions as "basic and sloooow" with "too basic" transitions. New direction: cute-luxe, art-forward, animated brand girl, fast visual variety.

## Source assets
- Animated girl clips: `../animated/media-generation-stv-girl-{intro,journal,planner}-0-*.mp4` (944×960, 24fps, 10s each)
- Brand illustration: `../../brand-illustration.png` → circular crop `assets/brand-circle.png`
- Fonts (downloaded from Google Fonts): Parisienne (script), Montserrat VF (sans), Playfair Display VF (serif)
- Card generator: `assets/gen_cards.py` (PIL) → 19 PNG cards at `assets/cards/`
- Assembler: `assemble.py` (ffmpeg)

## Build pipeline
1. PIL renders 1080×1920 text cards: burgundy (#451425) / cream (#F7E7CE) backgrounds, champagne gold (#C9A96E) frames + sparkles + flourishes, script/sans/serif type hierarchy.
2. Each card → segment via `zoompan` (subtle Ken Burns push-in/out, alternating).
3. Hook segments get the animated girl clip overlaid in a gold-bordered frame (700px wide, lower third so headline text stays clear).
4. v1 brand card gets the circular brand illustration (alpha-preserved overlay).
5. Segments joined with `xfade` (0.4s): slideleft/slideright (whip pans), circleopen/radial (scale pops), smoothup. No slow crossfades.

## Videos

### 1. tiktok-manifesto-final.mp4 (15.6s, 1080×1920, 30fps, H.264/yuv420p)
- 0.0–2.5s HOOK: "STOP SCROLLING" (gold Playfair) + "3 words changed my life" (script) + intro girl clip in gold frame
- 2.5–5.0s "PRACTICAL" + "pretty is pointless if it doesn't work"
- 5.0–7.5s "PRETTY" + "beautiful things get USED"
- 7.5–10.0s "YOU" + "never about fitting a box"
- 10.0–13.0s Brand card: "She's The Vibe" script + circular brand illustration + @shes.the.vibe.co + "Practical. Pretty. You."
- 13.0–15.6s Pillars: PLANNERS ✦ JOURNALS ✦ JEWELRY → CTA "FOLLOW FOR THE VIBE" + shesthevibe.co
- Suggested audio: trending bold/confident sound. Caption: STOP SCROLLING 👑 3 words that changed my life #brandstory #womenownedbusiness #smallbusiness #shesthevibe

### 2. tiktok-journal-prompts-final.mp4 (16.0s)
- 0.0–2.5s HOOK: "FEELING STUCK?" + "write this down" (script) + journal girl clip in gold frame
- 2.5–6.0s Prompt 1: "What am I pretending not to know?"
- 6.0–9.5s Prompt 2: "What would I do if I trusted myself?"
- 9.5–13.0s Prompt 3: "Who am I becoming?"
- 13.0–15.0s Product: "the HEALING VIBE JOURNAL" + "50 more prompts inside" + "SAVE THIS POST"
- 15.0–16.0s CTA: "SAVE THIS" + "your future self says thanks" + @shes.the.vibe.co
- Suggested audio: trending soft audio. Caption: feeling stuck? write this down 🤍✨ #journalprompts #shadowwork #selfdiscovery #journaling #healingjourney #shesthevibe

### 3. tiktok-dashboard-final.mp4 (12.6s)
- 0.0–2.5s HOOK: "POV: YOUR WHOLE LIFE on ONE spreadsheet" + planner girl clip in gold frame
- 2.5–4.0s "BUDGET ✓" · 4.0–5.5s "HABITS ✓" · 5.5–7.0s "GOALS ✓" · 7.0–8.5s "BILLS ✓" (rapid checkmark flashes)
- 8.5–11.5s Product: "the spreadsheet that runs my life" + "THE VIBE DASHBOARD" + "$37"
- 11.5–12.6s CTA: "LINK IN BIO" + "get your life together, cutely" + @shes.the.vibe.co
- Suggested audio: trending upbeat/productivity sound. Caption: POV: your whole life fits on ONE spreadsheet 📊✨ #planner #budgetplanner #organization #smallbusiness #shesthevibe

## Notes
- No audio baked in — add trending sounds in the TikTok app at post time.
- TikTok auto-captions OFF (all text baked in).
- Post order 1 → 2 → 3, spaced hours apart or one per day.
- Link in bio → https://shesthevibe.co/links.html (pending verification).
- **Do NOT post without Christina's preview + approval.**
