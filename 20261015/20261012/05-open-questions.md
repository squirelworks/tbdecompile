# Open questions

> Duplicate of `TBdecompile/20261012/`. Do not edit this copy. The current statement is `record/`.

## Bounds

- Disk `14 00 00` record → object+0xF expansion rule.
- `CDBSENDCREATE` receives bounds as parameters. The reader is a caller.
- Next: XREFs on `CDBSENDCREATE` in BAS or the RTM/Tbload open path.

## Graphics

- Curve control structure (P420 flame). Points exist; order/structure wrong.
- Arc disk layout. Live object (type 0x11) known; disk match missing.
- Picture id → DIB binding. BMPs carved; widget field unknown.
- Computed shapes (brackets, lines) once bounds exist.

## OpenScript / system

- Full NIDA call inventory (initialize*, session, gotoPageList).
- Stubs for the closed set that appears in the corpus.
- Modern CMP expander (standalone, no W16). Test corpus already extracted.

## Engine

- RTM book-open path. Unicorn hosts die before a book open (FFFF:0158 / unbound far call).
- CMP W16 segment-not-present fault (001c:00000015). Needs live selector capture.
- TBKX export via ToolBook 11.5. Prospective; no samples in tree yet.

## Closed

- FIDB trial. moralrecordings DOS/Win16 databases produce zero CRT renames.
- Compiler is Microsoft C (R60xx strings). VC++ 1.52c / MSC 7.0 already covered.
- SoftICE `BAS(nn)` syntax does not work. Use MAP → selector.
