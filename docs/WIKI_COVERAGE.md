# Wiki coverage

The durable coverage map and standing gap list. Updated by `/pi-gap-audit`. The dated audit files in `investigations/` hold the evidence; this file is the summary.

**Last audit:** [2026-09-28](investigations/2026-09-28-gap-audit.md). A Max 9 ingest was in progress during that audit.

## Coverage by domain

Domain groupings follow `wiki_scope.yaml`, collapsed from `wiki/index.md`'s ~30 sections.

| Domain | Evidence base | Depth | Weak spots |
| ------ | ------------- | ----- | ---------- |
| Music Theory | OMT (cited by 83 concept pages), Music Theory for Dummies, Thinkspace, Wikipedia (neo-Riemannian, Tonnetz) | Deep; 10 OMT part maps plus detail pages | No voice-leading / part-writing page |
| Composition & Orchestration | Music Composition for Dummies (25 concept cites), 10 Tips PDF, 6 Composing Academy newsletters, 2 personal notes | Medium | **The least-evidenced domain.** Cinematic claims rest on newsletters and uncited notes. No leitmotif, spotting or trailer-structure pages. Two raw sources contain errors the wiki reproduced |
| Electronic Production | 4 personal notes (ambient techno ×2, dub techno, synthwave), 1 tips note | Medium | Every page rests on uncited personal notes. Mixing, mastering and loudness are thin (`[[gain-staging]]` only) |
| DAW & Hardware - Ableton | Live 12 manual (48 concept cites), Push 3 manual, Max 9 User Guide (in progress) | Deep, but partial | Live Ch. 23–27 (Racks, Automation, Envelopes) never processed |
| Synths | DUNE 3, Falcon, Pigments, Serum 2 manuals | Deep per product | No synth-agnostic fundamentals hub. Falcon at category-level depth (chosen by the user) |

## Standing gap list

Everything below is a recommendation for the wiki's own agent; pinky doesn't apply it. Numbers refer to the 2026-09-28 audit.

| Gap | Kind | Severity | First seen | Status |
| --- | ---- | -------- | ---------- | ------ |
| Rings of Power *Main Titles* credited to McCreary (composed by Shore) (#1) | Truth | High | 2026-09-28 | open |
| Chromatic-mediant common tone wrong (the shared tone is C, not A) (#2) | Truth | High | 2026-09-28 | open |
| Phantom `raw/Write Dark, Delicate…pdf` path on 3 pages (#3) | Provenance | Medium | 2026-09-27 (env-check) | open |
| `[[god-chords]]` overstates an uncited note; Shepard example wrong (#4) | Truth | Medium | 2026-09-28 | open |
| Synthwave "kick and snare on 1 and 3" (#5) | Truth | Medium | 2026-09-28 | open |
| Live 12 Ch. 23–27 unprocessed (#6) | Ingestion | Medium | 2026-09-28 | open |
| No synthesis-fundamentals hub (#7) | Depth | Medium | 2026-09-28 | open |
| No voice-leading page (#8) | Depth | Medium | 2026-09-28 | open |
| Mixing / mastering / loudness thin (#9) | Depth | Medium | 2026-09-28 | open; needs a new raw source |
| No leitmotif / film-scoring craft pages (#10) | Depth | Medium | 2026-09-28 | open |
| 10 pages with frontmatter that isn't valid YAML (#11) | Structural | Medium | 2026-09-27 (env-check) | open |
| Max 9 LOM and JS API not ingested (#12) | Ingestion | Low | 2026-09-27 (env-check) | in progress |
| Falcon category-level depth (#13) | Ingestion | Low | 2026-09-28 | chosen by the user |
| Composer entities single-source (#14) | Depth | Low | 2026-09-28 | caveated |
| `comparison` type unused (#15) | Structural | Low | 2026-09-28 | open |

## Deliberately not gaps

See the audit's "Not findings". In short: short `omt-part*` / `mcd-part*` chapter maps, Music Theory for Dummies' low citation count (deduplicated on purpose), the absent `wiki/entities/` directory, and sidechain compression (well covered).
