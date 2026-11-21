# ADR 0003: An ML lifecycle where data quality and evidence gate every step

- Status: accepted
- Date: 2026-11-21
- Evidence: [masterfabric-airflow-mlops](https://github.com/masterfabric/masterfabric-airflow-mlops) (pinned at `ea335bc`)

## Context

Churn and similar models decay: labels arrive a month late, feeds break, and the market changes.
Retraining on a timer wastes effort and can ship a worse model; never retraining loses value.

## Decision

- Orchestrate the monthly cycle in **Airflow**: land, quality gate, score last month once labels
  arrive, check feature drift (PSI), decide whether to retrain.
- A broken feed **halts** the month and is excluded from training.
- A challenger is promoted only if it beats the champion **on the same unseen month**; promotion is
  an **MLflow registry alias**, and the serving API follows the alias without a restart.

## Evidence

| Measured in airflow-mlops | Value |
|---|---|
| Quality gate | 2026-03 halted and excluded |
| Promotion gate | v2 rejected (2026-07, lost by 0.0003 AUC) |
| Drift trigger | PSI of `plan` 0.3151 (threshold 0.25) |
| Realised AUC, 2026-10 | auto policy 0.830 vs never retrained 0.789 (oracle 0.841) |
| Top-decile lift, 2026-10 | 4.98 vs 4.63 |
| Online scoring | p50 2.67 ms per subscriber |
| Rollback by alias | old champion served after 3.41 s, no restart |

## Consequences

- Every model decision leaves a record (gate result, drift value, comparison) that an auditor can read.
- Maps to Airflow in CDE plus model registry and serving in Cloudera Machine Learning.

## Update 2026-11-21: canary releases, a feature store and Evidently (airflow-mlops `ea335bc`)

- The offline gate is no longer the last step: a promoted model goes to a **canary** (5 %, 25 %,
  50 % of traffic, shadow-scored). A shuffled-label v6 was **rolled back at 5 %**; v5 passed all
  three stages (paired ΔAUC −0.0007, interval [−0.0031, +0.0016]) and was promoted. **The current
  champion is v5.** ADR 0011 records this.
- **Feast** serves the same features to training (point in time) and to the API: 0 of 194,913
  training rows differ from the hand-written join, while a naive latest join would have left all
  11,179 churners without features.
- **Evidently's** default drift test flagged columns in all 6 monitored months; the PSI > 0.25
  trigger used here agreed in 5 of 6, so it stays as the retraining signal.
