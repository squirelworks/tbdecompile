"""Long-running NIDA password search.

Encrypts candidates with MARY HELLE and searches nc81base.sbk.
Writes hits to nidabrute_hits.txt as it goes.
"""

import itertools
import sys
import time
from tb_password import encrypt

KEY = b"MARY HELLE"
BOOK = "/workspace/artifacts/Toolbook/NIDA/nc81base.sbk"
OUT = "/workspace/artifacts/tbworkingpapers/tbwp0004/nidabrute_hits.txt"

def main():
    nc = open(BOOK, "rb").read()
    print(f"loaded {len(nc)} bytes", flush=True)
    hits = open(OUT, "w")
    start = time.time()
    tested = 0

    # 1-6 char lowercase, then digits, then mixed short
    charsets = [
        ("lower4", "abcdefghijklmnopqrstuvwxyz", 4),
        ("lower5", "abcdefghijklmnopqrstuvwxyz", 5),
        ("digit4", "0123456789", 4),
        ("digit5", "0123456789", 5),
        ("lower3digit", "abcdefghijklmnopqrstuvwxyz0123456789", 3),
    ]

    for label, charset, length in charsets:
        n = len(charset) ** length
        print(f"=== {label}: {n} ===", flush=True)
        for i, chars in enumerate(itertools.product(charset, repeat=length)):
            pw = "".join(chars)
            c = encrypt(pw, KEY)
            if c in nc:
                msg = f"HIT {pw!r} cipher={c.hex()} at {nc.find(c):#x}"
                print(msg, flush=True)
                hits.write(msg + "\n")
                hits.flush()
            tested += 1
            if tested % 50000 == 0:
                elapsed = time.time() - start
                print(f"  {tested} tested, {elapsed:.0f}s", flush=True)
        print(f"  {label} done", flush=True)

    hits.close()
    print(f"finished {tested} in {time.time()-start:.0f}s", flush=True)

if __name__ == "__main__":
    main()
