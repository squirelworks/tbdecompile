# Rename the TB80RCR functions we have pinned down.
# Run from Ghidra Script Manager against the TB80RCR project.

#@category ToolBook
#@menupath ToolBook.Rename RCR functions

from ghidra.program.model.symbol import SourceType

RENAMES = [
    # Blit
    ("FUN_1008_158c", "RcrBitBlt"),
    ("FUN_1008_164c", "RcrBitBlt2"),
    ("FUN_1008_170e", "RcrBitBlt3"),
    # Message
    ("FUN_1008_077a", "RcrSendMessage"),
    ("FUN_1008_0e94", "RcrSendMessage2"),
    ("FUN_1008_11aa", "RcrSendMessage3"),
    # Memory / string
    ("FUN_1008_08e2", "RcrAlloc"),
    ("FUN_1008_2190", "RcrAlloc2"),
    ("FUN_1008_aa62", "RcrStrCpy"),
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
