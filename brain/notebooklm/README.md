# NorthWind Pay Second Brain — NotebookLM pack

Human brain for the **whole drop** (types `01`–`05`), not only Day 1. The rest of the week queries this notebook. Type `06` is sealed until Friday. Not the agent’s memory. `spec/` stays on disk.

Handout: [`northwind-pay-brain.zip`](northwind-pay-brain.zip)

| Pack | What |
|---|---|
| `00-how-this-notebook-thinks.md` | Inbound only. Cite or abstain. |
| `01-estate.md` | Mail, meetings, policies, cover. |
| `02-five-types.md` | Types `01`–`05` READMEs. Type `06` not here. |
| `03-type-01-inbound.md` | Card settlement — Day 1 steel thread. |
| `04-type-02-inbound.md` | PIX / instant payment. |
| `05-type-03-inbound.md` | Payment slips. |
| `06-type-04-inbound.md` | TED. |
| `07-type-05-inbound.md` | Merchant fees — HALF_UP. Day 4 lives here. |
| `08-the-lie.md` | Same shape of lie on every live type. |

Staff beat (Day 1 upload): [`../../run/d1/12-notebooklm.md`](../../run/d1/12-notebooklm.md)  
Staff beat (Day 2 query): [`../../run/d2/05-query-brain.md`](../../run/d2/05-query-brain.md)

**Day 2 does not add a tenth source.** The room queries this notebook. Specs, the graph, and `docs/` answer “what we build.” Java, contracts, the tech-spec, ADRs, and `modern/` stay out.

| Night 2 ask | Pack that can cite | Not this notebook |
|---|---|---|
| J1 privacy / PAN / CPF | `01` meeting + policy; `03` layout | Java tokenizer |
| J2 signed overpunch, Marina’s lie | `03` (`00000001234E` → `123.45`); `08` | a `.dat` |
| J3 refuse vs crash; do not patch the trailer | `00`, `08`, Marina’s mail | a “fix” |
| J4 sanitize (tokenize, last4) | `01` privacy; `03` field notes | `legacy/processor/src` |
| J5 is the Java parser here? | `00` says no | uploading Java to “help” |
| Research: first modern artifact | `01` architecture: parser → **sanitized Parquet**; must not call Java | `plans/modern.md` (repo, Research Q3) |

Rebuild packs from `spec/` whenever inbound changes:

```bash
bash brain/notebooklm/build.sh
```

NotebookLM does not ingest the zip. Unzip, upload the nine `.md` files.
Do not add `legacy/`, `contracts/`, a `.dat`, the Day 1 tech-spec, ADRs, or `modern/`.
