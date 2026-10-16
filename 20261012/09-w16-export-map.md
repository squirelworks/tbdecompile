# W16 export → decompile mapping

> Notes of 12 October 2026. The current statement is `TBdecompile/record/`. A sentence here that calls the reader a caller of `CDBSENDCREATE` is not current. Export tables are locations, not a claim about when a function runs.

Matched: 71 / 72

| Export | Decompile line |
|--------|----------------|
| `ACXCTBKSIMPLEOLEDISPATCH_DELETE` | 8697 |
| `DOCMDDRAW` | 8697 |
| `DOCMDMOUSEDOWN` | 8697 |
| `TBKGETGRAPHICID` | 8697 |
| `TBKGRAPHICFX` | 8697 |

W16 is the DoCmd* command bus and the graphics thunk layer. Not the record reader.
Full table in local TBdecompile/20261012/09-w16-export-map.md.
