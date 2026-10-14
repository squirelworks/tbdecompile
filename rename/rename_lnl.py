# Rename the TB80LNL functions we have pinned down.
# Run from Ghidra Script Manager against the TB80LNL project.

#@category ToolBook
#@menupath ToolBook.Rename LNL functions

from ghidra.program.model.symbol import SourceType

RENAMES = [
    # Memory
    ("FUN_1018_04a6", "LnlAlloc"),
    ("FUN_1050_043a", "LnlLock"),
    ("FUN_1070_203e", "LnlAlloc2"),
    ("FUN_10d8_097e", "LnlLock2"),
    # String
    ("FUN_1040_344c", "LnlStrCpy"),
    ("FUN_1040_40f0", "LnlStrLen"),
    ("FUN_1090_0130", "LnlStrCat"),
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
