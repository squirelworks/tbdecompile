# 01 — Call-return split

**Date:** 2026-10-17

**Status:** Known for `OBJFILEOPEN`. The same shape will show up in other Watcom bodies. Do not assume the same span.

**Image:** `TB80BAS.DLL`, NE segment 47, Ghidra block `1170`.

## What the listing showed

`OBJFILEOPEN` starts at `1170:177c` with `enter 0x25a`. Ghidra had cut it into a chain of functions at the jump targets. The decompiler showed `unaff_BP` and lines of the form `FUN_1170_21e9(); return;`.

Three signs, all present at once:

- `-- Flow Override: CALL_RETURN (CALL_TERMINATOR)` on a `jmp` and on a `callf` whose next instruction is another `jmp`.
- The bytes after that call shown as `??`. At `1170:17bc` those bytes were `E9 2A 0A`, which is `jmp 1170:21e9`.
- A cross-reference marked `(c)` on an instruction that is a jump. A thunk header, `thunk noreturn`, sat on the call itself.

`FUN_1160_0774` was marked no-return. It returns. The instruction after the call jumps to the epilogue.

`FUN_1170_181c` was not a function. The only reference to `1170:181c` is `jnz` at `1170:1808`, the success test of the second allocation. There is no `enter` there.

The real tail is inside the body:

```
1170:21e9  xor ax,ax
1170:21eb  pop ds
1170:21ec  pop si
1170:21ed  pop di
1170:21ee  leave
1170:21ef  retf 0xe
```

`retf 0xE` is three bytes. The body ends at `1170:21f1`, not at `1170:21ef`.

## What this build's UI did not do

`G` is Go To. It does not delete a function.

The `Delete` key on the signature line, and **Function → Delete Function**, did not work in this session. The action is in the 12.3 sources and is supposed to appear only in the Listing, on the signature, at the entry point. It was not available here. That is why the fragments were removed by script. Do not send the next cut back to that key.

Hand-editing the headers would not have repaired the `??` bytes anyway. The flow override has to be cleared or the disassembler will not follow the call.

## What the script runner rejected

The public class must be the file name. `ClaimObjFileOpen` inside `FixObjFileOpen.java` does not load.

`FunctionManager` in this build has no `getFunctionAfter`. Walk entries with `getFunctions(AddressSet, true)`, copy them out, then delete. Deleting during the iterator skips entries.

`GhidraScript.disassemble` takes an `Address`. Passing an `AddressSet` does not compile. `disassemble(start)` follows flow once the overrides are cleared.

`GhidraScript.createFunction` follows flow and lets the shared-return pass cut the exits again. The decompiler then goes back to `FUN_1170_21e9(); return;`. Create the function with an explicit body instead.

A script that prints `Finished!` and a later compile error are different runs. The compile error does not undo the run that finished. `Ctrl-Z` once per finished run.

## The pass that held

`scripts/FixObjFileOpen.java`, class `FixObjFileOpen`.

1. If `FUN_1160_0774` (`1160:0774`) is no-return, clear that.
2. Set every instruction from `1170:177c` through `1170:21f1` back to `FlowOverride.NONE`.
3. Remove every function whose entry is in that span, including the stub `OBJFILEOPEN`.
4. `disassemble` from `1170:177c`.
5. `FunctionManager.createFunction("OBJFILEOPEN", start, span, SourceType.USER_DEFINED)`.

Leave **Shared Return Analyzer** off. A later auto-analysis will cut the exits again.

## How to tell the repair held

- The old pieces are `LAB_1170_*`. Their cross-references are `(j)`.
- `1170:21e9` falls into `1170:21eb`, and `1170:21ef` is `retf 0xE`, all inside `OBJFILEOPEN`.
- The decompiler has a real frame. `unaff_BP` is gone. Failure is `return 0`. The exits are `goto LAB_1170_...`, not a call followed by `return`.

Calls with arguments stay calls. `FUN_15a0_01c0`, `FUN_1170_21f2`, `FUN_1170_2f48`, and the `FUN_1160_*` bodies are outside this span.

## Addresses used

| | |
|---|---|
| Entry | `1170:177c`, `enter 0x25a`, NE segment 47, file offset `0x58BDC` |
| Last byte | `1170:21f1` |
| False start | `1170:181c`, a `jnz` target |
| Callee cleared | `1160:0774` |
| Not this function | The export-map address `11A8:04F6`. The entry table says segment 47, offset `0x177c`. |
