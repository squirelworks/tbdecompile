# System book triage (2026-10-14)

> Superseded, 2026-10-16. Chapter 15. The 'no OpenScript in any sbk' line is superseded for tb80r.sbk only. Read `TBdecompile/record/` for the claim. This sheet is the trail.

Fifteen .sbk files. Ranked by value for NIDA courseware playback.

## Ranking

### Tier 1 — Core for NIDA

| File | Size | Notes |
|------|------|-------|
| `tb80r.sbk` | 954 KB | Reader log book. Already processed (66 objects). Lessons reference it. Contains sysBooks, AICC strings. |
| `INST80.SBK` | 70 KB | Installer system book. Referenced by Inst80.exe. Contains tb80r. Small. |
| `tb80.sbk` | 3.1 MB | Large core system book. Type table present. Likely the main runtime library. |
| `tb80a.sbk` | 2.4 MB | Author-side companion. Large. |
| `tb80i.sbk` | 619 KB | Instructor system book. |

### Tier 2 — Specialized but relevant

| File | Size | Notes |
|------|------|-------|
| `tb80anm.sbk` | 64 KB | Animation. Already processed to JS. |
| `tb80hyp.sbk` | 141 KB | Hypertext. Already processed. Contains initialize, AICC. |
| `tb80aicc.sbk` | 86 KB | AICC compliance. Training standard. Contains initialize, AICC, tb80r. |
| `tb80actr.sbk` | 208 KB | ActiveX runtime. Contains initialize, ActiveX. |
| `tb80acta.sbk` | 2.1 MB | ActiveX author. Large. |
| `tb80axf.sbk` | 618 KB | ActiveX related. JBO at 0xE00. |

### Tier 3 — Lower priority for NIDA

| File | Size | Notes |
|------|------|-------|
| `tb80web.sbk` | 1.1 MB | Web support. Not required for local NIDA playback. |
| `tb80ftp.sbk` | 243 KB | FTP. Not required. |
| `tb80x.sbk` | 256 KB | Unknown specialty. |
| `tb80lmx.sbk` | 62 KB | Small. Contains initialize, AICC. Possibly license or metrics. |

## Structure notes

- All contain the object type table (Polygon, Button, Field, Page, Book, Picture, Curve).
- Most are resource containers (type tables, menus). Few have live page objects in the first 128 KB.
- JBO at 0xC00 for most; 0xE00 for tb80axf, tb80lmx, tb80ftp.
- Prior work confirmed system .sbk files do not contain OpenScript handlers. Logic is in nc81int.dll / nc81rec.dll for Nida books.

## Recommended processing

1. Confirm `tb80.sbk` and `tb80i.sbk` are the main runtime system books. Extract type table and menu resources if not already done.
2. Process `tb80aicc.sbk` — AICC is a training standard; NIDA may use it for session tracking.
3. Note `tb80actr.sbk` for ActiveX runtime support. Park deep dive until NIDA playback is solid.
4. Park web/FTP and large author books. They are not on the NIDA playback path.
5. INST80.SBK is small; extract its type table and any sysbook references for the installer load path.

## Cross-reference

Already processed to JS: tb80anm, tb80hyp, tb80r, plus the Nida books (nc81base/recs/test/trnr). See `artifacts/sbk/`.
