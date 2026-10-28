# Author password is already loaded by open

Filed 2026-10-17. Follows password-as-append.md and 16-cipher.md.

## Claim

By the time ToolBook presents the author-password dialog, it has already read the stored password from the file. It does not create a new password to check the user's entry. It already knows what the password is.

## Fit

The append-style Save (Denny) requires the engine to load the whole file and apply the append log before the user can interact. The author password is stored as a 14 00 00 f0 property block (16-cipher.md, section 16.3). That block is part of the file the engine walks. Once the walk completes, the stored password value is in the live object graph.

The dialog therefore compares the user's entry against a value the engine already holds. It does not re-derive or re-encrypt a fresh password at dialog time. That matches the observation that writing the password on a new book does not load TBCBT, and that a refused system book also does not load TBCBT. The cipher DLL is not required for the comparison once the property block has been read.

## Consequence for a clean rewrite

If the password is only a property-block value that the engine loads and then compares, a front-to-end rewrite that omits the 14 00 00 f0 block (and the shift artifacts after it) removes the value the dialog would check. The engine would then have nothing to compare against, and the book would open without the author-password prompt. That is the Save As case.

This still requires confirming that no other region of the file is encrypted or shifted relative to the password block. The non-reconverging tails in the with/without pair are the remaining risk.
