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
    ("Small-job engine", "5 queries, 50M rows, s", "PySpark", C["sr_sum"]["pyspark"],
     "Polars", C["sr_sum"]["polars"], True, "ADR 0008", "YELLOW"),
]


def fmt(v):
    if isinstance(v, float):
        return f"{v:.3f}" if v < 1 else f"{v:,.3f}".rstrip("0").rstrip(".")
    return f"{v:,}"


def evidence():
    fig, axes = plt.subplots(2, 4, figsize=(18, 8.4))
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


if __name__ == "__main__":
    evidence()
    print("chart written")
