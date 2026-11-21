.PHONY: venv check check-local test cost charts
PY = .venv/bin/python

venv:
	uv venv --python 3.12 .venv && uv pip install --python .venv -r requirements.txt

check:  ## verify every claim against the source READMEs on GitHub (pinned commits)
	$(PY) tools/check_claims.py

check-local:  ## same, against sibling checkouts in ..
	$(PY) tools/check_claims.py --local ..

test:
	$(PY) -m pytest -q

cost:  ## cost per unit of work from verified claims + dated prices -> evidence/cost_model.json
	$(PY) tools/cost_model.py

charts:
	cd viz && ../$(PY) make_charts.py && ../$(PY) make_diagrams.py && ../$(PY) make_hero.py
