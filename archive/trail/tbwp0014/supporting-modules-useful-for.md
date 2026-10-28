# Supporting modules — what is useful for other goals

> Trail, 2026-10-16. Chapter 17. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## Not the book engine

None of F32L, FLT, JPG, LNL, NET, OCX, RUN, UTL, W16, W32, zlib hold the 14 00 00 reader or the PaintPolygon type table. That is settled.

## What is still useful

| Module | Useful for | Why |
|--------|------------|-----|
| TB80W16 | Script-to-object command bus | `DoCmdDraw`, `DoCmdLoad`, `DoCmdOcxLoadPicture`. The nearest script-side paint entry. When a handler does something visual, it goes through here. |
| TB80LNL | Media in lessons | MCI, wave, MMIO. Any NIDA lesson that plays a clip goes through LNL. Not page objects. |
| TB80JPG | JPEG pictures | Real JPEG path (`JPEG_CREATE_COMPRESS` etc.). Separate from the BAS/BMP bitmap path. |
| TB80OCX | OLE-embedded pictures | `OCXLOADPICTURE`. Out of NIDA scope for now, but it is the other picture loader. |
| TB80RUN / TB80NET | Launch seam | Confirms 32-bit RUN spawns 16-bit NET with the book on the command line. Already noted. |
| TB80UTL | Object-type table | Already extracted (ComboBox, Stage, Picture, Polygon, Field, Button, Page, Book). |
| TB80FLT | Common controls | Sliders, bitmap buttons. Not page geometry. |
| TB80F32L / W32 / zlib | Thunk / compression | Supporting only. zlib is from the cour1 menu, not ToolBook. |

## Minor successes

- W16's `DoCmdDraw` is a confirmed script-side entry into the paint path. It does not itself parse 14 00 00 records, but it is the command the editor and runtime use to ask an object to draw.
- JPG and OCX are the two picture loaders outside BAS. The carved BMPs in the course books are the BAS/BMP path; JPEG and OLE pictures are these.
- LNL is the media path. If a lesson has a clip, this is where it goes.

## Not worth more static time

F32L, FLT, W32, zlib. They do not touch page records, bounds, or painters.

## Status

Supporting modules are classified. The book-engine questions remain in TB80BAS (record reader) and the runtime-built type table (painter dispatch).
