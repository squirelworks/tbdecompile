# Field text

`FUN_1440_0160` reads the near pointer at object `+0x24`. When byte `+0x33` bit 4 is set and `DAT_1630_148E` is nonzero, it reads `+0x44` instead. Neither book sets that bit.

The block behind the pointer holds two words. `FUN_1170_4098` resolves word 0 into `DAT_1630_2D30` and word 1 into `DAT_1630_2D34` / `DAT_1630_2D36`. For a RecordField (class `0x16`) it also copies word 4 into object `+0x34`. The function does not read object `+0x42`.

On disk, word 1 of that block is the text handle. It matches the exported text for 497 of 497 fields in the Logic Families book and 226 of 226 in `nida81`. The old `+0x42` guess missed the scripted fields. Word 0 is the style-run handle. `FUN_1440_0160` resolves it into `DAT_1630_2D30`. The run block's count is at `+2` and the runs start at `+4`, `0x0B` bytes each.

The `+0x42` in `property-block-expansion.md` is a different copy, from the property block onto the live object. Leave that note as it is.

Chapter 5 draws a field with `DRAWTEXT` from `param_5+0x4A`, `+0x4C`, and `+0x50`. That is the paint path. This note is the handle on the disk record. They are not the same field.
