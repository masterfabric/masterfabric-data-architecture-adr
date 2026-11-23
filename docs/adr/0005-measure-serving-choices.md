# ADR 0005: Choose serving hardware and quantisation by measurement, per workload

- Status: accepted
- Date: 2026-11-21
- Evidence: [masterfabric-llm-serving-bench](https://github.com/masterfabric/masterfabric-llm-serving-bench) (pinned at `83af7fe`)

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

## Update 2026-11-21: MLX, KV cache, long context, speculative decoding (llm-serving-bench `0bdc279`)

- **Engine:** on the same GPU, MLX 4-bit decoded 210 vs 171 tok/s for llama.cpp Q4_K_M, but its
  perplexity rose 17.5% over 8-bit against 4.5% for Q4_K_M. Choose by quality and speed together.
- **KV cache:** a q8_0 KV cache halved the KV buffer at 32k context (896 → 476 MiB) at the same
  speed; use it for long contexts.
- **Speculative decoding** with a 0.5B draft paid off only for a 7B target on predictable text (1.60x
  llama.cpp, 1.73x MLX on code/SQL/YAML) and slowed open text; enable it per workload, not globally.
- The cost of these choices per token is in ADR 0009.

## Update 2026-11-23: speculative mismatches and a second machine (llm-serving-bench `83af7fe`)

- Where speculative decoding changed the output, the target's own top two tokens were nearly tied
  (0.002-0.034 nats apart at 7B). Speculative output is not guaranteed token-identical in practice;
  test it against target-only output on near-ties, not on exact match.
- The same harness on a MacBook Air M5 decoded at 107 tok/s against 164 on the M4 Pro (0.65x) for
  one request with llama.cpp Q4_K_M. Capacity figures are per machine and are re-measured, not scaled.
