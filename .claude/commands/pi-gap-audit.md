---
name: pi-gap-audit

description: Coverage and quality audit of the wiki - un-ingested sources, thin or shallow concepts, stale claims, unsupported assertions, and topics the corpus can't answer. Cross-checks against world knowledge. Complements the wiki's own lint rather than repeating it.

---

# Gap audit

Map what the wiki *can't* tell you, and where what it does tell you is weak. The output is a prioritized list of what to ingest, deepen, caveat, or correct.

## Division of labor - read this first

The wiki has its own lint (defined in the wiki's `CLAUDE.md`, output to `outputs/lint-YYYY-MM-DD.md`). It covers **internal consistency**: contradictions between pages, orphan pages, unresolved wikilinks, stale claims, structural housekeeping.

** Don't repeat the lint.** This audit covers what an internal-consistency check structurall cannot see:

| The wiki's lint sees | This audit sees |
| -------------------- | --------------- |
| Contradictions between pages | Claims that are wrong or unsupported against the outside world |
| Orphan pages | Topics with no page at all |
| Unresolved `[[wikilinks]]` | Sources sitting `raw/` that were never ingested |
| Page-level staleness flags | Whether a caveated-as-stale claim is *actually* now false |
| Structural housekeeping | Depth - a page that exists but is too thin to answer real questions |

**Start by reading the most recent `outputs/lint-*.md`, then `wiki/log.md`.** The lint tells you what's already known; the log tells you which of those findings were subsequently fixed. Repeating a finding that was fixed three weeks ago costs you credibility. Where the audit *does* overlap the lint, cite the lint's finding number and add what's new - don't restate it.

## Input

Optional scope from args: a domain (`ambient techno`), a page, or a topic area. With no args, audit the whole wiki.

## Step 1: Establish the corpus state

Run `/pi-env-check` (or its Part 2 checks) to get current counts and the un-ingested list. You need accurate numbers before judging coverage. Note the QMD index date - if it's stale, recent additions may look absent when they aren't.

Read `wiki/index.md` for the domain groupings, and the most recent `outputs/lint-*.md` plus `wiki/log.md` as above.

## Step 2: Ingestion gaps

Run from the Pinky workspace. Compare a recursive document inventory of `raw/` (excluding attachments) against the `sources:` frontmatter across `wiki/sources/` and `wiki/concepts/`:

```bash
python3 scripts/source_paths.py "$WIKI/wiki/sources" "$WIKI/wiki/concepts"
```

The helper uses PyYAML and reports malformed frontmatter recovery on stderr. Resolve extraction failures before declaring coverage complete.

Report:

- **Un-ingested sources** - files in `raw/` cited by no page. For each: what it appears to be about (read enough to say), and what it would add. Skip `raw/attachments/`.
- **Partially ingested sources** - a source summary exists but no concept page cites the raw document, meaning the material never made it into the synthesized layer.
- **Search-invisible sources** - the PDFs. QMD indexes `**/*.md` only, so a PDF's content is reachable only through its source summary. If that summary is think, the PDF is effectively unsearchable. Flag thin summaries of PDF sources as higher priority than thin summaries generally.
- **Phantom sources** - a `sources:` path that doesn't exist in `raw/`. Broken provenance.

## Step 3: Depth gaps

For each concept page in scope, judge whether it can actually answer questions or just names a thing. Signals of a thin page:

- Short relative to its subject, or a bare list of bullet headings with no mechanism, example, or caveat
- Cites exactly one source when the topic clearly spans several
- No `related:` links out, or links only to its own source summary
- `confidence: low` or `medium` that has never been revisited (`created` == `updated`)
- Reads as a definition without an application - nothing a reader could act on

For the domains in scope, also ask what a competent practitioner would expect the wiki to cover that it doesn't. State each as a **missing topic**, not a vague "could be deeper", and say which existing pages would link to it.

## Step 4: Truth gaps - cross-check against world knowledge

This is the part only an LLM can do, and it's the core value-add. For substantive factual claims in scope, check them against what you know:

1. **Is it factually right?** Frameworks attributed to the right author, terminology used as the field uses it, figures plausible.
2. **Is the attribution right?** "Rumelt's strategy kernel", "Moore's four zones", "Willink's extreme ownership" - verify the framework matches the named source, and that the wiki's rendering isn't a mutated version.
3. **Has the world moved?** A claim can be correctly transcribed from a 2023 deck and false today: org structures, headcounts, tooling, product names, industry practice. Date-sensitive claims about a fast-moving area (AI tooling, model capabilities, costs) go stale fastest.
4. **Is a caveat doing enough work?** A page marked "(2024 - may be outdated)" is honest but may still mislead if the substance is now wrong. Distinguish "caveated and still roughly true" from "caveated and now false".
5. **What's missing from a framework?** If the wiki renders a well-know framework with parts left out, say which arts and whether the omission distorts it.

Be specific and honest about your own confidence. "I believe this is wrong because X" beats a vague flag. Where you're unsure, say unsure - and say what would settle it.

## Step 5: Structural gaps

- **Unused page types** - `wiki_scope.yaml` lists the declared types. `entity` and `comparison` are declared; check whether any pages use them, by `type:` frontmatter rather than by directory. There is no `wiki/entities/`; entity pages live in `wiki/concepts/` with `type: entity`, so a missing directory is not a gap. The real gap is people and orgs named all over the concept pages with no `type: entity` page of their own. That's substantive, not stylistic.
- **Domain imbalance** - page counts per domain against the volume of `raw/` material for each. A domain with four raw sources and one thin concept page is under-synthesized.
- **Index drift** - does `wiki/index.md` list every page that exists, and does every page it lists exist? Is its `updated` date current?
- **Log fidelity** - spot-check that `wiki/log.md` entries name files that actually exist. The log is the only provenance record for *edits*; if it's wrong, change history is unreliable.

## Step 6: Report

Write the full report to `docs/investigations/YYYY-MM-DD-gap-audit.md`, and summarize in the response.

```
# Gap audit - YYYY-MM-DD

**Scope:** <whole wiki | domain | pages>
**Corpus:** N raw (N md + N pdf) | N concepts | N sources | N entities
**Prior lint:** outputs/lint-YYYY-MM-DD.md - N findings, N resolved per log
**Findings:** N total - N ingestion, N depth, N truth, N structural

## Priority

| # | Gap | Kind | Severity | Action |
| - | --- | ---- | -------- | ------ |
| 1 | <one line> | Ingestion | High | Ingest `raw/X` - only source on Y |
| 2 | <one line> | Truth | High | `[[page]]` claims X; now false because Y |
| 3 | <one line> | Depth | Medium | `[[page]]` names the framework, no mechanism |

< Then a section per finding: what it is, evidence with paths and quotes, why it matters, and the concrete action.>

## Not findings

<Things that look like gaps but aren't, with the reason. Keeps the next audit from re-raising them.>
```

Severity:

- **High** - a wrong claim someone would act on, or a missing source that leaves a domain unanswerable
- **Medium** - real gap, no immediate harm
- **Low** - housekeeping, cosmetic, or already adequately caveated

Order by severity, not by the order you found them. Include a **delta** against the previous gap audit in `docs/investigations/` if one exists: what was fixed, what persists, what's new.

## Step 7: Capture

- Update `docs/WIKI_COVERAGE.md` with the current coverage map and the standing gap list - it is the durable summary; the dated investigation file is the evidence.
- New provenance quirks -> `docs/WIKI_PROVENANCE.md`
- New structural facts about the corpus -> `docs/WIKI_STRUCTURE.md`
- Add a line to `docs/README.md` if you created a doc.

**Everything is a recommendation.** This workspace does not ingest sources, write pages, fix the index, or correct the log - the wiki's own Claude instance does. Hand the prioritized list to the user and say plainly that applying it is the wiki agent's job.
