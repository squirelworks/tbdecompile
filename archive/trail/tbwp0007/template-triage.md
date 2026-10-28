# Template and documentation triage (2026-10-14)

> Trail, 2026-10-16. Chapter 15. Templates are not the NIDA playback path. If this sheet and `TBdecompile/record/` disagree, the record wins.

Large batch of ToolBook II Instructor 8.x files. Ranked by value for the NIDA courseware reverse-engineering work.

## Ranking

### Tier 1 — High value (process soon)

| Item | Why |
|------|-----|
| `Tb80os.pdf` (Programming in OpenScript, 372 pp) | Language reference. System books, handlers, message hierarchy, DLL linking, debugging. Directly supports OpenScript corpus and engine work. |
| `inst80UG.pdf` (Instructor User Guide, 774 pp) | Architecture, system books, authoring concepts, object model. Background for NIDA shell behavior. |
| `blank.tbk` | Minimal book. JBO at 0xE00. Baseline for format comparison. |
| `default.tbk` / `defaulth.tbk` | Single-page generic template. JBO at 0xC00. Clean structure. |
| `quiz1.tbk` / `quiz1h.tbk` / `quiz1i.tbk` | Quiz template. Multiple-choice objects. Closest to NIDA assessment pages. |
| `learn1.tbk` / `learn1h.tbk` / `learn1i.tbk` | Advanced training template. Skill-mastery structure. |
| `train1.tbk` / `train1h.tbk` | Basic training (objectives, explanation, example, quiz). |
| `activeX.tbk` / `actxexpl.tbk` | ActiveX support examples. Limited authoring surface mentioned earlier. |
| `Quizbldr.tbk` + `Quizbldr.pdf` | Quiz Builder. Specialized quiz objects. |
| `tbkcache.ini` | Template catalog index. Maps names to descriptions. |

### Tier 2 — Useful later

| Item | Why |
|------|-----|
| `catalog.tbk` / `catalogh.tbk` | Product catalog template. Object catalog system. |
| `present.tbk` / `presenth.tbk` | Presentation template. Bullet-point structure. |
| `generic.tbk` / `generich.tbk` | Basic content. Few built-in features. |
| `gen1ch.tbk` / `gen2ch.tbk` (+ h variants) | Advanced content, 1- and 2-chapter. |
| `Walkthrough.tbk` | Large (1.3 MB). Likely tutorial. JBO at 0xE00. |
| `scrwalk.tbk` | Screen walkthrough. JBO at 0xC00. |
| `chewbyte.tbk` | Unknown purpose. JBO at 0xE00. Inspect if time. |
| `Profiler.pdf` | Profiler guide. Low priority for playback. |
| Catalog cache books (`Catalog Blank Cache.tbk` etc.) | Object catalog internals. Authoring path. |

### Tier 3 — Low priority for NIDA

| Item | Why |
|------|-----|
| `hr.tbk` / `hrh.tbk` | Employee handbook template. Content example. |
| `roi.tbk` / `roih.tbk` | Business plan template. |
| `sales1.tbk` / `sales2.tbk` (+ h) | Sales training. Content examples. |
| `simquiz.tbk` / `simquizh.tbk` | Basic quiz variant. Redundant with quiz1. |
| `ppointi.tbk` | PowerPoint + quiz HTML. Export target. |
| HTML variants (`*h.tbk`, `*i.tbk`) | HTML export shells. Less relevant for native TBK format. |
| `TBKSLICE.DLL` | Supporting DLL. Not core engine. |
| `TBKMMWID.FON` | Font. Supporting. |
| `qb_corpr.tbk` | Unknown. Low priority. |

## Format notes

- JBO signature (`03 4A 42 4F 01 00 00 08`) appears at **0xC00** or **0xE00** depending on stub size.
- `blank.tbk`, `chewbyte.tbk`, `activeX.tbk`, `Quizbldr.tbk`, `Walkthrough.tbk` use the larger stub (JBO at 0xE00).
- Most templates use the standard 0xC00 stub.
- All are ToolBook II 8.x books. No new format variants observed.

## Recommended processing order

1. Extract OpenScript handlers from `quiz1.tbk`, `learn1.tbk`, `train1.tbk`, and `default.tbk` using the existing decoder. Compare against NIDA lesson handlers.
2. Skim `Tb80os.pdf` chapters 5 (messages/objects/properties) and 13 (DLLs) for system-book and hierarchy details.
3. Inspect `activeX.tbk` for ActiveX object records. Note any new 14 00 00 subtypes.
4. Park the rest. HTML variants and content templates add little to the NIDA playback path.

## File locations

All attachments are under `/workspace/attachments/`. PDFs: `inst80UG.pdf`, `Tb80os.pdf`, `Quizbldr.pdf`, `Profiler.pdf`.
