# Modern ToolBook runtime

This is a clean-room reader and object model for the ToolBook II 8.1 course books already on disk. It is not a translation of the Click2learn NE images. Those binaries stay the reference. Behavior is taken from the file format, the property-name resource, and the handlers the books actually contain.

## What a rewrite of each file means

| Old file | Role in 8.0 | Modern module | Status |
|---|---|---|---|
| TB80RUN.EXE | 32-bit launcher | `python -m runtime` / viewer3 | shell only |
| Tbload.exe + MINSTB32 | opener, finds ZZZTBKBOOKLOC | `tbk.book_offset` | done for the stub |
| TB80RTM.EXE | 16-bit book engine, object 0 / page P0 | `engine.py` | page list and go/next/back |
| TB80W16.DLL / TB80W32.DLL | 16/32 thunk | not needed | browser or Python replaces it |
| TB80BAS.DLL | object model, property getters, stdprops 0x2d1/0x2d0 | `props.py` | names loaded; getters not ported |
| TB80CMP.DLL | OpenScript compiler, COMPILEREXPANDTEXT | future `compile.py` | opcode names still in CMP |
| TB80ENU1/ENU2 | dialogs, strings | skip | English resources, not the book |
| TB80BMP / TB80JPG / TB80FLT | picture codecs | already carved to `tbk_images/` | BMP path works |
| TB80MM / tb80anm.sbk | media, animation | later | unused by the text lessons |
| TB80OLE / TB80OCX / TB80VBX / TB80ACX | OLE and VBX controls | drop | no course book needs them |
| TB80NET.EXE / TB80RMT.DLL | network reader | drop | local files only |
| TBDB3 / TBPDX | dBASE / Paradox | drop | not in these lessons |
| TBDLG / TBWIN / TBCBT / TBDOS | UI, DOS bridge | viewer3 chrome | replaced |
| TB80MAIN.EXE | author shell | viewer3 editor | reader, not author |
| TB80UTL / TBREG / TB80LNL / TB80RCR | install, licensing, record | drop | not part of playback |

## Documenter

You name the directory. It walks that tree, runs the runtime on each `.tbk`, and writes a viewer3 catalog.

```
python -m runtime.documenter D:\your\tbk\tree --xml Toolbook\courses.xml --out documented
```

Output:

- `documented/books/<id>.html` is the runtime reader for that book.
- `documented/extra.xml` is the viewer3 catalog (main / module / lesson, menu `0_MASTER3`).
- `documented/index.html` is the same list as links.

It does not choose a directory and it does not stop at the books sitting in this workspace.

`python -m runtime courses/93955601.tbk` reads the TBK and writes `runtime/out/93955601.html`. Open that file. It shows the page text, Next, Back, and a button for each quoted `P…` jump in the page. That is the reader loop: enter a page, click, go. It still does not execute OpenScript bytecode.

1. Read the TBK. Book magic `0x22222222` is at file `0xC00`.
2. Split on `80 65 00 05 00 02 02`. Keep names that start with `P`.
3. Pull `Text\\0\\0` fields and quoted `P…` jumps out of the page blob.
4. `Engine.go` is what a `buttonClick ("P…")` handler did.

Widget bounds are still the nested `14 00 00` chunk. Property `0x4004` is `bounds`. The in-memory block SoftICE saw on Win98 was `14 00 00 11`, not the on-disk `14 00 00 01`.

## OpenScript

Handlers are already sliced for 93950101 (`viewer2/openscript_corpus.json`, 299 pages, 207 handlers). Top bytes are `e0`, `92`, `83`, `90`. Names for those bytes come from `TB80CMP` `COMPILEREXPANDTEXT`, not from the book. Until that table is copied into this package, the engine navigates by the quoted page ids the handlers push. It does not execute the bytecode.

## Not the goal

A byte-for-byte reimplementation of every NE segment. Segment 61 and segment 144 of TB80BAS are unpacked; that is evidence, not a source tree. Porting the decompile would copy Click2learn code. New code here only implements observed book behavior.
