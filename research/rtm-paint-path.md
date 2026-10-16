# RTM paint path

> Trail, 2026-10-16. Still the paint handoff, not the reader. The current statement is `record/05-graphics.md` and `record/03-runtime.md`.

WM_PAINT handler calls CLIENTTOPAGE then Ordinal_26 (CDBPAINTCLIENT).

Shape drawing is in BAS, not RTM. The type dispatcher and the painters (PaintPolygon, PaintRectangle, PaintArc) live in TB80BAS.

No 14 00 00 reader was found in the RTM triage.
