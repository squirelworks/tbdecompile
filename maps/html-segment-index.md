# HTML export segment index

> Trail, 2026-10-16. Lookup. The HTML export's segment table. Not a finding. If this file and `TBdecompile/record/` disagree, the record wins.

Two tables that had been sitting at the artifacts root, next to no note. They are a lookup from Ghidra HTML exports, not a narrative and not a live selector map.

| File | What it is |
|---|---|
| `html-ne-index.tsv` | One row per HTML dump: segment count, entry NE segment, the Ghidra base that dump used, entry IP, autodata. |
| `html-ne-segments.tsv` | The longer table behind that index. |

The bases in these files are whatever that Ghidra session assigned. They are not the NE-to-Ghidra maps in `bas-ne-to-ghidra.md`, `rtm-ne-to-ghidra.md`, and `wdw-to-ghidra.md`, and they are not a selector from a boot. If a number here and a number in those three files disagree, those three files are the ones the record uses.

A row is a location. It is not a claim about the record reader.
