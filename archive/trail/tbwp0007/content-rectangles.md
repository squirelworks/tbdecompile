# Content rectangles — confirmed (2026-10-14)

> Trail, 2026-10-16. Chapters 5 and 13.1. Bounds-only, marker 01 00 00 04. If this sheet and `TBdecompile/record/` disagree, the record wins.

Yes. Content rectangles are bounds-only records.

## Pattern

In the page blob:
```
left top  right bottom  00 00 00 00  fill_color  01 00 00 04
```

- Four words: left, top, right, bottom (twips).
- Fill color dword (0xC0C0C0 silver for pins, 0x404040 dark gray for bodies).
- Screen = twips / 15.

## Evidence

P1040 (9e954d01.tbk, file 0x19C03A):
- 28 pin records, each a bounding box + fill.
- 2 body rectangles.
- No 11-point vertex lists. The tip shape is expanded at paint time.

## Renderer path

1. Walk the page blob for the four-word + fill pattern.
2. Scale by /15.
3. Draw the rectangle with the fill color.
4. For pins, optionally expand the tip from the bounds (the live paint does this).

No further format research is needed for playback of content rectangles.

## OpenScript engine update

`openscript_analysis/tbk/openscript_analysis/engine.py` now handles:

- `send NAME to TARGET`
- `get FUNC(ARGS)` as a call action
- `forward to TARGET`
- `break NAME`
- `PROP of TARGET` (property read placeholder)
- `local` / `system` declarations (ignored)

These cover the patterns seen in quiz1, learn1, train1, and activeX handlers.
