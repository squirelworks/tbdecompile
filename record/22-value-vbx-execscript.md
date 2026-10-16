# 22. Value, VBX, and EXECSCRIPT

These are three mechanisms. A name belongs to one of them, or to none. It does not belong to two.

A VBX is a Visual Basic extension control. It is not the `0x76` page object. The value bus is not a VBX. `EXECSCRIPT` is not a VBX. The page object is chapter 4. The heap tags are chapter 19. The book API that locks the page object is chapter 20. This chapter is the split between the three names that get confused with that object.

## Claims

| Id | Grade | Statement | Source |
|---|---|---|---|
| V-001 | Known | A script value is a tag and a payload. `VALUENEWLONG` is tag `0xB`, four bytes. `VALUENEWDOUBLE` is `0xA`, eight. `VALUENEWSTACK` is `0x10`, a `0xC`-byte header. | Chapter 19, the `TBHEAPALLOC` sites |
| V-002 | Known | `CDBGETVALUE`, `CDBSETVALUE`, and `CDBSENDVALUE` are one call into the `EX` form. The `EX` form locks the `0x76` object, calls the code pointer in the slot, and unlocks. The value is what is passed. The object is what is locked. | Chapter 20 |
| V-003 | Known | `VBXINIT` loads `TB80VBX.DLL` and calls `GetProcAddress` for `VbxInit`. It does not allocate the view. | Appendix K, the body that was read |
| V-004 | Known | `VBXNEWVIEW` pushes `0x11C` and calls far. The view magic in that reading is `0xABC1`. The size is not `0x76`. | `maps/wdw-to-ghidra.md`; Appendix K |
| V-005 | Known | `TBXEXECSCRIPT` is BAS ordinal 405 at `1268:060c`, decompile line 115148. The other five names in the family are separate exports. | BAS export map |
| V-006 | Thought | `EXECSCRIPT` is the TBX edge that runs a script. The bodies were not read. The stack thunks that were read are one call and a return. That shape is not claimed for this family. | The names, and chapter 19 on the thunks that were read |
| V-007 | Not true | A VBX view, a script value, and `EXECSCRIPT` are the page object, or are each other. | This chapter |

## 22.1 Value

The constructors whose tags were read:

| Export | Tag | Size |
|---|---|---|
| `VALUENEW` | `0` | The caller's |
| `VALUENEWSTRING` | `9` | `param_1 + 3` |
| `VALUENEWDOUBLE` | `0xA` | 8 |
| `VALUENEWLONG` | `0xB` | 4 |
| `VALUENEWPOINT` | `0xC` | 4 |
| `VALUENEWRECT` | `0xD` | 8 |
| `VALUENEWDATE` | `0xE` | 7 |
| `VALUENEWTIME` | `0xF` | 3 |
| `VALUENEWSTACK` | `0x10` | `0xC` |
| `VALUENEWCSTR` | `0x11` | In the helper, not in the export's own body |
| `VALUENEWCOLORTABLE` | `0x12` | `0x100` |
| `VALUENEWICON` | `0x13` | `param_1 + 2` |

`VALUENEWBOOK`, `VALUENEWRESOURCE`, and `VALUENEWGRAPHIC` are constructors in segment `4267`. The `enter` sizes on the one-boot capture are frame sizes. They are not the tags in the table. A frame of `0xE` is not tag `0xE`, and tag `0xE` is a date.

`TBXVALUENEWSTACK` is a thunk onto the value constructor. It is still the value mechanism. The `TBX` stem does not make it `EXECSCRIPT`.

The bus is `CDBGETVALUE`, `CDBSETVALUE`, `CDBSENDVALUE`, the `EX` forms, and `CDBPARENTVALUE`, `CDBDEREFVALUE`, `CDBLOCKVALUE`. They use a value. They are not a value allocation, and they are not a VBX.

## 22.2 VBX

A VBX is a Visual Basic extension control. The host module is `TB80VBX.DLL`. A file that ends in `.vbx` is the control that host loads. BAS does not implement the control. BAS reaches the host.

| Export | What the body is | What it is not |
|---|---|---|
| `VBXINIT` | Loads `TB80VBX.DLL`. `GetProcAddress` of `VbxInit`. | Not the allocator. Not a view. |
| `VBXNEWVIEW` | The view. `0x11C` bytes. Magic `0xABC1`. | Not `0x76`. Not a script value. |
| `CDBREGISTERVBXFORM` | Registers a form. Seen on open. Not the reader. | Not `VBXNEWVIEW`. |

`TB80VBX` does not name `TB80BAS` in the module-reference table. The call goes the other way: BAS loads the DLL. Opening `TB80VBX.DLL` is a different image. The decompiler will not follow `GetProcAddress` into it.

## 22.3 EXECSCRIPT

| Export | Line | Address, when the map has one |
|---|---|---|
| `TBXEXECSCRIPT` | 115148 | Ordinal 405, `1268:060c` |
| `TBXEXECSCRIPT_CALLBACK` | 115128 | `1268:0488` |
| `TBXEXECSCRIPTDYNAMIC` | 115215 | |
| `TBXEXECSCRIPTVARIANT` | 115231 | `1268:0516` |
| `TBXAUTOEXECSCRIPTVARIANT` | 115293 | `12F8:0018` |
| `TBXEXECSCRIPTVARIANTSPCL` | 115358 | `1008:09F8` |

These are six exports. They are not one function with six names. The body grade is Thought, and only for the role: the TBX edge that runs a script. The operation is not Known until a body is read. Do not fill the gap with the stack thunks. Do not file the family under VBX because both words sit near "control" in a search.

## 22.4 What the suite does with the split

The classifier lives in `openscript_analysis` only. Foolversity does not keep a second copy. `CDBGETVALUE` and `CDBREGISTERVBXFORM` are the book API, in `cdb.py`. `OBJFILEOPEN` and `OBJNEWNEAR` are the object file, in `obj.py`. Those two are not the same record: the book API locks an object and does not allocate it, and the object layer is the `0x76` array. `VALUENEWLONG` stays a heap constructor. `VBXNEWVIEW` stays the control view. `TBXEXECSCRIPT` stays the script edge. A value constructor refuses a size of `0x76`.
