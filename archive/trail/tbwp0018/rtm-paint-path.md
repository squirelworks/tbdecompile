# RTM paint path

> Trail, 2026-10-16. Chapters 3 and 5. CLIENTTOPAGE then ordinal 26. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## Paint handler

The first `BEGINPAINT` is in a window procedure. It:

1. Calls `BEGINPAINT` to get the DC and update rect.
2. Calls `ISRECTEMPTY` on the update rect.
3. If empty and a flag is set, calls `ENDPAINT`, clears the flag, calls `INVALIDATERECT`, and returns.
4. If not empty, calls `CLIENTTOPAGE` twice to convert client coords to page coords.
5. Calls `FUN_1168_0346`, `Ordinal_26` (`CDBPAINTCLIENT`), and `FUN_1070_0d40`.

`Ordinal_26` is `CDBPAINTCLIENT` in BAS. That is the handoff from RTM to the BAS paint path.

## Wrappers

`FUN_1070_0be0`, `FUN_1098_14fc`, and `FUN_1120_06da` are window procedures that handle `WM_PAINT` (0x0F). They call `BEGINPAINT` and `ENDPAINT`. The actual drawing is in BAS.

## Useful for graphics?

The RTM paint path is the window message handler. It converts client coords to page coords and calls `CDBPAINTCLIENT`. The shape drawing (polygon, arc, rect) is in BAS, not RTM.

For graphics rendering, the useful path is:

1. RTM `WM_PAINT` handler calls `CLIENTTOPAGE` then `CDBPAINTCLIENT`.
2. BAS `CDBPAINTCLIENT` walks the page objects and calls the type dispatcher.
3. The type dispatcher calls `PaintPolygon`, `PaintArc`, `PaintRectangle`, etc.

The RTM side is the window and coordinate conversion. The BAS side is the shape drawing.
