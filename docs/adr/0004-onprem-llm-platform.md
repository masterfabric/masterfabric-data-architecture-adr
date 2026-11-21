# ADR 0004: Generative AI on-prem: open-weight models, RAG and layered guardrails on Kubernetes

- Status: accepted
- Date: 2026-11-21
- Evidence: [masterfabric-onprem-llm-stack](https://github.com/masterfabric/masterfabric-onprem-llm-stack) (pinned at `d55ea0f`)

## Context

Customer and network data cannot leave the operator, so hosted LLM APIs are out for many use
cases. The platform needs OpenAI-compatible endpoints that teams can build on, answers grounded
in internal documents, and protection against prompt attacks.

## Decision

- Serve open-weight chat and embedding models behind **OpenAI-compatible APIs**, packaged as one
  **Helm chart** with NetworkPolicies. llama.cpp in the CPU-only lab; vLLM on GPU nodes in the chart.
- **pgvector** (HNSW) as the vector store, so retrieval sits in an engine the DBAs already run.
- **Guardrails at three points**: input, retrieved context, output. Refuse when the context does
  not contain the answer.

## Evidence

| Measured in onprem-llm-stack | Value |
|---|---|
| Corpus | 23 documents → 207 chunks |
| Retrieval | hit@4 0.933 |
| Answers | accuracy 0.767; 5/5 unanswerable questions refused |
| Guardrails | 22/26 attacks handled; 0/4 paraphrase evasions caught |
| LLM load, CPU | 160 tok/s at 4 users |
| RAG load | best 3.97 req/s at 2 users |

## Consequences

- Deterministic guardrails miss paraphrased attacks (0/4); a model-based classifier is the next
  layer, and red-team tests stay in CI.
- The CPU numbers are a floor; GPU serving choices are measured separately (ADR 0005).
- Maps to Cloudera AI Inference / CML on GPU nodes, or any Kubernetes with GPU operators.
