# Rename the TB80CMP functions we have pinned down.
# Run from Ghidra Script Manager against the TB80CMP project.

#@category ToolBook
#@menupath ToolBook.Rename CMP functions

from ghidra.program.model.symbol import SourceType

RENAMES = [
    # Resource
    ("FUN_1010_0ee6", "LoadCompilerResource"),
    ("FUN_1010_1390", "LockCompilerResource"),
    ("FUN_1038_0dea", "LockCompilerResource2"),
    ("FUN_1040_0970", "ExpandTextCore"),
    # String
    ("FUN_1010_0070", "CompilerStrLen"),
    ("FUN_1010_1774", "CompilerStrCpy"),
    ("FUN_1010_1a28", "CompilerStrCat"),
    ("FUN_1038_06f8", "CompilerStrHelper"),
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
