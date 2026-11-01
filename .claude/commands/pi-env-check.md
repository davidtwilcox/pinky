---
name: pi-env-check

description: Read-only diagnostic - verify the wiki path resolves, page counts by type, and QMD index freshness. Use when something isn't working or to verify setup.

---

# Environment check

Read-only audit of the investigation environment. Do NOT write, move, or modify anything - not in this workspace, and certainly not in the wiki.

## Part 0: Does the config exist?

`wiki_scope.yaml` is gitignored, so a fresh clone won't have one. Check for it first.

**If it's missing**, stop and report this is as the blocking failure - don't attempt the rest of the audit:

> No `wiki_scope.yaml`. It's gitignored (it holds a machine-specific path), so a fresh clone starts without one. Copy the template and fill it in:
> ```bash
> cp wiki_scope.yaml.example wiki_scope.yaml
> ```
> Then run `/pi-env-config` to be walked through placeholders, or edit it directly and re-run this check.

**If it exists but still contains `<angle-bracket>` placeholders**, report which fields are unfiled and point at `/pi-env-config`. An unfilled `wiki.root` is blocking; an unfilled optional field (`canonical_root`, `agent_instructions`) is a warning.

Note that a resolvable `PINKY_WIKI_ROOT` or `.wiki_root` makes an unfilled `wiki.root` non-blocking - the override wins. Say so rather than reporting a failure that isn't one.

## Part 1: Is the environment ready?

Resolve the wiki root, in this order, and report which source won:

1. `PINKY_WIKI_ROOT` environment variable
2. `.wiki_root` file in this directory
3. `wiki.root` in `wiki_scope.yaml`

The run these checks and report pass/fail for each. **Quote every path - it contains spaces.**

1. **Wiki root exists** - does the resolved directory exist and is it readable?
2. **Layout matches `wiki_scope.yaml`** - for each entry in the `layout` block, does the path exist? Report anything mssing or unexpected. An empty directory is a pass with a note, not a failure.
3. **Wiki's own instructions present** - is there a `CLAUDE.md` at the wiki root? Note its `updated`/modification date. If it's changed since `wiki_scope.yaml`'s conventions were recorded, the conventions may be out of date.
4. **QMD available** - call `mcp__plugin_qmd_qmd_status`. Check that the collection named in `search.qmd.collection` exists and its `path` resolves to the same directory as the wiki root. These can be spelled differently and still be the same directory: status reports the canonical path, while `wiki.root` may reach it through a symlink. Compare resolved paths (`realpath`), not strings, and consult `wiki.canonical_root` before reporting a mismatch.
5. **QMD index freshness** - compare the collection's `lastUpdated` against the newest markdown file in the wiki:
    ```bash
    find "$WIKI" -name '*.md' -newermt "<lastUpdated date>" -not -path '*/.obsidian/*'
    ```
    If files are newer than the index, the index is stale - semantic search will miss them. Say so and name them. Also report `needsEmbedding` and `hasVectorIndex` from the status call.

If QMD is unavailable or stale, that is a **degraded pass*, not a failure - skills fall back to `Grep`/`Read`. Say clearly what capability is lost (semantic/HyDE search; keyword search still works).

## Part 2: Corpus audit

Count and report, comparing against `wiki_scope.yaml`'s layout:

- **`raw/** - markdown count and PDF count, listed separately. **PDFs are invisible to QMD** (it indexes `**/*.md`), so note how many sources are search-invisible.
- **`wiki/concepts/`**, **`wiki/sources/`** - page counts.
- **Entities** - count pages by `type: entity` in frontmatter, not by directory. This wiki has no `wiki/entities/` directory; entity pages live in `wiki/concepts/`. Report concept and entity counts separately so they don't double-count. If a `wiki/entities/` directory ever appears, count it too and flag the change as a layout deviation.
- **`outputs/** - report count, and the date of the most recent lint report.
- **Total markdown** - and whether it reconciles with QMD's document count for the collection. A mismatch means the index is stale or the pattern excludes something.

### Ingestion coverage

Every file in `raw/` should have a corresponding source summary. Cross-check by reading the `sources:` frontmatter of every page in `wiki/sources/` and comparing against a recursive inventory of documents in `raw/` (excluding attachments). Run from the Pinky workspace; install PyYAML if unavailable:

```bash
python3 scripts/source_paths.py "$WIKI/wiki/sources"
```

The helper parses the complete YAML `sources` list. If unrelated malformed YAML prevents parsing, it recovers only a simple block list under `sources:` and emits a warning. Unsupported source syntax fails explicitly; never report a complete audit after a failure.

Report:
- How many `raw/` documents are cited by at least one source summary
- Which `raw/` documents are cited by **none** - these are un-ingested. List them.

Skip `raw/attachments/` - those are supporting assets, not sources.

### Frontmatter integrity

Spot-check that every page in `wiki/concepts/` and `wiki/sources/` has the required frontmatter fields from `wiki_scope.yaml` (`title`, `type`, and on content pages `sources`, `related`, `created`, `updated`, `confidence`). Report any page missing fields, and any `confidence` value outside the allowed set.

## Part 3: Report

Give a compact summary:

```
Config: wiki_scope.yaml / missing (cp from .example) / N placeholders unfilled
Wiki root: <path> (resolved from: env / .wiki_root / wiki_scope.yaml)
Reachable: yes / no
Layout: yes / no (any deviations)
QMD: fresh / stale (N files newer than index) / unavailable
Corpus: N raw md + N raw PDF | N concepts | N sources | N entities | N outputs
Ingestion: N/N raw docs ingested (list any missing)
Frontmatter: yes / N pages with issues
```

Then the detail for anything that isn't a clean pass, with the fix.

If a check fails, suggest `/pi-env-config` for path/setup problems, or the specific `qmd` reindex step for index problems.

Do NOT reindex, clone, fetch, write, or modify anything. This is an audit only. If findings are worth keeping (a new un-ingested source, a structural change in the wiki), tell the user and offer to record them in `docs/WIKI_COVERAGE.md` - don't write silently.
