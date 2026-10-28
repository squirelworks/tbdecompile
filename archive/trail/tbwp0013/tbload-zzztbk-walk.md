# Tbload Walk: ZZZTBKBOOKLOC to the 16-bit Boundary

> Trail, 2026-10-16. Chapters 2 and 17. Marker search and the unresolved vtable+4. If this sheet and `TBdecompile/record/` disagree, the record wins.

Date: 2026-10-14  
Source: `/workspace/attachments/Tbload.exe.html`

## Path

1. **String**  
   `.data:s_ZZZTBKBOOKLOC_0040c61c` = `"ZZZTBKBOOKLOC"`

2. **FUN_00405460** (00405460)  
   - Pushes the string, length `0xa`, and the caller's buffer.  
   - Calls `FUN_00405420` (search helper).  
   - On return: `CMP byte ptr [ESI], 0x42` then `MOV byte ptr [ESI], 0x3`.  
   - The `0x42` is the 'B' of the JBO signature that follows the marker; the write of `0x3` is the book-version byte.

3. **FUN_00405420** (search)  
   - Calls `FUN_004051b0` (likely a file-map or buffer search).  
   - Returns success/failure.

4. **Caller: FUN_00406a70** (00406a70)  
   - Calls `FUN_00405460`.  
   - On success:  
     ```
     MOV ECX, [ESI+4]          ; object
     MOV EDX, [ECX]            ; vtable
     PUSH 4
     PUSH ESI
     PUSH EAX                  ; search result
     PUSH EDI                  ; buffer
     CALL dword ptr [EDX+4]    ; virtual call
     ```
   - This virtual call is the first handoff out of the pure 32-bit search path.

## 16-bit boundary

The virtual call at **00406aa1** (`CALL dword ptr [EDX+4]`) is the first call that leaves the ZZZTBKBOOKLOC search. The vtable itself is not yet resolved in this listing.  

Other process-launch sites exist but are not on this path:
- `WinExec` at 00402bfe (FUN_00402b80, used for older TB30/TB40/TB50 paths and TB80TRIAL)
- `CreateProcessA` at 00402f34 / 00403078
- `LoadLibraryA` of WININET.DLL and user32.dll only

No direct string reference to `TB80NET.EXE` or `TB80RTM.EXE` appears in this Tbload image. The 16-bit engine entry is therefore behind the vtable slot at `[EDX+4]`, not a named WinExec.

## Next cut

Resolve the vtable that is stored at the book-object `+4` and identify the function at slot `+4`. That function is the first code that crosses into the 16-bit side (or into the thunk that does).
