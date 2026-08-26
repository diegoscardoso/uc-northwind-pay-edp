# Seams — Type 01 ingest → landing

**Pass:** Converge Pass 3 Decompose — plan-altitude only. No tasks, no code, no SQL.
**Steel thread:** Type 01 card settlement, ingest → landing. Running `valid-minimal`
end to end (one landing row) and `df-source-001` end to end (zero landing rows, lie
kept) across all four swimlanes below **is** the steel-thread proof — it is not a
fifth lane.
**Reads:** `docs/tech-spec-type-01-card-settlement.md`, `docs/adrs/0001`–`0005`,
`docs/CONTEXT.md`.
**Grounds:** `contracts/types/01-card-settlement/{layout,privacy,reconciliation}.yaml`
(read-only — frozen, not written here).

Four genuine seams, one per stage of the five-file package's data flow
(ADR 0002's `model`/`parser`/`schema`/`writer` map onto Parse, Judge, and
Landing below; `handler`'s "acquire" step is Ingest). No more, no fewer —
the right number of lanes is the number of joints the contract already has.

---

## Build order and dependencies

```
Ingest → Parse & Sanitize → Judge → Landing
```

Strictly sequential for one batch — each lane's output is the next lane's
only input. No lane may skip forward (e.g. Landing may not read raw bytes)
or reach backward (e.g. Judge may not re-parse).

---

## Swimlane 1 — Ingest

**Owns:** claiming the same raw Type 01 bytes the legacy line reads,
independent of Java. Mirrors what `legacy/intake/` does for the legacy
plant, reimplemented, not imported.

**Interface out:** verified raw bytes + `batch_id`, claimed exactly once —
or a stable transport/manifest rejection. Parse does not need to know how
hashing or claiming works inside this lane (deep-lane test).

| Leg | Responsibility | Proving test |
|---|---|---|
| 1.1 Read & hash | Read the raw `.dat`, verify its SHA-256 sidecar before anything downstream sees the bytes | `valid-minimal`'s sidecar verifies; a tampered or missing sidecar is refused, not silently parsed |
| 1.2 Claim once | A batch cannot be claimed/processed twice | Replaying the same `batch_id` a second time is rejected or no-ops — it never produces a second landing write |

**Non-goals:** grammar decoding, privacy transforms, any accept/refuse
verdict on content — Ingest only says "these are the verified bytes for
this batch," or refuses to hand anything on.

**Handoff owner (Ingest → Parse):** **Rafael Costa** — he owns what "the
same raw bytes" means on this tree; he signs off that Ingest's contract
matches the legacy line's own manifest/checksum handling.

---

## Swimlane 2 — Parse & Sanitize

**Owns:** decoding Type 01's fixed-width/overpunch grammar into the typed
model (ADR 0002 `model` + `parser`), and applying the privacy transform —
PAN tokenize, CPF mask — inside this same boundary (ADR 0004). Nothing
downstream may ever see a raw PAN or CPF.

**Interface out:** a fully sanitized, typed batch model, or a stable
grammar-rejection code (e.g. `INVALID_OVERPUNCH`). Judge does not parse or
sanitize; it only validates what this lane hands it.

| Leg | Responsibility | Proving test |
|---|---|---|
| 2.1 Decode the grammar | Header/detail/trailer decode, overpunch → exact decimal (ADR 0003) | `malformed` produces a stable rejection code, not a crash or a best-effort partial parse |
| 2.2 Sanitize at the boundary | Tokenize PAN (HMAC-SHA-256, fail-closed on missing key), mask CPF to last4, before the model leaves this lane | No raw PAN/CPF digit sequence appears anywhere this lane emits — model, logs, or error messages |

**Non-goals:** cross-record validation (detail-count vs. trailer, movement
sign, duplicate `transaction_id`), control-total recomputation, any
accept/refuse/quarantine decision — those are Judge's job on the model
this lane produces.

**Handoff owner (Parse → Judge):** **Priya Shah** — she signs off that
nothing crossing this boundary carries a raw PAN or CPF, before Judge is
allowed to touch it.

---

## Swimlane 3 — Judge

**Owns:** validating the sanitized model against the Type 01 contract's
cross-record rules, independently recomputing the control total in exact
decimal, and deciding accepted / refused / quarantined — including the
kept-lie rule (ADR 0005).

**Interface out:** exactly one of three verdicts — accepted-batch,
refused-batch + stable code, or quarantined-batch + declared amount +
computed amount, both kept distinct. Landing branches on this verdict; it
never re-derives it.

| Leg | Responsibility | Proving test |
|---|---|---|
| 3.1 Validate the grammar rules | Detail-count match, movement-sign rules, duplicate `transaction_id` rejection, etc. | `valid-boundary` is accepted; a structurally-bad batch is refused with a stable code |
| 3.2 Recompute and compare | Sum detail `amount_brl` (exact decimal) vs. declared trailer `net_amount_brl`; on mismatch, keep the declared value, record the computed value separately, quarantine | `df-source-001`: declared stays `173.44`, computed `173.45` is recorded as a separate field, batch is quarantined, unrelated batches are unaffected |

**Non-goals:** writing anything to disk, choosing a storage format —
Judge only decides; it never lands.

**Handoff owner (Judge → Landing):** **Marina Alves** — she owns the
accept/refuse/quarantine semantics and confirms every verdict this lane
produces obeys "keep the lie, refuse the batch" before Landing is allowed
to act on it.

---

## Swimlane 4 — Landing

**Owns:** writing the modern plant's first artifact (ADR 0001) — Parquet
under `modern/landing/` for an accepted batch — and writing nothing for a
refused or quarantined one (ADR 0005).

**Interface out:** `modern/landing/<batch>.parquet` exists with N rows, or
it does not exist for this batch. Nothing downstream of this week's scope
is decided by this lane.

| Leg | Responsibility | Proving test |
|---|---|---|
| 4.1 Write the accepted shape | One Parquet write per accepted batch, decimal-typed money columns (ADR 0003), matching Parse's sanitized model | `valid-minimal` lands one Parquet file, one row, net `173.45`, decimal-typed |
| 4.2 Write nothing for a bad batch | Refused or quarantined verdicts produce zero landing rows | `df-source-001` and `malformed` both land zero Parquet rows; unrelated batches still land normally |

**Non-goals:** any storage engine, warehouse, or lakehouse choice beyond
"Parquet in `modern/landing/`" (ADR 0001) — no `dbt`, no `dlt`, no
Bronze/Silver/Gold. Where a refused/quarantined batch's outcome is
*recorded* (a manifest? a log? a table?) is an open question for Pass 4,
not settled here.

**Handoff owner (Landing → later, not built this week):** **Helena Dias**
— she owns deciding when the next handoff (Bronze/Silver/Gold, golden-match
against `reporting.card_settlement_reconciliation`) actually starts; per
the tech-spec's open question, that is "after Consensus," not a Pass 3
decision.

---

## Named but not cut here — later weeks' seams

Naming these keeps the count honest without building them tonight:

- **Bronze → Silver → Gold, `dlt` registration, golden-match** — Day 3
  (Constructor). Reads Landing's output; not decomposed here.
- **Type `05` unattended loop, `HALF_UP` pill** — Day 4 (Orchestrator).
- **Types `02`–`05` ingest → landing** — same four-seam shape as this
  file, one per type, cut on their own nights — not cut here.
- **Type `06`** — sealed. Not in the drop, not named beyond this line.

## What this file is not

Plan-altitude only. No atomic tasks (Pass 5), no runnable evals (Pass 5),
no code, no SQL, no storage engine chosen, no ADR re-litigated. Leg
acceptance above is prose, on purpose — it becomes a runnable eval only
after Consensus (Pass 4) signs.
