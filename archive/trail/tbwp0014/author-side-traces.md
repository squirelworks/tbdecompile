# Author-side traces in the runtime

> Trail, 2026-10-16. Chapter 4. Author exports are real and not book open. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## What is absent

`TB80EDT.DLL` and `TB80.EXE` are not in the tree. Author-level commands cannot be confirmed from this archive alone.

## What the runtime already knows

BAS exports several author-mode entry points:

| Function | What it does |
|----------|--------------|
| `CDBEDITBOOK` | Sets a viewer into edit mode. Checks a flag at `DAT_1630_01e4`, writes the book id to offset +0x90, and sets the mode bits to 0x10. |
| `CDBVIEWBOOK` | The reverse. Clears edit mode if the current book matches. |
| `CDBISVIEWERINGENERICEDITMODE` | Returns whether the current viewer is in generic edit mode. |
| `CDBSENDEDITLEAVETOALLFILEVIEWERS` / `CDBSENDEDITLEAVETOALLVIEWERS` | Broadcast an edit-leave message. |
| `TBXAUTHORMODE` | Returns the word at object+0x74. A simple flag read. |

RTM calls `GETAUTHORLOCALIZEDDLL` in several places. That is the runtime asking for the author-side localization DLL (likely TB80EDT or a companion). The call sites are in the 148xxx–154xxx range of the RTM decompile.

## What this means

The reader runtime is not completely author-blind. It has:

- An edit-mode flag per viewer (`DAT_1630_01e4` bits, object+0x90 book id)
- Entry points that a missing author DLL would call
- A localization hook that looks for an author DLL

Without `TB80EDT.DLL` or `TB80.EXE`, the calls into those entry points cannot be traced, and the author command set cannot be enumerated. The runtime side of the contract is visible; the author side is not.

## What can be produced

A short note (this file) documenting the runtime half of the author contract. That is the limit of what the current tree supports. If a copy of TB80EDT.DLL or TB80.EXE appears, the next step is to unpack it and match its imports against the BAS ordinals listed above.
