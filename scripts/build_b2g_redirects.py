#!/usr/bin/env python3
"""Generate root-level redirect pages for every page on the ca-b2g-research site.

Visitors who type the short URL on the personal domain (e.g. avaluev.github.io/initiatives/)
land here and get bounced to the canonical project URL
(avaluev.github.io/ca-b2g-research/initiatives/).

GitHub Pages does not support server-side 301 redirects, so this is the only option.
The redirect HTML carries:
- <meta http-equiv="refresh"> for old-school + no-JS
- <link rel="canonical"> so search engines do not penalise duplicate content
- inline JS location.replace for instant client-side hop
- minimal body content as a fallback

Idempotent: re-running produces byte-identical output.
"""

from __future__ import annotations

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT_BASE = "https://avaluev.github.io/ca-b2g-research"

# Slugs from the project site that should be reachable at the root domain.
# Keep in lock-step with ca-b2g-research/outputs/site/ directory tree.
SLUGS: list[tuple[str, str, str]] = [
    # (slug, short title, short description)
    ("uzbekistan",     "Uzbekistan B2G AI report",     "Live country report for Uzbekistan: 50 initiatives, 17 Tier-A, 56 decrees, 27 donor programmes, 30 live tenders."),
    ("kyrgyzstan",     "Kyrgyzstan B2G AI report",     "Live country report for Kyrgyzstan: 50 initiatives, 11 Tier-A, 44 decrees, 29 donor programmes, 20 live tenders."),
    ("initiatives",    "B2G initiatives — UZ + KG",    "100 deployable AI/digital-government initiatives across Uzbekistan and Kyrgyzstan, scored on five axes."),
    ("donors",         "Donor programme pipeline",     "World Bank, ADB, EU, EBRD, UN, and bilateral programmes funding AI/digital government in UZ and KG."),
    ("procurement",    "Live procurement",             "Live and forthcoming AI/digital procurements in UZ and KG with win-probability annotations."),
    ("trends",         "Sectoral trends",              "AI/digital trends across 12 sectors in Uzbekistan and Kyrgyzstan with TAM and lens annotations."),
    ("people",         "Decision-makers",              "Tier-1 / Tier-2 decision-makers in UZ and KG with mandate over AI/digital procurement."),
    ("institutions",   "Institution map",              "Eight-tier institution taxonomy covering AI/digital state bodies in UZ and KG."),
    ("decrees/uz",     "UZ decree atlas",              "Decrees on AI/digital government in Uzbekistan with implementation half-life status."),
    ("decrees/kg",     "KG decree atlas",              "Decrees on AI/digital government in Kyrgyzstan with implementation half-life status."),
    ("mvp",            "Solopreneur MVPs",             "200 solopreneur-bootstrappable MVP ideas grounded in the UZ + KG B2G knowledge graph."),
    ("mvp/uz",         "Uzbekistan solo MVPs",         "100 solopreneur MVP ideas grounded in the Uzbekistan knowledge graph."),
    ("mvp/kg",         "Kyrgyzstan solo MVPs",         "100 solopreneur MVP ideas grounded in the Kyrgyzstan knowledge graph."),
    ("methodology",    "Research methodology",         "How the multi-agent pipeline produces a typed knowledge graph of B2G AI/digital opportunities."),
    ("lenses",         "Analytical lenses",            "Five non-obvious analytical lenses applied to every B2G initiative in the knowledge graph."),
    ("scoring",        "Scoring rubric",               "Five-axis scoring rubric used to rank every B2G initiative in the knowledge graph."),
    ("audit-team",     "16-specialist AI Audit Team",  "Five-layer audit team of 16 AI specialists that re-audits every page on every site build."),
    ("honesty",        "Honesty: what we did not find","Documented gaps, dead-end research pathways, and contradictions in the B2G knowledge graph."),
    ("provenance",     "Provenance and audit trail",   "Every claim's source, every cross-model verification card, every audit finding."),
]


def render_redirect(slug: str, title: str, description: str) -> str:
    target = f"{PROJECT_BASE}/{slug}/"
    return (
        '<!doctype html>\n'
        '<html lang="en">\n'
        '<head>\n'
        '<meta charset="utf-8">\n'
        f'<title>{escape(title)} — redirecting…</title>\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        f'<meta name="description" content="{escape(description)}">\n'
        '<meta name="robots" content="noindex,follow">\n'
        f'<link rel="canonical" href="{target}">\n'
        f'<meta http-equiv="refresh" content="0; url={target}">\n'
        '<meta property="og:type" content="article">\n'
        f'<meta property="og:title" content="{escape(title)}">\n'
        f'<meta property="og:description" content="{escape(description)}">\n'
        f'<meta property="og:url" content="{target}">\n'
        '<style>body{font-family:system-ui,-apple-system,sans-serif;max-width:640px;'
        'margin:80px auto;padding:24px;line-height:1.6;color:#0d1117}a{color:#0057cc}</style>\n'
        '</head>\n'
        '<body>\n'
        f'<h1>{escape(title)}</h1>\n'
        f'<p>This page has moved to <a href="{target}">{target.replace("https://", "")}</a>.</p>\n'
        '<p>If you are not redirected automatically, follow the link above.</p>\n'
        f'<script>location.replace("{target}");</script>\n'
        '</body>\n'
        '</html>\n'
    )


def main() -> int:
    written = 0
    unchanged = 0
    for slug, title, description in SLUGS:
        out_dir = ROOT / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / "index.html"
        new = render_redirect(slug, title, description)
        if out_file.exists() and out_file.read_text(encoding="utf-8") == new:
            unchanged += 1
            print(f"[nochange] /{slug}/")
            continue
        out_file.write_text(new, encoding="utf-8")
        written += 1
        print(f"[wrote]    /{slug}/")
    print(f"\nTotal: {written} written, {unchanged} unchanged, {len(SLUGS)} total slugs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
