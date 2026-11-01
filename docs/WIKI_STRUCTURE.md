# Wiki structure

How the corpus is shaped. `wiki_scope.yaml` holds the machine-readable map; this doc records what we've verified and what surprised us.

## Layout (verified 2026-09-28)

- `raw/`: 29 sources: 8 `.md` (personal notes) and 21 `.pdf` (manuals, books, newsletters, Wikipedia exports). `raw/attachments/` holds 23 supporting files, not sources.
- `wiki/concepts/`: concept **and** entity pages. There is no `wiki/entities/` directory; the 5 entity pages (4 composers plus `music-theorists-profiles`) sit here with `type: entity`.
- `wiki/sources/`: one source summary per raw document (`type: source-summary`).
- `wiki/index.md`, `wiki/log.md`: no frontmatter. The index lists pages by `[[slug]]` under ~30 fine-grained sections. The log is newest-first despite being "append-only".
- `outputs/`: lint reports (`lint-YYYY-MM-DD.md`) and one curriculum document. No frontmatter.

## Counts

| Date | Raw | Concept | Entity | Source | Note |
| ---- | --- | ------- | ------ | ------ | ---- |
| 2026-09-27 | 29 (8 md + 21 pdf) | 235 | 5 | 26 | Matches lint 2026-09-26 |
| 2026-09-28 | 29 | 242 | 5 | 27 | Max 9 ingest in progress (+7 concepts, +1 source) |

## Agent instructions

The wiki's `CLAUDE.md` and `AGENTS.md` are identical as of 2026-09-27. Before that, `CLAUDE.md` was a one-line `@AGENTS.md` import. They define the frontmatter contract (`title`, `id`, `type`, `sources`, `related`, `created`, `updated`, `confidence`, `tags`), an H1 title matching the topic, and a closing `### Sources` section.

## Ingest patterns worth knowing

- **Ingests happen live.** The wiki's agent may be writing while you investigate. It creates pages first and updates `index.md` and `log.md` at the end, so mid-ingest the new pages appear unindexed. Check file modification times before reporting index drift.
- **Partial ingestion is recorded in the source summary**, not in the log. Look for "Not yet processed" / "category-level summary depth" on `[[live12-manual]]` and `[[falcon-manual]]`.
- **Book-length sources get "part map" pages** (`omt-part*`, `mcd-part*`) that are deliberately short and link out to detail pages.
- **Overlapping sources are deduplicated**, not cross-cited. A topic covered by OMT and Music Theory for Dummies usually cites only OMT, so single-source pages don't necessarily mean single-source coverage.
