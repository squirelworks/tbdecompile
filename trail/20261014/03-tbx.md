# The 11.5 export

> Trail, 2026-10-16. The 11.5 export, as known that day. Chapter 2 is the statement. The correspondent is JohnDoe1. No mail is copied here. If this file and `TBdecompile/record/` disagree, the record wins.

From correspondence with JohnDoe1, 14 October 2026. The personal name and the mail are not in this record.

## How a book is saved

1. In `Instructor115.ini`, under `[Options]`, set `saveSpecial=true`.
2. Start ToolBook 11.5 and accept the trial. A TB90 install can hide the menu. A repair install of 11.5 puts it back.
3. Open a copy of the 8.1 book, not the original. Answer yes to the version warning.
4. Press F3 for Author level.
5. File, Save To XML.

The result is a folder named `<book>.TBK TBX`: XML plus the extracted resources. A `.TBKX` is a ZIP of that folder. Opening the ZIP in 11.5 imports it and rebuilds a book. The XML was added around 9.5 so a newer file can be read by keeping the elements a program knows and ignoring the rest. Schema files exist. Bounds is required on a draw object. Vertices is optional.

One lesson, `9e954d01`, has already been exported this way. The plain-text `.script` files in that export are what a small interpreter reads. It follows `go to page`, `send`, assignment, `if`, `conditions`, and `step`. It does not apply property writes to a live object, and predicates such as `is not in` are recorded rather than evaluated. Parsing the full export is slow. It is a playback path for the export, not a reader of the `.tbk`.

## What was said about versions, and what the binaries say

JohnDoe1 said 8.1 is 32-bit and needs Windows 10 or earlier, and that 9.0 added 64-bit support. The images in this work are 16-bit NE. ToolBook 9.0 is the 32-bit product, which is why it runs on 64-bit Windows. Those two accounts are not the same claim. The binaries win until a 32-bit 8.1 engine is actually in hand.

Saving from the trial converts the book to 11.5. An 8.1 runtime cannot open that file. 8.1 stores an imported picture as a basic blob and turns it into a BMP. 11.5 stores WMF, JPG, TIF, BMP, PNG, and GIF as themselves.

The Nida system books are password-protected. The password is not in this record, and it is not required for the decompile.
