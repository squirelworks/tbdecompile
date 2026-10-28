# Foolbook 1.0.7r17 against r15 and ToolBook
Written 2026-10-25 (Asia/Tokyo). Read-only on every repo. Fresh clone under `/workspace/repro/src_r17_git` (tag `v1.0.7r17` = b56fea9), new venvs `/workspace/repro/venv313_r17` (Python 3.13.5, Tk 8.6.16 + Liberation Sans) and `venv314_r17` (Python 3.14, Tk 9.0.4, no Xft), with the pinned `openscript-analysis` **v1.0.1r5** (installed 1.0.1.post5; r15 pinned r4). Real viewer under Xvfb, same harness as the r15 check (`/workspace/repro/rvp.py`, `rvp_nida.py`, `rvclick.py`, `run2.sh`, `cmp_pages.py`, `cmp_items.py`). Nothing written into any repo; opentoolbook8, Graal and Seihai untouched.
ToolBook shots from `/workspace/bochs/shots` were copied to `/workspace/repro/tbcopy/` before reading. Colour from the Bochs guest is not evidence and is ignored.

## 1. What r17 changed (git log v1.0.7r15..v1.0.7r17: 2 commits)
- **r16 (53adf5c):** a quiz letter is not coloured in before it is chosen; OK/Next/Skip/Back leave a question opened from the page list; "the nida81 equipment picture is drawn, P310 is the computer".
- **r17 (b56fea9):** a coloured letter is drawn once, at the width of the letters before it (no more yellow letter printed over its neighbour); a word fitted to its field keeps the fitted size (`_typeface`: the caller's size wins, the recorded size is only the fallback); the pale field behind a chip stays behind the pins and the number (`place.in_front`, `covers_drawing`); P10 greets the student ("Student" default); the end of a test shows the score instead of XX (Reader level; Author level still XX).
- **Dependency:** openscript-analysis pin r4 -> r5. The class 0x19 picture decode is there (`formats/tbk/store.py`, "metafile in a class 0x19 picture, as a BMP").
- Repo tests: `pytest` 57 passed (includes `engine/test_click.py`).

## 2. Verdict table (previously reported problems)
| # | Problem (r15) | r17 verdict | Evidence |
|---|---|---|---|
| 1 | P400 "Output" splits "Outpu/t" at 683x540 and about 1896x1000 | **fixed** | "Output" is one line (wrap 0, size shrunk to 13/32 px) in all 4 runs: 683 and 1896x1000, normal Tk and user-Tk emulation. Also fine on Tk 9.0.4. Image `page-compare-r17/r17_P400_sizes.png` (top row r15, bottom row r17). |
| 2 | INTRODUCTION / Digital Circuit / Input wraps under the user's-Tk emulation (points @ 1.45 scaling) | **still fixed** (no regression) | INTRODUCTION 1 line, "Digital / Circuit" 2 lines, Input 1 line at 683x540 and 1896x1000, with and without the emulation. Same image. |
| 3a | P1040 letters overprint | **fixed** | Each coloured letter is its own item at the prefix width; no overprint. `zoom_P1040_letters.png`, `r17_P1040_sizes.png`. Same fix on P1085, P1205, P1256, P2060, P2232 (`ab_*.png`). |
| 3b | P1040 wrap does not match ToolBook | **still wrong** | ToolBook (v_p1040.png, P1040) breaks after "family"; r17 at 1:1 puts "family" at the start of line 2; at 683 and 1896 (normal) line 1 ends "family of". Only the 683 user-Tk case ends line 1 at "family" (by luck). Same wraps as r15 in all five runs. `zoom_P1040_text.png`. |
| 3c | (new side effect) spacing around coloured letters | **new** | See section 5. |
| 4a | P2170 header "POWER (mw)" drops to a second line (683x540, user-Tk emulation) | **still wrong** | Header item still ends "...POWER" in `r17_pxpt_683` (same as r15); fine in the other four runs. |
| 4b | P2170 patterned frame | **still wrong** | Flat blue panel; ToolBook has a dotted frame. `05_P2170_P2210.png`. |
| 4c | P2170 dark row bands behind TTL/IIL/CMOS/ECL | **still wrong** | Not drawn. Row text still within 6 to 9 px of ToolBook (x) and about +6 px lower. |
| 5 | P1290/P1300 answer frames with chip drawings | **fixed (drawing)** | The three frames now show the chip body, pins and notch with the label on it (ToolBook s_p1290.png, clock 12:30 PM; s_p1300.png 12:31 PM). `04_P1290_P1300.png`. Left over: the frame is a flat colour, not dotted (colour/texture, not evidence); on P1290 the "08" of "7408" is drawn in a different colour from "74" while ToolBook shows all of 7408 in white (see 5). |
| 6 | P410/P420/P1070 stray clipped header text | **still wrong** | "INTRODUCTION"/"DISCUSSION" still half visible above the panel. `02_P410_P420.png`, `03_P430_P1070.png`. |
| 7 | P410/P420 extra chip labels | **still wrong** | "MM54240" (P410, P420) and the "TMS 2732A JL-45" chip with square window (P410 bottom) still drawn; ToolBook (d1.png 12:42 PM, m5.png 12:42 PM) is blank on those chips. |
| 8 | P430 connector arrowheads | **still wrong** | Lines drawn without arrowheads (ToolBook s0.png 12:59 PM shows them). |
| 9a | P10303 no line wrap | **still wrong** | Line 1 still runs off the right edge ("...score is 0%.  Do yo"), no second line, no "________" blank. P10302 has the same (cut at "Do you want to ___"). `06_P10303_P10410.png`. |
| 9b | P10303 score reads "XX%" | **fixed** | Reads "0%" at Reader level. ToolBook's shot (o_q10ok.png, 12:00 PM) says 50%, which is a different test state, not a fault. |
| 10 | P10 no student name | **changed** | Name appears ("Hello Student, this lesson ..."), but the last run is broken: "i  s about:" has a gap and "s about:" is drawn at **size 14 instead of 12** (items `Hello Student, this lesson i` + `s about:`). New defect, `zoom_P10_hello.png`, `01_P10_P300.png` (ToolBook e1.png, 1:18 PM). |
| 11 | P2210 "IC DATA BOOK" label too low | **still wrong** | Ink rows 302 to 313 in Foolbook against 293 to 304 in ToolBook (v_p2210.png): **+9 px** (r15 said 8 to 10). Items identical to r15. |
| 12 | Bullets oval vs square | **still wrong** | nida81 P310 still draws 5 oval bullets; ToolBook has small squares. |
| 13 | Heading text 3 to 4 px low | **still wrong (unchanged)** | White heading ink ends 3 px lower on P900 and P1001 (P900 40 vs 43, P1001 38 vs 41); the corner label is 3 to 4 px lower on every page. Item positions identical to r15. |

**Counts (17 verdict lines above):** fixed 5 (rows 1, 2, 3a, 5, 9b; row 2 means "stays fixed"), changed 1 (row 10), still wrong 11 (3b, 4a, 4b, 4c, 6, 7, 8, 9a, 11, 12, 13). New problems: 5 (section 5).

## 3. nida81
- **P300 click -> P310 "IBM PC Compatible Computer": the picture is drawn.** With `nida81.tbk` beside the book the click lands on P310 with 29 items (4 images, 14 text, 10 oval, 1 rectangle); list goes from 131 to 44 pages. Images: `nida_P310.png` (ToolBook t4.png, P310, guest clock 1:15 PM, left; Foolbook r17 right), `r17-P300-click-nida81tbk-beside.png`.
- **Not a pixel match.** (a) The picture sits on an opaque **white rectangle** (ToolBook shows it on the page background), so the page looks like a photo pasted on a white box. (b) The white "Minimum Requirements" text partly lands on that white box, so the left part of the heading and bullets is hard to read (the r15 problem is reduced, not gone). (c) Bullets are ovals, ToolBook squares. Position and size of the computer match ToolBook.
- **P20001 (HELP, y_bk.png, 12:52 PM):** computer drawn, same white box. `nida_P20001.png`. Help panel, text and Lesson Menu inset match as in r15.
- **P10020 (q_dir.png):** still matches (`nida_P10020.png`).
- **The other class 0x19 pages (26 in total):** the contact sheet `nida_class19_pages_r17.png` shows 25 of 26 now draw a picture (P310 to P395, P20000, P20001, P22045 to P22120). **Decode faults:** the pictures on P320, P330, P335, P357, P360, P376, P380 and P390 (and probably more) are torn: a horizontal band is missing or shifted, with white gaps (`nida_picture_defects_r17.png`, `nida_picture_defects2_r17.png`). **P22130 still draws a plain white box** (no picture). P20000 draws two overlapping panels (no ToolBook shot, not judged). Only P310 and P20001 have ToolBook shots, so the torn pictures are judged by look, not by comparison.
- **Is nida81.tbk needed beside the book? Yes, still.** In an isolated folder with only 9E954D01.TBK (`/tmp/iso_a`), the P300 click lands on a **completely white page** (0 items, page list 43): the stub `core/nida81.fsk` (2.3 KB, unchanged since r15) holds no pictures. Image `r17-P300-click-stub-only.png`. Note: an earlier-style "stub only" folder that has sibling directories can still find a nida81.tbk in a child folder (`find_book` scans up to 40 child directories), so isolate the folder when testing this.

## 4. Full comparison and regression run
- **131-page batch (9e954d01, 808x466, page at 1.0):** 131/131 pages rendered, no exception in the logs, total canvas items 5985 (r15) -> 5989 (r17). Pixel diff against r15: **72 pages identical, 59 changed** (threshold 60 on the channel sum). Biggest: P1290/P1291/P1300/P1301 (chip frames, 41k px each), then four info pages (P30000, P30010, PINFO, PQINFO, 8.6 to 8.9k px), P2130/P2150, P1256, P1205, P1040, P2060, P1085, P2075, the colour-run pages (P1230 to P1256, P2180 to P2242), P10, P10303.
- **nida81 (44 pages):** all rendered, no exception; 36 pages changed (25 because the pictures now draw, the rest by the coloured-letter fix); 8 identical.
- **Sizes:** P400, P410, P420, P430, P450, P1040, P2170 at 683x540 and 1896x1000, normal Tk and user-Tk emulation (`PXASPT`, scaling 1.45); Tk 9.0.4 at 1896x1000 for P400, P1040, P2170, P10 (no crash, "Output"/"Input" one line).
- **Click checks:** P300 click run twice (nida81.tbk beside, stub only) as above; the repository's `test_click.py` is in the 57 passing tests.
- **Page-by-page against ToolBook, 27 pages of 9e954d01 + 3 nida81 pages** (`page-compare-r17/*.png`, all three-panel composites in `page-compare-r17/full_composites_r17/`, text-box table in `/workspace/repro/cmp17/items.txt`): P400, P420 (body), P430, P440, P450, P1001, P1170, P1210, P1290 (question), P1300, P1302, P1304, P1310, P1311, P1312, P2001, P2170 (body), P2210 (body), P10004, P10020 keep the ToolBook line breaks. The text-box flag count rose from 125 to 137 only because coloured runs are now several items instead of one (P1070, P1210, P1302, P1304, P1040, P1290); the positions of those pieces are within about 5 px of ToolBook's (for example P1290 "74" and "08", P1302 "74 L 00"). I did not treat that as a regression. Not compared (no usable shot): P0, quiz question pages P10210 to P10229, the other 23 nida81 pages with the picture type.
- **Matches but not pixel-identical:** text x positions within about 1 to 6 px of ToolBook, first body lines 1 to 2 px, row labels about +6 px low (P10, P2170, P1290 chip labels, P1040 chip numbers 5400/7400).

## 5. New differences found in r17
1. **Gaps before coloured letters.** The new per-colour drawing leaves about one extra space of gap before a coloured piece in running text: P1040 "Transistor- Transistor  Logic ( TTL)", P2150 "or  Integrated  Injection  Logic" (e.g. ' family or ' ends at x 192, the next piece "I" starts at x 197), P1256 "are  Super", P2060 "Complementary  MOS (CMOS)". This is cosmetic, but visible. It also lengthens P1040 line 1 to x 507 (r15: 498). Images `zoom_P1040_letters.png`, `ab_P30010_P2150.png`, `ab_P1256_P2060.png`.
2. **P10 "s about:" drawn at size 14 with a gap** (verdict row 10).
3. **Hidden info pages P30000, P30010, PINFO, PQINFO changed:** the version line now reads "Version: __nidaVersion" (r15: "Version: 2.003.0001"), "Question Correlation" is drawn twice on top of itself, a "??" box and a second outline appear. No ToolBook shot, so this is a change, not a judged fault (`ab_P30010_P2150.png`).
4. **P1910, P1999, P2910, P2999:** a small white box with a pink arrow (an icon) now appears at the top left of the panel (page 24,25); r15 did not draw it. No ToolBook shot (`ab_P1085_P1910.png`).
5. **P1290 "08"** (in colour a different run from "74") and the label y offset is +6 px; present in r15 under the old covering box, now visible.

## 6. Bottom line
r17 fixes what it says: "Output" split (P400), the coloured-letter overprint, the answer-frame chip drawings (P1290/P1300), the XX in the score, the student name (with a size glitch), and the nida81 pictures (25 of 26 pages draw, 8 or more are torn, P22130 is blank, and the picture is on a white box). Still open: P1040 wrap, P2170 frame/bands and the user-Tk header wrap, stray clipped headers (P410, P420, P1070), extra chip labels (P410, P420), P430 arrowheads, P10303 wrap, P2210 +9 px, bullets, heading +3 px, the stub .fsk landing on a white page. New: spacing gaps around coloured letters, the P10 "s about:" size, the four info pages and the P1910 family icon.

## Files
- Report: `/workspace/reports/foolbook-r17-vs-r15.md`
- Images: `/workspace/reports/page-compare-r17/` (01 to 09 side-by-side composites, `nida_*.png`, `r17_P400/P1040/P2170_sizes.png`, `zoom_*.png`, `ab_*.png` r15|r17, click shots, `full_composites_r17/`)
- Data: `/workspace/repro/out/r17_*.json` and `r17_*/` (png per page), `/workspace/repro/out/r17_vs_r15_pixdiff.json`, `/workspace/repro/cmp17/`
