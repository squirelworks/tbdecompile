**Correction 2026-10-15:** `CDBSENDCREATE` is an author function. Not on the runtime path. See `tbwp0025/cdbsendcreate-is-author.md`.

# 14 00 00 Reader Search by Assembly Pattern

> Trail, 2026-10-16. Superseded. Chapter 4. No literal compare found. Author-path sentences superseded. If this file and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14  
Approach: generate a plausible "read word, CMP to 0x14" pattern and search BAS/RTM HTML.

## Expected pattern

A 14 00 00 record starts with the three bytes `14 00 00`. A word read of the first two bytes yields `0x0014`. A reader is therefore likely to contain something like:

```
LES BX, <buffer pointer>
MOV AX, word ptr ES:[BX]     ; or ES:[BX+n]
CMP AX, 0x14
Jxx <handle or skip>
```

## Hits in TB80BAS.DLL.html

| Address | Context | Notes |
|---------|---------|-------|
| 1028:26d7 | `LES BX, [BP+local_30]; MOV AX, ES:[BX]; CMP AX,0x14; JNC ...; SUB AX,2` | Strongest candidate. Reads a word from a far pointer, compares to 0x14, then adjusts the pointer by -2 and stores into a structure at +0x154/+0x156. Function is FUN_1028_2680. Calls TBREGISTERFILTER and an indirect CALLF; does not directly call CDBSENDCREATE. |
| 10c8:00b2 | After GETFREESYSTEMRESOURCES, CMP AX,0x14 | Resource check, not a record reader. |
| 10d8:0215 | `LES BX, [BP+local_6]; MOV AX, ES:[BX+4]; CMP AX,0x14; JZ ...` | Reads a word at offset +4 from a structure and branches on equality to 0x14. Possible type-field check. |
| 10d8:0237 / 0253 | Additional CMP AX,0x14 in the same function | Same function as above. |
| 14f0:01a4 | `INC AX; CMP AX,0x14; JBE ...` then a switch | Counter/limit check, not a buffer signature. |

## RTM

No `CMP AX,0x14` that reads from a buffer pointer. The 0x14 comparisons present are against structure fields (ES:[BX+0x14]) or stack locals.

## Status

FUN_1028_2680 (BAS segment 6, offset 0x2680) is the best current candidate for a 14 00 00 record walker. It is not yet proven: it does not call CDBSENDCREATE, and its callers are not yet fully traced. The 10d8 function that compares a structure field at +4 to 0x14 is a secondary candidate.

Next step: dump the full body of FUN_1028_2680 and its caller at 1028:2678, and check whether the structure it writes (+0x154) is later used by the create path.
