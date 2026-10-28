"""ToolBook password crypto, from TBCBT.DLL.

MAKEKEYEDPASSWORDEX / ENCRYPTEX / FUN_1030_1046.

Schemes tried by the verifier:
  (0xa01, 0x300)  — addition of upper(key) to each char
  (1,     0x400)  — addition, wrap at 0xff
  (1,     0x700)  — addition of raw key byte, wrap at 0xff
"""

def _toupper(b):
    return b - 32 if 97 <= b <= 122 else b


def derive_key(table10):
    """10-byte key from the local_16 % 10 + 0x32 loop."""
    key = []
    i = 0
    while i < 0x14:
        key.append(table10[i % 10])
        if i == 8:
            i = 9
        i += 2
    return bytes(key)


def encrypt(password: str, key: bytes, scheme=(0xa01, 0x300)) -> bytes:
    """ENCRYPTEX for the three scheme pairs."""
    pw = password.upper().encode("latin1")
    p1, p2 = scheme
    out = []
    for i, c in enumerate(pw):
        k = key[i % len(key)]
        if p1 == 0xa01 and p2 == 0x300:
            out.append((_toupper(k) + c) & 0xff)
        elif p1 == 1 and p2 == 0x400:
            s = (_toupper(k) + c) & 0xff
            out.append(s if s < 0x100 else s % 0xff)
        elif p1 == 1 and p2 == 0x700:
            s = (k + c) & 0xff
            out.append(s if s < 0x100 else s % 0xff)
        else:
            raise ValueError(f"unknown scheme {scheme}")
    return bytes(out)


def decrypt(cipher: bytes, key: bytes, scheme=(0xa01, 0x300)) -> str:
    """Inverse of encrypt for the addition schemes."""
    p1, p2 = scheme
    out = []
    for i, c in enumerate(cipher):
        k = key[i % len(key)]
        if p1 == 0xa01 and p2 == 0x300:
            out.append((c - _toupper(k)) & 0xff)
        elif p1 == 1 and p2 == 0x400:
            out.append((c - _toupper(k)) & 0xff)
        elif p1 == 1 and p2 == 0x700:
            out.append((c - k) & 0xff)
        else:
            raise ValueError(f"unknown scheme {scheme}")
    return bytes(out).decode("latin1", "replace")


SCHEMES = [(0xa01, 0x300), (1, 0x400), (1, 0x700)]


def verify(password: str, cipher: bytes, key: bytes) -> tuple:
    """FUN_1030_1046: try each scheme until one reproduces the cipher."""
    for scheme in SCHEMES:
        trial = encrypt(password, key, scheme)
        if trial == cipher[:len(trial)]:
            return True, scheme
    return False, None


if __name__ == "__main__":
    # Demo with a stand-in key (real key is DS:0x32 in the runtime)
    table = list(range(0x41, 0x4b))  # 'A'..'J'
    key = derive_key(table)
    print("key:", key)
    for pw in ("nida", "adin"):
        c = encrypt(pw, key)
        print(f"  {pw!r} -> {c.hex()}  verify={verify(pw, c, key)}")
