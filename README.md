# pinky

Investigation workspace for a research wiki. Not a software project - no build, no deploy. This is where you ask questions of the wiki, trace claims back to their evidence, find the gaps, and build up knowledge over time.

## What's Here

- **`wiki_scope.yaml.example`** - generic template for a fresh checkout; copy it to `wiki_scope.yaml` and fill in the placeholders.
- **`scripts/`** - source-path extraction and local validation helpers.
- **`wiki_scope.yaml`** - your local config: where the wiki lives and how it's laid out (directories, page types, the frontmatter contract, domains, search config).
- **`docs/`** - knowledge built up through investigations. Start at **`docs/README.md`**
- **`docs/investigations/`** - question-scoped work (gap audits, claim traces). Promoted durable learnings to `docs/`
- **`CLAUDE.md`** - instructions for investigation sessions in Claude Code
- **`AGENTS.md`** - the same instructions, harness-agnostic, for any other agent
- **`.claude/commands/`** - the skills, available as `/pi-*` slash commands

## The Wiki Is Read-Only

The wiki is an Obsidian vault with its own Claude instance, which owns ingestion, organization, querying and linting. **pinky never writes to it.**

Nothing is copied here either - the wiki is always read live from its configured location. This workspace is the second pair of eyes: it reads the wiki, checks the derived claims against the raw evidence behind them, and writes its findings to `docs/`. When an investigation concludes the wiki should change, that's a recommendation to hand to the wiki's own agent, not an edit to make.

## Prerequisites

- **Python 3 and PyYAML** - required for coverage extraction and local validation; install with `python3 -m pip install -r scripts/requirements.txt`. Bash and Git are required by the validator.
- **QMD** - the `qmd` MCP server with a collection indexing the wiki, named in `search.qmd.collection`. Optional; skills fall back to `Grep`/`Read`, at the cost of semantic search.

## Setup

**1. Configure and verify.** Open the workspace in Claude Code and run the commands below. With another agent, read the matching files in `.claude/commands/`.

- **`/pi-env-check`** - diagnostic: wiki reachable, page counts by type, QMD index freshness, ingestion coverage
- **`/pi-env-config`** - configure or repair the wiki path, layout mapping, and QMD collection; fixes whatever env-check flagged

`/pi-env-check` reports a missing config; `/pi-env-config` creates it from `wiki_scope.yaml.example` and walks through configuration.

`wiki_scope.yaml` and `.wiki_root` are gitignored; keep machine-specific paths in those files.

The wiki path resolves from `PINKY_WIKI_ROOT`, then a machine local `.wiki_root`, then `wiki.root` in `wiki_scope.yaml`.

**2. Review the agent instructions and corpus docs for your wiki.** Keep `AGENTS.md` and `CLAUDE.md` consistent when adapting investigation rules. Read it through and correct anything that doesn't match yours - it is the instruction file every session loads, so a wrong statement there misleads every investigation.
Specifically:

- **The QMD collection name** - update it to whatever indexes your wiki, or remove the QMD references if you aren't using it
- **The Wiki Root section** - configure any symlink-specific details for your environment. Always quote paths, since source filenames may contain spaces.
- **"The Wiki Is Read-Only"** - The `WIKI_*` docs are findings verified against *a specific* wiki - page counts, provenance quirks, coverage gaps. Inherited by a different wiki they are not merely stale, they are wrong, and the investigation loop treats them as known-good starting points. Either empty them to stubs and rebuild from your own `/pi-env-check` and `/pi-gap-audit` runs, or read each one and correct it before trusting it.

## Skills

| Command | What it does |
| ------- | ------------ |
| `/pi-env-config` | Configure the wiki path, verify the layout, check the QMD collection |
| `/pi-env-check` | Read-only diagnostic - wiki reachable, page counts by type, QMD index freshness |
| `/pi-investigate` | The core loop. Question -> search -> read -> verify against `raw/` -> cited answer -> capture findings |
| `/pi-claim-trace` | Provenance trace. Take a claim or page and chase it back through concept -> source summary -> `raw/` document, reporting exactly where support runs out |
| `/pi-gap-audit` | Coverage and quality audit. Un-ingested sources, thin concepts, stale claims, unsupported assertions. Complements the wiki's own lint rather than repeating it |

To install a skill into another workspace, copy the `.md` file:

```bash
cp .claude/commands/pi-claim-trace.md /path/to/other-project/.claude/commands/
```

> **Using a different LLM?** [`AGENTS.md`](AGENTS.md) is a harness-agnostic port of `CLAUDE.md` - same rules, nothing that assumes Claude Code's tooling. The skills files in `.claude/commands/` are plain Markdown prompts, so any agent can read one and follow it even without slash-command support. If your agent reads a differently-named file (`GEMINI.md`, `.cursorrules`), symlink or copy `AGENTS.md` to it.

## How It Works

1. Check `docs/` for what we already know
2. Read `wiki/index.md` to orient - it catalogs every page by domain
3. Search: QMD first, `Grep` as fallback. Classify every hit by path prefix - `raw/` is evidence, `wiki/` is LLM-derived
4. Follow load-bearing claims to the `raw/` document behind them
5. Answer with citations - `[[wikilinks]]` for pages, `raw/<file>` for evidence
6. Capture non-obvious findings back in `docs/`

Step 4 is the point of this workspace. The wiki's derived layer is generated; reading it back is not verification.

## Local validation

The audit helper and validator require Python 3 and PyYAML. Install the dependency in your Python environment, then run:

```bash
python3 -m pip install -r scripts/requirements.txt
python3 scripts/validate.py
```

Run validation after edits and before committing. A nonzero exit status means a check failed.

The validator checks required setup files, the generic config template, ignore rules, local inline Markdown links, shell-example syntax, and source-extraction fixtures. It does not read or modify the external wiki, execute shell examples, or contact QMD. External URLs, wikilinks, and Markdown anchor targets are not checked.

Coverage workflows use `scripts/source_paths.py` to read complete `sources:` lists. Malformed frontmatter produces a warning when a simple source block can be recovered; extraction errors exit nonzero without printing partial results. When copying a coverage workflow to another workspace, also copy `scripts/source_paths.py` and `scripts/requirements.txt`.
