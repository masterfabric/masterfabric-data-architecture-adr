"""Evidence chart: one decision per panel, the measured value without and with it.

Every value is read from evidence/claims.json, which tools/check_claims.py verifies against the
source READMEs.
"""
from __future__ import annotations

import json

from mfviz import HEX, IMG, ROOT, mpl_setup

plt = mpl_setup()
C = {c["id"]: c["values"] for c in json.loads((ROOT / "evidence" / "claims.json").read_text())["claims"]}

# (title, unit, without label, without, with label, with, lower is better, ADR, colour)
PANELS = [
    ("Iceberg compaction", "one-day query, ms", "71 + 2 files", C["lh_query"]["before"],
     "14 files", C["lh_query"]["after"], True, "ADR 0001", "ICE"),
    ("Streaming table maintenance", "per-cell aggregate, ms", "357 files", C["rt_maint"]["before"],
     "6 files", C["rt_maint"]["after"], True, "ADR 0002", "ORANGE"),
    ("Adaptive detector", "false alerts, 36 incidents", "static rules", C["rt_static"]["false_alerts"],
     "adaptive", C["rt_detect"]["false_alerts"], True, "ADR 0002", "ORANGE"),
    ("Evidence-gated retraining", "realised AUC, 2026-10, axis from 0.70", "never retrained", C["af_auc"]["never"],
     "auto policy", C["af_auc"]["auto"], False, "ADR 0003", "GREEN"),
    ("Policy-aware retrieval", "unauthorised chunks in context, %", "plain RAG", C["sd_rag"]["before_pct"],
     "policy filter", C["sd_rag"]["after_pct"], True, "ADR 0006", "RED"),
    ("LLM output guards", "PII disclosure attacks that work, of 8", "no guards", C["sd_llm02"]["before"],
     "guards", C["sd_llm02"]["after"], True, "ADR 0006", "RED"),
    ("Quantisation on CPU", "output tok/s, 4 concurrent", "Q4_K_M", C["sv_q4"]["cpu"],
     "Q8_0", C["sv_q8"]["cpu"], False, "ADR 0005", "PURPLE"),
    ("Small-job engine", "6 queries, 200M rows, s", "PySpark", C["sr_sum"]["pyspark"],
     "Polars", C["sr_sum"]["polars"], True, "ADR 0008", "YELLOW"),
    ("Streaming engine", "average CPU, same windowed job, %", "Spark 3.5", C["rt_flink"]["spark_cpu_pct"],
     "Flink 2.2", C["rt_flink"]["flink_cpu_pct"], True, "ADR 0010", "ORANGE"),
    ("Exactly-once sink", "duplicates after kill -9", "at-least-once", C["rt_exactly_once"]["alo"],
     "exactly-once", C["rt_exactly_once"]["eo"], True, "ADR 0010", "ORANGE"),
    ("Guard classifier, on-prem", "held-out attacks stopped, of 16", "rules", C["op_heldout"]["rules"],
     "+ classifier", C["op_heldout"]["classifier"], False, "ADR 0012", "PURPLE"),
    ("Guard classifier, governed", "held-out injections that work, of 12", "rules", C["sd_heldout"]["before"],
     "+ classifier", C["sd_heldout"]["after"], True, "ADR 0012", "RED"),
]


def fmt(v):
    if isinstance(v, float):
        return f"{v:.3f}" if v < 1 else f"{v:,.3f}".rstrip("0").rstrip(".")
    return f"{v:,}"


def evidence():
    fig, axes = plt.subplots(3, 4, figsize=(18, 12.4))
    for a, (title, unit, l0, v0, l1, v1, lower, adr, col) in zip(axes.flat, PANELS):
        bars = a.bar([0, 1], [v0, v1], 0.62, color=[HEX["GREY"], HEX[col]])
        top = max(v0, v1)
        if title.startswith("Evidence"):
            a.set_ylim(0.7, 0.86)
            top = 0.86 - 0.7
        for b, v in zip(bars, (v0, v1)):
            y = b.get_height() if not title.startswith("Evidence") else v
            a.text(b.get_x() + b.get_width() / 2, y + top * 0.02, fmt(v), ha="center", va="bottom",
                   fontsize=12, fontweight="bold", color=HEX["WHITE"])
        a.set_xticks([0, 1], [l0, l1], fontsize=10)
        a.set_title(f"{title}\n", loc="left", fontsize=12.5, fontweight="bold")
        a.text(0, 1.02, f"{unit} · {'lower' if lower else 'higher'} is better · {adr}", transform=a.transAxes,
               fontsize=9, color=HEX["GREY"])
        if not title.startswith("Evidence"):
            a.set_ylim(0, top * 1.18)
        a.grid(axis="x", visible=False)
    fig.suptitle("Each decision, measured: the same metric without it (grey) and with it", x=0.01, ha="left",
                 fontsize=15, fontweight="bold", color=HEX["WHITE"])
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(IMG / "evidence.png", dpi=150)


# Second round (2026-11-23): what each lab learned when it was pushed further. Same layout as PANELS.
ROUND2 = [
    ("Iceberg table maintenance", "one-day query after 60 batches, ms", "never", C["lh_maint_query"]["unmaintained_ms"],
     "every 20 batches", C["lh_maint_query"]["maintained_ms"], True, "ADR 0001", "ICE"),
    ("Watermark delay", "late reports lost, of 172,800", "10 s", C["rt_wm_10s"]["lost"],
     "2 min (live)", C["rt_wm_2min"]["lost"], True, "ADR 0002", "ORANGE"),
    ("Drift-triggered retrain", "realised AUC, axis from 0.70", "champion", C["am_drift_watch"]["champion"],
     "promoted v11", C["am_drift_watch"]["v11"], False, "ADR 0003", "GREEN"),
    ("Guard threshold v1.2", "fresh held-out attacks caught, of 24", "v1.1", C["op_guard_v12"]["v11_caught"],
     "v1.2", C["op_guard_v12"]["v12_caught"], False, "ADR 0012", "PURPLE"),
    ("Clarify instead of block", "legitimate questions blocked, of 12", "block", C["sd_clarify"]["blocked_before"],
     "clarify", C["sd_clarify"]["blocked_after"], True, "ADR 0012", "RED"),
    ("Serving hardware", "llama.cpp Q4_K_M tok/s, 1 request", "Air M5", C["lsb_air"]["air"],
     "M4 Pro", C["lsb_air"]["m4"], False, "ADR 0005", "PURPLE"),
    ("DataFusion allocator cap", "peak memory at 10M rows, MiB", "default", C["sr_df_default"]["mib_10m"],
     "segments capped", C["sr_df_mimalloc"]["mib_10m"], True, "ADR 0008", "YELLOW"),
    ("On-policy DPO round", "reward on unseen prompts, axis from 0.70", "round 1", C["gf_dpo_iter"]["round1"],
     "round 2", C["gf_dpo_iter"]["round2"], False, "ADR 0007", "GREEN"),
]


def round2():
    fig, axes = plt.subplots(2, 4, figsize=(18, 8.6))
    for a, (title, unit, l0, v0, l1, v1, lower, adr, col) in zip(axes.flat, ROUND2):
        base = 0.7 if "axis from 0.70" in unit else 0
        bars = a.bar([0, 1], [v0 - base, v1 - base], 0.62, bottom=base, color=[HEX["GREY"], HEX[col]])
        top = max(v0, v1) - base
        for b, v in zip(bars, (v0, v1)):
            a.text(b.get_x() + b.get_width() / 2, v + top * 0.02, fmt(v), ha="center", va="bottom",
                   fontsize=12, fontweight="bold", color=HEX["WHITE"])
        a.set_xticks([0, 1], [l0, l1], fontsize=10)
        a.set_title(f"{title}\n", loc="left", fontsize=12.5, fontweight="bold")
        a.text(0, 1.02, f"{unit} · {'lower' if lower else 'higher'} is better · {adr}", transform=a.transAxes,
               fontsize=9, color=HEX["GREY"])
        a.set_ylim(base, base + top * 1.18)
        a.grid(axis="x", visible=False)
    fig.suptitle("Second round (2026-11-23): each lab pushed one step further, same metric before (grey) and after",
                 x=0.01, ha="left", fontsize=15, fontweight="bold", color=HEX["WHITE"])
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(IMG / "round2.png", dpi=150)


OPTIONS = [("cloud_on_demand", "Cloud on demand", "GREY"), ("cloud_reserved_1y", "Cloud 1-year reserved", "ICE"),
           ("cloud_reserved_3y", "Cloud 3-year reserved", "PURPLE"), ("onprem", "On-prem server (assumed)", "GREEN")]


def cost():
    """Cost per unit of work from evidence/cost_model.json (written by tools/cost_model.py)."""
    m = json.loads((ROOT / "evidence" / "cost_model.json").read_text())
    inp = json.loads((ROOT / "evidence" / "cost_inputs.json").read_text())
    vcpu, rate, be = inp["container_vcpu"], m["usd_per_vcpu_hour"], m["break_even_utilisation_vs_on_demand"]
    tok = m["measured"]["llm_cpu_q8_tok_s"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(17, 6.6), gridspec_kw={"width_ratios": [1.25, 1]})
    us = [u / 100 for u in range(5, 101)]
    for key, label, col in OPTIONS:
        per_m = rate[key] * vcpu / (tok * 3600) * 1e6
        ys = [per_m if key == "cloud_on_demand" else per_m / u for u in us]
        a.plot([u * 100 for u in us], ys, color=HEX[col], lw=2.6, label=label)
        if key in be:
            a.axvline(be[key] * 100, color=HEX[col], lw=1, ls=":")
            a.text(be[key] * 100 + 0.8, 1.6, f"break-even\n{be[key] * 100:.0f} %", color=HEX[col], fontsize=9.5)
    a.set_yscale("log")
    a.set_ylim(0.02, 3)
    a.set_yticks([0.03, 0.1, 0.3, 1, 3], ["$0.03", "$0.10", "$0.30", "$1", "$3"])
    a.minorticks_off()
    a.set_xlim(5, 100)
    a.set_xlabel("utilisation of the committed capacity, %")
    a.set_ylabel("USD per 1M output tokens (log)")
    a.set_title(f"LLM on CPU, Q8_0 at {tok} tok/s on {vcpu} vCPU\n", loc="left", fontweight="bold")
    a.text(0, 1.02, "committed capacity is paid when idle; on demand is paid only when used · ADR 0009",
           transform=a.transAxes, fontsize=9, color=HEX["GREY"])
    a.legend(loc="upper right", fontsize=10)
    row = m["sql_usd_per_thousand_runs"]["30%"]
    engines = [("polars", "Polars"), ("duckdb", "DuckDB"), ("pyspark", "PySpark")]
    w = 0.2
    for i, (key, label, col) in enumerate(OPTIONS):
        vals = [row[key][e] for e, _ in engines]
        xs = [j + (i - 1.5) * w for j in range(len(engines))]
        bars = b.bar(xs, vals, w * 0.92, color=HEX[col], label=label)
        for bar, v in zip(bars, vals):
            b.text(bar.get_x() + bar.get_width() / 2, v + 0.04, f"{v:.2f}", ha="center", fontsize=8.5,
                   color=HEX["WHITE"])
    b.set_xticks(range(len(engines)), [e for _, e in engines])
    b.set_ylabel("USD per 1,000 runs")
    b.set_title("Six-query SQL job on 200M rows, at 30 % utilisation\n", loc="left", fontweight="bold")
    b.text(0, 1.02, "the engine choice moves cost as much as the hosting choice · ADR 0008, 0009",
           transform=b.transAxes, fontsize=9, color=HEX["GREY"])
    b.grid(axis="x", visible=False)
    fig.suptitle("Cost per unit of work: measured throughput × dated cloud prices and stated on-prem assumptions",
                 x=0.01, ha="left", fontsize=14, fontweight="bold", color=HEX["WHITE"])
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(IMG / "cost.png", dpi=130)


if __name__ == "__main__":
    evidence()
    cost()
    round2()
    print("chart written")
