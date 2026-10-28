# Foolbook r11 real viewer: is text scaled like the page?
Written 2026-10-25 (Asia/Tokyo). Foolbook at 59530ea (tag v1.0.7r11), openscript-analysis 1.0.1.post4. File-only: nothing written into any repo, no Bochs action.
**Method.** The real app (`viewer.native.open_book`, not the harness) ran under Xvfb with real Tk windows. For each run a screenshot of the canvas widget was taken (PIL `ImageGrab`, an X screen grab), pages were opened by selecting them in the viewer's page list, and text ink boxes were measured. The page scale and offset come from the viewer's own `fit_view` call. Widths below are divided by that scale, so 1:1 is 624x442. Tk scaling was set with `tk scaling` right after the root is created. Scripts: `/workspace/foolbook_out_new/tools/real_view_measure.py`, `rv_matrix.sh`, `rv_agg.py`; data `foolbook_out_new/realview/*.json`.
**Limits.** Xvfb only, Linux Tk with Liberation/DejaVu fonts. The user's Windows/other desktop (fonts, DPI awareness, Tk version) was not tested.

## 1. Maximised window first (the viewer's own default is screen-24 x screen-80)
Screen sizes 1366x768, 1920x1080, 2560x1440, Tk scaling 1.333. Text values are width / page scale, in page pixels.
| item | ToolBook (1:1) | 1366x768 (page scale 1.502) | 1920x1080 (2.208) | 2560x1440 (3.023) | text/page-scale ratio |
|---|---|---|---|---|---|
| P400 line 1 width | 481 | 490.6 | 479.6 | 481.0 | 1.02 / 1.00 / 1.00 |
| P400 glyph rows (height) | 15 | 15.3 | 14.9 | 14.9 | 1.02 / 0.99 / 0.99 |
| P450 sentence width | 325 | 331.5 | 322.0 | 323.6 | 1.01 / 0.99 / 0.99 |
| P1 Title width (h) | 169 (12) | 173.7 (12.0) | 169.8 (11.8) | 169.4 (11.6) | 1.03 / 1.00 / 1.00 |
| P300 label width | 243 + more text in the region | 394.7 | 394.9 | 395.0 | 1.02 on all three (vs harness 1:1 386) |
| P1310 body line 1 | - | 491.9 | 481.4 | 482.0 | 1.03 / 1.00 / 1.00 |
| Final Quiz stem (ToolBook 292.8) | 292.8 | 294.2 | 286.7 | 288.2 | 1.02 / 0.99 / 1.00 |
| Final Quiz answers A / B / C / D (ToolBook 28.9 / 38.3 / 36.9 / 37.6) | | 28.6 / 37.9 / 36.6 / 37.3 | 28.1 / 37.6 / 36.2 / 36.7 | 28.5 / 38.0 / 36.4 / 37.4 | 0.97 to 1.01 |
| P900 panel picture, width / page scale | | 446.0 | 446.1 | 446.3 | constant |
Every row of the matrix (all 4 Tk scalings) gives the same text widths; mean text-width ratio over the 16 regions is 1.07, 1.07 and 1.2 only because P900 button edges and one P1 copyright merge fall in the measured regions (measurement artefacts), the plain-text rows are 0.97 to 1.03.

## 2. Answer: does the text scale with the page and shapes?
**Yes. Text is scaled by the same factor as the page picture and shapes, rounded to whole pixels (about +-2%).** It does not stay at 1:1 and is not double-scaled. Evidence: text width / page scale stays at 0.97 to 1.03 for page scales 0.74, 0.99, 1.50, 2.21 and 3.02, while the P900 picture/panel bbox / scale is constant (443.8 to 446.3). A maximised 2560x1440 window shows 45-pixel glyph rows on P400 (45 / 3.023 = 14.9 vs ToolBook 15).
- The page is fitted by height: scale = (canvas height - 24) / 442. The viewer's listbox sidebar takes about 160 px of the width, so on a wide window the page sits centred with blank space on both sides. If the user's page looks small compared with the window, that is why; the text is not the cause.
- **Tk scaling (DPI) has no effect on text size**: widths and glyph rows are identical at tk scaling 1.0, 1.333, 1.667 and 2.0 on every page of the matrix. Exceptions below.

## 3. Other window sizes
| window | canvas | page scale | P400 line 1 / scale | P400 glyph h |
|---|---|---|---|---|
| root 648x466 | 488x466 | 0.744 | 482.8 | 12 px (= 16.1 / scale, ToolBook 15) |
| root 800x600 | 640x600 | 0.987 | 488.2 | 15 |
| 808x466 (canvas 648x466, exactly 1.0) | 648x466 | 1.000 | 482 | 15 |
In the small window (scale 0.744) the width still follows the page (482.8) but the glyph rows are 16.1 page px against 15, from whole-pixel font sizes.

## 4. Where in the code (read only, `/workspace/foolbook_new`)
- `engine/place.py` `place_window` (lines ~116-170), the one place the window scale reaches text: `item["size"] = max(1, int(round(recorded * scale * 96 / 72)))` and `item["px"] = True` (also per run, `item_run["size"]`). The book stores points; 12 pt becomes 16 px at scale 1.0. The window scale multiplies once, and `marginL` / `marginR` / `indentRest` are scaled the same way.
- `engine/graphics.py` `_typeface` (lines ~424-436): when `px` is set the Tk font size is made negative: `size = -abs(int(size))`. A negative Tk size is pixels, so Tk's DPI setting (`tk scaling`) cannot enlarge it a second time. That is why DPI does not matter.
- `viewer/native.py` `_apply_fit` (lines ~219-250): `scale, dx, dy, ox, oy = fit_view(box, cw, ch)` then `_redraw((scale, ...))` -> `place_window` -> `draw`. Pictures, shapes and text all go through `place_window`.
- Not scaled (inferred from code, not seen on a page): the fallback label of a button whose picture file is missing, `graphics.py` ~line 147, `canvas.create_text(x + 4, y + 2, text=..., anchor="nw")` has no font, so it is Tk's default font at a fixed size, not scaled with the page, only by `tk scaling`.

## 5. Things I did see that look wrong in the real viewer
1. **P400 "Output" label wraps ("Outpu" / "t")** at 1366x768 (scale 1.50) and 1920x1080 (2.21), but not at 2560x1440 (3.02). Fields keep their width x scale while the integer font size grows in steps, so a tight label breaks at some window sizes. Same code, not DPI related. Picture: `/workspace/reports/foolbook-real-viewer-P400-1to1.png` (right panel).
2. **P1040 (coloured letters) depends on Tk scaling**: scaling 1.0, 1.333 and 2.0 give two lines and "family" ends line 1 (w 489.9 / 165.7 at 1366x768; ToolBook 483 / 162). At **scaling 1.667** the coloured-run painter draws "Transistor-TransistorLogic" with the yellow letters overprinting the neighbours and "family of" on line 1 (w 766 / 211 at scale 1.50). This is the one text path where DPI matters (the run measure and the paint disagree at that scaling); `engine/graphics.py` `_paint_marked` / `piece_width`. Image: `p900-work/rv_P1040_by_scaling.png`.
3. The headless harness (Tk at its default scaling 1.388 on Xvfb) shows P1040 at 1:1 with overprint and "family" on line 2 (w 432). In the real viewer at 1:1 it shows 502 / 140 (the wrap is one word late). So the harness numbers I gave for P1040 and P2170 were harness-specific; the real viewer at 800x600 and at 1366x768 draws P1040 and the P2170 table like ToolBook (P2170: header y250, rows y289 / 308 / 327 / 347, `.00001` on the CMOS row; ToolBook rows 290 / 308 / 327 / 347). At exactly scale 1.0 P1040 is "family of" / "integrated circuits." (502 / 140).

## 6. Side-by-side images (P400 at the default maximised 1366x768 window)
- `/workspace/reports/foolbook-real-viewer-P400-1to1.png`: ToolBook shot (left, the page at 1:1) and the viewer's page area scaled back to 1:1 (right).
- `/workspace/reports/foolbook-real-viewer-P400-side-by-side.png`: ToolBook scaled up x1.5 (nearest) next to the viewer's page area as drawn (scale 1.502).
- Full viewer window: `/workspace/reports/foolbook-real-viewer-P400-window-1366x768.png` (1182x688 canvas).
Differences visible there: page colours (blue/grey vs ToolBook's dark red / lilac), not text size.

## 7. Not verified
- Windows or other-OS Tk, DPI-aware or bitmap-scaled windows, other fonts (here Arial maps to a metric-compatible face).
- The user's real window and screen size and DPI; no screenshot from the user's machine was available.
- 1920x1080 / 2560x1440 are Xvfb screens, not real displays.
