# ADR 0001: An open lakehouse on Apache Iceberg with a REST catalog

- Status: accepted
- Date: 2026-11-21
- Evidence: [masterfabric-lakehouse-lab](https://github.com/masterfabric/masterfabric-lakehouse-lab) (pinned at `bea60a2`)

## Context

An operator's analytics estate has several engines (Spark for pipelines, an interactive SQL engine
for analysts, Python for data science) and data that must change after it lands: re-rated calls,
late mediation files, schema changes from vendors. The table layer has to give all engines one
consistent view and survive those changes without rewrites.

## Decision

- Store analytical data as **Apache Iceberg v2** tables in **S3-compatible object storage**, with a
  **REST catalog** so Spark and Trino resolve the same table names.
- Land data through a **medallion** flow: bronze keeps every raw value plus lineage, silver
  enforces contracts and sends rule-breaking records to quarantine, gold holds business marts.
- Make convergence explicit: duplicates and late records reach one row through `MERGE INTO` on the
  business key, and a **20-rule quality gate** reconciles against the producer's manifest.
- Schedule **table maintenance** (compaction, delete-file rewrite, snapshot expiry) as part of the
  platform, not as an afterthought.

## Evidence

| Measured in lakehouse-lab | Value |
|---|---|
| Scale test, 0.26M → 2.1M raw rows | 8× the data costs 2.1× the time (68.59 s end to end at 2,097,761 rows, quality gate 20/20) |
| Compaction | 71 + 2 data and delete files → 14 + 0 |
| One-day query, median of 7 | 67.8 ms → 28.9 ms after maintenance |
| Trino on the same tables | 135 ms end to end, 51 ms of it planning |

## Consequences

- Any engine that speaks the Iceberg REST catalog can join later (Impala in CDP, Flink, Polars).
- Maintenance is a scheduled job with its own SLO; small files come back with every streaming or
  small-batch writer (see ADR 0002).
- In a Cloudera estate this maps to Iceberg tables in CDP with Spark (CDE) and Impala (CDW).
