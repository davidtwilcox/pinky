# Investigations

Question-scoped work. One file per question or thread - gap audits, claim traces worth keeping, contradiction hunts, "can the wiki actually answer X".

The investigation doc stays as the record of the work, including the dead ends. When something in it turns out to be durable - a retrieval tactic, a provenance quirk, a coverage gap, a synthesis - **promote it up into `docs/`** and leave the evidence here.

## Naming

- `YYYY-MM-DD-short-slug.md` for dated runs (`2026-08-28-gap-audit.md`)
- `short_slug.md` for ongoing threads with no single date

## Shape

No rigid template, but the ones that stay useful open with the question, the verdict, and the status - so a reader knows in ten seconds whether to keep reading:

```markdown
# <Question as a question>

**Started:** YYYY-MM-DD
**Status:** <in progress | findings established | closed>
**Trigger:** <what prompted this>

**Verdict:** <the answer, in one or two sentences, up front>

<Then the evidence: page paths, quoted passages, what was checked and what wasn't.>
```

Cite wiki pages as `[[wikilinks]]` and evidence as `raw/<file>`. Don't paste wiki content in wholesale - it's live and one directory away, and a copy here goes stale silently.

## Nothing here modifies the wiki

Investigations produce finding and recommendations. Applying the to the wiki is the wiki agent's job - see [../../CLAUDE.md](../../CLAUDE.md). Where an investigation concludes the wiki should change, state the recommendation plainly so it can be handed over.

---

## Index

- [2026-09-28-gap-audit.md](2026-09-28-gap-audit.md) - first whole-wiki gap audit. 16 findings: 2 High truth errors (Rings of Power attribution, chromatic-mediant common tone), a phantom provenance path, and depth gaps in synthesis fundamentals, voice leading, mixing and film-scoring craft
