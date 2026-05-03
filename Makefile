# avaluev.github.io — developer convenience targets.
#
# All targets are non-destructive. The build target re-runs the
# deterministic SEO-asset and OG-image generators. The audit target
# runs the unified content + SEO quality gate.

.PHONY: help install lint typecheck audit build seo-assets og-image \
	check-quality clean serve
.DEFAULT_GOAL := help

PY ?= python3
PORT ?= 8000

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | sort | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}'

install: ## Install Python dev deps
	$(PY) -m pip install -e '.[dev]'

lint: ## Run ruff lint + format check
	ruff check scripts
	ruff format --check scripts

typecheck: ## Run mypy --strict on scripts/
	mypy scripts

build: og-image seo-assets ## Rebuild generated assets (idempotent)

og-image: ## Regenerate the og-default.png social card
	$(PY) scripts/build_og_image.py

seo-assets: ## Regenerate robots / llms / sitemap / feed / manifest / security
	$(PY) scripts/build_seo_assets.py

check-quality: ## Run the unified content / SEO quality gates
	$(PY) scripts/check_quality.py

audit: build check-quality ## Full local pre-merge audit
	@echo ""
	@echo "[audit] all checks passed"

serve: ## Serve the site locally on http://localhost:$(PORT)
	$(PY) -m http.server $(PORT)

clean: ## Remove generated cache artefacts
	rm -rf .mypy_cache .ruff_cache .pytest_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
