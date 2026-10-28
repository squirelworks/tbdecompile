#!/usr/bin/env python3
"""Turn each ToolBook system book into a JS module.

Usage: python3 sbk_to_js.py <directory with .sbk files> <output directory>
"""

import json
import sys
from pathlib import Path

MARK = bytes.fromhex("80650005000202")
CHUNK = b"\x14\x00\x00"


def cstr(buf, off, n):
    out = []
    for i in range(n):
        if off + i >= len(buf):
            break
        c = buf[off + i]
        if c == 0 or c < 32 or c > 126:
            break
        out.append(chr(c))
    return "".join(out)


def strings(blob):
    out = []
    cur = []
    for c in blob:
        if 32 <= c < 127:
            cur.append(chr(c))
        else:
            s = "".join(cur).strip()
            cur = []
            if len(s) >= 4 and s not in out:
                out.append(s)
    return out


def fields(blob):
    out = []
    start = 0
    while True:
        i = blob.find(b"Text\x00\x00", start)
        if i < 0:
            break
        start = i + 6
        if i + 16 > len(blob):
            continue
        length = int.from_bytes(blob[i + 14:i + 16], "little")
        if length < 8 or i + 16 + length > len(blob):
            continue
        raw = blob[i + 16:i + 16 + length]
        if raw[:1] not in (b"\r", b"\n"):
            continue
        text = raw.replace(b"\r", b"").decode("latin-1").strip()
        if text:
            out.append(text)
    return out


def jumps(blob):
    found = []
    start = 0
    while True:
        i = blob.find(b'("P', start)
        if i < 0:
            i = blob.find(b"(P", start)
        if i < 0:
            break
        j = i + 1
        if blob[j:j + 1] == b'"':
            j += 1
        k = j
        while k < len(blob) and 32 < blob[k] < 127 and chr(blob[k]).isalnum():
            k += 1
        name = blob[j:k].decode("ascii", "ignore")
        if name.startswith("P") and name not in found:
            found.append(name)
        start = k + 1
    return found


def objects(data):
    hits = []
    start = 0
    while True:
        i = data.find(MARK, start)
        if i < 0:
            break
        hits.append(i)
        start = i + 1
    out = []
    for n, off in enumerate(hits):
        nxt = hits[n + 1] if n + 1 < len(hits) else len(data)
        blob = data[off:nxt]
        sites = []
        p = 0
        while True:
            j = blob.find(CHUNK, p)
            if j < 0:
                break
            sites.append(j)
            p = j + 1
        out.append({
            "id": int.from_bytes(blob[7:11], "little"),
            "name": cstr(data, off + 11, 32),
            "offset": off,
            "size": len(blob),
            "sections": sites,
            "fields": fields(blob),
            "jumps": jumps(blob),
            "strings": strings(blob)[:80],
            "bm": blob.count(b"BM"),
            "jpeg": blob.count(b"\xff\xd8\xff"),
        })
    return out


def module(path, objs):
    body = json.dumps({
        "file": path.name,
        "size": path.stat().st_size,
        "objects": objs,
    }, indent=2)
    return "export default " + body + ";\n"


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: python3 sbk_to_js.py <sbk directory> <output directory>")
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    dst.mkdir(parents=True, exist_ok=True)
    books = sorted(src.glob("*.sbk")) + sorted(src.glob("*.SBK"))
    names = []
    for path in books:
        objs = objects(path.read_bytes())
        stem = path.stem.lower()
        out = dst / f"{stem}.js"
        out.write_text(module(path, objs), encoding="utf-8")
        names.append((stem, len(objs), path.stat().st_size))
        print(f"{out.name} objects {len(objs)} bytes {out.stat().st_size}")
    index = ["export { default as %s } from \"./%s.js\";" % (stem, stem) for stem, _, _ in names]
    (dst / "index.js").write_text("\n".join(index) + "\n", encoding="utf-8")
    print(f"index {len(names)} modules")


if __name__ == "__main__":
    main()
