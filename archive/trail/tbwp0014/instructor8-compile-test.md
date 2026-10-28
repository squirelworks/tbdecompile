# Compiling a short OpenScript with Instructor 8

> Trail, 2026-10-16. Chapter 14.6. Written, not run. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14

## What works

Instructor 8 (ToolBook 8.1) can compile OpenScript. It cannot export TBX. TBX was added in 9.5. The way to get bytecode out of 8.1 is to save a book as TBK and extract the handler from the binary.

## Steps

1. On the Win98 or WinXP VM, open Instructor 8.
2. Create a new book.
3. Add a button. Open its script. Paste a short handler:

   ```
   to handle buttonClick
     go to page "P100"
   end buttonClick
   ```

4. Save the book as `compile-test.tbk`.
5. Copy the TBK off the VM.
6. Run the existing decoder on it. The handler bytecode will be in the page object. The decoder already knows how to find the `to handle` / `end` pair and expand the tokens.

## What this locks

The token for `go to` and the token for the page-name string. A second script with `if` / `else` / `send` / `step` covers the rest of the common subset. Any token that does not resolve is a gap.

## What this does not do

It does not give a full author-side trace. It only confirms the token map for the scripts that were compiled. The author binaries (TB80EDT, TB80.EXE) are still absent.
