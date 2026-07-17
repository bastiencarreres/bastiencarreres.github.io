# Site Reorganization — Simpler Updates

**Date:** 2026-07-17
**Goal:** Make the most frequent site updates (talks, CV, software list, content pages) one-file edits or one-script runs, and remove duplicated sources of truth.

## Context

Personal academic site on al-folio (pre-v1, repo-embedded theme). Pain points identified with the owner:

- Adding a talk requires hand-editing `talks/talks.md` in an exact markdown format.
- CV content is duplicated: LaTeX CV lives in the private GitHub repo `bastiencarreres/My_CV` (Overleaf-synced; `main.tex`, `main_fr.tex`, `papers.bib`, `papers_fr.bib`), while the web CV is a hand-maintained `assets/json/resume.json`. The website's `cv-latex/` directory is a stale near-duplicate of the `My_CV` repo files.
- The software page (`_pages/repositories.md`) hardcodes repo cards in raw HTML with frozen star counts, duplicating `_data/repositories.yml`.
- `_pages/research.md` is an unfinished hidden draft; `_pages/outreach.md` is one line.

Out of scope: al-folio v1.0 migration (assessed separately, deferred ~6 months), publications workflow in `_bibliography/papers.bib` (works fine).

## Part 1 — Talks become data-driven

**New file `_data/talks.yml`**, one entry per talk:

```yaml
- date: 2026-07-01
  title: Red Dust Redemption
  venue: Next-Generation of SN Ia Survey Mini-Workshop
  location: Oxford, UK
  link: oxfordnextgensn-2026-07-01/Red_Dust_Redemption.pdf
```

- `link` is relative to `/talks/` (PDF or reveal.js `index.html`); absent `link` renders title without a link.
- New include `_includes/talks_list.liquid`: sorts by date descending, groups by year, renders the current visual format (`MM/DD - **Title** at _Venue_, Location`).
- `talks/talks.md` becomes a thin page that includes the template.
- All existing entries in `talks/talks.md` are migrated to YAML verbatim (dates, titles, links, venues checked one-to-one).
- Slides continue to live in `talks/<name>/` directories; nothing about slide hosting changes.
- Adding a talk = drop slides in `talks/<name>/`, add one YAML entry anywhere in the file (template sorts).

## Part 2 — CV and bibliography: two repos, one bridge each way

**Sources of truth:**

- Website repo owns the publication list: `_bibliography/papers.bib`.
- `My_CV` repo owns CV content: `main.tex` (edited on Overleaf, synced to GitHub).

**Bridge 1 — publications → CV repo.** `bin/update_bibliography.py` is retargeted: instead of writing `cv-latex/papers_latex.bib` / `papers_latex_fr.bib`, it clones or pulls `bastiencarreres/My_CV` (into a temp/cache dir), updates its `papers.bib` and `papers_fr.bib` with the same transformation it does today, shows the diff, and on confirmation commits and pushes to `My_CV`. Overleaf picks the change up via its GitHub sync.

**Bridge 2 — CV content → web CV.** New script `bin/update_cv.py`:

- Clones or pulls `My_CV`, reads `main.tex`.
- Parses `\section*{...}` blocks and `\cventry{title}{org}{location}{dates}{details}` entries (also `\subsection*` inside Teaching & Mentoring).
- Maps sections → `resume.json` keys: Education → `education`, Research Experience → `research_experience`, Teaching & Mentoring → `teaching`, Awards & Grant → `grants`, Technical skills → `skills`, Responsibilities & Services → `volunteer` (rendered section list is controlled by the `jsonresume` key in `_config.yml`; final mapping reviewed with owner at implementation).
- Summarizes rather than copies: strips LaTeX markup (`\href`, `~`, `\\`, font commands), keeps title/organization/location/dates plus a short details line. Not all `.tex` content lands in JSON, matching current curation.
- Shows a diff of `resume.json` and asks for confirmation before writing.

**Cleanup:** delete `cv-latex/` from the website repo (redundant, already diverged). `CLAUDE.md` documents the two-repo flow and both scripts.

## Part 3 — Software page from data

- Extend `_data/repositories.yml`: each repo entry gains `description` and `lang`; `stars` is a cached field.
- New include renders the existing card design (name, description, language dot, star count) by looping over the YAML.
- `_pages/repositories.md` becomes a thin page invoking the include; hardcoded HTML cards removed.
- New workflow `.github/workflows/update-repo-stars.yml`: weekly, fetches star counts from the GitHub API (public repos, no token needed), writes them into `_data/repositories.yml`, commits — same pattern as `update-citations.yml`.
- Adding a repo = one YAML entry; stars fill in automatically.

## Part 4 — Research page draft

- Draft `_pages/research.md` from the owner's first-author papers in `_bibliography/papers.bib`: one section per paper with a plain-language summary and 1–2 key figures per paper.
- Figures pulled from arXiv source tarballs, stored in `assets/img/research/` (jekyll-imagemagick generates WebP variants automatically).
- Page stays `nav: false` — owner reviews and publishes manually. Draft quality goal: reviewable starting point, not final copy.

## Part 5 — Outreach page

- Add a "Teaching & Mentoring" section at the top of `_pages/outreach.md`, content sourced from `My_CV`'s `main.tex` teaching section (AMU bachelor lectures, tutoring, PhD/graduate student mentoring at Duke).
- Existing outreach paragraph stays below.
- Static markdown, no automation — content changes rarely.

## Error handling

- `update_cv.py` and `update_bibliography.py`: fail with a clear message if `My_CV` clone/pull fails (no credentials, offline); never write partial output; always show diff + confirm before writing or pushing.
- `update-repo-stars.yml`: if the GitHub API call fails for a repo, keep the previous cached star count rather than writing an empty value.
- `talks_list.liquid`: entries with a missing `link` render unlinked rather than broken; malformed dates fail the build loudly (Jekyll sort error) rather than silently misordering.

## Testing

- Talks: build site locally, diff rendered `/talks/` HTML against current output — same entries, same order, same links.
- CV script: run against the real `My_CV` `main.tex`; verify resulting `resume.json` renders correctly on `/cv/` locally; check LaTeX-stripping on the trickiest entries (accents, `\href`, math like `low-$z$`).
- Bibliography script: dry-run diff against `My_CV` bibs; verify no regression vs. the current `cv-latex/` output before deleting `cv-latex/`.
- Software page: local build, cards visually match current design.
- Stars workflow: trigger manually once (`workflow_dispatch`), verify commit contents.
- Prettier passes on all touched liquid/HTML (CI enforces it).

## Implementation order

1. Talks (self-contained, high value)
2. Software page + stars workflow (self-contained)
3. CV bridge scripts + `cv-latex/` removal (touches two repos, needs owner's git credentials)
4. Outreach header (small, depends on `My_CV` content)
5. Research draft (content work, longest, independent)
