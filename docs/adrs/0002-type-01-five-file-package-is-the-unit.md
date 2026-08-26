# 0002. Type 01's build unit is a five-file package: model, parser, schema, writer, handler

**Status:** Accepted — Pass 2 Structure, human-led, 2026-08-25
**Deciders:** Helena Dias

## Context

The 2026-06-09 file-decomposition sync recorded, as decision D1
(approved): "One handler per type, five files: model, parser, schema,
writer, handler" (`spec/estate/meetings/2026-06-09-file-decomposition.md`).

Grounding that shape against the real Type 01 grammar
(`contracts/types/01-card-settlement/layout.yaml`) shows it is not a
trivial split: Type 01 is a fixed-width, ISO-8859-1, LF-terminated
`.dat` with three record kinds (`header` 40 bytes, `detail` 124 bytes,
`trailer` 46 bytes), COBOL signed-overpunch amounts, cross-record
invariants (detail-count and net-amount agreement, movement-sign
rules, duplicate-`transaction_id` rejection), and a privacy transform
on two fields (`pan`, `cpf`). That is enough surface area to justify a
durable file boundary rather than one script.

## Decision

For Type 01 — and, by the same approved shape, for each of types
02–05 later — the unit of build is exactly five files, one package per
type:

- **model** — typed shapes for header, detail, trailer records.
- **parser** — turns raw fixed-width bytes into the model: grammar,
  encoding, overpunch decode, record-sequence enforcement. Owns the
  privacy transform (see ADR 0004).
- **schema** — validates a parsed batch against the contract: field
  formats, cross-record rules, the type's canonical rejection codes.
- **writer** — emits the sanitized, schema-valid batch to
  `modern/landing/` Parquet (see ADR 0001).
- **handler** — orchestrates: acquire → parse → validate → sanitize →
  write → record the outcome (accepted / refused / kept source lie).

No sixth file. No merging two of these into one. Type 01 is tonight's
steel thread; the same five-file shape is the unit named for types
02–05 when their nights come, not a Type-01-only convention.

## Consequences

- Decompose (Pass 3) cuts *within* this shape — e.g. one swimlane per
  responsibility, or one per type — not around it.
- A stack or engine choice for any of these five files is out of scope
  for this ADR and for tonight.
- Reviewers checking "did this package do the whole job" have five
  named places to look, not one undifferentiated module.
