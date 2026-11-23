# ADR 0004: Generative AI on-prem: open-weight models, RAG and layered guardrails on Kubernetes

- Status: accepted
- Date: 2026-11-21
- Evidence: [masterfabric-onprem-llm-stack](https://github.com/masterfabric/masterfabric-onprem-llm-stack) (pinned at `bd383f7`)

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

## Update 2026-11-21: classifier guard, held-out attacks, reranker, monitoring (onprem-llm-stack `80b2a9c`)

- A second guard layer (Granite Guardian 3.2 classifier on its own llama.cpp server) raised the
  development result to 24/26 and caught all 4 paraphrase evasions, but blocked 2 of 4 PII questions.
- On attacks written before the classifier existed, rules alone stopped 0/16 and rules plus
  classifier 10/16. ADR 0012 makes held-out evaluation the rule for every guard.
- A cross-encoder reranker improved hit@1 from 0.833 to 0.933 but added 3.8 s p50 on CPU and did not
  change answer accuracy, so it runs on request only.
- Prometheus and Grafana now scrape the API and the four model servers.
