# Presentation

What the room **sees**. Self-contained HTML. Open in a browser, `F11`.
No build step, no server — the only external fetch is Google Fonts.

This folder is not the week map ([`agenda/`](../agenda/README.md)), not
the staff clock ([`run/`](../run/README.md)), not the Converge papers
([`docs/`](../docs/README.md)), and not the engagement spec
([`plans/`](../plans/README.md)). Images live in [`../assets/`](../assets/).

Two shapes live here:

| Shape | How it plays | Files |
|---|---|---|
| **Follow-along deck** | Snap slides, HUD, Hands-On boards. One Night. | `d1-archaeologist.html`, `d2-translator.html`, `d3-constructor.html` |
| **Method / reference** | Manual or workshop. Teach the kit, not the clock. | `seamwise.html`, `task-spec.html`, `cvg-…`, `asd-…`, `boot-…`, `wrkp-…`, `yt-…` |

If a night’s HTML and [`run/dN/`](../run/) disagree, **agenda wins on
scope**; **run wins on the clock**. Identify Night 2–3 slides by
**`data-act-name`**, not a HUD integer. Type `06` is not in `spec/` until
Friday.

**Live this week:** Night 1 (44), Night 2 (34), Night 3 (Constructor +
[`run/d3/`](../run/d3/README.md) — Type 01 Gold steel thread). **Not built:**
Days 4–5 HTML (Thursday generates remaining SWE+DE then cranks).

---

## What’s in this folder

| File | Kind | What it is | When you open it |
|---|---|---|---|
| [`d1-archaeologist.html`](d1-archaeologist.html) | Night 1 deck | Onboard + Archaeologist. **44 slides**, six blocks, HUD `01`–`44`. Pass **0–1** only. **Live.** | Night 1. Staff: [`run/d1/`](../run/d1/README.md) |
| [`d2-translator.html`](d2-translator.html) | Night 2 deck | Translator · java2py. **34 slides**, six blocks, five Hands-On boards (slices a–e). Identify by `data-act-name`. **Live.** | Night 2. Staff: [`run/d2/`](../run/d2/README.md) |
| [`d3-constructor.html`](d3-constructor.html) | Night 3 deck | Constructor · DE + analytics. Six blocks, four Hands-On boards (A–D). Identify by `data-act-name`. **Live.** Lockstep with `run/d3/`. | Night 3. Staff: [`run/d3/`](../run/d3/README.md) |
| Days 4–5 | — | Orchestrator / Dark Factory. **Not in this folder.** | Build from [`agenda/d4.md`](../agenda/d4.md)–[`d5.md`](../agenda/d5.md). Staff still stubs: [`run/d4.md`](../run/d4.md) |
| [`seamwise.html`](seamwise.html) | Method kit | SeamWise internals. **Leave · SeamWise** parks here (Nights 2 and 3), then **returns** to the numbered beat | Pass 3 kit. Not the Night clock |
| [`task-spec.html`](task-spec.html) | Method kit | Task-Spec internals. Dig **Show**, then return to Execute (Night 2: 11 · Night 3: 10) | Pass 5 kit. Not the Night clock |
| [`cvg-aut-systems-spine-steps.html`](cvg-aut-systems-spine-steps.html) | Method manual | Converge spine — nine passes, two phases, one human barrier. **36 slides**, print-page layout. v7 · Converge 0.2.0 | When the room needs the kit, not the Night. Papers: [`docs/`](../docs/README.md) |
| [`asd-agentic-loop.html`](asd-agentic-loop.html) | Method manual | ASD — the Agentic Loop. Scroll document, **12 sections** (not a HUD deck) | Doctrine |
| [`boot-uc-northwind-pay-edp-oss.html`](boot-uc-northwind-pay-edp-oss.html) | Method manual | Bootcamp reference — case framing, Shapiro ladder, the week arc. **19 slides** | Framing. Not the follow-along |
| [`wrkp-dark-factory.html`](wrkp-dark-factory.html) | Workshop | Dark Factory Operation. **83 slides**. Broader workshop, not Night 5’s sealed Type `06` | Context / seed |
| [`yt-agentic-engineering.html`](yt-agentic-engineering.html) | Talk | *Engenharia Agêntica* (pt-BR). **44 slides** | Outreach. Do not drive a Night from it |

One Night — no morning / afternoon split.

**Week story on these HUDs:** Night 1 understands (0–1). Nights 2–3 are
**Type 01 steel threads** (SWE ingest → landing, then DE landing → Gold).
Night 4 (not built) generates remaining SWE+DE and cranks (Mesh + Pass 6–8,
Linear), then Type `05` unattended.

---

## Night 1 · Archaeologist

[`d1-archaeologist.html`](d1-archaeologist.html) — **44 slides, six blocks**.
HUD pill is the block name. HUD `01`–`44`.

| Block | Slides | Mode |
|---|---|---|
| Opening | 1 | title |
| Stage | 7 | presentation, keyboards down |
| Craft | 6 | teaching + Hands-On A (01–04) |
| Floor | 9 | teaching, Hands-On B (05–09), MATCHED look-up |
| Dig | 14 | roles, estate, Show then Hands-On C–F (10–16) |
| Debrief | 7 | Research (17), Next, silent Tomorrow |

Six Hands-On boards only (slices A–F). Brain: unzip
[`brain/notebooklm/northwind-pay-brain.zip`](../brain/notebooklm/northwind-pay-brain.zip)
and upload the **nine** `.md` files. Days 2–4 **query** that notebook. Type `06`
is not in it.

Staff: [`run/d1/README.md`](../run/d1/README.md).

## Night 2 · Translator

[`d2-translator.html`](d2-translator.html) — **34 slides, six blocks**.
Identify by `data-act-name`.

| Block | Mode |
|---|---|
| Opening | title |
| Stage | Recap Shows, Execute 01–02, then lecture (SWE, java2py, ingest) |
| Craft | Harness Shows, Execute 03–04 |
| Floor | Query Shows, Execute 05–06 |
| Dig | Converge Show, Leave · SeamWise (`seamwise.html`), Execute 07–10, Task-Spec Show (`task-spec.html`), Execute 11, Task-Mesh Show |
| Debrief | In hand, Research 12, Next, silent Tomorrow |

Five Hands-On boards (slices a–e). Research is Close, not a sixth board.
`java2py` is a nickname for the second plant, not a Java port.
Staff: [`run/d2/README.md`](../run/d2/README.md).

## Night 3 · Constructor

[`d3-constructor.html`](d3-constructor.html) — six blocks, four Hands-On
boards (A–D). Identify by `data-act-name`. Extra Stage talk slides (Lakehouse,
Agentic field) are talk only — they have **no** `run/d3/` file. **SA plan · mermaids**
is Stage Show; the room **types** it as `run/d3/04` on Execute 08 after J5 abstains.

| Block | Mode |
|---|---|
| Opening | title · Constructor |
| Stage | Recap, DE+analytics role, foundations, pipeline, engines, **SA plan mermaids**, medallion, agentic modeling |
| Craft | Bind still on (Show). Kits. **No** fail-closed board |
| Floor | Second Brain + OntoLayer Shows, **Execute 08** (`run/d3/` 02–04) |
| Dig | Converge Show, Leave · SeamWise, **Execute 09** (05–08), Task-Spec Show, **Execute 10** (09), **Execute Gold** (10–12), Task-Mesh seed, Thursday queue |
| Debrief | In hand, Research (`run/d3/13`), Next, silent Tomorrow |

Type 01 **steel thread** tonight: leftover emit if no Parquet, then dlt
register → Bronze → Silver → Gold → golden-match. Types `02`–`05` wait for
Thursday. Unsigned lakehouse sign → skip Execute 10–Gold.

Staff: [`run/d3/README.md`](../run/d3/README.md).

---

## Method manuals vs week papers

Leave the Night HUD to teach a kit; **return** to the numbered beat. Do not
paste Pass 3 or Pass 5 execute from inside the kit.

| Need | Open |
|---|---|
| What is Converge / ASD / the boot arc | this folder (`cvg-…`, `asd-…`, `boot-…`) |
| SeamWise internals | [`seamwise.html`](seamwise.html) |
| Task-Spec internals | [`task-spec.html`](task-spec.html) |
| BRD, tech-spec, ADRs, seams, the sign, Task-Specs | [`docs/`](../docs/README.md) |
| Independence, type map, golden-match | [`plans/modern.md`](../plans/modern.md) |

`wrkp-dark-factory.html` is the long workshop. `yt-agentic-engineering.html`
is the Portuguese talk. Neither replaces Night 5.

---

## Driving a follow-along deck

| Key | Does |
|---|---|
| `→` `↓` `Space` `PageDown` | next slide |
| `←` `↑` `PageUp` | previous |
| `Home` / `End` | first / last |

Dots on the right edge are clickable. The bar across the top is scroll
progress. Slides snap, so a trackpad flick moves exactly one.

`asd-agentic-loop.html` is a **scroll page** (anchor nav, Print / save as
PDF). `boot-…` and `cvg-…` are **print-page** slides (fixed 1000×1414),
not the HUD snap deck.

---

## House rules for editing

- **One file per deck.** Styles, markup and script live together — no imports.
- **Every number is traceable.** Amounts, byte offsets and verdicts come from
  `contracts/`, `spec/` or `evidence/`. If it is on a slide, it is in the repo.
- **Hands-On is one mold.** Clone Day 1 Execute 01–04: chip, `run/dN/` path,
  `.req` beat tiles, look-up / do not. Show slides teach; they do not invent a
  local “beat 01”. Point at `run/dN/NN`. Night 1: six boards. Night 2: five.
  Night 3: four. Research is Close, not a Hands-On badge.
- **Each Show slide shows its information differently.** Flow, annotated artifact,
  diff, matrix, gauges — repeating a mechanism is a smell. The Hands-On boards
  are the exception: they must look the same.
- **Namespace new components.** Two decks merged into this one already collided
  on `.mac`; the second set became `.cmac`. Check before adding a class.
- **Cut HTML blocks by their own closing tag,** not the next `</div>`. Getting
  this wrong once pushed 5 slides outside `.deck` and the counter read `02`.

The Day 1 deck uses 35 files from [`../assets/`](../assets/).
