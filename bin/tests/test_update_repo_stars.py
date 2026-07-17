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
