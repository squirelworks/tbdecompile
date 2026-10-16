# OpenScript and NIDA system books

> Duplicate of `TBdecompile/20261012/`. Do not edit this copy. The current statement is `record/`.

## OpenScript decoder

- Keyword table is resource 0x77 (type 100, id 119). Offset table at byte 2 + count*4.
- High-bit opcodes (`0xE0`, `0xF0`, `0xFF`, …) emit whitespace, CR/LF, or repeats.
- Back-references (`0xC0`–`0xFF`) copy from the compressed input stream.
- Decoder stops at the first standalone `end`.
- Handles `go to page`, `send next`/`previous`, basic conditionals, and system properties.
- Corpus: 76 handlers from 9e954d01.tbk, 100 buttonClick handlers from nida81.tbk.

## tb80r.sbk compression

- Uses the same bytecode as the lesson books.
- Difference: the handler name prefix ("to handle" / "to get") is also compressed.
- 33 handlers extracted (`tbwp0004/tb80r_handlers.json`).
- Encoding rules are identical; byte distribution differs (more 0xFF/0xE0).

## NIDA system books

| File | Role |
|------|------|
| `nida81.tbk` | Shared shell. 43 objects, pages P20000–P22130. 100 buttonClick handlers. |
| `nc81base.sbk` | Resource container. Object-type table. No OpenScript. |
| `nc81recs.sbk` | Resource container. No OpenScript. |
| `nc81test.sbk` | Resource container. No OpenScript. |
| `nc81trnr.sbk` | Resource container. No OpenScript. |
| `nc81int.dll` | 47 exports. Trainer/comms (IntCheckComm*, voltages, switches, faults). |
| `nc81rec.dll` | Session recording (RecStartSession, RecWriteResponse, RecBookmarkSession, …). |

Lessons call `initializebase`, `initializerecs`, `initializetest`, `openSession`, `gotoPageList`.
These resolve to nida81.tbk handlers or the two DLL exports. The `.sbk` files hold no script.

## Still open

- Full call inventory across the ATT Master_3 set (not just one lesson).
- Minimal stubs for the closed NIDA call set.
- Picture-id binding and remaining draw-object disk layouts.
