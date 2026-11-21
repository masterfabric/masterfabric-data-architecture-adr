# Reference architecture in diagrams

All diagrams are Mermaid, so GitHub renders them and they stay editable in review. Lab names in
brackets point to the repository that runs and measures that part.

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
    K[Kafka<br/>realtime-telco] --> SS[Spark Structured Streaming<br/>realtime-telco]
    B[Batch landing + quality gate<br/>lakehouse-lab]
  end
  subgraph LH[Lakehouse · ADR 0001]
    ICE[(Apache Iceberg v2<br/>REST catalog · S3 storage)]
  end
  subgraph CMP[Compute · ADR 0008]
    SP[Spark<br/>big jobs]
    PL[Polars / DataFusion<br/>small jobs]
    TR[Trino<br/>interactive SQL]
  end
  subgraph AI[ML and GenAI]
    ML[Airflow + MLflow + FastAPI<br/>airflow-mlops · ADR 0003]
    LLM[Helm: llama.cpp / vLLM, pgvector, RAG<br/>onprem-llm-stack · ADR 0004/0005]
  end
  GOV[[Governance: PII masking, role policies, audit,<br/>policy-aware retrieval, output guards<br/>secure-data-ai · ADR 0006]]
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

## 3. Model lifecycle, one month (ADR 0003)

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
  C -- yes --> P[Move @champion alias]
  P --> API[FastAPI follows alias<br/>no restart]
```

## 4. A governed RAG request (ADR 0004 and 0006)

```mermaid
flowchart LR
  U[User + role] --> G1{Input guard}
  G1 -- attack --> X[Refuse]
  G1 -- ok --> EM[Embed question]
  EM --> R[(pgvector top-k)]
  R --> F[Entitlement filter<br/>+ PII masking]
  F --> G2{Context guard}
  G2 --> M[LLM<br/>llama.cpp CPU / vLLM GPU]
  M --> G3{Output guard<br/>PII, prompt leak}
  G3 --> A[Answer or refusal]
```

## 5. Choosing a compute path for a new job (ADR 0008)

```mermaid
flowchart TD
  J[New batch job] --> F{Input after pruning<br/>fits one node?}
  F -- yes --> S{Needs cluster fault tolerance<br/>or platform-only integration?}
  S -- no --> P[Polars / DataFusion container]
  S -- yes --> SP[Spark]
  F -- no --> SP
  SP --> U{Custom logic?}
  U -- yes --> B[Built-ins, then Arrow UDF,<br/>Scala for hot paths]
```

## 6. Mapping to a Cloudera estate

| Layer | Lab implementation | Cloudera Data Platform |
|---|---|---|
| Streaming | Kafka KRaft, Spark Structured Streaming | Streams Messaging (Kafka), CDE Spark or CSA (Flink) |
| Lakehouse | Iceberg v2, REST catalog, S3-compatible storage | Iceberg in CDP, HMS/REST catalog, Ozone or S3 |
| Batch compute | Spark 3.5, Polars, DataFusion | Cloudera Data Engineering; single-node jobs in CML |
| Interactive SQL | Trino | Cloudera Data Warehouse (Impala, Hive) |
| ML lifecycle | Airflow, MLflow, FastAPI | CDE Airflow, Cloudera Machine Learning registry and serving |
| LLM serving | Helm chart, llama.cpp / vLLM, pgvector | Cloudera AI Inference service, CML on GPU nodes |
| Governance | PII detectors, role policies, retrieval filter | Ranger, Atlas, Cloudera Data Catalog (SDX) |
