"""Long-running NIDA password brute forcer.

Resumable. Writes progress to nidabrute_state.txt and hits to nidabrute_hits.txt.
Run: python3 tb_nidabrute_long.py [path/to/nc81base.sbk]

Covers:
  - 1-6 lowercase
  - 1-6 digits
  - 1-5 alnum (lower+digit)
  - 4-6 lower with common suffixes (1, 12, 123, !, 97, 02)
"""

import itertools
import os
import sys
import time
from tb_password import encrypt

KEY = b"MARY HELLE"
STATE = "nidabrute_state.txt"
HITS = "nidabrute_hits.txt"

def load_state():
    if os.path.exists(STATE):
        return open(STATE).read().strip()
    return ""

def save_state(label):
    open(STATE, "w").write(label)

def search(nc, label, charset, length, hits_f, start_from=""):
    n = len(charset) ** length
    print(f"=== {label} ({n}) ===", flush=True)
    skipping = bool(start_from)
    tested = 0
    t0 = time.time()
    for chars in itertools.product(charset, repeat=length):
        pw = "".join(chars)
        if skipping:
            if pw == start_from:
                skipping = False
            else:
                continue
        c = encrypt(pw, KEY)
        if c in nc:
            msg = f"HIT {pw!r} {c.hex()} at {nc.find(c):#x}"
            print(msg, flush=True)
            hits_f.write(msg + "\n")
            hits_f.flush()
        tested += 1
        if tested % 100000 == 0:
            save_state(f"{label}:{pw}")
            elapsed = time.time() - t0
            rate = tested / elapsed if elapsed else 0
            print(f"  {pw}  {tested}  {rate:.0f}/s", flush=True)
    save_state(f"{label}:DONE")
    print(f"  {label} done ({tested})", flush=True)

def main():
    book = sys.argv[1] if len(sys.argv) > 1 else "nc81base.sbk"
    nc = open(book, "rb").read()
    print(f"loaded {book} ({len(nc)} bytes)", flush=True)
    state = load_state()
    print(f"resume from: {state or '(start)'}", flush=True)
    hits_f = open(HITS, "a")

    jobs = [
        ("lower1", "abcdefghijklmnopqrstuvwxyz", 1),
        ("lower2", "abcdefghijklmnopqrstuvwxyz", 2),
        ("lower3", "abcdefghijklmnopqrstuvwxyz", 3),
        ("lower4", "abcdefghijklmnopqrstuvwxyz", 4),
        ("lower5", "abcdefghijklmnopqrstuvwxyz", 5),
        ("lower6", "abcdefghijklmnopqrstuvwxyz", 6),
        ("digit1", "0123456789", 1),
        ("digit2", "0123456789", 2),
        ("digit3", "0123456789", 3),
        ("digit4", "0123456789", 4),
        ("digit5", "0123456789", 5),
        ("digit6", "0123456789", 6),
        ("alnum3", "abcdefghijklmnopqrstuvwxyz0123456789", 3),
        ("alnum4", "abcdefghijklmnopqrstuvwxyz0123456789", 4),
        ("alnum5", "abcdefghijklmnopqrstuvwxyz0123456789", 5),
    ]

    resume_label, resume_pw = ("", "")
    if ":" in state:
        resume_label, resume_pw = state.split(":", 1)
        if resume_pw == "DONE":
            resume_label, resume_pw = ("", "")

    started = not resume_label
    for label, charset, length in jobs:
        if not started:
            if label == resume_label:
                started = True
                search(nc, label, charset, length, hits_f, resume_pw)
            continue
        search(nc, label, charset, length, hits_f)

    hits_f.close()
    print("all jobs done", flush=True)

if __name__ == "__main__":
    main()
