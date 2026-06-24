# Purinton Analytics Site Overhaul — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Re-skin pa-expert.com to the real Purinton Analytics brand (navy + orange + teal, real logo/photos/credential marks), correct every fact to the CV baseline, add 9 practice-area pages + 4 metro office pages + a Credentials page + an Insights section, and wire a working Web3Forms contact form — all through the single `build.py` generator.

**Architecture:** Static site; `build.py` (1,956 lines) is the single source of truth. It holds data (`SITE`, `SERVICES`, `PRACTICE_AREAS`, `DETAILS`, `STATES`, city helpers) and render functions (`head`, `header`, `footer`, `cta_band`, `faq_block`, `page_hero`, `*_schema`, `card_grid`, `*_body`, `build_pages`, `write_page`, `write_meta_files`). `python3 build.py` regenerates all HTML + `sitemap.xml`/`robots.txt`/`llms.txt`/`site.webmanifest`/`CNAME`. Styling: `assets/css/style.css` (447 lines, CSS-variable design system). Behavior: `assets/js/main.js`. We extend data + render functions; we never hand-edit generated `index.html`.

**Tech Stack:** Python 3 static generator, semantic HTML, CSS variables, vanilla JS, JSON-LD schema, WebP imagery, GitHub Pages hosting, Web3Forms (form handler).

**Verification model (no unit-test framework exists):** each task verifies by (a) `python3 build.py` exiting 0, (b) `grep` assertions on generated output, and (c) a local preview check on the running server (`http://localhost:8123`, started via `.claude/launch.json` → `pa-site`). "Failing test" = a grep that returns nothing / a visual gap before the change; "passing" = the grep matches / the preview renders correctly.

**Source of truth for facts:** the committed spec `docs/superpowers/specs/2026-06-23-pa-expert-overhaul-design.md` (§4 CV-verified facts, §4.1 discrepancies shipped conservatively until the user confirms).

---

## File Structure

**Created:**
- `assets/img/brand/*` — imported brand WebP assets (headshots, hero, wave, skylines, 11 credential logos).
- `assets/img/logo.svg`, `assets/img/logo-light.svg` — navy-wordmark (header) + white-wordmark (dark) logo variants.
- `assets/img/favicon-32.png`, `assets/img/apple-touch-icon.png`, `assets/img/og-default.png` (1200×630) — generated.
- `offices/{kansas-city,st-louis,denver,chicago}/index.html` — generated metro pages.
- `practice-areas/{...}/index.html` — 9 new generated practice-area pages.
- `credentials/index.html` — generated.
- `insights/index.html` + `insights/<slug>/index.html` — generated.

**Modified (all in `build.py` unless noted):**
- `SITE` dict (23–46) — CV-accurate contact/brand facts.
- `SERVICES` (66–77), `PRACTICE_AREAS` (79–88), `DETAILS` (754–1147) — corrected + expanded.
- New data: `OFFICES`, `AFFILIATIONS`, `ARTICLES`.
- Render fns: `header` (169), `footer` (197), `home_body` (426), `about_body` (546), `practice_index_body` (667), `contact_body` (1150), plus new `office_body`, `credentials_body`, `insights_index_body`, `article_body`.
- Schema fns: `org_schema` (318), `person_schema` (344) — CV creds, multi-office, social `sameAs`.
- `build_pages` (1722), `write_meta_files` (1850) — register new pages in nav/sitemap/llms.
- `assets/css/style.css` — palette tokens + new components (credential strip, logo img, office cards, article list).

---

## Phase 0 — Setup & Asset Import

### Task 0.1: Branch + baseline build
**Files:** none (git only)

- [ ] **Step 1: Confirm branch & clean build baseline**

Run:
```bash
cd ~/Documents/"New project"/PA-Site
git rev-parse --abbrev-ref HEAD     # expect: claude/pa-expert-website-redesign-8wb1bh
python3 build.py && echo OK
```
Expected: prints build output then `OK`; `git status` shows only generated files unchanged (regeneration is deterministic).

- [ ] **Step 2: Commit any baseline drift** (only if `build.py` regen changed committed HTML)
```bash
git add -A && git commit -m "chore: baseline rebuild" || echo "no drift"
```

### Task 0.2: Import brand assets into the repo
**Files:** Create `assets/img/brand/*`, `assets/img/logo.svg`, `assets/img/logo-light.svg`

- [ ] **Step 1: Copy raster brand assets**
```bash
SRC=~/Downloads/pa-expert-brand-assets
DST=assets/img/brand
mkdir -p "$DST"
cp "$SRC"/images/*.webp "$DST"/
ls "$DST" | wc -l      # expect 18 (2 portraits, hero, wave, 4 skylines, 10 assoc logos)
```

- [ ] **Step 2: Add the logo (white-wordmark original) as the dark variant**
```bash
cp ~/Downloads/purinton-analytics-logo.svg assets/img/logo-light.svg
```

- [ ] **Step 3: Create the navy-wordmark variant for the light header**

Copy `logo-light.svg` → `assets/img/logo.svg`, then recolor the wordmark: change the `.st1 { fill: #fff; }` rule to `fill: #012262;` (navy). The orange `.st0` mark stays. Verify both files are valid SVG (`xmllint --noout assets/img/logo.svg` if available, else open in preview).

- [ ] **Step 4: Commit**
```bash
git add assets/img/brand assets/img/logo.svg assets/img/logo-light.svg
git commit -m "assets: import Purinton Analytics brand kit (logo, photos, credential marks)"
```

---

## Phase 1 — Brand Foundation (palette, logo, chrome, icons)

### Task 1.1: Re-skin the palette (gold → orange + teal)
**Files:** Modify `assets/css/style.css:4-28` (`:root` tokens) and `build.py:45` (`SITE["theme"]`)

- [ ] **Step 1 (failing check):** `grep -c "c69a4b\|gold-500" assets/css/style.css` → returns >0 (gold still present).

- [ ] **Step 2: Replace brand tokens.** In `:root`, set:
```css
  --navy-900: #001a40;
  --navy-800: #012262;   /* hero deep navy */
  --navy-700: #00256A;   /* hero cobalt */
  --navy-600: #1f4d80;
  --brand-500: #FE8F36;  /* primary orange (was gold) */
  --brand-400: #ff9f52;
  --brand-grad: linear-gradient(135deg, #ff8f36, #f47108);
  --brand-100: #ffe9d6;
  --teal-500: #479B83;   /* secondary accent */
  --teal-100: #e3f0ec;
```
Then **find/replace usages**: `--gold-500`→`--brand-500`, `--gold-400`→`--brand-400`, `--gold-100`→`--brand-100` throughout `style.css`. Re-point button shadows from `rgba(198,154,75,…)` to `rgba(254,143,54,…)`. Set `build.py:45` `"theme": "#012262"`.

- [ ] **Step 3 (passing check):**
```bash
grep -c "c69a4b" assets/css/style.css   # expect 0
grep -c "FE8F36\|brand-500" assets/css/style.css  # expect >0
python3 build.py && echo OK
```

- [ ] **Step 4: Preview check.** Reload `http://localhost:8123/` — buttons/accents are orange, hero navy. Spot-check WCAG: orange (`#FE8F36`) fills keep **dark** text (`#1c150a`) as today; orange-on-navy used only for large text/accents.

- [ ] **Step 5: Commit** `style: re-skin palette to brand navy + orange + teal`

### Task 1.2: Real logo in header + footer
**Files:** Modify `build.py:169-196` (`header`), `build.py:197-243` (`footer`); add `.brand-logo` CSS.

- [ ] **Step 1:** Read `header()` and `footer()` to see the current text "PA" `.brand-mark` markup.
- [ ] **Step 2:** Replace the `.brand-mark` + `.brand-text` block in `header()` with an `<img src="/assets/img/logo.svg" alt="Purinton Analytics" class="brand-logo" width="187" height="66">` (link wraps to `/`). In `footer()`, use `/assets/img/logo-light.svg` (white wordmark on navy). Add CSS: `.brand-logo{height:40px;width:auto;display:block}` and a footer variant.
- [ ] **Step 3:** `python3 build.py`; `grep -r "logo.svg" --include=index.html . | head` → matches in header/footer of generated pages.
- [ ] **Step 4: Preview** — header shows navy-wordmark logo legibly on the light sticky bar; footer shows white-wordmark logo on navy. Mobile nav still toggles.
- [ ] **Step 5: Commit** `feat: use real Purinton Analytics logo in header and footer`

### Task 1.3: Favicon + OG PNG
**Files:** Create `assets/img/favicon-32.png`, `assets/img/apple-touch-icon.png`, `assets/img/og-default.png`; modify `head()` (`build.py:98-168`) and `write_meta_files()` manifest.

- [ ] **Step 1:** Generate a favicon/touch-icon from the logo **mark** (orange monogram on transparent/navy) and a 1200×630 `og-default.png` (logo + name + tagline on navy). Use a quick Python/Pillow or `rsvg-convert`/`sips` step; commit the PNGs. (If tooling unavailable, render via the preview canvas and screenshot at exact size.)
- [ ] **Step 2:** Point `og_img` in `head()` to `/assets/img/og-default.png`; add `<link rel="apple-touch-icon">`; keep `favicon.svg` and add the PNG fallback. Update `site.webmanifest` icons.
- [ ] **Step 3:** `python3 build.py`; `grep "og-default.png" index.html` → match.
- [ ] **Step 4: Commit** `feat: real favicon + 1200x630 OG image`

---

## Phase 2 — Content Accuracy (CV baseline)

### Task 2.1: Correct `SITE` contact/brand facts
**Files:** Modify `build.py:23-46`

- [ ] **Step 1 (failing check):** `grep -n "info@pa-expert\|purintonanalytics\|913" build.py` → matches (stale values present).
- [ ] **Step 2:** Update `SITE`: `principal_creds` → `"LPC, CRC, CVE, ABVE/F, IPEC"`; `email` → `"jason@pa-expert.com"`; `linkedin` → `"https://www.linkedin.com/in/pa-expert"`; add `"facebook": "https://www.facebook.com/Purinton.Analytics"`, `"x": "https://x.com/PurintonExpert"`. **Remove** `mobile_display`/`mobile_e164` (not on CV — §4.1) **and** the hard-coded `street`/`postal`/`geo_*` single-office address (replaced by `OFFICES` data, Task 3.2); keep `city/region` as "Kansas City, MO" headquarters reference only where a city (not street) is needed. Tagline stays.
- [ ] **Step 3 (passing):** `grep -c "info@pa-expert\|/in/purintonanalytics" build.py` → 0. `python3 build.py && echo OK`.
- [ ] **Step 4:** `grep -rl "913-484-4346\|231 S. Bemiston" *.html */index.html 2>/dev/null` → empty (no fabricated contact data in output).
- [ ] **Step 5: Commit** `fix: CV-accurate contact, credentials, and social links`

### Task 2.2: CV-accurate JSON-LD (`org_schema`, `person_schema`)
**Files:** Modify `build.py:318-362`

- [ ] **Step 1:** Update `person_schema()`: `jobTitle` "Forensic Vocational Expert & Life Care Planner"; `alumniOf` = Emporia State, MidAmerica Nazarene, University of Kansas; `hasCredential` list = LPC, CRC, CVE, ABVE Fellow, IPEC, FVE, RN (CV §4 item 1, **no CLCP**); `sameAs` = LinkedIn/Facebook/X + JurisPro/SEAK if desired; `memberOf` = ABVE, AREA, IARP. Update `org_schema()`: multiple `areaServed` (US + the 4 metros) and `address`/`location` **only** as cities (no fabricated street; see Task 3.2 for per-office LocalBusiness).
- [ ] **Step 2:** `python3 build.py`; validate JSON-LD parses: `python3 -c "import json,re,sys; html=open('index.html').read(); [json.loads(m) for m in re.findall(r'<script type=\"application/ld\+json\">(.*?)</script>', html, re.S)]; print('JSON-LD OK')"`.
- [ ] **Step 3 (passing):** `grep -o "CLCP" index.html | head` → empty. `grep "in/pa-expert" index.html` → match.
- [ ] **Step 4: Commit** `fix: CV-accurate Person/Organization schema (no CLCP, correct sameAs)`

### Task 2.3: Rewrite Home + About copy to CV facts
**Files:** Modify `build.py:426-543` (`home_body`), `546-640` (`about_body`)

- [ ] **Step 1:** In `home_body()`: hero card uses `/assets/img/brand/Jason-Purinton-2025-BW.webp` (replace "JP" avatar); credentials line CV-accurate; stats band uses defensible numbers — **"3,000+ SSA disability hearings testified," "4 offices," "Since 2018," "MO · KS · NE licensed"** (replace any invented stats). Add the home hero illustration (`home-hero-PA-header-image.webp`) as a tasteful hero-side/background element. Insert the **credential strip** component (Task 3.4) below the hero.
- [ ] **Step 2:** In `about_body()`: use `about-Jason-Purinton-Informal-BW.webp`; bio reflects CV — Vocational Pros (2018) → Purinton Analytics (2024); RN + LPC clinical depth; 3,000+ SSA hearings; DOT/O*NET/ORS methodology; AREA President-Elect & IARP forensic-section history; education list CV-exact (Task spec §4 item 6); leadership/affiliations CV-exact. **No CLCP, no "President" (use President-Elect), no ABVE board.**
- [ ] **Step 3:** `python3 build.py`; `grep -c "3,000" index.html` → >0; `grep -c "President-Elect" about/index.html` → >0; `grep -c "CLCP" about/index.html` → 0.
- [ ] **Step 4: Preview** Home + About at desktop + mobile: real photos render, copy reads accurately, contrast OK.
- [ ] **Step 5: Commit** `content: CV-accurate Home and About with real portraits`

### Task 2.4: Correct existing Service + Practice-area detail copy
**Files:** Modify `DETAILS` (`build.py:754-1147`) entries for the 5 services + 4 existing practice areas

- [ ] **Step 1:** Audit each `DETAILS` entry against the CV; fix any overstated capability, align methodology language (DOT, O*NET, ORS, transferable-skills analysis, labor-market survey), ensure FAQ answers are factual/citable (GEO). Keep structure; change copy/facts only.
- [ ] **Step 2:** `python3 build.py`; spot-grep a corrected phrase per page.
- [ ] **Step 3: Commit** `content: align service & practice-area copy with CV methodology`

---

## Phase 3 — New Pages

### Task 3.1: Expand to 9 new practice-area pages
**Files:** Modify `PRACTICE_AREAS` (79–88), `PRACTICE_ICONS` (402), `DETAILS` (754–1147), `practice_index_body` (667), `build_pages` (1722); pages auto-generate via existing `detail_body`.

- [ ] **Step 1:** Append 9 entries to `PRACTICE_AREAS` (slug, title, blurb) and matching `DETAILS[slug]` configs, reusing the existing detail schema (intro, "what we evaluate", related services, FAQ, CTA). Areas + framing:
  | Slug | Title | Angle |
  |---|---|---|
  | medical-malpractice | Medical Malpractice | post-injury earning capacity where negligence caused impairment |
  | motor-vehicle-trucking | Motor Vehicle & Trucking | MVA/CMV catastrophic-injury vocational loss; FMCSA fitness |
  | premises-liability | Premises Liability | slip/fall and unsafe-premises injury earning-capacity loss |
  | product-liability | Product Liability | defective-product injury employability/earning capacity |
  | labor-railroad-fela | Labor & FELA / Railroad | FELA railroad-worker wage-loss (CV-evidenced) |
  | long-term-disability | Long-Term Disability | own-occ/any-occ LTD vocational review |
  | social-security-disability | Social Security Disability | SSA listings/grids VE testimony (CV: 3,000+ hearings) |
  | wrongful-death | Wrongful Death | lost earning capacity & household-services foundation |
  | veterans-disability | Veteran's Disability | veteran vocational capacity & transferable military skills |
  Provide one fully-written `DETAILS` entry as the template in-line during execution; the rest follow the same shape with the angle above. Add each slug to `PRACTICE_ICONS` (reuse sensible existing icons).
- [ ] **Step 2:** Ensure `build_pages()` iterates `PRACTICE_AREAS` for detail pages (it already does for the existing 4 — confirm the loop is data-driven, not hard-coded). Update `practice_index_body()` grid to show all 13.
- [ ] **Step 3:** `python3 build.py`; `ls practice-areas/ | wc -l` → 13 dirs (+ index). `grep -c "FAQPage" practice-areas/social-security-disability/index.html` → >0.
- [ ] **Step 4: Preview** two new pages (SSDI, trucking) desktop+mobile.
- [ ] **Step 5: Commit** `feat: 9 new practice-area pages (med-mal, trucking, premises, product, FELA, LTD, SSDI, wrongful death, veterans)`

### Task 3.2: Four metro office pages + honest LocalBusiness schema
**Files:** Add `OFFICES` data; new `office_body(office)`; new `local_business_schema(office)`; register in `build_pages`, `NAV`/footer, `write_meta_files`.

- [ ] **Step 1:** Define `OFFICES = [{slug, city, region, skyline, courts/venues blurb, address|None}]` for Kansas City, St. Louis, Denver, Chicago. `address` is `None` until the user supplies a real street (§7) — when `None`, render "Meetings by appointment" and **omit** `PostalAddress`/`GeoCoordinates` from schema (emit only `areaServed` city). Use the matching `contact-*-Skyline.webp`.
- [ ] **Step 2:** Write `office_body()` (page-hero with skyline, who-we-serve-locally, services, statewide reach note, CTA) and `local_business_schema()` (conditional on `address`).
- [ ] **Step 3:** Register `/offices/<slug>/` in `build_pages`, add an "Offices" nav item (or group under Locations — keep distinct from the 7-state/city programmatic pages), add to sitemap/llms.
- [ ] **Step 4:** `python3 build.py`; `ls offices/ | wc -l` → 4. `grep -L "PostalAddress" offices/*/index.html` → all 4 (no fabricated address) until addresses provided.
- [ ] **Step 5: Preview** one office page; skyline renders, no fake address.
- [ ] **Step 6: Commit** `feat: 4 metro office pages (KC, St. Louis, Denver, Chicago) with honest local schema`

### Task 3.3: Credentials & Affiliations page
**Files:** Add `AFFILIATIONS` data; new `credentials_body()`; register page.

- [ ] **Step 1:** `AFFILIATIONS = [{logo, name}]` for the 10 association marks (SEAK, IARP, ABVE, ICHCC, CRCC, AREA, NBCC, Psychology Today, ALM/Law.com, JurisPro). `credentials_body()` renders: full CV credential list (with issuing bodies), memberships & leadership (CV §4 item 5, conservative), and the logo strip labeled **"Memberships & Professional Listings"** (honest framing — listings/memberships, not endorsements).
- [ ] **Step 2:** Register `/credentials/`; add to nav/footer/sitemap/llms; add `.credential-strip` CSS (monochrome, grayscale logos that color on hover).
- [ ] **Step 3:** `python3 build.py`; `grep -c "Memberships & Professional Listings" credentials/index.html` → >0; `grep -c "CLCP" credentials/index.html` → 0.
- [ ] **Step 4: Commit** `feat: Credentials & Affiliations page with association marks`

### Task 3.4: Reusable credential strip (shared component)
**Files:** Add `credential_strip()` helper; call from `home_body`, `about_body`, `credentials_body`.

- [ ] **Step 1:** Factor the logo strip into one `credential_strip()` function (DRY) used on Home, About, Credentials. (If Task 2.3 inlined it, refactor to the shared helper now.)
- [ ] **Step 2:** `python3 build.py`; confirm strip appears on all three pages via grep.
- [ ] **Step 3: Commit** `refactor: shared credential strip component`

### Task 3.5: Insights/Articles section
**Files:** Add `ARTICLES` data; new `insights_index_body()`, `article_body(article)`, `article_schema(article)`; register pages.

- [ ] **Step 1:** Define `ARTICLES = [{slug, title, dek, date, body_sections, faq}]`. Seed **3** factual, citable articles grounded in his methodology (e.g., "What a Vocational Expert Evaluates in a Personal-Injury Case", "Earning Capacity vs. Wage Loss: How Forensic Vocational Opinions Are Built", "How Social Security Vocational Expert Testimony Works"). No fabricated case outcomes; cite DOT/O*NET/ORS/BLS generically. Log that only 3 are seeded (not a full content program — spec §9).
- [ ] **Step 2:** Write `insights_index_body()` (card list) + `article_body()` (page-hero, prose sections, FAQ, CTA, author = Jason) + `Article`/`BreadcrumbList` schema.
- [ ] **Step 3:** Register `/insights/` + `/insights/<slug>/` in `build_pages`, nav, sitemap, llms.
- [ ] **Step 4:** `python3 build.py`; `ls insights/ | wc -l` → 4 (index + 3); JSON-LD validates (reuse Task 2.2 validator on an article).
- [ ] **Step 5: Preview** the index + one article.
- [ ] **Step 6: Commit** `feat: Insights section with 3 seed articles`

---

## Phase 4 — Launch Readiness

### Task 4.1: Wire Web3Forms contact handler
**Files:** Modify `contact_body()` (`build.py:1150-1218`), `SITE` (add `web3forms_key` placeholder constant), `assets/js/main.js` if AJAX submit desired.

- [ ] **Step 1:** Replace the Formspree placeholder `action` with Web3Forms: `<form action="https://api.web3forms.com/submit" method="POST">` + hidden `<input type="hidden" name="access_key" value="{SITE['web3forms_key']}">` + honeypot `<input type="checkbox" name="botcheck" style="display:none">` + `redirect`/success handling. Keep all existing fields. `SITE["web3forms_key"]` defaults to an empty placeholder string with an HTML comment noting "set real key before deploy".
- [ ] **Step 2:** `python3 build.py`; `grep "api.web3forms.com" contact/index.html` → match; `grep -c "formspree" contact/index.html` → 0.
- [ ] **Step 3: Preview** the contact form renders; (live submit deferred until the real `access_key` is provided by the user).
- [ ] **Step 4: Commit** `feat: wire contact form to Web3Forms (key pending)`

### Task 4.2: Full rebuild, meta files, and verification sweep
**Files:** all generated output

- [ ] **Step 1:** `python3 build.py`; confirm `sitemap.xml`, `robots.txt`, `llms.txt` include every new page (`grep -c "offices/\|insights/\|credentials/" sitemap.xml` → all present; same for `llms.txt`).
- [ ] **Step 2:** JSON-LD validation sweep across a sample of each page type (reuse Task 2.2 validator).
- [ ] **Step 3:** Accuracy sweep: `grep -rl "CLCP\|913-484-4346\|231 S. Bemiston\|formspree\|c69a4b" . --include=index.html` → empty.
- [ ] **Step 4: Preview matrix** — Home, About, a service, a new practice area, an office, Credentials, an article, Contact — at desktop (1280) + mobile (375), light + dark-emulation. Check: logo legibility, orange/navy contrast, real images load with alt text, reduced-motion respected, mobile nav works.
- [ ] **Step 5: Commit** `chore: full rebuild + meta files for all new pages`

### Task 4.3: Launch checklist (requires user inputs)
**Files:** `build.py` final values

- [ ] **Step 1:** Apply user-provided launch values when available: Web3Forms `access_key`; confirmed office street addresses (flip `OFFICES[*].address` and enable LocalBusiness schema where real); §4.1 credential confirmations (CLCP / AREA title / ABVE board / mobile phone) — upgrade copy only if the user confirms each.
- [ ] **Step 2:** `python3 build.py`; re-run the Task 4.2 sweeps.
- [ ] **Step 3: Deploy** per user's choice (GitHub Pages; CNAME `pa-expert.com` already set) — push branch / open PR / merge as directed; confirm DNS cutover timing with the user.
- [ ] **Step 4: Commit/PR** `release: launch-ready Purinton Analytics overhaul`

---

## Self-Review

**Spec coverage:**
- §3 brand (palette/logo/fonts/imagery) → Tasks 1.1–1.3, 0.2. ✓
- §4 content accuracy (all 10 facts) → Tasks 2.1–2.4. ✓ (CLCP/President-Elect/ABVE/mobile/address handled conservatively per §4.1 → Tasks 2.1/2.2/2.3/3.2; user upgrade path → 4.3.)
- §5.2 new pages (9 practice areas, 4 offices, credentials, insights) → Tasks 3.1, 3.2, 3.3, 3.5. ✓
- §6 architecture (data-driven build.py, asset pipeline, meta regen) → Phases 0–4. ✓
- §7 launch (Web3Forms, addresses, deploy) → Tasks 4.1–4.3. ✓
- §8 testing → per-task verification + Task 4.2 sweep. ✓
- Fonts unchanged (spec §3.3) — intentionally no task. ✓

**Placeholder scan:** `SITE["web3forms_key"]` and `OFFICES[*].address=None` are intentional, user-supplied launch values (Task 4.3), explicitly flagged — not plan gaps. Per-page prose is generated at execution from the CV facts in the spec + brand assets; the repetitive sets (3.1/3.2/3.5) give exact data + one worked template, which is DRY rather than a placeholder.

**Type/name consistency:** new data names (`OFFICES`, `AFFILIATIONS`, `ARTICLES`) and fns (`office_body`, `local_business_schema`, `credentials_body`, `credential_strip`, `insights_index_body`, `article_body`, `article_schema`) are referenced consistently across Phase 3 and registered in `build_pages`/`write_meta_files`. CSS tokens renamed `--gold-*`→`--brand-*` consistently in Task 1.1 before any new component uses them.

**Accuracy guardrail (forensic-critical):** every task that emits credentials/roles/addresses asserts the conservative CV baseline via grep (`CLCP`→0, `President-Elect` present, no `PostalAddress` without real address); upgrades are gated on explicit user confirmation in Task 4.3.
