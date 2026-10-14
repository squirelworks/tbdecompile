# Rename the TB80RTM functions we have pinned down.
# Run from Ghidra Script Manager against the TB80RTM project.

#@category ToolBook
#@menupath ToolBook.Rename RTM functions

from ghidra.program.model.symbol import SourceType

RENAMES = [
    # Paint
    ("FUN_10e0_0050", "PaintRectangle"),
    ("FUN_1398_05c6", "PaintRectangleAlt"),
    # Blit
    ("FUN_1070_0b32", "BitBltHelper"),
    ("FUN_10d0_2d4e", "BitBltHelper2"),
    ("FUN_10d0_2fa0", "BitBltHelper3"),
    ("FUN_10e0_0dea", "BitBltHelper4"),
    ("FUN_1130_32ce", "BitBltHelper5"),
    # Message
    ("FUN_1010_1a0a", "SendMessageHelper"),
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
