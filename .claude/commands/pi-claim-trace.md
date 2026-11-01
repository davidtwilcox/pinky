---
name: pi-claim-trace

description: Trace a claim back through the wiki to its evidence. Takes a claim, a page name, or a wikilink and follows concept page -> source summary -> raw document, reporting exactly where support runs out.

---

# Claim Trace

Trace a claim through the wiki's derivation chain to determine whether the evidence actually supports it - and if not, where it broke.

The chain runs one way:

```
raw/<document>      <- primary evidence, immutable
    wiki/sources/<summary>.md       <- what the LLM read out of that one document
        wiki/concepts/<concept>.md      <- what the LLM concluded across documents
            the claim as stated to the user
```

Every step is a place meaning can drift. Your job is to find which step, if any, it drifted at.

## Input

The user provides one of:

- A **claim** in prose ("the wiki says synthwave started in 2010")
- A **page name** or `[[wikilink]]` - trace all of that page's load-bearing claims
- A **quote** pasted from a wiki page or from an earlier answer

If not provided as args, ask for it.

## Step 1: Locate the claim in the wiki

Resolve the wiki root (`PINKY_WIKI_ROOT` -> `.wiki_root` -> `wiki_scope.yaml`). Quote all paths.

Find where the claim is actually stated:

- **QMD**, with the claim's distinctive wording as `lex` and its meaning as `vec`:
  ```
  searches: [
    { type: "lex", query: "\"distinctive phrase from the claim\"" },
    { type: "vec", query: "<the claim restated as a question>" }
  ]
  collections: ["<search.qmd.collection from wiki_scope.yaml>"]
  ```
- Fall back to `Grep` on distinctive substrings if QMD is unavailable or the claim is newer than the index

**QMD results paths are virtual** - collection-prefixed and slugified (`Research/raw/falcon_manual.pdf` for `raw/falcon_manual.pdf`). Use them with `qmd get` only; `Glob` for the real filename when you need `Read`. This bites hardest in tracing, because `raw/` filenames are exactly the ones with spaces in them. See [`docs/WIKI_RETRIEVAL.md`](../../docs/WIKI_RETRIEVAL.md).

Report **every** page that states it, not just the first. A claim appearing in three concept pages with three slightly different formulations is itself the finding.

If the claim exists nowhere in the wiki, stop and say so; it may be the user's paraphrase, or an earlier answer's invention. Distinguish between "the wiki doesn't say this" from "the wiki says something adjacent" and show the adjacent text.

## Step 2: Read the frontmatter chain

For each page that states the claim, record:

| Field | Why it matters |
| ----- | -------------- |
| `type` | `concept` = cross-source synthesis; `source-summary` = single document. Different burdens of proof |
| `sources:` | The provenance link. Paths into `raw/`. **A content page with no `sources:` is a dead end - report it** |
| `related:` | Where else the claim may be restated |
| `confidence` | The wiki's own self-assessment. A `high` on an unsupported claim is a worse finding than a `low` |
| `created` / `updated` | How old the claim is, and whether it's been revisited |

Follow `sources:` upward. A concept page may cite several raw documents; a source summary should cite exactly one. Note when a concept page's `sources:` list is missing a document that one of its cited sources summaries covers, or vice versa.

**Name collisions:** Follow actual links and the naming conventions in `wiki_scope.yaml`; do not construct a filename using a fixed suffix. This wiki uses descriptive source-summary suffixes (`-note`, `-wikipedia`, `-manual`), as documented in `docs/WIKI_PROVENANCE.md`.

## Step 3: Go to the raw evidence

Open each cited `raw/` document and find the passage the claim rests on.

**PDFs**: several sources are PDFs (`raw/*.pdf`). QMD does not index them - `Read` them directly with the `pages` parameter. If the PDF is long, locate the relevant section rather than reading all of it.

For each claim / source pair, assign a verdict:

| Verdict | Meaning |
| ------- | ------- |
| **SUPPORTED** | The raw document states this, in substance |
| **GENERALIZED** | The source says something narrower; the page broadened it (one study -> a general law) |
| **STALE** | Supported, but the source is dated and the page presents it as current. Note the source's date and whether the page caveats it |
| **UNSUPPORTED** | The cited document does not say this. Quote what it does say |
| **UNVERIFIABLE** | The cited path is missing, ureadable, or the citation is too vague to check |
| **UNCITED** | No `sources:` entry covers this claim at all. A verdict without the quote isn't checkable, which defeats the point. |

Quote the supporting (or contradicting) passage. A verdict without the quote isn't checkable, which defeats the point.

**Watch for the two common drift modes:**

1. **Scope creep** - a training deck's example becomes a stated fact about the company
2. **Confidence laundering** - a source hedges ("we believe", "draft", "may"), the summary keeps the hedge, the concept page drops it

## Step 4: Check the log

Read `wiki/log.md` for entries touching the pages in the chain. The log is append-only and dated, so it tells you whether a claim was edited, caveated, or fixed after a lint - and whether an old `outputs/lint-*.md` finding you might otherwise repeat has already been addressed.

## Step 5: Report

```
## Claim

> < the claim, as stated>

**Verdict:** SUPPORTED / GENERALIZED / STALE / UNSUPPORTED / UNVERIFIABLE / UNCITED

## Chain

| Layer | File | Says | Verdict |
| ----- | ---- | ---- | ------- |
| Concept | [[page-name]] | <as stated there> | uncited |
| Source summary | [[source-page]] | <as stated there> | supported |
| Raw evidence | `raw/<file>` | "quoted passage" | generalized |

## Where it broke

< The specific step, with both texts side by side. If nothing broke, say so in one line.>

## Also states this claim

<other pages, with any variation in wording>

## Recommendation

< What the wiki should do - caveat the claim, narrow it, add a citation, re-ingest a newer source>
```

Be direct about the verdict. The evidence either says it or doesn't; don't split the difference to be polite about the wiki.

## Step 6: Capture

- **A drift pattern worth remembering** (a whole class of claims from one source that over-generalize, a page type that routinely loses citations) -> add it to `docs/WIKI_PROVENANCE.md`
- **A one-off trace the user will want again** -> `docs/investigations/<slug>.md`
- **A verified-good chain** -> usually not worth a doc, but if the claim is load-bearing and gets asked about repeatedly, record the verified chain so nobody re-traces it
- **Do not fix the wiki.** Every recommendation goes in `docs/` and to the user. The wiki's own Claude instance applies changes; this workspace is read-only on it - say so when you hand over the recommendation.
