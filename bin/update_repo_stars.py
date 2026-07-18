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
