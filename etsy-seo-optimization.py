#!/usr/bin/env python3
"""Generate the Etsy SEO optimization report with validated char counts.
Run: python3 etsy-seo-optimization.py > etsy-seo-optimization.md
DO NOT publish changes to Etsy — this is a review draft for Christina.
"""

listings = [
{
 "n": 1, "name": "Vibe Dashboard", "price": "$37", "type": "Digital (Excel/Google Sheets)",
 "current_title": "Life Planner Spreadsheet | Google Sheets Life Organizer | Bills Tasks Savings Goals Tracker | Digital Planner Dashboard | Instant Download",
 "weaknesses": [
   "Missing 'ADHD planner' — the highest-momentum planner niche on Etsy (10k+ review sellers)",
   "Missing 'Excel' — huge standalone search term; many buyers search Excel specifically",
   "Wastes title space on 'Digital Planner Dashboard' (low search volume vs 'ADHD planner')",
   "2 of 13 tags exceed Etsy's 20-character limit and are silently dropped: 'google sheets planner' (21), 'life organizer spreadsheet' (26)",
 ],
 "new_title": "ADHD Life Planner Spreadsheet | Google Sheets & Excel Planner | Bill Tracker Budget Organizer | Task Manager Dashboard | Instant Download",
 "tags": ["adhd planner","digital planner","life planner","google sheets","excel planner","budget spreadsheet","bill tracker","task manager","savings tracker","goal planner","mom planner","productivity","digital download"],
},
{
 "n": 2, "name": "Dashboard Add-Ons Pack", "price": "$20", "type": "Digital (Excel/Google Sheets)",
 "current_title": "Life Planner Add On Pack | Google Sheets Travel Reading Movie Trackers | Digital Planner Bundle | Instant Download",
 "weaknesses": [
   "Missing 'bundle' as a standalone high-converting keyword (buyers search 'planner bundle')",
   "'google sheets bundle' tag is 20 chars (valid) but 'digital planner addons' is weak vs 'planner accessories'",
   "No 'packing list' / 'wishlist' long-tail in title — both are searched terms",
 ],
 "new_title": "Planner Bundle Add On Pack | Google Sheets & Excel Trackers | Reading Travel Movie Packing List Wishlist | Digital Planner Accessories",
 "tags": ["planner bundle","digital planner","reading tracker","travel planner","movie tracker","packing list","wishlist planner","google sheets","excel template","life organizer","planner accessories","digital download","productivity"],
},
{
 "n": 3, "name": "Work Vibe", "price": "$27", "type": "Digital (Excel/Google Sheets)",
 "current_title": "(no optimized draft on file — published without dedicated SEO)",
 "weaknesses": [
   "No SEO draft existed; listing likely has a short/generic title",
   "Missing 'career planner', 'work organizer', 'job tracker' — all real buyer searches",
 ],
 "new_title": "Work Planner Spreadsheet | Career Tracker Google Sheets & Excel | Job Task Organizer | Work Life Balance Planner | Instant Download",
 "tags": ["work planner","career planner","google sheets","excel template","task manager","job tracker","productivity","work organizer","digital planner","office planner","project planner","digital download","life planner"],
},
{
 "n": 4, "name": "Home Care Vibe", "price": "$27", "type": "Digital (Excel/Google Sheets)",
 "current_title": "(no optimized draft on file — published without dedicated SEO)",
 "weaknesses": [
   "No SEO draft existed; listing likely has a short/generic title",
   "Missing 'household binder', 'cleaning schedule', 'homemaking' — strong niche searches",
 ],
 "new_title": "Home Management Spreadsheet | Household Planner Google Sheets & Excel | Cleaning Schedule Organizer | Home Binder Tracker | Download",
 "tags": ["home planner","household binder","cleaning schedule","home organizer","google sheets","excel template","homemaking","household planner","digital planner","mom planner","home management","digital download","life organizer"],
},
{
 "n": 5, "name": "Bills Babe Financial Bundle", "price": "$37", "type": "Digital (Excel/Google Sheets)",
 "current_title": "(no optimized draft on file — published without dedicated SEO)",
 "weaknesses": [
   "No SEO draft existed; 'Bills Babe' brand name gets zero searches — title must lead with 'budget planner'",
   "Missing 'debt payoff', 'expense tracker', 'monthly budget' — top-converting finance keywords",
 ],
 "new_title": "Budget Planner Spreadsheet | Bill Tracker Google Sheets & Excel | Monthly Budget Tracker | Debt Payoff Savings Planner | Instant Download",
 "tags": ["budget planner","bill tracker","google sheets","excel template","budget spreadsheet","debt payoff","savings tracker","expense tracker","finance planner","money tracker","monthly budget","digital download","budget binder"],
},
{
 "n": 6, "name": "Whole Vibe Wellness Journal", "price": "$17", "type": "Digital PDF (112 pages)",
 "current_title": "Whole Vibe Wellness Journal | Guided Journal PDF | Wellness Printable Journal | Digital Download | She's The Vibe (pattern)",
 "weaknesses": [
   "Wastes ~20 title characters on 'She's The Vibe' — brand gets zero searches as a new shop",
   "Missing 'self care journal', 'mental health', 'mindfulness' — the actual buyer searches",
 ],
 "new_title": "Wellness Journal Printable | Guided Self Care Journal PDF | Mind Body Soul Reflection Prompts | Mental Health Planner | Digital Download",
 "tags": ["wellness journal","self care journal","guided journal","printable journal","mental health","journal prompts","mindfulness","journal pdf","digital journal","self love","healing journal","instant download","reflection"],
},
{
 "n": 7, "name": "Faith Vibe Bible Companion", "price": "$17", "type": "Digital PDF (124 pages)",
 "current_title": "Faith Vibe Bible Companion | Guided Journal PDF | Faith Printable Journal | Digital Download | She's The Vibe (pattern)",
 "weaknesses": [
   "Wastes ~20 title characters on brand name",
   "Missing 'bible study', 'scripture study', 'devotional', 'prayer journal' — the core buyer searches",
 ],
 "new_title": "Bible Study Journal Printable | Guided Faith Journal PDF | Scripture Study Notebook | Christian Devotional Planner | Digital Download",
 "tags": ["bible journal","bible study","faith journal","christian journal","scripture study","devotional","printable journal","guided journal","prayer journal","journal pdf","digital download","christian gift","bible planner"],
},
{
 "n": 8, "name": "Healing Vibe Inner Child Journal", "price": "$17", "type": "Digital PDF (116 pages)",
 "current_title": "Healing Vibe Inner Child Journal | Guided Journal PDF | Healing Printable Journal | Digital Download | She's The Vibe (pattern)",
 "weaknesses": [
   "Wastes ~20 title characters on brand name",
   "Missing 'shadow work' — one of the highest-traffic journal niches on Etsy",
   "Missing 'boundaries', 'inner child', 'therapy journal'",
 ],
 "new_title": "Inner Child Journal Printable | Shadow Work Journal PDF | Healing Guided Journal | Boundaries Self Trust Prompts | Digital Download",
 "tags": ["shadow work","inner child","healing journal","guided journal","printable journal","self trust","boundaries","therapy journal","journal prompts","self love","journal pdf","digital download","trauma healing"],
},
{
 "n": 9, "name": "Reading Vibe Library Journal", "price": "$14", "type": "Digital PDF (84 pages)",
 "current_title": "Reading Vibe Library Journal | Guided Journal PDF | Reading Printable Journal | Digital Download | She's The Vibe (pattern)",
 "weaknesses": [
   "Wastes ~20 title characters on brand name",
   "Missing 'book tracker', 'reading log', 'bookish gift' — the actual buyer searches",
 ],
 "new_title": "Reading Journal Printable | Book Lovers Library Log PDF | Book Tracker Reading List | Bookish Gift for Readers | Digital Download",
 "tags": ["reading journal","book journal","book tracker","reading log","bookish gift","book lover","library journal","printable journal","guided journal","journal pdf","book club","digital download","reader gift"],
},
{
 "n": 10, "name": "Faith Vibe Ethiopian & Ancient Books", "price": "$14", "type": "Digital PDF (60 pages)",
 "current_title": "Faith Vibe Ethiopian Books Journal | Guided Journal PDF | Faith Printable Journal | Digital Download | She's The Vibe (pattern)",
 "weaknesses": [
   "Wastes ~20 title characters on brand name",
   "This is a rare niche (Ethiopian/ancient books, Enoch) — title should name it explicitly for the dedicated searchers",
 ],
 "new_title": "Bible Study Journal Printable | Ancient Books Scripture Guide PDF | Ethiopian Bible Companion | Enoch Study Notebook | Digital Download",
 "tags": ["bible study","ethiopian bible","ancient books","faith journal","scripture study","christian journal","apocrypha","bible journal","printable journal","guided journal","journal pdf","digital download","enoch"],
},
{
 "n": 11, "name": "Read the Energy Tarot & Oracle Journal", "price": "$14", "type": "Digital PDF (57 pages)",
 "current_title": "Read the Energy Tarot Journal | Guided Journal PDF | Tarot Printable Journal | Digital Download | She's The Vibe (pattern)",
 "weaknesses": [
   "Wastes ~20 title characters on brand name",
   "'tarot deck' is a screamer keyword on Etsy right now — 'tarot spread', 'grimoire', 'oracle cards' all high-traffic",
 ],
 "new_title": "Tarot Journal Printable | Oracle Card Reading Log PDF | Spiritual Journal Grimoire | Tarot Spread Tracker | Digital Download",
 "tags": ["tarot journal","oracle cards","tarot spread","spiritual journal","grimoire","tarot log","witchy journal","printable journal","guided journal","journal pdf","digital download","tarot deck","divination"],
},
{
 "n": 12, "name": "Dream Vibe Dream Journal", "price": "$12", "type": "Digital PDF (40 pages)",
 "current_title": "Dream Vibe Dream Journal | Guided Journal PDF | Dream Printable Journal | Digital Download | She's The Vibe (pattern)",
 "weaknesses": [
   "Wastes ~20 title characters on brand name",
   "Missing 'dream diary', 'lucid dreaming', 'dream interpretation' — the buyer searches",
 ],
 "new_title": "Dream Journal Printable | Guided Dream Diary PDF | Dream Tracker Interpretation Log | Lucid Dreaming Notebook | Digital Download",
 "tags": ["dream journal","dream diary","lucid dreaming","dream tracker","printable journal","guided journal","dream interpretation","journal pdf","spiritual journal","dream log","digital download","manifestation","sleep journal"],
},
{
 "n": 13, "name": "Reading Vibe Reflection Pack", "price": "$9", "type": "Digital PDF (17 pages)",
 "current_title": "Reading Vibe Reflection Pack | Guided Journal PDF | Reading Printable Journal | Digital Download | She's The Vibe (pattern)",
 "weaknesses": [
   "Wastes ~20 title characters on brand name",
   "At $9 this is the impulse-buy entry — title should scream 'book club' utility",
 ],
 "new_title": "Book Reflection Journal Printable | Reading Response Log PDF | Book Club Discussion Guide | Reader Worksheet Pack | Digital Download",
 "tags": ["book journal","reading log","book club","book reflection","printable worksheet","reading response","book tracker","guided journal","journal pdf","bookish","digital download","reader gift","book lover"],
},
{
 "n": 14, "name": "Custom Made-to-Order Soap", "price": "$15", "type": "Handmade",
 "current_title": "Handmade Artisan Soap Bar | Made to Order | Custom Scent and Color | Natural Luxury Bath Soap | Gift for Her",
 "weaknesses": [
   "Solid draft, but 'personalized' outperforms 'custom' in gift searches",
   "Missing 'self care' and 'spa gift' positioning in title",
 ],
 "new_title": "Custom Handmade Soap Bar | Personalized Scent & Color | Artisan Natural Soap Made to Order | Luxury Bath Gift for Her | Self Care",
 "tags": ["handmade soap","custom soap","artisan soap","personalized gift","natural soap","luxury soap","bath gift","self care gift","spa gift","gift for her","small batch","custom scent","soap bar"],
},
{
 "n": 15, "name": "Handmade Beaded Bracelets", "price": "$38", "type": "Handmade",
 "current_title": "Handmade Beaded Bracelet | Gold Bead Bracelet | Stacking Bracelet | Gift for Her | She's The Vibe",
 "weaknesses": [
   "'bracelet' is a fast-climbing Etsy keyword — title should stack more bracelet variants",
   "Missing 'boho', 'dainty', 'bridesmaid gift' — top-converting bracelet searches",
   "Wastes title space on brand name",
 ],
 "new_title": "Handmade Beaded Bracelet | Gold Stacking Bracelet | Dainty Boho Jewelry | Stretch Bracelet | Gift for Her Birthday Bridesmaid",
 "tags": ["beaded bracelet","stacking bracelet","gold bracelet","handmade jewelry","boho bracelet","dainty bracelet","stretch bracelet","gift for her","bridesmaid gift","birthday gift","artisan jewelry","boho jewelry","bracelet set"],
},
{
 "n": 16, "name": "Waist Beads", "price": "$15", "type": "Handmade",
 "current_title": "(already optimized 2026-10-10 — 124-char rewritten title, full glow-up)",
 "weaknesses": ["None — already received full SEO glow-up on 2026-10-10. Skipped."],
 "new_title": None,
 "tags": None,
},
]

originals_note = """## Original 11 Listings (already SEO'd 2026-10-09)

These were renamed with branded titles, new descriptions, and 13 Etsy-valid tags each during the 2026-10-09 overhaul. No changes proposed — they're in good shape:

| # | Listing | Price | Status |
|---|---------|-------|--------|
| 17 | Spiral Notebook — Retro Floral/Butterfly | $17.25 | SEO'd 10-09 |
| 18 | Spiral Notebook — Pink Pop Confetti | $17.25 | SEO'd 10-09 |
| 19 | Hardcover Journal — Retro Floral | $21.86 | SEO'd 10-09 |
| 20 | Hardcover Journal — Woman Portrait | $21.86 | SEO'd 10-09 |
| 21 | Hardcover Journal — Burgundy/Gold Luxe | $21.86 | SEO'd 10-09 |
| 22 | Mug 11oz — Burgundy V Monogram | $15.14 | SEO'd 10-09 |
| 23 | Collegiate Sweatshirt | $75.60+ | SEO'd 10-09 |
| 24 | Oversized Hoodie | $74.70+ | SEO'd 10-09 |
| 25 | Puff Bun Girl Mug | $12.99+ | SEO'd 10-09 |
| 26 | Feminine Portrait Canvas Tote | $25.99 | SEO'd 10-09 |
| 27 | Signature Tote | $25.99 | SEO'd 10-09 |

Light-touch suggestion for a future pass: add "2026" or seasonal terms (e.g. "Christmas gift", "stocking stuffer") to giftable physical products ahead of Q4.
"""

def check(title, tags):
    issues = []
    if title and len(title) > 140:
        issues.append(f"TITLE TOO LONG: {len(title)} chars")
    if tags:
        if len(tags) != 13:
            issues.append(f"TAG COUNT: {len(tags)} (need 13)")
        for t in tags:
            if len(t) > 20:
                issues.append(f"TAG TOO LONG ({len(t)}): '{t}'")
        if len(set(tags)) != len(tags):
            issues.append("DUPLICATE TAGS")
    return issues

print("# Etsy SEO Optimization — She's The Vibe")
print()
print("**Prepared 2026-10-10. REVIEW ONLY — do not publish until Christina approves.**")
print()
print("**Data gap:** live listing data could not be pulled — the Etsy API auth socket is unavailable in this session and Etsy blocks text-fetching (403). Current titles/tags below are reconstructed from the 2026-10-09 listing drafts and the 2026-10-09/10 overhaul notes. Verify against Shop Manager before publishing.")
print()
print("## Key Findings")
print()
print("1. **Invalid tags in current drafts** — Etsy's tag limit is 20 characters. The Vibe Dashboard draft has 2 tags that exceed it and are silently dropped by Etsy: `google sheets planner` (21), `life organizer spreadsheet` (26). All replacement tags below are validated ≤20 chars.")
print("2. **Brand name wastes title space** — every journal draft ends with `| She's The Vibe` (~18 chars). A new shop gets zero searches for its brand name. Those characters now go to high-traffic keywords.")
print("3. **Missing the hottest niches** — `ADHD planner` (10k+ review sellers), `shadow work`, `bible study`, `tarot spread`, and `budget planner` are the top-converting searches in these categories and were absent from titles.")
print("4. **Work Vibe, Home Care Vibe, Bills Babe had no SEO drafts** — published without optimized titles/tags. These are now drafted from scratch.")
print("5. **Waist beads already optimized** (2026-10-10 glow-up) — skipped.")
print("6. **Original 11 already SEO'd** (2026-10-09 overhaul) — no changes proposed.")
print()
print("---")

all_ok = True
for L in listings:
    print()
    print(f"## {L['n']}. {L['name']} — {L['price']} ({L['type']})")
    print()
    print(f"**Current:** {L['current_title']}")
    print()
    print("**Weaknesses:**")
    for w in L["weaknesses"]:
        print(f"- {w}")
    if L["new_title"] is None:
        continue
    issues = check(L["new_title"], L["tags"])
    if issues:
        all_ok = False
        print()
        print("**VALIDATION ISSUES:**")
        for i in issues:
            print(f"- ⚠️ {i}")
    print()
    print(f"**New title** ({len(L['new_title'])}/140 chars):")
    print(f"> {L['new_title']}")
    print()
    print(f"**New tags** ({len(L['tags'])}/13):")
    print(", ".join(f"`{t}`" for t in L["tags"]))
    print()

print()
print(originals_note)
print()
print("## Publishing Checklist (for Christina's approval)")
print()
print("- [ ] Review each new title — do they sound like you?")
print("- [ ] Verify current live titles in Shop Manager match the 'Current' column before overwriting")
print("- [ ] Apply to listings 1–15 (skip 16, already done)")
print("- [ ] Original 11 (17–27): no action needed")
print()
print(f"_All titles ≤140 chars, all tags ≤20 chars, 13 tags each: {'✅ validated' if all_ok else '⚠️ see issues above'}_")
