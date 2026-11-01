# Wiki provenance

How claims chain back to evidence in this wiki, and where the chain is known to break.

## The chain

`wiki/concepts/<page>` → `sources:` frontmatter (paths into `raw/`) → `raw/<file>`. Each raw file also has a source summary in `wiki/sources/` whose `sources:` points at it. Concept pages cite `raw/` directly, not the summary. Every `sources:` entry in the wiki is a `raw/` path; there are no non-raw entries.

Pages also end with a `### Sources` section of relative Markdown links (`../../raw/...`, URL-encoded). This is a second copy of the provenance and can drift from the frontmatter.

## Source summaries don't use a `-source` suffix

When a concept and a source summary would share a name, the source summary gets a descriptive suffix: `-note` (personal notes), `-wikipedia`, or `-manual`. Examples: `god-chords` / `god-chords-note`, `tonnetz` / `tonnetz-wikipedia`. The older `-source` convention in some templates is not used.

## Known quirks

- **Phantom path (found 2026-09-27).** `[[chromatic-mediants-orchestration]]`, `[[howard-shore]]` and `[[lotr-two-chords-chromatic-mediants]]` cite `raw/Write Dark, Delicate or Mysical Music with Just Two Chords.pdf`. The real file has no comma. Match raw filenames loosely when tracing this cluster. The misspelled "Mysical" and "4-Chod" in raw filenames are the real names, not typos to fix.
- **The log's paths predate the 2026-06-16 reorganisation.** Entries before that date name flat `wiki/<slug>.md` paths. They resolve by basename to `wiki/concepts/` or `wiki/sources/` (113 of 114 non-resolving log paths as of 2026-09-28).
- **Faithful transcription of wrong sources.** The wiki reproduces raw content accurately, *including its errors*. Confirmed cases: `raw/You don't need better chords.pdf` (Rings of Power attribution) and `raw/Synthwave production.md` (beat placement). A claim that traces cleanly to `raw/` is only as good as the raw document. Newsletters and personal notes deserve an outside check.
- **Errors introduced by synthesis also happen.** `[[chromatic-mediants-orchestration]]` adds a wrong detail ("share only the note A") that isn't in its raw source. Tracing to `raw/` catches these; the wiki's lint doesn't.
- **Uncited personal notes as sole evidence.** `raw/God chords.md`, `Synthesis tips.md`, `Synthwave production.md` and the ambient/dub techno notes cite nothing themselves, and at least one reads like pasted LLM output. Pages built on them may state claims more firmly than the note does (see `[[god-chords]]`).

## The wiki lint's blind spots

`outputs/lint-*.md` checks the wiki against itself. It doesn't:
- parse frontmatter as YAML (it passed 10 pages that are invalid YAML),
- resolve `sources:` paths against `raw/` (it missed the phantom path above), or
- check claims against the outside world.

A clean lint means consistent, not correct.
