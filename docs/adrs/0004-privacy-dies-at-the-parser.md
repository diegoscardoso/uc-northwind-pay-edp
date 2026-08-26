# 0004. Privacy transforms happen inside the parser — nothing downstream sees a raw PAN or CPF

**Status:** Accepted — Pass 2 Structure, human-led, 2026-08-25
**Deciders:** Priya Shah (privacy)

## Context

The NorthWind Pay privacy policy (`spec/estate/policies/privacy.md`,
2026-06-16, "applies to every type in this drop") states that PAN,
CPF, CNPJ, account numbers, and holder names "must not exist after
sanitize" in any CSV, Parquet, log, evidence packet, ticket, or
warehouse table, unless a type policy names an approved transform
(token, last4, mask); that a missing tokenization key must fail
closed; and that a leak "stalls the type. There is no 'just this
demo.'"

Type 01's contract makes this concrete
(`contracts/types/01-card-settlement/privacy.yaml`,
`layout.yaml` detail record):

- `pan` — `privacy: tokenize`, algorithm `HMAC-SHA-256`, keyed by
  `NWP_TOKENIZATION_KEY`, output `tok_<first-24-lowercase-hex-characters>`,
  `missing_key_behavior: fail_closed`.
- `cpf` — `privacy: mask`, algorithm `retain_last4`, output
  `*******<last4>`.
- Both fields carry the same `prohibited_outputs` list: `sanitized_csv`,
  `application_logs`, `error_messages`, `batch_evidence`,
  `database_staging`, `database_operational`.
- `handling.evidence.store_raw_content: false`;
  `handling.failure_messages.include_field_value_for_pan_or_cpf: false`.

This is written against the legacy Java line, but the obligation is
type-level, not implementation-level — it applies equally to the
modern plant's own parser.

## Decision

For the modern plant, PAN tokenization and CPF masking happen inside
the **parser** file of the five-file package (ADR 0002) — the same
step that turns raw fixed-width bytes into the typed model. Past that
point, no code path in `schema`, `writer`, or `handler` may hold, log,
or emit a raw PAN or raw CPF digit sequence, in memory, in an error
message, in evidence, or in the eventual Parquet row. A missing
`NWP_TOKENIZATION_KEY` fails the batch closed — it does not fall back
to skipping tokenization or emitting the field unmasked.

## Consequences

- `schema`, `writer`, and `handler` can assume every value they
  receive is already sanitized; none of them is ever given a code path
  that sees the raw record.
- Debugging output and evidence capture anywhere downstream of `parser`
  must treat raw PAN/CPF as absent by construction, not as something to
  remember to redact.
- A leak found in `writer` or later is a `parser`-boundary defect, not
  a missing filter to bolt on downstream.
