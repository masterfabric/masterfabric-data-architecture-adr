import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import check_claims as cc  # noqa: E402

DATA = cc.load()
SIBLINGS = Path(__file__).resolve().parents[2]


def test_ids_unique_and_repos_pinned():
    ids = [c["id"] for c in DATA["claims"]]
    assert len(ids) == len(set(ids))
    assert {c["repo"] for c in DATA["claims"]} == set(DATA["repos"])


def test_every_value_appears_in_its_quote():
    assert [p for c in DATA["claims"] for p in cc.value_problems(c)] == []


def test_value_forms():
    assert "2,097,761" in cc.value_forms(2097761)
    assert "0.830" in cc.value_forms(0.83)


def test_checker_catches_a_wrong_number():
    bad = {"id": "x", "repo": "r", "quote": "precision **0.956**", "values": {"precision": 0.965}}
    assert cc.value_problems(bad)


@pytest.mark.skipif(not (SIBLINGS / "masterfabric-lakehouse-lab").exists(), reason="sibling checkouts not present")
def test_quotes_in_local_checkouts():
    assert cc.check(DATA, SIBLINGS) == []
