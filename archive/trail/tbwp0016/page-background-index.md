# Page / background index

> Trail, 2026-10-16. Chapters 4.5 and 10. Background id is not a word in the page record that has been decoded. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## Finding

The TBX page `Page1000` (name `P10213`) references `Background id 23`.
The matching binary page record is at file `0x21db85` (page index 104).

A word or dword search for the value 23 across the entire 3716-byte page record returned zero hits.

## Conclusion

The background link is not a direct integer field inside the page record. It is either:

- stored in a separate index table that is not adjacent to the page object, or
- resolved at load time from a parent or shared-script reference.

A static search of the page record is closed. The next step is a live break on the page-open path to see which structure is consulted for the background.
