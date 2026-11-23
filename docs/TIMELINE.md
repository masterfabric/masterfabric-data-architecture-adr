# Build timeline

Build history of MasterFabric Data Architecture, generated from the git log. Times are Europe/Istanbul (UTC+3).

Every step below is one commit, in order. Times are Europe/Istanbul (UTC+3).

| # | Commit | Time | Change |
|---|---|---|---|
| 1 | `a0329fe` | 2026-11-21 05:28 | chore: scaffold repository with AGPL-3.0 license and community files |
| 2 | `05502bf` | 2026-11-21 05:30 | feat(evidence): 47 measured claims from the eight labs, each with its source quote |
| 3 | `b9dbda5` | 2026-11-21 05:30 | feat(tools): claim checker against source READMEs at pinned commits |
| 4 | `ad89933` | 2026-11-21 05:30 | test: claim file integrity and the checker's failure path |
| 5 | `94ae106` | 2026-11-21 05:31 | build: pinned render and test requirements, shared image style |
| 6 | `e506f47` | 2026-11-21 05:31 | docs: evidence chart, one measured decision per panel |
| 7 | `74f2400` | 2026-11-21 05:31 | docs: reference platform diagram naming the lab behind each layer |
| 8 | `8593bba` | 2026-11-21 05:33 | feat(evidence): seven more claims used by the ADR text |
| 9 | `1cc8844` | 2026-11-21 05:33 | docs(adr): 0001 open lakehouse on Apache Iceberg with a REST catalog |
| 10 | `e1e2a23` | 2026-11-21 05:33 | docs(adr): 0002 Kafka and Spark Structured Streaming judged on event time |
| 11 | `fc146b2` | 2026-11-21 05:33 | docs(adr): 0003 ML lifecycle gated by data quality and evidence |
| 12 | `f4ed7e9` | 2026-11-21 05:33 | docs(adr): 0004 on-prem LLMs, RAG and layered guardrails on Kubernetes |
| 13 | `e911a9d` | 2026-11-21 05:33 | docs(adr): 0005 serving hardware and quantisation chosen by measurement |
| 14 | `02f5ad6` | 2026-11-21 05:33 | docs(adr): 0006 enforce governance before data reaches a model |
| 15 | `785ec99` | 2026-11-21 05:33 | docs(adr): 0007 first-principles team knowledge; LoRA for adaptation |
| 16 | `64e785f` | 2026-11-21 05:33 | docs(adr): 0008 Spark for big jobs, a single-node Rust engine for small ones |
| 17 | `12b9b04` | 2026-11-21 05:33 | docs(adr): index of the eight platform ADRs |
| 18 | `e53f2a2` | 2026-11-21 05:34 | docs: reference architecture in six Mermaid diagrams |
| 19 | `ea4921f` | 2026-11-21 05:34 | fix(docs): declare Mermaid nodes one per line; cite the 11-rule gate |
| 20 | `ec09e5e` | 2026-11-21 05:35 | docs: hero image from the platform diagram, evidence chart and verified claims |
| 21 | `73e49fd` | 2026-11-21 05:35 | build: Makefile for claim checks, tests and images |
| 22 | `b311ab3` | 2026-11-21 05:35 | docs: contributing guide |
| 23 | `faf34c5` | 2026-11-21 05:36 | docs: README tying the eight labs into one platform |

The final commit adds this file and the README; see `git log` for the full messages, which explain
the why of each step (including the fixes found by running the system).


## Addition: re-pin to the labs' new heads, cost model, C4 views, ADRs 0009-0012

After each of the eight labs gained new features, this repository was re-pinned to their new heads
(lakehouse `2382c11`, realtime `8776322`, airflow `ea335bc`, onprem `80b2a9c`, serving `0bdc279`,
secure `30bf75f`, genai `32102dd`, spark `8a6e137`). Times are Europe/Istanbul (UTC+3).

| # | Commit | Time | Change |
|---|---|---|---|
| 1 | `d4218b4` | 2026-11-21 15:02 | evidence: re-pin the eight labs to their new heads and update seven quotes |
| 2 | `c17202b` | 2026-11-21 15:02 | evidence: 27 claims for the additions to the eight labs |
| 3 | `a00a9c5` | 2026-11-21 15:04 | feat(cost): on-prem vs cloud cost model on top of the measured throughput |
| 4 | `17028f5` | 2026-11-21 15:04 | test(cost): compare the idle-capacity rate with a tolerance (0.01 / 0.2 is not exactly 0.05 in floating point) |
| 5 | `0c3bfa4` | 2026-11-21 15:05 | docs(adr): 0001-0004 re-pinned, with the evidence from each lab's addition |
| 6 | `3544098` | 2026-11-21 15:05 | docs(adr): 0005-0008 re-pinned, with the evidence from each lab's addition |
| 7 | `e5cbe0c` | 2026-11-21 15:06 | docs(adr): 0009 place workloads by measured cost per unit of work |
| 8 | `910e0f5` | 2026-11-21 15:06 | docs(adr): 0010 Flink for new low-latency streams, Spark Structured Streaming where Spark already runs |
| 9 | `5a84fb6` | 2026-11-21 15:06 | docs(adr): 0011 release models through a canary and a feature store (v5 promoted, v6 rolled back at 5 %) |
| 10 | `61aabb1` | 2026-11-21 15:06 | docs(adr): 0012 judge guardrails on held-out attacks and legitimate traffic |
| 11 | `6c03bf7` | 2026-11-21 15:06 | docs(adr): index lists ADRs 0009-0012; 0008 title no longer says Rust only |
| 12 | `8704339` | 2026-11-21 15:08 | docs(c4): system context, container and RAG component views in Mermaid |
| 13 | `fffb223` | 2026-11-21 15:08 | viz(c4): Pillow versions of the three C4 views for the README |
| 14 | `8c71622` | 2026-11-21 15:08 | viz(platform): show Flink, schema registry, WAP, DuckDB, Feast, canary, classifier guard, MLX and audit chain |
| 15 | `fd15a56` | 2026-11-21 15:10 | viz(evidence): 12 panels; small-job panel now 6 queries on 200M rows, add Flink CPU, exactly-once and held-out guard panels |
| 16 | `72b780b` | 2026-11-21 15:10 | viz(cost): LLM cost per 1M tokens against utilisation with break-even lines, and SQL cost per 1,000 runs by engine |
| 17 | `90f14e6` | 2026-11-21 15:10 | viz(hero): 12 ADRs, 82 verified numbers, 200M-row small-job figure |
| 18 | `1230b93` | 2026-11-21 15:11 | docs(architecture): Flink and schema registry, WAP, DuckDB, canary and feature store, classifier and reranker in the request path, updated Cloudera mapping |
| 19 | `1921c70` | 2026-11-21 15:11 | build: make cost target |
| 20 | `371db4d` | 2026-11-21 15:11 | evidence: extend three quotes so ADRs 0010 and 0012 cite only verified numbers |
| 21 | `c49fe5e` | 2026-11-21 15:13 | docs(readme): 12 ADRs, 82 verified numbers, C4 views, cost section with figure, champion v5 |
| 22 | `1b6b5b9` | 2026-11-21 15:13 | docs: NOTICE notes the dated price source and no new dependency; CONTRIBUTING rule for cost inputs |
| 23 | (this commit) | 2026-11-21 15:13 | docs(timeline): this section |

### Verification

| Check | Result |
|---|---|
| `make check` (GitHub raw at the pinned commits) | 82/82 claims verified |
| `make check-local` (sibling checkouts) | 82/82 claims verified |
| `make test` | 10 passed (5 claim tests, 5 cost-model tests) |
| Mermaid in README, `docs/architecture.md`, `docs/c4.md` | all 10 diagrams render with mermaid-cli |
| New dependencies | none (NOTICE updated to say so) |

### Found while running it

- **Seven quotes broke on re-pin.** The labs had rewritten their own tables (for example spark-rust-bench
  moved its headline from 50M to 200M rows and added DuckDB; secure-data-ai added a classifier
  layer to its injection rows). The checker failed on exactly those seven, which is its purpose;
  ADR 0006 and 0008 evidence was rewritten to the new numbers rather than keeping old ones.
- **A Unicode minus does not parse as a number.** airflow-mlops prints ΔAUC as "−0.0007"; the value
  check compares against the quote with `*` and backticks stripped, so the claim stores the absolute
  value (`delta_auc_abs`) instead.
- **A failing test was pushed once.** The first cost-model test compared floats exactly
  (0.01 / 0.2 is not exactly 0.05) and `pytest | tail` hid the exit code; `17028f5` fixed it with a
  tolerance. Test output is now read before committing.
- **The claims commit message says "three per lab"** but spark-rust-bench got six new claims; the
  count in the message is wrong, the file is right.
- **Not every ADR number was a claim at first.** A scan of ADRs 0010-0012 for numbers missing from
  the claim quotes found four (521,044 offsets, 0/35 and 1/14 benign blocked, 1.17 s); `371db4d`
  extended three quotes so they are verified too.
- **Prices change.** The cloud prices are list prices from instances.vantage.sh on 2026-11-21 and the
  on-prem server is an assumption; the ADR says to re-run with real quotes. Committed capacity is
  more expensive than on demand below its break-even (66 %, 45 %, 17 %), which the cost chart shows.
- `fffb223` also contains the platform-diagram code change; its image is in `8c71622`.

## Addition: second round of the labs (2026-11-23)

Every lab was pushed one step further on 2026-11-23; this repository re-pins them and cites the new
results. Times are Europe/Istanbul.

| Commit | Time | What |
|---|---|---|
| `bc8b507` | 2026-11-23 13:37 | evidence: re-pin all eight labs to their 2026-11-23 heads; 18 new claims from the second round; DataFusion and DPO claims follow the corrected READMEs (100 claims) |
| `061d200` | 2026-11-23 13:37 | charts: second-round evidence (figure 6), hero with 100 verified numbers |
| `af29088` | 2026-11-23 13:37 | docs(adr): Update 2026-11-23 sections for 0001, 0002, 0003, 0005, 0007, 0008, 0012; DPO comparison corrected, DataFusion note withdrawn; evidence pins |
| `5085333` | 2026-11-23 13:37 | docs(readme): second round table and figure, 100/100 verified, corrected DPO and DataFusion rows, cost inputs still assumptions |
| (this commit) | 2026-11-23 | docs(timeline): second round |

### Verification

| Check | Result |
|---|---|
| Pins | lakehouse `6ba927f`, realtime `456e642`, airflow `3546e6f`, onprem `bd383f7`, serving `83af7fe`, secure `df8125e`, genai `9e3b863`, spark `361bb4a` |
| `make check` (GitHub at pinned commits) | 100/100 claims verified |
| `make check-local` | 100/100 claims verified |
| `make test` | 10 passed |
| `make cost` | unchanged: no cost input changed (PySpark/Polars runtime 3.69, Spark/Flink CPU 6.92) |

### Found while running it

- Re-pinning broke 5 claims, all in spark-rust-bench: its tables now have DataFusion values at 200M
  rows instead of "killed", and 240 instead of 234 matching results. The quotes were updated, not the
  check.
- genai-foundations corrected its own DPO table during this round (dropout was on in the reference
  model). The old quote still matched at the previous pin, which is the checker's known limit: it
  proves where a number comes from, not that it is right. ADR 0007 now says best-of-4 is ahead.
- On-prem costs are still assumptions; no real quote was obtained this round.

## Addition: data-subject request deadlines (2026-11-23)

Times are Europe/Istanbul. secure-data-ai added a GDPR / CCPA / KVKK request workflow with a deadline engine
(its commits `e7fe5c3` to `fe90c23`); this repository records the design decision and pins the evidence.

| Change | Detail |
|---|---|
| ADR 0013 | Track request deadlines with one rule table and pure date functions; calendar-month clamping for GDPR; not legal advice |
| ADR 0006 | "Update 2026-11-23" section pointing to ADR 0013 |
| Evidence | secure-data-ai re-pinned `df8125e` → `fe90c23`; 3 new claims (`sd_dsr`, `sd_dsr_latency`, `sd_dsr_deadlines`), 103 in all |

### Verification

| Check | Result |
|---|---|
| `make check` (GitHub at pinned commits) | 103/103 claims verified |
| `make check-local` | 103/103 claims verified |
| `make test` | 10 passed |

The hero image and the evidence figure still show the earlier counts (twelve ADRs, 100 numbers); they were not
regenerated in this step.
