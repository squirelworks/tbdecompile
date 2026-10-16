# The shelf

> Trail, 2026-10-16. What the miscellaneous shelf was. Not a finding about the reader. If this file and `TBdecompile/record/` disagree, the record wins.

The readable shelf is `tbworkingpapers/history/miscellaneous/`. On 11 October 2026 it was `tbworkingpapers/miscellaneous/`, about 3,200 files and 170 MB. Most of the pictures and the SoftICE memory dumps were deleted that night because they can be cut from the books again, or because they were the same splash saved under several names. What follows is the part worth keeping. The Numega kit and the Maybe2–Maybe4 trees did not survive the later move; see `tbworkingpapers/history/README.md`.

## Readers, in the order they were dropped

Each one read the same lessons. None of them ran `TB80RTM`.

- `viewer` was one `book.xml` and one HTML frame.
- `viewer2` was the XML player: page, paragraph, image, go, choice, quiz. About 400 course files. It followed quoted page ids.
- `viewer3` added notes and callouts and still loaded the older course file.
- `maybe` through `Maybe4` were JSON lessonshells. Maybe4 was the first of them to expand handlers with `TB80CMP` resource `0x77` and get real `go to page` text instead of a string scan.
- `runtime/` replaced the translators. It splits on the page marker, pulls `Text`, and does next and back. `documented/` is 559 HTML books that package wrote.
- `runtime_cpp/` is the same idea, plus a few SVG frames.

The reader that replaced these is TBpipeline. The viewer that replaced the XML player is Foolbook.

## Hosts that were not readers

`nehost/` unfolded the Optloader stub under Unicorn and materialized the RTM segments. It did not implement USER, GDI, or OLE, so a lesson does not run there. The passes that were kept moved to `tbpipeline/tbpipeline_bf/nehost/` and then into TBpipeline. `nedllhost/` bound BAS segments: 461 resolved, 339 not. `bmpproxy/` is a Watcom stand-in for `TB80BMP` that logs ordinal 3 and ordinal 13. Source only.

## Format, as the shelf left it

Book signature `03 4A 42 4F`, version `01 00 00 08`. The page marker was in every course book then on disk. A 32-byte name follows the object id. At offset 43 the property block begins `14 00 00 01`. `PHYSSIZE` does not occur. Ordinary BMPs are stored whole. A second form is a `BITMAPINFOHEADER` with no `BM` signature. In one book that form was four progress bars.

The keyword resources in `TB80CMP` are `0x77` (992 strings), `0x78` (980), and `0x70` (213 property names). An early decoder emitted the wrong words. The later one matches the handlers. A back-reference copies compressed input. It is not a call.

## SoftICE, closed the same day

Selectors die on reboot. `14 00 00 11` was not confirmed. A dump that starts with the SoftICE window missed. A lesson click is delivered to `TBKClient`. The polygon painter, the scale, and the arc and rectangle painters are the live results, and they are already in `trail/20261012/`. The kit itself is a SoftICE 4.05 installer and ICEDUMP. It does not belong in this repository.

## Names

The Ghidra rename scripts and the nameable lists are in `rename/`. Eight of thirteen modules had been walked by 11 October: about 11,000 functions, about 18 percent nameable by pattern, a little over a hundred confirmed by hand. The Java scripts are the same lists, one module at a time.
