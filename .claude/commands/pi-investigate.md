---
name: pi-investigate

description: The core investigation loop. Takes a question about the wiki's subject matter, searches and reads the live wiki, verifies claims against raw sources, answers with citations, and captures durable findings in docs/

---

# Investigate

Answer a question from the wiki - properly. Search it, read it, check the derived claims against the evidence behind them, cite what you used, and keep what's worth keeping.

## Input

The user provides a question. If not given as args, ask for it.

Questions come in three shapes; the shape determines how deep you go:

| Shape | Example | Depth |
| ----- | ------- | ----- |
| **Lookup** | "What are the four zones?" | Read the concept page, cite it. Done. |
| **Synthesis** | "What does the wiki say about how to get a strategy funded?" | Several pages across domains, assembled into an answer that doesn't exist as a single page. |
| **Interrogation** | "Is this claim that code quality drives productivity actually supported?" | Follow every claim to `raw/`. This is `pi-claim-trace` territory - offer to hand off, or do it inline. |

Say which shape you're treating it as if it's ambiguous.

## Step 1: Check what we already know

Read [`docs/README.md`](../../docs/README.md). If a `SYNTHESIS_*` doc already answers this, start from it - then verify it's still current against the wiki rather than trusting it blind.

Check [`docs/WIKI_RETRIEVAL.md`](../../docs/WIKI_RETRIEVAL.md) for search tactics that work on this corpus, and any recorded traps.

## Step 2: Orient on the wiki

Resolve the wiki root ('PINKY_WIKI_ROOT` -> `.wiki_root` -> `wiki_scope.yaml`). **Quote it - it has spaces.**

Read `wiki/index.md`. It is short and it catalogs every page by domain. This is almost always cheaper than searching blind, and it tells you the vocabulary the wiki actually uses - which is what makes the next step work.

## Step 3: Search

**QMD first.** Combine sub-queries; the first gets 2x weight:

```
mcp__plugin_qmd_qmd__query with:
    searches: [
        { type: "lex", query: "\"exact phrase\" keyword" },
        { type: "vec", query: "natural language question" }
    ]
    collections: ["Research"]       # from wiki_scope.yaml search.qmd.collection
    intent: "<what you're actually after - disambiguates>"
```

- Known term or name -> `lex` alone
- Conceptual question -> `lex` + `vec`
- Nuanced or cross-cutting -> add `hyde` with a 50-100 word passage of what the answer would look like
- Every result carries a `line`, accurate against the real file. To read around a hit: `get(file, fromLine = max(1, line - 20), maxLines = 80, lineNumbers = true)`
- **QMD result paths are virtual** - collection-prefixed and slugified (`Research/raw/Music-Theory.md` for a file actually named `raw/Music Theory.md`). Pass them to `qmd get` or use the `#docid`; they will **not** work with `Read` or `Grep`, and the slugification is lossy so you can't reverse it. To open a hit with `Read`, `Glob` for the real name. See [`docs/WIKI_RETRIEVAL.md`](../../docs/WIKI_RETRIEVAL.md).

**Classify every hit by its path prefix before you trust it:**

| Prefix | What it is | How to use it |
| ------ | ---------- | ------------- |
| `raw/` | Primary evidence, immutable | Authoritative for "what the source said" |
| `wiki/concepts/`, `wiki/sources/` | LLM-derived synthesis | Authoritative for "what the wiki concluded" - not for ground truth |
| `wiki/index.md`, `wiki/log.md` | Catalog and change history | Structure and provenance of edits |
| `outputs/` | Point-in-time lint reports | Historical; findings may already be fixed. Check `wiki/log.md` for a later fix before repeating a stale finding |
| `CLAUDE.md` | (wiki root) | The wiki's own agent instructions | Conventions, not content |

**Fallback if QMD is unavailable or stale:** `Grep` over the wiki root, `Glob` for filenames, `Read` for pages. Keyword-only - compensate by trying the wiki's own vocabulary from `index.md`, plus synonyms.

**PDFs in `raw/` are not indexed by QMD.** If the question touches a PDF-sourced topic (check `sources:` frontmatter for `.pdf`), read the PDF directly - semantic search will never surface it.

## Step 4: Read the pages

Read the pages that matter, in full. Concept pages give the synthesis; source summaries give what one specific document said. Follow `related:` wikilinks - the wiki's cross-links are curated and usually lead somewhere useful.

Note each page's `confidence` and `updated` fields. A `confidence: low` page or one that hasn't been touched in months carries less weight, and you shoul say so in the answer rather than flattening everything to equal authority.

## Step 5: Go to the evidence

**For any claim the answer leans on, follow it to `raw/`.** The `sources:` frontmatter gives you the path. This is the step that separates this skill from just reading the wiki back to the user.

Check:
- Does the raw document actually say this?
- Did the concept page generalize beyond what the source supports?
- Is the source dated in some way that matters - a 2024 training deck, a document marked "Draft"?
- Do two sources disagree, with the concept page silently picking one?

If a claim is load-bearing and you can't verify it, say so explicitly. "The wiki asserts X, citing `raw/Y`; I couldn't find support for X in `raw/Y`" is a far more useful sentence than a confident restatement.

## Step 6: Answer

Structure the answer to the question, not to your search path. Lead with the answer.

Citation rules:
- Wiki pages: `[[page-name]]`
- Evidence: `raw/<filename>`, with the section or heading when the file is long
- When derived and primary differ, show both and say which you believe

Be direct. Flag uncertainty where it exists and don't manufacture it where it doesn't. If the wiki simply doesn't cover the question, say that plainly - a clean "the wiki has nothing on this; the nearest pages are A and B" is a real answer, and it's a `pi-gap-audit` input.

## Step 7: Capture

Two separate decisions:

**Does this belong in `docs/`?** Yes if:

- The answer is a synthesis that took real work and spans pages the wiki doesn't connect -> new or updated `SYNTHESIS_*` doc, citing pages rather than reproducing them
- You learned something about how the corpus behaves -> update `WIKI_STRUCTURE.md`, `WIKI_RETRIEVAL.md`, or `WIKI_PROVENANCE.md`
- You found a coverage gap -> note it in `WIKI_COVERAGE.md`
- The work is question-scoped and ongoing -> `docs/investigations/<slug>.md`

Add line to `docs/README.md` for any new doc. Don't copy wiki content in - cite it.

**Does the wiki need to change?** If the investigation surfaced something the wiki should fix - a missing concept, an unsupported claim, a stale page - **write the recommendation in `docs/` and tell the user.** Do not edit the wiki. The wiki has its own Claude instance that owns those edits; hand it over rather than doing it here.

End by stating what you wrote and what, if anything, you're recommending upstream.
