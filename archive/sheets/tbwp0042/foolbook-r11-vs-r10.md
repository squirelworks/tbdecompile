# Foolbook r11 vs r10 (ToolBook comparison)
Written 2026-10-25 (Asia/Tokyo). No repo write, nothing pushed, no Bochs action. Same method as the r10 report (headless harness at Tk canvas scale 1.0: `tools/meas.py`, `all/check4.py`, `all/newchecks.py`, `all/menu10.py`, batch of 131 pages). New this time: items marked **RV** were also measured in the real viewer (`viewer/native.py` under Xvfb, canvas 648x466 = scale 1.0, or 800x600 = 0.987); see `foolbook-real-viewer-text-size.md`. **The harness and the real viewer disagree on P1040 and P2170 (section 3).** Results: `/workspace/foolbook_out_new/` (r11), `/workspace/foolbook_out_r10/` (moved).

## 1. What is new
- `/workspace/foolbook_new` fast-forwarded to **59530ea** (tag v1.0.7r11, 2026-10-25 04:42 JST). One commit since r10 (72be9b2): **59530ea "Measure a coloured word as one string."** 3 files, +12/-2 (`engine/graphics.py` +6, CHANGELOG, pyproject). Changelog: a coloured letter is measured with the rest of its word so it no longer sits on the next letter; the P2170 rows use the 10-point run, including the first letter of the header.
- **openscript-analysis pin: v1.0.1r3 -> v1.0.1r4** (installed 1.0.1.post4). Foolbook 1.0.7.post11 in `/workspace/foolbook_venv_new`.
- The pin change moved font sizes on several pages that have a stored 10 pt / 18 pt run (P1, P0, P10, P2050, P2170-P2242, P10301-P10303, P10410): 15 of 131 pages differ from r10 in pixels.

## 2. Compact table
| check | ToolBook | r10 | r11 | matches? |
|---|---|---|---|---|
| (b) OK with no choice | next question | stays (P10214, index 1) | **stays** (P10217, index 1) | **no** |
| (h) review (A) then OK, 50% | P10410 | P10214 | **P10213** | **no** |
| (h) same at 70% | P10410 | P10211 | **P10213** | **no** |
| P10020 Directions | text shown | 0 objects drawn | **0 objects drawn** (stored text exists) | **no** |
| P10020 bottom-left / bottom-right strips | return to P10004 | stay P10020 | **stay P10020** | **no** |
| P900 labels: fresh / leave P1910 / leave P2910 / quiz 50, 60% fail / 70, 100% pass / Lesson Exit | black / "1" grey / "2" grey / "3" black / "3" grey / Exit black | as the script says | **same, unchanged**: flags [1..] then 2 as before; colour #bf80ff; Exit black in every state; new session resets. Real viewer (page list drive): fresh black, after P1910 "1" #bf80ff, after P2910 "1","2" #bf80ff | yes |
| P2210 lines 1 / 2 / 3 | 425 / 462 / 428 | 425 / 492 / 395 | **425 / 492 / 395** (harness and **RV**) | **no** |
| P2170 header | one line | one line, y247..261 (first letter larger) | harness **one line x186..428, y250..261, h12** | yes |
| P2170 rows (panel x160..457, y222..372; four aligned rows, pitch ~19, ".00001" not wrapped) | 4 rows y ~290 / 308 / 327 / 347 | 5 lines, ".00001" on its own line (y342) | harness: **4 rows y288 / 307 / 326 / 345, pitch 19, ".00001" on the CMOS row (x185..396), last row ends y353 inside the panel** (x162..462, y222..374); glyph rows h9. **RV** (scale 1.0): header y250, rows y289 / 308 / 327 / 347, clean | **yes** (r10 no) |
| P2170 glyph look | clean | first letters larger/overlapping | harness: heavy/doubled "TTL", "10", "10" in the first row; **RV: clean** | RV yes, harness no |
| P1040 line 1 / 2 (harness, canvas 1.0) | x65..547 y84 w483 ("...family") / x66..227 y103 w162 | w441 y85 / w213 | **w432 y85 / w213 (unchanged line 2; line 1 shorter again)**, "family" on line 2, yellow letters overprint ("Transistor-TTransistor", "(TTL)") | **no** (harness) |
| P1040 **RV** at scale 1.0 / 0.987 / 1.50 | same as above | n/a | **1.0: w502 / 140 ("family of" on line 1); 0.987: w482 / 164 ("family" on line 1, no overprint); 1.50: 490 / 166** | 0.987 and 1.50 yes, 1.0 no (one word late) |
| P1 Copyright (ToolBook x64..575, 7 lines, pitch 16, widths 223/489/512/477/490/491/69) | | x65..612, 7 lines, pitch 16, h12, widths 261/548/502/538/517/497/331 | **x65..591, 7 lines, pitch 16, h10, widths 222 / 468 / 489 / 454 / 466 / 527 / 9** (RV the same: 222 / 468 / 489 / 454 / 466 / 533 / 3) | partly: line 1 now 222 vs 223, lines 2-5 about 21-24 px narrow, line 6 +36, last line 9 vs 69 (wraps differ) |
| TRY AGAIN tab (P1312) | fully visible x214..407, y24..49 | yellow (243,249,70) x217..405, y27..39 visible | **pixel-identical to r10** | **no** |
| Click checks | all pass | 26 of 26 | **26 of 26**; real viewer empty clicks 5/5; Lesson Exit one dialog, No stays P900, Yes closes | yes |
| P400 / P450 / P300 / P1310 / P10210 pages | | | **pixel-identical to r10** | no regression |
| P400 line 1 / pitch / P450 / P1 Title / P300 | 481 / 19 / 325 / 169 / 243 | 482 (y85, 104) / 327 / 169 / 386 | **same numbers** | no regression |
| P900 labels 1 / 2 / 3 / Exit | 189 / 202 / 91 / 98 | 189 / 202 / 92 / 99 | **189 / 202 / 92 / 99** | no regression |
| Final Quiz answers (ref 28.9 / 38.3 / 36.9 / 37.6) | | 28 / 37 / 36 / 37, stem 289 | **28 / 37 / 36 / 37, stem 289**; RV at 1366x768 28.6 / 37.9 / 36.6 / 37.3 | yes |
| Long-text pages (P1290 / P1300 / P1302 / P2170 msg) | 397 / 259; 487 / 204; 481 / 291 | 397 / 258; 486 / 206; 481 / 290 | **same as r10** (not in the diff) | no regression |
| Plain-text body pages P1070 / P1170 / P1210 | 447 / 490+181 / 465+359 | 447 / 490+182 / 463+360 | **same as r10**; RV 447 / 490+182 | no regression |
| Fields on Tk default font | 0 | 0 of 677 | **0 of 677** (677 sized) | yes |
| Quiz drive / (a) B then OK at 50% and 70% | ok / P10410 | ok / P10410 | ok / **P10410 at both** | yes |
| Batch of 131 pages | - | 131 ok, 0 crash, 2998 objects, 0 bitmap failures | **131 ok, 0 crash, 2998 objects, 0 bitmap failures**; 15 pages differ in pixels | see below |

## 3. New and changed pages (anything worse)
1. **Quiz result pages P10301 / P10302 / P10303 are bigger and now overflow.** r10: stem 15 px glyph rows, one line x63..515 (w453). r11: glyph rows 23, one line x63..611 (w549, P10301 w514 past x619). ToolBook's P10303 shows the same large type (shot `r_q10ok.png`: line 1 "The test is complete and your score is 100%." about x63..568, line 2 "Do you want to _________"), so the **size is now closer**, but the text is **not wrapped onto two lines** and runs to the page edge. The batch now flags P10301-P10303 as text past the page edge (it flagged P0 and P1 in r10; those two are no longer flagged). The answers are drawn larger too (P10301 "answer the skipped questions?" 236 -> 332 wide, "end the test?" 125 -> 165; P10303 "review the test?" 141 -> 189, "exit?" 74 -> 89).
2. **P1 Copyright text is smaller (h10 vs 12)**: it now fits the page (x65..591, was ..612) and line 1 matches (222 vs 223), but later lines wrap differently from ToolBook. Mixed: nearer in size, further in wraps.
3. **P1040 in the harness is not fixed** (432 / 213, overprint). In the real viewer it is right at scale 0.987 and 1.50 and one word late at exactly 1.0 (502 / 140).
4. **Harness vs real viewer**: the harness is Tk at its default scaling 1.388 and canvas 648x466. The real viewer under Xvfb with Tk scaling set to 1.0, 1.333 or 2.0 draws P1040 and P2170 cleanly, at **1.667** P1040 overprints. So numbers for the coloured-run pages (P1040, P2170) depend on Tk scaling; they are not stable across environments.
5. **Changed pages not compared with ToolBook**: P10 (line 1 235 -> 200 wide, y85..100), P2050 (text now split, y291..311), P10410 (bbox x199..406, y125..223), P0 (as P1).

## 4. Still wrong, same as r10
(b) OK with no choice; (h) review then OK (now P10213); P10020 blank and strips dead; P2210 wrap (492 / 395 vs 462 / 428); TRY AGAIN tab; P1 Copyright widths; P1040 in the harness.

## 5. Not verified
- Real-viewer P2210 / P1312 were measured at scale 1.0 only (P2210 425 / 492 / 395 as the harness). P1312 tab in the real viewer: ink h26 at y17..43 (ToolBook y24..49); not compared further.
- Quiz drive and the quiz-pass menu colour were done in the harness (mirrors `native.on_canvas`), not in the real viewer.
- Windows Tk and real display DPI were not tested.
