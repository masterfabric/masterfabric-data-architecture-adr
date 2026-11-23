# Reference architecture in diagrams

All diagrams are Mermaid, so GitHub renders them and they stay editable in review. Lab names in
brackets point to the repository that runs and measures that part. The same platform as C4 context,
container and component views is in [c4.md](c4.md); cost per unit of work is in
[ADR 0009](adr/0009-cost-onprem-vs-cloud.md).

## 1. Platform layers

```mermaid
flowchart TB
  subgraph SRC[Sources]
    CDR[Switch CDRs]
    PC[Packet-core sessions]
    CRM[CRM / billing]
    KPI[Radio KPIs, 10 s]
  end
  subgraph ING[Ingest]
    K[Kafka + Avro schema registry<br/>realtime-telco] --> SS[Flink 2.2 or Spark Structured Streaming<br/>realtime-telco · ADR 0010]
    B[Batch landing, quality gate,<br/>WAP branch + audit<br/>lakehouse-lab]
  end
  subgraph LH[Lakehouse · ADR 0001]
    ICE[(Apache Iceberg v2<br/>REST catalog · S3 storage)]
  end
  subgraph CMP[Compute · ADR 0008]
    SP[Spark<br/>big jobs]
    PL[Polars / DuckDB<br/>small jobs]
    TR[Trino<br/>interactive SQL]
  end
  subgraph AI[ML and GenAI]
    ML[Airflow + MLflow + Feast + FastAPI<br/>canary releases<br/>airflow-mlops · ADR 0003/0011]
    LLM[Helm: llama.cpp / vLLM, pgvector, RAG<br/>onprem-llm-stack · ADR 0004/0005]
  end
  GOV[[Governance: PII masking, role policies, hash-chained audit,<br/>KVKK erasure, GDPR/CCPA/KVKK request deadlines,<br/>policy-aware retrieval, two guard layers<br/>secure-data-ai · ADR 0006/0012/0013]]
  KPI --> K
  CDR & PC & CRM --> B
  SS --> ICE
  B --> ICE
  ICE --> SP & PL & TR
  ICE --> ML
  ICE --> LLM
  GOV -.-> ICE & TR & ML & LLM
```

## 2. Streaming path, from report to alert (ADR 0002)

Shown with the Spark job the lab started with; the Flink job (ADR 0010) computes the same windows (identical results) and
drained the same 1.04M records in 3.07 s instead of 10.54 s.

```mermaid
sequenceDiagram
  participant Cell as Radio cell
  participant K as Kafka cell.kpi
  participant S as Spark streaming
  participant I as Iceberg bronze/silver
  participant D as Adaptive detector
  participant O as rt.alerts + cell.alerts
  Cell->>K: KPI report (late, out of order, sometimes twice)
  K->>S: micro-batch
  S->>I: bronze (all rows), silver (dedup, event-time windows)
  Note over S,I: window closes when the watermark passes
  I->>D: finalised window
  D->>O: MERGE alert + Kafka (measured p50 9.8 s from last report)
```

## 3. Model lifecycle, one month (ADR 0003, 0011)

```mermaid
flowchart LR
  L[Land snapshot] --> Q{Quality gate<br/>11 rules}
  Q -- fail --> H[Halt month<br/>exclude from training]
  Q -- pass --> E[Score last month<br/>with arrived labels]
  E --> DR{Decay or<br/>PSI drift?}
  DR -- no --> K[Keep champion]
  DR -- yes --> T[Train challenger]
  T --> C{Beats champion<br/>on same unseen month?}
  C -- no --> K
  C -- yes --> CN{Canary 5 / 25 / 50 %<br/>agrees with champion?}
  CN -- no --> RB[Roll back<br/>v6: at 5 %]
  CN -- yes --> P[Move @champion alias<br/>v5 is the champion]
  P --> API[FastAPI follows alias<br/>no restart]
```

## 4. A governed RAG request (ADR 0004, 0006 and 0012)

```mermaid
flowchart LR
  U[User + role] --> G1{Input guard}
  G1 -- attack --> X[Refuse]
  G1 -- ok --> CL{Risk classifier<br/>Granite Guardian}
  CL -- attack --> X
  CL -- ok --> EM[Embed question]
  EM --> R[(pgvector top-k)]
  R --> F[Entitlement filter<br/>+ PII masking]
  F --> RR[Reranker<br/>on request]
  RR --> G2{Context guard}
  G2 --> M[LLM<br/>llama.cpp CPU / vLLM GPU]
  M --> G3{Output guard<br/>PII, prompt leak}
  G3 --> A[Answer or refusal]
```

## 5. A data-subject request, intake to response (ADR 0006 and 0013)

Not legal advice: the periods are one simplified engineering reading; see the
[comparison in secure-data-ai](https://github.com/masterfabric/masterfabric-secure-data-ai/blob/main/docs/dsr-gdpr-ccpa-kvkk.md).

```mermaid
flowchart LR
  IN[Intake<br/>receipt date · law · type] --> DL[Deadline rule table<br/>GDPR 1 calendar month · CCPA 45 days<br/>opt-out 15 business days · KVKK 30 days]
  DL --> V{Verify identity<br/>2 factors · CCPA opt-out 1}
  V -- not enough --> NI[Ask for more information] --> V
  V -- verified --> P[Process<br/>access · erasure · consent / opt-out]
  P -- post-checks pass --> R[Respond<br/>on time vs due date]
  P -- post-checks fail --> T
  DL -.->|notice on or before due date| EX[Extension<br/>GDPR +2 months · CCPA +45 days]
  DL -.-> T[Tracker<br/>ok · due soon · overdue]
  IN & V & P & R -.-> L[(Hash-chained audit<br/>subject as pseudonym)]
```

## 6. Choosing a compute path for a new job (ADR 0008)

```mermaid
flowchart TD
  J[New batch job] --> F{Input after pruning<br/>fits one node?}
  F -- yes --> S{Needs cluster fault tolerance<br/>or platform-only integration?}
  S -- no --> P[Polars or DuckDB container]
  S -- yes --> SP[Spark]
  F -- no --> SP
  SP --> U{Custom logic?}
  U -- yes --> B[Built-ins, then Arrow UDF,<br/>Scala for hot paths]
```

## 7. Mapping to a Cloudera estate

| Layer | Lab implementation | Cloudera Data Platform |
|---|---|---|
| Streaming | Kafka KRaft, Avro schema registry, Flink 2.2, Spark Structured Streaming | Streams Messaging (Kafka, Schema Registry), CSA (Flink), CDE Spark |
| Lakehouse | Iceberg v2, REST catalog, S3-compatible storage, WAP branches, OpenLineage + Marquez | Iceberg in CDP, HMS/REST catalog, Ozone or S3, Atlas lineage |
| Batch compute | Spark 3.5, Polars, DuckDB | Cloudera Data Engineering; single-node jobs in CML |
| Interactive SQL | Trino | Cloudera Data Warehouse (Impala, Hive) |
| ML lifecycle | Airflow, MLflow, Feast, Evidently, FastAPI canary | CDE Airflow, Cloudera Machine Learning registry, feature store and serving |
| LLM serving | Helm chart, llama.cpp / vLLM, pgvector, reranker, Prometheus + Grafana | Cloudera AI Inference service, CML on GPU nodes |
| Governance | PII detectors, role policies, retrieval filter, hash-chained audit, erasure, request deadlines | Ranger, Atlas, Cloudera Data Catalog (SDX) |
