# CLAUDE.md

Personal academic website for Bastien Carreres (cosmologist at Duke University), built on [al-folio](https://github.com/alshedivat/al-folio) Jekyll theme. Deployed to GitHub Pages via the `gh-pages` branch.

## Dev Commands

```bash
docker compose up                          # preferred — http://localhost:8080
bundle exec jekyll serve                   # direct (requires Ruby + imagemagick)
npx prettier --write "**/*.{html,liquid}"  # format templates
```

## Key Files

| What | Where |
|------|-------|
| Pages | `_pages/*.md` |
| Publications | `_bibliography/papers.bib` |
| CV data | `assets/json/resume.json` (JSON Resume schema) |
| Social links | `_data/socials.yml` (order = display order) |
| Styles | `_sass/_variables.scss`, `_themes.scss` |
| Feature flags | `_config.yml` — `enable_*` keys |

## Conventions

**Publications:** `selected={true}` shows paper on about page. `inspirehep_id` / `ads_bibcode` enable citation badges. Author highlighting via `scholar.last_name`/`first_name` in `_config.yml`.

**CV:** Edit `assets/json/resume.json`. Sections shown controlled by `jsonresume` key in `_config.yml`.

**NASA ADS logo:** stored as `_includes/nasa_ads_logo.svg`, base64-encoded at build time via `_plugins/base64-filter.rb` and inlined into the shields.io badge URL in `_layouts/bib.liquid`.

**Talk presentations:** standalone reveal.js HTML files in `talks/<name>/index.html`. Must manually include `<link rel="icon" type="image/x-icon" href="/assets/img/favicon.ico" />` — not auto-injected by Jekyll.

**Images:** place in `assets/img/`. `jekyll-imagemagick` auto-generates WebP at 480/800/1400px.

## CI/CD

- `deploy.yml` — builds (npm + Jekyll) and deploys `_site` to `gh-pages` on push to `main`; reveal.js installed via npm (`npm run copy-reveal`), not a git submodule
- `prettier.yml` — enforces formatting on PRs
- pre-commit hooks: trailing whitespace, EOF newlines, YAML validity
