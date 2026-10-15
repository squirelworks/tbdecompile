# 4. Objects, file open, and the reader

## Claims

| Id | Grade | Statement | Source |
|---|---|---|---|
| O-001 | Known | A live object is `0x76` bytes. Bounds are four words at `+0x0F`, in twips. At 96 dpi, screen pixels are stored / 15, which is `(stored * 96 + 720) / 1440`. | live traces, `FUN_1008_01dd` |
| O-002 | Known | `+0x1F` selects the BitBlt raster op. `+0x3B` is a GDI handle. `+0x30` is the point count. `+0x32` is the point-array far pointer, 4 bytes per point, stored twips. | polygon and BitBlt traces |
| O-003 | Known | `CDBSENDCREATE` (BAS ordinal 51, `12c8:00BC`) creates or rewrites objects from the Instructor UI. The runtime book-open path does not call it. `FUN_12c8_0ef8` is downstream of that author path. | `tbwp0025/cdbsendcreate-is-author.md`, WV-042 |
| O-004 | Superseded | The chain `CDBSENDCREATE` → `FUN_12c8_0850` → `FUN_12c8_0e32` → `FUN_12c8_0ef8` is the runtime reader. | `TBdecompile/20261015/00-how-toolbook-operates.md` §2, `tbwp0002`, `tbwp0008` |
| O-005 | Known | SoftICE and WDW both reached `OBJFILEOPEN` and the buffered read in `FUN_1160_03de`. The raw DOS path at offset `04F3` is skipped when the buffer is already satisfied. | 2026-10-16 consolidated note |
| O-006 | Known | The W16, UTL, and BAS traces in `tbwp0026` do not contain a function that reads a `14 00 00` record. `CDBCHUNK*` walks text. `VALUENEWLONG` constructs a value. `OBJFILEOPEN` is downstream of the reader. | `tbwp0026/trace-review.md`, WV-044 |
| O-007 | Thought | The runtime reader walks nested chunks by length, classifies them, and builds objects without calling `CDBSENDCREATE`. It sits in BAS after `CDBFILEOPEN` and before the first paint. It has no name. | open-question notes |

## 4.1 The live object

These offsets are the ones the papers and the live traces agree on.

| Offset | What | Grade |
|---|---|---|
| `-2` | Type byte. `0x11` is an arc. The other type bytes are not mapped. | Known for `0x11` only |
| `+0x0F` | Bounds: left, top, right, bottom. Written as twips. | Known |
| `+0x17` `+0x19` `+0x1B` `+0x1D` | Four words copied by `FUN_12c8_0ef8` from a source structure at `+0x3E` `+0x40` `+0x42` `+0x44`. The disk `14 00 00` record does not sit at those source offsets. | Known as a copy. The source is not the disk record. |
| `+0x1F` | BitBlt raster-op flag | Known |
| `+0x30` | Point count (word) | Known |
| `+0x32` | Point array far pointer | Known |
| `+0x3B` | GDI handle | Known |
| `+0x52` | Per-pin index. Not applied by the current renderer. Pins that share point bytes draw on top of each other. | Known that the field exists. Not known how paint uses it. |

`ScaleTwipsToScreen` is `FUN_1008_01dd`, BAS segment 2 offset `0x1DD`. With `DS:01A6` and `DS:01A8` set to 96 it turns stored twips into screen points. On the P1140 to P1130 change those words were 96 and 96, so the short form is division by 15.

`FUN_12c8_0ef8` copies four words into the object. It does not parse a page. The disk record and the structure it copies from are different shapes. The step between those two shapes is still unnamed. That step is not `CDBSENDCREATE`.

## 4.2 Author create, stated once

`CDBSENDCREATE` receives bounds that are already formed. It does not compare a buffer to `14 00 00`. Type dispatch inside it selects among new-object and bounds-checked paths. The property registrar `FUN_1058_0a98` writes property id `0x4034`. It does not write painter pointers.

Nothing inside BAS calls `CDBSENDCREATE` by name. One external thunk from `FUN_13d0_0822` reaches ordinal 51. That caller is author UI state (it tests bytes such as `0x26`, `0x36`, `0x38` and stores coordinates around object `+0x638`). It is not the book-open loop.

**Do not break on ordinal 51 to find the reader.** The stop will fire when Instructor creates or rewrites an object. It will not fire because a lesson page was opened.

Older notes that drew this chain as the runtime path:

- `tbworkingpapers/tbwp0002/bas-create-path.md`
- `tbworkingpapers/tbwp0008/cdbsendcreate-sites.md`
- `TBdecompile/20261015/00-how-toolbook-operates.md`, section 2
- `TBWorldview/ToolBook_Architecture.md`, the book-open flowchart that calls `CDBSENDCREATE` per widget

Those files still describe a real function. They mis-place it.

## 4.3 File open, as far as it has been stepped

`CDBFILEOPEN` is BAS ordinal 8. **Thought (WV-007).** It is the export on the open path. It has not been shown to expand a `14 00 00` record itself.

Under it, `OBJFILEOPEN` has a large frame (`0x25A` in one trace). `FUN_1160_03de` is the read wrapper. It calls `FUN_1258_00a8` (buffered path). If that call satisfies the request, a jump skips the raw DOS read at offset `04F3`. Live dumps of a 4-byte read returned an internal pointer (`FC B5 BD B0` at one buffer), not a page header and not the JBO signature. A wider dump showed `4F 46` nearby. That is not a page record.

`CDBCHUNKFIND`, `CDBCHUNKLAST`, `CDBCHUNKEND`, and `CDBSKIPSEP` walk characters: comma, CR, LF, tab, space. They are text chunkers. A decompile that shows `ISDBCSLEADBYTE` and a comma test is not the page walker.

## 4.4 Where the reader is not

Closed, so they are not searched again as the reader:

| Candidate | What it actually is |
|---|---|
| `FUN_1028_2680` | Filter registrar. Calls `TBREGISTERFILTER`. The `0x14` is a type-code limit, not the record marker. |
| `FUN_1008_2d31` (switch at `1008:2DC7`) | OpenScript math. `+ - * /`, `abs`, `sqrt`, `log`, `exp`, `sin`, `cos`, `atan`, `asin`, `acos`. |
| `TB80RTM` | No named file open. Paint goes to BAS ordinal 26. |
| BAS segments `1018`, `1278`, `1478`, `14b8`, `1508`, `10d0`, `1030`, `14a8`, `1160`, `1070` | Sampled. No stream walker. `1160` is debugging (`CDBGETNEURONURL`, `CDBATTACHBREAKADDRESS`). |
| `FUN_10b0_00a6` | Dispatches on type codes including `0x14`. It is a type dispatcher, not a reader. |
| Code at `12e8:0000` | OLE object clone. |
| BAS segment 182 | Real preload code, 39 far calls with a zero segment and no reloc. Not on the book-open path. |

**Known.** No static search of the disassembled image has found the bytes `14 00 00` used as a compare against a far pointer that then builds an object. Thirteen undisassembled runs contain the word `14 00`. Those are far-call immediates, `MOV CX, 0x14`, or jump displacements.

**Thought.** The reader trusts the length-prefixed layout and does not search for the marker. That would explain the missing literal. It is not proven. The way to prove it is a break after `CDBFILEOPEN`, before the first paint, on a lesson page, with the page blob address in hand.

## 4.5 Page and background

**Known.** `80 65` records are the pages. `9e954d01.tbk` has 129 of them.

**Known.** A TBX page can name a background by an id, such as 23 on P10213, that does not appear as a word or a dword in the matching binary page. The link is indirect. Parent and z-order are not in the page record that has been decoded. Absolute bounds are not stored for every shape. The P1170 bracket was computed from bounds relative to a parent. The parent offset has not been applied to the P420 rects.
