# CONTEXT — shared vocabulary

Pass 2 Structure glossary. This file says what terms **mean**; the
`adrs/` say what is **true** (facts and constraints). Terms only —
pinned as they crystallize, not a second decision log.

## Steel thread

The single narrowest end-to-end slice that proves the whole shape
works before the rest is built. Tonight's steel thread is **Type 01**
card settlement; types 02–05 exist in the drop for later nights; Type
06 is not in the drop. (`docs/brd-type-01-card-settlement.md` §1–2)

## Five-file package

The unit of build for one settlement file type: **model, parser,
schema, writer, handler** — one handler per type, no sixth file.
Decided 2026-06-09 (D1). See ADR 0002.

## Overpunch

A COBOL fixed-width encoding where the final character of a numeric
field carries both the last digit and the sign (`positive_characters`
/ `negative_characters` alphabets), at a fixed decimal scale. Type 01
uses it for `amount_brl` and `net_amount_brl`, scale 2.
(`contracts/types/01-card-settlement/layout.yaml`)

## Sanitize

The act of turning a raw parsed record into one safe to persist or
emit: applying each field's approved privacy transform (tokenize,
mask, last4) and validating it against the type's schema. "Privacy
dies at the parser" (ADR 0004) names *where* sanitize happens for the
modern plant.

## Tokenize vs. mask

Two distinct approved transforms, not synonyms. **Tokenize** (PAN):
HMAC-SHA-256 keyed by `NWP_TOKENIZATION_KEY`, output
`tok_<24-hex-chars>`, fails closed if the key is missing. **Mask**
(CPF): retain last 4 digits, output `*******<last4>`.
(`contracts/types/01-card-settlement/privacy.yaml`)

## Source lie / kept source lie

A batch where the source's own declared control total (trailer
`net_amount_brl`) does not match the independently computed sum of its
detail records — on purpose, so the plant proves it does not silently
correct the source. "Keep the lie" means: keep the declared number
exactly as sent, record the computed number separately, and refuse the
batch. Never means patch the declaration to match. See ADR 0005.

## Net amount vs. settlement total

Two names for the same trailer bytes (positions 16–30 in the Type 01
layout): the layout PDF calls it **net amount**; Marina Alves's ops
mail calls it **settlement total**. Both refer to the same field. This
is an open, owned contradiction (`docs/brd-type-01-card-settlement.md`
§2, §5) — not resolved here. The judge (`contracts/`) uses "net
amount"; ops prose may keep saying "settlement total."

## Quarantine (batch-scoped)

When a batch is refused, only that one batch is held — no sanitized
output, no business mutation for it — while every unrelated batch
keeps moving. Decided 2026-06-09 (D3): "Quarantine is batch-scoped."

## MATCHED

The reconciliation status meaning: source, staged, and applied net
amounts and counts all agree, with zero amount/count delta. The
canonical happy-path example is batch `B202607230000001`,
`valid-minimal`, net `173.45`.

## Landing

`modern/landing/` — the modern plant's first artifact write: sanitized
Parquet, produced only by its own independent parser, never by
reusing Java or legacy's stored procedures. See ADR 0001. Distinct
from legacy's first write, which is CSV on `SFTP csv/outgoing`.

## Frozen plant

`legacy/`, `contracts/`, `gen/`, `infra/` — must not be edited to make
a later gate pass, by anyone, for any reason. (`README.md`)

## Judge

`contracts/` — the source of correctness once a type's contract is
installed. Outranks inbound prose (`spec/`) and outranks code. A
meeting using the wrong noun for a field (see "Net amount vs.
settlement total" above) is never grounds to edit the contract.

## Bronze / Silver / Gold, medallion

Terminology from the 2026-06-09 sync's architecture sketch. Recorded
here as **vocabulary the drop uses**, not as a Pass 2 decision — no
stack or lakehouse layout is chosen by this glossary or by ADR 0001.
Whether, and how, this vocabulary is adopted is a Decompose/Consensus
question.
