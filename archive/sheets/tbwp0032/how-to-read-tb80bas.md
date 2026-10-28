# How to read TB80BAS, and three claims that are wrong

Paste this into an analysis session before it names another function in `TB80BAS.DLL`.

The target is a 16-bit Watcom binary, loaded as an NE image. The decompiler lies in specific, repeatable ways. A function name invented from a search target is not a finding. A live breakpoint is a finding only for the instruction it stopped on.

## 1. What counts as evidence

A claim about a function needs one of these, and the text of the claim has to match it:

- The instruction bytes, at a stated offset inside a function whose entry point has been shown.
- The decompiler output of that same function, quoted, not paraphrased into a new name.
- A live register or stack dump, tied to the instruction pointer of that stop, and then matched to the static function by offset. Selectors change every run. Offsets do not.

These do not count:

- Naming a function after the thing the search was sent to find. If the search was "the `14 00 00` parser," the next function touched may not be titled "the `14 00 00` parser" unless that function reads those bytes or walks a record whose layout has been shown to be that record.
- A Ghidra label in the middle of a function. `FUN_ssss_oooo` is the entry point. An address between that entry and the next function is not a new function.
- A comment written into the decompiler output. `unaff_BP + 6` is not "the engine context" until a store or a call uses it as one.
- One call site described as the only call site. Say "the call site that was recorded."

If the bytes and the title disagree, the title is wrong. Do not keep the title and soften the bytes.

## 2. How this binary calls functions

Watcom uses two conventions in the same DLL.

Exported entry points are far and stack-based. The live stop on `OBJFILEOPEN` shows four `push`es and a far call, on the `enter 025A,00` at offset `0x177F`. `CDBFILENEW` and `RESMGRGETPROPERTY` decompile as `__stdcall16far` with real stack parameters. That is correct. Do not change it.

Internal static functions take arguments in `AX`, `DX`, `BX`, `CX`, left to right. A far pointer takes two registers, offset then segment. Further arguments are pushed. The callee keeps `SI`, `DI`, `BP`, `DS`, and `SS`. It does not keep `AX`, `BX`, `CX`, `DX`, or `ES`. The export is often a short thunk that moves the stack arguments into those registers and jumps to the static body. That thunk is why so many one-call functions exist. It is not evidence that the thunk and the body are the same function, and it is not evidence that every small function is a thunk.

In the current decompile, arguments Ghidra failed to put on a signature show up as `in_AX` (46 times), `in_DX` (233), `in_BX` (142), and `in_CX` (75). `FUN_1048_0014` decompiles as `GLOBALUNLOCK()` with no handle. The handle arrived in a register and was dropped. That is the bug a `__watcall` prototype fixes.

`unaff_BP` is a different bug. It means the function reads `BP` and never sets it, so Ghidra treats `BP` as an incoming value. A function that already takes its arguments from `[bp+n]` is not repaired by declaring it register-argument. `FUN_1048_1766` is one of those.

Do not replace `<default_proto>` with `__watcall`. That would rewrite the exports, whose arguments are on the stack. Add `__watcall16near` and `__watcall16far` beside the existing prototypes, and set them only on a `FUN_` that uses `in_AX` or `in_DX` and does not read `[bp+n]`. Leave every export on `__stdcall16far`.

The prototype has to have a return in `AX`, a 4-byte return in `DX:AX`, preserved registers, and a stack slot after `CX`. Four input registers and nothing else is not a calling convention. A 4-byte pointer will still appear as two words. That is acceptable. Ghidra will not join them.

```xml
<prototype name="__watcall16near" extrapop="0" stackshift="2">
  <input>
    <pentry minsize="1" maxsize="2"><register name="AX"/></pentry>
    <pentry minsize="1" maxsize="2"><register name="DX"/></pentry>
    <pentry minsize="1" maxsize="2"><register name="BX"/></pentry>
    <pentry minsize="1" maxsize="2"><register name="CX"/></pentry>
    <pentry minsize="1" maxsize="500" align="2">
      <addr offset="2" space="stack"/>
    </pentry>
  </input>
  <output>
    <pentry minsize="1" maxsize="2"><register name="AX"/></pentry>
    <pentry minsize="3" maxsize="4">
      <addr space="join" piece1="DX" piece2="AX"/>
    </pentry>
  </output>
  <unaffected>
    <register name="SP"/>
    <register name="BP"/>
    <register name="SI"/>
    <register name="DI"/>
    <register name="DS"/>
    <register name="SS"/>
    <register name="DF"/>
  </unaffected>
</prototype>
```

Far internal calls need the same block with `stackshift="4"` and the stack `offset="4"`, named `__watcall16far`.

Applying the convention does not merge a thunk into its callee. The body stays a separate function. Its inputs become parameters instead of undefined registers. That is the whole of the fix.

Do not collapse a function to its callee because it has one call. `FUN_1028_3adc` calls `FUN_1048_1766` and then copies the handles at `+0x88`, `+0x84`, and `+0x86` into globals. Calling it a redirector deletes that.

## 3. The record reader was not found

`FUN_1048_18c4` was called the Master Record Reader. There is no function with that entry point. `1048:18c4` sits inside `FUN_1048_1766`, whose entry is `1048:1766`. The next function is `FUN_1048_1b60`. A mid-function address is not a routine that was discovered. It is a line in a function that was already located and had not been read.

`FUN_1048_1766` opens a file, locks a handle pair stored at `+0x80` and `+0x82`, and calls `FUN_10c8_00de`. That is file setup. It does not walk the widgets of a page.

The live return address that was captured, offset `21AD`, is not in that function. It is inside `FUN_1048_2174`, which starts at `1048:2174`. That function was also already known, as one of the helpers between `CDBFILEOPEN` and `OBJFILEOPEN`. The stop identified which of those helpers was on the stack. It did not identify a new reader.

The instructions at that return are:

```text
21AD  mov  word ptr [bp-2C], ax
21B0  or   ax, ax
21B2  je   21B7
21B4  jmp  22DE
21B7  mov  bx, word ptr [bp+10]
21BA  cmp  byte ptr ss:[bx], 09
21BE  je   21C3
21C0  jmp  23A8
```

`AX == 0` was read as success, and `0x09` as a property type that selects the length-prefixed parser. Both readings are backwards. The decompile of this function is:

```c
local_28 = OBJFILEOPEN(...);
if (local_28 == 0) {
  if (*param_7 != '\t') goto LAB_1048_23a8;
  *param_7 = '\0';
  local_2e = OBJFILETYPE(...);
  ...
  local_28 = OBJFILEOPEN(...);   /* retry */
}
```

`'\t'` is the byte `0x09`. `AX == 0` means the open failed. On that one error code the function clears the byte, asks `OBJFILETYPE` what the file is, and opens again. Any other error goes to `23A8`, which is the cleanup at the bottom of the same function, not an "alternative type parser" for text streams. The four pushes are the arguments of `OBJFILEOPEN`. They are not a length boundary that has been identified.

`FUN_1048_24a0` is the function `FUN_1048_2174` calls after an open has succeeded. It performs the same lock, the same call to `FUN_10c8_00de`, and the same second lock through `+0x2E` and `+0x30`. That sequence was merged with `FUN_1048_1766` and the merge was given a name. They are two functions, and neither one reads a page.

The reader is still unnamed. It runs after `CDBFILEOPEN` and before the first paint. It has not been shown to contain the immediate bytes `14 00 00`. Do not give it a name until a function's own bytes walk a page record into objects.

## 4. `FUN_10c8_00de` is not the `14 00 00` parser

`FUN_10c8_00de` was called the `14 00 00` length parser. It never compares a buffer with `14 00 00`, and it never walks a record of that shape. The absence of the immediate is not, by itself, the disproof. A length walk would not contain those three bytes. The disproof is the walk that is actually there.

`FUN_10c8_00de` locks a buffer. If bit 1 of the first byte is clear, it calls `FUN_10c8_1e6e`. Otherwise, and if that call returns nonzero, it calls `FUN_1110_0000`.

`FUN_10c8_1e6e` locks each block in a directory and copies from offset `+5`:

```c
local_46 = (undefined2 *)((int)locked + 5);
for (i = 6; i != 0; i--)
  *dst++ = *src++;          /* 6 words = 12 bytes */
local_46 = local_46 + 6;    /* step 12 bytes */
```

The directory slot advances by 3 words. The allocation is `count * 0x0C`. There is no add of `0x0A` and no add of `0x14`.

The table those bytes are copied into is allocated by `FUN_10f8_0444` as `count * 0x0D + 5`. `FUN_10f8_0502` and `FUN_10f8_0660` move the entries by `0x0D`, copying 6 words and one trailing byte. The header is 5 bytes. The record is 13 bytes.

`FUN_1110_0000` then walks a pointer table. The count is at `+2`, the pointers start at `+4`, and each object is passed to `UNLOCKFONT` through the word at `+0x29`. That is a font list.

So the path is: lock a file object, copy a 12-byte slice out of a 13-byte in-memory record, build an index, unlock fonts. It is not a parser for the bytes that begin a widget on disk.

On disk, a page record begins `80 65 00 05 00 02 02`. A widget nested in that page begins `14 00 00`. Those widget bytes are a chunk inside the page, not a top-level object and not an in-memory index entry. A function that deserves the name has to consume that chunk: a length, then the fields, then the next chunk. `FUN_10c8_00de` consumes a directory of already-built objects. Do not call a directory walker a record parser because it runs during file open.

## 5. The 10-byte chunk and the 20-byte header are not this path

A 20-byte header skip and a 10-byte stride were also described: 2 bytes of object id, 4 bytes of parent, 4 bytes of sibling, in a function named `FUN_1000_01ea`. That function is not in this decompile.

The stride rule is simple. A 10-byte record is five words, or a pointer add of `0x0A`. A 20-byte header is a pointer add of `0x14`, or a length word whose value is `0x14` and which is then added to the pointer. This path has a 5-byte header and a 13-byte record. Writing "10" and "20" because those were the numbers in the question is the same error as the title "`14 00 00` parser."

If a later function does step by 10, show the add. Until that instruction is quoted, the 10-byte unpacker does not exist.

## 6. Offsets `0x2E` and `0x30` are not the `0x76` object

`+0x2E` and `+0x30` were called the `0x76` live object hook, and described as the array of live text frames. They are one far pointer. The code loads those two words and passes them to `OBJLOCK`, then passes the result to `FUN_10c8_0000` with a first argument of 6.

`FUN_10c8_0000` switches on the word at `pointer - 2`. The cases are `4`, `5`, `0x0B`, `0x25`, and `0x26`. That is a type tag in front of a locked object. It is not a size, and it is not a loop over objects of `0x76` bytes.

The live object is `0x76` bytes long. `CDBNEWOBJECT` indexes it as `param_6 * 0x76`. The block is allocated in `FUN_1278_3be6` by `GLOBALALLOC` or `GLOBALREALLOC` of `count * 0x76`. `CDBGETVALUEEX` reaches a slot with `(param_7 & 0xff) * 0x76`, locks that slot, calls the code pointer at `+4`, and unlocks. The value is the argument. The object is what is locked. None of that code uses `+0x2E` or `+0x30` as the object.

A far pointer stored inside a file header is not the object it points at, and it is not an array. Do not promote two consecutive words to "the live object" because they are the next `OBJLOCK` in a function that has been decided is the reader.

## 7. How the three claims were produced

Each one has the same shape.

Three unnamed things were given: the reader, the `14 00 00` walk, and the `0x76` object. A file-open helper was stopped in. A call, a compare, and a lock were found, and the three names were assigned to those three instructions. The compare is an error byte. The lock is a far pointer. The call does not read a widget. The address promoted to a function entry is in the middle of a function that already had a name.

That is not a partial result. The labels are false, and they hide the function that was actually on the stack. `FUN_1048_2174` is worth reading because it is the open-failure retry. It is not worth reading under the name "record reader."

## 8. Rules for the next pass

Before a function is named, write its entry point and the entry point of the next function. If the address in hand is between them, it is inside the earlier one. Say so.

Before a compare is called a type switch, print the bytes it compares and find that constant in the decompile. `09` as `cmp byte ptr [bx], 09` was `*param_7 != '\t'`. One character of C would have stopped the claim.

Before a pointer pair is called an object, write the size of the object and the instruction that allocates it. `0x76` is allocated as `count * 0x76`. Two words at `+0x2E` are not that allocation.

Before a loop is called the disk parser, write the stride and the header skip from the instructions, then put them next to the on-disk record. This file's page begins `80 65 00 05 00 02 02`. Its widgets begin `14 00 00`. A walker that copies 13-byte index entries and then calls `UNLOCKFONT` is not that walker, whether or not the source contained the immediate `14 00 00`.

Do not repair Ghidra by replacing the default prototype. Add `__watcall` and apply it to internal bodies that already show `in_AX` or `in_DX`. Re-decompile those bodies. Leave the exports alone.

When a small function has one call, read the instructions after the call before deleting it. A copy into a global is a body.

The open problem is unchanged. Name the function that turns a `14 00 00` chunk into the `0x76`-byte object. Do not name it until its bytes do that.
