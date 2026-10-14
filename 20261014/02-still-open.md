# Still open

The one that matters is unchanged. Something reads a `14 00 00` record and produces the structure `CDBSENDCREATE` already expects. `FUN_12c8_0ef8` is after that step. A live break on `CDBFILEOPEN` (BAS ordinal 8) that dumps both the disk record and the structure at `12c8:0ef8` would show it. Static searches of the HTML will not.

Retired, so it is not searched again: on-disk `14 00 00 01` does not become `14 00 00 11` in memory. One early dump was read that way. Later live objects used `14 00 00 02`. A goals note from the same week still mentioned `11` as unconfirmed. It stays unconfirmed, and it is not the working theory.

Also open:

- Where an arc's angles are stored, and which page bytes are the type `0x11` record.
- The curve control structure on P420.
- Which property binds a carved BMP to a widget.
- Stroke color and pen width. Fill is known.
- The palette applied to an 8 bpp BMP, and who deletes the pens and brushes.
- `DRAWTEXT` field layout beyond the three offsets.
- The per-pin index at `+0x52`.
- Background id, parent, and z-order.
- What the system-book initialize calls actually invoke, and in what order `toolbook.lst` is walked.
- A re-decompile that recovers `SENDMESSAGE` and `LSTRLEN` arguments.

The host still does not open the book. That fact is kept in TBWorldview, not repeated here.
