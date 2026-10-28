# Foolbook 1.0.7r18 against r17 and ToolBook (major problems only)
Written 2026-10-25 (Asia/Tokyo). Read-only on every repo. Fresh clone `/workspace/repro/src_r18_git` (tag `v1.0.7r18` = 18801ec), new venv `/workspace/repro/venv313_r18` (Python 3.13.5, Tk 8.6.16, Liberation Sans) with the pinned `openscript-analysis` v1.0.1r5 (installed 1.0.1.post5, same pin as r17). Tk 9.0.4 run with `venv314_r17`'s Python on the r18 source. Real viewer under Xvfb, same harness as r17 (`rvp.py`, `rvp_nida.py`, `rvclick.py`, `cmp_pages18.py`, `cmp_items18.py`, `mont18.py`). Nothing written into any repo; opentoolbook8, Graal and Seihai untouched. ToolBook shots were copied from `/workspace/bochs/shots` before reading; Bochs colour is ignored.

Per the user's instruction this report lists major problems only (missing/blank/torn pictures or pages, mid-word or unreadable wrapping, wrong or missing content, wrong page reached, quiz flow, crashes, regressions). Few-px offsets, bullet shape, heading 3 px low, tiny gaps and hidden info pages are not listed.

## 1. What r18 changed (git log v1.0.7r17..v1.0.7r18: 1 commit, 6 files)
- **18801ec:** "Keep the greeting in one face, wrap the score, and drop the white mat around an equipment picture." Changelog: the P10 greeting keeps one face for the whole line; the score line wraps inside its field; a coloured letter is pulled back to the ink before it when the book stored no space there; white that touches the edge of an equipment picture is treated as the page showing through; an unknown book property no longer replaces the version line.
- Pin unchanged (`openscript-analysis` v1.0.1r5). Repo tests: **60 passed** (r17: 57; +3 in `engine/test_sysbook.py`).

## 2. Counts
- 131/131 pages of 9e954d01 and 44/44 nida81 pages render, **0 exceptions, 0 errors** (Tk 8.6 at 808x466; sizes 683x540 and 1896x1000 with normal Tk and user-Tk emulation; Tk 9.0.4 at 1896x1000, no crash). Canvas items 5989 (r17) -> 6001 (r18) in the main book.
- Pixel diff r18 against r17 (channel-sum threshold 60): main book 12 of 131 pages changed (P100, P10302, P10303, PQINFO, P30000, P30010, PINFO, P10, P10301, P2130, P1040, P1100); nida81 27 of 44 changed (the picture pages). `/workspace/repro/out/r18_vs_r17_pixdiff.json`.
- ToolBook comparison, 27 pages of 9e954d01 + 3 nida81 pages: the text-box table is identical to r17 except P10 (now one line, fixed) and P10303 (now wraps). Text-box flag count 124 in both. No regression on any compared page. Not compared (no usable shot): P0, quiz question pages P10210 to P10229, the other 23 nida81 picture pages.
- Click checks: P300 click with `nida81.tbk` beside the book -> **P310** (page list 131 -> 44, 29 items, 4 images); same with the second layout. Stub only (`/tmp/iso18`, a copy of the book alone): click lands on P310 with **0 items, a completely white page** (page list 43), as in r15 and r17.

## 3. Verdict table: major problems from the r17 report
| # | Problem (r17) | r18 | Major? | Evidence |
|---|---|---|---|---|
| 1 | nida81 picture on an opaque white box (P310, P20001, others) | **fixed** | was major | P310 now shows the computer on the page background, as ToolBook does; the white "Minimum Requirements" text is readable. P20001 the same. `page-compare-r18/nida_P310.png` (ToolBook t4.png, guest clock 1:15 PM, left; r17 middle; r18 right), `nida_P20001.png`, `r18-P300-click-nida81tbk-beside.png`. |
| 2 | Torn pictures P320, P330, P335, P357, P360, P376, P380, P390 | **still wrong** (not better, not worse) | **yes, major** | All eight still show a horizontal band missing or shifted with a white gap. The only visible change is that the white box behind them is gone, so the tear now shows against the grey page. P390: top band (the cable) is shifted left and cut. P376: top third of the BNC cable is offset from the rest. P320: white gap at the top centre. Images `nida_picture_defects_r17_vs_r18.png` (r17 | r18 per page), `nida_class19_pages_r18.png` (all 28 picture pages). Judged by look: only P310 and P20001 have a ToolBook shot. Decode fault, not a paint fault. |
| 3 | P22130 plain white box (no picture) | **still wrong** | **yes, major** (one page) | Still a white square with a "Power Cord" label, no picture. `nida_class19_pages_r18.png` (last tile). |
| 4 | P1040 wrap differs from ToolBook ("family" starts line 2) | **still wrong** | **no** | Two lines, readable, only one word moves ("family" on line 2; ToolBook ends line 1 with "family"). The r17 spacing gaps around the coloured letters are gone ("Transistor-Transistor Logic (TTL)" now reads normally). `cmp18/P1040.png`, `r18_P1040_sizes.png`. |
| 5 | P2170 header wrap "POWER (mw)" | **still wrong** | **no** | Only in the user-Tk emulation at 683x540 ("POWER" / "(mw)" on two lines). One line in the other 4 runs, including the user-Tk emulation at 1896x1000 (the user's maximized window). `r18_P2170_sizes.png`. |
| 6 | P2170 patterned frame and row bands missing | **still wrong** | **no** | Table text, rows and header are all present and readable on a flat panel; only the texture is missing. `cmp18/P2170.png`. |
| 7 | P410/P420/P1070 half-hidden header text above the panel | **still wrong** | **borderline, not major** | A ghost half-line of "INTRODUCTION" / "DISCUSSION" still shows above the grey panel on P410, P420, P1070 (ToolBook shows nothing). Readable pages, no content lost. If the user wants one cosmetic item fixed, this is the most visible one. `cmp18/P410.png`. |
| 8 | P410/P420 extra chip labels ("MM54240", "TMS 2732A") | **still wrong** | **no** | The chips themselves are drawn in ToolBook too; only the label and window are extra. |
| 9 | P430 connector arrowheads | **still wrong** | **no** | Lines present, small arrowheads missing. `cmp18/P430.png`. |
| 10 | P10303 / P10302 / P10301 score and prompt run off the right edge | **fixed (runs on)**, small wrap difference left | was major, now not | The line now wraps inside the field on all three end-of-test pages and the "________" blank shows. Left over: the wrap point is a word later than ToolBook ("...score is 0%.  Do" / "you want to ____" against ToolBook "...score is 50%." / "Do you want to ____"). Readable. `ab_P10302_P10301_P10303_P10.png`, `cmp18/P10303.png` (ToolBook o_q10ok.png, 12:00 PM, shows 50%, a different test state). |
| 11 | P10 "Hello Student, this lesson i  s about:" (gap and size 14) | **fixed** | was minor-major | One line, one face: "Hello Student, this lesson is about:". `cmp18/P10.png` (ToolBook e1.png, 1:18 PM). |

Totals for the 11 rows: fixed 3 (rows 1, 10, 11), still wrong 8 (2 to 9). Of the still-wrong ones **2 are major** (rows 2 and 3, both nida81 pictures), 1 is borderline (row 7), 5 are not major. Nothing got worse.

## 4. Other r17 items, checked for regressions (all unchanged, none major)
- P400 "Output", "Input", "INTRODUCTION", "Digital / Circuit": one line each, no mid-word splits, at 683x540 and 1896x1000, normal Tk, user-Tk emulation (points at 1.45), and Tk 9.0.4. Fixed in r17 and still fixed.
- P1290/P1300 answer-frame chip drawings: unchanged from r17 (still drawn).
- The four hidden info pages: the version line is back to "Version: 2.003.0001". No ToolBook shot, noted only because r17 had made it worse.
- P10303 reads "0%" (not XX), as in r17.

## 5. New problems in r18
No new major problem. Only this minor change: on P100 (and other bullet lists) the bullet is now its own item, drawn a size larger and a pixel lower than the text (`/workspace/repro/out/r18_all_1to1.json`, P100: bullets at size 16, text at 15). The picture of P100 is otherwise the same; I have no ToolBook shot of P100. Not major.

## 6. Still needed / not tested
- `nida81.tbk` must still sit beside the book, otherwise the P300 click lands on a completely white page (the stub `core/nida81.fsk` holds no pictures). This is unchanged since r15; counted here as a known limitation, not a regression.
- Not tested: Windows, a real display, the user's own Tk and fonts. The "user-Tk emulation" is a Linux Tk that reads Font sizes as points at scaling 1.45.
- I did not drive a full quiz run by hand. Quiz end pages P10301 to P10303 render and the repo's 60 tests (including `test_click.py` and `test_sysbook.py`) pass.

## Bottom line
r18 fixes the white box behind the nida81 pictures, the end-of-test line running off the edge, and the P10 greeting. The major problems still open are the torn picture decode on 8 nida81 pages (P320, P330, P335, P357, P360, P376, P380, P390) and the blank P22130. The rest of the r17 list is cosmetic.

## Files
- Report: `/workspace/reports/foolbook-r18-vs-r17.md`
- Images: `/workspace/reports/page-compare-r18/`: `nida_P310.png`, `nida_P20001.png`, `nida_P10020.png` (ToolBook | r17 | r18), `nida_picture_defects_r17_vs_r18.png` (the 8 torn pages + P22130, r17 | r18), `nida_class19_pages_r18.png` (all 28 picture pages), `r18-P300-click-nida81tbk-beside.png`, `r18-P300-click-stub-only.png`, `r18-P300-start.png`, `ab_P10302_P10301_P10303_P10.png` (r17 | r18), `r18_P400/P1040/P2170/P450_sizes.png` (top row r17, bottom row r18; 683 / 683 user-Tk / 1896 / 1896 user-Tk), `full_composites_r18/` (ToolBook | r18 | white-text overlay for the 27 compared pages)
- Data: `/workspace/repro/out/r18_*.json` and `r18_*/` (png per page), `/workspace/repro/out/r18_vs_r17_pixdiff.json`, `/workspace/repro/cmp18/`
