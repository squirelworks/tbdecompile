"""Recover ToolBook key bytes from a known plaintext/ciphertext pair.

For the addition schemes:
  key[i] = (cipher[i] - plain[i]) & 0xff

No search required once you have both sides.
"""

import argparse
from tb_password import derive_key, encrypt, SCHEMES


def recover(plain, cipher, scheme):
    pw = plain.upper().encode("latin1")
    p1, p2 = scheme
    key = []
    for i, c in enumerate(pw):
        cb = cipher[i]
        if p1 == 0xa01 and p2 == 0x300:
            k = (cb - c) & 0xff
            # undo toupper assumption: k was uppercased before add
            key.append(k)
        elif p1 == 1 and p2 == 0x400:
            key.append((cb - c) & 0xff)
        elif p1 == 1 and p2 == 0x700:
            key.append((cb - c) & 0xff)
        else:
            raise ValueError(scheme)
    return bytes(key)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plain", required=True)
    ap.add_argument("--cipher", help="hex")
    ap.add_argument("--cipher-file")
    ap.add_argument("--scheme", default="a01,300")
    args = ap.parse_args()

    if args.cipher:
        cipher = bytes.fromhex(args.cipher)
    else:
        cipher = open(args.cipher_file, "rb").read()

    p1, p2 = (int(x, 16) for x in args.scheme.split(","))
    scheme = (p1, p2)
    key = recover(args.plain, cipher, scheme)
    print(f"recovered key bytes: {key.hex()}  {key!r}")

    # verify round-trip
    # We only have len(plain) key bytes; pad/truncate for the check
    trial = encrypt(args.plain, key, scheme)
    print(f"round-trip match: {trial == cipher[:len(trial)]}")


if __name__ == "__main__":
    main()
