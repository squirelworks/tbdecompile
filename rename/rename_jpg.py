# Rename the TB80JPG functions we have pinned down.
# Run from Ghidra Script Manager against the TB80JPG project.

#@category ToolBook
#@menupath ToolBook.Rename JPG functions

from ghidra.program.model.symbol import SourceType

RENAMES = [
    # Memory
    ("FUN_1008_c9ca", "JpgAlloc"),
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
