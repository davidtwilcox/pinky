# AGENTS.md

Instructions for any agent working in this repo. [`CLAUDE.md`](CLAUDE.md) is the Claude Code companion. **Keep the two in sync** any change to investigation rules belongs in both.

## What is this?

**pinky** is a workspace for interrogating an LLM research wiki. It is not a software project - there is no build, no deploy. You use it to ask questions of the wiki, trace claims back to their evidence, find the gaps, and build up knowledge over time.

Everything starts from two places:

- **`wiki_scope.yaml`** - where the wiki lives and how it is laid out (directories, page types, frontmatter contract, domains, search config)
- **`docs/`** - knowledge we've built up through investigation: how the corpus behaves, and durable answers that span multiple wiki pages

When you ask a question, start by checking `docs/` for what we already know, then read the wiki live. If we learn something new, update `docs/`.

## The Wiki Is Read-Only

**This workspace never writes to the wiki.** Not to `raw/`, not to `wiki/`, not to `index.md`, not to `log.md`, not to `outputs`.

The wiki has its own Claude instance - see the `CLAUDE.md` at the wiki root - which owns ingestion, organization, querying and linting. pinky is the second pair of eyes: it reads, investigates, and writes its findings here in `docs/`.

When an investigation concludes the wiki *should* change (a missing concept, a stale claim, a broken provenance link), **write the recommendation into `docs/`, don't apply it.** Say so plainly to the user so they can take it to the wiki's own agent. If the user explicitly asks you to edit the wiki in a given session, that's their call - but never do it as a side effect of an investigation.

## Prerequisites
- **QMD** - the `qmd` MCP server, with a collection indexing the wiki (default: `Research`). Not strictly required; skills fall back to `Grep`/`Read`. Without it you lose semantic search.

Read and follow `.claude/commands/pi-env-check.md` to verify everything, or `.claude/commands/pi-env-config.md` to configure the wiki path from scratch.

## Config
If `wiki_scope.yaml` is missing, stop investigation and bootstrap it from `wiki_scope.yaml.example` using the environment-config workflow. The local config and `.wiki_root` override are gitignored.

## Wiki Root
The wiki is always read from its live location - nothing is copied into this repo. Resolve the path in this order:
1. `PINKY_WIKI_ROOT` environment variable
2. `.wiki_root` file in this directory
3. `wiki.root` in `wiki_scope.yaml`

**Paths may contain spaces.** Quote it in every shell command: `ls "$WIKI/wiki/concepts"`. QMD indexes the canonical path, so QMD result paths and your `ls` paths can look different while pointing at the same file. `wiki_scope.yaml` records both.

## The Investigation Loop
The core workflows: **find the pages -> read them -> verify against evidence -> capture what you learned**.

1. **Check `docs/` first** - start [`docs/README.md`](docs/README.md). [`WIKI_STRUCTURE.md`](docs/WIKI_STRUCTURE.md) tells you how the corpus is shaped, [`WIKI_RETRIEVAL.md`](docs/WIKI_RETRIEVAL.md) tells you which searches actually work on it.
2. **Read `wiki/index.md`** - it is the wiki's own catalog of every page by domain. It is cheap to read and orients you fast.
3. **Search** - QMD first if available (keyword and semantic search, then retrieve the hit), native text search and file reading as fallback. Classify every hit by path prefix before you trust it: `raw/` is evidence, `wiki/` is derived, `outputs/` is a point-in-time report.
4. **Read the pages** - concept pages for the synthesis, source summaries for what a specific document said.
5. **Go to the evidence** - a claim on a concept page is only as good as the `raw/` document behind it. Follow the `sources:` frontmatter. Don't stop at the derived layer when the question is "is this true?".
6. **Answer with citations** - cite wiki pages as `[[wikilinks]]` and evidence as `raw/<file>` paths, so the answer can be re-checked.
7. **Capture what you learned** - If you discovered something non-obvious, update the relevant doc in `docs/`, or create a new one in `docs/`.

## Docs
Two tiers of documentation, same split as the source pattern:

**`docs/`** - durable knowledge. How the corpus behaves, and syntheses that span multiple wiki pages. These are living documents. **Any time you learn something non-obvious about the wiki**, check whether the relevant doc covers it - if not, add it. Don't wait to be asked.

**`docs/investigations/`** - question-scoped work. One file per question: gap audits, contradiction hunts, "does the wiki actually support X". The investigation doc stays as a record of the work; promote durable learnings up into `docs/`.

### Doc naming convention
Docs in `docs/` are **prefixed by kind**, so an `ls` groups them:

| Prefix | What it covers |
| ------ | -------------- |
| `WIKI_*` | How the corpus works - structure, retrieval, provenance, coverage |
| `SYNTHESIS_*` | Durable answers that span several wiki pages and don't exist as a single page in the wiki |

`docs/investigations/` uses `YYYY-MM-DD-short-slug.md` for dated runs (gap audits) and bare `short-slugs.md` for ongoing threads.

**Read [`docs/README.md`](docs/README.md) first** - it indexes every doc.

### What not to capture
Don't restate wiki content in `docs/`. The wiki is one directory away and always live; a copy here is just a stale copy. `SYNTHESIS_*` docs are for answers the wiki doesn't hold in any single page - and they cite the wiki rather than reproducing it.

The bar for `docs/`: **would this save someone some time in a future investigation?**

Things worth capturing:
- A retrieval tactic that works on this corpus (or one that looks right and fails)
- A provenance quirk - a claim whose evidence doesn't say what the page says it does
- A structural gap: un-ingested sources, orphan pages, an unused page type
- A cross-page synthesis that took real work to assemble
- A correction to something already in `docs/`

## Skills (Slash Commands)
Workflows live in `.claude/commands`. Read and follow the corresponding Markdown file; slash-command support is optional. Adapt tool names to the current harness.

| Command | What it does |
| ------- | ------------ |
| `/pi-env-config` | Configure the wiki path, verify the layout, check the QMD collection |
| `/pi-env-check` | Read-only diagnostic - wiki reachable, page counts by type, QMD index freshness |
| `/pi-investigate` | The core loop. Question -> search -> read -> verify against `raw/` -> cited answer -> capture findings |
| `/pi-claim-trace` | Provenance trace. Take a claim or page and chase it back through concept -> source summary -> `raw/` document, reporting exactly where support runs out |
| `/pi-gap-audit` | Coverage and quality audit. Un-ingested sources, thin concepts, stale claims, unsupported assertions. Complements the wiki's own lint rather than repeating it |

**Recognizing when to use a skill:** - if the user asks "does the wiki actually say that?" or "where did this come from?", offer `/pi-claim-trace` rather than manually grepping. If they ask "what's missing?" or "what should I ingest next?", offer `/pi-gap-audit`.

To install a skill into another workspace, copy the `.md` file:

```bash
cp .claude/commands/pi-claim-trace.md /path/to/other-project/.claude/commands/
```

## Workspace maintenance

- Bootstrap missing local configuration from `wiki_scope.yaml.example`, then configure it against the live wiki. Keep `wiki_scope.yaml`, `.wiki_root`, and `.claude/settings.local.json` out of commits.
- Install helper dependencies with `python3 -m pip install -r scripts/requirements.txt`.
- Run `python3 scripts/validate.py` after changing prompts, documentation, configuration templates, or helpers, and before committing. It checks local files only; it does not validate the live wiki or QMD.
- For ingestion coverage, use `scripts/source_paths.py` on the source-page directories instead of fixed-window grep. Review recovery warnings and resolve extraction failures before reporting complete coverage.
- Keep setup instructions in `README.md` current. When copying coverage workflows elsewhere, include `scripts/source_paths.py` and `scripts/requirements.txt`.

## Conventions
- **`wiki_scope.yaml` is the source of truth** for where the wiki is and how it's laid out update it when the wiki's shape changes
- **The wiki is read-only** - findings go in `docs/`, recommendations go to the user
- **Never copy wiki content into this repo** - reference it live, cite it by path
- **Quote paths** - roots and source filenames may contain spaces
- **Separate evidence from derivation** - `raw/` is what a source said; `wiki/` is what an LLM concluded. Never present the second as the first
- **Cite everything** - `[[wikilink]]` for pages, `raw/<file>` for evidence
- **Keep docs current** - when you learn something that contradicts or extends what's written, update the doc
