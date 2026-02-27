# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Personal academic website for Bastien Carreres (cosmologist at Duke University), built on the [al-folio](https://github.com/alshedivat/al-folio) Jekyll theme. Deployed to GitHub Pages via the `gh-pages` branch.

## Development Commands

**Local development (via Docker — preferred):**
```bash
docker compose up
# Site available at http://localhost:8080 with live reload on port 35729
```

**Direct Jekyll (requires Ruby/Bundler and imagemagick installed):**
```bash
bundle exec jekyll serve
```

**Format code (Liquid/HTML templates):**
```bash
npx prettier --write "**/*.{html,liquid}"
```

## Architecture

### Content Layer
- **`_pages/`** — Site pages as Markdown with YAML front matter (about.md, cv.md, publications.md, research.md, outreach.md, thesis.md, books.md)
- **`_bibliography/papers.bib`** — BibTeX publication list managed by `jekyll-scholar`. Supports custom fields: `selected`, `abbr`, `arxiv`, `inspirehep_id`, `pdf`, `code`, `preview`, `bibtex_show`, etc.
- **`assets/json/resume.json`** — JSON Resume format, loaded by `jekyll-get-json` and rendered on the CV page
- **`_data/`** — YAML data files: `socials.yml` (social links), `coauthors.yml` (publication co-author links), `venues.yml` (venue abbreviations), `repositories.yml`

### Presentation Layer
- **`_layouts/`** — Liquid layout templates (`default.liquid`, `about.liquid`, `bib.liquid`, `cv.liquid`, `page.liquid`, `pub_page.liquid`, etc.)
- **`_includes/`** — Reusable Liquid components (header, footer, social icons, figure, citation, bib_search, resume subcomponents in `resume/`, cv subcomponents in `cv/`)
- **`_sass/`** — SCSS stylesheets: `_variables.scss` (colors, fonts), `_themes.scss` (light/dark mode), `_layout.scss`, `_cv.scss`

### Configuration
- **`_config.yml`** — Single source of truth for all site settings: scholar config, plugin options, third-party library versions, feature flags (dark mode, math, masonry, etc.)

## Key Conventions

**Publications:** Add entries to `_bibliography/papers.bib`. The `selected={true}` field shows a paper on the about page. `inspirehep_id` and `nasa_ads` fields enable citation badges. Author highlighting is controlled by `scholar.last_name` / `scholar.first_name` in `_config.yml`.

**CV:** Edit `assets/json/resume.json` using the [JSON Resume schema](https://jsonresume.org/). The `_config.yml` `jsonresume` key controls which sections appear.

**Social links:** Add/remove from `_data/socials.yml`. Order in the file determines display order.

**Feature flags:** All optional features (dark mode, math, masonry, tooltips, etc.) are toggled via `enable_*` keys in `_config.yml`.

**Images:** Place in `assets/img/`. The `jekyll-imagemagick` plugin auto-generates responsive WebP variants at 480/800/1400px widths during build.

## CI/CD

- `deploy.yml` — Builds and deploys to `gh-pages` branch on push to `main`
- `prettier.yml` — Enforces formatting on PRs
- `add_reveal.yml` — Adds reveal.js submodule to `gh-pages` after deploy
- pre-commit hooks enforce trailing whitespace, EOF newlines, and YAML validity
