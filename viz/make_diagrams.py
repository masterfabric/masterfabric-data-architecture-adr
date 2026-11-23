"""Diagrams (Pillow): the reference platform, and C4 context, container and component views.

The C4 element lists match docs/c4.md (Mermaid versions of the same diagrams)."""
from mfviz import GREEN, GREY, ICE, IMG, ORANGE, PANEL, PURPLE, RED, WHITE, YELLOW, arrow, box, canvas, font


def platform():
    im, d = canvas(1600, 1000)
    d.text((60, 40), "MasterFabric reference data & AI platform", font=font(34, 800), fill=WHITE)
    d.text((60, 86), "Eight runnable labs, one architecture. Each box names the lab that measures it. C4 views: docs/c4.md.",
           font=font(20, 450), fill=GREY)
    # sources
    box(d, (50, 170, 300, 420), "Operator sources", ["switch CDRs, sessions", "CRM, cell inventory", "radio KPIs (10 s)",
                                                     "all synthetic"], GREY, line_size=17)
    # ingestion
    box(d, (360, 170, 680, 330), "Streaming ingest", ["Kafka + Avro registry", "Flink 2.2 / Spark 3.5", "exactly-once · realtime-telco"], ORANGE, line_size=17)
    box(d, (360, 360, 680, 500), "Batch landing", ["bronze, quarantine", "WAP branch + audit gate", "lakehouse-lab"], ICE, line_size=17)
    # lakehouse
    box(d, (740, 170, 1080, 500), "Lakehouse", ["Apache Iceberg v2", "REST catalog", "S3-compatible storage",
                                                 "bronze → silver → gold", "compaction, time travel", "lakehouse-lab"], ICE, line_size=17)
    # compute
    box(d, (1140, 170, 1550, 330), "Compute", ["Spark for big jobs", "Polars / DuckDB for", "small jobs · spark-rust-bench"], YELLOW, line_size=17)
    box(d, (1140, 360, 1550, 500), "Interactive SQL", ["Trino (Impala role)", "lakehouse-lab"], ICE, line_size=17)
    # ML / AI
    box(d, (360, 590, 760, 780), "ML lifecycle", ["Airflow · MLflow · Feast", "drift gates, Evidently", "canary 5/25/50 % · FastAPI",
                                                   "airflow-mlops"], GREEN, line_size=17)
    box(d, (800, 590, 1180, 780), "On-prem LLM platform", ["Helm on Kubernetes", "llama.cpp · pgvector", "guards + classifier, reranker",
                                                           "onprem-llm-stack"], PURPLE, line_size=17)
    box(d, (1220, 590, 1550, 780), "Serving choices", ["quantisation, KV q8", "MLX, speculative decoding", "llm-serving-bench"],
        PURPLE, line_size=17)
    # cross-cutting
    box(d, (50, 830, 1000, 960), "Governance across every layer", ["PII masking · column/row policies · hash-chained audit · KVKK erasure",
                                                                    "GDPR/CCPA/KVKK request deadlines · retrieval filter · two guard layers · secure-data-ai"],
        RED, line_size=17)
    box(d, (1040, 830, 1550, 960), "Team foundations", ["Transformer, LoRA, WGAN-GP, diffusion,", "DPO and RL from scratch",
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




def person(d, cx, y, title, lines, color=ICE):
    d.ellipse((cx - 28, y, cx + 28, y + 56), fill=PANEL, outline=color, width=3)
    box(d, (cx - 160, y + 64, cx + 160, y + 190), title, lines, color, title_size=21, line_size=16)


def legend(d, y, items):
    x = 60
    for label, color in items:
        d.rounded_rectangle((x, y, x + 22, y + 22), radius=5, fill=color)
        d.text((x + 32, y), label, font=font(17, 500), fill=GREY)
        x += 44 + int(d.textlength(label, font=font(17, 500)))


def c4_context():
    im, d = canvas(1600, 1000)
    d.text((60, 36), "C4 level 1 · System context", font=font(34, 800), fill=WHITE)
    d.text((60, 82), "Who uses the platform and which systems it exchanges data with.", font=font(20, 450), fill=GREY)
    people = [("NOC engineer", ["typed alarms per cell"]), ("Analyst / data scientist", ["SQL, features, models"]),
              ("Customer-care agent", ["asks the RAG assistant"]), ("Data protection officer", ["GDPR/CCPA/KVKK requests, audit"])]
    xs = [230, 620, 1010, 1400]
    for cx, (t, ln) in zip(xs, people):
        person(d, cx, 130, t, ln, ICE)
    box(d, (360, 430, 1240, 640), "MasterFabric data and AI platform",
        ["lakehouse · streaming · batch compute · ML lifecycle", "on-prem LLMs with RAG · governance across all layers",
         "built and measured by 8 labs"], YELLOW, title_size=28, line_size=19)
    for cx, lab in zip(xs, ["alarms", "SQL, models", "questions", "requests, audit"]):
        arrow(d, (cx, 320), (min(max(cx, 420), 1180), 430), ICE, lab, at=0.45)
    ext = [("Radio network", ["KPI reports (10 s)", "via Kafka"]), ("Mediation", ["switch CDR files"]),
           ("Packet core", ["data sessions"]), ("CRM and billing", ["subscribers, plans"]),
           ("Model hub", ["open weights,", "downloaded once"])]
    ex = [50, 360, 670, 980, 1290]
    for x, (t, ln) in zip(ex, ext):
        box(d, (x, 760, x + 260, 900), t, ln, GREY, title_size=21, line_size=16)
        cx = x + 130
        if t == "Model hub":
            arrow(d, (1150, 640), (cx, 760), GREY, "weights", at=0.5)
        else:
            arrow(d, (cx, 760), (min(max(cx, 420), 1180), 640), GREY)
    legend(d, 940, [("person", ICE), ("the platform", YELLOW), ("external system", GREY)])
    d.text((1000, 940), "Synthetic data in every lab; no real operator system is connected.", font=font(16, 450), fill=GREY)
    im.save(IMG / "c4_context.png", optimize=True)


def c4_container():
    im, d = canvas(1600, 1060)
    d.text((60, 36), "C4 level 2 · Containers", font=font(34, 800), fill=WHITE)
    d.text((60, 82), "Deployable pieces of the platform; the last line of each box is the lab that measures it.",
           font=font(20, 450), fill=GREY)
    d.rounded_rectangle((30, 130, 1570, 1000), radius=24, outline=(90, 100, 125), width=2)
    d.text((50, 140), "MasterFabric platform", font=font(18, 650), fill=GREY)
    s = 16
    box(d, (60, 180, 400, 340), "Kafka + Schema Registry", ["Avro, BACKWARD rule", "realtime-telco"], ORANGE, 21, s)
    box(d, (60, 400, 400, 560), "Stream processing", ["Flink 2.2 · Spark 3.5", "exactly-once sinks", "realtime-telco"], ORANGE, 21, s)
    box(d, (480, 180, 1100, 400), "Iceberg lakehouse", ["Iceberg v2 · REST catalog · S3 storage",
        "bronze / silver / gold, WAP branches", "time travel, rollback", "lakehouse-lab"], ICE, 24, 17)
    box(d, (1180, 180, 1540, 340), "Batch compute", ["Spark for big jobs", "Polars / DuckDB small", "spark-rust-bench"], YELLOW, 21, s)
    box(d, (1180, 400, 1540, 560), "Interactive SQL", ["Trino", "lakehouse-lab"], ICE, 21, s)
    box(d, (60, 640, 460, 820), "ML lifecycle", ["Airflow · MLflow · Feast", "canary, FastAPI scoring", "airflow-mlops"], GREEN, 21, s)
    box(d, (540, 640, 1060, 820), "LLM platform", ["llama.cpp · pgvector · RAG API", "guards, classifier, reranker",
        "onprem-llm-stack · llm-serving-bench"], PURPLE, 21, s)
    box(d, (1140, 640, 1540, 820), "Observability", ["Prometheus · Grafana", "Marquez lineage", "onprem-llm-stack, lakehouse-lab"],
        GREY, 21, s)
    box(d, (480, 870, 1540, 980), "Governance services", ["PII masking · policies · hash-chained audit · erasure · request deadlines · secure-data-ai"],
        RED, 21, s)
    arrow(d, (230, 340), (230, 400), ORANGE, "consume")
    arrow(d, (400, 480), (560, 400), ORANGE, "commit", at=0.45)
    arrow(d, (1100, 260), (1180, 260), YELLOW)
    arrow(d, (1100, 360), (1180, 450), ICE)
    arrow(d, (640, 400), (300, 640), GREEN, "features", at=0.55)
    arrow(d, (800, 400), (800, 640), PURPLE, "documents")
    arrow(d, (1140, 730), (1060, 730), GREY)
    arrow(d, (1010, 870), (1010, 820), RED, "retrieval filter", at=0.3)
    arrow(d, (1100, 870), (1090, 400), RED, "masks, policies", at=0.62)
    d.text((60, 870), "Sources (RAN, core, CRM) enter", font=font(16, 450), fill=GREY)
    d.text((60, 895), "through Kafka and file landing.", font=font(16, 450), fill=GREY)
    legend(d, 1020, [("streaming", ORANGE), ("storage, SQL", ICE), ("compute", YELLOW), ("ML", GREEN), ("LLM", PURPLE),
                      ("governance", RED)])
    im.save(IMG / "c4_container.png", optimize=True)


def c4_component():
    im, d = canvas(1600, 900)
    d.text((60, 36), "C4 level 3 · Components of the governed RAG API", font=font(34, 800), fill=WHITE)
    d.text((60, 82), "Order of checks for one question. Measured values come from onprem-llm-stack and secure-data-ai.",
           font=font(20, 450), fill=GREY)
    s = 16
    row1 = [("Input rules", ["regex, encodings"], RED), ("Risk classifier", ["Granite Guardian 3.2", "held-out 10/16 stopped"], RED),
            ("Retriever", ["pgvector HNSW", "hit@4 0.933"], ICE), ("Entitlement filter", ["role policies, PII", "masked (ADR 0006)"], RED)]
    row2 = [("Reranker", ["bge-reranker-v2-m3", "hit@1 0.833→0.933, +3.8 s"], PURPLE), ("Generator", ["llama.cpp", "cites passages"], PURPLE),
            ("Output guard", ["PII, prompt leak", "LLM02 6/8 → 0/8"], RED), ("Audit log", ["SHA-256 hash chain", "tamper-evident"], GREY)]
    xs = [60, 440, 820, 1200]
    for x, (t, ln, c) in zip(xs, row1):
        box(d, (x, 200, x + 340, 360), t, ln, c, 22, s)
    for x, (t, ln, c) in zip(xs, row2):
        box(d, (x, 520, x + 340, 680), t, ln, c, 22, s)
    for a in range(3):
        arrow(d, (xs[a] + 340, 280), (xs[a + 1], 280), GREY)
    arrow(d, (1370, 360), (230, 520), GREY, "allowed chunks", at=0.5)
    for a in range(3):
        arrow(d, (xs[a] + 340, 600), (xs[a + 1], 600), GREY)
    d.text((60, 140), "question from a customer-care agent  →", font=font(18, 600), fill=ICE)
    d.text((820, 700), "↓ answer with citations back to the agent", font=font(18, 600), fill=ICE)
    d.text((60, 780), "The reranker runs only on request because it adds 3.8 s on CPU. Some held-out attacks pass both input layers;",
           font=font(17, 450), fill=GREY)
    d.text((60, 806), "the entitlement filter and output guard are what keep data a role may not read out of the answer (ADR 0012).",
           font=font(17, 450), fill=GREY)
    im.save(IMG / "c4_component.png", optimize=True)


if __name__ == "__main__":
    platform()
    c4_context()
    c4_container()
    c4_component()
    print("diagrams written")
