import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from update_bibliography import parse_entries, update_entry_fields

BIB = "@article{k,\n  title = {T},\n  ads_bibcode = {X}\n}\n"


def test_insert_field_adds_missing_comma():
    out = update_entry_fields(BIB, "k", {"inspirehep_id": "1"})
    assert "  ads_bibcode = {X},\n  inspirehep_id = {1},\n}" in out
    assert parse_entries(out)[0]["inspire"] == "1"


def test_replace_existing_field():
    out = update_entry_fields(BIB, "k", {"ads_bibcode": "Y"})
    assert "ads_bibcode = {Y}," in out and "X" not in out
