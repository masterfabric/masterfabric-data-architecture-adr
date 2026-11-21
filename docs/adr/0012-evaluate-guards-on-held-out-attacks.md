# ADR 0012: Judge LLM guardrails on held-out attacks and on legitimate traffic

- Status: accepted
- Date: 2026-11-21
- Evidence: [masterfabric-onprem-llm-stack](https://github.com/masterfabric/masterfabric-onprem-llm-stack) (`80b2a9c`),
  [masterfabric-secure-data-ai](https://github.com/masterfabric/masterfabric-secure-data-ai) (`30bf75f`)

## Context

Two labs built layered prompt-injection defences independently (rules, then an LLM classifier) and
both kept a set of attacks that was written before the defence was tuned. Their results on the
development set and on the held-out set differ sharply.

## Evidence

| | Development set | Held-out set | Legitimate questions blocked |
|---|---|---|---|
| onprem-llm-stack, rules | 22/26 handled, 0/4 paraphrases caught | 0/16 stopped | 0 |
| onprem-llm-stack, rules + classifier | 24/26 handled, 4/4 paraphrases caught | 10/16 stopped | 2/4 PII questions; 0/35 benign; 1/14 hard benign |
| secure-data-ai, rules | injection 4/10 succeed | 7/12 succeed | 0/22 |
| secure-data-ai, rules + classifier | 0/10 succeed | 1/12 succeed | 3/22 |

## Decision

- Every guard is reported on **three numbers**: development attacks, **held-out attacks written
  before tuning**, and legitimate questions blocked. A guard is not accepted on the first alone.
- Thresholds are fixed on the development set and never re-tuned on the held-out set; a new held-out
  set is written before each re-tune.
- Guards are a layer, not the control: entitlement filtering at retrieval (ADR 0006) and output PII
  guards stay in place because some attacks get through every classifier measured here.

## Consequences

- Red-team work becomes a recurring task (new held-out sets), not a one-time test.
- Classifiers add latency (p50 1.17 s on 2 CPU threads in onprem-llm-stack, 71 ms in
  secure-data-ai) and false positives that users notice; both are reported with the block rate.
