# Lovable Prompt — Re-sync whitepapers to production (the /live cross-links)
Version 07-20-2026 · paste the block below into Lovable · source: _upload_whitepapers_07-20-2026.zip (41 files)

> Gap found in RE-CHECK 21: whitepaper→/live cross-links are LOCAL ONLY. Production WP34 = 5,799 B / 0 /live links; local = 6,044 B / 4. WP03, WP25 also 0 in prod. The /live PAGES are deployed (writeup rows present); the 40-whitepaper library was not re-synced.

## PASTE INTO LOVABLE

Replace the static whitepaper files with updated versions. The 41 files (KFE-WP01 … KFE-WP40 plus index.html) in `public/whitepapers/` need to be overwritten with the copies I'm providing (from _upload_whitepapers_07-20-2026.zip). Content-only updates — do NOT convert any into React pages, do NOT change routing, do NOT modify their HTML. Self-contained static files served at /whitepapers/KFE-WPxx_*.html.

What changed: 9 whitepapers (WP03, WP04, WP06, WP10, WP17, WP25, WP27, WP33, WP34) gained a "Run it live." CTA box linking to their matching /live page; WP34 gained a paragraph noting the engine runs in-browser at kronosfusionenergy.com/live.

Steps: (1) overwrite every file in public/whitepapers/ with the provided same-named version (41 total); (2) do not touch any other page/route/file; (3) publish.

VERIFY — show actual output, don't just claim success:
1. Fetch /whitepapers/KFE-WP34_run-it-yourself.html — confirm it contains "in your browser" and a link to "/live"; paste the lines.
2. Fetch /whitepapers/KFE-WP03_d-he3-low-neutron.html — confirm "/live" present; paste the line.
3. Report deployed WP34 byte size (≈6,044, not ≈5,799).
4. /whitepapers index still lists all 40, none render with the React header.
