# ADR 0001: An open lakehouse on Apache Iceberg with a REST catalog

- Status: accepted
- Date: 2026-11-21
- Evidence: [masterfabric-lakehouse-lab](https://github.com/masterfabric/masterfabric-lakehouse-lab) (pinned at `6ba927f`)

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

## Update 2026-11-21: write-audit-publish on branches (lakehouse-lab `2382c11`)

- New data lands on an **Iceberg audit branch**, is checked by Great Expectations, and is published by
  `fast_forward` only if every expectation passes; `main` never shows unaudited rows.
- Measured: release 2.3 passed 11/11 expectations and was published; the buggy release 2.4 passed
  8/11 and was blocked; 0 new rows were visible on `main` during either audit. An accidental delete
  was undone by `rollback_to_snapshot` to a tag: 138,373 rows restored in 0.057 s, metadata only.
- Consequence: publishing becomes a gated step, like model promotion in ADR 0003.

## Update 2026-11-23: table maintenance as a scheduled job (lakehouse-lab `6ba927f`)

- Two tables received the same 60 batches with MERGE updates. Without maintenance the one-day query
  slowed to 156.5 ms over 74 data files and 10 position-delete files; maintained every 20 batches
  (rewrite data files, rewrite position deletes, rewrite manifests, expire snapshots) it stayed at
  28.1 ms over 5 data files and no delete files.
- Decision added: maintenance runs on a schedule tied to write volume, not on demand; orphan-file
  cleanup keeps an age guard so files of running writers are never deleted.
