#!/usr/bin/env python3
"""
Static site generator for Purinton Analytics, LLC (pa-expert.com).

Produces a fast, fully static, SEO + GEO optimized marketing site.
Run:  python3 build.py
Output is written in-place (clean-URL directories with index.html).

The generated HTML requires no build step to host — deploy the repo root
to any static host (GitHub Pages, Netlify, Cloudflare Pages, S3, etc.).
"""

import os
import re
import shutil
from datetime import date

# --------------------------------------------------------------------------- #
#  Site-wide configuration
# --------------------------------------------------------------------------- #

SITE = {
    "name": "Purinton Analytics, LLC",
    "short_name": "Purinton Analytics",
    "domain": "https://pa-expert.com",
    "tagline": "Vocational Expert & Life Care Planning Services",
    "principal": "Jason C. Purinton",
    "principal_creds": "LPC, CRC, CVE, FVE, ABVE/F, IPEC",
    "phone_display": "(877) 882-9778",
    "phone_e164": "+18778829778",
    "mobile_display": "(913) 484-4346",
    "mobile_e164": "+19134844346",
    "email": "info@pa-expert.com",
    "street": "231 S. Bemiston Ave., Ste. 800",
    "city": "St. Louis",
    "region": "MO",
    "region_full": "Missouri",
    "postal": "63105",
    "country": "US",
    "geo_lat": "38.6446",
    "geo_lng": "-90.3318",
    "founded": "2018",
    "linkedin": "https://www.linkedin.com/in/purintonanalytics/",
    "theme": "#0f2a4a",
}

BUILD_YEAR = date.today().year
LASTMOD = date.today().isoformat()

ROOT = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------- #
#  Navigation
# --------------------------------------------------------------------------- #

NAV = [
    ("Home", "/"),
    ("About", "/about/"),
    ("Services", "/services/"),
    ("Practice Areas", "/practice-areas/"),
    ("Contact", "/contact/"),
]

SERVICES = [
    ("Vocational Expert Witness", "/services/vocational-expert-witness/",
     "Objective, defensible evaluations of employability and earning capacity for litigation."),
    ("Earning Capacity & Wage Loss", "/services/earning-capacity-evaluation/",
     "Pre- and post-injury earning capacity analysis and quantified wage loss opinions."),
    ("Life Care Planning", "/services/life-care-planning/",
     "Comprehensive, evidence-based plans projecting the future cost of care."),
    ("Case Management", "/services/case-management/",
     "Coordinated rehabilitation and medical case management that keeps recovery on track."),
    ("Economic Damages", "/services/economic-damages/",
     "Clear calculation of economic loss that translates injury into defensible numbers."),
]

PRACTICE_AREAS = [
    ("Personal Injury", "/practice-areas/personal-injury/",
     "Catastrophic and non-catastrophic injury cases for plaintiff and defense counsel."),
    ("Workers' Compensation", "/practice-areas/workers-compensation/",
     "Employability, transferable skills, and labor-market analysis for comp claims."),
    ("Employment Litigation", "/practice-areas/employment-litigation/",
     "Wage loss and earning capacity in wrongful termination and discrimination matters."),
    ("Family Law", "/practice-areas/family-law/",
     "Earning capacity and employability evaluations for support and imputation disputes."),
]

# --------------------------------------------------------------------------- #
#  HTML helpers
# --------------------------------------------------------------------------- #

def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def head(page):
    """Build the <head> for a page dict."""
    url = SITE["domain"] + page["path"]
    title = page["title"]
    desc = page["description"]
    canonical = url
    og_img = SITE["domain"] + "/assets/img/og-default.svg"

    json_ld = "\n".join(
        '<script type="application/ld+json">%s</script>' % j for j in page.get("schema", [])
    )

    breadcrumb_html = ""
    if page.get("breadcrumb"):
        items = []
        for i, (label, href) in enumerate(page["breadcrumb"], start=1):
            items.append(
                '{"@type":"ListItem","position":%d,"name":"%s","item":"%s"}'
                % (i, label, SITE["domain"] + href)
            )
        breadcrumb_html = (
            '<script type="application/ld+json">'
            '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[%s]}'
            "</script>" % ",".join(items)
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="author" content="{SITE['principal']}, {SITE['principal_creds']}">
<meta name="geo.region" content="US-MO">
<meta name="geo.placename" content="St. Louis, Missouri">
<meta name="geo.position" content="{SITE['geo_lat']};{SITE['geo_lng']}">
<meta name="ICBM" content="{SITE['geo_lat']}, {SITE['geo_lng']}">

<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(SITE['name'])}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{og_img}">

<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/favicon.svg">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="{SITE['theme']}">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/css/style.css">
{breadcrumb_html}
{json_ld}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""


def header(active):
    links = ""
    for label, href in NAV:
        cls = ' class="active"' if href == active or (href != "/" and active.startswith(href)) else ""
        links += f'<li><a href="{href}"{cls}>{label}</a></li>'
    return f"""
<header class="site-header" id="site-header">
  <div class="container header-inner">
    <a class="brand" href="/" aria-label="{SITE['name']} home">
      <span class="brand-mark" aria-hidden="true">PA</span>
      <span class="brand-text">
        <span class="brand-name">Purinton Analytics</span>
        <span class="brand-sub">Vocational Expert &amp; Life Care Planning</span>
      </span>
    </a>
    <nav class="main-nav" aria-label="Primary">
      <button class="nav-toggle" aria-expanded="false" aria-controls="nav-menu" aria-label="Toggle menu">
        <span></span><span></span><span></span>
      </button>
      <ul id="nav-menu">{links}
        <li class="nav-cta"><a href="/contact/" class="btn btn-sm">Request a Consultation</a></li>
      </ul>
    </nav>
  </div>
</header>
"""


def footer():
    svc = "".join(f'<li><a href="{h}">{n}</a></li>' for n, h, _ in SERVICES)
    pa = "".join(f'<li><a href="{h}">{n}</a></li>' for n, h, _ in PRACTICE_AREAS)
    return f"""
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-col footer-about">
      <span class="brand-name">Purinton Analytics, LLC</span>
      <p>Objective, defensible vocational expert and life care planning opinions for
         plaintiff and defense counsel across the United States and Canada.</p>
      <p class="footer-creds">{SITE['principal']}, {SITE['principal_creds']}</p>
      <a class="footer-linkedin" href="{SITE['linkedin']}" rel="noopener" target="_blank">LinkedIn &rarr;</a>
    </div>
    <div class="footer-col">
      <h3>Services</h3>
      <ul>{svc}</ul>
    </div>
    <div class="footer-col">
      <h3>Practice Areas</h3>
      <ul>{pa}</ul>
    </div>
    <div class="footer-col">
      <h3>Contact</h3>
      <ul class="footer-contact">
        <li><a href="tel:{SITE['phone_e164']}">{SITE['phone_display']}</a> <span>(office)</span></li>
        <li><a href="tel:{SITE['mobile_e164']}">{SITE['mobile_display']}</a> <span>(mobile)</span></li>
        <li><a href="mailto:{SITE['email']}">{SITE['email']}</a></li>
        <li class="footer-addr">{SITE['street']}<br>{SITE['city']}, {SITE['region']} {SITE['postal']}</li>
      </ul>
    </div>
  </div>
  <div class="container footer-bottom">
    <p>&copy; {BUILD_YEAR} Purinton Analytics, LLC. All rights reserved.</p>
    <p><a href="/sitemap.xml">Sitemap</a> &middot; <a href="/privacy/">Privacy</a></p>
  </div>
</footer>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
"""


def cta_band(heading="Discuss your case with a vocational expert",
             sub="Tell us about your matter and receive a candid assessment of how a vocational or life care planning opinion can support it."):
    return f"""
<section class="cta-band">
  <div class="container cta-inner">
    <div>
      <h2>{heading}</h2>
      <p>{sub}</p>
    </div>
    <div class="cta-actions">
      <a href="/contact/" class="btn btn-light">Request a Consultation</a>
      <a href="tel:{SITE['phone_e164']}" class="btn btn-ghost-light">{SITE['phone_display']}</a>
    </div>
  </div>
</section>
"""


def faq_block(title, faqs):
    """faqs = list of (question, answer_html). Returns section HTML + FAQPage schema."""
    items = ""
    for q, a in faqs:
        items += f"""
      <details class="faq-item">
        <summary>{q}</summary>
        <div class="faq-answer">{a}</div>
      </details>"""
    html = f"""
<section class="section faq-section">
  <div class="container narrow">
    <h2 class="section-title">{title}</h2>
    <div class="faq-list">{items}
    </div>
  </div>
</section>
"""
    schema_items = []
    for q, a in faqs:
        plain = re.sub("<[^>]+>", "", a).replace('"', "'").strip()
        plain = re.sub(r"\s+", " ", plain)
        schema_items.append(
            '{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'
            % (q.replace('"', "'"), plain)
        )
    schema = (
        '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}'
        % ",".join(schema_items)
    )
    return html, schema


def page_hero(eyebrow, h1, lead, primary=("Request a Consultation", "/contact/"),
              secondary=None, variant=""):
    sec = ""
    if secondary:
        sec = f'<a href="{secondary[1]}" class="btn btn-ghost">{secondary[0]}</a>'
    return f"""
<section class="page-hero {variant}">
  <div class="container">
    <p class="eyebrow">{eyebrow}</p>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    <div class="hero-actions">
      <a href="{primary[1]}" class="btn">{primary[0]}</a>
      {sec}
    </div>
  </div>
</section>
"""

# --------------------------------------------------------------------------- #
#  Reusable schema fragments
# --------------------------------------------------------------------------- #

def org_schema():
    return (
        '{"@context":"https://schema.org","@type":["ProfessionalService","LegalService"],'
        '"@id":"%s/#organization","name":"%s","alternateName":"Purinton Analytics",'
        '"url":"%s/","telephone":"%s","email":"%s","priceRange":"$$$",'
        '"image":"%s/assets/img/og-default.svg","logo":"%s/favicon.svg",'
        '"description":"Vocational expert and life care planning services providing objective, '
        'defensible evaluations of employability, earning capacity, wage loss, and future cost of '
        'care for plaintiff and defense attorneys nationwide.",'
        '"founder":{"@type":"Person","name":"%s","honorificSuffix":"%s"},'
        '"address":{"@type":"PostalAddress","streetAddress":"%s","addressLocality":"%s",'
        '"addressRegion":"%s","postalCode":"%s","addressCountry":"US"},'
        '"geo":{"@type":"GeoCoordinates","latitude":"%s","longitude":"%s"},'
        '"areaServed":[{"@type":"Country","name":"United States"},{"@type":"Country","name":"Canada"}],'
        '"sameAs":["%s"],'
        '"knowsAbout":["Vocational Evaluation","Earning Capacity Analysis","Wage Loss Analysis",'
        '"Life Care Planning","Vocational Rehabilitation","Forensic Vocational Assessment",'
        '"Transferable Skills Analysis","Labor Market Survey","Economic Damages"]}'
    ) % (
        SITE["domain"], SITE["name"], SITE["domain"], SITE["phone_e164"], SITE["email"],
        SITE["domain"], SITE["domain"], SITE["principal"], SITE["principal_creds"],
        SITE["street"], SITE["city"], SITE["region"], SITE["postal"],
        SITE["geo_lat"], SITE["geo_lng"], SITE["linkedin"],
    )


def person_schema():
    return (
        '{"@context":"https://schema.org","@type":"Person","@id":"%s/about/#person",'
        '"name":"%s","honorificSuffix":"%s","jobTitle":"Vocational Expert & Life Care Planner",'
        '"worksFor":{"@id":"%s/#organization"},"url":"%s/about/","sameAs":["%s"],'
        '"knowsAbout":["Vocational Evaluation","Earning Capacity","Life Care Planning",'
        '"Vocational Rehabilitation","Forensic Economics"],'
        '"hasCredential":['
        '{"@type":"EducationalOccupationalCredential","credentialCategory":"Licensed Professional Counselor (LPC)"},'
        '{"@type":"EducationalOccupationalCredential","credentialCategory":"Certified Rehabilitation Counselor (CRC)"},'
        '{"@type":"EducationalOccupationalCredential","credentialCategory":"Certified Vocational Evaluator (CVE)"},'
        '{"@type":"EducationalOccupationalCredential","credentialCategory":"Fellow, American Board of Vocational Experts (ABVE/F)"},'
        '{"@type":"EducationalOccupationalCredential","credentialCategory":"Forensic Vocational Expert (FVE)"},'
        '{"@type":"EducationalOccupationalCredential","credentialCategory":"International Psychometric Evaluator, Certified (IPEC)"}'
        ']}'
    ) % (SITE["domain"], SITE["principal"], SITE["principal_creds"], SITE["domain"],
         SITE["domain"], SITE["linkedin"])


def service_schema(name, desc, path):
    return (
        '{"@context":"https://schema.org","@type":"Service","name":"%s",'
        '"serviceType":"%s","url":"%s","description":"%s",'
        '"provider":{"@id":"%s/#organization"},'
        '"areaServed":[{"@type":"Country","name":"United States"},{"@type":"Country","name":"Canada"}],'
        '"audience":{"@type":"Audience","audienceType":"Attorneys and Insurers"}}'
    ) % (name, name, SITE["domain"] + path, desc.replace('"', "'"), SITE["domain"])


# --------------------------------------------------------------------------- #
#  Page bodies
# --------------------------------------------------------------------------- #

def icon(name):
    icons = {
        "scale": '<path d="M12 3v18M5 21h14M7 7l-3 7a3 3 0 006 0L7 7zm10 0l-3 7a3 3 0 006 0l-3-7zM12 6l5-1M12 6L7 5"/>',
        "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
        "clipboard": '<rect x="6" y="4" width="12" height="17" rx="2"/><path d="M9 4V3h6v1M9 11h6M9 15h4"/>',
        "route": '<circle cx="6" cy="18" r="2.5"/><circle cx="18" cy="6" r="2.5"/><path d="M8.5 18H14a4 4 0 000-8H9a4 4 0 010-8h.5"/>',
        "calc": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 12h2M14 12h2M8 16h2M14 16h2"/>',
        "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6l8-3z"/><path d="M9 12l2 2 4-4"/>',
        "doc": '<path d="M7 3h7l5 5v13a1 1 0 01-1 1H7a1 1 0 01-1-1V4a1 1 0 011-1z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
        "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-5 6-5s6 1.7 6 5M16 11a3 3 0 100-6M21 20c0-2.5-1.5-4-4-4.5"/>',
        "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.5 4 6 4 9s-1.5 6.5-4 9c-2.5-2.5-4-6-4-9s1.5-6.5 4-9z"/>',
        "check": '<circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/>',
    }
    return (f'<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true">{icons.get(name, icons["check"])}</svg>')


SERVICE_ICONS = {
    "/services/vocational-expert-witness/": "scale",
    "/services/earning-capacity-evaluation/": "chart",
    "/services/life-care-planning/": "clipboard",
    "/services/case-management/": "route",
    "/services/economic-damages/": "calc",
}
PRACTICE_ICONS = {
    "/practice-areas/personal-injury/": "shield",
    "/practice-areas/workers-compensation/": "doc",
    "/practice-areas/employment-litigation/": "users",
    "/practice-areas/family-law/": "scale",
}


def card_grid(items, icon_map=None):
    cards = ""
    for name, href, desc in items:
        ic = icon(icon_map.get(href, "check")) if icon_map else ""
        cards += f"""
      <a class="card" href="{href}">
        <span class="card-ico">{ic}</span>
        <h3>{name}</h3>
        <p>{desc}</p>
        <span class="card-link">Learn more &rarr;</span>
      </a>"""
    return f'<div class="card-grid">{cards}\n    </div>'


# ---- HOME ----------------------------------------------------------------- #

def home_body():
    creds = ["LPC", "CRC", "CVE", "ABVE/F", "FVE", "IPEC"]
    chips = "".join(f'<span class="chip">{c}</span>' for c in creds)
    stats = [
        ("2019", "Providing expert testimony in U.S. &amp; Canadian courts since"),
        ("2", "Sides served — retained by plaintiff and defense counsel alike"),
        ("100%", "Opinions grounded in objective, defensible methodology"),
    ]
    stat_html = "".join(
        f'<div class="stat"><span class="stat-num">{n}</span><span class="stat-label">{l}</span></div>'
        for n, l in stats
    )

    why = [
        ("scale", "Objective &amp; defensible", "Every opinion is built on accepted methodology and the published data that holds up under cross-examination."),
        ("globe", "Plaintiff &amp; defense, nationwide", "Retained on both sides of the aisle in civil litigation across the United States and Canada."),
        ("doc", "Litigation-ready reports", "Clear, well-supported written opinions that translate complex vocational and medical facts for judges and juries."),
        ("users", "A single, accountable expert", "You work directly with Jason Purinton from intake through testimony — not a rotating roster."),
    ]
    why_html = ""
    for ic, t, d in why:
        why_html += f'<div class="feature"><span class="feature-ico">{icon(ic)}</span><div><h3>{t}</h3><p>{d}</p></div></div>'

    faq_html, faq_schema = faq_block(
        "Frequently asked questions",
        [
            ("What does a vocational expert do?",
             "<p>A vocational expert evaluates a person's ability to work and earn following an injury, illness, or other life event. The expert analyzes medical records, education, work history, transferable skills, and the local labor market to form an objective opinion on employability and earning capacity — opinions that are used as evidence in personal injury, workers' compensation, employment, and family law matters.</p>"),
            ("What is a life care plan?",
             "<p>A life care plan is a comprehensive, evidence-based document that projects the future medical and non-medical needs of an individual with a catastrophic or chronic injury, along with the associated costs. It gives attorneys, courts, and families a defensible roadmap of the care required over a lifetime.</p>"),
            ("Do you work for plaintiffs or defendants?",
             "<p>Both. Purinton Analytics is retained by both plaintiff and defense counsel. Our methodology and conclusions are the same regardless of who retains us — the goal is an objective, defensible opinion, not an advocacy position.</p>"),
            ("What geographic areas do you serve?",
             "<p>We provide vocational expert and life care planning services for cases throughout the United States and Canada. Remote evaluation and testimony are available, and the firm is based in St. Louis, Missouri.</p>"),
            ("How do I retain Purinton Analytics for a case?",
             f"<p>Call {SITE['phone_display']} or send your case details through our <a href='/contact/'>contact form</a>. We will discuss the issues, confirm there is no conflict, and outline the scope, timeline, and fee structure before any work begins.</p>"),
        ],
    )

    body = f"""
<section class="hero">
  <div class="container hero-grid">
    <div class="hero-copy">
      <p class="eyebrow">Forensic Vocational &amp; Life Care Planning Experts</p>
      <h1>Objective vocational expert &amp; life care planning opinions that hold up in court</h1>
      <p class="lead">Purinton Analytics provides attorneys and insurers with defensible evaluations of
        employability, earning capacity, wage loss, and future cost of care — for plaintiff and defense
        matters across the United States and Canada.</p>
      <div class="hero-actions">
        <a href="/contact/" class="btn">Request a Consultation</a>
        <a href="/services/" class="btn btn-ghost">Explore Services</a>
      </div>
      <div class="hero-chips">{chips}</div>
    </div>
    <aside class="hero-card" aria-label="About the expert">
      <div class="hero-card-top">
        <span class="hero-avatar" aria-hidden="true">JP</span>
        <div>
          <span class="hero-card-name">{SITE['principal']}</span>
          <span class="hero-card-role">Principal Vocational Expert &amp; Life Care Planner</span>
        </div>
      </div>
      <p>Licensed counselor and board-certified vocational expert providing expert opinions and
         testimony in civil litigation since 2019.</p>
      <ul class="hero-card-list">
        <li>{icon('check')} Fellow, American Board of Vocational Experts</li>
        <li>{icon('check')} Certified Rehabilitation Counselor &amp; Vocational Evaluator</li>
        <li>{icon('check')} Retained nationwide, plaintiff &amp; defense</li>
      </ul>
      <a href="/about/" class="card-link">Meet Jason &rarr;</a>
    </aside>
  </div>
</section>

<section class="stats-band">
  <div class="container stats-grid">{stat_html}</div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">What we do</p>
      <h2 class="section-title">Expert services built for litigation</h2>
      <p class="section-intro">From the first evaluation to testimony at trial, every engagement is
        designed to produce clear, well-supported opinions that withstand scrutiny.</p>
    </div>
    {card_grid(SERVICES, SERVICE_ICONS)}
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">Why Purinton Analytics</p>
      <h2 class="section-title">Experience attorneys can build a case on</h2>
    </div>
    <div class="feature-grid">{why_html}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">Where we help</p>
      <h2 class="section-title">Practice areas</h2>
      <p class="section-intro">Vocational and life care planning opinions tailored to the standards and
        burden of proof in each area of law.</p>
    </div>
    {card_grid(PRACTICE_AREAS, PRACTICE_ICONS)}
  </div>
</section>

{faq_html}
{cta_band()}
"""
    return body, [org_schema(), person_schema(), faq_schema]


# ---- ABOUT ---------------------------------------------------------------- #

def about_body():
    creds = [
        ("Licensed Professional Counselor", "LPC"),
        ("Certified Rehabilitation Counselor", "CRC"),
        ("Certified Vocational Evaluator", "CVE"),
        ("Fellow, American Board of Vocational Experts", "ABVE/F"),
        ("Forensic Vocational Expert", "FVE"),
        ("International Psychometric Evaluator, Certified", "IPEC"),
    ]
    cred_html = "".join(
        f'<li><span class="cred-abbr">{ab}</span><span class="cred-full">{full}</span></li>'
        for full, ab in creds
    )
    edu = [
        ("M.S., Counseling", "Emporia State University"),
        ("B.S., Nursing", "MidAmerica Nazarene University"),
        ("B.S., Business", "University of Kansas"),
    ]
    edu_html = "".join(f'<li><strong>{d}</strong><span>{s}</span></li>' for d, s in edu)

    faq_html, faq_schema = faq_block(
        "About the practice",
        [
            ("What makes a vocational opinion defensible?",
             "<p>A defensible opinion is transparent and reproducible: it relies on accepted assessment methods, documented data sources, and clearly stated assumptions, so that another qualified expert reviewing the same records would reach a consistent conclusion. That discipline is what allows an opinion to survive cross-examination and <em>Daubert</em> or <em>Frye</em> challenges.</p>"),
            ("Will the same expert handle my case from start to finish?",
             "<p>Yes. Jason Purinton personally handles each engagement — from records review and evaluation through report writing, deposition, and trial testimony.</p>"),
            ("Do you provide deposition and trial testimony?",
             "<p>Yes. Purinton Analytics has provided expert opinions and testimony in civil litigation across the United States and Canada since 2019, in both deposition and trial settings.</p>"),
        ],
    )

    body = f"""
{page_hero("About", "Jason C. Purinton, " + SITE['principal_creds'],
           "A licensed counselor and board-certified vocational expert helping attorneys translate "
           "injury, disability, and loss into objective, defensible opinions.",
           secondary=("View Credentials", "#credentials"))}

<section class="section">
  <div class="container split">
    <div class="split-main">
      <h2>Background</h2>
      <p>Jason Purinton is the principal of Purinton Analytics, LLC, a forensic vocational and life
        care planning practice serving attorneys and insurers nationwide. He provides objective
        evaluations of employability and earning capacity, comprehensive life care plans, and expert
        testimony in civil litigation.</p>
      <p>The firm was founded in {SITE['founded']} as Vocational Pros, LLC and was rebranded in 2024 as
        Purinton Analytics to reflect a broader range of analytical services. Since 2019, Jason has
        provided expert opinions and testimony in cases across the United States and Canada, retained
        by both plaintiff and defense counsel.</p>
      <p>His clinical background as a licensed counselor and registered nurse, combined with
        board-level certification in vocational evaluation, allows him to connect medical evidence,
        functional capacity, and real-world labor-market data into opinions that are both clinically
        grounded and legally defensible.</p>

      <h2 id="credentials">Credentials &amp; certifications</h2>
      <ul class="cred-list">{cred_html}</ul>

      <h2>Education</h2>
      <ul class="edu-list">{edu_html}</ul>

      <h2>Professional focus</h2>
      <ul class="check-list">
        <li>{icon('check')} Vocational expert evaluations of employability and earning capacity</li>
        <li>{icon('check')} Transferable skills analysis and labor-market research</li>
        <li>{icon('check')} Wage loss and lost earning capacity analysis</li>
        <li>{icon('check')} Life care planning for catastrophic and non-catastrophic injury</li>
        <li>{icon('check')} Vocational rehabilitation and medical case management</li>
        <li>{icon('check')} Expert reports, deposition, and trial testimony</li>
      </ul>
    </div>
    <aside class="split-aside">
      <div class="aside-card">
        <h3>At a glance</h3>
        <dl class="aside-dl">
          <dt>Principal</dt><dd>{SITE['principal']}</dd>
          <dt>Credentials</dt><dd>{SITE['principal_creds']}</dd>
          <dt>Testifying since</dt><dd>2019</dd>
          <dt>Engagements</dt><dd>Plaintiff &amp; defense</dd>
          <dt>Service area</dt><dd>United States &amp; Canada</dd>
          <dt>Based in</dt><dd>St. Louis, Missouri</dd>
        </dl>
        <a href="/contact/" class="btn btn-block">Request a Consultation</a>
        <a href="{SITE['linkedin']}" class="card-link" rel="noopener" target="_blank">Connect on LinkedIn &rarr;</a>
      </div>
    </aside>
  </div>
</section>

{faq_html}
{cta_band()}
"""
    return body, [person_schema(), org_schema(), faq_schema]


# ---- SERVICES INDEX ------------------------------------------------------- #

def services_index_body():
    body = f"""
{page_hero("Services", "Vocational expert &amp; life care planning services",
           "Objective, litigation-ready analysis across the full arc of a damages case — from "
           "employability and earning capacity to the lifetime cost of care.")}
<section class="section">
  <div class="container">
    {card_grid(SERVICES, SERVICE_ICONS)}
  </div>
</section>
{cta_band()}
"""
    schema = (
        '{"@context":"https://schema.org","@type":"ItemList","itemListElement":[%s]}'
        % ",".join(
            '{"@type":"ListItem","position":%d,"name":"%s","url":"%s"}' % (i, n, SITE["domain"] + h)
            for i, (n, h, _) in enumerate(SERVICES, 1)
        )
    )
    return body, [org_schema(), schema]


# ---- PRACTICE AREAS INDEX ------------------------------------------------- #

def practice_index_body():
    body = f"""
{page_hero("Practice Areas", "Where vocational &amp; life care evidence makes the difference",
           "Tailored vocational and life care planning opinions for the cases where lost earning "
           "capacity and future care costs drive the value of the claim.")}
<section class="section">
  <div class="container">
    {card_grid(PRACTICE_AREAS, PRACTICE_ICONS)}
  </div>
</section>
{cta_band()}
"""
    return body, [org_schema()]


# ---- GENERIC SERVICE / PRACTICE DETAIL ------------------------------------ #

def detail_body(cfg):
    """Generic detail page: hero + overview + 'what's included' + process + faqs + cta."""
    incl = "".join(
        f'<li>{icon("check")}<div><strong>{t}</strong><p>{d}</p></div></li>'
        for t, d in cfg["included"]
    )
    process = ""
    for i, (t, d) in enumerate(cfg["process"], 1):
        process += f'<li><span class="step-n">{i}</span><div><h3>{t}</h3><p>{d}</p></div></li>'

    related = cfg.get("related", [])
    related_html = ""
    if related:
        rc = "".join(f'<a class="pill" href="{h}">{n}</a>' for n, h in related)
        related_html = f"""
<section class="section section-alt">
  <div class="container narrow center">
    <h2 class="section-title">Related services &amp; practice areas</h2>
    <div class="pill-row">{rc}</div>
  </div>
</section>"""

    faq_html, faq_schema = faq_block("Frequently asked questions", cfg["faqs"])

    overview_paras = "".join(f"<p>{p}</p>" for p in cfg["overview"])

    body = f"""
{page_hero(cfg["eyebrow"], cfg["h1"], cfg["lead"])}

<section class="section">
  <div class="container split">
    <div class="split-main">
      <h2>Overview</h2>
      {overview_paras}
      <h2>{cfg.get("included_title", "What's included")}</h2>
      <ul class="incl-list">{incl}</ul>
    </div>
    <aside class="split-aside">
      <div class="aside-card">
        <h3>{cfg.get("aside_title", "Engagement details")}</h3>
        <dl class="aside-dl">{"".join(f"<dt>{d}</dt><dd>{v}</dd>" for d, v in cfg["aside"])}</dl>
        <a href="/contact/" class="btn btn-block">Discuss Your Case</a>
        <a href="tel:{SITE['phone_e164']}" class="card-link">{SITE['phone_display']} &rarr;</a>
      </div>
    </aside>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">How it works</p>
      <h2 class="section-title">{cfg.get("process_title", "A clear, defensible process")}</h2>
    </div>
    <ol class="steps">{process}</ol>
  </div>
</section>

{faq_html}
{related_html}
{cta_band()}
"""
    schema = [org_schema(), service_schema(cfg["schema_name"], cfg["lead"], cfg["path"]), faq_schema]
    return body, schema


# --------------------------------------------------------------------------- #
#  Detail page content
# --------------------------------------------------------------------------- #

DETAILS = {
    "/services/vocational-expert-witness/": {
        "eyebrow": "Service",
        "h1": "Vocational expert witness services",
        "lead": "Objective, defensible evaluations of employability and earning capacity — and "
                "credible expert testimony — for plaintiff and defense counsel nationwide.",
        "schema_name": "Vocational Expert Witness Evaluation",
        "overview": [
            "A vocational expert evaluates whether — and at what level — an individual can work and "
            "earn following an injury, illness, or other disabling event. At Purinton Analytics, that "
            "evaluation integrates medical evidence, functional capacity, education, work history, "
            "transferable skills, and current labor-market data into a single, well-supported opinion.",
            "Whether you are establishing or rebutting a damages claim, the analysis is built the same "
            "way: on accepted methodology and documented data, so the opinion stands up under "
            "cross-examination and Daubert or Frye scrutiny.",
        ],
        "included": [
            ("Employability assessment", "An objective determination of the occupations a person can realistically perform given their limitations."),
            ("Transferable skills analysis", "Identification of skills from past work that transfer to other jobs in the current economy."),
            ("Labor market survey", "Research into the availability, wages, and requirements of suitable jobs in the relevant geographic market."),
            ("Earning capacity opinion", "A reasoned opinion on pre- and post-event earning capacity and the resulting loss."),
            ("Vocational rehabilitation analysis", "Assessment of the retraining, education, or accommodation needed to return to work."),
            ("Expert report & testimony", "A clear written report supported by deposition and trial testimony."),
        ],
        "process": [
            ("Records review", "We review medical records, vocational history, depositions, and relevant financial documents."),
            ("Evaluation & interview", "When appropriate, we conduct a clinical vocational interview and standardized testing."),
            ("Analysis", "We apply transferable skills analysis and labor-market research to the documented facts."),
            ("Report", "We deliver a clear, defensible written opinion with sources and assumptions stated."),
            ("Testimony", "We support the opinion through deposition and trial testimony as needed."),
        ],
        "aside": [("Used by", "Plaintiff &amp; defense"), ("Deliverable", "Written report &amp; testimony"),
                  ("Service area", "U.S. &amp; Canada"), ("Turnaround", "Case-dependent")],
        "faqs": [
            ("When should I retain a vocational expert?",
             "<p>As early as practical. Engaging a vocational expert during discovery allows time for a thorough evaluation, informs settlement valuation, and ensures the opinion is fully developed before disclosure deadlines.</p>"),
            ("What is the difference between employability and earning capacity?",
             "<p>Employability addresses whether a person can work and which jobs they can perform; earning capacity addresses how much they can reasonably be expected to earn. A complete vocational opinion typically addresses both.</p>"),
            ("Can you rebut an opposing vocational expert?",
             "<p>Yes. We provide rebuttal analysis that evaluates the methodology, data, and assumptions of an opposing expert and identifies where conclusions are not supported by the record.</p>"),
        ],
        "related": [("Earning Capacity & Wage Loss", "/services/earning-capacity-evaluation/"),
                    ("Personal Injury", "/practice-areas/personal-injury/"),
                    ("Workers' Compensation", "/practice-areas/workers-compensation/")],
    },

    "/services/earning-capacity-evaluation/": {
        "eyebrow": "Service",
        "h1": "Earning capacity & wage loss analysis",
        "lead": "Quantified, defensible opinions on lost earning capacity and wage loss that translate "
                "an injury into numbers a court can rely on.",
        "schema_name": "Earning Capacity and Wage Loss Analysis",
        "overview": [
            "Lost earning capacity is frequently the largest element of economic damages in an injury "
            "or employment case — and the most contested. Purinton Analytics establishes pre-injury "
            "earning capacity, post-injury earning capacity, and the difference between them, grounded "
            "in the individual's vocational profile and the realities of the labor market.",
            "The analysis distinguishes actual wage loss from the broader concept of lost earning "
            "capacity, and provides the vocational foundation an economist needs to project losses "
            "over a worklife.",
        ],
        "included": [
            ("Pre-event earning capacity", "Establishment of the individual's earning capacity before the injury or loss."),
            ("Post-event earning capacity", "A reasoned opinion on what the individual can earn given current limitations."),
            ("Wage loss quantification", "The measurable gap between pre- and post-event earning capacity."),
            ("Worklife considerations", "Vocational input on retirement age, labor-force participation, and work tolerance."),
            ("Mitigation analysis", "Assessment of the individual's realistic options to reduce their loss."),
            ("Foundation for economists", "Vocational findings packaged to support economic damages testimony."),
        ],
        "process": [
            ("Profile development", "We document education, training, work history, and earnings."),
            ("Capacity assessment", "We evaluate functional limitations against occupational demands."),
            ("Labor-market research", "We research wages and job availability in the relevant market."),
            ("Quantification", "We calculate the difference between pre- and post-event capacity."),
            ("Report & support", "We deliver findings and coordinate with economic experts as needed."),
        ],
        "aside": [("Best paired with", "Economic Damages"), ("Deliverable", "Earning capacity opinion"),
                  ("Used by", "Plaintiff &amp; defense"), ("Service area", "U.S. &amp; Canada")],
        "faqs": [
            ("What is the difference between wage loss and lost earning capacity?",
             "<p>Wage loss is the actual income a person has lost; lost earning capacity is the diminished ability to earn going forward, whether or not the person is currently working. Earning capacity is the broader, forward-looking measure used in most damages analyses.</p>"),
            ("Do you work with economic experts?",
             "<p>Yes. Our vocational findings on earning capacity provide the foundation an economist uses to project losses to present value over the individual's worklife.</p>"),
            ("Can earning capacity be analyzed for someone with no work history?",
             "<p>Yes. For students, homemakers, or young claimants, earning capacity is established using education, aptitudes, labor-market data, and statistical earnings for comparable individuals.</p>"),
        ],
        "related": [("Vocational Expert Witness", "/services/vocational-expert-witness/"),
                    ("Economic Damages", "/services/economic-damages/"),
                    ("Employment Litigation", "/practice-areas/employment-litigation/")],
    },

    "/services/life-care-planning/": {
        "eyebrow": "Service",
        "h1": "Life care planning",
        "lead": "Comprehensive, evidence-based life care plans that project the future medical and "
                "support needs — and costs — of individuals with catastrophic or chronic injuries.",
        "schema_name": "Life Care Planning",
        "overview": [
            "A life care plan is a dynamic, comprehensive document that maps the future care a person "
            "will need as a result of a catastrophic or chronic injury, together with the cost of that "
            "care over their lifetime. It gives attorneys, courts, and families a defensible roadmap "
            "for medical and non-medical needs.",
            "Purinton Analytics builds life care plans on accepted standards of practice — grounded in "
            "the medical record, treating-provider recommendations, and researched local costs — so "
            "the plan reflects genuine need and withstands scrutiny in catastrophic and "
            "non-catastrophic cases alike.",
        ],
        "included_title": "What a life care plan covers",
        "included": [
            ("Medical & surgical care", "Projected physician, surgical, and specialist needs over the lifespan."),
            ("Therapies & rehabilitation", "Physical, occupational, speech, and behavioral therapy needs."),
            ("Medications & supplies", "Ongoing prescription, equipment, and supply requirements."),
            ("Durable medical equipment", "Wheelchairs, prosthetics, orthotics, and replacement schedules."),
            ("Home & attendant care", "Personal care, nursing, and home modification needs."),
            ("Researched costs", "Current, geographically appropriate costs for every recommended item."),
        ],
        "process": [
            ("Records & intake", "We review the complete medical record and case materials."),
            ("Provider input", "We incorporate treating-provider recommendations and, where needed, clinical interview."),
            ("Needs assessment", "We identify each future care need supported by the record."),
            ("Cost research", "We research current costs in the individual's geographic area."),
            ("Plan & testimony", "We deliver a comprehensive plan and support it through testimony."),
        ],
        "aside": [("Applies to", "Catastrophic &amp; chronic injury"), ("Deliverable", "Comprehensive life care plan"),
                  ("Standards", "Accepted LCP methodology"), ("Service area", "U.S. &amp; Canada")],
        "faqs": [
            ("What is the purpose of a life care plan?",
             "<p>A life care plan establishes the future care an injured person will need and what that care will cost, providing a defensible basis for damages in litigation and a practical guide for the family and care team.</p>"),
            ("When is a life care plan needed?",
             "<p>Life care plans are most common in catastrophic injury cases — such as spinal cord injury, traumatic brain injury, amputation, or severe burns — but they are also valuable in chronic and non-catastrophic injury claims where ongoing care is required.</p>"),
            ("Is the plan based on the treating physicians' recommendations?",
             "<p>Yes. A defensible life care plan is grounded in the medical record and the recommendations of treating providers, supplemented by accepted standards of practice and researched costs.</p>"),
        ],
        "related": [("Economic Damages", "/services/economic-damages/"),
                    ("Case Management", "/services/case-management/"),
                    ("Personal Injury", "/practice-areas/personal-injury/")],
    },

    "/services/case-management/": {
        "eyebrow": "Service",
        "h1": "Vocational rehabilitation & medical case management",
        "lead": "Coordinated, clinically informed case management that keeps recovery and return-to-work "
                "on track — and documents the process along the way.",
        "schema_name": "Vocational Rehabilitation and Medical Case Management",
        "overview": [
            "Effective case management aligns medical treatment, rehabilitation, and return-to-work "
            "goals so an injured individual recovers as fully and efficiently as possible. Drawing on a "
            "clinical counseling and nursing background, Purinton Analytics coordinates care, monitors "
            "progress, and identifies the services needed to restore function and employability.",
            "Thorough documentation of the rehabilitation process also produces a clear record that "
            "supports vocational and life care planning opinions when a case proceeds to litigation.",
        ],
        "included": [
            ("Care coordination", "Coordination among treating providers, therapists, and employers."),
            ("Return-to-work planning", "Development of realistic, medically supported return-to-work goals."),
            ("Rehabilitation planning", "Identification of retraining, accommodation, and support services."),
            ("Progress monitoring", "Ongoing tracking of recovery and treatment milestones."),
            ("Resource identification", "Connection to community, vocational, and medical resources."),
            ("Documentation", "A clear record of services that supports later vocational analysis."),
        ],
        "process": [
            ("Assessment", "We assess medical status, functional capacity, and vocational goals."),
            ("Plan", "We build a coordinated rehabilitation and return-to-work plan."),
            ("Coordinate", "We align providers, services, and stakeholders around the plan."),
            ("Monitor", "We track progress and adjust the plan as recovery evolves."),
            ("Report", "We document outcomes for the case file or litigation."),
        ],
        "aside": [("Background", "Counseling &amp; nursing"), ("Deliverable", "Coordinated care plan"),
                  ("Supports", "Return-to-work goals"), ("Service area", "U.S. &amp; Canada")],
        "faqs": [
            ("How does case management support a litigation case?",
             "<p>Beyond improving recovery, case management produces a documented record of treatment, services, and outcomes that strengthens the foundation for vocational and life care planning opinions.</p>"),
            ("Who benefits from vocational rehabilitation case management?",
             "<p>Injured workers, personal injury claimants, and insurers all benefit from coordinated care that restores function and supports a realistic return to work.</p>"),
        ],
        "related": [("Life Care Planning", "/services/life-care-planning/"),
                    ("Vocational Expert Witness", "/services/vocational-expert-witness/"),
                    ("Workers' Compensation", "/practice-areas/workers-compensation/")],
    },

    "/services/economic-damages/": {
        "eyebrow": "Service",
        "h1": "Economic damages analysis",
        "lead": "Clear calculation of the economic loss flowing from injury or loss — the vocational and "
                "cost foundation that turns harm into defensible numbers.",
        "schema_name": "Economic Damages Analysis",
        "overview": [
            "Economic damages quantify the financial harm caused by an injury, wrongful termination, or "
            "death — lost earnings, lost earning capacity, lost benefits, and the cost of future care. "
            "Purinton Analytics provides the vocational and life care foundation those calculations "
            "depend on, presented so attorneys and economists can build a complete damages model.",
            "By tying every figure to documented vocational findings and researched costs, the damages "
            "analysis remains transparent, reproducible, and defensible at trial.",
        ],
        "included": [
            ("Lost earnings & earning capacity", "Vocational basis for past and future income loss."),
            ("Future cost of care", "Life care plan costs structured for economic projection."),
            ("Lost benefits", "Identification of benefits tied to lost employment."),
            ("Mitigation & offsets", "Vocational input on residual earning capacity and offsets."),
            ("Coordination with economists", "Findings packaged to support economic present-value analysis."),
            ("Defensible documentation", "Sources and assumptions stated for every figure."),
        ],
        "process": [
            ("Define the loss", "We identify each category of economic damage at issue."),
            ("Build the vocational foundation", "We establish earning capacity and care needs."),
            ("Research costs", "We document current wages and care costs."),
            ("Coordinate", "We work with economists to project losses to present value."),
            ("Support", "We support the analysis through report and testimony."),
        ],
        "aside": [("Foundation for", "Damages models"), ("Deliverable", "Vocational &amp; cost basis"),
                  ("Used by", "Plaintiff &amp; defense"), ("Service area", "U.S. &amp; Canada")],
        "faqs": [
            ("What economic damages can a vocational expert support?",
             "<p>A vocational expert provides the foundation for lost earnings, lost earning capacity, and the future cost of care — the elements that typically drive economic damages in injury, employment, and wrongful-death cases.</p>"),
            ("Do you replace an economist?",
             "<p>No. We provide the vocational and life care foundation; a forensic economist projects those figures to present value. We routinely coordinate with economic experts to deliver a complete, consistent damages model.</p>"),
        ],
        "related": [("Earning Capacity & Wage Loss", "/services/earning-capacity-evaluation/"),
                    ("Life Care Planning", "/services/life-care-planning/"),
                    ("Personal Injury", "/practice-areas/personal-injury/")],
    },

    "/practice-areas/personal-injury/": {
        "eyebrow": "Practice Area",
        "h1": "Personal injury",
        "lead": "Vocational and life care planning opinions that establish the true cost of catastrophic "
                "and non-catastrophic injuries — for plaintiff and defense counsel.",
        "schema_name": "Personal Injury Vocational & Life Care Services",
        "overview": [
            "In personal injury litigation, the value of a claim often turns on lost earning capacity "
            "and the future cost of care. Purinton Analytics helps attorneys establish — or test — both, "
            "with objective evaluations grounded in the medical record and labor-market data.",
            "From traumatic brain and spinal cord injuries to orthopedic and soft-tissue claims, we "
            "provide vocational evaluations, life care plans, and the foundation for economic damages, "
            "tailored to the burden of proof in personal injury cases.",
        ],
        "included_title": "How we help in personal injury cases",
        "included": [
            ("Earning capacity opinions", "Pre- and post-injury earning capacity and quantified loss."),
            ("Life care plans", "Comprehensive future-care cost projections for serious injuries."),
            ("Employability analysis", "Objective findings on the claimant's ability to return to work."),
            ("Rebuttal analysis", "Critical review of opposing vocational and life care opinions."),
            ("Damages foundation", "Vocational and cost findings to support economic experts."),
            ("Testimony", "Clear deposition and trial testimony."),
        ],
        "process": [
            ("Intake & conflict check", "We confirm scope and screen for conflicts."),
            ("Records review", "We analyze medical, vocational, and financial records."),
            ("Evaluation", "We assess employability, earning capacity, and care needs."),
            ("Report", "We deliver a defensible written opinion."),
            ("Testimony", "We support the opinion through trial."),
        ],
        "aside": [("Case types", "Catastrophic &amp; non-catastrophic"), ("Used by", "Plaintiff &amp; defense"),
                  ("Deliverables", "Vocational &amp; life care opinions"), ("Service area", "U.S. &amp; Canada")],
        "faqs": [
            ("What vocational evidence matters most in a personal injury case?",
             "<p>Objective opinions on whether the claimant can return to work, what they can earn, and what future care will cost — each tied to the medical record and labor-market data — typically have the greatest impact on damages.</p>"),
            ("Do you handle both catastrophic and minor injury cases?",
             "<p>Yes. We provide life care plans and earning capacity analyses for catastrophic injuries and vocational opinions for non-catastrophic injuries where return-to-work and wage loss are at issue.</p>"),
        ],
        "related": [("Life Care Planning", "/services/life-care-planning/"),
                    ("Vocational Expert Witness", "/services/vocational-expert-witness/"),
                    ("Economic Damages", "/services/economic-damages/")],
    },

    "/practice-areas/workers-compensation/": {
        "eyebrow": "Practice Area",
        "h1": "Workers' compensation",
        "lead": "Employability, transferable skills, and labor-market analysis that addresses the "
                "vocational questions at the heart of workers' compensation claims.",
        "schema_name": "Workers' Compensation Vocational Services",
        "overview": [
            "Workers' compensation disputes frequently turn on vocational questions: Can the injured "
            "worker return to their job? To any job? What can they earn now? Purinton Analytics provides "
            "the objective vocational analysis needed to answer those questions for employers, insurers, "
            "and injured workers.",
            "Through transferable skills analysis, labor-market surveys, and earning capacity opinions, "
            "we help quantify wage loss and identify realistic return-to-work and retraining options.",
        ],
        "included_title": "How we help in workers' compensation",
        "included": [
            ("Employability evaluation", "Whether the worker can return to past or alternative work."),
            ("Transferable skills analysis", "Skills that transfer to suitable available occupations."),
            ("Labor market survey", "Availability and wages of suitable jobs in the worker's area."),
            ("Earning capacity & wage loss", "Quantified loss of earning capacity."),
            ("Vocational rehabilitation", "Retraining and return-to-work recommendations."),
            ("Testimony", "Support at hearing and deposition."),
        ],
        "process": [
            ("Referral & records", "We review the claim file and medical restrictions."),
            ("Skills analysis", "We identify transferable skills and suitable occupations."),
            ("Market research", "We survey the local labor market for suitable jobs."),
            ("Opinion", "We deliver employability and earning capacity findings."),
            ("Testimony", "We testify at hearing or deposition as needed."),
        ],
        "aside": [("Used by", "Employers, insurers &amp; workers"), ("Deliverables", "Employability &amp; TSA"),
                  ("Focus", "Return-to-work &amp; wage loss"), ("Service area", "U.S. &amp; Canada")],
        "faqs": [
            ("What is a transferable skills analysis?",
             "<p>A transferable skills analysis identifies the skills a worker has acquired and matches them to other occupations the worker can perform within their medical restrictions — a central question in workers' compensation.</p>"),
            ("What is a labor market survey?",
             "<p>A labor market survey researches whether suitable jobs actually exist in the worker's geographic area, including their availability, requirements, and wages, to support an earning capacity opinion.</p>"),
        ],
        "related": [("Vocational Expert Witness", "/services/vocational-expert-witness/"),
                    ("Earning Capacity & Wage Loss", "/services/earning-capacity-evaluation/"),
                    ("Case Management", "/services/case-management/")],
    },

    "/practice-areas/employment-litigation/": {
        "eyebrow": "Practice Area",
        "h1": "Employment litigation",
        "lead": "Earning capacity, wage loss, and mitigation analysis for wrongful termination, "
                "discrimination, and other employment disputes.",
        "schema_name": "Employment Litigation Vocational Services",
        "overview": [
            "In employment cases, damages often hinge on what the plaintiff lost and what they could "
            "reasonably have earned through diligent job search. Purinton Analytics provides objective "
            "earning capacity, wage loss, and mitigation analysis for both plaintiff and defense.",
            "We evaluate the plaintiff's vocational profile, the relevant labor market, and the "
            "reasonableness of mitigation efforts, producing opinions that withstand scrutiny in "
            "wrongful termination, discrimination, and retaliation matters.",
        ],
        "included_title": "How we help in employment cases",
        "included": [
            ("Earning capacity analysis", "What the plaintiff could earn pre- and post-separation."),
            ("Wage loss quantification", "Back-pay and front-pay vocational foundation."),
            ("Mitigation analysis", "Whether job-search efforts were reasonable and diligent."),
            ("Labor market research", "Comparable job availability and wages."),
            ("Rebuttal analysis", "Review of opposing vocational opinions."),
            ("Testimony", "Deposition and trial support."),
        ],
        "process": [
            ("Records review", "We review employment, earnings, and case records."),
            ("Profile & market", "We assess the plaintiff's profile and labor market."),
            ("Mitigation review", "We evaluate the reasonableness of job-search efforts."),
            ("Opinion", "We quantify wage loss and earning capacity."),
            ("Testimony", "We support the opinion in deposition and at trial."),
        ],
        "aside": [("Case types", "Termination, discrimination"), ("Used by", "Plaintiff &amp; defense"),
                  ("Focus", "Wage loss &amp; mitigation"), ("Service area", "U.S. &amp; Canada")],
        "faqs": [
            ("How is mitigation of damages evaluated?",
             "<p>We assess whether the plaintiff made reasonable, diligent efforts to find comparable employment, based on their vocational profile and the availability of suitable jobs in the relevant market.</p>"),
            ("What is the vocational role in back-pay and front-pay?",
             "<p>The vocational expert establishes what the plaintiff could reasonably earn over time, providing the foundation that supports or limits back-pay and front-pay calculations.</p>"),
        ],
        "related": [("Earning Capacity & Wage Loss", "/services/earning-capacity-evaluation/"),
                    ("Economic Damages", "/services/economic-damages/"),
                    ("Vocational Expert Witness", "/services/vocational-expert-witness/")],
    },

    "/practice-areas/family-law/": {
        "eyebrow": "Practice Area",
        "h1": "Family law",
        "lead": "Objective earning capacity and employability evaluations for support, alimony, and "
                "income-imputation disputes.",
        "schema_name": "Family Law Vocational Services",
        "overview": [
            "In family law, the question of what a spouse can earn — not just what they do earn — often "
            "drives support and maintenance awards. Purinton Analytics provides neutral, objective "
            "earning capacity and employability evaluations to inform income imputation.",
            "We evaluate education, work history, skills, and the local labor market to opine on a "
            "party's realistic earning capacity, supporting fair and defensible support determinations.",
        ],
        "included_title": "How we help in family law matters",
        "included": [
            ("Earning capacity evaluation", "A party's realistic ability to earn given their profile."),
            ("Employability assessment", "Suitable occupations and the path to them."),
            ("Income imputation support", "Vocational basis for imputing income."),
            ("Re-entry analysis", "Retraining or education needed to re-enter the workforce."),
            ("Labor market research", "Wages and availability of suitable local jobs."),
            ("Testimony", "Clear, neutral testimony for the court."),
        ],
        "process": [
            ("Engagement", "We confirm scope and neutrality."),
            ("Evaluation", "We assess education, history, and skills."),
            ("Market research", "We research suitable local employment."),
            ("Opinion", "We opine on realistic earning capacity."),
            ("Testimony", "We support the opinion in court."),
        ],
        "aside": [("Matters", "Support &amp; imputation"), ("Stance", "Neutral &amp; objective"),
                  ("Deliverable", "Earning capacity opinion"), ("Service area", "U.S. &amp; Canada")],
        "faqs": [
            ("What is income imputation?",
             "<p>Income imputation is the court's assignment of income to a party based on their earning capacity rather than actual earnings. A vocational expert provides the objective basis for what that party could reasonably earn.</p>"),
            ("Can you evaluate a spouse who has been out of the workforce?",
             "<p>Yes. We assess prior education and experience, the impact of time out of the workforce, and the retraining or job search needed to re-enter, then opine on realistic current earning capacity.</p>"),
        ],
        "related": [("Earning Capacity & Wage Loss", "/services/earning-capacity-evaluation/"),
                    ("Vocational Expert Witness", "/services/vocational-expert-witness/")],
    },
}


# ---- CONTACT -------------------------------------------------------------- #

def contact_body():
    body = f"""
{page_hero("Contact", "Request a consultation",
           "Tell us about your matter and we'll discuss how a vocational or life care planning opinion "
           "can support it — including scope, timeline, and fees.")}

<section class="section">
  <div class="container split">
    <div class="split-main">
      <form class="contact-form" action="https://formspree.io/f/your-form-id" method="POST"
            aria-label="Consultation request">
        <p class="form-note">Fields marked * are required. Do not include privileged or confidential
           case details in this initial message.</p>
        <div class="form-row">
          <label>Full name *<input type="text" name="name" required autocomplete="name"></label>
          <label>Firm / Organization<input type="text" name="firm" autocomplete="organization"></label>
        </div>
        <div class="form-row">
          <label>Email *<input type="email" name="email" required autocomplete="email"></label>
          <label>Phone<input type="tel" name="phone" autocomplete="tel"></label>
        </div>
        <label>Matter type
          <select name="matter">
            <option value="">Select…</option>
            <option>Personal Injury</option>
            <option>Workers' Compensation</option>
            <option>Employment Litigation</option>
            <option>Family Law</option>
            <option>Other</option>
          </select>
        </label>
        <label>Service needed
          <select name="service">
            <option value="">Select…</option>
            <option>Vocational Expert Evaluation</option>
            <option>Earning Capacity / Wage Loss</option>
            <option>Life Care Planning</option>
            <option>Case Management</option>
            <option>Economic Damages</option>
            <option>Not sure yet</option>
          </select>
        </label>
        <label>How can we help? *<textarea name="message" rows="5" required></textarea></label>
        <button type="submit" class="btn btn-block">Send Request</button>
      </form>
    </div>
    <aside class="split-aside">
      <div class="aside-card">
        <h3>Direct contact</h3>
        <ul class="contact-list">
          <li><span>Office</span><a href="tel:{SITE['phone_e164']}">{SITE['phone_display']}</a></li>
          <li><span>Mobile</span><a href="tel:{SITE['mobile_e164']}">{SITE['mobile_display']}</a></li>
          <li><span>Email</span><a href="mailto:{SITE['email']}">{SITE['email']}</a></li>
          <li><span>Office</span>{SITE['street']}<br>{SITE['city']}, {SITE['region']} {SITE['postal']}</li>
          <li><span>Service area</span>United States &amp; Canada</li>
        </ul>
        <a href="{SITE['linkedin']}" class="card-link" rel="noopener" target="_blank">Connect on LinkedIn &rarr;</a>
      </div>
    </aside>
  </div>
</section>
"""
    schema = (
        '{"@context":"https://schema.org","@type":"ContactPage","name":"Contact Purinton Analytics",'
        '"url":"%s/contact/","mainEntity":{"@id":"%s/#organization"}}' % (SITE["domain"], SITE["domain"])
    )
    return body, [org_schema(), schema]


def privacy_body():
    body = f"""
{page_hero("Privacy", "Privacy policy",
           "How Purinton Analytics handles information submitted through this website.")}
<section class="section">
  <div class="container narrow legal">
    <p>Purinton Analytics, LLC ("we", "us") respects your privacy. This policy explains what
       information we collect through pa-expert.com and how we use it.</p>
    <h2>Information we collect</h2>
    <p>We collect the information you voluntarily provide through our contact form — such as your name,
       firm, email, phone number, and the details of your inquiry. We may also collect standard,
       non-identifying analytics data (such as pages visited) to improve the site.</p>
    <h2>How we use information</h2>
    <p>We use the information you provide solely to respond to your inquiry, evaluate potential
       engagements, and screen for conflicts of interest. We do not sell your information.</p>
    <h2>Confidentiality</h2>
    <p>Please do not transmit privileged or confidential case material through this website's contact
       form. Submitting an inquiry does not create an expert-engagement or any professional
       relationship until a conflict check is completed and an engagement is confirmed in writing.</p>
    <h2>Contact</h2>
    <p>Questions about this policy may be directed to
       <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p>
    <p class="legal-updated">Last updated: {LASTMOD}</p>
  </div>
</section>
"""
    return body, [org_schema()]


def not_found_body():
    return f"""
<section class="page-hero">
  <div class="container">
    <p class="eyebrow">404</p>
    <h1>Page not found</h1>
    <p class="lead">The page you're looking for isn't here. Let's get you back on track.</p>
    <div class="hero-actions">
      <a href="/" class="btn">Go to Homepage</a>
      <a href="/services/" class="btn btn-ghost">View Services</a>
    </div>
  </div>
</section>
""", []


# --------------------------------------------------------------------------- #
#  Page registry & writer
# --------------------------------------------------------------------------- #

def make_breadcrumb(path, label):
    crumbs = [("Home", "/")]
    if path.startswith("/services/") and path != "/services/":
        crumbs.append(("Services", "/services/"))
    elif path.startswith("/practice-areas/") and path != "/practice-areas/":
        crumbs.append(("Practice Areas", "/practice-areas/"))
    crumbs.append((label, path))
    return crumbs


def build_pages():
    pages = []

    b, s = home_body()
    pages.append(dict(path="/", title="Vocational Expert & Life Care Planning Services | Purinton Analytics",
                      description="Purinton Analytics provides objective, defensible vocational expert "
                      "evaluations and life care planning for personal injury, workers' compensation, "
                      "employment, and family law — plaintiff and defense, U.S. & Canada.",
                      active="/", body=b, schema=s))

    b, s = about_body()
    pages.append(dict(path="/about/",
                      title="About Jason C. Purinton, Vocational Expert | Purinton Analytics",
                      description="Jason C. Purinton, LPC, CRC, CVE, FVE, ABVE/F, IPEC — a licensed "
                      "counselor and board-certified vocational expert and life care planner serving "
                      "attorneys nationwide since 2019.",
                      active="/about/", body=b, schema=s,
                      breadcrumb=make_breadcrumb("/about/", "About")))

    b, s = services_index_body()
    pages.append(dict(path="/services/",
                      title="Vocational & Life Care Planning Services | Purinton Analytics",
                      description="Vocational expert evaluations, earning capacity and wage loss "
                      "analysis, life care planning, case management, and economic damages support "
                      "for litigation.",
                      active="/services/", body=b, schema=s,
                      breadcrumb=make_breadcrumb("/services/", "Services")))

    b, s = practice_index_body()
    pages.append(dict(path="/practice-areas/",
                      title="Practice Areas | Purinton Analytics Vocational Experts",
                      description="Vocational and life care planning opinions for personal injury, "
                      "workers' compensation, employment litigation, and family law matters.",
                      active="/practice-areas/", body=b, schema=s,
                      breadcrumb=make_breadcrumb("/practice-areas/", "Practice Areas")))

    # Detail pages
    titles = {
        "/services/vocational-expert-witness/": "Vocational Expert Witness Services | Purinton Analytics",
        "/services/earning-capacity-evaluation/": "Earning Capacity & Wage Loss Analysis | Purinton Analytics",
        "/services/life-care-planning/": "Life Care Planning Services | Purinton Analytics",
        "/services/case-management/": "Vocational Rehabilitation & Case Management | Purinton Analytics",
        "/services/economic-damages/": "Economic Damages Analysis | Purinton Analytics",
        "/practice-areas/personal-injury/": "Personal Injury Vocational & Life Care Experts | Purinton Analytics",
        "/practice-areas/workers-compensation/": "Workers' Compensation Vocational Expert | Purinton Analytics",
        "/practice-areas/employment-litigation/": "Employment Litigation Vocational Expert | Purinton Analytics",
        "/practice-areas/family-law/": "Family Law Earning Capacity Evaluations | Purinton Analytics",
    }
    for path, cfg in DETAILS.items():
        cfg["path"] = path
        b, s = detail_body(cfg)
        label = cfg["h1"].replace("&amp;", "&")
        active = "/services/" if path.startswith("/services/") else "/practice-areas/"
        pages.append(dict(path=path, title=titles[path], description=cfg["lead"],
                          active=active, body=b, schema=s,
                          breadcrumb=make_breadcrumb(path, label)))

    b, s = contact_body()
    pages.append(dict(path="/contact/",
                      title="Contact & Request a Consultation | Purinton Analytics",
                      description="Contact Purinton Analytics to discuss a vocational expert or life "
                      "care planning engagement. Call (877) 882-9778 or request a consultation online.",
                      active="/contact/", body=b, schema=s,
                      breadcrumb=make_breadcrumb("/contact/", "Contact")))

    b, s = privacy_body()
    pages.append(dict(path="/privacy/", title="Privacy Policy | Purinton Analytics",
                      description="Privacy policy for pa-expert.com — how Purinton Analytics handles "
                      "information submitted through this website.",
                      active="", body=b, schema=s, noindex=False))

    b, s = not_found_body()
    pages.append(dict(path="/404.html", title="Page Not Found | Purinton Analytics",
                      description="The page you requested could not be found.",
                      active="", body=b, schema=s, is_file=True))

    return pages


def write_page(page):
    html = head(page) + header(page["active"]) + '<main id="main">' + page["body"] + "</main>" + footer()
    if page.get("is_file"):
        out = os.path.join(ROOT, page["path"].lstrip("/"))
    else:
        rel = page["path"].strip("/")
        out_dir = ROOT if rel == "" else os.path.join(ROOT, rel)
        os.makedirs(out_dir, exist_ok=True)
        out = os.path.join(out_dir, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    return page["path"]


# --------------------------------------------------------------------------- #
#  Sitemap / robots / llms.txt / manifest
# --------------------------------------------------------------------------- #

def write_meta_files(pages):
    indexable = [p for p in pages if not p.get("is_file") and p["path"] != "/404.html"]
    priorities = {"/": "1.0", "/services/": "0.9", "/practice-areas/": "0.9", "/about/": "0.8",
                  "/contact/": "0.8"}
    urls = ""
    for p in indexable:
        pr = priorities.get(p["path"], "0.7")
        cf = "monthly" if p["path"] not in ("/", "/services/", "/practice-areas/") else "weekly"
        urls += (f"  <url>\n    <loc>{SITE['domain']}{p['path']}</loc>\n"
                 f"    <lastmod>{LASTMOD}</lastmod>\n    <changefreq>{cf}</changefreq>\n"
                 f"    <priority>{pr}</priority>\n  </url>\n")
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               f"{urls}</urlset>\n")
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(sitemap)

    robots = (f"User-agent: *\nAllow: /\n\n"
              f"# AI / GEO crawlers are welcome to index this content\n"
              f"User-agent: GPTBot\nAllow: /\n"
              f"User-agent: OAI-SearchBot\nAllow: /\n"
              f"User-agent: ChatGPT-User\nAllow: /\n"
              f"User-agent: ClaudeBot\nAllow: /\n"
              f"User-agent: Claude-Web\nAllow: /\n"
              f"User-agent: anthropic-ai\nAllow: /\n"
              f"User-agent: PerplexityBot\nAllow: /\n"
              f"User-agent: Google-Extended\nAllow: /\n"
              f"User-agent: Applebot-Extended\nAllow: /\n\n"
              f"Sitemap: {SITE['domain']}/sitemap.xml\n")
    open(os.path.join(ROOT, "robots.txt"), "w").write(robots)

    # llms.txt — GEO / AI discovery
    llms = f"""# Purinton Analytics, LLC

> Forensic vocational expert and life care planning practice providing objective, defensible
> evaluations of employability, earning capacity, wage loss, and the future cost of care for
> attorneys and insurers across the United States and Canada. Principal: {SITE['principal']},
> {SITE['principal_creds']}. Based in {SITE['city']}, {SITE['region_full']}. Retained by both
> plaintiff and defense counsel; testifying in civil litigation since 2019.

## Contact
- Phone (office): {SITE['phone_display']}
- Phone (mobile): {SITE['mobile_display']}
- Email: {SITE['email']}
- Address: {SITE['street']}, {SITE['city']}, {SITE['region']} {SITE['postal']}
- Website: {SITE['domain']}

## Services
- [Vocational Expert Witness]({SITE['domain']}/services/vocational-expert-witness/): Objective evaluations of employability and earning capacity, with expert testimony.
- [Earning Capacity & Wage Loss]({SITE['domain']}/services/earning-capacity-evaluation/): Pre- and post-injury earning capacity and quantified wage loss analysis.
- [Life Care Planning]({SITE['domain']}/services/life-care-planning/): Comprehensive, evidence-based projection of future care needs and costs.
- [Case Management]({SITE['domain']}/services/case-management/): Vocational rehabilitation and medical case management.
- [Economic Damages]({SITE['domain']}/services/economic-damages/): Vocational and cost foundation for economic damages models.

## Practice Areas
- [Personal Injury]({SITE['domain']}/practice-areas/personal-injury/)
- [Workers' Compensation]({SITE['domain']}/practice-areas/workers-compensation/)
- [Employment Litigation]({SITE['domain']}/practice-areas/employment-litigation/)
- [Family Law]({SITE['domain']}/practice-areas/family-law/)

## About
- [About Jason C. Purinton]({SITE['domain']}/about/): Credentials — Licensed Professional Counselor (LPC), Certified Rehabilitation Counselor (CRC), Certified Vocational Evaluator (CVE), Fellow of the American Board of Vocational Experts (ABVE/F), Forensic Vocational Expert (FVE), International Psychometric Evaluator Certified (IPEC).
"""
    open(os.path.join(ROOT, "llms.txt"), "w").write(llms)

    manifest = (
        '{\n  "name": "Purinton Analytics, LLC",\n  "short_name": "Purinton Analytics",\n'
        '  "description": "Vocational expert and life care planning services",\n'
        '  "start_url": "/",\n  "display": "standalone",\n'
        f'  "background_color": "#ffffff",\n  "theme_color": "{SITE["theme"]}",\n'
        '  "icons": [\n'
        '    { "src": "/favicon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any" }\n'
        '  ]\n}\n'
    )
    open(os.path.join(ROOT, "site.webmanifest"), "w").write(manifest)

    open(os.path.join(ROOT, "CNAME"), "w").write("pa-expert.com\n")


# --------------------------------------------------------------------------- #

def main():
    pages = build_pages()
    written = [write_page(p) for p in pages]
    write_meta_files(pages)
    print(f"Built {len(written)} pages:")
    for w in written:
        print("  ", w)
    print("Wrote sitemap.xml, robots.txt, llms.txt, site.webmanifest, CNAME")


if __name__ == "__main__":
    main()
