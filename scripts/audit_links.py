#!/usr/bin/env python3
"""Crawl every HTML page on the personal site + the b2g research site and check
that every internal link resolves. Emits a tab-separated report grouped by
status code, plus a summary of unique broken targets.

Output: stdout. Exit code 1 if any HTTP status >= 400 found, else 0.

Usage:
    python3 scripts/audit_links.py
"""

from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from typing import Iterable

PERSONAL = "https://avaluev.github.io"
PROJECT = "https://avaluev.github.io/ca-b2g-research"

SEED_URLS = [
    f"{PERSONAL}/",
    f"{PERSONAL}/about.html",
    f"{PERSONAL}/projects.html",
    f"{PERSONAL}/coaching.html",
    f"{PERSONAL}/contact.html",
    f"{PROJECT}/",
    f"{PROJECT}/uzbekistan/",
    f"{PROJECT}/kyrgyzstan/",
    f"{PROJECT}/initiatives/",
    f"{PROJECT}/donors/",
    f"{PROJECT}/procurement/",
    f"{PROJECT}/people/",
    f"{PROJECT}/institutions/",
    f"{PROJECT}/decrees/uz/",
    f"{PROJECT}/decrees/kg/",
    f"{PROJECT}/trends/",
    f"{PROJECT}/mvp/",
    f"{PROJECT}/methodology/",
    f"{PROJECT}/lenses/",
    f"{PROJECT}/scoring/",
    f"{PROJECT}/audit-team/",
    f"{PROJECT}/honesty/",
    f"{PROJECT}/provenance/",
    f"{PROJECT}/about/",
]

# Domains we care about checking. Anything else (linkedin, github, t.me, etc.)
# is reported but skipped — too rate-limited to crawl reliably.
INTERNAL_DOMAINS = {"avaluev.github.io"}

USER_AGENT = "ca-b2g-link-audit/1.0 (+https://avaluev.github.io/)"
TIMEOUT = 15


class LinkExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        for k, v in attrs:
            if k == "href" and v:
                self.hrefs.append(v)


def fetch(url: str) -> tuple[int, str]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status, r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
        return 0, str(e)


def head(url: str) -> int:
    """Return HTTP status; follow redirects; HEAD with GET fallback."""
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status
    except urllib.error.HTTPError as e:
        if e.code == 405:
            # HEAD not allowed — try GET
            try:
                req2 = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(req2, timeout=TIMEOUT) as r:
                    return r.status
            except urllib.error.HTTPError as e2:
                return e2.code
            except Exception:
                return 0
        return e.code
    except (urllib.error.URLError, TimeoutError, ConnectionError):
        return 0


def normalise(href: str, page_url: str) -> str | None:
    href = href.strip()
    if not href or href.startswith(("mailto:", "tel:", "javascript:", "#")):
        return None
    abs_url = urllib.parse.urljoin(page_url, href)
    parsed = urllib.parse.urlparse(abs_url)
    if parsed.scheme not in ("http", "https"):
        return None
    # Drop fragment for the check (we only verify the page exists)
    return urllib.parse.urlunparse(parsed._replace(fragment=""))


def discover_links(seeds: Iterable[str]) -> dict[str, set[str]]:
    """For each seed page, return the set of internal links it points at."""
    out: dict[str, set[str]] = {}
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(fetch, u): u for u in seeds}
        for f in as_completed(futs):
            url = futs[f]
            status, body = f.result()
            if status != 200:
                out[url] = set()
                print(f"[seed-fail] {status:>3} {url}", file=sys.stderr)
                continue
            ex2 = LinkExtractor()
            try:
                ex2.feed(body)
            except Exception as exc:  # noqa: BLE001
                print(f"[parse-fail] {url} {exc}", file=sys.stderr)
                continue
            links: set[str] = set()
            for h in ex2.hrefs:
                norm = normalise(h, url)
                if not norm:
                    continue
                host = urllib.parse.urlparse(norm).netloc
                if host in INTERNAL_DOMAINS:
                    links.add(norm)
            out[url] = links
    return out


def check_links(targets: Iterable[str]) -> dict[str, int]:
    out: dict[str, int] = {}
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(head, u): u for u in targets}
        for f in as_completed(futs):
            out[futs[f]] = f.result()
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quiet", action="store_true", help="Only print broken-link summary.")
    args = parser.parse_args()

    print(f"# Link audit — seeds: {len(SEED_URLS)}", flush=True)
    page_links = discover_links(SEED_URLS)
    all_targets: set[str] = set()
    for links in page_links.values():
        all_targets.update(links)
    # Also check that the seed pages themselves return 200.
    all_targets.update(SEED_URLS)
    print(f"# Unique internal targets to verify: {len(all_targets)}", flush=True)

    statuses = check_links(all_targets)

    # Build reverse map: which seed pages reference each broken target
    referrers: dict[str, list[str]] = {}
    for page, links in page_links.items():
        for link in links:
            referrers.setdefault(link, []).append(page)

    # Group by status
    by_status: dict[int, list[str]] = {}
    for url, code in statuses.items():
        by_status.setdefault(code, []).append(url)

    print()
    for code in sorted(by_status):
        n = len(by_status[code])
        label = "OK" if code == 200 else "REDIR" if 300 <= code < 400 else "BROKEN" if code >= 400 else "ERROR"
        print(f"## HTTP {code:>3}  ({label}) — {n}")
        if args.quiet and code < 400:
            continue
        for url in sorted(by_status[code]):
            print(f"  {url}")
            if code >= 400:
                refs = referrers.get(url, [])
                for r in sorted(set(refs))[:5]:
                    print(f"    ← linked from {r}")

    broken = sum(len(by_status.get(c, [])) for c in by_status if c >= 400 or c == 0)
    print(f"\n# Total broken/errored: {broken}")
    return 1 if broken > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
