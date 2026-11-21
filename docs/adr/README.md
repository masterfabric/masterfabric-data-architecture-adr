# Architecture decision records

| ADR | Decision | Evidence |
|---|---|---|
| [0001](0001-iceberg-lakehouse.md) | Open lakehouse on Apache Iceberg with a REST catalog | lakehouse-lab |
| [0002](0002-streaming-event-time.md) | Kafka + Spark Structured Streaming, event time, adaptive detection | realtime-telco |
| [0003](0003-gated-ml-lifecycle.md) | ML lifecycle gated by data quality and evidence | airflow-mlops |
| [0004](0004-onprem-llm-platform.md) | On-prem LLMs, RAG and layered guardrails on Kubernetes | onprem-llm-stack |
| [0005](0005-measure-serving-choices.md) | Serving hardware and quantisation chosen by measurement | llm-serving-bench |
| [0006](0006-govern-data-before-ai.md) | Governance enforced before data reaches a model | secure-data-ai |
| [0007](0007-understand-the-models.md) | First-principles team knowledge; LoRA for adaptation | genai-foundations |
| [0008](0008-two-compute-paths.md) | Spark for big jobs, a single-node engine (Polars or DuckDB) for small ones | spark-rust-bench |
| [0009](0009-cost-onprem-vs-cloud.md) | Place workloads by measured cost per unit of work | cost model on serving-bench, spark-rust-bench, realtime-telco |
| [0010](0010-streaming-engine.md) | Flink for new low-latency streams; Spark where Spark already runs | realtime-telco |
| [0011](0011-release-models-through-canary.md) | Release models through a canary and a feature store | airflow-mlops |
| [0012](0012-evaluate-guards-on-held-out-attacks.md) | Judge LLM guardrails on held-out attacks and legitimate traffic | onprem-llm-stack, secure-data-ai |

Format: context, decision, evidence (numbers from the linked lab, verified by
`tools/check_claims.py`), consequences. Each lab also keeps its own detailed ADRs. ADRs 0001-0008 carry a dated
update section for the additions measured on 2026-11-21.
