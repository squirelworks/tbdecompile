# Rename the TB80MM functions we have pinned down.
# Run from Ghidra Script Manager against the TB80MM project.

#@category ToolBook
#@menupath ToolBook.Rename MM functions

from ghidra.program.model.symbol import SourceType

RENAMES = [
    # Message / window
    ("FUN_1070_03f4", "MmSendMessage"),
    ("FUN_1088_0200", "MmSendMessage2"),
    ("FUN_1088_0642", "MmSendMessage3"),
    ("FUN_1088_09f0", "MmCreateWindow"),
    # Memory / string
    ("FUN_1048_00d0", "MmAlloc"),
    ("FUN_1098_006a", "MmAllocStr"),
    ("FUN_1098_0134", "MmStrCpy"),
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
