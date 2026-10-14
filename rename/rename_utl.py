# Rename the TB80UTL functions we have pinned down.
# Run from Ghidra Script Manager against the TB80UTL project.

#@category ToolBook
#@menupath ToolBook.Rename UTL functions

from ghidra.program.model.symbol import SourceType

RENAMES = [
    # Memory
    ("FUN_1000_093b", "UtlAlloc"),
    ("FUN_1018_1472", "UtlLock"),
    ("FUN_10b8_0eac", "UtlAlloc2"),
    ("FUN_10c0_028c", "UtlLock2"),
    # String
    ("FUN_1008_0504", "UtlStrCpy"),
    ("FUN_10b8_0000", "UtlStrLen"),
    ("FUN_10c8_001e", "UtlStrCat"),
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
