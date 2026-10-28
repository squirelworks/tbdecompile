# Author password as an appendable 14 00 00 object

Filed 2026-10-17. Follows the append-style Save note (tbwp0030/live-session.md) and the TBCBT cipher record (TBdecompile/record/16-cipher.md).

## Hypothesis

An author password can be added at any time. It is stored as a 14 00 00 object like the rest. The file after that point changes to account for the new record. Removing the password requires the engine to agree with the prior password section and then write new information afterward. A front-to-end rewrite that omits the password object and the artifacts of its generation should yield a clean file without author-password material.

## What the record already shows

From 16-cipher.md:

- The author password path does not load TBCBT when writing the password on a new book. TBCBT segment 7 is the cipher, but it is linked only when a handler calls `linkDLL`. A new book has no such handler.
- A small book saved with a password and the same book saved without one differ from file offset `0xCEC` onward. The tails do not reconverge. The extra length is 1526 bytes of shift, not 1526 bytes of cipher text sitting at the end.
- The local blob at the first difference begins `14 00 00 f0 ...`. Writing the author password stores the property block described in section 16.3 of that note.
- After a failed password dialog the constants `0xA01` and `0x300` appear. Those are the keyed-password scheme selectors, not the book password itself.

## Fit with the append model

The append-style Save (Denny, 2026-10-17) makes the hypothesis plausible:

- Adding a password appends (or inserts and shifts) a 14 00 00 f0 property block and subsequent layout changes.
- The engine on the next open loads the full file, then applies the password state before the user can interact.
- Removing the password would append a compensating edit (or a Save As that omits the object). A clean rewrite that never writes the password object is the Save As case.

The observed non-reconverging tails are consistent with a shift, not a pure trailing append of cipher text. That is why a simple "delete the password object and truncate" is not guaranteed to produce a valid file: later records may have been re-laid-out or re-encoded relative to the password block.

## What a front-to-end rewrite would require

1. Identify the exact 14 00 00 f0 (or equivalent) records that constitute the password property block. The 16.3 blob is the current candidate.
2. Confirm that the password does not also encrypt other regions of the file. The current record says the difference is a shift starting at 0xCEC, and that the author write does not map TBCBT. That leans toward a property-block model rather than wholesale encryption, but it is not proven for a NIDA .sbk.
3. Rewrite the file from the book start through the end, omitting the password block and any generation artifacts (the shift, the extra length). This is the clean Save As.
4. The result should open without the author-password prompt if the block was the only store. If later sections were re-encoded relative to the password, the rewrite will still fail until those sections are also reconstructed.

## Open

- The 10-byte key used on a real NIDA .sbk has not been captured.
- Whether the password block is the sole store, or whether other regions are encrypted or shifted relative to it, is not settled.
- A front-to-end rewrite that omits the 14 00 00 f0 block is the next experiment, but only on a copy, and only after the block boundaries are confirmed against a with/without pair.
