# Site Reorganization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make talks, CV, software list, and content pages one-file edits or one-script runs, per spec `docs/superpowers/specs/2026-07-17-site-reorganization-design.md`.

**Architecture:** Data-driven Jekyll templates (`_data/*.yml` + `_includes/*.liquid`) replace hand-edited HTML/markdown; two Python bridge scripts sync with the private `bastiencarreres/My_CV` repo (publications → CV repo; CV content → `resume.json`); one new CI workflow refreshes GitHub star counts.

**Tech Stack:** Jekyll/Liquid (al-folio pre-v1), Python 3 (stdlib + requests), GitHub Actions, GitHub REST API.

**Verification notes for the executor:**
- Site builds with `docker compose up` (serves http://localhost:8080) or `bundle exec jekyll serve`. For one-shot builds use: `docker compose run --rm jekyll bundle exec jekyll build` (or `bundle exec jekyll build` if Ruby is set up locally). If neither works in your environment, say so in your report — do not claim the build passed.
- Python script tests use pytest: `pip install pytest` (not added to requirements.txt — dev-only).
- Prettier CI enforces formatting on `.liquid`/`.html`: run `npx prettier --write` on every touched liquid file before committing.
- The `My_CV` repo is private but the user's stored git credentials can clone it over HTTPS. Never push to `My_CV` during testing — dry-run only.

---

### Task 1: Talks data file

**Files:**
- Create: `_data/talks.yml`

All 21 existing entries from `talks/talks.md` migrated. Date format on the current page is inconsistent (2026 entries render DD/MM, earlier years MM/DD); the YAML stores ISO dates and the template (Task 2) renders a uniform MM/DD. Entries with no exact day (two 2022 posters) use `date_display`. The two poster entries get `type: poster`; the Moriond poster keeps its proceedings link via `proceedings:`.

- [ ] **Step 1: Create `_data/talks.yml`**

```yaml
# Talks and posters, rendered on /talks/ by _includes/talks_list.liquid.
# Add entries anywhere — the template sorts by date (newest first) and groups by year.
#
# Fields:
#   date:         YYYY-MM-DD (required; used for sorting and MM/DD display)
#   date_display: optional string shown instead of MM/DD (e.g. "Feb.") when day is unknown
#   title:        talk title (required)
#   venue:        event/seminar name, rendered in italics (required)
#   location:     city/institution/country or "online" (optional)
#   link:         slides — relative to /talks/ (e.g. mydir/index.html) or absolute URL (optional)
#   type:         "poster" to prefix the entry with "Poster:" (optional)
#   proceedings:  URL to proceedings, rendered as a trailing "+ Proceedings" link (optional)

- date: 2026-07-01
  title: Red Dust Redemption
  venue: Next-Generation of SN Ia Survey Mini-Workshop
  location: Oxford, UK
  link: oxfordnextgensn-2026-07-01/Red_Dust_Redemption.pdf

- date: 2026-04-21
  title: "Cosmology with SNe Ia: measuring growth-rate of structures with the new generation of survey"
  venue: Yale cosmology group seminar
  location: Yale University, New Haven, CT, USA
  link: yale-2026-04-21/index.html

- date: 2026-01-12
  title: "SNe Ia growth-rate measurements with Rubin-LSST simulations: intrinsic scatter systematics"
  venue: CPPM Renoir Meeting
  location: Marseille, France
  link: CPPM-2026-01-12/index.html

- date: 2025-11-12
  title: "DESC Project announcement: Constraining Structure Growth and Modified Gravity Using LSST low-z SN Ia PVs and Weak Lensing"
  venue: DESC-MCP meeting
  location: online
  link: descmcp-2025-11-12/DESC_Project_Announcement_Constraining_Structure_Growth_and_Modified_Gravity_Using_LSST_lowz_SNe_Ia_PVs_and_Weak_Lensing.pdf

- date: 2025-09-22
  title: Status of PV cosmology in LSST-DESC
  venue: DESC workshop on cosmology with peculiar velocities
  location: Marseille, France
  link: desc-pv-workshop-2025-09-22/DESCPV-2025-09-22.pdf

- date: 2025-07-02
  title: "SNe Ia growth-rate measurements with Rubin-LSST simulations: intrinsic scatter systematics"
  venue: Cosmic Lighthouses 2025
  location: Cambridge, UK
  link: cosmiclighthouse-2025-07-02/index.html

- date: 2025-03-19
  title: "SNe Ia growth-rate measurements with Rubin-LSST simulations: intrinsic scatter systematics"
  venue: SN Ia Cosmology group of LPCA
  location: online
  link: clermontferrand-2025-03-19/index.html

- date: 2025-02-06
  title: "SNe Ia growth-rate measurements with Rubin-LSST simulations: intrinsic scatter systematics"
  venue: CosmicFlows 2025
  location: Brisbane, Australia
  link: cosmicflows-2025-02-06/index.html

- date: 2025-02-03
  title: Improving SN Ia Hubble residual scatter with galaxy groups
  venue: CosmicFlows 2025
  location: Brisbane, Australia
  link: cosmicflows-2025-02-03/CF2025_GalGrpSN_250203.pdf

- date: 2024-10-15
  title: "DESC Project announcement: Measurement of the growth-rate of structures using SN Ia PVs in the BBC framework"
  venue: DESC-TD biweekly meeting
  location: online
  link: desctd-2024-10-15/DESC_PV_BBC_project.pdf

- date: 2023-09-29
  title: Thesis defense
  venue: Centre de Physique des Particules de Marseille
  location: Marseille, France
  link: PhD/index.html

- date: 2023-09-12
  title: Possible velocity systematic on the Hubble diagram fit
  venue: ZTF France
  location: LPC, Clermont-Ferrand, France
  link: https://indico.in2p3.fr/event/30615/contributions/128392/attachments/79574/116616/Possible%20impacts%20of%20velocities%20on%20the%20fit%20of%20the%20HD.pdf

- date: 2023-04-20
  title: Growth-rate measurement with type Ia supernovae
  venue: Duke cosmology group' seminar
  location: Duke University, Durham, NC, USA
  link: duke-2023-04-20/index.html

- date: 2023-03-28
  title: Growth-rate measurement with type Ia supernovae
  venue: DESC-TD biweekly meeting
  location: online
  link: desctd-2023-03-28/index.html

- date: 2022-11-18
  title: Cosmology with the growth rate using type Ia supernovae
  venue: Action Dark Energy 2022
  location: Marseille, France
  link: https://indico.in2p3.fr/event/27399/contributions/116473/attachments/74014/106473/ADE_2022_bc.pdf

- date: 2022-07-01
  date_display: July
  type: poster
  title: Cosmology with the growth rate of structures using type Ia supernovae
  venue: DESC Summer Meeting 2022
  location: University of Chicago
  link: Poster_Moriond_Chicago.pdf

- date: 2022-05-13
  title: Measuring the growth-rate with the ZTF SN Ia sample
  venue: ZTF Spring Meeting
  location: LPNHE, Paris, France
  link: https://indico.in2p3.fr/event/26793/contributions/110110/attachments/70411/99926/f%CF%838%20with%20SN%20Ia%20-%20ZTF%20Paris%20-%20PhD%20talks.pdf

- date: 2022-02-01
  date_display: Feb.
  type: poster
  title: Cosmology with the growth rate of structures using type Ia supernovae
  venue: Rencontres de Moriond
  link: Poster_Moriond_Chicago.pdf
  proceedings: https://moriond.in2p3.fr/download/proceedings_cosmology_2022.pdf

- date: 2021-05-27
  title: Peculiar velocities with Type Ia Supernovae
  venue: Rubin-LSST France 2021
  location: LPSC, Grenoble, France
  link: https://indico.in2p3.fr/event/23494/contributions/95032/attachments/64400/89320/Pre%CC%81sentation_lsst_france_final.pdf
```

- [ ] **Step 2: Verify YAML parses and count entries**

Run: `python3 -c "import yaml; d = yaml.safe_load(open('_data/talks.yml')); print(len(d)); assert len(d) == 19"`
Expected: `19`

(19 entries, matching the source list one-to-one: 2026×3, 2025×6, 2024×1, 2023×4, 2022×4, 2021×1 = 19.)

- [ ] **Step 3: Commit**

```bash
git add _data/talks.yml
git commit -m "feat: add talks data file"
```

---

### Task 2: Talks template + thin page

**Files:**
- Create: `_includes/talks_list.liquid`
- Modify: `talks/talks.md` (replace entire body)

- [ ] **Step 1: Create `_includes/talks_list.liquid`**

```liquid
{% assign talks_sorted = site.data.talks | sort: "date" | reverse %}
{% assign current_year = "" %}
{% for talk in talks_sorted %}
  {% assign talk_year = talk.date | date: "%Y" %}
  {% if talk_year != current_year %}
    {% assign current_year = talk_year %}
    <h2 class="talks-year">{{ talk_year }}</h2>
  {% endif %}
  {% capture talk_date %}
    {%- if talk.date_display -%}
      {{- talk.date_display -}}
    {%- else -%}
      {{- talk.date | date: "%m/%d" -}}
    {%- endif -%}
  {% endcapture %}
  <p class="talks-entry">
    {{ talk_date | strip }} -
    {% if talk.type == "poster" %}Poster:{% endif %}
    {% if talk.link %}
      {% if talk.link contains "://" %}
        <a href="{{ talk.link }}"><b>{{ talk.title }}</b></a>
      {% else %}
        <a href="{{ talk.link | prepend: '/talks/' | relative_url }}"><b>{{ talk.title }}</b></a>
      {% endif %}
    {% else %}
      <b>{{ talk.title }}</b>
    {% endif %}
    {% if talk.proceedings %}
      + <a href="{{ talk.proceedings }}">Proceedings</a>
    {% endif %}
    at <em>{{ talk.venue }}</em>
    {%- if talk.location %}, {{ talk.location }}{% endif %}
  </p>
{% endfor %}
```

Note: the old page inconsistently mixed DD/MM and MM/DD; this template standardizes on MM/DD (matching the majority of existing entries and the CLAUDE.md convention).

- [ ] **Step 2: Replace `talks/talks.md` body**

Replace the entire file with:

```markdown
---
layout: page
permalink: /talks/
title: Talks
description:
nav: true
nav_order: 1
---

{% include talks_list.liquid %}
```

- [ ] **Step 3: Format with prettier**

Run: `npx prettier --write _includes/talks_list.liquid`
Expected: file formatted (or unchanged), exit 0.

- [ ] **Step 4: Build site and verify rendered talks page**

Run: `bundle exec jekyll build 2>&1 | tail -3` (or the docker equivalent from the header notes)
Expected: build succeeds.

Then: `python3 -c "
import re
html = open('_site/talks/index.html').read()
assert 'Red Dust Redemption' in html
assert 'Peculiar velocities with Type Ia Supernovae' in html
assert html.count('talks-year') >= 6, 'expected year headings 2021-2026'
assert 'Poster:' in html
assert 'Proceedings' in html
pos_2026 = html.find('>2026<'); pos_2021 = html.find('>2021<')
assert 0 < pos_2026 < pos_2021, 'years must be newest-first'
print('talks page OK')
"`
Expected: `talks page OK`

- [ ] **Step 5: Spot-check links against the old page**

Run: `python3 -c "
html = open('_site/talks/index.html').read()
for frag in ['oxfordnextgensn-2026-07-01/Red_Dust_Redemption.pdf', 'PhD/index.html', 'Poster_Moriond_Chicago.pdf', 'https://indico.in2p3.fr/event/23494']:
    assert frag in html, frag
print('links OK')
"`
Expected: `links OK`

- [ ] **Step 6: Commit**

```bash
git add _includes/talks_list.liquid talks/talks.md
git commit -m "feat: render talks page from _data/talks.yml"
```

---

### Task 3: Software page data + template

**Files:**
- Modify: `_data/repositories.yml` (replace `github_repos` list with rich entries)
- Create: `_includes/repo_cards.liquid`
- Modify: `_pages/repositories.md` (replace hardcoded cards)

- [ ] **Step 1: Rewrite `_data/repositories.yml`**

Replace the whole file with (preserving `github_users` used by al-folio's `repository/` includes elsewhere, if referenced):

```yaml
github_users:
  - bastiencarreres

repo_description_lines_max: 2

# Repo cards shown on /software/. `stars` is refreshed automatically by
# .github/workflows/update-repo-stars.yml — do not edit it by hand.
github_repos:
  - repo: bastiencarreres/snsim
    description: Simulator for supernovae surveys.
    lang: python
    lang_display: Python
    stars: 5
  - repo: corentinravoux/flip
    description: "Field Level Inference Package: infer growth rate from density and velocity fields."
    lang: python
    lang_display: Python
    stars: 6
  - repo: LSSTDESC/OpSimSummaryV2
    description: Tools for summarizing LSST Operations Simulator outputs.
    lang: jupyter
    lang_display: Jupyter Notebook
    stars: 2
  - repo: bastiencarreres/snanapytools
    description: Python utilities to visualize and work with SNANA.
    lang: python
    lang_display: Python
    stars: 0
```

`lang` maps to the `.lang-dot.<lang>` CSS classes already defined in `_sass/_base.scss` (`python`, `jupyter`). A repo with `stars: 0` renders no star badge (snanapytools currently shows none).

First check nothing else consumes the old flat `github_repos` format:
Run: `grep -rn "github_repos" _includes/ _layouts/ _pages/ --include="*.liquid" --include="*.md"`
If `_includes/repository/` templates iterate `site.data.repositories.github_repos` expecting plain strings, update those loops to use `entry.repo` — report what you found and changed.

- [ ] **Step 2: Create `_includes/repo_cards.liquid`**

```liquid
<div class="repo-cards">
  {% for entry in site.data.repositories.github_repos %}
    {% assign repo_name = entry.repo | split: "/" | last %}
    <a href="https://github.com/{{ entry.repo }}" class="repo-card" target="_blank" rel="noopener">
      <div class="repo-card-header">
        <i class="fa-brands fa-github"></i>
        <span class="repo-name">{{ repo_name }}</span>
      </div>
      <p class="repo-description">{{ entry.description }}</p>
      <div class="repo-meta">
        <span class="repo-lang"><span class="lang-dot {{ entry.lang }}"></span>{{ entry.lang_display }}</span>
        {% if entry.stars and entry.stars > 0 %}
          <span class="repo-stars"><i class="fa-regular fa-star"></i> {{ entry.stars }}</span>
        {% endif %}
      </div>
    </a>
  {% endfor %}
</div>
```

- [ ] **Step 3: Replace `_pages/repositories.md`**

```markdown
---
layout: page
permalink: /software/
title: Software
description: Open-source tools I develop and contribute to.
nav: true
nav_order: 3
---

{% include repo_cards.liquid %}
```

- [ ] **Step 4: Prettier + build + verify**

Run: `npx prettier --write _includes/repo_cards.liquid`

Run: `bundle exec jekyll build 2>&1 | tail -3`
Expected: build succeeds.

Run: `python3 -c "
html = open('_site/software/index.html').read()
for name in ['snsim', 'flip', 'OpSimSummaryV2', 'snanapytools']:
    assert 'repo-name\">' + name in html.replace(chr(39), '\"') or name in html, name
assert html.count('repo-card-header') == 4
assert 'Field Level Inference' in html
print('software page OK')
"`
Expected: `software page OK`

- [ ] **Step 5: Commit**

```bash
git add _data/repositories.yml _includes/repo_cards.liquid _pages/repositories.md
git commit -m "feat: render software cards from _data/repositories.yml"
```

---

### Task 4: Star-count refresh script + workflow

**Files:**
- Create: `bin/update_repo_stars.py`
- Create: `.github/workflows/update-repo-stars.yml`
- Test: `bin/tests/test_update_repo_stars.py`

- [ ] **Step 1: Write the failing test**

Create `bin/tests/test_update_repo_stars.py`:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from update_repo_stars import set_stars_in_yaml_text


SAMPLE = """\
github_users:
  - bastiencarreres

github_repos:
  - repo: bastiencarreres/snsim
    description: Simulator for supernovae surveys.
    lang: python
    lang_display: Python
    stars: 5
  - repo: corentinravoux/flip
    description: "Field Level Inference Package."
    lang: python
    lang_display: Python
    stars: 6
"""


def test_updates_star_count_in_place():
    out = set_stars_in_yaml_text(SAMPLE, {"bastiencarreres/snsim": 12})
    assert "stars: 12" in out
    assert "stars: 6" in out  # untouched repo keeps its value


def test_missing_count_keeps_previous_value():
    out = set_stars_in_yaml_text(SAMPLE, {})
    assert out == SAMPLE


def test_preserves_comments_and_layout():
    text = "# comment\n" + SAMPLE
    out = set_stars_in_yaml_text(text, {"corentinravoux/flip": 7})
    assert out.startswith("# comment\n")
    assert "stars: 7" in out
    assert "stars: 5" in out
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest bin/tests/test_update_repo_stars.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'update_repo_stars'`

- [ ] **Step 3: Write `bin/update_repo_stars.py`**

The updater edits the YAML textually (regex on the `stars:` line following each `repo:` line) instead of round-tripping through a YAML parser, so comments and layout survive — same philosophy as `update_bibliography.py`'s bib editing.

```python
#!/usr/bin/env python3
"""
Refresh GitHub star counts in _data/repositories.yml.

Reads the `github_repos` list, queries the GitHub REST API for each repo's
stargazers_count, and rewrites only the `stars:` lines (comments and layout
are preserved). If the API call fails for a repo, its previous cached value
is kept.

Usage:
    python bin/update_repo_stars.py [--dry-run]

No token required for public repos (60 requests/hour unauthenticated).
Set GITHUB_TOKEN to raise the rate limit in CI.
"""

import argparse
import os
import re
import sys

import requests

YAML_PATH = "_data/repositories.yml"
API_URL = "https://api.github.com/repos/{repo}"


def fetch_star_counts(repos: list[str]) -> dict[str, int]:
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    counts = {}
    for repo in repos:
        try:
            resp = requests.get(API_URL.format(repo=repo), headers=headers, timeout=15)
            resp.raise_for_status()
            counts[repo] = resp.json()["stargazers_count"]
            print(f"  {repo}: {counts[repo]} stars")
        except (requests.RequestException, KeyError, ValueError) as e:
            print(f"  {repo}: fetch failed ({e}), keeping cached value", file=sys.stderr)
    return counts


def list_repos_in_yaml_text(text: str) -> list[str]:
    return re.findall(r"^\s*-\s*repo:\s*(\S+)\s*$", text, flags=re.MULTILINE)


def set_stars_in_yaml_text(text: str, counts: dict[str, int]) -> str:
    """Rewrite `stars:` lines. Each repo entry is `- repo: owner/name` followed
    (within the same list item) by an indented `stars:` line."""
    lines = text.split("\n")
    current_repo = None
    for i, line in enumerate(lines):
        m = re.match(r"^\s*-\s*repo:\s*(\S+)\s*$", line)
        if m:
            current_repo = m.group(1)
            continue
        m = re.match(r"^(\s*)stars:\s*\d+\s*$", line)
        if m and current_repo in counts:
            lines[i] = f"{m.group(1)}stars: {counts[current_repo]}"
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    with open(YAML_PATH) as f:
        text = f.read()

    repos = list_repos_in_yaml_text(text)
    if not repos:
        print(f"No `repo:` entries found in {YAML_PATH}", file=sys.stderr)
        sys.exit(1)

    print(f"Fetching star counts for {len(repos)} repos...")
    counts = fetch_star_counts(repos)
    new_text = set_stars_in_yaml_text(text, counts)

    if new_text == text:
        print("No changes.")
        return
    if args.dry_run:
        print("Dry run: changes not written.")
        return
    with open(YAML_PATH, "w") as f:
        f.write(new_text)
    print(f"Updated {YAML_PATH}.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest bin/tests/test_update_repo_stars.py -v`
Expected: 3 passed.

- [ ] **Step 5: Live smoke test (read-only)**

Run: `python3 bin/update_repo_stars.py --dry-run`
Expected: prints current star counts for the 4 repos (network permitting; if offline, note it and move on — unit tests cover the logic).

- [ ] **Step 6: Create `.github/workflows/update-repo-stars.yml`**

```yaml
name: Update repo star counts

on:
  schedule:
    - cron: "0 3 * * 1" # Monday 03:00 UTC
  workflow_dispatch:

jobs:
  update-stars:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.13"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests

      - name: Update star counts
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: python bin/update_repo_stars.py

      - name: Configure Git
        run: |
          git config --local user.email "actions@github.com"
          git config --local user.name "GitHub Actions"

      - name: Commit and push if changed
        run: |
          git add _data/repositories.yml
          git diff --staged --quiet || (
            git commit -m "Update repo star counts"
            git push
          )
```

- [ ] **Step 7: Commit**

```bash
git add bin/update_repo_stars.py bin/tests/test_update_repo_stars.py .github/workflows/update-repo-stars.yml
git commit -m "feat: auto-refresh GitHub star counts weekly"
```

---

### Task 5: CV parser script (`bin/update_cv.py`)

**Files:**
- Create: `bin/update_cv.py`
- Test: `bin/tests/test_update_cv.py`

The script clones/pulls `bastiencarreres/My_CV`, parses `main.tex`, and updates `assets/json/resume.json`. Parsing is TDD'd against real excerpts from `main.tex`.

**Section → resume.json mapping:**

| LaTeX `\section*{...}` | resume.json key | notes |
| --- | --- | --- |
| `Education` | `education` | `\cventry{studyType}{institution}{location}{date}{details}`; details → `score` if it starts with "Graduated", else first `courses` item |
| `Research Experience` | `research_experience` | details kept as `summary` |
| `Teaching \& Mentoring Experience` | `teaching` | `\subsection*{Student Mentoring}` entries get `"subsection": "Student Mentoring"` |
| `Responsibilities \& Services` | `volunteer` | position = entry title; details → summary |
| `Awards \& Grant` | `grants` | first detail line → `summary`, rest → `highlights` |
| `Technical skills` | *skipped* | resume.json's curated `skills` are richer than the .tex list; left untouched |
| `Collaborations`, `Selected publications`, research-interests box | *skipped* | not represented in the web CV |

The script only replaces the mapped keys; everything else in `resume.json` (basics, skills, languages, …) is preserved as-is. This matches the "summarize, don't copy everything" requirement.

`volunteer` note: `_config.yml`'s `jsonresume` list already includes `volunteer`, and `_layouts/cv.liquid` + `_includes/resume/volunteer.liquid` render it under the heading "Volunteer". Add a heading override in `_layouts/cv.liquid` (`when 'volunteer'` → "Responsibilities & Services"), shown in Step 6.

- [ ] **Step 1: Write the failing tests**

Create `bin/tests/test_update_cv.py`:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from update_cv import (
    parse_sections,
    parse_cventries,
    strip_latex,
    tex_to_resume_updates,
)


SAMPLE_TEX = r"""
\begin{document}

\section*{Education}
\cventry{PhD -- Astrophysics and Cosmology}{Aix-Marseille Université}{Marseille, France}{2023}{Thesis title: Measurement of the growth rate of structures.}
\cvspace
\cventry{Master's degree -- Subatomic Physics and Cosmology}{Université Grenoble-Alpes}{Grenoble, France}{2020}{Graduated with honors}

\section*{Research Experience}
\cventry{Post-doctoral Associate}{Duke University}{Durham, NC, USA}{Nov.~2023~--~Present}{Supervisor: Prof. Dan Scolnic.\\
Subjects: Cosmology with low-$z$ SNe~Ia.}

\section*{Teaching \& Mentoring Experience}
\subsection*{Teaching}
\cventry{Calculus tutoring}{Université de Montpellier}{Montpellier, France}{Oct.~2017~--~Dec.~2017}{Tutoring for first-year college students.}
\subsection*{Student Mentoring}
\cventry{PhD student Mentoring}{Duke University}{}{Nov.~2023~--~Present}{Maria Acevedo -- Subject: Cosmology with the DEBASS survey.}

\section*{Responsibilities \& Services}
\cventry{Reviewer for MNRAS}{}{}{Feb.~2025~--~Present}{Review of 1 publication.}

\section*{Awards \& Grant}
\cventry{Marie Skłodowska-Curie Actions Postdoctoral Fellowship}{European Commission}{}{2025}{
Project ``PEGASUS'': Probing dark Energy \\
Amount: €276,187\\
Host organisation: University of Oxford, UK\\
}

\end{document}
"""


def test_parse_sections_finds_all():
    sections = parse_sections(SAMPLE_TEX)
    assert set(sections) >= {
        "Education",
        "Research Experience",
        "Teaching & Mentoring Experience",
        "Responsibilities & Services",
        "Awards & Grant",
    }


def test_parse_cventries_extracts_fields():
    sections = parse_sections(SAMPLE_TEX)
    entries = parse_cventries(sections["Education"])
    assert len(entries) == 2
    assert entries[0]["title"] == "PhD -- Astrophysics and Cosmology"
    assert entries[0]["org"] == "Aix-Marseille Université"
    assert entries[0]["location"] == "Marseille, France"
    assert entries[0]["dates"] == "2023"
    assert "growth rate" in entries[0]["details"]


def test_parse_cventries_tracks_subsections():
    sections = parse_sections(SAMPLE_TEX)
    entries = parse_cventries(sections["Teaching & Mentoring Experience"])
    assert entries[0]["subsection"] == "Teaching"
    assert entries[1]["subsection"] == "Student Mentoring"


def test_strip_latex():
    assert strip_latex(r"low-$z$ SNe~Ia") == "low-z SNe Ia"
    assert strip_latex(r"Nov.~2023~--~Present") == "Nov. 2023 -- Present"
    assert strip_latex(r"``PEGASUS''") == '"PEGASUS"'
    assert strip_latex(r"line one\\line two") == "line one\nline two"
    assert strip_latex(r"\href{https://x.org}{text}") == "text"
    assert strip_latex(r"\textbf{bold}") == "bold"


def test_tex_to_resume_updates_shapes():
    updates = tex_to_resume_updates(SAMPLE_TEX)
    assert set(updates) == {
        "education",
        "research_experience",
        "teaching",
        "volunteer",
        "grants",
    }
    edu = updates["education"]
    assert edu[0]["institution"] == "Aix-Marseille Université"
    assert edu[0]["studyType"] == "PhD -- Astrophysics and Cosmology"
    assert edu[1]["score"] == "Graduated with honors"

    teach = updates["teaching"]
    assert teach[0]["course"] == "Calculus tutoring"
    assert "subsection" not in teach[0]
    assert teach[1]["subsection"] == "Student Mentoring"

    vol = updates["volunteer"]
    assert vol[0]["position"] == "Reviewer for MNRAS"
    assert vol[0]["summary"] == "Review of 1 publication."

    grants = updates["grants"]
    assert grants[0]["title"] == "Marie Skłodowska-Curie Actions Postdoctoral Fellowship"
    assert grants[0]["awarder"] == "European Commission"
    assert grants[0]["date"] == "2025"
    assert any("276,187" in h for h in grants[0]["highlights"])
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest bin/tests/test_update_cv.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'update_cv'`

- [ ] **Step 3: Write `bin/update_cv.py`**

```python
#!/usr/bin/env python3
"""
Summarize the LaTeX CV from the private bastiencarreres/My_CV repo into
assets/json/resume.json (the web CV rendered on /cv/).

Usage:
    python bin/update_cv.py [--tex PATH] [--dry-run]

By default the script clones (or pulls) https://github.com/bastiencarreres/My_CV
into a cache directory and reads main.tex from it. Pass --tex to parse a local
.tex file instead (e.g. a fresh Overleaf download).

Only these resume.json keys are overwritten, mapped from \\section*{...} blocks:
    education, research_experience, teaching, volunteer (Responsibilities &
    Services), grants (Awards & Grant).
Everything else (basics, skills, languages, ...) is preserved untouched.

The script shows a diff and asks for confirmation before writing.
"""

import argparse
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

CV_REPO_URL = "https://github.com/bastiencarreres/My_CV.git"
CACHE_DIR = Path.home() / ".cache" / "my_cv_repo"
RESUME_PATH = Path("assets/json/resume.json")

SECTION_TO_KEY = {
    "Education": "education",
    "Research Experience": "research_experience",
    "Teaching & Mentoring Experience": "teaching",
    "Responsibilities & Services": "volunteer",
    "Awards & Grant": "grants",
}


def clone_or_pull() -> Path:
    if CACHE_DIR.exists():
        cmd = ["git", "-C", str(CACHE_DIR), "pull", "--ff-only"]
    else:
        cmd = ["git", "clone", "--depth", "1", CV_REPO_URL, str(CACHE_DIR)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(
            f"Failed to fetch My_CV repo:\n{result.stderr}\n"
            "Check your git credentials / network, or pass --tex PATH.",
            file=sys.stderr,
        )
        sys.exit(1)
    return CACHE_DIR / "main.tex"


def strip_latex(s: str) -> str:
    s = re.sub(r"\\href\{[^}]*\}\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\(?:textbf|textit|emph|underline|mbox)\{([^}]*)\}", r"\1", s)
    s = s.replace(r"\\", "\n")
    s = s.replace("``", '"').replace("''", '"')
    s = re.sub(r"\$([^$]*)\$", r"\1", s)  # drop inline-math delimiters
    s = s.replace("~", " ")
    s = re.sub(r"\\&", "&", s)
    s = re.sub(r"\\%", "%", s)
    s = re.sub(r"\\,", " ", s)
    s = re.sub(r"\\[a-zA-Z]+\s*", "", s)  # any leftover command, e.g. \faPython
    s = re.sub(r"[ \t]+", " ", s)
    return "\n".join(line.strip() for line in s.split("\n")).strip()


def parse_sections(tex: str) -> dict[str, str]:
    """Split document body into {section title: section source}."""
    parts = re.split(r"\\section\*\{([^}]*)\}", tex)
    sections = {}
    # parts[0] is preamble/front matter; then alternating title, body
    for i in range(1, len(parts) - 1, 2):
        title = strip_latex(parts[i]).strip()
        sections[title] = parts[i + 1]
    return sections


def _read_braced_args(src: str, start: int, n: int) -> tuple[list[str], int]:
    """Read n {...} groups (brace-aware) starting at src[start]; return (args, end)."""
    args = []
    i = start
    for _ in range(n):
        while i < len(src) and src[i] != "{":
            i += 1
        depth = 0
        arg_start = i + 1
        while i < len(src):
            if src[i] == "{":
                depth += 1
            elif src[i] == "}":
                depth -= 1
                if depth == 0:
                    args.append(src[arg_start:i])
                    i += 1
                    break
            i += 1
    return args, i


def parse_cventries(section_src: str) -> list[dict]:
    """Extract \\cventry{title}{org}{location}{dates}{details} entries,
    tagging each with the \\subsection* it appears under (if any)."""
    entries = []
    subsection = None
    pos = 0
    token_re = re.compile(r"\\(subsection\*|cventry)")
    while True:
        m = token_re.search(section_src, pos)
        if not m:
            break
        if m.group(1) == "subsection*":
            args, pos = _read_braced_args(section_src, m.end(), 1)
            subsection = strip_latex(args[0])
        else:
            args, pos = _read_braced_args(section_src, m.end(), 5)
            title, org, location, dates, details = (strip_latex(a) for a in args)
            entry = {
                "title": title,
                "org": org,
                "location": location,
                "dates": dates,
                "details": details,
            }
            if subsection:
                entry["subsection"] = subsection
            entries.append(entry)
    return entries


def _split_dates(dates: str) -> tuple[str, str]:
    """'Nov. 2023 -- Present' -> ('Nov. 2023', ''); '2023' -> ('2023', '')."""
    parts = re.split(r"\s*--\s*", dates)
    start = parts[0].strip()
    end = parts[1].strip() if len(parts) > 1 else ""
    if end.lower() == "present":
        end = ""
    return start, end


def tex_to_resume_updates(tex: str) -> dict[str, list]:
    sections = parse_sections(tex)
    updates: dict[str, list] = {}

    for sec_title, key in SECTION_TO_KEY.items():
        if sec_title not in sections:
            continue
        entries = parse_cventries(sections[sec_title])
        out = []
        for e in entries:
            detail_lines = [l for l in e["details"].split("\n") if l.strip()]
            if key == "education":
                item = {
                    "institution": e["org"],
                    "location": e["location"],
                    "url": "",
                    "area": "",
                    "studyType": e["title"],
                    "date": e["dates"],
                    "endDate": "",
                    "score": "",
                    "courses": [],
                }
                if detail_lines and detail_lines[0].startswith("Graduated"):
                    item["score"] = detail_lines[0]
                else:
                    item["courses"] = detail_lines
            elif key == "research_experience":
                start, end = _split_dates(e["dates"])
                item = {
                    "institution": e["org"],
                    "position": e["title"],
                    "url": "",
                    "startDate": start,
                    "endDate": end,
                    "summary": " ".join(detail_lines),
                    "location": e["location"],
                    "highlights": [],
                }
            elif key == "teaching":
                start, end = _split_dates(e["dates"])
                item = {
                    "course": e["title"],
                    "institution": e["org"],
                    "location": e["location"],
                    "startDate": start,
                    "endDate": end,
                    "highlights": detail_lines,
                }
                if e.get("subsection") and e["subsection"] != "Teaching":
                    item["subsection"] = e["subsection"]
                item = {k: v for k, v in item.items() if v not in ("", [])}
            elif key == "volunteer":
                start, end = _split_dates(e["dates"])
                item = {
                    "organization": e["org"],
                    "position": e["title"],
                    "url": "",
                    "startDate": start,
                    "endDate": end,
                    "summary": " ".join(detail_lines),
                    "highlights": [],
                }
            elif key == "grants":
                item = {
                    "title": e["title"],
                    "date": e["dates"],
                    "awarder": e["org"],
                    "url": "",
                    "summary": detail_lines[0] if detail_lines else "",
                    "highlights": detail_lines[1:],
                }
                if not item["highlights"]:
                    del item["highlights"]
            out.append(item)
        updates[key] = out

    return updates


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tex", type=Path, default=None, help="Parse this .tex file instead of cloning My_CV")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    tex_path = args.tex if args.tex else clone_or_pull()
    if not tex_path.exists():
        print(f"{tex_path} not found.", file=sys.stderr)
        sys.exit(1)
    tex = tex_path.read_text()

    updates = tex_to_resume_updates(tex)
    if not updates:
        print("No mapped sections found in the .tex file — nothing to do.", file=sys.stderr)
        sys.exit(1)

    resume = json.loads(RESUME_PATH.read_text())
    old_text = json.dumps(resume, indent=2, ensure_ascii=False) + "\n"
    resume.update(updates)
    new_text = json.dumps(resume, indent=2, ensure_ascii=False) + "\n"

    if new_text == old_text:
        print("resume.json already up to date.")
        return

    diff = difflib.unified_diff(
        old_text.splitlines(keepends=True),
        new_text.splitlines(keepends=True),
        fromfile="resume.json (current)",
        tofile="resume.json (from main.tex)",
    )
    sys.stdout.writelines(diff)
    print()

    if args.dry_run:
        print("Dry run: not written.")
        return
    if input("Write these changes to assets/json/resume.json? [Y/n]: ").strip().lower() in ("", "y", "yes"):
        RESUME_PATH.write_text(new_text)
        print(f"Wrote {RESUME_PATH}.")
    else:
        print("Aborted, nothing written.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest bin/tests/test_update_cv.py -v`
Expected: 5 passed. Iterate on the parsing code (not the tests) until they do.

- [ ] **Step 5: Run against the real CV (dry-run)**

Run: `python3 bin/update_cv.py --dry-run`
Expected: clones/pulls My_CV, prints a unified diff of resume.json. Read the diff carefully: education (3 entries), research_experience (2), teaching (5, two tagged Student Mentoring), volunteer (7 services entries), grants (3). Accented characters (Université, Skłodowska) must be intact, no leftover backslashes or `~`. If parsing chokes on a real-world construct not covered by tests, add a test reproducing it first, then fix.

- [ ] **Step 6: Add the volunteer heading override in `_layouts/cv.liquid`**

In `_layouts/cv.liquid`, the heading `{% case data[0] %}` block (around line 91) currently has cases for `research_experience`, `teaching`, `grants`. Add one more before `{% else %}`:

```liquid
              {% when 'volunteer' %}
                <h3 class="card-title font-weight-medium">Responsibilities & Services</h3>
```

Run: `npx prettier --write _layouts/cv.liquid`

- [ ] **Step 7: Apply for real and inspect the CV page**

Run: `python3 bin/update_cv.py` and confirm the write.
Then build: `bundle exec jekyll build 2>&1 | tail -3`
Then: `python3 -c "
html = open('_site/cv/index.html').read()
assert 'Responsibilities & Services' in html or 'Responsibilities &amp; Services' in html
assert 'Reviewer for MNRAS' in html
assert 'Marie Sk' in html
print('cv page OK')
"`
Expected: `cv page OK`

- [ ] **Step 8: Commit**

```bash
git add bin/update_cv.py bin/tests/test_update_cv.py assets/json/resume.json _layouts/cv.liquid
git commit -m "feat: generate web CV summary from My_CV LaTeX source"
```

---

### Task 6: Retarget `bin/update_bibliography.py` to the My_CV repo

**Files:**
- Modify: `bin/update_bibliography.py`
- Delete: `cv-latex/` (after verification)

The script currently mirrors entries into `cv-latex/papers_latex.bib` / `papers_latex_fr.bib`. Retarget those two paths to the cloned My_CV repo's `papers.bib` / `papers_fr.bib`, reusing `clone_or_pull()` from `update_cv.py`, and add an optional commit+push of the CV repo at the end.

- [ ] **Step 1: Update module docstring and path constants**

In `bin/update_bibliography.py`, replace lines 42-44:

```python
BIB_PATH = "_bibliography/papers.bib"
BIB_PATH_LATEX_EN = "cv-latex/papers_latex.bib"
BIB_PATH_LATEX_FR = "cv-latex/papers_latex_fr.bib"
```

with:

```python
from update_cv import clone_or_pull, CACHE_DIR

BIB_PATH = "_bibliography/papers.bib"
BIB_NAME_LATEX_EN = "papers.bib"
BIB_NAME_LATEX_FR = "papers_fr.bib"
```

(`bin/` scripts run from the repo root as `python bin/update_bibliography.py`; add `sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))` just before the import so `update_cv` resolves.)

Also update the docstring: the mirror targets are now `papers.bib`/`papers_fr.bib` in the private `bastiencarreres/My_CV` repo (Overleaf-synced), and mention the new final commit/push confirmation step.

- [ ] **Step 2: Resolve CV-repo paths at the top of `main()`**

At the start of `main()` (after `args` parsing), add:

```python
    clone_or_pull()
    bib_path_latex_en = str(CACHE_DIR / BIB_NAME_LATEX_EN)
    bib_path_latex_fr = str(CACHE_DIR / BIB_NAME_LATEX_FR)
```

Then replace every use of `BIB_PATH_LATEX_EN` / `BIB_PATH_LATEX_FR` in `main()` with the new local variables (loads at lines 330-331, both write blocks, and the final summary print).

- [ ] **Step 3: Add commit+push of the CV repo after a successful write**

In the two places where files are written (the `updated`-only early-return block and the final write block), after writing the CV-repo bibs, add a call to this new helper:

```python
def offer_cv_repo_push():
    status = subprocess.run(
        ["git", "-C", str(CACHE_DIR), "status", "--porcelain"],
        capture_output=True, text=True,
    ).stdout.strip()
    if not status:
        return
    print("\nMy_CV repo has changes:")
    subprocess.run(["git", "-C", str(CACHE_DIR), "diff", "--stat"])
    if yes_no("Commit and push the updated bib files to My_CV (Overleaf will sync)?", default=True):
        subprocess.run(["git", "-C", str(CACHE_DIR), "add", "papers.bib", "papers_fr.bib"], check=True)
        subprocess.run(["git", "-C", str(CACHE_DIR), "commit", "-m", "Update publication list from website"], check=True)
        subprocess.run(["git", "-C", str(CACHE_DIR), "push"], check=True)
        print("Pushed to My_CV.")
    else:
        print(f"Not pushed. The updated files remain in {CACHE_DIR} — push manually when ready.")
```

Add `import subprocess` to the imports.

- [ ] **Step 4: Reconcile content differences before first use**

The My_CV bibs and the old cv-latex bibs have drifted slightly (case of `arxiv` in a DOI, an `ads_bibcode`/`journal`/`pages` block present in cv-latex but missing in My_CV). The My_CV versions are the CV's source of truth for *presentation*; the website script only needs its *matching* to work (it matches entries by citekey via `update_entry_fields`, and appends via section banners). Verify the My_CV bibs contain the same citekeys and section banners:

Run:
```bash
git clone --depth 1 https://github.com/bastiencarreres/My_CV.git /tmp/mycv-check 2>/dev/null || git -C /tmp/mycv-check pull
python3 - <<'EOF'
import re
web = open("_bibliography/papers.bib").read()
for name in ("papers.bib", "papers_fr.bib"):
    cv = open(f"/tmp/mycv-check/{name}").read()
    web_keys = set(re.findall(r"@\w+\{([^,]+),", web))
    cv_keys = set(re.findall(r"@\w+\{([^,]+),", cv))
    print(f"{name}: in website but not CV: {sorted(web_keys - cv_keys)}")
    print(f"{name}: in CV but not website: {sorted(cv_keys - web_keys)}")
    for banner in ("FIRST AUTHOR", "SIGNIFICATIVE CONTRIB", "CO-AUTH CONTRIB"):
        assert banner in cv, f"{name} missing section banner {banner}"
print("banners OK")
EOF
```
Expected: `banners OK`, and empty (or explainable) key differences. If keys differ, report them to the user before proceeding — do not silently reconcile.

- [ ] **Step 5: Dry-run the retargeted script**

Run: `ADS_API_TOKEN=... python3 bin/update_bibliography.py --dry-run` (ask the user for the token, or skip with a note if unavailable — the structural change is covered by Step 4's checks).
Expected: script clones/pulls My_CV, queries ADS, reports new/stale papers, writes nothing.

- [ ] **Step 6: Delete `cv-latex/` and update CLAUDE.md**

```bash
git rm -r cv-latex/
```

In `CLAUDE.md`, replace the "LaTeX pub list" row of the Key Files table with:

```markdown
| LaTeX CV (external) | private repo [`bastiencarreres/My_CV`](https://github.com/bastiencarreres/My_CV) (Overleaf-synced) — its `papers.bib`/`papers_fr.bib` are updated by `bin/update_bibliography.py`; its `main.tex` is summarized into `assets/json/resume.json` by `bin/update_cv.py` |
```

And in the Conventions section, update the **CV** bullet:

```markdown
**CV:** Source of truth is `main.tex` in the private `My_CV` repo (edited on Overleaf). Run `python bin/update_cv.py` to summarize it into `assets/json/resume.json` (only education / research_experience / teaching / volunteer / grants are overwritten; other keys are hand-curated). Sections shown controlled by `jsonresume` key in `_config.yml`.
```

- [ ] **Step 7: Commit**

```bash
git add bin/update_bibliography.py CLAUDE.md
git commit -m "feat: sync LaTeX publication list to My_CV repo, drop cv-latex mirror"
```

---

### Task 7: Fix wrong preprint link in papers.bib

**Files:**
- Modify: `_bibliography/papers.bib:38`

Found during planning: entry `carreresztfsnia2025` ("ZTF SN Ia DR2: Peculiar velocities' impact on the Hubble diagram") has `preprint = {https://arxiv.org/abs/2505.13290}` — that arXiv ID belongs to the LSST intrinsic-scatter paper (`carreresTypeIaSupernova2025`). The correct ID for the ZTF DR2 PV paper is `2405.20409`.

- [ ] **Step 1: Verify the correct arXiv ID**

Run: `curl -s "http://export.arxiv.org/api/query?id_list=2405.20409" | grep -o "<title>[^<]*</title>" | head -2`
Expected: title contains "ZTF SN Ia DR2" and "peculiar velocities" (case-insensitive). If not, search: `curl -s "http://export.arxiv.org/api/query?search_query=ti:%22ZTF%20SN%20Ia%20DR2%22%20AND%20ti:%22peculiar%20velocities%22" | grep -o "arxiv.org/abs/[0-9.]*"` and use that ID.

- [ ] **Step 2: Fix the field**

In `_bibliography/papers.bib` line 38, change:

```
  preprint = {https://arxiv.org/abs/2505.13290},
```

to (with the ID verified in Step 1):

```
  preprint = {https://arxiv.org/abs/2405.20409},
```

Check whether the same wrong ID appears in the My_CV repo bibs (`grep -n "2505.13290" /tmp/mycv-check/papers.bib /tmp/mycv-check/papers_fr.bib`); if so, tell the user so they can fix it there (or fix it via the retargeted script's cache and offer the push).

- [ ] **Step 3: Commit**

```bash
git add _bibliography/papers.bib
git commit -m "fix: correct arXiv preprint link for ZTF DR2 peculiar-velocities paper"
```

---

### Task 8: Outreach page teaching header

**Files:**
- Modify: `_pages/outreach.md`

- [ ] **Step 1: Rewrite `_pages/outreach.md`**

```markdown
---
layout: page
permalink: /outreach/
title: Outreach & Teaching
description:
nav: true
nav_order: 5
---

## Teaching

- **Bachelor's lectures in basic physics** — Aix-Marseille Université, Marseille, France (Sept. 2020 – June 2023).
  PhD candidate with teaching duties, 64h / year: Electricity, Optics, Thermodynamics.
- **Calculus tutoring** — Université de Montpellier, Montpellier, France (Oct. 2017 – Dec. 2017).
  Tutoring for first-year college students.
- **Math tutoring** — independent (Sept. 2016 – June 2018).
  Tutoring for middle-school and high-school students.

## Student Mentoring

- **PhD student mentoring** — Duke University (Nov. 2023 – present).
  Maria Acevedo — Cosmology with the DEBASS survey.
- **Graduate student project supervision** — Duke University (Sept. 2024 – June 2025).
  Estimation of the velocity power spectrum in a N-body simulation.

## Outreach

I'm involved in a <a href="https://YoloNomy.github.io">page</a> / <a href="https://github.com/YoloNomy">github repository</a> about cosmology / physics stuff, co-created with <a href="https://leovacher.github.io">Leo Vacher</a>
```

- [ ] **Step 2: Build and check**

Run: `bundle exec jekyll build 2>&1 | tail -3`, then:
`python3 -c "
html = open('_site/outreach/index.html').read()
assert 'Teaching' in html and 'Student Mentoring' in html and 'YoloNomy' in html
print('outreach OK')
"`
Expected: `outreach OK`

- [ ] **Step 3: Commit**

```bash
git add _pages/outreach.md
git commit -m "feat: add teaching and mentoring sections to outreach page"
```

---

### Task 9: Research page draft (NOT published — stays nav: false)

**Files:**
- Modify: `_pages/research.md`
- Create: `assets/img/research/` (2-4 figures)

Draft one section per first-author paper, newest first. The three papers (from `_bibliography/papers.bib`, keyword `FirstAuth`):

1. `carreresTypeIaSupernova2025` — "Type Ia Supernova Growth-rate Measurement with LSST Simulations: Intrinsic Scatter Systematics", ApJ 994:178 (2025), arXiv:2505.13290
2. `carreresztfsnia2025` — "ZTF SN Ia DR2: Peculiar velocities' impact on the Hubble diagram", A&A 694:A8 (2025), arXiv:2405.20409 (use the ID as fixed in Task 7)
3. `carreresgromeawit2023` — "Growth-rate measurement with type-Ia supernovae using ZTF survey simulations", A&A 674:A197 (2023), arXiv:2303.01198

- [ ] **Step 1: Download arXiv sources and pick figures**

For each paper: `curl -sL "https://arxiv.org/src/<ID>" -o /tmp/<ID>.tar.gz && mkdir -p /tmp/<ID> && tar xzf /tmp/<ID>.tar.gz -C /tmp/<ID>`.
Pick 1-2 *key* figures per paper — prefer: the headline constraint/result figure (e.g. fσ8 posterior or bias summary) and at most one illustrative figure (e.g. Hubble-diagram residuals). Read the paper's abstract + figure captions in the .tex source to choose; favor figures the abstract's main claim rests on.
Convert PDFs to PNG at reasonable web resolution: `pdftoppm -png -r 150 fig.pdf out` (install poppler-utils if needed; if unavailable, use another available converter and note it).
Name files descriptively, e.g. `assets/img/research/lsst-scatter-fs8-bias.png`, and keep total ≤ 6 files.

- [ ] **Step 2: Write the draft page**

Structure for `_pages/research.md` (keep `nav: false` — the owner reviews before publishing; content below is a starting skeleton, the executor writes real summaries from the abstracts/conclusions in the arXiv sources, 1-2 paragraphs per paper, plain language, `\\(...\\)` for math as elsewhere on the site):

```markdown
---
layout: page
permalink: /research/
title: Research
nav: false
---

My research focuses on measuring the growth rate of cosmic structures (\\(f\sigma_8\\)) with type Ia supernovae, using their peculiar velocities as a tracer of the large-scale velocity field.

## Intrinsic scatter systematics in LSST growth-rate measurements

<!-- 1-2 paragraph summary of carreresTypeIaSupernova2025 -->

{% include figure.liquid path="assets/img/research/<figure>.png" class="img-fluid rounded z-depth-1" zoomable=true %}

_[Read the paper](https://arxiv.org/abs/2505.13290)_

## Peculiar velocities in the ZTF SN Ia DR2 Hubble diagram

<!-- 1-2 paragraph summary of carreresztfsnia2025 -->

_[Read the paper](https://arxiv.org/abs/2405.20409)_

## Forecasting growth-rate measurements with ZTF simulations

<!-- 1-2 paragraph summary of carreresgromeawit2023 -->

_[Read the paper](https://arxiv.org/abs/2303.01198)_
```

Check `_includes/figure.liquid` usage in existing pages (`grep -rn "include figure" _pages/ _posts/ 2>/dev/null` — if unused anywhere, verify parameter names against `_includes/figure.liquid` source before using).

- [ ] **Step 3: Build and check (page builds, images render)**

Run: `bundle exec jekyll build 2>&1 | tail -3`, then:
`python3 -c "
html = open('_site/research/index.html').read()
assert 'growth rate' in html
assert 'img' in html
print('research draft OK')
"`
Also verify the page does NOT appear in the navbar: `python3 -c "
html = open('_site/index.html').read()
import re
nav = html[html.find('<nav'):html.find('</nav>')]
assert '/research/' not in nav, 'research must stay out of nav'
print('nav OK')
"`
Expected: both OK.

- [ ] **Step 4: Commit**

```bash
git add _pages/research.md assets/img/research/
git commit -m "feat: draft research page from first-author papers (unpublished)"
```

---

### Task 10: Final verification pass

- [ ] **Step 1: Full build + all page checks**

Run: `bundle exec jekyll build 2>&1 | tail -3` — must succeed.
Re-run the check snippets from Tasks 2, 3, 5, 8, 9 against the fresh `_site/`.

- [ ] **Step 2: All Python tests**

Run: `python3 -m pytest bin/tests/ -v`
Expected: all pass.

- [ ] **Step 3: Prettier over touched templates**

Run: `npx prettier --check "_includes/talks_list.liquid" "_includes/repo_cards.liquid" "_layouts/cv.liquid"`
Expected: all formatted. Fix with `--write` if not.

- [ ] **Step 4: Report**

Summarize to the user: what changed, the new update workflows (add talk = edit `_data/talks.yml`; add repo = edit `_data/repositories.yml`; CV = edit on Overleaf then `python bin/update_cv.py`; publications = `python bin/update_bibliography.py` now also pushes to My_CV), and that `_pages/research.md` awaits their review. Do NOT push to origin — leave that to the user.
