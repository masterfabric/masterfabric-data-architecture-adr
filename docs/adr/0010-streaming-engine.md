# ADR 0010: Flink for new low-latency streaming jobs; Spark Structured Streaming where Spark already runs

- Status: accepted
- Date: 2026-11-21
- Evidence: [masterfabric-realtime-telco](https://github.com/masterfabric/masterfabric-realtime-telco) (pinned at `456e642`)

## Context

ADR 0002 chose Kafka with Spark Structured Streaming on event time. The realtime lab has since run the
same windowed KPI job on Apache Flink 2.2 against Spark 3.5, on the same Kafka topics, and killed both
mid-stream to test delivery guarantees.

## Evidence

| Measured in realtime-telco | Spark 3.5 | Flink 2.2 |
|---|---:|---:|
| Drain 1.04M records | 10.54 s | 3.07 s |
| Live latency p50 | 4.1 s | 2.6 s |
| Average CPU during the live feed | 83 % | 12 % |
| Window results | identical | identical |
| Duplicates after `kill -9` | Spark → Iceberg: 0 (521,044/521,044 offsets) | exactly-once sink: 0; at-least-once: 4,080 |

## Decision

- **New streaming jobs with a latency or CPU budget** (alarms, fraud, real-time KPIs) use **Flink**,
  with its exactly-once Kafka sink or a transactional table sink. Flink used 6.9 times less CPU for
  the same job (ADR 0009 turns that into cost).
- **Jobs that land streams in Iceberg next to Spark batch** may stay on **Spark Structured
  Streaming**: its checkpointed Iceberg commits gave 0 duplicates too, and one engine is simpler to run.
- Exactly-once is chosen explicitly per sink and tested with a kill; at-least-once is only allowed
  for sinks that deduplicate on a key.
- Producers register **Avro schemas** with a BACKWARD rule; the registry rejected an incompatible
  change with 409 before any consumer saw it.

## Consequences

- Two streaming engines to operate; Flink needs its own checkpoint storage and upgrade procedure.
- Maps to Cloudera Streaming Analytics (Flink) and CDE Spark; Schema Registry in Streams Messaging.
- Measured on one laptop with one job; the CPU ratio for other jobs must be measured, not assumed.
