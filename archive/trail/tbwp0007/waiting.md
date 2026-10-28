# Waiting list, 2026-10-14

> Trail, 2026-10-16. Chapter 10. Waiting list folded into the ranked gaps. If this sheet and `TBdecompile/record/` disagree, the record wins.

Things that need the user, and what was done instead.

## Done here

- Converted the remaining rename scripts to Java (same pattern as RenameBas.java).
  Drop into ~/ghidra_scripts/ and run against the matching project:
  - RenameRtm.java
  - RenameBmp.java
  - RenameCmp.java
  - RenameFlt.java
  - RenameJpg.java
  - RenameLnl.java
  - RenameMm.java
  - RenameNet.java
  - RenameRcr.java
  - RenameUtl.java
  - RenameVbx.java
  - RenameW16.java

## Still needs you

1. Run the Java rename scripts in Ghidra (one per module).
2. SoftICE / WDW on the Win98 VM for the book-open path (CDBFILEOPEN, bounds writer).
3. The three nehost pass dumps (rtm - pass 01/02/03) are stuck in
   tbworkingpapers/miscellaneous/nehost/ due to I/O errors on the segment bins.
   They can stay there or be deleted if the TBdecompile/nehost/ copies are enough.
