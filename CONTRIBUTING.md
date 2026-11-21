# Contributing

This repository holds decisions, not code that runs a platform. Changes are welcome when every
number stays traceable to a lab that measured it.

## Ground rules

- **No unsourced numbers.** A figure in an ADR, the README or an image must be a claim in
  `evidence/claims.json`, quoted verbatim from the source lab's README at a pinned commit.
  `make check` must pass.
- **Re-pin deliberately.** When a lab's results change, update its commit in `claims.json`, fix the
  quotes, re-run `make check charts`, and say in the commit body what changed.
- **Decisions keep their trade-offs.** An ADR states the consequences and the weak spots its
  evidence shows (for example paraphrased prompt injection), not only the wins.
- **Diagrams as code.** Mermaid in Markdown, images rendered by `viz/` scripts; never edit a PNG by hand.
- One logical change per commit, Conventional Commit subject, and a body that explains why.

## License of contributions

By contributing you agree that your contribution is licensed under the AGPL-3.0, as described in
[LICENSE](LICENSE) and [NOTICE](NOTICE).
