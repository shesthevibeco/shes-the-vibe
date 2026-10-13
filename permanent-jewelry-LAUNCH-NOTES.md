# Permanent Jewelry — Launch Notes

Everything below is built and sitting locally in this repo. Nothing has been
pushed or deployed — Christina pushes the code herself when she's ready.

## What was built

### New files
| File | What it is |
|---|---|
| `permanent-jewelry-book.html` | Booking hub: start-here steps, deposit cards, booking request form, aftercare teaser |
| `permanent-jewelry-release.pdf` | Release & Waiver (fillable by printing/signing; signature lines, minors block, photo consent) |
| `permanent-jewelry-before-your-appointment.pdf` | Client packet: lanes, deposits, setup, travel zones, pricing recap |
| `permanent-jewelry-aftercare.pdf` | Aftercare sheet: first 48h, cleaning, water/tanning notes, snag/break + re-weld policy, removal |
| `permanent-jewelry-docs/release.html` | PDF source (edit this, re-run WeasyPrint to rebuild the PDF) |
| `permanent-jewelry-docs/before-your-appointment.html` | PDF source |
| `permanent-jewelry-docs/aftercare.html` | PDF source |
| `apps-script-pj-update.gs` | Apps Script addendum for the v11 leads backend (see "Apps Script" below) |

Rebuild a PDF after editing its source:
`python3 -m weasyprint permanent-jewelry-docs/release.html permanent-jewelry-release.pdf`
(same pattern for the other two).

### Changed files
| File | Change |
|---|---|
| `permanent-jewelry.html` | "Permanent Jewelry" added to its own nav (desktop + mobile) |
| `script.js` | New `.pj-booking-form` submit handler — posts `type: 'permanent-jewelry'` with all booking fields to the same Apps Script endpoint as every other form |
| `services.html` | Jewelry card CTA now goes to `permanent-jewelry.html` ("See Chains & Pricing") + new "Book an Appointment" button to the booking hub (was: "Inquire" → contact.html) |
| `contact.html` | Services sidebar now sends jewelry folks to the jewelry page / booking hub instead of the contact form |
| `links.html` | New "Permanent Jewelry" section with two buttons (page + booking hub) — links.html has no top nav, so this is its version of the nav link |
| `sitemap.xml` | Added `permanent-jewelry.html` (0.8) and `permanent-jewelry-book.html` (0.7) |
| 31 site pages total | "Permanent Jewelry" link added to the main nav (desktop + mobile) of every page that has the site header — right after **Coaching** on newer-template pages, right after **Services** on older-template pages (blog posts, legal pages, resources subpages — those navs never had a Coaching link) |

Not touched: `permanent-jewelry-PREVIEW.html` (generated preview artifact —
regenerate with `make_preview.py` if needed; it isn't part of the site).

## Apps Script — go-live steps (Christina, ~10 min)

The form on the booking page already posts to the live endpoint, but the
backend won't route jewelry requests until this is merged:

1. Open the Apps Script project that runs the STV leads backend
   (the v11 code in `STV-Leads-Backend-v11.js`).
2. Open `apps-script-pj-update.gs` (in this repo) and merge its 5 snippets
   at the marked spots:
   - **Snippet 1:** add `PERMANENT_JEWELRY: 15` to the `COL` map.
   - **Snippet 2:** add the `permanent-jewelry` branch in `doPost`'s routing chain.
   - **Snippet 3:** two small insertions around the notification email
     (sends the client their next-steps email; adds booking details to your
     notification).
   - **Snippet 4:** add the detail-logging branch at the top of `logToLegacyTab`.
   - **Snippet 5:** paste the new functions (`pjDetailsText`, `pjEmailText`,
     `pjEmailHtml`, `sendPjBookingEmail`) at the end of the file.
   ⚠️ There must still be exactly **ONE** `doPost` in the file when you're done.
3. In the **Master Tracker** sheet tab, type the header `Permanent Jewelry`
   in column **O** (column 15). The "Permanent Jewelry" detail tab creates
   itself (with headers) on the first booking request.
4. Redeploy: **Deploy → Manage deployments → Edit → Version: New version**,
   Execute as **Me**. The `/exec` URL script.js already points to stays the same.

What happens when it works: the person lands in Master Tracker (one row per
person, jewelry column timestamped), the full request is logged in the
"Permanent Jewelry" tab, the client instantly gets the branded next-steps
email (booking page + packet + release + aftercare links), and you get the
usual `[STV]` notification email — now with all their booking details in it.

## When the Google Calendar link exists — ONE find & replace

The two deposit buttons on `permanent-jewelry-book.html` currently point to
the placeholder token `%%PJ_BOOKING_LINK%%`. When Christina's permanent
jewelry Google Calendar appointment schedule is ready:

1. In `permanent-jewelry-book.html`, replace **both** occurrences of
   `%%PJ_BOOKING_LINK%%` with the calendar link
   (e.g. `https://calendar.app.google/XXXX`).
   One command does it:
   `sed -i 's|%%PJ_BOOKING_LINK%%|https://calendar.app.google/XXXX|g' permanent-jewelry-book.html`
2. Optional but smart: point `permanent-jewelry.html`'s "Book Your
   Appointment" buttons at the calendar too — right now they go to the
   booking hub, which is fine as a funnel.

Note: the Apps Script next-steps email intentionally links clients to the
**booking page** (not the calendar directly), so the calendar link only
ever has to be updated in one place — this page.

## Christina's parallel checklist
- [ ] Build the permanent jewelry Google Calendar appointment schedule
- [ ] Turn on the Stripe payment setting on **both** calendars (coaching + permanent jewelry) so deposits collect at booking
- [ ] Send Talia the calendar link → token swap above → push
