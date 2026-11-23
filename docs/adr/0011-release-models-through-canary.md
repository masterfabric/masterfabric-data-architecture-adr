# ADR 0011: Release models through a canary and a feature store, not only an offline gate

- Status: accepted
- Date: 2026-11-21
- Evidence: [masterfabric-airflow-mlops](https://github.com/masterfabric/masterfabric-airflow-mlops) (pinned at `3546e6f`)

## Context

ADR 0003 gates promotion on a challenger beating the champion on the same unseen month. An offline
gate cannot catch a model that is broken in a way the holdout does not show, or features that are
computed differently online than in training.

## Evidence

| Measured in airflow-mlops | Value |
|---|---|
| Canary, broken model | shuffled-label v6 rolled back at 5 % of traffic (Spearman −0.088 against the champion) |
| Canary, good model | v5 passed 5 %, 25 % and 50 %, paired ΔAUC −0.0007 [−0.0031, +0.0016]; promoted, **now the champion** |
| Feature store, point in time | 0 of 194,913 training rows differ from the hand-written join |
| Naive "latest" join | all 11,179 churners left without features |
| Rollback by alias | previous champion served after 3.41 s, no restart |

## Decision

- Every promotion goes **offline gate → shadow → canary at 5 %, 25 %, 50 % → champion**, with an
  automatic rollback when agreement with the champion or the paired metric fails a threshold.
- Training and serving read features from **one feature store** (Feast here) with point-in-time
  joins; a hand-written join is kept only as a test oracle.
- Evidently reports drift monthly for people to read; the retraining trigger stays the PSI rule
  from ADR 0003 (they agreed in 5 of 6 months).

## Consequences

- A release takes several scoring cycles instead of one alias move; rollback stays one alias move.
- The canary needs labelled outcomes or a proxy (here, agreement with the champion) to judge
  quickly; for slow labels the paired metric arrives a month later.
- Maps to model registry, A/B deployments and the feature store in Cloudera Machine Learning.
