# Contributing

This repository is a single-author personal site, but pull requests are welcome for:

- Typo or grammar fixes.
- Broken-link fixes.
- Accessibility improvements.
- Quality-gate additions in `scripts/check_quality.py` that catch a real class of failure.

For substantive content changes (new pages, new copy, new branding), please open an issue first to discuss the direction before opening a PR.

## Local setup

```bash
make install          # install dev tooling (ruff, mypy, pytest)
make build            # rebuild og-default.png + SEO assets
make audit            # run the full local quality gate
make serve            # serve at http://localhost:8000
```

Python 3.11+ required. No runtime third-party dependencies.

## Quality bar

CI runs the same checks that `make audit` runs locally. PRs that fail the quality gate cannot merge. Common issues:

- Adding a new page without all the meta tags listed in `scripts/check_quality.py::check_meta_tags`.
- Adding a new page without a `<p class="summary">` 40-60 word citable summary.
- Adding a new page that is not in the nav block on every other page.
- Forgetting to re-run `make build` after a content change, leaving the SEO assets stale.

## Style

- Two-space indentation in HTML; four-space indentation in Python.
- Inline CSS lives inside `<style>` blocks per page (mirrors the padel reference). Do not introduce a global stylesheet — each page should remain self-contained for cache and edit locality.
- Use system fonts. Do not introduce web-font dependencies.
- Light- and dark-mode variants must both work; test both before submitting.
- No tracking scripts. No analytics. No ad code.

## License

By contributing you agree your changes are released under the MIT License (see `LICENSE`).
