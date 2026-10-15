# 16. The password cipher

The NIDA system books are password-protected. A lesson runtime opens them without presenting the password. Instructor and the author path are what ask. This chapter records where the cipher is and how the addition works. It does not record a working book password. The short strings tried against a stand-in key are not that password.

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

The 10-byte key used on a real NIDA `.sbk` has not been captured. Segment 7 has not been stepped on a failed password. Until that capture exists, do not treat a decrypted string from the stand-in key as a finding.
