# 0003. Money is exact decimal, end to end — never binary float

**Status:** Accepted — Pass 2 Structure, human-led, 2026-08-25
**Deciders:** Rafael Costa

## Context

The 2026-06-09 sync recorded, as decision D2 (approved): "Exact
Decimal. No float money."
(`spec/estate/meetings/2026-06-09-file-decomposition.md`).

The ops policy `spec/estate/policies/rounding-and-controls.md` sharpens
this into a rule with no exceptions on this type: "Money is exact
decimal. Two fractional digits unless a layout says otherwise. **Do
not** use binary float. **Do not** use a language default rounding
unless the type says so. ... Source-owned trailers and manifests are
declarations. Independently recompute. A one-cent miss is quarantine.
**Tolerances are zero.**"

Grounding against the real contract confirms why: every money field in
`contracts/types/01-card-settlement/layout.yaml` — `detail.amount_brl`
and `trailer.net_amount_brl` — is typed `signed_overpunch, scale: 2`,
a base-10, fixed-scale COBOL encoding. It was never a float on the
source side; representing it as one downstream would introduce error
the source never had. The type's own cross-record rule — "Trailer
`net_amount_brl` must equal the exact sum of detail `amount_brl`" — is
an exact-equality check, and `df-source-001` exists specifically to
prove a one-cent miss on that check is caught (ADR 0005).

## Decision

From decode through model, schema validation, writer, and any
recomputation used to judge a source's declared total, Type 01's
amounts are carried as an exact decimal type at scale 2 (e.g. Python
`Decimal`, Arrow `decimal128`) — never `float`/`double`, and never a
language's default rounding mode. The overpunch-decode step
(`parser`) is the single place raw bytes become this decimal type; no
later stage may re-derive it from a float intermediate.

Comparisons that decide accept/refuse — trailer vs. summed details,
this batch vs. the oracle — are exact-decimal equality. Tolerances are
zero: a one-cent difference is a defect, not noise to absorb. If a
later type's layout specifies its own rounding mode (e.g. Type 05's
`HALF_UP` at the cent), that type's contract governs its own rounding
— this ADR does not impose one rounding rule across all five types,
only that none of them may use float or a silent default.

## Consequences

- Rules out `float`/`double` anywhere in the money path, including the
  stored Parquet column type in `modern/landing/`.
- Rules out "close enough" comparisons — any tolerance-based accept
  logic is a violation of this ADR, not a tuning knob.
- Keeps rounding-mode decisions local to each type's own layout/policy
  rather than centralizing a single global rounding rule that could
  silently override a type-specific one.
