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
| **Follow-along deck** | Snap slides, HUD, Hands-On boards. One Night. | `d1-…`, `d2-…` (Days 3–5 not built) |
| **Method / reference** | Manual or workshop. Teach the kit, not the clock. | `cvg-…`, `asd-…`, `boot-…`, `wrkp-…`, `yt-…` |

If a night’s HTML and [`run/dN/`](../run/) disagree, **agenda wins on
scope**; **run wins on the clock**. Do not invent a Pass the brief did
not authorize. Type `06` is not in `spec/` until Friday.

## What’s in this folder

| File | Kind | What it is | When you open it |
| --- | --- | --- | --- |
| [`d1-archaeologist.html`](d1-archaeologist.html) | Night 1 deck | Onboard + Archaeologist. **44 slides**, six blocks, HUD `01`–`44`. Pass **0–1** only. **Live.** | Night 1. Staff: [`run/d1/`](../run/d1/README.md) |
| [`d2-translator.html`](d2-translator-java2py.html) | Night 2 deck | Translator · java2py. **34 slides**, six blocks, five Hands-On boards (slices a–e). Identify by `data-act-name`. Scope: [`agenda/d2.md`](../agenda/d2.md). Staff: [`run/d2/`](../run/d2/README.md) | Night 2. **Live.** |
| [`seamwise.html`](seamwise.html) | Method kit | Seamwise internals. Night 2 **Leave · Seamwise** parks here, then returns to Execute 07–10 | Pass 3 kit. Not the Night clock |
| Days 3–5 | — | Constructor / Orchestrator / Dark Factory nights. **Not in this folder.** | Build from [`agenda/d3.md`](../agenda/d3.md)–[`d5.md`](../agenda/d5.md). Staff still stubs: [`run/d3.md`](../run/d3.md) … |
| [`cvg-aut-systems-spine-steps.html`](cvg-aut-systems-spine-steps.html) | Method manual | Converge spine — nine passes, two phases, one human barrier. **36 slides**, print-page layout. v7 · Converge 0.2.0 | When the room needs the kit, not the Night. Week papers: [`docs/`](../docs/README.md) |
| [`asd-agentic-loop.html`](asd-agentic-loop.html) | Method manual | ASD — the Agentic Loop. Scroll document, **12 sections** (not a HUD deck): five layers, hop map, where Converge sits | Doctrine. Print/PDF from the page |
| [`boot-uc-northwind-pay-edp-oss.html`](boot-uc-northwind-pay-edp-oss.html) | Method manual | Bootcamp reference — case framing, Shapiro ladder, the week arc. **19 slides**, print-page layout | Framing before or beside Night 1. Not the follow-along |
| [`wrkp-dark-factory.html`](wrkp-dark-factory.html) | Workshop | Dark Factory Operation. **83 slides**. Broader workshop, not Night 5’s sealed Type `06` run | Context / seed. Night 5 clock is still [`agenda/d5.md`](../agenda/d5.md) |
| [`yt-agentic-engineering.html`](yt-agentic-engineering.html) | Talk | _Engenharia Agêntica_ (pt-BR). **44 slides**. Public talk, not a bootcamp night | Outreach. Do not drive a Night from it |

**Live this week:** Night 1 HTML (44) and Night 2 HTML (34). **Not built:**
Days 3–5 HTML.

Night 1 is Capture + Intent only. Night 2 **recaps** 0–1, **Binds** the
Agent Harness, then Structure → Consensus → one Task-Spec leaf. Mesh is
Show. Factory 6–8 is Day 4. No `modern/` required Tuesday.
One Night — no morning / afternoon split.

---

## Night 1 · how the live deck is laid out

[`d1-archaeologist.html`](d1-archaeologist.html) — one file, **44 slides,
six blocks**. The block name shows in the HUD pill bottom-right, and it
only changes at a block boundary.

| Block | Slides | Mode |
|---|---|---|
| Opening | 1 | title — the two seats, the contract |
| Stage | 7 | presentation, keyboards down |
| Craft | 6 | teaching + Hands-On A (01–04) |
| Floor | 9 | teaching, Hands-On B (05–09), MATCHED look-up |
| Dig | 14 | roles, estate, Show then Hands-On C–F (10–16) |
| Debrief | 7 | truths, receipts, Research (17), Next, silent Tomorrow |

Every block opens with a divider slide. HUD `01`–`44`.

### Hands-On vs Show

Six Hands-On boards only (slices A–F). Show slides teach; they do not wear
the Hands On badge. Dig sandwiches:

| HUD | Show | Then Hands-On |
|---|---|---|
| 32 → 33 | Second Brain (nine packs, whole drop) | Execute 12 |
| 34 → 35 | OntoLayer · the map | Execute 13 (`ontology-ask-sql` then `ontology-ask`) |
| 36 → 37 | Converge · the spine (0–1 tonight) | Execute 14–16 |

Brain handout: [`brain/notebooklm/northwind-pay-brain.zip`](../brain/notebooklm/northwind-pay-brain.zip).
Unzip, upload the **nine** `.md` files — not the zip. Days 2–5 query this
same notebook. Type `06` is not in it.

Close is not a seventh Hands-On: Research (42) → Next (43) → silent Tomorrow (44).

Staff clock: [`run/d1/README.md`](../run/d1/README.md) — slices A–F, then 17.

## Night 2 · java2py

[`d2-translator.html`](d2-translator-java2py.html) — **34 slides,
six blocks**. Identify by `data-act-name` (Stage/Craft extras shift HUD integers).

| Block | Mode |
|---|---|
| Opening | title |
| Stage | Recap Shows, Execute 01–02, then lecture (SWE, java2py, ingest) |
| Craft | Harness Shows, Execute 03–04 |
| Floor | Query Shows, Execute 05–06 |
| Dig | Converge Show, Leave · Seamwise (`seamwise.html`), Execute 07–10, Task-Spec Show, Execute 11, Task-Mesh Show |
| Debrief | In hand, Research 12, Next, silent Tomorrow |

Five Hands-On boards only (slices a–e). Research is Close, not a sixth board.
Staff: [`run/d2/README.md`](../run/d2/README.md) — 12 beats. The old `d2-translator.html` HUD is gone from the tree.

## Method manuals vs week papers

`cvg-…`, `asd-…`, and `boot-…` used to sit under `docs/`. They moved
here because they are **slides**, not the week’s signed artifacts.

| Need | Open |
|---|---|
| What is Converge / ASD / the boot arc | this folder |
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

## House rules for editing

- **One file per deck.** Styles, markup and script live together — no imports.
- **Every number is traceable.** Amounts, byte offsets and verdicts come from
  `contracts/`, `spec/` or `evidence/`. If it is on a slide, it is in the repo.
- **Hands-On is one mold.** Six boards only. Clone Execute 01–04: chip,
  `run/dN/` path, `.req` beat tiles, look-up / do not. Show slides teach;
  they do not invent a local “beat 01”. Point at `run/dN/NN`.
- **Each Show slide shows its information differently.** Flow, annotated artifact,
  diff, matrix, gauges — repeating a mechanism is a smell. The Hands-On boards
  are the exception: they must look the same.
- **Namespace new components.** Two decks merged into this one already collided
  on `.mac`; the second set became `.cmac`. Check before adding a class.
- **Cut HTML blocks by their own closing tag,** not the next `</div>`. Getting
  this wrong once pushed 5 slides outside `.deck` and the counter read `02`.

The Day 1 deck uses 35 files from [`../assets/`](../assets/).
