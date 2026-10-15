# 10. Open, retired, and superseded

## 10.1 High

These block a faithful page.

| Gap | Grade | Why it is still open | Next step that would close it |
|---|---|---|---|
| Runtime record reader | Thought that it is in BAS after `CDBFILEOPEN`, before first paint. No name. | Every static candidate in chapter 4 was something else. The WDW export traces do not contain it. | Break after `CDBFILEOPEN` on a lesson open. Dump the buffer that is about to become an object. Do not break ordinal 51. |
| Picture id | Known that BMPs are in the file. Not known which property binds one to a widget. | 67 markers paired with 72 TBX bitmaps, and the widget still has no name for the bitmap. | One live `TB80BMP` ordinal 3 stop, with the object pointer, compared to the page blob. |
| Property expansion | Known that `FUN_12c8_0ef8` copies four words from a structure that is not the disk record. | Offsets `+0x3E` and friends do not match a `14 00 00` header. | Only useful on the author path. For runtime, fold this into the reader break. Do not keep it as a separate `CDBSENDCREATE` hunt. |
| Tbload vtable | Thought. `FUN_00406a70` calls vtable+4 after the marker search. | The 32-bit search is found. The callee is not. | One break at `00406aa1` with the book path in a register. Low value until the reader is the goal again. |
| Polygon type table | Thought. Built at runtime. | No static pointer to `PaintPolygon`. | Break `PaintPolygon`, walk one frame up, dump the table. |

## 10.2 Medium

| Gap | Grade | Note |
|---|---|---|
| P420 stroke breaks | Thought | Three 96-point groups in TBX. One tangled dump from `+0xA13`. Look for length prefixes between runs before inventing a new curve format. |
| Arc on disk | Known live, unknown on disk | Type `0x11`, four pairs, fill at `+0x18`. Angles not located. No `GDI!PIE`. |
| Stroke color and pen width | Open | Fill is known. Segment `1018` creates pens and does not say who frees them. |
| Palette on an 8 bpp BMP | Known that segment `1150` builds a palette | Not known which palette a given carved BMP must use. |
| `DRAWTEXT` beyond three offsets | Open | `param_5+0x4A`, `+0x4C`, `+0x50`. |
| Per-pin index `+0x52` | Known the field exists | Not applied. Shared point bytes stack. |
| Background, parent, z-order | Known the TBX id is not a word in the page | P1170 bracket is parent-relative. The parent link is not decoded. |
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

## 10.4 Superseded notes

Read these for the function bodies. Do not read them for the runtime path.

| Note | What it got wrong |
|---|---|
| `tbworkingpapers/tbwp0002/bas-create-path.md` | Put `CDBSENDCREATE` on book open. |
| `tbworkingpapers/tbwp0008/cdbsendcreate-sites.md` | Same chain, more callers. The callers are author-side. |
| `TBdecompile/20261015/00-how-toolbook-operates.md` §2 | Same chain, written as “the create path that has been identified.” |
| `TBdecompile/20261015/01-theories-of-operation.md` §1 | Still calls the reader “the caller of `CDBSENDCREATE`.” |
| `TBdecompile/20261014/02-still-open.md` | Same wording. The rest of that file’s open list is still the open list. |
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
