# 2. File formats

## Claims

| Id | Grade | Statement | Source |
|---|---|---|---|
| F-001 | Known | A lesson begins with a `0xC00` PE stub that has no useful code. The book stream is marked by `ZZZTBKBOOKLOC` and magic `0x22222222`, then `03 4A 42 4F` and version `01 00 00 08`. | WV-002 |
| F-002 | Known | Page records are the only objects that start `80 65 00 05 00 02 02`. Widgets inside a page start `14 00 00`. | WV-003 |
| F-003 | Known | `.tbk` and `.sbk` are the same container. The page name sits at offset `0x0B` of the page record. | WV-031 |
| F-004 | Known | Field text is a `Text\0\0` property: 8 bytes, a 16-bit length, then the string. The string often starts with CRLF. | page reader notes |
| F-005 | Known | A ToolBook 11.5 Save To XML, enabled by `saveSpecial=true`, writes a folder of XML plus resources. A `.tbkx` file is a ZIP of that folder. | `TBdecompile/trail/20261014/03-tbx.md` |
| F-006 | Known | Binary 8.1 stores many draw objects as bounds. The 11.5 XML expands those bounds into Vertices lists. | P1040 pin bounds `5055,4605,5205,4860` match the TBX Vertices start |
| F-007 | Known | Foolbook `.fbk` / `.fsk` is a 4-byte magic (`FBK1` / `FSK1`), one flags byte, then JSON. Bit 0 means the payload is zlib-compressed. | Foolbook format notes |

## 2.1 Native book

`tbload.exe`, through `MINSTB32.dll`, searches for `ZZZTBKBOOKLOC`. The signature check is a virtual call, not a literal compare sitting in `tbload`. On `9e954d01.tbk` the JBO body is at file offset `0xC00`. A later open measurement put the same book’s first useful read at `0x9EC`. Both figures are about the same file. `0xC00` is the stub length. `0x9EC` is where one host’s stage-2 open landed. Do not treat them as two different formats.

A page record holds a 32-byte name, usually `P` plus digits, then a property block. The property block at +43 of the early notes starts `14 00 00 01`. Widgets are not separate top-level objects on disk. They are length-prefixed chunks nested in the page.

**Known.** An ascending table of words inside a page, such as the 27 words at page `+0x8C3` on P1170, is an offset directory into a `14 00 00 83` content blob. It is not a Group. A Group is its own object and has its own member list.

**Not true (WV-010).** On-disk `14 00 00 01` does not become `14 00 00 11` when the book loads. One early dump was read that way. Later live objects used `14 00 00 02`. `9e954d01.tbk` has both `01` and `11` on disk. `93950101.tbk` is the other way around. That is a file difference, not a load-time mutation.

Property ids recovered from `TB80BAS` resource type `0x2D1`, id `0x2D0`, are `0x4000` plus a slot:

| Id | Name |
|---|---|
| `0x4004` | bounds |
| `0x4015` | idNumber |
| `0x4023` | script |
| `0x402E` | text |
| `0x4034` | vertices |
| `0x4050` | Point-array setter. Runtime only. Not a record marker on disk. |
| `0x4059` | layer |
| `0x4097` | normalGraphic |
| `0x4098` | invertGraphic |
| `0x4099` | disabledGraphic |
| `0x409A` | stretchGraphic |
| `0x409B` | checkedGraphic |

The graphic ids are the names on a Button in the TBX specimen (`bitmap id N`) and in the property resource. `N` is a resource index, not a file offset. Which bytes inside a `14 00 00` chunk hold `0x4097` is still open. An early carve that reported 641 BMP headers is not this binding. The count used against the specimen is about 75 BMPs in the export, and 67 markers paired with 72 of them.

## 2.2 System books

`.sbk` files use the same container. The NIDA `.sbk` files are resource containers: the object-type name table (ComboBox, Stage, Picture, Hotword, RecordField, PaintObject, Curve, AngledLine, Pie, Arc, IrregularPolygon, Polygon, Line, RoundedRectangle, Ellipse, Group, Field, Button, Rectangle, then Page, Background, Book) and menu resources. They are password-protected. The password is not in this record, and the decompile does not need it.

**Thought, narrowed.** A search for the plain words `to handle` finds no OpenScript in those `.sbk` files. A later reader found compressed handler streams in `tb80r.sbk` (33 handlers), stored as keyword opcodes rather than the words `to handle`. “No script at all” is too strong. What those streams do when a lesson runs has not been traced. `nc81base`, `nc81recs`, `nc81test`, and `nc81trnr` still have no decoded `to handle` text.

`nida81.tbk` is a real book, not a resource bag. It has 43 objects and pages `P20000` through `P22130`. It does not name lesson ids. It has 100 `buttonClick` handlers in the same bytecode as a lesson. P310 is Minimum Requirements (586, 133 MHz, 12 MB RAM, 1 GB, mouse, Windows 98). P20001 is the small menu. P22130 is Test Console Setup.

## 2.3 The 11.5 export

**Known, as of the exported specimen.** In `Instructor115.ini`, under `[Options]`, set `saveSpecial=true`. Open a copy of the 8.1 book, answer the version warning, press F3 for Author level, then File → Save To XML. The result is a folder named `<book>.TBK TBX`. A `.tbkx` is a ZIP of that folder. Opening the ZIP in 11.5 imports it and rebuilds a book.

The schema says Bounds is required on a draw object and Vertices is optional. The schema spells IrregularPolygon wrong (`IrregularPloygon`). The binary stores bounds. The export expands them to Vertices. On P1040 the pin bounds `5055, 4605, 5205, 4860` match the start of the TBX Vertices list. That is the expansion direction: bounds in the 8.1 file, point list in the XML.

The exported specimen of `9e954d01` has 131 `Page.xml` files, 14 backgrounds, about 75 BMPs, and 302 `.script` files. Two of those pages, P440 and P2920, have no `80 65` page record of their own. The binary has 129 pages. All 129 names match a TBX page. They are not a missed page marker. P440's sentence and its house shapes are inside the P430 record (chapter 13). P2920 has not been searched the same way.

Saving from the 11.5 trial converts the book. An 8.1 runtime cannot open that converted file. 8.1 stores an imported picture as a basic blob and turns it into a BMP. 11.5 stores WMF, JPG, TIF, BMP, PNG, and GIF as themselves.

WV-009 called the export a conjecture on 12 October. The specimen exists. The conjecture is closed. WV-013’s description of the ZIP-plus-XML shape matches the specimen.

## 2.4 Foolbook envelope

`.fbk` and `.fsk` are not renamed JSON files with a new extension. The envelope is magic, one flags byte, then a JSON payload. The engine reads compressed, uncompressed, and the older plain-JSON working copies. `.json` remains the working copy. `.tbk` and `.sbk` stay supported so an existing ToolBook file can be opened. System books load core first, then user `.fsk` files as mods.

The philosophy written for that reader is discipline with a recorded deviance: use explicit points when they exist, then the TBX Vertices, then a bounds approximation, and say which one was used.
