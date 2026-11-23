# ADR 0006: Enforce data governance before data reaches a model

- Status: accepted
- Date: 2026-11-21
- Evidence: [masterfabric-secure-data-ai](https://github.com/masterfabric/masterfabric-secure-data-ai) (pinned at `df8125e`)

## Context

Under KVKK and GDPR, an LLM that can read a document can leak it. Access rules written for SQL
users do not apply by themselves to a RAG pipeline or a chatbot.

## Decision

- Detect and mask PII in free text with **format plus checksum validation** (TCKN check digits, IBAN mod-97, Luhn for cards), not
  patterns alone.
- Enforce **column and row policies per role** in the query layer, and audit every attempt.
- Apply the **same entitlements at retrieval time**: a user's RAG context contains only chunks they
  may read, with PII masked.
- Add **output guards** for PII disclosure and system-prompt leaks, and measure them against the
  OWASP Top 10 for LLM applications.

## Evidence

| Measured in secure-data-ai | Value |
|---|---|
| PII detection, 2,000 notes with decoys | precision 0.986, recall 1.0 (pattern only: 0.680) |
| Policy bypass attempts | 0 of 50 allowed |
| Unauthorised chunks in RAG context | 99.6% → 0; PII entities 4,476 → 0 |
| PII disclosure attacks (LLM02) | 6/8 → 0/8 |
| Direct prompt injection (LLM01), development set | 7/10 → 4/10 (rules) → 0/10 (rules + classifier) |
| Direct prompt injection, held-out set | 7/12 → 1/12 (rules + classifier) |
| Legitimate questions blocked | 0/22 with rules; 3/22 with the classifier |

## Consequences

- Prompt injection is reduced, not solved (1/12 held-out attacks still succeed, and the classifier
  blocks 3/22 legitimate questions); retrieval filtering is the control that does not depend on
  the model behaving.
- Maps to Ranger policies and Atlas classifications in CDP, applied again in the RAG layer.

## Update 2026-11-21: second injection layer, audit chain, KVKK erasure (secure-data-ai `30bf75f`)

- A classifier behind the rules took direct injection on the development set from 4/10 to 0/10, but
  on a **held-out set** it still let 1/12 through, and it blocked 3/22 legitimate questions (rules
  alone: 0/22). Injection is reduced, not solved; see ADR 0012.
- The audit log is **hash-chained**: 2,404 entries in a simulated day, chain verified, 3/3 tamper
  drills detected, 26 µs per append.
- **KVKK erasure** for 50 subjects left 0 residual rows outside the 100 invoice rows kept for legal
  retention, p50 108 ms per erasure request.

## Update 2026-11-23: data-subject requests with tracked deadlines (secure-data-ai `fe90c23`)

- Erasure is now one of three request types (access, erasure, consent withdrawal / CCPA opt-out) in a workflow
  with per-law response deadlines for GDPR, CCPA/CPRA and KVKK. 540/540 requests completed on time over 200,000
  customers; erasure p50 117 ms with 0 residual rows outside 360 retained invoice rows.
- The deadline design is recorded in [ADR 0013](0013-track-data-subject-request-deadlines.md). Not legal advice.
