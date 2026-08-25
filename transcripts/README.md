# Transcripts — live Nights

Closed captions from the projector room. They are **what was said**, not
the week map and not the staff clock.

| Need | Open |
|---|---|
| What the Night was *for* | [`agenda/`](../agenda/README.md) |
| What the three of you execute | [`run/`](../run/README.md) |
| What the room saw | [`presentation/`](../presentation/README.md) |
| Converge papers | [`docs/`](../docs/README.md) |

**One Night** each day. No morning / afternoon split. The `.vtt` is the
live language (this drop is pt-BR). Briefs in the repo stay English.

Do not treat a caption as a gate. If a transcript and [`agenda/dN.md`](../agenda/d1.md)
disagree, the brief wins. Do not paste these files into NotebookLM.

## Naming

```text
tr-dN-<seat>.cc.vtt
```

| File | Night | Seat |
|---|---|---|
| [`tr-d1-archaeologist.cc.vtt`](tr-d1-archaeologist.cc.vtt) | 1 | Archaeologist (SA + AI) — **on disk** |
| `tr-d2-translator.cc.vtt` | 2 | Translator (SWE) — not here yet |
| `tr-d3-constructor.cc.vtt` | 3 | Constructor (DE + analytics) — not here yet |
| `tr-d4-orchestrator.cc.vtt` | 4 | Orchestrator — not here yet |
| `tr-d5-dark-factory.cc.vtt` | 5 | Dark Factory — not here yet |

`.cc.vtt` = WebVTT closed captions. Rebuild or drop the next Night’s
file here with the same shape.

---

## Main points of each Night

The week is one steel thread: Type `01` card settlement, trailer lie
**173.44** vs rows **173.45**, keep the declaration, refuse the batch.
Autonomy goes up. HITL goes down. Type `06` stays sealed until Friday.

### Night 1 — Archaeologist · understand

**Rings:** prompt + context. **Converge:** Pass **0–1** only. **No product code.**

You arrive AI-native, brownfield. You do not inherit a brain, a graph,
or last run’s ADRs.

1. **Use-case.** Money arrives as overnight files. Two plants, same raw
   bytes. Legacy first write = CSV on SFTP. Modern first write (later) =
   Parquet in `modern/landing/`.
2. **Seat.** House stack: Oh My Pi → OpenRouter → a workspace → DeepSeek.
   Grade gates, not the vendor.
3. **Plant is a fact.** `make deploy` then `make run TYPE=01 SCENARIO=valid-minimal`.
   MATCHED, net `173.45`. `evidence/` in the **terminal**.
4. **Second Brain.** Nine packs, types `01`–`05`, NotebookLM. Type `01`
   is tonight’s steel thread. Days 2–5 **query** this notebook.
5. **OntoLayer.** Same question **without** (`make ontology-ask-sql`) then
   **with** (`make ontology-ask` / MCP).
6. **Converge 0–1.** Capture writes `docs/brd-type-01-card-settlement.md`.
   Intent writes `docs/tech-spec-type-01-card-settlement.md`. Stop.
   No ADRs, no seams, no Consensus, no `modern/`.

Staff: [`run/d1/`](../run/d1/README.md). Deck live: [`d1-archaeologist.html`](../presentation/d1-archaeologist.html).

### Night 2 — Translator · translate

**Rings:** harness (Bind). **Converge:** Recap 0–1. Run **2–4**, then **5**.
Mesh internals. Factory 6–8 is Day 4.

Yesterday you created the seat, the brain, the graph, and the brief.
Tonight you recap, bind the machine, query, sign, and hold leaves.

1. **Recap.** MATCHED still. Restate the BRD and the tech-spec.
2. **java2py.** Second plant, not a Java port. First write is Parquet, not SFTP.
3. **Bind the Agent Harness.** Frozen: `legacy/`, `contracts/`, `gen/`,
   `infra/`. Touch `legacy/processor/` → fail closed, or **stop**.
4. **Query.** Second Brain + OntoLayer until 2–4 has evidence.
5. **Consensus is the barrier.** ADRs → seams → owner **signs**. No sign → no leaf.
6. **Task-Spec.** One leaf, one eval, `signed_off` false. Mesh is Show.
   **No `modern/` required Tuesday.**

Staff: [`run/d2/`](../run/d2/README.md) — 12 beats, five boards.
Deck live: [`d2-translator-java2py.html`](../presentation/d2-translator-java2py.html).

### Night 3 — Constructor · register

**Rings:** harness + loop seed. **Converge:** 5–8 on **dlt → Gold**.

Landing exists. Tonight the lakehouse is real.

1. dlt **registers** Parquet. It does not re-parse. It does not own money.
2. Bronze → Silver → Gold. One grain, one owner each.
3. Attach golden-match. Two questions, **never netted**: match legacy
   observation? match the contract?
4. `valid-minimal` both yes. `DF-SOURCE-001` is `CONFIRMED_SOURCE_DEFECT`.
   Zero unexplained. Do not rewrite the referee.
5. Type `01` vertical closes. Stretch `02`–`04` only if `01` is green.
   No Dagster. No Type `05` build. No Type `06`.

### Night 4 — Orchestrator · leave

**Rings:** loop + eval. **Converge:** Bind + Loop. Type `05` unattended.

1. Dagster is lineage, retries, evidence — **not** the parser.
2. Direct and orchestrated must hash to the same Gold.
3. Bind Type `05`, walk away. Eval is the judge.
4. Small pill: `rounding-half-up` is `HALF_UP`. Python default `HALF_EVEN`
   and ops “normal rounding” are the trap. Wrong default → `MODERN_DEFECT`.
   Do not change `expected/`. Do not break Java.
5. Type `06` still absent.

### Night 5 — Dark Factory · classify

**Rings:** orchestration. **Converge:** full **0–8** on a sealed Type `06`.

1. Never-seen kit. Not in the Day 1 zip. Not in `spec/` until tonight.
2. Same spine, same barrier, same Bind. OntoLayer may answer the new
   schema; it does not skip Consensus.
3. Build the same shape: five-file → landing → dlt → Gold → golden-match.
4. When the cent disagrees: classify. Honest name may be
   `CONFIRMED_LEGACY_DEFECT` — the **main plant**, not the file.
5. Stall the type. Write the evidence. **Do not** edit frozen `legacy/`
   to go green.

The workshop deck [`wrkp-dark-factory.html`](../presentation/wrkp-dark-factory.html)
is not this Night’s HUD.

---

## How to use a caption

- Search a number (`173.45`, `173.44`) or a pass name to jump the tape.
- Pair with the matching `run/dN/` beat if you are reconstructing a Night.
- Do not upload into the Second Brain. Do not treat speech as `contracts/`.
