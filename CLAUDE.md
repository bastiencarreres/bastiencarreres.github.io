# CLAUDE.md

Personal academic website for Bastien Carreres (cosmologist at Duke University), built on [al-folio](https://github.com/alshedivat/al-folio) Jekyll theme. Deployed to GitHub Pages via the `gh-pages` branch.

## Dev Commands

```bash
docker compose up                          # preferred — http://localhost:8080
docker compose -f docker-compose-slim.yml up  # lighter build, no imagemagick
bundle exec jekyll serve                   # direct (requires Ruby + imagemagick)
npx prettier --write "**/*.{html,liquid}"  # format templates
```

## Key Files

| What               | Where                                                            |
| ------------------ | ---------------------------------------------------------------- |
| Pages              | `_pages/*.md`                                                    |
| Publications       | `_bibliography/papers.bib`                                       |
| LaTeX pub list     | `cv-latex/papers_latex.bib` (EN), `cv-latex/papers_latex_fr.bib` (FR), `cv-latex/main.tex` — mirrors of `papers.bib` for a separate LaTeX CV; kept in sync via `bin/update_bibliography.py` |
| CV data            | `assets/json/resume.json` (JSON Resume schema)                   |
| Social links       | `_data/socials.yml` (order = display order)                      |
| Talks index        | `talks/talks.md` (manually edited)                               |
| Co-author links    | `_data/coauthors.yml`                                            |
| Journal/venue URLs | `_data/venues.yml`                                               |
| Citation cache     | `_data/citations.yml` (auto-updated by CI, do not edit manually) |
| Styles             | `_sass/_variables.scss`, `_themes.scss`                          |
| Feature flags      | `_config.yml` — `enable_*` keys                                  |

## Conventions

**Publications:** `selected={true}` shows paper on about page. `inspirehep_id` / `ads_bibcode` enable citation badges. Author highlighting via `scholar.last_name`/`first_name` in `_config.yml`.

**CV:** Edit `assets/json/resume.json`. Sections shown controlled by `jsonresume` key in `_config.yml`.

**NASA ADS logo:** stored as `_includes/nasa_ads_logo.svg`, base64-encoded at build time via `_plugins/base64-filter.rb` and inlined into the shields.io badge URL in `_layouts/bib.liquid`.

**Talk presentations:** standalone reveal.js HTML files in `talks/<name>/index.html`. Must manually include `<link rel="icon" type="image/x-icon" href="/assets/img/favicon.ico" />` — not auto-injected by Jekyll. PDF slides also supported. Add entry to `talks/talks.md` in format:

```
- MM/DD - [**Title**](path/to/file) at _Venue Name_, City, Country
```

**Co-authors:** `_data/coauthors.yml` maps last name → list of firstname variants + optional URL. Used to auto-link author names in publications.

**Venues:** `_data/venues.yml` maps journal abbreviations → `url` + optional `color`. Controls badge appearance on publication entries.

**Images:** place in `assets/img/`. `jekyll-imagemagick` auto-generates WebP at 480/800/1400px.

## CI/CD

- `deploy.yml` — builds (npm + Jekyll) and deploys `_site` to `gh-pages` on push to `main`; reveal.js installed via npm (`npm run copy-reveal`), not a git submodule
- `update-citations.yml` — runs Mon/Wed/Fri via `bin/update_scholar_citations.py`; commits updated `_data/citations.yml` automatically
- `prettier.yml` / `prettier-html.yml` — enforce formatting on PRs
- `broken-links.yml` / `broken-links-site.yml` — check for dead links
- `update-tocs.yml` — keeps table-of-contents in sync
- pre-commit hooks: trailing whitespace, EOF newlines, YAML validity
