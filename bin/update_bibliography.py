#!/usr/bin/env python
"""
Find papers on ADS where you are an author but that are missing from
_bibliography/papers.bib, and interactively add them. Also mirrors new
entries into the LaTeX CV publication lists (papers.bib and papers_fr.bib)
in the private bastiencarreres/My_CV repo (Overleaf-synced), which is
cloned/pulled to a local cache dir.

Usage:
    ADS_API_TOKEN=xxxx python bin/update_bibliography.py [--since YEAR] [--dry-run]

Setup:
    1. Get a free ADS API token: https://ui.adsabs.harvard.edu/user/settings/token
    2. export ADS_API_TOKEN=<your token>
    3. (optional) export ORCID_ID=0000-0000-0000-0000 to also search by ORCID

The script:
    1. Queries ADS for papers matching your name (and ORCID, if set).
    2. Splits results into:
       - brand new papers (no matching bibcode/arXiv id/DOI in papers.bib)
       - known papers whose ADS bibcode changed since it was added (e.g. a
         preprint-only bibcode like `2025arXiv250513290C` that has since
         become a published one like `2025ApJ...994..178C`) — these get
         their journal/volume/number/pages/doi/ads_bibcode refreshed.
    3. For each new paper, asks you to confirm authorship and pick a
       section (`FirstAuth` / `SignContrib` / `Other`), then generates a
       bibtex entry following the file's existing conventions and appends
       it to the right section of all three bib files (papers.bib uses
       \\(...\\) math delimiters; the My_CV copies use $...$ and the
       _fr one gets a separately-entered French annotation).
    4. For each paper whose bibcode changed, shows a diff and asks for
       confirmation before updating the entry (by citekey) in all three
       bib files.
    5. If the My_CV repo files changed, asks for confirmation before
       committing and pushing them (Overleaf then syncs automatically).
"""

import argparse
import os
import re
import subprocess
import sys

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from update_cv import clone_or_pull, CACHE_DIR

BIB_PATH = "_bibliography/papers.bib"
BIB_NAME_LATEX_EN = "papers.bib"
BIB_NAME_LATEX_FR = "papers_fr.bib"
ADS_SEARCH_URL = "https://api.adsabs.harvard.edu/v1/search/query"
FIRST_AUTHOR_LASTNAME = "Carreres"

SECTION_BANNERS = {
    "FirstAuth": "################\n# FIRST AUTHOR #\n################",
    "SignContrib": "#########################\n# SIGNIFICATIVE CONTRIB #\n#########################",
    "Other": "###################\n# CO-AUTH CONTRIB #\n###################",
}
SECTION_ORDER = ["FirstAuth", "SignContrib", "Other"]


def ads_token() -> str:
    token = os.environ.get("ADS_API_TOKEN")
    if not token:
        print(
            "ADS_API_TOKEN environment variable not set.\n"
            "Get a free token at https://ui.adsabs.harvard.edu/user/settings/token "
            "and export it as ADS_API_TOKEN.",
            file=sys.stderr,
        )
        sys.exit(1)
    return token


def query_ads(token: str, since_year: int | None) -> list[dict]:
    orcid = os.environ.get("ORCID_ID")
    if orcid:
        q = f'orcid:"{orcid}" OR author:"Carreres, B"'
    else:
        q = 'author:"Carreres, B"'
    if since_year:
        q += f" year:{since_year}-"

    params = {
        "q": q,
        "fl": "bibcode,title,author,year,pub,volume,issue,page,doi,identifier,"
        "abstract,doctype,pubdate",
        "rows": 200,
        "sort": "date desc",
    }
    resp = requests.get(
        ADS_SEARCH_URL,
        params=params,
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )
    resp.raise_for_status()
    docs = resp.json()["response"]["docs"]
    # Exclude non-article record types (errata, catalogs, etc.)
    return [d for d in docs if d.get("doctype") in ("article", "eprint", None)]


def load_bib_text(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def unescape_latex(s: str) -> str:
    """Undo escape_latex, e.g. to compare a stored bibcode/journal against ADS's raw value."""
    return s.replace("\\&", "&")


def load_existing_identifiers() -> tuple[str, set, set, set, set]:
    text = load_bib_text(BIB_PATH)

    bibcodes = {
        unescape_latex(b) for b in re.findall(r"ads_bibcode\s*=\s*\{([^}]+)\}", text)
    }
    inspire_ids = set(re.findall(r"inspirehep_id\s*=\s*\{([^}]+)\}", text))
    arxiv_ids = set()
    for m in re.findall(r"preprint\s*=\s*\{([^}]+)\}", text):
        arx = re.search(r"(\d{4}\.\d{4,5})", m)
        if arx:
            arxiv_ids.add(arx.group(1))
    dois = set(re.findall(r"\bdoi\s*=\s*\{([^}]+)\}", text))
    return text, bibcodes, inspire_ids, arxiv_ids, dois


ENTRY_START_RE = re.compile(r"^@(\w+)\{([^,]+),\s*$")


def get_field(body: str, name: str) -> str | None:
    m = re.search(rf"\b{re.escape(name)}\s*=\s*\{{([^}}]*)\}}", body)
    return m.group(1) if m else None


def parse_entries(text: str) -> list[dict]:
    """Parse top-level bib entries (citekey + a handful of identifying fields).
    Relies on this file's convention of a lone '}' line closing each entry -
    safe even though field values like `title` may contain nested braces.
    """
    lines = text.split("\n")
    entries = []
    i = 0
    while i < len(lines):
        m = ENTRY_START_RE.match(lines[i])
        if m:
            key = m.group(2)
            end = None
            for j in range(i + 1, len(lines)):
                if lines[j].strip() == "}":
                    end = j
                    break
            if end is not None:
                body = "\n".join(lines[i + 1 : end])
                arxiv = None
                preprint = get_field(body, "preprint")
                if preprint:
                    arx = re.search(r"(\d{4}\.\d{4,5})", preprint)
                    arxiv = arx.group(1) if arx else None
                bibcode = get_field(body, "ads_bibcode")
                entries.append(
                    {
                        "key": key,
                        "bibcode": unescape_latex(bibcode) if bibcode else None,
                        "doi": get_field(body, "doi"),
                        "arxiv": arxiv,
                    }
                )
                i = end
        i += 1
    return entries


def update_entry_fields(text: str, key: str, updates: dict[str, str]) -> str:
    """Set (or insert) simple single-line fields in the entry identified by `key`."""
    lines = text.split("\n")
    start = None
    for i, line in enumerate(lines):
        if ENTRY_START_RE.match(line) and ENTRY_START_RE.match(line).group(2) == key:
            start = i
            break
    if start is None:
        return text

    end = None
    for j in range(start + 1, len(lines)):
        if lines[j].strip() == "}":
            end = j
            break
    if end is None:
        return text

    to_insert = []
    for field, value in updates.items():
        pattern = re.compile(rf"^(\s*){re.escape(field)}\s*=\s*\{{[^}}]*\}}\s*,?\s*$")
        found = False
        for i in range(start + 1, end):
            if pattern.match(lines[i]):
                indent = re.match(r"^(\s*)", lines[i]).group(1)
                lines[i] = f"{indent}{field} = {{{value}}},"
                found = True
                break
        if not found:
            to_insert.append((field, value))

    if to_insert:
        lines[end:end] = [f"  {field} = {{{value}}}," for field, value in to_insert]

    return "\n".join(lines)


def doc_arxiv_id(doc: dict) -> str | None:
    for ident in doc.get("identifier", []):
        m = re.match(r"^(?:arXiv:)?(\d{4}\.\d{4,5})$", ident)
        if m:
            return m.group(1)
    return None


def already_in_bib(doc: dict, bibcodes, arxiv_ids, dois) -> bool:
    if doc.get("bibcode") in bibcodes:
        return True
    arx = doc_arxiv_id(doc)
    if arx and arx in arxiv_ids:
        return True
    for d in doc.get("doi", []) or []:
        if d in dois:
            return True
    return False


def prompt(question: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default is not None else ""
    ans = input(f"{question}{suffix}: ").strip()
    return ans if ans else (default or "")


def yes_no(question: str, default: bool = True) -> bool:
    d = "Y/n" if default else "y/N"
    ans = input(f"{question} [{d}]: ").strip().lower()
    if not ans:
        return default
    return ans.startswith("y")


def citekey_slug(title: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", title)[:3]
    return "".join(w.lower()[:3] for w in words)


def make_citekey(first_author_last: str, title: str, year: str, existing_text: str) -> str:
    base = re.sub(r"[^a-z]", "", first_author_last.lower()) + citekey_slug(title) + str(year)
    key = base
    suffix = "b"
    while re.search(rf"@\w+\{{{re.escape(key)},", existing_text):
        key = base[:-len(str(year))] + suffix + str(year)
        suffix = chr(ord(suffix) + 1)
    return key


def format_authors(ads_authors: list[str]) -> str:
    return " and ".join(ads_authors)


def escape_latex(s: str) -> str:
    return s.replace("&", "\\&")


def to_plain_math(s: str) -> str:
    """Convert \\(...\\) math delimiters (used in papers.bib) to $...$ (used in the My_CV LaTeX bibs)."""
    return s.replace("\\(", "$").replace("\\)", "$")


def build_entry(doc: dict, citekey: str, keyword: str, selected: bool, annotation: str) -> str:
    title = escape_latex(doc.get("title", [""])[0])
    authors = format_authors(doc.get("author", []))
    year = doc.get("year", "")
    pub = escape_latex(doc.get("pub", ""))
    arxiv_id = doc_arxiv_id(doc)
    doi_list = doc.get("doi") or []

    lines = ["@article{" + citekey + ","]
    lines.append(f"  title = {{{title}}},")
    lines.append(f"  author = {{{authors}}},")
    lines.append(f"  year = {{{year}}},")
    if pub:
        lines.append(f"  journal = {{{pub}}},")
    if doc.get("volume"):
        lines.append(f"  volume = {{{doc['volume']}}},")
    if doc.get("page"):
        lines.append(f"  pages = {{{doc['page'][0]}}},")
    if doi_list:
        lines.append(f"  doi = {{{doi_list[0]}}},")
    if arxiv_id:
        lines.append(f"  preprint = {{https://arxiv.org/abs/{arxiv_id}}},")
    if annotation:
        lines.append(f"  annotation = {{{annotation}}},")
    lines.append(f"  keywords = {{{keyword}}},")
    lines.append(f"  selected = {{{'true' if selected else 'false'}}},")
    if doc.get("bibcode"):
        lines.append(f"  ads_bibcode = {{{escape_latex(doc['bibcode'])}}}")
    lines.append("}")
    return "\n".join(lines) + "\n"


def insert_entry(text: str, section: str, entry: str) -> str:
    banner = SECTION_BANNERS[section]
    idx = SECTION_ORDER.index(section)
    next_banners = [SECTION_BANNERS[s] for s in SECTION_ORDER[idx + 1 :]]

    insert_at = len(text)
    for nb in next_banners:
        pos = text.find(nb)
        if pos != -1:
            insert_at = pos
            break

    before = text[:insert_at].rstrip("\n") + "\n\n"
    after = text[insert_at:]
    return before + entry + "\n" + after


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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--since", type=int, default=None, help="Only consider papers from this year onward")
    parser.add_argument("--dry-run", action="store_true", help="Don't write to papers.bib")
    args = parser.parse_args()

    clone_or_pull()
    bib_path_latex_en = str(CACHE_DIR / BIB_NAME_LATEX_EN)
    bib_path_latex_fr = str(CACHE_DIR / BIB_NAME_LATEX_FR)

    token = ads_token()
    print("Querying ADS...")
    docs = query_ads(token, args.since)
    print(f"Found {len(docs)} papers on ADS matching your author query.")

    text, bibcodes, inspire_ids, arxiv_ids, dois = load_existing_identifiers()
    text_latex_en = load_bib_text(bib_path_latex_en)
    text_latex_fr = load_bib_text(bib_path_latex_fr)

    existing_entries = parse_entries(text)
    bibcode_index = {e["bibcode"]: e for e in existing_entries if e["bibcode"]}
    arxiv_index = {e["arxiv"]: e for e in existing_entries if e["arxiv"]}
    doi_index = {e["doi"]: e for e in existing_entries if e["doi"]}

    new_docs = []
    stale_docs = []  # (doc, matched existing entry) pairs whose ADS bibcode changed
    for d in docs:
        doc_bibcode = d.get("bibcode")
        if doc_bibcode in bibcode_index:
            continue  # already up to date

        matched = None
        doc_arxiv = doc_arxiv_id(d)
        if doc_arxiv and doc_arxiv in arxiv_index:
            matched = arxiv_index[doc_arxiv]
        if not matched:
            for doi in d.get("doi") or []:
                if doi in doi_index:
                    matched = doi_index[doi]
                    break

        if matched:
            stale_docs.append((d, matched))
        elif not already_in_bib(d, bibcodes, arxiv_ids, dois):
            new_docs.append(d)

    print(f"{len(new_docs)} new paper(s) not currently in {BIB_PATH}.")
    print(f"{len(stale_docs)} existing paper(s) whose ADS bibcode has changed (e.g. now published).\n")

    updated = 0
    for doc, matched in stale_docs:
        title = doc.get("title", ["(no title)"])[0]
        print("=" * 70)
        print(f"Entry:   {matched['key']}")
        print(f"Title:   {title}")
        print(f"Old bibcode: {matched['bibcode']}")
        print(f"New bibcode: {doc.get('bibcode')}")
        print(f"Journal: {doc.get('pub')}   Volume: {doc.get('volume')}   "
              f"Issue: {doc.get('issue')}   Pages: {(doc.get('page') or [None])[0]}")
        print(f"DOI: {(doc.get('doi') or [None])[0]}")
        print()

        if not yes_no(f"Update '{matched['key']}' with this published info?", default=True):
            print("Skipped.\n")
            continue

        upd = {"ads_bibcode": escape_latex(doc["bibcode"])} if doc.get("bibcode") else {}
        if doc.get("pub"):
            upd["journal"] = escape_latex(doc["pub"])
        if doc.get("volume"):
            upd["volume"] = doc["volume"]
        if doc.get("issue"):
            upd["number"] = doc["issue"]
        if doc.get("page"):
            upd["pages"] = doc["page"][0]
        if doc.get("doi"):
            upd["doi"] = doc["doi"][0]

        text = update_entry_fields(text, matched["key"], upd)
        text_latex_en = update_entry_fields(text_latex_en, matched["key"], upd)
        text_latex_fr = update_entry_fields(text_latex_fr, matched["key"], upd)
        updated += 1
        print(f"Updated '{matched['key']}'.\n")

    candidates = new_docs

    if not candidates:
        if updated and not args.dry_run:
            with open(BIB_PATH, "w") as f:
                f.write(text)
            with open(bib_path_latex_en, "w") as f:
                f.write(text_latex_en)
            with open(bib_path_latex_fr, "w") as f:
                f.write(text_latex_fr)
            print(f"Wrote {updated} updated entry/entries.")
            offer_cv_repo_push()
        elif updated:
            print(f"Dry run: {updated} entry/entries would have been updated (not written).")
        else:
            print("No new papers and no updates.")
        return

    added = 0
    for doc in candidates:
        title = doc.get("title", ["(no title)"])[0]
        authors = doc.get("author", [])
        year = doc.get("year", "?")
        pub = doc.get("pub", "?")
        arxiv_id = doc_arxiv_id(doc)

        print("=" * 70)
        print(f"Title:   {title}")
        print(f"Authors: {', '.join(authors[:8])}{' et al.' if len(authors) > 8 else ''}")
        print(f"Year:    {year}    Journal: {pub}")
        if arxiv_id:
            print(f"arXiv:   https://arxiv.org/abs/{arxiv_id}")
        if doc.get("bibcode"):
            print(f"ADS:     https://ui.adsabs.harvard.edu/abs/{doc['bibcode']}")
        abstract = doc.get("abstract")
        if abstract:
            print(f"Abstract: {abstract[:300]}{'...' if len(abstract) > 300 else ''}")
        print()

        if not yes_no(f"Are you ({FIRST_AUTHOR_LASTNAME}) really an author of this paper?", default=True):
            print("Skipped.\n")
            continue

        first_author_last = authors[0].split(",")[0].strip() if authors else FIRST_AUTHOR_LASTNAME
        is_first_author = first_author_last.lower() == FIRST_AUTHOR_LASTNAME.lower()

        if is_first_author:
            print("Detected as first author -> section 'FirstAuth'.")
            section, keyword = "FirstAuth", "FirstAuth"
            selected_default = True
        else:
            if yes_no("Significant contribution (vs. general co-author 'Other')?", default=False):
                section, keyword = "SignContrib", "SignContrib"
                selected_default = False
            else:
                section, keyword = "Other", "Other"
                selected_default = False

        selected = yes_no("Show on the /about page (selected)?", default=selected_default)
        annotation_en = prompt(
            "One-line note (English) on your contribution to this paper (optional, use \\(...\\) for math)",
            default="",
        )
        annotation_fr = prompt(
            "Same note in French, for the LaTeX CV (optional, use \\(...\\) for math)",
            default="",
        )

        citekey = make_citekey(first_author_last, title, str(year), text)
        entry = build_entry(doc, citekey, keyword, selected, annotation_en)
        entry_latex_en = build_entry(doc, citekey, keyword, selected, to_plain_math(annotation_en))
        entry_latex_fr = build_entry(doc, citekey, keyword, selected, to_plain_math(annotation_fr))

        print("\nGenerated entry (papers.bib):\n")
        print(entry)
        if not yes_no("Add this entry to papers.bib and the My_CV bib files?", default=True):
            print("Skipped.\n")
            continue

        text = insert_entry(text, section, entry)
        text_latex_en = insert_entry(text_latex_en, section, entry_latex_en)
        text_latex_fr = insert_entry(text_latex_fr, section, entry_latex_fr)
        added += 1
        print(f"Added to section '{section}'.\n")

    if (added or updated) and not args.dry_run:
        with open(BIB_PATH, "w") as f:
            f.write(text)
        with open(bib_path_latex_en, "w") as f:
            f.write(text_latex_en)
        with open(bib_path_latex_fr, "w") as f:
            f.write(text_latex_fr)
        print(
            f"Wrote {added} new and {updated} updated entry/entries to {BIB_PATH}, "
            f"{bib_path_latex_en} and {bib_path_latex_fr}."
        )
        offer_cv_repo_push()
    elif added or updated:
        print(f"Dry run: {added} new and {updated} updated entry/entries (not written).")
    else:
        print("No entries added or updated.")


if __name__ == "__main__":
    main()
