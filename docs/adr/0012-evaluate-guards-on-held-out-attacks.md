# ADR 0012: Judge LLM guardrails on held-out attacks and on legitimate traffic

- Status: accepted
- Date: 2026-11-21
- Evidence: [masterfabric-onprem-llm-stack](https://github.com/masterfabric/masterfabric-onprem-llm-stack) (`bd383f7`),
  [masterfabric-secure-data-ai](https://github.com/masterfabric/masterfabric-secure-data-ai) (`df8125e`)

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

## Update 2026-11-23: a re-tuned guard and clarify instead of block (onprem-llm-stack `bd383f7`, secure-data-ai `df8125e`)

- A new held-out set was written before re-tuning, as this ADR requires. Guard v1.2 (a narrower
  override at a lower threshold): attacks caught 18/24 → 22/24, benign blocked 2/20 → 4/20. It stays
  optional; v1.1 remains the default because the trade-off is a policy choice.
- Clarify instead of block: a flagged question is rewritten, re-checked and answered only after the
  user confirms the rewrite. On a fresh set, legitimate questions blocked fell from 3/12 to 0/12;
  attacks that succeed stayed 3/12, and the clarified path costs p50 753 ms against 368 ms.
- Decision added: report the three numbers for the clarify path too; clarification does not replace
  better detection, because attacks scored below the threshold never reach it.
