# BAS segment 182 — missed fixups

> Trail, 2026-10-16. Chapter 4. Not book open. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## What is in the segment

Segment 182 is preload code, file `0xc200`, 0x1d30 bytes. It contains:

- 25 `ENTER` prologues
- 135 far calls (`9A`)
- 40 of those far calls end in `00 00` (segment word is zero)
- 39 of those 40 are not covered by any NE relocation record

The NE reloc table for this segment has 266 entries. None of them cover the `00 00` far calls, and none cover offset `0x129`.

## The 0x129 site

Bytes at `+0x129`:

```
8B 9F A8 00   MOV BX, [BX+0xA8]
89 5E CC      MOV [BP-0x34], BX
```

This is ordinary code, not a pointer. The original note called it a "bind." It is not a relocation target. It is simply an offset that was mentioned in an earlier unpacker log and is not special.

## The real leftover

The 39 uncovered far calls with a zero segment word are the leftover. Examples:

```
+0x16:  9A D9 1C 00 00
+0x4e:  9A 11 1D 00 00
+0xf0:  9A FF FF 00 00
+0x15b: 9A E6 0D 00 00
```

In a correctly linked image these would have a real segment selector or a reloc record that fills it in at load time. They have neither.

## What this means

Two possibilities:

1. The OPTLOADER custom reloc block for this segment did not list these far calls, and the unpacker had nothing to rewrite. The segment was packed with unresolved external references.
2. These are internal references to other segments that the packer expected to fix up at runtime through a table that is not present in the static image.

Either way, the segment cannot be executed as-is. A far call to segment 0 will fault.

## Is it the book path?

No static entry point reaches segment 182. No map name points to it. The 39 unresolved far calls make it unlikely to be live code that the book engine calls during open or paint. It is more likely dead, or reached only through a runtime-built table that also supplies the missing segment values.

## Status

The "bind at 0x129" is not a missed fixup. The missed fixups are the 39 far calls with a zero segment word and no reloc record. The segment is real code but is not executable without those fixups being filled in. No evidence it is on the book-open path.
