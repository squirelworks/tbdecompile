
# Rename the TB80RTM book-open and page-paint functions.
# Run from Ghidra Script Manager against the TB80RTM project.

#@category ToolBook
#@menupath ToolBook.Rename RTM book functions

from ghidra.program.model.symbol import SourceType

RENAMES = [
    # Page paint
    ("FUN_1398_05c6", "PaintPageRect"),
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
