# Wiki retrieval

What works for searching this corpus.

## QMD

- Collection `Research`, pattern `**/*.md`. It indexes `raw/*.md`, `wiki/**`, `outputs/**`, and the wiki's `CLAUDE.md` / `AGENTS.md`.
- **Not indexed:** every PDF in `raw/`, which is 21 of 29 sources. A PDF's content is reachable through QMD only via its source summary and the concept pages built from it.
- Classify hits by path prefix: `raw/` = evidence, `wiki/` = derived, `outputs/` = point-in-time report.

## Reading PDFs directly

`pdftotext` (Homebrew) works on every `raw/*.pdf` checked so far. Use it when a claim traces to a PDF:

```bash
pdftotext "$WIKI/raw/<file>.pdf" - | grep -n -i -A3 '<term>'
```

It's the only way to check unprocessed chapters, such as Live 12 Ch. 23–27.

## Shell gotchas on this machine

- `find` is aliased to `bfs`. `-newermt` needs an ISO-8601 timestamp (`2026-09-26T19:50:13Z`); strings like `"2026-09-26 19:50:13 UTC"` are rejected.
- The shell is zsh: an unquoted `===` at the start of a word triggers `=cmd` expansion and fails. Quote separators in `echo`.
- The wiki root contains no spaces at present (`/Users/bender/Documents/Research`), but many `raw/` filenames do. Always quote.

## Parsing frontmatter

Use a real YAML parser (`python3` + PyYAML) for frontmatter checks, but expect 10 pages to fail (see [WIKI_PROVENANCE.md](WIKI_PROVENANCE.md)). For coverage, use `python3 scripts/source_paths.py <source-page-directory>` from the Pinky workspace. It parses the full `sources:` list and, when other malformed frontmatter blocks YAML parsing, recovers a simple source block with an explicit warning. Unsupported syntax fails rather than silently producing partial coverage. Fixed-window grep extraction can capture neighboring lists and truncate long source lists.
