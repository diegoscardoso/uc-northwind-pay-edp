---
id: T-20260826-type01-landing-writer
title: "Write an accepted Type 01 batch to deterministic Parquet under modern/landing/, refusing anything unsanitized"
status: blocked
format_version: 3
profile: standard
effort: S
budget_iterations: 15
agent: any
parent: docs/seams.md
depends_on: []
supersedes: (none)

touches_paths:
  - modern/type01/writer.py
creates_paths:
  - modern/type01/writer.py
  - modern/type01/model.py
source_note: "Pass 5 Tasking, authored 2026-08-26 by explicit instruction to proceed past an unsigned Pass 4 for training purposes. See precondition and Open Questions below — this is NOT a real authorization to dispatch."
created: 2026-08-26T03:00:43Z
tags: [type-01, landing, writer, privacy, decimal]
owner: (none)
priority: P2
severity: financial-critical
due_date: (none)
precondition: "Pass 4 Consensus has NOT signed for docs/seams.md (no cross-family adversary review completed; docs/consensus.md does not exist). This leaf exists as a Pass 5 authoring exercise only. It must stay signed_off:false and must not be dispatched or run against real modern/ code until Consensus actually closes."
blocked_reason: "Unsigned Consensus (Pass 4) — see precondition. Authored out-of-band on explicit request, not queued for pickup."
security_class: pii-and-money
source_action_item: (none)
tracker_ref: (none)
execution_backend: any
signed_off: false
signed_off_by: (none)
signed_off_at: (none)
accepted: false
accepted_by: (none)
accepted_at: (none)
evidence_refs: []

---

# "Write an accepted Type 01 batch to deterministic Parquet under modern/landing/, refusing anything unsanitized"

> **Why:** `modern/landing/` is the modern plant's first artifact (ADR 0001) and
> the last line of defense for two non-negotiable properties — exact decimal
> money (ADR 0003) and no raw PAN/CPF ever reaching disk (ADR 0004) — plus the
> kept-lie rule's "zero rows" side (ADR 0005). The writer must enforce all
> three at its own boundary, not merely trust that Parse/Judge upheld them.

---

## Goal

Given a sanitized, schema-valid Type 01 batch model and its Judge verdict
(accepted / refused / quarantined), a `write_batch` function writes exactly
one deterministic Parquet file under a `modern/landing/`-shaped directory for
an accepted batch — decimal-typed money columns, byte-identical output across
repeated runs on the same input — and writes **zero rows** for a refused or
quarantined batch. The function refuses (raises, writes nothing) if handed a
record carrying a raw PAN, a raw CPF, or a float-typed money field, regardless
of what verdict it was given. Nothing this leaf creates ever touches a path
outside `modern/type01/` and its own `landing_dir` output.

---

## Context

This leaf is Swimlane 4 ("Landing") from `docs/seams.md`, legs 4.1 and 4.2,
narrowed to one runnable unit. It reads `docs/adrs/0001` (destination and
ordering), `0003` (exact decimal), `0004` (privacy at the parser — the writer
re-checks this boundary rather than trusting it blindly), and `0005` (kept
lie, zero rows). The full picture — Ingest, Parse & Sanitize, and Judge — is
`docs/seams.md`; this leaf implements none of those, only the Landing
interface each of them hands off to.

**This leaf is not authorized to run.** Pass 4 Consensus has not signed
`docs/seams.md` — the only adversary dispatch attempted (`cvg review
--adversary claude --dir docs`) failed closed (`REVIEW=ERROR`, no parseable
judgment), and no cross-family engine (`codex`/`kimi`) is installed. It was
authored anyway, on explicit instruction, as a Pass 5 Tasking exercise. Its
`signed_off` field stays `false`; nothing here should be dispatched to an
executor until a real Consensus closes this seam.

**Update, same day:** `modern/type01/model.py` and `modern/type01/writer.py`
were implemented anyway, on a second explicit instruction, and `taskspec run`
reports all three evals green. This does not retroactively authorize
anything — `signed_off`, `status: blocked`, and `blocked_reason` are left
exactly as above on purpose, because the gate this file names was still
never run. Treat the passing evals as a training-exercise proof of the
approach, not as settlement evidence for a real dispatch.

---

## Behavior

- **B-1** — GIVEN a Judge-accepted `SanitizedBatch` with decimal-typed
  amounts, tokenized PANs, and masked CPFs, WHEN `write_batch` runs on it
  twice into two separate output paths, THEN both writes succeed, both files'
  money columns are decimal-typed (not float), and the two files are
  byte-identical (SHA-256 match).
- **B-2** — GIVEN a batch containing any one of: a raw (untokenized) PAN, a
  raw (unmasked) CPF, or a float-typed money field, WHEN `write_batch` runs on
  it, THEN it raises rather than writing any file — regardless of the verdict
  the batch was given.
- **B-3** — GIVEN a batch whose verdict is `refused` or `quarantined`, WHEN
  `write_batch` runs on it, THEN it produces zero rows and zero files for
  that batch; and across every case in B-1/B-2/B-3, no file is created or
  modified anywhere outside the function's own `landing_dir` argument — in
  particular never under `legacy/`, `contracts/`, `gen/`, or `infra/`.

---

## Success Criteria

Each criterion is a runnable bash function returning 0 (pass) or non-zero (fail).
Each MUST be terminal (deterministic, idempotent, non-flaky).

```bash
# eval-1: accepted batch -> deterministic, decimal-typed Parquet (B-1)
eval_1() {
  REPO_ROOT="$(git rev-parse --show-toplevel)"
  cd "$REPO_ROOT" || return 1
  "$REPO_ROOT/modern/.venv/bin/python3" - <<'PY'
import sys, decimal, hashlib, tempfile, os

try:
    from modern.type01.writer import write_batch
    from modern.type01.model import SanitizedBatch, SanitizedDetail
except ModuleNotFoundError as e:
    print(f"RED (expected until this leaf is implemented): {e}", file=sys.stderr)
    sys.exit(1)

batch = SanitizedBatch(
    batch_id="B202607230000001",
    net_amount=decimal.Decimal("173.45"),
    verdict="accepted",
    details=[
        SanitizedDetail(pan_token="tok_" + "a" * 24, cpf_masked="*******1234",
                         amount=decimal.Decimal("100.00")),
        SanitizedDetail(pan_token="tok_" + "b" * 24, cpf_masked="*******5678",
                         amount=decimal.Decimal("73.45")),
    ],
)

with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
    out1 = write_batch(batch, landing_dir=d1)
    out2 = write_batch(batch, landing_dir=d2)
    h1 = hashlib.sha256(open(out1, "rb").read()).hexdigest()
    h2 = hashlib.sha256(open(out2, "rb").read()).hexdigest()
    assert h1 == h2, f"writer is not deterministic: {h1} != {h2}"

    import pyarrow.parquet as pq
    schema = pq.read_schema(out1)
    amt_type = str(schema.field("net_amount").type)
    assert amt_type.startswith("decimal"), f"net_amount column is {amt_type}, not decimal"

print("OK")
PY
}

# eval-2: raw PAN, raw CPF, or float money -> refused, nothing written (B-2)
eval_2() {
  REPO_ROOT="$(git rev-parse --show-toplevel)"
  cd "$REPO_ROOT" || return 1
  "$REPO_ROOT/modern/.venv/bin/python3" - <<'PY'
import sys, decimal, tempfile

try:
    from modern.type01.writer import write_batch
    from modern.type01.model import SanitizedBatch, SanitizedDetail
except ModuleNotFoundError as e:
    print(f"RED (expected until this leaf is implemented): {e}", file=sys.stderr)
    sys.exit(1)

def expect_refusal(batch, label):
    with tempfile.TemporaryDirectory() as d:
        try:
            write_batch(batch, landing_dir=d)
        except Exception:
            return
        raise AssertionError(f"writer accepted a batch it must refuse: {label}")

expect_refusal(SanitizedBatch(batch_id="X", net_amount=decimal.Decimal("1.00"), verdict="accepted",
    details=[SanitizedDetail(pan_token="4111111111111111", cpf_masked="*******1234",
                              amount=decimal.Decimal("1.00"))]), "raw PAN")

expect_refusal(SanitizedBatch(batch_id="X", net_amount=decimal.Decimal("1.00"), verdict="accepted",
    details=[SanitizedDetail(pan_token="tok_" + "a" * 24, cpf_masked="12345678901",
                              amount=decimal.Decimal("1.00"))]), "raw CPF")

expect_refusal(SanitizedBatch(batch_id="X", net_amount=1.00, verdict="accepted",
    details=[SanitizedDetail(pan_token="tok_" + "a" * 24, cpf_masked="*******1234",
                              amount=1.00)]), "float money")

print("OK")
PY
}

# eval-3: refused/quarantined -> zero rows; nothing ever written outside landing_dir (B-3)
eval_3() {
  REPO_ROOT="$(git rev-parse --show-toplevel)"
  cd "$REPO_ROOT" || return 1
  before="$(find . -type f 2>/dev/null | sort)"
  "$REPO_ROOT/modern/.venv/bin/python3" - <<'PY'
import sys, decimal, tempfile, os

try:
    from modern.type01.writer import write_batch
    from modern.type01.model import SanitizedBatch, SanitizedDetail
except ModuleNotFoundError as e:
    print(f"RED (expected until this leaf is implemented): {e}", file=sys.stderr)
    sys.exit(1)

refused = SanitizedBatch(batch_id="B-refused", net_amount=decimal.Decimal("0.00"),
                          details=[], verdict="refused")
quarantined = SanitizedBatch(batch_id="B202607230000004", net_amount=decimal.Decimal("173.44"),
                              details=[], verdict="quarantined")

for batch, label in [(refused, "refused"), (quarantined, "quarantined")]:
    with tempfile.TemporaryDirectory() as d:
        out = write_batch(batch, landing_dir=d)
        assert out is None or not os.path.exists(out), f"{label} batch produced a landing file"
        assert os.listdir(d) == [], f"{label} batch left files under landing_dir"

print("OK")
PY
  rc=$?
  after="$(find . -type f 2>/dev/null | sort)"
  # A ModuleNotFoundError above exits before touching the filesystem at all — the
  # expected RED state pre-implementation. Once implemented, this still asserts the
  # run left the repo tree untouched outside its own temp landing_dir.
  if [ "$before" != "$after" ]; then
    echo "writer touched files outside its own landing_dir — repo tree changed" >&2
    diff <(echo "$before") <(echo "$after") >&2
    return 1
  fi
  return $rc
}
```

---

## Validation Card

```yaml
success_criteria:
  # check_type: deterministic (default, bash-checked, preferred) | llm_judge
  # (subjective criteria graded by a fast LLM via judge_prompt — deterministic-first).
  # verifies: the behavior id(s) this eval proves. Standard/full profiles require
  # every B-N to be covered by >=1 eval and every eval to map to a behavior.
  - id: eval_1
    description: Accepted batch writes deterministic, decimal-typed Parquet
    runnable: bash
    check_type: deterministic
    verifies: [B-1]
    terminal: true
    expected_duration_sec: 5
  - id: eval_2
    description: Raw PAN, raw CPF, or float money is refused before any write
    runnable: bash
    check_type: deterministic
    verifies: [B-2]
    terminal: true
    expected_duration_sec: 5
  - id: eval_3
    description: Refused/quarantined batches write zero rows; no writes outside landing_dir
    runnable: bash
    check_type: deterministic
    verifies: [B-3]
    terminal: true
    expected_duration_sec: 5

retry_policy:
  max_iterations: 15
  circuit_breaker_no_progress: 3
  on_terminal_failure: park_with_context

agent_contract:
  version: 2
  read: [intent, behavior, contract, guardrails, operations]
  produce:
    - code
    - docs
    - config
    - tests
  required_tools: [git, bash, python3]
  timeout_minutes: 30
  sandbox_type: host
  output_artifacts: []
  mcp_dependencies: []
  emit:
    - pass
    - fail
    - retry_with_reason
    - parked_with_context
  backend_metadata: {}
```

---

## Exit Check

```bash
# Final proof-of-done. Returns 0 only when ALL evals pass.
eval_1 && eval_2 && eval_3
```

---

## Rollback Plan

(none — this task is append-only: it only ever creates new files under
`modern/type01/`. No existing file is modified. If execution goes wrong,
delete `modern/type01/writer.py` and `modern/type01/model.py` and reset the
task's status to `parked`.)

---

## Observability Hooks

- **Expected duration:** under 30 minutes to a first green (S-tier).
- **Key metric:** Parquet files written == accepted batches processed, for
  every run over `contracts/types/01-card-settlement/main/*.dat` samples.
- **Alert condition:** any raw 16-digit PAN or raw 11-digit CPF digit
  sequence found in a written Parquet file, or any float-typed money column.
- **Log tail:** `write_batch`'s own stdout/stderr for the batch_id in
  question — no separate log file is created by this leaf.

---

## Anti-Patterns

- **Don't use `float`/`double` for any money column** — ADR 0003 makes this a
  hard rule, not a style preference; a "close enough" comparison anywhere in
  the write path is itself a violation. Use `decimal.Decimal` in Python and a
  fixed-scale decimal Arrow/Parquet type on disk.
- **Don't trust that Parse/Judge already sanitized the record** — ADR 0004
  puts tokenization/masking at the parser, but this leaf's job is to be the
  last independent check; accepting an unsanitized record "because upstream
  should have caught it" defeats the point of a boundary guard.
- **Don't write a placeholder or "adjusted" row for a refused/quarantined
  batch** — ADR 0005 requires zero rows, not one row with a corrected total.
  If a caller ever needs to know *why* a batch produced nothing, that's a
  separate recorded outcome (see Open Questions), never a landing row.

---

## Do-Not-Touch

Files the executor MUST NOT modify:

- `legacy/`, `contracts/`, `gen/`, `infra/` — frozen plant, see `README.md`.
- `docs/adrs/*`, `docs/seams.md`, `docs/CONTEXT.md` — signed Structure/Decompose
  papers this leaf reads, not edits.
- Any path under `modern/` other than `modern/type01/writer.py` and
  `modern/type01/model.py` — no `modern/landing/` fixtures committed to git,
  no lakehouse scaffolding, no stack picked (ADR 0001).

---

## Open Questions

Things the executor should resolve DURING build, not assume:

1. **Where is a refused/quarantined batch's outcome recorded?** — `docs/seams.md`
   Swimlane 4 leaves this open (a manifest? a log? a table?). This leaf only
   requires zero landing rows; it does not specify where the refusal itself
   is recorded. Do not invent a destination — flag it back to Decompose/Consensus
   if a real answer is needed to proceed.
2. **Exact Arrow/Parquet decimal precision and scale for `net_amount` /
   detail `amount`** — ADR 0003 fixes "exact decimal, scale 2, never float";
   it does not pick the concrete Arrow decimal width (`decimal128(9,2)` vs.
   another precision). Pick the narrowest exact type that cannot silently
   truncate a valid Type 01 amount, and record the choice — don't default
   without checking it against the layout's field widths.

(This task is not fully specified on purpose — those two questions are true
open items, not filler.)
