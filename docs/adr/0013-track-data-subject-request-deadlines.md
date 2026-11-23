# ADR 0013: Track data-subject request deadlines with one rule table and pure date functions

- Status: accepted
- Date: 2026-11-23
- Evidence: [masterfabric-secure-data-ai](https://github.com/masterfabric/masterfabric-secure-data-ai) (`fe90c23`):
  [README section 8](https://github.com/masterfabric/masterfabric-secure-data-ai#8-data-subject-requests-gdpr-ccpa-kvkk),
  [lab ADR 0008](https://github.com/masterfabric/masterfabric-secure-data-ai/blob/main/docs/adr/0008-dsr-deadline-tracking.md),
  [comparison of the three laws](https://github.com/masterfabric/masterfabric-secure-data-ai/blob/main/docs/dsr-gdpr-ccpa-kvkk.md)
- Extends: [ADR 0006](0006-govern-data-before-ai.md) (erasure becomes one request type of a tracked workflow)

> **This is not legal advice.** The periods below are one simplified engineering reading of well-established
> general provisions; see the comparison linked above and consult qualified counsel.

## Context

The platform serves people covered by GDPR, CCPA/CPRA and KVKK. Each gives them the right to ask for their
data, its erasure, or an end to marketing use (under CCPA, an opt-out of sale or sharing), and each sets its own
response clock: generally one calendar month, extendable by two further months with notice (GDPR Art. 12(3));
45 days, extendable once by 45 with notice, and no later than 15 business days for an opt-out (Cal. Civ. Code
1798.130(a)(2), CCR tit. 11 s. 7026(f)); 30 days with no extension in the Law (KVKK Art. 13(2)). ADR 0006 made
erasure complete across every store; it did not say by when a reply is due or which requests are late.

## Decision

- **One rule table per law and request type** (unit, base period, extension, citation, modelling note). A new
  law or a different legal reading is a row change, reviewed with counsel, not a code change across services.
- **Pure date functions with an explicit `today`.** Due date, extension-notice deadline, days remaining and
  status are functions of dates; nothing reads the clock, so every case can be replayed and tested.
- **Calendar months for GDPR, clamped to the month's last day** (31 Jan + 1 month = 28 or 29 Feb), not a flat
  30 days. Day 0 is the receipt day; weekends, holidays and Regulation 1182/71 are not modelled yet.
- **Status `ok` / `due_soon` / `overdue`**, with a 7-day warning window (a default, not a legal concept), and a
  tracker that lists open requests earliest due date first.
- **Every transition is audited** in the hash-chained log of ADR 0006 with the subject as a keyed pseudonym; a
  request is `completed` only when its post-checks pass, otherwise it stays open and visible.
- **Identity**: two matching factors, except a CCPA opt-out, which on one reading of s. 7026(d) needs only enough
  to identify the record.

Rejected: a flat 30 days for GDPR (wrong on 481 of 731 receipt dates, see below), a date library dependency for
one clamping function, and a workflow engine or cron job as the source of truth for deadlines (a scheduler can
call the tracker, but the rule stays a pure function).

## Evidence

| Measured in secure-data-ai (Apple M4 Pro, `make dsr`) | Value |
|---|---|
| Requests, 3 laws × 3 types × 60, over 200,000 customers | 540/540 completed on time |
| Latency per request, p50 / p95 | access 2.1 / 2.7 ms; consent withdrawal 1.5 / 2.1 ms; erasure 117 / 141 ms |
| Residual rows after 180 erasures | 0 outside 360 retained invoice rows |
| Deadline sweep, 731 receipt dates (2027-2028) | GDPR month lands 28-31 days out |
| Audit log | 0 raw identifiers in 2,340 audit entries, chain verified |
| Unit tests | 98, including month-end and leap-year deadlines |

The 481 figure comes from the same sweep: 29 receipt dates land at 28 days, 31 at 29 and 421 at 31; only 250
are exactly 30. The lab's identity-check result (820 attempts, 0 false accepts or rejects) uses attempts written
to the rules, so it confirms the rules are applied, not that two factors stop a real impostor.

## Consequences

- Deadlines are visible and testable in one place; a change of reading shows up as a diff in one table plus the
  tests that move.
- A due date on a weekend is shown as is, so the tracker can say `overdue` a day before a reading that rolls to
  Monday would. A holiday calendar and weekend rolling are the next step, per jurisdiction.
- The lab tracker is in memory; production needs persisted requests, reminders and the same rule table behind
  the DSR tooling (for example OneTrust or BigID) rather than a second copy of the rules.
- Rectification, restriction, portability and the CCPA right to limit sensitive data are not yet request types.
