# CDBUNIONDAMAGE (TB80BAS) static read
Written 2026-10-25 (Asia/Tokyo). File-only: no repo write, no Bochs action. Marked **[read]** (straight from the bytes or the NE tables) or **[inferred]**.
Disassembly is `objdump -D -b binary -m i8086` of segment 4 (`reports/cdb-work/seg4.bin`, 0x1b50 bytes). Offsets are segment offsets. Branch/call targets in `call 0x...` are resolved; far-call operands show NE relocation chain links, so I resolved them from the reloc table (`import_sites.json`).

## 0. Module and source
- Searched `/workspace` and `/workspace/bochs/extracted`: `TB80BAS.DLL` is at `bochs/extracted/TBK/TB80BAS.DLL` (identical to `.../TBSystem/`; 683,872 bytes, NE, 199 segments, segment data compressed) and the expanded copy `unpacked/TB80BAS.DLL` (1,163,488 bytes, same NE header). I disassembled the unpacked copy. Existing work used: `decomp/TB80BAS.DLL.c` (Ghidra decompile, names `FUN_1018_xxxx`, segment 4 = Ghidra 1018), `bochs/README.md`, `bochs/logs/tb80bas_segments_moduledb.txt`.
- Export **CDBUNIONDAMAGE = ordinal 288**, a non-resident name **[read]**. Entry table: ordinal 288 -> **segment 4, offset 0x014c (332), flags 3** (Ghidra 1018:014c). Segment 4 (alloc 0x1b50) sits at file offset 0xfb80 in the unpacked copy, so the entry is at file offset **0xfccc**. In the original guest file segment 4 is stored compressed (0xb500, len 0xe8f), so its code bytes are not searchable there.

## 1. Entry point and arguments
```
 14c:  b8 ff ff        mov  $0xffff,%ax        ; reloc 0x14d: selector of DGROUP (seg 199)
 14f:  c8 0a 00 00     enter $0xa,$0x0         ; 10 bytes of locals
 153:  1e              push %ds
 154:  8e d8           mov  %ax,%ds
 156:  8d 46 fe        lea  -0x2(%bp),%ax
 159:  50              push %ax                ; &local_4 (word)
 15a:  ff 76 06        push 0x6(%bp)           ; THE ONLY ARGUMENT
 15d:  6a 03           push $0x3
 15f:  9a fc 02 ff ff  lcall 1030:02fc         ; reloc 0x162 -> seg 7 (Ghidra 1030): FUN_1030_02fc(3, arg, &local)
 164:  0b c0           or   %ax,%ax
 166:  74 7f           je   0x1e7              ; arg rejected -> return
 168:  8b 1e e0 01     mov  0x1e0,%bx          ; DS:[01e0] = the object actually used
 16c:  83 7f 72 00     cmpw $0x0,0x72(%bx)
 170:  74 75           je   0x1e7
 ...
 1e7:  1f pop %ds ; c9 leave ; ca 02 00  lret $0x2
```
- **Exactly one stack argument, a 16-bit word** at `[bp+6]` (`lret $2`). Far frame: `[bp+0]` old bp, `[bp+2]` IP, `[bp+4]` CS, `[bp+6]` arg. At a breakpoint on 4:014c: `[sp]`=IP, `[sp+2]`=CS, `[sp+4]`=arg **[read]**.
- The arg is only checked: `FUN_1030_02fc(3, arg, &local)` fails when mode 3 and `(arg & 1) != 0` (it wants an even value, i.e. a near object pointer) or the value mismatches a global (decompile, lines 23797+) **[read from decompile]**. So it is a near pointer to a view/object, as you said; it is **not a rectangle** and is never used again **[read]**.
- **No rectangle argument exists.** The object used afterwards is the global `DS:[0x01e0]` (`mov 0x1e0,%bx`, then `push 0x1e0` before each call below) **[read]**. That it is "the current view" is **[inferred]**.
- Guard: `[DS:[01e0]+0x72] != 0` or the function returns without doing anything.

## 2. The call to 026c (layer 0) and its 8 bytes
```
 172:  53              push %bx            ; (this, for 0b00: arg 1)
 173:  6a 00           push $0x0           ; layer 0
 175:  8d 46 f6        lea  -0xa(%bp),%ax  ; buffer at bp-0xa .. bp-3  (8 bytes)
 178:  16              push %ss
 179:  50              push %ax            ; far ptr ss:(bp-0xa)
 17a:  0e              push %cs
 17b:  e8 82 09        call 0xb00          ; FUN_1018_0b00(buf, layer, this): FILLS the buffer
 17e:  ff 36 e0 01     push 0x1e0          ; this
 182:  6a 00           push $0x0           ; layer 0
 184:  8d 46 f6        lea  -0xa(%bp),%ax
 187:  16              push %ss
 188:  50              push %ax            ; far ptr ss:(bp-0xa) = the 8 bytes
 189:  0e              push %cs
 18a:  e8 df 00        call 0x26c          ; FIRST CALL TO 026c (next IP 0x18d, +0xdf = 0x26c)
```
- Pascal order (callee `lret $8`): 026c(`this` = DS:[01e0], `layer`, `seg`, `off`). In 026c: `[bp+0xc]`=this, `[bp+0xa]`=layer, `[bp+8]`=buffer segment (SS), `[bp+6]`=buffer offset **[read]**.
- **The 8 bytes are passed by far pointer, not by value**: SS:(BP-0xa) of CDBUNIONDAMAGE's own frame (a local 8-byte buffer; `bp-2` is the 2-byte `local_4`) **[read]**.
- Stack at the instant of `call 0x26c` (before executing 4:018a): `[sp]`=CS(pushed), `[sp+2]`=buffer offset, `[sp+4]`=SS, `[sp+6]`=layer (0), `[sp+8]`=DS:[01e0] value. Stack at entry of 026c (4:026c): `[sp]`=IP 0x18d, `[sp+2]`=CS, `[sp+4]`=buffer offset, `[sp+6]`=buffer seg, `[sp+8]`=layer, `[sp+0xa]`=this **[read]**.

## 3. "Four times with the same 8 bytes": partly wrong
- Four calls, layers 0, 1, 2, 3, at offsets **0x18a, 0x1a8, 0x1c6, 0x1e4** (`push $0/$1/$2/$3` before each) **[read]**, all with the **same buffer address** ss:(bp-0xa).
- **The contents are not the same.** Before every 026c call the function calls `0b00` again with the same buffer and the next layer (call sites 0x17b, 0x199, 0x1b7, 0x1d5), and `0b00` rewrites all 8 bytes **[read]**:
```
 b18:  26 ff 77 08     push %es:0x8(%bx)   ; layer record +8 (an HRGN)
 b21:  9a 34 0b 00 00  lcall GDI.134 (GetRgnBox)  ; (hrgn, ss:bp-0xc)  -> tmp rect
 b29:  26 ff 77 0a     push %es:0xa(%bx)   ; layer record +0xa (another HRGN)
 b2d/b30: push 0x8(%bp) ; push 0x6(%bp)    ; the caller's buffer
 b33:  9a 99 0c 00 00  lcall GDI.134 (GetRgnBox)  ; (hrgn2, buffer)   -> buffer = bbox of region 2
 b49:  9a e5 00 00 00  lcall USER.80 (UnionRect)  ; (buffer, buffer, tmp) -> buffer = union of both boxes
 b62:  9a 93 0b ..     lcall TB80UTL.9 (CLIENTTOPAGE)  ; point (buffer+0, buffer+2) -> back into buffer+0..3
 b92:  9a 12 09 ..     lcall TB80UTL.9 (CLIENTTOPAGE)  ; point (buffer+4, buffer+6) -> back into buffer+4..7
```
  Names for GDI.134 / USER.80 / TB80UTL.9 come from the Ghidra decompile of 0b00 (`GETRGNBOX`, `UNIONRECT`, `CLIENTTOPAGE`, decomp line 16902) and the export name of TB80UTL ordinal 9 (`CLIENTTOPAGE`) **[read]**.
- So each layer's 8 bytes = union of the bounding boxes of the layer record's two regions (record +8 and +0xa), converted by CLIENTTOPAGE **[read]**. Layer record address from `0e60(layer, this)` (jump table at 0xe74 = `0e9a 0ea6 0eb2 0eba 0eb2 0eba 0eb2 0eba`): layer 0 = `[this+0xa8]+0x29`, layer 1 = `[this+0xa8]+0x1d`, layer 2 = `this+0x8c`, layer 3 = `this+0x80` **[read]**.
- 026c skips the layer when the layer record has `[rec+4] != 0` (`cmpw $0x0,%es:0x4(%bx)` at 0x284 -> `jne 0x2eb`), so 0ee0 is not reached for it **[read]**.

## 4. 026c -> 1a44 -> 0ee0 and where SETRECTRGN happens
```
 28b:  ff 76 0c / ff 76 08 / ff 76 06     ; this, buf seg, buf off
 294:  8d 46 f4 / 16 / 50                 ; ss:(bp-0xc) = a SECOND local rect (8 bytes, bp-0xc..bp-5)
 299:  e8 a8 17        call 0x1a44        ; clip: FUN_1018_1a44(this, buf, ss:tmp)
 29c:  0b c0 ; 74 4b   je 0x2eb           ; empty -> return
 2a0:  ff 76 fa        push -0x6(%bp)     ; word 3 (bottom)  pushed FIRST
 2a3:  ff 76 f8        push -0x8(%bp)     ; word 2 (right)
 2a6:  ff 76 f6        push -0xa(%bp)     ; word 1 (top)
 2a9:  ff 76 f4        push -0xc(%bp)     ; word 0 (left)    pushed LAST
 2ac:  e8 31 0c        call 0xee0         ; FUN_1018_0ee0 (NEAR call, ret $8)
```
**What 0ee0 receives is not the raw 8 bytes**. 1a44 first fixes and clips them **[read]**:
```
1a44:  c8 10 00 00 enter $0x10 ; ... SetRect(ss:bp-8, 0, 0, [[this+0xa6]+0xc], [[this+0xa6]+0xe]) (USER.72, via reloc 0x1a5f)
1a69:  e8 ac f3  call 0xe18            ; normalise the 8 bytes IN PLACE:
 e1f:  26 8b 07 / 26 39 47 04 / 7d 11    ; if right(+4) < left(+0): swap them
 e40:  26 39 47 02 / 7e 16               ; if top(+2) > bottom(+6): swap them
1a7c:  lcall USER.79 (IntersectRect)     ; (ss:bp-0x10, ss:bp-8 = client rect {0,0,w,h}, the 8 bytes)
1a81:  0b c0 / 75 11                     ; empty -> SetRectEmpty(dst), return 0
1aa3:  9a dd 01 24 0c  lcall 1008:01dd(2, ss:bp-0x10, dst) ; copy result into the dst rect (026c's bp-0xc), return 1
```
So the order is: **normalise (swap left/right and top/bottom if reversed) -> intersect with the client rectangle {0, 0, [[this+0xa6]+0xc], [[this+0xa6]+0xe]} -> 0ee0**. No inflation anywhere in 026c, 1a44 or 0ee0. The `0xc`/`0xe` fields being the client width/height is **[inferred]** (SetRect right/bottom args).

0ee0 (near function, args at `[bp+4]`..`[bp+0xa]`, `ret $8`; Ghidra 1018:0ee0):
```
 ee0:  55 ; 8b ec           push bp ; mov bp,sp
 ee3:  83 3e 32 17 00       cmpw $0x0,0x1732        ; DS:[1732] = a cached HRGN
 ee8:  75 16                jne  0xf00
 eea:  8d 46 04             lea  0x4(%bp),%ax       ; &RECT = the 4 words on the stack
 eed:  16 ; 50              push %ss ; push %ax
 eef:  9a ff ff 00 00       lcall GDI.65 (CreateRectRgnIndirect)   ; first time only: region created from [bp+4..bp+0xb]
 ef4:  a3 32 17             mov  %ax,0x1732
 f00:  ff 36 32 17          push 0x1732             ; hrgn
 f04:  ff 76 04             push 0x4(%bp)           ; left   = word 0  (lowest stack word = last pushed by 026c)
 f07:  ff 76 06             push 0x6(%bp)           ; top    = word 1
 f0a:  ff 76 08             push 0x8(%bp)           ; right  = word 2
 f0d:  ff 76 0a             push 0xa(%bp)           ; bottom = word 3
 f10:  9a e5 0d 00 00       lcall GDI.172 (SetRectRgn)   ; SetRectRgn(hrgn, left, top, right, bottom); at 0xf10
 f15:  b8 01 00 ... c2 08 00   mov $1,%ax ... ret $8
```
- SETRECTRGN is at **0xf10** (when `[1732] != 0`; the first time the region is created by CreateRectRgnIndirect at 0xeef from the same four words) **[read]**. No normalising or inflating in 0ee0 **[read]**. GDI.172 is SetRectRgn and GDI.65 CreateRectRgnIndirect in the decompile (`SETRECTRGN`, `CREATERECTRGNINDIRECT`) **[read]**.
- bochs/README's hook at 0ee0 says "words 1-4 at entry = left, top, right, bottom"; this agrees: `[sp+2]`=left, `[sp+4]`=top, `[sp+6]`=right, `[sp+8]`=bottom at entry (`[sp]` = return IP).

## 5. Memory-order layout of the 8 bytes, units
- At the buffer (and at the clipped temp in 026c): **four 16-bit words in memory order = left, top, right, bottom**, i.e. a Windows RECT. Evidence: 0e18 swaps +0/+4 as one axis and +2/+6 as the other (`right<left`, `top>bottom` swap); 026c pushes word3, word2, word1, word0 so that word0 ends at `[bp+4]` and is used as SetRectRgn's left, word1 top, word2 right, word3 bottom **[read]**.
- Units: the code never converts to twips. 0b00 takes GetRgnBox boxes (GDI, device pixels), runs two CLIENTTOPAGE calls with arguments (1,0,0) **[read]**, then 026c intersects with a client-sized rectangle and 0ee0 passes it to SetRectRgn (device coordinates by definition). So at 0ee0 the values are **client/device pixels [inferred]**. What CLIENTTOPAGE does exactly (scroll/zoom offset, scale 1) is unverified: its body (TB80UTL 5:0x24a) scales by a call into a helper and adds an offset; I did not resolve the helper. At a live 1:1 view it is probably identity, **[inferred, not verified]**.

## 6. Finding the layer-0 call in a live trace
Selectors are per boot (README: re-derive from `info ldt`; the segment-4 code descriptor is the one with limit 0x1b5f, alloc 0x1b50; module DB lists seg 4 handle 0x2bde, sel 0x2bdf for one boot). Offsets in segment 4:
| what | seg 4 offset | file offset in `unpacked/TB80BAS.DLL` (= 0xfb80 + off) |
|---|---|---|
| CDBUNIONDAMAGE entry (`b8 <DGROUP sel> c8 0a 00 00`) | 0x014c | 0xfccc |
| layer 0 `call 0xb00` (fills buffer) | 0x017b | 0xfcfb |
| **first call to 026c (layer 0)** | **0x018a** (`e8 df 00`, ret IP 0x18d) | **0xfd0a** |
| layers 1 / 2 / 3 call 026c | 0x1a8 / 0x1c6 / 0x1e4 | 0xfd28 / 0xfd46 / 0xfd64 |
| 026c entry | 0x026c | 0xfdec |
| 0ee0 call inside 026c | 0x2ac | 0xfe2c |
| 1a44 clip function | 0x1a44 | 0x115c4 |
| 0ee0 entry / SETRECTRGN call | 0xee0 / 0xf10 | 0x10a60 / 0x10a90 |
- Runtime bytes to search (relocated; selectors vary): entry `b8 ?? ?? c8 0a 00 00 1e 8e d8 8d 46 fe 50 ff 76 06 6a 03 9a fc 02 ?? ?? 0b c0 74 7f`; the layer-0 call site `ff 36 e0 01 6a 00 8d 46 f6 16 50 0e e8 df 00`.
- Break at `4:0x018a` (before `call 0x26c`): word at `[ss:sp+2]` = buffer offset, `[sp+4]` = SS, `[sp+6]` = 0 (layer), `[sp+8]` = DS:[01e0] value; read the 8 bytes with `x /4hx ss:<offset>` = left, top, right, bottom **after** the preceding `call 0xb00` (so the layer-0 box). Or break at `4:026c` entry and read `[sp+4]` (offset), `[sp+6]` (seg). The pre-clip box is on the buffer; the post-clip box is at `[bp-0xc]` of 026c, readable at `4:0x2ac` (`call 0xee0`): words at `[sp+2]..[sp+8]`.
- A hit at 4:014c with `[sp+4]` odd, or with `[DS:1e0]+0x72 == 0`, will not reach 026c.

## 7. Not verified / limits
- Not run in Bochs; nothing was compared with Fred's live hits. Unverified: the exact unit semantics of CLIENTTOPAGE, the meaning of fields `[this+0x72]`, `[this+0xa6]+0xc/0xe`, and that `DS:[01e0]` is the current view.
- The "same 8 bytes" premise is only true for the buffer address; the contents are rewritten by 0b00 per layer (union of that layer's two region boxes).
- `unpacked/TB80BAS.DLL` was disassembled; I did not diff it against the guest's runtime memory. The Bochs README confirms the same bytes at 0ee0 (`55 8b ec 83 3e 32 17 00`) and the `b8 <DGROUP> c8` pattern.
- Files: `reports/cdb-work/seg4.bin` (7 kB of segment 4), `import_sites.json`, `utl.bin`.
