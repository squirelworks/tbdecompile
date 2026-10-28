# TBX full analysis (9e954d01)

> Trail, 2026-10-16. Chapters 2 and 5. Specimen graphics. Renders are not re-shipped here. If this sheet and `TBdecompile/record/` disagree, the record wins.

Source: `9e954d01 tbx/`. Outputs below. Page names are the runtime `P` ids from the XML `Name` attribute.

## 1. Vertices / SVG
- `vertices.json` — every shape with Vertices or Bounds, keyed by page name (96 pages).
- `P430.svg`, `P420.svg`, `P1040.svg` — simple SVG renders of those pages (pins, flame, DIP packages). Twips are the viewBox units.

## 2. Groups
- `groups.json` — parent/child tree for every page (131 pages). Groups nest the visual units.

## 3. Extra pages (TBX only)
- `extra_pages.json`
- **P440** (folder Page876) and **P2920** (folder Page961).
- Both use Background id 2. Both have the same heavy diagram mix (12 IrregularPolygon, 108 Line, 32 Rectangle, ~48 Group) and no page script.
- Not system/info pages; they look like export-only or unused diagram pages. No corresponding 80 65 record in the raw TBK.

## 4. Script corpus / jump graph
- `script_corpus.json`
- 302 script files.
- 23 distinct handler names.
- External book jumps: **nida81.tbk** (15 times). No other books.
- Pages with no Script attribute are listed.

## 5. Book and Background scripts
- `book_and_backgrounds.txt`
- Book.script: enterSystem pushes tb80r, nc81base, nc81test, nc81recs, nc81trnr; calls initialize* and openSession / gotoPageList. Also enterApplication.
- 12 Background*.script files.

## 6. Construct coverage
- `constructs.json`
- Counts across all scripts: if 297, set 184, get 113, forward 48, when 37, else 27, conditions 26, break 22, increment 14, step 10, put 1, decrement 0.
- Current TBX runner covers the common path; conditions/when/step/increment are present but lightly used.

## 7. Bitmaps
- `bitmaps.json`
- 72 Bitmap*.bmp files, all referenced from XML.
- Sizes and reference counts included. Shared buttons (Next, OK, Help, Skip, etc.) account for most.

## 8. Backgrounds
- `backgrounds.json`
- 14 backgrounds used.
- Background id 2 (41 pages) and id 3 (40 pages) dominate.
- 12 of the 14 have a .script file.

## 9. Page name diff
- `page_diff.json`
- TBX 131, TBK 129.
- Only in TBX: P440, P2920.
- Only in TBK: none. Names match otherwise.

## 10. Twip spot check
- `twip_spot.json`
- P430 first pin: twips (3762,3682)… → screen ≈ (251,245) at /15.
- P1040 first pin: twips (5055,4605)… → screen ≈ (337,307).
- P420 sample: twips (3915,5340)… → screen ≈ (261,356).
- Matches the earlier “screen = twips/15” scale from the SoftICE traces.
