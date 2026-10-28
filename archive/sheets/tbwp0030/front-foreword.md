# Foreword

**Date:** 16 October 2026

This volume is the current statement on the ToolBook II 8.1 decompile. It replaces the 15 October 2026 operational notes. Those notes stay on disk under `TBdecompile/20261012/` and in the 15 October PDF. They are the trail. They are not a second current text.

The 15 October contents put `CDBSENDCREATE` (BAS ordinal 51) on the path that builds objects while a book opens. That placement is not true. Ordinal 51 is the Instructor create and rewrite path. A lesson open does not call it. Chapter 4 is the correction. Appendix B draws it.

The 15 October OpenScript note copied back-reference bytes `0xC0`–`0xFF` from the output stream and decoded the keyword table to the wrong words. The copy is from the compressed input. Chapter 14 is that encoding.

Absence from a Ghidra HTML export is not absence from the binary. The listings have undisassembled runs. Appendix K is how those listings are finished and then made readable. It does not name the record reader.

Chapters 19 and 20 were written after the first contents file of this date. Chapter 19 is the NearScript heap, the value stack, and `RESMGR*`. None of those is the `0x76`-byte object array. Chapter 20 is the split between `CDB*` and `OBJ*`. They are not a header and its definitions. Chapter 21 is the stress run of the Python that models those layers. Nested `step` and a reused heap index were the breaks. It is not a timing of `TB80BAS`. Chapter 22 is the value bus, a VBX control, and `EXECSCRIPT`. A VBX is a Visual Basic extension control. It is not the page object, and neither of the other two is a VBX.

A contents PDF printed earlier on this date ends at chapter 18. The table of contents is a separate sheet. Print that sheet when the list has changed and the contents file is not ready to print again. The chapter titles on it are the record. The page counts are the PDFs that already exist. If those two disagree, the record is ahead of the print.

The 15 October operational notes were compared with this volume. What that short file still had, and this volume had thinned, is in the contents: the author-path dispatch and the property-id list (chapter 4), the graphic property names (chapters 2 and 5), and the SoftICE standing orders (chapter 7, with the command cards in Appendices G, H, and I). What it got wrong is not put back. The unsifted symbol-map dumps are not put back either.

v0.0.8r1 adds chapter 16.5. The author password-protected `ssssssssssss.tbk` and `TBCBT` was not in the module list. `nc81base.sbk` was refused. Writing that password is not a load of the cipher DLL.

TBWorldview 1.0.0r3 is its own binder. It is already under 100 pages and it is not reprinted here. Where that binder still draws ordinal 51 on book open, this volume and Appendix B win.

