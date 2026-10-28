# WDW breakpoint syntax correction

> Trail, 2026-10-16. Kept. Chapters 7 and 12. @ not !, resume on is not a creation flag. If this file and `TBdecompile/record/` disagree, the record wins.

**Date:** 2026-10-16

## SoftICE vs WDW

| Debugger | Module qualification |
|----------|----------------------|
| SoftICE | `TB80BAS!OBJFILEOPEN` |
| WDW | `TB80BAS@OBJFILEOPEN` |

`!` does not work in WDW. Use `@`.

## Resume

`resume on` is a property of an existing breakpoint, not a creation flag.

```
break TB80BAS@OBJFILEOPEN
break 1 resume on
```

## If `@` fails

ToolBook DLLs are NE without Watcom debug info. WDW sees export names in the Functions window but may not resolve them on the command line.

1. Open Functions window. Find the name.
2. Right-click → Break.
3. In Break window, select it and turn on Resume.

Or use the live address from a prior hit:

```
break 44CF:0DE8
break 1 resume on
```

Selector changes per boot.
