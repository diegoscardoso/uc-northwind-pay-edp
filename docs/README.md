# Docs — Converge paper trail

This folder is where Converge **writes**. It is not inbound (`spec/`),
not the judge (`contracts/`), and not the method manuals
([`presentation/`](../presentation/README.md)).

Staff: Day 1 Capture → Intent writes the first two files. Day 2 Structure
→ Consensus → Tasking writes the rest **here**. Landing Parquet is product
(`modern/`) **after** the sign — not required Tuesday. Clock: [`run/d2/`](../run/d2/README.md).

```text
docs/
  README.md                              this map
  brd-type-01-card-settlement.md         Pass 0 Capture     Day 1 · exists
  tech-spec-type-01-card-settlement.md    Pass 1 Intent      Day 1 · exists
  CONTEXT.md                             glossary           Day 2 Pass 2
  adrs/NNNN-*.md                         Structure          Day 2 Pass 2
  seams.md                               Decompose          Day 2 Pass 3
  consensus.md                           the sign           Day 2 Pass 4
  tasks/                                 Task-Specs         Day 2 Pass 5
  no-go-*.md                             cheap kill         Pass 0 only if needed
```

This repo’s Converge home is **`docs/`**, not `cvg/docs/`. If `cvg`
emits under `cvg/docs/`, put the artifact in the path above.

Do not pre-seed ADRs. Do not copy last run’s papers out of git history.
Do not upload these files into NotebookLM.

## Pass → file

| Pass | Name | File | Night |
|---|---|---|---|
| 0 | Capture | [`brd-type-01-card-settlement.md`](brd-type-01-card-settlement.md) | Day 1 wrote it. Day 2 **looks** ([`run/d2/02-prompt-papers.md`](../run/d2/02-prompt-papers.md)) |
| 1 | Intent | [`tech-spec-type-01-card-settlement.md`](tech-spec-type-01-card-settlement.md) | Day 1 wrote it. Day 2 **looks** ([`run/d2/02-prompt-papers.md`](../run/d2/02-prompt-papers.md)) |
| 2 | Structure | `adrs/` + `CONTEXT.md` | Day 2 writes ([`run/d2/08-structure.md`](../run/d2/08-structure.md)) |
| 3 | Decompose | `seams.md` | Day 2 writes ([`run/d2/09-decompose.md`](../run/d2/09-decompose.md)) |
| 4 | Consensus | `consensus.md` | Day 2 **signs** ([`run/d2/10-consensus.md`](../run/d2/10-consensus.md)). No sign → no parser |
| 5 | Tasking | `tasks/` | Day 2 writes one leaf, one eval ([`run/d2/11-taskspec.md`](../run/d2/11-taskspec.md)) |
| 6 | Register | opt-in | Not required tonight |
| 7 | Bind | harness, not a doc | [`run/d2/03-prompt-harness.md`](../run/d2/03-prompt-harness.md)–[`04-fail-closed.md`](../run/d2/04-fail-closed.md) |
| 8 | Loop | `modern/landing/` | Product, not this folder. Factory is Day 4 |

## Method manuals (not this folder)

The spine, the loop, and the boot live next to the decks:

| Manual | What it is |
|---|---|
| [`presentation/cvg-aut-systems-spine-steps.html`](../presentation/cvg-aut-systems-spine-steps.html) | Converge spine — nine passes, one human barrier |
| [`presentation/asd-agentic-loop.html`](../presentation/asd-agentic-loop.html) | ASD — the Agentic Loop |
| [`presentation/boot-uc-northwind-pay-edp-oss.html`](../presentation/boot-uc-northwind-pay-edp-oss.html) | Bootcamp reference |
| [`presentation/seamwise.html`](../presentation/seamwise.html) | Seamwise kit — Night 2 Leave · Seamwise |

Plans steer the plant: [`plans/`](../plans/README.md). This folder is
the week’s signed papers.

## What this folder is not

- Not contracts, fixtures, or expected outputs.
- Not a second copy of `plans/legacy.md` or `plans/modern.md`.
- Not the HTML manuals (those moved to `presentation/`).
- Not `modern/`. First write after the sign is landing Parquet.
