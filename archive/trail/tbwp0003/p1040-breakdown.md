# P1040 object breakdown (TBKX Page.xml)

> Trail, 2026-10-16. Chapter 13.1. TBX expansion of P1040. If this sheet and `TBdecompile/record/` disagree, the record wins.

Source: TBKX export of page Name="P1040", IdNumber=880.
Background: Background id 2.
Coordinates are ToolBook twips. Screen estimate = twips / 15 (matches earlier live ScaleTwipsToScreen observations).

## Page-level objects

| Type | Id | Name | Bounds (twips) | Screen ≈ | Notes |
|------|----|------|----------------|----------|-------|
| Field | 0 | Text | 600,600,8805,2490 | 40,40–587,166 | TTL intro paragraph. Fill 128,128,128 |
| Button | 1 | Next | 8907,6210,9342,6630 | 593,414–622,442 | Rollover. ASYMI_UseRollover=true |
| Button | 2 | Back | -3,6210,432,6630 | -1,414–28,442 | Rollover. ASYMI_UseRollover=true |
| Group | 53 | | | | Right chip package (7400) |
| Group | 52 | | | | Left chip package (5400) |
| Group | 58 | DiscussionTitle | | | Gold plate + DISCUSSION label |

## Group 53 — 7400 package (right)

Body:
- Rectangle 9: Bounds 4875,3555,7830,4605 → screen ≈ 325,237–522,307. Fill 64,64,64. Stroke 128,128,128
- Arc 10: Vertices (2 pts) 4872,4300 / 4868,3889 → screen ≈ (324,286),(324,259). Stroke 128,128,128
- Field 29: Bounds 6195,3990,6690,4260 → screen ≈ 413,266–446,284. Text "7400"

Bottom pins (7 × IrregularPolygon, 11 points each, fill 192,192,192):
- id 11: screen ≈ [(337,307),(347,307),(347,315),(345,317),(344,321),(343,324),(341,324),(340,321),(339,317),(337,315),(337,313)]
- id 12: offset +27 x
- id 13: offset +55 x
- id 14: offset +84 x
- id 24: offset +110 x
- id 25: offset +138 x
- id 26: offset +167 x

Top pins (nested Group 20 + 3 free):
- Group 20: ids 16–19 (mirrored upward, y base 237)
- ids 21,22,23 (remaining top pins)

All pin polygons share the same 11-point "tip" shape; only the x (and top/bottom y) offsets differ.

## Group 52 — 5400 package (left)

Body:
- Rectangle 31: Bounds 1500,3555,4455,4605 → screen ≈ 100,237–297,307. Fill 64,64,64
- Arc 32: Vertices (2 pts) 1497,4300 / 1493,3889 → screen ≈ (99,286),(99,259)
- Field 51: Bounds 2760,3975,3330,4245 → screen ≈ 184,265–222,283. Text "5400"

Bottom pins (7 × IrregularPolygon):
- ids 33,34,35,36,46,47,48 — same tip shape, x starting at ~112

Top pins:
- Group 42: ids 38–41
- ids 43,44,45

## Group 58 — DiscussionTitle

- Button 55: Bounds 2557,105,6322,1005 → screen ≈ 170,7–421,67. NormalGraphic="bitmap id 149". ASYMI_AutoSize=true
- Field 56: Bounds 3217,375,6157,765 → screen ≈ 214,25–410,51. Text "DISCUSSION" (stroke 0,0,128)
- Field 57: Bounds 3202,360,6142,750 → screen ≈ 213,24–409,50. Text "DISCUSSION" (white stroke, drop-shadow offset)

## Relation to earlier raw-book work

- Pin geometry matches the 11-point IrregularPolygon records previously extracted from P430-style pages (fill 0xC0C0C0 / 192,192,192).
- Chip body is a plain Rectangle with bounds, not a computed region.
- Arc is stored with only two vertices in the XML (bounding points); full arc angles were not exported here.
- This page is Name="P1040", not P420. P420 was the flame/curve page in the original 9e954d01 notes.
