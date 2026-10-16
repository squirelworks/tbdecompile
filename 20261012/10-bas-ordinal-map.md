# BAS ordinal map (from ExportList.java)

> Notes of 12 October 2026. The current statement is `TBdecompile/record/`. A sentence here that calls the reader a caller of `CDBSENDCREATE` is not current. Export tables are locations, not a claim about when a function runs.

Source: Ghidra ExportList.java console output.

| Ordinal | Name | Address |
|---------|------|---------|
| 1 | CDBINIT | 1058:0000 |
| 51 | CDBSENDCREATE | 12c8:00bc |
| 55 | CDBSKIPSEP | 12f0:04b4 |

Full ordinal table (600+ entries) is in local TBdecompile/20261012/10-bas-ordinal-map.md.
Break on ordinal 51 for the object create path.
