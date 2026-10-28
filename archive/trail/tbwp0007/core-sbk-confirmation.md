# Core system books confirmation (2026-10-14)

> Trail, 2026-10-16. Chapter 15. If this sheet and `TBdecompile/record/` disagree, the record wins.

## tb80.sbk and tb80i.sbk — confirmed as main runtime system books

| File | Size | Type table | sysBooks refs | Notes |
|------|------|------------|---------------|-------|
| `tb80.sbk` | 3.1 MB | Polygon at 11957 | 4 | Core runtime library. High menu/dialog counts. |
| `tb80i.sbk` | 619 KB | Polygon at 8021 | 0 (linkSysBook: 4) | Instructor system book. Higher Page/Book counts. Contains AICC and initialize. |
| `tb80a.sbk` | 2.4 MB | Polygon at 11477 | 3 | Author-side companion. Parked. |

Both contain the full object type table (Polygon, IrregularPolygon, Line, AngledLine, Curve, PaintObject, Picture, Group). Neither contains OpenScript handlers. They are resource containers (type tables, menus, dialogs).

**Conclusion:** `tb80.sbk` is the main runtime system book. `tb80i.sbk` is the Instructor companion. Both are confirmed.

## tb80aicc.sbk — AICC session tracking

Size: 86 KB. No OpenScript handlers. Contains AICC property and function names used for session tracking.

### Key properties

| Property | Purpose |
|----------|---------|
| `ASYM_AICC_SID` | Session ID |
| `ASYM_AICC_student_id` | Student identifier |
| `ASYM_AICC_score` | Score |
| `ASYM_AICC_lesson_location` | Bookmark / location |
| `ASYM_AICC_time` / `ASYM_AICC_Time` | Time tracking |
| `ASYM_AICC_LaunchFile` | Launch file |
| `ASYM_AICC_URL` | AICC URL |
| `ASYM_AICC_credit` | Credit flag |
| `ASYM_AICC_output_file` | Output file |
| `ASYM_AICC_path` | Path |
| `ASYM_AICC_Interactions` | Interaction records |
| `ASYM_AICC_InitDone` | Init complete flag |
| `ASYM_AICC_InLesson` | In-lesson flag |

### Key functions

| Function | Purpose |
|----------|---------|
| `ASYM_AICC_Init` | Initialize AICC session |
| `ASYM_AICC_ExitAU` | Exit assignable unit |
| `ASYM_AICC_GetSingleParameter` / `GetMultipleParameters` | Read AICC parameters |
| `ASYM_AICC_BuildPostStr_PutParam` | Build putparam post string |
| `ASYM_AICC_Set_Score` | Set score |
| `ASYM_AICC_ProcessForError` | Error handling |
| `ASYM_CMS_MarkAsCompleted` | Mark course complete |
| `ASYM_CMS_IsCourseCompleted` | Check completion |
| `ASYM_CMS_RecordScore` / `CollectTotalScore` | Score recording |
| `ASYM_CMS_SetBookmarkFileName` | Bookmark file |
| `ASYM_ConvertToAICCPercent` | Score conversion |
| `ASYM_BlockSuspend` / `ASYM_RestoreSuspend` | Suspend/resume |

### Config flags

`AICC_AllowDecimalsInScore`, `AICC_ScoreIndividualQuestions`, `AICC_IncludeHTTP`, `AICC_DateFormat`, `AICC_TimeFormat`, `AICC_CustomConfig`.

**Conclusion:** `tb80aicc.sbk` is the AICC compliance system book. It holds the property and function names used for session tracking, scoring, and bookmarking. Logic is implemented in the DLLs (likely nc81rec.dll or a companion). No OpenScript handlers are present.

## Parked

| File | Reason |
|------|--------|
| `tb80web.sbk` | Web support. Not required for local NIDA playback. |
| `tb80ftp.sbk` | FTP. Not required. |
| `tb80a.sbk` | Author-side. Parked. |
| `tb80acta.sbk` | ActiveX author. Parked. |
| `tb80x.sbk` / `tb80lmx.sbk` | Specialty. Parked. |

## Next steps

- Extract the full type table from `tb80.sbk` if not already captured from the Nida books.
- AICC property names can be added to the runtime property table for session tracking support.
- Parked books remain in the archive. No further processing unless NIDA playback requires them.
