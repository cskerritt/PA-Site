# Purinton Analytics - pa-expert.com

Static, zero-runtime marketing site for Jason C. Purinton's forensic vocational
expert and life care planning practice. Everything is generated from `build.py`.

## Build

- `python3 build.py` regenerates every `index.html` plus `sitemap.xml`,
  `robots.txt`, `llms.txt`, `site.webmanifest`, and `CNAME`. Never hand-edit
  generated HTML; edit the data/render functions in `build.py`.
- Expanded content lives in `content_practice.py` (practice areas) and
  `content_insights.py` (articles), merged into `build.py`.
- Verify before done: build exits 0, JSON-LD parses on a sample of each page
  type, and the content rules below all pass (grep should return zero hits).

## Content rules (apply to ALL site copy)

- **OBJECTIVE TONE ALWAYS.** Jason serves BOTH plaintiff AND defense counsel.
  Never use advocacy language ("maximize recovery", "fight for", "win your
  case", "on your side"). Use "objective", "defensible", "independent".
- **NO em dashes.** Use hyphens (-), never em (U+2014) or en (U+2013) dashes,
  and not the `&mdash;` / `&ndash;` entities.
- **NO stat counts.** No "3,000+ hearings", "X+ cities", "N years",
  case/firm/community counts, or any quantified brag. Use qualitative wording
  ("extensive", "across the United States") instead.
- **NO credential / affiliation logo badge strips.** Text credential lists on
  the Credentials page are fine; do not re-add the association-logo strip.

## Accuracy (CV-verified + confirmed 2026-06-24)

- Credentials post-nominal: **LPC, CRC, CVE, CLCP, ABVE/F, IPEC** (also holds
  FVE, NCC, RN). Leadership: **President, Board of Directors** of the American
  Rehabilitation Economics Association; **Board of Directors** of the American
  Board of Vocational Experts.
- Based in **Kansas City, MO**; offices in Kansas City, St. Louis, Denver,
  Chicago (cities only). Do NOT publish a street address or GeoCoordinates for
  any office without a confirmed real address; offices default to "by
  appointment" with no `PostalAddress`/`geo`.
- Contact: `jason@pa-expert.com`, (877) 882-9778, LinkedIn `/in/pa-expert`.
- Contact form posts to Web3Forms; set `SITE["web3forms_key"]` before launch.

## Deploy

GitHub Pages with `CNAME = pa-expert.com`. The redesign branch is the repo
default branch, so pushing may publish to the live domain - confirm before push.
