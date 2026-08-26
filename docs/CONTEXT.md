# CONTEXT — Type 01 domain terms

Pass 2 Structure glossary. Not inbound. Not the judge. Not a stack.
Papers live in `docs/`, not `cvg/docs/`.

| Term | Meaning here |
|---|---|
| **Inbound** | `spec/` — mail, meetings, layouts, samples. Contradictions allowed. `cover.md` is mail. |
| **Judge** | `contracts/` — signed layouts and oracles. Outranks inbound prose and outranks code. |
| **Frozen plant** | `legacy/`, `contracts/`, `gen/`, `infra/`. Do not write. |
| **Steel thread** | Type 01 card settlement, `CRD_SETTLE01`, `.dat`. Tonight’s slice. Types 02–05 exist; Type 06 does not. |
| **Five-file package** | `model → parser → schema → writer → handler`. The Type 01 unit (ADR 0002). |
| **Landing** | `modern/landing/` — first write of the second plant: sanitized Parquet + readiness manifest. **Not SFTP** (ADR 0001). |
| **First write (legacy)** | Sanitized CSV on SFTP `csv/outgoing`. Comparison observation only for modern. |
| **MATCHED** | Source, stage, and books agree to the cent: counts equal, nets equal, `reject_count` 0. Type 01 happy path: net `173.45`, two records, `amount_delta` `0.00`. |
| **Paid (Type 01)** | Observed on `reporting.card_settlement_reconciliation`. Grain: `batch_id` + `currency`. Writer: `reporting.refresh_card_settlement_reconciliation`. Staging is not paid. (OntoLayer / `make ontology-ask`.) |
| **Source lie** | Declared control ≠ independently computed control. Type 01: trailer **173.44** vs rows **173.45**, batch `B202607230000004`, code `SOURCE_CONTROL_TOTAL_MISMATCH`. Keep the declaration (ADR 0005). |
| **Refuse the batch** | Stable terminal: quarantine that batch, no sanitized rows, no business mutation, peers continue. Not a crash. Modern: **zero Parquet**. |
| **Net amount** | Layout / contract name for trailer bytes 16–30 (`net_amount_brl`). |
| **Settlement total** | Ops mail noun for the same bytes (Marina). Does not outrank the contract. Parked (ADR 0006). |
| **Overpunch** | Last digit carries the sign. Scale 2. Example: `00000001234E` → `123.45`. |
| **Decimal** | Exact money. Never binary float (ADR 0003). Tolerances are zero. |
| **Privacy boundary** | Clear PAN and CPF die at the parser. Token + last4 / `*******` + last4 before landing (ADR 0004). Live line: Java. Second plant: the Type 01 parser, not a Java import. |
| **Bind** | Rails on the harness. Frozen trees refuse writes. A polite prompt is not a fence. |
| **Consensus** | Pass 4. Owner signs. No sign → no parser. |
| **Lakehouse / dlt / dbt / Dagster** | Later nights. Not chosen in Structure (ADR 0006). |

Do not upload this file into NotebookLM.
