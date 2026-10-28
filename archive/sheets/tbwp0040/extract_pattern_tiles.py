#!/usr/bin/env python3
"""Pull ToolBook's pattern tiles out of TB80BAS.DLL.

The shipped DLL and the unpacked one hold the same resource bytes.
Nothing here depends on Ghidra. Point it at either file:

    python3 extract_pattern_tiles.py TB80BAS.DLL out/

What it writes
    tiles/NN.png          one 8x8 tile, NN = 0..128
    pattern_strip.png     the strip as stored, top of the picture first
    pattern_tiles.json    the 8 picture bytes of each tile

A pattern number in a book is the tile number. Tile 0 is in the strip
but it is not a legal pattern. Legal numbered patterns are 1..128.
253, 254 and 255 are solid fills, not tiles.
"""

from __future__ import annotations

import json
import struct
import sys
import zlib
from pathlib import Path

RT_BITMAP = 0x8002
BITMAP_ID = 1
TILE_ROWS = 8
TILE_COUNT = 129  # rows / 8


def _chunk(tag: bytes, data: bytes) -> bytes:
    return (
        struct.pack(">I", len(data))
        + tag
        + data
        + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    )


def write_png(path: Path, width: int, height: int, rgb_rows: list[bytes]) -> None:
    raw = b"".join(b"\x00" + row for row in rgb_rows)
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png = (
        b"\x89PNG\r\n\x1a\n"
        + _chunk(b"IHDR", ihdr)
        + _chunk(b"IDAT", zlib.compress(raw, 9))
        + _chunk(b"IEND", b"")
    )
    path.write_bytes(png)


def ne_resource(blob: bytes, type_id: int, res_id: int) -> bytes:
    """One integer resource from a 16-bit NE image."""
    if blob[:2] != b"MZ":
        raise SystemExit("not a DOS/NE image")
    ne = struct.unpack_from("<I", blob, 0x3C)[0]
    if blob[ne : ne + 2] != b"NE":
        raise SystemExit("not an NE image (this reader does not do PE)")
    table = ne + struct.unpack_from("<H", blob, ne + 0x24)[0]
    shift = struct.unpack_from("<H", blob, table)[0]
    pos = table + 2
    while True:
        typ, count, _reserved = struct.unpack_from("<HHI", blob, pos)
        pos += 8
        if typ == 0:
            break
        entries = []
        for _ in range(count):
            off, length, _flags, rid, _handle, _usage = struct.unpack_from(
                "<HHHHHH", blob, pos
            )
            pos += 12
            entries.append((off, length, rid))
        if typ != type_id:
            continue
        for off, length, rid in entries:
            if (rid & 0x7FFF) == res_id:
                start = off << shift
                return blob[start : start + (length << shift)]
    raise SystemExit(f"resource type {type_id:#x} id {res_id} not found")


def decode_strip(resource: bytes) -> tuple[list[bytes], list[int]]:
    """Return top-to-bottom picture rows, and the two palette colours.

    A Win16 RT_BITMAP has no BITMAPFILEHEADER. It is a BITMAPINFOHEADER,
    then RGBQUADs, then the bits. This one is 8 wide, 1032 tall, 1 bit,
    bottom-up. Each stored row is 4 bytes and only byte 0 is picture data.
    """
    if len(resource) < 48:
        raise SystemExit("bitmap resource is too small")
    size, width, height, planes, bits, comp, size_image, _x, _y, used, _imp = (
        struct.unpack_from("<IiiHHIIiiII", resource, 0)
    )
    if (size, width, height, planes, bits, comp) != (40, 8, 1032, 1, 1, 0):
        raise SystemExit(
            f"unexpected bitmap {width}x{height} {bits}bpp "
            f"(wanted 8x1032, 1 bit)"
        )
    colours = used or 2
    pal_at = 40
    bits_at = pal_at + colours * 4
    palette = []
    for i in range(colours):
        b, g, r, _a = resource[pal_at + i * 4 : pal_at + i * 4 + 4]
        palette.append((r << 16) | (g << 8) | b)
    stride = ((width * bits + 31) // 32) * 4
    if bits_at + abs(height) * stride > len(resource):
        raise SystemExit("bitmap bits run past the resource")
    if size_image not in (0, abs(height) * stride):
        raise SystemExit(f"SizeImage {size_image} does not match the rows")
    stored = [
        resource[bits_at + row * stride] for row in range(abs(height))
    ]
    # A positive height is bottom-up: the first stored row is the bottom.
    if height > 0:
        stored.reverse()
    return stored, palette


def tiles_from_rows(rows: list[bytes]) -> list[bytes]:
    if len(rows) != TILE_COUNT * TILE_ROWS:
        raise SystemExit(f"expected {TILE_COUNT * TILE_ROWS} rows, got {len(rows)}")
    return [
        bytes(rows[n * TILE_ROWS : (n + 1) * TILE_ROWS]) for n in range(TILE_COUNT)
    ]


def _rgb(rows_of_bits: list[int], palette: list[int], scale: int) -> list[bytes]:
    out = []
    for bits in rows_of_bits:
        row = bytearray()
        for x in range(8):
            # Bit 7 is the leftmost pixel. 0 selects palette 0.
            colour = palette[(bits >> (7 - x)) & 1]
            row += bytes(((colour >> 16) & 255, (colour >> 8) & 255, colour & 255)) * scale
        out.extend([bytes(row)] * scale)
    return out


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: extract_pattern_tiles.py TB80BAS.DLL out/", file=sys.stderr)
        return 2
    blob = Path(argv[1]).read_bytes()
    out = Path(argv[2])
    tile_dir = out / "tiles"
    tile_dir.mkdir(parents=True, exist_ok=True)

    resource = ne_resource(blob, RT_BITMAP, BITMAP_ID)
    rows, palette = decode_strip(resource)
    found = tiles_from_rows(rows)

    write_png(out / "pattern_strip.png", 8, len(rows), _rgb(rows, palette, 1))
    sheet: list[int] = []
    record = []
    for n, tile in enumerate(found):
        write_png(tile_dir / f"{n:03d}.png", 8, 8, _rgb(tile, palette, 1))
        record.append({"pattern": n, "rows": [f"{b:02x}" for b in tile]})
    (out / "pattern_tiles.json").write_text(json.dumps(record, indent=2) + "\n")

    # Contact sheet, 16 tiles across, each blown up so the bits are visible.
    across = 16
    scale = 8
    cell = 8 * scale
    pad = 4
    cols = across
    grid_rows = (TILE_COUNT + across - 1) // across
    width = cols * (cell + pad) + pad
    height = grid_rows * (cell + pad) + pad
    canvas = [bytearray([0xE8, 0xE4, 0xF4]) * width for _ in range(height)]
    for n, tile in enumerate(found):
        glyph = _rgb(tile, palette, scale)
        left = pad + (n % across) * (cell + pad)
        top = pad + (n // across) * (cell + pad)
        for y, row in enumerate(glyph):
            canvas[top + y][left * 3 : (left + cell) * 3] = row
    write_png(out / "contact_sheet.png", width, height, [bytes(r) for r in canvas])
    print(f"{len(found)} tiles, palette {[f'#{c:06x}' for c in palette]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
