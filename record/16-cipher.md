# 16. The password cipher

The NIDA system books are password-protected. A lesson runtime opens them without presenting the password. Instructor and the author path are what ask. This chapter records where the cipher is and how the addition works. Section 16.6 is the empty-key branch and the ciphertext stored on the NIDA system books. The keyed 10-byte path in 16.2 is still open. The short strings tried against a stand-in key are not that password.

## 16.1 Where it lives

`TBCBT.DLL`, NE segment 7. Ghidra's name for that segment is `Code7`, base `1030`. The usual map is `0x1000 + (N - 1) * 8`, so segment 7 is `1030`. NE segment numbers stay fixed. Live selectors change. Segment 7 was not mapped in the SoftICE session that listed TBCBT code segments `01`, `0E`, `02`, `0B`, `08`, `0D`, `04`, and `03`. Those loaded segments are stubs and KERNEL/USER imports, not the cipher.

Exports on this path: `MAKEKEYEDPASSWORD`, `MAKEKEYEDPASSWORDEX`, `KEYEDPASSWORDENCRYPT`, `KEYEDPASSWORDENCRYPTEX`, `ENCRYPT`, `ENCRYPTEX`, `DECRYPT`, `DECRYPTEX`, `DECRYPTFILE`, `CREATEENCRYPTEDFILE`, `READENCRYPTEDFILE`, `WRITEENCRYPTEDFILE`.

The book path is `MAKEKEYEDPASSWORDEX` then `KEYEDPASSWORDENCRYPTEX`.

`TB80RCA.DLL` is Asymetrix UI (ASYMBITMAP, STATIC, TABS, spell, palette, BMR). It is not on the book-open path and not on the password path. `TB80ATH.EXE` is the 16-bit author and runs under NTVDM. The 32-bit pieces on a lesson launch are the launcher and the thunk (`TB80RUN`, `TB80W32`, `TB80MAIN`), not the cipher.

## 16.2 Three addition schemes

From `MAKEKEYEDPASSWORDEX`, `KEYEDPASSWORDENCRYPTEX`, and `FUN_1030_1046`. Inverse of each is `plain = (cipher - key) & 0xFF`.

| Scheme | Add | Key byte |
|---|---|---|
| `(0xA01, 0x300)` | `toupper` of the key byte | From a 10-byte table. Index is `local_16 % 10`, then `+ 0x32`. |
| `(1, 0x400)` | `toupper` of the key byte, wrap at `0xFF` | Same table. |
| `(1, 0x700)` | The raw key byte, wrap at `0xFF` | Same table. |

The live key is the 10 bytes that table selects. It is not the ASCII the user types. A test that encrypts `"nida"` or `"adin"` with a stand-in key `A`–`J` only checks the adder. It does not recover a book.

After a failed password dialog, search memory for the typed ASCII and for the constants `0xA01` and `0x300`. That finds the call site even while segment 7 is unloaded. Clicking OK and accepting "Wrong password" is the intended setup for that search. The dialog procedure itself is an ordinary Windows dialog.

## 16.3 What a with-password file difference is

A small book saved with a password and the same book saved without one differ from file offset `0xCEC` onward. The tails do not reconverge. The extra length is 1526 bytes of shift, not 1526 bytes of cipher text sitting at the end.

The local blob at the first difference begins:

```
c9 18 03 00 00 00 00 00 14 00 00 f0 00 00 77 2e
18 00 77 2e 6e 00 00 00 0c 45 00 00 7a 45 00 00
54 00 16 0d 00 00 0b 00 98 05 56 0e 00 00 00 00
```

The stand-in key does not decrypt it. Brute-force hits that came back short (`vgah`, `ap1`, `db9`, `iud`, `lxg`, `t57`, `vga`, `3p1`, `3ro`, `9e4`) are not the book password. They are discarded.

## 16.4 What is still open

This section is the keyed path only. The empty-key branch is 16.6 and does not use this table. The 10-byte key used on a real NIDA `.sbk` has not been captured. Segment 7 has not been stepped on a failed password. Until that capture exists, do not treat a decrypted string from the stand-in key as a finding.

## 16.5 Author password does not load TBCBT

On 16 October 2026 the author asked for `C:\TBK\nc81base.sbk`: "Please enter the password to gain Author level access." The next box said that password was not correct. The window title stayed `(Untitled)`, then became `ssssssssssss.tbk`. The system book did not open.

`ssssssssssss.tbk` became a password-protected book in that same session. `TBCBT.DLL` was not in the module list. The Extensions dialog on that book is the machine's OLE registry (`LMRT.DLL` and the other registered controls). It is not the `linkDLL` set, and `TBCBT` is not an entry on it.

Writing the author password stores the property block in section 16.3. It does not map segment 7. `TBCBT` is present only when a handler `linkDLL`s it. A new book has no such handler. A refused system book never runs its script, so it does not link the DLL either.

The stops while `ssssssssssss.tbk` was current:

| Stop | What it did |
|---|---|
| `??0TASKCOLLECTION` | UTL constructor. One `0x3C`-byte block. The flags word pushed is `0x2042` (movable, zeroed, shared). Called twice, two incoming selectors. |
| `GETTBKINIPROFILESTRING` | Reads `tbk.ini`. `AX` held a pointer (`AEA0`, `AD62`) when a string was found, and `0000` when it was not. |
| `GETTBKINIPROFILEINT` | Same file. The default at `[bp+6]` was `0x32D0`, then `0x3304`. `AX` came back `0000` both times. |
| `TB80ATH` `4E67:0642` | The author EXE. `AX` was `4E2F`, so the `je` was not taken. Stores ES, CX+`0x100`, SI, DI, BX (`0x80`), and DX at `DS:305C`. |
| `GETCHARINFO` | Returns the cached dword at UTL `DS:0518`. That dword was zero. |
| `GETSTRMGRSTRING` | String id at `[bp+6]` was `0001`, then the function decrements it. Id `0` is the empty case. |
| `GETDATA@TASKCOLLECTION` | Lookup. Arguments were `0000` and `42F7`. |
| `OBJFILEOPEN` | BAS, `enter 025A` (602-byte frame). This is the open of the `.tbk`. `BX` was `0x50`, `CX` was `0x32D`. |

After the status line "The task has completed running", every register was zero and the assembly pane was `????`. The `OLEUI*`, `DATASTUB*`, and `COPENSCRIPT` names on that screen are the export list of a dead task. They did not run.


## 16.6 Empty key

`ENCRYPTEX` with an empty key does not use the 10-byte table in 16.2. The nine bytes at `DS:0x28` are `BMWBMWBMW`, indexed by position modulo 9. A letter encrypts as `((K + c - 0x82) mod 58) + 0x41`. The inverse is what `DECRYPTEX` does: subtract `K`, and if the result is negative add 58, then add `0x41`. `cipher/empty_key.py` is that pair. It is not the keyed branch.

**Known.** `62 6d 77 62` decrypts to `aaaa`. One `a` encrypts to `62`.

**Known.** `nc81base.sbk` stores `62 70 49 6a 7a` at file `0x1F6C`. That decrypts to `admin`. The same five bytes are in `NC81BANK.SBK`, `nc81recs.sbk`, `nc81test.sbk`, and `nc81trnr.sbk`. Round-trip of `admin` produces those bytes. This is the author password those books store. It is not required to read the records.

The keyed path in 16.4 is unchanged.
