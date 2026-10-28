# TBK vs TBX render comparison (2026-10-14)

> Trail, 2026-10-16. Chapters 2 and 13. If this sheet and `TBdecompile/record/` disagree, the record wins.

## Output

| Set | Pages | Path |
|-----|-------|------|
| TBX v2 | 131 | tbworkingpapers/tbx-render-v2/ |
| TBK | 69 | tbworkingpapers/tbk-render/ |

TBX has every page. TBK only rendered pages with detectable bounds or polygon records.

## What TBX has that TBK does not

- **Lines and AngledLines.** TBX has explicit Line elements. TBK has no line records decoded.
- **Text.** TBX Field elements carry Text. TBK text is in property blocks, not yet extracted.
- **Bitmaps.** TBX has Bitmap*.bmp files and NormalGraphic references. TBK stores images as blobs; the placement record is not decoded.
- **Vertices expansion.** TBX expands bounds to tip shapes. TBK stores only the bounding box.

## What TBK has that TBX does not

- **Raw record layout.** The 14 00 00 subtype-0 records with +0x1a count and +0x22 points are the source. TBX is the expanded form.
- **Page order.** TBK page order is the file order. TBX page numbers are IdNumber values.

## Gaps for viewer-accurate render

1. **Lines.** Need to find the line record in the binary or compute them from bounds.
2. **Text.** Need to extract the Text property from the page blob.
3. **Bitmaps.** Need to locate the picture placement record and match it to the carved BMP.
4. **Tip expansion.** Need the algorithm that turns a bounds box into the pin tip.

## Next

- Extract Text properties from the binary page blobs.
- Match Bitmap*.bmp files to picture records.
- Compare Page880 (TBX) to the corresponding TBK page for visual gaps.
