# ADR 0006: Enforce data governance before data reaches a model

- Status: accepted
- Date: 2026-11-21
- Evidence: [masterfabric-secure-data-ai](https://github.com/masterfabric/masterfabric-secure-data-ai) (pinned at `b0b1740`)

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
| Direct prompt injection (LLM01) | 7/10 → 4/10 |
| Benign questions blocked | 0/10 |

## Consequences

- Prompt injection is reduced, not solved (4/10 still succeed); retrieval filtering is the control
  that does not depend on the model behaving.
- Maps to Ranger policies and Atlas classifications in CDP, applied again in the RAG layer.
