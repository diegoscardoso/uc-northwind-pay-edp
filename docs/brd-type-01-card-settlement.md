# BRD — Card Settlement Detail (Type 01)

**Pass:** Converge Pass 0 · Capture — human-led, no product code
**Owner voice:** Helena Dias, Partner Integration
**Sources:** Second Brain (NotebookLM, packs `00`–`03`, `08`) · `spec/estate/` · `spec/type-01-card-settlement/` · `spec/README.md`
**Status:** Draft for the room, not signed

---

## 1. Who asked, and what is out of scope

I asked for this. My cover memo of 2026-06-24 to the modernization team is
plain: **rebuild the five live settlement files beside the current Java
line. Do not replace Java. Do not "fix" source totals.** NorthWind Pay
already runs five file types through SFTP → Java 21 → sanitized CSV →
PostgreSQL. I want a second, independent implementation that reads what we
mailed you — not the Java — and still lands on the same terminal outcomes.

That request was confirmed at kick-off on 2026-06-02, with the room agreeing
to four decisions that bound everything downstream: Java is not replaced
(Rafael — the live line stays the oracle); five types only are in this drop
(me — a sixth file is a later pack); source totals are never rewritten
(Marina — the lie is evidence); privacy is finished before any CSV exists
(Priya — the loader must never see a PAN). Rafael also made clear, in the
9 June file-decomposition sync, that your plant must not call Java and must
not reuse our stored procedures to invent an answer — it reads the same raw
bytes and reaches its own answer.

**Out of scope for this drop, and for tonight:**

- Replacing or modifying the live Java line.
- Editing `legacy/`, `contracts/`, `gen/`, or `infra/` to make anything
  easier later.
- Type `06`. It is not in this folder. If a sixth file shows up, it arrives
  as its own pack — I said so at kick-off, and I am saying it again here.
- A parser, a lakehouse model, or permission to touch the live line. We are
  not sending those. We are sending the drop.
- Tonight specifically is **Type `01` only** — card settlement. Types
  `02`–`05` (instant payment, payment slip, TED, merchant fees) are real and
  in the drop, but they are for the rest of the week to ask, not for tonight
  to build.

## 2. What lands

Five live file types land in this drop, one inbound pack each: `01` card
settlement, `02` instant payment events, `03` payment slip settlement, `04`
TED transfer settlement, `05` merchant fee assessment. Every pack has the
same shape — `inbound/` (what we mailed, messy on purpose), `samples/` (raw
bytes plus SHA-256 sidecars), `expected/` (the oracle: sanitized rows and
reconciliation for what should be accepted, stable refusal codes for what
should not).

**Type `01` — the steel thread for tonight — is `CRD_SETTLE01`, `.dat`,
ISO-8859-1 fixed width, COBOL overpunch.** What we mailed for it:

- **Layout Revision 3** — one 40-byte header, one or more 124-byte details,
  one 46-byte trailer. Positions are 1-based. The detail carries a clear PAN
  (tokenize it), a clear CPF (mask it), an overpunch-encoded amount, and a
  movement code (`P` purchase, strictly positive; `R` refund, strictly
  negative). The trailer carries a detail count and a net-amount overpunch
  field that must equal the sum of the details.
- **Two dated apply procedures.** The 2026-05-12 dump only copies positive
  amounts — it predates refunds on the same file. Rafael was explicit at the
  30 June walk-through: ignore it, "SSMS dumps the object history wrong."
  Use the 2026-07-01 script — refunds are first-class there, and
  `chargeback_flag` is confirmed dead; it does not belong downstream.
- **A table dump** (`staging.card_settlement`, `legacy.card_settlement`)
  from Rafael, and a reconciliation shape
  (`reporting.card_settlement_reconciliation`) built from source, staged,
  and applied counts and net amounts.
- **Five samples with checksums**, and an oracle for each: `valid-minimal`
  (happy, net `173.45`), `valid-boundary` (boundary, accepted),
  `negative-overpunch` (refund edge, net `-12.34`), `malformed` (grammar
  failure, `INVALID_OVERPUNCH`), and `df-source-001` (the source lie —
  Section 4).

One open item the room has not closed: Marina still calls trailer bytes
16–30 "settlement total" on the ops dashboard; the layout calls the same
bytes "net amount." Same number, two nouns. I have not resolved that yet —
see Section 5.

## 3. What "done" means

Done is not "the file parsed." Done is one of three outcomes, and I named
all three in my cover memo:

- **Accepted** — for every accepted sample, the sanitized rows and the
  reconciliation match the oracle exactly, privacy holds, and tolerances are
  zero. Not "close." Zero.
- **Refused** — for every sample that should not go through, the plant
  returns a stable rejection code, writes no CSV, applies no business rows,
  and every unrelated batch keeps moving. One bad batch never stops the
  line.
- **A kept source lie** — for every sample where the source itself declared
  something false, the plant classifies it as a source defect and never
  repairs it.

Those are the only three terminal states I will accept as "done" for Type
`01` tonight. A fourth outcome — quietly writing a corrected number and
calling it accepted — is not on this list, and it is not a passing outcome
under any reading of what I asked for.

## 4. The lie

`df-source-001`, batch `B202607230000004`, is Type `01`'s source-owned lie,
and it is the one every later pass has to respect. The trailer's net-amount
field **declares 173.44**. The detail records **add up to 173.45**. That is
not a rounding artifact — it is the source lying about its own total, on
purpose, so the drop can prove the plant does not quietly correct it.

Marina Alves said it as plainly as it can be said, on 2026-07-14, after we
sent back a version that resolved the mismatch:

> "I am not sending another 'corrected' file. Card settlement
> `B202607230000004` still declares 173.44. Our details add to 173.45. …
> If your new plant quietly writes 173.45 into the trailer we will have
> nothing to show the source. **Keep their number. Refuse the batch. That
> is the whole point.**"

The same shape of lie exists on every one of the five live types — PIX,
slips, TED, and the fee file all carry their own one-unit source lie. Type
`01` is the one we prove tonight.

The expected outcome for `df-source-001` is not ambiguous:
`expected_status: quarantined`, `expected_code:
SOURCE_CONTROL_TOTAL_MISMATCH`, `declared_net_amount: "173.44"` (kept,
unedited), `computed_net_amount: "173.45"` (computed for the finding, never
written back), `csv_produced: false`, `postgres_business_mutation: false`,
quarantine scoped to this one batch, and every unrelated batch continues.

**We do not "fix" 173.44.** We keep the declaration, compute the truth for
the finding, and refuse the batch. That is the whole point, and it stays the
whole point past tonight.

## 5. Inbound vs judge

Everything this BRD is built from — the estate, the Type `01` inbound pack,
and what the Second Brain retrieved from them — is **inbound**, not the
judge. It is mail, meeting notes, an SSMS table dump, two dated stored
procedures, and an ops thread. It is allowed to be messy, allowed to use the
wrong noun, and allowed to contradict itself, because that is what a real
customer drop looks like. Marina calling bytes 16–30 "settlement total"
while the layout calls the same bytes "net amount" is exactly that kind of
open contradiction — real, unresolved, and owned by nobody yet.

The Second Brain was built from this inbound prose and nothing else. It does
not have `contracts/`. It does not have the Java implementation. It cannot
read a raw `.dat` file — it has never seen signed overpunch bytes. Every
number in this BRD that the Second Brain surfaced — the 173.44-declared,
173.45-computed shape, and that the same shape repeats across all five types
— was retrieved from the mail and meeting prose in the drop, not from
opening a sample or a contract.

**Inbound prose does not outrank `contracts/`.** Once a contract for Type
`01` is installed, `contracts/` is the source of correctness that DataGen,
the Java processor, and the independent oracles are bound to obey. If a
meeting note used the wrong noun, we write that down as an open
contradiction for Structure to resolve later — we do not "fix" the contract
to match the mail, and we do not let the mail stand in for the contract in
the meantime.

## 6. What we will not do tonight

- **We will not write `modern/`.** The first modern write is a later
  event — Type `01` landing Parquet, after Consensus signs off the plans.
  Tonight is Capture. There is no product code in this pass.
- **We will not pick a stack.** Rafael's file-decomposition sync named a
  shape (one handler per type: model, parser, schema, writer, handler; exact
  decimal, no float money) — that shape is real, but choosing the concrete
  stack against it is a later Structure/Decompose decision, not tonight's.
- **We will not write ADRs.** Grounding decisions come at Pass 2, after
  Consensus, against the real repo. Tonight has no repo to ground against
  yet.
- **We will not cut seams.** Splitting the system along swimlanes is Pass
  3, after Structure. Nothing here is decomposed into legs or tasks.
- **We will not "fix" 173.44 to 173.45** — not tonight, not later. The
  declaration is kept, the truth is computed and recorded, the batch is
  refused. That rule outlives this BRD.
- **We will not touch Type `06`.** It is not in this drop. It is sealed
  until it arrives as its own pack.
- **We will not edit `legacy/`, `contracts/`, `gen/`, or `infra/`** to make
  any of the above easier. Nothing in tonight's capture requires it, and if
  it ever seems to, that is a hard stop, not a shortcut.

---

*This BRD captures intent only. It is not a tech-spec, not an ADR, not a
plan, and not permission to write code. Pass 1 reads this next.*
