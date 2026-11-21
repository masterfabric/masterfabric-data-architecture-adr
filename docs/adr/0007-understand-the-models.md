# ADR 0007: Build team understanding from first principles; adapt models with LoRA

- Status: accepted
- Date: 2026-11-21
- Evidence: [masterfabric-genai-foundations](https://github.com/masterfabric/masterfabric-genai-foundations) (pinned at `bfc85b3`)

## Context

A platform team that only calls APIs cannot judge model claims, debug training, or choose between
fine-tuning methods. Full fine-tuning of every model per use case is also expensive to store and
risks forgetting.

## Decision

- Keep a small from-scratch reference (attention, GPT, LoRA, GAN, RL in PyTorch), tested against
  library implementations, as the team's shared understanding.
- Default to **LoRA** for domain adaptation; use full fine-tuning only when LoRA measurably falls short.

## Evidence

| Measured in genai-foundations | Value |
|---|---|
| Attention vs PyTorch SDPA | matches within 1.5e-7 |
| GPT, 0.82M parameters | validation loss 4.72 → 1.516 nats/char |
| LoRA r=8 vs full fine-tuning, new corpus | 1.758 vs 1.725 |
| LoRA r=8 vs full fine-tuning, original corpus (forgetting) | 1.642 vs 1.747 |

LoRA came within 0.033 nats of full fine-tuning on the new data and forgot less of the original.

## Consequences

- Adapters are small and can be swapped per use case on one served base model (ADR 0004).
- Laptop-scale results show the mechanics, not production model quality.
