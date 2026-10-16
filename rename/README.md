# Rename scripts and nameable lists

> Trail, 2026-10-16. Scripts and nameable lists. A name is a location. It is not a claim about when the function runs. If this file and `TBdecompile/record/` disagree, the record wins.

Ghidra rename scripts and pattern-based nameable function lists for the ToolBook 8.1 modules.

## Scripts

- `RenameBas.java` / `rename_bas.py` — PaintPolygon, ScaleTwipsToScreen, SetProperty, SetPointArray
- `RenameRtm.java` / `rename_rtm.py` — PaintPageRect, SendMessageHelper
- `RenameBmp.java`, `RenameCmp.java`, `RenameUtl.java`, `RenameW16.java`, and the rest

## Lists

- `bas_nameable.tsv` (650 entries), `rtm_nameable.tsv`, `toolbook_naming_progress.md`
- Summary: ~17.5% nameable by pattern across 8 modules; 112 confirmed renames

Full scripts and TSVs are in the local TBdecompile/rename/ tree.
