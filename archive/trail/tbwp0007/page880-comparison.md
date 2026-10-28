# Page880 (TBX) vs TBK comparison (2026-10-14)

> Trail, 2026-10-16. Chapter 13. Page880 is P1040, IdNumber 880. If this sheet and `TBdecompile/record/` disagree, the record wins.

## Page identity

- TBX: Page880/Page.xml (IdNumber 880, P1040)
- TBK: page record at file 0x19C03A (from prior notes)

## TBX content

- 28 IrregularPolygon pins (Vertices expanded)
- 2 Rectangle bodies
- 5 Field text blocks (TTL intro, 7400, 5400, DISCUSSION)
- 5 bitmap references (bitmap id 130-135)
- 2 Arc elements

## TBK content at same page

- 28 pin records as bounding boxes (fill 0xC0C0C0)
- 2 Rectangle bodies
- Text properties present (extracted, noisy)
- BM markers present (matched by size to Bitmap*.bmp)
- No Vertices lists

## Visual gaps

| Element | TBX | TBK |
|---------|-----|-----|
| Pin tips | Expanded Vertices | Bounds only |
| Bodies | Rectangle | Rectangle |
| Text | Clean Field text | Present, needs cleanup |
| Bitmaps | Referenced by id | Present as BM blobs |
| Lines | None on this page | N/A |
| Arcs | Present | Not decoded |

## Extraction results

- Text: 87 pages have Text properties. Format is `Text\x00\x00` + length. Output: tbwp0007/tbk-text.txt
- Bitmaps: 67 BM markers matched to 72 TBX bitmaps by size. Output: tbwp0007/tbk-bmp-matches.txt

## Next

- Clean the text extractor (filter control bytes).
- Place matched bitmaps at their record offsets.
- Diff Page880 render against the TBX render for remaining gaps.
