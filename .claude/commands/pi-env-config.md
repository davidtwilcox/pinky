---
name: pi-env-config

description: Configure the wiki path and search index - runs env-check first, then repairs the wiki root, layout mapping, and QMD collection as needed.

---

# Environment config

Set up or repair this workspace's connection to the LLM wiki. This configures **Pinky**; it never modifies the wiki.

## Step 1: Bootstrap the config if it's missing

`wiki_scope.yaml` is gitignored - a fresh clone starts without one. If it doesn't exist, create it from the tracked template:

```bash
cp wiki_scope.yaml.example wiki_scope.yaml
```

Then walk the user through `<angle_bracket>` placeholders. Read the template first - it documents every field inline, including which keys to delete when they don't apply.

Ask for the essentials rather than making the user edit YAML:

1. **`wiki.root`** - where the wiki lives. Validate it before writing (see Step 3). Required.
2. **`wiki.name`** - what to call it. Cosmetic
3. **`wiki.storage`** - `local` only for this version of **Pinky**
4. **`search.qmd.collection`** - if QMD is in use. Get the real name from `mcp__plugin_qmd_qmd__status` rather than asking the user to recall it; if a collection already indexes the wiki root, use its name and say so. Delete the whole `qmd` block if they aren't using QMD.
5. **`wiki.canonical_root`** - only if `wiki.root` goes through a symlink. Resolve it yourself with `realpath` instead of asking. Delete the key otherwise.
6. **`wiki.agent_instructions`** - if the wiki has its own agent instructions file, name it. Check for a `CLAUDE.md`/ `AGENTS.md` at the wiki root and offer what you find. Delete the key otherwise.

Then reconcile `layout`, `conventions`, and `domains` against the wiki as it actually is - that's Step 4, and on a first run it matters more than usual, since the template's defaults describe an expected shape rather than the user's real one.

Leave `access: read-only` alone. Changing it is a deliberate decision the user has to raise explicitly; don't offer it.

## Step 2: Run env-check

Run `/pi-env-check` as a prerequisite. If everything passes, say so and stop - there is nothing to configure. Otherwise use its findings to drive the steps below.

## Step 3: Wiki root

If the wiki root doesn't resolve, or the user wants to point at a different wiki:

1. Ask where the wiki lives. Offer the current `wiki.root` from `wiki_scope.yaml` as the default, unless it's still an unfilled placeholder.
2. Verify the path exists and looks like the wiki - it should contain a `wiki/` directory with an `index.md`, and a `raw/` directory. If it doesn't, say what's missing and ask again rather than accepting a wrong path.
3. Write the confirmed path. On a first-run bootstrap, put it in `wiki_scope.yaml` as `wiki.root` - the file is gitignored, so there's no leak and no conflict. To point *this checkout* somewhere else without touching the config, write `.wiki_root` instead (one line holding a raw path).

Both files are gitignored, so neither choice publishes a local path. `.wiki_root` is the narrow override - reach for it when the config is otherwise correct and you only want to redirect the root.

**Symlink note:** if the path goes through a symlink, resolve the real path with `realpath` and record it as `wiki.canonical_root`. QMD's status output reports the canonical form; having both written down prevents "two different paths" confusion later. Note this is separate from QMD *result* paths, which are collection-prefixed and slugified - see `docs/WIKI_RETRIEVAL.md`.

## Step 4: Layout and conventions

If env-check reported layout deviations - a directory in `wiki_scope.yaml` that no longer exists, or a directory in the wiki that isn't in the config - or if this is a first-run bootstrap, where the template's defaults are assumptions rather than observations:

1. Read the wiki's own agent instructions (`wiki.agent_instructions`, if set) - they define the authoritative structure and page conventions.
2. Reconcile `wiki_scope.yaml`'s `layout`, `conventions`, and `domains` blocks against what the wiki actually contains now. Read `wiki/index.md` for the current domain groupings, and check the real frontmatter on a few pages rather than trusting the template's contract.
3. Update `wiki_scope.yaml` to match, and tell the user what changed.

The wiki's own instructions win any conflict. `wiki_scope.yaml` is Pinky's cached map of them, not a competing definition.

## Step 5: QMD collection

If env-check reported QMD unavailable or stale:

**Collection missing** - the wiki isn't indexed. Point the user at the `qmd` skill to add a collection over the wiki root with pattern `**/*.md`, then re-run `/pi-env-check`. Don't guess at qmd's config file format; invoke `/qmd` or ask.

**Collection present but pointing elsewhere** - if the collection path and the wiki root are genuinely different directories (not just symlink-vs-canonical spellings of the same one), report the mismatch and ask which is correct before changing anything.

**Index stale** - files are newer than `lastUpdated`. Tell the user which files, and that a reindex is needed for semantic search to see them. Keyword search via `Grep` is unaffected in the meantime.

**Collection name differs** - if the indexed collection is named something other than `search.qmd.collection`, update that value in `wiki_scope.yaml`.

## Step 6: Confirm

Re-run `/pi-env-check` and show the summary. Report what you changed:

- Files written in this workspace (`.wiki_root`, `wiki_scope.yaml`)
- What still needs the user's hand (a qmd reindex)

State explicitly that nothing in the wiki was touched.
