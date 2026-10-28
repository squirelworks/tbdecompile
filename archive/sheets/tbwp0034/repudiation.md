# Repudiation

Read this before naming another function in `TB80BAS.DLL`. The last long answer repeated a breakpoint recipe, then took back corrections that had already been checked against the decompile. Those corrections stand. The pages that walk them back do not.

## What is settled

`09` compared through a `char *` is the byte 9. Ghidra prints it as `'\t'`. It is not a tab scan and it is not a property-type switch. `OBJFILEOPEN` stores 9, through `FUN_1190_0000`, after the `JBO` marker (`0x4A03`, `0x4F42`) has matched and the type words are not the type that was requested. `FUN_1048_2174` sees a failed open and that byte, clears the byte, calls `OBJFILETYPE`, and opens again.

`1048:18c4` is not a function. It is inside `FUN_1048_1766`. The live return `21AD` is inside `FUN_1048_2174`, whose entry is `1048:2174` and whose next function starts at `1048:23da`.

`FUN_10c8_00de` does not parse a `14 00 00` chunk. It walks an in-memory directory. The record is 13 bytes with a 5-byte header. `FUN_1110_0000` then calls `UNLOCKFONT`. There is no add of `0x0A` and no add of `0x14` on that path.

`1000:01ea` is a label inside `FUN_1000_0169`, not a file parser. The `+ 10` there steps a startup slot table whose base is `[0x22]` and whose count is `[0x1c]`. Nothing in that function reads a `.tbk`.

`+0x2E` and `+0x30` are one far pointer passed to `OBJLOCK`. The live object is `0x76` bytes, allocated as `count * 0x76` in `FUN_1278_3be6`. Two words are not that allocation.

A burst of `CDBCREATEPAGEREF`, `CDBSETVALUEEX`, and `CDBPAINTCLIENT` means those exports ran. It does not mean any of them walks a `14 00 00` chunk. Breaking `CDBCREATEPAGEREF` and reading the caller is an experiment. The caller is not known until the Calls window shows an offset, and that offset is then found in the listing. Do not write the recipe again. Do not call the export the unmarshaler.

## Errors that were repeated after they had been corrected

`ne_cbenttab` is at `NE+0x06`. `NE+0x36` is `ne_exetyp`. Writing a length at `+0x36` corrupts the executable-type byte. `ne_nrestab` at `NE+0x2C` is a file offset, not a physical address.

The loader fix honors `ne_cbenttab` and treats the entry segment byte as unsigned. A snippet that breaks on a zero count and ignores `ne_cbenttab` is the bug, not the patch. `patch_ne_entry.py` zeros the bundle count and strips the export names. Do not recommend it. The image that loads is the unpacked DLL, 1,163,488 bytes. The packed 683,872-byte file is still OPTLOADER.

`1048:2325` is not `FUN_1048_24A0`. That function starts at `1048:24A0`. An address between `2174` and `23da` is inside `FUN_1048_2174`.

The comments that label `0x08000001` as ToolBook 8.0 and `0x02000003` as ToolBook 2.0 are not in the binary. The function also tests `0x1C421372` and `0x1C421371` before the arm that stores `0xB6`. Dropping those two compares changes the branch.

`FUN_1048_24A0` is not a table-of-contents read. On the success path it stores the handle, locks `+0x80` and `+0x82`, calls `FUN_10c8_00de`, then locks `+0x2E` and `+0x30`. That is the index and the font list. It is not the widget reader.

A subtype list that runs line `1`, rectangle `2`, round rectangle `3`, ellipse `4`, polygon `5`, pie `6`, arc `7`, curve `8` under class `0x12` has no compare behind it. The only live type word with a name is `0x11`, an arc, at object offset `-2`. `0x0F`, `0x10`, `0x13`, and `0x14` allocate a point array. Which one is Polygon is not known. Do not fill the gap.

## How to make the next claim

State the entry point and the entry point of the next function. If the address in hand is between them, it is inside the earlier function.

Quote the instruction that performs the step. A 10-byte record is an add of `0x0A`. A 20-byte header is an add of `0x14`. A name is not a substitute for the add.

A live selector is not an identity. Match the offset. `FUN_1170_177c` is `OBJFILEOPEN` at offset `0x177c` no matter what selector Windows assigned.

If the only new fact is that an export was hit again, say that it was hit. Do not promote it to the reader, and do not send the breakpoint recipe back.
