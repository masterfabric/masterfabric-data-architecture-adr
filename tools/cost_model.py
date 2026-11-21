"""On-prem vs cloud cost per unit of work, built on the labs' measured throughput.

Measured inputs come from evidence/claims.json (verified by check_claims.py); prices and on-prem
assumptions come from evidence/cost_inputs.json. Writes evidence/cost_model.json.

    python tools/cost_model.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOURS_PER_YEAR = 8760
UTILISATION = [0.1, 0.2, 0.3, 0.5, 0.7, 1.0]


def load_inputs(root: Path = ROOT) -> tuple[dict, dict]:
    claims = {c["id"]: c["values"] for c in json.loads((root / "evidence" / "claims.json").read_text(encoding="utf-8"))["claims"]}
    inputs = json.loads((root / "evidence" / "cost_inputs.json").read_text(encoding="utf-8"))
    measured = {k: claims[v["claim"]][v["key"]] for k, v in inputs["measured"].items()}
    return inputs, measured


def onprem_usd_per_vcpu_hour(o: dict) -> float:
    """Yearly cost (depreciation + energy + operations) spread over every vCPU-hour of the year."""
    capex = o["server_usd"] / o["life_years"]
    energy = o["avg_power_kw"] * o["pue"] * HOURS_PER_YEAR * o["usd_per_kwh"]
    ops = o["server_usd"] * o["ops_share_of_capex_per_year"]
    return (capex + energy + ops) / (o["server_vcpu"] * HOURS_PER_YEAR)


def rates(inputs: dict) -> dict[str, float]:
    p = inputs["prices"]
    r = {f"cloud_{k}": v / p["instance_vcpu"] for k, v in p["usd_per_hour"].items()}
    r["onprem"] = onprem_usd_per_vcpu_hour(inputs["onprem"])
    return r


def per_used_hour(rate_name: str, rate: float, utilisation: float) -> float:
    """On-demand is paid only while used; reserved and on-prem capacity is paid for every hour."""
    return rate if rate_name == "cloud_on_demand" else rate / utilisation


def model(root: Path = ROOT) -> dict:
    inputs, m = load_inputs(root)
    vcpu = inputs["container_vcpu"]
    r = rates(inputs)
    out = {"usd_per_vcpu_hour": {k: round(v, 5) for k, v in r.items()}, "measured": m,
           "break_even_utilisation_vs_on_demand": {k: round(v / r["cloud_on_demand"], 3) for k, v in r.items() if k != "cloud_on_demand"},
           "llm_usd_per_million_tokens": {}, "sql_usd_per_thousand_runs": {}}
    for u in UTILISATION:
        key = f"{int(u * 100)}%"
        out["llm_usd_per_million_tokens"][key] = {
            name: {q: round(per_used_hour(name, rate, u) * vcpu / (m[f"llm_cpu_{q}_tok_s"] * 3600) * 1e6, 4) for q in ("q8", "q4")}
            for name, rate in r.items()}
        out["sql_usd_per_thousand_runs"][key] = {
            name: {e: round(per_used_hour(name, rate, u) * vcpu * m[f"sql_{e}_s"] / 3600 * 1000, 4) for e in ("polars", "duckdb", "pyspark")}
            for name, rate in r.items()}
    out["stream_cpu_ratio_spark_over_flink"] = round(m["stream_spark_cpu_pct"] / m["stream_flink_cpu_pct"], 2)
    out["sql_runtime_ratio_pyspark_over_polars"] = round(m["sql_pyspark_s"] / m["sql_polars_s"], 2)
    return out


def main() -> None:
    out = model()
    (ROOT / "evidence" / "cost_model.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print("USD per vCPU-hour:", out["usd_per_vcpu_hour"])
    print("break-even utilisation vs on-demand:", out["break_even_utilisation_vs_on_demand"])
    for u in ("30%", "100%"):
        print(f"LLM USD / 1M tokens at {u}:", out["llm_usd_per_million_tokens"][u])
        print(f"SQL USD / 1,000 runs at {u}:", out["sql_usd_per_thousand_runs"][u])
    print("Spark/Flink CPU:", out["stream_cpu_ratio_spark_over_flink"], "· PySpark/Polars runtime:", out["sql_runtime_ratio_pyspark_over_polars"])


if __name__ == "__main__":
    main()
