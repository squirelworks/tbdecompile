# How to read this record

**Date:** 2026-10-16

**Status:** This directory is the official statement.

`TBdecompile/record/` is the consolidated record of the ToolBook II 8.1 work. The loose sheets under `tbworkingpapers/tbwpNNNN/` are the trail those findings were written on. They are not a second current record. When a loose sheet and this directory disagree, this directory wins. Chapter 18 names every loose sheet and the section that absorbed it.

The dated folders `trail/20261012/`, `trail/20261014/`, and `trail/20261015/` stay as the notes of those days. `trail/20261016/00-consolidated.md` is the short correction this volume expands. Read those folders for the trail. Do not read `trail/20261015/00-how-toolbook-operates.md` section 2, or `trail/20261015/01-theories-of-operation.md` section 1, or `trail/20261014/02-still-open.md` opening paragraph, as the runtime create path.

## Grades

| Grade | Meaning |
|---|---|
| Known | Seen in a binary, a live trace, or a matching export. A later observation would have to contradict the evidence, not just a reading of a listing. |
| Thought | Fits the evidence and is the working model. Not yet watched end to end. |
| Conjecture | Plausible. Not tested. |
| Not true | Was a working idea. Later evidence closed it. Do not search it again. |
| Superseded | An older note still says this. The later note wins. The older path is listed so it is not reopened by accident. |

## Order

| File | Subject |
|---|---|
| [01-corpus.md](01-corpus.md) | What the books are, and which machines can run them |
| [02-formats.md](02-formats.md) | `.tbk`, `.sbk`, `.tbx`, `.fbk` |
| [03-runtime.md](03-runtime.md) | Modules, launch seam, NIDA system layer |
| [04-objects.md](04-objects.md) | Live object, file open, the unnamed reader |
| [05-graphics.md](05-graphics.md) | Painters and what is stored versus computed |
| [06-openscript.md](06-openscript.md) | Bytecode, handlers, the modern subset |
| [07-debugging.md](07-debugging.md) | SoftICE, WDW, Unicorn, where the cipher lives |
| [08-naming.md](08-naming.md) | What has been named, and what a name is worth |
| [09-modern.md](09-modern.md) | Foolbook, Foolcourse, Foolversity, TBpipeline |
| [10-open.md](10-open.md) | Ranked gaps, and the notes that are closed |
| [11-keepers.md](11-keepers.md) | One-boot live addresses and decompile line numbers |
| [12-wdw-spine.md](12-wdw-spine.md) | The book-open spine and what the three traces hit |
| [13-specimen-pages.md](13-specimen-pages.md) | P1040, P430, P420, P1170, and the TBX draw inventory |
| [14-openscript-bytes.md](14-openscript-bytes.md) | Encoding, the back-reference fix, corpus counts |
| [15-system-books.md](15-system-books.md) | `.sbk` tiers, NIDA shell, type-name table |
| [16-cipher.md](16-cipher.md) | TBCBT segment 7 and the keyed-password schemes |
| [17-modules.md](17-modules.md) | Module roles, including the ones that are not the reader |
| [18-absorption.md](18-absorption.md) | Every loose sheet, and where its claim went |
| [19-heap-stack-resmgr.md](19-heap-stack-resmgr.md) | NearScript heap, the value stack, `RESMGR*`, and the callers the breakpass did not name |
| [20-cdb-obj.md](20-cdb-obj.md) | `CDB*` is the book API. `OBJ*` is the object file and object memory. Not a header and its definitions. |

Lookup tables that are too long to typeset live in `maps/`:

| File | What it is |
|---|---|
| [maps/rtm-ne-to-ghidra.md](../maps/rtm-ne-to-ghidra.md) | TB80RTM NE segment to Ghidra space |
| [maps/bas-ne-to-ghidra.md](../maps/bas-ne-to-ghidra.md) | TB80BAS NE segment to Ghidra space |
| [maps/wdw-to-ghidra.md](../maps/wdw-to-ghidra.md) | One boot's WDW selector:offset against the decompile |

NE segment numbers are not Ghidra `CodeN` names. Segment 1 is `1000`, segment 2 is `1008`, and the usual step is 8, with gaps. Live selectors change every boot. Offsets inside a segment do not.

## What this record will not hold

Binary dumps, SoftICE console logs, and personal correspondence stay out of this repository. Names of correspondents are masked. The correspondent already used in the public notes is JohnDoe1. `who-is-who` is not part of this record.

## Which older sentence to trust

If a note written on or before 2026-10-15 puts `CDBSENDCREATE` between file open and the first painted object, that sentence is superseded. The correction is chapter 4. Instructor calls ordinal 51 when it creates or rewrites an object. A lesson open does not.

If `tbworkingpapers/tbwp0001/openscript_notes.md` says the keyword table decodes to "italic" or "systime", that sentence is superseded. The bug was copying bytes `0xC0`–`0xFF` from the output stream. Chapter 14 is the encoding that actually decodes the handlers.

Absence from a Ghidra HTML export is not absence from the binary. The listings have undisassembled runs. A candidate is closed only when the disassembly or a live trace shows what the function actually does.

If a note says `HEAP*` or `TBHEAP*` allocates the `0x76`-byte object, or that `TBHEAPCLEARCRITSECT` has no definition, that sentence is superseded. Chapter 19.

The printable form of this directory is [ToolBook-record-20261016.pdf](ToolBook-record-20261016.pdf). That file was typeset before chapters 19 and 20. It ends at chapter 18 until the contents are rebuilt.
