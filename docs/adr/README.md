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
| [0008](0008-two-compute-paths.md) | Spark for big jobs, a single-node Rust engine for small ones | spark-rust-bench |

Format: context, decision, evidence (numbers from the linked lab, verified by
`tools/check_claims.py`), consequences. Each lab also keeps its own detailed ADRs.
