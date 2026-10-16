# Debugger notes (SoftICE / WDW)

> Notes of 12 October 2026. The current statement is `TBdecompile/record/`. A sentence here that calls the reader a caller of `CDBSENDCREATE` is not current. Export tables are locations, not a claim about when a function runs.

From field notes and the corrected breakpoint form.

## Correct breakpoint form

SoftICE and WDW do not load the MAP. Break on the ordinal or use the Ghidra space:offset as a lookup.

- BAS ordinal 51 is `CDBSENDCREATE`.
- Break form that worked: `BPX 12c8:00bc` (or the live selector for that segment).

## Cautions

- SoftICE and WDW stay on separate command cards. Do not mix.
- The 16-bit side only debugs cleanly on Win98. XP NTVDM is not the host.
- A breakpoint left set on PaintPolygon freezes SoftICE while scrolling.
- `/DUMP` writes the SoftICE console, not the address given.

## Confirmed live

- Polygon points: object+0x30 = count, object+0x32 = far pointer to twip pairs.
- Scale: DS:01A6 = 96 → screen = stored / 15.
- Arc geometry: four twip pairs at object+0x25. Fill at +0x18.
- Bracket: computed from bounds by segment 0x5B. Not stored points.
