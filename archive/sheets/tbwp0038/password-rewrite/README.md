# nc81base.sbk password rewrite experiment

Filed 2026-10-17. Experimental copies only. The original in /Toolbook/NIDA/ is untouched.

## Source

`/workspace/artifacts/Toolbook/NIDA/nc81base.sbk` (67938 bytes).

The unique `14 00 00 f0` is at file offset `0xCF4`. Non-zero password-related data begins at `0xCEC`. The region from `0xCEC` through roughly `0xE00` contains the `14 00 00 f0` header and a repeating `04 00 06 00` pattern. The next `14 00 00` is at `0x17E4`.

## Copies

| File | What it does |
|---|---|
| `nc81base.sbk.orig` | Unmodified copy of the source. |
| `nc81base.zeroed.sbk` | Zeros `0xCEC`–`0xE00` in place. Same length. The password property value is cleared; layout is unchanged. |
| `nc81base.removed.sbk` | Removes `0xCEC`–`0xE00` and shifts the tail. 276 bytes shorter. This is the clean-rewrite attempt. |

## Limits

- The end boundary `0xE00` is a candidate, not a confirmed record length. The repeating pattern may extend further, or the password contribution may be shorter.
- No without-password twin of `nc81base.sbk` exists in the workspace, so the exact shift cannot be verified by diff.
- Both files are untested. A ToolBook author open on a copy is required to see whether the password dialog is gone and whether the book still loads.
- If later sections were re-encoded relative to the password block, neither rewrite will be sufficient.

## Result (2026-10-18)

Both experimental copies failed.

- `nc81base.removed.sbk` produced the internal error at File 'Unknown' line 7547.
- `nc81base.zeroed.sbk` also failed.

Zeroing the candidate region was not sufficient, and removing it and shifting the tail was not sufficient. The password contribution is not confined to a simple property value at `0xCEC`–`0xE00`, or later records are encoded relative to it. A clean rewrite requires a with/without pair of the same book so the exact difference can be measured.
