"""Reference platform diagram (Pillow): the eight labs as layers of one operator platform."""
from mfviz import GREEN, GREY, ICE, IMG, ORANGE, PURPLE, RED, WHITE, YELLOW, arrow, box, canvas, font


def platform():
    im, d = canvas(1600, 1000)
    d.text((60, 40), "MasterFabric reference data & AI platform", font=font(34, 800), fill=WHITE)
    d.text((60, 86), "Eight runnable labs, one architecture. Each box names the lab that measures it.",
           font=font(20, 450), fill=GREY)
    # sources
    box(d, (50, 170, 300, 420), "Operator sources", ["switch CDRs, sessions", "CRM, cell inventory", "radio KPIs (10 s)",
                                                     "all synthetic"], GREY, line_size=17)
    # ingestion
    box(d, (360, 170, 680, 330), "Streaming ingest", ["Kafka KRaft · Spark", "Structured Streaming", "realtime-telco"], ORANGE, line_size=17)
    box(d, (360, 360, 680, 500), "Batch landing", ["bronze, quarantine", "20-rule quality gate", "lakehouse-lab"], ICE, line_size=17)
    # lakehouse
    box(d, (740, 170, 1080, 500), "Lakehouse", ["Apache Iceberg v2", "REST catalog", "S3-compatible storage",
                                                 "bronze → silver → gold", "compaction, time travel", "lakehouse-lab"], ICE, line_size=17)
    # compute
    box(d, (1140, 170, 1550, 330), "Compute", ["Spark for big jobs", "Polars / DataFusion for", "small jobs · spark-rust-bench"], YELLOW, line_size=17)
    box(d, (1140, 360, 1550, 500), "Interactive SQL", ["Trino (Impala role)", "lakehouse-lab"], ICE, line_size=17)
    # ML / AI
    box(d, (360, 590, 760, 780), "ML lifecycle", ["Airflow monthly DAG", "drift + label decay gates", "MLflow aliases · FastAPI",
                                                   "airflow-mlops"], GREEN, line_size=17)
    box(d, (800, 590, 1180, 780), "On-prem LLM platform", ["Helm on Kubernetes", "llama.cpp / vLLM · pgvector", "RAG + guardrails",
                                                           "onprem-llm-stack"], PURPLE, line_size=17)
    box(d, (1220, 590, 1550, 780), "Serving choices", ["quantisation, KV cache", "GPU vs CPU, measured", "llm-serving-bench"],
        PURPLE, line_size=17)
    # cross-cutting
    box(d, (50, 830, 1000, 960), "Governance across every layer", ["PII detection and masking · column/row policies · audit",
                                                                    "policy-aware retrieval · LLM output guards · secure-data-ai"],
        RED, line_size=17)
    box(d, (1040, 830, 1550, 960), "Team foundations", ["Transformer, LoRA, GAN, RL from scratch",
                                                        "genai-foundations"], GREEN, line_size=17)
    arrow(d, (300, 250), (360, 250), ORANGE)
    arrow(d, (300, 400), (360, 430), ICE)
    arrow(d, (680, 250), (740, 250), ORANGE)
    arrow(d, (680, 430), (740, 430), ICE)
    arrow(d, (1080, 250), (1140, 250), YELLOW)
    arrow(d, (1080, 430), (1140, 430), ICE)
    arrow(d, (860, 500), (600, 590), GREEN)
    arrow(d, (960, 500), (990, 590), PURPLE)
    arrow(d, (1180, 685), (1220, 685), PURPLE)
    im.save(IMG / "platform.png", optimize=True)


if __name__ == "__main__":
    platform()
    print("diagram written")
