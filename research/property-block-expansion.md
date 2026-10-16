# Property-block expansion

> Trail, 2026-10-16. `FUN_12c8_0ef8` is on the author path. It is not the runtime reader. The current statement is `record/04-objects.md`.

`FUN_12c8_0ef8` copies source+0x3e / +0x40 / +0x42 / +0x44 to object+0x17 / +0x19 / +0x1b / +0x1d.

The disk `14 00 00` record does not match those offsets. The expansion step that turns the on-disk property block into the source structure is still unnamed.

Bounds themselves are written to object+0xf..+0x15 by the same function, from parameters, not from a direct disk read.
