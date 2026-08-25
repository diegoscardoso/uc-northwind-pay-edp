# Run — staff follow-along

This folder is for **you and the two designers**. It is the night you
actually run: beats, commands, who speaks, what “done” is, what to do
when a table dies.

It is not the student brief. It is not the deck.

| Folder | Job |
|---|---|
| [`agenda/`](../agenda/README.md) | Scope. What the night closes. Not the clock. |
| [`presentation/`](../presentation/README.md) | What the room sees. |
| **This folder** | What the three of you execute, in order. |

One folder per night. One file per beat, numbered. **One Night** — no
morning / afternoon split. Converge papers: [`docs/`](../docs/README.md).

Night 1 HTML is live — lockstep with [`d1-archaeologist.html`](../presentation/d1-archaeologist.html).
Night 2 HTML is live — lockstep with [`d2/`](d2/README.md) and [`d2-translator-java2py.html`](../presentation/d2-translator-java2py.html) (34 slides, five Hands-On boards). Identify Night 2 slides by `data-act-name`. Days 3–5 are stubs until those decks exist.

```text
run/
  README.md
  d1/          live — six slices A–F + Close 17. Deck 44 slides.
    README.md  slice index
    01–04      Slice A · Seat
    05–09      Slice B · Plant (boot before any status/run)
    10–11      Slice C · Read
    12         Slice D · Second Brain (nine packs, whole drop)
    13         Slice E · OntoLayer
    14–16      Slice F · Converge Capture → Intent · no Pass 2
    17         Close · Research, then walk
  d2/          live — 12 beats, same mold as d1 (prompts + proofs)
    README.md  slices A–E + Close
    01–02      A · Recap (status, papers)
    03–04      B · Harness (prompt, fail closed)
    05–06      C · Query (brain, graph)
    07–10      D · Pass 2–4 (kits, ADRs, seams, sign)
    11         E · Task-Spec
    12         Close · Research
  d3.md        stub — Constructor
  d4.md        stub — Orchestrator
  d5.md        stub — Dark Factory
```

## How to write a beat file

```text
# NN · name
- Slide:
- Who:
- Next: NN+1-….md

## Do / Prompt (verbatim)
## Proof
## If fail
```

Homework for the room is not a beat.

If `agenda/dN.md` and `run/dN/` disagree, **agenda wins on scope**.
Fix the run file. Do not invent a sixth type or a Pass the brief did
not authorize.
