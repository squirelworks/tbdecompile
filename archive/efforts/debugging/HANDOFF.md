# SoftICE book — closed 11 Oct 2026

This chat is decommissioned as the SoftICE field manual. A Debugging chat should read this file and the Watcom debugging notes, and should not mix their commands.

Do not suggest a WDW key from this file. Do not suggest a SoftICE command from the Watcom file.

## Obey these

- Selectors die on reboot. Never reuse a CS, hMod, or linear address from these notes. Remap with `MAP`. Segment numbers in `MAP` are hex.
- `T` into a call, `P` over it, `G` to run. F12 is `P RET`. On the book-open path it paints the splash.
- `BC *` before a new breakpoint. A live `GDI!POLYGON` breakpoint freezes SoftICE if the page scrolls.
- `14 00 00 01` does not become `14 00 00 11`. Later live `80 65` objects used `14 00 00 02`.
- A dump that starts with the SoftICE window, or with the DOS device chain `CON` / `AUX` / `PRN`, missed. Real dumps: `page.bin01511`, `p400.bin0157`, `dump-001.bin`, `dump-002.bin`.
- Do not search all of memory. The wide `80 65` search found nothing and can GPF the VM.
- If the user is in WDW, stop and use the Watcom notes.

## Where SoftICE stopped

Book probe: `PUSH CS` / `CALL 2F00` at TB80BAS `316F:1791`. `D DS:BX` is the path. System books hit first (`nc81base`, `nc81recs`, `nc81trnr`, `tb80anm`, `tb80r`). Splash book is `nida81.tbk`. Outer frame: `2F2F:183D`. Selectors are from that boot.

Calls that painted when stepped over or returned from: `CALL 0614` in BMP(7), a short call in BAS(37) near `017F` or `01A6`, a near call in BAS(2).

Next SoftICE break, not yet a live hit: TB80BMP segment 7 offset `0x805`, the signature check. `T` in. Do not `P RET`.

## Confirmed at a stop

- `GDI!POLYGON`, `POLYLINE`, `RECTANGLE`, `ARC` fire. `GDI!PIE` does not.
- Polygon: BAS segment `0x82` offset `0x376`. Count at object+`0x30`, points at +`0x32`, twips. Scale segment 2 offset `0x1DD`. At `DS:01A6` = 96, screen = twips/15. Points land at `DS:30AC`. An 11-point polygon is one gray pin tip.
- Polyline brackets are computed from bounds at object+`0x0E`..`+0x14`.
- Arc: segment `0x7B`, type word `0x11` at object−2, box at +`0x0F`.
- Rectangle: segment `0x83`, bounds at object+`0x0F`.
- A lesson click is delivered to `TBKClient`, not `TBKChildWindow`. `BMSG` does not see that queue.
- `GetObject(14)` on the splash bitmap only fires during load.
- ICEDUMP 6.021 needed `kernel32` and `user32` exports in `winice.dat`. `/option n` sets screen-dumper mode 1. A filename without `*` printed a literal name. The memory-dump recipe is not repeatable yet.

## Open, SoftICE only

1. Catch the splash decode before it paints.
2. One-shot the rectangle painter for the chip body, then `BC *`.
3. One clean memory dump of an address just displayed, then repeat it.

The full manual is `artifacts/debugging/FIELD_NOTES.md`.
