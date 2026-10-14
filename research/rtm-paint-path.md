# RTM paint path

WM_PAINT handler calls CLIENTTOPAGE then Ordinal_26 (CDBPAINTCLIENT).

Shape drawing is in BAS, not RTM. The type dispatcher and the painters (PaintPolygon, PaintRectangle, PaintArc) live in TB80BAS.

No 14 00 00 reader was found in the RTM triage.
