# SEO Audit — shesthevibe.co
**Date:** 2026-10-10
**Scope:** 24 HTML pages (23 content pages + `links.html`), `robots.txt`, `sitemap.xml`
**Note:** Audit only — no site files were changed.

## Overall verdict: B+ (strong foundation, a few fixable gaps)

The site is in genuinely good shape. Every page has a unique `<title>`, a unique meta description, complete Open Graph tags, `lang`/`charset`/`viewport`, a single H1, JSON-LD organization schema, and 100% image alt-text coverage. `robots.txt` and `sitemap.xml` are correct and complete. The gaps below are mostly polish and missed opportunities, not emergencies.

---

## Site-wide findings

### HIGH priority
1. **No interlinking between blog posts.** The three posts (`post-no-contact.html`, `post-silence-to-script.html`, `post-words-hurt.html`) don't link to each other at all — no "related posts" / "keep reading" block. Internal links between posts are one of the cheapest SEO wins for a blog.
   - *Fix:* Add a "More from The Vibe Journal" block at the bottom of each post linking to the other two.
2. **No cross-links between resource sub-pages.** Each of the six `resources-*.html` pages links only to itself (and the parent `resources.html` via nav). A reader on `resources-parenting.html` never discovers `resources-journal-prompts.html` (except one link on the parenting page).
   - *Fix:* Add a "Explore more resources" link row at the bottom of each resource sub-page pointing to the other five.
3. **No `<link rel="canonical">` on any page.** For a static site this is low-risk today, but canonicals protect against future duplicate-URL issues (trailing slashes, `www` vs non-`www`, UTM params).
   - *Fix:* Add `<link rel="canonical" href="https://shesthevibe.co/<page>">` to every page's `<head>`.
4. **No `404.html`.** Dead links and mistyped URLs currently hit the host's default error page instead of a branded page that funnels visitors back to the shop.
   - *Fix:* Create `404.html` in brand style with links to `index.html`, `shop.html`, and `resources.html`.

### MEDIUM priority
5. **OG images are generic on most pages.** 21 of 24 pages share `og:image = brand-illustration.png`. The three blog posts have their own images (`blog-no-contact.jpg`, `blog-words-hurt.jpg`, `blog-silence-to-script.jpg`) but don't use them as `og:image` — a missed opportunity for click-through on social shares.
   - *Fix:* Point each post's `og:image` (and `twitter:image`) at its own featured image. Consider a unique OG image for `shop.html` (currently `vibe-dashboard.png` — fine, keep) and `book.html` (already uses the book cover — good).
6. **Two meta descriptions exceed ~160 characters** and will truncate in Google results:
   - `book.html` (173 chars) → trim to ≤160.
   - `resources-local.html` (165 chars) → trim to ≤160.
7. **`links.html` has no Twitter Card tags and no JSON-LD.** It's the link-in-bio hub — the page most likely to be shared. Add `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`, and the Organization JSON-LD block for consistency.
8. **Four dashboard-family products share one image.** On `shop.html`, Dashboard Add-Ons Pack, Work Vibe, Home Care Vibe, and Bills Babe all use `vibe-dashboard.png`. Not a bug (alt text is correct per product), but unique product images would improve both UX and image search.
9. **Heading hierarchy skips levels on several pages** (cosmetic; screen readers and crawlers prefer sequential order):
   - `contact.html`, `gallery.html`: H1 → H4 (footer headings are fine, but in-content sections jump).
   - `privacy.html`, `returns.html`, `shipping.html`, `terms.html`: H1 → H3 (add H2 section wrappers or demote to H2).
   - `resources.html`, `resources-worksheets.html`, `services.html`, `blog.html`: H3s appear before the page's H2 (reorder so H2s precede their H3s).

### LOW priority
10. **No `meta keywords` anywhere.** Google ignores this tag; Bing gives it negligible weight. Safe to skip entirely — noted only because it was requested.
11. **Two titles are long** and may truncate in SERPs: `post-silence-to-script.html` (77 chars), `post-words-hurt.html` (70 chars). Consider front-loading keywords.
12. **`about.html` title lacks the brand name** ("About — The Woman Behind the Vibe"). Every other page title includes "She's The Vibe" — make this consistent.
13. **JSON-LD could go further.** Organization schema is present on 23/24 pages (good). Opportunity: add `BlogPosting` schema to the three posts and `Product`/`ItemList` schema to `shop.html` for rich-result eligibility.

---

## Per-page findings

| Page | Title (len) | Description (len) | OG/Twitter | H1 | Images (alt) | Issues |
|---|---|---|---|---|---|---|
| `index.html` | She's The Vibe — More Than a Brand, It's a Lifestyle (52) | 159 ✓ | Full ✓ | 1 ✓ | 5/5 ✓ | — |
| `shop.html` | Shop the Collection — She's The Vibe (36) | 142 ✓ | Full ✓ | 1 ✓ | 28/28 ✓ | #8 (shared product images) |
| `about.html` | About — The Woman Behind the Vibe (33) | 152 ✓ | Full ✓ | 1 ✓ | 1/1 ✓ | #12 (title lacks brand name) |
| `services.html` | Services — She's The Vibe (25) | 123 ✓ | Full ✓ | 1 ✓ | 2/2 ✓ | #9 (H3 before H2) |
| `book.html` | The Girl Who Burned Her Mother's Blueprint — A Novel by Christina Wood (70) | 173 ✗ too long | Full ✓ | 1 ✓ | 1/1 ✓ | #6 (trim description) |
| `blog.html` | The Vibe Journal — She's The Vibe (33) | 82 ✓ | Full ✓ | 1 ✓ | 5/5 ✓ | #1 (no related-post links on hub is fine; #9 H3 before H2) |
| `post-no-contact.html` | No Contact Is Not Punishment — She's The Vibe (45) | 130 ✓ | Full ✓ | 1 ✓ | 0 ✓ | #1 (no related posts), #5 (generic OG image) |
| `post-words-hurt.html` | Sticks and Stones… — She's The Vibe (70) | 147 ✓ | Full ✓ | 1 ✓ | 0 ✓ | #1, #5, #11 (long title) |
| `post-silence-to-script.html` | From Silence to Script… — She's The Vibe (77) | 151 ✓ | Full ✓ | 1 ✓ | 0 ✓ | #1, #5, #11 (long title) |
| `resources.html` | Free Resources — She's The Vibe (31) | 112 ✓ | Full ✓ | 1 ✓ | 0 ✓ | #9 (H3s before H2) |
| `resources-discover.html` | Discover Yourself — Resources — She's The Vibe (46) | 143 ✓ | Full ✓ | 1 ✓ | 0 ✓ | #2 (no sibling links) |
| `resources-journal-prompts.html` | Journal Prompts — Resources — She's The Vibe (44) | 160 ✓ (borderline) | Full ✓ | 1 ✓ | 0 ✓ | #2 |
| `resources-local.html` | Local Resources — She's The Vibe (32) | 165 ✗ too long | Full ✓ | 1 ✓ | 0 ✓ | #2, #6 (trim description) |
| `resources-worksheets.html` | Worksheets — Resources — She's The Vibe (39) | 121 ✓ | Full ✓ | 1 ✓ | 0 ✓ | #2, #9 (H3 before H2) |
| `resources-thinking.html` | What Changed My Thinking — Resources — She's The Vibe (53) | 130 ✓ | Full ✓ | 1 ✓ | 0 ✓ | #2 |
| `resources-parenting.html` | Parent & Family Resources — Resources — She's The Vibe (54) | 140 ✓ | Full ✓ | 1 ✓ | 0 ✓ | #2 (only page with one sibling link) |
| `gallery.html` | Gallery — She's The Vibe (24) | 97 ✓ | Full ✓ | 1 ✓ | 12/12 ✓ | #9 (H1→H4 skip) |
| `testimonials.html` | Community Love — She's The Vibe (31) | 104 ✓ | Full ✓ | 1 ✓ | 0 ✓ | — |
| `contact.html` | Contact — She's The Vibe (24) | 106 ✓ | Full ✓ | 1 ✓ | 0 ✓ | #9 (H1→H4 skip) |
| `privacy.html` | Privacy Policy — She's The Vibe (31) | 81 ✓ | Full ✓ | 1 ✓ | 0 ✓ | #9 (H1→H3 skip) |
| `terms.html` | Terms of Service — She's The Vibe (33) | 91 ✓ | Full ✓ | 1 ✓ | 0 ✓ | #9 (H1→H3 skip) |
| `shipping.html` | Shipping — She's The Vibe (25) | 114 ✓ | Full ✓ | 1 ✓ | 0 ✓ | #9 (H1→H3 skip) |
| `returns.html` | Returns — She's The Vibe (24) | 112 ✓ | Full ✓ | 1 ✓ | 0 ✓ | #9 (H1→H3 skip) |
| `links.html` | She's The Vibe — All My Links (29) | 128 ✓ | OG ✓ / Twitter ✗ | 1 ✓ | 0 ✓ | #7 (no Twitter tags, no JSON-LD) |

---

## `robots.txt` — PASS
```
User-agent: *
Allow: /

Sitemap: https://shesthevibe.co/sitemap.xml
```
Correct and minimal. No action needed.

## `sitemap.xml` — PASS
Lists all 24 URLs with sensible `changefreq`/`priority` values (homepage 1.0, shop 0.9, legal pages 0.3). Every HTML page on the site is included — nothing orphaned, nothing extra. No action needed.

---

## What's already excellent (don't touch)
- Unique, keyword-aware `<title>` on every page
- Unique, compelling meta descriptions on every page (2 need trims — see #6)
- Complete Open Graph tags with page-specific `og:url` on all 24 pages
- Twitter `summary_large_image` cards on 23/24 pages
- `lang="en"`, charset, and viewport meta on every page
- Exactly one H1 per page, all descriptive
- 100% image alt-text coverage (46 images checked), alt text is descriptive and product-accurate
- Organization JSON-LD on 23/24 pages
- Global nav links every main page from every page (strong internal-link backbone)
- `resources.html` hub links all six sub-pages; `blog.html` hub links all three posts

## Suggested fix order (biggest ROI first)
1. Related-post blocks on the 3 blog posts (#1)
2. "Explore more resources" cross-links on the 6 resource sub-pages (#2)
3. Canonical tags on all pages (#3)
4. Branded `404.html` (#4)
5. Per-post OG images (#5)
6. Trim 2 long descriptions (#6)
7. Twitter/JSON-LD on `links.html` (#7)
8. Everything else as time allows
