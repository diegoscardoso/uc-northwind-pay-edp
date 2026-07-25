# Dark Factory Operation — Master Content & Run of Show

> **Purpose.** The single source of truth for the workshop: the run of
> show (act order, durations, gates) *and* the content each act draws
> from (beats, key lines, slide topics, assets, numbers, sources).
>
> **Internal — do not publish with the OSS repo.**
>
> **Supersedes** `docs/workshop-run-of-show-v1.md` (Run of Show v2) and
> `docs/content.md` (the standalone master content document), which were
> merged into this file. The operator cheat-sheet
> [`demo.md`](demo.md)
> stays separate: it holds the verified commands and their real output
> for Acts 3A/3B. This document is the narrative; that one is the
> keyboard.
>
> Lives beside the deck it feeds: `presentation/workshop-dark-factory.html`
> and `presentation/images/`. The older
> `presentation/tmpl-agentic-engineering.html` is now the **design-system
> template only** — it is never presented; it is the source of the tokens,
> components, chrome, and runtime the workshop deck inherits.

---

## 0. Latest state — read before touching any slide

**The Act 3B reveal changed on 2026-07-25.** Every earlier draft scripted
the AHA as *"it's the legacy — a silent defect summing wrong cents for
years; the factory indicted the oracle."*

**That is not what this system found.** The golden-match closed with
**zero** `CONFIRMED_LEGACY_DEFECT`. The legacy baseline is correct on all
five types. What exists is five **source-system** defects — the upstream
declared a total that its own detail rows contradict:

| Batch | Type | Source declared | Independently computed |
|---|---|---|---|
| `B202607230000004` | `01` | `173.44` | `173.45` |
| `B202607230000105` | `02` | `173.44` | `173.45` |
| `B202607230000205` | `03` | `198.49` | `198.50` |
| `B202607230000305` | `04` | `999.99` | `1000.00` |
| `B202607230000405` | `05` | `0.99` (fee) | `1.00` |

Delivering the old line would claim a defect the evidence does not
support, in front of an audience who may later read the repo. The true
reveal is stronger: the audience watches the machine **refuse to
conclude** when you take its evidence away.

**The AHA, said aloud:**

> "Three independent implementations — Java, SQL, and Python — each
> computed `173.45`. The source declared `173.44`. **Nobody corrected
> it.** Every system preserved the lie exactly as written, refused the
> batch, and kept the other batches running. The one cent never reached
> the database. And the factory can prove *who* lied, without ever
> showing you a card number."

**Consequences that ripple through this document**
- The Act 3B beats are rewritten (see Act 3B below).
- The "planted legacy defect" rehearsal item is **closed as
  not-needed** — the real finding replaced it.
- The demo type question is **settled**: Type 01, batch
  `B202607230000004`, for the beat-by-beat; all five types at the close.
- Act 4's KurvPay scar story is unaffected and still true — there, the
  *golden itself* was defective. The doctrine line **"the golden is
  evidence, not truth"** survives both stories.

## 0.1 Deck build state — updated 2026-07-25

**The deck is `presentation/workshop-dark-factory.html`.** It inherits the
design system, navigation chrome, and runtime JS from
`tmpl-agentic-engineering.html` byte-for-byte; only the title, meta,
favicon hue, and slide counter were changed. Every act authored into it
must reuse the existing components (`card`, `callout`, `stat-cell`,
`aud-cell`, `nv-card`, `pill`, `kicker`, `slide--hands`, `slide--silent`)
rather than inventing new ones.

**Slide 25 — "The three questions" (added 2026-07-25).** The last teaching
beat of Act 1, immediately before the "green is not true" closer. Osmani's
three diagnostic questions — *how quickly will we know we're wrong · how
cleanly can we undo · what would prove we're right* — rendered as a
**verification instrument panel**, a visual register the deck did not have:
three bays, each with a status LED reading `NO SIGNAL`, the failure answer lit
and the correct answer dimmed. Hover or tab a bay and it powers on — LED flips
to `ANSWERED`, the failure fades, the standard illuminates. New component
`.vq-*` in the design system (bay, LED, readout rows, scanline, corner
brackets); reuses `.callout`, `.pill`, `.pyr-hint` and the gold governance
accent. Verified at 1600×900 and 1366×768: no clipping, three columns hold,
keyboard-reachable, honours `prefers-reduced-motion`.

> **This slide creates an obligation.** Each bay is stamped *"answered live in
> Act 3B"* and the closing callout promises the room will see the panel again
> "filled in by the machine, not by me." Act 3B must therefore land the same
> three bays with the run's real answers — beat 2 (the gates) answers Q1,
> beat 5 (containment) answers Q2, beats 7–8 (withhold + determinism) answer
> Q3. If that callback is cut, cut the promise on slide 25 too.

**Built: all 80 slides — Act 0 (8), Act 1 (18), Act 2 (12), Break (1),
Act 3A (7), Act 3B (15), Act 4 (11), Act 5 (8). Exactly one `.todo` token
remains, deliberately: the pre-sale price on slide 78, blocked on open
item 4.** Each act's slide-by-slide table and beats live in its own section
below; only Act 0 is itemised here.

| # | Slide | State |
|---|---|---|
| 01 | Title — "The factory that runs with the lights off" | done |
| 02 | Act 0 divider — The Selection Mechanism | done |
| 03 | Who is in this room — 561 / 249 / 44% | done · real data |
| 04 | Where this room said it stands — pool × room | done · real data |
| 05 | The frame — "it is the one that scored you" | done |
| 06 | The promise | done |
| 07 | The honesty contract | done |
| 08 | The agenda | done |
| 09–26 | **Act 1 — 18 slides** | done · see the Act 1 section |
| 27–38 | **Act 2 — 12 slides** | done · see the Act 2 section |
| 39 | **Break** — the question, alone | done |
| 40–46 | **Act 3A — 7 slides** | done · see the Act 3A section |
| 47–61 | **Act 3B — 15 slides** | done · see the Act 3B section |
| 62–72 | **Act 4 — 11 slides** | done · see the Act 4 section |
| 73–80 | **Act 5 — 8 slides** | done · see the Act 5 section |

**Assets.** Four cinematic backgrounds generated with Higgsfield
(`soul_location`, 16:9 → 2048×1152, downsampled to the repo's `*-opt.jpg`
convention, ~120–150 KB each):
`images/gen/df-hero-opt.jpg` (lights-out factory floor),
`df-ato0-opt.jpg` (a few violet nodes lit among thousands of dim ones —
the selection mechanism with no words), `df-promessa-opt.jpg` (one machine
working alone under a single violet light), and `df-ato1-opt.jpg` (five
ascending blue light strips in a dark machine hall — the five layers and
the ruler, with no words). Note: `soul_location` ignores `width`/`height`
and defaults to 3:4 — pass `aspect_ratio: "16:9"` or the frame comes back
portrait.

**Act 2 backgrounds (2026-07-25), same pipeline:** `df-ato2-opt.jpg` (an
industrial stairwell descending into blackness under one red lamp — the
descent), `df-legacy-opt.jpg` (a single sealed cabinet alone in an empty
hall, one red indicator still lit — the machine nobody opens),
`df-risco-opt.jpg` (an analogue console reading perfectly calm above a
flooded, mirror-still floor — working and being wrong), `df-oraculo-opt.jpg`
(a blank monolith on a plinth under one hard shaft of light — the oracle).

> **Warning for future image work.** `soul_location` will sometimes bake a
> *garbled pseudo-text caption* into the frame — invented letterforms that
> look like a title card, usually in the exact left-hand area reserved for
> typography. Two Act 2 images came back this way and were regenerated. The
> phrase that worked: enumerate the ban (*"no lettering, no signage, no
> title card, no watermark, no caption, no glyphs, no numbers — zero text of
> any kind"*) and avoid nouns that invite writing (**inscriptions**,
> **labels**, **gauges reading X**). **Always eyeball the render before
> committing it**; gibberish text on a projector is the single most
> expensive AI tell in a deck like this.

**Act 3 backgrounds (2026-07-25):** `df-ato3a-opt.jpg` (a cyan ignition flare
at the end of a long machine aisle, robot arms just catching the light — the
moment of ignition), `df-ato3b-opt.jpg` (a production hall running at speed
in the dark, lit only by green status indicators and their reflections — no
human anywhere), `df-gates-opt.jpg` (a row of heavy gates standing wide open
in a dark corridor, amber light behind them — gates that cannot fail). All
three came back clean on the first attempt with the enumerated no-text ban.

**Act 4 runs deliberately image-light.** The Higgsfield connector was
offline when Act 4 was built, and on reflection that was the right constraint:
Act 4 is the *receipts* act, and it should read like evidence rather than
atmosphere. Only the divider carries a photograph (`darkfactory-bg-opt.jpg`,
reused from Act 1 slide 24 so the flywheel promise and its payment share an
image). Slide 70 instead uses the template's **spinning concentric-ring
mandala** — pure SVG, seven rings at seven speeds and directions, recoloured
to gold — behind the doctrine line. That was one of only two template patterns
the deck had never used. If you want photographs for Act 4 later, slides 63,
69 and 72 are the candidates.

**New design-system components (2026-07-25), appended to the style block:**
- `.fog` / `.fog-inner` / `.fog-seal` — the **silhouette treatment**. A real
  artefact is rendered inside and then blurred and hatched, with a seal
  reading “interior closed” over it. Used for Task-Spec (slide 44) and for
  all nine Converge boxes (slide 45). The name-never-open rule stops being a
  spoken caveat and becomes *visible*: the audience can see there is
  something in the box and that it is deliberately shut.
- `.vq-bay--on` — the powered-on state of the Act 1 instrument panel,
  applied permanently so slide 58 can show the same three bays with the
  run's real answers. Mirrors every `:hover` declaration; no JS.
- `.wh-row` / `.wh-ch` / `.wh-verd` — the **withhold matrix** on slide 54:
  one row per removed evidence channel, the withheld one struck through in
  red, the verdict on the right. Five rows carry the whole money shot.
- `.lg-*` — the **transformation ledger**, built for Act 4 slide 65 when the
  first version of that slide came out looking like a spreadsheet. Each row
  carries the metric in display serif with a mono descriptor beneath it, the
  legacy value **struck through in red** (with its qualifier outside the
  strike, so the rule never crosses the word), a pair of micro-bars whose
  lengths *are* the measured ratio, the new value, and the gain as a solid
  chip. Two hero rows (42× and ~98%) get filled chips and a halo; the middle
  four get outline chips. The "after" bar is always green regardless of the
  row's category colour, with `min-width:7px` so a 1% ratio still reads as a
  deliberate mark rather than as nothing.
  **It also carries the deck's first height-aware media query**
  (`@media (max-height: 820px)`): at 1366×768 the header sub-labels, the
  per-row legends and one trailing clause are shed and the rows tighten, which
  takes the slide from 92px of overflow to fitting with 11px to spare. The
  1600×900 rendering is untouched. If you add rows to this table, re-measure
  both resolutions — six is what fits.

**Act 0 data — landed 2026-07-25.** Pulled from the `applications` export
(`product = dark-factory-v1`, 703 submissions from 561 distinct people,
142 repeat attempts). Deduplicated by e-mail; a person counts as selected
if any of their submissions was approved. All nine `.todo` placeholders
are gone and the bar widths carry the real percentages. Numbers are a
**snapshot** — the slide-03 callout tells the operator to re-run the query
live or drop the word "live". The full figures are in §5.

**Slide 04 was redesigned, not just filled.** The real distribution broke
the original design: the form only ever offered **four rungs (L1–L4)**, so
L0 and L5 bars at 0% would have implied a choice nobody was given. And the
room is not "middle-heavy" — the gate admitted **nobody below L3**. The
slide is now two cards side by side, pool × room, which makes the selection
mechanism visible instead of merely asserted. It is a stronger Act 0 beat
and it sets up Act 1 slide 20 and the Act 5 close.

**Act 1 was rebuilt and expanded on 2026-07-25** — from 9 slides to 17,
by folding in five concepts from the design-system template and
verifying every external claim against its primary source. That pass
also caught a **naming error carried by every earlier draft**: the
autonomy levels were labelled with our paraphrases, not Dan Shapiro's
actual level names. See the correction table in the Act 1 section — it
changes what is said out loud on stage.

**Geometry reuse.** The rings SVG (slide 15), the orbital loop (18), the
flywheel (24) and the autonomy curve (21) reuse the template's exact
geometry — same `viewBox`, radii, ring classes and orbit insets — with
all copy re-authored in English. That is deliberate: the template's
`hr-ring`, `ring-spin`, `df-card` and `sdd-glow` animations are already
in the deck's inherited CSS, so nothing new had to be invented and the
motion matches the rest of the deck.

## 0.2 Deck conventions — binding for every act

1. **Language: English, end-to-end.** Slide copy, headings, tags, act
   names, code comments, and the HUD are all English. `<html lang="en">`.
   No Portuguese survives in any presented string. (This reverses the
   earlier pt-BR assumption inherited from the template.)
2. **Naming.** The operation is **"Dark Factory Operation"** — that exact
   string is the hero badge on slide 01 and the canonical name everywhere.
   Never "Operação Dark Factory".
3. **Tags.** Every tag, chip, and badge uses the `.pill` component — solid
   fill, black text, mono uppercase, diamond `◆` prefix — matching the
   slide-01 hero badge. Do not use outline/bracket-style `[ LABEL ]` tags.
4. **Act colour semantics.** Act 0 purple · Act 1 accent-blue · Act 2 red ·
   Act 3A cyan · Act 3B green · Act 4 gold · Act 5 purple. The colour
   carries the argument; it is not decoration.
5. **Every slide declares its act** via `data-act`, `data-act-name`, and
   `data-accent` on the `<section>`. The presenter HUD reads these — a
   slide without them shows a blank act label.
6. **Sourced numbers.** Any number on screen carries its source
   (`.sc-src` / `.aud-src`) or it does not go on screen.
7. **Time-of-day words are not settled.** The schedule conflict (open item
   below) is still open, so slides currently mix "today" and "tonight".
   Prefer duration-relative phrasing ("in about two hours", "before we
   finish") until the schedule lands, then sweep the whole deck once.
8. **Colour continuity across acts.** The autonomy rungs keep the same
   colours everywhere they appear — L1 accent-blue · L2 cyan · L3 gold ·
   L4 purple · L5 green. Act 0 slide 04 and Act 1 slide 15 must agree, and
   Act 5's recap must too.

## 1. Governing rules

1. **Main intent.** The workshop is a 360° tease of the Bootcamp. Show
   the factory from outside, running for real; never open the machine.
   Every act builds desire for the "how" — the Bootcamp is the only
   place that delivers it.
2. **Stage rule — name, never open.** Converge and Task-Spec are the
   named stars. On screen they appear as silhouettes: what enters, what
   exits, what they guarantee. Fog inside every box. Never spoken:
   Fork, HMAC, safe-to-delegate, the contents of the 8 passes.
3. **Honesty doctrine.** The loop converges to green evals, not to
   truth. Say the limits out loud — with a senior room, honesty is the
   conversion engine.
4. **Claim discipline (hard limits).** Do not say, in any act:
   - "the factory found a legacy defect" — it did not; there are zero;
   - "the agent wrote all this unsupervised with no corrections" — the
     run was autonomous, but it found and fixed four vacuous gates
     along the way, which is the better story anyway. **Six gates were
     vacuous in total: four caught by the run, two caught afterwards by a
     human reading code.** Both numbers are true and they measure different
     things — say which one you mean. Act 3B slide 60 states both;
     Act 0 slide 07's "corrected itself four times" refers to the run and
     is correct as written;
   - "production-ready" or "CI-ready" — `plans/modern.md` forbids
     claiming either from local proof, and no CI exists;
   - "modern replaces legacy" — legacy is the frozen oracle; modern is
     an independent second implementation whose whole purpose is to
     disagree detectably.
5. **Privacy on stage.** Evidence shown from the legacy run must be
   privacy-safe and allowlisted. Type 01 may show its approved safe
   transaction reference and derived controls; never PAN, CPF, or a raw
   row. Worker packets are internally reconciled but scenario-unscored;
   the independent acceptance harness binds canonical identities to
   expected outcomes.
6. **Project-state boundary.** The legacy oracle was live-verified on
   2026-07-24: 25 canonical outcomes (15 success, 10 quarantine), four
   exact-batch restart seams, one integrity quarantine, and one forced
   oracle mismatch; terminal cache and recovery-journal state empty.
   The Dark Factory demonstrated at the workshop is new work on top of
   this proven baseline.

## 2. The storytelling spine

**The through-line question** (on screen from Act 2 to the end):

> "Who guarantees the new number matches the old one — cent by cent?"

**The twist.** When the answer arrives (Act 3B), it points somewhere
nobody expected: neither implementation was wrong. **The upstream source
lied by one cent** — and not one of the three systems silently corrected
it. They preserved the lie, refused the batch, and named the liar.

**The real-world echo** (Act 4): KurvPay's stalled types prove the same
doctrine with real money — there the *golden* was the defective party.
Same lesson from the other direction: *the golden is evidence, not
truth.*

**Recurring motifs** (plant early, harvest late):
- *The cent.* Money is the unit of truth all night.
- *Green ≠ true.* Planted in Act 1, detonated at the Act 3B AHA,
  echoed in the Act 5 close.
- *Refusing to conclude.* A system that declines beats a system that
  guesses with a confidence score.
- *Watching vs. mastering.* The emotional gap the offer resolves.
- *The room as first demo.* The scoring system of Act 0 is the theme
  in miniature.

**The autonomy curve of the night.** The room doesn't gain autonomy
step by step (that's the Semana/Bootcamp); it *witnesses* total
autonomy once, in Act 3, and leaves wanting to build it.

## 3. The act structure

| # | Act | Duration | Job in the story |
|---|-----|----------|------------------|
| 0 | The Scoring Mechanism | 15 min | Belonging — "the first agentic system tonight is the one that scored you" |
| 1 | Fundamentals (not-101) | 45 min | Vocabulary + autonomy ladder; only what makes Act 3 legible |
| 2 | NorthWind Pay | 40 min | Legacy, works-but-wrong risk, BRD read-along, frozen budget, the question |
| — | Break | 10 min | Question stays on screen |
| 3A | The Anatomy (ignition first) | 25 min | Fire the factory; teach the machine over live telemetry |
| 3B | Lights-Off Execution | 45 min | The run: golden-match, divergence, the AHA, loop closes |
| 4 | KurvPay — the receipts | 20 min | Real numbers + stalled-types scar story; monetization lands here |
| 5 | The Bridge | 30 min | The gap, Monday workflows, Factory Ladder offer, honest close |

Total 3h50 + 10 min slack.

---

## Act 0 — The Scoring Mechanism (15 min)

**Objective.** The room recognizes itself as selected, understands what
it will witness, and buys the honesty contract.

**Beats**
1. Live Supabase pull on screen: applicants vs. selected, the
   Shapiro-level distribution of the room. A qualified room, not a
   generic audience.
2. The frame that beats flattery: "the first agentic system you see
   tonight is the one that scored you" — a system evaluating against a
   criterion is literally the theme of the event.
3. Celebrate the selected without humiliating the rest (the funnel
   repositions non-approved people; their colleagues are in the room).
4. The promise: a factory will migrate a legacy financial system by
   itself and catch a money error that hid in plain sight — nobody
   types code in the loop.
5. The honesty contract + brief agenda of the night.

**Slide/screen topics**
- Live data screen (Supabase query result, styled)
- Applicant distribution chart (Shapiro levels)
- The promise, one sentence, huge type
- Agenda of the night (acts as chapters)

**Key lines**
- "You were scored by a system against a criterion. That is literally
  what you'll watch a factory do with money tonight."
- "We won't sell magic. We'll show what's real and say exactly where
  the limits are."

**Assets/sources.** Supabase scoring data (live); qualification-funnel
design in `docs/wrksp-secret-dark-factory-v1.pdf` §3–4.

**Gate.** The room knows what it will witness and bought the contract.

---

## Act 1 — Fundamentals, not-101 (45 min)

**Objective.** Give the room exactly the vocabulary that makes Act 3
legible — nothing more. Best practices appear later as live-run
callbacks, not slides.

**Built: 17 slides (09–25), 2026-07-25.** Expanded from the first
9-slide draft by folding in five concepts from the design-system
template (its slides 20–24: the four-rung ladder, the concentric rings,
the closed loop, the calibrated-autonomy curve, the factory flywheel),
all re-authored in English with sourced detail. The act now has a spine:
**four rungs → the anatomy → the ruler → the evidence.**

| # | Slide | Shape |
|---|---|---|
| 09 | Act 1 divider — Fundamentals, not a 101 | poster over `df-ato1` |
| 10 | Three names, three questions — Loop · Converge · ASD | 3 cards |
| 11 | The four rungs: prompt → context → harness → agentic | `.ladder` staircase |
| 12 | The five layers — and who is allowed to decide | 5 rows + 2 callouts |
| 13 | The hop map — the model never invokes anything | flow, mono |
| 14 | A whole agent in 40 lines — the receipt | terminal |
| 15 | The architecture, in rings | full-bleed SVG |
| 16 | Context engineering — the attention budget, 4 levers | 3 + 4 cards |
| 17 | Harness engineering — what is in it, and MCP placed | 6 cards + 2 callouts |
| 18 | How the rings close the loop | orbital diagram |
| 19 | Belief × reality — six misconceptions | `.guard-card` ×6 |
| 20 | The autonomy ruler L0–L5 | 6-rung staircase |
| 21 | Autonomy is calibrated, not switched | curve + rules + anti-pattern |
| 22 | The evidence, both directions — METR × StrongDM | 2 cards |
| 23 | L3 is a trap, L5 is the target | 2 cards |
| 24 | The factory flywheel | orbital over `darkfactory-bg` |
| 25 | The seed — “green evals, not truth” | silent |

### ⚠ Naming correction — 2026-07-25

**The level names in every earlier draft were wrong.** The bootcamp PDF
(p.17) and the template both label the six levels with the *car
analogy* — “Manual / lane-keeping / autopilot / Waymo with a driver /
robotaxi / dark factory” — and with role descriptions (“you became a
manager”, “you became a PM”). Those are our paraphrases, not Shapiro's
level names. **His actual names are:**

| Level | Shapiro's name | Car analogy (his framing device) |
|---|---|---|
| L0 | Spicy autocomplete | the car has cruise control |
| L1 | The coding intern | lane-keeping |
| L2 | The junior developer | autopilot on the motorway |
| L3 | The developer | a Waymo with a safety driver |
| L4 | The engineering team | a robotaxi |
| L5 | The dark software factory | not a car any more |

The deck now carries **both** — his name as the rung title, the car
analogy as the subtitle — which is the honest rendering and reads better
on stage. Also corrected: the essay is **“The Five Levels: from Spicy
Autocomplete to the Dark Factory,” danshapiro.com, January 2026** (Dan
Shapiro is CEO of Glowforge). The ~90% figure attaches to **L2**, not to
a vague middle. Do not say “L1 delegated tasks” or “L2 pairing” on
stage — those were ours.

**Beats**
1. **Three names, three questions.** The Agentic Loop — how does a
   running system work? Converge — how does it deliver a project?
   ASD — how do you build the machine itself? (First appearance of the
   stars: names only.)
2. **The four rungs.** Prompt engineering (the right sentence) →
   context engineering (the right information) → harness engineering
   (the right system) → agentic engineering (the whole discipline, in
   an autonomous loop). Each is a named discipline with published
   literature; each assumes the one below already works.
3. **The five layers.** L1 Model (pure text function, stateless) ·
   L2 Harness (a normal program: owns the API key, the while-loop,
   permissions) · L3 Tools (schemas offered as text) · L4 Environment
   (filesystem, git, databases, CLIs) · L5 Referee (deterministic
   gates and evals; exit 0/1 decides — the model's opinion is never
   consulted). *The model thinks, the harness acts, the referee
   judges* — only text and exit codes ever cross between them. Land
   the formula the field converged on: **Agent = Model + Harness.**
4. **The hop map + the receipt.** The model never invokes anything — it
   asks (emits a request blob); the harness calls. The while-loop wraps
   hops 1–4; the referee judges outside them. Then the forty-line demo
   where the model is scripted, so only the machinery is visible.
5. **The architecture, in rings.** Model at the core; six rings around
   it — prompt/spec, context, harness, loop, eval, governance. Take a
   ring away, lose a guarantee. Say the bridge out loud: *the five
   layers tell you who decides; the rings tell you what to build.*
6. **Context engineering, up close.** A finite attention budget ·
   context rot (quality degrades before the window fills) · and the
   four levers: just-in-time retrieval, compaction, notes on disk,
   sub-agent isolation. This is why a four-hour run does not drown.
7. **Harness engineering, up close.** The six parts you own:
   instructions, capability, containment, orchestration, **verification**,
   observability. Place MCP correctly — plumbing, three primitives,
   Linux Foundation since Dec 2025. Land the punchline: *the model got
   commoditized; the harness did not.*
8. **The closed loop.** Intent → context → harness → loop → eval →
   delivery, with the engines interchangeable in the middle. The
   reviewer is deliberately from a different vendor than the writer.
9. **The misconception table** (senior-room hook):
   - "The model runs commands" → the harness runs them
   - "The model remembers our conversation" → the transcript is re-sent
     in full every call
   - "The model knows my tools" → schemas are injected into every
     prompt; remove them, knowledge gone
   - "An agent is a special model" → agent = model + while-loop + tools
   - "MCP is a protocol models speak" → the model just sees more tool
     schemas
   - "Autonomy means a smarter model" → autonomy = a scheduler replaces
     the trigger and a referee replaces judgment
10. **The autonomy ruler** (Shapiro L0→L5 on the NHTSA frame — use his
    names, see the correction above). Place the room honestly: the gate
    admitted nobody below L3, and 70% of the room is on L3.
11. **Autonomy is calibrated.** Climb a level when the work is
    reversible, small-blast-radius, and covered by an eval that has
    actually failed something. Drop a level the moment it is
    irreversible, wide, or the eval has never said no. Goals,
    permissions and accountability stay human at every level. The
    anti-pattern is **the switch**.
12. **The evidence, both directions.** METR's RCT for the trap
    (believed +20%, measured −19%) and StrongDM for the destination
    (three engineers, two rules, an agent shipped as a spec with zero
    code). Neither number is mine — that is the point.
13. **The flywheel.** Runs leave lessons; lessons become memory; a
    recurring lesson is promoted to a skill; better skills make better
    agents. This is the one thing L5 does that L4 cannot. Forward-links
    to Act 4's measured ~55–60 lessons → 4 skills.
14. Close on the destination and the seed: **the loop converges to
    green evals, not to truth.**

**Key lines**
- "The model never invokes anything. It asks; the harness calls."
- "Agent = model + harness. If you are not the model, you are the
  harness."
- "Filling the window is not using it."
- "The model got commoditized. The harness did not."
- "A harness whose only completion signal is 'done' has no verification
  layer — it has a suggestion box."
- "They felt 20% faster. They were 19% slower. Feeling is not a metric."
- "Validation replaces code review."
- "Autonomy is earned with evidence — never decreed with a button."
- "Eval is the ring that frees you — without it you never trust
  autonomy."
- "Most of the market is parked at L3, reviewing diffs, feeling it got
  worse."
- "The loop converges to green evals, not to truth."

**Assets/sources.** `docs/asd-agentic-loop-v1.0.html` (five layers,
hop map, misconceptions, two seats); `presentation/tmpl-agentic-engineering.html`
(the rings SVG, the orbital loop, the autonomy curve — geometry reused
verbatim, all copy re-authored). External, all cited on-slide:
- Dan Shapiro · “The Five Levels: from Spicy Autocomplete to the Dark
  Factory” · danshapiro.com · Jan 2026 — the ruler
- METR · “Measuring the Impact of AI Tools on Developer Productivity”
  RCT, 2025 · arXiv:2507.09089 — 16 maintainers, 246 tasks, +24%
  forecast / +20% believed / −19% measured
- StrongDM · “Software Factories and the Agentic Moment” · Feb 2026,
  with Simon Willison's write-up — three engineers, two rules, Attractor
  shipped as three markdown files and zero code
- Anthropic · “Effective context engineering for AI agents” · 2025 —
  attention budget, JIT retrieval, compaction, note-taking, sub-agents
- Chroma · “Context Rot” · 2025 — 18 frontier models
- OpenAI · “Harness engineering” · Feb 2026 — “the environment was
  underspecified”
- Böckeler (martinfowler.com) and Osmani on harness engineering —
  *Agent = Model + Harness*
- Model Context Protocol — Anthropic Nov 2024 → Linux Foundation
  Agentic AI Foundation, Dec 2025; primitives Tools / Resources / Prompts
- Anthropic Agent Skills — `SKILL.md` and progressive disclosure
  (discovery → activation → execution), the mechanism behind the flywheel

Converge/Task-Spec silhouette source:
`docs/cvg-aut-systems-spine-steps-v5.pdf`, `docs/task-spec-v3.2.0.pdf`
(updates to come — fold in on arrival).

**Stage discipline for this act.** Everything above is public
literature, so it is all sayable. The named stars stay silhouettes:
Converge appears as “brief in, validated software out” and nothing more;
ASD is named once and deferred to Act 5. Never spoken: Fork, HMAC,
safe-to-delegate, the contents of the passes.

**Gate.** The room has the vocabulary, knows where it stands, has seen
that both the trap and the destination are documented by other people,
and L5 is named as tonight's destination.

---

## Act 2 — NorthWind Pay (40 min)

**Objective.** The room understands the legacy, feels the
works-but-wrong risk, and holds the unanswered question.

**Built: 12 slides (27–38), 2026-07-25.** Authored entirely from the
repository — `plans/legacy.md`, `plans/modern.md`, `contracts/types/`, and
the Type 01 fixtures. No external research; this act is repo archaeology.
Three layouts appear here that exist nowhere else in the deck, so Act 2
does not look like Act 1: the **five-column code-proof cards**
(`.unit-card` / `.uc-code`), the **interactive requirement stack**
(`.pyr-step`, the deck's only click-to-expand slide), and the
**logo-tile** strip.

| # | Slide | Shape |
|---|---|---|
| 27 | Act 2 divider — NorthWind Pay | poster over `df-ato2` |
| 28 | A processor that works, a pipeline nobody owns | 4 stat-cells over `df-legacy` |
| 29 | Every arrow is an explicit interface | full-width topology SVG |
| 30 | “Just parse the file” — five times, five problems | 5 code-proof cards |
| 31 | One character carries the last digit and the sign | redacted bytes + decode table |
| 32 | “Correct” is four different questions | 4 cards (2×2) |
| 33 | Working and being wrong | poster over `df-risco` + 3 strips |
| 34 | Understand it before you build it — **the BRD** | interactive 6-layer stack |
| 35 | It froze on one question | silent · the through-line |
| 36 | The legacy, with all its defects, is the oracle | poster over `df-oraculo` |
| 37 | The new system is not a replacement | decision-flow SVG |
| 38 | What the factory is going to build tonight | 5 zones + stack + limits |

### Scope note — the modern decision was added deliberately

The original Act 2 beats ended at “the legacy is the oracle.” Slides 37–38
extend that with **the modern decision** — why the new system is an
independent second implementation rather than a rewrite in place, and what
its zones and stack are. This was an explicit instruction (2026-07-25) and
it is the right call: it is a *design decision*, which is Act 2's job
(“understand before you build”), and it sets up Act 3 without opening the
factory. If Act 2 ever runs long, 38 is the slide to cut — 37 carries the
argument on its own.

### Two content rules this act had to solve

1. **No raw row may go on a projector.** §1.5 forbids PAN, CPF and raw
   rows in anything shown. Slide 31 nevertheless has to make the room
   *feel* the bytes. Resolution: show the real header and trailer verbatim,
   show the detail rows with the PAN and CPF spans **blocked out**, and say
   out loud that the redaction is the contract working, not a slide
   decision. The privacy discipline gets demonstrated instead of described,
   which is stronger than either alternative.
2. **“HMAC” is on the never-speak list** (§1.2). The Type 01 privacy
   contract names HMAC-SHA-256 as the tokenization algorithm. The slide and
   the BRD layer therefore say **“a keyed token”** and **“fail closed if
   the key is missing”** — accurate, and it does not spend a word the
   Bootcamp needs. Do not restore the algorithm name on stage.

### The plant that pays off in Act 3B

Slide 31 teaches the COBOL overpunch decode table and lands on *“one
character carries the last digit and the sign — remember this byte.”* It
uses batch `B202607230000001`, the **accepted** batch, whose trailer reads
`…1734E` → `173.45`, correctly declared.

Act 3B's defect batch `B202607230000004` differs from it by **exactly one
character**: the trailer reads `…1734D` → `173.44`. Same fourteen digits,
one byte apart. That is the whole one-cent finding, and the room will be
able to read it unaided because of this slide. **Do not spoil it in Act 2** —
slide 31 must stay on the accepted batch, and the two `.pill` tags at the
bottom right (“remember this byte” / “it comes back in Act 3”) are the only
foreshadowing allowed.

**Beats — a descent into the mine**
1. **The company.** Transactions in; every cycle the core drops 30+ raw
   file types onto SFTP — proprietary positional layouts, COBOL overpunch,
   PII in the clear. The business rules live inside ~300 stored procedures
   and a Java parser whose author left: executable and unreadable at the
   same time. Say plainly that this repository implements **five** of those
   types, end to end.
2. **The machine nobody touches.** Walk the topology left to right and
   name every boundary: system of record → SFTP raw → Java 21 privacy
   boundary → SFTP CSV → PostgreSQL (one transaction) → independent oracle
   → archive or quarantine. The doctrine line is *“every arrow is an
   explicit interface”* — DataGen does not call Java, Java does not write
   PostgreSQL, procedures do not read SFTP. Then the payoff for later:
   **sealed interfaces are what make the system observable from outside
   without being modified.**
3. **Five types, five grammars.** One slide, five code-proof cards: fixed
   width with the sign in the last byte · UTF-8 pipes where the delimiter
   appears inside the data · exactly-240-byte paired segments · one length
   per record type with inherited context · semicolons with decimal commas
   and exact `HALF_UP`. The point is not the formats; it is that **there is
   no shared parser**, five times over, times thirty-plus types.
4. **The craft, and the discipline.** Slide 31 — see the plant above.
5. **Four truth roles.** System of record (what was declared) · source of
   observation (what happened) · source of correctness (what should have
   happened) · executable contract (what was agreed, in Git). No component
   may merge them, and a source-defect scenario **keeps the wrong
   declaration exactly as written**. This is the single most load-bearing
   slide in the act: without it, the Act 3B reveal is just a bug story.
6. **The real risk.** Not downtime — *working and being wrong*. Contrast
   the three cards: an outage costs hours; a plausible-wrong number costs a
   quarter and your credibility; and a test written from the same
   misunderstanding as the code **agrees with the code**. Green means
   consistent, not correct.
7. **The BRD read-along (interactive).** Six layers, five rules each, for
   *one* file type — transport & identity, record grammar, money & sign,
   privacy, controls & reconciliation, terminal behaviour. Click each layer
   and interrogate it together; **this is where the room talks.** Close on
   the uncomfortable line: *“you cannot delegate what you cannot specify.”*
8. **The frozen budget and the question.** 12–18 months, 8–12 developers,
   approved twice, started zero times. It did not die on cost — it froze on
   *“who guarantees the new number matches the old one, cent by cent?”*
   The question goes on screen and stays, including through the break.
9. **The design secret.** The legacy, defects and all, is the oracle —
   frozen, observable, already trusted. And immediately the limit: an
   oracle is **evidence, not truth**. Flag that it gets tested from both
   directions tonight (here, and in Act 4 where the golden itself lied).
10. **The modern decision.** Same contracts, same raw bytes, two
    independent implementations, one golden-match gate. Why not rewrite in
    place: a rewrite that reuses the old logic inherits the old bugs and
    cannot detect them. Why not trust the tests: they pass on the same
    misunderstanding. What it buys: **every disagreement becomes cheap to
    find and expensive to ignore.** Then the zones (restricted raw →
    landing → Bronze → Silver → Gold), the stack, and the claim limits.

**Key lines**
- "The rules are executable and unreadable at the same time."
- "Every arrow is an explicit interface."
- "Five layouts, five grammars, five ways to be wrong about money."
- "One character carries the last digit and the sign."
- "You are watching the privacy boundary work right now."
- "The real risk is not the system going down. It's the system working —
  and being wrong."
- "A test written from the same misunderstanding as the code agrees with
  the code."
- "You cannot delegate what you cannot specify."
- "The legacy, with all its defects, is the oracle."
- "An oracle is evidence, not truth."
- "You need a second implementation — not a second reading of the first
  one."

**Assets/sources.** Everything on these twelve slides traces to the
repository, and each slide carries its source line:
- `plans/legacy.md` — topology, boundary rules, the four truth roles, the
  proof ledgers, and the frozen baseline
- `plans/modern.md` — the independent-second-implementation decision, the
  zone model, the shared boundaries, and the claim limits (no CI, not
  production-ready, modern does not replace legacy)
- `contracts/types/registry.yaml` — the five types and their distinct
  problems
- `contracts/types/01-card-settlement/layout.yaml` — byte offsets, record
  lengths, the overpunch table, cross-record rules
- `contracts/types/01-card-settlement/privacy.yaml` — tokenize/mask rules,
  prohibited outputs, fail-closed behaviour
- `contracts/types/01-card-settlement/reconciliation.yaml` — source/stage/
  operational controls, procedure order, zero count-delta tolerance
- `contracts/types/01-card-settlement/main/valid-minimal.dat` — the real
  bytes on slide 31
- Case framing and the didactic figures (30+ types, ~300 procedures, 4–6
  reconcilers, 12–18 months): `docs/boot-uc-northwind-pay-edp-oss-v2.pdf`.
  **These are labelled “didactic case” on the slide**; the repository
  figures are labelled separately.

**Gate.** Legacy understood, risk felt, question held — and the room knows
why the answer is a second implementation rather than a bigger team.

---

## Break (10 min) — the question stays on screen

**Built: 1 slide (39).** Silent. The through-line question inside a glowing
red frame, the act-marker reading "Break · 10 minutes", and one line
underneath: *"When we come back, a machine answers it. Nobody types code from
here on."* Slide 35 already promised the question would survive the break;
this pays that promise.

---

## Act 3A — The Anatomy, ignition first (25 min)

**Objective.** The room understands the machine that is — at that very
moment — visibly working behind the speaker.

**Built: 7 slides (40–46), 2026-07-25.** Deliberately few. This act's
content is a running terminal and a second screen; the deck is scaffolding
around them, and every slide is designed to be talked over rather than read.

| # | Slide | Shape |
|---|---|---|
| 40 | Act 3A divider — The Anatomy | poster over `df-ato3a` |
| 41 | The ignition — one command | silent · ceremonial code block |
| 42 | “Dark” because nobody needs to see | 3 cards + honest-analogy callout |
| 43 | The launcher never believes the thinker | **nesting SVG** — the two seats |
| 44 | Task-Spec — no eval, no task | **silhouette**: in · sealed · out |
| 45 | Stop writing the system. Compile it. | **nine sealed boxes** — the spine |
| 46 | Four things on the second screen | 4 cards + hard-stop callout |

### The two decisions I made without you

You said "go for it" with four questions open. Two I answered from the
repository; two were forced by the calendar. All four are recorded here so
they can be reversed on purpose rather than by accident.

1. **Six gates, and four — both are true.** `demo.md` §5.3 says six checks
   were vacuous: *"four were found by the autonomous run itself, two were
   found last night, reading code."* The commit `cc0c5d7` says "close six
   vacuous gates." The agenda said four in three places. **The numbers
   measure different things** — the run caught four; a human reading code
   afterwards caught two more; six existed. So Act 0 slide 07 ("it corrected
   itself four times") is *correct as written* and stays, and Act 3B slide 60
   states both numbers explicitly in its opening line. Nothing needs
   retracting.
2. **Track A, not Track B.** `demo.md` offers a Track B where a sixth file
   type arrives and the factory builds it live. It needs a Type 06 kit that
   does not exist and takes about two days to build. The workshop is today.
   Act 3B is therefore the hybrid the run-of-show always specified: **ignite
   live, narrate the completed evidence while it runs.** If Track B is ever
   prepared, slides 48–49 are where it would splice in, and the seven-beat
   sequence after them still works unchanged.
3. **Auto-allow closes Act 3B** (slides 59–61) rather than opening Act 5.
   It is the strongest material in the demo script and it lands while the run
   is still on screen and the room is hot. Act 5 stays about the bridge and
   the offer.
4. **Converge and Task-Spec silhouettes were built from what the repo
   supports** — the real pass names and their real inputs/outputs, from
   `docs/cvg-aut-systems-spine-steps-v5.pdf`. If updated docs arrive, slides
   44–45 are the two to revisit; nothing else in Act 3 depends on them.

### On showing the spine without opening it

§1.2 permits pass names, inputs and outputs at silhouette level and forbids
the contents. Slide 45 therefore names all nine boxes — Capture (optional),
Intent, Structure, Decompose, **Consensus**, Tasking, Register, Harness, The
Loop — with what enters and what exits each, and renders every interior as a
**visibly sealed, hatched, blurred panel**. The audience can see that there
is something inside and that it is deliberately shut. That is a far better
tease than a bullet promising depth, and it is auditable: the slide claims
exactly what §1.2 allows and nothing more.

The invariant is on the slide because it is public doctrine and it is the
whole design: *every pass lowers altitude, binds an engine, and ends at a
gate. Pass 8 does not lower — it closes.* Plus the line that makes the
factory argument land early: **the framework is factory-shaped from pass 1,
so when you decide to step out there is nothing to retrofit.**

**Beats**
1. **Ignition (~3 min, ceremonial).** One visible invocation fires the
   factory. Said out loud: *"While I explain how this works, it is working."*
   From this moment nobody touches the keyboard.
2. **What lights-out actually means.** The literal industry category; what
   goes dark (the execution path) versus what stays lit (intent, limits,
   accountability). Then the honest limit: a lights-out plant builds **one
   part, to a fixed spec, with a jig that catches the bad ones** — tonight's
   factory is exactly that narrow.
3. **The two seats.** The same binary inside the loop (a tool the model asks
   for) and outside it (launcher + referee). Walk the nesting: trigger →
   orchestrator → launcher → spawned loop → post-gate → done/retry/park.
   Land the self-report being **discarded unread**.
4. **Task-Spec, silhouette.** What enters, what exits, what it guarantees.
   *"No eval, no task."* Close on the commodity trick: once the eval defines
   done, the executor is a slot — which is why Act 1's engines were
   interchangeable.
5. **Converge, silhouette.** The nine boxes, all sealed. *"Stop writing the
   system. Compile it."*
6. **What to watch.** Cards moving (a gate let them move) · branches
   appearing (blast radius is a branch) · **something going red** (the best
   moment of the night — it does not ask, it reads the error and retries) ·
   a PR opening (because the referee exited zero). Then the hard stops, and
   the admission that not peeking is the whole point.

**Key lines**
- "While I explain how this works, it is working."
- "The launcher never believes the thinker. It checks the world."
- "No eval, no task."
- "Six tiers, and what each one is allowed to promise. That is the Bootcamp."
- "Stop writing the system. Compile it."
- "You are converged when an eval passed — not when you feel done."
- "If I am going to claim nobody is in the loop, I have to actually not be in
  the loop — including now, while it would be easy to peek."

**Gate.** The machine is understood while visibly working.

---

## Act 3B — Lights-Off Execution (45 min) — THE HEART

**Objective.** The room witnesses the factory migrate, validate, and
*name the liar* — no human in the loop. L5 stops being a concept.

**Scope discipline.** 1 file type · 1 seam (transform) · 1 oracle ·
4 layers (model → parser → schema → writer) · 0 lines typed by hand.

**Demo target — settled.** Type `01`, batch `B202607230000004`. One
cent, two detail rows. All five types at the close.

**Built: 15 slides (47–61), 2026-07-25.** Every command behind these slides
is already verified in [`demo.md`](demo.md) — keep it on the second screen.
The slides are captions and diagrams around a live terminal, not substitutes
for it.

| # | Slide | Shape |
|---|---|---|
| 47 | Act 3B divider — Lights Off | poster over `df-ato3b` |
| 48 | A different vendor tore up its plan | 2 cards + refuted arrow |
| 49 | Green means the referee said so | 4 gate strips |
| 50 | The upstream says 173.44 — hold that number | silent · manifest |
| 51 | All three computed 173.45 | **triptych** + the byte callback |
| 52 | Not rolled back. Never written. | stat-cells + 3 batch rows |
| 53 | It names the owner | 4 point-at cards |
| 54 | Remove any single witness | **withhold matrix** ← money shot |
| 55 | The confession | silent · 2 cards |
| 56 | A fact, not a generation | twin hashes + 3 cards |
| 57 | Five types, five findings, zero unexplained | 5-row table + 3 stats |
| 58 | Filled in by the run — not by me | **the Act 1 panel, lit** |
| 59 | Auto-allow moves the review onto your gates | mandate rules + the red-green box |
| 60 | A gate that cannot fail is worse than no gate | 6 cards over `df-gates` |
| 61 | Take these four | 4 practice cards + closing line |

### Two callbacks this act is now obliged to land

1. **The instrument panel.** Act 1 slide 25 stamps each of three bays
   *"answered live in Act 3B."* Slide 58 is that payment: the same three
   bays, permanently powered on, with the run's real answers — the control
   gate stopped it before the CSV existed (Q1), zero rows so there is
   nothing to undo (Q2), a finding that refuses to exist without its evidence
   and hashes identically everywhere (Q3). **If 58 is cut, cut the promise on
   25.**
2. **The overpunch byte.** Act 2 slide 31 taught the decode table on the
   accepted batch, whose trailer ends `…1734E` → `173.45`. Slide 51's second
   callout closes it: this batch ends `…1734D` → `173.44`. *Same fourteen
   digits. One character apart.* Do not explain the mechanic again here — the
   room already owns it, and the payoff is that they read it themselves.

**Beats.** ~18 min of the 45 is the seven-beat terminal sequence; the
rest is the trail-walk, the gates, and the AHA breathing room.

1. **Walk the trail it already left.** Task-spec picked up, plan drafted,
   cross-provider adversary refuted the plan — show the objections and what
   changed. The takeaway question for the room: *who is allowed to tell your
   system no, and can it overrule them?*
2. **Watch the gates pass.** Contract · privacy · control · golden-match.
   Narrate which gate the run is standing on, never the code.
3. **The lie, in the source's own words.** `net_amount: 173.44`.
   *"Hold that number."*
4. **Three independent implementations, one answer.** Java, SQL, Python —
   all computed `173.45`, all preserved `173.44` exactly. *"A system that
   silently fixes its source has destroyed the evidence that something
   upstream is broken."*
5. **The divergence, then containment.** Let the room say "the new code has a
   bug." Then staging `0`, business `0`, `quarantined`. *"Not rolled back —
   never written."* And the blast radius: the two adjacent batches succeeded
   and reconciled.
6. **Run the detector live — the attribution.** Point at four things only,
   never read JSON aloud: `owner` (who) · `basis[]` (a list a test can check,
   not a sentence a model wrote) · `controls.compared[]` · `independence`.
   Then invite them to scroll it looking for what is *missing*.
7. **Take its evidence away — the money shot.** Four channels, four
   withholds, four `DF-E-ATTRIBUTION-INCONCLUSIVE`. *"It does not lower a
   confidence score. It declines."*
8. **The confession, immediately.** The first version of that probe passed
   with any channel removed — "at least two of three" could not fail. The run
   caught it at hour six and tightened it. Say plainly: *the version of this
   talk that omits this slide is a worse talk, and you would have had no way
   to know.*
9. **Determinism.** Twin `finding_id` hashes, identical across four runtimes
   built on different days. Then the portable test: *run any agentic system
   twice and diff the output.*
10. **Close the loop — all five types.** Five findings, zero unexplained
    differences, zero legacy defects. *"The old system was right the whole
    time. Its inputs were not."*
11. **The panel, filled in.** Callback 1 above.
12. **Auto-allow is a bet on your gates.** The Cline reframe — ticking
    auto-approve does not remove the review, it moves it onto your gates.
    Then DR-011's rules of engagement, and what they all have in common:
    they exist to stop the agent **making the red thing green**.
13. **Six gates that could not fail.** Four found by the run, two found
    afterwards by reading. Land #4 hardest — the same account at two
    different banks would have shared a token, and only byte-for-byte
    comparison against a human-approved file caught it.
14. **What you actually do.** Freeze your oracles · mutation-test your gates
    · make evidence an artefact, not a log line · let it refuse. Close on:
    *"go and try to break one of your own gates this week. If you can't make
    it go red, it was never protecting you."*

**Key line — said aloud at the AHA**
> "Three independent implementations each computed 173.45. The source
> declared 173.44. Nobody corrected it. Every system preserved the lie
> exactly as written, refused the batch, and kept the other batches
> running. The one cent never reached the database — and the factory
> can prove *who* lied, without ever showing you a card number."

Then the doctrine callback:

> "A wrong money number passes unnoticed — that is exactly why the
> golden-match exists. Eval engineering is not optional in a financial
> system."

**Key lines**
- "Who is allowed to tell it no, and can it overrule them?"
- "Green means the referee said so — not the model."
- "Not rolled back — never written. The cent never entered the database."
- "A bad file does not take the night down."
- "The explanation is a list a test can check, not a sentence a model wrote."
- "It does not lower a confidence score. It declines."
- "The gate was green and proved nothing."
- "The finding is a fact, not a generation."
- "The old system was right the whole time. Its inputs were not."
- "Auto-allow does not remove the review. It moves it onto your gates."
- "A gate that cannot fail is worse than no gate."
- "If you can't make it go red, it was never protecting you."

**Production notes**
- Run duration must not depend on talking pace: pre-time stages; early
  finish → the PR waits; late → checkpoint recovery covers.
- Terminal: 16pt minimum, dark background, ~100 columns. Nothing in
  the demo script needs more width.
- Failure protocol: checkpoint worktree just before the reveal + cued
  backup recording. Errors on screen are fine and on-brand; a stall is
  not. Fall back to reading the committed evidence packets under
  `evidence/factory/` and `evidence/modern/` — they are already on
  disk from the pre-flight.
- Rehearse second-screen choreography (Linear + PR view) as
  deliberately as the slides.
- **Slides 50 and 55 are silent slides.** Do not fill the silence. Slide 50
  is where the room memorises 173.44; slide 55 is where they decide whether
  to trust you. Both need a beat.

**Assets/sources.** The live harness + repo;
[`demo.md`](demo.md) (verified commands and output);
`.runtime/e2e-evidence/`, `evidence/modern/`, `evidence/factory/`;
`docs/decisions/011-autonomous-execution-mandate…md` (slide 59's rules);
backup recording.

**Gate.** Witnessed: migrate, validate, attribute — and refuse to
conclude without evidence. L5 became a thing seen. And the room leaves
Act 3 with four things it can do on Monday having bought nothing.

---

## Act 4 — KurvPay: the receipts (20 min)

**Objective.** The room believes the pattern is real beyond the stage —
and sees what it is worth in money. (Monetization lands here, grounded
in measured numbers, not projections. Play it immediately after the
AHA, energy hot.)

**Built: 11 slides (62–72), 2026-07-25.** Every figure traces to
`docs/kurv-edp-v2.pdf` — the condensed engineering reference, compiled
2026-07-24, whose own cover states *"metrics measured at compile time."*
The act's structure is borrowed from that document's own opening pages:
a four-stat hero row, then four labelled quadrants, then the tables.

| # | Slide | Shape |
|---|---|---|
| 62 | Act 4 divider — The receipts | poster over `darkfactory-bg` |
| 63 | Not a demo trick — the twin | silent · NorthWind ↔ KurvPay |
| 64 | One repository, two products | 4 stats + 4 quadrant cards |
| 65 | Numbers somebody had to defend | 6-row measured table |
| 66 | Eight gates. And exactly one human decision. | **pipeline SVG** |
| 67 | Two to three months, or about eight hours | 2 cards + 4-step timeline |
| 68 | When the two systems disagree, who is wrong? | 4 stats + **the triage tree** |
| 69 | Two types stalled — the golden was wrong | 2 cards + the cost callout |
| 70 | The golden is evidence, not truth | silent · **ring mandala** |
| 71 | Sixty lessons became five skills | promotion rule + skills table |
| 72 | Tonight was the trailer | silent · hands off to Act 5 |

### ⚠ Four number corrections — 2026-07-25

Reading the source properly contradicted the Numbers Bank in four places.
**The figures below are now what §5 says and what the slides show.**

| Was | Is | Where it came from |
|---|---|---|
| "29/32 types migrated" | **32 of 32 onboarded, status complete** | the v2 reference, twice |
| — | **26 of 28 *matched* types golden-signed, 2 stalled** | `match-state.yaml`, the parity ledger |
| "4 permanent skills" | **5 promoted skills** | the promotion table |
| "~55–60 lessons" | **60 numbered + 9 global** | `memory.md` |

The 32 / 28 / 26 relationship matters on stage and is easy to fumble:
**32** types were onboarded; **28** of those have a legacy counterpart to
match against; **26** of those 28 are signed; **2** stalled. Saying "26 of
32" would be wrong and would undersell the work.

The fifth skill is **`golden-match`**, promoted out of the diff-triage batch
— which is why Act 1 slide 24's promise now reads *five*, and why slide 71's
heading is "five skills and three gates."

### Two things in the source that were too good to leave out

1. **The diff-triage tree (slide 68).** The engagement's own framing:
   *"the reflex 'edit the parser until the diff vanishes' is the single most
   dangerous move in the program."* So every dirty column is classified
   before anyone touches code — representation (config only) · fixture
   defect (the golden is wrong) · legacy manufacture (the old system
   invented a value) · parser bug (**the only branch allowed to edit code,
   and only with a citation**). *No citation, no edit: stall with proof.*
   This is the slide that answers the question Act 3B leaves hanging, and
   it carries the number the whole discipline exists to protect: **0
   uncited edits.**
2. **The full doctrine line (slide 70).** We had been using half of it. The
   source says: *"the golden is evidence, not truth — the raw bytes plus the
   proc are truth."* The second clause is what makes it actionable rather
   than merely wise, and slide 70 now carries both.

### The Act 1 obligation, paid

Act 1 slide 24 promises the flywheel "will be counted in Act 4." Slide 71
is that payment: the three-part promotion rule (recurrence across ≥3 types ·
high cost if wrong · mechanizable), the five skills with what each one
prevents, and the detail that makes it real — **the loop creates the skill
itself and does not defer to a human**, then retires the lesson into a
pointer and retrofits one existing caller as proof.

It also closes a loop with Act 3B: three of the sharpest lessons became
**deterministic guards**, each shipped with **a verified negative control** —
somebody broke the code on purpose and watched the guard go red. That is
exactly Act 3B slide 61's second practice, invented independently by the
people who needed it.

### Operator decisions still open

- **Naming.** The slides say "KurvPay" (as the run of show always has) and
  describe the client only as "a client." The source names the client
  entity; the deck deliberately does not. **Confirm that is the boundary you
  want** before doors open — 249 people will read these slides.
- **62 or 63 subagents?** The reference's cover stat says 63; its body says
  "62 instantiated." Slide 64 uses **62** because the body is the more
  specific claim. Change both the stat and its source line together if you
  prefer 63.

**Beats**
1. **The reveal.** *"What you just watched is not a demo trick."* NorthWind
   Pay is the didactic, open-source twin of a live production engagement —
   and every architectural choice from tonight came from doing it for money
   first.
2. **The engagement at a glance.** 32 types · 62 subagents · 8 gated stages ·
   60 lessons. Then the four quadrants: the business, the engineering, the
   agentic system, the dark factory. Note out loud that the four-layer parser
   and the COBOL overpunch are things they *already saw* on the twin.
3. **The measured numbers.** One file 42s → 1s. A thousand files 11.6h → 2s.
   Deploy 4h with 6+ people → 15 min with one. Recovery 2h → 16 min. Monthly
   cost $2,500 → $25. And the row nobody expects: **parser code 7,600 lines →
   1,555.** Less code is less surface for a wrong cent to hide in.
4. **Eight gates, one human.** Walk the pipeline. Land two things: *stall,
   never halt* (one type's failure stalls that type; the queue carries on;
   the operator cadence is a morning review) and the honest answer to "is it
   really unattended?" — **no, and that is the design.** Cloud deploy is a
   human decision by written rule, because that is where a mistake stops
   being reversible.
5. **Months or hours.** 2–3 months of T-SQL archaeology per type versus ~8
   hours agentic — and the 8 hours is **measured**, read off session
   transcripts with token and cost counts, not asserted. Then the timeline:
   kick-off 2025-11-25 → four types 2026-02-02 → the full 32-type surface
   2026-06-29 → the sign-off crank 2026-07-13/16.
6. **The triage tree.** See above. This is the intellectual centre of the act.
7. **The scar story.** Two types stalled on defective goldens — one exported
   on the wrong day, one a 2025 golden against a 2026 input, proven **from
   the golden's own header row** and kicked back to the client rather than
   faked green. Say the expensive part out loud: reporting 26 of 28 instead
   of 28 of 28 costs you the number a client wants to hear, and buys the only
   thing that makes the other twenty-six mean anything.
8. **The doctrine.** *The golden is evidence, not truth — the raw bytes plus
   the specification are truth.* Tonight the source lied; on the engagement
   the golden lied, twice. **Same discipline, tested from opposite
   directions. It only counts as a principle if it costs you something.**
9. **The flywheel, counted.** See the obligation above.
10. **The frame.** *"Tonight was the trailer. This is the poster from a
    theatre where it already played."* Then hand off: *"which raises the only
    question left — and it is about you, not about the factory."*

**Key lines**
- "What you just watched is not a demo trick."
- "The legacy stack is retired — and then kept, because it becomes the golden."
- "Less code is less surface for a wrong cent to hide in."
- "Stall, never halt."
- "Is it really unattended? No — and that is the design."
- "The eight-hour figure is measured, not asserted."
- "Edit the parser until the diff goes away — the single most dangerous move
  in the entire programme."
- "No citation, no edit: stall with proof."
- "When this system says signed, it means signed."
- "The golden is evidence, not truth — the raw bytes plus the specification
  are truth."
- "It only counts as a principle if it costs you something."
- "Tonight was the trailer. This is the poster from a theatre where it
  already played."

**Assets/sources.** `docs/kurv-edp-v2.pdf` — every number, the eight stages,
the triage tree, the promotion rule, the two stalled types, and the doctrine
line. Each slide carries its own source line. Slide 62 reuses
`images/gen/darkfactory-bg-opt.jpg`; slide 70 uses the ring-mandala SVG
adapted from `tmpl-agentic-engineering.html`.

**Gate.** Real beyond the stage; worth known in money; and the room has
watched the same discipline hold when it was inconvenient.

---

## Act 5 — The Bridge (30 min)

**Objective.** The room feels the gap between watching and mastering —
and receives the Factory Ladder as the path, at the peak of intention.

**Built: 8 slides (73–80), 2026-07-25.** The offer mechanics come from
`docs/wrksp-secret-dark-factory-v1.pdf` §13–14 (Escada da Fábrica,
credit-that-flows, bundle logic); that document is never cited on-slide —
it is the internal alignment doc, and the slides carry its numbers, not
its name.

| # | Slide | Shape |
|---|---|---|
| 73 | Act 5 divider — The bridge | poster over `ato8-travessia` (purple bridge to a lit door — the act's whole argument in one image) |
| 74 | You watched it run — you did not watch it being built | seen vs not-seen columns |
| 75 | You live at L3. You just watched L5. | **staircase recap** + the gap bar |
| 76 | What changes Monday morning | 3 workflows × 3 ticks — **interactive checklist** |
| 77 | The Factory Ladder | 3 rung cards + the 3 things pre-sale buys |
| 78 | The ladder, priced in the open | **price staircase** + the credit rule |
| 79 | We did not sell you magic | silent · the honesty contract honoured |
| 80 | The lights are off. The factory is still running. | silent · end card |

**Notes, in build order.**
- **Slide 74's not-seen column uses only stage-safe silhouette words** —
  grounded harness, eval-as-contract, adversary, fleet — the exact list
  Bloco 4's own script puts on stage. Nothing from the R1 banned list
  (Converge, the passes, Fork, safe-to-delegate, HMAC), and "signed gate"
  was deliberately left out: it is on the hidden list, not the script.
- **Slide 75 reuses the slide-20 `.rung` staircase**, compressed (name +
  one-line verdict, no car analogies), with Shapiro's real level names.
  L0–L2 are dimmed, L3 carries "seven in ten of this room", L4 "three in
  ten" (both from the Act 0 room data), and the gold→green gap bar says
  quote 18's second half. The callback is visual, as required.
- **Slide 76 is the `.ck` interactive checklist's first and only use** —
  it was the last unused template pattern. The three workflows (repo
  agent-brief · a falsifiable check per task · one-task-one-worktree)
  deliberately do not overlap Act 3B slide 61's four takeaways, which are
  repository disciplines; these are weekly working habits. Tick them live
  or leave them — both read fine.
- **Slide 78 carries the deck's one remaining `.todo`: the pre-sale
  price.** The source doc literally writes "R$[X]" — the number does not
  exist yet (open item 4). The two anchor rungs are real: Semana lot
  R$997, public lot R$1.997. The credit rule shown is the one the agenda
  locked: 100%, released the day the Bootcamp ends, stacking on the
  bundle discount. Validity window is *not* on the slide — it is still
  undecided, and inventing it would violate the no-fine-print promise.
- **Slides 74/76 carry the same 1366×768 lesson as the Act 4 ledger**:
  row and checklist spacings are vh-clamped so both fit at 768px with
  nothing to spare (768/768 and 766/768). If you add a row to either,
  re-measure both resolutions first.

**Gate.** Gap felt; ladder received at peak intention.

---

## 4. Rehearsal checklist (before doors open)

- [x] **Legacy clean-volume acceptance proof** executed on 2026-07-24,
      with 25 synchronous evidence packets and the separate
      automatic-worker gate passed. The worker proof covered `15`
      canonical successes, `10` canonical quarantines, four exact-batch
      restarts (`database_commit`, `raw_archive`, rejection
      `raw_quarantine`, and oracle mismatch), one integrity quarantine,
      and one oracle mismatch. It ended with 26 evidence packets and
      empty cache/journal state — the factory's oracle is proven before
      the show.
- [x] **Act 3B reveal corrected** to the source-system finding, with
      the commands and output verified against this checkout
      (2026-07-25). The "planted legacy defect" item is closed as
      not-needed: the real finding is stronger than the planted one.
- [x] **Demo target locked:** Type `01`, batch `B202607230000004`, plus
      the five-type close.
- [ ] **Pre-flight run** on the show machine:
      `make clean CONFIRM=clean-runtime` → `make deploy` (~30s) →
      `make test-e2e TYPE=all` (~3 min) → `make df-accept TYPE=all`
      (~30s). Fixture keys exported in the demo shell (see the demo
      script's `export` block; they live in `.env`).
- [ ] **Full dress rehearsal of Acts 3A+3B** with the real harness
      (orchestrator + adversary + executor) converging live, timed
      against the talk track.
- [ ] **Second-screen choreography** wired and rehearsed: Linear board
      + GitHub PR view visible while speaking; terminal at 16pt, dark,
      ~100 columns.
- [ ] **Backup recording** of a successful run, cued and tested.
- [ ] **Checkpoint worktree** saved just before the reveal.
- [x] **Supabase room numbers pulled** (2026-07-25) and all nine `.todo`
      placeholders on Act 0 slides 03–04 replaced with real values; bar
      widths carry the real percentages. Slide 04 was redesigned to
      pool × room — see §0.1. **Still to do at door time:** re-run the
      query and confirm 561 / 249 / 44% have not moved, or drop the word
      "live" from slide 03.
- [x] **English pass** on Acts 0–1 — no Portuguese in any presented string,
      every tag on the `.pill` component, act name "Dark Factory
      Operation". Also fixed: `<title>`, the meta description, and the two
      navigation `aria-label`s, which were still pt-BR. The inherited
      CSS/JS comments are still Portuguese — harmless, never presented,
      left as-is because the design system is inherited verbatim.
- [ ] **Time-of-day sweep** once the schedule conflict is resolved — the
      deck currently mixes "today" and "tonight" (§0.2 item 7).
- [x] **Autonomy level names corrected** (2026-07-25) to Dan Shapiro's
      own — spicy autocomplete · coding intern · junior developer ·
      developer · engineering team · dark software factory — with the car
      analogy kept as the subtitle. **Rehearse the new words:** the old
      paraphrases ("L1 delegated tasks", "L2 pairing", "you became a
      manager") must not come out on stage, and Act 5's recap has to
      match. *(It does — slide 75 was built with Shapiro's names,
      2026-07-25.)*
- [ ] **Sources legible from the back row** — Act 1 carries eight
      on-slide citations at ~9–11px mono. Check them on the real
      projector; if they do not read, they still belong in the deck for
      the repo, but say the attribution out loud.
- [ ] **Stage-language pass** on every slide (name-never-open rule:
      Converge and Task-Spec at silhouette level only; Fork, HMAC,
      safe-to-delegate, pass internals never spoken). Same pass must
      catch any surviving "legacy defect" phrasing — see §1.4.
- [x] **Act 2 BRD** drafted (2026-07-25) — derived from the Type 01
      contracts and built as the interactive six-layer stack on slide 34,
      thirty rules in total. **Still to do:** rehearse it as a
      *conversation*, not a reading. Decide in advance which two layers you
      open live; opening all six burns the act's whole budget.
- [ ] **Offer screens final:** only the pre-sale price is missing — lock
      it and replace the `.todo` on slide 78. The ladder, both lot prices
      and the credit rule are already on slides 77–78.
- [ ] **Schedule confirmed:** internal ementa says 19h30–23h30; public
      page says 09h00–13h00 BRT. Resolve before publishing timings.

## 5. Numbers Bank

**The live demo (verified 2026-07-25 — Act 3B)**
- 5 source-system defects, one per type; **zero** confirmed legacy
  defects; **zero** unexplained differences
- Demo batch `B202607230000004`: declared `173.44`, computed `173.45`
  by three independent implementations (Java, SQL, Python)
- Containment: staging rows `0`, business rows `0`, status
  `quarantined`; adjacent batches succeeded
- Withhold sweep: 4 of 4 channels → `DF-E-ATTRIBUTION-INCONCLUSIVE`
- Determinism: identical `finding_id` across runs and across four
  runtimes built from scratch on different days
- **6 vacuous gates in total.** 4 found and fixed by the run itself
  (unfalsifiable withhold probe; cached Java suite; golden-match never
  contacting legacy; Type 04 token scope) and 2 found afterwards by reading
  code (dbt release gate existed for Type 01 only, so Types 02–05 ran none;
  rejected-batch parity built its "legacy observation" out of the contract
  and so compared the contract with itself). Act 3B slide 60 carries all six,
  labelled by who found them.

**KurvPay (real engagement — Act 4).** All from
`docs/kurv-edp-v2.pdf`, compiled 2026-07-24, "metrics measured at compile
time." **Four figures were corrected on 2026-07-25 — see the Act 4 section.**
- **32 of 32** file types onboarded, status complete
- **26 of 28** *matched* types golden-signed · **2 stalled**. Say the
  relationship carefully: 32 onboarded, 28 have a legacy counterpart, 26 of
  those signed. "26 of 32" is wrong.
- ~160k rows compared value-for-value · **9 cited parser fixes · 0 uncited
  edits**
- One file: ~42s → ~1s (**42×**) · 1,000 files: ~11.6h serial → ~2s parallel
- Parser code, four types: ~7,600 → ~1,555 lines (**6.8× less**)
- Deploy: ~4h with 6+ people → ~15 min with 1 dev (**16×**)
- Recovery: ~2h → ~16 min (**8×**)
- Monthly infra cost: ~$2,500 → ~$25 (**~98%**)
- Per-type effort: 2–3 months by hand → **~8h agentic, measured** (read off
  session transcripts with token/cost counts — not asserted)
- 62 instantiated subagents, 28 of them parser experts · 29 commands ·
  12 skills · 10 rules *(the reference's cover says 63 subagents; its body
  says 62 — the deck uses 62)*
- 8 gated factory stages + a manual deploy runbook; the deploy gate is the
  only human decision
- Flywheel: **60 numbered lessons + 9 global** → **5 promoted skills**
  (money-field · positional-hierarchical · cobol-overpunch · reconciliation ·
  golden-match) + **3 deterministic guards**, each with a verified negative
  control
- Programme shape: kicked off 2025-11-25 · 4 types by 2026-02-02 · full
  32-type surface 2026-06-29 · sign-off crank 2026-07-13→16 · 666 commits,
  ~210 branches
- The 2 stalled types: a golden exported on a different day, and a 2025
  golden against a 2026 input — both proven from the golden's own header row
  and kicked back to the client

**The offer (Act 5, slides 77–78).** From
`docs/wrksp-secret-dark-factory-v1.pdf` §14 — never cite the document on
stage.
- Ladder: pre-sale = **R$[X], still unlocked** (the deck's one `.todo`) ·
  Semana lot = **R$997** · public lot = **R$1.997**
- Credit rule: **100%** of the pre-sale price becomes Formação credit,
  released the day the Bootcamp ends, stacking on the bundle discount.
  Validity window undecided — not on any slide.
- Pre-sale includes A Semana (the week the base pays **R$97** for)
- Dates said on stage: Semana **10–14/08** · Bootcamp **24–28/08**

**The legacy case (didactic — Act 2)**
- 30+ raw file types on SFTP
- ~300 PL/pgSQL stored procedures
- 12–18 months / 8–12 devs — the frozen migration quote
- 4–6 people reconciling numbers by hand at close

**The repo baseline (do not overclaim on stage)**
- 5 types implemented (01–05), migrations 001–010
- Oracle proof 2026-07-24: 25 canonical outcomes (15 success,
  10 quarantine), 4 restart seams, 1 integrity quarantine, 1 forced
  oracle mismatch
- No CI exists; nothing here is production-ready or CI-ready

**The external evidence (Act 1 — all published, all cited on-slide)**
- **METR RCT, 2025** (arXiv:2507.09089): 16 experienced open-source
  maintainers, 246 real tasks in their own repositories (avg 22k+ stars,
  1M+ lines). Forecast **+24%** faster · believed **+20%** faster ·
  measured **19% slower**. With AI allowed they spent less time writing
  and more time prompting, waiting and reviewing.
- **StrongDM, Feb 2026** — “Software Factories and the Agentic Moment”
  (write-up by Simon Willison): AI team founded July 2025, **3 people**,
  two rules — *code must not be written by humans; code must not be
  reviewed by humans*. Their agent, Attractor, ships as a repository of
  **three markdown files and zero lines of code**. Doctrine:
  **validation replaces code review.**
- **Chroma, 2025** — context rot measured across **18 frontier models**:
  quality degrades as input grows, before the window fills.
- **MCP** — Anthropic, Nov 2024 → **Linux Foundation** Agentic AI
  Foundation, Dec 2025. Primitives: Tools, Resources, Prompts.
- **Shapiro, Jan 2026** — the ruler; **~90%** of self-described
  “AI-native” developers sit at **L2**.
- Say these as *other people's* numbers. That is what makes them work.

**The room (Act 0 — snapshot 2026-07-25, on slides 03–04)**
- **561** distinct people applied (703 submissions, 142 repeat attempts)
- **249** selected · **44%** approval rate (below the 50–60% target)
- 312 turned away — all routed, none simply rejected
- Applicant pool by self-declared level: L1 **21%** · L2 **32%** ·
  L3 **33%** · L4 **13%** (the form offered only L1–L4)
- The room by level: L1 **0%** · L2 **0%** · L3 **70%** · L4 **30%** —
  the gate admitted nobody below L3
- Room seniority: 133 senior · 57 staff/lead · 39 pleno (**76% senior or
  above**)
- Source: `applications` export, `product = dark-factory-v1`. Deduplicated
  by e-mail; selected = any submission approved. Re-run before doors open.

**The funnel (Act 0 context, internal)**
- ~50–60% target approval rate; 2 waves
- 12.2% of low-ticket buyers historically migrate to high ticket

## 6. Quote Bank (say these, verbatim)

1. "The first agentic system you see tonight is the one that scored
   you."
2. "The model never invokes anything. It asks; the harness calls."
3. "The loop converges to green evals, not to truth."
4. "The real risk is not the system going down. It's the system
   working — and being wrong."
5. "The legacy, with all its defects, is the oracle."
6. "While I explain how this works, it is working."
7. "The launcher never believes the thinker. It checks the world."
8. "No eval, no task."
9. "What happens inside each pass is five nights of engineering."
10. "Three implementations that share no code. All three computed
    173.45. Nobody corrected the source."
11. "Not rolled back — never written. The cent never entered the
    database."
12. "Remove any single piece of evidence and it refuses to conclude.
    It does not lower a confidence score — it declines."
13. "A green gate that cannot fail is worse than a red one."
14. "Green is not the goal — green for the right reason is."
15. "The finding is a fact, not a generation."
16. "A wrong money number passes unnoticed — that is exactly why the
    golden-match exists."
17. "The golden is evidence, not truth."
18. "You live at L3. You just watched L5. The distance is engineering
    — and it's teachable."

## 7. Source index

| Source | Feeds |
|---|---|
| `presentation/workshop-dark-factory.html` | **The deck itself** — all 80 slides built (Acts 0–5 + break). One `.todo` remains: the pre-sale price, slide 78 |
| `presentation/tmpl-agentic-engineering.html` | Design system, components, chrome, runtime JS — template only, never presented. Also the source of the rings / orbital / curve **geometry** reused in Act 1 slides 15, 18, 21 and 24 |
| Shapiro · “The Five Levels” (danshapiro.com, Jan 2026) | The autonomy ruler — Act 1 slides 20–21, Act 5 recap. **Use his level names**, not our paraphrases |
| METR · RCT 2025 · arXiv:2507.09089 | The L2/L3 trap, measured — Act 1 slide 22 |
| StrongDM · “Software Factories and the Agentic Moment” (Feb 2026) | Independent proof that L5 ships real software — Act 1 slide 22 |
| Anthropic · “Effective context engineering for AI agents” (2025) · Chroma · “Context Rot” (2025) | Attention budget and the four levers — Act 1 slide 16 |
| OpenAI · “Harness engineering” (Feb 2026) · Böckeler / martinfowler.com · Osmani | Harness engineering and *Agent = Model + Harness* — Act 1 slides 11, 17 |
| Anthropic Agent Skills (`SKILL.md`, progressive disclosure) | The lesson → skill mechanism behind the flywheel — Act 1 slide 24 |
| `presentation/images/gen/df-*.jpg` | Act 0 and Act 1 cinematic backgrounds (Higgsfield `soul_location`) |
| `applications` export (`product = dark-factory-v1`) | The room numbers on Act 0 slides 03–04 (§5). Kept outside the repo — it carries names, e-mails and WhatsApp numbers; only aggregates ever reach a slide |
| `presentation/demo.md` | Verified commands, real output, the corrected reveal, the six vacuous gates, and the Track A / Track B choice (Acts 3A, 3B) |
| `docs/cvg-aut-systems-spine-steps-v5.pdf` | The real Converge pass names and their inputs/outputs — Act 3A slide 45's nine sealed boxes |
| `docs/decisions/011-autonomous-execution-mandate…md` | The dated grant of autonomy and its rules of engagement — Act 3B slide 59 |
| `docs/wrksp-secret-dark-factory-v1.pdf` | Funnel, scoring, moat discipline, offer mechanics (Acts 0, 5) |
| `docs/boot-uc-northwind-pay-edp-oss-v2.pdf` | Case framing, Shapiro ladder, bootcamp arc (Acts 1, 2, 5) |
| `docs/asd-agentic-loop-v1.0.html` | Five layers, hop map, misconceptions, two seats (Acts 1, 3A) |
| `docs/cvg-aut-systems-spine-steps-v5.pdf` | Converge silhouette (Act 3A) — updates pending |
| `docs/task-spec-v3.2.0.pdf` | Task-Spec silhouette (Act 3A) — updates pending |
| `docs/kurv-edp-v2.pdf` | **The whole of Act 4** — every number, the 8 gated stages, the diff-triage tree, the promotion rule, the two stalled types, and the full doctrine line. Compiled 2026-07-24; metrics measured at compile time |
| `README.md`, `plans/legacy.md` | Legacy topology, boundary rules, four truth roles, proof ledgers (Act 2) |
| `contracts/types/registry.yaml` + each `layout.yaml` | The five types and their grammars — Act 2 slides 30–31 |
| `contracts/types/01-card-settlement/` (`layout` · `privacy` · `reconciliation`) | The BRD's thirty rules — Act 2 slide 34 |
| `contracts/types/01-card-settlement/main/valid-minimal.dat` | The real bytes shown redacted on Act 2 slide 31 |
| `plans/modern.md` | Claim limits — what may not be said on stage (§1.4) |
| Past presentations (to be provided) | Slide raw material, all acts |

## 8. Open items

1. *(closed 2026-07-25)* **Act 5 slides** — built, 8 slides (73–80); see
   the Act 5 section. All four constraints honoured: Shapiro's real level
   names on the recap, the slide-20 staircase reused, the Monday workflows
   distinct from slide 61's takeaways, the act opening on the person (the
   bridge image is one person before a lit door), and the `.ck` checklist
   carrying the Monday beat.
2. *(closed 2026-07-25)* Act 1 slide 24's forward-reference was corrected in
   the same pass — it now reads "60 lessons distilled into 5 permanent skills
   and 3 gates", matching Act 4 slide 71.
3. **Track B is unbuilt and out of reach for today.** A sixth file type
   arriving live needs a Type 06 kit (~2 days). If it is ever prepared,
   Act 3B slides 48–49 are the splice point. Recorded so the option is not
   silently forgotten.
3. *(closed 2026-07-25)* **Monday workflows** — selected and built into
   slide 76: repo agent-brief · a falsifiable check per task ·
   one-task-one-worktree. Chosen to be weekly habits, not repository
   disciplines, so they cannot collide with slide 61.
4. **Offer screens — one number missing.** Slides 77–78 already carry the
   ladder (Semana lot R$997 · public lot R$1.997), the 100% credit rule and
   the bundle-stacking line. The pre-sale price is the only gap — the
   source doc says "R$[X]". When it is locked, replace the `.todo` on
   slide 78 and decide the credit's validity window (not shown on-slide;
   still undecided).
5. **Schedule conflict** — internal 19h30–23h30 vs public 09h00–13h00
   BRT. Resolve before publishing timings, then run the time-of-day sweep
   over the deck (§0.2 item 7).
6. **Converge / Task-Spec updated docs** — fold into Act 3A silhouettes
   on arrival.
7. **Past presentations** — glue into acts on arrival.
8. **Door-time re-check** of the room numbers — see the §4 checklist.

*Closed:* demo type decision (Type 01 / `B202607230000004`, settled
2026-07-25); planted legacy defect (not needed — the real source-system
finding replaced it); deck language (English end-to-end, settled
2026-07-25); deck file and design-system inheritance (settled 2026-07-25 —
see §0.1); Supabase room numbers (landed 2026-07-25 — figures in §5,
slide 04 redesigned to pool × room); Act 1 slides (built and then
expanded 2026-07-25 — 17 slides, see the Act 1 section); autonomy level
names (corrected 2026-07-25 to Shapiro's own — see the Act 1 section);
Act 2 slides (built 2026-07-25 — 12 slides, see the Act 2 section); Act 2
BRD (drafted 2026-07-25 as the interactive stack on slide 34).
