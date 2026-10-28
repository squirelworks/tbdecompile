# ToolBook vs Foolbook: overnight results (as of 2026-10-25 00:29 JST)

Book: C:\TBK\9e954d01.tbk (file 9E954D01.TBK). Nothing was written into any repository. Colour is closed (the Bochs guest is 16-colour planar VGA, so screenshot hues are not evidence). Pages count only where the screenshot file was quoted (title, corner label, guest clock), each copied to a new path and read by Frank.

Supersedes the older notes where they disagree: in `p-layout.md` the helper functions are listed as "not found". They are found, in `nc81base.sbk` (see `helper-scripts.md`).

## 1. Region reads at FUN_1020_16de (Fred, Bochs, from the GDI heap)
Correction: 43d0 is param_4 of 16de, not the region. The boxes below were read from the REGION object passed as param_2 (the FillRgn argument). Coordinates are in the DC's space (origin unknown). Five hits on P420 to P430 at Author level:

| hit | region handle | box (left,top)-(right,bottom) |
|---|---|---|
| 1 | 0fe4 | (24,24)-(604,182) |
| 2 | 0fd8 | (0,0)-(624,442) |
| 3 | 0fd8 | (0,2)-(86,23) |
| 4 | 0fd8 | (0,0)-(624,442) |
| 5 | 0fd8 | (24,24)-(604,182) |

Filed as boxes only. No erase rule is claimed. Hits 2 and 4 cover the whole page area (624x442). Hits 1 and 5 are a 580x158 box; I have not matched it to any object (the P400 body field record is 40,40 547x126, a different box). Fill ablation (skipping the fill, one hit or all five): 0 changed pixels versus normal P430. There was no positive control, so this is inconclusive and says nothing about the flame.

## 2. ToolBook Reader-level shots (all verified by Frank from the files)
| page | file | title | corner label | clock |
|---|---|---|---|---|
| P300 | shots/r300.png | Nida Corporation - Logic Families | P300 | 1:44 PM |
| P1 | shots/r1.png | same | not visible (page is LESSON INFO) | 1:48 PM |
| P450 | shots/r450.png | same | P450 | 1:52 PM |
| P900 | shots/r900.png | same | P900 | 12:54 PM |
(Earlier: shots/k5.png, P400, 12:07 PM.) Folder: /workspace/bochs/shots/.

## 3. Layout differences seen in those shots (colour ignored; details in `p-layout-toolbook-compare.md`)
- P450: ToolBook centres the sentence in the blue panel (x 66, y 102-116 in page px); Foolbook puts it at the bottom (x 46, y 141-159).
- P1: ToolBook's copyright block stays inside the page (x 64-575, 16 px line pitch, wraps near x 590); Foolbook starts it at about x 18, uses a 21 px pitch and runs off the right and bottom edges. Title line is about 1.7 times too large in Foolbook. Filename "93954d01.TBK" and Revision Date "01-16-02" read the same in both.
- P300, P900: boxes and bitmaps match within 1-2 px. ToolBook text is bold and starts about 5 px left of Foolbook's. The star in "* Lesson Exit" is a small dot in ToolBook and a full `*` in Foolbook (cause not found).
- P400 (earlier): ToolBook text left edge about x 66, line spacing 19-20 px, about 7.3 px per character, wraps after "one and"; Foolbook x 44, spacing 30, wraps after "thought of". The body field word set 360/360/310/border 5 is shared by 85 of 518 class 0x0A fields; not proved to be a margin (only P400 has a ToolBook measurement).

## 4. Click tests in ToolBook at Reader level (Fred; shots verified by Frank)
| page | click | ToolBook result | shot | Foolbook |
|---|---|---|---|---|
| P900 | empty page | page does NOT change (P900, 12:55 PM) | c3.png | moves to P1001: DIFFERENT |
| P900 | * Lesson Exit | modal "Are you sure you want to Exit the Lesson?" with Yes / No (12:56 PM); No leaves P900 (12:57 PM) | c5.png, c7.png | jumps to P1001: DIFFERENT |
| P450 | Menu | lands on P900 (1:00 PM) | m2.png | P900: same |
| P450 | Back | lands on P440 (1:02 PM) | m4.png | P440: same |
| P900 | 1. TTL Integrated Circuits | P1001, heading TTL INTEGRATED CIRCUITS (1:04 PM) | q1.png | same |
| P900 | 2. Other Integrated Circuits | P2001, heading OTHER INTEGRATED CIRCUITS (1:06 PM) | q3.png | same |
| P900 | 3. Final Quiz | P10004, heading FINAL QUIZ (1:08 PM) | q5.png | same |
| P400 | Next | P410 (1:12 PM) | t1.png | same |
| P410 | Back | P400 (1:13 PM) | t2.png | same |
| P400 | Back | P300, EQUIPMENT REQUIRED (1:14 PM) | t3.png | same |
| P300 | orange bar "1. IBM PC Compatible Computer" | opens nida81.tbk in the same window, title bar "ToolBook II - nida81.tbk", corner label P310, heading "IBM PC Compatible Computer", list 586 133 MHz / 12 MB RAM / 1 Gig Hard Drive / Mouse / Windows 98 (1:15 PM) | t4.png | nida81 P310: same |
| P1 | empty pink area right of the text | goes to P10, LESSON TITLE "Hello Student, this lesson is about: LOGIC FAMILIES" (1:18 PM; P1 has no readable corner label, named from content) | e1.png | P10: same |
| P300 | empty page area | no change (P300, 1:20 PM) | e3.png | moves to P400: DIFFERENT |
| P400 | empty page area | no change (P400, 1:22 PM) | e4.png | moves to P410: DIFFERENT |
| P450 | empty page area | no change (P450, 1:25 PM) | e5.png | moves to P440: DIFFERENT |

On P450 the Back and Menu buttons sit mostly under the Windows taskbar in the Bochs window (about 7 px visible); Fred clicked that strip.

## 5. Helper scripts (from `nc81base.sbk`, see `helper-scripts.md`)
- gotoMenuPage calls getMenuPage(): default P900; P10001 if lesson mode 0 and no assessment; P10002 if lesson mode 1 and no pretest; falls back to P900 if the page is missing. gotoQuizPage: P10004, or P10003 in lesson mode 1. Mode comes from NIDAREC.INI [Lesson] Lesson Mode, default 2 (the guest INI has no such key), so P900 and P10004 hold. Foolbook's hard-coded pages are right for the default.
- setSection only writes [NC71] Section to the monitor file. setupMenuPageLocal and clearPageList navigate nowhere. At mode 2 setupMenuPage disables or hides nothing on P900.
- keyF2 handler (book-level, 9E954D01 at 0xb3a8b): asks "Are you sure you want to Exit the Lesson?"; Yes runs EndExperiment() and closeSession(), then `send exit`. ToolBook's real behaviour matches this (section 4).
- Not found: how the runtime handles a missing field font or a bitmap larger than its record box (compiled code, not in any script).

## 6. State and still open
- Bochs is running (restored from state-reader-p310), Reader level, mouse capture on. Bochs is on P450 of 9e954d01.tbk, Reader level. Fred's next job: read the body field's font and margins in ToolBook's own properties dialogs at Author level on P400 (read-only, Cancel out).
- Parked: the buffer-copy function (the flame), the quiz and Author passes, the P0 chase.
- Open: font face and size, bold text rule, the P450 sentence position cause, the P1 title size, the small star, the 3 fields of the 518 vs 515 count.

## 7. ToolBook's own field properties (Fred, Author level, Properties for Text Field palette; shots verified by Frank)
Page units, 15 per pixel. Bounds are Left/Top/Width/Height. Indents are first line / other lines / from right. Tab spacing is 720 everywhere.

| page | field | layer, ID | bounds | font | indents | border, draw |
|---|---|---|---|---|---|---|
| P400 | Text (body) | 1 of 13, ID 9 | 600/600/8205/1890 | Arial Bold 12 | 360/360/310 | Inset, word wrap, custom colours (shots f3c to f6) |
| P450 | text (sentence) | 1 of 3, ID 2 | 600/600/8205/1890 | Arial Bold 12 | 360/360/310 | Inset, word wrap, locked |
| P1 | Filename | 4 of 11, ID 18 | 1950/1140/5265/285 | Arial Bold 12 | 0/0/0 | None, transparent |
| P1 | Title | 8 of 11, ID 22 | 1950/1440/5775/585 | Arial Bold 12 | 0/650/0 | None, transparent |
| P1 | Copyright | 2 of 11, ID 9 | 248/4500/9390/1800 | Arial Bold 10 | 720/720/720 | None, transparent |
| P900 | "Selection 1" | a GROUP, 5 of 8, ID 20 | 2536/975/4320/600 | style Bold, size blank | 0/0/0 | group; the member field was not reached |
| P300 | "Selection1" | a GROUP, 3 of 5, ID 18 | 1762/1170/5925/570 | style Bold, size blank | 0/0/0 | group; the member field was not reached |

Mapping confirmed by P1 Title (first 0, other lines 650): the record word +0x28 is the first-line indent, +0x2A is other lines, +0x2C is from right, +0x2E is tab spacing. Font is the entry pointed to by record word +0x22 (see field-font-and-indents.md). The P1 Copyright result (Arial Bold 10) matches the file-side reading that a text run overrides the base font on that field. P1 Title's box (1950/1440/5775/585) is "also covers the empty line under it" per Fred.

## 8. Final Quiz full run in ToolBook (Fred, restored 01:51 JST, ended 02:07 JST; guest clock about 12:00 PM at the end)
Checked by Frank against shots o_q10ok.png and o_p10303_ok.png (copied to new paths before reading).
- 10 questions, Reader level. A choice click only turns the letter button light cyan. OK (bottom strip) advances. No feedback banner, dialog or page after any OK. Q6 had no choice chosen (missed click) and OK still advanced.
- Answers: Q1 b, Q2 c, Q3 d (wrong on purpose), Q4 a, Q5 a, Q6 none, Q7 a (wrong on purpose), Q8 d, Q9 a, Q10 a. Questions 1 to 6 were the same as in the first, interrupted run.
- P10303 (o_q10ok.png): corner P10303, centre tab "End of Test", text "The test is complete and your score is 50%. Do you want to ________", a "review the test?", b "exit?".
- OK on P10303 with neither chosen (o_p10303_ok.png): P10410 "Review These Objectives:", buttons "1. TTL Integrated Circuits" and "2. Other Integrated Circuits", corner label "P10410". Matches the script. New Foolbook goes to P900 here.
- Bochs death: first run died after OK on Q6 at about 14 min after restore, second run passed the same point at about 12 min and ran 15.5 min without dying. Cause unknown; fewer shots may help.

## 9. More ToolBook quiz and exit findings (Fred, 02:20 to 03:04 JST; each key shot checked by Frank)
- 100% run: P10303 "your score is 100%" (r_q10ok.png). Choosing b "exit?" then OK goes to P900 with no dialog (r_exitok.png). "3. Final Quiz" is then drawn in greyish-blue text but still opens P10004. Correct answers were read from the hidden "Correct" rectangle: its top y (1515 / 2490 / 3465 / 4440 twips) lines up with choice a / b / c / d.
- 70% run (7 right, 3 wrong): P10303 "your score is 70%" (u_q10ok.png). "review the test?" with OK goes to P10410, the same "Review These Objectives" page as at 50% (u_rev1.png). The two buttons are disabled and do nothing. There is no question-by-question review.
- "- Directions" is P10020 (q_dir.png): four lines of instructions and a cartoon teacher. The bottom-left and bottom-right strips both go back to P10004.
- A second Begin in the same session starts at Question 1 with a different question order.
- Long-text pages P1290, P1300, P1302, P1304, P2170 (Reader): all fit, no scroll bar, nothing clipped or past the page edge.
- Lesson Exit on P900 (t_exit1b.png): exactly one "Are you sure you want to Exit the Lesson?" with Yes and No. No stays on P900. Yes quits ToolBook entirely and leaves the Win98 desktop (t_yes3.png).
- Bochs: three deaths in total (two while changing pages, one after OK on Q6). Later runs of 15 to 53 minutes with fewer shots did not die.

## 10. P1040 body field in ToolBook's dialog (Fred, 12:36 to 12:42 PM guest; one shot checked by Frank, g_w1040_1.png)
- Properties for Text Field: Name "Text", Layer 1 of 6, bounds 600/600/8205/1890, Arial Bold 12, indents first 360 / other 360 / right 310, tab spacing 720, border Inset, word wrap, locked text with mouse events. Same values as the P400 and P450 fields.
- Caret inside the highlighted "TTL" and in the plain text after it: "Typing font" Arial Bold 12 Normal in both.
- Selected "TTL": Arial Bold 12 Normal, text colour swatch light cyan. Selected plain text: same font, swatch a dithered near-white pattern.
- So the colour runs carry only a colour. The whole field is Arial Bold 12 from the field level. (Guest colour is not evidence, so the exact shade is not used.)
