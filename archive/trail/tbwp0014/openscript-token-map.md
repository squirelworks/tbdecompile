# OpenScript token map — what "compile+expand" means

> Trail, 2026-10-16. Chapter 14. What compile-plus-expand would lock. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## Current state

The common subset works. The decoder in `openscript_analysis` and the Foolbook engine handle:

- `go to page`, `send`, `put into`, `set to`, `get`
- `if` / `else` / `end if`
- `step from` / `to`
- `name of this book` / `name of this page`
- assignment and simple conditions

The keyword table is resource 0x77 (15,776 bytes, 994 keywords). The decoder uses an offset table at byte 2 + count*4 to map tokens to names.

## What a real compile+expand would do

Take a short OpenScript source. Compile it with the original TB80CMP. Expand the resulting bytecode back to source with the current decoder. Check that every token round-trips to the keyword it came from.

That confirms the token map instead of inferring it from the keyword table and from patterns in extracted handlers. It also catches tokens that the decoder currently drops or mis-names.

## Why we cannot do it here

The original CMP needs the author runtime (or a full ToolBook author install) to compile a script. The tree has the CMP binary and the keyword resource, but not a host that can call the compiler and get a clean token stream out.

## Practical substitute

Keep extracting handlers from the NIDA books. Decode them with the current map. Note any token that does not resolve to a keyword. Those unresolved tokens are the remaining gaps.

The 76 handlers already extracted from 9e954d01.tbk are the current test set. A second pass that lists every token not in the 994-keyword table would quantify the gap without a compiler.
