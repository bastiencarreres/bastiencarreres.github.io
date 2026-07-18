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
| LaTeX CV (external) | private repo [`bastiencarreres/My_CV`](https://github.com/bastiencarreres/My_CV) (Overleaf-synced) — its `papers.bib`/`papers_fr.bib` are updated by `bin/update_bibliography.py`; its `main.tex` is summarized into `assets/json/resume.json` by `bin/update_cv.py` |
| CV data            | `assets/json/resume.json` (JSON Resume schema)                   |
| Social links       | `_data/socials.yml` (order = display order)                      |
| Talks index        | `_data/talks.yml` (rendered by `_includes/talks_list.liquid`)    |
| Co-author links    | `_data/coauthors.yml`                                            |
| Journal/venue URLs | `_data/venues.yml`                                               |
| Citation cache     | `_data/citations.yml` (auto-updated by CI, do not edit manually) |
| Styles             | `_sass/_variables.scss`, `_themes.scss`                          |
| Feature flags      | `_config.yml` — `enable_*` keys                                  |

## Conventions

**Publications:** `selected={true}` shows paper on about page. `inspirehep_id` / `ads_bibcode` enable citation badges. Author highlighting via `scholar.last_name`/`first_name` in `_config.yml`.

**CV:** Source of truth is `main.tex` in the private `My_CV` repo (edited on Overleaf). Run `python bin/update_cv.py` to summarize it into `assets/json/resume.json` (only education / research_experience / teaching / volunteer / grants are overwritten; other keys are hand-curated). Sections shown controlled by `jsonresume` key in `_config.yml`.

**NASA ADS logo:** stored as `_includes/nasa_ads_logo.svg`, base64-encoded at build time via `_plugins/base64-filter.rb` and inlined into the shields.io badge URL in `_layouts/bib.liquid`.

**Talk presentations:** standalone reveal.js HTML files in `talks/<name>/index.html`. Must manually include `<link rel="icon" type="image/x-icon" href="/assets/img/favicon.ico" />` — not auto-injected by Jekyll. PDF slides also supported. Add an entry to `_data/talks.yml` (fields documented in the file header; the template sorts by date and groups by year):

```yaml
- date: YYYY-MM-DD
  title: Talk title
  venue: Event Name
  location: City, Country
  link: mydir/slides.pdf # relative to /talks/, or absolute URL
```

**Software page:** `/software/` cards come from `_data/repositories.yml` (`github_repos` entries: repo/description/lang/lang_display/stars). Star counts auto-refreshed weekly by `update-repo-stars.yml`.

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
