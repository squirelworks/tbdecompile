# tbwp0030 — reference manual, 16 October 2026

`build.py` typesets `bundle/`. Do not hand-edit a PDF.

Front matter is four files: `cover.pdf`, `toc.pdf`, `preface.pdf`, `foreword.pdf`. The table of contents is generated from the record's chapter titles and from the page counts of PDFs that already exist. Reprint it without the contents:

```
python3 build.py front
```

The contents file is the record, copied whole, and does not include the preface. Appendices are A through K. Appendix K is Ghidra. Page counts are in `bundle/MANIFEST.md` and `TBdecompile/manual/20261016/README.md`.

When this sheet and `TBdecompile/record/` disagree, the record wins. 
