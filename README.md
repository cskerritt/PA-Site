# Purinton Analytics, LLC — pa-expert.com

A fast, fully static, SEO- and GEO-optimized marketing website for
**Purinton Analytics, LLC** — a forensic vocational expert and life care
planning practice (principal: Jason C. Purinton, LPC, CRC, CVE, FVE, ABVE/F, IPEC).

This is a redesign / facelift of the existing pa-expert.com site, rebuilt for
performance, accessibility, and discoverability in both classic search engines
and AI/generative engines.

## Highlights

- **Zero build step to host.** The generated HTML is committed. Deploy the repo
  root to any static host (GitHub Pages, Netlify, Cloudflare Pages, S3, etc.).
- **Clean-URL structure** (`/services/life-care-planning/`) via `index.html`
  directories.
- **Deep SEO:** per-page titles/descriptions, canonical URLs, Open Graph +
  Twitter cards, `sitemap.xml`, `robots.txt`, semantic HTML, mobile-first
  responsive design.
- **Structured data (JSON-LD):** `ProfessionalService`/`LegalService`,
  `Person` (with credentials), `Service`, `BreadcrumbList`, and `FAQPage` on
  every relevant page — the schema that powers rich results and AI answers.
- **GEO (Generative Engine Optimization):** an `llms.txt` summary file, explicit
  `robots.txt` allowances for AI crawlers (GPTBot, ClaudeBot, PerplexityBot,
  Google-Extended, etc.), and clear, factual, citable FAQ content.
- **Local SEO:** `geo.*` meta tags and `PostalAddress` / `GeoCoordinates`
  structured data for the St. Louis, MO office.
- **Accessible & fast:** skip links, focus styles, reduced-motion support,
  system + Google fonts with `preconnect`, no heavy frameworks or trackers.

## Pages

```
/                              Home
/about/                        About Jason C. Purinton
/services/                     Services overview
  /services/vocational-expert-witness/
  /services/earning-capacity-evaluation/
  /services/life-care-planning/
  /services/case-management/
  /services/economic-damages/
/practice-areas/               Practice areas overview
  /practice-areas/personal-injury/
  /practice-areas/workers-compensation/
  /practice-areas/employment-litigation/
  /practice-areas/family-law/
/contact/                      Contact + consultation form
/privacy/                      Privacy policy
/404.html                      Not-found page
```

## Editing & rebuilding

All pages are generated from a single source of truth, `build.py`, which keeps
the header, footer, SEO tags, and structured data consistent across every page.

```bash
python3 build.py
```

This regenerates every `index.html`, plus `sitemap.xml`, `robots.txt`,
`llms.txt`, `site.webmanifest`, and `CNAME`. Edit content in `build.py`
(see the `SITE`, `SERVICES`, `PRACTICE_AREAS`, and `DETAILS` structures), then
re-run. Styling lives in `assets/css/style.css`; behavior in
`assets/js/main.js`.

## Local preview

```bash
python3 -m http.server 8000
# then open http://localhost:8000/
```

## Notes / follow-ups

- **Contact form** posts to a Formspree placeholder
  (`https://formspree.io/f/your-form-id`). Replace with a real Formspree form ID
  or your own form handler/endpoint.
- **Email address** uses `info@pa-expert.com` as a sensible default — confirm or
  update in `build.py` (`SITE["email"]`).
- **Social/OG image & icons** are provided as SVG (`assets/img/og-default.svg`,
  `favicon.svg`). For best previews on Facebook/LinkedIn/X, export a 1200×630
  PNG and point `og_img` / `apple-touch-icon` / manifest icons at it.
- **Custom domain:** `CNAME` is set to `pa-expert.com` for GitHub Pages. Remove
  it if deploying elsewhere.
- Business facts (credentials, services, address, phone) were reconstructed from
  public professional listings; please review for accuracy before launch.
