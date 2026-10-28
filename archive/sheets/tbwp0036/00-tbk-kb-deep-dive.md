# ToolBook Knowledge Base Deep Dive

**Source:** https://dennydedmore.com/toolbook/knowledgebase/kb/ToolBook%20Knowledge%20Base.html  
(and related pages under https://dennydedmore.com/toolbook/)

**Host / Author:** Denny Dedmore (ex-SumTotal / Asymetrix ToolBook SME). He created the official Knowledge Base while at SumTotal and preserved a copy after SumTotal scrubbed ToolBook resources following EOL on 31 Dec 2021. Personal site established ~January 2026. He wrote >95% of the articles. Contact: contact@dennydedmore.com.

**Last noted update on main KB page:** 10/12/2026.

## Overview and Historical Context

ToolBook (Asymetrix → click2learn → SumTotal) was a Windows-based multimedia / e-learning authoring tool using a book/page metaphor, OpenScript scripting, Catalog objects, Actions Editor, DHTML export, SCORM/AICC support, etc. Final version: 11.5 (Dec 2012). Sales, support, and activation services ended 31 Dec 2021. No new activations possible; existing activated installs continue to work. Older versions (<9.5) do not require activation.

The KB is explicitly for historical purposes now. It covers troubleshooting, compatibility, patches, publishing, and usage tips.

Main entry page emphasizes:
- Use Topics, Keywords, and Search tabs.
- Key resources: Download ToolBook, Learning Resource Center (LRC), Mini Lessons, LiveXtensions.
- Latest release is 11.5 + Patch 4 (recommended after any reinstall).

## License Activation (Critical Post-EOL Issue)

From Activation.html:

- Activation started with 9.5. License Key + real-time check against SumTotal server (needs internet). Trial mode available offline temporarily.
- One license = primary + secondary (home/laptop) for same user.
- Deactivate from Help → License Activation to move to new machine (requires internet).
- Post-EOL: Activation servers offline. **No workaround. No new activations possible.** Existing activations persist on the original machines.
- Manual activation process existed (Activation ID + License Key exchanged offline with support) but is now irrelevant.
- Common historical issues: grayed-out key entry (no internet/proxy), invalid key, product activation failed (version mismatch, cancelled license, Windows 10 quirks), deactivation failures without connectivity.
- Proxy support: server:port format.

Related: 64-bit Windows support (9.0–11.5 yes as 32-bit app; pre-9.0 no due to 16-bit components).

## Downloads and Patches

- ToolBook 11.5 installer available via the KB (TB115Download.html / downloadtoolbook.html). Does **not** include patches. Requires admin + internet for activation (now impossible for new installs).
- **Patch 4** (4 Aug 2015) for 11.5: supersedes prior patches. Fixes include:
  - Web publishing errors ("Not an object: <target>", Popup Media Frame property errors)
  - IE11 compatibility
  - Universal Media Player Time Markers saving
  - Bookmarking checkbox grayed out
  - Chapter Title length (64 → 255)
  - False "SCORE Actions Editor logic" in DHTML log
  - About dialog / Startup screen shows patch level + Check for Update
  - Microsoft Edge handling
- Install: close ToolBook, Run as Administrator, no reboot. Verify via Startup screen "ToolBook 11.5 Patch 4".
- Removal: rename install folder + Repair from Programs and Features.
- Other resources historically linked: Neuron, Runtime, LiveXtensions, Repair Kit.

**Author's PDFs (on main toolbook page):**
- OpenScript Reference Manual (2003)
- ToolBook Catalog Manual (2003)
- Actions Editor Cheat Sheet (2005, updated 2013)
- Actions Editor Programming Cheat Sheet (2005, updated 2013)

## Compatibility and Browser / OS Notes

Quick links cover:
- Windows 8 / 10 / 64-bit
- Chrome 80+ lesson exit problems
- Flash EOL implications
- Windows Media Player plugin issues in Firefox/Chrome
- IE11 missing objects / Creators Update / compatibility
- Edge support
- Chrome Java plug-in errors
- AICC/SCORM versions supported
- DHTML considerations for mobile
- Script Editor "Not Enough Memory" error
- Mixed content HTTPS warnings (suppress checkbox in Publish to Web)

WhatsNew115 highlights for 11.5: simplified Publish to Web, better error logging, larger Resource Manager with preview, expanded Clipart, Delete Pages tool, Character Map, right-click menu improvements, Drag & Drop property clarifications, LMS exit confirmation, Display Book Information utility, voice recording summary, Resource Lookup, mixed content suppress, copy/paste bitmap with text, dropped FF2/IE6 support.

Earlier (9.5): PowerPoint import add-in, XML open support, iPhone/iPod touch styles + publish option.

## File Corruption

From corruption.html:

**Symptoms:** Reproducible crash ("stopped responding") or "The last save was interrupted. This book may be corrupted."

**Avoidance:**
- Never save after a crash.
- Prefer Save As to new names; keep archives (Project1.tbk, Project2.tbk...).
- Enable View | Options | Backup.

**Recovery:**
1. **Repair Kit utility** (best): copies objects/pages/backgrounds/resources into a new book, stripping many forms of corruption.
2. Copy/paste objects page-by-page into a blank book (two instances).
3. Insert → Pages... from the damaged book (can select ranges to skip bad pages; option for backgrounds).

## Publishing, LMS, and Debug

- Debug Mode for DHTML: checkbox in Publish to Web ("Show Debug Information in Browser" / "Display Diagnostic Information"). Shows AICC/SCORM traffic, HTTP Post actions, etc. Useful for LMS data problems. SMTP email logs appear in Java console.
- SCORM/AICC support documented.
- Mobile: limited / special styles; newer Windows Phone not officially supported; iPhone support added earlier.

## Mini Lessons, LRC, LiveXtensions

- **Mini Lessons:** Task-oriented guides also present in the Help system (Contents tab).
- **Learning Resource Center (LRC):** ToolBook Intro (Flash demo), User Guide (~341 pp PDF), Getting Started guide, Learning and Mastering ToolBook CD (30+ hours), Help system (F1), Guides/Tutorials on Startup screen, Release Notes, DHTML Export Considerations.
- **LiveXtensions:** Internet-hosted utilities (or local). Categories: subscription-only LiveXtensions, free Devex tools, user-imported tools. Launched via Tools | LiveXtensions. Third parties can create with OpenScript.

## Other Notable Articles Observed

- Drag Object Question Object (mini-lesson style: use Hotspots as targets).
- Prevent next button until question answered (hide/disable/cover with transparent rectangle + On Load Page action).
- Various media player crashes (e.g., WMP.DLL on page navigation from On Media Complete — not recommended).
- MSXML4 required (MSXML6 does not replace it).
- Bounds vs Vertices discussions appear in related literature (Denny contributions to ToolBook Companion).

## Relevance to Reverse-Engineering / Preservation Work

- Confirms 11.5 is the terminal authoring version; earlier (including ToolBook II 8.x / 8.1) used 16-bit components and different binary layout.
- TBX / Save to XML path (mentioned in project correspondence with Denny) is the modern export; binary .tbk remains proprietary.
- Activation and support end date align with known EOL.
- Repair Kit and corruption recovery techniques may be useful if analyzing damaged specimens.
- OpenScript and Catalog references in the hosted PDFs are high-value primary sources for the language and object model.

## Site Structure Notes

- Main KB: index with quick links + 11.5-specific topics.
- Tabs implied for Topics / Keywords / Search (not fully enumerated in static fetch).
- Individual articles often end with KEYWORDS and related topics.
- Some content still references SumTotal support paths that no longer exist.
- Mirror / alternate host noted in searches: toolbook.dennydedmore.com in some links.

## Recommended Next Steps for Local Archive

1. Mirror key HTML articles and the four PDFs.
2. Cross-reference with existing tbsme/ correspondence and TBX export notes.
3. Extract OpenScript examples and Catalog object descriptions from the manuals for the runtime/decoder work.
4. Note that full Topics/Keywords index may require interactive browsing or additional crawling.

---
*Compiled 2026-10-19 from public pages on dennydedmore.com. For integration into TBWorldview, place under a dedicated section (e.g., Sources/ or KnowledgeBase/) after confirmation, as TBWorldview is a versioned GitHub repository.*
