# Denny exchange — technical summary (2026-10-14)

> Trail, 2026-10-16. Chapter 2 for the Save To XML steps. The 32-bit claim in that exchange is rejected (C-006). Personal names are not copied. If this sheet and `TBdecompile/record/` disagree, the record wins.

Source: Gmail thread "Regarding Toolbook, I have some ancient NIDA electronics courses..."
PDF: /workspace/attachments/Gmail - Regarding Toolbook, I have some...pdf

## Key findings

### TBX export path (TB115)

1. Edit `C:\Program Files (x86)\ToolBook\ToolBook 11.5\Instructor115.ini`
2. Under `[Options]`, add `saveSpecial=true`
3. Launch TB115, accept Trial mode (30-day countdown after license server timeout)
4. Open a **copy** of the 8.1 TBK (not the original)
5. Reply YES to the version warning
6. Press F3 to reach Author level
7. File → Save To XML
8. Output: `<name>.TBK TBX` folder (XML + extracted resources)

TB90 install can suppress the menu item. Repair-install TB115 restores it.

### TBX format

- A `.TBKX` is a ZIP of the TBX folder.
- Double-clicking a `.TBKX` in TB115 imports and rebuilds the book.
- The XML is an industry-standard exchange format added in TB9.5.
- Purpose: allow older versions to open newer files by parsing known elements and ignoring unknown ones.
- Schema files exist in the Engineering source. Denny attached them (see `SumTotal.ToolBook.XML.*.xsd`).

### Version constraints

- TB8.1 is 32-bit only. Needs Windows 10 or earlier (32- or 64-bit).
- TB9.0 added 64-bit support.
- Windows 11 is 64-bit only.
- TB115 can open 8.1 files but saving converts them to 11.5 format.
- NIDA system books (`.sbk`) are password-protected. Author password is held by NIDA.

### Binary format notes

- TB8.1 stores imported images in a basic image blob (converted to BMP on import).
- TB115 stores images in native format (WMF, JPG, TIF, BMP, PNG, GIF).
- This is why 8.1 cannot open a 11.5 file: it does not understand the newer image structures.

## Relation to current work

- The 9e954d01 TBX export we have matches this format.
- Schema files confirm Bounds is required on DrawObject; Vertices is optional.
- The "reader-to-bounds" function Brian mentioned is the missing piece for a pure binary parser.
- TBX remains the practical path for content extraction until that function is located.

## Open items

- NIDA author password for system books (unlikely to be provided).
- Schema validation of the existing 9e954d01 TBX export.
- Mapping binary record subtypes to the object types listed in the schema.
