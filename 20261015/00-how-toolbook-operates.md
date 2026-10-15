# How ToolBook Operates

A consolidated reading of what the decompiles, SoftICE traces, TBX exports, and disk analysis have shown about ToolBook II 8.1. Written so the operational picture can be read without walking the working papers.

## 1. What a book is

A `.tbk` is a 16-bit NE-wrapped file. After a short PE stub the book data begins at the `ZZZTBKBOOKLOC` marker. The signature is `JBO` (ToolBook II 8.x). Pages are the only objects that use the `80 65` marker. Everything else on a page is nested inside it as `14 00 00` records.

A page record contains:
- a 32-byte name (usually `P…`)
- a property block
- nested widget records

Widgets are not separate top-level objects on disk. They are chunks inside the page. Field text is stored as a `Text\0\0` property: an 8-byte header, a 16-bit length, then the string (often starting with CRLF).

The same format is used by the NIDA system books (`nida81.tbk`, the `.sbk` files). The `.sbk` files are primarily resource containers (type tables, menus). Script lives in the lesson `.tbk` files and in `nida81.tbk`.

## 2. Object lifetime

An object in memory is 0x76 bytes. Bounds are four 16-bit words at object+0x0F (left, top, right, bottom). These are in twips. At the observed DPI of 96 the conversion to screen pixels is division by 15.

The create path that has been identified is:

```
CDBSENDCREATE (BAS Ordinal 51, 12c8:00BC)
  → FUN_12c8_0850
    → FUN_12c8_0e32 (allocator)
      → FUN_12c8_0ef8 (copies bounds and selected fields into the object)
```

`CDBSENDCREATE` receives the bounds already formed. It does not parse a `14 00 00` record. The function that reads the disk record and turns it into the structure that `CDBSENDCREATE` expects has not been named. That is the remaining gap on the create path.

Type dispatch inside `CDBSENDCREATE` uses a parameter that selects among new-object, bounds-checked, and other paths. The property registrar (`FUN_1058_0a98`) builds the per-type property-id table. Property ids are 0x4000 + slot (bounds = 0x4004, text = 0x402E, script = 0x4023, vertices = 0x4034, etc.).

## 3. Graphics

The painters live in TB80BAS. They are reached through a type dispatcher, not by name from outside BAS.

- Polygon: `FUN_1408_0376` (segment 0x82). Point count at object+0x30, point array far pointer at object+0x32 (4 bytes per point, stored twips). Calls GDI `POLYGON`.
- Rectangle: simple painter in segment 0x83. Reads bounds at object+0x0F and calls GDI `RECTANGLE`.
- Arc: segment 0x7B. Type code 0x11. Four twip pairs at fixed offsets inside the object; bounding box at +0x0F. Calls GDI `ARC`. Pie objects are synthesized from the same geometry; ToolBook never calls GDI `PIE`.
- Scale: `FUN_1008_01dd`. Converts stored twips to screen coordinates.

On disk, many polygons and content rectangles are stored as bounds-only `14 00 00` records (subtype 0, fill color at +4, point count at +0x1A, twip pairs at +0x22). The TBX export expands these to explicit Vertices lists. The expansion direction has been confirmed against live traces.

Curves (the P420 flame) and some brackets are not stored as simple point lists. Brackets are computed from bounds by segment 0x5B. Curve control structure is still incomplete.

Picture binding is open. BMPs are carved from the book; the widget field that holds the picture id has not been identified. TB80BMP ordinal 3 is the reader.

## 4. OpenScript

Handlers are stored as compressed bytecode. The keyword table is NE resource 0x77. The decoder recovers readable source for the common subset used by the NIDA courses: `go to page`, `send next`/`previous`, basic conditionals, property gets, and system calls.

Back-references (`0xC0`–`0xFF`) copy from the compressed input stream. The decoder stops at the first standalone `end`. The same format appears in `tb80r.sbk` (with the handler name prefix also compressed) and in `nida81.tbk` (100 `buttonClick` handlers).

The expression evaluator is `FUN_1008_2d31` (a large switch that handles the math and transcendental functions). The modern engine implements the common subset; the full evaluator is not ported.

## 5. NIDA system layer

A lesson is not self-contained. `9e954d01.tbk` (Logic Families) names the system books and calls:

- `initializebase`, `initializerecs`, `initializetest`
- `openSession`, `gotoPageList`
- jumps into `nida81.tbk`

`nc81int.dll` exports the trainer/comms functions. `nc81rec.dll` exports the session recording functions (`RecStartSession`, `RecWriteResponse`, etc.). The `.sbk` files supply the object-type table and menu resources. Removing the system books breaks resize, the splash, and the menu.

The load list is `toolbook.lst`. The exact order of the initialize calls has not been watched live.

## 6. What is solid and what is still open

Solid:
- Page marker, object size, bounds location, scale factor.
- Polygon and rectangle painters and their disk record shapes.
- OpenScript decoder for the NIDA navigation patterns.
- Create-path chain after `CDBSENDCREATE`.
- Distinction between stored points and computed shapes.

Still open:
- The disk `14 00 00` → object structure reader (the caller of `CDBSENDCREATE`).
- Curve control structure.
- Arc angle storage and disk match.
- Picture-id binding.
- Background / parent / z-order linkage.
- Full system-book initialize sequence.

## 7. How this was learned

Static analysis of the unpacked NE images (honest unpacker, Ghidra with the NE entry-table patch) plus live SoftICE traces on Win98. The TBX export from ToolBook 11.5 (enabled by `saveSpecial=true`) supplied ground-truth Vertices and property names that could be matched back to the binary. Ordinal breakpoints (`TB80BAS.Ordinal_51` etc.) are stable across boots; hard-coded selectors are not.

The Unicorn hosts never completed a book open. The working path for graphics and object layout has been the combination of disk parsing, TBX comparison, and SoftICE on the real Win98 runtime.

## 8. Practical debugging entry

To watch object creation:

1. Restore the Win98 VHD and start the VM with SoftICE resident.
2. Launch a book so that TB80BAS is loaded.
3. Set `BPX TB80BAS.Ordinal_51`.
4. Resume. On the stop, `STACK` shows the caller and `D SS:SP L 10` shows the parameters.
5. Step into the chain `CDBSENDCREATE` → `FUN_12c8_0850` → `FUN_12c8_0e32` → `FUN_12c8_0ef8` to watch bounds land in the object.

Selectors change every boot. Ordinal names are stable. The disk-to-object reader is still the unnamed caller of this path.
