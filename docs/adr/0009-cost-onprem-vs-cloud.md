# ADR 0009: Place workloads by measured cost per unit of work, not by list price per server

- Status: accepted
- Date: 2026-11-21
- Evidence: [`tools/cost_model.py`](../../tools/cost_model.py) on measured throughput from
  [llm-serving-bench](https://github.com/masterfabric/masterfabric-llm-serving-bench) (`0bdc279`),
  [spark-rust-bench](https://github.com/masterfabric/masterfabric-spark-rust-bench) (`8a6e137`) and
  [realtime-telco](https://github.com/masterfabric/masterfabric-realtime-telco) (`8776322`)

## Context

An operator with its own data centres has to decide, per workload, whether to run on its own
servers or in a public cloud. Price lists compare servers; the decision needs cost per token, per
job or per stream, which depends on how much work a vCPU does and how busy the capacity is.

The model ([`evidence/cost_inputs.json`](../../evidence/cost_inputs.json), output in
[`evidence/cost_model.json`](../../evidence/cost_model.json)) multiplies three things:

1. **Measured work per vCPU**, read from verified claims: 328 output tok/s for Qwen2.5-1.5B Q8_0 in a
   6 vCPU container (184 tok/s at Q4_K_M); 4.325 s (Polars), 4.777 s (DuckDB) and 15.975 s (PySpark)
   for six SQL queries on 200M rows in the same container.
2. **Cloud list prices**: AWS m7g.2xlarge (8 vCPU arm64), US East, as listed on 2026-11-21:
   $0.3264/h on demand, $0.216/h 1-year reserved, $0.148/h 3-year reserved, so $0.0408, $0.0270 and
   $0.0185 per vCPU-hour.
3. **An on-prem server, as an assumption** (to replace with a real quote): $20,000 for 128 vCPU over
   5 years, 0.6 kW at PUE 1.5 and $0.12/kWh, operations 15% of the purchase price per year. That gives
   $0.0071 per vCPU-hour if every hour is used.

Committed capacity (on-prem or reserved) costs the same whether it is busy or not, so its cost per
*used* hour is its rate divided by utilisation. On-demand is paid only while used (assuming the
workload scales to zero).

## Results

| | On demand | 1-year reserved | 3-year reserved | On-prem (assumed server) |
|---|---:|---:|---:|---:|
| USD per vCPU-hour, fully used | 0.0408 | 0.0270 | 0.0185 | 0.0071 |
| Break-even utilisation against on demand | | 66% | 45% | **17%** |
| LLM, USD per 1M output tokens (Q8_0, CPU), 30% busy | 0.207 | 0.457 | 0.313 | 0.120 |
| LLM, USD per 1M output tokens (Q8_0, CPU), 100% busy | 0.207 | 0.137 | 0.094 | 0.036 |
| SQL, USD per 1,000 runs, Polars, 30% busy | 0.294 | 0.649 | 0.445 | 0.170 |
| SQL, USD per 1,000 runs, PySpark, 30% busy | 1.086 | 2.396 | 1.642 | 0.629 |

The engine choice moves cost as much as the hosting choice: PySpark took 3.69 times as long as
Polars for the same SQL, so it costs 3.69 times as much on any hosting; Spark used 6.92 times the
CPU of Flink for the same streaming job. The quantisation choice does too: Q4_K_M on CPU costs 1.78
times Q8_0 per token because it is slower there (ADR 0005).

## Decision

- Run **steady, predictable workloads on-prem** (streaming, scheduled batch, an always-on LLM
  endpoint): with the assumed server they are cheaper than on-demand cloud above about 17%
  utilisation, and cheaper than 3-year reserved capacity used to the same degree ($0.0071 vs
  $0.0185 per vCPU-hour).
- Use **on-demand cloud for bursty or exploratory work** that is idle most of the time, and for
  capacity the operator cannot buy in time (for example GPUs for a pilot).
- **Choose the engine and model format before the hosting:** the measured 3.7x (PySpark vs Polars),
  6.9x (Spark vs Flink CPU) and 1.8x (Q4_K_M vs Q8_0 on CPU) factors are as large as the hosting gap.
- Re-run `python tools/cost_model.py` with real quotes and the operator's own utilisation before a
  purchase; the structure stays, the numbers will change.

## Consequences

- Cost becomes a reviewable artefact in the same repository as the evidence; a re-pinned lab changes
  the cost model automatically (the test `test_written_model_is_current` fails until it is re-run).
- Not modelled: staff beyond the operations share, network egress, storage, software licences,
  GPU prices, data-residency obligations (which under KVKK can rule out a cloud region regardless of
  cost), and the speed difference between an M4 Pro vCPU in Colima and a Graviton3 vCPU.
