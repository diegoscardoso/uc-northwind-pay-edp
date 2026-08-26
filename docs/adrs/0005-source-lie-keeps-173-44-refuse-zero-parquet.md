# 0005. On a source control-total mismatch, keep the declared number, refuse the batch, write zero Parquet rows

**Status:** Accepted — Pass 2 Structure, human-led, 2026-08-25
**Deciders:** Marina Alves (settlement ops)

## Context

Batch `B202607230000004` (`DF-SOURCE-001`) is Type 01's source-owned
lie: the trailer declares net `173.44`
(`contracts/types/01-card-settlement/main/expected-df-source-001-finding.yaml`,
`declared_net_amount: "173.44"`), while the details independently sum
to `173.45` (`computed_net_amount: "173.45"`) — exactly the invariant
`layout.yaml` requires ("Trailer `net_amount_brl` must equal the exact
sum of detail `amount_brl`") and exactly the check ADR 0003's exact
decimal makes trustworthy.

Marina Alves, 2026-07-14: "I am not sending another 'corrected' file.
... If your new plant quietly writes 173.45 into the trailer we will
have nothing to show the source. Keep their number. Refuse the batch.
That is the whole point."
(`spec/estate/mail/2026-07-14-the-cent-that-will-not-die.md`).

The expected finding record for this batch is unambiguous about the
legacy side's behavior: `expected_status: quarantined`,
`expected_code: SOURCE_CONTROL_TOTAL_MISMATCH`, `csv_produced: false`,
`postgres_business_mutation: false`, `quarantine_scope: batch`,
`unrelated_batches_continue: true`. The 2026-06-09 sync's D3 (approved):
"Quarantine is batch-scoped."

## Decision

When the modern plant's independently computed net amount does not
equal the source's declared trailer net amount, the plant:

1. **Never overwrites the declared value** anywhere it is recorded —
   `173.44` stays `173.44` in every manifest, finding, and log for
   this batch.
2. Records the independently computed value (`173.45`) as a separate,
   distinctly named field — never merged into, or silently replacing,
   the declared field.
3. Quarantines the batch under a stable code equivalent to
   `SOURCE_CONTROL_TOTAL_MISMATCH`.
4. Writes **zero rows** to `modern/landing/` Parquet for this batch —
   the Parquet-side equivalent of `csv_produced: false`.
5. Leaves every unrelated batch unaffected — quarantine scope is this
   one batch, per D3.

This decision generalizes: the same declared-vs-computed mismatch
shape exists on all five live types (`docs/brd-type-01-card-settlement.md`
§4), so "keep the declared number, refuse, zero output rows" is the
modern plant's rule for a control-total mismatch on any of them, not a
Type-01-only carve-out.

## Consequences

- Any finding/quarantine record format the modern plant defines must
  carry both a `declared_*` and a `computed_*` field, distinctly
  named, so this rule is mechanically checkable rather than a matter
  of trust.
- An implementation that ships "zero Parquet rows" as "one row with an
  adjusted total" is a violation of this ADR, not a bug to patch
  quietly — the same prohibition the BRD and tech-spec already carry
  forward as "do not fix 173.44."
- Downstream consumers of `modern/landing/` must be able to tell "this
  batch produced zero rows because it was refused" apart from "this
  batch simply had zero details" — that distinction is left for
  Decompose/schema design, not settled here.
