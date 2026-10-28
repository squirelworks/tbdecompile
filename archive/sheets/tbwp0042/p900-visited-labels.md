# P900 Lesson Menu: why "1. TTL" and "3. Final Quiz" turn light-blue

Source: decoded scripts in 9E954D01.TBK and nc81base.sbk / nc81recs.sbk / nc81test.sbk (existing decoder dumps in
`/workspace/foolbook_out/all/*_handlers.txt`, `/workspace/reports/nc81base_handlers.txt`). No Bochs action, no repo write.
Evidence shot: `y_r900g.png` (copied to `/workspace/reports/p900-work/`, crop `p900_visited_crop.png`).

## Short answer
- The hypothesis (setSection writes progress, enterPage reads it back) is **wrong in both halves**.
  `setSection` only logs the section name into the monitor file. It has nothing to do with the colours.
- The colour is a **menu flag held in a ToolBook system variable** `__menuFlags[1..10]`.
  Flag 1 = not done (black). Flag 2 = done (colour `"270,50,100"`).
- P900 `enterPage` -> `setupMenuPageLocal()` -> `setupMenuPage()` recolours the labels from that array.
- Nothing is read from a file, INI or registry for the colours.
  The array only survives while the ToolBook process lives, which explains close/reopen vs fresh restore.

## 1. The script that colours the labels (nc81base.sbk, `setupMenuPage`, file 0xdd76)
```
to get setupMenuPage string menupage, int mode
    system int __menuFlags[10]
    ...
    step i from 1 to 10
        if  not isObject(field("Selection " & i) of page(menupage))  then
            break step
        end if
        increment(nObjectives)
        strokeColor of field("Selection " & i) of page(menupage) = GetMenuTextColor(i)
        if (__menuFlags[i] = 1) then finished = false end if
    end step
    ...   (modes 0-3)  strokeColor of field("Selection T") of page(menupage) = GetMenuTextColor(10)
```
Where the colour comes from (nc81base.sbk):
```
to get getMenuTextColor iColor            -- 0xef0e
    system int __menuFlags[10]
    ...  return __menuColors[__menuFlags[iColor]]

to get clearMenuFlags                      -- 0xed15
    step i from 1 to 10 : __menuFlags[i] = 1

to get setMenuFlag index                   -- 0xedbf
    ... if __quizHelp = 0 then __menuFlags[index] = 2 end if

initializeBase (0xbbef):  error = clearMenuFlags()
                          error = specifyMenuColors(black, "270,50,100")   -- (old line: --specifyMenuColors(black, magenta))
```
Hooks in the book and quiz library that set the flags:
```
P1910 leavepage:   get SetMenuFlag(1)        -- (Next -> P1001, Back -> P1310)
P2910 leavepage:   get SetMenuFlag(2)        -- (Next -> P2001, Back -> P2250)
nc81test saveQuizResults (0xa42c):
    passed = 0
    if getquizscore() >= getObjectiveLevel() then
        passed = 1
        get setMenuFlag(10)
    end if
```
P900 side (book, page script):
```
enterPage:  get setupMenuPageLocal()   -- calls setupMenuPage(name of this page, __lessonMode)
            get setSection("Menu")
            forward
```
(`author` and `reader` handlers on P900 call `setupMenuPageLocal` again.)

Mapping: Selection 1 = "1. TTL Integrated Circuits" (flag 1), Selection 2 = "2. Other ICs" (flag 2),
Selection T = "3. Final Quiz" (flag 10).

## 2. What file / key does it read
None for colours. The state is the in-memory system array `__menuFlags`.

Related file I/O, which does **not** feed the colours:
- `setSection(section)` (nc81base 0xfc37): reads `NIDAREC.INI [Monitor] File`, then writes `[NC71] Section=<section>` into that monitor file (only if the key is non-empty).
  The only reader of that value is the help/quiz alert record. It is not read by `setupMenuPage`.
- `__lessonMode` = `NIDAREC.INI [Lesson] Lesson Mode` (default 2). It only selects which branch of `setupMenuPage` runs.
- Optional persistence, **off in this guest**: `bookmarkSession` (nc81recs 0x5588) writes `__menuFlags1..10` via nc81rec.dll
  `RecWriteVariable`, and `restartSession` reads them back (empty or "0" becomes "1").
  Both return at once unless `NIDAREC.INI [Student] Records` is non-zero. The guest `C:\WINDOWS\NIDAREC.INI` has only `[Lesson]` / `Window=348`, so Records=0 and this path never runs.

## 3. What value means "visited"
- `__menuFlags[i] = 2` means done, so the label is stroked `"270,50,100"`. `= 1` (the default) means black.
- Flag 1 is set when the user **leaves** P1910 (the last page of section 1, by any route, including Back).
  Flag 2 is set when the user leaves P2910 (section 2 end). Neither is set by entering section 1 or by `setSection`.
- Flag 10 (Final Quiz) is set when the quiz is finished with score >= `getObjectiveLevel()`.
  The default is **70** (`[Quiz] Objective Level` is absent, see book-survey-and-quizzes.md). A fail does not grey the label.
  `setMenuFlag` does nothing if `__quizHelp <> 0`.
- Colour: the Bochs guest is 16-colour planar VGA. Shot `y_r900g.png` shows labels 1 and Selection T text at RGB (109,145,255), and labels 2 and Exit at (0,0,0).
  `"270,50,100"` read as RGB (270 clamps, 50, 100) would be a pink-red, so the shot only fits **hue/sat/brightness** = (191,128,255) lavender,
  quantised to light blue by the 16-colour palette. On a true-colour display it would probably look light purple (the old comment said `magenta`). Unverified on a true-colour display.

## 4. Does "Lesson Exit" have a condition?
No. The P900 field is named "Exit". `setupMenuPage` only touches fields named "Selection <n>" and "Selection T", so Exit is never recoloured.
Its scripts are `buttonClick` (`send keyup keyF2 to this page`) plus the mouse enter/leave/down/up highlight handlers. It stays black.
"2. Other ICs" is black simply because flag 2 is still 1 in that session. (In the shot, section 2 had not been left via P2910.)

## 5. Why it survives close/reopen and not a fresh restore
`clearMenuFlags` runs only inside `initializeBase`. `enterSystem` / `enterBook` (book script, ~lines 318-345 / 411) call it only if `nc81base.sbk` is **not already in `sysBooks`**.
System variables live as long as the ToolBook runtime. Closing and reopening the book inside the same runtime keeps `__menuFlags`.
A fresh runtime (Bochs snapshot restore or full exit and relaunch of ToolBook) resets it to all 1, so all four labels are black.
To confirm: exit the ToolBook Reader entirely, not only the book. The colours should then reset, since Records=0.

## 6. Could Foolbook reproduce it from the book alone?
**Not from the book alone, but cheaply with a small built-in.** r8 draws all four black: it has no `__menuFlags`, no `leavePage` hook for these calls, and no `setupMenuPage` (grep of `engine/` finds none).
- In the book: the P900 `enterPage` call, the P1910 / P2910 `leavepage` handlers (`SetMenuFlag(1/2)`), and the label field names.
- Not in the book (nc81base.sbk / nc81test.sbk): `setupMenuPage`, `getMenuTextColor`, the colours (black / `"270,50,100"`), flag semantics, pass mark 70.
  `engine._builtin_page` already hard-codes the sibling `gotoMenuPage` / `gotoQuizPage` for the same reason.
- To add: a state array `__menuFlags[1..10]` = 1. On leaving P1910 set flag 1 and on leaving P2910 set flag 2 (these are the exact book handlers).
  On quiz completion with score >= 70 (default) set flag 10. On entering P900 (and re-showing it), set the text colour of "Selection 1", "Selection 2" and "Selection T" to black or `"270,50,100"` per flag; leave "Exit" alone.
  The state should be per Foolbook session (not saved to disk), like ToolBook.
- Open: how Foolbook should render `"270,50,100"` (HSB lavender (191,128,255) is my inference; the one ToolBook shot is 16-colour).

## 7. Searched and not found / remaining
- Searched: all 46 nc81base handlers, nc81recs, nc81test, 9E954D01.TBK page/layer/book/field handlers for `strokeColor`, `textcolor`, `fillcolor`, `enabled`, `menuFlag`, `GetPrivateProfile`, `nc81rec.dll`. The P900 label fields have no colour scripts. No book handler sets the colours directly.
- Not read: tb system books (tb80*.sbk) were not needed. `nc81trnr` / nc81bank were grepped and do not use `__menuFlags`.
- Remaining: (a) the exact true-colour appearance of `"270,50,100"`; (b) a live test that leaving P1910 sets flag 1 (inferred from script and the shot, no new Bochs run);
  (c) `__quizObjectiveLevel` is 70 only if no INI override. The guest INI has none.
