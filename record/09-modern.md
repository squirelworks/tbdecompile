# 9. The modern stack

## Claims

| Id | Grade | Statement | Source |
|---|---|---|---|
| M-001 | Known | The clean-room reader is not the engine. It does not score quizzes, place every bitmap, or run the NE images. | WV-005 |
| M-002 | Known | Foolbook opens `.tbk`, `.sbk`, `.fbk`, and `.fsk`. Shapes come from kind `0400` polygons and from bounds-only rectangles. | Foolbook `engine/shapes.py` |
| M-003 | Known | Foolcourse is the process that serves a book. Foolbook is a local window. If Foolbook is started by a course, it pulls the book and skips the splash. | release notes, 2026-10-13 |
| M-004 | Known | The dependency order is Foolversity, then Foolcourse, then Foolbook, then `openscript_analysis`. Foollege is the layer under Foolversity that holds courses. It is not a running server in the current release. | hierarchy note |
| M-005 | Known | TBpipeline 1.0.0r4 parses `9e954d01.tbk` (129 pages) without running RTM. A known bug is an 18-versus-23 render count. | pipeline release note |
| M-006 | Thought | A reader that prefers explicit points, then TBX Vertices, then bounds, will look like the lesson often enough to study it. It will not be a substitute for the Win98 runtime until the reader in chapter 4 has a name and the picture id is known. | project philosophy |

## 9.1 Foolbook

The engine parses the 8.1 container. It does not load `TB80BAS`. Polygons use the kind `0400` layout (count at `+0x1A`, pairs at `+0x22`). Rectangles use the bounds-only tail (`01 00 00 04`). On Logic Families that is on the order of 165 shapes from the early polygon-and-rect pass, and 961 rectangles from the later marker scan. Both counts can be true. They are different patterns.

System books: core `.fsk` first, user `.fsk` after, as mods. `.sbk` is accepted. It is not required for the v1 player.

The window is native. A direct start opens `using_foolbook.fbk` and a splash that asks whether to resume the last page. A start from Foolcourse, or a start on a named file, skips the splash and uses the last page the course recorded. The splash text is a joke (`2+2=5` / “For greater values of 2.”). It is not part of the book format.

OpenScript in this player is the subset in chapter 6. ActiveX, Python, and C++ as replacement engines are a stated direction. They are not implemented.

## 9.2 Foolcourse and Foolversity

Foolcourse is the only server in the current release. Foolbook does not listen. The earlier idea that Foolbook itself served on port 1337 was withdrawn: a local viewer should not be the thing that stays up after the tab closes.

Foolversity writes students, schools, and curricula. Foolcourse reads them. The hierarchy, as stated, is: a Foollege sits under Foolversity and has Foolcourses; a Foolcourse has Foolbooks; a Foolbook can run OpenScript. Foollege is not the current server. A later Foolcollege was discussed as the place that would hold several courses for several students. That program does not exist yet.

Install is a virtual environment and `pip install` of the Foolversity git URL. A system Python on Debian will refuse the install. That is PEP 668, not a missing package. If a dependency has not changed, a reinstall should not download it again unless a fresh-start flag is set. That rule was written after several reinstalls pulled `openscript_analysis` for no content change.

## 9.3 TBpipeline and the unpacker

TBpipeline’s useful stage is the file parser: load order recorded from a SoftICE log, then a TBK open, then a page walk, then HTML. The Unicorn RTM stage still stops before the book is opened, so a render from this package is a parse, not a playback. Curves, including an attempt at the P420 flame, are emitted as separate files. They are not placed on the page (WV-004’s falsifier still stands for placement).

`toolbookunpacker` produces an honest NE image. It clears the Optloader self-load flag. It does not patch the entry table for Ghidra. That patch lives beside the unpacker as an optional post-step. Only BAS, on the current set, has entry segment bytes at or above 128.

## 9.4 What “getting NIDA working” means

Three different finishes are easy to mix up.

| Finish | Done when |
|---|---|
| A page can be read | Field text, jumps, and the decoded shapes for that page match the Win98 screen closely enough to study the lesson. |
| A lesson can be walked | Next, Back, menus, and quiz flow follow the handlers, including the jumps into `nida81.tbk`. |
| A lesson can be run | The system books load, `initializebase` / `initializerecs` / `initializetest` do what the DLL exports imply, pictures land on their widgets, and the unnamed reader is no longer unnamed because the clean-room code does the same thing for the same bytes. |

The first is partly done for Logic Families. The second is partly done for the menu and the quiz ids that have been transcribed. The third is not done. Authorship and a modern `TB80CMP` are side work. They help the next person. They do not open P1040.
