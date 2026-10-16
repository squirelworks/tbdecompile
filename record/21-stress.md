# 21. What the stress run broke

**Date:** 2026-10-16

**Status:** The Python in `openscript_analysis` and the Foolbook engine, run under a stress suite. This is not a timing of `TB80BAS`. It does not name the record reader.

## Claims

| Id | Grade | Statement | Source |
|---|---|---|---|
| P-001 | Known | Four nested `step` loops from 1 to 100 do not finish. Each loop had its own cap of 10,000, so the caps multiplied. | `engine.py` before the shared budget |
| P-002 | Known | Eighty nested `if` lines raised `RecursionError`. | The same runners |
| P-003 | Known | `name = "a and b"` was split on the `and` inside the quotes, so the comparison was false. | `_eval` |
| P-004 | Known | `ScriptHeap.free` keyed only on the 10-bit index. After the index was reused, freeing the old value freed the new block. | `heap.py` |
| P-005 | Known | `GHeap.alloc` did not look at `data + zero + 0x10`. A request larger than the block was accepted. | `GHeap.alloc` |
| P-006 | Known | One `0xFF` opcode appends up to 256 bytes after the output cap had already been checked. | `expand.decompress`, Foolbook `decode` |
| P-007 | Known | A resource row whose `type` was the word `Bitmap`, or a row that was not a dict, aborted `adopt` before the later rows. | `resmgr.adopt` |

## 21.1 What runs now

The runners share one budget of 200,000 line steps and stop nesting at 48. The four-deep step returns in the stress suite, which itself finishes in under two seconds, and the action list contains `stopped`. The deep `if` does the same. It does not walk off the Python stack.

`and`, `or`, and the comparisons are scanned outside quotes. `&&` in the TBX runner is the same. `if name = "a and b"` now stores `1`.

`free` and `pointer` require the offset as well as the index. A stale value does not resolve, and it does not free the block that reused the index. `GHeap` refuses a request that would pass the end of its block, and a second free of the same ident returns false.

`decompress` and Foolbook `decode` clip each opcode to the room that is left. A 4,000-opcode `0xFF` run with `max_out` of 1,000 stays at 1,000 characters.

A bad resource row is skipped. The row with `type` 1 is still adopted.

A push of 3,000 comma-separated pieces still stops at the index limit (`0x400`) with `0x1F7A`. That path was already right. It stays under a second. The index limit was not raised. Raising it would not match the 10-bit value.

## 21.2 What was not made faster

The heap's per-frame block list is still a list. At 1,024 indexes a free is not the cost. The cost was the nested step, which did not return.

`tbpipeline` `layer_of` is a prefix test. It was not on this path.

The suite after the change is `openscript_analysis.test_stress`, `openscript_analysis.test_machine`, `engine.test_stress`, and `engine.test_runtime`. 38 tests, all passing. None of them reads a page record.
