# Seams — Type 01 ingest → landing

Pass 3 Decompose. Seamwise names: **seam**, **swimlane**, **leg**.
One owner per handoff. Papers live in `docs/`, not `cvg/docs/`.

The seam is a **handoff**, not a language. **Java vs Python is not a
seam.** Both plants read the same SFTP raw bytes; they do not own each
other.

## Steel thread

**Type 01 ingest → landing.** This is the only lane for leaves tonight
(Pass 5). Days 3–4 seams are named so the week has a map; they are not
tonight’s Task-Specs.

Landing facts already closed (ADRs 0001–0005): first write is
`modern/landing/` Parquet, not SFTP; five-file package; Decimal;
privacy dies at the parser; source lie keeps 173.44 and emits zero
Parquet.

## Vocabulary

| Name | Meaning here |
|---|---|
| **Seam** | The cut: what is consumed, what is produced, who may write |
| **Swimlane** | Exactly one owning seat. Coordinates the write surface. Others read through the contract |
| **Leg** | Ordered, observable capability on that lane. Proof is a terminal, not a promise |

Two owners on one seam, or a seam with no owner, is refused.

## Seam list

### 1. Ingest → landing

| | |
|---|---|
| **Seam** | Type 01 raw intake → sanitized landing |
| **Swimlane** | Translator (SWE) — Night 2 |
| **When** | Tonight’s design. Product write after Consensus |
| **Consumes** | Same SFTP `raw/incoming` bytes, checksum, manifest last. `contracts/types/01-card-settlement/` |
| **Produces** | Accepted: atomic Parquet + readiness manifest in `modern/landing/`. Refused / source lie: **zero Parquet**, stable finding |
| **Write surface** | Type 01 five-file package (`model → parser → schema → writer → handler`) and `modern/landing/` |
| **Must not write** | `legacy/`, `contracts/`, `gen/`, `infra/`, SFTP `csv/outgoing`, lakehouse, Gold |
| **Reads through contract** | Legacy CSV, Postgres paid grain, Java — observation only. Never inputs |

**Legs** (ordered):

1. **Sense** — identity, checksum, manifest-last, replay. Same raw the live line already reads.
2. **Claim** — Type 01 parse, Decimal money, privacy at the parser, independent controls.
3. **Emit** — landing Parquet for `valid-minimal` (net 173.45, MATCHED shape); quarantine with zero Parquet for `df-source-001` (keep 173.44) and malformed.

Tonight’s leaf attaches here only.

### 2. dlt → Gold

| | |
|---|---|
| **Seam** | Immutable landing → governed Gold |
| **Swimlane** | Constructor (DE + analytics) — Night 3 |
| **When** | Day 3. Parked in ADR 0006 |
| **Consumes** | `modern/landing/` Parquet already published. Does **not** re-parse raw |
| **Produces** | Bronze → Silver → Gold; golden-match attached to contract and to legacy observation |
| **Write surface** | dlt register / load, lakehouse, dbt models — **unparked on Day 3**, not chosen tonight |
| **Must not write** | Raw files, the Type 01 parser, frozen plant, landing bytes |

**Legs** (named, not run tonight): register landing → medallion grains → golden-match. Exact dlt role and Gold keys stay parked.

### 3. Orchestrate + serve

| | |
|---|---|
| **Seam** | Gold + Type 01 landing → unattended run and read-only serve |
| **Swimlane** | Orchestrator — Night 4 |
| **When** | Day 4. Parked in ADR 0006 |
| **Consumes** | Approved Gold; Type 05 contract when that night opens. Not restricted raw |
| **Produces** | Dagster lineage / replay; Type 05 unattended including `HALF_UP`; read-only serve of approved Gold only |
| **Write surface** | Dagster, serving — **unparked on Day 4** |
| **Must not write** | Parser, landing contract, frozen `legacy/`, unresolved Gold |

**Legs** (named, not run tonight): orchestrate replay → Type 05 pill → serve approved Gold. FastAPI/MCP and CI stay parked (default CI = no).

## Refused cuts

- Java vs Python
- CSV-as-input to modern
- SFTP as modern destination
- Type 06 (not in this drop)
- A lakehouse named as tonight’s lane

## Handoff rule

Each seam has one owner. Translator does not write Gold. Constructor
does not rewrite landing. Orchestrator does not parse Type 01. Pass 5
writes **one leaf on seam 1** after Consensus. No sign → no parser.
