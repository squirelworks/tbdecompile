#!/usr/bin/env python3
"""Empty-key book password cipher from TBCBT.DLL ENCRYPTEX / DECRYPTEX.

The nine key bytes live at DS:0x28 and are indexed by position % 9.
Ghidra's WBMWBMW label starts two bytes into that table. A non-empty key
is a different branch and is not this script.

  python3 empty_key.py enc a
  python3 empty_key.py enc aaaa
  python3 empty_key.py dec 626d7762
  python3 empty_key.py dec --ascii bmwb
"""

import sys

KEY = b"BMWBMWBMW"


def encrypt(plain: bytes) -> bytes:
    out = bytearray()
    for i, c in enumerate(plain):
        k = KEY[i % 9]
        if c < 0x41 or (0x5A < c < 0x61):
            raise ValueError(f"byte {c:#04x} at {i} is rejected (error -10)")
        if c < 0x7B:
            out.append(((k + c - 0x82) % 0x3A) + 0x41)
        else:
            v = (k + c + 0xBF) & 0xFF
            out.append(0x1B if v == 0 else v)
    return bytes(out)


def decrypt(cipher: bytes) -> bytes:
    out = bytearray()
    for i, c in enumerate(cipher):
        k = KEY[i % 9]
        if c < 0x41 or c > 0x7A:
            if c == 0x1B:
                c = 0
            out.append(((c - k) & 0xFF) + 0x41 & 0xFF)
        else:
            v = c - k
            if v < 0:
                v += 0x3A
            out.append(v + 0x41)
    return bytes(out)


def main(argv):
    if len(argv) < 2 or argv[0] not in ("enc", "dec"):
        print(__doc__.strip())
        return 2
    if argv[0] == "enc":
        if len(argv) != 2:
            print(__doc__.strip())
            return 2
        print(encrypt(argv[1].encode("latin1")).hex())
        return 0
    raw = argv[1:]
    if raw and raw[0] == "--ascii":
        if len(raw) != 2:
            print(__doc__.strip())
            return 2
        blob = raw[1].encode("latin1")
    elif len(raw) == 1:
        blob = bytes.fromhex(raw[0])
    else:
        print(__doc__.strip())
        return 2
    sys.stdout.buffer.write(decrypt(blob) + b"\n")
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 1:
        assert encrypt(b"a") == bytes.fromhex("62")
        assert encrypt(b"aaaa") == bytes.fromhex("626d7762")
        assert decrypt(bytes.fromhex("626d7762")) == b"aaaa"
        assert decrypt(encrypt(b"Nida")) == b"Nida"
        print("ok")
    else:
        sys.exit(main(sys.argv[1:]))
