# Undisassembled regions in BAS HTML

> Trail, 2026-10-16. Chapter 17. Forced disassembly does not name them. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## What is there

165 runs of more than 20 consecutive `??` lines. The largest are thousands of lines. Many begin with `C8` (ENTER) or `90` (NOP).

Example — Code94 at `12e8:0000`:

```
C8 CA 00 00   ENTER 0xCA, 0
57            PUSH DI
56            PUSH SI
```

This is a normal function prologue. Ghidra left it as undefined because analysis never flowed into the segment.

## Why it happened

The unpacked BAS image still carries Optloader segment-table artifacts (nonsense lengths and flags on some segments). Ghidra's NE loader did not create entry points or flow into every code segment. The HTML reflects that incomplete analysis.

## How to resolve

Three practical options, in order of cost:

1. **Ghidra script.** Walk the listing, find `C8` bytes that are currently undefined, and call `disassemble` + `createFunction` at each. This recovers the ENTER-prologue functions without manual work. One script covers all 165 runs.

2. **Manual force.** In the Listing view, select a `??` run, press D (Disassemble). Repeat for the large runs. Slow, but confirms the script is finding real code.

3. **Different disassembler.** A tool that does not rely on the NE entry table (or that re-analyzes after a full clear) may cover more. The Ghidra NE-loader patch already fixed the signed-segment and entry-table-size bugs; a re-analysis after clearing the previous results is the cheapest test.

## What it is not

These regions are not automatically the 14 00 00 reader. They are simply code that was never disassembled. Until they are turned into functions, any search that only looks at the HTML will miss them.

## Status

Open. The largest runs are real code (ENTER prologues). A Ghidra script that forces disassembly on undefined `C8` sites is the lowest-cost next step.
