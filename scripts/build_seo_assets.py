#!/usr/bin/env python3
"""Build the AI-search-optimisation assets for avaluev.github.io.

Generates these files at the repo root (the deploy directory for
GitHub Pages user-pages):

- ``robots.txt`` — AI-crawler-aware allow/disallow per the 2026 reference
  template. Allows GPTBot, OAI-SearchBot, ClaudeBot family, PerplexityBot,
  Google-Extended, Applebot-Extended; blocks deprecated Anthropic agents
  and the no-respect Bytespider crawler.
- ``llms.txt`` — concise machine-readable index per the llmstxt.org spec.
- ``llms-full.txt`` — full plain-text concatenation of every published
  page's body content, for LLM training and citation use.
- ``sitemap.xml`` — XML sitemap with lastmod from the file mtime.
- ``humans.txt`` — human credit file.
- ``feed.xml`` — RSS feed of pages.
- ``.well-known/security.txt`` — RFC 9116 security policy.
- ``manifest.webmanifest`` — minimal PWA manifest.
- ``favicon.svg`` — SVG favicon (skipped if it already exists; the brand
  mark is hand-crafted and shouldn't be overwritten by the generator).

Sources for the AI-crawler list and llms.txt format are documented in
the upstream padel-research-os repo's ``evidence/research/`` directory.

Usage::

    python3 scripts/build_seo_assets.py
    python3 scripts/build_seo_assets.py --check   # CI mode

Idempotent. Safe to re-run.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SITE_ORIGIN = "https://avaluev.github.io"
SITE_TITLE = "Alex Valuev — Senior AI Product Manager & Career Coach"
SITE_AUTHOR = "Alex Valuev"
SITE_DESCRIPTION = (
    "Alex Valuev — Senior AI Product Manager with 11+ years shipping AI and "
    "data products across healthcare, FinTech, and MedTech. Career coach to "
    "100+ senior software engineers. Portfolio, public research, and contact."
)
LICENSE_URL = "https://opensource.org/licenses/MIT"

# Hardcoded build date so feed/sitemap output is byte-for-byte identical
# between local re-runs and CI rebuilds. Bump manually when content changes
# materially. Format: ISO-8601 date (YYYY-MM-DD).
BUILD_DATE = "2026-05-03"

# Page registry. Order matters for sitemap and llms.txt.
# Entries: (filename, title, summary).
PAGES: list[tuple[str, str, str]] = [
    (
        "index.html",
        "Alex Valuev — Senior AI Product Manager & Career Coach",
        "Landing page. Senior Product Manager (11+ years, healthcare AI, "
        "FinTech, MedTech) and career coach to 100+ senior engineers. "
        "Featured public research, projects, and contact.",
    ),
    (
        "about.html",
        "About — Alex Valuev",
        "Long-form professional bio: career history from 2014 to present, "
        "leadership philosophy, technical and domain expertise, and the "
        "principles behind low-ego coaching leadership.",
    ),
    (
        "projects.html",
        "Projects — public work by Alex Valuev",
        "Public research and engineering projects, including the padel-market-"
        "analysis evidence-graded research portfolio, agent-factory multi-"
        "agent orchestration, and other open-source experiments.",
    ),
    (
        "coaching.html",
        "Career Coaching for Senior Software Engineers — VALUEV CAREER",
        "Career coaching for senior software engineers: resume rewriting, "
        "behavioural interview preparation, salary negotiation. 100+ engineers "
        "coached since 2022. Run through Telegram and YouTube.",
    ),
    (
        "contact.html",
        "Contact Alex Valuev",
        "Email, LinkedIn, GitHub, Telegram, and YouTube channels. Available "
        "for senior product roles in AI healthcare and FinTech, and for one-"
        "on-one career coaching engagements.",
    ),
]


def _abs(href: str) -> str:
    if href in {"", "/"}:
        return f"{SITE_ORIGIN}/"
    return f"{SITE_ORIGIN}/{href}"


def _file_lastmod_iso(name: str) -> str:
    """Return BUILD_DATE as the lastmod for every page.

    Using a single BUILD_DATE keeps the generated assets byte-for-byte
    deterministic across local builds and CI rebuilds, which is what the
    idempotency check enforces. Real content updates require bumping
    BUILD_DATE explicitly.
    """
    return f"{BUILD_DATE}T00:00:00Z"


# --------------------------------------------------------------- robots.txt

ROBOTS_TXT = f"""\
# robots.txt — AI search visibility profile (2026)
#
# Goal: stay citable in ChatGPT, Claude, Perplexity, Gemini, and Copilot
# search surfaces, while opting out of training-only ingestion where the
# crawler is a separate user agent.
#
# References:
#   - https://developers.openai.com/api/docs/bots
#   - https://privacy.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler
#   - https://llmstxt.org/

# ---- Standard search engines ----
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: DuckDuckBot
Allow: /

# ---- OpenAI ----
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

# ---- Anthropic (three separate bots; rules are independent) ----
User-agent: ClaudeBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Claude-User
Allow: /

# Deprecated Anthropic agents
User-agent: anthropic-ai
Disallow: /

User-agent: Claude-Web
Disallow: /

# ---- Google AI ----
User-agent: Google-Extended
Allow: /

# ---- Perplexity ----
User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

# ---- Apple ----
User-agent: Applebot
Allow: /

User-agent: Applebot-Extended
Allow: /

# ---- Common Crawl (powers many downstream LLMs) ----
User-agent: CCBot
Allow: /

# ---- Cohere ----
User-agent: cohere-ai
Disallow: /

User-agent: cohere-training-data-crawler
Disallow: /

# ---- ByteDance ----
# Poor robots.txt-respect history; block by default.
User-agent: Bytespider
Disallow: /

# ---- Catch-all for unknown crawlers ----
User-agent: *
Allow: /

Sitemap: {SITE_ORIGIN}/sitemap.xml
"""


# ------------------------------------------------------------------ llms.txt


def build_llms_txt() -> str:
    lines = [
        f"# {SITE_TITLE}",
        "",
        f"> {SITE_DESCRIPTION}",
        "",
        f"Author: {SITE_AUTHOR}. License: MIT. Repository: https://github.com/avaluev/avaluev.github.io.",
        "",
        "## Pages",
    ]
    for name, title, summary in PAGES:
        lines.append(f"- [{title}]({_abs(name)}): {summary}")
    lines.append("")
    lines.append("## Optional")
    lines.append(
        f"- [Full text]({_abs('llms-full.txt')}): All page bodies concatenated for retrieval contexts."
    )
    lines.append(
        "- [Padel research](https://avaluev.github.io/padel-market-analysis/): "
        "External — Alex's flagship public research portfolio on padel coaching technology."
    )
    lines.append("")
    return "\n".join(lines)


# ------------------------------------------------------------ llms-full.txt


class _HtmlToMarkdown(HTMLParser):
    """Convert the <main> region of a page into clean Markdown."""

    SKIP_TAGS = frozenset(
        {"nav", "header", "footer", "aside", "noscript", "svg", "style", "script"}
    )

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_main = False
        self.skip_depth = 0
        self.out: list[str] = []
        self.list_stack: list[str] = []
        self.ol_counters: list[int] = []
        self.in_pre = False
        self.in_code = False
        self.in_blockquote = False
        self.text_buf: list[str] = []
        self.link_stack: list[str] = []
        self.heading_level: int | None = None

    def _flush_paragraph(self) -> None:
        text = "".join(self.text_buf).strip()
        self.text_buf = []
        if not text:
            return
        if self.list_stack:
            indent = "  " * (len(self.list_stack) - 1)
            marker = "-" if self.list_stack[-1] == "ul" else f"{self.ol_counters[-1]}."
            if self.list_stack[-1] == "ol":
                self.ol_counters[-1] += 1
            text = re.sub(r"\s+", " ", text)
            self.out.append(f"{indent}{marker} {text}")
            return
        if self.in_blockquote:
            for line in text.splitlines():
                self.out.append(f"> {line}")
            self.out.append("")
            return
        text = re.sub(r"[ \t]+", " ", text)
        self.out.append(text)
        self.out.append("")

    def _emit_blank(self) -> None:
        if self.out and self.out[-1] != "":
            self.out.append("")

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        t = tag.lower()
        if t == "main":
            self.in_main = True
            return
        if not self.in_main:
            return
        if t in self.SKIP_TAGS:
            self.skip_depth += 1
            return
        if self.skip_depth > 0:
            return
        if t in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._flush_paragraph()
            self._emit_blank()
            self.heading_level = int(t[1])
            return
        if t == "p":
            self._flush_paragraph()
            return
        if t == "br":
            self.text_buf.append("  \n")
            return
        if t == "hr":
            self._flush_paragraph()
            self._emit_blank()
            self.out.append("---")
            self._emit_blank()
            return
        if t == "ul":
            self._flush_paragraph()
            self._emit_blank()
            self.list_stack.append("ul")
            return
        if t == "ol":
            self._flush_paragraph()
            self._emit_blank()
            self.list_stack.append("ol")
            self.ol_counters.append(1)
            return
        if t == "li":
            self._flush_paragraph()
            return
        if t == "blockquote":
            self._flush_paragraph()
            self._emit_blank()
            self.in_blockquote = True
            return
        if t == "pre":
            self._flush_paragraph()
            self._emit_blank()
            self.in_pre = True
            self.out.append("```")
            return
        if t == "code" and not self.in_pre:
            self.text_buf.append("`")
            self.in_code = True
            return
        if t in {"strong", "b"}:
            self.text_buf.append("**")
            return
        if t in {"em", "i"}:
            self.text_buf.append("*")
            return
        if t == "a":
            href = ""
            for k, v in attrs:
                if k.lower() == "href" and v:
                    href = v
                    break
            self.link_stack.append(href)
            self.text_buf.append("[")
            return
        if t == "div":
            self._flush_paragraph()
            return

    def handle_endtag(self, tag: str) -> None:
        t = tag.lower()
        if t == "main":
            self._flush_paragraph()
            self.in_main = False
            return
        if not self.in_main:
            return
        if t in self.SKIP_TAGS:
            if self.skip_depth > 0:
                self.skip_depth -= 1
            return
        if self.skip_depth > 0:
            return
        if t in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            text = re.sub(r"\s+", " ", "".join(self.text_buf).strip())
            self.text_buf = []
            if text and self.heading_level is not None:
                hashes = "#" * self.heading_level
                self.out.append(f"{hashes} {text}")
                self.out.append("")
            self.heading_level = None
            return
        if t == "p":
            self._flush_paragraph()
            return
        if t == "ul":
            self._flush_paragraph()
            if self.list_stack and self.list_stack[-1] == "ul":
                self.list_stack.pop()
            if not self.list_stack:
                self._emit_blank()
            return
        if t == "ol":
            self._flush_paragraph()
            if self.list_stack and self.list_stack[-1] == "ol":
                self.list_stack.pop()
                if self.ol_counters:
                    self.ol_counters.pop()
            if not self.list_stack:
                self._emit_blank()
            return
        if t == "li":
            self._flush_paragraph()
            return
        if t == "blockquote":
            self._flush_paragraph()
            self.in_blockquote = False
            self._emit_blank()
            return
        if t == "pre":
            content = "".join(self.text_buf).strip("\n")
            self.text_buf = []
            for line in content.splitlines():
                self.out.append(line)
            self.out.append("```")
            self._emit_blank()
            self.in_pre = False
            return
        if t == "code" and self.in_code and not self.in_pre:
            self.text_buf.append("`")
            self.in_code = False
            return
        if t in {"strong", "b"}:
            self.text_buf.append("**")
            return
        if t in {"em", "i"}:
            self.text_buf.append("*")
            return
        if t == "a":
            href = self.link_stack.pop() if self.link_stack else ""
            if href:
                self.text_buf.append(f"]({href})")
            else:
                self.text_buf.append("]")
            return
        if t == "div":
            self._flush_paragraph()
            return

    def handle_data(self, data: str) -> None:
        if not self.in_main or self.skip_depth > 0:
            return
        if self.in_pre:
            self.text_buf.append(data)
            return
        self.text_buf.append(data)

    def to_markdown(self) -> str:
        self._flush_paragraph()
        out = "\n".join(self.out)
        out = re.sub(r"[ \t]+$", "", out, flags=re.MULTILINE)
        out = re.sub(r"\n{3,}", "\n\n", out)
        return out.strip()


def _markdown_for_page(name: str) -> str:
    html_path = ROOT / name
    if not html_path.exists():
        return ""
    converter = _HtmlToMarkdown()
    try:
        converter.feed(html_path.read_text(encoding="utf-8"))
    except Exception:
        return ""
    return converter.to_markdown()


def build_llms_full_txt() -> str:
    sections: list[str] = []
    sections.append(f"# {SITE_TITLE} — Full Reference\n")
    sections.append(f"> {SITE_DESCRIPTION}\n")
    sections.append(
        f"_Author: {SITE_AUTHOR}. License: MIT._  "
        "_Repository: <https://github.com/avaluev/avaluev.github.io>._\n"
    )
    sections.append(
        "_This file concatenates every published page in markdown for "
        "retrieval contexts. Page boundaries are marked by `# Page: …` "
        "headings. The original page lives at the canonical URL noted "
        "directly under each heading._\n"
    )
    sections.append("\n---\n")

    for name, title, summary in PAGES:
        body = _markdown_for_page(name)
        if not body:
            continue
        canonical = _abs(name) if name != "index.html" else _abs("")
        sections.append(f"\n## Page: {title}\n")
        sections.append(f"_Canonical: <{canonical}>_\n")
        sections.append(f"> {summary}\n")
        sections.append("\n" + body + "\n")
        sections.append("\n---\n")

    return "\n".join(sections).strip() + "\n"


# ----------------------------------------------------------------- sitemap


def build_sitemap_xml() -> str:
    urlset = ET.Element(
        "urlset",
        attrib={
            "xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9",
        },
    )
    for name, _title, _summary in PAGES:
        u = ET.SubElement(urlset, "url")
        loc_href = "" if name == "index.html" else name
        ET.SubElement(u, "loc").text = _abs(loc_href)
        ET.SubElement(u, "lastmod").text = _file_lastmod_iso(name)
        pr = (
            "1.0"
            if name == "index.html"
            else "0.9"
            if name == "about.html"
            else "0.8"
        )
        ET.SubElement(u, "priority").text = pr
        ET.SubElement(u, "changefreq").text = "monthly"
    ET.indent(urlset, space="  ")
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(
        urlset, encoding="unicode"
    )


# ------------------------------------------------------------------- feed


def build_rss_feed() -> str:
    build_dt = dt.datetime.fromisoformat(f"{BUILD_DATE}T00:00:00+00:00")
    now = build_dt.strftime("%a, %d %b %Y %H:%M:%S +0000")
    items: list[str] = []
    for name, title, summary in PAGES:
        if name == "index.html":
            continue
        items.append(
            f"""    <item>
      <title><![CDATA[{title}]]></title>
      <link>{_abs(name)}</link>
      <guid isPermaLink="true">{_abs(name)}</guid>
      <description><![CDATA[{summary}]]></description>
      <pubDate>{now}</pubDate>
    </item>"""
        )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title><![CDATA[{SITE_TITLE}]]></title>
    <link>{SITE_ORIGIN}/</link>
    <atom:link href="{SITE_ORIGIN}/feed.xml" rel="self" type="application/rss+xml" />
    <description><![CDATA[{SITE_DESCRIPTION}]]></description>
    <language>en</language>
    <copyright>MIT licensed</copyright>
    <lastBuildDate>{now}</lastBuildDate>
{chr(10).join(items)}
  </channel>
</rss>
"""


# ----------------------------------------------------------------- humans

HUMANS_TXT = f"""\
/* TEAM */
Author: {SITE_AUTHOR}
Role:   Senior AI Product Manager & Career Coach
LinkedIn: https://www.linkedin.com/in/valuev/
GitHub:   https://github.com/avaluev
Telegram: https://t.me/asnkt
Coaching: https://t.me/itcareertech
YouTube:  https://youtube.com/@itcareertech

/* SITE */
Last update:   {BUILD_DATE}
Language:      English
Doctype:       HTML5
Standards:     HTML5, WCAG AA, AI-search optimised
"""


# --------------------------------------------------------------- security

_BUILD_DT = dt.datetime.fromisoformat(f"{BUILD_DATE}T00:00:00+00:00")
_EXPIRES_DT = _BUILD_DT + dt.timedelta(days=365)
SECURITY_TXT = f"""\
Contact: https://www.linkedin.com/in/valuev/
Contact: mailto:valuev.alexandr@gmail.com
Expires: {_EXPIRES_DT.date().isoformat()}T00:00:00.000Z
Preferred-Languages: en, ru
Canonical: {SITE_ORIGIN}/.well-known/security.txt
"""


# ----------------------------------------------------------------- manifest

MANIFEST_JSON = """\
{
  "name": "Alex Valuev — Senior AI Product Manager & Career Coach",
  "short_name": "Alex Valuev",
  "description": "Senior AI Product Manager. Career coach to senior software engineers.",
  "start_url": "/",
  "scope": "/",
  "display": "browser",
  "background_color": "#ffffff",
  "theme_color": "#2563eb",
  "icons": [
    {"src": "favicon.svg", "type": "image/svg+xml", "sizes": "any"},
    {"src": "android-chrome-192x192.png", "type": "image/png", "sizes": "192x192"},
    {"src": "android-chrome-512x512.png", "type": "image/png", "sizes": "512x512"},
    {"src": "apple-touch-icon.png", "type": "image/png", "sizes": "180x180"}
  ],
  "lang": "en",
  "dir": "ltr",
  "categories": ["business", "productivity", "education"]
}
"""


# ------------------------------------------------------------------- main


def write(path: Path, content: str) -> bool:
    """Write only if content differs. Returns True if written."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="Verify only, no writes."
    )
    args = parser.parse_args()

    artifacts: list[tuple[Path, str]] = [
        (ROOT / "robots.txt", ROBOTS_TXT),
        (ROOT / "llms.txt", build_llms_txt()),
        (ROOT / "llms-full.txt", build_llms_full_txt()),
        (ROOT / "sitemap.xml", build_sitemap_xml()),
        (ROOT / "feed.xml", build_rss_feed()),
        (ROOT / "humans.txt", HUMANS_TXT),
        (ROOT / ".well-known" / "security.txt", SECURITY_TXT),
        (ROOT / "manifest.webmanifest", MANIFEST_JSON),
    ]

    written = 0
    for path, content in artifacts:
        rel = path.relative_to(ROOT)
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                print(f"[stale] {rel}", file=sys.stderr)
                return 1
            print(f"[ok]    {rel}")
            continue
        did = write(path, content)
        verb = "wrote" if did else "nochange"
        print(f"[{verb}] {rel} ({len(content):,} bytes)")
        if did:
            written += 1

    if not args.check:
        print(f"\nTotal new/changed: {written}/{len(artifacts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
