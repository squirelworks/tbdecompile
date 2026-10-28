# 14 00 00 search in the undisassembled runs

> Trail, 2026-10-16. Chapter 4. The hits are immediates and displacements. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## Result

Zero of the 165 ?? runs contain the full signature `14 00 00`.

## What was found

13 runs contain the word `14 00`. None of them are a signature check:

| Run | Context | What it is |
|-----|---------|------------|
| 76 | `FF 76 FE 9A 14 00 E0 16` | Far call to 0x16E0:0x0014 |
| 102 | `FF 76 DE 9A 14 00 E0 16` | Far call to 0x16E0:0x0014 |
| 103 | `B9 14 00 99 F7 F9` | MOV CX, 0x14; then a divide |
| 121 | `C9 CA 14 00 90` | Leave / retf 0x14; then a NOP |

The remaining hits are jump displacements or data that happen to contain the word.

## Conclusion

The 14 00 00 record reader is not sitting as a literal signature compare inside the undisassembled regions. If it is in one of those runs, it compares a word or a byte that it has already read, not an immediate `14 00 00` in the instruction stream. The earlier candidate `FUN_1028_2680` (CMP AX, 0x14 after a far read) remains the closest static pattern, and it was already closed as a filter registrar.
