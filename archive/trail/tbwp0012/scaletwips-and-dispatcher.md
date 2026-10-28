# ScaleTwips Call Sites + Type Dispatcher Notes

> Trail, 2026-10-16. Chapters 4 and 5. FUN_1008_01dd and the type dispatcher. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14  
Source: `/workspace/attachments/TB80BAS.DLL.html`

## ScaleTwipsToScreen call pattern

Most of the 21 sites follow the same pattern:

```
PUSH AX          ; or word ptr [BP+...]
PUSH 0x2         ; count of coordinate pairs
CALLF 1008:01dd  ; CDBSCALETWIPSTOSCREEN
```

Sample sites with context:

- 1010:1c44 / 1ce6 / 1d8c — push AX, push 2, call; then load from DAT_1630_01e0 + 0xa8
- 1010:3a75 — push word from stack, push 2, call
- 1018:055f — push word [BP+8], push 2, call; then push several locals
- 1018:05e3 — push AX, push 2, call; then LES BX and push ES:[BX+6]
- 1020:09c6 / 1a28 — push AX, push 2, call

The call is always far to segment 1008 offset 01dd. The second argument is almost always the constant 2 (two coordinates).

## Type dispatcher / PaintPolygon path

- `CDBPAINTPOLYGON` is defined at 1408:0376. Its header XREFs are only internal locals.
- No direct named CALL/CALLF to the function start appears in the listing.
- A large switch (148 cases) lives at 1008:2dc7. Cases jump within the 1008 segment; none of the sampled case labels reference the 1408 segment.
- Prior SoftICE notes placed the type dispatcher at BAS segment 0x7E (selector 3617 that boot), which calls the generic draw at segment 0x5B. That matches the pattern of a table-driven dispatch rather than a direct call visible in the HTML XREF list.

The polygon painter is reached through a function-pointer table indexed by object type, not by a named near call that Ghidra's HTML export listed as an XREF.

## Status

- ScaleTwips call pattern is uniform (push coords, push count=2, far call).
- PaintPolygon has no external named callers in the HTML; the type table that reaches it is still not extracted as a data array in this listing.

Next possible cut: dump the data segment for a table of far pointers that includes 1408:0376, or walk the 148-case switch at 1008:2dc7 to see which cases call into other paint segments.
