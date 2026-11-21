# ADR 0008: Two compute paths: Spark for big jobs, a single-node Rust engine for small ones

- Status: accepted
- Date: 2026-11-21
- Evidence: [masterfabric-spark-rust-bench](https://github.com/masterfabric/masterfabric-spark-rust-bench) (pinned at `aeac1b1`)

## Context

Many jobs on a Spark cluster read a day or a month of one table. They pay JVM start-up, scheduling
and memory overhead built for much larger data.

## Decision

- Offer a **single-node path** (Polars or DataFusion in a container) next to Spark for jobs whose
  input fits one machine; keep Spark for everything larger.
- Keep **SQL portable** so a job can move between paths without a rewrite; both read Iceberg.
- In Spark, prefer built-in functions; never row-at-a-time Python UDFs.

## Evidence

| Measured in spark-rust-bench (6 CPU / 8 GiB containers, 50M rows) | Value |
|---|---|
| Same 5 SQL queries, sum of medians | PySpark 3.731 s · Scala 3.929 s · Polars 0.966 s · DataFusion 1.450 s |
| Peak memory | PySpark 3,616 MiB · Scala 5,055 MiB · Polars 1,766 MiB |
| Correctness | 60 of 60 query results identical |
| Same column in Spark | built-in 0.273 s vs Python UDF 6.613 s |

## Consequences

- Two runtimes to operate; the single-node path needs its own resource limits and scheduling.
- The benchmark is single-node; it does not show where a cluster starts to win.
