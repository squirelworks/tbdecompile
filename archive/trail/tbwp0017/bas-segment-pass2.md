# BAS segment pass 2 — 10d0, 1030, 14a8, 1160, 1070

> Trail, 2026-10-16. Chapter 4. Segments sampled, no stream walker. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## Character

| Segment | Functions | Character | 14 00 00 reader? |
|---------|-----------|-----------|------------------|
| 10d0 | 32 | Structure walking with stride 0xe / 0x1c. Array comparisons. | No |
| 1030 | 18 | Calls into 1010. Flag checks on DAT_1630_01e4. | No |
| 14a8 | 32 | Table helpers, CARRY2. | No |
| 1160 | 26 | Debugging exports: CDBGETNEURONURL, CDBATTACHBREAKADDRESS, GETTASKREMOTEDATA. | No |
| 1070 | 54 | Flag checks on DAT_1630_01e4 / 01e6. | No |

None contain a function that walks a far pointer and compares the first word to 0x0014.

## Notes

1160 is the debugging/neuron side of BAS. CDBGETNEURONURL and CDBATTACHBREAKADDRESS are thin wrappers over internal functions. Not the book path.

10d0 has the most stream-like functions (18 of 32), but the walks are over fixed-stride arrays (0xe, 0x1c), not a byte stream of records.

## Next

The high-density BAS segments have been sampled. No 14 00 00 reader turned up. The remaining path is RTM, or a live break on CDBFILEOPEN.
