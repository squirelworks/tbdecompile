# Foolbook r10 vs r8 (ToolBook comparison)
Written 2026-10-25 (Asia/Tokyo). No repo write, nothing pushed, no Bochs action. Numbers are page pixels at scale 1.0 (ink boxes, `tools/meas.py`, `tools/cmp10.py`). Results: `/workspace/foolbook_out_new/` (r10), `/workspace/foolbook_out_r8/` (r8, moved, not copied). Menu drive log: `foolbook_out_new/menu10.log`, `real_menu.log`.

## 1. What is new
- `/workspace/foolbook_new` fast-forwarded to **72be9b24f650da12d00bfcd5b9db7fab8c5e7401** (tag v1.0.7r10, 2026-10-25 04:13 JST). Two commits since r8 (32a87f2), 10 files, +248/-45:
  - **eaa3a1c** (tag v1.0.7r9, 03:48 JST) "Keep the highlighted letters on the same line." Changelog: the yellow letters on P1040 are painted on the same word, so they no longer open a gap or push "family" down a line; the P2170 table uses its 10-point run instead of the field's 12.
  - **72be9b2** (tag v1.0.7r10, 04:13 JST) "Colour a menu label after its section is left." New `engine/menu.py`, `leave_page` hooks in `engine.goto` / `press` / `open_book` / `viewer/native.py`, quiz pass sets flag 10.
- Install: foolbook 1.0.7.post10 (editable, `/workspace/foolbook_venv_new`). openscript-analysis pin is **unchanged** (v1.0.1r3, installed 1.0.1.post3).
- Harness: `clicks.Session.show` now calls `leave_page` like `native.show`. New `all/menu10.py` and `tools/real_viewer_menu.py` for the P900 labels. No pytest on the box, so the repo tests were not run.

## 2. Compact table
| check | ToolBook | r8 | r10 | matches? |
|---|---|---|---|---|
| (b) OK with no choice | advances to next question | stays (P10213, index 1) | **stays** (P10214, index 1) | **no** |
| (h) "review the test?" (A) then OK, 50% | P10410 | P10212 | **P10214** (a question page, review pass) | **no** |
| (h) same at 70% | P10410 | P10212 | **P10211** | **no** |
| P10020 Directions text | shows paragraph | 0 objects drawn | **0 objects drawn** (stored text exists, not drawn) | **no** |
| P10020 bottom-left / bottom-right strip | return to P10004 | stay P10020 | **stay P10020** | **no** |
| P900 fresh, all four labels | black | black | black (#000000, 352/361 px) | yes |
| leave P1910 (Next or Back) | "1. TTL" greyed | not done | **"1. TTL" #bf80ff** (191,128,255); 2, Final Quiz, Exit black | yes (logic) |
| leave P2910 (Back) | "2. Other ICs" greyed | not done | **"2" #bf80ff** (with "1" kept); T, Exit black | yes |
| quiz 50% / 60% (fail) | "3. Final Quiz" stays black | black | **black**, flag 10 stays 1 | yes |
| quiz 70% / 100% (pass) | "3. Final Quiz" greyed | black | **#bf80ff**, flag 10 = 2 (1 and 2 unchanged) | yes |
| "Lesson Exit" | never changes | black | **black in every state** (also after a Lesson Exit click: dialog, stays P900) | yes |
| Flags per session | reset on a fresh runtime | n/a | new Session resets to black | yes |
| Real viewer (`viewer/native.py`, Xvfb) | - | n/a | fresh black; after P1910 -> P900 "1" #bf80ff; after P2910 "1","2" #bf80ff; T and Exit black | yes (quiz not driven in real viewer) |
| P1040 line 1 / 2 | x65..547 y84 w483 ("...family") / x66..227 y103 w162 | x64..504 w441, y85 / x64..275 w213, y104 | **x64..495 w432, y85 / x64..276 w213, y104** | **no**: "family" still on line 2, line 1 now 9 px shorter |
| P1040 yellow letters | cyan in 16-colour shot | yellow, extra gaps | yellow, but **overprint**: "Transistor-TTransistor", "(TTL)" and the L glyphs overlap | **worse** |
| P2210 line 1 / 2 / 3 | 425 / 462 / 428 ("you" on line 3) | 425 / 492 / 394 | **425 / 492 / 395** | **no** |
| P2170 header | FAMILY / SPEED (ns) / POWER (mw) on one line | wraps ("POWER (mw)" on line 2, y266..280) | **one line** x186..430, y247..261 (but the "F" and "TTL" first letters are drawn larger than the rest) | header yes, look no |
| P2170 rows | four aligned rows, pitch ~19, inside panel x160..457, y222..372 | 4 rows plus a wrapped ".00001" line | **5 lines, pitch 19**: TTL y285, IIL 304, CMOS 323, ".00001" 342 (its own line, left-aligned x186), ECL 361..371. Panel x162..462, y222..374 | **no** (".00001" still wraps; ECL ends y371, inside the panel) |
| P1 Copyright | x64..575, 7 lines, pitch 16, widths 223/489/512/477/490/491/69 | x65..612, 7 lines, pitch 16, 261/548/502/538/517/497/331 | **identical to r8** (same boxes; only blue-channel antialias differs) | lines and pitch yes, widths no |
| TRY AGAIN tab (P1312) | fully visible x214..407, y24..49 | yellow (243,249,70) x217..405, y27..39 visible | **pixel-identical to r8** | **no** |
| Click checks | all pass | 26 of 26 | **26 of 26** (25 plus "Yes leaves") | yes |
| Real viewer empty clicks (P400, P300, P450, P900) | stay | stay | stay (5 of 5); Lesson Exit: one dialog, No stays P900, Yes closes | yes |
| P400 / P450 / P300 / P900 pages | - | see r8 report | **pixel-identical to r8** (no diff) | no regression |
| P1 Title / info / Copyright boxes | 169 / 188-108-142-177 / above | same | **same numbers** (page differs by antialias only, 14k px, max 40 in blue) | no regression |
| Final Quiz answers (ref 28.9 / 38.3 / 36.9 / 37.6) | 13 px bold | 28 / 37 / 36 / 37, h 9 | **28 / 37 / 36 / 37, h 9**; stem w 289 | yes |
| Long-text pages P1290 / P1300 / P1302 / P2170 msg | stem 397 / 259; msg 487 / 204; 481 / 291 | 397 / 258; 486 / 206; 481 / 290 | **397 / 258; 486 / 206; 481 / 290** (P1290-P1304 chip labels differ 1 px in width) | no regression |
| Body pages P1070 / P1170 / P1210 | w 447 / 490+181 / 465+359 | 447 / 490+182 / 463+360 | **same as r8** | no regression |
| Fields on Tk default font | 0 | 0 of 677 (677 sized, 664 bold) | **0 of 677 (677 sized, 664 bold)** | yes |
| Quiz drive | 10 questions, score, OK | ok | ok: 100% and 70%, 10 questions each; second Begin gives a new order | yes |
| (a) score under 100%: B then OK | P10410 | P10410 | P10410 at 50% and 70%; review buttons do nothing; Menu -> P900 | yes |
| Batch of 131 pages | - | 131 ok, 0 crash, 2998 objects, 0 bitmap failures | **131 ok, 0 crash, 2998 objects, 0 bitmap failures**. 29 pages differ in pixels from r8 | see below |

## 3. Batch
- 29 of 131 pages differ from r8. Line geometry changed on only one: **P1040**. P1 and P0 (Copyright, antialias only), P1210 / P1290 / P1300 / P1302 / P1304 (chip labels, 1 px), P2170-P2200 / P2232 / P2242 (table panel, see above) and about 15 pages with highlighted letters changed in pixel colour only (line boxes the same).
- Flagged "text past edge": same pages as r8 (P0, P1, P1290, P1300, PQINFO). The item count went 8 to **10** because the Copyright line is now listed twice on P0 and P1; the ink still stops at x 612.

## 4. Worse than r8, and still wrong
1. **P1040 is worse**: line 1 shrank 441 to 432 (ToolBook 483, ends with "family") and the highlighted letters now overprint their neighbours. "family" is still on line 2.
2. **P2170**: the header now fits on one line, but ".00001" still wraps to its own line, so the table has five lines where ToolBook has four rows; the header "F" and the "T" of "TTL" are drawn larger and overlap.
3. **Not fixed since r8**: (b) OK with no choice; (h) review then OK (50% -> P10214, 70% -> P10211, not P10410); P10020 empty and strips dead; P2210 wrap (w 492 / 395); TRY AGAIN tab; P1 Copyright widths (37 px wider).
4. **Fixed**: the P900 menu labels (flags 1, 2, 10, Exit never changes, session only).

## 5. Not verified
- The menu colour is #bf80ff (hue 270, sat 50, bright 100). The ToolBook shot is the 16-colour guest, light blue; a true-colour ToolBook was not seen.
- Quiz pass colouring was driven in the harness (mirrors `native.on_canvas`) only; in the real viewer I drove P1910 / P2910 through the page list. The flag also sets on Back (any leave), as in ToolBook's `leavepage`.
- The repo's own unit tests were not run (no pytest).
- Window-resize scaling was not exercised; all renders are at scale 1.0.
