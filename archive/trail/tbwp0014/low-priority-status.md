# Low-priority open items — status

> Trail, 2026-10-16. Chapter 10. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## Closed or not actionable

| Item | Result |
|------|--------|
| PHYSSIZE index | Already closed. Not in these 8.1 books. |
| Author-side binaries (TB80EDT, TB80.EXE) | Absent from the tree. Cannot resolve without the files. |
| FPU/math dispatcher (1008:2dc7) | Filed. Stays in segment 1008. Not the book path. |
| BAS segment 182 leftover | Real preload code, no static entry points. Packing artifact. Note already written. |

## TB80RCR

Present. Exports blit, message, and alloc helpers. The four "RCR" hits in the BAS decompile are `HEAPENTERCRITSECT` / `TBHEAPCLEARCRITSECT` — string matches, not calls. RCR is a supporting module for record/resource operations. It is not on the book-open or page-paint path by any static reference in BAS.

## What the user can do

- Author-side: if a copy of TB80EDT.DLL or TB80.EXE appears, drop it in. Otherwise this stays closed.
- Segment 182: if a runtime trace ever lands in BAS segment 182, disassemble it then. No static reason to do it now.
- RCR: ignore for the book-open goal. It is media/record support.

## Next

Moving up to medium-priority items: remaining draw-object layouts, system-book scripts, OpenScript token map, picture-binding ids.
