# avaluev.github.io

Personal site of **Alex Valuev** — Senior AI Product Manager and career coach. Live at <https://avaluev.github.io/>.

This repo is the source of the deployed site. Static HTML, no build step at runtime, no JavaScript framework, no tracking scripts. The only generators are two Python scripts that produce SEO assets and the OG preview image.

## Quick links

| | |
|---|---|
| Live site | <https://avaluev.github.io/> |
| LinkedIn | <https://www.linkedin.com/in/valuev/> |
| Email | <mailto:valuev.alexandr@gmail.com> |
| Telegram (direct) | <https://t.me/asnkt> |
| VALUEV CAREER channel | <https://t.me/itcareertech> |
| YouTube | <https://youtube.com/@itcareertech> |
| Flagship public research | <https://avaluev.github.io/padel-market-analysis/> |

## What ships in this repo

```
.
├── index.html           # Landing — hero, signature stats, featured work, CTAs
├── about.html           # Long-form bio, career history, leadership philosophy
├── projects.html        # Public projects grid
├── coaching.html        # VALUEV CAREER service page
├── contact.html         # Direct contact methods
├── 404.html             # Friendly not-found page
├── favicon.svg          # Brand mark
├── topnav.css           # Shared navigation styles
├── manifest.webmanifest # PWA manifest (generated)
├── robots.txt           # AI-crawler-aware allow/disallow (generated)
├── sitemap.xml          # XML sitemap (generated)
├── llms.txt             # llmstxt.org index (generated)
├── llms-full.txt        # Full-text retrieval corpus (generated)
├── feed.xml             # RSS feed (generated)
├── humans.txt           # Human credit file (generated)
├── og-default.png       # Social-card image (generated)
├── .well-known/
│   └── security.txt     # RFC 9116 security policy (generated)
└── scripts/
    ├── build_seo_assets.py   # Idempotent SEO-asset generator
    ├── build_og_image.py     # Pure-stdlib PNG generator for the OG card
    └── check_quality.py      # 12-check unified content + SEO quality gate
```

## Quality bar

Every page must pass the unified gate before merge. The gate runs in CI on every push and pull request, and locally via `make audit`.

Per-page checks:

- exactly one `<h1>` per page
- 40-60 word `<p class="summary">` citable summary lead under H1
- full meta package: title, description, canonical, og:title, og:description, og:url, viewport, robots
- valid JSON-LD with `@context: "https://schema.org"`
- consistent five-link top navigation across all pages
- no broken internal links
- no marketing badges, run-IDs, or jargon (`kill experiment`, `north star`, `red team`, etc.)
- every `<img>` has `alt`; warning if missing `width` (Core Web Vitals)
- no leaked Markdown auto-link `<URL>` syntax

Site-wide checks:

- every well-known SEO file present and non-empty (`robots.txt`, `sitemap.xml`, `llms.txt`, `llms-full.txt`, `feed.xml`, `humans.txt`, `manifest.webmanifest`, `favicon.svg`, `.well-known/security.txt`)
- `sitemap.xml` is parseable
- `llms.txt` starts with an H1

Run all checks:

```bash
make audit            # build assets + run quality gates
python3 scripts/check_quality.py --list   # list available checks
python3 scripts/check_quality.py --json   # machine-readable output
```

## Local development

```bash
make install          # install ruff / mypy / pytest
make build            # rebuild og-default.png + SEO assets
make audit            # full pre-merge audit
make serve            # serve on http://localhost:8000
```

The build step is **idempotent**. CI verifies that `make build` followed by `git diff` produces no changes — this catches drift between the source and the generated assets.

## Toolchain provenance

The quality-gate scripts and the AI-search-optimisation rules were lifted from the [`avaluev/padel-market-analysis`](https://github.com/avaluev/padel-market-analysis) repo, which is the reference implementation for this engineering bar across all of Alex's public properties.

## License

[MIT](LICENSE). Reuse, adapt, and remix freely.
