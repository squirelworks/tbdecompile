# Rename the TB80NET functions we have pinned down.
# Run from Ghidra Script Manager against the TB80NET project.

#@category ToolBook
#@menupath ToolBook.Rename NET functions

from ghidra.program.model.symbol import SourceType

RENAMES = [
    # Message / window
    ("FUN_1038_01b4", "NetSendMessage"),
    ("FUN_1038_0484", "NetSendMessage2"),
    ("FUN_1040_0000", "NetSendMessage3"),
    ("FUN_1008_17c8", "NetCreateWindow"),
    # Memory / string
    ("FUN_1008_0862", "NetAlloc"),
    ("FUN_1008_136c", "NetAlloc2"),
    ("FUN_1020_0410", "NetStrCpy"),
    ("FUN_1020_0a10", "NetStrCpy2"),
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
