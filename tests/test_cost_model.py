import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import cost_model as cm  # noqa: E402

INPUTS, MEASURED = cm.load_inputs()


def test_measured_inputs_come_from_verified_claims():
    claims = {c["id"]: c["values"] for c in json.loads((cm.ROOT / "evidence" / "claims.json").read_text())["claims"]}
    for name, ref in INPUTS["measured"].items():
        assert MEASURED[name] == claims[ref["claim"]][ref["key"]]


def test_onprem_rate_by_hand():
    o = {"server_usd": 8760, "server_vcpu": 1, "life_years": 1, "avg_power_kw": 0, "pue": 1, "usd_per_kwh": 0,
         "ops_share_of_capex_per_year": 0}
    assert abs(cm.onprem_usd_per_vcpu_hour(o) - 1.0) < 1e-12


def test_only_committed_capacity_gets_dearer_when_idle():
    assert cm.per_used_hour("cloud_on_demand", 0.04, 0.2) == 0.04
    assert abs(cm.per_used_hour("onprem", 0.01, 0.2) - 0.05) < 1e-12


def test_break_even_is_where_costs_meet():
    out = cm.model()
    r = out["usd_per_vcpu_hour"]
    u = out["break_even_utilisation_vs_on_demand"]["onprem"]
    assert abs(cm.per_used_hour("onprem", r["onprem"], u) - r["cloud_on_demand"]) < 1e-3


def test_written_model_is_current():
    assert json.loads((cm.ROOT / "evidence" / "cost_model.json").read_text()) == json.loads(json.dumps(cm.model()))
