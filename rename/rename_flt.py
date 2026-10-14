# Rename the TB80FLT functions we have pinned down.
# Run from Ghidra Script Manager against the TB80FLT project.

#@category ToolBook
#@menupath ToolBook.Rename FLT functions

from ghidra.program.model.symbol import SourceType

RENAMES = [
    # Blit
    ("FUN_1028_14be", "FltBitBlt"),
    ("FUN_1040_071a", "FltBitBlt2"),
    # Message
    ("FUN_1028_0390", "FltSendMessage"),
    ("FUN_1028_2316", "FltSendMessage2"),
    ("FUN_1028_26ac", "FltSendMessage3"),
    # Memory / string
    ("FUN_1010_0e98", "FltAlloc"),
    ("FUN_1010_20b6", "FltAlloc2"),
    ("FUN_1000_093b", "FltStrCpy"),
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
