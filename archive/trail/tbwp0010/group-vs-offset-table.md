# Group vs Offset Table — Script Strip Test

> Trail, 2026-10-16. Chapter 13.4. The word table is an index, not a Group. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## Question

Is the ascending offset table (e.g. page +0x8C3 on P1170, 27 entries) a Group member list, or a page-level directory into the large `14 00 00 83` content blob?

## Test

- P1170 content blob: file 0x1AB651, 1844 bytes (`14 00 00 83`).
- Offset table at file 0x1ABE97: word values 0x14, 0x16, 0x40, 0x52, 0x66, 0x7a, 0xc2, … (relative into the blob).
- Extracted OpenScript handlers (handlers_extracted.json) do not fall inside this blob; the scripts are stored as embedded bytecode/strings inside the blob itself.
- Script-like markers found at blob +0xA9, +0xB9, +0x17B, +0x18B (`buttonClick`, `"P1180"`, `"P1140"`).

## After stripping ~100-byte regions around those markers

Remaining non-zero runs are short structured sequences (type bytes, small integers, color-like 0xFFFFFF, property-like dwords). No large free-form text remains. The offset table still points into these remaining structured regions.

## Conclusion

The offset table is a **page content index**, not a Group. It enumerates sub-items (shape records, property blocks, script chunks) inside the `14 00 00 83` blob.  

A Group is a separate object type that can appear as one of those sub-items (or as its own `14 00 00` record). It owns a member list of child objects; that list is not the page-level offset table.

Shared scripts, if present, would appear as referenced chunks inside the content blob (or as system-book resources), not as the offset table itself.

## Next

- Walk the offset table entries against the remaining structured data to classify each sub-item.
- Check nida81.tbk and system books for true shared-script resources.
