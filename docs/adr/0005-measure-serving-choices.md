# ADR 0005: Choose serving hardware and quantisation by measurement, per workload

- Status: accepted
- Date: 2026-11-21
- Evidence: [masterfabric-llm-serving-bench](https://github.com/masterfabric/masterfabric-llm-serving-bench) (pinned at `06e944f`)

## Context

"Use the smallest quantisation" and "GPUs are always faster" are both common rules of thumb.
Capacity planning for an on-prem LLM platform needs numbers for the actual model and prompt sizes.

## Decision

- Benchmark every candidate model on the target hardware for throughput under concurrency,
  single-stream decode, prefill speed and time to first token, before sizing.
- Pick quantisation **per hardware class**: the faster format on GPU is not always the faster one
  on CPU.
- Route long-prompt (RAG) traffic to accelerators: prefill dominates there.

## Evidence

| Measured in llm-serving-bench | Metal GPU (host) | CPU container (6 vCPU) |
|---|---:|---:|
| Peak output throughput, Q4_K_M, 4 concurrent | 381 tok/s | 184 tok/s |
| Peak output throughput, Q8_0, 4 concurrent | 358 tok/s | 328 tok/s |
| Prefill, ~1k-token prompt | 2,196 prompt tok/s | 330 prompt tok/s |
| TTFT, 3.8k-token prompt, cold | 1.91 s | 13.83 s |

On CPU, Q8_0 gave 1.8× the throughput of Q4_K_M; on the GPU, Q4_K_M was slightly ahead.

## Consequences

- Benchmarks are rerun when the model, runtime version or hardware changes.
- Long-context RAG on CPU is a latency risk (13.83 s to first token at 3.8k tokens).
