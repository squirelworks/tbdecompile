# Foolbook r18: Begin button, quiz click, and the ? link. Static reading only

Date: 2026-10-25 (Asia/Tokyo). No Bochs, no viewer, no test run, nothing written into any repo.
Read: `/workspace/repro/src_r18_git` (r18, commit 18801ec), `9E954D01.TBK`, the ToolBook shot `/workspace/bochs/shots/l_p10004.png`,
the script dumps (`foolbook_out/all/page_handlers.txt`, `nc81test_handlers.txt`, `reports/p-layout_scripts.txt`), the Ghidra output `decomp/TB80BAS.DLL.c`.
To read the book file I called `openscript_analysis`' store reader (read-only parse, `PYTHONDONTWRITEBYTECODE=1`). The Foolbook viewer was not started.
Store reader = `/workspace/repro/venv313_r18/lib/python3.13/site-packages/openscript_analysis/formats/tbk/store.py` (cited below as store.py).

---------------------------------------------------------------------------
## 1. "- Begin" on P10004 always looks pressed

### What ToolBook's scripts say (P10004)
| object | handlers |
|---|---|
| button `selection1` (Begin) | `buttonClick`: `setupQuizEx("Quiz",2,"P10301","P10302","P10303")`, `clearpool`, `addObjectiveToPool(1,110,119,6)`, `(2,120,129,4)`, `setuppool()`, `gotoNextQuestionEx()` |
| text field `selection1` (the "- Begin" label, sits on top of the button) | `mouseenter`: `send mouseenter to button "selection1"`; `mouseleave`: same with mouseleave; `buttonDown`: `set invert of button "Selection1" to true`; `buttonUp`: `set invert of button "Selection1" to false` |
| button `selection2` / field `Selection2` (Directions) | identical pattern; click goes to P10020 of nida81.tbk |
| page script | same handlers again (page_handlers.txt lines 5516-5690) |

Nothing in the book or in nc81base/nc81test/nc81recs/nc81trnr defines a mouseenter/mouseleave for a button (grep over all handler dumps: only these forwarders). No `hilite`, `sysState`, or stroke-colour logic exists on P10004.
So ToolBook's behaviour, from the scripts alone:
- **normal**: the button's *up* face (flags byte `0x0b` = enabled, not pressed).
- **hover**: nothing visible. `mouseenter` is forwarded to the button, which has no handler for it.
- **pressed**: while the mouse is down on the label, `invert` of the button is true, and false again on mouse up. How ToolBook draws `invert` is not decoded here (UNVERIFIED). The likely candidate is the stored "down" face (bitmap 162, the glowing white one). The draw routine `FUN_1230_18d2` picks the down face for flag bit `0x04` (decomp/TB80BAS.DLL.c:103798).

### Why Foolbook shows Begin pale ("pressed")
**Cause: data, not state.** Foolbook draws the button's stored *up* face, and on P10004 that slot holds a different bitmap.
- `store.py:535-544` (`_button_bmp`): `flags = d[rec+0x26]`; `up = w(block+0x15)`; picks `down` only if flag bit `0x04`, `disabled` only if bit `0x01` is clear; otherwise `stored = up`. Loader turns it into the image at `engine/loader.py:328` (`picture = _png(obj.get("bmp"), ...)`).
- Face table of the button record (slots at block +0x15, +0x27, +0x39, +0x4B = up, down, disabled, **checked** face). `FUN_1230_18d2` uses the 4th slot only when flag bit `0x10` is set on a radio/check style button (styles 5,6,8,9). P10004 Begin has flags `0x0b`, style 1.
  - P10001, P10002, P10003 `selection1`: up=161, down=162, checked=163.
  - P10004 `selection2` (Directions): up=161, down=162, checked=163.
  - **P10004 `selection1` (Begin): up=163, down=162, checked=161.** Up and checked are swapped in the file (the record's own width is also 208 px instead of 207, bounds 3120..6225 vs ..6210).
- Bitmaps: 161 = saturated cyan, raised, dark bottom edge. 162 = glowing white (down). 163 = pale light-cyan flat face (the "checked" look, same look the quiz letters take when chosen). Foolbook therefore draws the pale checked face on Begin and nothing can ever change it.
- File scan of all 380 buttons in 9E954D01.TBK: 301 have a 4th (checked) face. In 300 of them up-id < checked-id. **P10004 `selection1` is the only exception.** So this is a one-off oddity of that record. P10001-P10003 and P900 are fine, which matches the user's observation (only Begin on P10004).
- Foolbook has **no hover and no press handling at all**. `viewer/native.py:342` binds only `<Button-1>` (a release-less click). No `<Motion>`, `<ButtonPress>`, `<ButtonRelease>`, `<Enter>`, `<Leave>` anywhere (grep over engine/, viewer/, foolbook/). `engine/engine.py:_apply_set` handles only `text of field/button`; `set invert ...` is never run, `mouseenter/mouseleave/buttonDown/buttonUp` are never dispatched (only the keyword tables mention them). So Foolbook cannot show the pressed look on any button; it only shows whatever face is stored.

### What ToolBook actually draws for Begin
The ToolBook shot `l_p10004.png` (Reader level, pointer below Directions): the Begin and Directions faces are **pixel-identical** except inside the label rectangle (diff bounding box x65-139, y12-27 of the 207x41 face; I diffed the two regions directly). Faces 161 and 163 differ a lot in raw colour, so if ToolBook had drawn 163 for Begin the two buttons would very probably differ in the shot. Colour from the guest is not evidence, so treat this as supporting, not proof.
- Confidence: **high** that Foolbook draws bitmap 163 for Begin because the file stores it in the up slot (store.py:536, loader.py:328, the swap shown above). **Medium** (about 70%) that ToolBook draws 161 there. **Not determined statically:** why ToolBook shows a normal face when the record's up slot says 163 (the decompiled draw routine reads slot 1 as the up face; something else at load may swap them back, e.g. the author's saved "invert/checked" state).
- Candidate fix (not applied, not verified in ToolBook): for push-button styles (record byte +0x27 & 0x7f = 1) never take the checked slot as the rest face; use the lower of the up/checked ids, which is right for 300/301 buttons and for P10004 Begin. Separately, press feedback needs `<ButtonPress-1>`/`<ButtonRelease-1>` handlers that show the down face while the mouse is down on the label field (the label field is the one that forwards buttonDown).

---------------------------------------------------------------------------
## 2. Quiz logic: choice click, OK, Next

### What ToolBook runs
Each question page (P10210-P10229) has a page script with `enterPage` and `buttonClick`; the latter is only `get handleQuizClick(target)` (page_handlers.txt; exactly one `handleQuizClick(target)` per page, 20 in total). `target` is the object clicked.
`handleQuizClick(vTarget)` (nc81test at file 0x80d3):
1. If the target is a field or group child (not a button, not the page): take its name (or its parent group's). If it is a..e, and that button is enabled, `send buttonClick to button temp` and return. This re-enters the handler with the button as target.
2. If the target is a button named a..e: `manageQuizButtons(temp)` = `set checked of button temp to true` and uncheck the others (radio behaviour, file 0x85a8). **Nothing else happens on a choice click.** The checked state is the face change (the 4th-slot light-cyan face; the stored `checked` flag).
3. If the target is `OK`: in pass 1 or 2, `response = getQuizResponse()` (reads which of buttons a..e is `checked`); empty means `beep(1)` and return; otherwise `get gotoNextQuestionEx()`.
4. `Help`: sets `__quizHelp`, goes to the page's helppage. `Skip`: if a choice is checked it asks "Do you want to discard your answer?", then `gotoNextQuestionEx`. `Back`: `gotoPreviousQuestionEx`. `Next`: `gotoNextQuestionEx`.

`gotoNextQuestionEx` (file 0x63b7): in pass <=3 with index > 0 it records the answer of the page you are leaving: `response = getQuizResponse()`; `score = 100` if `response = answer of this page`; `storeQuestionResponse(testNo, questionNo, response, score)`; empty response goes to `storeQuestionSkipped`. Then `getNextQuestion()` picks the next page (`questionno of page i`) and runs `setupQuizPage`. At the end of the pool it goes to `__quizPages[3]` = P10303 at the default Quiz Mode 0.
State recorded: `__quizResponse[]`, `__quizScore[]`, `__quizIndex`, plus the checked flag on the page's buttons.
What enables OK/Next: `setupQuizPage` (file 0x6d36, lines 883-895 of nc81test_handlers.txt) in pass 1: OK enabled; **Skip enabled only if `__quizMode <> 0`**; Back, Next, Help disabled. OK never depends on a choice being made; with none it beeps.
The stored flags in the book match that state on P10210: Back, Help, Next have flags `0x0a` (disabled), OK and Skip `0x0b`. (My dump, `A` is `0xab`, the others `0x0b`.)

### What Foolbook does (r18)
- `viewer/native.py:302-332` (`on_canvas`): hit-tests the object, stores its name in `state.variables["target"]` (line 307). For a letter A-E it first calls `quiz.call(state,"handleQuizClick",'"A"')` (lines 309-312), then runs the object's own click script if any, then the page's `buttonClick` (line 320), i.e. `handleQuizClick(target)` a second time (harmless, `_choose` is idempotent).
- `engine/quiz.py:254-265` `_choose`: sets `__choice`, sets `checked` on the non-text shapes named A-E, sets `__redraw`. `native.py:327-329` repaints. The face change is a flat `#91ffff` rectangle painted over the whole button box (`engine/graphics.py:159-163`), not the stored 4th-slot checked bitmap. It also hides the letter.
- `quiz.py:285-297` `_click` for `OK`: if the quiz is not running (`__quizCount` = 0) it goes to the next page of the book (`_neighbor`, the r16 change); if pass is 1/2 and `__choice` is empty it returns 0 (no beep, no visual); otherwise `_next` (quiz.py:217-237): scores the page, bumps `__quizIndex`, `_prepare` clears `__choice`, returns `("goto", page)`. `engine.py:_run_block` turns that into a goto action; `follow` moves; `native.show` repaints.

### Can a choice click leave the quiz stuck?
- **I found no code path in the engine that leaves Begin -> choice -> OK stuck.** Checked by reading: (a) the hit test on a question page: the OK image is in front of the bottom strip rect; no object covers it (objects of P10210 listed from the file: Test rect, strips, Back/OK/Help/Skip/Next, Correct rect hidden, Stem, A-D buttons, A-D text; OK at x227-276 y419-437); (b) `_click` OK with `__choice` set always reaches `_next`; (c) `__choice` is cleared only in `_setup`, `_clear`, `_prepare` (on a page change), end of pool and Skip; (d) a single page `buttonClick` per page, so OK does not run twice; (e) repo tests `engine/test_sysbook.py:106-150` cover the same chain on stub pages.
- So the symptom "the button changes, then nothing" is **not explained by the quiz engine as I read it**. Things that could produce it and cannot be ruled out statically:
  1. **An exception inside the Tk callback.** `on_canvas` has no try/except (native.py:302-332). Tk prints the traceback to the terminal and the window keeps the half-updated state. The user should check the terminal for a traceback after the click.
  2. **The click did not land on OK** (for example on the strip beside it, on greyed Back/Help/Next, or on the label of a different page). A click on a stored-disabled button still runs its handler in Foolbook (Next/Help/Back are drawn greyed, flags `0x0a`, but `_click` handles `NEXT/BACK/HELP` anyway, quiz.py:298-313). In ToolBook a disabled button sends nothing.
  3. **OK with no recorded choice is silent.** ToolBook beeps; Foolbook returns 0 with no beep or message (quiz.py:295-296). If `__choice` is empty, Foolbook looks frozen.
  4. **Skip is clickable and shows as enabled** (flags `0x0b`) although `setupQuizPage` disables it at Quiz Mode 0. Pressing it records 0 and advances (quiz.py:298-303).
  5. **A different build / book copy** than r18 + this 9E954D01.TBK.
- Differences from ToolBook worth fixing (none proven to cause the stuck report):
  - choice face is an overlay, not the checked bitmap (graphics.py:159-163);
  - checked state lives in `shape["checked"]` on page shapes and `__choice`, not per button like `checked of button`; going Back resets it (`_prepare` clears `__choice`);
  - no disabled-button handling; no `beep`; no `setupQuizPage` enable/disable run;
  - `__quizResponse[]` is not kept, so Back/Next review (passes 3-5) cannot restore answers.
- Confidence: **high** on the ToolBook handler list; **medium-high** that the engine chain Begin -> letter -> OK works as coded; **low** on the cause of the user's stuck quiz. **Not determinable statically:** which object the user clicked, whether a traceback was printed, and the user's exact build.

---------------------------------------------------------------------------
## 3. The "?" button (Help) and nida81

### ToolBook
P10004 `Help` button script (page_handlers.txt):
```
system lastbook; lastbook = name of this book
system nextpage; nextpage = name of this page
go to page "P20001" of book "nida81.tbk"
```
P300's equipment bar does the same with `go to page "P310" of book "nida81.tbk"` (p-layout_scripts.txt). Bochs shot `y_bk.png` shows P20001 fine.

### Foolbook
1. The click runs the Help button's own `buttonClick` (`native.on_canvas` -> `click_script`); `engine.py:_run_block` turns the `go to page ... of book ...` into a goto action with book `nida81.tbk`; `follow` calls `open_book(state,"nida81.tbk","P20001")` (engine.py:776-805).
2. `open_book` looks in the shelf first, else `find_book(book_name, state.book.path)` (engine.py:788), then `load(found)` (line 792) and **switches `state.book` before it knows the page exists** (line 795), then `goto(..., "P20001")` (line 801).
3. `engine/loader.py:36-75` `find_book`: search directories in this order: the book's own folder; the folder above; every subfolder (first 40, unsorted `iterdir`) of both; then **Foolbook's `core/`** last. In each directory the suffix order is `.fsk, .sbk, .fbk, .tbk, .json` (line 67-70). So a `nida81.tbk` anywhere in the first group of directories beats the stub in `core/`, but inside one directory a `nida81.fsk` beats a `nida81.tbk` in that same directory. The current directory (cwd) is never searched. `find_book` takes the *book's path*, so launching from another folder (Foolcourse's `subprocess.Popen([python,-m,foolbook,path])`, `menu/menu.py:124-127`) does not change the search as long as the path to the course is what is passed; it only matters that nida81.tbk sits next to that course, one level up, or in a sibling folder.
4. **When no nida81.tbk is found, the stub `core/nida81.fsk` is opened.** It holds 48 pages with text lists and links only: `shapes` is empty for every page, including P20001 (text "INPUT DEVICE - Use your mouse to make se...") and P310 ("Minimum Requirements 586 133 MHz ..."). The viewer draws shapes and synthesised buttons from `items` (`native._objects`, native.py:159-183), not the page's text list, so **P20001 and P310 from the stub draw as a completely blank white page** (the stub-only P300 shot `reports/page-compare-r18/r18-P300-click-stub-only.png` is that). The sidebar list also switches to the stub's page names (P20000, P22130, ...). That is "a broken page from the other book". P10020 from the stub is also text only (no shapes), so Directions would be blank too.
5. When a real `nida81.tbk` is found: `_load_store` decodes P310's picture (class 0x19, row 6 of the table at header+0x104; `store.py:_picture`) and `loader.py:_clear_edge` removes the white mat; r18 P310 and P20001 matched the ToolBook shots in my earlier compare (that compare used the real nida81.tbk beside the book).
6. If the page is missing in the opened book, `open_book` has already switched the book (line 795) and returns False; native still calls `show(state.index)` (native.py:325/339), so the viewer shows the other book at its remembered/first page. Not the case for P20001/P310 (both exist in tbk and stub), but it is how a half-failed jump would look.

What the user sees, by case:
| nida81 found | what the ? and P300 links show |
|---|---|
| real nida81.tbk in the search path | P20001/P310 drawn (picture + text), as in the Bochs shots |
| only core/nida81.fsk (a fresh git clone has only this) | blank white page, sidebar switches to the stub list |
| a different nida81.tbk build | unknown; the picture table row index (store.py `_picture`) is verified only against our copy |

- Confidence: **high** for the search order and the stub's emptiness (read from loader.py and the unpacked stub). **High** that a clone without nida81.tbk shows a blank page. **Not determined statically:** where the user's nida81.tbk is (if anywhere); whether their copy matches ours; what Foolbook shows if they found a torn picture page (P320...P390 are torn in r18 regardless).
- Candidate fixes (not applied): ship a real fallback or show a clear "nida81.tbk not found, put it next to the course" notice instead of the blank stub; do not switch `state.book` until the target page exists; prefer `.tbk` over a same-folder `.fsk` stub.
