# Mass Save As EXE utility

OpenScript utility that walks a folder of .tbk files and calls the documented `save as EXE` command on each.

The save line is isolated:

```openscript
save as EXE destPath, true
```

When Denny supplies the correct XML export command, replace that line and re-run.

File: `mass_save_as_exe.script`

Notes:
- Uses `askFileName` for source and destination folders.
- Relies on a DOS `dir` helper for the file list (ToolBook has no native directory iterator in all versions).
- Skips books that fail to open.
- Closes each book after the save.
- No error recovery beyond the skip.
