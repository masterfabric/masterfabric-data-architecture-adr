"""Verify every claim in evidence/claims.json against its source README.

Each quote must appear verbatim in the README of the source repository at the pinned commit, and
every value recorded for a claim must appear in its quote (so charts cannot drift from the source).

    python tools/check_claims.py                  # fetch READMEs from GitHub at the pinned commits
    python tools/check_claims.py --local ..       # use sibling checkouts instead (offline)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = "https://raw.githubusercontent.com/masterfabric/masterfabric-{repo}/{commit}/README.md"


def load(path: Path = ROOT / "evidence" / "claims.json") -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def value_forms(v) -> set[str]:
    """Ways a number can be written in a README: 0.83 -> 0.830, 2097761 -> 2,097,761."""
    forms = {str(v)}
    if isinstance(v, int):
        forms.add(f"{v:,}")
    if isinstance(v, float):
        forms |= {f"{v:.{d}f}" for d in range(1, 5)} | {f"{v:,.{d}f}" for d in range(1, 5)}
        if v == int(v):
            forms.add(str(int(v)))
    return forms


def value_problems(claim: dict) -> list[str]:
    plain = re.sub(r"[*`]", "", claim["quote"])
    return [f"{claim['id']}: value {k}={v} not in quote" for k, v in claim["values"].items()
            if not any(f in plain for f in value_forms(v))]


def readme(repo: str, commit: str, local: Path | None) -> str:
    if local is not None:
        return (local / f"masterfabric-{repo}" / "README.md").read_text(encoding="utf-8")
    with urllib.request.urlopen(RAW.format(repo=repo, commit=commit), timeout=30) as r:
        return r.read().decode("utf-8")


def check(data: dict, local: Path | None = None) -> list[str]:
    problems, cache = [], {}
    for c in data["claims"]:
        problems += value_problems(c)
        repo = c["repo"]
        if repo not in cache:
            cache[repo] = readme(repo, data["repos"][repo], local)
        if c["quote"] not in cache[repo]:
            problems.append(f"{c['id']}: quote not found in {repo} README")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--local", type=Path, help="directory holding masterfabric-* checkouts")
    args = ap.parse_args()
    data = load()
    problems = check(data, args.local)
    for p in problems:
        print("FAIL", p)
    n = len(data["claims"])
    print(f"{n - len({p.split(':')[0] for p in problems})}/{n} claims verified "
          f"({'local checkouts' if args.local else 'GitHub at pinned commits'})")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
