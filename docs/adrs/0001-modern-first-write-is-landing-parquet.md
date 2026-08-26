# 0001. The modern plant's first write is `modern/landing/` Parquet, not SFTP

**Status:** Accepted — Pass 2 Structure, human-led, 2026-08-25
**Deciders:** Helena Dias (owner), Rafael Costa (legacy line)

## Context

Two plants read the same raw bytes and must not converge on the same
write path. The 2026-06-09 file-decomposition sync fixed the modern
side's shape:

> customer drop → understand / decide → independent parser →
> **sanitized Parquet** → Bronze / Silver / Gold → compare to
> `expected/` and to a live legacy observation
> (`spec/estate/meetings/2026-06-09-file-decomposition.md`)

and its executive summary is explicit that the modern plant "must not
call Java and must not reuse the stored procedures to invent an
answer" — it is a second reader, not a second writer into the legacy
path.

`docs/tech-spec-type-01-card-settlement.md` R-7 states the same
constraint from Intent: "First write of the second plant is later, and
is not SFTP." `docs/README.md` names the artifact directly: Pass 8
Loop writes `modern/landing/`, and that write is "Product, not this
folder. Factory is Day 4" — i.e. explicitly not tonight.

The legacy plant's first write is CSV on `SFTP csv/outgoing`, landed
by Java after sanitize. That destination, and everything downstream of
it (`COPY`, stored procedures, `reporting.*`), belongs to the frozen
plant.

## Decision

Whenever the modern plant's first artifact write happens — after
Consensus, not tonight, per R-7 and `docs/README.md` — that first write
is **sanitized Parquet under `modern/landing/`**. It is not an SFTP
drop, it does not touch `legacy/postgres` tables, and it does not exist
until the modern plant's own independent parser has produced it.

This ADR fixes the *destination and ordering* only. It does not pick a
warehouse engine, a transform tool, or a lakehouse layout. The
2026-06-09 sync's "Bronze / Silver / Gold" phrasing is recorded here as
**inbound preference, not a Pass 2 decision** — Decompose/Consensus own
that choice, if any.

## Consequences

- Rules out treating `SFTP raw/incoming` or `SFTP csv/outgoing` as a
  modern output surface.
- Rules out sharing legacy's `COPY` / stored-procedure write path as a
  shortcut to a modern answer.
- Does not authorize creating `modern/landing/` on disk tonight — Pass
  2 records the decision; the write itself waits for its own gate.
- Leaves the storage engine, file layout, and medallion naming as open
  questions for Decompose/Consensus, not settled here.
