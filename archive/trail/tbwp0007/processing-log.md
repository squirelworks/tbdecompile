# Processing log (2026-10-14)

> Trail, 2026-10-16. Chapter 18. A log, not a separate finding. If this sheet and `TBdecompile/record/` disagree, the record wins.

Tier 1 items processed. Exhausted items marked.

## Exhausted (no further value for NIDA)

| Item | Reason |
|------|--------|
| `blank.tbk` | 1 page, 0 handlers. Minimal baseline confirmed. |
| `default.tbk` | 1 page, 10 handlers (standard widget lifecycle: make, sized, mouseEnter/Leave, ASYM_Reset). Generic shell. |
| `tbkcache.ini` | Template index only. Descriptions already noted. |
| `tb80anm.sbk` / `tb80hyp.sbk` | Already processed to JS in prior work. |
| `tb80r.sbk` | Already processed (66 objects). |
| HTML variants (`*h.tbk`, `*i.tbk`) | Export shells. Not native format insight. |
| `TBKSLICE.DLL` / `TBKMMWID.FON` | Supporting files. Not core. |

## Processed (useful data extracted)

### Templates

| File | Pages (marker) | Handlers loaded | Notes |
|------|----------------|-----------------|-------|
| `quiz1.tbk` | 15 | 20 | Quiz exit via `ASYM_ACIEndLesson`. Standard widget handlers. |
| `learn1.tbk` | 19 | 73 | Training template. Includes clip/media handlers (`playClip`, `mmnotify`). Some decode noise. |
| `train1.tbk` | 10 | 31 | Basic training. Standard widget + menu handlers. |
| `activeX.tbk` | 10 | 32 | ActiveX example. Handlers: `linkDLLs`, `sysBookChk`, `runtimeChk`, `enterBook`. |
| `Quizbldr.tbk` | 21 | 285 | Quiz Builder. ADO/question bank handlers (`ADO_QBank_*`). Authoring tool. |

Handler patterns are standard ToolBook widget lifecycle (make, sized, mouseEnter/Leave, ASYM_Reset, ASYM_Trigger). No new object subtypes observed.

### System books

| File | Status |
|------|--------|
| `tb80.sbk` | Confirmed main runtime. Type table present (ComboBox, Button, Field, RecordField, Hotword, Rectangle, Polygon, Line, etc.). Resource container. |
| `tb80i.sbk` | Confirmed Instructor companion. |
| `tb80aicc.sbk` | AICC properties and functions extracted. No handlers. |

## Parked (not exhausted, but not on NIDA path)

| Item | Reason |
|------|--------|
| `tb80web.sbk` / `tb80ftp.sbk` | Web/FTP. Not required for local playback. |
| `tb80a.sbk` / `tb80acta.sbk` | Author-side. Large. |
| `tb80x.sbk` / `tb80lmx.sbk` | Specialty. |
| Catalog cache books | Authoring object catalog. |
| Sales/HR/ROI templates | Content examples. |
| `Walkthrough.tbk` / `scrwalk.tbk` / `chewbyte.tbk` | Large or unknown. Inspect only if needed. |

## Remaining open

- Bounds extractor still missing.
- Content rectangles and some curves not fully decoded.
- AICC logic is in the DLLs (nc81rec.dll or companion), not in the SBK.
- Quiz Builder ADO handlers are authoring-only. Not needed for NIDA playback.
