# Night 4 queue — the board

Linear is the **board**, not the judge. A card moves only when a packet
exists under `evidence/` (terminal, not Git). Chat is not a settle.

**Tonight do not open GitKraken / Linear in the browser.** The signed-in
Linear MCP is down. This file **is** the queue. If Linear comes back
later, copy these rows; do not recut the night for it.

| Card | Lane | Eval (exact) | Status tonight |
|---|---|---|---|
| T-20260825-type-01-landing-parser | ingest-landing | live `B202607230000001` MATCHED 173.45 + `evidence/modern/B202607230000001/golden-match.json` both questions true | packet `evidence/loop/T-20260825-type-01-landing-parser.json` · exit 0 |
| T-20260827-type-02-ingest | ingest-landing | `make run TYPE=02 SCENARIO=valid-minimal` | queued · `signed_off: false` |
| T-20260827-type-02-lakehouse | dlt-gold | golden-match Type 02 · both questions | queued |
| T-20260827-type-03-ingest | ingest-landing | `make run TYPE=03 SCENARIO=valid-minimal` | queued |
| T-20260827-type-03-lakehouse | dlt-gold | golden-match Type 03 | queued |
| T-20260827-type-04-ingest | ingest-landing | `make run TYPE=04 SCENARIO=valid-minimal` | queued |
| T-20260827-type-04-lakehouse | dlt-gold | golden-match Type 04 | queued |
| T-20260827-type-05-ingest | ingest-landing | `make run TYPE=05 SCENARIO=valid-minimal` · `SCENARIO=malformed` · `SCENARIO=DF-SOURCE-005` | queued |
| T-20260827-type-05-lakehouse | dlt-gold | `DF-SOURCE-005` = `CONFIRMED_SOURCE_DEFECT` · `rounding-half-up` = `HALF_UP` · `HALF_EVEN` = `MODERN_DEFECT` | queued |
| T-20260827-orchestrate-type-01 | orchestrate-serve | same Gold hash if Dagster exists · **skip hash if Dagster is not up** | queued · do not stand up Dagster to look busy |

Do not settle from chat. Do not open Type `06`.
