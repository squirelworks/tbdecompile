# Research notes index

These files are the short notes that used to live only in the working papers, plus the 21 October additions. They are not a second record. `TBdecompile/record/` is the statement. The dated folders are `trail/20261012/`, `trail/20261014/`, `trail/20261015/`, and `trail/20261016/`. Do not prefer `trail/20261014/` when it disagrees with `record/`. `trail/20261014/02-still-open.md` still names `CDBSENDCREATE` in the reader sentence. That sentence is not current.

| File | What it still is |
|---|---|
| `property-block-expansion.md` | `FUN_12c8_0ef8` copies four words. Author path. Not the reader. Chapter 4. |
| `rtm-paint-path.md` | `WM_PAINT` goes to `CLIENTTOPAGE`, then BAS ordinal 26. Not the reader. Chapters 3 and 5. |
| `field-text.md` | The disk text handle is word 1 of the `+0x24` block. Word 0 is the style-run handle. |
| `class-providers.md` | Segment 1278 loads providers. It does not load `sysBooks`. Chapter 15. |
| `class-table.md` | Class `0x3A` is `ClassTbl`. Class `0x26` is `Viewer`. |
| `paint-20261021.md` | Button picture block, the 67 stored bitmaps, the type directory, and the live page background. |

`maps/html-segment-index.md` is the HTML-export segment table that had been sitting loose. It is a lookup. It is not a finding.

Segment 1578 rebuilds objects pasted from the clipboard. Segment 1508 reads and writes rich text. Neither runs when a `.tbk` loads. The live-object array stays `FUN_1278_3be6` (chapter 19). It is not segment 1160.

The longer trail is `archive/trail/`. Chapter 18 of the record names each sheet. The draft in `archive/trail/tbwp0028/chapters/` is frozen and lags the record. The 16 October manual source is `archive/sheets/tbwp0030/`.
