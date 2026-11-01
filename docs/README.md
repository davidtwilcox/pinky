# pinky Docs

Knowledge built up through investigation. `wiki_scope.yaml` is the source of truth for *where the wiki is and how it's laid out*; these docs cover *how the corpus behaves and what we've concluded from it*.

Question-scoped work lives in [investigations/](investigations/).

**These docs never reproduce wiki content.** The wiki is live, one directory away, and read-only from here - a copy in this repo would just be a stale copy. Docs cite wiki pages as `[[wikilinks]]` and evidence as `raw/<file>`.

## Naming

| Prefix | What it covers |
| ------ | -------------- |
| `WIKI_*` | How the corpus works - structure, retrieval, provenance, coverage |
| `SYNTHESIS_*` | Durable answers that span several wiki pages and exist as no single page in the wiki |

## Corpus knowledge

| Doc | What it covers |
| --- | -------------- |
| [WIKI_STRUCTURE.md](WIKI_STRUCTURE.md) | Start here - layout, the evidence / derivation split, page types, frontmatter contract, verified counts |
| [WIKI_RETRIEVAL.md](WIKI_RETRIEVAL.md) | How to search this corpus. QMD coverage and blind spots, when *not* to search, path-prefix classification |
| [WIKI_PROVENANCE.md](WIKI_PROVENANCE.md) | How claims chain back to evidence, source-summary naming (`-note`/`-wikipedia`/`-manual`, not `-source`), known provenance quirks, the lint's blind spots |
| [WIKI_COVERAGE.md](WIKI_COVERAGE.md) | Coverage map by domain and the standing gap list. Updated by `/pi-gap-audit` |

## Syntheses

## Investigations

See [investigations/README.md](investigations/README.md).