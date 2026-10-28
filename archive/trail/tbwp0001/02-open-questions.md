# Open Questions and Next Steps

> Superseded, 2026-10-16. Chapter 10. The reader is still unnamed; the create-path wording in that note is superseded. Read `TBdecompile/record/` for the claim. This sheet is the trail.

**Date:** 2026-10-11

Prioritized by what unblocks a viewer that can place widgets and run the navigation the lessons actually use.

## Highest leverage

1. **Expand the property block.**  
   On disk: marker `80 65 00 05 00 02 02`, id, 32-byte name, then at +43 the block `14 00 00 01` + six words.  
   In memory (SoftICE, object 0 / P0): the same block appears as `14 00 00 11`.  
   Hypothesis: disk form is compacted; `CDBFILEOPEN` (TB80BAS ordinal 8) expands it and writes bounds at object+0xF.  
   Next: trace the open path far enough to see the write to +0xF, or dump a live object and a matching disk record side-by-side.

2. **Page / background index.**  
   The `80 65` markers are a heap of objects, not a display list. Parent, z-order, and which background a page uses are still missing.  
   Without this, a viewer can jump on `buttonClick ("P…")` but cannot lay out the page.

3. **OpenScript token map.**  
   `COMPILEREXPANDTEXT` (TB80CMP ordinal 3) is the oracle. Compile one known handler, expand it, and lock the opcode table.  
   Current decoder (`openscript_notes.md`) produces keywords that do not always match expected OpenScript; the 0x77/0x78 resources are the right tables, but the interpretation of the high-byte encoding still has gaps.

## Medium

4. **Picture and resource binding.**  
   Whole BMPs have been carved (641 unique pictures, 113 icons). Compressed DIBs, paint objects, and the shared chrome (the 581×157 gold plate) are referenced by ids that have not been tied back to page widgets.

5. **System-book scripts.**  
   `tb80r.sbk` and the four `nc81*.sbk` files are ordinary books. Decompiling their handlers will show the path manager, quiz helpers, and status-bar behavior the lessons call.

6. **Remaining draw-object layouts.**  
   Polygon (kind `04 00`) is solved, including the live painter in TB80BAS segment 0x82 and the twip scale. Arc, curve, and picture placement are only partially mapped.

## Lower / cleanup

7. Annotate `TB80RCR` exports and confirm whether it is on the lesson open path.  
8. Author-side binaries (`TB80EDT.DLL`, `TB80.EXE`) are absent; Author-level commands cannot be confirmed from this tree.  
9. Optloader leftovers: TB80BAS segment 182 bind at 0x129 is not among its five relocations.  
10. The 1.5 `PHYSSIZE` index does not appear in these 8.1 books; do not spend more time looking for it.

## What the existing viewers already approximate

The clean-room players (viewer2, Maybe2/4, runtime/, Brickwall) already:

- Walk `80 65` pages and extract text + quoted jumps.
- Decode enough OpenScript for `go to page` / `send next` / quiz logic on books that resemble Logic Families.
- Render polygons where the kind=`04 00` layout is known.
- Stub system-book services.

They deliberately do not re-implement the 16-bit engine. The gaps above are exactly the difference between those viewers and a page that looks like the original.
