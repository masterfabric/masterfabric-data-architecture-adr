# ADR 0008: Two compute paths: Spark for big jobs, a single-node Rust engine for small ones

- Status: accepted
- Date: 2026-11-21
- Evidence: [masterfabric-spark-rust-bench](https://github.com/masterfabric/masterfabric-spark-rust-bench) (pinned at `8a6e137`)

## Context

Many jobs on a Spark cluster read a day or a month of one table. They pay JVM start-up, scheduling
and memory overhead built for much larger data.

## Decision

- Offer a **single-node path** (Polars or DuckDB in a container; see the update below) next to Spark for jobs whose
  input fits one machine; keep Spark for everything larger.
- Keep **SQL portable** so a job can move between paths without a rewrite; both read Iceberg.
- In Spark, prefer built-in functions; never row-at-a-time Python UDFs.

## Evidence

| Measured in spark-rust-bench (6 CPU / 8 GiB containers, 200M rows) | Value |
|---|---|
| Same 6 SQL queries, sum of medians | PySpark 15.975 s · Scala 15.922 s · Polars 4.325 s · DuckDB 4.777 s |
| Peak memory | PySpark 7.6 GiB · Scala 7.1 GiB · Polars 3.6 GiB · DuckDB 3.2 GiB |
| Correctness | 234 of 234 query results identical (10M to 200M rows, Parquet and Iceberg) |
| Same column in Spark | built-in 0.846 s vs Python UDF 24.754 s |

## Consequences

- Two runtimes to operate; the single-node path needs its own resource limits and scheduling.
- The benchmark is single-node; it does not show where a cluster starts to win.

## Update 2026-11-21: DuckDB, Iceberg reads and 200M rows (spark-rust-bench `8a6e137`)

- **DuckDB** joins Polars on the single-node path: at 200M rows the six queries took 4.777 s (DuckDB)
  and 4.325 s (Polars) against 15.975 s for PySpark, with 3.2 and 3.6 GiB peak memory against 7.6 GiB.
  DataFusion was killed at the 8 GiB limit at 200M rows and is no longer recommended as a stand-alone tool.
- **The gap narrows with size but stays large on one node:** PySpark / Polars 5.9x at 10M rows, 3.7x
  at 200M. The crossover to a cluster is still unmeasured.
- **Single-node engines read the lakehouse's Iceberg tables directly**; a one-week filter read 20 of 92
  files and DuckDB's Q6 dropped from 0.693 to 0.314 s.
- **Spark needs `TIMESTAMP_NTZ` literals** on zone-less timestamp columns: with the portable literal
  Q6 took 2.989 s on Iceberg, with `TIMESTAMP_NTZ` 0.742 s, because only then does the filter reach the scan.
- The cost per run of each path is in ADR 0009.
