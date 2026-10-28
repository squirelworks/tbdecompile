# ToolBook pattern tiles from TB80BAS.DLL

The fill patterns painted on polygons, rectangles and the houses on P440 are not stored in the book. The book stores a pattern number. The picture for that number is bitmap resource 1 inside `TB80BAS.DLL`.

Both files carry the same 4,192 bytes: the 683,872-byte Optloader original and the 1,163,488-byte unpacked image. Run the script on whichever one you have.

```
python3 extract_pattern_tiles.py TB80BAS.DLL out/
```

No install. Python 3.9 or later. It writes `tiles/000.png` through `tiles/128.png`, `pattern_strip.png`, `pattern_tiles.json`, and `contact_sheet.png`.

## Where the bytes are

1. DOS header. The dword at file offset `0x3C` is the NE header.
2. NE header. The word at NE+`0x24` is the resource table, relative to the NE header.
3. Resource table. First word is an alignment shift. Then records until a type word of 0. A type record is `type, count, reserved`, then `count` entries of `offset, length, flags, id, handle, usage`. Offset and length are in units of `1 << shift`, not bytes. Integer types and ids have the high bit set.
4. Bitmap resource: type `0x8002` (`RT_BITMAP`), id `0x8001`. There is no `BITMAPFILEHEADER`.

## What the bitmap is

| Field | Value |
|---|---|
| Header | 40-byte `BITMAPINFOHEADER` |
| Size | 8 wide, 1032 tall |
| Planes, bits | 1, 1 |
| Compression | 0 |
| Colours | 2 RGBQUADs. First is black, second is white |
| Rows | 4 bytes each. Only byte 0 is the picture. Bytes 1–3 are padding |
| Order | Bottom-up. Reverse the stored rows before cutting tiles |

1032 / 8 = 129 tiles, numbered 0 through 128 from the top of the picture.

A 1-bit is the fill colour. A 0-bit is the stroke colour. Bit 7 of each byte is the left pixel.

## What a book stores

The pattern property is the tile number.

- `0` and anything above `128` are rejected.
- `1` through `128` select that tile. The painter copies an 8×8 block from `x = 0`, `y = pattern * 8`.
- `253`, `254` and `255` are not tiles. They are solid: none, solid fill, solid stroke.

Tile 33 is `00 FF 00 FF 00 FF 00 FF`, the house siding. Tile 105 is the brick. Tile 119 is the roof.

`pattern_tiles.json` is the whole strip as eight hex bytes per tile, so a viewer can hard-code the masks without parsing a DLL again. Regenerate it from your own `TB80BAS.DLL` rather than shipping the DLL.
