# 10. Open, retired, and superseded

## 10.1 High

These block a faithful page.

| Gap | Grade | Why it is still open | Next step that would close it |
|---|---|---|---|
| Runtime record reader | Known as the read in chapter 4.6: `1178:08B2` → `1188:04DA` → `1188:08D6` → `1160:02CC`. | The bytes are in memory before message `0xE`. Still open: the dispatcher for handle `0x0C36`, and which fields of the 412-byte body are the page. | One Bochs stop at the return of `1180:03C8` for that handle. Appendix L. Do not break ordinal 51. |
| Picture id | Known for a button and the directory (G-012). | The id is the fourth word. The button stores it plus one. A background picture is the block at `+0x37` when that block is present. | Which of the non-bitmap huge entries are palettes. |
| Property expansion | Known that `FUN_12c8_0ef8` copies four words from a structure that is not the disk record. | Offsets `+0x3E` and friends do not match a `14 00 00` header. | Only useful on the author path. For runtime, fold this into the reader break. Do not keep it as a separate `CDBSENDCREATE` hunt. |
| Tbload vtable | Thought. `FUN_00406a70` calls vtable+4 after the marker search. | The 32-bit search is found. The callee is not. | One break at `00406aa1` with the book path in a register. Low value until the reader is the goal again. |
| Polygon type table | Known for the specimen. | Class `0xF` and class `0x10` both call `POLYGON`. This book uses `0x10`, count at `+0x30`, points at `+0x32`. | Class `0x14` curves, and the eight class `0x19` records in `nida81.tbk`. |

## 10.2 Medium

| Gap | Grade | Note |
|---|---|---|
| P420 stroke breaks | Thought | Three 96-point groups in TBX. One tangled dump from `+0xA13`. Look for length prefixes between runs before inventing a new curve format. |
| Arc on disk | Known live, unknown on disk | Type `0x11`, four pairs, fill at `+0x18`. Angles not located. No `GDI!PIE`. |
| Stroke color and pen width | Stroke known (G-011). Width is the pen table | Fill is `+0x1B` on a draw object and `+0x5B` on a background. Styles 1 through 9 are none, dot, dash, solid, then inside-frame widths 2, 3, 4, 6, and 8. | The table is `DS:0x1708` in the unpacked DLL. Not re-checked on a painted line. |
| Palette on an 8 bpp BMP | Known that segment `1150` builds a palette | Not known which palette a given carved BMP must use. |
| `DRAWTEXT` beyond three offsets | Open | `param_5+0x4A`, `+0x4C`, `+0x50` are the paint path. The disk handle is word 1 at `+0x24` (O-009). |
| Per-pin index `+0x52` | Known the field exists | Not applied. Shared point bytes stack. |
| Background, parent, z-order | Background known on disk | Page `+0x47` names the class 4 record, 131/131 (O-011). Parent is the near pointer at `+0x04`. Z-order is the list at `+0x2C`, not a byte. | The on-disk bytes of that list header were not dumped. |
| `initializebase` and `toolbook.lst` order | Thought | Names are in the lesson. The call log is not. |
| OpenScript keyword lock | Thought | Instructor 8 compile, then expand. Not run. |
| `SENDMESSAGE` / `LSTRLEN` arguments | Known mangled | Re-decompile. Not a new algorithm. |

## 10.3 Retired

| Idea | Grade | Why it stays closed |
|---|---|---|
| On-disk `14 00 00 01` becomes `14 00 00 11` in memory | Not true | Both values exist on disk. A later live object used `14 00 00 02`. WV-010. |
| `FUN_1028_2680` is the reader | Not true | Filter registrar. |
| `FUN_1008_2d31` is the reader | Not true | Math. |
| RTM contains the reader | Not true | Paint handoff only. |
| `CDBCHUNK*` is the reader | Not true | Text separators. |
| `GDI!PIE` draws pies | Not true | No import. |
| The reader must contain the literal bytes `14 00 00` | Thought, not a requirement | Length-prefixed walks would not. Do not close a function for lacking the literal, and do not keep scanning for the literal as the only method. |
| HTML listing absence | Not evidence | `??` runs and forced-disassembly passes exist. |
| `TB80BMP` resolves a stored bitmap id | Not true | The id is a type directory in `TB80BAS` segment `1028` (G-010). BMP's palette notify can still run. |
| `TB80FLT` reads a bitmap out of a book | Not true | It is the import filter. A picture already in the book does not go through it. |

## 10.4 Superseded notes

Read these for the function bodies. Do not read them for the runtime path.

| Note | What it got wrong |
|---|---|
| `tbworkingpapers/tbwp0002/bas-create-path.md` | Put `CDBSENDCREATE` on book open. |
| `tbworkingpapers/tbwp0008/cdbsendcreate-sites.md` | Same chain, more callers. The callers are author-side. |
| `TBdecompile/trail/20261015/00-how-toolbook-operates.md` §2 | Same chain, written as “the create path that has been identified.” |
| `TBdecompile/trail/20261015/01-theories-of-operation.md` §1 | Still calls the reader “the caller of `CDBSENDCREATE`.” |
| `TBdecompile/trail/20261014/02-still-open.md` | Same wording. The rest of that file’s open list is still the open list. |
| `TBWorldview/ToolBook_Architecture.md` book-open flowchart | Draws `CDBSENDCREATE` once per widget. |

The correction, in one paragraph: Instructor calls `CDBSENDCREATE` when it creates or rewrites an object. A lesson open does not. The function that turns a `14 00 00` chunk into a live object during that open has not been named. It does not call ordinal 51. `FUN_12c8_0ef8` is on the author side of the same line.

## 10.5 Side quests that are real and not the reader

Kept because they will matter after the reader has a name.

- Object pool: `FUN_1478_014a` allocates near objects. `FUN_1478_00a0` is the pool.
- RTM dialog chrome: `GETDLGITEM` id `0x65` (55 hits), `GETWINDOWLONG` index 10 (196 hits). `FUN_1068_0098` is `GLOBALALLOC` with an out-of-memory retry.
- Author mode exports on BAS, and `GETAUTHORLOCALIZEDDLL` on RTM. The author binaries themselves are not in the archive.
- Password cipher in TBCBT segment 7. Constants `0xA01` and `0x300` after a failed password.
- CMP expand, parked at the W16 segment-not-present fault. Not on the NIDA open path.

## 10.6 Order of work

1. One lesson open under WDW. Break `TB80BAS@CDBFILEOPEN`, resume, then break the next BAS export that runs before the first paint. Log it.
2. When an object exists, dump `+0x0F` and the page offset it came from. That pair names the reader, whatever the export happens to be called.
3. Only then place bitmaps, split the P420 strokes, and apply `+0x52`.
4. Do not schedule another full-module naming pass, another Unicorn boot, or another break on ordinal 51 in service of step 1.

## 10.7 The loose sheets are not a second record

Chapter 18 names every markdown sheet under `tbworkingpapers/` and the section of this directory that replaced it. A sheet can still describe a real function and still be wrong about when that function runs. Leaving the sheet on disk keeps the trail. It does not keep the old claim alive. The printable form of the claim is the PDF next to these chapters.
