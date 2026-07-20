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

MONTH_ABBREV = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}


def _date_sort_key(date_str: str) -> tuple[int, int]:
    """'Oct. 2020' / 'June 2023' / '2023' / '' (ongoing) -> (year, month) for descending sort."""
    if not date_str:
        return (9999, 12)  # ongoing/present ranks as most recent
    m = re.match(r"^([A-Za-z]+)\.?\s+(\d{4})$", date_str.strip())
    if m:
        month_num = MONTH_ABBREV.get(m.group(1)[:3].lower(), 0)
        return (int(m.group(2)), month_num)
    m = re.match(r"^(\d{4})$", date_str.strip())
    if m:
        return (int(m.group(1)), 0)
    return (0, 0)


def _sort_by_date_desc(items: list[dict], date_field: str) -> list[dict]:
    return sorted(items, key=lambda it: _date_sort_key(it.get(date_field, "")), reverse=True)


def _sort_teaching(items: list[dict]) -> list[dict]:
    """Sort within each subsection group by date desc, preserving group order of first appearance."""
    groups: dict[str | None, list[dict]] = {}
    order: list[str | None] = []
    for it in items:
        key = it.get("subsection")
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(it)
    result = []
    for key in order:
        result.extend(_sort_by_date_desc(groups[key], "startDate"))
    return result


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
    s = s.replace(r"\$", "\x00")  # protect escaped dollars from math stripping
    s = re.sub(r"\$([^$]*)\$", r"\1", s)  # drop inline-math delimiters
    s = s.replace("\x00", "$")
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
        if key == "research_experience" or key == "volunteer":
            out = _sort_by_date_desc(out, "startDate")
        elif key == "teaching":
            out = _sort_teaching(out)
        elif key in ("education", "grants"):
            out = _sort_by_date_desc(out, "date")
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
