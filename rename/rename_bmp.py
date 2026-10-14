# Rename the TB80BMP functions we have pinned down.
# Run from Ghidra Script Manager against the TB80BMP project.

#@category ToolBook
#@menupath ToolBook.Rename BMP functions

from ghidra.program.model.symbol import SourceType

RENAMES = [
    # DIB creation
    ("FUN_1078_05c2", "CreateDibBitmap"),
    ("FUN_1090_0558", "CreateDibBitmapAlt"),
    ("FUN_1098_0874", "CreateDibBitmapAlt2"),
    ("FUN_10a0_16ee", "CreateDibBitmapAlt3"),
    # Blit
    ("FUN_1048_0116", "BitBltBmp"),
    ("FUN_1048_1250", "BitBltBmp2"),
    ("FUN_1048_2c5e", "BitBltBmp3"),
    ("FUN_1080_0194", "BitBltBmp4"),
    # DC / palette
    ("FUN_1010_18a4", "SelectPaletteBmp"),
    ("FUN_1030_03e4", "GetDcBmp"),
    ("FUN_1080_0548", "SelectPaletteBmp2"),

    # Compression
    ("FUN_1000_0031", "Lz77Expand"),
    ("FUN_1000_0162", "Lz77ExpandCaller"),
    ("FUN_1000_0752", "Lz77ExpandCaller2"),
]

println("program: %s" % currentProgram.getName())
renamed = 0
for old, new in RENAMES:
    hits = getGlobalFunctions(old)
    if hits is None or len(hits) == 0:
        println("NOT FOUND: %s" % old)
        continue
    for func in hits:
        func.setName(new, SourceType.USER_DEFINED)
        println("renamed %s -> %s at %s" % (old, new, func.getEntryPoint()))
        renamed += 1
println("done, renamed %d" % renamed)
