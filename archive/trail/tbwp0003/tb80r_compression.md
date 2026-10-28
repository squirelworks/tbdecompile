# tb80r.sbk OpenScript compression

> Trail, 2026-10-16. Chapters 14 and 15. 33 handlers, prefix also compressed. If this sheet and `TBdecompile/record/` disagree, the record wins.

## Finding
tb80r.sbk uses the same OpenScript bytecode compression as the lesson books
(9e954d01.tbk etc.). The decoder in openscript_decode.py works when pointed
at the correct stream offset.

## Difference from lesson books
- Lesson books store the handler name as plain text ("To Handle EnterPage")
  followed by compressed body bytes.
- tb80r.sbk compresses the entire handler, including the "to handle" /
  "to get" name prefix. There is almost no plain-text "to handle" in the file.

## Stream location
Compressed streams are scattered through the file (high density of 0xE0 and
0x80-0xBF opcodes). A scan that decodes candidate windows and keeps those
whose output starts with "to handle" or "to get" recovers the handlers.

## Extraction
- Script: ad-hoc scan using openscript_decode.decode()
- Output: tbwp0004/tb80r_handlers.json (33 handlers)
- Quality: readable, but some "?" remain where a back-reference falls
  outside the decoded window or a keyword index misses.

## Byte distribution note
tb80r.sbk has more 0xFF (repeat) and 0xE0 (CRLF) bytes than the lesson books;
the lesson books have more 0xBF / 0xC0-range back-references. The encoding
rules are the same.

## Next
The "?" marks were back-references that landed before the slice being decoded.
`decompress()` now reads those from the whole book. On tb80r.sbk that dropped
the marks from 14256 to 66, and the 66 that remain are real question marks in
the script. Stream boundaries are still a scan, not a length prefix.
