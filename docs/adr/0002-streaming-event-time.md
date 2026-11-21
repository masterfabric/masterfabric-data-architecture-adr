# ADR 0002: Streaming on Kafka and Spark Structured Streaming, judged on event time

- Status: accepted
- Date: 2026-11-21
- Evidence: [masterfabric-realtime-telco](https://github.com/masterfabric/masterfabric-realtime-telco) (pinned at `0e6637e`)

## Context

Network KPIs arrive late, out of order and sometimes twice, the way real mediation chains deliver
them. Alerts drive field operations, so false alerts cost money and missed incidents cost more.

## Decision

- **Kafka** as the backbone; **Spark Structured Streaming** writes bronze, silver and gold
  **Iceberg** tables (one table format for batch and streaming, ADR 0001).
- Window on **event time with watermarks**, deduplicate on event id, and keep very late rows in
  bronze rather than silently dropping them.
- Detect with a **per-cell adaptive detector** (hard rules, EWMA z-scores and a Bernoulli CUSUM) instead of static
  thresholds, and score every alert against ground truth before trusting it.
- Compact streaming tables on a schedule.

## Evidence

| Measured in realtime-telco | Value |
|---|---|
| Live run | 520,931 events delivered in 12 minutes; 2,531 duplicates removed |
| Adaptive detector, held-out seed | 36/36 incidents, 45 alerts, 2 false, precision 0.956 |
| Static thresholds, same windows | 334 alerts, 253 false, precision 0.243 |
| Last report → alert | p50 9.8 s |
| Bronze drain throughput | 125,611 events/s |
| Per-cell aggregate after compaction | 736.9 ms → 43.5 ms |

## Consequences

- Latency is bounded below by the watermark; correctness for late data is paid in seconds.
- Detector thresholds are tuned on a development seed and judged on a held-out one, like a model.
- In Cloudera terms: Kafka in CDP Streams Messaging, Spark Streaming in CDE or Flink in CSA.
